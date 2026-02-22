# QA Report -- CLOSURE_DEL-08-06_2026-02-21

## Coverage

| Metric | Value |
|---|---|
| Deliverables in scope | 1 |
| Dependencies.csv found | 1 |
| Dependencies.csv readable | 1 |
| Schema valid (v3.1) | 1 |
| Total rows parsed | 12 |
| Rows passing edge filter | 5 |
| Rows excluded (ANCHOR class) | 2 |
| Rows excluded (TargetType=WBS_NODE) | 1 |
| Rows excluded (TargetType=DOCUMENT) | 4 |

## Schema Validation Detail

| DeliverableID | SchemaVersion | ColumnCount | RequiredColumnsPresent | Status |
|---|---|---|---|---|
| DEL-08-06 | v3.1 | 29 | YES | VALID |

All 29 columns expected by v3.1 schema are present in the CSV header:
`RegisterSchemaVersion`, `DependencyID`, `FromPackageID`, `FromDeliverableID`, `FromDeliverableName`, `DependencyClass`, `AnchorType`, `Direction`, `DependencyType`, `TargetType`, `TargetPackageID`, `TargetDeliverableID`, `TargetRefID`, `TargetName`, `TargetLocation`, `Statement`, `EvidenceFile`, `SourceRef`, `EvidenceQuote`, `Explicitness`, `RequiredMaturity`, `ProposedMaturity`, `SatisfactionStatus`, `Confidence`, `Origin`, `FirstSeen`, `LastSeen`, `Status`, `Notes`

## Direction Handling

All 5 filtered edges have explicit `Direction` values (UPSTREAM or DOWNSTREAM). No ambiguity flagged for SCC detection.

## Limitations

- This is a single-deliverable closure run. The graph is inherently incomplete -- only edges declared by DEL-08-06 are analyzed. Reciprocal edges from other deliverables are not visible.
- Cycle detection across the broader workspace requires a SCOPE=ALL run.
- Bidirectional pair detection is limited to what DEL-08-06 declares (i.e., cannot detect if DEL-08-07 also declares a dependency back to DEL-08-06 unless DEL-08-07's CSV is also parsed).

## ID Format

All `FromDeliverableID` and `TargetDeliverableID` values are already in short-form (`DEL-XX-YY`). Normalization rate: 0 IDs required normalization out of 17 non-empty ID fields.
