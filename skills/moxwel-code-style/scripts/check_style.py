"""
check_style.py: the mechanical part of the style references. Checks .ts/.tsx/.js/.jsx/.mjs/.css/.py/.sh files for:

- lines over 120 columns (readability.md rule 4);
- non-ASCII characters inside comments (comments-and-docs.md rule 1); strings may keep accents;
- a missing header comment (comments-and-docs.md rule 2): a /* */ block in TS/JS/CSS, a module docstring
  in Python, a # block in Bash. Only a shebang or a Python encoding line may come before it.

And documentation .md files for typographic symbols and emojis outside code spans and fenced blocks
(markdown.md rules 3 and 4). Letters, accents and numbers of any language pass. Markdown skips the column and
header checks: a paragraph is one line however long (markdown.md rule 2). Emojis the user asked for are still
reported. Agent files are not documentation and are skipped: AGENT_FILES and any .md inside a skill folder.

Comment detection reads line by line and skips markers inside one-line string literals ("image/*" is not
a comment). It tracks /* */ blocks, and Python triple-quoted strings (a docstring when the line opens with
it, a plain string otherwise). Multi-line template literals and heredocs are not understood: a marker
inside one can be misread. Skips hidden folders and dependency or build output (SKIPPED_DIRS).
Usage: python3 check_style.py <folder>. With no problems it prints nothing; with problems it prints
path:line: problem and exits with code 1.
"""

import os
import re
import sys
import unicodedata

MAX_COLUMNS = 120
C_STYLE_EXTENSIONS = (".ts", ".tsx", ".js", ".jsx", ".mjs", ".css")
PYTHON_EXTENSION = ".py"
SHELL_EXTENSION = ".sh"
MARKDOWN_EXTENSION = ".md"
SOURCE_EXTENSIONS = C_STYLE_EXTENSIONS + (PYTHON_EXTENSION, SHELL_EXTENSION)
SKILL_FILE = "SKILL.md"
# Markdown written for agents, not people: markdown.md does not apply to it.
AGENT_FILES = {SKILL_FILE, "CLAUDE.md", "AGENTS.md", "GEMINI.md"}
# Dependency and build output folders, never hand-written code.
SKIPPED_DIRS = {"node_modules", "dist", "build", "__pycache__", "venv"}
STRING_QUOTES = ('"', "'", "`")
DOCSTRING_QUOTES = ('"""', "'''")
TRIPLE_QUOTE_LENGTH = 3
LINE_COMMENT = "//"
BLOCK_START = "/*"
BLOCK_END = "*/"
HASH_COMMENT = "#"
# Block state carried from one line to the next.
NO_BLOCK, COMMENT_BLOCK, STRING_BLOCK = "", "comment", "string"
# PEP 263: the encoding declaration must be on line 1 or 2.
MAX_ENCODING_LINE = 2
ENCODING_PATTERN = re.compile(r"^#.*coding[:=]")
# A fence opens with 3+ backticks or tildes and closes with the same character, at least as many times.
FENCE_PATTERN = re.compile(r"^(`{3,}|~{3,})")
INLINE_CODE_PATTERN = re.compile(r"(`+).*?\1")
# Unicode category initials of letters, marks (accents) and numbers: text of the language, not typography.
LANGUAGE_CATEGORIES = ("L", "M", "N")
# Spanish inverted question and exclamation marks open a sentence; they are orthography, not typography.
ALLOWED_SYMBOLS = {"\u00bf", "\u00a1"}


def find_marker(text: str, markers: tuple[str, ...]) -> tuple[int, str]:
    """Finds the first marker that sits outside one-line string literals.

    :param text: Text to scan.
    :param markers: Markers to look for, checked before quotes at each position.
    :returns: (index, marker) of the first match, or (-1, "") if every marker is inside a string or missing.
    """
    open_quote = ""
    index = 0
    while index < len(text):
        char = text[index]
        is_in_string = open_quote != ""
        if is_in_string:
            is_escape = char == "\\"
            is_closing = char == open_quote
            index += 2 if is_escape else 1
            open_quote = "" if is_closing else open_quote
            continue
        for marker in markers:
            if text.startswith(marker, index):
                return index, marker
        open_quote = char if char in STRING_QUOTES else ""
        index += 1
    return -1, ""


def scan_c_style_line(stripped: str, block: str) -> tuple[str, str]:
    """Extracts the comment text of a TS/JS/CSS line, tracking /* */ blocks.

    :param stripped: Line without surrounding whitespace.
    :param block: Block state left by the previous line.
    :returns: (comment text, empty if none; block state after the line).
    """
    is_in_comment = block == COMMENT_BLOCK
    if is_in_comment:
        is_closed = BLOCK_END in stripped
        return stripped, NO_BLOCK if is_closed else COMMENT_BLOCK
    index, marker = find_marker(stripped, (LINE_COMMENT, BLOCK_START))
    is_line_comment = marker == LINE_COMMENT
    if is_line_comment:
        return stripped[index:], NO_BLOCK
    is_block_comment = marker == BLOCK_START
    if not is_block_comment:
        return "", NO_BLOCK
    comment = stripped[index:]
    is_closed = BLOCK_END in comment[len(BLOCK_START):]
    return comment, NO_BLOCK if is_closed else COMMENT_BLOCK


def scan_python_line(stripped: str, block: str) -> tuple[str, str]:
    """Extracts the comment and docstring text of a Python line, tracking triple-quoted strings.

    :param stripped: Line, or the rest of one, without surrounding whitespace.
    :param block: Block state left by the previous line or by the start of this one.
    :returns: (comment text, empty if none; block state after the line).
    """
    is_in_block = block != NO_BLOCK
    if is_in_block:
        is_docstring = block == COMMENT_BLOCK
        end, _ = find_marker(stripped, DOCSTRING_QUOTES)
        is_still_open = end < 0
        if is_still_open:
            return stripped if is_docstring else "", block
        block_text = stripped[:end] if is_docstring else ""
        rest_comment, rest_block = scan_python_line(stripped[end + TRIPLE_QUOTE_LENGTH:], NO_BLOCK)
        return block_text + rest_comment, rest_block
    is_docstring_start = stripped.startswith(DOCSTRING_QUOTES)
    if is_docstring_start:
        return scan_python_line(stripped[TRIPLE_QUOTE_LENGTH:], COMMENT_BLOCK)
    index, marker = find_marker(stripped, (HASH_COMMENT,) + DOCSTRING_QUOTES)
    is_hash_comment = marker == HASH_COMMENT
    if is_hash_comment:
        return stripped[index:], NO_BLOCK
    is_string_start = marker in DOCSTRING_QUOTES
    if not is_string_start:
        return "", NO_BLOCK
    return scan_python_line(stripped[index + TRIPLE_QUOTE_LENGTH:], STRING_BLOCK)


def scan_shell_line(stripped: str) -> str:
    """Extracts the comment text of a Bash line.

    :param stripped: Line without surrounding whitespace.
    :returns: The comment text, or empty if the line has none.
    """
    index, _ = find_marker(stripped, (HASH_COMMENT,))
    # A # starts a comment only at the start of a word; $# and ${#var} are code
    is_word_start = index == 0 or (index > 0 and stripped[index - 1].isspace())
    return stripped[index:] if is_word_start else ""


def scan_comment_line(line: str, extension: str, block: str) -> tuple[str, str]:
    """Extracts the comment text of a line with the rules of its language.

    :param line: Line without its newline.
    :param extension: File extension, with the dot.
    :param block: Block state left by the previous line.
    :returns: (comment text, empty if none; block state after the line).
    """
    stripped = line.strip()
    is_c_style = extension in C_STYLE_EXTENSIONS
    is_python = extension == PYTHON_EXTENSION
    if is_c_style:
        return scan_c_style_line(stripped, block)
    if is_python:
        return scan_python_line(stripped, block)
    return scan_shell_line(stripped), NO_BLOCK


def scan_markdown_line(stripped: str, fence: str) -> tuple[str, str]:
    """Extracts the prose of a Markdown line, dropping code spans and tracking fenced blocks.

    :param stripped: Line without surrounding whitespace.
    :param fence: Fence left open by the previous line, empty if none.
    :returns: (prose text, empty inside or on a fence; fence open after the line, empty if none).
    """
    fence_match = FENCE_PATTERN.match(stripped)
    is_fence_line = fence_match is not None
    is_in_fence = fence != NO_BLOCK
    if is_in_fence:
        line_fence = fence_match.group(1) if is_fence_line else ""
        is_closing = line_fence.startswith(fence[0]) and len(line_fence) >= len(fence)
        return "", NO_BLOCK if is_closing else fence
    if is_fence_line:
        return "", fence_match.group(1)
    return INLINE_CODE_PATTERN.sub("", stripped), NO_BLOCK


def is_typographic_symbol(char: str) -> bool:
    """Tells whether a character is a typographic symbol or an emoji rather than text of a language.

    :param char: One character.
    :returns: True for non-ASCII characters that are not letters, marks or numbers, nor in ALLOWED_SYMBOLS.
    """
    is_language_text = unicodedata.category(char)[0] in LANGUAGE_CATEGORIES
    return not char.isascii() and not is_language_text and char not in ALLOWED_SYMBOLS


def check_markdown(path: str, lines: list[str]) -> list[str]:
    """Reports typographic symbols and emojis outside code in a Markdown file.

    :param path: Path of the file.
    :param lines: Lines of the file.
    :returns: One "path:line: problem" entry per line with symbols; empty if clean.
    """
    problems = []
    fence = NO_BLOCK
    for line_number, line in enumerate(lines, start=1):
        prose, fence = scan_markdown_line(line.strip(), fence)
        # dict.fromkeys keeps each symbol once, in order of appearance
        symbols = list(dict.fromkeys(char for char in prose if is_typographic_symbol(char)))
        has_symbols = len(symbols) > 0
        if has_symbols:
            problems.append(f"{path}:{line_number}: typographic symbol or emoji outside code: {' '.join(symbols)}")
    return problems


def has_header(lines: list[str], extension: str) -> bool:
    """Tells whether the file opens with the header comment form of its language.

    :param lines: Lines of the file.
    :param extension: File extension, with the dot.
    :returns: True if the first line after the allowed preamble opens the header; True for an empty file.
    """
    is_c_style = extension in C_STYLE_EXTENSIONS
    is_python = extension == PYTHON_EXTENSION
    for line_number, line in enumerate(lines, start=1):
        stripped = line.strip()
        is_shebang = line_number == 1 and stripped.startswith("#!")
        is_encoding_position = is_python and line_number <= MAX_ENCODING_LINE
        is_encoding_line = is_encoding_position and ENCODING_PATTERN.match(stripped) is not None
        is_preamble = stripped == "" or is_shebang or is_encoding_line
        if is_preamble:
            continue
        if is_c_style:
            return stripped.startswith(BLOCK_START)
        if is_python:
            return stripped.startswith(DOCSTRING_QUOTES)
        return stripped.startswith(HASH_COMMENT)
    return True


def check_file(path: str) -> list[str]:
    """Runs every check on one source or Markdown file.

    :param path: Path of the file.
    :returns: One "path:line: problem" entry per problem found; empty if clean.
    """
    extension = os.path.splitext(path)[1]
    try:
        with open(path, encoding="utf-8", errors="replace") as source_file:
            lines = source_file.read().splitlines()
    except OSError:
        # A dangling symlink or an unreadable file is reported, not a crash of the whole run
        return [f"{path}:1: cannot read file"]
    is_markdown = extension == MARKDOWN_EXTENSION
    if is_markdown:
        return check_markdown(path, lines)
    problems = []
    if not has_header(lines, extension):
        problems.append(f"{path}:1: missing header comment")
    block = NO_BLOCK
    for line_number, line in enumerate(lines, start=1):
        is_too_long = len(line) > MAX_COLUMNS
        if is_too_long:
            problems.append(f"{path}:{line_number}: {len(line)} columns (max {MAX_COLUMNS})")
        comment, block = scan_comment_line(line, extension, block)
        if not comment.isascii():
            problems.append(f"{path}:{line_number}: non-ASCII character in a comment")
    return problems


def is_scanned_dir(name: str) -> bool:
    """Tells whether a folder may hold hand-written code.

    :param name: Folder name, without its path.
    :returns: False for hidden folders and SKIPPED_DIRS; True otherwise.
    """
    is_hidden = name.startswith(".")
    return not is_hidden and name not in SKIPPED_DIRS


def is_checked_file(file_name: str, is_in_skill: bool) -> bool:
    """Tells whether a file is source code or user documentation that the checks cover.

    :param file_name: File name, without its path.
    :param is_in_skill: Whether the file sits inside a skill folder (one holding SKILL_FILE).
    :returns: True for source files, and for Markdown that is neither an agent file nor inside a skill.
    """
    is_markdown = file_name.endswith(MARKDOWN_EXTENSION)
    if not is_markdown:
        return file_name.endswith(SOURCE_EXTENSIONS)
    is_agent_file = is_in_skill or file_name in AGENT_FILES
    return not is_agent_file


def main() -> int:
    """Walks the folder given as argument and prints every problem.

    :returns: Exit code: 0 if clean, 1 with problems, 2 on bad usage.
    """
    has_folder = len(sys.argv) == 2 and os.path.isdir(sys.argv[1])
    if not has_folder:
        print("Usage: python3 check_style.py <folder>")
        return 2
    problems = []
    skill_roots = []
    for root, dir_names, file_names in os.walk(sys.argv[1]):
        dir_names[:] = sorted(name for name in dir_names if is_scanned_dir(name))
        # os.walk is top-down, so a skill folder is recorded before its subfolders are visited
        if SKILL_FILE in file_names:
            # Normalized because commonpath drops a leading "./" from what it returns
            skill_roots.append(os.path.normpath(root))
        is_in_skill = any(os.path.commonpath([root, skill_root]) == skill_root for skill_root in skill_roots)
        for file_name in sorted(file_names):
            if is_checked_file(file_name, is_in_skill):
                problems.extend(check_file(os.path.join(root, file_name)))
    for problem in problems:
        print(problem)
    has_problems = len(problems) > 0
    return 1 if has_problems else 0


if __name__ == "__main__":
    sys.exit(main())
