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

## Details

- **New project:**
  1. Run `npx create-next-app@latest <name> --ts --app --src-dir --import-alias "@/*"`. Skip ESLint and accept Tailwind.
  2. Run `npm i @base-ui/react @mdi/react @mdi/js tailwind-merge`. Copy [cn.ts](../assets/cn.ts) and [useFormAction.ts](../assets/useFormAction.ts) to `src/lib/ui/`.
  3. Copy [globals.css](../assets/globals.css) to `src/app/`. Set `postcss.config.mjs` to `export default { plugins: { "@tailwindcss/postcss": {} } };`.
  4. In `next.config.ts`, set `output: "standalone"` and `allowedDevOrigins` from the `DEV_ORIGINS` env (empty by default). Set `experimental.serverActions.bodySizeLimit` (default 1 MB) only when the app accepts uploads.
  5. In `app/layout.tsx`: `<html lang>` set to the UI language (`en` by default), the body and `isolate` div from styling.md, `ToastProvider` and `metadata`.
  6. Create the folders from project-structure.md, and start the project `CLAUDE.md`/`AGENTS.md` with one short bullet per convention.
- **Tests:** `validate.test.ts` imports `./validate.ts` with its extension, so `tsconfig` needs `"allowImportingTsExtensions": true`.

```dockerfile
FROM node:24-bookworm-slim AS build
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM node:24-bookworm-slim
WORKDIR /app
ENV NODE_ENV=production NEXT_TELEMETRY_DISABLED=1 PORT=3000 HOSTNAME=0.0.0.0
COPY --from=build --chown=node:node /app/.next/standalone ./
COPY --from=build --chown=node:node /app/.next/static ./.next/static
# standalone doesn't include public/
COPY --from=build --chown=node:node /app/public ./public
USER node
EXPOSE 3000
CMD ["node", "server.js"]
```

- **`.dockerignore`:** `node_modules`, `.next`, `web-data`, `.env`, `Dockerfile`, `.dockerignore`. The live DB and the secrets must never enter the build context.
- **Compose:** `restart: unless-stopped`. Env comes from `.env` (`TZ`, `ADMIN_USER`, `ADMIN_PASSWORD`), plus `DATA_DIR: "/data"`. Volume `./web-data:/data`. Join the reverse proxy network.
- **External binaries** (ffmpeg) go in their own stage: static, with a pinned version + sha256 and minimal configure flags.
- **Rebuild:** `docker compose up -d --build <service>`.
