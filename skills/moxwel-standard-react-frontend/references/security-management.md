# Security

Covers entry points (pages, server actions, route handlers), auth, sessions, validation, output, files, processes, uploads and secrets. Background: the Next.js authentication guide and the OWASP cheat sheets.

## Rules

1. **Every page, server action and route handler is a trust boundary.** Server actions are public HTTP endpoints, even when only an admin page renders the form.
2. **Each entry point runs five steps, in order:**
   1. `requireUser()`/`requireAdmin()` (route handlers: `getSession()` → 401/403). Public pages and the `login` action skip this step and say so in their header.
   2. Sanitize every input, typed action args included.
   3. Check everything that can be checked up front (access, state, existence, uniqueness, limits) before any side effect or slow work; late guards (UNIQUE, row counts) stay for races.
   4. Call `lib/`.
   5. Respond with no internals: actions call `refresh()` when data changed and return `ActionState`, route handlers return a `Response`, pages render.
3. **Layouts and `proxy.ts` (formerly middleware) never gate access.** Layouts don't re-render on navigation, so their check goes stale. Each page and action checks for itself.
4. **Validate on the server with allow-lists** (regex, enum) in `lib/validation/validate.ts`, which returns the clean value or `null`. Client checks are UX only.
5. **Output escaping** is code-style.md rule 8 (every task reads it).
6. **Passwords:** scrypt with a random salt, verified with `timingSafeEqual`. Never trimmed, logged or returned. **Sessions:** a random token in an `httpOnly` cookie, with only its sha256 stored.
7. **Files:** paths come from `lib/const/paths.ts` + sanitized segments. Never overwrite and never delete user content. **Processes:** `execFile` with an args array, never a shell, always with a timeout.
8. **Deployment values** (credentials, tokens, connection strings, IPs, ports, URLs) live only in `.env`, never hardcoded or printed. **Secrets have no default:** a missing one is logged by name and stops the server at startup; the first-admin seed variables are required only while `users` is empty. Optional non-secret settings may default to a safe, neutral value (empty `DEV_ORIGINS`). Container-internal values fixed by the image or compose design (`PORT=3000`, `DATA_DIR=/data`) are not deployment values.
9. **No sign-up or self-service password change** unless the user asks.

Details and gotchas, binding too: [details/security-management.md](details/security-management.md).

## Checklist

- [ ] Every new page, action or route runs the five steps in order; public ones say so in their header.
- [ ] Every new kind of input has a sanitizer + test. No secret field or internal path reaches the client.
- [ ] Files use a constant base + sanitized segment; processes use `execFile` with a timeout.
