# Dependencies -- DEL-03-06

**Tracking Mode:** FULL_GRAPH
**Status:** EXTRACTED

---

## Declared Upstream Dependencies

*No manually declared upstream dependencies. See Extracted Dependency Register below.*

## Declared Downstream Dependencies

*No manually declared downstream dependencies. See Extracted Dependency Register below.*

---

## Extracted Dependency Register

**Schema Version:** v3.1
**Total ACTIVE rows:** 14
**Total RETIRED rows:** 0

### ANCHOR rows (6 ACTIVE)

| DependencyID | AnchorType | TargetType | TargetRefID / TargetName | Confidence | Status |
|---|---|---|---|---|---|
| DEP-0306-001 | IMPLEMENTS_NODE | WBS_NODE | PKG-03 -- Harness Runtime Core | HIGH | ACTIVE |
| DEP-0306-002 | TRACES_TO_REQUIREMENT | REQUIREMENT | SOW-006 -- Harness runtime responsibilities | HIGH | ACTIVE |
| DEP-0306-003 | TRACES_TO_REQUIREMENT | REQUIREMENT | OBJ-002 -- Harness runtime correctness + Anthropic-only outbound | HIGH | ACTIVE |
| DEP-0306-004 | TRACES_TO_REQUIREMENT | REQUIREMENT | OBJ-006 -- Validation posture and governance conformance | HIGH | ACTIVE |
| DEP-0306-005 | TRACES_TO_REQUIREMENT | REQUIREMENT | DEC-NET-001 -- Anthropic-only outbound network ruling | HIGH | ACTIVE |
| DEP-0306-006 | TRACES_TO_REQUIREMENT | REQUIREMENT | OI-002 -- Enforcement + verification method | HIGH | ACTIVE |

### EXECUTION rows (8 ACTIVE)

| DependencyID | Direction | DependencyType | TargetType | Target | Confidence | Status |
|---|---|---|---|---|---|---|
| DEP-0306-007 | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-03-05 -- Anthropic Provider Integration (endpoint info) | HIGH | ACTIVE |
| DEP-0306-008 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-03-05 -- Anthropic Provider Integration (domain list interface) | HIGH | ACTIVE |
| DEP-0306-009 | UPSTREAM | CONSTRAINT | REQUIREMENT | OI-002 -- Human ruling on enforcement mechanism + proof standard | HIGH | ACTIVE |
| DEP-0306-010 | UPSTREAM | PREREQUISITE | DOCUMENT | Anthropic API endpoint domain list (canonical) | MEDIUM | ACTIVE |
| DEP-0306-011 | UPSTREAM | PREREQUISITE | DOCUMENT | Electron security documentation (version-matched) | MEDIUM | ACTIVE |
| DEP-0306-012 | UPSTREAM | CONSTRAINT | DOCUMENT | DIRECTIVE Section 4.2 -- External integrations boundary | HIGH | ACTIVE |
| DEP-0306-013 | UPSTREAM | CONSTRAINT | DOCUMENT | CONTRACT K-GHOST-1 -- No ghost inputs; sealed context | HIGH | ACTIVE |
| DEP-0306-014 | DOWNSTREAM | HANDOVER | DELIVERABLE | DEL-07-01 -- Harness Validation Suite (test integration) | HIGH | ACTIVE |

---

## Lifecycle Summary

| Category | Count |
|---|---|
| **ACTIVE** | 14 |
| **RETIRED** | 0 |
| **ANCHOR (ACTIVE)** | 6 |
| **EXECUTION (ACTIVE)** | 8 |

### Satisfaction Status Breakdown (ACTIVE rows)

| SatisfactionStatus | Count |
|---|---|
| PENDING | 5 |
| TBD | 7 |
| NOT_APPLICABLE | 2 |

---

## Run Notes

**Run Date:** 2026-02-21
**Mode:** UPDATE
**Strictness:** CONSERVATIVE
**Consumer Context:** NONE
**Decomposition Path:** `execution/_Decomposition/ChiralityApp_SoftwareDecomposition_2026-02-21_G7-APPROVED.md`
**Decomposition Status:** Found and used for anchor validation and label resolution.

### Defaults Used

- **SOURCE_DOCS:** AUTO -- scanned deliverable folder; found: `Datasheet.md`, `Specification.md`, `Guidance.md`, `Procedure.md`, `_CONTEXT.md`, `_REFERENCES.md`
- **ANCHOR_DOC:** `Datasheet.md` (matched heuristic: "datasheet" in filename; contains Identification table with explicit IDs)
- **EXECUTION_DOC_ORDER:** `Procedure.md`, `Specification.md`, `Guidance.md` (ordered by workflow clarity)

### Assumptions Recorded

- All ANCHOR rows are FACT-grounded (explicit identifiers found in Datasheet and _CONTEXT.md, confirmed against decomposition).
- DEP-0306-010 (Anthropic API domain list) marked MEDIUM confidence because the canonical source document location is TBD.
- DEP-0306-011 (Electron security docs) marked MEDIUM confidence because the document is external and location is TBD.
- Guidance C5 describes a "coordination dependency" between DEL-03-05 and DEL-03-06. Two rows extracted: DEP-0306-007 (prerequisite for endpoint knowledge) and DEP-0306-008 (interface for domain list sync). The coordination protocol details (E-002) are TBD.

### Warnings

*No warnings.*

### Quality Check Results

- Parent anchor check: 1 IMPLEMENTS_NODE row (DEP-0306-001) -- PASS.
- DependencyID uniqueness: 14 unique IDs -- PASS.
- Required columns present: PASS.
- All ACTIVE rows have EvidenceFile and SourceRef: PASS.
- No obvious duplicate rows: PASS.
- _DEPENDENCIES.md counts match Dependencies.csv: PASS.

---

## Run History

| Timestamp | Mode | Strictness | DecompositionStatus | Warnings | ACTIVE Count |
|---|---|---|---|---|---|
| 2026-02-21 | UPDATE | CONSERVATIVE | Found; used for validation | None | 14 |
