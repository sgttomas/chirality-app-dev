# Decision Log

| Decision | Value | Rationale |
|---|---|---|
| SCOPE | ALL deliverables discovered under `execution/PKG-*/1_Working/DEL-*` | Full-graph audit truth requires complete scope. |
| FILTER_ACTIVE_ONLY | true | Excludes retired rows from active closure posture. |
| NORMALIZE_IDS | true | Ensures long-form folder IDs and short-form IDs reconcile deterministically. |
| BLOCKER_SUBSET_RULE | `EXECUTION + DELIVERABLE + ACTIVE + UPSTREAM + (PREREQUISITE|CONSTRAINT) + non-ASSUMPTION` | Execution sequencing truth follows `_COORDINATION.md` policy. |
| PKG-08 core sequencing | excluded in secondary advisory view | Human ruling keeps PKG-08 traceable but non-driving. |
| Data-quality handling | report caveats only | AUDIT_DEP_CLOSURE is read-only on deliverables. |

## Overrides

- None.
