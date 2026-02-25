# QA Report

**Run:** `CLOSURE_DEL-02-05_2026-02-22_2300`
**Date:** 2026-02-22

---

## Coverage

| Metric | Value |
|---|---|
| Deliverables in scope | 1 |
| Dependencies.csv found | 1 |
| Dependencies.csv readable | 1 |
| Schema valid (v3.1) | 1 |
| Coverage rate | 100% |

## Schema Issues

None. The single Dependencies.csv conforms to v3.1 schema with all 29 expected columns present.

## Direction Ambiguity

None. All 11 rows have explicit `Direction` values (UPSTREAM or DOWNSTREAM). No undirected/unknown edges.

## Normalization

All IDs in the register are already short-form (`DEL-XX-YY`). Zero normalization transformations were applied.

## Cross-Reference Validation

6 neighboring Dependencies.csv files were read to validate bidirectional pairs:
- DEL-01-03: 17 rows, v3.1, readable
- DEL-03-07: 18 rows, v3.1, readable
- DEL-02-01: 6 rows, v3.1, readable
- DEL-02-02: 10 rows, v3.1, readable
- DEL-02-03: 11 rows, v3.1, readable
- DEL-02-04: 9 rows, v3.1, readable

All neighbor CSVs were successfully parsed. No schema errors in neighbors.

## Limits

- Hub threshold (20) was not approached (max degree = 6).
- Max cycles limit (10000) was not approached (0 cycles detected).
- Single-deliverable scope limits the graph to a local star topology. Full-workspace closure analysis would be needed for transitive cycle detection beyond the immediate neighborhood.

## Data Quality Notes

- All 11 rows have `Status=ACTIVE`, so `FILTER_ACTIVE_ONLY=true` had no filtering effect.
- All 11 rows have `Confidence=HIGH`.
- All 11 rows have `Origin=EXTRACTED`.
- `RequiredMaturity`, `ProposedMaturity`, and `SatisfactionStatus` are uniformly `TBD` across all rows. This is expected for a freshly extracted register.
