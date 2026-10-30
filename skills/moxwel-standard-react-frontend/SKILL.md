---
name: moxwel-standard-react-frontend
description: Use this skill when building, changing, styling, reviewing or auditing a web frontend that follows moxwel's standard (Next.js App Router, React 19, Base UI, Tailwind v4 for layout + plain CSS for looks, database behind lib/db, Docker), or when starting a new web app with no stack chosen yet. Applies even when the user never names the stack and only says things like "add a page", "make a form for X", "fix this layout on mobile", "add login", "show this data in a table", "add a delete button" or "does the project follow the standard?". Covers where files go, styling, semantic HTML, forms, page metadata and Open Graph link previews, server-action security and database queries. Do not use for frontends on another stack (Vue, Angular, a plain Vite SPA) unless the user wants to move them to this standard.
---

# moxwel's standard for React frontends

**The references are the standard. This file states no coding rules: it routes you to the references that hold them.** Each reference opens with its **Rules**, followed by Details (binding too), and Gotchas and a Checklist where present: read the whole file. If anything here seems to disagree with a reference, the reference wins.

## Before acting

1. Read the project `CLAUDE.md`/`AGENTS.md`. A convention it declares is a deliberate deviation and wins over this skill.
2. **Read in full the references for your task** (table below), every time, before writing, changing or reviewing code. Don't rely on memory of an earlier session: the standard has many non-obvious rules and gotchas that only the references state.
3. If the repo ships `node_modules/next/dist/docs/`, read the relevant Next.js guide too.

| Task | Read |
|---|---|
| Any code change or review | [workflow-and-verification.md](references/workflow-and-verification.md), [code-style.md](references/code-style.md), [naming.md](references/naming.md) |
| UI: component, feature, page, layout, styling, markup | + [styling.md](references/styling.md), [semantic-html.md](references/semantic-html.md), [components.md](references/components.md) |
| New file, moving or splitting code | + [project-structure.md](references/project-structure.md) |
| Page, server action, route handler, auth, uploads, env | + [security-management.md](references/security-management.md) |
| Page metadata, Open Graph, link previews, video or image embeds | + [social-metadata.md](references/social-metadata.md) |
| Any data access or schema | + [database.md](references/database.md), [security-management.md](references/security-management.md) |
| New project, dependencies, config, Docker, deploy | + [stack-and-setup.md](references/stack-and-setup.md), [security-management.md](references/security-management.md) |
| Audit or "find and fix inconsistencies" | all references |

When an API is in doubt, check [links.md](references/links.md) (official docs) rather than memory.

## Always

- Edit this skill only when the user explicitly asks to change the skill. Project conventions go to the project `CLAUDE.md`/`AGENTS.md`.
- No git writes unless the user explicitly asks.
- Before saying "done", go through the Checklist of every reference you read.

## Why the standard looks like this

- Code anyone understands on first read, with one consistent shape in every file.
- The smallest thing that fully solves the request: platform and Node built-ins first, no abstractions or dependencies "for later".
- Minimal never means insecure.
- A DOM that reads like a document, layout and looks kept apart, and nothing animated or added "just in case".

## Templates

[assets/](assets/) holds complete files in the placeholder `items`/`Badge` domain. Copy their shape, rename them, and create any imported module they don't provide.

- Global CSS and helpers: `globals.css`, `cn.ts`, `useFormAction.ts`.
- Components: `component.tsx`/`.css` (a `ui/` piece), `feature.tsx`/`.css` (a client feature with form, list and confirm dialog).
- Server side: `page.tsx` (server page with auth), `action.ts` (server action), `dbTable.ts` (a `lib/db` table with soft delete), `requireUser.ts`.

[scripts/checkImports.py](scripts/checkImports.py) checks import order (`--fix` reorders).
