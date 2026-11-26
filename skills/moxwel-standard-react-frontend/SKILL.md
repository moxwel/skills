---
name: moxwel-standard-react-frontend
description: Use this skill when building, changing, styling, reviewing or auditing a web frontend that follows moxwel's standard (Next.js App Router, React 19, Base UI, Tailwind v4 for layout + plain CSS for looks, database behind lib/db, Docker), or when starting a new web app with no stack chosen yet. Applies even when the user never names the stack and only says things like "add a page", "make a form for X", "fix this layout on mobile", "add login", "show this data in a table", "add a delete button", "add a helper in lib/" or "does the project follow the standard?", and to any file added to such a project, UI or not. Covers where files and constants go, styling, semantic HTML, forms, page metadata and Open Graph link previews, server-action security and database queries. Do not use for frontends on another stack (Vue, Angular, a plain Vite SPA) unless the user wants to move them to this standard.
---

# moxwel's standard for React frontends

**The references are the standard. This file states no coding rules: it routes you to the references that hold them.** Each reference opens with its **Rules**, followed by Details (binding too), and Gotchas and a Checklist where present: read the whole file. If anything here seems to disagree with a reference, the reference wins.

## Before acting

1. Read the project `CLAUDE.md`/`AGENTS.md`. A convention it declares is a deliberate deviation and wins over this skill.
2. **Also load the base `moxwel-code-style` skill and read the files its table lists for your task** (comments, naming, readability, copy, git): its rules apply here and are not repeated. Loading it is not enough. Every row below already links the base files its task needs (the two skills are sibling folders, so the links resolve from this skill's folder); the other rows of the base table (robustness, Markdown, git) still apply when they match. If it is not installed, stop and ask the user to install it (`npx skills add moxwel/skills`). Only if the user declines, or nobody can answer (a headless or scheduled session), read the base references you need from `https://raw.githubusercontent.com/moxwel/skills/main/skills/moxwel-code-style/references/<file>.md`: `comments-and-docs.md`, `copy.md`, `naming.md`, `readability.md`, `robustness.md`, `git-conventions.md`, `delegating.md`. Save them in the session scratchpad under `moxwel-code-style/references/`, and read the linked base files from that folder instead.
3. **Read in full the references for your task** (table below), every time, before writing, changing or reviewing code. If a read is denied or fails, read the file with another tool; never write code without them. Each row is complete: read every file it lists, the base skill's files included, however narrow the task looks (only the order, only a name, a one-line fix), since every rule applies to each line written or moved. When several rows match (a new component is UI and a new file), read the files of every matching row. Don't rely on memory of an earlier session: the standard has many non-obvious rules and gotchas that only the references state.
4. If the repo ships `node_modules/next/dist/docs/`, read the relevant Next.js guide too.

| Task | Read |
|---|---|
| Any code change or review, however small or narrow (a reorder, a rename, a one-line fix). The two `naming.md` are different files: read both | Base: [comments-and-docs.md](../moxwel-code-style/references/comments-and-docs.md), [copy.md](../moxwel-code-style/references/copy.md), [naming.md](../moxwel-code-style/references/naming.md), [readability.md](../moxwel-code-style/references/readability.md). This skill: [workflow-and-verification.md](references/workflow-and-verification.md), [code-style.md](references/code-style.md), [naming.md](references/naming.md) |
| UI: component, feature, page, layout, styling, markup | Base: [comments-and-docs.md](../moxwel-code-style/references/comments-and-docs.md), [copy.md](../moxwel-code-style/references/copy.md), [naming.md](../moxwel-code-style/references/naming.md), [readability.md](../moxwel-code-style/references/readability.md). This skill: [workflow-and-verification.md](references/workflow-and-verification.md), [code-style.md](references/code-style.md), [naming.md](references/naming.md), [project-structure.md](references/project-structure.md), [styling.md](references/styling.md), [semantic-html.md](references/semantic-html.md), [components.md](references/components.md), [user-experience.md](references/user-experience.md) |
| New file (component, page, action, `lib/` module, hook), moving or splitting code | Base: [comments-and-docs.md](../moxwel-code-style/references/comments-and-docs.md), [copy.md](../moxwel-code-style/references/copy.md), [naming.md](../moxwel-code-style/references/naming.md), [readability.md](../moxwel-code-style/references/readability.md). This skill: [workflow-and-verification.md](references/workflow-and-verification.md), [code-style.md](references/code-style.md), [naming.md](references/naming.md), [project-structure.md](references/project-structure.md) |
| Page, server action, route handler, auth, uploads, env | Base: [comments-and-docs.md](../moxwel-code-style/references/comments-and-docs.md), [copy.md](../moxwel-code-style/references/copy.md), [naming.md](../moxwel-code-style/references/naming.md), [readability.md](../moxwel-code-style/references/readability.md). This skill: [workflow-and-verification.md](references/workflow-and-verification.md), [code-style.md](references/code-style.md), [naming.md](references/naming.md), [project-structure.md](references/project-structure.md), [security-management.md](references/security-management.md), [database.md](references/database.md) |
| Page metadata, Open Graph, link previews, video or image embeds | Base: [comments-and-docs.md](../moxwel-code-style/references/comments-and-docs.md), [copy.md](../moxwel-code-style/references/copy.md), [naming.md](../moxwel-code-style/references/naming.md), [readability.md](../moxwel-code-style/references/readability.md). This skill: [workflow-and-verification.md](references/workflow-and-verification.md), [code-style.md](references/code-style.md), [naming.md](references/naming.md), [project-structure.md](references/project-structure.md), [social-metadata.md](references/social-metadata.md) |
| Any data access or schema | Base: [comments-and-docs.md](../moxwel-code-style/references/comments-and-docs.md), [copy.md](../moxwel-code-style/references/copy.md), [naming.md](../moxwel-code-style/references/naming.md), [readability.md](../moxwel-code-style/references/readability.md). This skill: [workflow-and-verification.md](references/workflow-and-verification.md), [code-style.md](references/code-style.md), [naming.md](references/naming.md), [project-structure.md](references/project-structure.md), [database.md](references/database.md), [security-management.md](references/security-management.md) |
| New project, dependencies, config, Docker, deploy | Base: [comments-and-docs.md](../moxwel-code-style/references/comments-and-docs.md), [copy.md](../moxwel-code-style/references/copy.md), [naming.md](../moxwel-code-style/references/naming.md), [readability.md](../moxwel-code-style/references/readability.md). This skill: [workflow-and-verification.md](references/workflow-and-verification.md), [code-style.md](references/code-style.md), [naming.md](references/naming.md), [project-structure.md](references/project-structure.md), [stack-and-setup.md](references/stack-and-setup.md), [security-management.md](references/security-management.md) |
| Audit or "find and fix inconsistencies" | Base: [comments-and-docs.md](../moxwel-code-style/references/comments-and-docs.md), [copy.md](../moxwel-code-style/references/copy.md), [naming.md](../moxwel-code-style/references/naming.md), [readability.md](../moxwel-code-style/references/readability.md). This skill: every file in [references/](references/) |
| Audit, or applying picked fixes, over more than 5 files | Base: [comments-and-docs.md](../moxwel-code-style/references/comments-and-docs.md), [copy.md](../moxwel-code-style/references/copy.md), [naming.md](../moxwel-code-style/references/naming.md), [readability.md](../moxwel-code-style/references/readability.md), [delegating.md](../moxwel-code-style/references/delegating.md). This skill: [workflow-and-verification.md](references/workflow-and-verification.md), [code-style.md](references/code-style.md), [naming.md](references/naming.md), [delegating.md](references/delegating.md) |

When an API is in doubt, check [links.md](references/links.md) (official docs) rather than memory.

## Always

- Edit this skill only when the user explicitly asks to change the skill. Project conventions go to the project `CLAUDE.md`/`AGENTS.md`.
- Git follows the base skill's [git-conventions.md](../moxwel-code-style/references/git-conventions.md).
- Before saying "done", go through the Checklist of every reference you read.

## Why the standard looks like this

- Code anyone understands on first read, with one consistent shape in every file.
- The smallest thing that fully solves the request: platform and Node built-ins first, no abstractions or dependencies "for later".
- Minimal never means insecure.
- A DOM that reads like a document, layout and looks kept apart, and nothing animated or added "just in case".

## Templates

[assets/](assets/) holds complete files in the placeholder `items`/`Badge` domain. Copy their shape, rename them, and create any imported module they don't provide. Their headers, doc comments and inline comments show the form to use when the user asks for documentation; without that request, leave them out.

- Global CSS and helpers: `globals.css`, `cn.ts`, `useFormAction.ts`.
- Components: `component.tsx`/`.css` (a `ui/` piece), `feature.tsx`/`.css` (a client feature with form, list and confirm dialog).
- Server side: `page.tsx` (server page with auth), `action.ts` (server action), `dbTable.ts` (a `lib/db` table with soft delete), `requireUser.ts`.
- Route states: `loading.tsx` (loading fallback) and `error.tsx` (error boundary with a retry).

[scripts/checkImports.py](scripts/checkImports.py) checks import order (`--fix` reorders).
