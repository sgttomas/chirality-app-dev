# Dependency Audit Refresh — 2026-02-24

Generated UTC: `2026-02-24T18:49:00.000000+00:00`
Baseline closure snapshot: `CLOSURE_AUDIT_DEP_CLOSURE_2026-02-23_0804`

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

## Delta vs Prior Baseline (2026-02-23_0804)
- Prior subset edges: `46`
- Current subset edges: `47`
- Subset edge delta: `+1`
- Tier assignment changes:
  - `DEL-01-02`: Tier 1 -> Tier 4

## Execution Front (Core, threshold IN_PROGRESS)
- Active front: DEL-01-01, DEL-01-02, DEL-01-03, DEL-02-05, DEL-03-01, DEL-03-02, DEL-03-04, DEL-03-05, DEL-03-07, DEL-05-02, DEL-05-03, DEL-05-04, DEL-07-03
- Unblocked not-started: DEL-02-01, DEL-02-02, DEL-02-03, DEL-02-04, DEL-04-01, DEL-06-03, DEL-06-04, DEL-06-05
- Blocked not-started:
  - `DEL-04-02` blocked by DEL-04-01 (DEP-04-02-003)
  - `DEL-07-01` blocked by DEL-04-01 (DEP-07-01-011)

## Read Quality
- Missing Dependencies.csv: `0`
- Unreadable Dependencies.csv: `0`
- Schema invalid Dependencies.csv: `0`

Machine-readable snapshot: `execution/_Coordination/DEPENDENCY_AUDIT_2026-02-24.json`
