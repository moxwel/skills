# moxwel's skills

Agent Skills that teach coding agents moxwel's conventions. They ship as a Claude Code plugin marketplace (`.claude-plugin/marketplace.json`) and through `npx skills add moxwel/skills`.

## Layout

- `skills/<name>/SKILL.md` only routes: it says which references to read for each task and holds no rules of its own.
- `references/` holds the rules. Each style reference opens with its Rules, then Details, Gotchas and a Checklist.
- `assets/` holds complete template files that follow every rule.
- `scripts/` holds checkers for the mechanical rules.

`moxwel-code-style` is the base layer and `moxwel-standard-react-frontend` builds on it.

## Conventions

- Everything is written in English.
- Code follows `moxwel-code-style`. Its [markdown.md](skills/moxwel-code-style/references/markdown.md) applies only to user documentation such as `README.md`, not to skill files or this `CLAUDE.md`.
- A change to a skill keeps its `SKILL.md`, its references, the table in `README.md` and `marketplace.json` in sync.
- Run `python3 skills/moxwel-code-style/scripts/check_style.py .` before finishing. It prints nothing when clean.
- Commits use Conventional Commits (`feat:`, `fix:`, `chore:`).
