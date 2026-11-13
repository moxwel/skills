"""
Checks of what a session wrote: one function per scenario, registered in CHECKS under the scenario name,
plus the checks several scenarios share.
"""

import itertools
from pathlib import Path
import re

from alignment import alignment_problems, assignment_problems, block_problems, rows_of
from scenarios import HEADER_SCENARIOS, LEGACY_TS, REVIEWS_TS, SCENARIOS, UNALIGNED_START_SCENARIOS

MAX_COLUMNS = 120
# Files checked for assignment alignment, at the top level of the session folder.
SOURCE_SUFFIXES = (".ts", ".tsx", ".py")
# A comparison or compound condition written straight into an if or while (readability.md rule 1).
INLINE_CONDITION_TS = re.compile(r"^\s*(if|while) \([^)]*(===|!==|[<>]=?|&&|\|\|)", re.M)
INLINE_CONDITION_PY = re.compile(r"^\s*(if|elif|while) [^\n]*(==|!=| not in | in |<|>)", re.M)
SINGLE_LETTER_TS    = re.compile(r"\(\s*[a-hj-z]\s*\)\s*=>|\(\s*[a-hj-z]\s*,|(const|let) [a-hj-z] (=|of)|of [a-hj-z]\)")
PREDICATE_NAME      = re.compile(r"(is|has|can|should|was)[A-Z]")
GOOGLE_DOC_SECTION  = re.compile(r"^\s+(Args|Returns|Raises):\s*$", re.M)
IMPORT_GROUPS       = ["external", "relative", "type"]


def read_output(work_dir: Path, file_name: str) -> str:
    return (work_dir / file_name).read_text(encoding="utf-8")


def found(checks: dict[str, object]) -> list[str]:
    """Returns the problems whose condition is truthy."""
    return [problem for problem, is_found in checks.items() if is_found]


def unchanged_problems(original: str, text: str) -> list[str]:
    """Lists the original lines that are no longer in the text verbatim."""
    kept_lines    = set(text.splitlines())
    changed_lines = [line for line in original.splitlines() if line.strip() and line not in kept_lines]
    return [f"existing line changed or removed: {line.strip()!r}" for line in changed_lines]


def has_long_doc(text: str) -> bool:
    """True if a /** */ doc comment has more than two lines of text."""
    docs = re.findall(r"/\*\*.*?\*/", text, re.S)
    return any(len([line for line in doc.splitlines() if line.strip(" */")]) > 2 for doc in docs)


def import_kind(line: str) -> str:
    is_type_only = "import type" in line
    is_external  = "node:" in line
    if is_type_only:
        return "type"
    return "external" if is_external else "relative"


def check_align(work_dir: Path) -> list[str]:
    text       = read_output(work_dir, "config.ts")
    new_blocks = [block for block in text.split("\n\n") if "MAX_ITEMS" not in block]
    new_names  = re.findall(r"const (\w+)", text.replace("MAX_ITEMS", "").replace("PAGE_SIZE", ""))
    has_unit   = any(name.endswith("_MS") for name in new_names)
    problems   = found({
        "existing constants were changed": "const MAX_ITEMS = 50\nconst PAGE_SIZE = 10\n" not in text,
        f"expected 2 new constants, got {new_names}": len(new_names) != 2,
        f"timeout constant has no unit in its name: {new_names}": not has_unit,
    })
    return problems + block_problems("\n\n".join(new_blocks), r"const (\w+)(\s+)= ", "new constants")


def check_cut(work_dir: Path) -> list[str]:
    lines = read_output(work_dir, "settings.ts").splitlines()
    rows  = rows_of(lines, r"\s+(\w+):(\s+)\S")
    has_all_fields   = len(rows) == 4
    is_existing_kept = '    id:      "itemList",' in lines and "    enabled: true," in lines
    problems = alignment_problems(rows, "fields") if has_all_fields else [f"expected 4 fields, got {rows}"]
    return problems + found({"existing fields were re-padded or changed": not is_existing_kept})


def check_cut2(work_dir: Path) -> list[str]:
    """Checks only the constant names: assignment_problems covers their alignment."""
    names = re.findall(r"const (\w+)", read_output(work_dir, "limits.ts"))
    expected_names = ["API_URL", "REQUEST_TIMEOUT_SEC", "MAX_ATTEMPTS", "TTL_SEC"]
    return found({f"unexpected constants: {names}": names != expected_names})


def check_imports(work_dir: Path) -> list[str]:
    text     = read_output(work_dir, "report.ts")
    kinds    = [import_kind(line) for line in text.splitlines() if line.startswith("import ")]
    external = re.findall(r"""from ["'](node:[\w/]+)["']""", text)
    return found({
        f"import groups out of order: {kinds}": kinds != sorted(kinds, key=IMPORT_GROUPS.index),
        f"external imports not alphabetical: {external}": external != sorted(external),
        "FolderStats not imported as type-only": "import type" not in text,
        "single-letter name": SINGLE_LETTER_TS.search(text),
        "inline comparison in a condition": INLINE_CONDITION_TS.search(text),
    })


def check_robust(work_dir: Path) -> list[str]:
    text = read_output(work_dir, "items_client.py")
    has_domain_error = re.search(r"class \w+\((\w*Error|Exception)\)", text)
    is_cause_dropped = re.search(r"raise \w+\(", text) and " from " not in text
    problems = found({
        "no module docstring header": not text.lstrip().startswith('"""'),
        "request without timeout":    "timeout=" not in text,
        "bare or swallowing except":  re.search(r"except\s*:|except Exception[^\n]*:\s*\n\s*pass", text),
        "no domain error: library errors reach the caller": not has_domain_error,
        "re-raise without chained cause": is_cause_dropped,
        "ignores Retry-After": "Retry-After" not in text,
        "magic number in sleep or timeout": re.search(r"time\.sleep\(\s*\d|timeout=\s*\d", text),
        "Google-style docstring sections instead of :param/:returns/:raises": GOOGLE_DOC_SECTION.search(text),
    })
    return problems + block_problems(text, r"([A-Z_]+)(\s+)= ", "constants")


def check_naming(work_dir: Path) -> list[str]:
    text       = read_output(work_dir, "slugs.ts")
    body       = text.split("*/", 1)[-1]
    functions  = re.findall(r"function (\w+)\([^)]*\):\s*(\w+)", text)
    predicates = [name for name, return_type in functions if return_type == "boolean"]
    has_predicate_name  = bool(predicates) and PREDICATE_NAME.match(predicates[0])
    has_length_constant = re.search(r"^(export )?const [A-Z_]+\s*=\s*40", text, re.M)
    return found({
        f"boolean function not named is/has/can/should/was: {functions}": not has_predicate_name,
        "inline comparison in a condition": INLINE_CONDITION_TS.search(text),
        "single-letter name": SINGLE_LETTER_TS.search(text),
        "max length 40 is not a named constant":   re.search(r"\b40\b", body) and not has_length_constant,
        "doc comment longer than two lines":       has_long_doc(text),
        "@param that echoes an obvious parameter": re.search(r"@param (slug|items|title)\b", text),
    })


def check_doc(work_dir: Path) -> list[str]:
    text = read_output(work_dir, "store.py")
    has_returns_tag = ":returns:" in text or ":return:" in text
    return found({
        "existing constants were re-aligned or changed": 'PENDING = "pending"\nREVIEWED = "reviewed"\n' not in text,
        "no snake_case function added": not re.search(r"def [a-z_]+\(", text),
        "Google-style docstring sections instead of :returns:": GOOGLE_DOC_SECTION.search(text),
        "hidden False outcome not documented with :returns:":   not has_returns_tag,
        "inline comparison in a condition":        INLINE_CONDITION_PY.search(text),
        ":param that echoes an obvious parameter": ":param item_id:" in text,
    })


def check_bash(work_dir: Path) -> list[str]:
    text          = read_output(work_dir, "sync_folder.sh")
    lines         = text.splitlines()
    header        = "\n".join(itertools.takewhile(lambda line: line.startswith("#"), lines[1:]))
    functions     = re.findall(r"^(?:function\s+)?(\w+)\s*\(\)", text, re.M)
    has_usage     = "usage" in header.lower()
    compound_test = re.search(r"^\s*(if|elif|while) [^\n]*(\]\s*(&&|\|\|)\s*\[|\s-[ao]\s|&&|\|\|)", text, re.M)
    return found({
        "no shebang on line 1": not text.startswith("#!"),
        "no # header block right after the shebang": not header,
        "header has no usage section": bool(header) and not has_usage,
        "compound test inline in an if (should be a predicate function)": compound_test,
        f"function names not snake_case: {functions}": any(name != name.lower() for name in functions),
        f"line over {MAX_COLUMNS} columns": any(len(line) > MAX_COLUMNS for line in lines),
        "non-ASCII character": re.search(r"[^\x00-\x7f]", text),
    })


def check_tsdoc(work_dir: Path) -> list[str]:
    text      = read_output(work_dir, "reviews.ts")
    functions = re.findall(r"function (\w+)\(", text)
    problems  = found({
        "hidden false outcome not documented with @returns": "@returns" not in text,
        "doc comment longer than two lines":       has_long_doc(text),
        "@param that echoes an obvious parameter": re.search(r"@param \w+", text),
        "inline comparison in a condition":        INLINE_CONDITION_TS.search(text),
        f"command that reports success named like a predicate: {functions}": any(map(PREDICATE_NAME.match, functions)),
    })
    return unchanged_problems(REVIEWS_TS, text) + problems


def check_mindiff(work_dir: Path) -> list[str]:
    text = read_output(work_dir, "legacy.ts")
    original_lines = set(LEGACY_TS.splitlines())
    added    = "\n".join(line for line in text.splitlines() if line not in original_lines)
    problems = found({
        "single-letter name in the new code": SINGLE_LETTER_TS.search(added),
        "inline comparison in a condition in the new code": INLINE_CONDITION_TS.search(added),
        "no exported function added": "export function" not in added,
    })
    return unchanged_problems(LEGACY_TS, text) + problems


def check_react(work_dir: Path) -> list[str]:
    """Checks nothing in the output: this scenario only verifies which files the session read."""
    return []


CHECKS = {
    "align":   check_align,
    "cut":     check_cut,
    "cut2":    check_cut2,
    "imports": check_imports,
    "robust":  check_robust,
    "naming":  check_naming,
    "doc":     check_doc,
    "bash":    check_bash,
    "tsdoc":   check_tsdoc,
    "mindiff": check_mindiff,
    "react":   check_react,
}


def header_problems(name: str, work_dir: Path) -> list[str]:
    """Lists the starting files whose header comment is no longer in the output verbatim."""
    headers  = {file_name: content.split("*/")[0] for file_name, content in SCENARIOS[name]["files"].items()}
    reworded = [file_name for file_name, header in headers.items() if header not in read_output(work_dir, file_name)]
    return [f"existing header of {file_name} was reworded" for file_name in reworded]


def is_checked_source(path: Path) -> bool:
    """True for the code the scenario asked for: tests the session added on its own are not checked."""
    return path.suffix in SOURCE_SUFFIXES and not path.name.startswith("test_")


def output_problems(name: str, work_dir: Path) -> list[str]:
    """Runs the check of the scenario plus the checks several scenarios share, on what the session wrote.

    :raises OSError: If the session did not write a file the scenario expects.
    """
    is_alignment_checked = name not in UNALIGNED_START_SCENARIOS
    is_header_checked    = name in HEADER_SCENARIOS
    sources = [path for path in sorted(work_dir.iterdir()) if is_checked_source(path)]
    checked_sources = sources if is_alignment_checked else []
    problems        = CHECKS[name](work_dir)
    for source in checked_sources:
        problems += assignment_problems(source.read_text(encoding="utf-8"))
    problems += header_problems(name, work_dir) if is_header_checked else []
    return problems
