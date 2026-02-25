# QA Report -- CLOSURE_DEL-01-03_2026-02-22_0800

## Coverage

| Metric | Value |
|---|---|
| Deliverables in scope | 1 |
| Dependencies.csv found | 1 |
| Dependencies.csv readable | 1 |
| Schema valid | 1 |
| Coverage rate | 100% |

## Schema Validation Detail

| Deliverable | Schema Version | Columns Expected | Columns Found | Valid |
|---|---|---|---|---|
| DEL-01-03 | v3.1 | 29 | 29 | YES |

All 29 v3.1 columns present: RegisterSchemaVersion, DependencyID, FromPackageID, FromDeliverableID, FromDeliverableName, DependencyClass, AnchorType, Direction, DependencyType, TargetType, TargetPackageID, TargetDeliverableID, TargetRefID, TargetName, TargetLocation, Statement, EvidenceFile, SourceRef, EvidenceQuote, Explicitness, RequiredMaturity, ProposedMaturity, SatisfactionStatus, Confidence, Origin, FirstSeen, LastSeen, Status, Notes.

## Data Quality Observations

1. **All 17 rows have Status=ACTIVE.** No RETIRED rows present.
2. **All IDs are short-form (DEL-XX-YY).** NORMALIZE_IDS had no effect.
3. **DependencyID sequence**: DEP-01-03-001 through DEP-01-03-017, contiguous, no gaps.
4. **Confidence distribution**: 16 rows HIGH, 1 row MEDIUM (DEP-01-03-008, docs/CONTRACT.md -- notes indicate location TBD for specific K-* invariants).
5. **SatisfactionStatus**: 5 PENDING (downstream deliverable edges), 6 NOT_APPLICABLE (anchors), 6 TBD (document constraints + upstream interface).
6. **No direction ambiguity**: All rows have explicit Direction values (UPSTREAM or DOWNSTREAM).

## Limits and Caveats

1. **Single-deliverable scope**: This run only analyzes edges declared by DEL-01-03. Reciprocal edges (e.g., DEL-03-07 declaring a dependency on DEL-01-03) are not verified because DEL-03-07's Dependencies.csv is outside scope.
2. **Bidirectional pair detection is one-sided**: The bidirectional pair DEL-01-03 <-> DEL-03-07 is detected from DEL-01-03's perspective only. A full cross-deliverable run would confirm whether DEL-03-07's register declares the reciprocal relationship.
3. **No prior run for comparison**: PRIOR_RUN_LABEL was not provided; no delta analysis performed.

## Methodology Notes

- Graph edges filtered by: DependencyClass=EXECUTION AND TargetType=DELIVERABLE AND Status=ACTIVE.
- Orphan detection used all 36 workspace deliverables as the reference node set.
- SCC detection (Tarjan) applied to the directed ego graph of DEL-01-03.
- All checks produced deterministic results.
