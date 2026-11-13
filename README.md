# moxwel's skills

[Agent Skills](https://agentskills.io) that teach an AI coding agent moxwel's conventions. They work with Claude Code, Codex, Cursor, Gemini CLI, GitHub Copilot and any other agent that reads `SKILL.md`.

| Skill | What it covers |
|---|---|
| [`moxwel-code-style`](skills/moxwel-code-style) | Language-agnostic code style: language of code and comments, file headers, doc comments, naming, booleans, conditions, control flow, robustness and error handling, line length, imports, Markdown documentation, git conventions, copy and briefs for delegating audits to subagents. |
| [`moxwel-standard-react-frontend`](skills/moxwel-standard-react-frontend) | Web frontends on Next.js App Router, React 19, Base UI, Tailwind v4 for layout + plain CSS for looks, a database behind `lib/db`, and Docker. |

`moxwel-code-style` is the base layer and `moxwel-standard-react-frontend` builds on it, so install both for frontend work.

In Claude Code, the optional `moxwel-agents` plugin adds two generic agents that both skills delegate to: `moxwel-auditor` (read-only, one per area of an audit) and `moxwel-sweeper` (applies the exact edits of the findings the user picked, on Haiku). Without it, and in other agents, the skills run the same steps themselves.

## Install

### Claude Code

```
/plugin marketplace add moxwel/skills
/plugin install moxwel-code-style@moxwel-skills
/plugin install moxwel-standard-react-frontend@moxwel-skills
/plugin install moxwel-agents@moxwel-skills
```

### Any agent

With the [`skills`](https://github.com/vercel-labs/skills) CLI, which asks which skills and agents to install for:

```
npx skills add moxwel/skills
```

Add `-g` to install for your user instead of the current project, `--skill <name>` to pick a skill and `-a <agent>` to pick an agent.

### From a local clone

Use this when you work on the skills themselves: symlinks point your agent at the clone, so every edit takes effect in the next session without reinstalling anything.

```bash
git clone https://github.com/moxwel/skills.git ~/projects/moxwel-skills
cd ~/projects/moxwel-skills

mkdir -p ~/.claude/skills ~/.claude/agents
ln -s "$PWD/skills/moxwel-code-style" ~/.claude/skills/moxwel-code-style
ln -s "$PWD/skills/moxwel-standard-react-frontend" ~/.claude/skills/moxwel-standard-react-frontend
ln -s "$PWD/agents/moxwel-auditor.md" ~/.claude/agents/moxwel-auditor.md
ln -s "$PWD/agents/moxwel-sweeper.md" ~/.claude/agents/moxwel-sweeper.md
```

The agents are optional and only Claude Code reads them. For another agent, link the skill folders into its own skills folder instead, such as `~/.agents/skills/` for Codex.

Check that the links point at the clone with `ls -l ~/.claude/skills ~/.claude/agents`. Don't also install the plugin or run `npx skills add`, or the agent sees every skill twice.

## Project overrides

A convention declared in a project's `CLAUDE.md` or `AGENTS.md` wins over these skills, so a project can deviate (another comment language, another line width) without editing them.

## License

[MIT](LICENSE)
