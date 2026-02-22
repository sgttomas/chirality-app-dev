# Dependencies -- DEL-06-02

**Tracking Mode:** FULL_GRAPH
**Status:** EXTRACTED

---

## Declared Upstream Dependencies

*Human-owned section. No declared upstream dependencies at this time.*

## Declared Downstream Dependencies

*Human-owned section. No declared downstream dependencies at this time.*

---

## Extracted Dependency Register

**RegisterSchemaVersion:** v3.1
**Total ACTIVE rows:** 17
**Total RETIRED rows:** 0

### Anchor Edges (DependencyClass=ANCHOR)

| DependencyID | AnchorType | TargetType | TargetRefID / TargetName | Confidence | Status |
|---|---|---|---|---|---|
| DEP-06-02-001 | IMPLEMENTS_NODE | WBS_NODE | PKG-06 Agent Suite & Governance | HIGH | ACTIVE |
| DEP-06-02-002 | TRACES_TO_REQUIREMENT | REQUIREMENT | SOW-017 | HIGH | ACTIVE |
| DEP-06-02-003 | TRACES_TO_REQUIREMENT | REQUIREMENT | SOW-019 | HIGH | ACTIVE |
| DEP-06-02-004 | TRACES_TO_REQUIREMENT | REQUIREMENT | OBJ-004 | MEDIUM | ACTIVE |
| DEP-06-02-005 | TRACES_TO_REQUIREMENT | REQUIREMENT | OBJ-006 | MEDIUM | ACTIVE |

**Anchor summary:** 1 parent anchor (IMPLEMENTS_NODE), 4 trace anchors (TRACES_TO_REQUIREMENT). Parent anchor resolves to PKG-06 in decomposition. OBJ-004/OBJ-006 traces marked MEDIUM confidence per Datasheet ASSUMPTION note on best-effort mapping.

### Execution Edges (DependencyClass=EXECUTION)

| DependencyID | Direction | DependencyType | TargetType | Target | Confidence | Status |
|---|---|---|---|---|---|---|
| DEP-06-02-006 | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-06-01 Agent Instruction Suite Structural Conformance | HIGH | ACTIVE |
| DEP-06-02-007 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-05-04 Dependency Tracking File Contract (v3.1) | HIGH | ACTIVE |
| DEP-06-02-008 | DOWNSTREAM | INTERFACE | DELIVERABLE | DEL-06-03 Cross-deliverable Workflow Support | MEDIUM | ACTIVE |
| DEP-06-02-009 | UPSTREAM | INTERFACE | DOCUMENT | docs/SPEC.md | HIGH | ACTIVE |
| DEP-06-02-010 | UPSTREAM | INTERFACE | DOCUMENT | docs/CONTRACT.md | HIGH | ACTIVE |
| DEP-06-02-011 | UPSTREAM | INTERFACE | DOCUMENT | docs/TYPES.md | HIGH | ACTIVE |
| DEP-06-02-012 | UPSTREAM | INTERFACE | DOCUMENT | docs/DIRECTIVE.md | HIGH | ACTIVE |
| DEP-06-02-013 | UPSTREAM | INTERFACE | DOCUMENT | agents/AGENT_PREPARATION.md | HIGH | ACTIVE |
| DEP-06-02-014 | UPSTREAM | INTERFACE | DOCUMENT | agents/AGENT_4_DOCUMENTS.md | HIGH | ACTIVE |
| DEP-06-02-015 | UPSTREAM | INTERFACE | DOCUMENT | agents/AGENT_CHIRALITY_FRAMEWORK.md | HIGH | ACTIVE |
| DEP-06-02-016 | UPSTREAM | INTERFACE | DOCUMENT | agents/AGENT_CHIRALITY_LENS.md | HIGH | ACTIVE |
| DEP-06-02-017 | UPSTREAM | INTERFACE | DOCUMENT | agents/AGENT_HELPS_HUMANS.md | MEDIUM | ACTIVE |

**Execution summary:** 11 UPSTREAM edges (1 PREREQUISITE to DEL-06-01, 1 INTERFACE to DEL-05-04, 8 DOCUMENT interfaces, 1 DOCUMENT context reference). 1 DOWNSTREAM edge (INTERFACE to DEL-06-03).

---

## Run Notes

**Run timestamp:** 2026-02-21
**Mode:** UPDATE
**Strictness:** CONSERVATIVE
**Consumer context:** NONE
**Decomposition path:** `/Users/ryan/ai-env/projects/chirality-app-dev1/execution/_Decomposition/ChiralityApp_SoftwareDecomposition_2026-02-21_G7-APPROVED.md`
**Decomposition status:** Found and used for anchor validation and label resolution.

**Defaults applied:**
- SOURCE_DOCS: AUTO -- scanned deliverable folder, identified Datasheet.md, Specification.md, Guidance.md, Procedure.md, _CONTEXT.md, _REFERENCES.md
- ANCHOR_DOC: Datasheet.md (highest-confidence match for definition/traceability signal via "datasheet" keyword; _CONTEXT.md used as secondary anchor source)
- EXECUTION_DOC_ORDER: Procedure.md, Specification.md, Guidance.md, Datasheet.md (Procedure.md ranked first for workflow/execution signal)
- DOC_ROLE_MAP: DEFAULT heuristic applied

**Pass 1 (Anchor) notes:**
- Parent anchor (IMPLEMENTS_NODE) resolved to PKG-06 via _CONTEXT.md PackageID and decomposition confirmation.
- SOW-017 and SOW-019 confirmed in decomposition scope ledger as mapping to PKG-06/DEL-06-02.
- OBJ-004 and OBJ-006 confirmed in decomposition deliverable table. Datasheet flags these as ASSUMPTION (best-effort mapping via PKG-06 heuristic, confirmation pending lensing item X-001). Confidence set to MEDIUM accordingly.

**Pass 2 (Execution) notes:**
- DEL-06-01 upstream dependency explicitly stated in Procedure.md as a non-blocking contextual dependency. Typed as PREREQUISITE (non-blocking) rather than CONSTRAINT because the Procedure clarifies it can be executed independently.
- DEL-05-04 interface dependency explicitly stated in Specification.md scope exclusions and reinforced in Guidance.md C3.
- DEL-06-03 downstream interface identified from Specification.md scope exclusions. Direction is DOWNSTREAM because local workflow outputs feed into cross-deliverable operations.
- DEL-06-04 and DEL-06-05 are mentioned in Specification.md scope exclusions but only as boundary statements ("covered by DEL-06-04/05"), not as information-flow dependencies. Not extracted per information-flow-only rule.
- Document dependencies (docs/SPEC.md, docs/CONTRACT.md, docs/TYPES.md, docs/DIRECTIVE.md, four agent instruction files) are all explicitly listed as required references in Procedure.md and/or Datasheet.md References table.
- agents/AGENT_HELPS_HUMANS.md included at MEDIUM confidence as it is referenced in Datasheet but not listed as a Procedure required reference.
- DEL-07-01 is mentioned in Procedure.md Step 10.3 as an escalation path for test case additions, but this is a recommendation, not an information-flow dependency. Not extracted.

**Warnings:** None.

---

## Run History

| Timestamp | Mode | Strictness | DecompositionStatus | Warnings | ACTIVE Anchors | ACTIVE Execution | Total ACTIVE |
|---|---|---|---|---|---|---|---|
| 2026-02-21 | UPDATE | CONSERVATIVE | Found; used for validation | None | 5 | 12 | 17 |

---

## Lifecycle Summary

| Category | Count |
|---|---|
| **ACTIVE** | 17 |
| **RETIRED** | 0 |

### Closure-state breakdown (ACTIVE rows)

| SatisfactionStatus | Count |
|---|---|
| TBD | 17 |

---

## Downstream Handoff Notes

*No consumer context specified (CONSUMER_CONTEXT=NONE). No handoff notes generated.*
