# Dependencies -- DEL-06-05

**Tracking Mode:** FULL_GRAPH
**Status:** EXTRACTED
**Register Schema:** v3.1

---

## Declared Upstream Dependencies

*No declared upstream dependencies. See Extracted Dependency Register below.*

## Declared Downstream Dependencies

*No declared downstream dependencies. See Extracted Dependency Register below.*

---

## Extracted Dependency Register

**Total rows:** 17
**ACTIVE:** 17 | **RETIRED:** 0

### ANCHOR rows (7 ACTIVE)

| DependencyID | AnchorType | TargetType | TargetRefID | Statement (summary) |
|---|---|---|---|---|
| DEP-06-05-001 | IMPLEMENTS_NODE | WBS_NODE | OBJ-006 | Implements OBJ-006: Validation posture and governance/agent-suite conformance |
| DEP-06-05-002 | TRACES_TO_REQUIREMENT | REQUIREMENT | SOW-030 | Traces to SOW-030: Maintain governance doc internal alignment |
| DEP-06-05-003 | TRACES_TO_REQUIREMENT | REQUIREMENT | SOW-039 | Traces to SOW-039: No automated approval/issuance (OUT) |
| DEP-06-05-004 | TRACES_TO_REQUIREMENT | REQUIREMENT | SOW-040 | Traces to SOW-040: No financial transactions (OUT) |
| DEP-06-05-005 | TRACES_TO_REQUIREMENT | REQUIREMENT | SOW-041 | Traces to SOW-041: No safety-critical decisions without review (OUT) |
| DEP-06-05-006 | TRACES_TO_REQUIREMENT | REQUIREMENT | SOW-042 | Traces to SOW-042: No replacing professional judgment (OUT) |
| DEP-06-05-007 | TRACES_TO_REQUIREMENT | REQUIREMENT | SOW-043 | Traces to SOW-043: No external integration (exception: Anthropic API) (OUT) |

### EXECUTION rows (10 ACTIVE)

| DependencyID | Direction | DependencyType | TargetType | Target | Statement (summary) |
|---|---|---|---|---|---|
| DEP-06-05-008 | UPSTREAM | PREREQUISITE | DOCUMENT | docs/DIRECTIVE.md | Coherence review requires reading DIRECTIVE |
| DEP-06-05-009 | UPSTREAM | PREREQUISITE | DOCUMENT | docs/CONTRACT.md | Coherence review requires reading CONTRACT |
| DEP-06-05-010 | UPSTREAM | PREREQUISITE | DOCUMENT | docs/SPEC.md | Coherence review requires reading SPEC |
| DEP-06-05-011 | UPSTREAM | PREREQUISITE | DOCUMENT | docs/TYPES.md | Coherence review requires reading TYPES |
| DEP-06-05-012 | UPSTREAM | PREREQUISITE | DOCUMENT | docs/PLAN.md | Coherence review requires reading PLAN |
| DEP-06-05-013 | UPSTREAM | PREREQUISITE | DOCUMENT | Decomposition (G7-APPROVED) | Procedure requires decomposition for scope ledger verification |
| DEP-06-05-014 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-06-01 | REQ-GR-06 requires reading agent instruction files; DEL-06-01 owns structural conformance |
| DEP-06-05-015 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-03-04 | Runtime guardrail enforcement (SOW-041) scope boundary with DEL-03-04 |
| DEP-06-05-016 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-03-06 | Runtime network guardrail enforcement (SOW-043) scope boundary with DEL-03-06 |
| DEP-06-05-017 | UPSTREAM | CONSTRAINT | EXTERNAL | DEC-NET-001 | REQ-GR-04 requires consistency with DEC-NET-001 Anthropic API exception |

---

## Lifecycle Summary

| Category | Count |
|---|---|
| **ACTIVE** | 17 |
| **RETIRED** | 0 |

### Closure state breakdown (ACTIVE rows)

| SatisfactionStatus | Count |
|---|---|
| TBD | 17 |

---

## Run Notes

### Defaults and paths used

- **MODE:** UPDATE
- **STRICTNESS:** CONSERVATIVE
- **CONSUMER_CONTEXT:** NONE
- **DECOMPOSITION_PATH:** `execution/_Decomposition/ChiralityApp_SoftwareDecomposition_2026-02-21_G7-APPROVED.md`
- **DECOMPOSITION_STATUS:** Available; used for anchor validation and label resolution.
- **SOURCE_DOCS (AUTO):** Datasheet.md, Specification.md, Guidance.md, Procedure.md, _CONTEXT.md, _REFERENCES.md
- **ANCHOR_DOC (AUTO):** Datasheet.md (contains identification fields, scope items, objectives, invariant mapping)
- **EXECUTION_DOC_ORDER (AUTO):** Procedure.md, Specification.md, Guidance.md

### Assumptions logged during extraction

- All five governance documents (docs/DIRECTIVE.md, docs/CONTRACT.md, docs/SPEC.md, docs/TYPES.md, docs/PLAN.md) are treated as DOCUMENT-type prerequisites because the Procedure explicitly requires them to be readable. They are not deliverable-to-deliverable edges because they are not managed by a specific deliverable in the decomposition; they are shared governance artifacts.
- DEC-NET-001 is classified as TargetType=EXTERNAL because it is a decision-log entry, not a deliverable or document file.

### Warnings

*No warnings. Parent anchor (IMPLEMENTS_NODE) found: 1. No ambiguous anchors.*

---

## Run History

| Timestamp | Mode | Strictness | Decomposition | Warnings | ACTIVE Count |
|---|---|---|---|---|---|
| 2026-02-21 | UPDATE | CONSERVATIVE | G7-APPROVED (available; validated) | None | 17 |

---

## Downstream Handoff Notes

*CONSUMER_CONTEXT is NONE; no downstream handoff notes generated.*
