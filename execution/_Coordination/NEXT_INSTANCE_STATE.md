# NEXT INSTANCE STATE — Mutable Handoff Snapshot (Concise Control-Plane)

This file is intentionally concise. Keep only current pointers, current graph truth, and the immediate execution queue.
Detailed chronology belongs in deliverable-local `MEMORY.md`, tier control-loop reports, reconciliation artifacts, and git history.

**Last Updated:** 2026-02-24 (DEL-04-01 advanced to `IN_PROGRESS`; attachment resolver hardening pass landed; execution queue refreshed from current `_STATUS.md` lifecycle truth)

## History and Archive Policy

- Immutable archived state history:
  - `execution/_Coordination/NEXT_INSTANCE_STATE_ARCHIVE_2026-02-24_pre_simplify.md`
- Archive rule:
  - treat archived state snapshots as immutable historical records.
  - do not append new session logs to archive files.
- Transfer rule (completed):
  - deliverable-specific publish-trace entries from archived state have been transferred into corresponding deliverable `MEMORY.md` files under:
    - `## Coordination Publish Trace (Transferred 2026-02-24)`

## Current Pointers

| Item | Current pointer |
|---|---|
| Coordination policy | `execution/_Coordination/_COORDINATION.md` |
| Stable startup instructions | `execution/_Coordination/NEXT_INSTANCE_PROMPT.md` |
| Strategic roadmap | `docs/PLAN.md` |
| Decomposition scope | `execution/_Decomposition/ChiralityApp_SoftwareDecomposition_2026-02-21_G7-APPROVED.md` |
| Latest immutable closure snapshot pointer | `execution/_Reconciliation/DepClosure/_LATEST.md` |
| Latest immutable closure snapshot | `execution/_Reconciliation/DepClosure/CLOSURE_AUDIT_DEP_CLOSURE_2026-02-24_0138/` |
| Blocker-subset analysis (latest snapshot) | `execution/_Reconciliation/DepClosure/CLOSURE_AUDIT_DEP_CLOSURE_2026-02-24_0138/Execution_Path_Blocker_Analysis.md` |
| Blocker-subset machine summary (latest snapshot) | `execution/_Reconciliation/DepClosure/CLOSURE_AUDIT_DEP_CLOSURE_2026-02-24_0138/execution_path_summary.json` |
| Current dependency audit refresh (this handoff) | `execution/_Coordination/DEPENDENCY_AUDIT_2026-02-24.md` |
| Current dependency audit JSON (this handoff) | `execution/_Coordination/DEPENDENCY_AUDIT_2026-02-24.json` |

## Current Graph Truth

### Full-Graph Closure (Audit Truth)

- Status: `BLOCKER`
- Active `EXECUTION`/`DELIVERABLE` rows: `158`
- Unique directed edges: `125`
- SCCs: `3` (total SCC nodes: `28`)
- Source: `execution/_Reconciliation/DepClosure/CLOSURE_AUDIT_DEP_CLOSURE_2026-02-24_0138/closure_summary.json`

### Blocker-Subset Topology (Execution Sequencing Truth)

- Status: `PASS` (acyclic)
- Rule: `EXECUTION + DELIVERABLE + ACTIVE + UPSTREAM + (PREREQUISITE|CONSTRAINT) + non-ASSUMPTION`
- Edge count (all/core): `47` / `43`
- Tier count (all/core): `9` / `9`
- Read quality: `0` missing CSV, `0` unreadable, `0` schema-invalid
- Source: `execution/_Reconciliation/DepClosure/CLOSURE_AUDIT_DEP_CLOSURE_2026-02-24_0138/execution_path_summary.json`

### Delta vs Prior Baseline Snapshot (`2026-02-23_0804`)

- Blocker-subset edges: `46 -> 47` (`+1`)
- Tier assignment change:
  - `DEL-01-02`: Tier `1 -> 4`

### Lifecycle Delta Since Latest Immutable Closure Snapshot

- `DEL-03-02` transitioned `SEMANTIC_READY -> IN_PROGRESS` on 2026-02-24.
- `DEL-04-01` transitioned `SEMANTIC_READY -> IN_PROGRESS` on 2026-02-24.
- Blocker-subset sequencing impact:
  - Newly unblocked by `DEL-04-01` promotion: `DEL-04-02`, `DEL-07-01`
  - Current core blocker set at threshold `IN_PROGRESS`: *(none)*

## Execution Queue Snapshot (Core, maturity threshold = `IN_PROGRESS`)

### Active Front (`IN_PROGRESS`/`CHECKING`)

- `DEL-01-01`, `DEL-01-02`, `DEL-01-03`, `DEL-02-05`, `DEL-03-01`, `DEL-03-02`, `DEL-03-04`, `DEL-03-05`, `DEL-03-07`, `DEL-04-01`, `DEL-05-02`, `DEL-05-03`, `DEL-05-04`, `DEL-07-03`

### Unblocked but Not Started (`< IN_PROGRESS`)

- `DEL-02-01`, `DEL-02-02`, `DEL-02-03`, `DEL-02-04`, `DEL-04-02`, `DEL-06-03`, `DEL-06-04`, `DEL-06-05`, `DEL-07-01`

### Blocked (`< IN_PROGRESS` with unmet upstreams)

- *(none in core scope at current maturity threshold)*

### Issued (Core)

- `DEL-03-03`, `DEL-03-06`, `DEL-05-01`, `DEL-06-01`, `DEL-06-02`, `DEL-07-02`

## Active Human Rulings (Still in Force)

- Sequencing invariant: full graph closure is audit truth; blocker subset is execution truth.
- `PKG-08` remains traceable but non-driving for core sequencing until `SOW-032..038` are explicitly ruled `IN`.
- `_MEMORY.md` is disabled for this project profile; use deliverable-local `MEMORY.md` only.

## Immediate Next Actions

1. Run ORCHESTRATOR scan using blocker-subset sequencing and current lifecycle states.
2. Advance the newly unblocked set with focus on `DEL-04-02` and `DEL-07-01`, while continuing parallel advancement on `DEL-02-03`.
3. For touched deliverables, rerun DEPENDENCIES locally and update deliverable-local continuity (`MEMORY.md`, `_STATUS.md`, `_DEPENDENCIES.md` as applicable).
4. Run RECONCILIATION on touched interfaces (especially PKG-04 <-> PKG-07 attachment flow contracts) and write a dated tier control-loop + interface reconciliation pair.
5. Periodically rerun full-scope closure (`AUDIT_DEP_CLOSURE`) and refresh `_LATEST.md` when a new immutable closure snapshot is produced.

## Startup Checklist (Next Session)

1. Read `README.md`.
2. Read `AGENTS.md`.
3. Read `execution/_Coordination/NEXT_INSTANCE_PROMPT.md`.
4. Read this file (`execution/_Coordination/NEXT_INSTANCE_STATE.md`).
5. Verify `execution/_Reconciliation/DepClosure/_LATEST.md` path exists.
6. Read `execution/_Coordination/DEPENDENCY_AUDIT_2026-02-24.md` for current graph status.
