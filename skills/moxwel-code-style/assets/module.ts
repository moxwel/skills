/*
 * Item store on disk: items kept as JSON files in one folder. Reads the folder on every call instead of caching,
 * because other processes write to it too.
 */

import { readdir, readFile, rename } from "node:fs/promises";
import { join } from "node:path";

import { formatBytes } from "./formatBytes";

import type { Item } from "./types";

/** Folder that holds one <name>.json file per item; Item keeps the file's snake_case keys. */
const ITEMS_DIR = process.env.ITEMS_DIR ?? "./items";
/** Cap on one listing, so a huge folder can't flood the caller. */
const MAX_LISTED_ITEMS = 500;
const ITEM_EXTENSION = ".json";
/** Lowercase letters, digits and _, so a name is always a safe file name; 48 keeps paths short. */
const NAME_PATTERN = /^[a-z0-9_]{1,48}$/;

/**
 * Lists the items whose name contains `query` (all if empty), newest first, at most MAX_LISTED_ITEMS.
 * @throws If the folder or an item file cannot be read or parsed.
 */
export async function listItems(query: string): Promise<Item[]> {
  const fileNames = await readdir(ITEMS_DIR);
  const itemFiles = fileNames.filter((fileName) => fileName.endsWith(ITEM_EXTENSION));
  const items = await Promise.all(itemFiles.map((fileName) => readItem(join(ITEMS_DIR, fileName))));
  const isFiltered = query !== "";
  const matchingItems = isFiltered ? items.filter((item) => item.name.includes(query)) : items;
  const newestItems = matchingItems.sort((first, second) => second.created_at - first.created_at);
  return newestItems.slice(0, MAX_LISTED_ITEMS);
}

/**
 * Renames an item; returns false if the new name is invalid or already taken.
 * @throws If the item does not exist or the folder is not writable.
 */
export async function renameItem(name: string, newName: string): Promise<boolean> {
  const isValidName = NAME_PATTERN.test(newName);
  if (!isValidName) return false;
  const fileNames = await readdir(ITEMS_DIR);
  const isTaken = fileNames.includes(newName + ITEM_EXTENSION);
  if (isTaken) return false;
  await rename(join(ITEMS_DIR, name + ITEM_EXTENSION), join(ITEMS_DIR, newName + ITEM_EXTENSION));
  return true;
}

export function describeItem(item: Item): string {
  const size = formatBytes(item.size_bytes);
  const archivedLabel = item.is_archived ? " (archived)" : "";
  return `${item.name}, ${size}${archivedLabel}`;
}

async function readItem(path: string): Promise<Item> {
  const itemJson = await readFile(path, "utf8");
  return JSON.parse(itemJson) as Item;
}
