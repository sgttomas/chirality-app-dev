# QA Report -- CLOSURE_DEL-05-02_2026-02-21

## Coverage

| Metric | Value |
|---|---|
| Deliverables in scope | 1 |
| Dependencies.csv found | 1 / 1 (100%) |
| Dependencies.csv readable | 1 / 1 (100%) |
| Schema-valid (v3.1) | 1 / 1 (100%) |
| Total rows parsed | 13 |
| Rows with Status=ACTIVE | 13 / 13 (100%) |
| Rows excluded by FILTER_ACTIVE_ONLY | 0 |
| Qualifying edges (EXECUTION + DELIVERABLE + ACTIVE) | 5 |
| ANCHOR rows | 4 |
| EXECUTION rows (non-DELIVERABLE target) | 4 |

## Schema Validation Detail

**DEL-05-02 Dependencies.csv:**
- RegisterSchemaVersion declared: `v3.1`
- Expected columns (29): All present
- Missing columns: None
- Extra columns: None
- Schema verdict: **VALID**

## Data Quality Observations

1. **All rows have Status=ACTIVE.** No RETIRED rows exist, so FILTER_ACTIVE_ONLY had no filtering effect.
2. **All FromDeliverableID values are consistent** (`DEL-05-02` in all 13 rows).
3. **All IDs are in short-form.** No normalization was required.
4. **FromPackageID is consistent** (`PKG-05` in all 13 rows).
5. **Confidence values are well-populated:** HIGH (11 rows), MEDIUM (2 rows -- DEP-05-02-005, DEP-05-02-012).
6. **RequiredMaturity and ProposedMaturity are TBD** across all rows. This is expected for initial extraction.
7. **SatisfactionStatus:** NOT_APPLICABLE for ANCHOR rows (4), TBD for EXECUTION rows (9). Expected.

## Direction Metadata

All edges have explicit Direction values (UPSTREAM or DOWNSTREAM). No UNKNOWN or missing directions were encountered. No ambiguity flags needed for SCC detection.

| Direction | Count |
|---|---|
| UPSTREAM | 5 (1 DELIVERABLE + 4 DOCUMENT) |
| DOWNSTREAM | 4 (all DELIVERABLE) |

## Limitations

1. **Single-deliverable scope:** Circular dependency detection is limited to self-loops (none found). Full cycle detection requires SCOPE=ALL.
2. **Bidirectional pair detection:** Requires examining multiple CSVs. Not assessable from a single deliverable's CSV.
3. **Isolated deliverable assessment:** Adjacent nodes (DEL-05-01, DEL-05-03, etc.) cannot have their isolation status determined from this CSV alone.
4. **No prior run comparison:** PRIOR_RUN_LABEL was not provided, so no delta analysis was performed.
