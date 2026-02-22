# Specification — DEL-07-02: Example Execution Roots + Conformance Fixtures

---

## Scope

### Included

- Creation and maintenance of one or more example execution root directory structures under `examples/` at the repository root.
- Each example execution root demonstrates a SPEC-conformant folder layout suitable for regression and conformance testing.
- Example deliverable folders populated with metadata files and (where appropriate) document kit files at various lifecycle states.
- Example `_Decomposition/` documents to satisfy the execution root validation checklist.
- Coverage of the canonical file inventory defined in `docs/SPEC.md` Section 2.1.

Source: SOW-029 (Decomposition G7-APPROVED); PLAN.md Section 2.

### Excluded

- Harness validation scripts and CI integration (covered by DEL-07-01).
- Automated folder-structure validator tooling (covered by DEL-08-03, TBD scope).
- Real project data or proprietary content in examples.
- Example execution roots for non-Chirality project types (**ASSUMPTION**: examples are Chirality-specific).

---

## Requirements

### REQ-01: Execution Root Layout Conformance

Each example execution root MUST conform to the canonical layout defined in `docs/SPEC.md` Section 1:

- At least one `PKG-XX_{Label}/` package folder.
- `_Decomposition/` folder containing at least one decomposition document.
- `INIT.md` with session parameters.

Source: SPEC.md Section 1; SPEC.md Section 12.1.

### REQ-02: Package Folder Conformance

Each example package folder MUST conform to `docs/SPEC.md` Section 1.1:

- Named `{PKG-ID}_{PkgLabel}/` with a valid `PKG-XX` identifier.
- Contains required subfolders: `0_References/`, `0_References/_Archive/`, `1_Working/`, `1_Working/_Archive/`, `2_Checking/`, `2_Checking/From/`, `2_Checking/To/`, `3_Issued/`, `3_Issued/_Archive/`.

Source: SPEC.md Section 1.1; SPEC.md Section 12.2.

### REQ-03: Deliverable Folder Conformance

Each example deliverable folder MUST conform to `docs/SPEC.md` Section 2:

- Named `{DEL-ID}_{DelLabel}/` with a valid `DEL-XX-YY` identifier.
- Contains minimum viable fileset: `_STATUS.md`, `_CONTEXT.md`, `_DEPENDENCIES.md`, `_REFERENCES.md`.
- `_STATUS.md` contains a valid lifecycle state per `docs/SPEC.md` Section 3.2.
- `_CONTEXT.md` header fields are internally consistent with the example's decomposition document.

Source: SPEC.md Section 2; SPEC.md Section 12.3.

### REQ-04: Initialized Deliverable Demonstration

At least one example deliverable MUST demonstrate the `INITIALIZED` (or later) lifecycle state by including the full document kit: `Datasheet.md`, `Specification.md`, `Guidance.md`, `Procedure.md`.

**Lifecycle state ordering** (for "or later" determination): `OPEN` < `INITIALIZED` < `SEMANTIC_READY` < `IN_PROGRESS` < `CHECKING` < `ISSUED`. Any state from `INITIALIZED` onward satisfies this requirement.

Source: SPEC.md Section 12.3 ("initialized" validation); TYPES.md Section 5.1; SPEC.md Section 3.2 (lifecycle sequence).

### REQ-05: Filesystem-Safe Naming

All folder names in examples MUST follow the sanitization rules defined in `docs/SPEC.md` Section 10:

- Package folders: `{PKG-ID}_{Sanitize(PackageName)}/`
- Deliverable folders: `{DEL-ID}_{Sanitize(DeliverableName)}/`
- Canonical (unsanitized) names recorded in `_CONTEXT.md`.

Source: SPEC.md Section 10.

### REQ-06: Lifecycle State Validity

Every `_STATUS.md` in example deliverable folders MUST contain:

- A valid `Current State` from the canonical lifecycle: `OPEN`, `INITIALIZED`, `SEMANTIC_READY`, `IN_PROGRESS`, `CHECKING`, `ISSUED`.
- A `Last Updated` date.
- A `History` section with at least one entry.

Source: SPEC.md Section 3.1; SPEC.md Section 3.2.

### REQ-07: Semantic Artifact Inclusion

At least one example deliverable SHOULD include a `_SEMANTIC.md` file demonstrating the semantic lens artifact.

**Modality note:** This requirement uses SHOULD rather than MUST. See Guidance for rationale on this modality choice (Lensing Items A-001, E-003). If elevated to MUST, acceptance criteria below would become mandatory.

**Acceptance criteria** (when included):
- The `_SEMANTIC.md` file MUST contain at minimum the Matrix A and Matrix B tables (the two canonical/input matrices).
- The file MUST parse as valid Markdown without structural errors.
- Content SHOULD demonstrate the matrix construction pattern consistent with the Chirality Semantic Algebra framework.

Source: PLAN.md Section 2; _SEMANTIC.md format (**location TBD** -- formal schema specification for `_SEMANTIC.md` not yet published; criteria above derived from observed structure in existing `_SEMANTIC.md` files).

### REQ-08: Internal Consistency

Within each example execution root:

- Stable IDs (`PKG-XX`, `DEL-XX-YY`) MUST be internally consistent across folder names, `_CONTEXT.md`, `_STATUS.md`, and the example decomposition document.
- Lifecycle states in `_STATUS.md` MUST be plausible given the files present (e.g., a folder with document kit files should not be in `OPEN` state).

Source: SPEC.md Sections 3, 4; CONTRACT.md K-ID-1, K-STATUS-1.

### REQ-09: No Real Project Data

Example execution roots MUST NOT contain real project data, proprietary content, or credentials. All content MUST be synthetic or placeholder.

Source: **ASSUMPTION** (standard practice for test fixtures in public/shared repositories). **Rationale note:** This requirement is sourced from ASSUMPTION rather than a binding governance document because no explicit data-handling policy document exists in the current governance suite. The requirement reflects widely accepted practice for test fixtures. If a formal data policy is established, this requirement should be re-sourced to that document. (See Lensing Item F-001.)

### REQ-10: Regression Test Usability

Example execution roots MUST be usable as test fixtures by validation scripts and CI processes without requiring external setup or network access.

**Acceptance criteria:**
- Validation scripts from DEL-07-01 execute against the examples and exit with status 0 (no errors).
- No manual intervention is required between fixture setup and validation completion.
- No outbound network connections are required during validation.

Source: SOW-029; OBJ-006 ("repeatable operation"); **ASSUMPTION** (self-contained test fixtures). **Rationale note:** Like REQ-09, this requirement's ASSUMPTION source reflects standard engineering practice for regression fixtures. The acceptance criteria above make "usable" measurable. If a formal test-fixture policy is established, this requirement should be re-sourced. (See Lensing Items F-001, C-001.)

---

## Standards

| Standard / Document | Relevance | Accessibility |
|---------------------|-----------|---------------|
| `docs/SPEC.md` | Primary conformance target: execution root layout, deliverable folder layout, file schemas, validation checklist | Accessible |
| `docs/TYPES.md` | Canonical vocabulary, stable ID formats, lifecycle states | Accessible |
| `docs/CONTRACT.md` | Binding invariants (K-HIER-1, K-ID-1, K-STATUS-1, K-GHOST-1) | Accessible |
| `docs/DIRECTIVE.md` | Filesystem-as-state principle, design philosophy | Accessible |
| `docs/PLAN.md` | Description of `examples/` purpose and existing tooling context | Accessible |

---

## Verification

| Requirement | Verification Approach |
|-------------|----------------------|
| REQ-01: Execution Root Layout | Manual or automated inspection against SPEC.md Section 12.1 checklist |
| REQ-02: Package Folder Conformance | Manual or automated inspection against SPEC.md Section 12.2 checklist |
| REQ-03: Deliverable Folder Conformance | Manual or automated inspection against SPEC.md Section 12.3 checklist |
| REQ-04: Initialized Deliverable | Verify at least one deliverable folder contains all four document kit files and has state in {INITIALIZED, SEMANTIC_READY, IN_PROGRESS, CHECKING, ISSUED} per the lifecycle ordering in SPEC.md Section 3.2 |
| REQ-05: Filesystem-Safe Naming | Regex validation of folder names against `{ID}_{SanitizedLabel}` pattern |
| REQ-06: Lifecycle State Validity | Parse `_STATUS.md` files; verify state is in canonical enum; verify history section present |
| REQ-07: Semantic Artifact | Verify at least one `_SEMANTIC.md` file exists in example deliverable folders; verify file contains Matrix A and Matrix B tables; verify valid Markdown structure (Source: acceptance criteria defined above; formal `_SEMANTIC.md` schema **location TBD**) |
| REQ-08: Internal Consistency | Cross-check IDs across folder names, `_CONTEXT.md`, `_STATUS.md`, and decomposition document within each example |
| REQ-09: No Real Project Data | Manual review; optionally scan for credential patterns |
| REQ-10: Regression Usability | Run DEL-07-01 validation scripts against examples without network access; verify scripts exit with status 0 and no manual intervention required |

---

## Documentation

### Required Artifacts

| Artifact | Format | Purpose |
|----------|--------|---------|
| Example execution root(s) | Directory structure under `examples/` | Primary deliverable: conformance test fixtures |
| Example decomposition document(s) | Markdown (`.md`) | Decomposition document within each example `_Decomposition/` |
| Example `INIT.md` | Markdown | Session initialization parameters for each example root |
| Example deliverable metadata files | Markdown (`_STATUS.md`, `_CONTEXT.md`, `_DEPENDENCIES.md`, `_REFERENCES.md`) | Minimum viable fileset for each example deliverable |
| Example document kit files | Markdown (`Datasheet.md`, `Specification.md`, `Guidance.md`, `Procedure.md`) | For initialized deliverable demonstrations |
| Example `_SEMANTIC.md` | Markdown | Semantic lens artifact sample |
| TBD: Maintenance/usage documentation | Markdown | Instructions for updating examples and using them in regression testing |
