# Dependencies -- DEL-06-04

**Tracking Mode:** FULL_GRAPH
**Status:** EXTRACTED

---

## Declared Upstream Dependencies

*No upstream dependencies were declared prior to extraction.*

## Declared Downstream Dependencies

*No downstream dependencies were declared prior to extraction.*

---

## Extracted Dependency Register

**Register:** `Dependencies.csv` (v3.1 schema)
**Total ACTIVE rows:** 9
**Total RETIRED rows:** 0

### ANCHOR Dependencies (3 ACTIVE)

| DependencyID | AnchorType | TargetType | TargetRefID / TargetName | Confidence | Status |
|---|---|---|---|---|---|
| DEP-0604-A001 | IMPLEMENTS_NODE | WBS_NODE | SOW-021 | HIGH | ACTIVE |
| DEP-0604-A002 | TRACES_TO_REQUIREMENT | REQUIREMENT | OBJ-004 | MEDIUM | ACTIVE |
| DEP-0604-A003 | TRACES_TO_REQUIREMENT | REQUIREMENT | OBJ-006 | MEDIUM | ACTIVE |

### EXECUTION Dependencies (6 ACTIVE)

| DependencyID | Direction | DependencyType | TargetType | Target | Confidence | Status |
|---|---|---|---|---|---|---|
| DEP-0604-E001 | UPSTREAM | PREREQUISITE | DOCUMENT | Governance Document Suite (DIRECTIVE, CONTRACT, SPEC, TYPES) | HIGH | ACTIVE |
| DEP-0604-E002 | UPSTREAM | PREREQUISITE | DOCUMENT | AGENT_CHANGE.md (CHANGE agent instruction file) | HIGH | ACTIVE |
| DEP-0604-E003 | UPSTREAM | INTERFACE | DOCUMENT | AGENT_SCOPE_CHANGE.md (boundary review) | HIGH | ACTIVE |
| DEP-0604-E004 | UPSTREAM | INTERFACE | DOCUMENT | AGENT_HELPS_HUMANS.md (structural conformance) | HIGH | ACTIVE |
| DEP-0604-E005 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-06-01 Agent Instruction Suite Structural Conformance | MEDIUM | ACTIVE |
| DEP-0604-E006 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-06-05 Governance Coherence + Guardrails | MEDIUM | ACTIVE |

---

## Lifecycle Summary

| Category | Count |
|---|---|
| ACTIVE | 9 |
| RETIRED | 0 |
| **Total** | **9** |

### By DependencyClass

| DependencyClass | ACTIVE | RETIRED |
|---|---|---|
| ANCHOR | 3 | 0 |
| EXECUTION | 6 | 0 |

### By SatisfactionStatus (ACTIVE rows only)

| SatisfactionStatus | Count |
|---|---|
| TBD | 5 |
| PENDING | 4 |

---

## Run Notes

**Run date:** 2026-02-21
**Mode:** UPDATE
**Strictness:** CONSERVATIVE
**Consumer context:** NONE

### Defaults and Paths Used

- **RUN_ROOT:** `/Users/ryan/ai-env/projects/chirality-app-dev/execution/`
- **DECOMPOSITION_PATH:** `/Users/ryan/ai-env/projects/chirality-app-dev/execution/_Decomposition/ChiralityApp_SoftwareDecomposition_2026-02-21_G7-APPROVED.md`
- **DECOMP_VARIANT:** SOFTWARE
- **SOURCE_DOCS (AUTO):** Datasheet.md, Specification.md, Guidance.md, Procedure.md, _CONTEXT.md, _REFERENCES.md
- **ANCHOR_DOC (AUTO):** Datasheet.md (selected: contains "datasheet" in filename; has explicit scope coverage and objective IDs)
- **EXECUTION_DOC_ORDER (AUTO):** Procedure.md, Specification.md, Guidance.md, Datasheet.md, _CONTEXT.md, _REFERENCES.md

### Decomposition Validation

Decomposition located and loaded successfully. All anchor targets validated:
- SOW-021: Confirmed in Scope Ledger (PKG-06, DEL-06-04)
- OBJ-004: Confirmed in Objectives and Deliverable table (SupportsObjectives for DEL-06-04)
- OBJ-006: Confirmed in Objectives and Deliverable table (SupportsObjectives for DEL-06-04)
- DEL-06-01: Confirmed in Deliverable table (PKG-06)
- DEL-06-05: Confirmed in Deliverable table (PKG-06)

### Extraction Notes

- **Pass 1 (ANCHOR):** Extracted 1 parent anchor (SOW-021 via Datasheet Identification) and 2 requirement traces (OBJ-004, OBJ-006 via Datasheet Identification). Objective mapping is marked ASSUMPTION per Datasheet note ("best-effort mapping via PKG-06 package grouping"); confirmed by decomposition deliverable table which lists both objectives for DEL-06-04.
- **Pass 2 (EXECUTION):** Extracted 6 execution edges. All are UPSTREAM direction. 2 are PREREQUISITE type (governance docs suite, AGENT_CHANGE.md as primary input); 4 are INTERFACE type (AGENT_SCOPE_CHANGE.md boundary review, AGENT_HELPS_HUMANS.md conformance, DEL-06-01 structural conformance standard, DEL-06-05 governance coherence).
- **Exclusion boundary items (NOT extracted):** Specification.md explicitly excludes DEL-08-07 (staleness tooling), DEL-08-01 (content hash verification), dependency governance, and scope change management. These are scope boundary statements, not information-flow dependencies, and were not extracted per the "information flow only" rule.
- **No DOWNSTREAM edges extracted.** The source documents describe outputs (updated AGENT_CHANGE.md, publication guidance constraints document) but do not explicitly name consuming deliverables. Downstream consumers may be identified during aggregation or reconciliation.

### Quality Check Results

- [PASS] Required columns present and CSV parseable.
- [PASS] DependencyID values unique (9 unique IDs).
- [PASS] All ACTIVE rows have EvidenceFile and SourceRef populated.
- [PASS] All enum values are canonical write-form.
- [PASS] FromDeliverableID = DEL-06-04 for all rows.
- [PASS] TargetDeliverableID populated only for TargetType=DELIVERABLE rows (DEP-0604-E005, DEP-0604-E006).
- [PASS] TargetRefID used for non-deliverable targets (SOW-021, OBJ-004, OBJ-006).
- [PASS] Parent anchor count = 1 (DEP-0604-A001). No FLOATING_NODE or AMBIGUOUS_ANCHOR warnings.
- [PASS] _DEPENDENCIES.md counts consistent with Dependencies.csv (9 ACTIVE, 0 RETIRED).

---

## Run History

| Timestamp | Mode | Strictness | DecompositionStatus | Warnings | ACTIVE_ANCHOR | ACTIVE_EXECUTION | ACTIVE_Total |
|---|---|---|---|---|---|---|---|
| 2026-02-21 | UPDATE | CONSERVATIVE | LOADED (G7-APPROVED) | None | 3 | 6 | 9 |
