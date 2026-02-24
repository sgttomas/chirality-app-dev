# Dependency Audit Refresh — 2026-02-24

Generated UTC: `2026-02-24T02:48:01.052561+00:00`
Baseline closure snapshot: `CLOSURE_AUDIT_DEP_CLOSURE_2026-02-24_0138`

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

## Delta vs Prior Baseline (2026-02-24_0138)
- Prior subset edges: `47`
- Current subset edges: `47`
- Subset edge delta: `+0`
- Tier assignment changes: *(none)*

## Execution Front (Core, threshold IN_PROGRESS)
- Active front: DEL-01-01, DEL-01-02, DEL-01-03, DEL-02-03, DEL-02-05, DEL-03-01, DEL-03-02, DEL-03-04, DEL-03-05, DEL-03-07, DEL-04-01, DEL-04-02, DEL-05-02, DEL-05-03, DEL-05-04, DEL-07-01, DEL-07-03
- Unblocked not-started: DEL-02-01, DEL-02-02, DEL-02-04, DEL-06-03, DEL-06-04, DEL-06-05
- Blocked not-started: *(none in core scope at current maturity threshold)*

## Read Quality
- Missing Dependencies.csv: `0`
- Unreadable Dependencies.csv: `0`
- Schema invalid Dependencies.csv: `0`

Machine-readable snapshot: `execution/_Coordination/DEPENDENCY_AUDIT_2026-02-24.json`
