# QA Report -- AUDIT_DEP_CLOSURE_2026-02-24_2306

## Coverage Summary

| Metric | Value |
|---|---|
| Deliverables discovered | 37 |
| Dependencies.csv exists | 37 / 37 (100%) |
| Dependencies.csv readable | 37 / 37 (100%) |
| Schema valid (v3.1) | 37 / 37 (100%) |
| Schema coverage | 100.0% |

All 37 deliverables have readable, schema-valid Dependencies.csv registers. No MISSING_DEPENDENCIES_CSV or SCHEMA_INVALID entries.

## Schema Issues

None. All registers conform to v3.1 schema with all 29 required columns present.

## ID Normalization

| Metric | Value |
|---|---|
| NORMALIZE_IDS | `true` |
| Long-form FromDeliverableID | 0 |
| Long-form TargetDeliverableID | 0 |
| Normalization rate | 0% (all IDs already in short form) |

## Direction Handling

All 143 EXECUTION/DELIVERABLE/ACTIVE rows have explicit `Direction` values (UPSTREAM or DOWNSTREAM). No rows with missing or unknown direction were encountered. No ambiguity flags required for SCC analysis.

## Edge Filter Statistics

| Metric | Value |
|---|---|
| Total rows across all CSVs | (varies by deliverable) |
| EXECUTION/DELIVERABLE/ACTIVE rows | 143 |
| Unique directed edges (after direction normalization) | 101 |
| Orphan target rows (target not in scope) | 0 |

## Blocker Subset Statistics

| Metric | Value |
|---|---|
| Blocker-subset edges (UPSTREAM + PREREQUISITE/CONSTRAINT) | 45 |
| Blocker-subset SCCs | 0 |
| Topological tiers (all nodes) | 9 |
| Topological tiers (core, excl PKG-08) | 9 |
| Remaining after topo sort | 0 |

## Data Quality Caveats

None. No data quality issues were detected in this run.

## Limits

- MAX_CYCLES (10000) was not reached (0 cycles found).
- HUB_THRESHOLD (20) was not reached by any deliverable. Highest degree: DEL-03-01 and DEL-03-07 at 12.
