---
name: moxwel-code-style
description: Use this skill whenever writing, changing, refactoring, reviewing or auditing code in any language or project for moxwel (TypeScript, JavaScript, Python, Bash, CSS and others), even when the user never mentions style and only says things like "add a function that does X", "write a script for Y", "clean up this file", "rename this", "add comments/docs", "review this code", "write a README", "document this in a .md" or "does this follow my conventions?". Covers moxwel's code style, language of code and comments, file headers, doc comments, naming, booleans, conditions, control flow, line length, imports, Markdown documentation the user asks for (READMEs, docs) and git conventions (explicit repo creation, commits and pushes, Conventional Commits messages, one commit per topic). It is the base layer, a stack-specific skill or the project CLAUDE.md/AGENTS.md adds to it. Do not use for other prose, agent files (skills, CLAUDE.md/AGENTS.md, memory, plans), configuration-only edits or questions that write no code.
---

# moxwel's code style

**The references are the standard. This file states no coding rules: it routes you to the references that hold them.** Each style reference (all but links.md) opens with its **Rules**, followed by Details (binding too), and Gotchas and a Checklist where present: read the whole file. A convention declared in the project `CLAUDE.md`/`AGENTS.md` overrides this skill and its references; otherwise, if anything here seems to disagree with a reference, the reference wins.

## Before acting

1. Read the project `CLAUDE.md`/`AGENTS.md`. A convention it declares (another comment language, another line width) is a deliberate deviation, not a mistake to fix. A stack-specific skill in use adds rules on top of these.
2. **Read in full the references for your task** (table below), every time, before writing, changing or reviewing code. Don't rely on memory of an earlier session: several rules are non-obvious and only the references state them.

| Task | Read |
|---|---|
| Any code change or review | [comments-and-docs.md](references/comments-and-docs.md), [naming.md](references/naming.md), [readability.md](references/readability.md) |
| Writing or changing Markdown documentation the user asked for (README, docs), not agent files | [markdown.md](references/markdown.md) |
| Creating a repository, committing, pushing, writing a commit message or splitting changes into commits | [git-conventions.md](references/git-conventions.md) |
| Style audit ("does it follow my conventions?") | all references |

When a doc tag or language convention is in doubt, check [links.md](references/links.md) (official docs) rather than memory.

## Always

- Edit this skill only when the user explicitly asks to change the skill. Project conventions go to the project `CLAUDE.md`/`AGENTS.md`.
- New code matches these rules; existing code is changed only where the task touches it, unless the user asks for a sweep.
- A style audit reports findings (rule, `path:line`, problem, fix) and applies nothing until the user picks which ones.
- Before saying "done", go through the Checklist of every reference you read.

## Why the style looks like this

- Code anyone understands on first read, with one consistent shape in every file and every language.
- Names and comments carry the intent, so a reader never has to reconstruct *why*.
- The smallest code that fully solves the request; a shortcut is fine when it says so.

## Templates

[assets/](assets/) holds complete files in the placeholder `items` domain, each following every rule. Copy their shape and rename them.

- `module.ts`: TypeScript module (header, imports, constants, doc comments, named conditions).
- `module.py`: the same in Python (docstrings, `snake_case`).
- `script.sh`: a Bash script (header with usage, flags, documented functions).

[scripts/check_style.py](scripts/check_style.py) checks line width, ASCII comments and file headers, plus typographic symbols and emojis in documentation Markdown (`python3 scripts/check_style.py <folder>`, prints nothing when clean).
