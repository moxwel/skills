# Code style

Covers every `.ts`/`.tsx` file (headers and line length also cover CSS) where React differs from the base skill: comments, JSX composition, client vs server, forms and imports.

## Rules

1. **Language, headers and doc comments follow the base `moxwel-code-style` skill** (`comments-and-docs.md`, `copy.md`). In React code that also means: the header goes before `"use client"`/`"use server"` (config files need none), `aria-label`, `title`, errors and toasts are UI strings, and route segments follow the UI language.
2. **Readability follows the base skill** (`readability.md`): 120 columns, named conditions, flat control flow, derived values named before the return, grouped and sorted imports. React adds the `render*` helpers and import groups in Details.
3. **Names follow [naming.md](naming.md):** casing, booleans, functions, hooks, callback props, files, CSS classes and constants all live there.
4. **Props live in a local type** right before the component, never inline in the signature (its name is in naming.md).
5. **`"use client"` only when needed:** state or effects (including hooks built on them), event handlers the component creates, or browser APIs. Pages and layouts stay server components. Hooks and helpers imported only by client code need no directive.
6. **Forms keep their values on failure:** never use the `<Form action>` prop. Use `useFormAction`, which resets only on `ok`.
7. **Validate everything, then execute:** nothing slow or with side effects runs until every check that can run has passed. Every field the server requires carries its HTML constraint (`required` on selects too), so the Form blocks the submit. A form that processes data before sending first calls a server pre-check action with the same `lib/` validation as the final action (without uploading files), and the final action validates again.
8. **Output:** rely on React's escaping. Never use `dangerouslySetInnerHTML`. User-influenced URL segments go through `encodeURIComponent`.

## Details

- **Doc comments in React code:** a component documents only the props that `Props` does not make obvious (`[props.x=default]` when optional). `@throws` applies when the function throws on purpose or calls one whose JSDoc has it without catching; Next's `redirect()`/`notFound()` are control flow, not throws.

```ts
/**
 * Marks the suggestion as reviewed if it is still pending.
 * @returns false if it doesn't exist or was already reviewed.
 */
export function markSuggestionReviewed(id: string, status: ReviewStatus): boolean {
```

- **Routes** always come from `PAGES`.
- **Component body order:** hooks → derived consts → `render*` helpers → named JSX blocks (`createForm`, `userTable`) → a short `return` that composes them.
- **JSX details:** render conditionally through a named boolean (`{isEmpty && …}`). Build classes with `cn()`, never by concatenation. Optional data attributes use `data-active={isActive || undefined}`. Lists use a stable `key`.
- **Client code** imports from `lib/` only Node-free modules (such as `lib/const/*` except `paths`, `lib/ui/*`, `lib/format/*`), plus types via `import type`.
- **Forms** ([useFormAction template](../assets/useFormAction.ts)):

```tsx
const { state, isPending: isCreating, formRef, handleSubmit } = useFormAction(createUser);
const toast = useActionToast();
useEffect(() => {
  toast(state);
}, [state, toast]);

<Form ref={formRef} onSubmit={handleSubmit} errors={state.errors}>
  <Field name="username" label="Username"><Input name="username" required /></Field>
  <div className={FORM_ACTIONS_LAYOUT}>
    <Button type="submit" icon={mdiAccountPlus} isLoading={isCreating}>Create user</Button>
  </div>
</Form>
```

- **Form behavior:**
  - Field errors come back in `state.errors`, keyed by field name, and `ok`/`error` messages go to a toast.
  - A generic error with no field (login) moves no focus, so that form focuses its first field itself.
  - Non-form actions (delete, toggle) use `useTransition` + the busy row's id.
  - HTML constraints mirror the server's rules, and the server stays the authority.
- **Import order** (the base rules apply; these are the React groups):
  - Groups, in order: external, `@/actions`, `@/components`, `@/features`, `@/lib`, relative, then `import type` (same group order inside), then CSS (`shared.css` first, the file's own last). Alphabetical within each group.
  - `lib/db/<table>.ts` is always imported as a namespace (`import * as itemsDb`).
  - Use the `@/` alias across folders and relative paths inside one.

## Gotchas

- **Form wiped after a failed submit.** With the `action` prop, React 19 resets uncontrolled fields whenever the action completes, even when it returns an error state.
- **`useEffect(() => toast(state))` crashes** because the effect returns a value. Use braces.

## Checklist

- [ ] The base skill's checklists pass (comments, naming, readability, copy), and naming.md for the React names.
- [ ] No inline prop types.
- [ ] `"use client"` only where needed. No `<Form action=` (`grep -rn "<Form action=" src`).
- [ ] Forms validate fully before processing or sending.
- [ ] `python3 <skill>/scripts/checkImports.py src` prints nothing (`--fix` reorders).
