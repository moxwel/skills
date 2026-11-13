"""
Reads the stream-json log of a headless session: the skills it loaded, the skill files it read and its cost.
"""

import json
import os
from pathlib import Path
import re
import shlex

REACT_SKILL = "moxwel-standard-react-frontend"
# References every code change must read (first row of the SKILL.md table of the base skill).
BASE_REFERENCES = ["comments-and-docs", "copy", "naming", "readability"]
# A skill reference path: group 1 is the skill, 2 is "details/" when present, 3 is the file name.
SKILL_FILE = re.compile(r"moxwel-([a-z-]+)/references/(details/)?([a-z-]+)\.md")
# Separators between the commands of one Bash call.
COMMAND_SEPARATOR = re.compile(r"&&|\|\||;|\n")
SHELL_ASSIGNMENT  = re.compile(r"(\w+)=(\S+)$")


def expanded(word: str, variables: dict[str, str]) -> str:
    """Replaces $NAME and ${NAME} with the values the command set, then with the environment."""
    with_variables = re.sub(r"\$\{?(\w+)\}?", lambda match: variables.get(match.group(1), match.group(0)), word)
    return os.path.expandvars(with_variables)


def resolved_paths(command: str) -> str:
    """Rewrites the paths of a Bash command as absolute ones, following its cd steps and variables.

    Sessions often read the skill as `cd <skill> && cat references/naming.md` or `D=<skill>; cat $D/...`.
    shortcut: handles plain cd, NAME=value and $NAME/${NAME}; a subshell or a loop variable is not followed.
    """
    folder    = "/"
    variables = {}
    resolved  = []
    for step in COMMAND_SEPARATOR.split(command):
        try:
            words = shlex.split(step)
        except ValueError:
            # an unbalanced quote: fall back to plain words
            words = step.split()
        words = [expanded(word, variables) for word in words]
        assignments = [SHELL_ASSIGNMENT.match(word) for word in words]
        variables.update({match.group(1): match.group(2) for match in assignments if match})
        is_cd = words[:1] == ["cd"] and len(words) > 1
        if is_cd:
            folder = os.path.normpath(os.path.join(folder, words[1]))
            continue
        resolved += [os.path.normpath(os.path.join(folder, word)) for word in words]
    return " ".join(resolved)


def log_events(log_path: Path) -> list[dict]:
    events = []
    for line in log_path.read_text(encoding="utf-8", errors="ignore").splitlines():
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            # stderr shares the log, so some lines are plain text
            continue
        if isinstance(event, dict):
            events.append(event)
    return events


def content_blocks(event: dict) -> list[dict]:
    message = event.get("message")
    content = message.get("content") if isinstance(message, dict) else None
    blocks  = content if isinstance(content, list) else []
    return [block for block in blocks if isinstance(block, dict)]


def session_facts(log_path: Path) -> dict:
    """Reads a session log: skills loaded, skill files it read with success and their words, cost, clean end.

    :returns: "references" and "details" hold file names without extension, prefixed "react:" for the React skill.
    """
    facts   = {"skills": [], "references": set(), "details": set(), "words": 0, "cost_usd": 0.0, "is_finished": False}
    targets = {}
    for event in log_events(log_path):
        is_result = event.get("type") == "result"
        if is_result:
            facts["cost_usd"]    = event.get("total_cost_usd") or 0.0
            facts["is_finished"] = not event.get("is_error")
        for block in content_blocks(event):
            arguments      = block.get("input") or {}
            is_tool_call   = block.get("type") == "tool_use"
            is_skill_call  = is_tool_call and block.get("name") == "Skill"
            is_good_result = block.get("type") == "tool_result" and not block.get("is_error")
            if is_skill_call:
                facts["skills"].append(arguments.get("skill"))
            if is_tool_call:
                target = str(arguments.get("file_path") or "") or resolved_paths(str(arguments.get("command") or ""))
                targets[block.get("id")] = target
            if not is_good_result:
                continue
            # a denied or failed read does not count: only results that carry the file content
            for match in SKILL_FILE.finditer(targets.get(block.get("tool_use_id"), "")):
                kind   = "details" if match.group(2) else "references"
                prefix = "react:" if "react" in match.group(1) else ""
                facts[kind].add(prefix + match.group(3))
                facts["words"] += len(json.dumps(block.get("content")).split())
    return facts


def missing_skill_files(scenario: dict, facts: dict) -> list[str]:
    """Lists the skill files the scenario requires that the session never read."""
    references             = BASE_REFERENCES + scenario.get("references", [])
    react_references       = [f"react:{name}" for name in scenario.get("react", [])]
    is_react_skill_missing = "react" in scenario and REACT_SKILL not in facts["skills"]
    missing = [f"details/{name}" for name in scenario["details"] if name not in facts["details"]]
    missing += [name for name in references + react_references if name not in facts["references"]]
    missing += ["React skill not loaded"] if is_react_skill_missing else []
    return missing


def self_check() -> None:
    """Checks resolved_paths on the ways sessions were seen reading the skill files."""
    cases = {
        "cd /s/moxwel-a && cat references/x.md; cd ../moxwel-b/references && cat details/y.md":
            ["moxwel-a/references/x.md", "moxwel-b/references/details/y.md"],
        "D=/s; cat $D/moxwel-a/references/x.md ${D}/moxwel-a/references/details/y.md":
            ["moxwel-a/references/x.md", "moxwel-a/references/details/y.md"],
        "cat /s/moxwel-a/references/x.md": ["moxwel-a/references/x.md"],
    }
    for command, expected in cases.items():
        found_paths = [match.group(0) for match in SKILL_FILE.finditer(resolved_paths(command))]
        assert found_paths == expected, (command, found_paths)
