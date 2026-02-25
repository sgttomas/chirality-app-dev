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

**Total ACTIVE rows:** 16
**ANCHOR rows:** 5 (IMPLEMENTS_NODE: 1, TRACES_TO_REQUIREMENT: 4)
**EXECUTION rows:** 11

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
| DEP-03-01-009 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-03-05 (Anthropic Provider Integration & Key Provisioning) | Boot requires Anthropic SDK integration for bootstrap turn | HIGH |
| DEP-03-01-010 | UPSTREAM | PREREQUISITE | DOCUMENT | SPEC Section 9.8 (Harness turn input contract) | Normative source for session boot API and opts chains | HIGH |
| DEP-03-01-011 | UPSTREAM | CONSTRAINT | DOCUMENT | DIRECTIVE Section 2 (Design philosophy) | Filesystem-as-state and root separation constraints | HIGH |
| DEP-03-01-012 | UPSTREAM | CONSTRAINT | DOCUMENT | CONTRACT invariant catalog (K-GHOST-1, K-STATUS-1) | Binding invariants constraining session implementation | HIGH |
| DEP-03-01-013 | UPSTREAM | PREREQUISITE | DOCUMENT | Harness Architecture Graphs & Sequence | Boot sequence definition and module dependency graph | HIGH |
| DEP-03-01-014 | UPSTREAM | PREREQUISITE | EXTERNAL | Anthropic Agent SDK | SDK required for bootstrap turn execution; location TBD | MEDIUM |
| DEP-03-01-015 | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-03-07 (Harness API Baseline in Frontend Runtime) | Session boot requires API route surface in frontend; SCA-001 gate was previously blocking and is now met at IN_PROGRESS | HIGH |
| DEP-03-01-016 | UPSTREAM | CONSTRAINT | DELIVERABLE | DEL-01-03 (Frontend Workspace Bootstrap & Packaging Baseline) | Frontend workspace must exist before session boot implementation; SCA-001 gate was previously blocking and is now met at IN_PROGRESS | HIGH |

---

## Lifecycle Summary

| Category | Count |
|---|---|
| ACTIVE | 16 |
| RETIRED | 0 |

### Closure State Breakdown (ACTIVE rows)

| SatisfactionStatus | Count |
|---|---|
| TBD | 13 |
| SATISFIED | 2 |
| NOT_APPLICABLE | 1 |

---

## Run Notes

**Run date:** 2026-02-23
**Mode:** UPDATE
**Strictness:** CONSERVATIVE
**Consumer context:** NONE

### Defaults and Paths Used

- **DECOMPOSITION_PATH:** `/Users/ryan/ai-env/projects/chirality-app-dev/execution/_Decomposition/ChiralityApp_SoftwareDecomposition_2026-02-21_G7-APPROVED.md` (found; G7-APPROVED revision + SCA-001 amendment)
- **SOURCE_DOCS (AUTO):** Datasheet.md, Specification.md, Guidance.md, Procedure.md, _CONTEXT.md, _REFERENCES.md
- **ANCHOR_DOC:** Datasheet.md (contains Identification table with Package, Scope Coverage, Objectives, Decomposition Ref)
- **EXECUTION_DOC_ORDER:** Specification.md, Guidance.md, Procedure.md (ordered by normative weight)

### Assumptions

- OBJ-001 and OBJ-002 are treated as TRACES_TO_REQUIREMENT anchors (objectives function as requirement-level traceability targets in this decomposition).
- DEP-03-01-015 and DEP-03-01-016 use `RequiredMaturity=IN_PROGRESS` based on the SCA-001 Execution Gating Rule text ("reach at least IN_PROGRESS per blocker maturity policy"). Both are now set `SatisfactionStatus=SATISFIED` after lifecycle confirmation that `DEL-03-07` and `DEL-01-03` are `IN_PROGRESS`.

### Integration Fan-In Refresh (2026-02-22)

- Re-validated lifecycle truth from upstream `_STATUS.md` files:
  - `DEL-03-07` = `IN_PROGRESS`
  - `DEL-01-03` = `IN_PROGRESS`
- Updated `Dependencies.csv` rows `DEP-03-01-015` and `DEP-03-01-016`:
  - `SatisfactionStatus: PENDING -> SATISFIED`
  - Statement/notes normalized to indicate gate-met state while retaining SCA-001 provenance.
- No rows were added or retired in this fan-in refresh.

### Integration Fan-In Refresh (2026-02-23)

- Re-ran dependency validation after live ChatPanel + WORKBENCH consumer wiring pass.
- Re-confirmed upstream gating edges remain SATISFIED:
  - `DEP-03-01-015` (`DEL-03-07`) = SATISFIED
  - `DEP-03-01-016` (`DEL-01-03`) = SATISFIED
- No rows were added, retired, or reclassified in this refresh.

### Warnings

- None. Parent anchor (IMPLEMENTS_NODE) found: 1. No FLOATING_NODE or AMBIGUOUS_ANCHOR condition.

### Extraction Notes

**Trigger:** Re-extraction after SCA-001 scope amendment added DEL-03-07, DEL-01-03, DEL-02-05, DEL-07-03 with pre-tier gating for frontend-dependent Tier 2 work.

**Pass 1 (ANCHOR):** Re-confirmed 1 parent anchor (PKG-03) and 4 trace anchors (SOW-003, SOW-004, OBJ-001, OBJ-002). No changes from prior extraction. All `LastSeen` updated to 2026-02-22.

**Pass 2 (EXECUTION):** Re-confirmed 9 existing execution edges. Added 2 new edges:
- DEP-03-01-015: DEL-03-07 (UPSTREAM PREREQUISITE) -- SCA-001 Execution Gating Rule explicitly names DEL-03-01 as blocked on DEL-03-07 (Harness API Baseline). DEL-03-07 covers SOW-045 (session/turn route baseline in local runtime tree), which is a direct prerequisite for session boot API implementation.
- DEP-03-01-016: DEL-01-03 (UPSTREAM CONSTRAINT) -- SCA-001 Execution Gating Rule explicitly names DEL-03-01 as blocked on DEL-01-03 (Frontend Workspace Bootstrap). DEL-01-03 covers SOW-044 (in-repo frontend workspace baseline), which constrains all frontend-path-dependent code work.

**Not extracted (information-flow filter applied):**
- DEL-02-05 (Frontend Workflow Shell Baseline): Named in the SCA-001 gating rule as a blocker at the tier level, but no explicit information/artifact transfer between DEL-03-01 and DEL-02-05 is stated. The shell UI is not an input to session boot implementation.
- DEL-07-03 (Frontend Validation & Runbook Baseline): Named in the SCA-001 gating rule as a blocker at the tier level, but no explicit information/artifact transfer between DEL-03-01 and DEL-07-03 is stated. Validation tooling is downstream verification, not an implementation input.
- DEL-03-04 (Subagent Governance): mentioned in Specification Excluded section but no explicit information/artifact transfer stated between DEL-03-01 and DEL-03-04.
- DEL-03-06 (Outbound Network Guardrails): mentioned in Specification Excluded section but no explicit information/artifact transfer stated.
- DEL-04-01 (Attachments): mentioned in Specification Excluded section but no explicit information/artifact transfer stated.
- `docs/harness/harness_manual_validation.md`: referenced for validation script alignment but is a verification reference, not an input/prerequisite for producing this deliverable's artifacts.

---

## Run History

| Timestamp | Mode | Strictness | Decomposition | Warnings | ACTIVE Count |
|---|---|---|---|---|---|
| 2026-02-23 (fan-in refresh) | UPDATE | CONSERVATIVE | G7-APPROVED + SCA-001 (found) | None | 16 |
| 2026-02-22 (fan-in refresh) | UPDATE | CONSERVATIVE | G7-APPROVED + SCA-001 (found) | None | 16 |
| 2026-02-22 | UPDATE | CONSERVATIVE | G7-APPROVED + SCA-001 (found) | None | 16 |
| 2026-02-21 | UPDATE | CONSERVATIVE | G7-APPROVED (found) | None | 14 |

---

## Downstream Handoff Notes

*Not applicable (CONSUMER_CONTEXT = NONE).*
