# Working Memory — DEL-03-02

*This file is shared working memory for WORKING_ITEMS and TASK agents operating on this deliverable.*

## Key Decisions

- 2026-02-24: Added route-level per-session turn lock in `frontend/src/app/api/harness/turn/route.ts`. A second in-flight turn for the same session now fails pre-stream with HTTP 409 (`TURN_IN_PROGRESS`).
- 2026-02-24: Partial attachment resolution failures now prepend a warning text block to runtime content blocks when executable content remains (text and/or at least one resolved attachment).
- 2026-02-24: Added stream-cancel cleanup path to issue best-effort interrupt and release the route-level session lock.
- 2026-02-24: Resolved concurrent-turn taxonomy question by codifying dedicated typed error `TURN_IN_PROGRESS` across route contract, harness types, and UI error mapping.
- 2026-02-24: Resolved REQ-13 by enforcing pre-stream API-key readiness for Anthropic provider turns. Missing key now returns HTTP 503 with typed error `MISSING_API_KEY`; the turn stream is not opened.
- 2026-02-24: Resolved REQ-12 by codifying typed mid-stream SSE error event `turn:error` with payload `{ phase, errorType, message, status, severity, fatal, details }`, followed by terminal `process:exit` for fatal errors.
- 2026-02-24: Resolved REQ-10 by codifying the pre-stream session-validation taxonomy for turn start as HTTP 404 `SESSION_NOT_FOUND` JSON with `error.details.sessionId` and no SSE stream open.

## Open Questions

*None currently.*

## Notes

- Tests added in `frontend/src/__tests__/api/harness/routes.test.ts`:
  - partial attachment warning is prepended and passed to runtime content blocks
  - overlapping turn is rejected (409 `TURN_IN_PROGRESS`) and lock is released for subsequent turns
  - Anthropic provider turns now fail pre-stream with HTTP 503 `MISSING_API_KEY` when no key is configured
  - mid-stream runtime failures now emit ordered `turn:error` then `process:exit` with typed payload fields
  - unknown session turn submission now fails pre-stream with HTTP 404 `SESSION_NOT_FOUND` including `error.details.sessionId`
- UI typed-error mapping coverage added in `frontend/src/__tests__/lib/harness-error-display.test.ts` for `TURN_IN_PROGRESS`.
- UI typed-error mapping coverage added in `frontend/src/__tests__/lib/harness-error-display.test.ts` for `MISSING_API_KEY`.
- SSE parsing coverage added in `frontend/src/__tests__/lib/harness-client.test.ts` for `turn:error`.
- Verification evidence (2026-02-24):
  - `npm test -- src/__tests__/api/harness/routes.test.ts src/__tests__/lib/harness-error-display.test.ts`
  - `npm run typecheck`
  - `npm run build`
- Publish sync (2026-02-24):
  - `devsession-1` commit `29d8adc` pushed to `origin` with REQ-13 implementation, DEL-03-02 docs/status updates, Tier 3 PASS13/PASS14 control-loop + interface reconciliation artifacts, and handoff pointer refresh.
