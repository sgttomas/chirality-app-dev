# Dependency Audit Refresh — 2026-02-24

Generated UTC: `2026-02-24T19:40:04Z`
Baseline closure snapshot: `CLOSURE_AUDIT_DEP_CLOSURE_2026-02-24_1939`

## Full-Graph Audit Truth
- Status: `BLOCKER`
- Active EXECUTION/DELIVERABLE rows: `158`
- Unique directed edges: `125`
- SCCs: `3` (nodes in SCCs: `28`)

## Blocker-Subset Execution Truth
- Status: `PASS`
- Rule: `EXECUTION + DELIVERABLE + ACTIVE + UPSTREAM + (PREREQUISITE|CONSTRAINT) + non-ASSUMPTION`
- Edge count (all/core): `47` / `43`
- Tier count (all/core): `9` / `9`

## Delta vs Prior Baseline (2026-02-24_1858)
- Prior subset edges: `47`
- Current subset edges: `47`
- Subset edge delta: `+0`
- Tier assignment changes: *(none)*

## Row-Level Delta Since Last Refresh
- No dependency edge additions/removals/reclassifications detected in this refresh.
- Lifecycle transitions since prior refresh: `10` deliverables moved `IN_PROGRESS -> CHECKING -> ISSUED` (`DEL-01-03`, `DEL-02-01`, `DEL-02-03`, `DEL-02-04`, `DEL-03-04`, `DEL-05-03`, `DEL-05-04`, `DEL-06-03`, `DEL-06-04`, `DEL-06-05`).

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
