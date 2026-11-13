# Naming: details

Details and gotchas for the rules in [../naming.md](../naming.md).

## Details

| Name | Casing | Example |
|---|---|---|
| Component, `Props` | PascalCase | `ItemRow`, `ItemRowProps` |
| Hook, callback prop | camelCase | `useFormAction`, `onDelete` |
| File | camelCase | `passwordInput.tsx`, `useFormAction.ts` |
| CSS class | kebab-case | `.muted-text` |
| Component-owned CSS class | `<componentName>-<element>` | `.itemManager-item` |

- **Hooks:** `use` is a convention the linter (`react-hooks/rules-of-hooks`) reads, not something React checks: React tracks each hook by its call order in the render. Build one when two or more components repeat the same stateful logic (`useFormAction`), when state and effects bury a component's JSX, or when a browser API needs subscribe and unsubscribe (`useSyncExternalStore`). A value derived from props is a named const, not a hook. A hook returns an object with named fields (`{ state, isPending, formRef, handleSubmit }`), and its file is named after it (`useFormAction.ts`). Never write a `use*` function that calls no hook, such as one that only returns a constant function: import that function instead.
- **Callback props:** `<ItemRow item={item} onDelete={confirmDelete} />`. Name the event by what happened (`onClose`), never by the child's markup (`onClickCloseButton`). Use one prefix per project for the same thing, never `on*` mixed with `handle*` or `callback*` as prop names.
