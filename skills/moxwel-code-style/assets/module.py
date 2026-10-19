"""
Item store on disk: lists, renames and describes the items kept as JSON files in one folder.

Reads the folder on every call instead of caching, because other processes write to it too.
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
    """Lists the items, newest first.

    :param query: Text the name must contain; empty lists every item.
    :returns: At most MAX_LISTED_ITEMS items.
    :raises OSError: If the folder or an item file cannot be read.
    :raises json.JSONDecodeError: If an item file is not valid JSON.
    """
    item_files = [name for name in os.listdir(ITEMS_DIR) if name.endswith(ITEM_EXTENSION)]
    items = [read_item(os.path.join(ITEMS_DIR, file_name)) for file_name in item_files]
    is_filtered = query != ""
    matching_items = [item for item in items if query in item["name"]] if is_filtered else items
    matching_items.sort(key=lambda item: item["created_at"], reverse=True)
    return matching_items[:MAX_LISTED_ITEMS]


def rename_item(name: str, new_name: str) -> bool:
    """Renames an item if the new name is valid and free.

    :param name: Current name.
    :param new_name: Name to give it.
    :returns: True if it renamed it; False if either name is invalid or the new name is taken.
    :raises OSError: If the item does not exist or the folder is not writable.
    """
    are_valid_names = NAME_PATTERN.match(name) is not None and NAME_PATTERN.match(new_name) is not None
    if not are_valid_names:
        return False
    old_path = os.path.join(ITEMS_DIR, name + ITEM_EXTENSION)
    new_path = os.path.join(ITEMS_DIR, new_name + ITEM_EXTENSION)
    # ponytail: link+unlink instead of rename so a taken name fails atomically; needs hard links
    try:
        os.link(old_path, new_path)
    except FileExistsError:
        return False
    os.unlink(old_path)
    return True


def describe_item(item: dict) -> str:
    """One-line summary of an item for logs.

    :param item: Item to describe.
    :returns: Name, size and whether it is archived.
    """
    size = format_bytes(item["size_bytes"])
    archived_label = " (archived)" if item["is_archived"] else ""
    return f"{item['name']}, {size}{archived_label}"


def read_item(path: str) -> dict:
    """Reads and parses one item file.

    :param path: Path of the JSON file.
    :returns: The parsed item.
    :raises OSError: If the file is missing.
    :raises json.JSONDecodeError: If the file is not valid JSON.
    """
    with open(path, encoding="utf-8") as item_file:
        return json.load(item_file)
