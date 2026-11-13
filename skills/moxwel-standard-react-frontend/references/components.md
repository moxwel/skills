# Components

Covers Base UI wrappers (`components/base-ui/`), generic UI pieces (`components/ui/`) and navigation state in the URL fragment. Base UI docs: https://base-ui.com/llms.txt.

## Rules

1. **App code never imports `@base-ui/react`;** only `components/base-ui/` does. Use every Base UI primitive over a native control (Button, Input, Select, RadioGroup, Switch, Slider, Tabs, Accordion, Dialog, AlertDialog, Toast, Collapsible, Fieldset…). Native elements only where Base UI has nothing (`<table>`, `<audio>`, text, links).
2. **Wrapper names, import aliases and file names follow [naming.md](naming.md)** (`form.tsx` holds the complementary parts `Form` + `Field` + `Input`). A variant is a prop mode of the same wrapper, not a second wrapper (`Slider` with a number or a `[start, end]` range).
3. **Wrappers stay minimal.** Composing several primitives for one use case of the app is a feature. A `ui/` piece knows no domain and calls no action.
4. **Every destructive action** (delete, reject, logout) asks first with `AlertDialog`.
5. **Navigation state lives in the URL fragment:** the active tab and the opened accordion item, as `#id`, hierarchical with `-` (`/admin#taunts-props-laughs`). Ephemeral state (open modal, drafts) stays local, and shareable filters go in the query string.
6. **No password reveal button unless the user asks.** If asked: a click toggle (never hold-to-reveal), crossed eye while hidden (the default), fixed `aria-label` + `aria-pressed`.

Details and gotchas, binding too: [details/components.md](details/components.md).

## Checklist

- [ ] No `@base-ui/react` import outside `components/base-ui/` (`grep -rn "@base-ui/react" src`).
- [ ] Every `<Icon>` uses `ICON_SIZE`, or `ICON_SIZE_SMALL` (status rows, properties, details, inline with text) / `ICON_SIZE_LARGE` (page titles, logo), unless the user set another size; any other size is a fitted mark or a focal icon that says so in its file.
- [ ] New wrappers use the Base UI docs name. Destructive actions use `AlertDialog`.
- [ ] New `Tabs`/`Accordion` values follow naming.md. Reloading with `#id` reopens the same item.
- [ ] No password reveal unless asked.
- [ ] Every `Switch` comes before its text, inside the same `<label>`.
