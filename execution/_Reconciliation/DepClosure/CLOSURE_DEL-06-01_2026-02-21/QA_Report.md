# QA Report -- CLOSURE_DEL-06-01_2026-02-21

## Coverage

| Deliverable | Dependencies.csv | Schema Version | Schema Valid | Rows Parsed | Edges Extracted |
|---|---|---|---|---|---|
| DEL-06-01 | FOUND | v3.1 | YES | 10 | 0 |

**Coverage rate:** 1/1 (100%) deliverables in scope have a readable, schema-valid Dependencies.csv.

## Schema Validation Detail

The Dependencies.csv for DEL-06-01 declares `RegisterSchemaVersion = v3.1` and contains all 29 expected columns per AGENT_DEPENDENCIES.md specification:

`RegisterSchemaVersion, DependencyID, FromPackageID, FromDeliverableID, FromDeliverableName, DependencyClass, AnchorType, Direction, DependencyType, TargetType, TargetPackageID, TargetDeliverableID, TargetRefID, TargetName, TargetLocation, Statement, EvidenceFile, SourceRef, EvidenceQuote, Explicitness, RequiredMaturity, ProposedMaturity, SatisfactionStatus, Confidence, Origin, FirstSeen, LastSeen, Status, Notes`

No schema issues detected.

## Edge Filter Application

Default edge filter applied: `DependencyClass = EXECUTION` AND `TargetType = DELIVERABLE`.

- 6 rows matched `DependencyClass = EXECUTION` but none had `TargetType = DELIVERABLE` (all were `DOCUMENT`).
- 4 rows had `DependencyClass = ANCHOR` (excluded by filter as expected).
- Result: 0 qualifying edges extracted.

## Direction Handling

All 10 rows have explicit `Direction` values (9 UPSTREAM, 1 DOWNSTREAM). No ambiguity flags needed for SCC analysis. However, with zero qualifying edges, SCC analysis is trivially empty.

## Limits and Bounds

- `MAX_CYCLES = 10000` -- not reached (0 cycles).
- `HUB_THRESHOLD = 20` -- not reached (max degree = 0).
- No truncation or sampling applied.

## Notes

- All `Status` values are `ACTIVE`; `FILTER_ACTIVE_ONLY=true` had no filtering effect (no RETIRED rows present).
- `NORMALIZE_IDS=true` was enabled but no long-form IDs were found in `FromDeliverableID` or `TargetDeliverableID` columns. All `FromDeliverableID` values are already in short form (`DEL-06-01`). All `TargetDeliverableID` values are empty.
