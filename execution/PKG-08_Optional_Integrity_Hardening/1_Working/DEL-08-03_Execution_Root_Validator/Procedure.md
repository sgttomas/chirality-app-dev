# Procedure — DEL-08-03

## Purpose

This procedure describes how to produce and validate the Execution Root Folder Structure Validator deliverable (DEL-08-03), and how to use the validator once produced.

## Prerequisites

| # | Prerequisite | Source |
|---|-------------|--------|
| 1 | SOW-034 must be flipped to IN before this deliverable is actively worked | Decomposition SSOW (SOW-034: TBD); OI-034 |
| 2 | `docs/SPEC.md` Section 12 must be accessible (defines all validation rules) | _REFERENCES.md; Decomposition DEL-08-03 description |
| 3 | `docs/TYPES.md` Section 2 must be accessible (defines ID format rules) | _REFERENCES.md |
| 4 | `docs/SPEC.md` Sections 1-3 must be accessible (defines folder layout and lifecycle states) | _REFERENCES.md |
| 5 | Implementation language/runtime decision must be made | **ASSUMPTION: TBD pending human decision** |
| 6 | At least one valid execution root must be available for testing (e.g., `examples/` fixtures from DEL-07-02 or the project's own execution root) | Decomposition DEL-07-02 |

## Steps

### Part A: Produce the Validator

#### A1. Confirm Scope Status

> **[Lensing E-001]** The scope confirmation step has two distinct decision paths. Follow the appropriate path based on the current SOW-034 status:

1. **If SOW-034 is IN:** Proceed to Step A2.
2. **If SOW-034 is TBD:** The human must explicitly authorize work to proceed while scope is TBD. Record the authorization decision (who authorized, date, rationale) in `_MEMORY.md` before proceeding. Without explicit authorization, do not proceed.
3. **If SOW-034 is OUT:** Stop. This deliverable should be retired per OI-034 resolution path. Update `_STATUS.md` per lifecycle rules and notify ORCHESTRATOR.

Source: Decomposition Open Issues (OI-034); Decomposition SSOW (SOW-034).

#### A2. Select Implementation Language

1. Review the project's existing scripting conventions (`.mjs` validation scripts in `frontend/scripts/`, Python candidates mentioned in PLAN.md Section 3.2).
2. Select a language/runtime that aligns with the CI environment.
3. Record the decision in `_MEMORY.md`.

**ASSUMPTION: language decision is TBD.**

#### A3. Implement Execution Root Checks (REQ-01)

1. Implement check REQ-01a: scan for at least one `PKG-XX_{Label}/` directory.
2. Implement check REQ-01b: verify `_Decomposition/` directory exists.
3. Implement check REQ-01c: verify `_Decomposition/` contains at least one `.md` file (decomposition document).
4. Implement check REQ-01d: verify `INIT.md` exists.
5. Each failing check emits an ERROR-level finding with the check ID, the affected path, and a human-readable message describing what was expected (per Guidance P5).

Source: SPEC.md Section 12.1.

#### A4. Implement Package Folder Checks (REQ-02)

For each directory matching `PKG-XX_{Label}/` pattern:

1. Implement check REQ-02a: validate the folder name matches `PKG-XX_{Label}` with zero-padded numeric `XX`.
2. Implement check REQ-02b: verify `1_Working/` subfolder exists (ERROR).
3. Implement check REQ-02c: verify `0_References/` subfolder exists (WARNING).
4. Implement check REQ-02d: verify `2_Checking/` subfolder exists (WARNING).
5. Implement check REQ-02e: verify `3_Issued/` subfolder exists (WARNING).

Source: SPEC.md Section 12.2; TYPES.md Section 2.1.

#### A5. Implement Deliverable Folder Checks (REQ-03, REQ-04, REQ-05)

For each directory matching `DEL-XX-YY_{Label}/` under `1_Working/`:

1. Implement check REQ-03a: validate the folder name matches `DEL-XX-YY_{Label}` with hyphen-separated, zero-padded numeric segments.
2. Implement check REQ-03b: verify `_STATUS.md` exists (ERROR).
3. Implement check REQ-03c: if `_STATUS.md` exists, parse it and verify `Current State` is one of the valid lifecycle states (`OPEN`, `INITIALIZED`, `SEMANTIC_READY`, `IN_PROGRESS`, `CHECKING`, `ISSUED`).
4. Implement check REQ-03d: verify `_CONTEXT.md` exists (ERROR).
5. Implement check REQ-03e: verify `_DEPENDENCIES.md` exists (ERROR).
6. Implement check REQ-03f: verify `_REFERENCES.md` exists (ERROR).
7. If lifecycle state is >= `INITIALIZED` (using the canonical ordering from SPEC.md Section 3.2: `OPEN` < `INITIALIZED` < `SEMANTIC_READY` < `IN_PROGRESS` < `CHECKING` < `ISSUED` -- see Specification REQ-04 Note **[Lensing B-003]**):
   - Implement checks REQ-04a through REQ-04d: verify `Datasheet.md`, `Specification.md`, `Guidance.md`, `Procedure.md` exist.
8. Determine if the deliverable is dependency-tracked:
   - TBD -- the mechanism for determining "dependency-tracked" status needs definition (see Specification REQ-05 Note **[Lensing A-002]**). **ASSUMPTION: presence of `Dependencies.csv` file or a tracking mode indicator in `_DEPENDENCIES.md`.**
   - If dependency-tracked, implement checks REQ-05a and REQ-05b.

Source: SPEC.md Section 12.3; SPEC.md Section 3.2.

#### A6. Implement ID Format Validation (REQ-06)

1. Implement regex patterns for `PKG-XX` and `DEL-XX-YY` validation per TYPES.md Section 2.1.
2. Optionally validate that deliverable ID prefix matches parent package ID (REQ-06c -- **ASSUMPTION**, pending human confirmation per Specification **[Lensing A-003]**).

Source: TYPES.md Section 2.1.

#### A7. Implement Report Output (REQ-07)

1. Implement structured report collecting all findings (ERROR and WARNING).
2. Output the report in human-readable format.
3. Include a summary line with total error and warning counts (REQ-07d). **[Lensing F-001]**
4. Return exit code 0 if no ERRORs, non-zero if any ERRORs present.
5. Optionally implement machine-readable output mode (JSON) for CI consumption (REQ-08c).
6. Ensure each finding message identifies the rule ID, affected path, and expected condition (per Guidance P5). **[Lensing X-001]**

Source: **ASSUMPTION: standard validation script conventions.**

#### A8. Implement CLI Interface (REQ-08)

1. Accept execution root path as a required command-line argument.
2. Validate the input path exists and is a directory; produce a clear error and exit non-zero if not (REQ-08d). **[Lensing F-002]**
3. Optionally accept flags for output format, verbosity, or warning-as-error mode.
4. Print usage help when invoked without arguments or with `--help`.

Source: PLAN.md Section 3.3 ("standalone validator enables pre-run checks and CI integration").

### Part B: Test the Validator

#### B1. Create Test Fixtures

1. Create a valid execution root fixture (all checks pass).
2. Create execution root fixtures with specific violations:
   - Missing `INIT.md`
   - Empty `_Decomposition/`
   - No package folders
   - Package with invalid ID format
   - Package missing `1_Working/`
   - Deliverable with invalid ID format
   - Deliverable missing required metadata files
   - `INITIALIZED` deliverable missing document kit files
   - `_STATUS.md` with invalid lifecycle state
   - Non-existent input path (REQ-08d). **[Lensing F-002]**
   - Input path is a file, not a directory (REQ-08d). **[Lensing F-002]**
3. Optionally reuse `examples/` fixtures from DEL-07-02 as additional test cases.

Source: Specification.md Verification table.

#### B2. Write Automated Tests

1. Write tests covering all REQ checks per the Specification Verification table.
2. Verify ERROR vs. WARNING severity classification.
3. Verify exit code behavior.
4. Verify report content accuracy (including summary line per REQ-07d). **[Lensing F-001]**
5. Verify that each finding message includes rule ID, affected path, and expected condition (per Guidance P5). **[Lensing X-001]**

#### B3. Run Full Test Suite

1. Execute all automated tests.
2. Verify all tests pass.
3. Record test results.

#### B4. Run Self-Validation Acceptance Test

> **[Lensing D-002, X-004]** Run the validator against the project's own execution root (or a fully conformant fixture) and confirm zero ERROR findings and zero false-positive WARNINGs. This satisfies Specification REQ-09.

1. Execute the validator against a known-conformant execution root.
2. Verify output shows zero ERRORs.
3. Record the result as acceptance evidence.

Source: Specification.md REQ-09; Procedure.md Verification "Overall" row.

### Part C: Document the Validator

#### C1. Write Usage Documentation

1. Document CLI invocation syntax and options.
2. Document output format (human-readable and machine-readable if applicable).
3. Document CI integration instructions (e.g., adding to a CI pipeline step).
4. Document the mapping from SPEC.md Section 12 rules to validator checks.

## Verification

| Step | Verification |
|------|-------------|
| A3-A6 | All REQ checks implemented and individually testable |
| A7 | Report correctly classifies ERROR vs. WARNING findings; summary line present (REQ-07d) |
| A8 | Script runs from command line with path argument; produces clear error on invalid path (REQ-08d) |
| B1-B3 | All test fixtures produce expected findings; full test suite passes |
| B4 | Self-validation against conformant root produces zero ERRORs and zero false-positive WARNINGs (REQ-09) |
| C1 | Usage documentation is complete and accurate |
| Overall | Validator correctly validates the project's own execution root (or `examples/` roots) without false positives or missed violations |

## Records

| Record | Description |
|--------|-------------|
| Validator script | The implemented validation script (SCRIPT artifact) |
| Test suite | Automated tests with fixtures (TEST artifact) |
| Usage documentation | CLI and CI integration guide (DOC artifact) |
| Test execution results | Evidence of test suite passing |
| Self-validation results | Evidence of zero false positives against conformant root (REQ-09 acceptance) **[Lensing D-002]** |
| `_MEMORY.md` entries | Key decisions (language choice, scope boundary decisions, scope authorization if SOW-034 is TBD, etc.) |
