# Dependency Closure Report -- DEL-06-05

**Run ID:** CLOSURE_DEL-06-05_2026-02-21
**Scope:** DEL-06-05 (Governance Coherence + Guardrails)
**Requested by:** RECONCILIATION
**Date:** 2026-02-21
**Overall Status:** PASS

---

## 1. Scope and Coverage

| Metric | Value |
|---|---|
| Deliverables in scope | 1 (DEL-06-05) |
| Dependencies.csv found | 1/1 (100%) |
| Schema version | v3.1 |
| Schema valid | Yes |
| Total rows | 17 |
| ACTIVE rows | 17 (all) |
| RETIRED rows | 0 |

### Edge Filter Applied

- DependencyClass = EXECUTION
- TargetType = DELIVERABLE
- Status = ACTIVE

**Qualifying edges:** 3 (DEP-06-05-014, DEP-06-05-015, DEP-06-05-016)

### Graph Summary

- **Nodes:** 4 (DEL-06-05, DEL-06-01, DEL-03-04, DEL-03-06)
- **Directed edges:** 3 (all UPSTREAM from DEL-06-05)
  - DEL-06-05 --> DEL-06-01 (INTERFACE, DEP-06-05-014)
  - DEL-06-05 --> DEL-03-04 (INTERFACE, DEP-06-05-015)
  - DEL-06-05 --> DEL-03-06 (INTERFACE, DEP-06-05-016)

---

## 2. Core Check Results

### Check 1: Schema Compliance -- PASS

| Metric | Value |
|---|---|
| Deliverables with readable CSV | 1/1 |
| Schema-valid CSVs | 1/1 |
| Coverage | 100% |

**Verdict:** PASS. The Dependencies.csv declares `RegisterSchemaVersion=v3.1` and all 29 expected columns are present.

**Evidence:** `Evidence/coverage.csv`

---

### Check 2: Orphan Dependencies -- PASS

Orphan check verifies that every `TargetDeliverableID` in qualifying edges resolves to a deliverable that exists in the workspace.

| TargetDeliverableID | Exists in Workspace | DependencyID |
|---|---|---|
| DEL-06-01 | Yes (PKG-06) | DEP-06-05-014 |
| DEL-03-04 | Yes (PKG-03) | DEP-06-05-015 |
| DEL-03-06 | Yes (PKG-03) | DEP-06-05-016 |

**Verdict:** PASS. All 3 DELIVERABLE targets exist in the workspace (32 known deliverables across PKG-01 through PKG-08).

**Evidence:** `Evidence/orphans.csv`

---

### Check 3: Circular Dependencies -- PASS

**Method:** Tarjan's algorithm for SCC detection on the directed graph.

**Graph:** 4 nodes, 3 edges (all outbound from DEL-06-05; no return edges in scope).

**SCCs found:** 4 trivial (size=1). No non-trivial SCCs.

**Verdict:** PASS. No circular dependencies detected.

**Evidence:** `Evidence/cycles_sample.csv`, `Evidence/scc_summary.csv`

**Note:** This is a single-deliverable scope run. Cycles that span multiple deliverables' registers would only be detected in a SCOPE=ALL run. The absence of cycles here means DEL-06-05's own register does not introduce self-referential loops.

---

### Check 4: Anchor Coverage -- PASS

Anchor rows (DependencyClass=ANCHOR) for DEL-06-05:

| DependencyID | AnchorType | TargetType | TargetRefID |
|---|---|---|---|
| DEP-06-05-001 | IMPLEMENTS_NODE | WBS_NODE | OBJ-006 |
| DEP-06-05-002 | TRACES_TO_REQUIREMENT | REQUIREMENT | SOW-030 |
| DEP-06-05-003 | TRACES_TO_REQUIREMENT | REQUIREMENT | SOW-039 |
| DEP-06-05-004 | TRACES_TO_REQUIREMENT | REQUIREMENT | SOW-040 |
| DEP-06-05-005 | TRACES_TO_REQUIREMENT | REQUIREMENT | SOW-041 |
| DEP-06-05-006 | TRACES_TO_REQUIREMENT | REQUIREMENT | SOW-042 |
| DEP-06-05-007 | TRACES_TO_REQUIREMENT | REQUIREMENT | SOW-043 |

**IMPLEMENTS_NODE anchors:** 1 (DEP-06-05-001, anchoring to OBJ-006)
**TRACES_TO_REQUIREMENT anchors:** 6 (SOW-030, SOW-039 through SOW-043)

**Verdict:** PASS. At least one ANCHOR row with AnchorType=IMPLEMENTS_NODE exists.

**Evidence:** Dependencies.csv rows DEP-06-05-001 through DEP-06-05-007.

---

### Check 5: Misplaced Fields -- PASS

Misplaced fields check: rows where TargetType != DELIVERABLE but TargetDeliverableID is non-empty.

| Row Range | TargetType | TargetDeliverableID | Status |
|---|---|---|---|
| DEP-06-05-001 to -007 | WBS_NODE / REQUIREMENT | (empty) | OK |
| DEP-06-05-008 to -013 | DOCUMENT | (empty) | OK |
| DEP-06-05-017 | EXTERNAL | (empty) | OK |
| DEP-06-05-014 to -016 | DELIVERABLE | DEL-06-01, DEL-03-04, DEL-03-06 | OK (TargetType=DELIVERABLE, so field is expected) |

**Verdict:** PASS. No rows have a non-empty TargetDeliverableID when TargetType is not DELIVERABLE.

**Evidence:** Full Dependencies.csv scan (17 rows).

---

### Check 6: ID Format Consistency -- PASS

With NORMALIZE_IDS=true, IDs are checked for long-form suffixes (e.g., `DEL-XX-YY_Description`).

| Field | Unique Values | Long-Form Count | Short-Form Count |
|---|---|---|---|
| FromDeliverableID | 1 (DEL-06-05) | 0 | 1 |
| TargetDeliverableID | 3 (DEL-06-01, DEL-03-04, DEL-03-06) | 0 | 3 |

**Normalization rate:** 0% required (all IDs are already short-form DEL-XX-YY).

**Verdict:** PASS. All deliverable IDs use consistent short-form format.

**Evidence:** Dependencies.csv columns FromDeliverableID and TargetDeliverableID.

---

### Check 7: Isolated Deliverables -- PASS

An isolated deliverable has zero EXECUTION edges with TargetType=DELIVERABLE (after filters).

| DeliverableID | Outbound EXECUTION-DELIVERABLE Edges | Isolated? |
|---|---|---|
| DEL-06-05 | 3 | No |

**Verdict:** PASS. DEL-06-05 has 3 outbound execution-deliverable edges and is not isolated.

**Note:** The target deliverables (DEL-06-01, DEL-03-04, DEL-03-06) appear as leaf nodes in this single-deliverable-scope graph. Their isolation status can only be fully assessed in a SCOPE=ALL run where their own Dependencies.csv files are loaded.

**Evidence:** `Evidence/hubs.csv`

---

### Check 8: Hub Analysis -- PASS

Hub threshold: 20 (default).

| DeliverableID | InDegree | OutDegree | TotalDegree | Hub? |
|---|---|---|---|---|
| DEL-06-05 | 0 | 3 | 3 | No |
| DEL-06-01 | 1 | 0 | 1 | No |
| DEL-03-04 | 1 | 0 | 1 | No |
| DEL-03-06 | 1 | 0 | 1 | No |

**Verdict:** PASS. No nodes meet or exceed the hub threshold of 20.

**Evidence:** `Evidence/hubs.csv`

---

### Check 9: Bidirectional Pairs -- PASS

Bidirectional pair detection requires edges in both directions between two nodes (A-->B and B-->A).

| Pair | A-->B | B-->A | Bidirectional? |
|---|---|---|---|
| DEL-06-05 <-> DEL-06-01 | Yes (DEP-06-05-014) | Unknown (DEL-06-01 register not in scope) | INCOMPLETE |
| DEL-06-05 <-> DEL-03-04 | Yes (DEP-06-05-015) | Unknown (DEL-03-04 register not in scope) | INCOMPLETE |
| DEL-06-05 <-> DEL-03-06 | Yes (DEP-06-05-016) | Unknown (DEL-03-06 register not in scope) | INCOMPLETE |

**Verdict:** PASS. No bidirectional pairs detected within the loaded scope. Reverse edges from DEL-06-01, DEL-03-04, and DEL-03-06 were not evaluated because their registers are outside this single-deliverable scope.

**Evidence:** `Evidence/bidirectional_pairs.csv`

---

## 3. Summary of Findings

| Check | Verdict | Issues |
|---|---|---|
| 1. Schema Compliance | PASS | 0 |
| 2. Orphan Dependencies | PASS | 0 |
| 3. Circular Dependencies | PASS | 0 |
| 4. Anchor Coverage | PASS | 0 |
| 5. Misplaced Fields | PASS | 0 |
| 6. ID Format Consistency | PASS | 0 |
| 7. Isolated Deliverables | PASS | 0 |
| 8. Hub Analysis | PASS | 0 |
| 9. Bidirectional Pairs | PASS | 0 |

**Overall closure status: PASS**

No BLOCKER or WARNING findings. The DEL-06-05 dependency register is well-formed, has proper anchoring, and all execution-deliverable targets resolve to known workspace deliverables.

---

## 4. Limitations

1. **Single-deliverable scope.** Only DEL-06-05's Dependencies.csv was analyzed. Cross-deliverable cycles, bidirectional pairs involving other registers, and full hub analysis require a SCOPE=ALL run.
2. **No comparison mode.** PRIOR_RUN_LABEL was not provided; no delta analysis performed.
3. **Target deliverable registers not loaded.** DEL-06-01, DEL-03-04, and DEL-03-06 are confirmed to exist in the workspace but their own Dependencies.csv files were not parsed. Any issues in those registers would be surfaced by their own closure runs.
