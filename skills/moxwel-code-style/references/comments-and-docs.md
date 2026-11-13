# Comments and docs

Covers every source file in any language: the language of code and text, file headers, inline comments and doc comments on functions, constants and types.

## Rules

1. **Language:** code, comments, doc comments, user-facing strings, logs and docs are in English. When the project names another language for user-facing strings, comments or docs (an override, see SKILL.md), those use it. Comments stay ASCII (drop accents) and identifiers stay English whatever that language; user-facing strings keep full orthography.
2. **Every source file starts with a header comment,** at most two lines: what the file is, plus any non-obvious decision and why. It never restates the file name. Only a line the language requires to be literally first (a shebang or an encoding declaration) precedes it; existing files get one when the task touches them. Config and data files need none.
3. **Inline comments explain *why*, never what the next line does.** Every non-obvious workaround gets one. No emojis. A line, variable or constant whose name already says it gets no comment.
4. **A doc comment goes on a function only when its name and signature do not say enough:** complex logic, an outcome the signature hides (a `false` that means "already taken", a deliberate throw, a side effect) or a parameter that is not obvious. A self-descriptive function (`formatBytes`, `describeItem`) gets none.
5. **A doc comment is short:** two lines at most, and tags (`@param`, `@returns`, `@throws` or the language's equivalent) only for what the name and the type do not already say. A comment that echoes the name, the type or the signature is deleted.
6. **Short inline comments are lowercase fragments:** one line, no capital at the start, no period at the end, as few words as it takes (`// retry once, the socket may be stale`). The tone rules of copy.md apply to every comment and doc.

Details and gotchas, binding too: [details/comments-and-docs.md](details/comments-and-docs.md).

## Checklist

- [ ] Every new or touched source file has a header of at most two lines saying what it is and why it looks that way.
- [ ] No comment echoes a name, a type or a signature; self-descriptive functions and constants have none.
- [ ] A doc comment exists where the name hides something (an outcome, a deliberate throw, complex logic), and is two lines at most.
- [ ] Every short inline comment is one lowercase line with no final period and no lead-in filler.
