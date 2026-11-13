# Delegating

Covers what a React audit or sweep hands to subagents: the areas, the references of each one and what to skip. The rules and the brief templates are the base skill's `delegating.md`; this file only adds what a Next.js project needs.

## Rules

1. **The base skill's `delegating.md` applies in full:** delegate only over more than 5 files, use its auditor and sweeper briefs word for word, every placeholder filled.
2. **One auditor per area of the table below, all in parallel.** Each gets only the references of its row, as absolute paths.
3. **Skip what is not the project's own code:** `node_modules`, `.next`, `out`, build output, generated files (`next-env.d.ts`, generated types) and anything the project `CLAUDE.md`/`AGENTS.md` marks as vendored.
4. **A sweeper's check** is `npx tsc --noEmit`, plus `python3 <react>/scripts/checkImports.py src` when the sweep touches imports. No build, no deploy.
5. **When the base skill is not installed,** `<base>` is the scratchpad copy that SKILL.md step 2 makes, with `references/` and `references/details/` in place, and the brief passes those local paths: a subagent may have no web access, and the auditor follows the `details/` links relative to each reference.

## Details

### Audit areas

`<react>` is this skill's folder and `<base>` the base `moxwel-code-style` skill's folder (the folder of each `SKILL.md`); the brief takes the paths absolute.

| Area | References | Include when |
|---|---|---|
| Structure | `<react>/references/project-structure.md` | always |
| Styling | `<react>/references/styling.md` | always |
| Semantic HTML | `<react>/references/semantic-html.md` | always |
| Components | `<react>/references/components.md` | always |
| Security | `<react>/references/security-management.md` | always |
| Database | `<react>/references/database.md` | the project has `lib/db` |
| Metadata | `<react>/references/social-metadata.md` | the project has public pages |
| Stack and dependencies | `<react>/references/stack-and-setup.md` | always; Docker only if the user asks |
| Code style | `<react>/references/code-style.md`, `<react>/references/naming.md`, `<base>/references/comments-and-docs.md`, `<base>/references/copy.md`, `<base>/references/naming.md`, `<base>/references/readability.md`, `<base>/references/robustness.md` and the four `<base>/references/details/` files | always |

## Checklist

- [ ] The base skill's `delegating.md` checklist passes.
- [ ] One auditor per area that applies, each with only its row's references as absolute paths.
- [ ] The skip list is in every brief.
- [ ] Without the base skill installed, its references and `details/` were saved to the scratchpad in their folder layout before passing them.
