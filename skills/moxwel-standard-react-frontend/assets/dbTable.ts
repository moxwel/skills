/*
 * Queries for the items table (TEMPLATE for lib/db/<table>.ts, SQLite version with node:sqlite; for Postgres or Mongo
 * the placeholders, error codes and conversion change). Each item has an owner (owner_id, reference to users). Each
 * function is a single named operation; nobody outside lib/db/ writes SQL. Justified exception to "one export per
 * file": many small functions on the same table. Soft delete: items are never deleted, they are marked with deleted_at
 * and every read filters them out. The name is unique only among active items (partial index
 * `CREATE UNIQUE INDEX items_name_active ON items(name) WHERE deleted_at IS NULL`), so a deleted name can be reused.
 * Imported as a namespace (`import * as itemsDb`).
 */

import { db, plain } from "./connection";
import type { ItemRow } from "./types";

/** SQLite errcode for a UNIQUE violation (SQLITE_CONSTRAINT_UNIQUE); found in error.errcode */
const SQLITE_CONSTRAINT_UNIQUE = 2067;

/** List cap: the query never returns an unbounded amount */
const MAX_LISTED_ITEMS = 200;

/**
 * Active items.
 * @returns Up to MAX_LISTED_ITEMS, newest first, as plain objects for the UI; [] if there are none.
 */
export function listItems(): ItemRow[] {
  const rows = db()
    .prepare(
      "SELECT id, name, owner_id, created_at FROM items WHERE deleted_at IS NULL ORDER BY id DESC LIMIT ?",
    )
    .all(MAX_LISTED_ITEMS);
  return plain<ItemRow>(rows);
}

/**
 * One active item by id.
 * @param id - Item id.
 * @returns The item, or undefined if it does not exist or is deleted.
 */
export function getItem(id: number): ItemRow | undefined {
  const row = db()
    .prepare("SELECT id, name, owner_id, created_at FROM items WHERE id = ? AND deleted_at IS NULL")
    .get(id);
  return row ? plain<ItemRow>([row])[0] : undefined;
}

/**
 * Inserts an item on behalf of its owner.
 * @param name - Already sanitized name.
 * @param ownerId - Owner user id.
 * @returns true if inserted; false if an active item with that name already exists (UNIQUE).
 * @throws If the DB fails for something other than the UNIQUE constraint.
 */
export function insertItem(name: string, ownerId: number): boolean {
  try {
    db().prepare("INSERT INTO items (name, owner_id) VALUES (?, ?)").run(name, ownerId);
    return true;
  } catch (error) {
    const isDuplicate = (error as { errcode?: number }).errcode === SQLITE_CONSTRAINT_UNIQUE;
    if (isDuplicate) return false;
    throw error;
  }
}

/**
 * Marks the item as deleted (soft delete); the row is kept.
 * @param id - Item id.
 * @returns true if marked; false if it does not exist or was already deleted.
 */
export function softDeleteItem(id: number): boolean {
  const result = db()
    .prepare("UPDATE items SET deleted_at = CURRENT_TIMESTAMP WHERE id = ? AND deleted_at IS NULL")
    .run(id);
  return result.changes > 0;
}
