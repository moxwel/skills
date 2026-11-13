# Styling

Covers Tailwind, plain CSS, cascade layers, responsive layout, modals, motion and the default visual language.

## Rules

1. **Layout in Tailwind, appearance in CSS, in every layer.** Box properties (display, position/inset, z-index, isolation, overflow, flex and alignment, gap, padding, width/height/min/max, aspect-ratio, object-fit) are Tailwind classes in JSX. Everything visual (colors, background, borders, radius, shadows, outline, typography, list-style, transforms, cursor, opacity, pointer-events, SVG fill) goes in the component's same-named `.css`. Ellipsis: `text-overflow` in CSS, its `overflow-hidden` in JSX. CSS classes are named per [naming.md](naming.md), and appearance state lives in data attributes (`[data-variant="ghost"]`), not modifier classes.
2. **Layout in CSS only where native Tailwind can't express it,** marked `/* Layout exception: <why> */`: pseudo-elements, attribute-value or `:has()` selectors, Base UI internal markup, Base UI CSS vars, `calc()`/`min()`/`max()`, and percentages other than 100%. Keep only those declarations, never one a utility on the same element also sets. The browser reset in `globals.css` is the other allowed layout in CSS.
3. **No inline `style`** in own code. A runtime value goes through a component prop (Base UI `Progress`/`Meter` `value`) or a data attribute. Inline styles that libraries set are fine.
4. **Pages (`app/`) have no CSS of their own** besides `globals.css`, and use no color or typography utilities. They render components and pass props.
5. **Tailwind native values only:** no arbitrary values (`w-[13px]`), no CSS-var shorthands (`max-h-(--var)`), no arbitrary variants (`data-[side=top]:`), no fractions (`basis-1/2`), no color or typography utilities. Spacing uses only the house scale ([details](details/styling.md)).
6. **Responsive is mobile-first with a single `md:` breakpoint.** No `@media` in CSS and no `max-*:` variants. `sm:`/`lg:`/`xl:`/`2xl:`/`3xl:` only when the user asks for that screen size, with a comment.
7. **Centered in the window means top on mobile:** the login card, hero, centered empty states, modals and page spinner sit at the top below `md` and are centered from `md`.
8. **Flexbox + `gap`, no margins.** Every grouping element is flex; padding is only inner fill. Tabular data uses `<table>`. `grid` only where the user asked for a specific column/row arrangement, using native `grid-cols-N`/`md:grid-cols-N`, with a comment saying it was requested.
9. **Cascade layers.** `globals.css` declares `@layer theme, base, components, utilities;` and imports Tailwind without preflight. Every other CSS file puts that same line right after its header comment and wraps its rules in `@layer components`. Two deliberate unlayered exceptions: the `:root` tokens in `globals.css`, and the field focus-border rule at the end of the file that defines its class (`shared.css`, `select.css`).
10. **Overrides go through `className`.** Every component that takes `className` builds its root with `cn("own-class <default layout>", className)`, so the caller's utilities win. Never override a component's layout from CSS.
11. **Shared layout is a constant** in `lib/const/layout.ts` (`BUTTON_LAYOUT` plus `BUTTON_LAYOUT_SMALL` and `BUTTON_LAYOUT_LARGE`, `FIELD_BOX_LAYOUT`, `MODAL_*_LAYOUT`, `FORM_ACTIONS_LAYOUT`), never a shared CSS class.
12. **Every component imports every CSS file it uses,** `shared.css` included. Each folder's `shared.css` serves only that folder.
13. **No animations unless the user asks for that element:** no `transition`, `animation`, `@keyframes`, `[data-starting-style]`/`[data-ending-style]` rules, or Tailwind `transition-*`/`animate-*`/`duration-*` utilities. State changes apply instantly. When asked, animate only that element and property, in the CSS of the component that renders it; if that component is shared, only the instances asked, through a data attribute the caller sets.
14. **Every view that shows data has three states:** loading, error and empty, each perceivable and saying what is happening and what to do next (copy.md rule 6 of the base skill). Loading is a server `loading.tsx` in the route-group segment (Tailwind only, top on mobile and centered from `md`) with the spinner and a text naming what loads. Error is an `error.tsx` in the same segment with a retry action. Empty is part of the component that renders the list.
15. **Contrast is computed, never eyeballed:** text needs 4.5:1 (large text 3:1), and the edge of a control or a status indicator needs 3:1 against the colors next to it, in every theme. Fields, selects, checkboxes, radios and switches use `--border-strong` for their edge; `--border` is only for dividers and card edges that do not identify a control. Check each new color pair with the WCAG formula or a contrast tool.

Details and gotchas, binding too: [details/styling.md](details/styling.md).

## Checklist

- [ ] No arbitrary values, fractions, off-scale steps, color/typography utilities or inline `style` (`grep -rn "style={" src`).
- [ ] No margins. No layout in `.css` except the reset and commented exceptions.
- [ ] Only `md:` breakpoints (others only where asked) and no `@media`. Window-centered elements are at the top on mobile.
- [ ] Every new CSS file has the layer-order line, and each component imports what it uses.
- [ ] No animation or grid unless asked (`grep -rnE "transition|animate-|@keyframes|grid" src`).
- [ ] Every data view has loading, error and empty states that say what happens and what to do.
- [ ] Contrast checked: text 4.5:1, control edges and indicators 3:1, in every theme.
