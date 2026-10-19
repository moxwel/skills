# Database

Covers `lib/db`, query functions, injection safety, soft deletes, transactions, schema and connection, for SQLite (default), PostgreSQL and MongoDB.

## Rules

1. **Every query is a named function in `lib/db/<table>.ts`** (`listUsers()`, `softDeleteItem(id)`), imported as a namespace (`import * as itemsDb`). Nothing outside `lib/db/` writes SQL or filters, imports the connection, or sees driver objects.
2. **Values are always parameters, never interpolated.** A dynamic identifier is allowed only after checking it against the engine catalog, and then quoted. Mongo values must be primitives of the expected type.
3. **Read only what's needed:** explicit columns or a projection, and a `LIMIT` on every list (plus offset or cursor when paginated). Secret fields never leave `lib/`. Return plain, app-typed objects.
4. **Invariants go in the filter** (`AND status = 'pending' AND deleted_at IS NULL`), and writes report whether they matched.
5. **Domain deletes are soft:** `softDelete<Thing>(id)` sets `deleted_at`, and every read, joins included, filters `deleted_at IS NULL` (Mongo: Details). A real `DELETE` is only for technical data (sessions, caches), justified in the file header.
6. **All-or-nothing writes are one transaction inside one `lib/db` function,** even across tables. File side effects are ordered or compensated, since the transaction doesn't cover them.
7. **Expected outcomes are return values** (a duplicate makes `insert*` return `false`). Catch only the specific expected error code and rethrow everything else.
8. **The schema constrains too:** `NOT NULL`, `UNIQUE`, `CHECK`, foreign keys (Mongo: unique indexes, `$jsonSchema`). Dates are stored in UTC.

## Details

- **Engine:** SQLite via `node:sqlite` is the default (one instance, no extra container, no ORM). Use PostgreSQL or MongoDB only for several instances, an existing database, or very large data.
- **Layout:** `lib/db/` holds `connection.ts`, `types.ts` and one file per table. Template: [dbTable.ts](../assets/dbTable.ts).
- **Function names:** verb + subject. `list*`, `find*`/`get*` (one result or `undefined`), `count*`, `insert*`, `update*`/`mark*`, `softDelete*`, and `delete*` for technical data only.
- **Return types:** row types keep the DB column names (`created_at`). Convert with `plain()` for `node:sqlite` rows and `toPlain()` for Mongo `ObjectId`/`Date`.
- **Mongo injection:** `{ username: input }` with `input = { $ne: null }` matches everyone. Never use `$where`/`$function` or keys taken from user input.
- **Unique among active rows only:** `CREATE UNIQUE INDEX … WHERE deleted_at IS NULL` (Mongo: `isDeleted` + `deletedAt` instead of `deleted_at`; reads filter `isDeleted: false`, and the unique index uses `partialFilterExpression`).
- **Transactions:** keep them short (no network or file I/O inside). Any error rolls back and rethrows. Example: `setUserPasswordAndCloseSessions`.
- **Schema changes:** SQLite uses `CREATE TABLE IF NOT EXISTS` on first open with no migrations; changes to an existing deployment are documented manual steps. PostgreSQL uses versioned migrations.
- **Connection:** one lazy connection per process, never opened during `next build`, cached on `globalThis`.

| | SQLite (`node:sqlite`) | PostgreSQL (`pg`) | MongoDB |
|---|---|---|---|
| Connection | `new DatabaseSync(file)`, `PRAGMA journal_mode = WAL; foreign_keys = ON` | `Pool` from `DATABASE_URL` | `MongoClient` from `MONGODB_URI` |
| Parameters | `?` | `$1, $2` | filter object, `$eq` for untrusted |
| Transaction | `exec("BEGIN")`/`COMMIT`/`ROLLBACK` | `BEGIN`…`COMMIT` on **the same** `pool.connect()` client, `release()` in `finally` | `session.withTransaction()` (needs a replica set) |
| Unique violation | `errcode === 2067` | `code === "23505"` | `code === 11000` |
| Did it match | `run().changes` | `rowCount` | `modifiedCount`/`matchedCount` |
| Ids from input | `cleanId` → number | `cleanId` or UUID check | 24-hex check, `new ObjectId()` inside `lib/db` |

## Gotchas

- **"Only plain objects can be passed to Client Components".** `node:sqlite` rows have a null prototype, so pass them through `plain()`.

## Checklist

- [ ] No SQL, driver or `connection` import outside `lib/db/`.
- [ ] Parameters only, explicit columns, invariants in the filter, writes report a match.
- [ ] Domain deletes are soft, and multi-writes are one transaction.
