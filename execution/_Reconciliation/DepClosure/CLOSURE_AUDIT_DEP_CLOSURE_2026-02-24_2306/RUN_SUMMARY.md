# RUN_SUMMARY -- AUDIT_DEP_CLOSURE_2026-02-24_2306

| Field | Value |
|---|---|
| RUN_STATUS | **WARNINGS** |
| RUN_LABEL | AUDIT_DEP_CLOSURE |
| RUN_DATE | 2026-02-24T23:11:54Z |
| SCOPE | ALL (37 deliverables, 8 packages) |
| REQUESTED_BY | ORCHESTRATOR |
| PRIOR_RUN | CLOSURE_AUDIT_DEP_CLOSURE_2026-02-24_2123 |

## Verdict Summary

| Check | Verdict |
|---|---|
| Schema compliance | PASS |
| Orphan dependencies | PASS |
| Circular dependencies | PASS |
| Anchor coverage | PASS |
| Misplaced fields | PASS |
| ID format consistency | PASS |
| Isolated deliverables | **WARNING** |
| Hub analysis | PASS |
| Bidirectional pairs | INFO (0 pairs) |

## Key Metrics

| Metric | Prior (2123) | Current (2306) | Delta |
|---|---|---|---|
| Total deliverables | 36 | 37 | +1 |
| EXECUTION/DELIVERABLE rows | 158* | 143 | see note |
| Unique directed edges | 100 | 101 | +1 |
| SCCs | 0 | 0 | 0 |
| Orphan targets | 0 | 0 | 0 |
| Isolated deliverables | 1 | 1 | 0 |
| Bidirectional pairs | 0 | 0 | 0 |
| Blocker-subset edges | 44 | 45 | +1 |

*Note: The prior run reported `total_execution_deliverable_rows = 158` which includes all EXECUTION/DELIVERABLE rows regardless of Status. This run's 143 count applies FILTER_ACTIVE_ONLY=true consistently. The prior run's `total_graph_edges = 141` (ACTIVE only) is the comparable figure; this run has 143 (+2 from SCA-003).

## Top Issues (1 total)

1. **ISS-001** (WARNING) -- `isolated_deliverables`: DEL-08-06 has zero EXECUTION/DELIVERABLE edges. This is an optional/integrity-hardening deliverable in PKG-08 (retired scope) and the isolation is expected.

## Recommended Next Actions

1. **No action required.** The single WARNING (DEL-08-06 isolation) is a known characteristic of the retired PKG-08 deliverables, not a defect.
2. **DEL-02-06 integration confirmed.** The new deliverable from SCA-003 is properly connected: DEL-03-05 -> DEL-02-06 via DEP-03-05-013 (UPSTREAM/INTERFACE) and DEL-02-06 -> DEL-03-05 via DEP-02-06-003 (DOWNSTREAM/INTERFACE, which normalizes to DEL-03-05 -> DEL-02-06).
3. **Tier correction noted.** DEL-02-01 correctly placed in Tier 3 (after DEL-03-01). Prior run's manual tier assignment had DEL-02-01 in Tier 0 -- see Decision_Log.md for details.
