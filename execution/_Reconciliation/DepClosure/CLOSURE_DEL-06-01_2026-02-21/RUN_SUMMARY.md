# RUN_SUMMARY

| Field | Value |
|---|---|
| **RUN_STATUS** | WARNINGS |
| **Snapshot** | `CLOSURE_DEL-06-01_2026-02-21` |
| **Run Date** | 2026-02-21 |
| **Requested By** | RECONCILIATION |
| **Scope** | DEL-06-01 (single deliverable) |
| **Deliverables in Scope** | 1 |
| **Dependencies.csv Found** | 1 / 1 |
| **Schema Valid** | 1 / 1 |
| **Total Rows Parsed** | 10 |
| **Qualifying Edges (EXECUTION + DELIVERABLE)** | 0 |
| **Core Checks Run** | 9 / 9 |
| **PASS** | 6 |
| **WARNING** | 1 |
| **INFO** | 2 |
| **BLOCKER** | 0 |

## Top Issues

1. **WARNING -- Isolated Deliverable:** DEL-06-01 has zero EXECUTION edges targeting other deliverables. All 6 EXECUTION dependencies target DOCUMENT-type artifacts (non-deliverable prerequisites and handovers). This means DEL-06-01 is structurally isolated from the cross-deliverable dependency graph.

## Recommended Next Action

Review whether DEL-06-01 should have explicit deliverable-to-deliverable dependencies. If the deliverable genuinely has no cross-deliverable execution dependencies (plausible for a governance/conformance task that operates on document-level inputs), the WARNING may be accepted as informational. Otherwise, dispatch DEPENDENCIES extraction rerun to capture missing edges.
