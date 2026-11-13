"""
Scenarios of the skill tests: the files each session starts with, its prompt and the skill files it must read.
The check of a scenario lives in checks.py, registered in CHECKS under the same name.
"""

# Starting files of the scenarios. legacy.ts and store.py break rules on purpose: a session must leave
# those lines exactly as they are, so do not fix them here either.
CONFIG_TS = """\
/*
 * config.ts: limits for the item list.
 */

const MAX_ITEMS = 50
const PAGE_SIZE = 10
"""
SETTINGS_TS = """\
/*
 * settings.ts: settings of the item list view.
 */

export const listSettings = {
    id:      "itemList",
    enabled: true,
}
"""
REPORT_TS = """\
/*
 * report.ts: builds the storage report for one folder.
 */

import { readdirSync } from "node:fs"

import { formatBytes } from "./formatBytes"

export function describeFolder(folder: string): string {
    const fileCount = readdirSync(folder).length
    return `${folder}: ${fileCount} files, ${formatBytes(0)}`
}
"""
FORMAT_BYTES_TS = """\
/*
 * formatBytes.ts: human readable byte counts.
 */

export function formatBytes(bytes: number): string {
    return `${bytes} B`
}
"""
TYPES_TS = """\
/*
 * types.ts: shared report types.
 */

export type FolderStats = { folder: string; totalBytes: number }
"""
SLUGS_TS = """\
/*
 * slugs.ts: slug helpers for items.
 */

export type Item = { slug: string; deletedAt: string | null }
"""
STORE_PY = '''\
"""
Review store: review status of items kept in memory.
"""

PENDING = "pending"
REVIEWED = "reviewed"

statuses: dict[str, str] = {}
'''
REVIEWS_TS = """\
/*
 * In-memory review status of items.
 */

export type ReviewStatus = "pending" | "reviewed"

const statuses = new Map<string, ReviewStatus>()
"""
LEGACY_TS = """\
/*
 * legacy.ts: legacy.ts file for item totals.
 */

const TAX = 0.19
const SHIPPING = 5

export function total(items: { price: number; qty: number }[]): number {
    let t = 0
    for (const x of items) {
        if (x.qty > 0) t += x.price * x.qty  // Add the price.
    }
    return t * (1 + TAX) + SHIPPING
}
"""
PACKAGE_JSON = """\
{
  "name": "items-app",
  "private": true,
  "dependencies": {
    "next": "15.5.0",
    "react": "19.1.0",
    "react-dom": "19.1.0",
    "@base-ui-components/react": "1.0.0",
    "tailwindcss": "4.1.0"
  }
}
"""
PAGE_TSX = """\
/*
 * Home page: lists the items.
 */

const ITEMS = ["Keyboard", "Mouse"];

export default function HomePage() {
  return (
    <main>
      <h1>Items</h1>
    </main>
  );
}
"""

# One entry per scenario: the files the session starts with, the prompt, and what it must read on top of
# BASE_REFERENCES (session_log.py). "details" and "references" name files of the base skill; "react" names
# references of the React skill and also requires that skill to load.
SCENARIOS = {
    "align": {
        "files":  {"config.ts": CONFIG_TS},
        "prompt": "In config.ts add a constant for the request timeout in milliseconds (5000) and one for the "
                  "retry count (3).",
        "details": [],
    },
    "cut": {
        "files":   {"settings.ts": SETTINGS_TS},
        "prompt":  "In settings.ts add two fields to listSettings: showArchivedItems (false) and limit (50).",
        "details": [],
    },
    "cut2": {
        "files":  {},
        "prompt": "Create limits.ts with these module constants, in this order: API_URL (https://api.example.com), "
                  "REQUEST_TIMEOUT_SEC (10), MAX_ATTEMPTS (4) and TTL_SEC (60).",
        "details": [],
    },
    "imports": {
        "files":  {"report.ts": REPORT_TS, "formatBytes.ts": FORMAT_BYTES_TS, "types.ts": TYPES_TS},
        "prompt": "In report.ts add an exported function that returns a FolderStats (from ./types) for a folder: "
                  "sum the sizes of its files using statSync from node:fs and join from node:path.",
        "details": [],
    },
    "robust": {
        "files":  {},
        "prompt": "Write items_client.py: a function that downloads the item list from "
                  "https://api.example.com/items with requests and returns it as a list of dicts. "
                  "The API is flaky and sometimes rate limits.",
        "details":    ["comments-and-docs", "naming", "readability"],
        "references": ["robustness"],
    },
    "naming": {
        "files":  {"slugs.ts": SLUGS_TS},
        "prompt": "In slugs.ts add a function that tells whether a slug is already used by a non deleted item in a "
                  "list, and a function that turns a title into a slug (lowercase, spaces to dashes, max 40 chars).",
        "details": [],
    },
    "doc": {
        "files":  {"store.py": STORE_PY},
        "prompt": "In store.py add a function that marks an item as reviewed if it is still pending, "
                  "and tells the caller whether it did.",
        "details": ["comments-and-docs", "naming", "readability"],
    },
    "bash": {
        "files":  {},
        "prompt": "Write sync_folder.sh: copies every file from a source folder to a destination folder (both given "
                  "as arguments) with rsync, and does nothing when both are the same folder or the source does not "
                  "exist.",
        "details": ["comments-and-docs", "naming", "readability"],
    },
    "tsdoc": {
        "files":  {"reviews.ts": REVIEWS_TS},
        "prompt": "In reviews.ts add a function that marks an item as reviewed if it is still pending, "
                  "and tells the caller whether it did.",
        "details": [],
    },
    "mindiff": {
        "files":   {"legacy.ts": LEGACY_TS},
        "prompt":  "In legacy.ts add an exported function that returns how many items have a quantity of zero.",
        "details": [],
    },
    "react": {
        "files":  {"package.json": PACKAGE_JSON, "app/page.tsx": PAGE_TSX},
        "prompt": "Add an ItemCount component that shows how many items there are (or a message when there are "
                  "none), with its own styles, and use it in the home page.",
        "details": [],
        "react":   ["code-style", "components", "naming", "semantic-html", "styling", "workflow-and-verification"],
    },
}

# Scenarios whose starting files hold unaligned assignments that must stay as they are.
UNALIGNED_START_SCENARIOS = ("doc", "mindiff", "cut")
# Scenarios whose starting file headers are compared with the output.
HEADER_SCENARIOS = ("naming", "imports", "cut")
