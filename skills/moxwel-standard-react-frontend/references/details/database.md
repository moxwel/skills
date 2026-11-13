# Database: details

Details and gotchas for the rules in [../database.md](../database.md).

## Details

- **Engine:** SQLite via `node:sqlite` is the default (one instance, no extra container, no ORM). Use PostgreSQL or MongoDB only for several instances, an existing database, or very large data.
- **Layout:** `lib/db/` holds `connection.ts`, `types.ts` and one file per table. Template: [dbTable.ts](../assets/dbTable.ts).
- **Return types:** row types keep the DB column names (naming.md). Convert with `plain()` for `node:sqlite` rows and `toPlain()` for Mongo `ObjectId`/`Date`.
- **Mongo injection:** `{ username: input }` with `input = { $ne: null }` matches everyone. Never use `$where`/`$function` or keys taken from user input.
- **UUID ids (rule 9):** a v4 UUID as lowercase text. In SQLite the column is `id TEXT PRIMARY KEY NOT NULL DEFAULT (<uuid v4 expression>) CHECK (length(id) = 36)`, so rows created by SQL or by the admin CRUD get one too; read the new id back with `INSERT … RETURNING id`. When the id must exist before the insert (files named after it), generate it with `crypto.randomUUID()` and pass it. A table with a `TEXT PRIMARY KEY` keeps its implicit `rowid`, which the generic CRUD can still use. The v4 expression for SQLite:

  ```sql
  lower(hex(randomblob(4))) || '-' || lower(hex(randomblob(2))) || '-4' || substr(lower(hex(randomblob(2))), 2)
    || '-' || substr('89ab', 1 + (abs(random()) % 4), 1) || substr(lower(hex(randomblob(2))), 2)
    || '-' || lower(hex(randomblob(6)))
  ```
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
| Ids from input | `cleanUuid` (entities, rule 9); `cleanId` → number for rowids and pages | `cleanUuid`; `cleanId` for technical ids | 24-hex check, `new ObjectId()` inside `lib/db` |

## Gotchas

- **"Only plain objects can be passed to Client Components".** `node:sqlite` rows have a null prototype, so pass them through `plain()`.
