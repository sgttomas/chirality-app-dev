# QA Report -- CLOSURE_DEL-05-03_2026-02-21

## Coverage

| Deliverable | Dependencies.csv Found | Schema Valid | Rows Parsed | Edges (filtered) |
|---|---|---|---|---|
| DEL-05-03 | YES | YES (v3.1) | 14 | 5 |

**Coverage rate:** 1/1 (100%) deliverables in scope have a readable, schema-valid `Dependencies.csv`.

## Schema Validation Details

The `Dependencies.csv` at `execution/PKG-05_Filesystem_Execution_Model/1_Working/DEL-05-03_Lifecycle_State_Handling/Dependencies.csv` declares `RegisterSchemaVersion = v3.1` on all 14 rows.

**Required columns (v3.1) -- all present:**

- RegisterSchemaVersion
- DependencyID
- FromPackageID
- FromDeliverableID
- FromDeliverableName
- DependencyClass
- AnchorType
- Direction
- DependencyType
- TargetType
- TargetPackageID
- TargetDeliverableID
- TargetRefID
- TargetName
- TargetLocation
- Statement
- EvidenceFile
- SourceRef
- EvidenceQuote
- Explicitness
- RequiredMaturity
- ProposedMaturity
- SatisfactionStatus
- Confidence
- Origin
- FirstSeen
- LastSeen
- Status
- Notes

No missing or extra columns detected.

## Filter Settings

| Filter | Setting | Effect |
|---|---|---|
| FILTER_ACTIVE_ONLY | true | All 14 rows have Status=ACTIVE; none excluded |
| EDGE_FILTER (DependencyClass) | EXECUTION | 9 of 14 rows are EXECUTION class |
| EDGE_FILTER (TargetType) | DELIVERABLE | 5 of 9 EXECUTION rows target DELIVERABLE |
| NORMALIZE_IDS | true | All IDs already in short-form; 0 normalizations applied |

## Direction Handling

All 5 filtered edges have explicit Direction values (2 UPSTREAM, 3 DOWNSTREAM). No ambiguous direction edges. SCC detection uses directed graph as-is.

## Limitations

- **Single-deliverable scope:** This run analyzes only the outgoing dependency edges from DEL-05-03. Reciprocal edges declared by other deliverables (incoming edges to DEL-05-03) are not visible in this scope. Full bidirectional pair analysis and complete cycle detection require SCOPE=ALL.
- **No prior run for comparison:** PRIOR_RUN_LABEL not provided; delta analysis not performed.
