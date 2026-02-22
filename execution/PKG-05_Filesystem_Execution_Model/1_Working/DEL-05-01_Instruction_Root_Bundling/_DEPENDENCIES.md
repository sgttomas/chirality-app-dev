# Dependencies -- DEL-05-01

**Tracking Mode:** FULL_GRAPH
**Status:** EXTRACTED
**Register:** `Dependencies.csv` (v3.1 schema)

---

## Declared Upstream Dependencies

*No human-declared upstream dependencies yet. See extracted register below.*

## Declared Downstream Dependencies

*No human-declared downstream dependencies yet. See extracted register below.*

---

## Extracted Dependency Register

**Total ACTIVE rows:** 11
**Total RETIRED rows:** 0

### ANCHOR edges (3 ACTIVE)

| DependencyID | AnchorType | TargetType | TargetRefID | TargetName | Confidence |
|---|---|---|---|---|---|
| DEP-05-01-001 | IMPLEMENTS_NODE | WBS_NODE | DEL-05-01 | DEL-05-01 (Decomposition Node) | HIGH |
| DEP-05-01-002 | TRACES_TO_REQUIREMENT | REQUIREMENT | SOW-013 | SOW-013: Maintain separation of Instruction Root vs Working Root | HIGH |
| DEP-05-01-003 | TRACES_TO_REQUIREMENT | REQUIREMENT | OBJ-004 | OBJ-004: Filesystem-as-state execution model is SPEC-conformant and auditable | HIGH |

### EXECUTION edges -- UPSTREAM (3 ACTIVE)

| DependencyID | DependencyType | TargetDeliverableID | TargetName | Confidence |
|---|---|---|---|---|
| DEP-05-01-004 | PREREQUISITE | DEL-01-01 | macOS 15+ Apple Silicon Build Baseline | HIGH |
| DEP-05-01-005 | PREREQUISITE | DEL-01-02 | Unsigned DMG Packaging Workflow | HIGH |
| DEP-05-01-006 | PREREQUISITE | DEL-03-01 | Working Root Binding & Session Boot | HIGH |

### EXECUTION edges -- DOWNSTREAM (5 ACTIVE)

| DependencyID | DependencyType | TargetDeliverableID | TargetName | Confidence |
|---|---|---|---|---|
| DEP-05-01-007 | INTERFACE | DEL-05-02 | Execution Root Scaffolding + Layout Conformance | MEDIUM |
| DEP-05-01-008 | INTERFACE | DEL-05-03 | Lifecycle State Handling (_STATUS.md canonical) | MEDIUM |
| DEP-05-01-009 | INTERFACE | DEL-05-04 | Dependency Tracking File Contract (v3.1) | MEDIUM |
| DEP-05-01-010 | ENABLES | DEL-08-01 | _REFERENCES.md Content Hashes + Verification | LOW |
| DEP-05-01-011 | INTERFACE | DEL-01-02 | Unsigned DMG Packaging Workflow | MEDIUM |

---

## Run Notes

**Run date:** 2026-02-21
**Mode:** UPDATE
**Strictness:** CONSERVATIVE
**Consumer context:** NONE
**Decomposition path:** `execution/_Decomposition/ChiralityApp_SoftwareDecomposition_2026-02-21_G7-APPROVED.md`
**Decomposition status:** AVAILABLE (G7-APPROVED)
**Decomposition variant:** SOFTWARE

**Source documents scanned (AUTO):**
- `Datasheet.md` (ANCHOR_DOC -- primary anchor source)
- `Specification.md` (EXECUTION_DOC -- scope boundaries, requirements)
- `Guidance.md` (EXECUTION_DOC -- considerations, trade-offs)
- `Procedure.md` (EXECUTION_DOC -- prerequisites, steps)
- `_CONTEXT.md` (supplementary -- deliverable identity/context)
- `_REFERENCES.md` (supplementary -- reference pointers)

**ANCHOR_DOC:** `Datasheet.md` (selected: contains Identification table with Package, Scope Coverage, Supports Objectives)
**EXECUTION_DOC_ORDER:** `Procedure.md`, `Specification.md`, `Guidance.md`

**Defaults applied:**
- SOURCE_DOCS=AUTO: all source documents in deliverable folder scanned
- ANCHOR_DOC=AUTO: Datasheet.md selected as primary anchor source
- EXECUTION_DOC_ORDER=AUTO: Procedure.md first (explicit prerequisites table), then Specification.md (scope exclusions), then Guidance.md (considerations with cross-references)

**Extraction decisions:**
- ANCHOR rows: 1 parent anchor (IMPLEMENTS_NODE to DEL-05-01 decomposition node) + 2 trace anchors (SOW-013, OBJ-004). All confirmed against decomposition G7-APPROVED.
- EXECUTION UPSTREAM rows: 3 prerequisites extracted from Procedure.md Prerequisites table (DEL-01-01, DEL-01-02, DEL-03-01). All explicitly stated with ASSUMPTION tags in source noting they are expected prerequisites pending dependency extraction. Hard vs. soft classification is TBD.
- EXECUTION DOWNSTREAM rows: 4 interface/enables edges. Three PKG-05 sibling interfaces from Specification Excluded section (DEL-05-02, DEL-05-03, DEL-05-04). One ENABLES edge to DEL-08-01 from Guidance C3. One downstream INTERFACE to DEL-01-02 from Specification Excluded section (.dmg packaging mechanics).
- Governance document references (DIRECTIVE, CONTRACT, SPEC, PLAN) were NOT extracted as dependency rows. These are ambient standards applied to all deliverables, not specific information-flow edges. The source documents reference them as design principles and constraints but do not state that specific artifacts must be received from those documents as prerequisites.
- DEL-01-02 appears twice: once as UPSTREAM PREREQUISITE (Procedure: packaging path must be available) and once as DOWNSTREAM INTERFACE (Specification: packaging mechanics scope boundary). These are distinct relationships with different evidence and semantics.
- DEL-03-01 is listed in both Specification Excluded and Procedure Prerequisites. Extracted only the UPSTREAM PREREQUISITE (Procedure) because the Specification exclusion ("Session boot and projectRoot binding API covered by DEL-03-01") is a scope boundary statement, while the Procedure explicitly states it as a prerequisite for runtime testing.

**Warnings:** None.

---

## Run History

| Run | Date | Mode | Strictness | Decomposition | Warnings | ACTIVE Count |
|---|---|---|---|---|---|---|
| 1 | 2026-02-21 | UPDATE | CONSERVATIVE | G7-APPROVED (available) | None | 11 |

---

## Lifecycle Summary

| Category | Count |
|---|---|
| **ACTIVE (total)** | 11 |
| ANCHOR | 3 |
| EXECUTION UPSTREAM | 3 |
| EXECUTION DOWNSTREAM | 5 |
| **RETIRED** | 0 |

### Closure state breakdown (ACTIVE rows)

| SatisfactionStatus | Count |
|---|---|
| TBD | 11 |

---

## Integrity Check Results

| Check | Result |
|---|---|
| Schema columns present | PASS |
| DependencyID uniqueness | PASS |
| ACTIVE rows have EvidenceFile + SourceRef | PASS |
| Enum values canonical | PASS |
| Parent anchor (IMPLEMENTS_NODE) count = 1 | PASS |
| FromDeliverableID consistency (all = DEL-05-01) | PASS |
| TargetDeliverableID/TargetRefID placement | PASS |
| No duplicate extracted rows | PASS |
