# Dependencies -- DEL-08-06

**Tracking Mode:** FULL_GRAPH
**Status:** EXTRACTED

---

## Declared Upstream Dependencies

*No declared upstream dependencies. All upstream dependencies were extracted from source documents.*

## Declared Downstream Dependencies

*No declared downstream dependencies. All downstream dependencies were extracted from source documents.*

---

## Extracted Dependency Register

**Register file:** `Dependencies.csv` (v3.1 schema)
**Total ACTIVE rows:** 12
**Total RETIRED rows:** 0

### Summary by Class

| DependencyClass | AnchorType | Count |
|-----------------|------------|-------|
| ANCHOR | IMPLEMENTS_NODE | 1 |
| ANCHOR | TRACES_TO_REQUIREMENT | 1 |
| EXECUTION | NOT_APPLICABLE | 10 |

### Summary by Direction

| Direction | Count |
|-----------|-------|
| UPSTREAM | 11 |
| DOWNSTREAM | 1 |

### Summary by DependencyType

| DependencyType | Count |
|----------------|-------|
| OTHER | 2 |
| CONSTRAINT | 1 |
| HANDOVER | 1 |
| INTERFACE | 4 |
| PREREQUISITE | 4 |

### Summary by TargetType

| TargetType | Count |
|------------|-------|
| WBS_NODE | 3 |
| DELIVERABLE | 5 |
| DOCUMENT | 4 |

### Compact Register

| DependencyID | Class | Direction | Type | TargetName | Confidence | Status |
|--------------|-------|-----------|------|------------|------------|--------|
| DEP-08-06-001 | ANCHOR | UPSTREAM | OTHER | SOW-037 | HIGH | ACTIVE |
| DEP-08-06-002 | ANCHOR | UPSTREAM | OTHER | OBJ-007 | HIGH | ACTIVE |
| DEP-08-06-003 | EXECUTION | UPSTREAM | CONSTRAINT | OI-037 / SOW-037 Scope Decision | HIGH | ACTIVE |
| DEP-08-06-004 | EXECUTION | DOWNSTREAM | HANDOVER | DEL-08-07 Staleness Propagation + Triage Tooling | HIGH | ACTIVE |
| DEP-08-06-005 | EXECUTION | UPSTREAM | INTERFACE | DEL-08-04 On-demand Dependency Graph Generator | MEDIUM | ACTIVE |
| DEP-08-06-006 | EXECUTION | UPSTREAM | INTERFACE | DEL-08-05 Deliverable-level Lock Mechanism | MEDIUM | ACTIVE |
| DEP-08-06-007 | EXECUTION | UPSTREAM | INTERFACE | DEL-05-04 Dependency Tracking File Contract (v3.1) | MEDIUM | ACTIVE |
| DEP-08-06-008 | EXECUTION | UPSTREAM | INTERFACE | DEL-08-02 Dependencies.csv v3.1 Schema Linter | LOW | ACTIVE |
| DEP-08-06-009 | EXECUTION | UPSTREAM | PREREQUISITE | docs/SPEC.md | HIGH | ACTIVE |
| DEP-08-06-010 | EXECUTION | UPSTREAM | PREREQUISITE | docs/CONTRACT.md | HIGH | ACTIVE |
| DEP-08-06-011 | EXECUTION | UPSTREAM | PREREQUISITE | docs/DIRECTIVE.md | HIGH | ACTIVE |
| DEP-08-06-012 | EXECUTION | UPSTREAM | PREREQUISITE | docs/PLAN.md | HIGH | ACTIVE |

---

## Lifecycle Summary

| Status | Count |
|--------|-------|
| ACTIVE | 12 |
| RETIRED | 0 |

### Satisfaction Status Breakdown (ACTIVE rows)

| SatisfactionStatus | Count |
|--------------------|-------|
| TBD | 7 |
| PENDING | 1 |
| SATISFIED | 4 |

---

## Run Notes

**Run timestamp:** 2026-02-21
**Mode:** UPDATE
**Strictness:** CONSERVATIVE
**Consumer context:** NONE
**Decomposition path:** `/Users/ryan/ai-env/projects/chirality-app-dev1/execution/_Decomposition/ChiralityApp_SoftwareDecomposition_2026-02-21_G7-APPROVED.md`
**Decomposition status:** Available and validated
**Decomp variant:** SOFTWARE

### Defaults Used

- `SOURCE_DOCS`: AUTO -- scanned deliverable folder; found Datasheet.md, Specification.md, Guidance.md, Procedure.md, _CONTEXT.md, _REFERENCES.md
- `ANCHOR_DOC`: AUTO -- selected Datasheet.md (contains Identification table with DeliverableID, PackageID, Scope Coverage, Supports Objectives)
- `EXECUTION_DOC_ORDER`: AUTO -- Procedure.md (prerequisites and steps), Specification.md (requirements and standards), Guidance.md (principles and considerations), Datasheet.md (attributes and references)
- `DOC_ROLE_MAP`: DEFAULT heuristic applied

### Anchor Validation

- Parent anchor (IMPLEMENTS_NODE): SOW-037 -- confirmed in decomposition Scope Ledger (SOW-037 maps to PKG-08, DEL-08-06, OBJ-007)
- Trace anchor: OBJ-007 -- confirmed in decomposition Objectives section and Scope Ledger
- No warnings.

### Extraction Notes

- DEP-08-06-003 (CONSTRAINT): OI-037 / SOW-037 scope prerequisite is both an ANCHOR target (SOW-037 as scope item) and an EXECUTION constraint (OI-037 must be resolved to IN before implementation). Separated into distinct rows to preserve Tree x DAG integrity.
- DEP-08-06-005 (INTERFACE to DEL-08-04): Procedure Prerequisite #6 states "status known" -- this is an informational interface, not a blocking prerequisite. The deliverable needs to know DEL-08-04's scope status to inform SHA computation design.
- DEP-08-06-006 (INTERFACE to DEL-08-05): Similar pattern -- "status known" plus conditional use of lock protocol in Step 2.1.
- DEP-08-06-007 (INTERFACE to DEL-05-04): Pattern reference, not a hard prerequisite. The Dependencies.csv v3.1 schema is used as a design pattern model.
- DEP-08-06-008 (INTERFACE to DEL-08-02): Confidence LOW -- stated as "may share infrastructure," which is a possibility not a requirement. Retained because the source text is explicit about the potential sharing.
- Document dependencies (DEP-08-06-009 through -012): All four governance documents are explicitly cited as required inputs across multiple source documents. SatisfactionStatus set to SATISFIED because Procedure notes them as "Available."

### Warnings

*No warnings.*

---

## Run History

| Timestamp | Mode | Strictness | Decomposition | Warnings | ACTIVE Count |
|-----------|------|------------|---------------|----------|--------------|
| 2026-02-21 | UPDATE | CONSERVATIVE | G7-APPROVED (available) | None | 12 |
