# Coordination Record

**Representation:** Full dependency graph (DAG)
**Dependency tracking mode:** FULL_GRAPH
**External schedule / coordination artifact:** N/A
**Default maturity threshold (for computing blockers):** IN_PROGRESS

## Dependency Register Format

- **Primary:** `Dependencies.csv` (v3.1 schema) — structured, machine-readable
- **Secondary:** `_DEPENDENCIES.md` — human-readable dependency summary
- Both produced by DEPENDENCIES agent for each deliverable

## Candidate Sourcing

Dependency candidates are proposed by ORCHESTRATOR from decomposition properties and software development domain knowledge. All candidates are labeled **PROPOSAL** and require human acceptance before becoming declared edges.

## Notes

- Graph integrity is maintained from the full declared graph (`Dependencies.csv` + `_DEPENDENCIES.md`), but execution-path blockers use a constrained subset to avoid false deadlocks from reciprocal interface declarations.
- A dependency is considered "met" when the upstream deliverable reaches `IN_PROGRESS` or later lifecycle state.
- Ambiguities in dependency mapping are raised to the human for resolution.
- Execution and implementation scope is this repository (`/Users/ryan/ai-env/projects/chirality-app-dev`) unless explicitly re-ruled by a human.
- New-session stable control-plane handoff instructions: `execution/_Coordination/NEXT_INSTANCE_PROMPT.md`.
- New-session mutable handoff state snapshot: `execution/_Coordination/NEXT_INSTANCE_STATE.md`.
- Established: 2026-02-21

## Execution-Path Blocker Subset (Human Ruling 2026-02-22)

For development sequencing and `BLOCKED/UNBLOCKED` advisory computation:

- Include only rows where:
  - `DependencyClass=EXECUTION`
  - `TargetType=DELIVERABLE`
  - `Direction=UPSTREAM`
  - `DependencyType in {PREREQUISITE, CONSTRAINT}`
  - `Status=ACTIVE`
  - `Notes` does **not** carry unresolved `ASSUMPTION` gating language
- Rows outside this subset remain valid graph/interface metadata but are treated as non-blocking for start sequencing.

## PKG-08 Scope Handling (Human Ruling 2026-02-22)

- `PKG-08` deliverables (`DEL-08-01` … `DEL-08-07`) are retained in the dependency graph for traceability.
- `PKG-08` does not drive core sequencing until `SOW-032` … `SOW-038` scope items are explicitly ruled `IN`.
- Established: 2026-02-21

## TASK Dispatch Autonomy (Global Policy)

- WORKING_ITEMS may spawn/dispatch TASK agents without per-task human approval.
- TASK execution invariant remains one deliverable per TASK session (`DeliverablePath`-scoped); session closes after that deliverable's bounded task is complete.
- Additional queued work is handled by newly booted TASK sessions.
