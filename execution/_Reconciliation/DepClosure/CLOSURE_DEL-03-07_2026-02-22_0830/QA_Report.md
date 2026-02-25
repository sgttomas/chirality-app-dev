# QA Report

## Coverage

| Deliverable | Dependencies.csv | Schema | Rows | ACTIVE Rows | Status |
|---|---|---|---|---|---|
| DEL-03-07 | FOUND | v3.1 VALID | 18 | 18 | OK |

**Coverage rate:** 1/1 deliverables in scope have readable, schema-valid Dependencies.csv (100%).

## Schema Validation

- **RegisterSchemaVersion:** v3.1 (all 18 rows)
- **Required columns (29):** All present; zero missing, zero extra.
- **Schema compliance verdict:** PASS

## Row-Level Quality

| Check | Result | Details |
|---|---|---|
| Empty DependencyID | PASS | All 18 rows have unique DependencyID values |
| FromDeliverableID consistency | PASS | All rows declare `DEL-03-07` |
| Status values | PASS | All rows are `ACTIVE` (no RETIRED, no unknown values) |
| Direction values | PASS | All rows use `UPSTREAM` or `DOWNSTREAM` (no UNKNOWN/empty) |
| DependencyClass values | PASS | Only `ANCHOR` (3) and `EXECUTION` (15) used |
| Explicitness values | PASS | All rows are `EXPLICIT` |
| Confidence values | PASS | 17 HIGH, 1 MEDIUM (DEP-03-07-008) |
| ID format | PASS | All FromDeliverableID and TargetDeliverableID values are short-form; no normalization required |

## Direction Ambiguity

None. All 18 rows have explicit UPSTREAM or DOWNSTREAM direction. No edges required undirected fallback for SCC analysis.

## Limits and Caveats

- **Single-deliverable scope:** Full SCC/cycle detection requires cross-deliverable graph (SCOPE=ALL). This run can only detect self-loops and bidirectional pairs visible from DEL-03-07's register.
- **Cross-register consistency not verified:** Reciprocal edges in DEL-03-01, DEL-03-02, DEL-01-03, DEL-02-05, DEL-07-03, DEL-03-05, DEL-04-01, DEL-03-03 registers are not checked in this scope.
