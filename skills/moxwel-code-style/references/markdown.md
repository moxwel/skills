# Markdown

Covers Markdown documentation the user asks for (`README.md`, docs, guides, changelogs): tone, line shape, characters and GitHub Flavored Markdown syntax. It does not apply to agent files: skills (`SKILL.md` and its references), `CLAUDE.md`/`AGENTS.md`, memory, plans and prompts keep whatever shape suits the agent, and `check_style.py` skips them.

## Rules

1. **Concise and human.** Short sentences and plain words, written the way a person explains something to a colleague. Say what the reader needs and stop: no filler, no marketing tone, no closing recap, no AI-isms (`comprehensive`, `seamless`, `robust`, `leverage`, `In summary`, `It's worth noting`).
2. **One paragraph per line.** Never hard-wrap prose: a paragraph, a list item or a table row is one line, however long. The 120-column limit (readability.md rule 4) does not apply to Markdown prose.
3. **No typographic symbols outside code.** No em or en dashes (`—`, `–`), curly quotes (`“ ” ‘ ’`), arrows (`→ ⇒`), bullets (`•`), the ellipsis character (`…`), `×`, check marks or box-drawing. Use the ASCII form instead: `-` for ranges (`4-12`), `->` or `>` for sequences (`hooks -> derived values -> return`), straight quotes (`"`, `'`), three periods (`...`) and `x`. Letters and accents of the doc language are fine, and so are Spanish `¿` and `¡`. Code spans and fenced blocks keep their literal content.
4. **No emojis** (Unicode or `:shortcode:`) unless the user explicitly asks for them.
5. **GitHub Flavored Markdown,** following the GitHub writing guides (links.md): one `#` title, no skipped heading levels, fenced code blocks with a language, relative links to files in the repo, alt text on images, `-` for unordered lists and a blank line between blocks.
6. **Reference-style links when there are many.** A file with many links or images (badges, a row of logos, the same URL used several times) writes them as references (`[![vscode][vscode-badge]][vscode-url]`) and defines them at the end of the file. A few one-off links stay inline.
7. **HTML only for what Markdown cannot do:** centering (`<div align="center">`), collapsible sections (`<details>` with `<summary>`), image size (`<img height="16">`) and `<sub>`/`<sup>`. Everything else stays Markdown.

The language of the text follows comments-and-docs.md rule 1.

## Details

- **README shape:** the title, one sentence on what the project is, then only the sections that have something to say, usually in this order: install, usage, configuration, license. No empty or placeholder sections, no table of contents (GitHub builds one from the headings).
- **Headings** in sentence case (`## Project overrides`), without a trailing colon or numbering.
- **Links:** the text says where the link goes (`see the [install guide](docs/install.md)`), never `here` or a bare URL in prose. A link stays on one line.
- **Emphasis:** bold for the few words a skimming reader must not miss, italics rarely. Never a whole sentence in bold.
- **Lists and tables:** a list for steps or parallel items, a table to compare things across the same columns. Numbered lists only when the order matters.
- **Code:** inline code for names, paths, commands and values; a fenced block with a language (`bash`, `ts`, `python`, `text`) for anything you would copy.
- **Alerts** (`> [!NOTE]`, `> [!TIP]`, `> [!IMPORTANT]`, `> [!WARNING]`, `> [!CAUTION]`) only when the reader would get hurt by missing it: at most one or two per file, never one after another and never nested.
- **Line breaks:** no forced breaks (`<br>`, trailing spaces, a trailing `\`). A new idea is a new paragraph.
- **Task lists** use `- [ ]` and `- [x]`.
- **Reference definitions:** one per line at the end of the file, grouped under a `<!-- Links -->` comment and then an `<!-- Images -->` comment. Names are lowercase kebab-case with a suffix for what they hold (`vscode-url`, `vscode-badge`, `logo-img`). Long URLs, such as badges with query strings or data URIs, only ever appear in a definition, so the prose stays readable.
- **HTML blocks:** `<div align="center">` wraps the content to center (title, badges, a screenshot). `<details>` takes `<summary>` as its first child and `open` when it should start expanded; use it for long optional content (full option lists, logs, a big table).

````markdown
# items-sync-example

Copies items from the old store to the new one and keeps them in sync until the old store is gone.

## Install

```bash
npm install
```

Then go to *Configuration* > *Stores* > *Add store* and add the old and new store URLs.

## Usage

Run `npm run sync` once to copy everything, then `npm run sync -- --watch` to keep both stores in sync. See [configuration](docs/configuration.md) for the store URLs.

## License

[MIT](LICENSE)
````

````markdown
<div align="center">

# items-sync-example

[![build][build-badge]][build-url] [![license][license-badge]][license-url]

</div>

<details>
<summary>All command-line options</summary>

| Option | What it does |
|---|---|
| `--watch` | Keeps syncing until stopped. |
| `--dry-run` | Prints what would change without writing. |

</details>

<!-- Links -->
[build-url]: https://github.com/moxwel/items-sync-example/actions
[license-url]: LICENSE

<!-- Images -->
[build-badge]: https://img.shields.io/github/actions/workflow/status/moxwel/items-sync-example/ci.yml?style=for-the-badge
[license-badge]: https://img.shields.io/badge/license-MIT-blue?style=for-the-badge
````

## Gotchas

- **Hard wrapping looks fine rendered** but every edit reflows the paragraph and the diff shows lines that did not change.
- **Dashes and arrows slip in from habit.** A sentence with `—` usually reads better as two sentences or with a comma. `4–12` becomes `4-12` and `A → B` becomes `A -> B`.
- **The checker flags emojis even when the user asked for them.** That finding is then expected, not a problem to fix.
- **Markdown inside an HTML block renders as plain text** unless there is a blank line after the opening tag and another before the closing tag.
- **A reference with no definition renders literally** as `[text][name]`. Check every name has its definition after renaming one.

## Checklist

- [ ] The text is short, plain and sounds like a person wrote it.
- [ ] Every paragraph, list item and table row is on one line.
- [ ] No typographic symbols outside code; `check_style.py` reports nothing for the file.
- [ ] No emojis, unless the user asked for them.
- [ ] Headings, links, images, lists and code blocks follow GitHub Flavored Markdown.
- [ ] Many links or images use references defined at the end, grouped under `<!-- Links -->` and `<!-- Images -->`.
- [ ] HTML appears only for centering, collapsible sections, image size and `<sub>`/`<sup>`.
