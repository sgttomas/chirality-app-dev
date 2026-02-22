# RUN_SUMMARY -- AUDIT_DEP_CLOSURE

| Field | Value |
|---|---|
| RUN_STATUS | WARNINGS |
| RUN_LABEL | AUDIT_DEP_CLOSURE |
| RUN_DATE | 2026-02-22 |
| SCOPE | ALL (32 deliverables) |
| SNAPSHOT | `CLOSURE_AUDIT_DEP_CLOSURE_2026-02-22_2235` |

## Check Verdicts

| Check | Verdict |
|---|---|
| 1. Schema Compliance | PASS |
| 2. Orphan Dependencies | PASS |
| 3. Circular Dependencies | WARNING |
| 4. Anchor Coverage | PASS |
| 5. Misplaced Fields | PASS |
| 6. ID Format Consistency | PASS |
| 7. Isolated Deliverables | PASS |
| 8. Hub Analysis | PASS |
| 9. Bidirectional Pairs | INFO |

## Key Metrics

| Metric | Value |
|---|---|
| Deliverables in scope | 32 |
| CSVs readable + schema-valid | 32 |
| CSVs schema-invalid | 0 |
| CSVs missing | 0 |
| EXECUTION/DELIVERABLE edges (unique directed) | 116 |
| Nontrivial SCCs | 1 |
| Largest SCC size | 31 |
| Orphans | 0 |
| Isolated deliverables | 0 |
| Hubs (degree >= 20) | 0 |
| Bidirectional pairs | 34 |
| Misplaced fields | 0 |
| Missing anchors | 0 |
| Total issues | 134 (BLOCKER=0, WARNING=100, INFO=34) |

## Interpretation

- Full-graph closure remains `WARNINGS` due to one large SCC driven by reciprocal interface declarations.
- Data-quality checks remain clean (schema/orphans/misplaced/anchors all pass).
- Execution-path blocker analysis is provided separately in `Execution_Path_Blocker_Analysis.md` and yields an acyclic blocker subset for sequencing.
- Open concern: ORCHESTRATOR's default blocker computation path may not yet enforce the blocker-subset filter from `_COORDINATION.md`; verify implementation before relying on automated `BLOCKED/UNBLOCKED`.
