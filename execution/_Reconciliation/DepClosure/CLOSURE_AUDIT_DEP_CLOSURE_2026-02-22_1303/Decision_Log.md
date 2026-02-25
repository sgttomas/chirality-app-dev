# Decision Log -- AUDIT_DEP_CLOSURE

## Defaults Applied

| Decision | Rationale |
|---|---|
| FILTER_ACTIVE_ONLY = true | Per AGENT_AUDIT_DEP_CLOSURE default; only ACTIVE status rows contribute edges |
| NORMALIZE_IDS = true | Per AGENT_AUDIT_DEP_CLOSURE default; strip `_Label` suffix from DEL-XX-YY_Label for analysis |
| HUB_THRESHOLD = 20 | Per AGENT_AUDIT_DEP_CLOSURE default |
| MAX_CYCLES = 10000 | Per AGENT_AUDIT_DEP_CLOSURE default |
| EDGE_FILTER = EXECUTION + DELIVERABLE | Per AGENT_AUDIT_DEP_CLOSURE default |

## Overrides

None. No human overrides were received during this run.

## Tie-breaks

| Item | Resolution |
|---|---|
| UPSTREAM edge direction | UPSTREAM edges are modeled as `from_deliverable -> target_deliverable` (the declaring deliverable depends on the target). This is the standard interpretation. |
| DOWNSTREAM edge direction | DOWNSTREAM edges are modeled as `target_deliverable -> from_deliverable` (the target depends on the declaring deliverable). The edge is reversed so the graph represents "depends on" uniformly. |
| Bidirectional pairs | Bidirectional pairs (A->B and B->A both present) are reported as INFO by default, not elevated. Both edge directions are preserved in the graph. This means bidirectional pairs inherently form 2-node SCCs. |
