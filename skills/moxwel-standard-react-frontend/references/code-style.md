# Code style

Covers every `.ts`/`.tsx` file (headers and line length also cover CSS) where React differs from the base skill: comments, JSX composition, client vs server, forms and imports.

## Rules

1. **Language, headers and doc comments follow the base `moxwel-code-style` skill** (`comments-and-docs.md`, `copy.md`). In React code that also means: the header goes before `"use client"`/`"use server"` (config files need none), `aria-label`, `title`, errors and toasts are UI strings, and route segments follow the UI language.
2. **Readability follows the base skill** (`readability.md`): 120 columns, named conditions, flat control flow, derived values named before the return, grouped and sorted imports. React adds the `render*` helpers and import groups in [details](details/code-style.md).
3. **Names follow [naming.md](naming.md):** casing, booleans, functions, hooks, callback props, files, CSS classes and constants all live there.
4. **Props live in a local type** right before the component, never inline in the signature (its name is in naming.md).
5. **`"use client"` only when needed:** state or effects (including hooks built on them), event handlers the component creates, or browser APIs. Pages and layouts stay server components. Hooks and helpers imported only by client code need no directive.
6. **Forms keep their values on failure:** never use the `<Form action>` prop. Use `useFormAction`, which resets only on `ok`.
7. **Validate everything, then execute:** nothing slow or with side effects runs until every check that can run has passed. Every field the server requires carries its HTML constraint (`required` on selects too), so the Form blocks the submit. A form that processes data before sending first calls a server pre-check action with the same `lib/` validation as the final action (without uploading files), and the final action validates again.
8. **Output:** rely on React's escaping. Never use `dangerouslySetInnerHTML`. User-influenced URL segments go through `encodeURIComponent`.

Details and gotchas, binding too: [details/code-style.md](details/code-style.md).

## Checklist

- [ ] The base skill's checklists pass (comments, naming, readability, copy), and naming.md for the React names.
- [ ] No inline prop types.
- [ ] `"use client"` only where needed. No `<Form action=` (`grep -rn "<Form action=" src`).
- [ ] Forms validate fully before processing or sending.
- [ ] `python3 <skill>/scripts/checkImports.py src` prints nothing (`--fix` reorders).
