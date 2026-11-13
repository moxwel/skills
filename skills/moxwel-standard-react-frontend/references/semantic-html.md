# Semantic HTML

Covers choosing elements and accessibility. Authority: MDN elements reference, https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements.

## Rules

1. **Use the native element whose meaning fits.** The inspected DOM should read like a document.
2. **`div`/`span` only where no element fits:** pure layout wrappers (form/dialog action rows, a table scroll container, the `isolate` root `div`), the root of a `ui/` component with no fitting element (`StatusBadge`, `Spinner`, a `Card as="div"` with no heading of its own), and one `<span>` grouping inline text in a flex row.
3. **Leave Base UI's internal markup alone,** except to swap in a native element through `render` where Base UI renders a plain `div` (`Fieldset.Legend render={<legend />}`).
4. **Changing an element must not change its look:** neutralize native defaults in the reset or in the component.
5. **Icon-only buttons** have an `aria-label` + the same `title`. Toggle buttons keep a fixed `aria-label` + `aria-pressed`.
6. **Keyboard focus is always visible** (`.focus-ring`). Never `outline: none` without a replacement.

Details and gotchas, binding too: [details/semantic-html.md](details/semantic-html.md).

## Checklist

- [ ] Semantic elements used, and every `div`/`span` fits rule 2.
- [ ] Icon-only buttons have `aria-label` + `title`. Radio groups are in a `Fieldset`.
