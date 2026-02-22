# QA Report -- CLOSURE_DEL-08-05_2026-02-21

## Coverage

| Metric | Value |
|---|---|
| Deliverables in scope | 1 |
| Dependencies.csv found | 1 (100%) |
| Dependencies.csv readable | 1 (100%) |
| Schema valid (v3.1) | 1 (100%) |
| Rows parsed | 15 |
| Rows excluded (schema errors) | 0 |

## Schema Validation Details

**DEL-08-05:** VALID (v3.1)
- All 29 expected columns present.
- No missing or extra columns.
- All 15 rows have non-empty DependencyID, FromDeliverableID, DependencyClass, Status.
- File: `execution/PKG-08_Optional_Integrity_Hardening/1_Working/DEL-08-05_Deliverable_Lock_Mechanism/Dependencies.csv`

## Edge Filter Application

| Filter | Setting | Rows Passing |
|---|---|---|
| Status = ACTIVE | Applied | 15/15 |
| DependencyClass = EXECUTION | Applied | 10/15 |
| TargetType = DELIVERABLE | Applied | 3/10 |
| Final graph edges | -- | 3 |

## Direction Handling

All 3 graph edges have explicit Direction values (DOWNSTREAM). No ambiguous/missing direction values were encountered. SCC detection used directed graph treatment throughout.

## Scope Limitations

This is a single-deliverable analysis. The following checks produce limited results:
- **Circular dependencies:** Only self-loops can be detected; cross-deliverable cycles require SCOPE=ALL.
- **Bidirectional pairs:** Only visible when both sides of a pair are in scope.
- **Hub analysis (InDegree):** Inbound edges from other deliverables are not visible.

These limitations are expected and documented in the closure report.

## Limits and Thresholds

| Parameter | Value | Hit Limit |
|---|---|---|
| MAX_CYCLES | 10000 | NO (0 cycles found) |
| HUB_THRESHOLD | 20 | NO (max degree = 3) |

## Data Quality Notes

- All rows have ACTIVE status.
- All DependencyIDs follow the expected pattern (DEP-08-05-NNN).
- All FromDeliverableID values are consistently DEL-08-05.
- All TargetDeliverableID values in DELIVERABLE rows are short-form (no normalization needed).
- No empty or malformed critical fields detected.
