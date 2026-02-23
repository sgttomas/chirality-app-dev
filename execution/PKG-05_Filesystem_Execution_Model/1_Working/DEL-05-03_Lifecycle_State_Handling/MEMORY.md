# Working Memory — DEL-05-03

*This file is shared working memory for WORKING_ITEMS and TASK agents operating on this deliverable.*

## Key Decisions & Human Rulings

- Tier 2 kickoff outcome: DEL-05-03 requires new implementation in this repo; no reusable lifecycle module exists today.
- Implementation target path in this repo: `/Users/ryan/ai-env/projects/chirality-app-dev/`.

## Domain Context

### Repo-local audit (2026-02-22)

- No dedicated parser/writer/transition module for `_STATUS.md` was found.
- No API surface was found that performs authorized lifecycle transitions.
- Current lifecycle consumption appears only in `frontend/app/api/project/deliverables/route.ts` via `getStatusFromContent(content)` string checks:
  - checks for `ISSUED`, `CHECKING`, `IN_PROGRESS`
  - otherwise defaults to `open`
- This approach is heuristic and read-only; it does not enforce canonical state extraction, transition graph rules, or actor authorization.

Gap summary versus procedure expectations:

- Missing `_STATUS.md` parser with structured field extraction (`Current State`, `Last Updated`, `History`).
- Missing `_STATUS.md` writer with append-only history behavior.
- Missing transition guardrails and authorized-actor enforcement.
- Missing rejection/error contract for invalid transitions.

## Open Items

- Implement lifecycle module in this repo (proposed split):
  - `frontend/lib/lifecycle/status-parser.ts`
  - `frontend/lib/lifecycle/status-writer.ts`
  - `frontend/lib/lifecycle/transition.ts`
- Add unit tests for parser/writer/transition matrix and unauthorized actor cases.
- Add integration tests for forward-only lifecycle progression and explicit rejection behavior.
- Reconcile UI status derivation to use canonical parser output instead of free-text contains checks.

## Proposal History

- 2026-02-22: Tier 2 kickoff audit completed; implementation gap identified as near-total (module absent).
- 2026-02-22: Tier 2 pass-2 control-loop refresh completed; lifecycle gap remains unchanged.

## Interface & Dependency Notes

- Upstream prerequisite `DEL-05-02` is maturity-satisfied (`IN_PROGRESS`) for Tier 2 start.
- Implementation should align with governance invariants in `docs/CONTRACT.md` (`K-STATUS-1`, `K-AUTH-1`, `K-AUTH-2`).

## Pass-2 Evidence Refresh (2026-02-22)

- Re-verified this repo runtime has no lifecycle module under `frontend/lib` for parser/writer/transition handling.
- Re-verified repo-local `frontend/app/api/project/deliverables/route.ts` still derives status using heuristic string checks (`ISSUED`, `CHECKING`, `IN_PROGRESS`) with default `open`.
- No code-bearing edits were applied from this workspace in this pass.

## Pass-3 Evidence Refresh (2026-02-22)

- Re-verified this repo runtime still has no dedicated lifecycle parser/writer/transition module under `frontend/lib`.
- DEL-05-03 remains queued after DEL-05-01/DEL-03-01 hardening work; no lifecycle-module code was applied in this pass.

## Pass-5 Evidence Refresh (2026-02-22)

- Verified current repository snapshot has no `frontend/` tree; proposed implementation targets under `frontend/lib/lifecycle/*` are not present.
- DEL-05-03 implementation remains blocked in this workspace due missing runtime source surface (execution-surface blocker).
- Carry-forward action remains unchanged after unblock: implement parser/writer/transition module and full rejection-path tests per Procedure steps.

## Pass-6 Evidence Refresh (2026-02-22)

- Runtime source surface is present under `frontend/src`; previous execution-surface blocker no longer applies in this workspace.
- Implemented lifecycle module at:
  - `frontend/src/lib/lifecycle/status-parser.ts`
  - `frontend/src/lib/lifecycle/status-writer.ts`
  - `frontend/src/lib/lifecycle/transition.ts`
- Implemented parser support for both list-format and table-format `History` sections; canonical writer emits list-format history with append-only transition entries.
- Implemented transition guardrails with explicit rejection codes:
  - `UNAUTHORIZED_ACTOR`
  - `BACKWARD_TRANSITION`
  - `TRANSITION_NOT_ALLOWED`
  - `INVALID_STATE`
- Added metadata-capable transition/update path (`approvalSha` + generic metadata fields) to preserve SHA-binding capability without blocking current flow.
- Added unit/integration coverage in `frontend/src/__tests__/lib/lifecycle-status.test.ts` for parse/write behavior, authorized transitions, rejection paths, and on-disk status updates.
- Verification results in this pass:
  - `npm test` (24 tests total) passed.
  - `npm run typecheck` passed.
  - `npm run build` passed.
- Residual follow-up: lifecycle module is implemented and tested, but no API route currently invokes it for deliverable state transitions in this repo snapshot.

## Pass-7 Evidence Refresh (2026-02-22)

- Lifecycle transition module is now wired into runtime/API flow via:
  - `frontend/src/lib/workspace/deliverable-contracts.ts`
  - `frontend/src/app/api/working-root/deliverable/status/route.ts`
  - `frontend/src/app/api/working-root/deliverable/status/transition/route.ts`
- Route-level transition enforcement coverage added in:
  - `frontend/src/__tests__/api/working-root/deliverable-contracts.test.ts`
- API integration now enforces:
  - canonical `_STATUS.md` parsing
  - project-root-bounded deliverable path validation
  - explicit transition rejection typing (including `UNAUTHORIZED_ACTOR`)
- Verification results after integration:
  - `npm test` (31 tests total) passed.
  - `npm run typecheck` passed.
  - `npm run build` passed.

## Pass-8 Evidence Refresh (2026-02-22)

- Added runtime UI consumer layer for lifecycle contracts:
  - `frontend/src/lib/workspace/deliverable-api.ts` (`fetchDeliverableStatus`, `transitionDeliverableStatus`, typed workspace API error mapping, forward-target helper).
  - `frontend/src/app/pipeline/pipeline-client.tsx` now consumes lifecycle snapshot and transition routes for selected TASK deliverable scope.
- Pipeline lifecycle transition surface now includes:
  - forward-target selector derived from canonical lifecycle state.
  - actor selector (`WORKING_ITEMS`, `HUMAN`, `CHIRALITY_FRAMEWORK`, `4_DOCUMENTS`), date field, optional approval SHA.
  - typed error feedback using API error code + message.
- Added helper test coverage:
  - `frontend/src/__tests__/lib/workspace-deliverable-api.test.ts` validates route integration helpers and transition payload behavior.
- Verification results for this pass:
  - `npm test` -> PASS (42 tests total).
  - `npm run typecheck` -> PASS (sequential rerun after resolving transient `.next/types` race from parallel build/typecheck execution).
  - `npm run build` -> PASS.

## Pass-9 Evidence Refresh (2026-02-23)

- Extended lifecycle contract consumption beyond PIPELINE into WORKBENCH read-only contract checks:
  - `frontend/src/app/workbench/workbench-client.tsx` now loads selected deliverable lifecycle status via `fetchDeliverableStatus`.
- WORKBENCH surface now reports lifecycle state, last update timestamp, and history count for selected deliverable scope.
- Verification in `frontend/`:
  - `npm run build` -> PASS
  - `npm run typecheck` -> PASS
  - `npm test` -> PASS

## Pass-10 Evidence Refresh (2026-02-23)

- Hardened human-gate lifecycle transition enforcement in:
  - `frontend/src/lib/lifecycle/transition.ts`
- New fail-closed transition errors added and wired through route contracts:
  - `APPROVAL_SHA_REQUIRED`
  - `INVALID_APPROVAL_SHA`
- `approvalSha` is now required for human-gated targets (`CHECKING`, `ISSUED`) and validated as a git-SHA-like hexadecimal token.
- Transition metadata persistence now captures:
  - `Checking Approval SHA` for `IN_PROGRESS -> CHECKING`
  - `Approval SHA` for `CHECKING -> ISSUED`
- Added lifecycle regression coverage in:
  - `frontend/src/__tests__/lib/lifecycle-status.test.ts`
  - required-approval path
  - malformed-approval path
  - metadata persistence for checking/issued transitions
- Verification in `frontend/`:
  - `npm test` -> PASS (`76` tests)
  - `npm run typecheck` -> PASS
  - `npm run build` -> PASS

## Pass-11 Evidence Refresh (2026-02-23)

- Extended lifecycle transition consumption into WORKBENCH for approved agent contexts:
  - `frontend/src/app/workbench/workbench-client.tsx`
  - transition controls are enabled for `CHANGE` and `WORKING_ITEMS`; other agents remain read-only.
- Added shared helper for transition-surface eligibility:
  - `frontend/src/lib/workspace/deliverable-api.ts`
  - `canAgentTransitionLifecycle(agent)` now gates WORKBENCH transition controls.
- WORKBENCH transition flow now reuses canonical lifecycle helpers:
  - `nextLifecycleTargets()` for forward transitions
  - `requiresApprovalShaForTarget()` for human-gated `CHECKING`/`ISSUED` targets
  - `transitionDeliverableStatus()` for route submission with typed error handling
- Added helper regression coverage:
  - `frontend/src/__tests__/lib/workspace-deliverable-api.test.ts`
- Verification in `frontend/`:
  - `npm test` -> PASS (`81` tests)
  - `npm run typecheck` -> PASS
  - `npm run build` -> PASS
