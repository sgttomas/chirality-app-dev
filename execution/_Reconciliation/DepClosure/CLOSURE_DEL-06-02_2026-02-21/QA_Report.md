# QA Report -- AUDIT_DEP_CLOSURE Run for DEL-06-02

**Run Label:** DEL-06-02
**Run Date:** 2026-02-21

---

## Coverage

| Metric | Value |
|---|---|
| Deliverables in scope | 1 |
| Dependencies.csv found | 1 |
| Dependencies.csv readable | 1 |
| Dependencies.csv schema-valid | 1 |
| Coverage rate | 100% |

No deliverables in scope had missing, unreadable, or schema-invalid Dependencies.csv files.

---

## Schema Issues

None. The Dependencies.csv for DEL-06-02 declares `RegisterSchemaVersion=v3.1` consistently across all 17 rows, and all 29 expected columns are present.

---

## Direction Ambiguity

No ambiguity detected. All 3 EXECUTION/DELIVERABLE rows specify a `Direction` value:
- DEP-06-02-006: UPSTREAM
- DEP-06-02-007: UPSTREAM
- DEP-06-02-008: DOWNSTREAM

No rows required undirected treatment for SCC analysis.

---

## Limits and Constraints

| Limit | Configured | Actual |
|---|---|---|
| MAX_CYCLES | 10000 | 0 cycles found (limit not reached) |
| HUB_THRESHOLD | 20 | Max degree = 3 (no hubs) |

---

## Scope Limitations

This is a **single-deliverable** run. The following analysis dimensions are inherently constrained:

1. **In-degree calculation**: Only outbound edges from DEL-06-02 were analyzed. In-degree from other deliverables cannot be determined without a workspace-wide scan.
2. **Cycle detection**: Only detectable within the subgraph visible from DEL-06-02's edges. No reciprocal edges from DEL-06-01, DEL-05-04, or DEL-06-03 were analyzed.
3. **Bidirectional pairs**: Requires both A and B dependencies.csv files to be in scope.

---

## Data Quality Observations

1. All `FromDeliverableID` values are consistently `DEL-06-02` (correct for a single-deliverable register).
2. All `FromPackageID` values are consistently `PKG-06` (correct).
3. `Status` is `ACTIVE` for all 17 rows (no RETIRED rows).
4. `Confidence` values are `HIGH` (13 rows) or `MEDIUM` (4 rows) -- reasonable distribution.
5. `Origin` is `EXTRACTED` for all rows (consistent with DEPENDENCIES agent output).
6. `FirstSeen` and `LastSeen` are both `2026-02-21` for all rows (consistent with initial extraction).
7. Two rows (DEP-06-02-004, DEP-06-02-005) are annotated as `ASSUMPTION` in Notes, reflecting best-effort objective mapping. This is correctly flagged in the source data.
