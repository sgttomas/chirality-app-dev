# Dependencies -- DEL-02-03

**Tracking Mode:** FULL_GRAPH
**Status:** EXTRACTED

---

## Declared Dependencies

### Upstream (this deliverable requires input FROM)

*No declared upstream dependencies. See Extracted Dependency Register below for extraction results.*

### Downstream (this deliverable produces output FOR)

*No declared downstream dependencies. See Extracted Dependency Register below for extraction results.*

---

## Extracted Dependency Register

**Schema Version:** v3.1
**Total ACTIVE rows:** 11
**Total RETIRED rows:** 0

### ANCHOR Dependencies (5 ACTIVE)

| DependencyID | AnchorType | TargetType | TargetRefID / TargetName | Confidence | Notes |
|---|---|---|---|---|---|
| DEP-02-03-001 | IMPLEMENTS_NODE | WBS_NODE | SOW-025 | HIGH | Parent scope anchor. Confirmed in decomposition. |
| DEP-02-03-002 | TRACES_TO_REQUIREMENT | REQUIREMENT | OBJ-005 | MEDIUM | Objective support via PKG-02 grouping (ASSUMPTION). |
| DEP-02-03-003 | TRACES_TO_REQUIREMENT | REQUIREMENT | K-GHOST-1 | HIGH | CONTRACT binding condition. |
| DEP-02-03-004 | TRACES_TO_REQUIREMENT | REQUIREMENT | K-INVENT-1 | HIGH | CONTRACT binding condition. |
| DEP-02-03-005 | TRACES_TO_REQUIREMENT | REQUIREMENT | K-AUTH-1 | HIGH | CONTRACT binding condition. |

### EXECUTION Dependencies (6 ACTIVE)

| DependencyID | Direction | DependencyType | TargetType | Target | Confidence | Notes |
|---|---|---|---|---|---|---|
| DEP-02-03-006 | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-03-02 (Turn Execution API + SSE Streaming) | HIGH | Harness Turn API must be functional or mockable. |
| DEP-02-03-007 | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-03-01 (Working Root Binding & Session Boot) | HIGH | Session Boot API must be functional or mockable. |
| DEP-02-03-008 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-02-04 (Multi-pane Layout + Theme Hardening) | HIGH | Sidebar integration point required for layout. |
| DEP-02-03-009 | DOWNSTREAM | HANDOVER | DELIVERABLE | DEL-03-03 (Turn Options Mapping & Fallback Chains) | HIGH | DEL-02-03 produces opts; DEL-03-03 consumes them. |
| DEP-02-03-010 | UPSTREAM | CONSTRAINT | DOCUMENT | SPEC Section 9.8 (docs/SPEC.md) | HIGH | Defines opts interface contract. |
| DEP-02-03-011 | UPSTREAM | CONSTRAINT | DOCUMENT | DIRECTIVE Section 2.5 (docs/DIRECTIVE.md) | HIGH | Defines non-authoritative state boundary. |

---

## Lifecycle Summary

| Status | Count |
|---|---|
| ACTIVE | 11 |
| RETIRED | 0 |

| SatisfactionStatus | Count |
|---|---|
| TBD | 11 |

| DependencyClass | ACTIVE | RETIRED |
|---|---|---|
| ANCHOR | 5 | 0 |
| EXECUTION | 6 | 0 |

---

## Run Notes

**Run: 2026-02-21**

- **MODE:** UPDATE
- **STRICTNESS:** CONSERVATIVE
- **CONSUMER_CONTEXT:** NONE
- **DECOMPOSITION_PATH:** `execution/_Decomposition/ChiralityApp_SoftwareDecomposition_2026-02-21_G7-APPROVED.md`
- **DECOMPOSITION_STATUS:** Available, G7-APPROVED. Anchor validation and label resolution performed successfully.
- **SOURCE_DOCS (AUTO):** Datasheet.md, Specification.md, Guidance.md, Procedure.md, _CONTEXT.md, _REFERENCES.md
- **ANCHOR_DOC (AUTO):** Datasheet.md (selected: contains deliverable identification, scope coverage, objective support, conditions)
- **EXECUTION_DOC_ORDER (AUTO):** Procedure.md, Guidance.md, Specification.md, Datasheet.md, _CONTEXT.md

**Defaults applied:**
- SOURCE_DOCS: AUTO -- scanned all .md files in deliverable folder excluding dependency artifacts.
- ANCHOR_DOC: AUTO -- Datasheet.md selected as primary anchor document (identification/scope/objective fields present).
- EXECUTION_DOC_ORDER: AUTO -- Procedure.md prioritized (explicit prerequisites table), then Guidance.md (integration points, relationships), then remaining docs.

**Extraction decisions:**
- SOW-025 anchor (DEP-02-03-001): Confirmed in Datasheet Identification table and decomposition Scope Ledger. Single parent anchor -- no ambiguity.
- OBJ-005 trace (DEP-02-03-002): Marked MEDIUM confidence per source ASSUMPTION tag. Decomposition maps DEL-02-03 -> OBJ-005 via PKG-02 grouping.
- K-GHOST-1, K-INVENT-1, K-AUTH-1 traces (DEP-02-03-003 through 005): Explicit CONTRACT references in Datasheet Conditions and Specification Standards table.
- DEL-03-02 prerequisite (DEP-02-03-006): Explicit in Procedure prerequisites table with enrichment F-002 noting mock/stub acceptability.
- DEL-03-01 prerequisite (DEP-02-03-007): Explicit in Procedure prerequisites table with enrichment F-002.
- DEL-02-04 interface (DEP-02-03-008): Explicit in Procedure prerequisites table; Guidance D-001 enrichment provides coordination protocol. Classified as INTERFACE (not PREREQUISITE) because the relationship is bidirectional layout integration, not a strict gate.
- DEL-03-03 handover (DEP-02-03-009): Explicit producer-consumer statement in Guidance. Direction is DOWNSTREAM because DEL-02-03 produces opts for DEL-03-03.
- SPEC Section 9.8 constraint (DEP-02-03-010): Listed as required accessible reference in Procedure prerequisites.
- DIRECTIVE Section 2.5 constraint (DEP-02-03-011): Listed as required accessible reference in Procedure prerequisites.

**Edges NOT extracted (reasoning):**
- DEL-03-04 (Subagent Governance Fail-Closed): Mentioned in Specification exclusions but no explicit data/artifact transfer from DEL-02-03. The toolkit panel may display governance fields (per Guidance), but runtime enforcement is independent. Insufficient evidence for information-flow edge under CONSERVATIVE strictness.
- docs/PLAN.md: Referenced in Datasheet but as a general context source, not as an explicit required input or constraint for this deliverable's execution.
- docs/CONTRACT.md (whole document): Individual contract clauses (K-GHOST-1, K-INVENT-1, K-AUTH-1) are traced as requirements. The document as a whole is not an information-flow dependency.

**Warnings:** None.

**Quality check results:**
- Parent anchor check: 1 ACTIVE IMPLEMENTS_NODE row (DEP-02-03-001). PASS.
- Schema check: All required columns present. PASS.
- DependencyID uniqueness: All 11 IDs unique. PASS.
- Evidence check: All ACTIVE rows have EvidenceFile and SourceRef populated. PASS.
- Enum normalization: All enums are canonical write-form. PASS.
- Lifecycle consistency: _DEPENDENCIES.md counts match Dependencies.csv. PASS.

---

## Run History

| Timestamp | Mode | Strictness | DecompositionStatus | Warnings | ACTIVE_ANCHOR | ACTIVE_EXECUTION | RETIRED |
|---|---|---|---|---|---|---|---|
| 2026-02-21 | UPDATE | CONSERVATIVE | Available (G7-APPROVED) | None | 5 | 6 | 0 |
