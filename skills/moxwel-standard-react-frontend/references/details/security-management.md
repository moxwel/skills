# Security: details

Details and gotchas for the rules in [../security-management.md](../security-management.md).

## Details

```ts
/**
 * Deletes (soft delete) an item the user owns, or any item for an admin.
 * @param itemId - Item UUID from the client; sanitized here.
 * @returns `ok` with the toast message, or `error` if it is invalid, missing or not theirs.
 */
export async function deleteItem(itemId: string): Promise<ActionState> {
  const session = await requireUser();
  const id = cleanUuid(String(itemId));
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
| UUID id (users and their content, database.md rule 9) | lowercase v4, `^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$` |
| list of UUIDs | an array of strings, each a UUID, deduplicated, with a length cap |
| numeric id (rowid, page) | `^[1-9]\d{0,14}$`, then `Number()` |
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
