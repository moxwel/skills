# Workflow and verification

Covers planning, delegating, verifying, audits and house rules for working on a project.

## Rules

1. **Big change** (new feature, multi-file refactor, new convention): get a short plan approved first. Small fixes: just do them.
2. **Back up `src/` to the scratchpad** before a large refactor or before applying audit fixes.
3. **Build foundations first** (components, then `tsc`), then features and pages.
4. **Verify cheapest first** (Details) before saying "done". If the user says they verify manually, skip headless runs but still run `tsc` and the build.
5. **Record new project conventions in the project `CLAUDE.md`/`AGENTS.md`,** never in this skill.
6. **Talk to the user in their language.** Audit reports are always in English.
7. **Git follows the base skill** (`git-conventions.md`): explicit writes only, Conventional Commits, one commit per topic.
8. **Before building or restyling a UI, read the project's design direction** (`DESIGN.md`, or the visual language in the project `CLAUDE.md`/`AGENTS.md`). With none, the defaults in styling.md are the direction. Say it in one line before the first edit: `Reading this as: <page kind> for <audience>, <visual language>, ENERGY n / RHYTHM n / MOTION n.` (Details).
9. **Kill processes only by a verified PID** (`/proc/<pid>/cmdline`), never with `pkill -f`. Temporary files go in the session scratchpad.

## Details

- **Dials** (1 calm, 2 balanced, 3 bold): ENERGY is how hard the design says hello, RHYTHM how much sections change from each other (1 uniform, 3 varied), MOTION how much moves (1 hover states only, 3 choreographed). The house defaults are ENERGY 1 / RHYTHM 1 / MOTION 1. A project that wants more says so in its `CLAUDE.md`/`AGENTS.md` or `DESIGN.md`, and the output must match the dials it declared.
- **The plan covers:** why, what changes and what doesn't, a file-by-file table, and verification. Feedback given during planning is binding.
- **"Why does X happen?":** explain the likely cause first, and fix only if asked or if the fix is small and obvious.
- **Delegating:** a wide mechanical sweep can go to a subagent (if the agent supports them) with a numbered rule list, a list of what not to touch, and "run tsc, don't build or deploy, no git writes, report every changed file". Review a sample yourself.
- **Verification ladder:**
  1. `npx tsc --noEmit` (after renaming routes, `npx next typegen` first).
  2. `node --test src/lib/validation/validate.test.ts`.
  3. `python3 <skill>/scripts/checkImports.py src` prints nothing.
  4. Build: `docker compose up -d --build <service>` when the project runs in a container, otherwise `npx next build`.
  5. Click through every interactive element (button, link, form, tab, dialog, toggle) once, in each theme and at the mobile width, with headless Playwright or by hand, and check the console. Report one line per element (`Delete item -> opens the confirm dialog`), and say if you could not run it and checked the code instead. A pass without that list is not a pass. Playwright runs against the container IP (`docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}} {{end}}' <container>`) or against `next start`. Run Playwright from a scratchpad script (never as a project dependency), and read credentials from `.env` at runtime without printing them. For refactors that shouldn't change visuals, compare every element's box before and after at 1280 and 390 px.
  6. The user's visual review is final. Say what you couldn't check.
- **Audits** ("does it follow the standard?") and "find and fix inconsistencies":
  1. Read the project `CLAUDE.md`/`AGENTS.md`. Every convention it declares is a deviation to list separately, not a finding.
  2. Launch read-only general-purpose subagents in parallel (if the agent has none, review the areas one by one yourself), one per area: structure, styling, semantic HTML, code style, components, security, database, stack and dependencies (Docker only if asked). Each reads its reference file and returns findings as rule, `path:line`, problem, fix and severity. Meanwhile, run verification ladder steps 1-3 (no build or deploy) and every reference's checklist `grep`s yourself.
  3. Verify each finding by opening the code. Drop false positives and duplicates.
  4. Report in chat: a count table by area, then IDs `A1…` with severity (High: security, data, build; Medium: structure, semantics, a11y, components; Low: styling, format, names, docs), where, problem and fix. Stop there: the user picks the IDs to apply.
  5. Applying: ask about ambiguous fixes, back up, apply, and re-run the analysis on the touched areas until a round comes back clean. Then build and summarize.

## Checklist

- [ ] Verification ladder run as far as the change requires; what couldn't be checked is said.
- [ ] New project conventions recorded in the project `CLAUDE.md`/`AGENTS.md`.
- [ ] Git rules of the base skill followed.
