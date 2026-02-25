# Datasheet — DEL-07-02: Example Execution Roots + Conformance Fixtures

---

## Identification

| Field | Value |
|-------|-------|
| **Deliverable ID** | DEL-07-02 |
| **Name** | Example Execution Roots + Conformance Fixtures |
| **Package** | PKG-07 — Validation & Example Assets |
| **Type** | TEST_SUITE |
| **Context Envelope** | M |
| **Responsible Party** | TBD — human ruling needed (see Lensing Item E-001: accountability for conformance requires an identified responsible party) |
| **Scope Item(s)** | SOW-029 |
| **Objective(s)** | OBJ-006 |
| **Decomposition Revision** | G7-APPROVED (2026-02-21) |

---

## Attributes

| Attribute | Value | Source |
|-----------|-------|--------|
| **Location in repo** | `examples/` (at repo root) | PLAN.md Section 2 |
| **Artifact types** | OTHER / DOC / TEST | Decomposition (DEL-07-02 row) |
| **Content type** | Concrete execution root directory structures with package/deliverable folders and metadata files | PLAN.md Section 2; SPEC.md Sections 1-2 |
| **Target conformance spec** | `docs/SPEC.md` Sections 1, 2, 10, 12 | SPEC.md |
| **Includes semantic artifacts** | Yes — `_SEMANTIC.md` samples expected | PLAN.md Section 2 |
| **Includes dependency artifacts** | OUT for current baseline — example `Dependencies.csv` samples are intentionally excluded to keep fixture surface minimal; revisit only if DEL-08-02 is ruled IN | Human ruling (2026-02-22) recorded in `MEMORY.md` |
| **Platform constraints** | None (filesystem artifacts; platform-independent) | **ASSUMPTION** |
| **Minimum example count** | 1 execution root (`examples/example-project/`) for baseline conformance/regression coverage | Human ruling (2026-02-22) recorded in `MEMORY.md` |
| **Canonical term form** | "execution root" (two words, unhyphenated when used as a noun phrase; hyphenated "execution-root" only when used as a compound modifier before a noun, e.g., "execution-root directory") | Guidance vocabulary note; SPEC.md usage convention |

---

## Conditions

| Condition | Detail |
|-----------|--------|
| **Conformance standard** | Execution root layout MUST match `docs/SPEC.md` Section 1; deliverable folders MUST match Section 2; folder naming MUST follow Section 10 sanitization rules (Source: SPEC.md) |
| **Validation checkability** | Examples MUST pass the folder structure validation checklist defined in `docs/SPEC.md` Section 12 (Source: SPEC.md Section 12) |
| **Lifecycle representativeness** | Examples SHOULD demonstrate multiple lifecycle states (e.g., OPEN, INITIALIZED, SEMANTIC_READY) to support regression testing (**ASSUMPTION**) |
| **Self-contained** | Each example execution root SHOULD be self-contained (no external file dependencies) so that regression tests can run against them in isolation (**ASSUMPTION**) |
| **Filesystem-as-state fidelity** | Examples MUST demonstrate the "filesystem is the state" principle: all state as plain files, no DB, git-trackable artifacts (Source: DIRECTIVE.md Section 2.1; CONTRACT.md K-GHOST-1) |

---

## Construction

| Element | Detail |
|---------|--------|
| **Directory structure** | One or more execution root directories under `examples/`, each containing the canonical layout: `INIT.md`, `PKG-XX_*/` package folders with `0_References/`, `1_Working/`, `2_Checking/`, `3_Issued/` subfolders, and tool-root directories as needed (Source: SPEC.md Section 1) |
| **Deliverable folder contents** | Each example deliverable folder contains the minimum viable fileset (`_STATUS.md`, `_CONTEXT.md`, `_DEPENDENCIES.md`, `_REFERENCES.md`) and optionally the document kit (`Datasheet.md`, `Specification.md`, `Guidance.md`, `Procedure.md`) depending on lifecycle state demonstrated (Source: SPEC.md Section 2.1) |
| **Metadata consistency** | `_STATUS.md` state, `_CONTEXT.md` fields, and folder naming MUST be internally consistent within each example (Source: SPEC.md Sections 3, 4, 10) |
| **Tool root examples** | TBD — whether examples include populated tool roots (`_Aggregation/`, `_Scheduling/`, etc.); human ruling needed (see Lensing Item B-002: SPEC.md Section 1.2 lists tool roots but the example coverage scope is unspecified) |
| **Decomposition document** | Each example execution root SHOULD include a decomposition document under `_Decomposition/` to satisfy the validation checklist (Source: SPEC.md Section 12.1) |

---

## References

| Ref | Document | Relevance |
|-----|----------|-----------|
| 1 | `docs/SPEC.md` | Authoritative specification for execution root layout, deliverable folder layout, file schemas, and validation checklist |
| 2 | `docs/TYPES.md` | Canonical vocabulary, stable ID formats, lifecycle states |
| 3 | `docs/DIRECTIVE.md` | Founding intent, filesystem-as-state principle, design philosophy |
| 4 | `docs/CONTRACT.md` | Binding invariants that examples must demonstrate compliance with |
| 5 | `docs/PLAN.md` Section 2 | Description of existing `examples/` assets and their purpose |
| 6 | Decomposition (G7-APPROVED) | DEL-07-02 definition, SOW-029, OBJ-006 |
