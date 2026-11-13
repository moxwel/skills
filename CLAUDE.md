# moxwel's skills

Agent Skills that teach coding agents moxwel's conventions. They ship as a Claude Code plugin marketplace (`.claude-plugin/marketplace.json`) and through `npx skills add moxwel/skills`.

## Layout

- `skills/<name>/SKILL.md` only routes: it says which references to read for each task and holds no rules of its own.
- `references/` holds the rules. Each style reference opens with its Rules, then Details, Gotchas and a Checklist.
- `references/details/` holds the part of a reference that only some tasks need (per-language forms, worked examples). A part moves there only when the SKILL.md table can name a condition for reading it that is known before the work starts; anything a change can hit mid-work stays in the Rules.
- `assets/` holds complete template files that follow every rule.
- `scripts/` holds checkers for the mechanical rules.
- `test/` holds scenarios that run each skill in fresh headless sessions and check what the model read and wrote (see [test/README.md](test/README.md)). Run them after changing a `SKILL.md` description or table, a rule, or what lives in `details/`.

`moxwel-code-style` is the base layer and `moxwel-standard-react-frontend` builds on it.

## Conventions

- Everything is written in English.
- Code follows `moxwel-code-style`. Its [markdown.md](skills/moxwel-code-style/references/markdown.md) applies only to user documentation such as `README.md`, not to skill files or this `CLAUDE.md`.
- A change to a skill keeps its `SKILL.md`, its references, the table in `README.md` and `marketplace.json` in sync.
- Run `python3 skills/moxwel-code-style/scripts/check_style.py .` before finishing. It prints nothing when clean.
- Commits use Conventional Commits with these types:
  - `add(<skill>)`, `refactor(<skill>)` and `delete(<skill>)` for a change to a skill: something added, something existing changed, something removed. `<skill>` is the name of the skill that changed (`refactor(moxwel-code-style): ...`).
  - `docs` or `docs(<skill>)` for documentation, such as `README.md`.
  - `test` for changes under `test/`.
