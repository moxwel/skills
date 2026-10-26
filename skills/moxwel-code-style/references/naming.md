# Naming

Covers names of variables, constants, functions, types and booleans, and the identifiers of stored records, in any language.

## Rules

1. **Casing:** PascalCase for types, classes and components; UPPER_CASE for module-level constants (values fixed when the module loads: literals and values derived from them or from the environment); camelCase for everything else. Languages with their own convention follow it (Details). Exceptions: names a framework or protocol fixes, and record types that mirror an external schema, which keep its field names (`created_at`).
2. **No single-letter names,** except the loop index `i`. Not in callbacks either: `items.map((item) => …)`, `catch (error)`.
3. **Booleans are named `is*`/`has*`/`can*`/`should*`/`was*`:** variables, state, function results, parameters, fields and predicates (`isTaken()`, `hasPendingItems()`). Exceptions: names fixed by a platform or library (`disabled`, `open`), fields of records that mirror an external schema (rule 1), and commands that report success (`insertItem()` returning `boolean`).
4. **Values are named after their content,** not their type or origin: `visibleItems`, `retryDelayMs`, not `list2`, `data` or `result`. Handlers and commands are named after the action (`confirmDelete`, `syncFiles`).
5. **Non-obvious literals become named constants** at the top of the file (`MAX_RETRIES = 3`), or in a shared constants module when several files use them.
6. **Records tied to a user or made public are identified by a UUID, never by an ascending number,** unless the user explicitly asks for numbers. That covers users and their content (posts, files, uploads, collections) and anything whose id reaches a URL, a file name, an API payload or another user, in any storage (SQL, document store, files). The UUID is the record's primary key and every reference to it uses the same UUID. Sequential integers stay for technical data that never leaves the system (row ids, page numbers, counters).

## Details

- **Casing by language:**

| Language | Types/classes | Constants | Functions and variables | Files |
|---|---|---|---|---|
| TypeScript / JavaScript | `PascalCase` | `UPPER_CASE` | `camelCase` | `camelCase.ts`, named after what it holds |
| Python | `PascalCase` | `UPPER_CASE` | `snake_case` | `snake_case.py` |
| Bash | none | `UPPER_CASE` for globals and env | `snake_case` functions, lowercase `local` and loop variables | `snake_case.sh` |
| CSS | none | custom properties `--kebab-case` | classes `camelCase` or `kebab-case`, one style per project, named after what they style | named after what it styles |

- **Units in the name** when a number has one and the type doesn't say it: `timeoutMs`, `sizeBytes`, `durationSec`.
- **Booleans read as a question:** `if (isEmpty)`, `if (canDelete)`. A negated name (`isNotReady`) is only for fields that already exist that way; prefer the positive form and `!`.
- **Function names:** verb + subject (`listItems`, `findItem`, `countItems`, `formatBytes`). A function whose job is to answer a yes/no question is a predicate and takes the prefix; a command that returns a success flag keeps its verb name (rule 3 exception).

## Checklist

- [ ] Casing matches the language table; constants are UPPER_CASE.
- [ ] No single-letter names besides `i`; every boolean has its prefix.
- [ ] No unexplained magic number or string in the body.
- [ ] Records tied to a user or made public use UUID ids and UUID references (unless numbers were asked for).
