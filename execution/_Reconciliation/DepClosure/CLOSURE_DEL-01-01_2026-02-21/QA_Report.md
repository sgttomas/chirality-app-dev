# QA Report -- CLOSURE_DEL-01-01_2026-02-21

## Coverage

| Deliverable | Dependencies.csv Found | Readable | Schema Valid | Schema Version | Rows Parsed | Status |
|---|---|---|---|---|---|---|
| DEL-01-01 | Yes | Yes | Yes | v3.1 | 9 | OK |

**Coverage Rate:** 1/1 in-scope deliverables have a readable, schema-valid Dependencies.csv (100%).

## Schema Validation Detail

**DEL-01-01** -- `execution/PKG-01_Build_And_Packaging/1_Working/DEL-01-01_macOS_Build_Baseline/Dependencies.csv`

Expected v3.1 columns (29):
`RegisterSchemaVersion`, `DependencyID`, `FromPackageID`, `FromDeliverableID`, `FromDeliverableName`, `DependencyClass`, `AnchorType`, `Direction`, `DependencyType`, `TargetType`, `TargetPackageID`, `TargetDeliverableID`, `TargetRefID`, `TargetName`, `TargetLocation`, `Statement`, `EvidenceFile`, `SourceRef`, `EvidenceQuote`, `Explicitness`, `RequiredMaturity`, `ProposedMaturity`, `SatisfactionStatus`, `Confidence`, `Origin`, `FirstSeen`, `LastSeen`, `Status`, `Notes`

All 29 columns present. No missing or extra columns detected.

## Edge Filter Application

| Filter | Setting | Rows Matched | Rows Excluded |
|---|---|---|---|
| Status = ACTIVE | FILTER_ACTIVE_ONLY=true | 9/9 | 0 |
| DependencyClass = EXECUTION | edge filter | 5/9 | 4 (ANCHOR class) |
| TargetType = DELIVERABLE | edge filter | 3/5 | 2 (EXTERNAL, DOCUMENT) |

Final edge set: 3 edges from 5 EXECUTION-class rows.

## ID Normalization

All `FromDeliverableID` and `TargetDeliverableID` values already in short-form `DEL-XX-YY` pattern. Normalization was a no-op.

## Direction Handling

All 3 EXECUTION/DELIVERABLE edges have explicit `Direction` values:
- DEP-01-01-005: DOWNSTREAM
- DEP-01-01-006: DOWNSTREAM
- DEP-01-01-007: UPSTREAM

No ambiguous or missing direction values. SCC detection used fully directed graph.

## Limits

| Parameter | Value | Reached |
|---|---|---|
| MAX_CYCLES | 10000 | No (0 cycles) |
| HUB_THRESHOLD | 20 | No (max degree = 3) |

## Issues

No schema issues, parse errors, or data quality problems detected.
