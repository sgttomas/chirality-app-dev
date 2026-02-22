# Dependencies -- DEL-08-02

**Tracking Mode:** FULL_GRAPH
**Status:** EXTRACTED
**Register Schema:** v3.1

---

## Declared Upstream Dependencies

*No manually declared upstream dependencies. See Extracted Dependency Register below.*

## Declared Downstream Dependencies

*No manually declared downstream dependencies.*

---

## Extracted Dependency Register

**Total rows:** 9
**ACTIVE:** 9 | **RETIRED:** 0
**ANCHOR:** 2 | **EXECUTION:** 7

| DependencyID | Class | AnchorType | Direction | Type | TargetType | Target | Confidence | Status |
|---|---|---|---|---|---|---|---|---|
| DEP-08-02-001 | ANCHOR | IMPLEMENTS_NODE | UPSTREAM | OTHER | WBS_NODE | SOW-033 | HIGH | ACTIVE |
| DEP-08-02-002 | ANCHOR | TRACES_TO_REQUIREMENT | UPSTREAM | OTHER | REQUIREMENT | OBJ-007 | HIGH | ACTIVE |
| DEP-08-02-003 | EXECUTION | NOT_APPLICABLE | UPSTREAM | CONSTRAINT | REQUIREMENT | SOW-033 Scope Decision (OI-033) | HIGH | ACTIVE |
| DEP-08-02-004 | EXECUTION | NOT_APPLICABLE | UPSTREAM | PREREQUISITE | DOCUMENT | docs/SPEC.md Section 6 | HIGH | ACTIVE |
| DEP-08-02-005 | EXECUTION | NOT_APPLICABLE | UPSTREAM | PREREQUISITE | DOCUMENT | docs/CONTRACT.md | HIGH | ACTIVE |
| DEP-08-02-006 | EXECUTION | NOT_APPLICABLE | UPSTREAM | PREREQUISITE | DOCUMENT | docs/TYPES.md Section 3 | HIGH | ACTIVE |
| DEP-08-02-007 | EXECUTION | NOT_APPLICABLE | UPSTREAM | INTERFACE | DELIVERABLE | DEL-05-04 (Dependency Tracking File Contract) | HIGH | ACTIVE |
| DEP-08-02-008 | EXECUTION | NOT_APPLICABLE | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-07-02 (Example Execution Roots) | MEDIUM | ACTIVE |
| DEP-08-02-009 | EXECUTION | NOT_APPLICABLE | UPSTREAM | PREREQUISITE | DOCUMENT | docs/PLAN.md Section 3.2 | MEDIUM | ACTIVE |

---

## Run Notes

**Run date:** 2026-02-21
**Mode:** UPDATE
**Strictness:** CONSERVATIVE
**Consumer context:** NONE
**Decomposition path:** `/Users/ryan/ai-env/projects/chirality-app-dev/execution/_Decomposition/ChiralityApp_SoftwareDecomposition_2026-02-21_G7-APPROVED.md`
**Decomposition status:** AVAILABLE (G7-APPROVED)

**Source documents scanned:**
- `Datasheet.md` (ANCHOR_DOC -- primary anchor signals)
- `Specification.md` (EXECUTION_DOC -- requirements and standards)
- `Guidance.md` (EXECUTION_DOC -- considerations, trade-offs, relationships)
- `Procedure.md` (EXECUTION_DOC -- prerequisites, steps, integration)
- `_CONTEXT.md` (supporting context)
- `_REFERENCES.md` (reference resolution)

**Defaults applied:**
- ANCHOR_DOC: `Datasheet.md` (selected by heuristic: contains "datasheet" in filename)
- EXECUTION_DOC_ORDER: `Procedure.md`, `Guidance.md`, `Specification.md` (procedure first for prerequisite signals, guidance for relationship signals, specification for standards)
- SOURCE_DOCS: AUTO (all .md files in deliverable folder excluding dependency artifacts and generated files)

**Extraction decisions:**
- DEL-08-03 (Guidance C4): NOT extracted. Guidance states "there may be an opportunity to share CLI infrastructure... but this is not required." This is coordination/structural adjacency, not information flow. Per protocol, coordination-only relationships are excluded.
- DEL-08-04 (Specification exclusion boundary): NOT extracted. Specification excludes graph generation as DEL-08-04 scope. While DEL-08-04 could consume validated output, no explicit information transfer is stated from DEL-08-02 to DEL-08-04. Conservative: do not invent downstream edges.
- docs/PLAN.md Section 3.2 (DEP-08-02-009): Extracted as PREREQUISITE with MEDIUM confidence. Provides directional guidance (implementation language, scope framing) but is not a hard gate.
- DEL-07-02 / examples/ (DEP-08-02-008): Extracted as PREREQUISITE with MEDIUM confidence. Required for integration testing (PRE-04, Step D2) but not a hard gate for initial implementation.

**Warnings:** None.

---

## Run History

| Run | Date | Mode | Strictness | Decomp Status | Warnings | ANCHOR (Active) | EXECUTION (Active) | Total (Active) |
|---|---|---|---|---|---|---|---|---|
| 1 | 2026-02-21 | UPDATE | CONSERVATIVE | AVAILABLE (G7-APPROVED) | None | 2 | 7 | 9 |

---

## Lifecycle Summary

**Extraction lifecycle:**
- ACTIVE: 9
- RETIRED: 0

**Closure lifecycle (SatisfactionStatus):**
- TBD: 8
- PENDING: 1 (DEP-08-02-003 -- SOW-033 scope decision is an explicit pending gate)

**Tree x DAG integrity:**
- Parent anchor (IMPLEMENTS_NODE): 1 (SOW-033) -- OK
- Trace anchors (TRACES_TO_REQUIREMENT): 1 (OBJ-007) -- OK
- No warnings (FLOATING_NODE or AMBIGUOUS_ANCHOR)
