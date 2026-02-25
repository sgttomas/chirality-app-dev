# Dependency Closure Report

**Run:** AUDIT_DEP_CLOSURE | **Date:** 2026-02-22 | **Scope:** ALL (36 deliverables) | **Status:** BLOCKER

## Summary Metrics

| Metric | Value |
|---|---|
| Deliverables | 36 |
| EXECUTION/DELIVERABLE rows | 156 |
| Graph edges (directed) | 154 |
| Graph edges (unique) | 122 |
| SCC count | 3 |
| SCC total nodes | 28 |
| Bidirectional pairs | 14 |

## Core Check Verdicts

| Check | Verdict | Detail |
|---|---|---|
| Schema compliance | PASS | 36/36 deliverables have valid v3.1 schema |
| Orphan dependencies | PASS | No orphan targets |
| Circular dependencies | BLOCKER | 3 SCC(s) containing 28 nodes |
| Anchor coverage | PASS | All deliverables have IMPLEMENTS_NODE anchors |
| Misplaced fields | PASS | No misplaced fields |
| ID format consistency | PASS | All IDs in short form. Long-form From: 0, Long-form Target: 0 |
| Isolated deliverables | PASS | All deliverables connected |
| Hub analysis | PASS | No hubs above threshold 20 |
| Bidirectional pairs | INFO | 14 bidirectional pair(s) |

## SCC Details

- **SCC-001** (21 nodes): DEL-01-01, DEL-01-02, DEL-01-03, DEL-02-01, DEL-02-02, DEL-02-03, DEL-02-04, DEL-02-05, DEL-03-01, DEL-03-02, DEL-03-03, DEL-03-04, DEL-03-05, DEL-03-06, DEL-03-07, DEL-04-01, DEL-05-01, DEL-05-02, DEL-06-04, DEL-06-05, DEL-07-03
- **SCC-002** (5 nodes): DEL-05-03, DEL-05-04, DEL-06-02, DEL-06-03, DEL-08-05
- **SCC-003** (2 nodes): DEL-07-01, DEL-07-02

## Evidence

- Coverage: `Evidence/coverage.csv`
- SCC summary: `Evidence/scc_summary.csv`
- Cycle sample: `Evidence/cycles_sample.csv`
- Orphans: `Evidence/orphans.csv`
- Hubs: `Evidence/hubs.csv`
- Bidirectional pairs: `Evidence/bidirectional_pairs.csv`
- Issue log: `Dependency_Closure_IssueLog.csv`

## Interpretation

Full-graph closure remains `BLOCKER` because reciprocal declarations generate SCCs. This does not change blocker-subset execution sequencing, which remains tracked separately in `Execution_Path_Blocker_Analysis.md`.
