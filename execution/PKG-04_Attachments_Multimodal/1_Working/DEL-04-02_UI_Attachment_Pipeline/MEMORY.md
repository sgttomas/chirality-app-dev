# Working Memory — DEL-04-02

*This file is shared working memory for WORKING_ITEMS and TASK agents operating on this deliverable.*

## Key Decisions

- 2026-02-24: Implemented a dedicated file picker modal (`frontend/src/components/shell/file-picker.tsx`) using `GET /api/working-root/tree` depth=1 for directory navigation + multi-select.
- 2026-02-24: Enforced client-side extension filter parity with SPEC Section 9.8 via shared constant set in `frontend/src/lib/harness/ui-attachments.ts` (`.png`, `.jpg`, `.jpeg`, `.gif`, `.webp`, `.pdf`, `.txt`, `.md`, `.csv`).
- 2026-02-24: Upgraded `chat-panel.tsx` to support preview chips, attachments-only send, and API payloads that send attachment paths only (`attachments: string[]`), preserving non-authoritative client metadata boundaries.
- 2026-02-24: Added optimistic rollback behavior on send failure to remove optimistic user/assistant placeholders and restore preserved draft + attachment selections.
- 2026-02-24: Added draft rehydration storage helpers (`frontend/src/lib/harness/chat-draft.ts`) + attachment shape sanitization (`sanitizeStoredAttachments`) so malformed entries are silently dropped.

## Open Questions

- Should picker navigation remain restricted to descendants of `projectRoot` (current behavior), or should it support broader filesystem browsing in a later pass?
- Should client-side pre-send file-size and cumulative-budget checks be added, or remain server-enforced only per current scope boundary?

## Notes

- New attachment helper tests:
  - `frontend/src/__tests__/lib/harness-ui-attachments.test.ts`
  - `frontend/src/__tests__/lib/harness-chat-draft.test.ts`
  - `frontend/src/__tests__/lib/harness-client.test.ts` includes attachment-only payload coverage.
- Verification run (2026-02-24):
  - `npm run typecheck`
  - `npm test -- src/__tests__/lib/harness-client.test.ts src/__tests__/lib/harness-ui-attachments.test.ts src/__tests__/lib/harness-toolkit.test.ts src/__tests__/lib/harness-chat-draft.test.ts`
