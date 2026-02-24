# Working Memory — DEL-04-01

*This file is shared working memory for WORKING_ITEMS and TASK agents operating on this deliverable.*

## Key Decisions

- Implemented a hardened `AttachmentResolver` in `frontend/src/lib/harness/attachment-resolver.ts` and switched runtime wiring from the legacy stub instantiation to `AttachmentResolver`.
- Enforced resolver validation contract server-side: absolute-path requirement, extension allowlist, readable path check, symlink rejection, regular-file check, per-file 10 MiB limit, and per-turn 18 MiB total budget.
- Kept Anthropic manager behavior unchanged for non-image files (explicit fallback text blocks) to avoid cross-deliverable regressions while DEL-04-02 remains blocked.
- Added route-level prompt-mode branch behavior in `frontend/src/app/api/harness/turn/route.ts`:
  - turns with at least one resolved attachment continue in content-block mode
  - turns without resolved attachments use string mode
  - warning text for all-failed attachments with remaining user text is prepended into string-mode message content

## Open Questions

- REQ-06 boundary/algorithm ambiguity remains in spec docs (exact-18 MiB equality and aggregate-vs-sequential handling). Current implementation uses sequential acceptance and rejects overflow files.
- REQ-12 SDK content-block completeness for non-image documents remains open; current implementation preserves explicit text fallback in Anthropic manager for non-image file blocks.

## Notes

- Validation evidence (2026-02-24):
  - `npm test -- --run src/__tests__/lib/harness-attachment-resolver.test.ts` (7/7 passing)
  - `npm test -- --run src/__tests__/api/harness/routes.test.ts` (23/23 passing)
- Files changed for this pass:
  - `frontend/src/lib/harness/attachment-resolver.ts`
  - `frontend/src/lib/harness/runtime.ts`
  - `frontend/src/app/api/harness/turn/route.ts`
  - `frontend/src/__tests__/lib/harness-attachment-resolver.test.ts`
  - `frontend/src/__tests__/api/harness/routes.test.ts`
