# QA Report

## Coverage

| Metric | Value |
|---|---|
| Deliverables in scope | 32 |
| Dependencies.csv found | 32 |
| Dependencies.csv readable + schema-valid | 31 (96.9%) |
| Dependencies.csv schema-invalid | 1 (DEL-05-04) |
| Dependencies.csv missing | 0 |
| Dependencies.csv unreadable | 0 |

## Schema Issues

### DEL-05-04 (SCHEMA_INVALID)

- **File**: `execution/PKG-05_Filesystem_Execution_Model/1_Working/DEL-05-04_Dependency_Tracking_Contract/Dependencies.csv`
- **Schema version declared**: v3.1
- **Issue**: Missing required columns `RequiredMaturity` and `ProposedMaturity`. Has extra columns `FromDeliverableType`, `TargetDeliverableType`, `ConflictFlag`.
- **Impact**: DEL-05-04's 10 rows were excluded from edge parsing. The node remains in the graph. 8 other deliverables reference DEL-05-04 as a target, so inbound edges to DEL-05-04 exist from those other CSVs. However, DEL-05-04's own outbound edges (to DEL-05-02, DEL-05-03, DEL-08-02, DEL-08-04, DEL-08-07) are missing from the graph.
- **Recommendation**: Add `RequiredMaturity` and `ProposedMaturity` columns (value `TBD` is acceptable) or rerun DEPENDENCIES extraction for DEL-05-04.

## Direction Ambiguity

No direction ambiguity detected. All EXECUTION/DELIVERABLE rows had a Direction value of either UPSTREAM or DOWNSTREAM. No UNKNOWN or empty Direction fields were encountered in the edge-filter-passing rows.

## Analysis Limits

| Parameter | Value | Notes |
|---|---|---|
| MAX_CYCLES | 10000 | Per-SCC cap of 100 was applied; the single SCC of 30 nodes has many more possible cycles |
| HUB_THRESHOLD | 20 | No nodes reached this threshold; highest degree is DEL-03-02 at 15 |
| Cycle enumeration | 100 sampled | Representative subset; full enumeration impractical for SCC of size 30 |

## Edge Count Verification

- Total rows across all 31 valid CSVs: 365
- Rows matching filter (ACTIVE + EXECUTION + DELIVERABLE + both IDs present): 111
- Unique directed edges: 111

## Reproducibility

The analysis script `analyze_closure.py` in this snapshot produces identical results when rerun against the same input CSVs. No randomization is used. Node and edge iteration is sorted alphabetically for determinism.
