# Project structure

Covers where a file goes, one export per file, one responsibility per component, types and constants.

## Rules

1. **Three UI layers:** `components/` holds minimal generic pieces with no domain knowledge, `features/<feature>/` holds complete use cases, and `app/` holds routing, data loading and auth. A piece that calls an action, knows the domain, or composes several components for one use case is a feature.
2. **Data flows down from the page.** Features never call `lib/db`: the page loads the data and passes it as props. Only `lib/db/*` imports `lib/db/connection`.
3. **One export per file,** with the file named after it and imported directly (no `index.ts` barrels). Exceptions must cover related exports only, each justified in the file header ([details](details/project-structure.md)).
4. **One responsibility per component:** one kind of data or one setting, with its state, actions and UI. A list with its create form and row actions is one job. A second job becomes a sibling component that the parent composes; siblings never import each other.
5. **File names follow [naming.md](naming.md).** No folder per component: `card.tsx` + `card.css` sit side by side.
6. **Constants:** routes, labels and icons live once, in `lib/const/pages.ts` (`PAGES`). `lib/const/` holds constants only, all Node-free except `paths.ts`. Shared types live in each folder's `types.ts`.

Details and gotchas, binding too: [details/project-structure.md](details/project-structure.md).

## Checklist

- [ ] Each new file is in its layer and named per naming.md (one export, or a justified exception).
- [ ] Each component/feature has one job, and no feature calls `lib/db` (`import type` of row types is fine).
