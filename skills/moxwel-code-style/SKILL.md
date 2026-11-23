---
name: moxwel-code-style
description: ALWAYS load this skill before writing or editing code, in any language and any project (TypeScript, JavaScript, Python, Bash, CSS and others), even for a one-line change, a new constant or field, a small function or a new import, and even when the user never mentions style and only says things like "add a function that does X", "add a field", "write a script for Y", "clean up this file", "rename this", "add comments/docs", "review this code", "write a README", "document this in a .md" or "does this follow my conventions?". moxwel's conventions (column alignment, import order, naming, booleans, named conditions, nesting depth, comments and doc comments, file headers, error handling, line length) differ from common defaults and cannot be guessed from the surrounding code, so skipping the skill produces code that has to be redone. Also covers robustness (expected and unexpected errors, catch boundaries, logs, timeouts, retries, rate limits), Markdown documentation the user asks for (READMEs, docs), git conventions (explicit repo creation, commits and pushes, Conventional Commits messages, one commit per topic) and the copy of user-facing strings, code comments and documentation. It is the base layer, a stack-specific skill or the project CLAUDE.md/AGENTS.md adds to it. Do not use for other prose, agent files (skills, CLAUDE.md/AGENTS.md, memory, plans), configuration-only edits or questions that write no code.
---

# moxwel's code style

**The references are the standard. This file states no coding rules: it routes you to the references that hold them.** Each style reference (all but links.md) opens with its **Rules**, followed by Details (binding too), and Gotchas and a Checklist where present: read the whole file. A convention declared in the project `CLAUDE.md`/`AGENTS.md` overrides this skill and its references; otherwise, if anything here seems to disagree with a reference, the reference wins.

## Before acting

1. Read the project `CLAUDE.md`/`AGENTS.md`. A convention it declares (another comment language, another line width) is a deliberate deviation, not a mistake to fix. A stack-specific skill in use adds rules on top of these.
2. **Read in full every file the table lists for your task,** every time, before writing, changing or reviewing code. Go down the table and take every row that matches: the rows add up. The first row is the minimum for any task that touches code, however narrow it looks (only the order, only a name, a one-line fix): every rule applies to each line written or moved, so the narrowest task still reads all of that row. Don't rely on memory of an earlier session: several rules are non-obvious and only the references state them.
3. If you notice while working that a row applies after all (you end up writing a `try`/`catch` or a commit), stop and read its files before you continue.
4. When you cannot tell how a rule looks in code, read the per-language forms and worked examples in that reference's Details instead of guessing.

| Your task includes | Read |
|---|---|
| Any code change or review, however small or narrow (a reorder, a rename, a one-line fix) | [comments-and-docs.md](references/comments-and-docs.md), [copy.md](references/copy.md), [naming.md](references/naming.md), [readability.md](references/readability.md) |
| Code that handles errors, I/O, network, external input, timeouts or retries | + [robustness.md](references/robustness.md) |
| Writing or changing Markdown documentation the user asked for (README, docs), not agent files | [markdown.md](references/markdown.md), [copy.md](references/copy.md) |
| Creating a repository, committing, pushing, writing a commit message or splitting changes into commits | [git-conventions.md](references/git-conventions.md) |
| Style audit ("does it follow my conventions?") | all references |
| An audit, or applying picked fixes, over more than 5 files | + [delegating.md](references/delegating.md) |

When a doc tag or language convention is in doubt, check [links.md](references/links.md) (official docs) rather than memory.

## Always

- Edit this skill only when the user explicitly asks to change the skill. Project conventions go to the project `CLAUDE.md`/`AGENTS.md`.
- New code matches these rules. Existing lines that break a rule stay exactly as they are (file header, comments, names, alignment, formatting, order of blocks): change a line only when the task needs that line changed, or when your change makes its comment wrong, unless the user asks for a sweep (git-conventions.md rule 7).
- A style audit reports findings (rule, `path:line`, problem, fix) and applies nothing until the user picks which ones.
- Before saying "done", go through the Checklist of every reference you read.

## Why the style looks like this

- Code anyone understands on first read, with one consistent shape in every file and every language.
- Names carry the intent, so a reader never has to reconstruct *why*. Comments are written only when the user asks for them.
- The smallest code that fully solves the request; a shortcut is fine when it says so.

## Templates

[assets/](assets/) holds complete files in the placeholder `items` domain, each following every rule. Copy their shape and rename them. Their headers and doc comments show the form to use when the user asks for documentation; without that request, leave them out.

- `module.ts`: TypeScript module (header, imports, constants, doc comments, named conditions).
- `module.py`: the same in Python (docstrings, `snake_case`).
- `script.sh`: a Bash script (header with usage, flags, documented functions).

[scripts/check_style.py](scripts/check_style.py) checks ASCII comments and nesting deeper than 3 levels in TS/JS, Python and Bash, plus typographic symbols and emojis in documentation Markdown (`python3 scripts/check_style.py <folder>`, prints nothing when clean).
