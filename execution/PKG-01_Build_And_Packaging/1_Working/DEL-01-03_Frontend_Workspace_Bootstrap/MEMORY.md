# Memory — DEL-01-03

> Organize by semantic topic, then chronologically within each topic. These headings are the minimum schema — add new sections as needed to capture what matters for this deliverable.

## Key Decisions & Human Rulings

- 2026-02-22: Bootstrap implemented as a standalone `frontend/` workspace with Next.js + Electron + TypeScript and electron-builder baseline configuration in `frontend/package.json`.
- 2026-02-22: Packaging baseline includes instruction-root resources via electron-builder `extraResources` (`../agents` -> `agents`, `../docs` -> `docs`) to satisfy SOW-047 intent.
- 2026-02-22: Initial bootstrap used `output: 'export'` for deterministic file loading; later superseded by server-capable Next runtime once DEL-03-07 introduced API routes.
- 2026-02-22: Updated runtime integration after DEL-03-07 route baseline: removed static export mode and switched Electron packaged runtime to local Next server startup, resolving API-route incompatibility.

## Domain Context

- DEL-01-03 is the first pre-tier gate item in Scope Amendment A1 (`Wave 0a`) and must reach `IN_PROGRESS` before Wave 0b (`DEL-03-07`) can start.
- Deliverable objective is bootstrap viability, not feature completion; downstream deliverables own API routes (`DEL-03-07`) and UI shell implementation (`DEL-02-05`).

## Open Items

- Optional hardening: set explicit `author` and custom app icon in `frontend/package.json` build metadata to remove electron-builder warnings.

## Proposal History

- 2026-02-22: Created `frontend/` workspace and bootstrap files:
  - `frontend/package.json`
  - `frontend/tsconfig.json`
  - `frontend/tsconfig.electron.json`
  - `frontend/next.config.mjs`
  - `frontend/next-env.d.ts`
  - `frontend/.gitignore`
  - `frontend/electron/main.ts`
  - `frontend/electron/preload.ts`
  - `frontend/src/app/layout.tsx`
  - `frontend/src/app/page.tsx`
  - `frontend/src/app/globals.css`
- 2026-02-22: Attempted `npm install` in sandbox:
  - Initial run failed writing npm logs to `~/.npm` (sandbox write-scope issue).
  - Retried with `NPM_CONFIG_CACHE=/tmp/npm-cache`.
  - Install still failed with `ENOTFOUND` on `https://registry.npmjs.org/next` (DNS/network restriction in sandbox).
  - Evidence log: `/tmp/npm-cache/_logs/2026-02-22T16_21_45_641Z-debug-0.log`.
- 2026-02-22: Verification completed via elevated execution:
  - `npm install --no-audit --no-fund` succeeded.
  - `npm run build` succeeded (Next static output + Electron TypeScript build).
  - `npm run typecheck` succeeded.
  - `npm run dev` reached Next ready state at `http://localhost:3000` and was manually stopped (SIGINT) after startup proof.
  - `npm run desktop:pack` produced `dist/mac-arm64/Chirality.app`.
  - `npm run desktop:dist` produced `dist/Chirality-0.1.0-arm64.dmg` and block map.
  - Non-local dependency audit (`grep -E '(git\\+|file:\\.\\.|link:|workspace:)' frontend/package.json`) returned no matches.
  - Instruction root inclusion verified in packaged app resources:
    - `dist/mac-arm64/Chirality.app/Contents/Resources/agents/`
    - `dist/mac-arm64/Chirality.app/Contents/Resources/docs/`
  - Architecture verification:
    - `dist/mac-arm64/Chirality.app/Contents/MacOS/Chirality` reports Mach-O arm64.

## Interface & Dependency Notes

- Downstream pre-tier dependencies are now materially unblocked from a filesystem-shape perspective:
  - `DEL-03-07` expected paths can now root under `frontend/`
  - `DEL-02-05` and `DEL-07-03` can consume established Next app structure (`frontend/src/app/`)
- No dependency row edits were made in this pass (`Dependencies.csv` unchanged), so DEPENDENCIES rerun was not triggered here.
