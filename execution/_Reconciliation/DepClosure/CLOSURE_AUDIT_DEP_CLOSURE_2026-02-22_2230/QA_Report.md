# QA Report -- AUDIT_DEP_CLOSURE

## Coverage

| Metric | Value |
|---|---|
| Total deliverables in scope | 36 |
| Dependencies.csv exists | 36 (100%) |
| Dependencies.csv readable | 36 (100%) |
| Schema v3.1 valid | 36 (100%) |
| Schema coverage | 100.0% |

All 36 deliverables have readable, schema-valid Dependencies.csv files conforming to v3.1.

## Schema Issues

None. All 36 registers pass v3.1 column validation.

## Direction Handling

All EXECUTION/DELIVERABLE edges have explicit Direction values (UPSTREAM or DOWNSTREAM). No UNKNOWN direction edges were encountered. The graph was built as a directed graph with no undirected fallback required.

## ID Normalization

- NORMALIZE_IDS = true
- All FromDeliverableID and TargetDeliverableID values were already in short form (DEL-XX-YY). Zero long-form IDs requiring normalization.
- Folder names use long form (DEL-XX-YY_Label); normalization was applied during discovery only.

## Edge Filtering

- FILTER_ACTIVE_ONLY = true: All rows with Status=ACTIVE were included.
- DependencyClass = EXECUTION: Only EXECUTION-class rows contributed graph edges. ANCHOR rows were excluded from the graph but analyzed for anchor coverage (Check 4).
- TargetType = DELIVERABLE: Only inter-deliverable edges were included. DOCUMENT, EXTERNAL, REQUIREMENT, WBS_NODE, PACKAGE, UNKNOWN targets were excluded from the graph.

## Limits

- MAX_CYCLES = 10000. 24 cycles were enumerated from 3 SCCs. No truncation.
- HUB_THRESHOLD = 20. No nodes exceeded this threshold (max total degree = 17).

## Reproducibility

The analysis script `analyze_closure.py` in this snapshot folder is deterministic: same Dependencies.csv inputs produce identical outputs. The script can be re-executed at any time for verification.
