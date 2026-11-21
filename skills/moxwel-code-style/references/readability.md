# Readability

Covers the shape of code in any language: conditions, control flow, function body order, definition order, line length, alignment and imports.

## Rules

1. **Named conditions:** a comparison or compound condition used in an `if`, ternary or markup template (JSX, HTML templates) becomes a named boolean first (naming.md rule 3). A plain boolean variable or a single predicate call needs no new name, and neither does a language idiom that is the condition itself (`if __name__ == "__main__":`). Filter callbacks and comprehension clauses are not covered.
2. **Flat control flow:** early returns over nested `if`s, and no nested ternaries (use a named const, an early return or a tiny helper).
3. **The result reads like a template:** derived values (computed strings, filtered lists, conditional texts) live in named consts before the `return` or the output, and a big result is split into named pieces composed at the end.
   - **Body order:** inputs and guards (early returns) → derived values → local helpers → named pieces → a short final `return` or output that composes them. A guard that needs a derived value comes right after it.
   - **One concept per line.** Chained operations that each do something different get their own line or their own named value.
4. **No line length limit: never break a line because it is long.** A call, signature, literal, condition or comment stays on one line however long it gets.
   - **A line too long to read** gets shorter by naming its parts (rule 3, one concept per line), never by wrapping it.
   - Multi-line forms that come from structure, not length, stay as they are: an object with one field per line, a function body, a list of steps.
5. **Imports are grouped and sorted,** always from the module that defines the name, never through a re-exporting barrel file.
   - Groups, in order: external packages and the standard library, internal modules by absolute alias, relative modules, then type-only imports (same group order inside), then side-effect imports of assets and styles.
   - Alphabetical by module path within each group, except side-effect imports, which keep their load order (shared or base first, the file's own last), since that order can change behavior.
6. **Consecutive lines of the same shape are aligned:** declarations, `key: value` attributes, assignments, expressions that differ only in an operand, one-line `if ... return` and arrow functions are padded with spaces so the same part starts in the same column.
   - A block is consecutive lines with no blank line between them. A blank line starts a new block, and each block is aligned on its own, to its widest item.
   - Declarations: pad the type so the names start in the same column, then pad after the separator (`=` or `:`) so the values start in the same column. `key: value` lines (attributes, object fields) follow the same rule.
   - Expressions and statements of the same shape: pad so the operator or keyword sits in the same column across the lines (the `=` of assignments, `&&` or `||`, the keyword after `if (...)`, the `=>` of arrow functions). For arrows, pad before the shorter parameter so the `=>` lines up. A declaration (`const url = ...`) and an assignment to a variable or property (`url.search = ...`) are the same shape, even when one value opens a multi-line expression: their `=` line up.
   - Trailing comments on consecutive lines go in the same column, one space after the longest line of the group.
   - **Cut at 8 columns:** a group ends where a line differs by 8 or more columns from the previous one (in the width of the name, or of the code for trailing comments), shorter or longer. The line left out keeps a single space, and each side of the cut aligns on its own. Compare each line with the one right above it, never with the widest of the block: after `PORT = 8080` (a 4-column name), `MAX_CONNECTIONS` (15) jumps by 11, so `PORT` keeps its single space and the aligned group starts at `MAX_CONNECTIONS`.
   - Never aligned: imports, a line alone, and data files (JSON, XML, `.po`, lockfiles).
   - Adding or renaming the widest item of a group re-pads its other lines. Re-pad the groups the change touches, and leave the rest of the file as it is (git-conventions.md rule 7).
7. **Defined before used:** every named thing (constant, variable, function, class, type, or a child element or component of a declarative tree) is defined above the first line that uses it, even when the language allows the reverse (hoisting, late binding, names resolved at load time). The file reads top to bottom in call order: helpers first, then the code that calls them, and the entry point last.
   - **What counts as a use:** a call, a read, a reference from a callback or an event or signal handler, and a declarative attribute or binding that reads another element by name.
   - **Variables come first, unconditionally:** variables, fields, properties and aliases stay at the top of their scope (module, class, component) even when one reads something defined below it. The rule orders what follows them. Inside a function body, rule 3 sets the order.
   - **Order after the variables:** the objects or elements that the code uses, then the functions, each after the helpers it calls, then whatever only calls into them (the entry point, a main block, a loop or timer that drives the code).
   - **Exceptions:**
     - An order that carries meaning stays: elements rendered or laid out in declaration order, decorator stacks, registration or middleware order, and anything whose execution order changes the result. An element outside that order (a popup, a dialog, a non-visual helper object) can move.
     - A cycle, such as mutual recursion or an element whose handler calls back a function that uses it: the side the other depends on comes first.
   - **Existing code moves as little as possible** (git-conventions.md rule 7):
     - A file that already complies is not reshuffled.
     - For each break, move either the block used too early (up) or the code that uses it (down), whichever changes fewer lines against the original file.
     - Move a block whole, with the comment above it, and nothing else in the same change.

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

- **Definition order** (rule 7), worked example: `readItem` is defined before `listItems` calls it, though a function declaration would be hoisted.

```ts
const ITEM_EXTENSION = ".json";

async function readItem(path: string): Promise<Item> {
  const itemJson = await readFile(path, "utf8");
  return JSON.parse(itemJson) as Item;
}

export async function listItems(): Promise<Item[]> {
  const fileNames = await readdir(ITEMS_DIR);
  const itemFiles = fileNames.filter((fileName) => fileName.endsWith(ITEM_EXTENSION));
  return Promise.all(itemFiles.map((fileName) => readItem(join(ITEMS_DIR, fileName))));
}
```

- **Definition order by language** (rule 7): the same sequence in each, variables, then what the code uses, then the code, then the entry point.
  - **Python:** module constants, private helpers, public functions, and `if __name__ == "__main__":` last. In a class, attributes first, then methods, each helper method above the methods that call it.
  - **Bash:** variables and flags, then functions (a helper above the functions that call it), then the main body.
  - **React or another component framework:** state and derived values first, then handlers, then the returned markup, whose element order is the rendered order and stays.
  - **QML:** properties and aliases first, then non-visual objects reached by `id`, then functions, then a timer or handler that only calls into them. Visual children keep their layout order.

- **Definition order in a declarative tree** (rule 7), QML: properties first, then the non-visual objects the functions use, then the functions, and last the timer that only calls into them. The `stopError` alias reads `stopper`, defined below it, and still stays with the properties.

```qml
Item {
    id: monitor

    property var processes: []
    readonly property alias stopError: stopper.stopError

    Plasma5Support.DataSource {
        id: launcher
        engine: "executable"
    }

    ProcessStopper {
        id: stopper
    }

    function sample(): void {
        processes = readProcesses();
    }

    function refresh(): void {
        sample();
    }

    function openSystemMonitor(): void {
        launcher.connectSource("plasma-systemmonitor");
    }

    Timer {
        repeat: true
        onTriggered: monitor.sample()
    }
}
```

- **Picking the smallest move** (rule 7): for each break, compare two candidates against the original file and keep the one with fewer changed lines (`diff original new | grep -c '^[<>]'`).
  - Two callers (16 lines) sit above the helper they call, which sits next to its own helper (18 lines together). Moving the two callers down beats moving the two helpers up.
  - A one-line handler uses an element declared five lines below it. Moving the handler line down beats moving the element up.
  - After reordering, check that only the order changed: the sorted lines of the old and new file are equal (`diff <(sort old) <(sort new)`).

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

const url  = new URL(slug, baseUrl);
url.search = new URLSearchParams({
  utm_source: utmSource,
}).toString();
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
- **An element looks positioned but is not.** In a declarative UI, a tooltip, menu, dialog or non-visual object declared among laid-out children takes no place in the layout, so it can move below what it reads; a laid-out sibling cannot.
- **A scripted reorder cuts a block wrong.** Text tools that cut from one marker to the next can split a function or drop its comment. Check the sorted lines afterwards (Details, picking the smallest move).
- **A named condition evaluated too early.** Naming `const isOwner = item.ownerId === userId` before the `item` guard throws on a missing item. Keep each named condition after the guard it depends on.

## Checklist

- [ ] No comparison or compound condition inline in an `if`, ternary or markup template; no nested ternaries; guards return early.
- [ ] Derived values are named before the result.
- [ ] No line broken only because it was long; a hard-to-read line was shortened by naming its parts.
- [ ] Imports grouped, sorted and taken from their defining module.
- [ ] Consecutive lines of the same shape are aligned per block, groups cut at 8 columns, trailing comments aligned.
- [ ] Variables, fields and properties (aliases too) first; every object, element and function defined above its first use (calls, reads, handlers, bindings by name), the entry point last.
- [ ] In existing code, only the smaller of the two candidate moves for each break, meaningful orders untouched, and the sorted lines unchanged.
