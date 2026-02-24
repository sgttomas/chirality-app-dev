# Working Memory — DEL-05-04

*This file is shared working memory for WORKING_ITEMS and TASK agents operating on this deliverable.*

## Key Decisions & Human Rulings

- Tier 2 kickoff confirms DEL-05-04 is not yet implemented in this repo runtime code; work starts with bootstrapping path A0 from Procedure.
- Implementation target path in this repo: `/Users/ryan/ai-env/projects/chirality-app-dev/`.
- Pass-12 follow-through decision: dependency-contract route operations must reject canonical-path escapes (including symlinked deliverable paths) outside `projectRoot`.

## Domain Context

### Repo-local audit (2026-02-22)

- No dependency contract module was found for:
  - `_DEPENDENCIES.md` generation/update
  - `Dependencies.csv` v3.1 write/read validation
  - provenance enforcement (`EvidenceFile`, `SourceRef`)
- Current runtime usage is limited to file-existence checks in `frontend/app/api/project/deliverables/route.ts` (knowledge type labeling only).
- No schema-level enforcement of v3.1 columns/enums/identity rules is currently present in this repo runtime code.

Gap summary versus procedure expectations:

- Step A2/A5 logic absent (agent-owned section-safe `_DEPENDENCIES.md` update path missing).
- Step A3/A4 logic absent (`Dependencies.csv` writer/reader contract not implemented).
- Step A6 test suite absent (no REQ-01..REQ-21 conformance tests in this repo runtime).

## Open Items

- Continue dependency-contract follow-through only when new contract-consuming surfaces are introduced.
- Keep blocker-subset reporting and satisfaction-transition rules aligned with shared helpers and route contracts.
- Prepare CHECKING gate artifacts when human scope/control rulings request lifecycle advancement.

## Proposal History

- 2026-02-22: Tier 2 kickoff audit completed; DEL-05-04 implementation identified as not started in this repo.
- 2026-02-22: Tier 2 pass-2 control-loop refresh completed; dependency-contract gap remains unchanged.

## Interface & Dependency Notes

- Upstream prerequisite `DEL-05-02` is maturity-satisfied (`IN_PROGRESS`) for Tier 2 start.
- Deliverable interfaces strongly with DEL-05-03 (lifecycle coupling), DEL-06-03 (cross-deliverable workflows), and future DEPENDENCIES/AUDIT_DEP_CLOSURE runs.

## Pass-2 Evidence Refresh (2026-02-22)

- Re-verified this repo runtime has no dependency-contract module under `frontend/lib` for `Dependencies.csv` v3.1 parsing/writing/validation.
- Re-verified repo-local `frontend/app/api/project/deliverables/route.ts` currently only checks dependency file presence (`_DEPENDENCIES.md` or `Dependencies.csv`) for labeling.
- No code-bearing edits were applied from this workspace in this pass.

## Pass-3 Evidence Refresh (2026-02-22)

- Re-verified this repo runtime still lacks `Dependencies.csv` v3.1 contract modules (schema/reader/writer) under `frontend/lib`.
- DEL-05-04 remains queued after DEL-05-01/DEL-03-01 hardening work; no dependency-module code was applied in this pass.

## Pass-5 Evidence Refresh (2026-02-22)

- Verified current repository snapshot has no `frontend/` tree; proposed implementation targets under `frontend/lib/dependencies/*` are not present.
- DEL-05-04 implementation remains blocked in this workspace due missing runtime source surface (execution-surface blocker).
- Carry-forward action remains unchanged after unblock: implement v3.1 schema/reader/writer contract modules and REQ-01..REQ-21 conformance tests per Procedure.

## Pass-6 Evidence Refresh (2026-02-22)

- Runtime source surface is present under `frontend/src`; previous execution-surface blocker no longer applies in this workspace.
- Implemented dependency contract modules at:
  - `frontend/src/lib/dependencies/schema.ts`
  - `frontend/src/lib/dependencies/csv-utils.ts`
  - `frontend/src/lib/dependencies/register-reader.ts`
  - `frontend/src/lib/dependencies/register-writer.ts`
- Added v3.1 contract coverage in code:
  - Canonical 29-column core schema ordering.
  - Enum/domain validation for class, type, direction, status, origin, confidence, explicitness.
  - Identity checks (`DependencyID` format/uniqueness, host deliverable ID enforcement).
  - Provenance enforcement for ACTIVE rows (`EvidenceFile`, `SourceRef`).
  - Target resolution rules (`TargetDeliverableID` conditional by `TargetType`).
  - Legacy normalization on read/write (`INBOUND`/`OUTBOUND` to `UPSTREAM`/`DOWNSTREAM`, missing `RegisterSchemaVersion` to `v3.1`).
  - SatisfactionStatus transition validation against prior-run rows.
- Added unit coverage in `frontend/src/__tests__/lib/dependencies-register-contract.test.ts` for legacy normalization, header ordering, invalid classification/provenance/target/duplicate-id rejection, and satisfaction transition rules.
- Verification results in this pass:
  - `npm test` (24 tests total) passed.
  - `npm run typecheck` passed.
  - `npm run build` passed.
- Residual follow-up: contract modules are library-level only in this pass; integration into DEPENDENCIES agent runtime/update flows is still open.

## Pass-7 Evidence Refresh (2026-02-22)

- Dependency contract module is now wired into runtime/API flow via:
  - `frontend/src/lib/workspace/deliverable-contracts.ts`
  - `frontend/src/app/api/working-root/deliverable/dependencies/route.ts`
- API integration now enforces:
  - project-root-bounded deliverable path validation
  - read/write integration for deliverable-local `Dependencies.csv`
  - host deliverable ID enforcement from folder identity
  - satisfaction transition checks against prior register rows
- Integration coverage against real deliverable files added in:
  - `frontend/src/__tests__/api/working-root/deliverable-contracts.test.ts`
- Verification results after integration:
  - `npm test` (31 tests total) passed.
  - `npm run typecheck` passed.
  - `npm run build` passed.

## Pass-8 Evidence Refresh (2026-02-22)

- Added runtime UI consumer layer for dependency contract snapshots:
  - `frontend/src/lib/workspace/deliverable-api.ts` (`fetchDeliverableDependencies`, `summarizeDependencyRows`).
  - `frontend/src/app/pipeline/pipeline-client.tsx` now consumes dependency snapshots for selected TASK deliverable scope.
- Pipeline dependency surface now reports:
  - total/active row counts.
  - active upstream blocker-candidate count (`ACTIVE + UPSTREAM + {PREREQUISITE|CONSTRAINT} + non-terminal satisfaction`).
  - satisfaction-status distribution and route-parsed warnings.
- Added helper test coverage:
  - `frontend/src/__tests__/lib/workspace-deliverable-api.test.ts` validates dependency snapshot helper usage and summary behavior.
- Verification results for this pass:
  - `npm test` -> PASS (42 tests total).
  - `npm run typecheck` -> PASS (sequential rerun after resolving transient `.next/types` race from parallel build/typecheck execution).
  - `npm run build` -> PASS.

## Pass-9 Evidence Refresh (2026-02-23)

- Extended dependency contract consumption beyond PIPELINE into WORKBENCH read-only contract checks:
  - `frontend/src/app/workbench/workbench-client.tsx` now loads selected deliverable dependency snapshots via `fetchDeliverableDependencies`.
- WORKBENCH surface now reports dependency totals/active rows/upstream blocker candidates and top unresolved blocker IDs.
- Verification in `frontend/`:
  - `npm run build` -> PASS
  - `npm run typecheck` -> PASS
  - `npm test` -> PASS

## Pass-10 Evidence Refresh (2026-02-23)

- Aligned runtime blocker reporting with control-plane blocker-subset policy from `execution/_Coordination/_COORDINATION.md`:
  - Added shared filter helper for execution-truth rows in `frontend/src/lib/workspace/deliverable-api.ts`:
    - includes only `EXECUTION` + `DELIVERABLE` + `UPSTREAM` + `ACTIVE` + `{PREREQUISITE|CONSTRAINT}` rows
    - excludes non-blocking satisfactions (`SATISFIED`, `WAIVED`, `NOT_APPLICABLE`)
    - excludes unresolved assumption-gated rows in `Notes` (`ASSUMPTION` without `RESOLVED/CLOSED`)
  - `summarizeDependencyRows()` now computes blocker counts from that canonical helper.
  - WORKBENCH blocker candidate list now consumes the same helper (eliminates diverging local filter behavior):
    - `frontend/src/app/workbench/workbench-client.tsx`
- Extended helper-level regression coverage in:
  - `frontend/src/__tests__/lib/workspace-deliverable-api.test.ts`
  - verifies exclusion of `ANCHOR` class rows, non-`DELIVERABLE` targets, unresolved `ASSUMPTION` notes, and inclusion of resolved-assumption rows.
- Verification in `frontend/`:
  - `npm test` -> PASS (70 tests)
  - `npm run typecheck` -> PASS
  - `npm run build` -> PASS

## Pass-11 Evidence Refresh (2026-02-23)

- Added shared lifecycle-target helper in deliverable API client surface:
  - `frontend/src/lib/workspace/deliverable-api.ts`
  - `requiresApprovalShaForTarget(targetState)`
- Helper is now used by PIPELINE transition UI to enforce control-plane aligned human-gate evidence behavior.
- Added helper regression coverage in:
  - `frontend/src/__tests__/lib/workspace-deliverable-api.test.ts`
  - verifies `CHECKING`/`ISSUED` require approval evidence and non-gated targets do not.
- No dependency schema/row logic changes were introduced in this pass; blocker-subset filtering semantics remain unchanged.
- Verification in `frontend/`:
  - `npm test` -> PASS (`76` tests)
  - `npm run typecheck` -> PASS
  - `npm run build` -> PASS

## Pass-12 Evidence Refresh (2026-02-23)

- Hardened shared working-root contract containment in:
  - `frontend/src/lib/workspace/deliverable-contracts.ts`
- Dependency register operations now resolve canonical (`realpath`) paths and enforce project-root containment before reading/writing `Dependencies.csv`.
- Added regression coverage:
  - `frontend/src/__tests__/api/working-root/deliverable-contracts.test.ts`
  - validates symlink deliverable path rejection (`DELIVERABLE_PATH_OUTSIDE_PROJECT_ROOT`) through working-root status/dependency contract routing.
- Verification in `frontend/`:
  - `npm test -- src/__tests__/api/working-root/deliverable-contracts.test.ts` -> PASS (`10` tests)
  - `npm test` -> PASS (`139` tests)
  - `npm run typecheck` -> PASS
  - `npm run build` -> PASS

## Coordination Publish Trace (Transferred 2026-02-24)

Source: `execution/_Coordination/NEXT_INSTANCE_STATE_ARCHIVE_2026-02-24_pre_simplify.md`

- `e75b461` — canonical working-root containment hardening in shared deliverable contracts, symlink-escape regression coverage, Tier 2 PASS17 control-loop + PASS13 reconciliation evidence, DEL-05-03/DEL-05-04 continuity updates, and coordination pointer refresh.
