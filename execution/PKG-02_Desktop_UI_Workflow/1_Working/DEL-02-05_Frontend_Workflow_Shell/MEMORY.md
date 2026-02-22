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
