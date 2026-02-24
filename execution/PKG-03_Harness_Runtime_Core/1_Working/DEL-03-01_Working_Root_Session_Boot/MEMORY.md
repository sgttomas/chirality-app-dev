# Working Memory — DEL-03-01

*This file is shared working memory for WORKING_ITEMS and TASK agents operating on this deliverable.*

## Key Decisions & Human Rulings

- Tier 2 kickoff focuses on gap-verified hardening of existing session boot code rather than net-new endpoint creation.
- Implementation path for code changes is this repo `/Users/ryan/ai-env/projects/chirality-app-dev/`.

## Domain Context

### Repo-local audit (2026-02-22)

Implemented surfaces already present:

- Session API routes:
  - `POST /api/harness/session/create`
  - `POST /api/harness/session/boot`
  - `GET /api/harness/session/list`
  - `GET /api/harness/session/:id`
  - `DELETE /api/harness/session/:id`
- Session persistence exists in `frontend/lib/harness/session-manager.ts` with filesystem storage under `{projectRoot}/.chirality/sessions/` and persisted `claudeSessionId`, `bootFingerprint`, `bootedAt`.
- Boot flow exists in `frontend/lib/harness/index.ts` (`ensureHarnessSessionBooted`, `startHarnessTurn`) including bootstrap turn execution and fingerprint drift handling.

Observed gaps against DEL-03-01 procedure/spec intent:

- `session/create` validates non-empty `projectRoot` but does not validate path existence, directory type, or accessibility.
- Error taxonomy remains coarse: `session/boot` maps only missing session to `404`; other boot failures collapse to generic `500`.
- REQ-11-style distinct failure contracts (persona missing, SDK failure, inaccessible working root) are not fully explicit.
- Working-root vs execution-root validity checks are not implemented (accept-any-path behavior).

## Open Items

- Add/extend tests for:
  - boot without create
  - well-formed but nonexistent session id
  - inaccessible `projectRoot`
  - failure-mode response payload conformance
- Decide whether boot failure taxonomy should reserve distinct status for persona-missing (`404` vs `422`) and codify that in deliverable docs/tests.

## Proposal History

- 2026-02-22: Tier 2 kickoff audit completed; existing implementation mapped and gap list established.
- 2026-02-22: Tier 2 pass-2 control-loop refresh completed; route-level findings re-verified, gap status unchanged.
- 2026-02-22 (Pass 3): applied this repo runtime hardening for REQ-02/REQ-11 path coverage:
  - Added `assertProjectRootAccessible()` and `ProjectRootValidationError` to `frontend/lib/harness/session-manager.ts`.
  - `sessionManager.create()` now validates project root existence, directory type, and read/write access before session creation.
  - `frontend/lib/harness/index.ts` now validates working root before boot, throws explicit `SessionPersonaNotFoundError` and `SessionBootSdkError`.
  - `POST /api/harness/session/create` and `POST /api/harness/session/boot` now return structured `errorType` + message responses with deterministic status mapping.
  - Sibling `frontend` build passes after changes.

## Interface & Dependency Notes

- Constraint edge `DEL-03-01 <- DEL-05-01` is maturity-satisfied but contract-sensitive until instruction-root bundling (including docs) is complete.
- Boot behavior interfaces with DEL-03-03 (opts/fallback semantics) and DEL-03-02 (turn execution stream behavior).

## Pass-2 Evidence Refresh (2026-02-22)

- Re-verified repo-local `frontend/app/api/harness/session/create/route.ts`: validates non-empty `projectRoot` but does not validate existence, directory type, or access.
- Re-verified repo-local `frontend/app/api/harness/session/boot/route.ts`: only `SessionNotFoundError` is mapped to `404`; other boot failures return generic `500`.
- No code-bearing edits were applied from this workspace in this pass.

## Pass-3 Evidence Refresh (2026-02-22)

- Re-verified repo-local `frontend/lib/harness/session-manager.ts` now exposes:
  - `ProjectRootValidationError` (`PROJECT_ROOT_NOT_FOUND`, `PROJECT_ROOT_NOT_DIRECTORY`, `PROJECT_ROOT_NOT_ACCESSIBLE`)
  - `assertProjectRootAccessible(projectRoot)` enforcing existence + directory + read/write access
- Re-verified repo-local `frontend/lib/harness/index.ts` now:
  - checks project root accessibility before boot
  - fails fast for missing persona with explicit typed error
  - maps bootstrap/session-init failures to `SessionBootSdkError`
- Re-verified repo-local route contracts:
  - `session/create` returns typed validation/create errors
  - `session/boot` returns typed REQ-11 style failure categories (`SESSION_NOT_FOUND`, project-root codes, persona missing, SDK boot failure)

## Pass-5 Evidence Refresh (2026-02-22)

- Verified current repository snapshot does not contain `frontend/lib/harness/*` or API route implementation paths referenced by prior pass notes.
- DEL-03-01 queued regression-test hardening is blocked in this workspace until the runtime/test source surface is restored or re-scoped by human ruling.
- Blocker state propagated to pass-5 control artifacts:
  - `execution/_Coordination/TIER2_CONTROL_LOOP_2026-02-22_PASS5.md`
  - `execution/_Reconciliation/TIER2_INTERFACE_RECON_2026-02-22_PASS5.md`

## Pass-8 Evidence Refresh (2026-02-22)

- Runtime surface is present in this workspace under `frontend/src/lib/harness/*` and `frontend/src/app/api/harness/session/*`.
- Implemented REQ-11 hardening for boot-time failure taxonomy and root/persona validation:
  - `frontend/src/lib/harness/session-manager.ts`: exported `assertProjectRootAccessible()` and strengthened accessibility checks (directory + read/write access).
  - `frontend/src/app/api/harness/session/boot/route.ts`: added boot-time working-root accessibility check, persona resolution check via `buildSystemPrompt()`, and explicit `SDK_FAILURE` mapping for non-zero bootstrap exit.
  - `frontend/src/lib/harness/persona-manager.ts`: persona existence now verified against instruction-root `agents/AGENT_<PERSONA>.md`, with `PERSONA_NOT_FOUND` on missing persona.
  - `frontend/src/lib/harness/agent-sdk-manager.ts`: added deterministic bootstrap failure marker (`opts.model="__BOOT_SDK_FAIL__"`) for regression coverage.
- Added targeted REQ-11 regression tests in `frontend/src/__tests__/api/harness/routes.test.ts`:
  - create-time inaccessible root (`WORKING_ROOT_INACCESSIBLE`)
  - boot without prior create (`SESSION_NOT_FOUND`)
  - boot with deleted working root (`WORKING_ROOT_INACCESSIBLE`)
  - boot with unknown persona (`PERSONA_NOT_FOUND`)
  - boot SDK non-zero exit (`SDK_FAILURE`)
- Verification in this workspace after changes:
  - `npm test` -> PASS (`36` tests)
  - `npm run typecheck` -> PASS
  - `npm run build` -> PASS

## Pass-9 Dependency Fan-In (2026-02-22)

- Re-verified SCA-001 gating lifecycle truth:
  - `execution/PKG-03_Harness_Runtime_Core/1_Working/DEL-03-07_Harness_API_Baseline/_STATUS.md` -> `IN_PROGRESS`
  - `execution/PKG-01_Build_And_Packaging/1_Working/DEL-01-03_Frontend_Workspace_Bootstrap/_STATUS.md` -> `IN_PROGRESS`
- Normalized dependency closure state in `Dependencies.csv`:
  - `DEP-03-01-015`: `SatisfactionStatus` set to `SATISFIED`
  - `DEP-03-01-016`: `SatisfactionStatus` set to `SATISFIED`
- Updated `_DEPENDENCIES.md` closure breakdown and run history to record this fan-in refresh.

## Pass-10 Evidence Refresh (2026-02-23)

- Added frontend harness API client module for typed create/boot/turn/interrupt consumption:
  - `frontend/src/lib/harness/client.ts`
- Added UI-level typed error taxonomy mapping for boot/runtime failures:
  - `frontend/src/lib/harness/error-display.ts`
- Wired shell chat surface to live harness session+turn flow with boot-time typed failure propagation (`WORKING_ROOT_INACCESSIBLE`, `PERSONA_NOT_FOUND`, `SDK_FAILURE`, etc.):
  - `frontend/src/components/shell/chat-panel.tsx`
  - `frontend/src/components/shell/app-shell.tsx` (`Suspense` wrapper for search-param hook boundary)
- Added contract tests for the new client/error mapping:
  - `frontend/src/__tests__/lib/harness-client.test.ts`
  - `frontend/src/__tests__/lib/harness-error-display.test.ts`
- Verification for this pass (in `frontend/`):
  - `npm run build` -> PASS
  - `npm run typecheck` -> PASS
  - `npm test` -> PASS

## Pass-11 Evidence Refresh (2026-02-23)

- Consumed DEL-05-01 hardening interfaces in runtime boot path:
  - Added canonical instruction-root resolver/validator module:
    - `frontend/src/lib/harness/instruction-root.ts`
  - `frontend/src/lib/harness/persona-manager.ts` now validates required instruction-root resources before persona lookup.
  - `frontend/src/lib/harness/session-manager.ts` now rejects `projectRoot` paths inside instruction root (`WORKING_ROOT_CONFLICT`, HTTP 409).
  - `frontend/electron/main.ts` now sets `CHIRALITY_INSTRUCTION_ROOT` deterministically (packaged: `process.resourcesPath`; dev: repo root fallback).
- Added explicit route-level regression coverage in `frontend/src/__tests__/api/harness/routes.test.ts`:
  - rejects projectRoot overlapping instruction root (`WORKING_ROOT_CONFLICT`)
  - returns typed boot failure when instruction root required files are missing (`INSTRUCTION_ROOT_INVALID`)
- Verification for this pass (in `frontend/`):
  - `npm test` -> PASS (`66` tests)
  - `npm run typecheck` -> PASS
  - `npm run build` -> PASS
  - `npm run desktop:pack` -> PASS
  - `npm run desktop:dist` -> PASS

## Pass-12 Evidence Refresh (2026-02-23)

- Turn-stream runtime failures now preserve typed error taxonomy in SSE payloads instead of collapsing to generic string-only process-exit errors:
  - `frontend/src/app/api/harness/turn/route.ts` now maps stream-time exceptions through `asHarnessError()` and emits `process:exit` metadata:
    - `errorType`
    - `status`
    - `errorDetails`
- Chat surface now consumes typed process-exit metadata and maps it through the existing harness UI error taxonomy:
  - `frontend/src/components/shell/chat-panel.tsx`
  - Non-zero stream exits now raise `HarnessApiClientError` when `errorType` is present, preserving actionable code/message/next-step behavior.
- Added deterministic turn-failure marker support in stub runtime for regression testing:
  - `frontend/src/lib/harness/agent-sdk-manager.ts` (`TURN_SDK_FAIL_TEST`)
- Updated shared event typing for richer process-exit payload contracts:
  - `frontend/src/lib/harness/types.ts`
- Added regression coverage:
  - `frontend/src/__tests__/api/harness/routes.test.ts` (typed `process:exit` SSE metadata on turn failure)
  - `frontend/src/__tests__/lib/harness-client.test.ts` (SSE parsing of structured process-exit error payloads)
- Verification for this pass (in `frontend/`):
  - `npm test` -> PASS (`78` tests)
  - `npm run typecheck` -> PASS
  - `npm run build` -> PASS

## Pass-13 Evidence Refresh (2026-02-23)

- Propagated boot-failure taxonomy into validation/reporting surfaces so higher-level harness checks no longer rely on generic boot failure assumptions:
  - `frontend/scripts/validate-harness-section8.mjs`
    - added `section8.boot_error_taxonomy` check to required execution order.
    - check asserts typed boot failures for:
      - `SESSION_NOT_FOUND` (boot with missing session id)
      - `PERSONA_NOT_FOUND` (boot with unknown persona)
      - `SDK_FAILURE` (bootstrap turn non-zero exit via deterministic marker model)
      - `WORKING_ROOT_INACCESSIBLE` (boot after project root deletion)
  - `frontend/scripts/validate-harness-premerge.mjs`
    - added `section8.boot_error_taxonomy` to `REQUIRED_TEST_IDS` so premerge artifact validation fails closed if taxonomy coverage is missing.
- Validation artifact output now includes:
  - `section8.boot_error_taxonomy.json` under the section8 API output directory.
- Verification for this pass (in `frontend/`):
  - `npm test` -> PASS (`80` tests)
  - `npm run build` -> PASS
  - `npm run typecheck` -> PASS (after sequential rerun; `.next/types` race observed when run in parallel with build)
  - `node --check scripts/validate-harness-section8.mjs` -> PASS
  - `node --check scripts/validate-harness-premerge.mjs` -> PASS

## Coordination Publish Trace (Transferred 2026-02-24)

Source: `execution/_Coordination/NEXT_INSTANCE_STATE_ARCHIVE_2026-02-24_pre_simplify.md`

- `65ae7b1` — execution fan-in evidence + DEL-03-01 continuity + handoff pointer refresh (`TIER2_CONTROL_LOOP_2026-02-23_PASS13.md`, `TIER2_INTERFACE_RECON_2026-02-23_PASS10.md`, `NEXT_INSTANCE_STATE.md`)
- `06b8ae1` — preserves typed process-exit taxonomy across turn-stream failure paths, chat consumer mapping, regression coverage, and deliverable-local continuity refresh (`DEL-02-05`, `DEL-03-01`).
