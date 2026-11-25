# Comments and docs

Covers every source file in any language: when comments are written at all, the language of code and text, file headers, inline comments and doc comments on functions, constants and types.

## Rules

1. **Language:** code, comments, doc comments, user-facing strings, logs and docs are in English. When the project names another language for user-facing strings, comments or docs (an override, see SKILL.md), those use it. Comments stay ASCII (drop accents) and identifiers stay English whatever that language; user-facing strings keep full orthography.
2. **No new comments unless the user asks for them:** write a comment, doc comment or file header only where the user explicitly asks for an explanation or documentation. Names, named conditions, types (readability.md rule 8) and small functions carry the intent instead. The rest of this file sets the form of the comments the user asked for and of the ones already in the code.
   - Existing comments stay. One that a change makes wrong is corrected, or deleted if it no longer applies (SKILL.md).
   - Code moved to another file keeps its existing comments, so the move adds none.
   - Tool directives and markers are not comments in this sense (`// eslint-disable-next-line`, `# noqa`, `shortcut: ...`) and go wherever the tool needs them. Neither is the `// slow: ...` comment above knowingly slow code (readability.md rule 9), written without a request.
   - A reason the user should know (a workaround, a dropped error, a non-obvious decision) goes in the reply to the user, not in a comment.
3. **A file header, when asked for,** is at most two lines: what the file is, plus any non-obvious decision and why. It never restates the file name. Only a line the language requires to be literally first (a shebang or an encoding declaration) precedes it. Config and data files need none.
4. **Inline comments explain *why*, never what the next line does.** No emojis. A line, variable or constant whose name already says it gets no comment, even when comments were asked for.
5. **A doc comment goes on a function only when its name and signature do not say enough:** complex logic, an outcome the signature hides (a `false` that means "already taken", a deliberate throw, a side effect) or a parameter that is not obvious. A self-descriptive function (`formatBytes`, `describeItem`) gets none.
6. **A doc comment is short:** two lines at most, and tags (`@param`, `@returns`, `@throws` or the language's equivalent) only for what the name and the type do not already say. A comment that echoes the name, the type or the signature is deleted.
   - **Doc tags:**
     - `param` only for a parameter the name and type leave unclear (a unit, a format, an accepted range). One line each; an options object documents only its non-obvious fields.
     - `returns` when the value has outcomes the type does not show (`true if it marked it; false if it doesn't exist or was already reviewed.`). The special case never goes in the summary line.
     - `throws` when the function throws or rethrows on purpose, or calls a function whose doc has `throws` without catching it. Say when it throws in the tag, never in prose.
     - No `@` inside the text: tag parsers read it as a new tag.
     - A summary-only doc is one line (`/** Number of active items. */`).
   - **Constants** never get a doc comment: one that needs explaining gets a short comment at the end of its line (rule 7). A constant with a descriptive name needs none.
   - **Shared types** get `@property name - Desc.` lines in the type's doc for non-obvious fields, never comments inside the type.
7. **Comments in code are line comments, as short as possible, placed by what they explain.** This rule only places the comments rule 2 allows; it never asks for one.
   - **A variable, constant or field:** at the end of its own line, in a few words (`const MAX_ITEMS = 100; // cap per listing`). Never a comment line above it.
   - **A function:** one line right above it (`// safe file name`, then the function). In Python too it is a `#` line above the `def`, never a docstring. A doc comment or docstring the user asked for as documentation replaces it, in the forms of rules 5 and 6.
   - **A statement or a block:** one line right above it.
   - Never a `/* */` block or several lines; a language with no line comment (CSS) uses a one-line `/* */` in the same place. It starts lowercase, has no final period, and uses the fewest words that keep the fact (`// socket may be stale`, not `// retry once here because the socket may be stale`). Only a header or doc comment the user asked for as documentation takes the forms of rules 3, 5 and 6. The tone rules of copy.md apply to every comment and doc.

## Details

- **Header and doc forms by language:**

| Language | File header | Doc comment | Tags |
|---|---|---|---|
| TypeScript / JavaScript | `/* … */` block | `/** … */` above the function | `@param name - Desc.`, `@returns Desc.`, `@throws Desc.` |
| CSS | `/* … */` block | none | none |
| Python | module docstring `"""…"""` | docstring as the first statement | `:param name: Desc.`, `:returns: Desc.`, `:raises Error: Desc.` |
| Bash | `#` block after the shebang, with a usage section for scripts | `#` lines right above the function | prose: what it takes, what it prints or returns |

- **Does it need a doc comment?** Read the name and the signature as a stranger would. If they answer what it does, what it takes and what it returns, stop. Otherwise write only the missing part: the unexpected outcome, the edge case, the throw.
- **Inline comment form:**
  - An inline comment is a `//` or `#` comment inside a body or after a line of code. File headers, doc comments and the usage block of a script keep full sentences (capital, final period).
  - Names, acronyms and proper nouns keep their case (`the API returns null`, `Plasma ignores it`), and a tool directive or marker stays as the tool expects it (`// eslint-disable-next-line`, `# noqa`, `shortcut: ...`, `slow: ...`).
  - Cut the lead-in: `this is needed because`, `note that`, `we need to`. Start at the fact.
  - Placement (rule 7): trailing comments on consecutive lines line up (readability.md rule 6). Python puts two spaces before a trailing `#` (PEP 8).

```ts
const MAX_LISTED_ITEMS = 500; // caps huge folders
const ITEM_EXTENSION   = ".json";

// safe file name
function isValidName(name: string): boolean {
```
  - A comment that seems to need several sentences is cut to one line: keep the constraint, drop the story (Gotchas).

| Before | After |
|---|---|
| `// Retry once, the socket may be stale.` | `// socket may be stale` |
| `// Note that the API returns null for an empty list.` | `// API returns null when empty` |
| `# This is needed because the file may not exist yet.` | `# file may not exist yet` |
| `/* The model fills a moment after it is enabled, so we sample again here. */` | `// model fills late` |

```ts
/**
 * Marks the item as reviewed if it is still pending.
 * @returns false if it doesn't exist or was already reviewed.
 */
export function markItemReviewed(id: string, status: ReviewStatus): boolean {
```

```python
def mark_item_reviewed(item_id: str, status: str) -> bool:
    """Marks the item as reviewed if it is still pending.

    :returns: False if it doesn't exist or was already reviewed.
    """
```

## Gotchas

- **Accents break ASCII-only tooling.** A comment written in another language keeps its words but drops the accents (`configuracion`, not `configuración`).
- **A doc that restates the name is noise.** `/** Gets the item. */` on `getItem`, or `@param item - Item to describe.` on `describeItem(item)`, adds nothing: say what is non-obvious (which item, what happens when it is missing) or write no comment.
- **A long comment is a smell.** Three lines of history and reasoning around a one-line fact bury the fact: keep the constraint, drop the story.

## Checklist

- [ ] No comment, doc comment or header was added unless the user asked for an explanation or documentation; reasons went in the reply.
- [ ] A header the user asked for is at most two lines saying what the file is and why it looks that way.
- [ ] No comment echoes a name, a type or a signature; self-descriptive functions and constants have none.
- [ ] A doc comment exists where the name hides something (an outcome, a deliberate throw, complex logic), and is two lines at most.
- [ ] Every comment in code is one `//` or `#` line, lowercase, no final period, no lead-in filler, as few words as possible.
- [ ] A comment on a variable, constant or field sits at the end of its line; one on a function or a statement sits on the line right above it; no constant has a doc comment.
