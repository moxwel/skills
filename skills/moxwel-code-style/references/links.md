# Official docs

Check the source when a tag or convention is in doubt. Where these guides disagree with the references, the references win.

- JSDoc tags: https://jsdoc.app/
- TSDoc (TypeScript doc comments): https://tsdoc.org/
- PEP 8, Python naming and imports: https://peps.python.org/pep-0008/
- PEP 257, Python docstrings: https://peps.python.org/pep-0257/
- Sphinx field lists (`:param:`, `:returns:`, `:raises:`): https://www.sphinx-doc.org/en/master/usage/domains/python.html#info-field-lists
- Bash manual: https://www.gnu.org/software/bash/manual/bash.html
- Linux kernel coding style, the 3-level nesting limit: https://www.kernel.org/doc/html/latest/process/coding-style.html
- Conventional Commits 1.0.0: https://www.conventionalcommits.org/en/v1.0.0/
- Writing on GitHub: https://docs.github.com/en/get-started/writing-on-github
- GitHub Markdown syntax: https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax

## Background

Videos behind some rules, for the reasoning. The references hold the rules and win where these differ.

- "Don't Write Comments": named constants and conditions, predicate functions, types instead of comments and sentinels (comments-and-docs.md rule 2, naming.md rule 5, readability.md rules 1 and 8): https://www.youtube.com/watch?v=Bf7vDBBOBUA
- Never nester: the 3-level limit, inversion and extraction, guards at the top (readability.md rules 2 and 3): https://www.youtube.com/watch?v=CFRhGnuXG-4
- Naming things: no single letters, no abbreviations, no types in names, units in names, no `utils` modules (naming.md rules 2, 4 and 7, readability.md rule 8): https://www.youtube.com/watch?v=-J3wNP6u5YU
- Premature optimization: readable before fast, measure first, data structures before micro-tuning, then the profiler (readability.md rule 9): https://www.youtube.com/watch?v=tKbV6BpH-C8
