# QA Report -- CLOSURE_DEL-05-01_2026-02-21

## Coverage

| Metric | Value |
|---|---|
| Deliverables in scope | 1 |
| Dependencies.csv found | 1 (100%) |
| Dependencies.csv readable | 1 (100%) |
| Dependencies.csv schema-valid (v3.1) | 1 (100%) |

## Schema Validation Detail

**DEL-05-01** (`execution/PKG-05_Filesystem_Execution_Model/1_Working/DEL-05-01_Instruction_Root_Bundling/Dependencies.csv`):
- RegisterSchemaVersion: v3.1
- Required columns: All present
- Column count: 29 (matches v3.1 expected set)
- Row count: 11 (header + 11 data rows)
- All rows have Status=ACTIVE
- No blank DependencyID fields
- No duplicate DependencyID values

## Schema Issues

None detected.

## Limits and Caveats

1. **Single-deliverable scope.** Only DEL-05-01's Dependencies.csv was parsed. Edges from other deliverables pointing to DEL-05-01 are not visible. This affects:
   - Circular dependency detection (cross-deliverable cycles are invisible).
   - Hub in-degree calculation (in-degree reported as 0).
   - True bidirectional pair detection (only pairs within DEL-05-01's own edges are found).

2. **Direction ambiguity.** No rows had missing or unknown Direction values. All edges have explicit UPSTREAM or DOWNSTREAM directions. No ambiguity flag required for SCC analysis.

3. **ID normalization.** No long-form IDs were encountered. Normalization logic was not exercised. This is expected for SOFTWARE_DECOMP IDs which are already short-form.

## Data Quality Observations

- All 11 rows have populated EvidenceFile, SourceRef, and EvidenceQuote fields.
- All Confidence values are populated (HIGH or MEDIUM or LOW).
- Origin is consistently EXTRACTED across all rows.
- FirstSeen and LastSeen are consistently 2026-02-21.
- Notes field is populated for all rows with FACT/ASSUMPTION classification.
