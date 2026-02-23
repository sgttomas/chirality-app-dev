# Memory — DEL-02-05

## Key Decisions & Human Rulings

- 2026-02-22: Implemented a single shared shell frame across `PORTAL`, `PIPELINE`, and `WORKBENCH` so file-tree and chat containers are always available.
- 2026-02-22: `projectRoot` is stored in local browser storage (`chirality.projectRoot`) for current-session continuity and fast route reload behavior.
- 2026-02-22: Native directory picking is exposed through Electron IPC (`chirality:select-directory`) with manual absolute-path fallback when Electron bridge is unavailable.
- 2026-02-22: PIPELINE OPERATIVE categories are rendered with explicit "coming soon" disabled options where functionality is intentionally not active yet (e.g., DECOMP BASE, selected TASK/AUDIT lanes).

## Domain Context

- DEL-02-05 is part of SCA-001 Wave 0c and is a pre-tier gate deliverable that must reach `IN_PROGRESS` before Tier 2 code-bearing resumption.
- Upstream preconditions from DEL-01-03 and DEL-03-07 are now materially present (`frontend/` workspace + harness API baseline), enabling actual shell wiring instead of document-only posture.

## Open Items

- Wire WORKBENCH chat panel to live turn/session APIs (currently structural container + local echo behavior only).
- Finalize accessibility posture (keyboard matrix navigation/focus strategy) once REQ-15 ruling is explicit.
- Confirm restart-persistence policy for `projectRoot` (current implementation persists in local storage; this may exceed "session-only" depending on final ruling).

## Proposal History

- 2026-02-22: Added shell and workspace components:
  - `frontend/src/components/shell/app-shell.tsx`
  - `frontend/src/components/shell/file-tree-panel.tsx`
  - `frontend/src/components/shell/chat-panel.tsx`
  - `frontend/src/components/portal/agent-matrix.tsx`
  - `frontend/src/components/workspace/workspace-provider.tsx`
- 2026-02-22: Added pages and routing surfaces:
  - `frontend/src/app/page.tsx`
  - `frontend/src/app/pipeline/page.tsx`
  - `frontend/src/app/pipeline/pipeline-client.tsx`
  - `frontend/src/app/workbench/page.tsx`
  - `frontend/src/app/workbench/workbench-client.tsx`
  - `frontend/src/app/not-found.tsx`
- 2026-02-22: Added working-root API surfaces:
  - `frontend/src/app/api/working-root/validate/route.ts`
  - `frontend/src/app/api/working-root/tree/route.ts`
  - `frontend/src/app/api/working-root/scope/route.ts`
  - `frontend/src/lib/workspace/filesystem.ts`
- 2026-02-22: Added Electron directory-picker bridge:
  - `frontend/electron/main.ts`
  - `frontend/electron/preload.ts`
  - `frontend/src/types/chirality-window.d.ts`
- 2026-02-22: Updated shell styling and provider wrapping:
  - `frontend/src/app/globals.css`
  - `frontend/src/app/layout.tsx`

Verification evidence:
- `npm run test` -> PASS (7/7).
- `npm run typecheck` -> PASS.
- `npm run build` -> PASS (Next.js + Electron TS).

## Interface & Dependency Notes

- DEL-02-05 now consumes DEL-03-07 API baseline via live Working Root scans and route-ready shell context, while preserving strict local-only filesystem execution.
- TASK split selector dynamically reads deliverables and knowledge types from selected `projectRoot` and honors `_Decomposition` domain marker presence for knowledge-type visibility.
- No `Dependencies.csv` edits were made in this pass; dependency metadata rerun is not triggered by structure-only and code-only implementation changes.

## Pass-11 Evidence Refresh (2026-02-22)

- Added Pipeline integration consumers for DEL-05-03/DEL-05-04 contract routes:
  - `frontend/src/lib/workspace/deliverable-api.ts`
  - `frontend/src/app/pipeline/pipeline-client.tsx`
  - `frontend/src/app/globals.css`
  - `frontend/src/__tests__/lib/workspace-deliverable-api.test.ts`
- PIPELINE now loads selected deliverable contract snapshots from:
  - `GET /api/working-root/deliverable/status`
  - `GET /api/working-root/deliverable/dependencies`
- PIPELINE now supports lifecycle transition submission through:
  - `POST /api/working-root/deliverable/status/transition`
  - actor/date/optional approval-SHA controls plus typed error presentation.
- Added dependency summary UI for active rows, active upstream blocker candidates, and satisfaction-status distribution.
- Verification results for this pass (in `frontend/`):
  - `npm test` -> PASS (42 tests total)
  - `npm run typecheck` -> PASS (rerun sequentially after build to avoid transient `.next/types` race)
  - `npm run build` -> PASS

## Pass-12 Evidence Refresh (2026-02-23)

- Chat panel is now wired to live harness routes instead of local echo placeholders:
  - `frontend/src/components/shell/chat-panel.tsx`
  - `frontend/src/lib/harness/client.ts`
  - `frontend/src/lib/harness/error-display.ts`
- WORKBENCH now consumes deliverable lifecycle/dependency contract APIs in a read-only contract panel:
  - `frontend/src/app/workbench/workbench-client.tsx`
- App shell now wraps `ChatPanel` in `Suspense` to satisfy App Router search-param CSR boundary requirements during static prerender:
  - `frontend/src/components/shell/app-shell.tsx`
- Styling updates for runtime status/error states and WORKBENCH contract layout:
  - `frontend/src/app/globals.css`
- Added regression tests:
  - `frontend/src/__tests__/lib/harness-client.test.ts`
  - `frontend/src/__tests__/lib/harness-error-display.test.ts`
- Verification results for this pass (in `frontend/`):
  - `npm run build` -> PASS
  - `npm run typecheck` -> PASS
  - `npm test` -> PASS (48 tests total)
