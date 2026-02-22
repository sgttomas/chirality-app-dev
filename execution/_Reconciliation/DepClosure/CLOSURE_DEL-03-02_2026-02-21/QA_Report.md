# QA Report -- CLOSURE_DEL-03-02_2026-02-21

## Coverage

| Deliverable | Dependencies.csv Status | Schema Status | Rows Parsed | Edges Extracted |
|---|---|---|---|---|
| DEL-03-02 | FOUND | VALID (v3.1) | 14 | 7 |

- **Coverage rate:** 1/1 deliverables in scope have readable, schema-valid Dependencies.csv (100%).
- **Total rows parsed:** 14
- **Rows filtered (ANCHOR / non-EXECUTION):** 7
- **Rows passing edge filter (EXECUTION + DELIVERABLE):** 7

## Schema Validation Details

The Dependencies.csv for DEL-03-02 declares `RegisterSchemaVersion = v3.1`. All 29 expected columns are present:

`RegisterSchemaVersion, DependencyID, FromPackageID, FromDeliverableID, FromDeliverableName, DependencyClass, AnchorType, Direction, DependencyType, TargetType, TargetPackageID, TargetDeliverableID, TargetRefID, TargetName, TargetLocation, Statement, EvidenceFile, SourceRef, EvidenceQuote, Explicitness, RequiredMaturity, ProposedMaturity, SatisfactionStatus, Confidence, Origin, FirstSeen, LastSeen, Status, Notes`

No missing columns. No extra columns. Schema is fully compliant.

## Direction Handling

All EXECUTION edges have explicit Direction values (6 UPSTREAM, 1 DOWNSTREAM). No ambiguous/missing direction values. No undirected fallback required for SCC detection.

## Normalization

NORMALIZE_IDS is enabled. All `FromDeliverableID` and `TargetDeliverableID` values are already in short-form (`DEL-XX-YY`). Normalization rate: 0 IDs required normalization out of 21 total ID references (14 FromDeliverableID + 7 TargetDeliverableID).

## Limitations

- **Single-deliverable scope:** Only DEL-03-02 is in scope. Cross-deliverable checks (cycles, bidirectional pairs, hub comparisons) are structurally limited.
- **No reverse-edge visibility:** Target deliverable CSVs are not read, so incoming edges to DEL-03-02 from other deliverables are not analyzed.
