/*
 * TEMPLATE for lib/db/<table>.ts (SQLite): many small queries on one table, hence several exports. Soft delete via
 * deleted_at; the name is unique only among active items (partial index), so a deleted name can be reused.
 */

import { db, plain } from "./connection";
import type { ItemRow } from "./types";

const SQLITE_CONSTRAINT_UNIQUE = 2067;

const MAX_LISTED_ITEMS = 200;

/** Active items, newest first, up to MAX_LISTED_ITEMS, as plain objects for the UI. */
export function listItems(): ItemRow[] {
  const rows = db()
    .prepare(
      // UUIDs carry no order: newest first goes by date, with rowid breaking ties
      `SELECT id, name, owner_id, created_at FROM items WHERE deleted_at IS NULL
       ORDER BY created_at DESC, rowid DESC LIMIT ?`,
    )
    .all(MAX_LISTED_ITEMS);
  return plain<ItemRow>(rows);
}

/** The active item, or undefined if it does not exist or is deleted. */
export function getItem(id: string): ItemRow | undefined {
  const row = db()
    .prepare("SELECT id, name, owner_id, created_at FROM items WHERE id = ? AND deleted_at IS NULL")
    .get(id);
  return row ? plain<ItemRow>([row])[0] : undefined;
}

/**
 * Inserts an item for its owner and returns its UUID, or null if an active item with that name already exists.
 * @throws If the DB fails for something other than the UNIQUE constraint.
 */
export function insertItem(name: string, ownerId: string): string | null {
  try {
    const row = db()
      .prepare("INSERT INTO items (name, owner_id) VALUES (?, ?) RETURNING id")
      .get(name, ownerId) as { id: string };
    return row.id;
  } catch (error) {
    const isDuplicate = (error as { errcode?: number }).errcode === SQLITE_CONSTRAINT_UNIQUE;
    if (isDuplicate) return null;
    throw error;
  }
}

/** Soft-deletes the item (the row is kept); false if it does not exist or was already deleted. */
export function softDeleteItem(id: string): boolean {
  const result = db()
    .prepare("UPDATE items SET deleted_at = CURRENT_TIMESTAMP WHERE id = ? AND deleted_at IS NULL")
    .run(id);
  return result.changes > 0;
}
