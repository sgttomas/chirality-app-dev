# QA Report -- AUDIT_DEP_CLOSURE 2026-02-22

## Coverage

| Metric | Value |
|---|---|
| Deliverables discovered | 32 |
| Dependencies.csv readable | 32 |
| Dependencies.csv schema-valid | 32 |
| Dependencies.csv schema-invalid | 0 |
| Dependencies.csv missing | 0 |

## Graph Stats

| Metric | Value |
|---|---|
| Unique directed EXECUTION/DELIVERABLE edges | 116 |
| Nontrivial SCC count | 1 |
| Bidirectional pairs | 34 |
| Orphans | 0 |
| Misplaced fields | 0 |

## Notes

- Full-graph SCC warning persists by design pattern (reciprocal declarations).
- Execution-path sequencing should use blocker-subset artifact (`Execution_Path_Blocker_Analysis.md`).
