# Dependency Audit Refresh — 2026-02-24

Generated UTC: `2026-02-24T21:09:08Z`
Baseline closure snapshot: `CLOSURE_AUDIT_DEP_CLOSURE_2026-02-24_2101`

## Full-Graph Audit Truth
- Status: `BLOCKER`
- Active EXECUTION/DELIVERABLE rows: `141`
- Unique directed edges: `112`
- SCCs: `1` (nodes in SCCs: `21`)

## Blocker-Subset Execution Truth
- Status: `PASS`
- Rule: `EXECUTION + DELIVERABLE + ACTIVE + UPSTREAM + (PREREQUISITE|CONSTRAINT) + non-ASSUMPTION`
- Edge count (all/core): `44` / `43`
- Tier count (all/core): `9` / `9`

## Delta vs Prior Baseline (2041)
- Full-graph SCC count: `3 -> 1` (`-2`)
- SCC nodes: `27 -> 21` (`-6`)
- Unique edges: `114 -> 112` (`-2`)
- Bidirectional pairs: `14 -> 12` (`-2`)
- Blocker-subset edges: `44 -> 44` (`0`)
- Tier assignment changes: none

## Row-Level Delta Since Last Refresh
- Reclassified assumption-only hard blocker row to interface-level coupling:
  - `DEP-02-02-005` (`DEL-02-02 -> DEL-01-01`): `PREREQUISITE -> INTERFACE`
- Reoriented non-blocking interface/handover directionality to reduce reciprocal loops:
  - `DEP-05-03-010` (`DEL-05-03 <-> DEL-06-02`)
  - `DEP-06-03-013` (`DEL-06-03 <-> DEL-06-02`)
  - `DEP-07-02-009` (`DEL-07-02 <-> DEL-07-01`)

## Execution Front (Core, threshold IN_PROGRESS)
- Active front: *(none; all core deliverables are at ISSUED)*
- Unblocked not-started: *(none in core scope at current maturity threshold)*
- Blocked not-started: *(none in core scope at current maturity threshold)*
- Issued (core): DEL-01-01, DEL-01-02, DEL-01-03, DEL-02-01, DEL-02-02, DEL-02-03, DEL-02-04, DEL-02-05, DEL-03-01, DEL-03-02, DEL-03-03, DEL-03-04, DEL-03-05, DEL-03-06, DEL-03-07, DEL-04-01, DEL-04-02, DEL-05-01, DEL-05-02, DEL-05-03, DEL-05-04, DEL-06-01, DEL-06-02, DEL-06-03, DEL-06-04, DEL-06-05, DEL-07-01, DEL-07-02, DEL-07-03

## Read Quality
- Missing Dependencies.csv: `0`
- Unreadable Dependencies.csv: `0`
- Schema invalid Dependencies.csv: `0`

Machine-readable snapshot: `execution/_Coordination/DEPENDENCY_AUDIT_2026-02-24.json`
