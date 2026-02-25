# Working Memory — DEL-03-03

*This file is shared working memory for WORKING_ITEMS and TASK agents operating on this deliverable.*

## Key Decisions

- Runtime opts resolution is now async and instruction-root-aware to support persona/global fallback tiers without introducing hidden state.
- Model fallback follows the explicit SPEC 9.8 example chain (`opts.model -> global model -> runtime default`), while tools/maxTurns use persona frontmatter tier (`tools`, `max_turns`).
- Global model source is fail-closed and repo-local: `CHIRALITY_GLOBAL_MODEL` env override first, then optional `model` in `AGENTS.md` frontmatter, else runtime default.
- Human ruling applied (2026-02-24): DEL-03-03 is directly approved for `IN_PROGRESS -> ISSUED`; CHECKING is considered complete for this cycle.

## Open Questions

- DEL-03-04 interface follow-through is still pending for explicit enforcement-field ownership (`disallowed_tools`, `auto_approve_tools`) once governance-layer implementation reaches active scope.

## Notes

- DEL-03-03 issuance approval application (2026-02-24):
  - Added issuance gate artifact:
    - `ISSUED_Gate_Decision_Input_2026-02-24.md`
  - Applied lifecycle transition in `_STATUS.md`:
    - `IN_PROGRESS -> ISSUED` (direct human ruling; CHECKING considered complete)
  - Added fan-in evidence artifacts:
    - `execution/_Coordination/TIER3_CONTROL_LOOP_2026-02-24_PASS12.md`
    - `execution/_Reconciliation/TIER3_INTERFACE_RECON_2026-02-24_PASS12.md`
- DEL-03-03 follow-through hardening pass (2026-02-24):
  - Runtime behavior updates in `frontend/src/lib/harness/options.ts`:
    - warns and ignores unknown opts fields (`warn-and-continue`)
    - logs explicit warning for malformed persona frontmatter and falls through to defaults
  - Added regression coverage in `frontend/src/__tests__/lib/harness-options.test.ts`:
    - model fallback explicitly excludes persona-level `model` Tier 2
    - opts `persona` override resolves alternate persona defaults
    - unknown opts warning behavior
    - malformed frontmatter warning behavior
  - Documentation/continuity refresh:
    - `Datasheet.md`, `Specification.md`, `Guidance.md`, `Procedure.md`, `_STATUS.md`, `MEMORY.md`
  - Tier 3 evidence artifacts:
    - `execution/_Coordination/TIER3_CONTROL_LOOP_2026-02-24_PASS11.md`
    - `execution/_Reconciliation/TIER3_INTERFACE_RECON_2026-02-24_PASS11.md`
  - Verification evidence (2026-02-24):
    - `cd frontend && npm test -- src/__tests__/lib/harness-options.test.ts src/__tests__/api/harness/routes.test.ts` -> PASS (28 tests)
    - `cd frontend && npm run typecheck` -> PASS
    - `cd frontend && npm run build` -> PASS
- DEL-03-03 verification-hardening continuation (2026-02-23):
  - Preserved governance boundary by carrying `opts.subagentGovernance` through resolved runtime options without fallback remapping:
    - `frontend/src/lib/harness/types.ts`
    - `frontend/src/lib/harness/options.ts`
  - Added verification coverage for unresolved requirement gaps:
    - `frontend/src/__tests__/lib/harness-options.test.ts`
      - governance passthrough assertion
      - deterministic resolution loop (`100` repeated runs)
    - `frontend/src/__tests__/api/harness/routes.test.ts`
      - boot-route assertion that `subagentGovernance` reaches runtime `startTurn` unchanged
  - Tier 3 evidence artifacts:
    - `execution/_Coordination/TIER3_CONTROL_LOOP_2026-02-23_PASS2.md`
    - `execution/_Reconciliation/TIER3_INTERFACE_RECON_2026-02-23_PASS2.md`
  - Verification evidence (2026-02-23):
    - `cd frontend && npm test -- src/__tests__/lib/harness-options.test.ts src/__tests__/api/harness/routes.test.ts` -> PASS (25 tests)
    - `cd frontend && npm test` -> PASS (91 tests)
    - `cd frontend && npm run typecheck` -> PASS
    - `cd frontend && npm run build` -> PASS
- DEL-03-03 implementation pass (2026-02-23):
  - Updated runtime options mapping in `frontend/src/lib/harness/options.ts`:
    - added lightweight YAML frontmatter parsing for persona defaults
    - added instruction-root global model resolution
    - enforced deterministic fallback normalization for model/tools/maxTurns
  - Updated route consumers to await async resolver:
    - `frontend/src/app/api/harness/session/boot/route.ts`
    - `frontend/src/app/api/harness/turn/route.ts`
  - Added regression suite:
    - `frontend/src/__tests__/lib/harness-options.test.ts`
- Verification evidence (2026-02-23):
  - `cd frontend && npm test` -> PASS (88 tests)
  - `cd frontend && npm run typecheck` -> PASS
  - `cd frontend && npm run build` -> PASS
- Tier 3 fan-in refresh (2026-02-23):
  - Updated dependency closure posture for DEL-03-03:
    - `DEP-03-03-004` (`DEL-03-01` prerequisite) now marked `SATISFIED` with `RequiredMaturity=IN_PROGRESS` after upstream lifecycle verification.
    - No dependency rows were added, retired, or reclassified in this refresh.
  - Added fan-in evidence artifacts:
    - `execution/_Coordination/TIER3_CONTROL_LOOP_2026-02-23_PASS1.md`
    - `execution/_Reconciliation/TIER3_INTERFACE_RECON_2026-02-23_PASS1.md`
  - Focused verification rerun:
    - `cd frontend && npm test -- src/__tests__/lib/harness-options.test.ts` -> PASS (7 tests)

## Coordination Publish Trace (Transferred 2026-02-24)

Source: `execution/_Coordination/NEXT_INSTANCE_STATE_ARCHIVE_2026-02-24_pre_simplify.md`

- `08970a5` — DEL-03-03 PASS11 options-contract hardening, PASS12 direct issuance gate application (`IN_PROGRESS -> ISSUED` by explicit human ruling), Tier 3 PASS11/PASS12 control-loop + reconciliation evidence, DEL-03-03 continuity updates, and coordination pointer refresh.
- `677299e` — frontend DEL-03-03 runtime/test hardening (`subagentGovernance` passthrough + deterministic fallback verification + boot-route passthrough coverage).
- `1cc6fef` — Tier 3 PASS2 control-loop/reconciliation evidence + DEL-03-03 continuity updates + coordination handoff refresh.
- `ebb437b` — DEL-03-03 dependency refresh (`DEP-03-03-004` gate-met), Tier 3 control-loop and interface reconciliation evidence, and deliverable-local continuity updates (`_STATUS.md`, `MEMORY.md`).
- `5a0168f` — DEL-03-03 runtime fallback-chain implementation (`options` resolver), boot/turn route async adoption, regression coverage, and deliverable-local continuity updates (`_STATUS.md` + `MEMORY.md`).
