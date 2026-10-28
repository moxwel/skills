# Components

Covers Base UI wrappers (`components/base-ui/`), generic UI pieces (`components/ui/`) and navigation state in the URL fragment. Base UI docs: https://base-ui.com/llms.txt.

## Rules

1. **App code never imports `@base-ui/react`;** only `components/base-ui/` does. Use every Base UI primitive over a native control (Button, Input, Select, RadioGroup, Switch, Slider, Tabs, Accordion, Dialog, AlertDialog, Toast, Collapsible, Fieldset…). Native elements only where Base UI has nothing (`<table>`, `<audio>`, text, links).
2. **Wrapper names match the Base UI docs exactly** (`AlertDialog`, never `ConfirmDialog`). Alias the import with a `Base` prefix. Complementary parts share a file named after the primitive (`form.tsx` holds `Form` + `Field` + `Input`). A variant is a prop mode of the same wrapper, not a second wrapper (`Slider` with a number or a `[start, end]` range).
3. **Wrappers stay minimal.** Composing several primitives for one use case of the app is a feature. A `ui/` piece knows no domain and calls no action.
4. **Every destructive action** (delete, reject, logout) asks first with `AlertDialog`.
5. **Navigation state lives in the URL fragment:** the active tab and the opened accordion item, as `#id`, hierarchical with `-` (`/admin#taunts-props-laughs`). Ephemeral state (open modal, drafts) stays local, and shareable filters go in the query string.
6. **No password reveal button unless the user asks.** If asked: a click toggle (never hold-to-reveal), crossed eye while hidden (the default), fixed `aria-label` + `aria-pressed`.

## Details

- **Props shape:** `type Props = Omit<ComponentProps<typeof BaseX>, "className"> & { className?: string; …own props }`. `className` is a plain string so `cn()` can merge it.
- **Each wrapper:**
  - applies its CSS class + default layout through `cn()` and exposes `data-*` variants;
  - offers data-driven props where simpler for callers (`items={[{ label, value }]}`);
  - casts `onValueChange` values to its own type once.
- **`render` prop composition:** `BaseAlertDialog.Close render={<Button variant="secondary" />}`. The rendered component must forward its `ref` and spread the props it receives. A button part rendered as a non-`<button>` needs `nativeButton={false}`.
- **State attributes:** `[data-checked]`, `[data-disabled]`, `[data-popup-open]` (triggers), `[data-open]` (popups/panels), `[data-highlighted]`, `[data-invalid]`.
- **Catalog:**
  - Icons: `<Icon path={mdiX} size={ICON_SIZE} />` from `@mdi/react` + `@mdi/js`. Three sizes, all in `lib/const/icons.ts` and in rem (so they don't depend on the surrounding font size):
    - `ICON_SIZE = "1.5rem"`, the default: buttons, navbar, tabs, toasts, chevrons and every icon nobody said otherwise about.
    - `ICON_SIZE_SMALL = "1rem"`, only where the user asks for it explicitly, typically next to small text: status badges and the property rows of a record (views, date, author, size).
    - `ICON_SIZE_LARGE = "3rem"`, only where the user asks for it explicitly: the icon next to a page title (`PageTitle`), and the large logo.
    No per-place size constants or `iconSize` props. Outside the three sizes there is only a mark that must fit a fixed box (the check inside a checkbox or a select option) and a deliberate focal icon (a large upload circle); each one names itself as an exception in its file. The `Button` loading spinner matches the icon (`size-6`), so the button doesn't change width while loading.
  - `Button`: `variant`, `icon` (MDI path), `isLoading` (spinner, stays focusable, `aria-busy`). With no children it is icon-only (`data-icon-only`) and needs `aria-label` + `title`.
  - `Form`: defaults to `method="post"`, so a submit before hydration never puts values in the URL. It focuses the first invalid field itself.
  - `AlertDialog`: its icon-only trigger uses `triggerAriaLabel` as both `aria-label` and `title`.
  - `Dialog`: controlled, for edit forms. Close it from the action's `ok` in an effect.
  - `Select`: `key={dependency}` resets it when its options depend on another field.
  - `Switch`: always the switch first and its text to the right, both inside one `<label>` (`flex items-center gap-3`), so a click on the text toggles it too. Never the text first or the switch pushed to the far end. The text names the "on" state ("Visibilidad pública"); a hint below can describe the current state.
  - `ToastProvider` + `useActionToast()`: `toast(state)` shows `ok` as success and `error` as error.
  - `Accordion`: closed panels are not mounted, so media inside loads only when opened.
- **`components/ui/`** pieces, built only when needed: `Card` (`as` = section (default)|article|div), `Notice`, `Table` (scroll wrapper + `<table>`), `StatusBadge`, `Spinner`, `AudioPlayer` (native `<audio preload="none">`), `PageTitle` (`<h1>` + icon from `PAGES`), `ButtonLink`.
- **Fragments:**
  - Each fragment is the real `id` of the element it names (`Tab`, accordion `Item`). Values are lowercase slugs without `-`, because `-` is the separator. Nested wrappers take a `fragmentPrefix`.
  - A tab is active when the fragment equals its id or starts with `id-`. Otherwise use `defaultValue`.
  - Write with `history.replaceState(null, "", url)`, never `location.hash`, which scrolls and adds history entries. Read with `useSyncExternalStore` (server snapshot `""`).
  - Both functions live in `lib/ui/urlFragment.ts`, an allowed two-export file because they share the private event.
  - An accordion that mounts with its item targeted calls `scrollIntoView()`, since the panel wasn't in the server HTML.

```ts
const FRAGMENT_EVENT = "urlfragmentchange";

/**
 * Listens to fragment changes.
 * @param onChange - Called on hashchange or replaceUrlFragment.
 * @returns A function that removes the listeners.
 */
function subscribe(onChange: () => void) {
  window.addEventListener("hashchange", onChange);
  window.addEventListener(FRAGMENT_EVENT, onChange);
  return () => {
    window.removeEventListener("hashchange", onChange);
    window.removeEventListener(FRAGMENT_EVENT, onChange);
  };
}

/**
 * Current fragment, decoded.
 * @returns The fragment without #, or "" if it is missing or malformed.
 */
function readFragment(): string {
  try {
    return decodeURIComponent(location.hash.slice(1));
  } catch {
    return "";
  }
}

/**
 * Current URL fragment, reactive.
 * @returns The fragment without #, decoded; "" on the server.
 */
export function useUrlFragment(): string {
  return useSyncExternalStore(subscribe, readFragment, () => "");
}

/**
 * Changes the fragment without scrolling or adding a history entry.
 * @param fragment - Element id; empty removes the fragment.
 */
export function replaceUrlFragment(fragment: string): void {
  const url = fragment ? `#${encodeURIComponent(fragment)}` : location.pathname + location.search;
  history.replaceState(null, "", url); // null: with history.state (Next internal state) Next ignores the change
  window.dispatchEvent(new Event(FRAGMENT_EVENT));
}
```

## Gotchas

- **Fragment lost after a server action.** `history.replaceState(history.state, …)` reuses Next's internal router state, so Next ignores the change and `refresh()` later drops the fragment. Always pass `null`, as the Next docs do. `replaceState` fires no `hashchange`, so dispatch your own event.
- **Toast render loop (React #185).** `useToastManager()` returns a new object on every render. Use one global `Toast.createToastManager()` passed to `Toast.Provider`.
- **Select chevron or state not styling.** Triggers use `[data-popup-open]`, not `[data-open]`.
- **Select options wrap one word per line.** Use flex items + `ItemIndicator keepMounted`.
- **`Fieldset.Legend` renders a `div`.** Pass `render={<legend />}`.

## Checklist

- [ ] No `@base-ui/react` import outside `components/base-ui/` (`grep -rn "@base-ui/react" src`).
- [ ] Every `<Icon>` uses `ICON_SIZE`, or `ICON_SIZE_SMALL` / `ICON_SIZE_LARGE` where it was asked for; any other size is a fitted mark or a focal icon that says so in its file.
- [ ] New wrappers use the Base UI docs name. Destructive actions use `AlertDialog`.
- [ ] New `Tabs`/`Accordion` values are slugs without `-`, and nested ones get `fragmentPrefix`. Reloading with `#id` reopens the same item.
- [ ] No password reveal unless asked.
- [ ] Every `Switch` comes before its text, inside the same `<label>`.
