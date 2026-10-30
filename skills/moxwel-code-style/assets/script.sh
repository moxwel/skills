#!/bin/bash
#
# Copies every item in items/ to backup/, keeping each source mtime so later runs can tell which files changed.
# Never deletes from backup/: a file removed from items/ stays there.
#
# Status of each file:
#   [NEW]  missing in backup/ -> copied
#   [SKIP] same as in backup/ -> skipped (only shown with --verbose)
#   [MOD]  differs from backup/ -> reported, left alone
#   [UPD]  modified file copied (with --update)
#
# Usage:
#   ./sync_items.sh              (copies only new files)
#   ./sync_items.sh --update     (also replaces modified files)
#   ./sync_items.sh --verbose    (also shows skipped files)
#

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SOURCE_DIR="$SCRIPT_DIR/items"
BACKUP_DIR="$SCRIPT_DIR/backup"

SHOULD_UPDATE=0
IS_VERBOSE=0
for arg in "$@"; do
    case "$arg" in
        --update)  SHOULD_UPDATE=1 ;;
        --verbose) IS_VERBOSE=1 ;;
        *)
            echo "Usage: $0 [--update] [--verbose]"
            exit 1
            ;;
    esac
done

# Compares size + mtime first (fast), then the contents.
is_same_file() {
    local source="$1"
    local destination="$2"
    local source_stat destination_stat
    source_stat="$(stat -c '%s %Y' "$source")"
    destination_stat="$(stat -c '%s %Y' "$destination")"
    if [ "$source_stat" = "$destination_stat" ]; then
        return 0
    fi
    cmp -s "$source" "$destination"
}

# Copies a new file to the backup (a modified one only with --update) and prints its status.
sync_file() {
    local name="$1"
    local source="$SOURCE_DIR/$name"
    local destination="$BACKUP_DIR/$name"
    if [ ! -e "$destination" ]; then
        cp --preserve=timestamps "$source" "$destination"
        echo "[NEW]  $name"
        return
    fi
    if is_same_file "$source" "$destination"; then
        if [ "$IS_VERBOSE" -eq 1 ]; then
            echo "[SKIP] $name"
        fi
        return
    fi
    if [ "$SHOULD_UPDATE" -eq 1 ]; then
        cp --preserve=timestamps "$source" "$destination"
        echo "[UPD]  $name"
        return
    fi
    echo "[MOD]  $name"
}

if [ ! -d "$SOURCE_DIR" ]; then
    echo "ERROR: folder '$SOURCE_DIR' not found"
    exit 1
fi
mkdir -p "$BACKUP_DIR"

for path in "$SOURCE_DIR"/*; do
    if [ -f "$path" ]; then
        sync_file "$(basename "$path")"
    fi
done
