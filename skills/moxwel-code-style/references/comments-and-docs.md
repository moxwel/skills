# Comments and docs

Covers every source file in any language: the language of code and text, file headers, inline comments and doc comments on functions, constants and types.

## Rules

1. **Language:** code, comments, doc comments, user-facing strings, logs and docs are in English. When the project names another language for user-facing strings, comments or docs (an override, see SKILL.md), those use it. Comments stay ASCII (drop accents) and identifiers stay English whatever that language; user-facing strings keep full orthography.
2. **Every source file starts with a header comment,** at most two lines: what the file is, plus any non-obvious decision and why. It never restates the file name. Only a line the language requires to be literally first (a shebang or an encoding declaration) precedes it; existing files get one when the task touches them. Config and data files need none.
3. **Inline comments explain *why*, never what the next line does.** Every non-obvious workaround gets one. No emojis. A line, variable or constant whose name already says it gets no comment.
4. **A doc comment goes on a function only when its name and signature do not say enough:** complex logic, an outcome the signature hides (a `false` that means "already taken", a deliberate throw, a side effect) or a parameter that is not obvious. A self-descriptive function (`formatBytes`, `describeItem`) gets none.
5. **A doc comment is short:** two lines at most, and tags (`@param`, `@returns`, `@throws` or the language's equivalent) only for what the name and the type do not already say. A comment that echoes the name, the type or the signature is deleted.

## Details

- **Header and doc forms by language:**

| Language | File header | Doc comment | Tags |
|---|---|---|---|
| TypeScript / JavaScript | `/* … */` block | `/** … */` above the function | `@param name - Desc.`, `@returns Desc.`, `@throws Desc.` |
| CSS | `/* … */` block | none | none |
| Python | module docstring `"""…"""` | docstring as the first statement | `:param name: Desc.`, `:returns: Desc.`, `:raises Error: Desc.` |
| Bash | `#` block after the shebang, with a usage section for scripts | `#` lines right above the function | prose: what it takes, what it prints or returns |

- **Does it need a doc comment?** Read the name and the signature as a stranger would. If they answer what it does, what it takes and what it returns, stop. Otherwise write only the missing part: the unexpected outcome, the edge case, the throw.
- **Doc tags:**
  - `param` only for a parameter the name and type leave unclear (a unit, a format, an accepted range). One line each; an options object documents only its non-obvious fields.
  - `returns` when the value has outcomes the type does not show (`true if it marked it; false if it doesn't exist or was already reviewed.`). The special case never goes in the summary line.
  - `throws` when the function throws or rethrows on purpose, or calls a function whose doc has `throws` without catching it. Say when it throws in the tag, never in prose.
  - No `@` inside the text: tag parsers read it as a new tag.
  - A summary-only doc is one line (`/** Number of active items. */`).
- **Constants** that need explaining get a one-line doc comment above them (`/** … */`, `#` in Python/Bash), never a trailing comment. A constant with a descriptive name needs none.
- **Shared types** get `@property name - Desc.` lines in the type's doc for non-obvious fields, never comments inside the type.

```ts
/**
 * Marks the item as reviewed if it is still pending.
 * @returns false if it doesn't exist or was already reviewed.
 */
export function markItemReviewed(id: string, status: ReviewStatus): boolean {
```

```python
def mark_item_reviewed(item_id: str, status: str) -> bool:
    """Marks the item as reviewed if it is still pending.

    :returns: False if it doesn't exist or was already reviewed.
    """
```

## Gotchas

- **Accents break ASCII-only tooling.** A comment written in another language keeps its words but drops the accents (`configuracion`, not `configuración`).
- **A doc that restates the name is noise.** `/** Gets the item. */` on `getItem`, or `@param item - Item to describe.` on `describeItem(item)`, adds nothing: say what is non-obvious (which item, what happens when it is missing) or write no comment.
- **A long comment is a smell.** Three lines of history and reasoning around a one-line fact bury the fact: keep the constraint, drop the story.

## Checklist

- [ ] Every new or touched source file has a header of at most two lines saying what it is and why it looks that way.
- [ ] No comment echoes a name, a type or a signature; self-descriptive functions and constants have none.
- [ ] A doc comment exists where the name hides something (an outcome, a deliberate throw, complex logic), and is two lines at most.
