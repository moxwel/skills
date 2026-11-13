# Readability

Covers the shape of code in any language: conditions, control flow, function body order, line length, alignment and imports.

## Rules

1. **Named conditions:** a comparison or compound condition used in an `if`, ternary or markup template (JSX, HTML templates) becomes a named boolean first (naming.md rule 3). A plain boolean variable or a single predicate call needs no new name, and neither does a language idiom that is the condition itself (`if __name__ == "__main__":`). Filter callbacks and comprehension clauses are not covered.
2. **Flat control flow:** early returns over nested `if`s, and no nested ternaries (use a named const, an early return or a tiny helper).
3. **The result reads like a template:** derived values (computed strings, filtered lists, conditional texts) live in named consts before the `return` or the output, and a big result is split into named pieces composed at the end.
4. **No line, code or comment, goes past 120 columns.**
5. **Imports are grouped and sorted** ([details](details/readability.md)), always from the module that defines the name, never through a re-exporting barrel file.
6. **Consecutive lines of the same shape are aligned:** declarations, `key: value` attributes, assignments, expressions that differ only in an operand, one-line `if ... return` and arrow functions are padded with spaces so the same part starts in the same column ([details](details/readability.md), Alignment).

Details and gotchas, binding too: [details/readability.md](details/readability.md).

## Checklist

- [ ] No comparison or compound condition inline in an `if`, ternary or markup template; no nested ternaries; guards return early.
- [ ] Derived values are named before the result.
- [ ] No line over 120 columns (`python3 <skill>/scripts/check_style.py <folder>`).
- [ ] Imports grouped, sorted and taken from their defining module.
- [ ] Consecutive lines of the same shape are aligned per block, groups cut at 8 columns, trailing comments aligned, nothing padded past 120 columns.
