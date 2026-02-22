# QA Report -- AUDIT_DEP_CLOSURE 2026-02-21

## Coverage

| Metric | Value |
|--------|-------|
| Deliverables discovered | 32 |
| Dependencies.csv present | 32/32 |
| Dependencies.csv SCHEMA_VALID | 32/32 |
| Dependencies.csv SCHEMA_INVALID | 0 |
| Dependencies.csv MISSING | 0 |
| Coverage rate | 100% |

## Discovery Notes

- The folder `execution/PKG-08_Optional_Integrity_Hardening/1_Working/_Archive/` was discovered during traversal but excluded from analysis because it has no `DEL-XX-YY` prefix and no `Dependencies.csv`. This is an infrastructure/archive folder, not a deliverable.
- All 8 packages have their `1_Working/` subfolder present and populated.

## Schema Validation Detail

All 32 deliverables declare `RegisterSchemaVersion=v3.1` with the correct 29-column header matching the canonical column order per `AGENT_DEPENDENCIES.md`.

### Fix Confirmation: DEL-05-04

| Property | Previous Run | This Run |
|----------|-------------|----------|
| Column count | 30 (INVALID) | 29 (VALID) |
| Column order | Non-canonical | Canonical v3.1 |
| RequiredMaturity present | No | Yes |
| ProposedMaturity present | No | Yes |
| Extra non-canonical columns | Yes | No |
| Schema status | SCHEMA_INVALID | SCHEMA_VALID |

### Fix Confirmation: DEL-08-04

| Property | Previous Run | This Run |
|----------|-------------|----------|
| DEP-08-04-007 TargetType | DELIVERABLE (misplaced) | DOCUMENT (correct) |
| DEP-08-04-007 TargetDeliverableID | (was non-empty) | (empty -- correct) |
| Misplaced field finding | 1 finding | 0 findings |

## Direction Metadata

All EXECUTION/DELIVERABLE edges across all 32 deliverables have explicit `Direction` values (UPSTREAM or DOWNSTREAM). No UNKNOWN or missing direction values were encountered. The graph was treated as fully directed for SCC detection with no ambiguity flags required.

## Limits and Methodology

- `FILTER_ACTIVE_ONLY=true`: Only `Status=ACTIVE` rows included. No RETIRED rows were encountered.
- `NORMALIZE_IDS=true`: All IDs were already in short form (`DEL-XX-YY`). Normalization rate: 0 long-form IDs found / 119 edge references = 0% normalization needed.
- `MAX_CYCLES=10000`: Cycle enumeration bounded. 115 representative cycles found within the single SCC.
- `HUB_THRESHOLD=20`: No nodes exceeded this threshold. Maximum degree observed: DEL-03-02 with degree 17 (7 outgoing + 10 incoming).

## Known Limitations

- The `_Archive` folder exclusion is based on naming convention (no `DEL-` prefix). If a legitimate deliverable were placed in `_Archive`, it would be missed. This is acceptable per the deliverable folder naming convention.
