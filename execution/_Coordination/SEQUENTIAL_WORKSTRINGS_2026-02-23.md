# Sequential Workstrings — No-Parallelism Throughput Plan (2026-02-23)

## Purpose

Define a no-parallelism execution model that reduces startup/context overhead by keeping one agent session on a coherent subsystem thread for multiple deliverable passes before handoff.

## Scope Assumptions

1. Work remains scoped to this repository (`/Users/ryan/ai-env/projects/chirality-app-dev`).
2. Execution sequencing continues to use blocker-subset truth from `_COORDINATION.md`.
3. Full-graph closure remains audit truth.
4. `PKG-08` stays traceable but non-driving unless SOW-032..038 are explicitly ruled `IN`.

## Workstrings

| Workstring | Deliverable sequence | Why this is coherent |
|---|---|---|
| WS-1 Frontend/Harness Foundation | `DEL-01-03 -> DEL-03-07 -> DEL-02-05 -> DEL-07-03 -> DEL-01-01 -> DEL-03-01 -> DEL-01-02` | Shared `frontend` route/runtime/build surfaces and validation scripts |
| WS-2 Execution-Root Contract Chain | `DEL-05-02 -> DEL-05-03 -> DEL-05-04` | Shared lifecycle/dependency contract modules and API consumers |
| WS-3 Runtime/Provider Hardening Chain | `DEL-03-03 -> DEL-03-05 -> DEL-03-06 -> DEL-03-02 -> DEL-03-04` | Shared harness runtime pipeline and provider/error/stream contracts |
| WS-4 Attachments + Validation Chain | `DEL-04-01 -> DEL-04-02 -> DEL-07-01` | Resolver contract to UI attachment path and validation evidence |
| WS-5 Desktop UI Completion Chain | `DEL-02-01 -> DEL-02-02 -> DEL-02-04 -> DEL-02-03` | Shared navigation/layout/operator-toolkit UI surfaces |
| WS-6 Governance Operationalization Chain | `DEL-06-03 -> DEL-06-04 -> DEL-06-05` | Shared governance/process documentation and workflow contracts |
| WS-7 Optional Hardening (only if ruled IN) | `DEL-08-02 -> DEL-08-03 -> DEL-08-01 -> DEL-08-04 -> DEL-08-06 -> DEL-08-05 -> DEL-08-07` | Aligns to PLAN dependencies (lint/validator before graph/run-record/staleness) |

## Session Operating Pattern

1. Keep one session on one workstring.
2. Execute 3-6 deliverable passes before macro handoff.
3. For each deliverable pass, do:
   1. deliverable implementation/doc updates
   2. touched-deliverable DEPENDENCIES refresh as needed
   3. touched-interface reconciliation
   4. deliverable continuity updates (`_STATUS.md`, `MEMORY.md`)
   5. scoped commit
4. At workstring fan-in boundary, do:
   1. ORCHESTRATOR/control-loop summary update
   2. periodic full-scope closure rerun at substantive merge points
   3. single `NEXT_INSTANCE_STATE.md` queue/pointer refresh
   4. push

## Exit Criteria

1. Active workstring sequence reaches agreed stop point (or a blocking dependency requires sequence switch).
2. Fan-in checks and evidence are written for touched scope.
3. Handoff pointers reference latest control/reconciliation artifacts.
