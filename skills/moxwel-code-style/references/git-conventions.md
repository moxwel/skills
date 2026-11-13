# Git conventions

Covers how repositories are created, committed and pushed, and how commit messages are written, in any project.

## Rules

1. **Git writes are explicit:** creating a repository (`git init`, `gh repo create`), `add`, `commit`, `push`, `stash`, `branch`, `reset` and a checkout that changes files happen only when the user asks for that operation. Reads are fine. Never as a side effect of another task, and approval for one does not extend to the next (a commit is not a push).
2. **Commit messages follow Conventional Commits 1.0.0:** `<type>[optional scope][!]: <description>`, then an optional body and footers, each separated by a blank line.
3. **The type may be any lowercase word,** not only `feat` and `fix`. Use the standard ones where they fit and invent a type when none does ([details](details/git-conventions.md)).
4. **One commit per topic:** each commit holds one specific, related set of changes. With many changes, split them into small commits; never put everything in a single commit.
5. **No body unless the user explicitly asks for one:** the subject line is the whole message. When a body is asked for, it is a list of dashes, one change per line.
6. **Every commit stands on its own:** the code and its tests, docs or config that the change needs go in the same commit, and the repository builds and passes its checks after each one.
7. **Diffs are minimal, so code reviews stay short and easy to read:** a change touches only the lines the task needs. No reformatting, whitespace, line-ending or reordering changes on lines the task does not change, and no rewording, moving or deleting of comments that are still correct. Existing code that breaks a style rule (alignment, line length, naming and the rest) stays as it is, and code blocks keep their order, unless the user asks for the change or a new order is strictly needed for what is shown on screen.

Details and gotchas, binding too: [details/git-conventions.md](details/git-conventions.md).

## Checklist

- [ ] Nothing was initialised, committed or pushed without the user asking.
- [ ] No body was written unless the user asked for one, and a requested body is a dash list.
- [ ] Every message is `type[(scope)][!]: description`, imperative, lowercase, no period.
- [ ] The type is a standard one or one already used in the project's history.
- [ ] Each commit holds one topic; unrelated changes are in separate commits.
- [ ] Each commit includes what it needs (tests, docs, config) and leaves the repository working.
- [ ] The diff has no unrelated line, whitespace or comment changes.
- [ ] No existing style violation was fixed and no block was moved without the user asking (or, for the order, a visual need).
- [ ] `git diff --staged` was checked before each commit.
