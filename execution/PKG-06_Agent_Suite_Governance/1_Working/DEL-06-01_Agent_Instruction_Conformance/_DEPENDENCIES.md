# Dependencies -- DEL-06-01

**Tracking Mode:** FULL_GRAPH
**Status:** EXTRACTED

---

## Declared Upstream Dependencies

*No upstream dependencies were declared prior to extraction.*

## Declared Downstream Dependencies

*No downstream dependencies were declared prior to extraction.*

---

## Extracted Dependency Register

**Register file:** `Dependencies.csv` (v3.1 schema)
**Total rows:** 10
**ACTIVE rows:** 10
**RETIRED rows:** 0

### ANCHOR Rows (4 ACTIVE)

| DependencyID | AnchorType | TargetRefID | TargetName | Confidence |
|---|---|---|---|---|
| DEP-06-01-001 | IMPLEMENTS_NODE | SOW-031 | SOW-031 | HIGH |
| DEP-06-01-002 | TRACES_TO_REQUIREMENT | OBJ-006 | OBJ-006 | MEDIUM |
| DEP-06-01-003 | TRACES_TO_REQUIREMENT | K-WRITE-1 | K-WRITE-1 | HIGH |
| DEP-06-01-004 | TRACES_TO_REQUIREMENT | SPEC.md Section 9 | SPEC.md Section 9 | HIGH |

### EXECUTION Rows (6 ACTIVE)

| DependencyID | Direction | DependencyType | TargetName | Confidence |
|---|---|---|---|---|
| DEP-06-01-005 | UPSTREAM | PREREQUISITE | AGENT_HELPS_HUMANS.md (v1.1) | HIGH |
| DEP-06-01-006 | UPSTREAM | PREREQUISITE | docs/SPEC.md Section 9 | HIGH |
| DEP-06-01-007 | UPSTREAM | CONSTRAINT | docs/CONTRACT.md (K-WRITE-1) | HIGH |
| DEP-06-01-008 | UPSTREAM | PREREQUISITE | AGENTS.md | HIGH |
| DEP-06-01-009 | UPSTREAM | INTERFACE | AGENT_AUDIT_AGENTS.md | HIGH |
| DEP-06-01-010 | DOWNSTREAM | HANDOVER | AGENTS.md (Full Agent Type Table) | HIGH |

---

## Lifecycle Summary

| Status | Count |
|---|---|
| ACTIVE | 10 |
| RETIRED | 0 |

| SatisfactionStatus | Count |
|---|---|
| TBD | 6 |
| SATISFIED | 4 |

**Notes:** Four EXECUTION UPSTREAM rows (DEP-06-01-005 through DEP-06-01-009) have SatisfactionStatus=SATISFIED because the Procedure prerequisites table confirms all required documents are accessible (Status: Available). The remaining rows are TBD pending execution progress.

---

## Run Notes

**Run date:** 2026-02-21
**Mode:** UPDATE
**Strictness:** CONSERVATIVE
**Consumer context:** NONE
**Decomposition path:** `execution/_Decomposition/ChiralityApp_SoftwareDecomposition_2026-02-21_G7-APPROVED.md`
**Decomposition status:** Available, G7-APPROVED. Anchor validation and label resolution performed successfully.

**Source documents scanned:**
- `Datasheet.md` (ANCHOR_DOC -- primary anchor source)
- `Specification.md` (ANCHOR_DOC + EXECUTION_DOC -- requirements and traceability)
- `Guidance.md` (EXECUTION_DOC -- principles, considerations, conflict table)
- `Procedure.md` (EXECUTION_DOC -- prerequisites, steps, verification)
- `_CONTEXT.md` (metadata envelope)
- `_REFERENCES.md` (reference index -- no additional dependencies derived solely from reference listing)

**Defaults applied:**
- ANCHOR_DOC: `Datasheet.md` (matched heuristic: filename contains "datasheet")
- EXECUTION_DOC_ORDER: `Procedure.md`, `Specification.md`, `Guidance.md`, `_CONTEXT.md`
- SOURCE_DOCS: AUTO (all .md files in deliverable folder excluding dependency artifacts)

**Assumptions recorded:**
- DEP-06-01-002: OBJ-006 mapping is best-effort per decomposition methodology (ASSUMPTION).

**Warnings:** None.

**Quality check results:**
- Schema: PASS -- all required columns present, CSV parseable, DependencyID unique.
- Parent anchor: PASS -- exactly one IMPLEMENTS_NODE row (DEP-06-01-001 -> SOW-031).
- Evidence: PASS -- all ACTIVE rows have EvidenceFile and SourceRef populated.
- Enum normalization: PASS -- all enums are canonical write-form values.
- Referential integrity: PASS -- FromDeliverableID=DEL-06-01 on all rows; non-deliverable targets use TargetRefID/TargetName (not TargetDeliverableID).
- Count consistency: PASS -- _DEPENDENCIES.md counts (10 ACTIVE, 0 RETIRED) match Dependencies.csv.

---

## Run History

| RunDate | Mode | Strictness | DecompositionStatus | Warnings | ActiveCount | RetiredCount |
|---|---|---|---|---|---|---|
| 2026-02-21 | UPDATE | CONSERVATIVE | Available (G7-APPROVED) | None | 10 | 0 |
