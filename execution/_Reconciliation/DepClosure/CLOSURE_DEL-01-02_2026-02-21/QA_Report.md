# QA Report -- AUDIT_DEP_CLOSURE Run: DEL-01-02

## Run Metadata

| Field | Value |
|---|---|
| Run Label | DEL-01-02 |
| Snapshot | `CLOSURE_DEL-01-02_2026-02-21` |
| Date | 2026-02-21 |
| Requested By | RECONCILIATION |
| Agent | AUDIT_DEP_CLOSURE (Type 2) |

## Coverage

| Metric | Value |
|---|---|
| Deliverables in scope | 1 |
| Dependencies.csv found and readable | 1 / 1 (100%) |
| Schema-valid CSVs | 1 / 1 (100%) |
| Total rows parsed | 8 |
| Rows matching edge filter (EXECUTION + DELIVERABLE) | 2 |
| Rows excluded by filter | 6 (3 ANCHOR, 3 EXECUTION with non-DELIVERABLE TargetType) |
| Distinct target deliverables referenced | 2 (DEL-01-01, DEL-05-01) |

## Schema Validation Detail

### DEL-01-02 Dependencies.csv

- **Declared schema version:** v3.1
- **Required columns present:** YES (all 29 columns found)
- **Column order:** matches v3.1 specification
- **Column list verified:**
  - RegisterSchemaVersion, DependencyID, FromPackageID, FromDeliverableID, FromDeliverableName, DependencyClass, AnchorType, Direction, DependencyType, TargetType, TargetPackageID, TargetDeliverableID, TargetRefID, TargetName, TargetLocation, Statement, EvidenceFile, SourceRef, EvidenceQuote, Explicitness, RequiredMaturity, ProposedMaturity, SatisfactionStatus, Confidence, Origin, FirstSeen, LastSeen, Status, Notes

## Limitations

| Limitation | Impact |
|---|---|
| Single-deliverable scope | Only DEL-01-02's Dependencies.csv was loaded. Cycle detection and bidirectional-pair analysis are limited to edges originating from this deliverable. A full workspace closure run (SCOPE=ALL) would provide complete topology analysis. |
| Target deliverables not loaded | DEL-01-01 and DEL-05-01 are graph nodes but their Dependencies.csv files were not parsed. Reverse edges from those deliverables back to DEL-01-02 would only be visible in a SCOPE=ALL run. |

## Direction Ambiguity

No direction ambiguity detected. All EXECUTION+DELIVERABLE edges have `Direction=UPSTREAM` explicitly declared.

## Issues Found During Parsing

None.
