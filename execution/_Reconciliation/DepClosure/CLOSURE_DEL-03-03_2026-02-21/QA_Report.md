# QA Report -- CLOSURE_DEL-03-03_2026-02-21

## Coverage

| Metric | Value |
|---|---|
| Deliverables in scope | 1 |
| Dependencies.csv found | 1 |
| Dependencies.csv readable | 1 |
| Schema-valid CSVs | 1 |
| Coverage rate | 100% |

## Schema Validation Details

| DeliverableID | SchemaVersion | ColumnCount | MissingColumns | ExtraColumns | Status |
|---|---|---|---|---|---|
| DEL-03-03 | v3.1 | 29 | 0 | 0 | VALID |

### Expected v3.1 Columns (29)

RegisterSchemaVersion, DependencyID, FromPackageID, FromDeliverableID, FromDeliverableName, DependencyClass, AnchorType, Direction, DependencyType, TargetType, TargetPackageID, TargetDeliverableID, TargetRefID, TargetName, TargetLocation, Statement, EvidenceFile, SourceRef, EvidenceQuote, Explicitness, RequiredMaturity, ProposedMaturity, SatisfactionStatus, Confidence, Origin, FirstSeen, LastSeen, Status, Notes

All 29 columns present in source CSV. Header order matches expected schema.

## Direction Ambiguity

No rows with missing or unknown Direction values. All 8 rows have explicit Direction (UPSTREAM or DOWNSTREAM). No ambiguity flags needed for SCC analysis.

## Scope Limitations

- **Single-deliverable scope:** Only DEL-03-03's Dependencies.csv was analyzed. Target deliverables (DEL-03-01, DEL-03-02, DEL-03-04, DEL-02-03) were validated for existence but their own Dependencies.csv files were not loaded.
- **Bidirectional pair detection** is inherently limited in single-deliverable scope (can only detect self-referential bidirectional edges, which do not apply here).
- **Cycle detection** is limited to the subgraph visible from DEL-03-03's declared edges. Cycles involving DEL-03-03 that are only visible via other deliverables' edges will not be detected until a workspace-wide run is performed.

## Data Quality Observations

- All 8 rows have `Status=ACTIVE` (no RETIRED rows to filter).
- All 8 rows have `Confidence=HIGH` and `Explicitness=EXPLICIT`.
- All 8 rows have `Origin=EXTRACTED` with `FirstSeen=LastSeen=2026-02-21`.
- Maturity fields (`RequiredMaturity`, `ProposedMaturity`, `SatisfactionStatus`) are all `TBD`, which is expected for newly extracted dependencies.

## Limits Applied

| Limit | Value | Hit? |
|---|---|---|
| MAX_CYCLES | 10000 | NO (0 cycles found) |
| HUB_THRESHOLD | 20 | NO (max degree: 4) |
