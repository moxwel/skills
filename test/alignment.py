"""
Alignment checks for readability.md rule 6: blocks of consecutive lines of the same shape and the 8-column cut.
"""

import re

# Width jump between consecutive names that ends an alignment group (readability.md rule 6).
CUT_COLUMNS = 8
# A plain assignment: group 1 is the indentation, 2 the name with its keyword, 3 the padding before "=".
ASSIGNMENT = re.compile(r"^(\s*)((?:export const |const |let |local )?[A-Za-z_][\w.]*)(\s+)= \S")


def alignment_problems(rows: list[tuple[int, int]], label: str) -> list[str]:
    """Checks consecutive lines of one block against the alignment and 8-column cut rules.

    :param rows: One (name width, spaces before the value) pair per line, in file order.
    """
    groups = []
    for row in rows:
        is_same_group = bool(groups) and abs(row[0] - groups[-1][-1][0]) < CUT_COLUMNS
        if is_same_group:
            groups[-1].append(row)
        else:
            groups.append([row])
    problems = []
    for group in groups:
        value_columns = {width + spaces for width, spaces in group}
        widest        = max(width for width, spaces in group)
        is_aligned    = len(value_columns) == 1
        is_tight      = value_columns == {widest + 1}
        if not is_aligned:
            problems.append(f"{label}: group {group} not aligned")
        elif not is_tight:
            problems.append(f"{label}: group {group} padded past its widest item (missed the 8-column cut?)")
    return problems


def rows_of(lines: list[str], pattern: str) -> list[tuple[int, int]]:
    """Measures the lines the pattern matches. Its group 1 is the name and its group 2 the padding after it."""
    matches = [re.match(pattern, line) for line in lines]
    return [(len(match.group(1)), len(match.group(2))) for match in matches if match]


def block_problems(text: str, pattern: str, label: str) -> list[str]:
    """Checks the alignment of every blank-line block that has two or more lines matching the pattern."""
    blocks_rows = [rows_of(block.splitlines(), pattern) for block in text.split("\n\n")]
    problems    = []
    for rows in blocks_rows:
        has_group = len(rows) >= 2
        problems += alignment_problems(rows, label) if has_group else []
    return problems


def assignment_problems(text: str) -> list[str]:
    """Checks every run of consecutive plain assignments at one indentation; any other line ends the run."""
    problems, run, run_indent = [], [], None
    for line in text.splitlines() + [""]:
        match       = ASSIGNMENT.match(line)
        is_same_run = match is not None and run_indent in (None, match.group(1))
        has_group   = len(run) >= 2
        if not is_same_run:
            problems += alignment_problems(run, "assignments") if has_group else []
            run, run_indent = [], None
        if match:
            run_indent = match.group(1)
            run.append((len(match.group(2)), len(match.group(3))))
    return problems


def self_check() -> None:
    """Asserts the alignment checks on known lines, without starting a session."""
    cut_kept   = "PORT = 8080\nMAX_CONNECTIONS = 100\nMAX_RETRIES     = 3\n"
    cut_missed = "PORT            = 8080\nMAX_CONNECTIONS = 100\n"
    unaligned  = "TIMEOUT_MS = 500\nRETRIES = 3\n"
    aligned    = "TIMEOUT_MS = 500\nRETRIES    = 3\n"
    assert assignment_problems(cut_kept) == [], "a line 8 columns shorter keeps its single space"
    assert assignment_problems(cut_missed) != [], "padding across an 8-column jump is a problem"
    assert assignment_problems(unaligned) != [], "names of similar width must be aligned"
    assert assignment_problems(aligned) == [], "an aligned group is clean"
    print("Self-check passed.")
