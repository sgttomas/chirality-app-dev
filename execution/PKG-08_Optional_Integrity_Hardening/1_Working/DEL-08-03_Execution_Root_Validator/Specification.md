# Specification — DEL-08-03

## Scope

### What This Deliverable Covers

This deliverable implements an automated folder structure validator that walks an execution root and validates its structure against the checklist defined in `docs/SPEC.md` Section 12. The validator is intended to run as a standalone pre-run check and to integrate into CI pipelines.

Source: Decomposition DEL-08-03 ("Implement folder validator per SPEC checklist"); PLAN.md Section 3.3.

### What This Deliverable Excludes

- Content validation within files (e.g., verifying `_STATUS.md` format beyond state validity, or verifying `_CONTEXT.md` field accuracy against the decomposition). **ASSUMPTION: content-level validation beyond state enum checking is out of scope unless sources indicate otherwise.**
- `Dependencies.csv` schema validation -- covered by DEL-08-02 (Dependencies.csv v3.1 Schema Linter).
- Content hash verification for `_REFERENCES.md` -- covered by DEL-08-01.
- Dependency graph generation -- covered by DEL-08-04.
- Any remediation or auto-fix capability. **ASSUMPTION: the validator reports findings; it does not modify the filesystem.**
- Label sanitization conformance checking (SPEC.md Section 10) -- TBD pending human decision. See Guidance Conflict Table CT-001. **[Lensing X-003]**

## Requirements

### REQ-01: Execution Root Validation

The validator MUST check the following conditions for a valid execution root (SPEC.md Section 12.1):

| Check | Rule | Severity | Source |
|-------|------|----------|--------|
| REQ-01a | At least one `PKG-XX_{Label}/` folder exists | ERROR | SPEC 12.1 |
| REQ-01b | `_Decomposition/` folder exists | ERROR | SPEC 12.1 |
| REQ-01c | `_Decomposition/` contains at least one decomposition document | ERROR | SPEC 12.1 |
| REQ-01d | `INIT.md` exists with session parameters | ERROR | SPEC 12.1 |

### REQ-02: Package Folder Validation

The validator MUST check the following conditions for each package folder (SPEC.md Section 12.2):

| Check | Rule | Severity | Source |
|-------|------|----------|--------|
| REQ-02a | Folder is named `{PKG-ID}_{PkgLabel}/` with a valid `PKG-XX` identifier | ERROR | SPEC 12.2; TYPES 2.1 |
| REQ-02b | Contains `1_Working/` subfolder | ERROR | SPEC 12.2 |
| REQ-02c | `0_References/` subfolder exists | WARNING (SHOULD) | SPEC 12.2 |
| REQ-02d | `2_Checking/` subfolder exists | WARNING (SHOULD) | SPEC 12.2 |
| REQ-02e | `3_Issued/` subfolder exists | WARNING (SHOULD) | SPEC 12.2 |

### REQ-03: Deliverable Folder Validation

The validator MUST check the following conditions for each deliverable folder (SPEC.md Section 12.3):

| Check | Rule | Severity | Source |
|-------|------|----------|--------|
| REQ-03a | Folder is named `{DEL-ID}_{DelLabel}/` with a valid `DEL-XX-YY` identifier | ERROR | SPEC 12.3; TYPES 2.1 |
| REQ-03b | Contains `_STATUS.md` | ERROR | SPEC 12.3 |
| REQ-03c | `_STATUS.md` contains a valid lifecycle state (`OPEN`, `INITIALIZED`, `SEMANTIC_READY`, `IN_PROGRESS`, `CHECKING`, `ISSUED`) | ERROR | SPEC 12.3; SPEC 3.2 |
| REQ-03d | Contains `_CONTEXT.md` | ERROR | SPEC 12.3 |
| REQ-03e | Contains `_DEPENDENCIES.md` | ERROR | SPEC 12.3 |
| REQ-03f | Contains `_REFERENCES.md` | ERROR | SPEC 12.3 |

### REQ-04: Initialized Deliverable Checks

When a deliverable's `_STATUS.md` indicates state >= `INITIALIZED`, the validator MUST additionally check (SPEC.md Section 12.3):

| Check | Rule | Severity | Source |
|-------|------|----------|--------|
| REQ-04a | Contains `Datasheet.md` | ERROR | SPEC 12.3 |
| REQ-04b | Contains `Specification.md` | ERROR | SPEC 12.3 |
| REQ-04c | Contains `Guidance.md` | ERROR | SPEC 12.3 |
| REQ-04d | Contains `Procedure.md` | ERROR | SPEC 12.3 |

**Note on lifecycle state ordering [Lensing B-003]:** The ">= INITIALIZED" condition uses the canonical lifecycle state ordering defined in SPEC.md Section 3.2: `OPEN` < `INITIALIZED` < `SEMANTIC_READY` < `IN_PROGRESS` < `CHECKING` < `ISSUED`. States at `INITIALIZED` or later in this ordering trigger the additional document checks. Implementers should reference SPEC.md Section 3.2 for the authoritative ordering definition rather than relying on implicit knowledge.

### REQ-05: Dependency-Tracked Deliverable Checks

When a deliverable is dependency-tracked, the validator MUST additionally check (SPEC.md Section 12.3):

| Check | Rule | Severity | Source |
|-------|------|----------|--------|
| REQ-05a | Contains `Dependencies.csv` | ERROR | SPEC 12.3 |
| REQ-05b | `Dependencies.csv` has valid v3.1 schema headers | ERROR | SPEC 12.3 |

**Note [Lensing A-002, C-001]:** Two aspects of REQ-05 require human clarification:

1. **Detection mechanism (TBD):** The mechanism for determining whether a deliverable is "dependency-tracked" is not defined. **ASSUMPTION: presence of `Dependencies.csv` file or a `Tracking Mode` indicator in `_DEPENDENCIES.md` (e.g., `FULL_GRAPH` or `MINIMAL`).** The Specification should define the detection rule so implementers know when to trigger REQ-05 checks. Source: Specification.md REQ-05; Procedure.md Step A5.8.

2. **Header validation scope (TBD):** The phrase "valid v3.1 schema headers" in REQ-05b is broader than the implementation assumption of a "minimal header check." **ASSUMPTION: this check is limited to verifying the presence of the `RegisterSchemaVersion` column with value `v3.1`; full schema linting is deferred to DEL-08-02.** The Specification should tighten the wording to match the intended scope. Source: Specification.md REQ-05b; Guidance.md C2.

### REQ-06: ID Format Validation

The validator MUST validate identifier formats per TYPES.md Section 2.1:

| Check | Rule | Source |
|-------|------|--------|
| REQ-06a | Package IDs match pattern `PKG-XX` where XX is zero-padded numeric | TYPES 2.1 |
| REQ-06b | Deliverable IDs match pattern `DEL-XX-YY` where XX and YY are zero-padded numeric, hyphen-separated | TYPES 2.1 |
| REQ-06c | Deliverable ID prefix (`XX`) matches parent package ID | **ASSUMPTION: implied by hierarchy; SPEC does not state this explicitly as a validation rule. [Lensing A-003] Human must confirm whether this is a requirement or should be removed.** |

### REQ-07: Report Output

| Check | Rule | Source |
|-------|------|--------|
| REQ-07a | The validator MUST produce a structured report distinguishing ERROR and WARNING findings | **ASSUMPTION: inferred from severity distinction in SPEC 12 (MUST vs. SHOULD)** |
| REQ-07b | The validator MUST return a non-zero exit code when any ERROR finding is present | **ASSUMPTION: standard CI convention for validation scripts** |
| REQ-07c | Report format is TBD (human-readable text, JSON, or both) | TBD |
| REQ-07d | The report SHOULD include a summary line reporting total counts of errors and warnings (e.g., "N errors, M warnings") | **[Lensing F-001]** ASSUMPTION: standard validation tool convention; provides a conformance assurance signal at a glance for operators and CI consumers. Source: Specification.md REQ-07 (severity distinction implies countable findings). |

> **[Lensing A-004, B-001]** REQ-07c (report format) is a blocking TBD. Acceptance criteria for report output format cannot be defined, and compliance cannot be verified, until the human decides the format. If JSON is selected, the minimal schema or required fields should also be specified (see also REQ-08c below). Source: Specification.md REQ-07c; _SEMANTIC_LENSING.md items A-004, B-001.

### REQ-08: CLI Integration Readiness

| Check | Rule | Source |
|-------|------|--------|
| REQ-08a | The validator MUST be executable as a standalone script from the command line | PLAN.md Section 3.3 ("standalone validator enables pre-run checks and CI integration") |
| REQ-08b | The validator MUST accept an execution root path as input | PLAN.md Section 3.3 |
| REQ-08c | The validator SHOULD support a machine-readable output mode for CI consumption | **ASSUMPTION: standard CI integration pattern** |
| REQ-08d | The validator MUST produce a clear error message and non-zero exit code when the input path does not exist or is not a directory | **[Lensing F-002]** ASSUMPTION: essential error handling for the most basic failure mode (invalid input path). Source: standard CLI tool conventions; no explicit SPEC source. |

> **[Lensing D-001]** REQ-08c (machine-readable output mode): if implemented, the definition of what constitutes a valid machine-readable mode should be specified. If JSON, a minimal schema or required fields should be documented. Currently the verification approach ("verify machine-readable output mode if implemented") defers the definition. Source: Specification.md REQ-08c; Verification table.

### REQ-09: Acceptance Criterion -- Self-Validation

> **[Lensing D-002]** The validator SHOULD be able to validate the project's own execution root and produce zero false positives against a structurally conformant root. This formalizes the informal check already present in Procedure.md Verification table ("Overall" row) as a testable acceptance criterion.

| Check | Rule | Source |
|-------|------|--------|
| REQ-09a | Running the validator against a fully conformant execution root MUST produce zero ERROR findings | **[Lensing D-002, X-004]** Source: Procedure.md Verification "Overall" row (informal); SPEC.md Section 12 (rules define conformance). |

## Standards

| Standard / Reference | Applicability | Source Access |
|---------------------|---------------|---------------|
| `docs/SPEC.md` Section 12 | Primary: defines all validation rules | Accessible |
| `docs/SPEC.md` Sections 1-2 | Defines the canonical folder structures being validated | Accessible |
| `docs/SPEC.md` Section 3.2 | Defines valid lifecycle states and their ordering | Accessible |
| `docs/SPEC.md` Section 10 | Defines filesystem-safe label sanitization (in-scope status TBD) | Accessible |
| `docs/TYPES.md` Section 2 | Defines stable identifier format rules | Accessible |
| `docs/CONTRACT.md` K-STATUS-1 | `_STATUS.md` is the canonical lifecycle indicator | Accessible |

## Verification

| Requirement | Verification Approach |
|-------------|----------------------|
| REQ-01 (Execution Root) | Test with valid execution root, empty directory, directory missing `_Decomposition/`, directory missing `INIT.md`, directory with no packages |
| REQ-02 (Package Folder) | Test with valid packages, package missing `1_Working/`, package with invalid ID format, package missing SHOULD-level subfolders |
| REQ-03 (Deliverable Folder) | Test with valid deliverable, deliverable missing each required file individually, deliverable with invalid ID format, deliverable with invalid lifecycle state in `_STATUS.md` |
| REQ-04 (Initialized Checks) | Test with `INITIALIZED`+ state deliverable missing document kit files; test with `OPEN` state deliverable (should not check for document kit) |
| REQ-05 (Dependency-Tracked) | Test with deliverable that has `Dependencies.csv` with valid headers; test with missing file; test with invalid headers. **[Lensing X-005]** Also test edge cases: empty `Dependencies.csv`, file with only headers, file with `RegisterSchemaVersion` column but wrong value. |
| REQ-06 (ID Formats) | Test with valid IDs, malformed IDs (missing zero-padding, wrong separators, non-numeric segments). **[Lensing X-005]** Also test edge cases: single-digit unpadded IDs, IDs with extra segments, mixed case. |
| REQ-07 (Report) | Verify report distinguishes ERROR/WARNING; verify exit codes; verify summary line includes error and warning counts (REQ-07d). **[Lensing X-005]** Also test: report with zero findings, report with only warnings (exit code 0), report with mixed errors and warnings. |
| REQ-08 (CI) | Run script from command line with valid and invalid paths; verify machine-readable output mode if implemented; verify clear error on non-existent path (REQ-08d). **[Lensing X-005]** Also test: path argument is a file (not directory), no argument provided, `--help` flag. |
| REQ-09 (Self-Validation) | Run validator against the project's own execution root (or a fully conformant fixture) and confirm zero ERROR findings. **[Lensing D-002, X-004]** Additionally confirm zero false-positive WARNINGs if fixture is fully conformant. |

> **[Lensing X-005]** The verification table above has been normalized to include specific edge-case scenarios for all REQ groups, addressing the uneven granularity identified in the original version (where REQ-01 and REQ-02 had specific fixture scenarios but REQ-07 and REQ-08 were generic).

## Documentation

| Artifact | Description | Status |
|----------|-------------|--------|
| Validator script | Standalone script implementing all REQ checks | TBD (anticipated: SCRIPT) |
| Test suite | Automated tests covering all REQ verification approaches | TBD (anticipated: TEST) |
| Usage documentation | CLI usage, options, output format, CI integration guide | TBD (anticipated: DOC) |
| Example execution roots | May leverage existing `examples/` fixtures (DEL-07-02) or create dedicated test fixtures | TBD |
