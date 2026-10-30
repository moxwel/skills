# moxwel's skills

[Agent Skills](https://agentskills.io) that teach an AI coding agent moxwel's conventions. They work with Claude Code, Codex, Cursor, Gemini CLI, GitHub Copilot and any other agent that reads `SKILL.md`.

| Skill | What it covers |
|---|---|
| [`moxwel-code-style`](skills/moxwel-code-style) | Language-agnostic code style: language of code and comments, file headers, doc comments, naming, booleans, conditions, control flow, line length, imports, Markdown documentation, git conventions and copy. |
| [`moxwel-standard-react-frontend`](skills/moxwel-standard-react-frontend) | Web frontends on Next.js App Router, React 19, Base UI, Tailwind v4 for layout + plain CSS for looks, a database behind `lib/db`, and Docker. |

`moxwel-code-style` is the base layer and `moxwel-standard-react-frontend` builds on it, so install both for frontend work.

## Install

### Claude Code

```
/plugin marketplace add moxwel/skills
/plugin install moxwel-code-style@moxwel-skills
/plugin install moxwel-standard-react-frontend@moxwel-skills
```

### Any agent

With the [`skills`](https://github.com/vercel-labs/skills) CLI, which asks which skills and agents to install for:

```
npx skills add moxwel/skills
```

Add `-g` to install for your user instead of the current project, `--skill <name>` to pick a skill and `-a <agent>` to pick an agent.

### Manually

Clone the repo and copy (or symlink) a folder from `skills/` into your agent's skills folder, such as `~/.claude/skills/` for Claude Code or `~/.agents/skills/` for Codex.

## Project overrides

A convention declared in a project's `CLAUDE.md` or `AGENTS.md` wins over these skills, so a project can deviate (another comment language, another line width) without editing them.

## License

[MIT](LICENSE)
