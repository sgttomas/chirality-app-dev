# Dependencies — DEL-04-01

**Tracking Mode:** FULL_GRAPH
**Status:** EXTRACTED

---

## Declared Upstream Dependencies

*No declared upstream dependencies. See Extracted Dependency Register below.*

## Declared Downstream Dependencies

*No declared downstream dependencies. See Extracted Dependency Register below.*

---

## Extracted Dependency Register

**Register file:** `Dependencies.csv`
**Schema version:** v3.1
**Total rows:** 10
**ACTIVE rows:** 10
**RETIRED rows:** 0

### ANCHOR Rows (5 ACTIVE)

| DependencyID | AnchorType | TargetType | TargetRefID / TargetName | Confidence |
|---|---|---|---|---|
| DEP-04-01-001 | IMPLEMENTS_NODE | PACKAGE | PKG-04 -- Attachments & Multimodal Turns | HIGH |
| DEP-04-01-002 | TRACES_TO_REQUIREMENT | REQUIREMENT | SOW-007: Support turns with multimodal attachments | HIGH |
| DEP-04-01-003 | TRACES_TO_REQUIREMENT | REQUIREMENT | SOW-008: Enforce attachment resolver validation rules | HIGH |
| DEP-04-01-004 | TRACES_TO_REQUIREMENT | REQUIREMENT | SOW-009: Ensure runtime prompt-mode selection behaves correctly | HIGH |
| DEP-04-01-005 | TRACES_TO_REQUIREMENT | REQUIREMENT | OBJ-003: Attachment-enabled turns are robust and UX-safe | HIGH |

### EXECUTION Rows (5 ACTIVE)

| DependencyID | Direction | DependencyType | TargetType | Target | Confidence |
|---|---|---|---|---|---|
| DEP-04-01-006 | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-03-02: Turn Execution API + SSE Streaming | HIGH |
| DEP-04-01-007 | DOWNSTREAM | INTERFACE | DELIVERABLE | DEL-04-02: UI Attachment Pipeline | HIGH |
| DEP-04-01-008 | UPSTREAM | PREREQUISITE | DOCUMENT | docs/SPEC.md Section 9.8 | HIGH |
| DEP-04-01-009 | UPSTREAM | PREREQUISITE | DOCUMENT | docs/harness/chirality_harness_graphs_and_sequence.md | HIGH |
| DEP-04-01-010 | UPSTREAM | PREREQUISITE | EXTERNAL | Anthropic Agent SDK documentation (location TBD) | MEDIUM |

---

## Run Notes

**Run date:** 2026-02-21
**Mode:** UPDATE
**Strictness:** CONSERVATIVE
**Consumer context:** NONE
**Decomposition path:** `execution/_Decomposition/ChiralityApp_SoftwareDecomposition_2026-02-21_G7-APPROVED.md`
**Decomposition status:** Available, validated

### Source Documents Scanned

| Role | File | Notes |
|---|---|---|
| ANCHOR_DOC | Datasheet.md | Primary anchor document; contains identification, scope coverage, objective, and references |
| EXECUTION_DOC | Specification.md | Requirements, excluded scope, standards, cross-deliverable verification |
| EXECUTION_DOC | Guidance.md | Principles, considerations C5/C6/C7 for cross-deliverable interfaces |
| EXECUTION_DOC | Procedure.md | Prerequisites, implementation steps, verification checks |
| CONTEXT | _CONTEXT.md | Deliverable identity and scope confirmation |
| REFERENCES | _REFERENCES.md | Reference pointers (decomposition link only; no deliverable-specific references) |

### Defaults Applied

- SOURCE_DOCS: AUTO -- all .md files in deliverable folder scanned (excluding _DEPENDENCIES.md, _SEMANTIC.md, _SEMANTIC_LENSING.md, _STATUS.md, MEMORY.md)
- DOC_ROLE_MAP: DEFAULT heuristic -- Datasheet.md matched as ANCHOR_DOC; Specification.md, Guidance.md, Procedure.md matched as EXECUTION_DOCs
- ANCHOR_DOC: Datasheet.md (matched by filename pattern "datasheet")
- EXECUTION_DOC_ORDER: Specification.md, Guidance.md, Procedure.md

### Anchor Validation

- Parent anchor (IMPLEMENTS_NODE): PKG-04 confirmed in Decomposition PKG-04 deliverables table (DEL-04-01 row)
- Scope item traces (SOW-007, SOW-008, SOW-009): Confirmed in Decomposition Scope Ledger
- Objective trace (OBJ-003): Confirmed in Decomposition Objectives section and PKG-04 deliverables table

### Warnings

*No warnings.*

### Assumptions

- Anthropic Agent SDK documentation location is TBD; SatisfactionStatus set to PENDING for DEP-04-01-010.

---

## Run History

| Timestamp | Mode | Strictness | Decomposition | Warnings | ACTIVE Count |
|---|---|---|---|---|---|
| 2026-02-21 | UPDATE | CONSERVATIVE | Available (G7-APPROVED) | None | 10 |

---

## Lifecycle Summary

| Status | Count |
|---|---|
| ACTIVE | 10 |
| RETIRED | 0 |

| SatisfactionStatus | Count |
|---|---|
| TBD | 9 |
| PENDING | 1 |

---

## Downstream Handoff Notes

*Consumer context is NONE. No downstream handoff notes generated.*
