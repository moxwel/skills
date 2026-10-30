"""
Item store on disk: items kept as JSON files in one folder. Reads the folder on every call instead of caching,
because other processes write to it too.
"""

import json
import os
import re

from format_bytes import format_bytes

# Folder that holds one <name>.json file per item.
ITEMS_DIR = os.environ.get("ITEMS_DIR", "./items")
# Cap on one listing, so a huge folder can't flood the caller.
MAX_LISTED_ITEMS = 500
ITEM_EXTENSION = ".json"
# Lowercase letters, digits and _, so a name is always a safe file name; 48 keeps paths short.
NAME_PATTERN = re.compile(r"^[a-z0-9_]{1,48}$")


def list_items(query: str) -> list[dict]:
    """Lists the items whose name contains `query` (all if empty), newest first, at most MAX_LISTED_ITEMS.

    :raises OSError: If the folder or an item file cannot be read (invalid JSON raises json.JSONDecodeError).
    """
    item_files = [name for name in os.listdir(ITEMS_DIR) if name.endswith(ITEM_EXTENSION)]
    items = [read_item(os.path.join(ITEMS_DIR, file_name)) for file_name in item_files]
    is_filtered = query != ""
    matching_items = [item for item in items if query in item["name"]] if is_filtered else items
    matching_items.sort(key=lambda item: item["created_at"], reverse=True)
    return matching_items[:MAX_LISTED_ITEMS]


def rename_item(name: str, new_name: str) -> bool:
    """Renames an item; returns False if the new name is invalid or already taken.

    :raises OSError: If the item does not exist or the folder is not writable.
    """
    is_valid_name = NAME_PATTERN.match(new_name) is not None
    if not is_valid_name:
        return False
    new_path = os.path.join(ITEMS_DIR, new_name + ITEM_EXTENSION)
    is_taken = os.path.exists(new_path)
    if is_taken:
        return False
    os.rename(os.path.join(ITEMS_DIR, name + ITEM_EXTENSION), new_path)
    return True


def describe_item(item: dict) -> str:
    size = format_bytes(item["size_bytes"])
    archived_label = " (archived)" if item["is_archived"] else ""
    return f"{item['name']}, {size}{archived_label}"


def read_item(path: str) -> dict:
    with open(path, encoding="utf-8") as item_file:
        return json.load(item_file)
