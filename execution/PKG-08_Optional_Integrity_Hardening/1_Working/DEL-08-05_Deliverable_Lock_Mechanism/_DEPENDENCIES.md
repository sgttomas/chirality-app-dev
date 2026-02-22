# Dependencies -- DEL-08-05

**Tracking Mode:** FULL_GRAPH
**Status:** EXTRACTED

---

## Declared Upstream Dependencies

*No human-declared upstream dependencies yet. See Extracted Dependency Register below.*

## Declared Downstream Dependencies

*No human-declared downstream dependencies yet. See Extracted Dependency Register below.*

---

## Extracted Dependency Register

**Schema Version:** v3.1
**Total ACTIVE rows:** 15
**Total RETIRED rows:** 0

### ANCHOR rows (5 ACTIVE)

| DependencyID | AnchorType | TargetType | TargetRefID | TargetName | Confidence | Status |
|---|---|---|---|---|---|---|
| DEP-08-05-001 | IMPLEMENTS_NODE | WBS_NODE | SOW-036 | SOW-036: Formalize a deliverable-level lock mechanism | HIGH | ACTIVE |
| DEP-08-05-002 | TRACES_TO_REQUIREMENT | REQUIREMENT | OBJ-007 | OBJ-007: Optional integrity hardening loop | MEDIUM | ACTIVE |
| DEP-08-05-003 | TRACES_TO_REQUIREMENT | REQUIREMENT | K-WRITE-1 | K-WRITE-1: Agent write scope enforcement | HIGH | ACTIVE |
| DEP-08-05-004 | TRACES_TO_REQUIREMENT | REQUIREMENT | K-STATUS-1 | K-STATUS-1: Lifecycle state authority | HIGH | ACTIVE |
| DEP-08-05-005 | TRACES_TO_REQUIREMENT | REQUIREMENT | K-GHOST-1 | K-GHOST-1: No ghost inputs | HIGH | ACTIVE |

### EXECUTION rows (10 ACTIVE)

| DependencyID | Direction | DependencyType | TargetType | TargetName | Confidence | Status |
|---|---|---|---|---|---|---|
| DEP-08-05-006 | UPSTREAM | CONSTRAINT | EXTERNAL | OI-036: Scope decision for SOW-036 | HIGH | ACTIVE |
| DEP-08-05-007 | UPSTREAM | INTERFACE | DOCUMENT | docs/PLAN.md Section 3.5 | HIGH | ACTIVE |
| DEP-08-05-008 | UPSTREAM | INTERFACE | DOCUMENT | docs/CONTRACT.md | HIGH | ACTIVE |
| DEP-08-05-009 | UPSTREAM | INTERFACE | DOCUMENT | docs/DIRECTIVE.md Sections 2.1 and 5 | HIGH | ACTIVE |
| DEP-08-05-010 | UPSTREAM | INTERFACE | DOCUMENT | docs/SPEC.md Sections 2 and 3 | HIGH | ACTIVE |
| DEP-08-05-011 | UPSTREAM | INTERFACE | DOCUMENT | docs/TYPES.md Section 4 | HIGH | ACTIVE |
| DEP-08-05-012 | UPSTREAM | CONSTRAINT | EXTERNAL | DEC-PLAT-001: macOS 15+ Apple Silicon only | HIGH | ACTIVE |
| DEP-08-05-013 | DOWNSTREAM | ENABLES | DELIVERABLE | DEL-08-06: Unified Pipeline Run Record Persistence | MEDIUM | ACTIVE |
| DEP-08-05-014 | DOWNSTREAM | ENABLES | DELIVERABLE | DEL-08-07: Staleness Propagation + Triage Tooling | MEDIUM | ACTIVE |
| DEP-08-05-015 | DOWNSTREAM | INTERFACE | DELIVERABLE | DEL-06-02: Local Deliverable Workflow Agents | MEDIUM | ACTIVE |

---

## Run Notes

**Run timestamp:** 2026-02-21
**Mode:** UPDATE
**Strictness:** CONSERVATIVE
**Consumer context:** NONE

**Defaults used:**
- SOURCE_DOCS: AUTO -- scanned Datasheet.md, Specification.md, Guidance.md, Procedure.md, _CONTEXT.md, _REFERENCES.md
- ANCHOR_DOC: Datasheet.md (highest-confidence match for definition/traceability signal)
- EXECUTION_DOC_ORDER: Specification.md, Guidance.md, Procedure.md (ordered by workflow clarity)
- DECOMPOSITION_PATH: `execution/_Decomposition/ChiralityApp_SoftwareDecomposition_2026-02-21_G7-APPROVED.md` (available; used for anchor validation and label resolution)

**Decomposition validation status:** AVAILABLE. All anchors validated against Decomposition Scope Ledger and Deliverables table.

**Anchor validation results:**
- SOW-036 confirmed in Scope Ledger: TBD status, PKG-08, DEL-08-05, OBJ-007.
- OBJ-007 confirmed in Objectives section: "Optional: integrity hardening loop (TBD scope)."
- K-WRITE-1, K-STATUS-1, K-GHOST-1 confirmed as CONTRACT.md invariants referenced explicitly in Specification requirements.
- Parent anchor count: 1 (IMPLEMENTS_NODE -> SOW-036). No warnings.

**Extraction notes:**
- OBJ-007 linkage is marked ASSUMPTION per source documents (best-effort mapping via PKG-08 grouping; Lensing C-001). Confidence set to MEDIUM.
- OI-036 (scope decision gate) is the primary blocking constraint. SOW-036 is TBD; deliverable is in scaffold state.
- Downstream ENABLES edges to DEL-08-06 and DEL-08-07 are based on Guidance C5 statement that "subsequent deliverables may need lock awareness." Confidence MEDIUM because coupling degree is TBD.
- Downstream INTERFACE to DEL-06-02 is based on Specification REQ-LOCK-007 requiring agent protocol updates. Confidence MEDIUM because the exact integration surface (which agent instruction files) is TBD.
- No coordination-only or structural-adjacency edges were emitted (per protocol: information-flow only).
- Governance documents (CONTRACT.md, DIRECTIVE.md, SPEC.md, TYPES.md, PLAN.md) are captured as INTERFACE/DOCUMENT edges because the deliverable explicitly requires compliance with their contents (not mere references).

---

## Run History

| Timestamp | Mode | Strictness | DecompositionStatus | Warnings | ACTIVE_ANCHOR | ACTIVE_EXECUTION | Notes |
|---|---|---|---|---|---|---|---|
| 2026-02-21 | UPDATE | CONSERVATIVE | AVAILABLE | None | 5 | 10 | Initial extraction. 15 total ACTIVE rows. No RETIRED rows. |

---

## Lifecycle Summary

| Category | Count |
|---|---|
| ACTIVE (total) | 15 |
| RETIRED (total) | 0 |
| ANCHOR ACTIVE | 5 |
| EXECUTION ACTIVE | 10 |

**Closure-state breakdown (SatisfactionStatus):**

| SatisfactionStatus | Count |
|---|---|
| TBD | 14 |
| PENDING | 1 |

Note: DEP-08-05-006 (OI-036 scope decision) is set to PENDING because the scope decision is an explicit outstanding gate that must be resolved.
