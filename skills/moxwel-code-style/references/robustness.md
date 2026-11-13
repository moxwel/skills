# Robustness and error handling

Covers how code handles failure, in any language and in scripts: which errors are caught and where, what is logged and at which level, how one failing unit of work is isolated, how external calls are timed, retried and paced, how resources are released, and what reaches the caller. A unit of work is a request, a job, an item of a batch, a file, or a command in a script; an error there is a thrown exception, an error value, or a non-zero exit status.

## Rules

1. **Catch where the failure can be handled, never everywhere.** A catch belongs to the boundary that knows what to do with the failure: one unit of work in a batch, one request, one job, one command. A catch that does nothing is a defect, unless a comment says why dropping the error is safe.
2. **Name the expected failures.** Every external call (network, disk, database, subprocess, parser, third-party API) has known failure modes: timeouts, rate limits (429), server errors (5xx), missing files, malformed input. Catch those by their kind (a named error type, a status code, an exit code) and turn them into a domain error that says what failed. Anything else is unexpected and stays unexpected.
3. **Log by kind.** An expected failure is logged as a warning with its message only. An unexpected failure is logged as an error with the full trace (stack, or the failing command and line in a script). Expected failures that repeat on every run must not drown the real errors.
4. **Isolate each unit of work.** One bad item (a subreddit, a file, a row, a message, a request in a batch) does not stop the rest. Continue, collect the outcome, and report it at the end of the run.
5. **Translate at the layer boundary.** A library's error (HTTP client, parser, driver) becomes the project's own error kind in the layer that owns that library. Callers above it never handle the library's error kinds, and the original error stays as the cause.
6. **Keep the original error.** Re-raise with the cause chained (every language has a form, see Details). Never replace it with a generic message that hides why it failed.
7. **Every external call has a timeout.** No call waits forever. Use the client's timeout option or a cancellation signal, and take the value from configuration.
8. **Retry only what can succeed later, a bounded number of times.** Retry timeouts, connection resets, 408, 429 and 5xx, with a fixed maximum and exponential backoff; honor `Retry-After` when it is given. Never retry validation, auth or other 4xx errors. Never blindly retry a non-idempotent operation (a charge, a send, an insert): retry it only with an idempotency key, or after checking that it did not happen.
9. **Respect rate limits by pacing, not by hammering.** When a service limits bursts, space the calls with a fixed delay between units of work. A 429 means back off, not retry at once. The delay is configuration, not a magic number in the loop.
10. **Validate before side effects.** Check everything that can fail up front (existence, format, limits, permissions) before writing, sending, charging or deleting. Late failures leave partial state behind; keep late guards only for races (unique constraints, row counts).
11. **Release resources on every path.** Files, sockets, streams, locks and temporary files are released by a cleanup step that runs on every path, including errors and early returns (the table gives each language's form).
12. **Never swallow cancellation.** Do not catch interrupts, aborts or process signals just to ignore them: restore the interrupt state and let cancellation propagate. A catch-all handler (the broadest kind the language offers) belongs only at the outermost boundary.
13. **Required settings fail fast.** A required setting has no default. When it is missing, the process stops at startup and the error names the setting. Optional settings may default to a named constant.
14. **Callers get no internals.** Responses and user-facing messages say what went wrong in plain words, with no trace, query, path, command line, token or URL with credentials. The details go to the log, at the boundary that logs.

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

## Checklist

- [ ] Every external call has a timeout and catches its expected failures by kind.
- [ ] Expected failures log a warning with the message; unexpected ones log an error with the full trace.
- [ ] No empty catch. Each catch handles the failure, translates it with the cause, or re-raises it.
- [ ] One failing unit does not stop the batch; the run reports successes and failures at the end.
- [ ] Retries are bounded, only for retryable errors, and never blind for non-idempotent operations.
- [ ] Rate limits are respected by a configured pacing delay, and a 429 backs off.
- [ ] Library errors do not cross the layer boundary; the original error is kept as the cause.
- [ ] Responses and user messages carry no internals; logs carry no secrets.
- [ ] A missing required setting stops startup and names the setting.
- [ ] Resources are released by a cleanup step that runs on every path.
