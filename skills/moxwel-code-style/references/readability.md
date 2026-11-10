# Readability

Covers the shape of code in any language: conditions, control flow, function body order, line length, alignment and imports.

## Rules

1. **Named conditions:** a comparison or compound condition used in an `if`, ternary or markup template (JSX, HTML templates) becomes a named boolean first (naming.md rule 3). A plain boolean variable or a single predicate call needs no new name, and neither does a language idiom that is the condition itself (`if __name__ == "__main__":`). Filter callbacks and comprehension clauses are not covered.
2. **Flat control flow:** early returns over nested `if`s, and no nested ternaries (use a named const, an early return or a tiny helper).
3. **The result reads like a template:** derived values (computed strings, filtered lists, conditional texts) live in named consts before the `return` or the output, and a big result is split into named pieces composed at the end.
4. **No line, code or comment, goes past 120 columns.**
5. **Imports are grouped and sorted** (Details), always from the module that defines the name, never through a re-exporting barrel file.
6. **Consecutive lines of the same shape are aligned:** declarations, `key: value` attributes, assignments, expressions that differ only in an operand, one-line `if ... return` and arrow functions are padded with spaces so the same part starts in the same column (Details, Alignment).

## Details

- **Bash:** a single `[ … ]` test counts as the predicate itself; a compound test becomes a function named like a predicate (`is_same_file`), called in the `if`.
- **Body order:** inputs and guards (early returns) → derived values → local helpers → named pieces → a short final `return` or output that composes them. A guard that needs a derived value comes right after it.

```ts
/** The count and names, or a message when there are no items or no matches. */
export function describeItems(items: Item[], query: string): string {
  const isEmpty = items.length === 0;
  if (isEmpty) return "No items.";
  const matchingItems = items.filter((item) => item.name.includes(query));
  const isFiltered    = query !== "";
  const hasMatches    = matchingItems.length > 0;
  if (!hasMatches) return `No items match "${query}".`;
  const label = isFiltered ? `${matchingItems.length} matching items` : `${items.length} items`;
  const names = matchingItems.map((item) => item.name).join(", ");
  return `${label}: ${names}`;
}
```

- **Long lines:** a call, signature or literal that doesn't fit breaks one item per line with a trailing comma (where the language allows it) and the closer on its own line. Long comments wrap at a whole word.
- **Import order:**
  - Groups, in order: external packages and the standard library, internal modules by absolute alias, relative modules, then type-only imports (same group order inside), then side-effect imports of assets and styles.
  - Alphabetical by module path within each group, except side-effect imports, which keep their load order (shared or base first, the file's own last), since that order can change behavior.
  - Inside one folder use relative paths; across folders use the project's alias when it has one.
  - Python overrides the first group (PEP 8): standard library, then third party, then local, each its own group. Bash sources its helpers at the top, after the header.
- **One concept per line.** Chained operations that each do something different get their own line or their own named value.
- **Alignment:**
  - A block is consecutive lines with no blank line between them. A blank line starts a new block, and each block is aligned on its own, to its widest item.
  - Declarations: pad the type so the names start in the same column, then pad after the separator (`=` or `:`) so the values start in the same column. `key: value` lines (attributes, object fields) follow the same rule.
  - Expressions and statements of the same shape: pad so the operator or keyword sits in the same column across the lines (the `=` of assignments, `&&` or `||`, the keyword after `if (...)`, the `=>` of arrow functions). For arrows, pad before the shorter parameter so the `=>` lines up.
  - Trailing comments on consecutive lines go in the same column, one space after the longest line of the group.
  - **Cut at 8 columns:** a group ends where a line differs by 8 or more columns from the previous one (in the width of the name, or of the code for trailing comments), shorter or longer. The line left out keeps a single space, and each side of the cut aligns on its own.
  - A line that the padding would push past 120 columns is left out of the group.
  - Never aligned: imports, a line alone, and data files (JSON, XML, `.po`, lockfiles).

```ts
const timeoutMs = 500; // milliseconds
const retries   = 3;   // per request
const maxConcurrentConnectionsPerHost = 8; // shared pool

const isHiddenUntilRunning = mode === MODE_RUNNING && !isRunning;
const isHiddenUntilActive  = mode === MODE_ACTIVE  && !isActive;

if (isActive)  return "active";
if (isRunning) return "running";
return "stopped";

const fields = {
  textFromValue: (value) => `${value} s`,
  valueFromText:  (text) => parseInt(text),
};
```

```qml
Button {
    id:      saveButton
    enabled: canSave
    showAlphaChannel: false
}
```

## Gotchas

- **A callback that must not return a value returns one.** An arrow function with an expression body returns that expression (`() => notify(state)`); when the caller treats a return value as meaningful (cleanup functions, event handlers that cancel on `false`), use braces.
- **Padding makes diffs wider.** Adding or renaming the widest item of a group re-pads its other lines. Re-pad the groups the change touches, and leave the rest of the file as it is (git-conventions.md rule 7).
- **A formatter can strip the padding.** If the project's formatter removes it, the formatter wins for those lines.
- **A named condition evaluated too early.** Naming `const isOwner = item.ownerId === userId` before the `item` guard throws on a missing item. Keep each named condition after the guard it depends on.

## Checklist

- [ ] No comparison or compound condition inline in an `if`, ternary or markup template; no nested ternaries; guards return early.
- [ ] Derived values are named before the result.
- [ ] No line over 120 columns (`python3 <skill>/scripts/check_style.py <folder>`).
- [ ] Imports grouped, sorted and taken from their defining module.
- [ ] Consecutive lines of the same shape are aligned per block, groups cut at 8 columns, trailing comments aligned, nothing padded past 120 columns.
