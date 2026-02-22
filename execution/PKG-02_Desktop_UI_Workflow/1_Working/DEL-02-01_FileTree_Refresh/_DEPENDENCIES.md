# Dependencies -- DEL-02-01

**Tracking Mode:** FULL_GRAPH
**Status:** EXTRACTED

---

## Declared Upstream Dependencies

- **DEL-03-01** (Working Root Binding & Session Boot) -- FileTree requires projectRoot binding to know which directory to scan. Procedure lists as prerequisite; Guidance notes a stub/mock may suffice for initial development.
- **DEL-05-02** (Execution Root Scaffolding + Layout Conformance) -- FileTree displays the execution root layout structure; the layout definition is an input.

## Declared Downstream Dependencies

- **DEL-02-04** (Multi-pane Layout + Theme Hardening) -- FileTree refresh logic is consumed for visual styling and interaction polish. Specification explicitly excludes styling scope as covered by DEL-02-04.
- **DEL-02-02** (Portal-Pipeline Navigation & Deliverable Key Semantics) -- FileTree refresh may need to signal deliverable-relevant filesystem changes to the shared deliverables state.

---

## Extracted Dependency Register

**Register:** `Dependencies.csv` (v3.1)
**Total rows:** 6
**ACTIVE:** 6
**RETIRED:** 0

| DependencyID | Class | AnchorType | Dir | Type | TargetType | Target | Confidence | Status |
|---|---|---|---|---|---|---|---|---|
| DEP-02-01-001 | ANCHOR | IMPLEMENTS_NODE | UPSTREAM | OTHER | WBS_NODE | SOW-022 | HIGH | ACTIVE |
| DEP-02-01-002 | ANCHOR | TRACES_TO_REQUIREMENT | UPSTREAM | OTHER | REQUIREMENT | OBJ-005 | HIGH | ACTIVE |
| DEP-02-01-003 | EXECUTION | NOT_APPLICABLE | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-03-01 | HIGH | ACTIVE |
| DEP-02-01-004 | EXECUTION | NOT_APPLICABLE | DOWNSTREAM | HANDOVER | DELIVERABLE | DEL-02-04 | HIGH | ACTIVE |
| DEP-02-01-005 | EXECUTION | NOT_APPLICABLE | DOWNSTREAM | INTERFACE | DELIVERABLE | DEL-02-02 | MEDIUM | ACTIVE |
| DEP-02-01-006 | EXECUTION | NOT_APPLICABLE | UPSTREAM | INTERFACE | DELIVERABLE | DEL-05-02 | MEDIUM | ACTIVE |

---

## Lifecycle Summary

| Lifecycle State | Count |
|---|---|
| ACTIVE | 6 |
| RETIRED | 0 |

| SatisfactionStatus | Count |
|---|---|
| TBD | 6 |

### By DependencyClass

| Class | ACTIVE | RETIRED |
|---|---|---|
| ANCHOR | 2 | 0 |
| EXECUTION | 4 | 0 |

---

## Run Notes

**Run date:** 2026-02-21
**Mode:** UPDATE
**Strictness:** CONSERVATIVE
**Consumer context:** NONE
**Decomposition path:** `execution/_Decomposition/ChiralityApp_SoftwareDecomposition_2026-02-21_G7-APPROVED.md`
**Decomposition status:** Available and validated (G7-APPROVED)

### Defaults used

- **SOURCE_DOCS:** AUTO -- scanned deliverable folder; found: Datasheet.md, Specification.md, Guidance.md, Procedure.md, _CONTEXT.md, _REFERENCES.md
- **DOC_ROLE_MAP:** DEFAULT heuristic
- **ANCHOR_DOC:** Datasheet.md (selected as highest-confidence anchor document per role heuristic)
- **EXECUTION_DOC_ORDER:** Procedure.md, Specification.md, Guidance.md (ordered by workflow clarity)

### Extraction notes

**Pass 1 (ANCHOR):**
- Parent anchor (IMPLEMENTS_NODE) found: SOW-022 -- explicitly stated in Datasheet Identification > Scope Coverage. Confirmed in decomposition Scope Ledger.
- Objective trace (TRACES_TO_REQUIREMENT) found: OBJ-005 -- explicitly stated in Datasheet Identification > Objective Association. Confirmed in decomposition deliverables table.

**Pass 2 (EXECUTION):**
- DEL-03-01 PREREQUISITE (UPSTREAM): Explicitly listed in Procedure Prerequisites table as "projectRoot binding." Guidance "Prerequisite Sequencing Rationale" elaborates that a stub/mock may suffice, but the dependency relationship itself is explicit.
- DEL-02-04 HANDOVER (DOWNSTREAM): Specification Excluded section explicitly names DEL-02-04 as the destination for FileTree visual styling and polish scope.
- DEL-02-02 INTERFACE (DOWNSTREAM): Guidance C5 explicitly discusses the interface between FileTree refresh and shared deliverables state (SOW-024/DEL-02-02). Confidence MEDIUM because the interface is described as a consideration, not a hard requirement.
- DEL-05-02 INTERFACE (UPSTREAM): Specification Standards table states "SPEC SS 1 (Execution Root Layout) -- FileTree displays this structure." Datasheet REF-03 confirms. Confidence MEDIUM because the dependency is on a layout definition rather than a blocking artifact transfer.

### Edges NOT extracted (with rationale)

- Governance documents (DIRECTIVE, PLAN, SPEC, CONTRACT): Referenced extensively as normative sources but do not represent information-flow dependencies requiring specific artifact transfer between deliverables. These are standards/constraints, not edge-forming couplings.
- UI_POLISH_EXECUTION_PLAN: Referenced for component lists and polish scope but the specific handover is already captured via DEL-02-04.
- FilePreview / SystemFileTree components: Mentioned as related components but the Specification explicitly excludes file content preview as a separate concern; no information flow identified.

### Warnings

*No warnings.*

### Quality checks

- [PASS] Parent anchor (IMPLEMENTS_NODE) count = 1 (SOW-022)
- [PASS] All ACTIVE rows have EvidenceFile and SourceRef
- [PASS] DependencyID values are unique
- [PASS] Required columns present; CSV parseable
- [PASS] Enum values are canonical write-form
- [PASS] FromDeliverableID = DEL-02-01 for all rows
- [PASS] TargetDeliverableID populated only for TargetType=DELIVERABLE rows
- [PASS] TargetRefID populated only for non-deliverable targets
- [PASS] Summary counts consistent with CSV

---

## Run History

| Run | Date | Mode | Strictness | Decomposition | Warnings | ACTIVE Count |
|---|---|---|---|---|---|---|
| 1 | 2026-02-21 | UPDATE | CONSERVATIVE | Available (G7-APPROVED) | None | 6 |
