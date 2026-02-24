# Memory — DEL-03-07

> Organize by semantic topic, then chronologically within each topic. These headings are the minimum schema — add new sections as needed to capture what matters for this deliverable.

## Key Decisions & Human Rulings

- 2026-02-24: Promoted harness runtime singleton storage from module-local state to `globalThis` (`frontend/src/lib/harness/runtime.ts`) so API route bundles share one runtime instance and `/api/harness/interrupt` can see active turns created by `/api/harness/turn`.
- 2026-02-24: Hardened error normalization (`frontend/src/lib/harness/errors.ts`) with cross-bundle `HarnessError` shape detection so typed errors preserve original status/type even when thrown across route bundle boundaries.
- 2026-02-24: Dependency refresh fan-in pass completed for DEL-03-07 (`Dependencies.csv` `LastSeen` refreshed to `2026-02-24`) with no edge additions/removals and no satisfaction-state transitions.
- 2026-02-22: Implemented Wave 0b using the Guidance-recommended module-interface stub strategy (Option B): route handlers delegate to typed `SessionManager`, `PersonaManager`, `AttachmentResolver`, and `AgentSdkManager` interfaces.
- 2026-02-22: Error taxonomy implemented as string constants in typed responses (`INVALID_REQUEST`, `SESSION_NOT_FOUND`, `PERSONA_NOT_FOUND`, `SDK_FAILURE`, `WORKING_ROOT_INACCESSIBLE`, `ATTACHMENT_FAILURE`) to satisfy typed failure contracts while keeping format explicit.
- 2026-02-22: Session persistence implemented as filesystem JSON records under `process.env.CHIRALITY_SESSION_ROOT` (test/runtime override) or default `frontend/.chirality/sessions` for local baseline execution.
- 2026-02-22: Session delete success contract set to `200 { ok: true }` for consistency with interrupt route and straightforward contract testing.
- 2026-02-22: Resolved `output: 'export'` conflict by switching `frontend/next.config.mjs` to server-capable output and updating Electron packaged runtime to start a local Next server before loading renderer URL.

## Domain Context

- DEL-03-07 is Wave 0b in the SCA-001 pre-tier gate sequence and becomes unblocked once DEL-01-03 reaches `IN_PROGRESS`.
- Wave 0b completion at `IN_PROGRESS` is sufficient to unblock Wave 0c kickoff (`DEL-02-05`, `DEL-07-03`) under current gate policy.

## Open Items

- Add a targeted regression test path that simulates cross-route bundle boundaries in dev mode (or equivalent integration harness) so singleton-sharing regressions are caught before live validation runs.

## Proposal History

- 2026-02-22: Added harness route modules:
  - `frontend/src/app/api/harness/session/create/route.ts`
  - `frontend/src/app/api/harness/session/list/route.ts`
  - `frontend/src/app/api/harness/session/boot/route.ts`
  - `frontend/src/app/api/harness/session/[id]/route.ts`
  - `frontend/src/app/api/harness/turn/route.ts`
  - `frontend/src/app/api/harness/interrupt/route.ts`
- 2026-02-22: Added harness library/stub modules:
  - `frontend/src/lib/harness/types.ts`
  - `frontend/src/lib/harness/errors.ts`
  - `frontend/src/lib/harness/http.ts`
  - `frontend/src/lib/harness/options.ts`
  - `frontend/src/lib/harness/session-manager.ts`
  - `frontend/src/lib/harness/persona-manager.ts`
  - `frontend/src/lib/harness/attachment-resolver.ts`
  - `frontend/src/lib/harness/agent-sdk-manager.ts`
  - `frontend/src/lib/harness/runtime.ts`
- 2026-02-24: Updated runtime/error surfaces for cross-route coherence:
  - `frontend/src/lib/harness/runtime.ts` (runtime singleton stored on `globalThis`)
  - `frontend/src/lib/harness/errors.ts` (cross-bundle `HarnessError` normalization)
- 2026-02-22: Added route-contract tests:
  - `frontend/src/__tests__/api/harness/routes.test.ts`
  - Coverage: CRUD success/failure, boot success/not-found, turn SSE ordering, attachment-only failure, interrupt success/not-found.
- 2026-02-22: Added test runner script and dependency:
  - `frontend/package.json` updates: `"test": "vitest run"`, `vitest` dev dependency.

Verification evidence:
- `npm test` -> PASS (7 tests).
- `npm run typecheck` -> PASS.
- `npm run build` -> PASS after runtime-mode switch.
- `npm test -- src/__tests__/lib/harness-runtime.test.ts src/__tests__/api/harness/routes.test.ts` -> PASS (25 tests).
- `HARNESS_BASE_URL=http://127.0.0.1:3000 npm run harness:validate:premerge` (x2 consecutive runs) -> PASS (`HARNESS_PREMERGE_TEST_COUNT=8` each run).

## Interface & Dependency Notes

- Upstream dependency from Wave 0a (`DEL-01-03`) is materially satisfied: `frontend/` workspace exists and route surface now compiles/tests under local TypeScript + test runtime.
- Session APIs now exist for downstream consumers:
  - `POST /api/harness/session/create`
  - `POST /api/harness/session/boot`
  - `GET /api/harness/session/list`
  - `GET /api/harness/session/:id`
  - `DELETE /api/harness/session/:id`
  - `POST /api/harness/turn`
  - `POST /api/harness/interrupt`
- Downstream wave impact: Wave 0c (`DEL-02-05`, `DEL-07-03`) can begin with concrete API endpoints and contract tests in place.
