# Dependencies — DEL-03-01

**Tracking Mode:** FULL_GRAPH
**Status:** EXTRACTED
**Register:** `Dependencies.csv` (v3.1)

---

## Declared Upstream Dependencies

*No manually declared upstream dependencies.*

## Declared Downstream Dependencies

*No manually declared downstream dependencies.*

---

## Extracted Dependency Register

**Total ACTIVE rows:** 14
**ANCHOR rows:** 5 (IMPLEMENTS_NODE: 1, TRACES_TO_REQUIREMENT: 4)
**EXECUTION rows:** 9

### ANCHOR Edges (Tree — Definition Traceability)

| DependencyID | AnchorType | TargetType | TargetRefID | TargetName | Confidence |
|---|---|---|---|---|---|
| DEP-03-01-001 | IMPLEMENTS_NODE | WBS_NODE | PKG-03 | Harness Runtime Core | HIGH |
| DEP-03-01-002 | TRACES_TO_REQUIREMENT | REQUIREMENT | SOW-003 | SOW-003: Working Root selection and filesystem-as-state | HIGH |
| DEP-03-01-003 | TRACES_TO_REQUIREMENT | REQUIREMENT | SOW-004 | SOW-004: Session boot and turn execution APIs | HIGH |
| DEP-03-01-004 | TRACES_TO_REQUIREMENT | REQUIREMENT | OBJ-001 | OBJ-001: Working macOS desktop build and install path | HIGH |
| DEP-03-01-005 | TRACES_TO_REQUIREMENT | REQUIREMENT | OBJ-002 | OBJ-002: Harness runtime correctness | HIGH |

### EXECUTION Edges (DAG — Information Flow)

| DependencyID | Direction | DependencyType | TargetType | Target | Statement (summary) | Confidence |
|---|---|---|---|---|---|---|
| DEP-03-01-006 | DOWNSTREAM | PREREQUISITE | DELIVERABLE | DEL-03-02 (Turn Execution API + SSE Streaming) | Boot is prerequisite for turn execution; produces session record consumed by turns | HIGH |
| DEP-03-01-007 | DOWNSTREAM | INTERFACE | DELIVERABLE | DEL-03-03 (Turn Options Mapping & Fallback Chains) | Boot-time opts subset feeds into full runtime opts mapping | MEDIUM |
| DEP-03-01-008 | UPSTREAM | CONSTRAINT | DELIVERABLE | DEL-05-01 (Instruction Root Bundling & Runtime Access) | Boot must resolve Instruction Root per DEL-05-01 contract | HIGH |
| DEP-03-01-009 | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-03-05 (Anthropic Provider Integration & Key Provisioning) | Boot requires Anthropic SDK integration for bootstrap turn | HIGH |
| DEP-03-01-010 | UPSTREAM | PREREQUISITE | DOCUMENT | SPEC Section 9.8 (Harness turn input contract) | Normative source for session boot API and opts chains | HIGH |
| DEP-03-01-011 | UPSTREAM | CONSTRAINT | DOCUMENT | DIRECTIVE Section 2 (Design philosophy) | Filesystem-as-state and root separation constraints | HIGH |
| DEP-03-01-012 | UPSTREAM | CONSTRAINT | DOCUMENT | CONTRACT invariant catalog (K-GHOST-1, K-STATUS-1) | Binding invariants constraining session implementation | HIGH |
| DEP-03-01-013 | UPSTREAM | PREREQUISITE | DOCUMENT | Harness Architecture Graphs & Sequence | Boot sequence definition and module dependency graph | HIGH |
| DEP-03-01-014 | UPSTREAM | PREREQUISITE | EXTERNAL | Anthropic Agent SDK | SDK required for bootstrap turn execution; location TBD | MEDIUM |

---

## Lifecycle Summary

| Category | Count |
|---|---|
| ACTIVE | 14 |
| RETIRED | 0 |

### Closure State Breakdown (ACTIVE rows)

| SatisfactionStatus | Count |
|---|---|
| TBD | 14 |

---

## Run Notes

**Run date:** 2026-02-21
**Mode:** UPDATE
**Strictness:** CONSERVATIVE
**Consumer context:** NONE

### Defaults and Paths Used

- **DECOMPOSITION_PATH:** `/Users/ryan/ai-env/projects/chirality-app-dev1/execution/_Decomposition/ChiralityApp_SoftwareDecomposition_2026-02-21_G7-APPROVED.md` (found; G7-APPROVED revision)
- **SOURCE_DOCS (AUTO):** Datasheet.md, Specification.md, Guidance.md, Procedure.md, _CONTEXT.md, _REFERENCES.md
- **ANCHOR_DOC:** Datasheet.md (contains Identification table with Package, Scope Coverage, Objectives, Decomposition Ref)
- **EXECUTION_DOC_ORDER:** Specification.md, Guidance.md, Procedure.md (ordered by normative weight)

### Assumptions

- No prior `Dependencies.csv` existed; all rows are newly created.
- OBJ-001 and OBJ-002 are treated as TRACES_TO_REQUIREMENT anchors (objectives function as requirement-level traceability targets in this decomposition).

### Warnings

- None. Parent anchor (IMPLEMENTS_NODE) found: 1. No FLOATING_NODE or AMBIGUOUS_ANCHOR condition.

### Extraction Notes

**Pass 1 (ANCHOR):** Extracted 1 parent anchor (PKG-03) and 4 trace anchors (SOW-003, SOW-004, OBJ-001, OBJ-002) from Datasheet.md Identification table. All confirmed against decomposition Deliverables table and Scope Ledger.

**Pass 2 (EXECUTION):** Extracted 9 execution edges:
- 2 DOWNSTREAM deliverable edges (DEL-03-02 prerequisite, DEL-03-03 interface) from Guidance.md C4 and C5.
- 2 UPSTREAM deliverable edges (DEL-05-01 constraint, DEL-03-05 prerequisite) from Specification.md REQ-09 and REQ-05.
- 4 UPSTREAM document edges (SPEC, DIRECTIVE, CONTRACT, harness architecture) from Datasheet.md References table and Specification.md Standards/Requirements.
- 1 UPSTREAM external edge (Anthropic Agent SDK) from Specification.md Standards and Procedure Prerequisites.

**Not extracted (information-flow filter applied):**
- DEL-03-04 (Subagent Governance): mentioned in Specification Excluded section but no explicit information/artifact transfer stated between DEL-03-01 and DEL-03-04.
- DEL-03-06 (Outbound Network Guardrails): mentioned in Specification Excluded section but no explicit information/artifact transfer stated.
- DEL-04-01 (Attachments): mentioned in Specification Excluded section but no explicit information/artifact transfer stated.
- `docs/harness/harness_manual_validation.md`: referenced for validation script alignment but is a verification reference, not an input/prerequisite for producing this deliverable's artifacts.

---

## Run History

| Timestamp | Mode | Strictness | Decomposition | Warnings | ACTIVE Count |
|---|---|---|---|---|---|
| 2026-02-21 | UPDATE | CONSERVATIVE | G7-APPROVED (found) | None | 14 |

---

## Downstream Handoff Notes

*Not applicable (CONSUMER_CONTEXT = NONE).*
