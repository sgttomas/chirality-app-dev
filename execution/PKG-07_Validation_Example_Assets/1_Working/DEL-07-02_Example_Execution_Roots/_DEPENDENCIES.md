# Dependencies -- DEL-07-02

**Tracking Mode:** FULL_GRAPH
**Status:** EXTRACTED
**Register:** `Dependencies.csv` (v3.1 schema, 11 rows)

---

## Declared Upstream Dependencies

*No manually declared upstream dependencies. See Extracted Dependency Register below.*

## Declared Downstream Dependencies

*No manually declared downstream dependencies. See Extracted Dependency Register below.*

---

## Extracted Dependency Register

**Total rows:** 11
**ACTIVE:** 11 | **RETIRED:** 0

### ANCHOR edges (2 ACTIVE)

| DependencyID | AnchorType | TargetRefID | TargetName | Confidence | Notes |
|---|---|---|---|---|---|
| DEP-07-02-001 | IMPLEMENTS_NODE | SOW-029 | SOW-029 | HIGH | Parent scope item. Confirmed in decomposition. |
| DEP-07-02-002 | TRACES_TO_REQUIREMENT | OBJ-006 | OBJ-006 | HIGH | Objective trace. Confirmed in decomposition. |

### EXECUTION edges (9 ACTIVE)

| DependencyID | Direction | DependencyType | TargetType | TargetName | Confidence | Notes |
|---|---|---|---|---|---|---|
| DEP-07-02-003 | UPSTREAM | PREREQUISITE | DOCUMENT | docs/SPEC.md | HIGH | Primary conformance target (Sections 1, 2, 10, 12). |
| DEP-07-02-004 | UPSTREAM | PREREQUISITE | DOCUMENT | docs/TYPES.md | HIGH | Canonical vocabulary, ID formats, lifecycle states. |
| DEP-07-02-005 | UPSTREAM | PREREQUISITE | DOCUMENT | docs/CONTRACT.md | HIGH | Binding invariants K-HIER-1, K-ID-1, K-STATUS-1, K-GHOST-1. |
| DEP-07-02-006 | UPSTREAM | PREREQUISITE | DOCUMENT | docs/DIRECTIVE.md | MEDIUM | Filesystem-as-state principle. |
| DEP-07-02-007 | UPSTREAM | PREREQUISITE | DOCUMENT | docs/PLAN.md | MEDIUM | Location and purpose of examples/ assets. |
| DEP-07-02-008 | DOWNSTREAM | HANDOVER | DELIVERABLE | DEL-07-01 (Harness Validation Suite) | HIGH | This deliverable produces test fixtures consumed by DEL-07-01. |
| DEP-07-02-009 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-07-01 (Harness Validation Suite) | HIGH | DEL-07-01 validation scripts required to verify examples (REQ-10). |
| DEP-07-02-010 | DOWNSTREAM | INTERFACE | DELIVERABLE | DEL-08-03 (Execution Root Folder Structure Validator) | LOW | Conditional: DEL-08-03 scope is TBD. |
| DEP-07-02-011 | DOWNSTREAM | INTERFACE | DELIVERABLE | DEL-08-02 (Dependencies.csv v3.1 Schema Linter) | LOW | Human ruling sets Dependencies.csv OUT for baseline; edge remains conditional/non-driving unless scope is re-ruled and DEL-08-02 is brought IN. |

---

## Lifecycle Summary

| Metric | Count |
|---|---|
| **ACTIVE** | 11 |
| **RETIRED** | 0 |
| **ANCHOR (ACTIVE)** | 2 |
| **EXECUTION (ACTIVE)** | 9 |

### Closure-state breakdown (ACTIVE rows)

| SatisfactionStatus | Count |
|---|---|
| SATISFIED | 2 |
| TBD | 9 |

---

## Run Notes

**Run timestamp:** 2026-02-21
**Mode:** UPDATE
**Strictness:** CONSERVATIVE
**Consumer context:** NONE

### Defaults and paths used

- **DECOMPOSITION_PATH:** `execution/_Decomposition/ChiralityApp_SoftwareDecomposition_2026-02-21_G7-APPROVED.md` (G7-APPROVED, located and validated)
- **SOURCE_DOCS (AUTO):** Datasheet.md, Specification.md, Guidance.md, Procedure.md, _CONTEXT.md, _REFERENCES.md
- **ANCHOR_DOC:** Datasheet.md (selected: contains Identification table with Scope Item(s) and Objective(s))
- **EXECUTION_DOC_ORDER:** Specification.md, Guidance.md, Procedure.md, _CONTEXT.md
- **DOC_ROLE_MAP:** DEFAULT heuristic applied

### Extraction notes

- **Pass 1 (ANCHOR):** 2 rows extracted. 1 parent anchor (IMPLEMENTS_NODE -> SOW-029), 1 objective trace (TRACES_TO_REQUIREMENT -> OBJ-006). Both confirmed against decomposition scope ledger and objectives table.
- **Pass 2 (EXECUTION):** 9 rows extracted. 5 upstream document prerequisites (SPEC.md, TYPES.md, CONTRACT.md, DIRECTIVE.md, PLAN.md), 2 deliverable-level edges with DEL-07-01 (bidirectional: downstream handover + upstream interface), 2 conditional downstream interfaces (DEL-08-03 TBD scope, DEL-08-02 TBD scope).
- **Evidence refresh (2026-02-22):** DEP-07-02-008 and DEP-07-02-009 set to `SATISFIED` after runtime-backed `harness:validate:premerge` pass against `examples/example-project` (`HARNESS_PREMERGE_STATUS=pass`, `HARNESS_PREMERGE_TEST_COUNT=7`).
- **Scope-ruling refresh (2026-02-22):** Dependencies.csv inclusion for DEL-07-02 set OUT for baseline; DEP-07-02-011 retained as conditional/non-driving with updated note and `LastSeen=2026-02-22`.
- Internal requirements REQ-01 through REQ-10 in Specification.md are deliverable-internal and were not emitted as separate trace rows; they reference external documents already captured as DOCUMENT prerequisites.
- The DEL-07-01 relationship is bidirectional: DEL-07-02 produces fixtures consumed by DEL-07-01 (DEP-008, DOWNSTREAM HANDOVER), and DEL-07-01 provides validation scripts required by DEL-07-02 for acceptance (DEP-009, UPSTREAM INTERFACE). Both edges are explicitly supported by source text.
- DEL-08-03 and DEL-08-02 edges are conditional. DEL-07-02 human ruling (2026-02-22) sets Dependencies.csv inclusion OUT for baseline, so DEP-07-02-011 remains non-driving unless scope is re-ruled and DEL-08-02 is brought IN.
- DEL-06-05 (Governance Coherence) was mentioned in Procedure Phase 5 Step 5.3 as an escalation target, but this is a coordination pathway, not an information-flow dependency. Not extracted per protocol (no data/artifact transfer).

### Warnings

*No warnings.*

### Quality check results

- Schema: All required columns present. CSV parseable.
- DependencyID uniqueness: PASS (11 unique IDs).
- EvidenceFile + SourceRef: All ACTIVE rows populated.
- Parent anchor check: PASS (exactly 1 IMPLEMENTS_NODE row: DEP-07-02-001).
- Enum normalization: All enums in canonical write form.
- _DEPENDENCIES.md counts match Dependencies.csv: PASS (11 ACTIVE, 0 RETIRED).
- No obvious duplicate rows detected.

---

## Run History

| Timestamp | Mode | Strictness | Decomposition | Warnings | ACTIVE Count |
|---|---|---|---|---|---|
| 2026-02-21 | UPDATE | CONSERVATIVE | G7-APPROVED (validated) | None | 11 |
| 2026-02-22 | EVIDENCE_REFRESH | N/A | G7-APPROVED (validated) | None | 11 |
