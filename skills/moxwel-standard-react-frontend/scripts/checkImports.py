"""
checkImports.py: import order from references/code-style.md, Details "Import order". Groups in this order:
external, @/actions, @/components, @/features, @/lib, relative, import type, CSS. Inside each
group, alphabetical by module path (external included: next/... before node:... before react).
The import type lines follow the same group order inside; the CSS goes shared first (shared.css),
then any other, and the file's own CSS (same name as the file) last.
Checks the block of consecutive imports at the start of the file; a comment between imports ends
the block. Usage: python3 checkImports.py <folder> [--fix]. With --fix it reorders the block. With
no problems it prints nothing; with problems it prints path:line and exits with code 1.
"""

import os
import re
import sys

# Sort ranks: values before import type before CSS; inside CSS, shared.css, then others, own CSS last
VALUE_RANK, TYPE_RANK, CSS_RANK = 0, 1, 2
SHARED_CSS_RANK, OTHER_CSS_RANK, OWN_CSS_RANK = 0, 1, 2
SOURCE_GROUPS = ["external", "@/actions", "@/components", "@/features", "@/lib", "relative"]
ALIAS_GROUPS = ("@/actions", "@/components", "@/features", "@/lib")
IMPORT = re.compile(r'^import (?:[^;"]*? from )?"([^"]+)";\n', re.M | re.S)
CODE_EXTENSIONS = (".ts", ".tsx")


def source_group(path: str) -> int:
    """Source group of an import path.

    :param path: Path of the imported module.
    :returns: Index in SOURCE_GROUPS (external, @/ alias or relative).
    """
    for prefix in ALIAS_GROUPS:
        if path.startswith(prefix + "/"):
            return SOURCE_GROUPS.index(prefix)
    if path.startswith("."):
        return SOURCE_GROUPS.index("relative")
    return SOURCE_GROUPS.index("external")


def sort_key(statement: str, path: str, position: int, own_css: str) -> tuple:
    """Sort key of an import: values, then import type, then CSS (shared.css, others, own CSS last).

    :param statement: Full import line.
    :param path: Path of the imported module.
    :param position: Original position, so CSS of the same kind keeps its order.
    :param own_css: File name of the checked file's own CSS (itemManager.css for itemManager.tsx).
    :returns: The tuple used for sorting.
    """
    if path.endswith(".css"):
        name = os.path.basename(path)
        is_shared = name == "shared.css"
        is_own = name == own_css
        css_rank = OTHER_CSS_RANK
        if is_shared:
            css_rank = SHARED_CSS_RANK
        if is_own:
            css_rank = OWN_CSS_RANK
        return (CSS_RANK, css_rank, "", position)
    is_type_import = statement.startswith("import type")
    kind = TYPE_RANK if is_type_import else VALUE_RANK
    return (kind, source_group(path), path.lower(), position)


def import_block(text: str) -> list:
    """Consecutive imports from the first one; stops at the first text that is not an import.

    :param text: File contents.
    :returns: The IMPORT matches of the block, in order.
    """
    block = []
    cursor = None
    for match in IMPORT.finditer(text):
        is_contiguous = cursor is None or not text[cursor:match.start()].strip()
        if not is_contiguous:
            break
        block.append(match)
        cursor = match.end()
    return block


def check_file(file: str, should_fix: bool) -> int:
    """Checks the import order of a file and, with should_fix, fixes it.

    :param file: Path of the file.
    :param should_fix: Whether to reorder the block instead of reporting it.
    :returns: 1 if a problem was reported, 0 otherwise.
    """
    text = open(file, encoding="utf-8").read()
    block = import_block(text)
    statements = [(match.group(0), match.group(1)) for match in block]
    own_css = os.path.splitext(os.path.basename(file))[0] + ".css"
    keys = [sort_key(statement, path, i, own_css) for i, (statement, path) in enumerate(statements)]
    is_sorted = keys == sorted(keys)
    if is_sorted:
        return 0
    if should_fix:
        ordered = [statement for _, (statement, _) in sorted(zip(keys, statements))]
        start, end = block[0].start(), block[-1].end()
        open(file, "w", encoding="utf-8").write(text[:start] + "".join(ordered) + text[end:])
        return 0
    for first_wrong in range(1, len(keys)):
        is_out_of_order = keys[first_wrong] < keys[first_wrong - 1]
        if is_out_of_order:
            break
    line = text.count("\n", 0, block[first_wrong].start()) + 1
    print(f"{file}:{line}: import out of order ({statements[first_wrong][1]})")
    return 1


def main() -> int:
    """Checks (or fixes with --fix) every .ts/.tsx in the given folder.

    :returns: 0 with no problems, 1 if it found any.
    """
    folder = sys.argv[1]
    should_fix = "--fix" in sys.argv
    problems = 0
    for root, _, names in os.walk(folder):
        for name in sorted(names):
            if name.endswith(CODE_EXTENSIONS):
                problems += check_file(os.path.join(root, name), should_fix)
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
