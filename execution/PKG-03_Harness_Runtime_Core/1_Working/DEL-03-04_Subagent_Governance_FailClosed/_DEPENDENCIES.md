# Dependencies -- DEL-03-04

**Tracking Mode:** FULL_GRAPH
**Status:** EXTRACTED

---

## Declared Upstream Dependencies

*No declared (human-authored) upstream dependencies. All entries below are extracted.*

## Declared Downstream Dependencies

*No declared (human-authored) downstream dependencies. All entries below are extracted.*

---

## Extracted Dependency Register

**Register file:** `Dependencies.csv`
**Schema version:** v3.1
**Total ACTIVE rows:** 15
**Total RETIRED rows:** 0

### ANCHOR rows (6 ACTIVE)

| DependencyID | AnchorType | TargetType | TargetRefID | TargetName | Confidence |
|---|---|---|---|---|---|
| DEP-03-04-001 | IMPLEMENTS_NODE | WBS_NODE | SOW-012 | SOW-012 | HIGH |
| DEP-03-04-002 | TRACES_TO_REQUIREMENT | REQUIREMENT | OBJ-002 | OBJ-002 | HIGH |
| DEP-03-04-003 | TRACES_TO_REQUIREMENT | REQUIREMENT | K-SEAL-1 | K-SEAL-1 | HIGH |
| DEP-03-04-004 | TRACES_TO_REQUIREMENT | REQUIREMENT | K-AUTH-1 | K-AUTH-1 | HIGH |
| DEP-03-04-005 | TRACES_TO_REQUIREMENT | REQUIREMENT | K-GHOST-1 | K-GHOST-1 | MEDIUM |
| DEP-03-04-006 | TRACES_TO_REQUIREMENT | REQUIREMENT | K-WRITE-1 | K-WRITE-1 | MEDIUM |

### EXECUTION rows (9 ACTIVE)

| DependencyID | Direction | DependencyType | TargetType | Target | Confidence |
|---|---|---|---|---|---|
| DEP-03-04-007 | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-03-01 (Working Root Binding & Session Boot) | HIGH |
| DEP-03-04-008 | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-03-02 (Turn Execution API + SSE Streaming) | HIGH |
| DEP-03-04-009 | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-03-03 (Turn Options Mapping & Fallback Chains) | HIGH |
| DEP-03-04-010 | DOWNSTREAM | INTERFACE | DELIVERABLE | DEL-02-03 (Operator Toolkit Panel) | HIGH |
| DEP-03-04-011 | DOWNSTREAM | INTERFACE | DELIVERABLE | DEL-07-01 (Harness Validation Suite) | MEDIUM |
| DEP-03-04-012 | UPSTREAM | CONSTRAINT | DOCUMENT | SPEC Section 9.7 | HIGH |
| DEP-03-04-013 | UPSTREAM | CONSTRAINT | DOCUMENT | CONTRACT.md (K-SEAL-1 / K-AUTH-1 / K-GATE-1) | HIGH |
| DEP-03-04-014 | UPSTREAM | INTERFACE | DOCUMENT | TYPES.md Section 4 | MEDIUM |
| DEP-03-04-015 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-06-04 (Change Management & Git Hygiene) | LOW |

---

## Run Notes

**Run date:** 2026-02-21
**MODE:** UPDATE
**STRICTNESS:** CONSERVATIVE
**CONSUMER_CONTEXT:** NONE
**DECOMPOSITION_PATH:** `execution/_Decomposition/ChiralityApp_SoftwareDecomposition_2026-02-21_G7-APPROVED.md`
**DECOMPOSITION_STATUS:** Located and used for anchor validation and label resolution.

**Defaults used:**
- SOURCE_DOCS: AUTO -- scanned deliverable folder; identified Datasheet.md, Specification.md, Guidance.md, Procedure.md, _CONTEXT.md, _REFERENCES.md.
- DOC_ROLE_MAP: DEFAULT -- ANCHOR_DOC = Datasheet.md (definition/traceability signal); EXECUTION_DOCS = Procedure.md, Guidance.md, Specification.md.
- ANCHOR_DOC: Datasheet.md (explicit identification table with SOW/OBJ references).
- EXECUTION_DOC_ORDER: Procedure.md (prerequisites table), Guidance.md (considerations/relationships), Specification.md (excluded scope / requirements).

**Assumptions recorded in rows:**
- DEP-03-04-015: DEL-06-04 file integrity assumption from Guidance security threat model (ASSUMPTION, LOW confidence).

**Warnings:**
- None.

**Integrity check results:**
- Parent anchor (IMPLEMENTS_NODE): 1 found (DEP-03-04-001 -> SOW-012). OK.
- Schema: All required columns present. CSV parseable.
- DependencyID uniqueness: All 15 IDs unique. OK.
- ACTIVE rows evidence: All ACTIVE rows have EvidenceFile and SourceRef. OK.
- Enum normalization: All enums are canonical write-form. OK.
- Referential integrity: FromDeliverableID = DEL-03-04 for all rows. OK.
- TargetDeliverableID populated only for TargetType=DELIVERABLE rows. OK.
- TargetRefID used for non-deliverable targets (SOW-012, OBJ-002, K-SEAL-1, K-AUTH-1, K-GHOST-1, K-WRITE-1). OK.

---

## Lifecycle Summary

| Status | Count |
|---|---|
| ACTIVE | 15 |
| RETIRED | 0 |

| SatisfactionStatus | Count |
|---|---|
| TBD | 15 |

| DependencyClass | ACTIVE | RETIRED |
|---|---|---|
| ANCHOR | 6 | 0 |
| EXECUTION | 9 | 0 |

---

## Run History

| Timestamp | Mode | Strictness | DecompositionStatus | Warnings | ACTIVE ANCHOR | ACTIVE EXECUTION | Total ACTIVE |
|---|---|---|---|---|---|---|---|
| 2026-02-21 | UPDATE | CONSERVATIVE | Located (G7-APPROVED) | None | 6 | 9 | 15 |
