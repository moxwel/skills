# Comments and docs

Covers every source file in any language: the language of code and text, file headers, inline comments and doc comments on functions, constants and types.

## Rules

1. **Language:** code, comments, doc comments, user-facing strings, logs and docs are in English. When the project names another language for user-facing strings, comments or docs (an override, see SKILL.md), those use it. Comments stay ASCII (drop accents) and identifiers stay English whatever that language; user-facing strings keep full orthography.
2. **Every source file starts with a header comment** (only a line the language requires to be literally first, such as a shebang or an encoding declaration, precedes it; existing files get one when the task touches them): what the file is, what it does, and any non-obvious decision and why. Config and data files need none.
3. **Inline comments explain *why*, never what the next line does.** Every non-obvious workaround gets one. No emojis.
4. **Deliberate shortcuts** get a `ponytail:` comment (a fixed marker word, so every shortcut can be found with one search) stating the trade-off (`// ponytail: linear scan, lists stay under 100 items`).
5. **Every named function has a doc comment:** a one-sentence summary, plus `@param`/`@returns`/`@throws` (or the language's equivalent) where they apply, with no `{type}`. Anonymous inline callbacks need none.

## Details

- **Header and doc forms by language:**

| Language | File header | Doc comment | Tags |
|---|---|---|---|
| TypeScript / JavaScript | `/* … */` block | `/** … */` above the function | `@param name - Desc.`, `@returns Desc.`, `@throws Desc.` |
| CSS | `/* … */` block | none | none |
| Python | module docstring `"""…"""` | docstring as the first statement | `:param name: Desc.`, `:returns: Desc.`, `:raises Error: Desc.` |
| Bash | `#` block after the shebang, with a usage section for scripts | `#` lines right above the function | prose: what it takes, what it prints or returns |

- **Doc tags:**
  - One `param` line per parameter. An object of options or props documents each field on its own line (`@param options.limit - Desc.`, `[options.limit=10]` when optional).
  - `returns` when the function returns a value, explaining each outcome (`The item, or undefined if it does not exist.`, `true if it marked it; false if it doesn't exist or was already reviewed.`). The special case never goes in the summary line.
  - `throws` when the function throws or rethrows on purpose, or calls a function whose doc has `throws` without catching it. Say when it throws in the tag, never in prose.
  - No `@` inside the text: tag parsers read it as a new tag.
  - A summary-only doc is one line (`/** Number of active items. */`).
- **Constants** that need explaining get a one-line doc comment above them (`/** … */`, `#` in Python/Bash), never a trailing comment.
- **Shared types** get `@property name - Desc.` lines in the type's doc for non-obvious fields, never comments inside the type.

```ts
/**
 * Marks the item as reviewed if it is still pending.
 * @param id - Item UUID.
 * @param status - Final status.
 * @returns true if it marked it; false if it doesn't exist or was already reviewed.
 * @throws If the store is not open.
 */
export function markItemReviewed(id: string, status: ReviewStatus): boolean {
```

```python
def mark_item_reviewed(item_id: str, status: str) -> bool:
    """Marks the item as reviewed if it is still pending.

    :param item_id: Item UUID.
    :param status: Final status.
    :returns: True if it marked it; False if it doesn't exist or was already reviewed.
    :raises RuntimeError: If the store is not open.
    """
```

## Gotchas

- **Accents break ASCII-only tooling.** A comment written in another language keeps its words but drops the accents (`configuracion`, not `configuración`).
- **A doc that restates the name is noise.** `/** Gets the item. */` on `getItem` adds nothing: say what is non-obvious (which item, what happens when it is missing) or keep the summary line minimal.

## Checklist

- [ ] Every new or touched source file has a header comment saying what it is and why it looks that way.
- [ ] Every named function has a doc comment, with each outcome explained in `returns` and every deliberate throw in `throws`.
- [ ] Comments are ASCII and explain why; shortcuts carry `ponytail:`.
