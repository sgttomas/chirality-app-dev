# Dependencies -- DEL-08-04

**Tracking Mode:** FULL_GRAPH
**Status:** EXTRACTED
**RegisterSchemaVersion:** v3.1

---

## Declared Upstream Dependencies

*No manually declared upstream dependencies at this time. All upstream edges are extraction-derived.*

## Declared Downstream Dependencies

*No manually declared downstream dependencies at this time. All downstream edges are extraction-derived.*

---

## Extracted Dependency Register

**Total ACTIVE rows:** 13
**Total RETIRED rows:** 0

### ANCHOR Edges (2 ACTIVE)

| DependencyID | AnchorType | TargetType | TargetRefID | TargetName | Confidence |
|---|---|---|---|---|---|
| DEP-08-04-001 | IMPLEMENTS_NODE | WBS_NODE | SOW-035 | SOW-035 | HIGH |
| DEP-08-04-002 | TRACES_TO_REQUIREMENT | REQUIREMENT | OBJ-007 | OBJ-007 | HIGH |

### EXECUTION Edges -- UPSTREAM (10 ACTIVE)

| DependencyID | DependencyType | TargetType | TargetID / Name | Confidence | Explicitness |
|---|---|---|---|---|---|
| DEP-08-04-003 | PREREQUISITE | DOCUMENT | docs/SPEC.md Section 6 (Dependencies.csv v3.1 schema) | HIGH | EXPLICIT |
| DEP-08-04-004 | PREREQUISITE | DOCUMENT | docs/SPEC.md Sections 1-2 (Execution root layout) | HIGH | EXPLICIT |
| DEP-08-04-005 | PREREQUISITE | DOCUMENT | docs/TYPES.md Section 3 (Dependency vocabulary) | HIGH | EXPLICIT |
| DEP-08-04-006 | CONSTRAINT | DOCUMENT | docs/CONTRACT.md K-DEP-1 and K-DEP-2 | HIGH | EXPLICIT |
| DEP-08-04-007 | INTERFACE | DELIVERABLE | All deliverable-local Dependencies.csv registers | HIGH | EXPLICIT |
| DEP-08-04-009 | CONSTRAINT | WBS_NODE | SOW-035 scope flip to IN | HIGH | EXPLICIT |
| DEP-08-04-010 | INTERFACE | DELIVERABLE | DEL-08-02 (Dependencies.csv v3.1 Schema Linter) | LOW | IMPLICIT |
| DEP-08-04-011 | INTERFACE | DELIVERABLE | DEL-08-03 (Execution Root Folder Structure Validator) | LOW | IMPLICIT |
| DEP-08-04-012 | INTERFACE | DELIVERABLE | DEL-05-04 (Dependency Tracking File Contract v3.1) | MEDIUM | EXPLICIT |
| DEP-08-04-013 | PREREQUISITE | DOCUMENT | docs/PLAN.md Section 3.4 (Feature description) | HIGH | EXPLICIT |

### EXECUTION Edges -- DOWNSTREAM (1 ACTIVE)

| DependencyID | DependencyType | TargetType | TargetID / Name | Confidence | Explicitness |
|---|---|---|---|---|---|
| DEP-08-04-008 | HANDOVER | DELIVERABLE | DEL-08-07 (Staleness Propagation + Triage Tooling) | HIGH | EXPLICIT |

---

## Lifecycle Summary

| Category | Count |
|---|---|
| ACTIVE (all classes) | 13 |
| RETIRED | 0 |
| ANCHOR rows | 2 |
| EXECUTION rows | 11 |
| UPSTREAM edges | 12 |
| DOWNSTREAM edges | 1 |

### Satisfaction Status Breakdown (ACTIVE rows)

| SatisfactionStatus | Count |
|---|---|
| TBD | 12 |
| PENDING | 1 |

Note: DEP-08-04-009 (SOW-035 scope flip) is marked PENDING because SOW-035 is currently TBD per the decomposition Scope Ledger and has not yet been flipped to IN.

---

## Run Notes

### Run 2026-02-21 (Initial Extraction)

**Configuration:**
- MODE: UPDATE
- STRICTNESS: CONSERVATIVE
- CONSUMER_CONTEXT: NONE
- DECOMPOSITION_PATH: `execution/_Decomposition/ChiralityApp_SoftwareDecomposition_2026-02-21_G7-APPROVED.md` (located and read successfully)
- DECOMP_VARIANT: SOFTWARE

**Source Documents Scanned (AUTO):**
- ANCHOR_DOC: Datasheet.md (identification table with scope/objective refs)
- EXECUTION_DOC_ORDER: Specification.md, Procedure.md, Guidance.md, _CONTEXT.md
- Additional: _REFERENCES.md (no deliverable-specific references found)

**Defaults Applied:**
- SOURCE_DOCS: AUTO -- scanned all .md files in deliverable folder
- ANCHOR_DOC: AUTO -- selected Datasheet.md (contains identification table)
- EXECUTION_DOC_ORDER: AUTO -- Specification.md first (richest requirement signal), then Procedure.md, Guidance.md, _CONTEXT.md

**Decomposition Validation:**
- SOW-035 confirmed in Scope Ledger: TBD status, maps to PKG-08 / DEL-08-04 / OBJ-007
- OBJ-007 confirmed in Objectives: "Optional: integrity hardening loop (TBD scope)"
- DEL-08-04 confirmed in Deliverables table: PKG-08, type BACKEND_FEATURE_SLICE, context envelope M
- DEL-08-07 confirmed as downstream consumer in decomposition (PKG-08, SOW-038, OBJ-007)
- DEL-08-02 confirmed in decomposition (PKG-08, SOW-033, OBJ-007)
- DEL-08-03 confirmed in decomposition (PKG-08, SOW-034, OBJ-007)
- DEL-05-04 confirmed in decomposition (PKG-05, SOW-018, OBJ-004)

**Warnings:**
- None.

**Assumptions Recorded:**
- DEP-08-04-010: DEL-08-02 relationship is undecided per Datasheet; recorded as IMPLICIT / LOW confidence
- DEP-08-04-011: DEL-08-03 relationship is undecided per Datasheet; recorded as IMPLICIT / LOW confidence

**Quality Check Results:**
- Schema check: PASS (all required columns present, CSV parseable)
- DependencyID uniqueness: PASS (13 unique IDs)
- Evidence check: PASS (all ACTIVE rows have EvidenceFile + SourceRef)
- Parent anchor check: PASS (exactly 1 IMPLEMENTS_NODE row: DEP-08-04-001)
- Duplicate check: PASS (no obvious duplicates)
- Enum normalization: PASS (all values are canonical write-form)
- _DEPENDENCIES.md consistency: PASS (counts match CSV)

---

## Run History

| Timestamp | Mode | Strictness | Consumer | Decomposition | Warnings | ACTIVE Count |
|---|---|---|---|---|---|---|
| 2026-02-21 | UPDATE | CONSERVATIVE | NONE | G7-APPROVED (located) | None | 13 |
