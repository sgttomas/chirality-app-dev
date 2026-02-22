# QA Report -- CLOSURE_DEL-06-05_2026-02-21

## Coverage

| Metric | Value |
|---|---|
| Deliverables in scope | 1 |
| Dependencies.csv found | 1/1 (100%) |
| Dependencies.csv readable | 1/1 (100%) |
| Dependencies.csv schema-valid | 1/1 (100%) |
| Total rows parsed | 17 |
| Rows excluded (Status != ACTIVE) | 0 |
| Rows matching edge filter | 3 |

## Schema Validation

| DeliverableID | Schema Version | Column Count | Expected Columns | Missing Columns | Status |
|---|---|---|---|---|---|
| DEL-06-05 | v3.1 | 29 | 29 | 0 | VALID |

**Expected v3.1 columns (29):** RegisterSchemaVersion, DependencyID, FromPackageID, FromDeliverableID, FromDeliverableName, DependencyClass, AnchorType, Direction, DependencyType, TargetType, TargetPackageID, TargetDeliverableID, TargetRefID, TargetName, TargetLocation, Statement, EvidenceFile, SourceRef, EvidenceQuote, Explicitness, RequiredMaturity, ProposedMaturity, SatisfactionStatus, Confidence, Origin, FirstSeen, LastSeen, Status, Notes

All 29 columns confirmed present in Dependencies.csv header row.

## Direction Ambiguity

No direction ambiguity detected. All 3 qualifying edges have Direction=UPSTREAM explicitly set. No undirected-edge fallback was required for SCC detection.

## ID Normalization

All FromDeliverableID and TargetDeliverableID values are already short-form (DEL-XX-YY). No normalization transforms were applied.

## Limits and Bounds

| Parameter | Configured | Used |
|---|---|---|
| MAX_CYCLES | 10000 | 0 (no cycles) |
| HUB_THRESHOLD | 20 | No hubs (max degree = 3) |

No limits were hit during analysis.

## Data Quality Notes

1. All 17 rows have Status=ACTIVE; no RETIRED rows.
2. All rows have non-empty DependencyID, FromPackageID, FromDeliverableID, DependencyClass, Status fields.
3. Confidence is HIGH across all rows.
4. Origin is EXTRACTED across all rows.
5. RequiredMaturity, ProposedMaturity, and SatisfactionStatus are TBD across all rows (expected for a deliverable in Working state).
