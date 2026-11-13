# Markdown

Covers Markdown documentation the user asks for (`README.md`, docs, guides, changelogs): tone, line shape, characters and GitHub Flavored Markdown syntax. It does not apply to agent files: skills (`SKILL.md` and its references), `CLAUDE.md`/`AGENTS.md`, memory, plans and prompts keep whatever shape suits the agent, and `check_style.py` skips them.

## Rules

1. **Concise and human.** Short sentences and plain words, written the way a person explains something to a colleague. Say what the reader needs and stop: no filler, no marketing tone, no closing recap, no AI-isms (`comprehensive`, `seamless`, `robust`, `leverage`, `In summary`, `It's worth noting`). The tone rules of copy.md (no buzzwords, no invented facts, write like a person) apply to documentation too.
2. **One paragraph per line.** Never hard-wrap prose: a paragraph, a list item or a table row is one line, however long. The 120-column limit (readability.md rule 4) does not apply to Markdown prose.
3. **No typographic symbols outside code.** No em or en dashes (`—`, `–`), curly quotes (`“ ” ‘ ’`), arrows (`→ ⇒`), bullets (`•`), the ellipsis character (`…`), `×`, check marks or box-drawing. Use the ASCII form instead: `-` for ranges (`4-12`), `->` or `>` for sequences (`hooks -> derived values -> return`), straight quotes (`"`, `'`), three periods (`...`) and `x`. Letters and accents of the doc language are fine, and so are Spanish `¿` and `¡`. Code spans and fenced blocks keep their literal content.
4. **No emojis** (Unicode or `:shortcode:`) unless the user explicitly asks for them.
5. **GitHub Flavored Markdown,** following the GitHub writing guides (links.md): one `#` title, no skipped heading levels, fenced code blocks with a language, relative links to files in the repo, alt text on images, `-` for unordered lists and a blank line between blocks.
6. **Reference-style links when there are many.** A file with many links or images (badges, a row of logos, the same URL used several times) writes them as references (`[![vscode][vscode-badge]][vscode-url]`) and defines them at the end of the file. A few one-off links stay inline.
7. **HTML only for what Markdown cannot do:** centering (`<div align="center">`), collapsible sections (`<details>` with `<summary>`), image size (`<img height="16">`) and `<sub>`/`<sup>`. Everything else stays Markdown.

The language of the text follows comments-and-docs.md rule 1.

Details and gotchas, binding too: [details/markdown.md](details/markdown.md).

## Checklist

- [ ] The text is short, plain and sounds like a person wrote it.
- [ ] Every paragraph, list item and table row is on one line.
- [ ] No typographic symbols outside code; `check_style.py` reports nothing for the file.
- [ ] No emojis, unless the user asked for them.
- [ ] Headings, links, images, lists and code blocks follow GitHub Flavored Markdown.
- [ ] Many links or images use references defined at the end, grouped under `<!-- Links -->` and `<!-- Images -->`.
- [ ] HTML appears only for centering, collapsible sections, image size and `<sub>`/`<sup>`.
