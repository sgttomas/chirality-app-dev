# Dependencies -- DEL-08-07

**Tracking Mode:** FULL_GRAPH
**Status:** EXTRACTED

---

## Declared Upstream Dependencies

*No declared (human-authored) upstream dependencies recorded yet.*

## Declared Downstream Dependencies

*No declared (human-authored) downstream dependencies recorded yet.*

---

## Extracted Dependency Register

**Source:** `Dependencies.csv` (RegisterSchemaVersion v3.1)
**Total Rows:** 15
**ACTIVE:** 15 | **RETIRED:** 0

### ANCHOR Rows (9 ACTIVE)

| DependencyID | AnchorType | TargetType | TargetRefID/TargetName | Confidence |
|---|---|---|---|---|
| DEP-08-07-001 | IMPLEMENTS_NODE | WBS_NODE | SOW-038 | HIGH |
| DEP-08-07-002 | IMPLEMENTS_NODE | WBS_NODE | OBJ-007 | HIGH |
| DEP-08-07-003 | TRACES_TO_REQUIREMENT | REQUIREMENT | K-STALE-1 | HIGH |
| DEP-08-07-004 | TRACES_TO_REQUIREMENT | REQUIREMENT | K-STALE-2 | HIGH |
| DEP-08-07-005 | TRACES_TO_REQUIREMENT | REQUIREMENT | K-VAL-1 | HIGH |
| DEP-08-07-006 | TRACES_TO_REQUIREMENT | REQUIREMENT | K-DEP-1 | HIGH |
| DEP-08-07-007 | TRACES_TO_REQUIREMENT | REQUIREMENT | K-GHOST-1 | HIGH |
| DEP-08-07-008 | TRACES_TO_REQUIREMENT | REQUIREMENT | K-AUTH-1 | HIGH |
| DEP-08-07-009 | TRACES_TO_REQUIREMENT | REQUIREMENT | K-SNAP-1 | HIGH |

### EXECUTION Rows (6 ACTIVE)

| DependencyID | Direction | DependencyType | TargetType | Target | Confidence |
|---|---|---|---|---|---|
| DEP-08-07-010 | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-08-04 (On-demand Dependency Graph Generator) | HIGH |
| DEP-08-07-011 | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-08-06 (Unified Pipeline Run Record Persistence) | HIGH |
| DEP-08-07-012 | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-05-04 (Dependency Tracking File Contract v3.1) | HIGH |
| DEP-08-07-013 | UPSTREAM | CONSTRAINT | DOCUMENT | docs/CONTRACT.md | HIGH |
| DEP-08-07-014 | UPSTREAM | INTERFACE | DOCUMENT | docs/SPEC.md Section 6 | HIGH |
| DEP-08-07-015 | UPSTREAM | CONSTRAINT | DOCUMENT | docs/DIRECTIVE.md | HIGH |

---

## Run Notes

**Run Date:** 2026-02-21
**Mode:** UPDATE
**Strictness:** CONSERVATIVE
**Consumer Context:** NONE

### Defaults and Paths Used

- **RUN_ROOT:** `/Users/ryan/ai-env/projects/chirality-app-dev1/execution/`
- **DECOMPOSITION_PATH:** `/Users/ryan/ai-env/projects/chirality-app-dev1/execution/_Decomposition/ChiralityApp_SoftwareDecomposition_2026-02-21_G7-APPROVED.md`
- **DECOMP_VARIANT:** SOFTWARE
- **SOURCE_DOCS (AUTO):** Datasheet.md, Specification.md, Guidance.md, Procedure.md, _CONTEXT.md, _REFERENCES.md
- **ANCHOR_DOC (AUTO):** Datasheet.md (selected: contains Identification table with Scope Item, Objective, and definition-node references)
- **EXECUTION_DOC_ORDER (AUTO):** Specification.md, Procedure.md, Guidance.md, Datasheet.md, _CONTEXT.md

### Warnings

- [WARNING] AMBIGUOUS_ANCHOR: Two IMPLEMENTS_NODE rows emitted (DEP-08-07-001 for SOW-038 and DEP-08-07-002 for OBJ-007). Both are explicitly stated in the Datasheet Identification table. SOW-038 is the scope item; OBJ-007 is the supporting objective. Downstream consumers should treat SOW-038 as the primary scope anchor.

### Assumptions Recorded

- ASSUMPTION (DEP-08-07-010): DEL-08-04 output format is TBD; graph artifact format not yet defined. Noted in Datasheet "Upstream Format Dependency" condition.
- ASSUMPTION (DEP-08-07-011): DEL-08-06 run record schema is TBD; schema not yet defined. Noted in Datasheet "Upstream Format Dependency" condition.
- ASSUMPTION (DEP-08-07-012): DEL-05-04 is listed as a technical prerequisite in Procedure.md; SOW-018 is IN scope, so this dependency should be satisfiable.

### Extraction Notes

- Pass 1 (ANCHOR): Extracted 1 scope-item anchor (SOW-038), 1 objective anchor (OBJ-007), and 7 requirement trace anchors (K-STALE-1, K-STALE-2, K-VAL-1, K-DEP-1, K-GHOST-1, K-AUTH-1, K-SNAP-1). All anchors are confirmed present in the decomposition and/or source governance documents.
- Pass 2 (EXECUTION): Extracted 3 deliverable prerequisites (DEL-08-04, DEL-08-06, DEL-05-04) and 3 document constraints/interfaces (CONTRACT.md, SPEC.md, DIRECTIVE.md). All are explicit in source documents.
- No DOWNSTREAM execution edges were extracted. Source documents describe DEL-08-07 as a terminal consumer in the integrity hardening chain; no explicit downstream artifact handoffs to other deliverables are stated.
- docs/PLAN.md was considered as a potential DOCUMENT dependency but not extracted as a separate row because its content is informational/rationale context rather than a specific input/constraint consumed by the deliverable's implementation. The relevant PLAN content (sequencing, effort) is already captured via the deliverable prerequisites and the decomposition anchors.
- docs/TYPES.md Section 3 was referenced in the Datasheet but not extracted as a separate row because it provides vocabulary definitions rather than an artifact/interface consumed by implementation. The relevant vocabulary (edge classes, directions) is embedded in the v3.1 schema (already captured via DEP-08-07-014).

---

## Run History

| Timestamp | Mode | Strictness | Decomposition | Warnings | ACTIVE Count |
|---|---|---|---|---|---|
| 2026-02-21 | UPDATE | CONSERVATIVE | G7-APPROVED (located) | AMBIGUOUS_ANCHOR (2 IMPLEMENTS_NODE rows) | 15 |

---

## Lifecycle Summary

| Category | Count |
|---|---|
| **ACTIVE** | 15 |
| **RETIRED** | 0 |
| **Total** | 15 |

### By DependencyClass

| Class | ACTIVE | RETIRED |
|---|---|---|
| ANCHOR | 9 | 0 |
| EXECUTION | 6 | 0 |

### Closure Status Breakdown (ACTIVE rows)

| SatisfactionStatus | Count |
|---|---|
| TBD | 9 |
| PENDING | 3 |
| NOT_APPLICABLE | 3 |

*Note: TBD rows are the 9 ANCHOR rows (scope/objective/requirement traces) whose satisfaction tracking is not yet established. PENDING rows are the 3 DELIVERABLE prerequisites (DEL-08-04, DEL-08-06, DEL-05-04) whose upstream deliverables exist in the decomposition but are not yet implemented. NOT_APPLICABLE rows are the 3 DOCUMENT constraints/interfaces that do not require "satisfaction" in the closure sense -- the documents exist and are accessible.*
