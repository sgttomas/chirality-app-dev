# Dependency Closure Report

**Run:** AUDIT_DEP_CLOSURE  
**Date:** 2026-02-22  
**Scope:** ALL (32 deliverables)

**Overall Status:** **WARNINGS**

## Summary

| Metric | Value |
|---|---|
| EXECUTION/DELIVERABLE edges (unique directed) | 116 |
| Nontrivial SCCs | 1 |
| Largest SCC size | 31 |
| Bidirectional pairs | 34 |
| Orphans | 0 |
| Misplaced fields | 0 |
| Missing anchors | 0 |

## Check Outcomes

| Check | Verdict |
|---|---|
| Schema compliance | PASS |
| Orphan dependencies | PASS |
| Circular dependencies | WARNING |
| Anchor coverage | PASS |
| Misplaced fields | PASS |
| ID format consistency | PASS |
| Isolated deliverables | PASS |
| Hub analysis | PASS |
| Bidirectional pairs | INFO |

## SCC Finding

- The graph still contains one large SCC (`size=31`), so full-graph topology is not strictly DAG-ordered.
- This remains expected under current reciprocal declaration style.
- For execution sequencing, use the blocker-subset analysis (`Execution_Path_Blocker_Analysis.md`), which is acyclic after the 2026-02-22 rulings.

## Artifacts

- `closure_summary.json`
- `Dependency_Closure_IssueLog.csv`
- `Evidence/scc_summary.csv`
- `Evidence/cycles_sample.csv`
- `Execution_Path_Blocker_Analysis.md`
- `execution_path_summary.json`
