# Working Memory — DEL-02-01

*This file is shared working memory for WORKING_ITEMS and TASK agents operating on this deliverable.*

## Key Decisions

- 2026-02-24: Refresh cadence set to `15s` (`FILE_TREE_POLL_INTERVAL_MS = 15_000`) for baseline external-change detection without tight-loop polling.
- 2026-02-24: Hidden-window policy resolved for this implementation pass: skip periodic polling while `document.visibilityState === 'hidden'`; run debounced refresh when window returns to visible/focus and restart polling cadence.
- 2026-02-24: Expand/collapse interaction introduced in the FileTree view with per-node path state retained across refresh cycles.

## Open Questions

- REQ-03a symlink/alias policy resolved (2026-02-24): symlinks are displayed as leaf nodes with `kind: 'symlink'` and `LNK` visual indicator in the FileTree; no traversal into symlink-to-directory targets (prevents circular symlink infinite loops). Implemented in `buildTree()` via explicit `isSymbolicLink()` check before `isDirectory()` check.
- REQ-09 lifecycle status badges in FileTree remain out-of-scope for this pass.
- REQ-10 security verification evidence (contextIsolation/nodeIntegration/preload-only FS bridge) is unchanged by this pass and should be recorded in a dedicated audit pass.

## Notes

- Baseline implementation landed in:
  - `frontend/src/components/shell/file-tree-panel.tsx`
  - `frontend/src/lib/workspace/file-tree-refresh.ts`
  - `frontend/src/app/globals.css`
- Added verification coverage for refresh helpers and external-change route behavior:
  - `frontend/src/__tests__/lib/workspace-file-tree-refresh.test.ts`
  - `frontend/src/__tests__/api/working-root/tree-route.test.ts`
- REQ-03a implementation landed in (2026-02-24):
  - `frontend/src/lib/workspace/filesystem.ts` — `TreeNode.kind` extended to `'symlink'`; `buildTree()` checks `isSymbolicLink()` first
  - `frontend/src/components/shell/file-tree-panel.tsx` — `LNK` icon for symlink nodes
  - `frontend/src/__tests__/api/working-root/tree-route.test.ts` — symlink regression test (dir-link + file-link both shown as `kind: 'symlink'`, no traversal into link-to-dir targets)
- Verification results (frontend workspace):
  - `npm test` -> PASS (`260` tests)
  - `npm run build` -> PASS
  - `npm run typecheck` -> PASS
