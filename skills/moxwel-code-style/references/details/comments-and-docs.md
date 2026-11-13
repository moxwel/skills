# Comments and docs: details

Details and gotchas for the rules in [../comments-and-docs.md](../comments-and-docs.md).

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
- **Inline comment form:**
  - An inline comment is a `//` or `#` comment inside a body or after a line of code. File headers, doc comments and the usage block of a script keep full sentences (capital, final period).
  - Names, acronyms and proper nouns keep their case (`the API returns null`, `Plasma ignores it`), and a tool directive or marker stays as the tool expects it (`// eslint-disable-next-line`, `# noqa`, `shortcut: ...`).
  - Cut the lead-in: `this is needed because`, `note that`, `we need to`. Start at the fact.
  - A comment that needs several sentences is written as sentences (capital, periods), and is a smell (Gotchas).

| Before | After |
|---|---|
| `// Retry once, the socket may be stale.` | `// retry once, the socket may be stale` |
| `// Note that the API returns null for an empty list.` | `// the API returns null for an empty list` |
| `# This is needed because the file may not exist yet.` | `# the file may not exist yet` |

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
