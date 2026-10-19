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
5. **Output escaping** is code-style.md rule 15 (every task reads it).
6. **Passwords:** scrypt with a random salt, verified with `timingSafeEqual`. Never trimmed, logged or returned. **Sessions:** a random token in an `httpOnly` cookie, with only its sha256 stored.
7. **Files:** paths come from `lib/const/paths.ts` + sanitized segments. Never overwrite and never delete user content. **Processes:** `execFile` with an args array, never a shell, always with a timeout.
8. **Deployment values** (credentials, tokens, connection strings, IPs, ports, URLs) live only in `.env`, never hardcoded or printed. **Secrets have no default:** a missing one is logged by name and stops the server at startup; the first-admin seed variables are required only while `users` is empty. Optional non-secret settings may default to a safe, neutral value (empty `DEV_ORIGINS`). Container-internal values fixed by the image or compose design (`PORT=3000`, `DATA_DIR=/data`) are not deployment values.
9. **No sign-up or self-service password change** unless the user asks.

## Details

```ts
/**
 * Deletes (soft delete) an item the user owns, or any item for an admin.
 * @param itemId - Item id from the client; sanitized here.
 * @returns `ok` with the toast message, or `error` if it is invalid, missing or not theirs.
 */
export async function deleteItem(itemId: number): Promise<ActionState> {
  const session = await requireUser();
  const id = cleanId(String(itemId));
  if (!id) return { error: "Invalid item." };
  // Same message whether it doesn't exist or isn't theirs, so it reveals nothing
  const item = itemsDb.getItem(id);
  const canDelete = item !== undefined && (item.owner_id === session.userId || session.isAdmin);
  if (!canDelete) return { error: "Item not found." };
  const wasDeleted = itemsDb.softDeleteItem(id);
  if (!wasDeleted) return { error: "Item not found." };
  refresh();
  return { ok: `Item ${item.name} deleted.` };
}
```

- **Untrusted input:** form fields, action args (any client can call any action with any payload), route params, query strings, cookies, headers, uploads, and names on disk or in the DB. `lib/` trusts typed args, so raw input never reaches it.
- **Auth helpers:** `requireUser()` returns the session or redirects to `PAGES.login`. `requireAdmin()` calls it and redirects non-admins home. `getSession()` is memoized per request with React `cache()`.
- **Route handlers:** answer 401/403/400/404 (no redirects), set an explicit `Content-Type`, and use `Cache-Control: private, no-store` for private data.
- **Errors** carry no stack traces, queries, paths or command lines. Log the details on the server.
- **Sessions:**
  - The token is `randomBytes(32).toString("base64url")` in a `sameSite: "lax"` cookie.
  - Expired sessions are deleted opportunistically.
  - Changing a password or soft-deleting a user closes that user's sessions in the same transaction.
- **Roles:**
  - An admin is a `users` row with `role = 'admin'` (CHECK constraint, `cleanRole` sanitizer).
  - The role is read on every request, so changes apply at once.
  - Nobody can delete their own account or drop their own admin role.
- **First admin:** seeded by `register()` in `src/instrumentation.ts` (guarded by `process.env.NEXT_RUNTIME === "nodejs"`) from `ADMIN_USER`/`ADMIN_PASSWORD`, only while `users` is empty.
- **Login:**
  - The error message is generic.
  - Failures are rate-limited in memory per IP **and** per username, because `X-Forwarded-For` can be forged.
  - Count the attempt before running scrypt, and cap the map size.
- **Validation patterns.** Errors are keyed by field `name` and say what *is* valid. Tests cover valid, edge and hostile input (`..`, `/`, unicode, empty, too long).

| Input | Pattern |
|---|---|
| any `FormData` field | `str(value)`: a missing field or `File` gives `""` |
| username | trim, `^[a-zA-Z0-9_.-]{3,32}$` |
| password | **no trim**, length 8–128 |
| file/folder name | lowercase, spaces → `_`, `^[a-z0-9_]{1,48}$` |
| numeric id | `^[1-9]\d{0,14}$`, then `Number()` |
| enum | value must be in the const list |

- **Files:**
  - Uploads are stored as `<id>.<ext>`.
  - Move with a `COPYFILE_EXCL` copy + `unlink`; rejected files go to `rejected/`.
  - Processes also use fixed paths and `maxBuffer`. User input is only ever a sanitized value, never a flag.
- **Uploads:**
  - Set `experimental.serverActions.bodySizeLimit` just above the limit and re-check size in the action.
  - Probe the real format (`ffprobe`) against an allow-list and force it.
  - Run with `-protocol_whitelist file` and cap the output.
- **Optional settings with a default** use a named constant: `process.env.X ?? NAMED_DEFAULT`.

## Gotchas

- **`redirect()`/`requireUser()` inside `try/catch`:** the catch swallows the navigation. Call them outside.
- **Login works on HTTPS but not on LAN HTTP.** Set the cookie's `secure` only when `x-forwarded-proto === "https"`.
- **`validate.ts` imports nothing,** because `node --test` runs it bare. It keeps its own copy of the enums and limits it checks, each commented with its source.

## Checklist

- [ ] Every new page, action or route runs the five steps in order; public ones say so in their header.
- [ ] Every new kind of input has a sanitizer + test. No secret field or internal path reaches the client.
- [ ] Files use a constant base + sanitized segment; processes use `execFile` with a timeout.
