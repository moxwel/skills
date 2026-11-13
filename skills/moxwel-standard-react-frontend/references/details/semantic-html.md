# Semantic HTML: details

Details and gotchas for the rules in [../semantic-html.md](../semantic-html.md).

## Details

- Navigation: `<nav>` + `<ul>` of `<li>`. Every `nav` besides the main one gets an `aria-label`.
- Thematic blocks: `<section>`. That covers a feature or panel root and tab content (heading optional), and a card with its own heading. A self-contained entry is an `<article>`.
- Headings: one `<h1>` per page (`PageTitle`), `<h2>` for sections and cards, `<h3>` for entries. Heading + subtitle: `<hgroup>`.
- Lists: `<ul>`/`<ol>`. Label/value pairs and stats: `<dl>`. Tabular data: `<table>` with `<thead>`/`<th>`.
- Values: dates in `<time dateTime="…Z">`, machine-readable values in `<data value>`, computed or live results in `<output>`, script output in `<pre><samp>`, code and file names in `<code>`.
- Related controls (radios) go in `<fieldset>` + `<legend>` through the `Fieldset` wrapper.
- Page shell: `<main>` once per page, in the `(app)` layout; pages outside it (login) render their own. The navbar is a `<header>`.
- Collapsibles and dialogs use Base UI, never the native equivalents.
- `<html lang>` matches the UI language. The active nav link gets `data-active` + `aria-current="page"`.
