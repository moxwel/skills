/*
 * Item store on disk: lists, renames and describes the items kept as JSON files in one folder. Reads
 * the folder on every call instead of caching, because other processes write to it too.
 */

import { link, readdir, readFile, unlink } from "node:fs/promises";
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
 * Lists the items, newest first.
 * @param query - Text the name must contain; empty lists every item.
 * @returns At most MAX_LISTED_ITEMS items.
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
 * Renames an item if the new name is valid and free.
 * @param name - Current name.
 * @param newName - Name to give it.
 * @returns true if it renamed it; false if either name is invalid or the new name is taken.
 * @throws If the item does not exist or the folder is not writable.
 */
export async function renameItem(name: string, newName: string): Promise<boolean> {
  const areValidNames = NAME_PATTERN.test(name) && NAME_PATTERN.test(newName);
  if (!areValidNames) return false;
  const oldPath = join(ITEMS_DIR, name + ITEM_EXTENSION);
  const newPath = join(ITEMS_DIR, newName + ITEM_EXTENSION);
  // ponytail: link+unlink instead of rename so a taken name fails atomically; needs hard links
  try {
    await link(oldPath, newPath);
  } catch (error) {
    const isTaken = (error as NodeJS.ErrnoException).code === "EEXIST";
    if (isTaken) return false;
    throw error;
  }
  await unlink(oldPath);
  return true;
}

/**
 * One-line summary of an item for logs.
 * @param item - Item to describe.
 * @returns Name, size and whether it is archived.
 */
export function describeItem(item: Item): string {
  const size = formatBytes(item.size_bytes);
  const archivedLabel = item.is_archived ? " (archived)" : "";
  return `${item.name}, ${size}${archivedLabel}`;
}

/**
 * Reads and parses one item file.
 * @param path - Path of the JSON file.
 * @returns The parsed item.
 * @throws If the file is missing or is not valid JSON.
 */
async function readItem(path: string): Promise<Item> {
  const itemJson = await readFile(path, "utf8");
  return JSON.parse(itemJson) as Item;
}
