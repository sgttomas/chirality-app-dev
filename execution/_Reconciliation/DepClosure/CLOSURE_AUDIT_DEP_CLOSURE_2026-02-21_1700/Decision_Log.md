# Decision Log -- AUDIT_DEP_CLOSURE 2026-02-21

## Defaults Applied

| Decision | Value | Rationale |
|----------|-------|-----------|
| FILTER_ACTIVE_ONLY | true | Per agent instructions default. All Status!=ACTIVE rows excluded from graph edges. |
| NORMALIZE_IDS | true | Per agent instructions default. Long-form IDs normalized by stripping `_{description}` suffix. |
| EDGE_FILTER | DependencyClass=EXECUTION, TargetType=DELIVERABLE | Per agent instructions default. Only execution-class deliverable-target edges included in graph. |
| HUB_THRESHOLD | 20 | Per agent instructions default. |
| MAX_CYCLES | 10000 | Per agent instructions default. |

## Overrides

None. No human overrides recorded for this run.

## Tie-breaks and Interpretive Decisions

| Item | Decision | Rationale |
|------|----------|-----------|
| `_Archive` folder under PKG-08 | Excluded from deliverable set | The folder `execution/PKG-08_Optional_Integrity_Hardening/1_Working/_Archive/` was discovered during traversal but has no DEL-XX-YY prefix. It is an infrastructure folder, not a deliverable. Excluded from all analysis (node count, edge count, coverage). |
| Direction handling for SCC | Directed graph used | All edges have explicit Direction metadata (UPSTREAM or DOWNSTREAM). Graph treated as directed for SCC detection. No ambiguous-direction edges found. |
| SCC severity classification | WARNING (not BLOCKER) | The single large SCC (31 nodes) is primarily composed of bidirectional pairs representing legitimate UPSTREAM/DOWNSTREAM relationships between related deliverables. These are interface and prerequisite relationships, not pathological cycles. Classified as WARNING with recommendation for human review rather than BLOCKER. |
| Bidirectional pairs | INFO level | Bidirectional pairs (A->B and B->A) reflect legitimate architectural relationships where two deliverables each declare the other as a dependency in complementary directions. Not elevated to WARNING. |
