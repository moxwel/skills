# Styling: details

Details and gotchas for the rules in [../styling.md](../styling.md).

## Details

- **Computed classes:** a *layout* condition known in React becomes a computed class (`cn(isFile && "h-auto py-2")`), not a CSS selector.
- **House spacing scale:** 0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4–12, 14, 16, 20, 24, 28, 32, 36, 40, 44, 48, 52, 56, 60, 64, 72, 80, 96, plus `px`, `full`, `auto`, `screen`, `min`/`max`/`fit`. Widths can also use the named scale (`max-w-xs` … `max-w-7xl`). Tailwind v4 accepts any number (`p-13`), but we snap to these steps for consistency.
- **Variants:** native ones are fine (`hover:`, `focus-visible:`, `active:`, `disabled:`, boolean `data-<name>:`, `aria-<state>:`, `*:`, `md:`…); only arbitrary variants are banned (rule 5), and breakpoints follow rule 6.
- **Large screens (`3xl`), only when asked:** declare `@theme { --breakpoint-3xl: 128rem; --container-8xl: 112rem; }` in `globals.css`. The breakpoint sits a bit above the container so the wider content fits when it switches. On `3xl` only the content grows (`max-w-6xl` → `3xl:max-w-8xl`, more columns in requested grids); navbar and footer keep their width.
- **Flex adapts the rest:** `flex-wrap` + `basis-*` + `min-w-*`, inside `max-w-*` containers.
- **Top on mobile, why:** on a phone a vertically centered element sits under the on-screen keyboard and clips tall content. Pattern: `<main className="flex flex-1 items-start justify-center px-4 pt-8 md:items-center md:pt-0">`.
- **Modals:** Base UI `Dialog.Viewport` is the positioner, `MODAL_VIEWPORT_LAYOUT = "fixed inset-0 flex items-start justify-center p-4 md:items-center"`. The popup stays in flow inside it (`flex max-h-full w-full flex-col gap-4 overflow-y-auto p-6 md:max-w-lg`; AlertDialog uses `md:max-w-sm`). Below `md` the popup takes the full window width. The viewport margin is `p-4` on every side at every width; the max width applies only from `md`. The backdrop is a sibling placed before the viewport. Never use `top: 50%` + `translate`.
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
  - Icons: three sizes, defined in the components.md catalog.
  - Spinner: a static ring with `role="status"` and a visible text naming what loads, so it never reads as a frozen page. It rotates only if the user asks for rotation (rule 13).
  - AlertDialog: Cancel left (secondary), confirm right (danger), each `flex-1`.

## Gotchas

- **Missing layer-order line → wrong colors.** Next may load a component's CSS chunk before `globals.css`, and the browser fixes the layer order at the first declaration it sees.
- **Component unstyled at the page bottom, mobile frozen.** It relied on another component to load `shared.css` (rule 12).
- **A `.css` size or padding rule has no effect.** Utilities beat every layered rule. Change layout through `className`.
- **Inline text in a flex row gets gaps between words.** Group the text run in one `<span>`.
- **Debugging a style:** read `getComputedStyle` to see which rule and layer won. Don't guess.
