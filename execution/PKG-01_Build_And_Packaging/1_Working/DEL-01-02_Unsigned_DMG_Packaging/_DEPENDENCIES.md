# Dependencies -- DEL-01-02

**Tracking Mode:** FULL_GRAPH
**Status:** EXTRACTED
**Register Schema:** v3.1

---

## Declared Upstream Dependencies

*No manually declared upstream dependencies yet. See Extracted Dependency Register below for agent-extracted edges.*

## Declared Downstream Dependencies

*No manually declared downstream dependencies yet.*

---

## Extracted Dependency Register

**Total ACTIVE rows:** 8
**Total RETIRED rows:** 0

### ANCHOR rows (3 ACTIVE)

| DependencyID | AnchorType | TargetType | TargetRefID / TargetName | Confidence | Status |
|---|---|---|---|---|---|
| DEP-01-02-001 | IMPLEMENTS_NODE | WBS_NODE | SOW-002 | HIGH | ACTIVE |
| DEP-01-02-002 | IMPLEMENTS_NODE | WBS_NODE | OBJ-001 | MEDIUM | ACTIVE |
| DEP-01-02-003 | TRACES_TO_REQUIREMENT | REQUIREMENT | DEC-PLAT-001 | HIGH | ACTIVE |

### EXECUTION rows (5 ACTIVE)

| DependencyID | Direction | DependencyType | TargetType | Target | Confidence | Status |
|---|---|---|---|---|---|---|
| DEP-01-02-004 | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-01-01 (macOS 15+ Apple Silicon Build Baseline) | HIGH | ACTIVE |
| DEP-01-02-005 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-05-01 (Instruction Root Bundling & Runtime Access) | HIGH | ACTIVE |
| DEP-01-02-006 | UPSTREAM | CONSTRAINT | DOCUMENT | docs/DIRECTIVE.md (Section 2.6) | HIGH | ACTIVE |
| DEP-01-02-007 | UPSTREAM | INTERFACE | DOCUMENT | docs/PLAN.md (Section 2) | MEDIUM | ACTIVE |
| DEP-01-02-008 | UPSTREAM | CONSTRAINT | EXTERNAL | Apple Developer Documentation (Info.plist; Gatekeeper; App Bundle) | MEDIUM | ACTIVE |

---

## Lifecycle Summary

| Category | Count |
|---|---|
| **ACTIVE** | 8 |
| **RETIRED** | 0 |

### Closure Status Breakdown (ACTIVE rows)

| SatisfactionStatus | Count |
|---|---|
| TBD | 6 |
| PENDING | 2 |

**PENDING rows:** DEP-01-02-004 (DEL-01-01 prerequisite) and DEP-01-02-005 (DEL-05-01 interface) -- these represent upstream deliverables whose outputs are needed but not yet available.

---

## Run Notes

### Run 2026-02-21 (Initial Extraction)

**Mode:** UPDATE
**Strictness:** CONSERVATIVE
**Consumer Context:** NONE
**Decomposition Path:** `execution/_Decomposition/ChiralityApp_SoftwareDecomposition_2026-02-21_G7-APPROVED.md`
**Decomposition Status:** AVAILABLE (G7-APPROVED)

**Source Documents Scanned:**
- `Datasheet.md` (ANCHOR_DOC -- primary anchor source; contains Identification table with Scope Items, Objectives, Decision References)
- `Specification.md` (EXECUTION_DOC -- primary execution source; contains Requirements, Upstream Dependencies, Standards)
- `Guidance.md` (EXECUTION_DOC -- secondary; contains Principles, Considerations, Trade-offs)
- `Procedure.md` (EXECUTION_DOC -- secondary; contains Prerequisites, Steps, Verification)
- `_CONTEXT.md` (metadata -- confirms deliverable identity and scope coverage)
- `_REFERENCES.md` (reference resolution -- minimal content; no deliverable-specific references yet)

**Defaults Applied:**
- ANCHOR_DOC: `Datasheet.md` (selected by heuristic: contains "datasheet" in filename and has explicit Identification table with scope/objective fields)
- EXECUTION_DOC_ORDER: `Specification.md`, `Procedure.md`, `Guidance.md` (ordered by workflow clarity)
- SOURCE_DOCS: AUTO (all .md files in deliverable folder excluding `_DEPENDENCIES.md` and `Dependencies.csv`)

**Anchor Validation (via decomposition):**
- SOW-002: CONFIRMED in Scope Ledger -- IN scope, PKG-01, DEL-01-02, OBJ-001
- OBJ-001: CONFIRMED in Objectives section -- "Working macOS desktop build and install path"
- DEC-PLAT-001: CONFIRMED in Decision Log -- "macOS 15+, Apple Silicon only; .dmg; signing/notarization not required"

**Target Resolution (via decomposition):**
- DEL-01-01: CONFIRMED in Deliverables table (PKG-01) -- "macOS 15+ Apple Silicon Build Baseline"
- DEL-05-01: CONFIRMED in Deliverables table (PKG-05) -- "Instruction Root Bundling & Runtime Access"

**Warnings:**
- [WARNING] AMBIGUOUS_ANCHOR: Two IMPLEMENTS_NODE rows found (DEP-01-02-001 for SOW-002 and DEP-01-02-002 for OBJ-001). SOW-002 is the scope item (primary parent anchor); OBJ-001 is the objective (supporting anchor). Both are explicitly stated in the Datasheet Identification table. Recommend human review to confirm whether OBJ-001 should be reclassified as TRACES_TO_REQUIREMENT or retained as IMPLEMENTS_NODE.

**Assumptions Logged:**
- DEP-01-02-004: DEL-01-01 prerequisite is stated as ASSUMPTION in all source documents ("not yet formally declared in decomposition"). Confidence remains HIGH because the information flow is explicit and logically necessary (SOW-001 precedes SOW-002).
- DEP-01-02-002: OBJ-001 mapping is stated as ASSUMPTION in the Datasheet ("best-effort mapping via PKG-01 package grouping"). Confidence set to MEDIUM.

---

## Run History

| Timestamp | Mode | Strictness | Consumer | Decomp Status | Warnings | ACTIVE Anchors | ACTIVE Execution | ACTIVE Total |
|---|---|---|---|---|---|---|---|---|
| 2026-02-21 | UPDATE | CONSERVATIVE | NONE | AVAILABLE (G7-APPROVED) | AMBIGUOUS_ANCHOR | 3 | 5 | 8 |

---

## Downstream Handoff Notes

*Not applicable (CONSUMER_CONTEXT = NONE).*
