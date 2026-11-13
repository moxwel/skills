# Delegating

Covers handing part of a style audit, or a sweep of fixes the user already picked, to subagents: when to do it, how to split it and the exact brief each one gets.

## Rules

1. **Delegate only wide work:** an audit or a sweep over more than 5 files. Smaller ones you do yourself.
2. **A subagent knows only its brief.** It does not inherit this skill, the conversation or the project `CLAUDE.md`/`AGENTS.md`. Everything it needs goes in the brief: the rules as absolute paths to the reference files, the target, what to skip and the project conventions quoted word for word.
3. **Use the brief templates below as they are,** with every `<placeholder>` filled. A field with nothing in it says `none`; never drop a field.
4. **Prefer the `moxwel-auditor` and `moxwel-sweeper` agents** (plugin `moxwel-agents`). Without them, give the same brief to a general-purpose subagent: the brief carries the steps and the output format, so it works with either. With no subagents at all, do the areas one at a time yourself.
5. **Audits run one auditor per area, all in parallel** (table below). Sweeps run one sweeper per group of files that do not overlap, so two sweepers never edit the same file.
6. **Check what comes back:** an auditor whose `References read` misses a file you passed is re-run; every finding is verified in the code before it reaches the user; a sweeper's changes are reviewed on a sample of files and its check output read.

## Details

### Audit areas

Paths are relative to this skill's folder (the folder of its `SKILL.md`); the brief takes them absolute.

| Area | References | Include when |
|---|---|---|
| Comments and docs | `references/comments-and-docs.md`, `references/details/comments-and-docs.md` | always |
| Copy | `references/copy.md`, `references/details/copy.md` | always |
| Naming | `references/naming.md`, `references/details/naming.md` | always |
| Readability | `references/readability.md`, `references/details/readability.md` | always |
| Robustness | `references/robustness.md` | the target has error handling, I/O, network or external input |
| Markdown | `references/markdown.md`, `references/copy.md`, `references/details/copy.md` | the target has documentation `.md` files (not agent files) |
| Git | `references/git-conventions.md` | the user asks about commits; the target is then a commit range, read with `git log` |

### Auditor brief

```text
You audit one area of a codebase against written rules. Read-only: do not edit, create or delete files, and run no command that writes (git writes, installs, builds, formatters).

Area: <area>
References (read each one in full before opening any code, plus every details/ file they call "binding too"):
- <absolute path>
Target: <absolute paths of the files or folders to audit>
Skip: <paths that are not the project's own code: dependencies, build output, generated or vendored files>
Project conventions (deliberate deviations: list them under Deviations, never as findings):
- <line quoted from CLAUDE.md/AGENTS.md, or "none">

Steps:
1. Read every reference and its details/ files.
2. Run the grep commands of each reference's Checklist over the target.
3. Open every file of the target the area applies to and compare it with every rule. Only the rules in the references count, not general best practice.
4. Drop anything you cannot point to a line for.

Output, and nothing else:
Area: <area>
References read: <file names>
Files checked: <count>; not opened: <paths, or "none">
Findings
- <reference file> rule <n> | <path>:<line> | <problem> | <fix> | <High|Medium|Low>
Deviations
- <convention> | <path>:<line>
Severity: High for security, data loss or a broken build; Medium for structure, semantics, accessibility and components; Low for styling, format, names and docs. Write "none" under an empty heading.
```

### Sweeper brief

```text
You apply one mechanical change that was already decided. You change nothing else.

Rules to apply (each quoted from its reference):
1. <rule text> (<absolute reference path>, rule <n>)
References (read before the first edit): <absolute paths>
Scope: <absolute paths of the files or folders>
Do not touch: <paths and kinds of lines, or "none">
Project conventions (they win over the rules):
- <line quoted from CLAUDE.md/AGENTS.md, or "none">
Check to run when done: <command>

Constraints: change only the lines the rules require, and every other line stays byte for byte as it was (no reformatting, reordering or comment rewording). No git writes, installs, builds, deploys or pkill. When a spot is ambiguous, skip it and list it; never guess.

Output, and nothing else:
Changed
- <path>: <what changed, one line>
Skipped
- <path>:<line>: <why>
Check
<command>: <output, or "clean">
```

## Gotchas

- A relative path in a brief resolves against the subagent's own working folder, which may not be the skill's. Always absolute.
- Quoting "the project uses tabs" from memory is not quoting: copy the line from the project file.
- An auditor that returns no findings and a short `References read` did not do the work; re-run it.

## Checklist

- [ ] Every placeholder filled, every path absolute and existing, empty fields say `none`.
- [ ] One auditor per area of the table that applies, launched in parallel; sweepers never share a file.
- [ ] `References read` of every auditor matches what was passed.
- [ ] Every finding verified in the code; sweeper changes reviewed on a sample and its check output read.
