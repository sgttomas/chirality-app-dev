# QA Report -- CLOSURE_DEL-08-01_2026-02-21_2105

## Coverage

| Metric | Value |
|---|---|
| Deliverables in scope | 1 |
| Dependencies.csv found | 1 |
| Dependencies.csv readable | 1 |
| Dependencies.csv schema-valid | 1 |
| Coverage rate | 100% (1/1) |
| Total rows parsed | 12 |
| Rows after ACTIVE filter | 12 (all rows are ACTIVE) |
| Rows matching edge filter (EXECUTION + DELIVERABLE) | 2 |

## Schema Validation Detail

| Deliverable | File | SchemaVersion | Column Count | Required Columns Present | Status |
|---|---|---|---|---|---|
| DEL-08-01 | execution/PKG-08_Optional_Integrity_Hardening/1_Working/DEL-08-01_References_Content_Hashes/Dependencies.csv | v3.1 | 29 | Yes (all 29 v3.1 columns present) | SCHEMA_VALID |

### Required v3.1 Columns Verified

All 29 required columns confirmed present: RegisterSchemaVersion, DependencyID, FromPackageID, FromDeliverableID, FromDeliverableName, DependencyClass, AnchorType, Direction, DependencyType, TargetType, TargetPackageID, TargetDeliverableID, TargetRefID, TargetName, TargetLocation, Statement, EvidenceFile, SourceRef, EvidenceQuote, Explicitness, RequiredMaturity, ProposedMaturity, SatisfactionStatus, Confidence, Origin, FirstSeen, LastSeen, Status, Notes.

## Direction Ambiguity

No direction ambiguity detected. All 12 rows have explicit Direction values (UPSTREAM or DOWNSTREAM).

## Scope Limitations

- **Single-deliverable scope**: This run analyzes only DEL-08-01. Cross-deliverable checks (bidirectional pairs, full cycle detection) are limited to edges originating from this deliverable. Edges originating from other deliverables toward DEL-08-01 are not loaded.
- **Orphan validation**: TargetDeliverableID values are checked against the full workspace ID set (32 deliverables) as specified in the brief.

## Limits Applied

| Limit | Configured | Reached |
|---|---|---|
| MAX_CYCLES | 10000 | No (0 cycles found) |
| HUB_THRESHOLD | 20 | No (max degree = 2) |
