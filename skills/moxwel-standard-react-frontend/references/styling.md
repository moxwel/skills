# Styling

Covers Tailwind, plain CSS, cascade layers, responsive layout, modals, motion and the default visual language.

## Rules

1. **Layout in Tailwind, appearance in CSS, in every layer.** Box properties (display, position/inset, z-index, isolation, overflow, flex and alignment, gap, padding, width/height/min/max, aspect-ratio, object-fit) are Tailwind classes in JSX. Everything visual (colors, background, borders, radius, shadows, outline, typography, list-style, transforms, cursor, opacity, pointer-events, SVG fill) goes in the component's same-named `.css`. Ellipsis: `text-overflow` in CSS, its `overflow-hidden` in JSX. CSS classes are named per [naming.md](naming.md), and appearance state lives in data attributes (`[data-variant="ghost"]`), not modifier classes.
2. **Layout in CSS only where native Tailwind can't express it,** marked `/* Layout exception: <why> */`: pseudo-elements, attribute-value or `:has()` selectors, Base UI internal markup, Base UI CSS vars, `calc()`/`min()`/`max()`, and percentages other than 100%. Keep only those declarations, never one a utility on the same element also sets. The browser reset in `globals.css` is the other allowed layout in CSS.
3. **No inline `style`** in own code. A runtime value goes through a component prop (Base UI `Progress`/`Meter` `value`) or a data attribute. Inline styles that libraries set are fine.
4. **Pages (`app/`) have no CSS of their own** besides `globals.css`, and use no color or typography utilities. They render components and pass props.
5. **Tailwind native values only:** no arbitrary values (`w-[13px]`), no CSS-var shorthands (`max-h-(--var)`), no arbitrary variants (`data-[side=top]:`), no fractions (`basis-1/2`), no color or typography utilities. Spacing uses only the house scale (Details).
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

## Details

- **Computed classes:** a *layout* condition known in React becomes a computed class (`cn(isFile && "h-auto py-2")`), not a CSS selector.
- **House spacing scale:** 0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4–12, 14, 16, 20, 24, 28, 32, 36, 40, 44, 48, 52, 56, 60, 64, 72, 80, 96, plus `px`, `full`, `auto`, `screen`, `min`/`max`/`fit`. Widths can also use the named scale (`max-w-xs` … `max-w-7xl`). Tailwind v4 accepts any number (`p-13`), but we snap to these steps for consistency.
- **Variants:** native ones are fine (`hover:`, `focus-visible:`, `active:`, `disabled:`, boolean `data-<name>:`, `aria-<state>:`, `*:`, `md:`…); only arbitrary variants are banned (rule 5), and breakpoints follow rule 6.
- **Large screens (`3xl`), only when asked:** declare `@theme { --breakpoint-3xl: 128rem; --container-8xl: 112rem; }` in `globals.css`. The breakpoint sits a bit above the container so the wider content fits when it switches. On `3xl` only the content grows (`max-w-6xl` → `3xl:max-w-8xl`, more columns in requested grids); navbar and footer keep their width.
- **Flex adapts the rest:** `flex-wrap` + `basis-*` + `min-w-*`, inside `max-w-*` containers.
- **Top on mobile, why:** on a phone a vertically centered element sits under the on-screen keyboard and clips tall content. Pattern: `<main className="flex flex-1 items-start justify-center px-4 pt-8 md:items-center md:pt-0">`.
- **Modals:** Base UI `Dialog.Viewport` is the positioner, `MODAL_VIEWPORT_LAYOUT = "fixed inset-0 flex items-start justify-center px-4 py-8 md:items-center"`. The popup stays in flow inside it (`flex max-h-full w-full max-w-lg flex-col gap-4 overflow-y-auto p-6`; AlertDialog uses `max-w-sm`). The backdrop is a sibling placed before the viewport. Never use `top: 50%` + `translate`.
- **globals.css** ([template](../assets/globals.css)) holds only the tokens, the Tailwind imports and `@layer base` (`color-scheme: dark`, the reset, base element appearance). Body layout lives in `app/layout.tsx`: `<body className="relative flex min-h-screen flex-col">` wraps `<div className="isolate flex flex-1 flex-col">`. `relative` is for Base UI backdrops on iOS, and `isolate` keeps popups above the page.
- **Shared CSS files:**
  - `components/base-ui/shared.css`: `focus-ring`, `field-box`, `field-label`, `popup-surface`, `modal-*`.
  - `features/shared.css`: `feature-muted`, `feature-sm`, `feature-empty`.
  - `components/ui/shared.css`: created once two `ui/` pieces share a class.
  - A piece in another folder that needs a shared class repeats it, with a comment naming the original.
- **Native defaults:** `<fieldset>` gets `p-0 min-w-0` + `border: none`. `<legend>` is floated (`float-left w-full p-0`) so it joins the `gap`. A `<p>` with mixed inline content stays block.
- **Button-styled links** use `ButtonLink` (Next `Link` + `.button` + the same `size` prop and `BUTTON_LAYOUT*` constants as Button). Explicit exception to the per-folder `shared.css` rule: it imports `@/components/base-ui/button.css`, since it is the link form of Button.
- **When animation is asked:** `transition: <property> 150ms ease-out` on that property only, never `all`. Keyframes go in `@layer components`, named per naming.md. Deleting the transition must leave a correct, instant UI.
- **Visual language (defaults for new projects):**
  - Theme: dark with an orange accent (`#f08a24`). Radius 3px except circles. Dials: ENERGY 1 / RHYTHM 1 / MOTION 1 (calm, uniform, static; workflow-and-verification.md).
  - `.button`: solid background + darker 3px bottom stripe. Variants `primary`/`secondary`/`danger`/`ghost` (ghost: no stripe, accent border on hover). Disabled at 50% opacity. Sizes (prop `size`): `default` is `h-11` (44 px, the minimum touch target), `small` is `h-9` with its touch area extended to 44 px by a `::after` (a Layout exception), `large` is `h-14`. Icon-only is a square of the same size.
  - Fields: `h-11`, 1px `--border-strong` border, accent on focus.
  - Popups: 1px accent border + soft shadow. Notice: 3px warning left border.
  - Toasts: a bottom-right list, newest at the bottom (`flex-col-reverse`), no stacked deck.
  - Icons: 1.5rem (24 px) by default (`ICON_SIZE`); 1rem (16 px, `ICON_SIZE_SMALL`) for status rows, properties, details and icons inline with text; 3rem (48 px, `ICON_SIZE_LARGE`) for page titles and the logo; the user can set another size (components.md catalog).
  - Spinner: a static ring with `role="status"` and a visible text naming what loads, so it never reads as a frozen page. It rotates only if the user asks for rotation (rule 13).
  - AlertDialog: Cancel left (secondary), confirm right (danger), each `flex-1`.

## Gotchas

- **Missing layer-order line → wrong colors.** Next may load a component's CSS chunk before `globals.css`, and the browser fixes the layer order at the first declaration it sees.
- **Component unstyled at the page bottom, mobile frozen.** It relied on another component to load `shared.css` (rule 12).
- **A `.css` size or padding rule has no effect.** Utilities beat every layered rule. Change layout through `className`.
- **Inline text in a flex row gets gaps between words.** Group the text run in one `<span>`.
- **Debugging a style:** read `getComputedStyle` to see which rule and layer won. Don't guess.

## Checklist

- [ ] No arbitrary values, fractions, off-scale steps, color/typography utilities or inline `style` (`grep -rn "style={" src`).
- [ ] No margins. No layout in `.css` except the reset and commented exceptions.
- [ ] Only `md:` breakpoints (others only where asked) and no `@media`. Window-centered elements are at the top on mobile.
- [ ] Every new CSS file has the layer-order line, and each component imports what it uses.
- [ ] No animation or grid unless asked (`grep -rnE "transition|animate-|@keyframes|grid" src`).
- [ ] Every data view has loading, error and empty states that say what happens and what to do.
- [ ] Contrast checked: text 4.5:1, control edges and indicators 3:1, in every theme.
