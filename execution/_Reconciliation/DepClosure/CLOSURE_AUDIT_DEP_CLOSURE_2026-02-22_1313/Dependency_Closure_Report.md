# Dependency Closure Report

## Run Metadata

| Field | Value |
|---|---|
| Scope | ALL (36 deliverables) |
| Overall status | BLOCKER |
| Graph | 36 nodes, 154 edges (122 unique) |
| SCCs | 3 (total members 28) |

## Check Verdicts

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

## Top Issues

1. **ISS-001 [BLOCKER]** SCC-001: DEL-01-01 | DEL-01-02 | DEL-01-03 | DEL-02-01 | DEL-02-02 | DEL-02-03 | DEL-02-04 | DEL-02-05 | DEL-03-01 | DEL-03-02 | DEL-03-03 | DEL-03-04 | DEL-03-05 | DEL-03-06 | DEL-03-07 | DEL-04-01 | DEL-05-01 | DEL-05-02 | DEL-06-04 | DEL-06-05 | DEL-07-03 
2. **ISS-002 [BLOCKER]** SCC-002: DEL-05-03 | DEL-05-04 | DEL-06-02 | DEL-06-03 | DEL-08-05 
3. **ISS-003 [BLOCKER]** SCC-003: DEL-07-01 | DEL-07-02 

## Execution Sequencing Advisory

- Full-graph closure remains audit truth.
- Sequencing advisory is provided in `Execution_Path_Blocker_Analysis.md` and `execution_path_summary.json` using blocker-subset filtering.
