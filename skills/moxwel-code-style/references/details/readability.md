# Readability: details

Details and gotchas for the rules in [../readability.md](../readability.md).

## Details

- **Bash:** a single `[ … ]` test counts as the predicate itself; a compound test becomes a function named like a predicate (`is_same_file`), called in the `if`.

- **Body order** (rule 3), worked example:

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

- **Import order** (groups and sorting are in rule 5):
  - Inside one folder use relative paths; across folders use the project's alias when it has one.
  - Python overrides the first group (PEP 8): standard library, then third party, then local, each its own group. Bash sources its helpers at the top, after the header.
- **Alignment** (the mechanics are in rule 6), worked examples:

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
- **A formatter can strip the padding.** If the project's formatter removes it, the formatter wins for those lines.
- **A named condition evaluated too early.** Naming `const isOwner = item.ownerId === userId` before the `item` guard throws on a missing item. Keep each named condition after the guard it depends on.
