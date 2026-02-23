# Working Memory — DEL-03-03

*This file is shared working memory for WORKING_ITEMS and TASK agents operating on this deliverable.*

## Key Decisions

- Runtime opts resolution is now async and instruction-root-aware to support persona/global fallback tiers without introducing hidden state.
- Model fallback follows the explicit SPEC 9.8 example chain (`opts.model -> global model -> runtime default`), while tools/maxTurns use persona frontmatter tier (`tools`, `max_turns`).
- Global model source is fail-closed and repo-local: `CHIRALITY_GLOBAL_MODEL` env override first, then optional `model` in `AGENTS.md` frontmatter, else runtime default.

## Open Questions

- Whether persona-level `model` should be treated as a Tier 2 fallback input remains a documented conflict (`CONF-01` in `Guidance.md`) and is not activated in this pass.

## Notes

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
