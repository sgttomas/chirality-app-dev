# Working Memory — DEL-02-02

*This file is shared working memory for WORKING_ITEMS and TASK agents operating on this deliverable.*

## Key Decisions

- 2026-02-24: Adopted `/api/project/deliverables` as the shared TASK-scope data contract (deliverables + knowledge decomposition marker + knowledge-type mappings) and moved scanning ownership into a root-level `DeliverablesProvider`.
- 2026-02-24: Navigation handoff mechanism for PORTAL -> PIPELINE deliverable rows is URL query state (`category=TASK`, `taskScopeMode=DELIVERABLES`, `scopeKey=pkg::id`) to keep state transfer deterministic across route transitions.
- 2026-02-24: TASK selector model now enforces canonical split controls: `Task Agent`, `Scope Mode`, `Scope`, and conditional `Target Deliverable` when `Scope Mode=KNOWLEDGE_TYPES`.
- 2026-02-24: Resolved REQ-12 policy gap by codifying `latest-click-wins` semantics via a microtask-coalesced navigation scheduler used by PORTAL matrix and deliverable-row routing.

## Open Questions

- None for current DEL-02-02 baseline scope.

## Notes

- Implementation files:
  - `frontend/src/app/api/project/deliverables/route.ts`
  - `frontend/src/components/workspace/deliverables-provider.tsx`
  - `frontend/src/components/portal/agent-matrix.tsx`
  - `frontend/src/app/pipeline/pipeline-client.tsx`
  - `frontend/src/lib/workspace/filesystem.ts`
  - `frontend/src/lib/workspace/navigation-intent.ts`
  - `frontend/src/lib/workspace/task-scope.ts`
  - `frontend/src/app/layout.tsx`
  - `frontend/src/app/globals.css`
- Verification coverage added:
  - `frontend/src/__tests__/api/project/deliverables-route.test.ts`
  - `frontend/src/__tests__/lib/navigation-intent.test.ts`
  - `frontend/src/__tests__/lib/task-scope-selection.test.ts`
- Verification results in `frontend/`:
  - `npm run typecheck` -> PASS
  - `npm test` -> PASS (`250` tests)
  - `npm run build` -> PASS
