# Robustness and error handling: details

Details and gotchas for the rules in [../robustness.md](../robustness.md).

## Details

Shape of the same logic, in neutral pseudocode. Every language follows this order:

```
for each unit in units:
    if unit is not the first: pause(configured delay)
    try:
        items = fetch(unit, timeout = configured timeout)
        queue the new items
    catch expected failure as error:
        warn("could not read {unit}: {error.message}")   # message only
    catch any other error as error:
        error_log("unexpected failure in {unit}", error)  # full trace
report: how many units succeeded, how many failed, which ones
```

- **Expected or unexpected?** Ask whether the same input could succeed later without a code change. If yes, the failure is expected (timeout, 429, host offline). If the code is wrong, it is unexpected (a missing value, a broken assumption). Expected failures get a named kind; unexpected ones are bugs and keep the full trace.
- **Retryable:** timeouts, connection resets, 408, 429, 5xx. **Not retryable:** other 4xx, validation, auth, not found, logic errors.
- **Backoff:** a base delay multiplied by 2 for each attempt, capped. The maximum attempts and the base delay are named constants or configuration.
- **Pacing between units:** one fixed delay, applied between units only, not before the first or after the last.
- **Partial batches:** when a batch ends with failures, report the counts (succeeded, failed) and the failed ids in a single final line.
- **Cleanup order:** release resources in reverse order of acquisition. A failed release is logged, and it never replaces the original error.

Language idioms. The rules do not change between languages; only the form does. For a language not in this table, use the equivalent of each row.

| Concept | TypeScript / JavaScript | Python | Bash |
|---|---|---|---|
| Named error kind | `class X extends Error` | `class X(Exception)` | a named exit code and a message prefix |
| Catch one kind only | `if (error instanceof X)` | `except X as error:` | check the status right after the command: `if ! command; then` |
| Keep the cause | `new X(message, { cause: error })` | `raise X(message) from error` | print the failing command's own stderr before exiting |
| Timeout | `AbortSignal.timeout(ms)` passed to the request | the `timeout=` argument of the client | `timeout <seconds> command` |
| Release on every path | `try { } finally { }` | `try: ... finally:` or `with` | `trap 'cleanup' EXIT` |
| Log expected (message only) | `logger.warn(message)` | `logger.warning(message)` | `echo "WARN: $message" >&2` |
| Log unexpected (full trace) | `logger.error(message, error)` | `logger.exception(message)` inside the handler | `trap 'echo "ERROR at line $LINENO" >&2' ERR` |
| Run independent units, wait for all | `Promise.allSettled(units)` | `asyncio.gather(*units, return_exceptions=True)` | start each unit in the background and check its status with `wait <pid>` |
| Pacing between units | `await sleep(ms)` | `time.sleep(seconds)` | `sleep <seconds>` |

## Gotchas

- **A catch that only logs and continues** hides data loss: the item is gone and nothing says so. Handle it, record it as failed, or re-raise it.
- **Logging at every layer** prints the same error three times. Log once, at the boundary that handles it; lower layers raise.
- **Running independent units with a form that stops at the first failure** leaves the others running in the background. Use the form that waits for every unit and reports each outcome (see the table).
- **A retry loop without a timeout or a cap** turns one outage into a stuck process.
- **URLs, headers and command lines in logs** can carry tokens or passwords. Redact them before logging.
- **Catching to decide control flow** (trying an operation to find out whether a file exists) hides real errors. Check first where the API allows it.
- **A pause without cancellation** blocks shutdown. Wait through the cancellation path.
- **A catch-all handler** also catches cancellation and shutdown. Keep it at the outermost boundary (rule 12).
- **Bash:** `set -e` does not stop a script inside an `if` condition, a `while` condition or on the left of `||`. Check the status explicitly where it matters.
