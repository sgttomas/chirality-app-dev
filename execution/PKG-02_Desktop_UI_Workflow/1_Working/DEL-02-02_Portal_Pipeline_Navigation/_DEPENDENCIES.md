# Dependencies -- DEL-02-02

**Tracking Mode:** FULL_GRAPH
**Status:** EXTRACTED

---

## Declared Upstream Dependencies

*No upstream dependencies have been formally declared by a human for this deliverable.*

## Declared Downstream Dependencies

*No downstream dependencies have been formally declared by a human for this deliverable.*

---

## Extracted Dependency Register

**Register file:** `Dependencies.csv` (v3.1 schema)
**Total rows:** 10
**ACTIVE:** 10 | **RETIRED:** 0

### ANCHOR Edges (3 ACTIVE)

| DependencyID | AnchorType | TargetType | TargetRefID / TargetName | Confidence |
|---|---|---|---|---|
| DEP-02-02-001 | IMPLEMENTS_NODE | WBS_NODE | OBJ-005 -- Desktop UI supports intended operator workflow | HIGH |
| DEP-02-02-002 | TRACES_TO_REQUIREMENT | REQUIREMENT | SOW-023 -- Portal-to-Pipeline navigation for deliverable-scoped TASK* variants | HIGH |
| DEP-02-02-003 | TRACES_TO_REQUIREMENT | REQUIREMENT | SOW-024 -- Shared deliverables state across PORTAL and PIPELINE | HIGH |

### EXECUTION Edges (7 ACTIVE)

| DependencyID | Direction | DependencyType | TargetType | Target | Confidence |
|---|---|---|---|---|---|
| DEP-02-02-004 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-02-01 (FileTree Refresh & External-Change Detection) | HIGH |
| DEP-02-02-005 | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-01-01 (macOS 15+ Apple Silicon Build Baseline) | LOW |
| DEP-02-02-006 | UPSTREAM | PREREQUISITE | UNKNOWN | /api/project/deliverables endpoint implementation | MEDIUM |
| DEP-02-02-007 | UPSTREAM | CONSTRAINT | DOCUMENT | docs/SPEC.md Section 14 -- UI Navigation and Selector Contract | HIGH |
| DEP-02-02-008 | UPSTREAM | CONSTRAINT | DOCUMENT | docs/SPEC.md Section 15 -- Deliverables API Response Contract | HIGH |
| DEP-02-02-009 | UPSTREAM | CONSTRAINT | DOCUMENT | docs/TYPES.md Section 9 -- UI Navigation Vocabulary | HIGH |
| DEP-02-02-010 | UPSTREAM | CONSTRAINT | DOCUMENT | docs/DIRECTIVE.md Section 2.1 -- Filesystem-as-state constraint | HIGH |

---

## Lifecycle Summary

| Status | Count |
|---|---|
| ACTIVE | 10 |
| RETIRED | 0 |

| SatisfactionStatus | Count |
|---|---|
| TBD | 10 |

---

## Run Notes

**Run date:** 2026-02-21
**Mode:** UPDATE
**Strictness:** CONSERVATIVE
**Consumer context:** NONE
**Decomposition path:** `execution/_Decomposition/ChiralityApp_SoftwareDecomposition_2026-02-21_G7-APPROVED.md`
**Decomposition status:** AVAILABLE (G7-APPROVED)

**Defaults applied:**
- SOURCE_DOCS: AUTO -- scanned Datasheet.md, Specification.md, Guidance.md, Procedure.md, _CONTEXT.md, _REFERENCES.md
- ANCHOR_DOC: Datasheet.md (matched `datasheet` heuristic; confirmed as primary anchor source with explicit SOW/OBJ identifiers)
- EXECUTION_DOC_ORDER: Specification.md, Guidance.md, Procedure.md (matched execution doc heuristics)
- DOC_ROLE_MAP: DEFAULT heuristics applied

**Anchor validation:** All anchor targets (OBJ-005, SOW-023, SOW-024) confirmed present in decomposition document.

**Warnings:**
- None.

**Observations:**
- DEP-02-02-005 (DEL-01-01 prerequisite): Marked IMPLICIT/LOW confidence. Source text explicitly states this is an ASSUMPTION. Recommend human review to decide whether to formalize or retire.
- DEP-02-02-006 (/api/project/deliverables endpoint): TargetType=UNKNOWN because the owning deliverable has not been identified in available sources. Procedure P7 and Datasheet Conditions both flag this as TBD. PROPOSAL: likely owned by a PKG-03 or PKG-05 deliverable; resolution requires cross-deliverable analysis.
- No DOWNSTREAM execution edges were extracted. All information flow runs into this deliverable. Guidance C4 notes DEL-02-03 and DEL-02-04 are orthogonal (no direct dependency). The state transfer mechanism choice (Guidance C1) may create a de facto downstream constraint for PKG-02 siblings, but this is not yet established as a concrete information flow edge.

---

## Run History

| Run | Date | Mode | Strictness | Decomposition | Warnings | ACTIVE Count |
|---|---|---|---|---|---|---|
| 1 | 2026-02-21 | UPDATE | CONSERVATIVE | G7-APPROVED (available) | None | 10 |

---

## Downstream Handoff Notes

*Not applicable (CONSUMER_CONTEXT=NONE).*
