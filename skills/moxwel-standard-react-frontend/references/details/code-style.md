# Code style: details

Details and gotchas for the rules in [../code-style.md](../code-style.md).

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
