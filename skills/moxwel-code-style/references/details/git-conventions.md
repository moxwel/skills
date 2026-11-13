# Git conventions: details

Details and gotchas for the rules in [../git-conventions.md](../git-conventions.md).

## Details

- **Format:**

```
<type>[optional scope][!]: <description>

[optional body]

[optional footer(s)]
```

- **Description:** imperative mood, lowercase after the colon, no trailing period, about 72 characters at most (`fix: handle empty item list`, not `Fixed the bug.`).
- **Body:** only on request. Write it as a dash list, one change per line, each in the same imperative style as the description:

```
feat(auth): add magic link login

- add sendMagicLink action
- add /login/verify route
- remove password field from login form
```

  Footers (`Refs:`, `BREAKING CHANGE:`) and attribution lines the project or tool requires are not a body and stay.
- **Scope:** a noun in parentheses naming the area, only when it adds information (`feat(auth): add magic link login`).
- **Breaking changes:** `!` after the type or scope, or a `BREAKING CHANGE: <description>` footer.
- **Footers:** `Token: value` lines, such as `Refs: #12` or `BREAKING CHANGE: ...`.
- **Standard types:** `feat` (new feature), `fix` (bug fix), `docs`, `style`, `refactor`, `perf`, `test`, `build`, `ci`, `chore`, `revert`. Where the convention's own definition and moxwel's use differ, moxwel's use wins: `docs` is for documentation changes.
- **Custom types:** when no standard type names the change, use a short lowercase noun of the project's own. The type is not defined in the spec, so reuse the ones the project's history already has (`git log --oneline`) before inventing another. Types in use:
  - `docs`: documentation changes.
  - `agents`: changes for AI agents (skills, `CLAUDE.md`/`AGENTS.md`, memory, prompts).
  - `init`: the first commit of a repository (`init: scaffold project`).
  - `release`: version bump and changelog (`release: v1.2.0`).
- **Splitting changes:** stage by topic with `git add <paths>` or `git add -p`, never `git add -A` or `git commit -a` over unrelated changes. Check `git status` and `git diff --staged` before each commit, so nothing unrelated is mixed in. Separate a refactor from the feature or fix that motivated it, formatting from logic, and each independent fix from the others.
- **Minimal diffs:** keep the existing formatting, quotes, import order and line breaks of code you do not change, and leave a comment alone unless the change makes it wrong. Existing lines that break a style rule are not fixed in passing, and functions, components and other blocks are not reordered to look tidier. A needed cleanup of unrelated lines goes in its own commit (`style:` or `refactor:`), never mixed into a feature or fix. Review `git diff` before committing and revert every hunk the task did not need.
- **Order:** commit prerequisites first, so the history reads in the order a reviewer would follow it.
- **Pushing:** `git push` only on request, to the branch the user names or the current one. Never force-push, and never rewrite published history, unless the user asks for it explicitly.

## Gotchas

- A request like "commit the changes" with many unrelated changes still means several commits, one per topic.
- "Commit" does not mean "push": stop after the commit and say what is ready to push.
- An editor or formatter that rewrites a whole file hides the real change: turn off format-on-save for files you only touch, or revert the formatting hunks.
- A message with `and` in the description usually hides two commits.
- Do not amend or reset commits the user made; add a new commit.
- A project `CLAUDE.md`/`AGENTS.md` may add its own types, scopes or attribution lines; they apply on top of these rules.
