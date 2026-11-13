# Robustness and error handling

Covers how code handles failure, in any language and in scripts: which errors are caught and where, what is logged and at which level, how one failing unit of work is isolated, how external calls are timed, retried and paced, how resources are released, and what reaches the caller. A unit of work is a request, a job, an item of a batch, a file, or a command in a script; an error there is a thrown exception, an error value, or a non-zero exit status.

## Rules

1. **Catch where the failure can be handled, never everywhere.** A catch belongs to the boundary that knows what to do with the failure: one unit of work in a batch, one request, one job, one command. A catch that does nothing is a defect, unless a comment says why dropping the error is safe.
2. **Name the expected failures.** Every external call (network, disk, database, subprocess, parser, third-party API) has known failure modes: timeouts, rate limits (429), server errors (5xx), missing files, malformed input. Catch those by their kind (a named error type, a status code, an exit code) and turn them into a domain error that says what failed. Anything else is unexpected and stays unexpected.
3. **Log by kind.** An expected failure is logged as a warning with its message only. An unexpected failure is logged as an error with the full trace (stack, or the failing command and line in a script). Expected failures that repeat on every run must not drown the real errors.
4. **Isolate each unit of work.** One bad item (a subreddit, a file, a row, a message, a request in a batch) does not stop the rest. Continue, collect the outcome, and report it at the end of the run.
5. **Translate at the layer boundary.** A library's error (HTTP client, parser, driver) becomes the project's own error kind in the layer that owns that library. Callers above it never handle the library's error kinds, and the original error stays as the cause.
6. **Keep the original error.** Re-raise with the cause chained (every language has a form, see [details](details/robustness.md)). Never replace it with a generic message that hides why it failed.
7. **Every external call has a timeout.** No call waits forever. Use the client's timeout option or a cancellation signal, and take the value from configuration.
8. **Retry only what can succeed later, a bounded number of times.** Retry timeouts, connection resets, 408, 429 and 5xx, with a fixed maximum and exponential backoff; honor `Retry-After` when it is given. Never retry validation, auth or other 4xx errors. Never blindly retry a non-idempotent operation (a charge, a send, an insert): retry it only with an idempotency key, or after checking that it did not happen.
9. **Respect rate limits by pacing, not by hammering.** When a service limits bursts, space the calls with a fixed delay between units of work. A 429 means back off, not retry at once. The delay is configuration, not a magic number in the loop.
10. **Validate before side effects.** Check everything that can fail up front (existence, format, limits, permissions) before writing, sending, charging or deleting. Late failures leave partial state behind; keep late guards only for races (unique constraints, row counts).
11. **Release resources on every path.** Files, sockets, streams, locks and temporary files are released by a cleanup step that runs on every path, including errors and early returns (the table gives each language's form).
12. **Never swallow cancellation.** Do not catch interrupts, aborts or process signals just to ignore them: restore the interrupt state and let cancellation propagate. A catch-all handler (the broadest kind the language offers) belongs only at the outermost boundary.
13. **Required settings fail fast.** A required setting has no default. When it is missing, the process stops at startup and the error names the setting. Optional settings may default to a named constant.
14. **Callers get no internals.** Responses and user-facing messages say what went wrong in plain words, with no trace, query, path, command line, token or URL with credentials. The details go to the log, at the boundary that logs.

Details and gotchas, binding too: [details/robustness.md](details/robustness.md).

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
