# User experience

Covers the reaction the interface gives to every user action: waiting, results, errors, confirmations, data view states and optimistic updates. This file is the only place for these rules; the other references point here.

## Rules

1. **Every action gets a visible reaction.** A click, a submit, a toggle or a navigation never leaves the screen unchanged. The kind of reaction depends on the kind of action (Details).
2. **Instant actions react through their own state.** A tab, a switch, a menu or an accordion changes at once, and that change is the reaction. Every interactive element has visible `hover`, `active`, `focus-visible` and `disabled` states.
3. **Waiting is shown on the control that started it.** While an action runs, its `Button` or `AlertDialog` shows `isLoading`, and the controls that would start it again are disabled, so there is no double submit. A row action marks only its own row busy (code-style.md Details).
4. **Every result is reported.** `ok` and `error` go to a toast through `useActionToast()`, and field errors go next to their field through `state.errors`, where `Form` focuses the first invalid one. A failure is never silent: every `catch` in client code ends in a toast or an error state.
5. **Long actions show progress with text.** An action that runs for more than a second with known steps (uploads, batches) shows a Base UI `Progress` plus a text that counts them (`Uploading 3 of 5`). Without known steps, the `isLoading` of rule 3 is the reaction.
6. **Destructive actions confirm before, never undo after.** Delete, reject and logout first ask with `AlertDialog`, whose title names what is lost (`Delete Budget 2026?`). After it runs, the toast names what changed (`Budget 2026 deleted`).
7. **Quiet actions confirm in place.** An action whose effect is not visible on the page (copy to clipboard, send a link) changes its own icon and text to the result (`Copied`) for 2 seconds, inside an element with `role="status"`. No toast for these.
8. **Every view that shows data has three states:** loading, error and empty. Loading is a server `loading.tsx` in the route-group segment (Tailwind only, top on mobile and centered from `md`) with the spinner and a text naming what loads; it is also the reaction to the navigation that opens the view. Error is an `error.tsx` in the same segment with a retry action. Empty is part of the component that renders the list.
9. **Every reaction says what happened and what to do next** (copy.md rule 6 of the base skill), and reaches screen readers: toasts and the spinner are live regions, and the in-place text of rule 7 has `role="status"`.
10. **No optimistic updates, except a single-value toggle** that meets all three conditions: it changes one value (favorite, read, done), reverting it loses nothing, and the server rejects it almost never for business rules (permissions, stock, validation). Such a toggle uses `useOptimistic` and toasts only the error (Details). Everything else waits for the server with rule 3.
11. **Reactions are not animated** (styling.md rule 13): state changes apply instantly, and the spinner is static unless the user asks for rotation.

## Details

- **Reaction by kind of action:**

| Action | Reaction |
|---|---|
| Instant (tab, switch, menu, accordion) | Its own state change (rule 2) |
| Server action (create, save) | `isLoading` while it runs, then a toast or field errors (rules 3, 4) |
| Long, with known steps (upload, batch) | `Progress` with a counting text (rule 5) |
| Destructive (delete, reject, logout) | `AlertDialog` before, a toast after (rule 6) |
| Quiet (copy, send a link) | Icon and text change in place (rule 7) |
| Navigation to a data view | `loading.tsx`, then the view or its error or empty state (rule 8) |
| Single-value toggle that meets rule 10 | Optimistic change, a toast only on error |

- **Toast or inline:** a result tied to one field goes next to the field; a result of the whole action goes to a toast. A toggle that already shows its new state needs no success toast.
- **Optimistic toggle:** the optimistic value lives only while the transition runs. On success the action revalidates the page, so the prop carries the new value; on error the prop keeps the old one and React shows it again.

```tsx
const [isFavorite, setIsFavorite] = useOptimistic(item.isFavorite);
const [, startTransition] = useTransition();
const toast = useActionToast();

const toggleFavorite = () => {
  startTransition(async () => {
    setIsFavorite(!isFavorite);
    const result = await setFavorite(item.id, !isFavorite);
    if (result.error) {
      toast(result);
    }
  });
};
```

## Gotchas

- **`useOptimistic` warns and does nothing outside a transition.** Call its setter inside `startTransition` or a form action.
- **The optimistic value stays after a successful toggle only if the action revalidates.** Without `revalidatePath`, the prop keeps the old value and the toggle jumps back.

## Checklist

- [ ] Every interactive element was clicked once and gave a visible reaction (workflow-and-verification.md verification step 5).
- [ ] Every action shows `isLoading` while it runs and cannot be submitted twice.
- [ ] Every `ok` and `error` reaches a toast or a field; no `catch` ends silently.
- [ ] Destructive actions use `AlertDialog`, and the toast after names what changed.
- [ ] Every data view has loading, error and empty states that say what happens and what to do.
- [ ] No `useOptimistic` outside a single-value toggle that meets rule 10 (`grep -rn "useOptimistic" src`).
