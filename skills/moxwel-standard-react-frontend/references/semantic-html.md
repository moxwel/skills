# Semantic HTML

Covers choosing elements and accessibility. Authority: MDN elements reference, https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements.

## Rules

1. **Use the native element whose meaning fits.** The inspected DOM should read like a document.
2. **`div`/`span` only where no element fits:** pure layout wrappers (form/dialog action rows, a table scroll container, the `isolate` root `div`), the root of a `ui/` component with no fitting element (`StatusBadge`, `Spinner`, a `Card as="div"` with no heading of its own), and one `<span>` grouping inline text in a flex row.
3. **Leave Base UI's internal markup alone,** except to swap in a native element through `render` where Base UI renders a plain `div` (`Fieldset.Legend render={<legend />}`).
4. **Changing an element must not change its look:** neutralize native defaults in the reset or in the component.
5. **Icon-only buttons** have an `aria-label` + the same `title`. Toggle buttons keep a fixed `aria-label` + `aria-pressed`.
6. **Keyboard focus is always visible** (`.focus-ring`). Never `outline: none` without a replacement.

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

## Checklist

- [ ] Semantic elements used, and every `div`/`span` fits rule 2.
- [ ] Icon-only buttons have `aria-label` + `title`. Radio groups are in a `Fieldset`.
