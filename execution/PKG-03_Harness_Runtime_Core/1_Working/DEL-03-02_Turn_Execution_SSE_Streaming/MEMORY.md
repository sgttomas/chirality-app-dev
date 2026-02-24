# Working Memory — DEL-03-02

*This file is shared working memory for WORKING_ITEMS and TASK agents operating on this deliverable.*

## Key Decisions

- 2026-02-24: Added route-level per-session turn lock in `frontend/src/app/api/harness/turn/route.ts`. A second in-flight turn for the same session now fails pre-stream with HTTP 409 (`INVALID_REQUEST`).
- 2026-02-24: Partial attachment resolution failures now prepend a warning text block to runtime content blocks when executable content remains (text and/or at least one resolved attachment).
- 2026-02-24: Added stream-cancel cleanup path to issue best-effort interrupt and release the route-level session lock.

## Open Questions

- Should overlapping-turn rejection use a dedicated error type (for example `TURN_IN_PROGRESS`) instead of `INVALID_REQUEST`?
- Should missing Anthropic API key be surfaced as a pre-stream HTTP error in the route, rather than as a streamed `process:exit` error event?

## Notes

- Tests added in `frontend/src/__tests__/api/harness/routes.test.ts`:
  - partial attachment warning is prepended and passed to runtime content blocks
  - overlapping turn is rejected (409) and lock is released for subsequent turns
- Verification evidence (2026-02-24):
  - `npm test -- src/__tests__/api/harness/routes.test.ts src/__tests__/lib/harness-anthropic-agent-sdk-manager.test.ts src/__tests__/lib/harness-client.test.ts`
  - `npm run typecheck`
