# Naming

Covers every name in a project: identifiers, functions, hooks, props, files, database functions, CSS classes and fragment ids. This file is the only place where naming rules live; every other reference points here.

## Rules

1. **Identifiers are English,** whatever language the UI strings use.
2. **Casing:** PascalCase for components and types, UPPER_CASE for module-level constants (values fixed when the module loads: literals and values derived from them or from env), camelCase for everything else. Exceptions: names a framework fixes (`metadata`), and row types, which keep their DB column names (`created_at`). No single-letter names, except the loop index `i`.
3. **Values are named after their content** (`visibleLinks`, `rootClassName`), handlers and commands after the action (`confirmDelete`). A comparison or compound condition becomes a named const (`const hasErrors = Object.keys(errors).length > 0;`). Non-obvious literals become constants at the top of the file, or in `lib/const/` when app-wide.
4. **Booleans are named `is*`/`has*`/`can*`/`should*`/`was*`:** variables, state, hook results, own props, predicates. Exceptions: names fixed by HTML/React/Base UI (`disabled`, `open`), and commands that report success (`insertItem()`).
5. **Functions are verb + subject** (`formatBytes`, `listItems`). Helpers that return JSX are `render*`. Query functions in `lib/db/<table>.ts` use `list*`, `find*`/`get*` (one result or `undefined`), `count*`, `insert*`, `update*`/`mark*`, `softDelete*`, and `delete*` for technical data only; the module is imported as a namespace named `<table>Db` (`import * as itemsDb`). A server action is named after what it does and its file after it (`actions/<domain>/<action>.ts`).
6. **Hooks:** a function that calls a React hook is named `use*`, and a function that calls none never is: pure helpers and the functions you pass to a hook (`subscribe`) keep plain names. Only components and other hooks call a hook, at the top level (never in `if`, loops or callbacks). Build a hook only to share stateful logic or to take it out of a crowded component (Details).
7. **Callback props are `on*`:** `on` + the event as the child sees it (`onSelect`, `onDelete`, `onClose`), typed in the local `Props`. The function the parent passes is named after the action (`confirmDelete`). Names fixed by HTML or Base UI stay as they are (`onSubmit`, `onValueChange`). Add one only when the parent owns the result (state, an action, navigation); a child that can do it alone does not take a callback.
8. **A component's props type is `Props`,** local and right before the component. Secondary components and the parts of a complementary file use `<Name>Props`.
9. **Files are camelCase,** named after their export (`formatBytes.ts`, `passwordInput.tsx`), or after their subject for a file of complementary parts (`form.tsx`). A component's CSS has the same name beside it (`card.tsx` + `card.css`). Base UI wrappers match the Base UI docs exactly (`AlertDialog`, never `ConfirmDialog`), and the import of the original takes a `Base` prefix.
10. **CSS classes are kebab-case** (`.muted-text`), except a class that a React component or feature owns: it is `<componentName>-<element>`, with the component name as in its camelCase file name and the element in kebab-case (`.itemManager-item`, `.itemManager-item-name`). The root element takes the bare component name (`.badge`). The classes in a folder's `shared.css` are named by purpose, never with a component prefix. Keyframes are `<component>-<verb>`. State goes in data attributes, never in modifier classes.
11. **Fragment ids** (`Tabs`, `Accordion` values) are lowercase slugs without `-`, because `-` is the separator. Nested wrappers take a `fragmentPrefix`.
12. **Records tied to a user or made public are identified by a UUID,** never by an ascending number. The rule and its schema details are in [database.md](database.md) (rule 9).

## Details

| Name | Casing | Example |
|---|---|---|
| Component, type, `Props` | PascalCase | `ItemRow`, `ReviewStatus`, `ItemRowProps` |
| Module-level constant | UPPER_CASE | `MAX_RETRIES`, `PAGES` |
| Variable, function, hook, prop | camelCase | `visibleLinks`, `formatBytes`, `useFormAction`, `onDelete` |
| File | camelCase | `passwordInput.tsx`, `useFormAction.ts` |
| CSS class | kebab-case | `.muted-text` |
| Component-owned CSS class | `<componentName>-<element>` | `.itemManager-item` |

- **Hooks:** `use` is a convention the linter (`react-hooks/rules-of-hooks`) reads, not something React checks: React tracks each hook by its call order in the render. Build one when two or more components repeat the same stateful logic (`useFormAction`), when state and effects bury a component's JSX, or when a browser API needs subscribe and unsubscribe (`useSyncExternalStore`). A value derived from props is a named const, not a hook. A hook returns an object with named fields (`{ state, isPending, formRef, handleSubmit }`), and its file is named after it (`useFormAction.ts`). Never write a `use*` function that calls no hook, such as one that only returns a constant function: import that function instead.
- **Callback props:** `<ItemRow item={item} onDelete={confirmDelete} />`. Name the event by what happened (`onClose`), never by the child's markup (`onClickCloseButton`). Use one prefix per project for the same thing, never `on*` mixed with `handle*` or `callback*` as prop names.

## Checklist

- [ ] Casing follows the table; constants are UPPER_CASE; no single-letter names besides `i`.
- [ ] Every boolean has its prefix; no `use*` function without a hook inside, and no hook call outside a `use*` function or a component.
- [ ] Callback props are `on*`; the parent's function is named after the action.
- [ ] A file is named after its single export; a Base UI wrapper keeps the Base UI name.
- [ ] CSS classes are kebab-case, or `<componentName>-<element>` when a component owns them.
- [ ] Tab and accordion ids are slugs without `-`.
