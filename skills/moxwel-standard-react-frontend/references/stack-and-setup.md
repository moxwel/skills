# Stack and setup

Covers the stack, scaffolding a new project, Docker and deployment.

## Rules

1. **Stack:**
   - Next.js 16+ App Router (`output: "standalone"`), React 19, TypeScript strict with the `@/*` alias, Node 24.
   - `@base-ui/react`, `@mdi/react` + `@mdi/js`.
   - Tailwind v4 without preflight + `tailwind-merge`, plus plain CSS.
   - SQLite via `node:sqlite` by default (another engine only per database.md "Engine"). Hand-rolled auth.
2. **No extra dependencies unless the user asks:** no ESLint, Prettier, Jest, ORM, state library, CSS-in-JS, component kit, or form/date library. Tests are only `node --test` for pure functions.
3. **The container runs as non-root (`USER node`),** with no published ports, no Docker socket and `:ro` mounts where possible. The one allowed port is a temporary LAN port, commented and labeled "Temporary", with its host port from `.env`. Never re-enable a port the user commented out.
4. **Deployment values and secrets** follow security-management.md rule 8. Only `lib/const/paths.ts` builds absolute paths (from `DATA_DIR`).
5. **Rebuild only the changed service.** Never restart unrelated containers.

Details and gotchas, binding too: [details/stack-and-setup.md](details/stack-and-setup.md).

