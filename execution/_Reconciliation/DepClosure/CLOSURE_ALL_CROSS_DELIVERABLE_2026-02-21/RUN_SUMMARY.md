# RUN_SUMMARY

| Field | Value |
|---|---|
| RUN_STATUS | WARNINGS |
| RUN_LABEL | ALL_CROSS_DELIVERABLE |
| RUN_DATE | 2026-02-21 |
| SCOPE | ALL (32 deliverables) |
| REQUESTED_BY | RECONCILIATION |

## Snapshot Path

`execution/_Reconciliation/DepClosure/CLOSURE_ALL_CROSS_DELIVERABLE_2026-02-21/`

## Overall Result

**WARNINGS** -- No BLOCKERs. 4 checks returned WARNING, 1 returned INFO, 4 returned PASS.

## Check Verdicts

| Check | Verdict |
|---|---|
| 1. Schema Compliance | WARNING |
| 2. Orphan Dependencies | PASS |
| 3. Circular Dependencies | WARNING |
| 4. Anchor Coverage | WARNING |
| 5. Misplaced Fields | WARNING |
| 6. ID Format Consistency | PASS |
| 7. Isolated Deliverables | PASS |
| 8. Hub Analysis | PASS |
| 9. Bidirectional Pairs | INFO |

## Key Metrics

| Metric | Value |
|---|---|
| Deliverables in scope | 32 |
| CSVs readable + schema-valid | 31 |
| CSVs schema-invalid | 1 (DEL-05-04) |
| CSVs missing | 0 |
| Total rows parsed | 365 |
| EXECUTION/DELIVERABLE edges | 111 |
| Graph nodes | 32 |
| Graph edges | 111 |
| Nontrivial SCCs | 1 (30 members) |
| Orphans | 0 |
| Isolated deliverables | 0 |
| Hubs (degree >= 20) | 0 |
| Bidirectional pairs | 29 |
| Misplaced fields | 1 |
| Missing anchors | 1 |
| Total issues | 132 (0 BLOCKER, 103 WARNING, 29 INFO) |

## Top Issues (for RECONCILIATION)

1. **Giant SCC (30/32 deliverables)** -- The cross-deliverable graph contains a single strongly connected component spanning 30 of 32 deliverables (all except DEL-05-04 and DEL-06-01). This is driven by 29 bidirectional edge pairs. While many of these are legitimate UPSTREAM/DOWNSTREAM mirrors (e.g., producer-consumer or scope-boundary interfaces), the resulting giant cycle means there is no topological ordering for the workspace -- every deliverable in the SCC transitively depends on every other. This finding was invisible to per-deliverable runs.

2. **DEL-05-04 schema invalid** -- The Dependencies.csv for DEL-05-04 has extra columns (FromDeliverableType, TargetDeliverableType, ConflictFlag) but is missing RequiredMaturity and ProposedMaturity. Its edges were excluded from analysis. Since 8 other deliverables reference DEL-05-04 as a target, the graph has partial coverage for this node.

3. **DEL-05-04 missing IMPLEMENTS_NODE anchor** -- Because DEL-05-04's CSV was excluded due to schema invalidity, its anchor rows were not parsed. DEL-05-04 does have an IMPLEMENTS_NODE row in its CSV; the anchor coverage check flagged this as a false positive caused by the schema exclusion.

4. **DEL-08-04 misplaced field** -- DEP-08-04-007 has TargetType=DELIVERABLE but TargetDeliverableID is empty (it targets "All deliverable-local Dependencies.csv registers" collectively).

5. **29 bidirectional pairs** -- These drive the giant SCC. Many are intentional (e.g., UPSTREAM prerequisite + DOWNSTREAM handover mirrors), but the graph topology impact warrants human review of whether all bidirectional edges are truly necessary.

## Recommended Next Actions

1. **Fix DEL-05-04 schema**: Add RequiredMaturity and ProposedMaturity columns to Dependencies.csv. Then rerun closure analysis.
2. **Review bidirectional edge necessity**: Especially pairs that create cycles across package boundaries (e.g., DEL-05-01 <-> DEL-01-01, DEL-05-01 <-> DEL-01-02, DEL-05-01 <-> DEL-03-01). Consider whether UPSTREAM CONSTRAINT edges need to be recorded in both directions.
3. **Fix DEL-08-04 DEP-08-04-007**: Either set TargetType to something other than DELIVERABLE (since the target is a set of files, not a single deliverable) or populate TargetDeliverableID.
4. **Rerun DEPENDENCIES for DEL-05-04** to regenerate a schema-conformant register.
5. **Rerun closure analysis** after fixes to verify SCC reduction.
