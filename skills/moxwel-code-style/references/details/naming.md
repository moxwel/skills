# Naming: details

Details and gotchas for the rules in [../naming.md](../naming.md).

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
