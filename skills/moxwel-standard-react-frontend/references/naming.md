# Naming

Covers every name in a project: identifiers, functions, hooks, props, files, database functions, CSS classes and fragment ids. General naming rules (casing, booleans, constants, UUID ids) are in the base skill's `naming.md`; this file is the only place for the React, Next, database and CSS names, and every other reference points here.

## Rules

1. **The base naming rules apply in full:** casing, no single-letter names, booleans, values named after their content, constants and UUID ids (schema details in [database.md](database.md)). Names a framework fixes (`metadata`) and HTML or Base UI props stay as they are.
2. **Functions are verb + subject** (`formatBytes`, `listItems`). Helpers that return JSX are `render*`. Query functions in `lib/db/<table>.ts` use `list*`, `find*`/`get*` (one result or `undefined`), `count*`, `insert*`, `update*`/`mark*`, `softDelete*`, and `delete*` for technical data only; the module is imported as a namespace named `<table>Db` (`import * as itemsDb`). A server action is named after what it does and its file after it (`actions/<domain>/<action>.ts`).
3. **Hooks:** a function that calls a React hook is named `use*`, and a function that calls none never is: pure helpers and the functions you pass to a hook (`subscribe`) keep plain names. Only components and other hooks call a hook, at the top level (never in `if`, loops or callbacks). Build a hook only to share stateful logic or to take it out of a crowded component (Details).
4. **Callback props are `on*`:** `on` + the event as the child sees it (`onSelect`, `onDelete`, `onClose`), typed in the local `Props`. The function the parent passes is named after the action (`confirmDelete`). Names fixed by HTML or Base UI stay as they are (`onSubmit`, `onValueChange`). Add one only when the parent owns the result (state, an action, navigation); a child that can do it alone does not take a callback.
5. **A component's props type is named `Props`.** Secondary components and the parts of a complementary file use `<Name>Props`.
6. **Files are camelCase,** named after their export (`formatBytes.ts`, `passwordInput.tsx`), or after their subject for a file of complementary parts (`form.tsx`). A component's CSS has the same name beside it (`card.tsx` + `card.css`). Base UI wrappers match the Base UI docs exactly (`AlertDialog`, never `ConfirmDialog`), and the import of the original takes a `Base` prefix.
7. **CSS classes are kebab-case** (`.muted-text`), except a class that a React component or feature owns: it is `<componentName>-<element>`, with the component name as in its camelCase file name and the element in kebab-case (`.itemManager-item`, `.itemManager-item-name`). The root element takes the bare component name (`.badge`). The classes in a folder's `shared.css` are named by purpose, never with a component prefix. Keyframes are `<component>-<verb>`. State goes in data attributes, never in modifier classes.
8. **Fragment ids** (`Tabs`, `Accordion` values) are lowercase slugs without `-`, because `-` is the separator. Nested wrappers take a `fragmentPrefix`.

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

## Checklist

- [ ] The base naming.md checklist passes.
- [ ] No `use*` function without a hook inside, and no hook call outside a `use*` function or a component.
- [ ] Callback props are `on*`; the parent's function is named after the action.
- [ ] A file is named after its single export; a Base UI wrapper keeps the Base UI name.
- [ ] CSS classes are kebab-case, or `<componentName>-<element>` when a component owns them.
- [ ] Tab and accordion ids are slugs without `-`.
