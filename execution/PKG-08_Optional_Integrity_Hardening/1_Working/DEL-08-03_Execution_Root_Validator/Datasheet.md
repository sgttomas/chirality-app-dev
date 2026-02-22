# Datasheet — DEL-08-03

## Identification

| Field | Value |
|-------|-------|
| **Deliverable ID** | DEL-08-03 |
| **Name** | Execution Root Folder Structure Validator |
| **Package** | PKG-08 — Optional Integrity Hardening |
| **Type** | TEST_SUITE |
| **Context Envelope** | S |
| **Responsible Party** | TBD |
| **Scope Item** | SOW-034 (TBD status) |
| **Objective** | OBJ-007 — Optional: integrity hardening loop |
| **Anticipated Artifacts** | SCRIPT / TEST / DOC |

> **[Lensing B-002]** Responsible Party is TBD. Human assignment required before this deliverable moves to IN_PROGRESS.
> Source: _CONTEXT.md (Responsible Party not specified); Decomposition DEL-08-03 row (ResponsibleParty: TBD).

## Attributes

| Attribute | Value | Source |
|-----------|-------|--------|
| Validation rule source | `docs/SPEC.md` Section 12 (Folder Structure Validation Checklist) | Decomposition (DEL-08-03 description); PLAN.md Section 3.3 |
| Scope status | TBD — scope item SOW-034 has not been flipped to IN | Decomposition SSOW table (SOW-034) |
| Effort estimate (qualitative) | Low | PLAN.md Section 3.3 ("The validation rules are fully defined.") |
| Target execution context | Standalone script; CI-integration-ready | PLAN.md Section 3.3 ("enables pre-run checks and CI integration") |
| Validation levels | Three tiers: Execution Root, Package Folder, Deliverable Folder | SPEC.md Section 12.1, 12.2, 12.3 |
| Platform | macOS 15+, Apple Silicon (consistent with project platform target) | Decomposition DEC-PLAT-001 |
| Language / runtime | TBD — not specified in sources | **ASSUMPTION: likely JavaScript/TypeScript or Python given repo context** |
| Input | Filesystem path to an execution root | SPEC.md Section 12 (rules operate on execution root structure) |
| Output format | TBD — validation report format not specified | TBD |

> **[Lensing A-001]** The Language / runtime decision is a blocking TBD. The prescriptive direction for this deliverable (implementation approach, dependency management, test framework choice) cannot be fully established until the human decides the implementation language. All downstream Procedure steps (A2 onward) depend on this decision.
> Source: Datasheet Attributes "Language / runtime" row; Procedure.md Step A2.

> **[Lensing X-003]** Datasheet References row 4 lists SPEC.md Section 10 (label sanitization rules) as relevant to this deliverable, but Specification Requirements contain no check for label sanitization. This is a cross-document scope inconsistency. Human must decide whether label sanitization validation is in scope for this validator. If not in scope, Datasheet References row 4 should be annotated accordingly. See Guidance Conflict Table entry CT-001.
> Source: Datasheet References row 4; Specification.md Requirements section (no label sanitization REQ found).

## Conditions

| Condition | Detail |
|-----------|--------|
| **Precondition** | An execution root folder must exist at the provided path |
| **Scope dependency** | SOW-034 must be flipped to IN before this deliverable becomes active work. **ASSUMPTION: deliverable may be drafted and scaffolded while TBD, but should not be ISSUED until scope is resolved.** |
| **No external dependencies** | PLAN.md Section 4 states this validator has "no dependencies" on other hardening candidates |
| **Input path validity** | The validator must handle the case where the input path does not exist or is not a directory (see Specification REQ-08d). Source: **[Lensing F-002]** |

## Construction

| Aspect | Detail |
|--------|--------|
| **Rule source** | SPEC.md Section 12 defines the complete checklist (Sections 12.1, 12.2, 12.3) |
| **Execution Root validation (SPEC 12.1)** | At least one `PKG-XX_{Label}/` folder; `_Decomposition/` with >= 1 decomposition doc; `INIT.md` exists |
| **Package Folder validation (SPEC 12.2)** | Named `{PKG-ID}_{PkgLabel}/` with valid `PKG-XX` identifier; contains `1_Working/`; SHOULD contain `0_References/`, `2_Checking/`, `3_Issued/` |
| **Deliverable Folder validation (SPEC 12.3)** | Named `{DEL-ID}_{DelLabel}/` with valid `DEL-XX-YY` identifier; contains `_STATUS.md` with valid lifecycle state; contains `_CONTEXT.md`; contains `_DEPENDENCIES.md`; contains `_REFERENCES.md` |
| **Initialized deliverable checks (SPEC 12.3)** | Additionally: `Datasheet.md`, `Specification.md`, `Guidance.md`, `Procedure.md` present |
| **Dependency-tracked checks (SPEC 12.3)** | Additionally: `Dependencies.csv` with valid v3.1 schema headers |
| **ID format validation** | `PKG-XX` (zero-padded numeric); `DEL-XX-YY` (hyphen-separated, zero-padded) per TYPES.md Section 2 |
| **Lifecycle state validation** | Valid states: `OPEN`, `INITIALIZED`, `SEMANTIC_READY`, `IN_PROGRESS`, `CHECKING`, `ISSUED` per SPEC.md Section 3.2 |
| **Lifecycle state ordering** | The ordering used for ">= INITIALIZED" checks is: `OPEN` < `INITIALIZED` < `SEMANTIC_READY` < `IN_PROGRESS` < `CHECKING` < `ISSUED` (per SPEC.md Section 3.2). See Specification REQ-04 Note. **[Lensing B-003]** |
| **Tool root validation** | TBD — SPEC.md Section 1.2 lists expected tool roots but Section 12 does not include explicit tool-root validation checklist items |
| **Label sanitization validation** | TBD — SPEC.md Section 10 defines filesystem-safe label sanitization rules; whether this validator checks label conformance is a human decision. See Guidance Conflict Table CT-001. **[Lensing X-003]** |

## Definition of Done

> **[Lensing E-002]** Acceptance criteria for this deliverable are currently distributed across Specification Documentation table, Procedure Verification table, and Procedure Records. A consolidated definition of done is TBD pending human decision. Candidate criteria include:
> - (a) Validator script passes all automated tests
> - (b) Validator successfully validates the project's own execution root without false positives
> - (c) CI integration is demonstrated (or documented as ready)
> - (d) Usage documentation is complete
>
> Source: Specification.md Documentation table; Procedure.md Verification table "Overall" row; Guidance.md Purpose section.

## References

| Ref | Document | Relevance |
|-----|----------|-----------|
| 1 | `docs/SPEC.md` Section 12 | Primary: defines the validation checklist |
| 2 | `docs/SPEC.md` Sections 1-2 | Defines execution root layout and deliverable folder layout |
| 3 | `docs/SPEC.md` Section 3 | Defines valid lifecycle states for `_STATUS.md` |
| 4 | `docs/SPEC.md` Section 10 | Defines filesystem-safe label sanitization rules. **Note: whether label sanitization validation is in scope for this deliverable is TBD (see Guidance Conflict Table CT-001). [Lensing X-003]** |
| 5 | `docs/TYPES.md` Section 2 | Defines stable identifier formats and rules |
| 6 | `docs/PLAN.md` Section 3.3 | Describes this deliverable as a future hardening candidate |
| 7 | `docs/PLAN.md` Section 4 | Sequencing rationale (no dependencies for this item) |
| 8 | `docs/CONTRACT.md` K-STATUS-1 | `_STATUS.md` is the canonical lifecycle indicator |
| 9 | Decomposition (G7-APPROVED) | DEL-08-03 entry, SOW-034, OBJ-007 |
