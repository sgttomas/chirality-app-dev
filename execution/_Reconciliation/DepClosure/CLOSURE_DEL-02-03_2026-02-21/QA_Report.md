# QA Report -- CLOSURE_DEL-02-03_2026-02-21

## Coverage

| Metric | Value |
|---|---|
| Deliverables in scope | 1 (DEL-02-03) |
| Dependencies.csv found | 1 / 1 (100%) |
| Dependencies.csv readable | 1 / 1 (100%) |
| Schema-valid CSVs | 1 / 1 (100%) |

## Schema Validation

| DeliverableID | SchemaVersion | ColumnCount | Valid | Notes |
|---|---|---|---|---|
| DEL-02-03 | v3.1 | 29 | YES | All required columns present and correctly ordered |

### Expected v3.1 Columns (29)

RegisterSchemaVersion, DependencyID, FromPackageID, FromDeliverableID, FromDeliverableName, DependencyClass, AnchorType, Direction, DependencyType, TargetType, TargetPackageID, TargetDeliverableID, TargetRefID, TargetName, TargetLocation, Statement, EvidenceFile, SourceRef, EvidenceQuote, Explicitness, RequiredMaturity, ProposedMaturity, SatisfactionStatus, Confidence, Origin, FirstSeen, LastSeen, Status, Notes

All 29 columns verified present in the source CSV header.

## Row-Level Validation

| Check | Result |
|---|---|
| Total rows | 11 |
| Rows with empty DependencyID | 0 |
| Rows with empty FromDeliverableID | 0 |
| Rows with empty Status | 0 |
| Rows with Status=ACTIVE | 11 |
| Rows with Status=RETIRED | 0 |
| Rows filtered out by FILTER_ACTIVE_ONLY | 0 |

## Direction Handling

All 11 rows have explicit Direction values (UPSTREAM or DOWNSTREAM). No UNKNOWN or missing direction values encountered. No ambiguity flags required for SCC detection.

## Limits and Constraints

| Limit | Setting | Reached |
|---|---|---|
| MAX_CYCLES | 10000 | NO (0 cycles found) |
| HUB_THRESHOLD | 20 | NO (max degree 4) |
| Single-deliverable scope | YES | N/A |

## Scope Limitations

This is a single-deliverable audit. The following checks have reduced detection power:

1. **Circular dependencies (Check 3):** Can only detect self-loops or cycles within edges declared by DEL-02-03. Cross-deliverable return paths are invisible.
2. **Isolated deliverables (Check 7):** Target nodes appear connected from DEL-02-03's perspective, but their own edge declarations are not in scope.
3. **Bidirectional pairs (Check 9):** Only detects pairs where both A-to-B and B-to-A are declared within DEL-02-03's CSV (impossible by definition since FromDeliverableID is always DEL-02-03).

A SCOPE=ALL run is recommended for full-power checks.
