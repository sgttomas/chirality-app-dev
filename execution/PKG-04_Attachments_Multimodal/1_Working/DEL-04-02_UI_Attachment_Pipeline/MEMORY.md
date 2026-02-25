# Working Memory — DEL-04-02

*This file is shared working memory for WORKING_ITEMS and TASK agents operating on this deliverable.*

## Key Decisions

- 2026-02-24: Implemented a dedicated file picker modal (`frontend/src/components/shell/file-picker.tsx`) using `GET /api/working-root/tree` depth=1 for directory navigation + multi-select.
- 2026-02-24: Enforced client-side extension filter parity with SPEC Section 9.8 via shared constant set in `frontend/src/lib/harness/ui-attachments.ts` (`.png`, `.jpg`, `.jpeg`, `.gif`, `.webp`, `.pdf`, `.txt`, `.md`, `.csv`).
- 2026-02-24: Upgraded `chat-panel.tsx` to support preview chips, attachments-only send, and API payloads that send attachment paths only (`attachments: string[]`), preserving non-authoritative client metadata boundaries.
- 2026-02-24: Added optimistic rollback behavior on send failure to remove optimistic user/assistant placeholders and restore preserved draft + attachment selections.
- 2026-02-24: Added draft rehydration storage helpers (`frontend/src/lib/harness/chat-draft.ts`) + attachment shape sanitization (`sanitizeStoredAttachments`) so malformed entries are silently dropped.
- 2026-02-24: Hardened draft persistence with local-storage failure resilience in `chat-panel.tsx` using new `readChatDraftSnapshotFromStorage`/`persistChatDraftSnapshotToStorage` helpers, including corrupt-state reset and an operator-visible dismissible warning when storage is unavailable.
- 2026-02-24: DEL-04-01/DEL-04-02 REQ-08 interface contract closed: pre-stream `ATTACHMENT_FAILURE` now carries structured `details` (`category`, `attachmentErrors[]`, `rejectedAttachmentCount`) and UI error mapping now renders bounded rejected-file context for operator guidance.
- 2026-02-24: DEL-04-01/DEL-04-02 CT-002 interface closure: partial-failure warning text now follows deterministic structure (counted header + `Rejected attachments:` + filename/reason bullets + omission summary), with route regression assertions updated.
- 2026-02-24: Executed live runtime validation pass for attachment rollback/error UX triggers against localhost harness routes:
  - attachment-only with invalid attachment -> `400 ATTACHMENT_FAILURE`
  - text + invalid attachment -> `200` SSE stream with explicit `Attachment warning` + `process:exit` (`exitCode=0`)
  - run completed with session boot/delete success and no cleanup residue.
- 2026-02-24: Human approved direct lifecycle promotion from `IN_PROGRESS` to `ISSUED` without intermediate `CHECKING` for same-session end-to-end review/signoff.

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
- Additional verification pass (2026-02-24):
  - `npm run typecheck`
  - `npm test -- src/__tests__/lib/harness-chat-draft.test.ts src/__tests__/lib/harness-ui-attachments.test.ts src/__tests__/lib/harness-client.test.ts src/__tests__/lib/harness-toolkit.test.ts` (24 tests passed)
- REQ-08 contract verification pass (2026-02-24):
  - `npm test -- --run src/__tests__/api/harness/routes.test.ts src/__tests__/lib/harness-error-display.test.ts` (37 tests passed; includes CT-002 warning-format assertions)
  - `npm run typecheck`
- Live runtime validation (2026-02-24):
  - `curl` live checks against `http://127.0.0.1:3000` for DEL-04-02 failure/warning cases using staged working root `/tmp/del0402-live-root`
  - `HARNESS_BASE_URL=http://127.0.0.1:3000 npm run harness:validate:premerge` (`HARNESS_PREMERGE_STATUS=pass`, `HARNESS_PREMERGE_TEST_COUNT=8`)
