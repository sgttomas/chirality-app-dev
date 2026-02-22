# Dependencies -- DEL-06-03

**Tracking Mode:** FULL_GRAPH
**Status:** EXTRACTED

---

## Declared Upstream Dependencies

*No manually declared upstream dependencies.*

## Declared Downstream Dependencies

*No manually declared downstream dependencies.*

---

## Extracted Dependency Register

**Schema Version:** v3.1
**Total Rows:** 15
**ACTIVE:** 15 | **RETIRED:** 0

| DependencyID | Class | AnchorType | Dir | Type | TargetType | Target | Confidence | Status |
|---|---|---|---|---|---|---|---|---|
| DEP-06-03-001 | ANCHOR | IMPLEMENTS_NODE | UPSTREAM | OTHER | WBS_NODE | SOW-020 | HIGH | ACTIVE |
| DEP-06-03-002 | ANCHOR | TRACES_TO_REQUIREMENT | UPSTREAM | OTHER | REQUIREMENT | OBJ-004 | MEDIUM | ACTIVE |
| DEP-06-03-003 | ANCHOR | TRACES_TO_REQUIREMENT | UPSTREAM | OTHER | REQUIREMENT | OBJ-006 | MEDIUM | ACTIVE |
| DEP-06-03-004 | EXECUTION | NOT_APPLICABLE | UPSTREAM | PREREQUISITE | DOCUMENT | AGENT_AGGREGATION.md | HIGH | ACTIVE |
| DEP-06-03-005 | EXECUTION | NOT_APPLICABLE | UPSTREAM | PREREQUISITE | DOCUMENT | AGENT_RECONCILIATION.md | HIGH | ACTIVE |
| DEP-06-03-006 | EXECUTION | NOT_APPLICABLE | UPSTREAM | PREREQUISITE | DOCUMENT | AGENT_ESTIMATING.md | HIGH | ACTIVE |
| DEP-06-03-007 | EXECUTION | NOT_APPLICABLE | UPSTREAM | PREREQUISITE | DOCUMENT | SCHEDULING.md | HIGH | ACTIVE |
| DEP-06-03-008 | EXECUTION | NOT_APPLICABLE | UPSTREAM | PREREQUISITE | DOCUMENT | SPEC.md | HIGH | ACTIVE |
| DEP-06-03-009 | EXECUTION | NOT_APPLICABLE | UPSTREAM | PREREQUISITE | DOCUMENT | CONTRACT.md | HIGH | ACTIVE |
| DEP-06-03-010 | EXECUTION | NOT_APPLICABLE | UPSTREAM | PREREQUISITE | DOCUMENT | DIRECTIVE.md | HIGH | ACTIVE |
| DEP-06-03-011 | EXECUTION | NOT_APPLICABLE | UPSTREAM | PREREQUISITE | DOCUMENT | Software Decomposition (G7-APPROVED) | HIGH | ACTIVE |
| DEP-06-03-012 | EXECUTION | NOT_APPLICABLE | UPSTREAM | INTERFACE | DELIVERABLE | DEL-06-01 | HIGH | ACTIVE |
| DEP-06-03-013 | EXECUTION | NOT_APPLICABLE | DOWNSTREAM | INTERFACE | DELIVERABLE | DEL-06-02 | MEDIUM | ACTIVE |
| DEP-06-03-014 | EXECUTION | NOT_APPLICABLE | UPSTREAM | INTERFACE | DELIVERABLE | DEL-05-02 | MEDIUM | ACTIVE |
| DEP-06-03-015 | EXECUTION | NOT_APPLICABLE | UPSTREAM | PREREQUISITE | DOCUMENT | AGENT_HELPS_HUMANS.md | HIGH | ACTIVE |

---

## Run Notes

### Defaults and Paths Used

| Setting | Value |
|---------|-------|
| MODE | UPDATE |
| STRICTNESS | CONSERVATIVE |
| CONSUMER_CONTEXT | NONE |
| DECOMPOSITION_PATH | `execution/_Decomposition/ChiralityApp_SoftwareDecomposition_2026-02-21_G7-APPROVED.md` |
| DECOMP_VARIANT | SOFTWARE |
| ANCHOR_DOC | Datasheet.md (AUTO -- selected by filename heuristic: contains "datasheet") |
| EXECUTION_DOC_ORDER | Specification.md, Procedure.md, Guidance.md (AUTO -- ordered by workflow clarity heuristic) |
| SOURCE_DOCS | Datasheet.md, Specification.md, Guidance.md, Procedure.md, _CONTEXT.md, _REFERENCES.md (AUTO -- all candidate source documents in deliverable folder) |

### Extraction Notes

- **Pass 1 (ANCHOR):** Extracted 1 IMPLEMENTS_NODE anchor (SOW-020) and 2 TRACES_TO_REQUIREMENT anchors (OBJ-004, OBJ-006). OBJ-004 and OBJ-006 mappings are marked ASSUMPTION per Datasheet: "best-effort mapping via PKG-06 package-grouping heuristic." Decomposition confirms these mappings at the deliverable table entry.
- **Pass 2 (EXECUTION):** Extracted 12 EXECUTION rows:
  - 8 PREREQUISITE/DOCUMENT rows for required input documents (4 agent instruction files + 3 governing documents + 1 decomposition document + 1 agent design standard = actually 9, but AGENT_HELPS_HUMANS.md counted separately).
  - 3 INTERFACE/DELIVERABLE rows for cross-deliverable edges (DEL-06-01, DEL-06-02, DEL-05-02).
- **Conflict C-001 impact:** SCHEDULING's `_Schedule/` tool root is not listed in SPEC Section 1.2. This creates a dependency from DEL-06-03's R-003 conformance assessment onto SPEC content managed by DEL-05-02 (captured in DEP-06-03-014).

### Warnings

*No warnings.*

### Integrity Check Results

- Parent anchor count (IMPLEMENTS_NODE, ACTIVE): 1 -- OK
- DependencyID uniqueness: PASS (15 unique IDs)
- Required columns present: PASS
- All ACTIVE rows have EvidenceFile + SourceRef: PASS
- No obvious duplicate rows: PASS

---

## Run History

| Timestamp | Mode | Strictness | Decomposition | Warnings | ACTIVE Count | Notes |
|-----------|------|-----------|--------------|----------|-------------|-------|
| 2026-02-21 | UPDATE | CONSERVATIVE | Located at `execution/_Decomposition/ChiralityApp_SoftwareDecomposition_2026-02-21_G7-APPROVED.md` | None | 15 | Initial extraction. 3 ANCHOR + 12 EXECUTION rows. |

---

## Lifecycle Summary

| Category | Count |
|----------|-------|
| **ACTIVE** | 15 |
| **RETIRED** | 0 |
| --- | --- |
| ANCHOR rows (ACTIVE) | 3 |
| EXECUTION rows (ACTIVE) | 12 |
| --- | --- |
| IMPLEMENTS_NODE (ACTIVE) | 1 |
| TRACES_TO_REQUIREMENT (ACTIVE) | 2 |
| --- | --- |
| SatisfactionStatus: TBD | 15 |
| SatisfactionStatus: SATISFIED | 0 |

---
