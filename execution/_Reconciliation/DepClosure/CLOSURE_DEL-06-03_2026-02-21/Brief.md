# Brief -- AUDIT_DEP_CLOSURE for DEL-06-03

## Verbatim Brief

- REQUESTED_BY: RECONCILIATION
- RUN_LABEL: DEL-06-03
- EXECUTION_ROOT: execution/
- SCOPE: DEL-06-03
- DELIVERABLE_PATH: execution/PKG-06_Agent_Suite_Governance/1_Working/DEL-06-03_Cross_Deliverable_Workflows/
- INPUT_ARTIFACTS: Dependencies.csv in the deliverable folder
- OUTPUT_REQUIREMENTS: Write all outputs to execution/_Reconciliation/DepClosure/CLOSURE_DEL-06-03_2026-02-21/
- ACCEPTANCE_CRITERIA: Closure report with PASS/WARNING/BLOCKER for all core checks; evidence pointers for every finding; no deliverable files modified
- CONSTRAINTS: Read-only on deliverables; evidence-first; no invention; deterministic
- ESCALATION: Return findings to RECONCILIATION

## Normalized Parameters

| Parameter | Value |
|---|---|
| EXECUTION_ROOT | `execution/` |
| SCOPE | `DEL-06-03` (single deliverable) |
| RUN_LABEL | `DEL-06-03` |
| REQUESTED_BY | `RECONCILIATION` |
| FILTER_ACTIVE_ONLY | `true` (default) |
| NORMALIZE_IDS | `true` (default) |
| EDGE_FILTER | `DependencyClass=EXECUTION, TargetType=DELIVERABLE` |
| HUB_THRESHOLD | `20` (default) |
| MAX_CYCLES | `10000` (default) |
| PRIOR_RUN_LABEL | (none) |

## Workspace Context

- 32 deliverables across 8 packages (PKG-01 through PKG-08)
- All 32 DEL-XX-YY IDs are valid targets per brief
- Single-deliverable scope: only DEL-06-03's Dependencies.csv is the primary input
- Bidirectional analysis required cross-referencing other deliverables' Dependencies.csv files
