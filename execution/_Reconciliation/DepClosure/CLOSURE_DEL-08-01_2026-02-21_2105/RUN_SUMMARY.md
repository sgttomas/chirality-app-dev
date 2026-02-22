# RUN SUMMARY -- CLOSURE_DEL-08-01_2026-02-21_2105

| Field | Value |
|---|---|
| **RUN_STATUS** | **OK** |
| Run ID | CLOSURE_DEL-08-01_2026-02-21_2105 |
| Run Label | DEL-08-01 |
| Scope | DEL-08-01 (single deliverable) |
| Requested By | RECONCILIATION |
| Timestamp | 2026-02-21T21:05:00 |
| Overall Closure Status | PASS |

## Verdicts

| Check | Verdict |
|---|---|
| 1. Schema Compliance | PASS |
| 2. Orphan Dependencies | PASS |
| 3. Circular Dependencies | PASS |
| 4. Anchor Coverage | PASS |
| 5. Misplaced Fields | PASS |
| 6. ID Format Consistency | PASS |
| 7. Isolated Deliverables | PASS |
| 8. Hub Analysis | PASS |
| 9. Bidirectional Pairs | INCOMPLETE |

## Metrics

- Deliverables in scope: 1
- Dependencies.csv coverage: 100% (1/1)
- Total rows parsed: 12
- EXECUTION/DELIVERABLE edges: 2
- Orphans: 0
- Non-trivial SCCs: 0
- Anchors (IMPLEMENTS_NODE): 1
- Misplaced fields: 0
- Isolated nodes: 0
- Hubs: 0
- Bidirectional pairs: N/A (scope-limited)
- Blockers: 0
- Warnings: 0
- Info items: 2

## Artifacts

- `Brief.md` -- verbatim and normalized brief
- `RUN_SUMMARY.md` -- this file
- `QA_Report.md` -- coverage, schema validation, scope limitations
- `Decision_Log.md` -- defaults and overrides
- `Dependency_Closure_Report.md` -- full closure report with all 9 checks
- `Dependency_Closure_IssueLog.csv` -- consolidated issue log (2 INFO entries)
- `closure_summary.json` -- machine-readable metrics
- `analyze_closure.py` -- reproducible analysis script
- `Evidence/coverage.csv` -- deliverable coverage table
- `Evidence/orphans.csv` -- orphan analysis
- `Evidence/cycles_sample.csv` -- cycle analysis
- `Evidence/scc_summary.csv` -- SCC decomposition
- `Evidence/hubs.csv` -- hub analysis
- `Evidence/bidirectional_pairs.csv` -- bidirectional pair analysis

## Recommended Next Action

No blockers or warnings. DEL-08-01's dependency register is clean. For full cross-deliverable analysis (cycle detection, bidirectional pairs), run AUDIT_DEP_CLOSURE with SCOPE=ALL.
