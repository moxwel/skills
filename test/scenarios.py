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
PARSE_IMPORT_TS = """\
/*
 * parseImport.ts: parses the rows of an item import file.
 */

const MAX_IMPORT_ROWS = 500;

export function parseImport(text: string): string[] {
  const rows      = text.split("\\n").filter((row) => row.trim() !== "");
  const isTooLong = rows.length > MAX_IMPORT_ROWS;
  if (isTooLong) {
    throw new Error(`An import holds at most ${MAX_IMPORT_ROWS} rows.`);
  }
  return rows;
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

LAYOUT_TSX = """\
/*
 * Root layout: html shell of every page.
 */

import "./globals.css";

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
"""
ITEMS_DB_TS = """\
/*
 * Items table: queries of the items owned by users.
 */

import { db } from "./connection";

export type Item = { id: string; name: string; ownerId: string };

/** Returns the item, or null when it does not exist or was deleted. */
export function getItem(itemId: string): Item | null {
  return db.prepare(
    "SELECT id, name, owner_id AS ownerId FROM items WHERE id = ? AND deleted_at IS NULL",
  ).get(itemId) ?? null;
}

/** @returns false when no live item of that owner matched. */
export function softDeleteItem(itemId: string, ownerId: string): boolean {
  const result = db.prepare(
    "UPDATE items SET deleted_at = datetime('now') WHERE id = ? AND owner_id = ? AND deleted_at IS NULL",
  ).run(itemId, ownerId);
  return result.changes > 0;
}
"""
REQUIRE_USER_TS = """\
/*
 * requireUser: the session of the logged-in user, or a redirect to the login page.
 */

export type Session = { userId: string };

export async function requireUser(): Promise<Session> {
  return { userId: "placeholder" };
}
"""
ACTION_TYPES_TS = """\
/*
 * Shared types of the server actions.
 */

export type ActionState = { ok?: string; errors?: Record<string, string> };
"""
TSCONFIG_JSON = """\
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "esnext",
    "strict": false
  }
}
"""
SLUGIFY_TS = """\
/*
 * slugify.ts: turns item titles into URL slugs.
 */

const MAX_SLUG_LENGTH = 40

/** Lowercases the title, turns spaces into dashes and cuts it to MAX_SLUG_LENGTH characters. */
export function slugify(title: string): string {
    return title.toLowerCase().trim().replace(/\\s+/g, "-").slice(0, MAX_SLUG_LENGTH)
}
"""
CHANGE_DIFF = """\
diff --git a/slugify.ts b/slugify.ts
--- a/slugify.ts
+++ b/slugify.ts
@@ -9,5 +9,5 @@
 export function slugify(title: string): string {
-    return title.toLowerCase().replace(/ /g, "-").slice(0, MAX_SLUG_LENGTH)
+    return title.toLowerCase().trim().replace(/\\s+/g, "-").slice(0, MAX_SLUG_LENGTH)
 }
"""
SLUGIFY_OLD_TS = SLUGIFY_TS.replace(".trim().replace(/\\s+/g", ".replace(/ /g")
ORDERS_TS      = """\
export type OrderLine = { price: number; quantity: number }

const TAX_RATE      = 0.19
const SHIPPING_COST = 5

export function orderTotal(lines: OrderLine[]): number {
    const isEmpty = lines.length === 0
    if (isEmpty) {
        return 0
    }
    const subtotal = lines.reduce((sum, line) => sum + lineTotal(line), 0)
    const taxed    = subtotal * (1 + TAX_RATE)
    return taxed + SHIPPING_COST
}

function lineTotal(line: OrderLine): number {
    return line.price * line.quantity
}
"""
ITEM_LIST_TSX = """\
type Props = { items: string[] };

export function ItemList({ items }: Props) {
  return (
    <ul>
      {items.map((item) => <ItemRow key={item} name={item} />)}
    </ul>
  );
}

type ItemRowProps = { name: string };

function ItemRow({ name }: ItemRowProps) {
  return <li>{name}</li>;
}
"""
NARROW_CLAUDE_MD = """\
# Project conventions

- Lines are at most 80 columns: wrap longer ones.
"""

# One entry per scenario: the files the session starts with, the prompt, and what it must read on top of
# BASE_REFERENCES (session_log.py). "references" names files of the base skill; "react" names
# references of the React skill and also requires that skill to load. "base": False drops BASE_REFERENCES for
# tasks that write no code, and "skill": False expects the session to read no reference of the base skill
# (loading its SKILL.md alone is allowed). "git": True commits "files" to a fresh repository before the session,
# "changes" are written after that commit, and "tools" are allowed on top of the read-only ones.
SCENARIOS = {
    "align": {
        "files":  {"config.ts": CONFIG_TS},
        "prompt": "In config.ts add a constant for the request timeout in milliseconds (5000) and one for the "
                  "retry count (3).",
    },
    "cut": {
        "files":   {"settings.ts": SETTINGS_TS},
        "prompt":  "In settings.ts add two fields to listSettings: showArchivedItems (false) and limit (50).",
    },
    "cut2": {
        "files":  {},
        "prompt": "Create limits.ts with these module constants, in this order: API_URL (https://api.example.com), "
                  "REQUEST_TIMEOUT_SEC (10), MAX_ATTEMPTS (4) and TTL_SEC (60).",
    },
    "imports": {
        "files":  {"report.ts": REPORT_TS, "formatBytes.ts": FORMAT_BYTES_TS, "types.ts": TYPES_TS},
        "prompt": "In report.ts add an exported function that returns a FolderStats (from ./types) for a folder: "
                  "sum the sizes of its files using statSync from node:fs and join from node:path.",
    },
    "robust": {
        "files":  {},
        "prompt": "Write items_client.py: a function that downloads the item list from "
                  "https://api.example.com/items with requests and returns it as a list of dicts. "
                  "The API is flaky and sometimes rate limits.",
        "references": ["robustness"],
    },
    "naming": {
        "files":  {"slugs.ts": SLUGS_TS},
        "prompt": "In slugs.ts add a function that tells whether a slug is already used by a non deleted item in a "
                  "list, and a function that turns a title into a slug (lowercase, spaces to dashes, max 40 chars).",
    },
    "doc": {
        "files":  {"store.py": STORE_PY},
        "prompt": "In store.py add a function that marks an item as reviewed if it is still pending, "
                  "and tells the caller whether it did. Document it.",
    },
    "bash": {
        "files":  {},
        "prompt": "Write sync_folder.sh: copies every file from a source folder to a destination folder (both given "
                  "as arguments) with rsync, and does nothing when both are the same folder or the source does not "
                  "exist. Document its usage in a header.",
    },
    "tsdoc": {
        "files":  {"reviews.ts": REVIEWS_TS},
        "prompt": "In reviews.ts add a function that marks an item as reviewed if it is still pending, "
                  "and tells the caller whether it did. Document it.",
    },
    "mindiff": {
        "files":   {"legacy.ts": LEGACY_TS},
        "prompt":  "In legacy.ts add an exported function that returns how many items have a quantity of zero.",
    },
    "react": {
        "files":  {"package.json": PACKAGE_JSON, "app/page.tsx": PAGE_TSX},
        "prompt": "Add an ItemCount component that shows how many items there are (or a message when there are "
                  "none), with its own styles, and use it in the home page.",
        "react":   ["code-style", "components", "naming", "project-structure", "semantic-html", "styling",
                    "user-experience", "workflow-and-verification"],
    },
    "action": {
        "files":  {"package.json": PACKAGE_JSON, "lib/db/items.ts": ITEMS_DB_TS,
                   "lib/auth/requireUser.ts": REQUIRE_USER_TS, "actions/types.ts": ACTION_TYPES_TS},
        "prompt": "Add a server action that deletes an item by its id for the logged-in user.",
        "react":   ["code-style", "database", "naming", "project-structure", "security-management",
                    "workflow-and-verification"],
    },
    "const": {
        "files":  {"package.json": PACKAGE_JSON, "lib/imports/parseImport.ts": PARSE_IMPORT_TS},
        "prompt": "Add lib/imports/countImportBatches.ts with a function that says how many batches of the "
                  "maximum import size a list of row counts needs.",
        "react":   ["code-style", "naming", "project-structure", "workflow-and-verification"],
    },
    "metadata": {
        "files":  {"package.json": PACKAGE_JSON, "app/page.tsx": PAGE_TSX, "app/layout.tsx": LAYOUT_TSX},
        "prompt": "When someone shares the home page link on WhatsApp or Slack it shows a bare URL. Make it show a "
                  "proper preview. The site lives at the URL in the SITE_URL environment variable.",
        "react":   ["code-style", "naming", "social-metadata", "workflow-and-verification"],
    },
    "config": {
        "files":   {"tsconfig.json": TSCONFIG_JSON},
        "prompt":  "In tsconfig.json turn on strict mode.",
        "skill":   False,
    },
    "question": {
        "files":   {"legacy.ts": LEGACY_TS},
        "prompt":  "What does the total function in legacy.ts return? Do not change anything.",
        "skill":   False,
    },
    "override": {
        "files":  {"CLAUDE.md": NARROW_CLAUDE_MD},
        "prompt": "Create links.ts with an exported function that builds the share URL of an item from the site base "
                  "URL, the item slug, the UTM source, the UTM medium and the UTM campaign.",
    },
    "nowrap": {
        "files":  {},
        "prompt": "Create links.ts with an exported function that builds the share URL of an item from the site base "
                  "URL, the item slug, the UTM source, the UTM medium and the UTM campaign.",
    },
    "audit": {
        "files":      {"legacy.ts": LEGACY_TS},
        "prompt":     "Does legacy.ts follow my conventions?",
        "references": ["robustness"],
    },
    "copy": {
        "files":   {},
        "prompt":  "Create itemMessages.ts exporting the UI texts of the item list: the empty state, the loading "
                   "message, the error shown when loading fails, and the label of the button that creates an item.",
    },
    "readme": {
        "files":      {"slugify.ts": SLUGIFY_TS},
        "prompt":     "Write a README.md for this folder that explains what slugify.ts does and how to use it.",
        "references": ["copy", "markdown"],
        "base":       False,
    },
    "commitmsg": {
        "files":      {"slugify.ts": SLUGIFY_TS, "change.diff": CHANGE_DIFF},
        "prompt":     "Write the commit message for the change in change.diff into COMMIT_MSG.txt. Do not commit.",
        "references": ["git-conventions"],
        "base":       False,
    },
    "commit": {
        "files":      {"slugify.ts": SLUGIFY_OLD_TS},
        "changes":    {"slugify.ts": SLUGIFY_TS},
        "git":        True,
        "tools":      ["Bash(git status:*)", "Bash(git diff:*)", "Bash(git log:*)", "Bash(git add:*)",
                       "Bash(git commit:*)"],
        "prompt":     "Commit the change in slugify.ts.",
        "references": ["git-conventions"],
        "base":       False,
    },
    "jsxorder": {
        "files":  {"package.json": PACKAGE_JSON, "features/items/itemList.tsx": ITEM_LIST_TSX},
        "prompt": "Fix the order of the code in features/items/itemList.tsx so it follows my conventions. Change nothing else.",
        "react":  ["code-style", "naming", "workflow-and-verification"],
    },
    "order": {
        "files":  {"orders.ts": ORDERS_TS},
        "prompt": "Fix the order of the code in orders.ts so it follows my conventions. Change nothing else.",
    },
    "names": {
        "files":  {},
        "prompt": "Add the helper functions this TypeScript app needs, in whatever files fit: one that formats a byte "
                  "count as text (B, KB, MB), one that turns a caught error into a message for the user, one that "
                  "reads a numeric query parameter from a URL with a default value, and one that returns the position "
                  "of the first item in a list whose name matches a query. Also add an interface for a storage "
                  "backend (save and load a string by key) with an in-memory implementation.",
    },
    "types": {
        "files":  {},
        "prompt": "Create orders.ts with three exported functions over a list of orders (each with an id, a "
                  "priceCents, a boughtAt Date, an isUsed flag and an isGift flag): one that returns the position "
                  "of the first order with a given id, one that returns the price of the order with a given id, "
                  "and one that keeps the orders that can be refunded: bought at most 30 days ago, not used, and "
                  "either over 1000 cents or a gift.",
    },
    "nesting": {
        "files":  {},
        "prompt": "Create stock.ts with an exported function that takes a list of warehouses (each with a name, "
                  "an isOpen flag and a list of shelves; each shelf has an isBlocked flag and a list of items with "
                  "a sku and a quantity) and returns the skus with quantity zero, only from open warehouses and "
                  "shelves that are not blocked. Also export a function that returns the label of a warehouse: "
                  "\"Closed\" when it is not open, \"Empty\" when it has no shelves, otherwise its name.",
    },
}

# Scenarios whose starting files hold unaligned assignments that must stay as they are.
UNALIGNED_START_SCENARIOS = ("doc", "mindiff", "cut", "question", "audit")
# Scenarios whose starting file headers are compared with the output.
HEADER_SCENARIOS = ("naming", "imports", "cut")
# Scenarios whose prompt asks for documentation: every other one must add no comment, doc comment or header.
DOCUMENTED_SCENARIOS = ("doc", "tsdoc", "bash")
