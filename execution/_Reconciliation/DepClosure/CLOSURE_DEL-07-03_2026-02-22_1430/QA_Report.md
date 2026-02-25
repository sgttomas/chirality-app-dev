# QA Report -- CLOSURE_DEL-07-03_2026-02-22_1430

## Coverage

| Metric | Value |
|---|---|
| Deliverables in scope | 1 |
| Dependencies.csv found | 1 |
| Dependencies.csv readable | 1 |
| Schema valid | 1 |
| Coverage rate | 100% |

## Schema Issues

None. All 17 rows conform to RegisterSchemaVersion v3.1. All required columns are present and populated.

## Limits and Caveats

| # | Caveat |
|---|---|
| 1 | **Single-deliverable scope:** Cycle detection is limited to self-loops. Cross-deliverable cycles involving DEL-07-03 cannot be detected without a SCOPE=ALL run. |
| 2 | **Bidirectional pair detection limited:** Whether target deliverables declare reciprocal edges back to DEL-07-03 cannot be verified without loading their Dependencies.csv files. |
| 3 | **Direction field present on all edges:** No ambiguity flags needed. All 7 graph edges have explicit Direction (UPSTREAM or DOWNSTREAM). |
| 4 | **No RETIRED rows:** `FILTER_ACTIVE_ONLY=true` had no effect since all rows are ACTIVE. |

## Data Quality Observations

- All `DependencyID` values follow the expected sequential pattern `DEP-07-03-001` through `DEP-07-03-017` (no gaps).
- All `EvidenceFile` and `SourceRef` fields are populated, providing full traceability.
- All `Confidence` values are HIGH (16 rows) or MEDIUM (1 row: DEP-07-03-017).
- All `Origin` values are EXTRACTED.
- `FirstSeen` and `LastSeen` are consistently `2026-02-22` across all rows, consistent with fresh extraction.
