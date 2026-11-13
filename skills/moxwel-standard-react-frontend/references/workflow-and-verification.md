# Workflow and verification

Covers planning, delegating, verifying, audits and house rules for working on a project.

## Rules

1. **Big change** (new feature, multi-file refactor, new convention): get a short plan approved first. Small fixes: just do them.
2. **Back up `src/` to the scratchpad** before a large refactor or before applying audit fixes.
3. **Build foundations first** (components, then `tsc`), then features and pages.
4. **Verify cheapest first** ([details](details/workflow-and-verification.md)) before saying "done". If the user says they verify manually, skip headless runs but still run `tsc` and the build.
5. **Record new project conventions in the project `CLAUDE.md`/`AGENTS.md`,** never in this skill.
6. **Talk to the user in their language.** Audit reports are always in English.
7. **Git follows the base skill** (`git-conventions.md`): explicit writes only, Conventional Commits, one commit per topic.
8. **Before building or restyling a UI, read the project's design direction** (`DESIGN.md`, or the visual language in the project `CLAUDE.md`/`AGENTS.md`). With none, the defaults in styling.md are the direction. Say it in one line before the first edit: `Reading this as: <page kind> for <audience>, <visual language>, ENERGY n / RHYTHM n / MOTION n.` ([details](details/workflow-and-verification.md)).
9. **Kill processes only by a verified PID** (`/proc/<pid>/cmdline`), never with `pkill -f`. Temporary files go in the session scratchpad.

Details and gotchas, binding too: [details/workflow-and-verification.md](details/workflow-and-verification.md).

## Checklist

- [ ] Verification ladder run as far as the change requires; what couldn't be checked is said.
- [ ] New project conventions recorded in the project `CLAUDE.md`/`AGENTS.md`.
- [ ] Git rules of the base skill followed.
