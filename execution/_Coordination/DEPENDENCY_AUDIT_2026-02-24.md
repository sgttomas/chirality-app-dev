# Dependency Audit Refresh — 2026-02-24

Generated UTC: `2026-02-24T21:23:34Z`
Baseline closure snapshot: `CLOSURE_AUDIT_DEP_CLOSURE_2026-02-24_2123`

## Full-Graph Audit Truth
- Status: `WARNINGS`
- Active EXECUTION/DELIVERABLE rows: `141`
- Unique directed edges: `100`
- SCCs: `0` (nodes in SCCs: `0`)
- Bidirectional pairs: `0`

## Blocker-Subset Execution Truth
- Status: `PASS`
- Rule: `EXECUTION + DELIVERABLE + ACTIVE + UPSTREAM + (PREREQUISITE|CONSTRAINT) + non-ASSUMPTION`
- Edge count (all/core): `44` / `43`
- Tier count (all/core): `9` / `9`

## Delta vs Prior Baseline (2101)
- Full-graph status: `BLOCKER -> WARNINGS`
- Full-graph SCC count: `1 -> 0` (`-1`)
- SCC nodes: `21 -> 0` (`-21`)
- Unique edges: `112 -> 100` (`-12`)
- Bidirectional pairs: `12 -> 0` (`-12`)
- Blocker-subset edges: `44 -> 44` (`0`)
- Tier assignment changes: none

## Row-Level Delta Since Last Refresh
- Direction reorientation set applied to remove residual reciprocal/interface loops and break final SCC:
  - `DEP-01-01-006`: `DOWNSTREAM -> UPSTREAM`
  - `DEP-01-03-017`: `UPSTREAM -> DOWNSTREAM`
  - `DEP-02-03-008`: `UPSTREAM -> DOWNSTREAM`
  - `DEP-02-03-009`: `DOWNSTREAM -> UPSTREAM`
  - `DEP-03-01-009`: `UPSTREAM -> DOWNSTREAM`
  - `DEP-03-02-008`: `UPSTREAM -> DOWNSTREAM`
  - `DEP-03-02-010`: `UPSTREAM -> DOWNSTREAM`
  - `DEP-03-03-003`: `UPSTREAM -> DOWNSTREAM`
  - `DEP-03-05-004`: `UPSTREAM -> DOWNSTREAM`
  - `DEP-03-05-007`: `UPSTREAM -> DOWNSTREAM`
  - `DEP-03-07-009`: `UPSTREAM -> DOWNSTREAM`
  - `DEP-03-07-013`: `UPSTREAM -> DOWNSTREAM`
  - `DEP-03-07-015`: `UPSTREAM -> DOWNSTREAM`
  - `DEP-03-07-016`: `UPSTREAM -> DOWNSTREAM`
  - `DEP-03-07-018`: `UPSTREAM -> DOWNSTREAM`
  - `DEP-05-01-004`: `UPSTREAM -> DOWNSTREAM`
  - `DEP-05-01-005`: `UPSTREAM -> DOWNSTREAM`
  - `DEP-05-01-006`: `UPSTREAM -> DOWNSTREAM`
  - `DEP-06-04-009`: `UPSTREAM -> DOWNSTREAM`
  - `DEP-07-03-012`: `DOWNSTREAM -> UPSTREAM`
  - `DEP-07-03-013`: `DOWNSTREAM -> UPSTREAM`

## Execution Front (Core, threshold IN_PROGRESS)
- Active front: *(none; all core deliverables are at ISSUED)*
- Unblocked not-started: *(none in core scope at current maturity threshold)*
- Blocked not-started: *(none in core scope at current maturity threshold)*
- Issued (core): DEL-01-01, DEL-01-02, DEL-01-03, DEL-02-01, DEL-02-02, DEL-02-03, DEL-02-04, DEL-02-05, DEL-03-01, DEL-03-02, DEL-03-03, DEL-03-04, DEL-03-05, DEL-03-06, DEL-03-07, DEL-04-01, DEL-04-02, DEL-05-01, DEL-05-02, DEL-05-03, DEL-05-04, DEL-06-01, DEL-06-02, DEL-06-03, DEL-06-04, DEL-06-05, DEL-07-01, DEL-07-02, DEL-07-03

## Read Quality
- Missing Dependencies.csv: `0`
- Unreadable Dependencies.csv: `0`
- Schema invalid Dependencies.csv: `0`

## Residual Warning
- Isolated deliverable remains: `DEL-08-06` (optional hardening scope; unchanged).

Machine-readable snapshot: `execution/_Coordination/DEPENDENCY_AUDIT_2026-02-24.json`
