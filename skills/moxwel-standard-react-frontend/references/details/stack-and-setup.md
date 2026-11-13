# Stack and setup: details

Details and gotchas for the rules in [../stack-and-setup.md](../stack-and-setup.md).

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
