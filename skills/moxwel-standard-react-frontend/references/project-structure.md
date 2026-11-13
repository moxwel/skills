# Project structure

Covers where a file goes, one export per file, one responsibility per component, types and constants.

## Rules

1. **Three UI layers:** `components/` holds minimal generic pieces with no domain knowledge, `features/<feature>/` holds complete use cases, and `app/` holds routing, data loading and auth. A piece that calls an action, knows the domain, or composes several components for one use case is a feature.
2. **Data flows down from the page.** Features never call `lib/db`: the page loads the data and passes it as props. Only `lib/db/*` imports `lib/db/connection`.
3. **One export per file,** with the file named after it and imported directly (no `index.ts` barrels). Exceptions must cover related exports only, each justified in the file header (Details).
4. **One responsibility per component:** one kind of data or one setting, with its state, actions and UI. A list with its create form and row actions is one job. A second job becomes a sibling component that the parent composes; siblings never import each other.
5. **File names follow [naming.md](naming.md).** No folder per component: `card.tsx` + `card.css` sit side by side.
6. **Constants:** routes, labels and icons live once, in `lib/const/pages.ts` (`PAGES`). `lib/const/` holds constants only, all Node-free except `paths.ts`. Shared types live in each folder's `types.ts`.

## Details

```
src/
├── app/                      # routing, data loading, auth gate; Tailwind only, no .css besides globals.css
│   ├── layout.tsx            # <html>, <body>, isolate root div, ToastProvider
│   ├── globals.css
│   ├── login/page.tsx        # public, outside (app)
│   ├── (app)/layout.tsx      # navbar + <main>; reads the session for display only, never gates
│   ├── (app)/<route>/page.tsx  # each page calls requireUser()/requireAdmin() itself
│   └── api/<resource>/route.ts
├── components/
│   ├── base-ui/              # one file per primitive, or per group of complementary parts (form.tsx: Form, Field, Input) + shared.css
│   └── ui/                   # generic pieces Base UI lacks
├── features/
│   ├── shared.css
│   └── <feature>/<piece>.tsx + <piece>.css
├── actions/
│   ├── types.ts              # ActionState = { ok?, error?, errors? }
│   └── <domain>/<action>.ts  # one "use server" action per file
└── lib/
    ├── const/                # pages (PAGES), limits, messages, layout, paths (Node only), enums
    ├── ui/                   # cn.ts, useFormAction.ts, urlFragment.ts
    ├── db/                   # connection.ts, types.ts, one file per table
    ├── auth/                 # password, session, rateLimit, requireUser, requireAdmin
    ├── validation/           # validate.ts + validate.test.ts
    ├── format/               # formatDateTime.ts, formatBytes.ts…
    └── <topic>/              # logic that isn't a query (combines db, files, processes)
```

- **What each layer imports:**
  - `features/`: `components/`, `actions/` and the Node-free parts of `lib/`.
  - `app/`: anything except `lib/db/connection` and `@base-ui/react`.
  - `actions/`: public HTTP entry points, so they hold auth + sanitizing. A helper shared by two actions goes in `lib/`.
- **Allowed multi-export files:**
  - many tiny functions on one subject (`lib/db/<table>.ts`, `validate.ts`);
  - private shared state (`rateLimit.ts`, `session.ts`, `urlFragment.ts`);
  - inseparable pairs (`hashPassword` + `verifyPassword`);
  - constants and types (`lib/const/*`, `types.ts`);
  - complementary parts of one component (`form.tsx`, `dialog.tsx`, `toast.tsx`).

  Private helpers stay unexported in the file that uses them.
- **Signs of two jobs:** the description needs "and" for unrelated things, a prop only something unrelated uses, or imports from another domain's actions. Split by responsibility, not by length: `render*` helpers and the dialogs of one job stay inside it.
- **Composing siblings:**

  ```tsx
  const settingsTab = (
    <section className="flex flex-col gap-5">
      <NotificationSettings isEnabled={isNotificationsEnabled} />
      <ItemManager items={items} />
    </section>
  );
  ```
- **`lib/const/` contents:** form limits come from `limits.ts`, and the field rule texts built from them (`NAME_RULES`) come from `messages.ts`. Types are imported with `import type`. After renaming a route, run `npx next typegen`.

## Checklist

- [ ] Each new file is in its layer and named per naming.md (one export, or a justified exception).
- [ ] Each component/feature has one job, and no feature calls `lib/db` (`import type` of row types is fine).
