# Working Memory — DEL-04-01

*This file is shared working memory for WORKING_ITEMS and TASK agents operating on this deliverable.*

## Key Decisions

- Implemented a hardened `AttachmentResolver` in `frontend/src/lib/harness/attachment-resolver.ts` and switched runtime wiring from the legacy stub instantiation to `AttachmentResolver`.
- Enforced resolver validation contract server-side: absolute-path requirement, extension allowlist, readable path check, symlink rejection, regular-file check, per-file 10 MiB limit, and per-turn 18 MiB total budget.
- Resolved REQ-12 non-image completeness: Anthropic manager now maps non-image attachments to SDK `document` blocks (`application/pdf` -> base64 PDF source; text attachments -> plain-text source) while retaining guarded fallback text for unexpected unsupported MIME.
- Added route-level prompt-mode branch behavior in `frontend/src/app/api/harness/turn/route.ts`:
  - turns with at least one resolved attachment continue in content-block mode
  - turns without resolved attachments use string mode
  - warning text for all-failed attachments with remaining user text is prepended into string-mode message content

## Open Questions

- None in the REQ-07/REQ-08 attachment warning/failure contract set (CT-002 and CT-003 resolved).

## Notes

- 2026-02-24: REQ-06 is now explicitly codified as input-order sequential accounting with inclusive boundary (`<= 18 MB` accepted). Overflowing files are rejected individually and evaluation continues for later files.
- 2026-02-24: REQ-12 is now codified and implemented against local `@anthropic-ai/sdk@0.78.0` message-type contract for `image` and `document` blocks.
- 2026-02-24: REQ-08 pre-stream rejection payload is now codified as structured `ATTACHMENT_FAILURE` details (`category`, per-file `attachmentErrors[]`, `rejectedAttachmentCount`) and consumed by DEL-04-02 error-display mapping.
- 2026-02-24: REQ-07 warning text block minimum format is now codified as deterministic plain text (`header` + `Rejected attachments:` + filename/reason bullets + omission summary when needed) and enforced in route regression tests.
- Validation evidence (2026-02-24):
  - `npm test -- --run src/__tests__/lib/harness-anthropic-agent-sdk-manager.test.ts` (78/78 passing)
  - `npm test -- --run src/__tests__/lib/harness-attachment-resolver.test.ts src/__tests__/api/harness/routes.test.ts src/__tests__/lib/harness-anthropic-agent-sdk-manager.test.ts` (113/113 passing)
  - `npm test -- --run src/__tests__/api/harness/routes.test.ts src/__tests__/lib/harness-error-display.test.ts` (37/37 passing; includes REQ-07 warning-format contract assertions)
  - `npm run typecheck`
- Files changed across recent Tier 4 DEL-04-01 passes:
  - `frontend/src/app/api/harness/turn/route.ts`
  - `frontend/src/lib/harness/types.ts`
  - `frontend/src/lib/harness/error-display.ts`
  - `frontend/src/__tests__/api/harness/routes.test.ts`
  - `frontend/src/__tests__/lib/harness-error-display.test.ts`
  - `frontend/src/lib/harness/anthropic-agent-sdk-manager.ts`
  - `frontend/src/__tests__/lib/harness-anthropic-agent-sdk-manager.test.ts`
  - `frontend/src/__tests__/lib/harness-attachment-resolver.test.ts`
  - `execution/PKG-04_Attachments_Multimodal/1_Working/DEL-04-01_Attachment_Resolver_PromptMode/Specification.md`
  - `execution/PKG-04_Attachments_Multimodal/1_Working/DEL-04-01_Attachment_Resolver_PromptMode/Guidance.md`
  - `execution/PKG-04_Attachments_Multimodal/1_Working/DEL-04-01_Attachment_Resolver_PromptMode/Procedure.md`
  - `execution/PKG-04_Attachments_Multimodal/1_Working/DEL-04-01_Attachment_Resolver_PromptMode/Datasheet.md`
