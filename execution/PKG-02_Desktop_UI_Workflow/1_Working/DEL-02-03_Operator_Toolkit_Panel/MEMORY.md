# Working Memory — DEL-02-03

*This file is shared working memory for WORKING_ITEMS and TASK agents operating on this deliverable.*

## Key Decisions

- 2026-02-24: Added a shared toolkit provider (`frontend/src/components/workspace/toolkit-provider.tsx`) so CONFIG visibility, opts values, and presets are centrally managed as non-authoritative local UI state.
- 2026-02-24: Implemented Operator Toolkit sidebar (`frontend/src/components/shell/operator-toolkit-panel.tsx`) with persisted visibility toggle, opts subset controls (`model`, `tools`, `maxTurns`, optional `subagentGovernance`), preset save/apply/delete, and payload preview.
- 2026-02-24: Wired toolkit opts into both `POST /api/harness/session/boot` and `POST /api/harness/turn` request paths from `chat-panel.tsx` with omission of unset fields to preserve runtime fallback semantics.
- 2026-02-24: Added toolkit helper tests in `frontend/src/__tests__/lib/harness-toolkit.test.ts` to validate payload shaping, state sanitization, and preset ordering behavior.
- 2026-02-24: Hardened toolkit persistence failure handling: `ToolkitProvider` now catches localStorage read/write failures, falls back to in-memory state for the active session, and surfaces an operator-visible warning banner with dismiss action in `OperatorToolkitPanel`.

## Open Questions

- Should presets remain global to the frontend workspace, or become scoped per `projectRoot` in a follow-up pass?
- Should `REQ-08` be upgraded from SHOULD to MUST (per existing conflict table CT-001) for lifecycle completion criteria?

## Notes

- Related shell/layout updates:
  - `frontend/src/app/layout.tsx` now wraps children with `ToolkitProvider`.
  - `frontend/src/components/shell/app-shell.tsx` now renders the CONFIG checkbox (`Show Tool Kit sidebar`) and conditionally shows the toolkit panel.
  - `frontend/src/app/globals.css` includes new toolkit panel and responsive grid styles.
- Verification run (2026-02-24):
  - `npm run typecheck`
  - `npm test -- src/__tests__/lib/harness-client.test.ts src/__tests__/lib/harness-ui-attachments.test.ts src/__tests__/lib/harness-toolkit.test.ts src/__tests__/lib/harness-chat-draft.test.ts`
  - `HARNESS_BASE_URL=http://127.0.0.1:3000 npm run harness:validate:premerge` (run twice; both pass)
