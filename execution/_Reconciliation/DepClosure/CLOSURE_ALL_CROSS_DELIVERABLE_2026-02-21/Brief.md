# Brief -- AUDIT_DEP_CLOSURE

## Verbatim Brief

- REQUESTED_BY: RECONCILIATION
- RUN_LABEL: ALL_CROSS_DELIVERABLE
- EXECUTION_ROOT: execution/
- SCOPE: ALL
- INPUT_ARTIFACTS: All 32 Dependencies.csv files across 8 packages
- OUTPUT_REQUIREMENTS: Write all outputs to execution/_Reconciliation/DepClosure/CLOSURE_ALL_CROSS_DELIVERABLE_2026-02-21/
- ACCEPTANCE_CRITERIA: Closure report with PASS/WARNING/BLOCKER for all 9 core checks using the FULL cross-deliverable graph; evidence pointers for every finding; no deliverable files modified
- CONSTRAINTS: Read-only on deliverables; evidence-first; no invention; deterministic
- ESCALATION: Return findings to RECONCILIATION

## Normalized Parameters

| Parameter | Value |
|---|---|
| EXECUTION_ROOT | `execution/` |
| SCOPE | `ALL` (32 deliverables) |
| RUN_LABEL | `ALL_CROSS_DELIVERABLE` |
| REQUESTED_BY | `RECONCILIATION` |
| FILTER_ACTIVE_ONLY | `true` |
| NORMALIZE_IDS | `true` |
| EDGE_FILTER | `DependencyClass=EXECUTION, TargetType=DELIVERABLE` |
| HUB_THRESHOLD | `20` |
| MAX_CYCLES | `10000` |
| PRIOR_RUN_LABEL | (not provided; no comparison mode) |
