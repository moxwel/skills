# Git conventions

Covers how repositories are created, committed and pushed, and how commit messages are written, in any project.

## Rules

1. **Git writes are explicit:** create a repository (`git init`, `gh repo create`), commit and push only when the user asks. Never as a side effect of another task, and approval for one does not extend to the next (a commit is not a push).
2. **Commit messages follow Conventional Commits 1.0.0:** `<type>[optional scope][!]: <description>`, then an optional body and footers, each separated by a blank line.
3. **The type may be any lowercase word,** not only `feat` and `fix`. Use the standard ones where they fit and invent a type when none does (Details).
4. **One commit per topic:** each commit holds one specific, related set of changes. With many changes, split them into small commits; never put everything in a single commit.
5. **Every commit stands on its own:** the code and its tests, docs or config that the change needs go in the same commit, and the repository builds and passes its checks after each one.

## Details

- **Format:**

```
<type>[optional scope][!]: <description>

[optional body]

[optional footer(s)]
```

- **Description:** imperative mood, lowercase after the colon, no trailing period, about 72 characters at most (`fix: handle empty item list`, not `Fixed the bug.`).
- **Body:** explains what changed and why, not how; wrap it at 72 characters. Skip it when the description says it all.
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
- **Order:** commit prerequisites first, so the history reads in the order a reviewer would follow it.
- **Pushing:** `git push` only on request, to the branch the user names or the current one. Never force-push, and never rewrite published history, unless the user asks for it explicitly.

## Gotchas

- A request like "commit the changes" with many unrelated changes still means several commits, one per topic.
- "Commit" does not mean "push": stop after the commit and say what is ready to push.
- A message with `and` in the description usually hides two commits.
- Do not amend or reset commits the user made; add a new commit.
- A project `CLAUDE.md`/`AGENTS.md` may add its own types, scopes or attribution lines; they apply on top of these rules.

## Checklist

- [ ] Nothing was initialised, committed or pushed without the user asking.
- [ ] Every message is `type[(scope)][!]: description`, imperative, lowercase, no period.
- [ ] The type is a standard one or one already used in the project's history.
- [ ] Each commit holds one topic; unrelated changes are in separate commits.
- [ ] Each commit includes what it needs (tests, docs, config) and leaves the repository working.
- [ ] `git diff --staged` was checked before each commit.
