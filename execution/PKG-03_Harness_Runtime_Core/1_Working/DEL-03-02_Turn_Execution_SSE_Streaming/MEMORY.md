# Working Memory — DEL-03-02

*This file is shared working memory for WORKING_ITEMS and TASK agents operating on this deliverable.*

## Key Decisions

- 2026-02-24: Added route-level per-session turn lock in `frontend/src/app/api/harness/turn/route.ts`. A second in-flight turn for the same session now fails pre-stream with HTTP 409 (`TURN_IN_PROGRESS`).
- 2026-02-24: Partial attachment resolution failures now prepend a warning text block to runtime content blocks when executable content remains (text and/or at least one resolved attachment).
- 2026-02-24: Added stream-cancel cleanup path to issue best-effort interrupt and release the route-level session lock.
- 2026-02-24: Resolved concurrent-turn taxonomy question by codifying dedicated typed error `TURN_IN_PROGRESS` across route contract, harness types, and UI error mapping.
- 2026-02-24: Resolved REQ-13 by enforcing pre-stream API-key readiness for Anthropic provider turns. Missing key now returns HTTP 503 with typed error `MISSING_API_KEY`; the turn stream is not opened.

## Open Questions

*None currently.*

## Notes

- Tests added in `frontend/src/__tests__/api/harness/routes.test.ts`:
  - partial attachment warning is prepended and passed to runtime content blocks
  - overlapping turn is rejected (409 `TURN_IN_PROGRESS`) and lock is released for subsequent turns
  - Anthropic provider turns now fail pre-stream with HTTP 503 `MISSING_API_KEY` when no key is configured
- UI typed-error mapping coverage added in `frontend/src/__tests__/lib/harness-error-display.test.ts` for `TURN_IN_PROGRESS`.
- UI typed-error mapping coverage added in `frontend/src/__tests__/lib/harness-error-display.test.ts` for `MISSING_API_KEY`.
- Verification evidence (2026-02-24):
  - `npm test -- src/__tests__/api/harness/routes.test.ts src/__tests__/lib/harness-error-display.test.ts`
  - `npm run typecheck`
  - `npm run build`
