# Database

Covers `lib/db`, query functions, injection safety, soft deletes, transactions, schema and connection, for SQLite (default), PostgreSQL and MongoDB.

## Rules

1. **Every query is a named function in `lib/db/<table>.ts`** (function and namespace names: [naming.md](naming.md)). Nothing outside `lib/db/` writes SQL or filters, imports the connection, or sees driver objects.
2. **Values are always parameters, never interpolated.** A dynamic identifier is allowed only after checking it against the engine catalog, and then quoted. Mongo values must be primitives of the expected type.
3. **Read only what's needed:** explicit columns or a projection, and a `LIMIT` on every list (plus offset or cursor when paginated). Secret fields never leave `lib/`. Return plain, app-typed objects.
4. **Invariants go in the filter** (`AND status = 'pending' AND deleted_at IS NULL`), and writes report whether they matched.
5. **Domain deletes are soft:** `softDelete<Thing>(id)` sets `deleted_at`, and every read, joins included, filters `deleted_at IS NULL` (Mongo: [details](details/database.md)). A real `DELETE` is only for technical data (sessions, caches), justified in the file header.
6. **All-or-nothing writes are one transaction inside one `lib/db` function,** even across tables. File side effects are ordered or compensated, since the transaction doesn't cover them.
7. **Expected outcomes are return values** (a duplicate makes `insert*` return `false`). Catch only the specific expected error code and rethrow everything else.
8. **The schema constrains too:** `NOT NULL`, `UNIQUE`, `CHECK`, foreign keys (Mongo: unique indexes, `$jsonSchema`). Dates are stored in UTC.
9. **Entities tied to a user or made public are identified by a UUID, never by an ascending number,** unless the user explicitly asks for numbers: users, their content (posts, files, clips, collections) and anything whose id reaches a URL, an embed or another user. The UUID is the primary key and every foreign key uses it. Integers stay for technical data (sessions keyed by token, rowids, page numbers).

Details and gotchas, binding too: [details/database.md](details/database.md).

## Checklist

- [ ] No SQL, driver or `connection` import outside `lib/db/`.
- [ ] Parameters only, explicit columns, invariants in the filter, writes report a match.
- [ ] Domain deletes are soft, and multi-writes are one transaction.
- [ ] Users, their content and anything public use UUID primary and foreign keys (unless numbers were asked for).
