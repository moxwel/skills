---
name: moxwel-code-style
description: ALWAYS load this skill before writing or editing code, in any language and any project (TypeScript, JavaScript, Python, Bash, CSS and others), even for a one-line change, a new constant or field, a small function or a new import, and even when the user never mentions style and only says things like "add a function that does X", "add a field", "write a script for Y", "clean up this file", "rename this", "add comments/docs", "review this code", "write a README", "document this in a .md" or "does this follow my conventions?". moxwel's conventions (column alignment, import order, naming, booleans, named conditions, comments and doc comments, file headers, error handling, line length) differ from common defaults and cannot be guessed from the surrounding code, so skipping the skill produces code that has to be redone. Also covers robustness (expected and unexpected errors, catch boundaries, logs, timeouts, retries, rate limits), Markdown documentation the user asks for (READMEs, docs), git conventions (explicit repo creation, commits and pushes, Conventional Commits messages, one commit per topic) and the copy of user-facing strings, code comments and documentation. It is the base layer, a stack-specific skill or the project CLAUDE.md/AGENTS.md adds to it. Do not use for other prose, agent files (skills, CLAUDE.md/AGENTS.md, memory, plans), configuration-only edits or questions that write no code.
---

# moxwel's code style

**The references are the standard. This file states no coding rules: it routes you to the references that hold them.** Each style reference (all but links.md) opens with its **Rules**, followed by Details (binding too), and Gotchas and a Checklist where present: read the whole file. Four references keep the part that only some tasks need (per-language forms, worked examples, gotchas) in `references/details/<file>.md`; it is binding too, and the table below says exactly when to read it. A convention declared in the project `CLAUDE.md`/`AGENTS.md` overrides this skill and its references; otherwise, if anything here seems to disagree with a reference, the reference wins.

## Before acting

1. Read the project `CLAUDE.md`/`AGENTS.md`. A convention it declares (another comment language, another line width) is a deliberate deviation, not a mistake to fix. A stack-specific skill in use adds rules on top of these.
2. **Read in full every file the table lists for your task,** every time, before writing, changing or reviewing code. Go down the table and take every row that matches: the rows add up. Don't rely on memory of an earlier session: several rules are non-obvious and only the references state them.
3. **A `details/` file in a matching row is required reading, not optional.** If you notice while working that a row applies after all (you end up writing a `try`/`catch`, a UI string, a Python file), stop and read its files before you continue.
4. When you cannot tell how a rule looks in code, read the worked examples in that reference's `details/` file instead of guessing.

| Your task includes | Read |
|---|---|
| Any code change or review | [comments-and-docs.md](references/comments-and-docs.md), [copy.md](references/copy.md), [naming.md](references/naming.md), [readability.md](references/readability.md) |
| A file in Python, Bash or CSS | + [details/comments-and-docs.md](references/details/comments-and-docs.md), [details/naming.md](references/details/naming.md), [details/readability.md](references/details/readability.md) |
| Code that handles errors, I/O, network, external input, timeouts or retries | + [robustness.md](references/robustness.md) |
| Writing or changing user-facing text: UI strings, button labels, errors, toasts, empty and loading messages | + [details/copy.md](references/details/copy.md) |
| Writing or changing Markdown documentation the user asked for (README, docs), not agent files | [markdown.md](references/markdown.md), [copy.md](references/copy.md), [details/copy.md](references/details/copy.md) |
| Creating a repository, committing, pushing, writing a commit message or splitting changes into commits | [git-conventions.md](references/git-conventions.md) |
| Style audit ("does it follow my conventions?") | all references and all their `details/` files |
| An audit, or applying picked fixes, over more than 5 files | + [delegating.md](references/delegating.md) |

When a doc tag or language convention is in doubt, check [links.md](references/links.md) (official docs) rather than memory.

## Always

- Edit this skill only when the user explicitly asks to change the skill. Project conventions go to the project `CLAUDE.md`/`AGENTS.md`.
- New code matches these rules. Existing lines that break a rule stay exactly as they are (file header, comments, names, alignment, formatting, order of blocks): change a line only when the task needs that line changed, or when your change makes its comment wrong, unless the user asks for a sweep (git-conventions.md rule 7).
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

[scripts/check_style.py](scripts/check_style.py) checks ASCII comments and file headers, plus typographic symbols and emojis in documentation Markdown (`python3 scripts/check_style.py <folder>`, prints nothing when clean).
