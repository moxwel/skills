# Readability

Covers the shape of code in any language: conditions, control flow and nesting depth, function body order, definition order, line length, alignment, imports, and the types that say what a comment would.

## Rules

1. **Named conditions:** a comparison or compound condition used in an `if`, ternary or markup template (JSX, HTML templates) becomes a named boolean first (naming.md rule 3). A plain boolean variable or a single predicate call needs no new name, and neither does a language idiom that is the condition itself (`if __name__ == "__main__":`). Filter callbacks and comprehension clauses are not covered.
   - **A condition that still reads badly after naming its parts** becomes a predicate function named after the question it answers (`isRefundable(order)`, naming.md rule 4), defined above its caller (rule 7), in any language.
2. **Flat control flow: at most 3 levels of nesting.** The body of a function is level 1, and each block inside it adds one: `if`, `else`, `for`, `while`, `try`, `catch`, `switch`, and the body of a callback or a nested function. Code that would reach level 4 is flattened:
   - **Inversion first:** flip the condition and leave early (`return`, `continue`, `break`, `throw`), so the main path stays at the shallowest level. The guards sit together at the top (rule 3, body order).
   - **Extraction second:** when inversion is not enough, move the inner block into its own function, named after what it does and defined above its caller (rule 7).
   - **Loops skip with `continue`:** a condition that skips an item is an inverted guard at the top of the body, never an `if` that wraps the rest of it.
   - **No `else` after a block that returns, continues, breaks or throws:** the code after it already is the else.
   - **No nested ternaries:** name the inner one as its own const first, or use an early return or a tiny helper. In markup (JSX, templates) the conditional values are named above the `return`.
   - **Not a level:** object and type literals, class bodies, `case` arms, markup elements, and a callback with an expression body (`items.map((item) => item.name)`).
   - Code the task adds or rewrites stays within level 3. Deeper code that already exists stays as it is (SKILL.md).
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
   - A line that only opens a body is not part of any group: the body of a function, handler or callback (`onFilled: {`, `onLineLaidOut: line => {`, `const onSave = () => {`) or a child object of a declarative tree (`contentItem: Item {`). It keeps a single space and does not count when measuring the group. A value that is an expression continuing on the next lines still aligns: a call (`url.search = new URLSearchParams({`), an object literal (`const config = {`) or an array literal (`const items = [`).
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
8. **Types say what a comment would:** a value that may be missing has the language's type for absence (`T | null`, `T | undefined`, `Optional[T]`, `T | None`), never a sentinel such as `-1`, `""` or `0` that the caller has to know about. A fixed set of states is a union or enum type, not a free string or number.
   - A library or built-in that returns a sentinel (`indexOf`, `str.find`) is read through a named condition right where it is called (`const isFound = index !== -1`), and the sentinel goes no further than that line.
   - Bash has no types: a function reports a missing value with its exit status and an empty output, never with a magic string.

## Details

- **Bash:** a single `[ … ]` test counts as the predicate itself; a compound test becomes a function named like a predicate (`is_same_file`), called in the `if`.

- **Inversion** (rule 2), worked example. The nested version reaches level 4 at `publish(item)`:

```ts
function publishItem(item: Item | null, userId: string): string {
  if (item) {
    const isOwner = item.ownerId === userId;
    if (isOwner) {
      if (!item.isPublished) {
        publish(item);
        return "Published.";
      }
      return "Already published.";
    }
    return "Not yours.";
  }
  return "Missing item.";
}
```

  Each condition flipped into a guard keeps the main path at level 1:

```ts
function publishItem(item: Item | null, userId: string): string {
  if (!item) return "Missing item.";
  const isOwner = item.ownerId === userId;
  if (!isOwner) return "Not yours.";
  if (item.isPublished) return "Already published.";
  publish(item);
  return "Published.";
}
```

- **Extraction** (rule 2), worked example. Inverting the `if` into a `continue` still leaves the row loop at level 4, so the part loop moves into a function defined above its caller:

```ts
function exportItems(items: Item[]): void {
  for (const item of items) {
    if (item.isValid) {
      for (const part of item.parts) {
        for (const row of part.rows) {
          writeRow(row);
        }
      }
    }
  }
}
```

```ts
function exportPart(part: Part): void {
  for (const row of part.rows) {
    writeRow(row);
  }
}

function exportItems(items: Item[]): void {
  for (const item of items) {
    if (!item.isValid) continue;
    for (const part of item.parts) {
      exportPart(part);
    }
  }
}
```

- **No `else` after a return** (rule 2): `if (isEmpty) { return "No items."; } else { return label; }` becomes `if (isEmpty) return "No items.";` followed by `return label;`.

- **Nested ternary** (rule 2): `isAdmin ? "Admin" : isEditor ? "Editor" : "Viewer"` becomes two named values.

```ts
const editorOrViewer = isEditor ? "Editor" : "Viewer";
const roleLabel      = isAdmin ? "Admin" : editorOrViewer;
```

- **Predicate function** (rule 1): the condition named part by part still takes three lines to read, so it becomes a function and the `if` reads as the question.

```ts
function isRefundable(order: Order): boolean {
  const isRecent       = daysSince(order.boughtAt) <= REFUND_WINDOW_DAYS;
  const isCostlyOrGift = order.priceCents > MIN_REFUND_CENTS || order.isGift;
  return isRecent && !order.isUsed && isCostlyOrGift;
}

if (isRefundable(order)) refund(order);
```

- **Flat control flow by language** (rule 2):
  - **Python:** the guard keeps its body on its own line (`if not is_owner:`, then `return None`), loops skip with `continue`, and a nested `def` is a level like a callback.
  - **Bash:** a guard is one line, `[ -d "$source" ] || return 1`, and a loop skips with `[ -f "$file" ] || continue`. A function body is level 1, and `if`, `for`, `while`, `until`, `case` and a `{ ... }` group each add one.

- **The checker** (rule 2): `scripts/check_style.py` reports each block that reaches level 4 in TS/JS, Python and Bash. It counts braces, indentation and keywords, not the syntax tree, so a regex literal in TS/JS or a heredoc in Bash can make it report a block that is not there. Read the reported line before flattening, and tell the user about a false report instead of reshaping correct code.

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
        id:     launcher
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
        repeat:      true
        onTriggered: monitor.sample()
    }
}
```

- **Types instead of sentinels** (rule 8): absence and states live in the return type, so the caller cannot miss them.

```ts
type ReviewStatus = "pending" | "reviewed";

function lastReviewedAt(item: Item): Date | null {
  return item.reviews.at(-1)?.reviewedAt ?? null;
}
```

  In Python the same function returns `datetime | None`, and a missing setting is `None`, never `""`.

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

  In QML, `showAlphaChannel` (16 columns) is 9 wider than `enabled`, so the cut leaves it a single space. `onClicked: {` only opens a handler body, so it does not join `showAlphaChannel` either.

```qml
Button {
    id:      saveButton
    enabled: canSave
    showAlphaChannel: false
    onClicked: {
        save();
    }
}
```

## Gotchas

- **A callback that must not return a value returns one.** An arrow function with an expression body returns that expression (`() => notify(state)`); when the caller treats a return value as meaningful (cleanup functions, event handlers that cancel on `false`), use braces.
- **A formatter can strip the padding.** If the project's formatter removes it, the formatter wins for those lines.
- **An element looks positioned but is not.** In a declarative UI, a tooltip, menu, dialog or non-visual object declared among laid-out children takes no place in the layout, so it can move below what it reads; a laid-out sibling cannot.
- **A scripted reorder cuts a block wrong.** Text tools that cut from one marker to the next can split a function or drop its comment. Check the sorted lines afterwards (Details, picking the smallest move).
- **Extraction that only renames the depth.** Moving a nested block into an inline callback (`items.forEach((item) => { ... })`) keeps every level it had. Extract a named function at the top level of the file, or invert first.
- **A guard with no main path.** Two branches of equal weight that pick one of two values are a named const with a ternary, not a guard and a fallthrough.
- **A named condition evaluated too early.** Naming `const isOwner = item.ownerId === userId` before the `item` guard throws on a missing item. Keep each named condition after the guard it depends on.

## Checklist

- [ ] No comparison or compound condition inline in an `if`, ternary or markup template; no nested ternaries; guards return early.
- [ ] No new or rewritten code past level 3 of nesting: inversion first, extraction second, `continue` in loops, no `else` after a block that leaves.
- [ ] A condition that still reads badly after naming its parts is a predicate function.
- [ ] Derived values are named before the result.
- [ ] No line broken only because it was long; a hard-to-read line was shortened by naming its parts.
- [ ] Imports grouped, sorted and taken from their defining module.
- [ ] Consecutive lines of the same shape are aligned per block, groups cut at 8 columns, trailing comments aligned; lines that only open a body are left out.
- [ ] Variables, fields and properties (aliases too) first; every object, element and function defined above its first use (calls, reads, handlers, bindings by name), the entry point last.
- [ ] A value that may be missing uses the type for absence and a fixed set of states uses a union or enum; no new sentinel such as `-1` or `""`.
- [ ] In existing code, only the smaller of the two candidate moves for each break, meaningful orders untouched, and the sorted lines unchanged.
