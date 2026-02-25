# Procedure -- DEL-08-02 Dependencies.csv v3.1 Schema Linter

## Purpose

This procedure describes the steps to produce, test, and integrate the Dependencies.csv v3.1 schema linter. It also describes how to use the linter once produced.

---

## Prerequisites

| # | Prerequisite | Source |
|---|-------------|--------|
| PRE-01 | SOW-033 flipped to IN scope (SCA-002) | `execution/_Coordination/NEXT_INSTANCE_STATE.md` |
| PRE-02 | `docs/SPEC.md` Section 6 (v3.1 schema) must be accessible and current | `docs/SPEC.md` |
| PRE-03 | Python 3.8+ runtime available on the development/CI environment -- **ASSUMPTION (ASMP-C1)** per Guidance C1 | `docs/PLAN.md` Section 3.2; Guidance C1 |
| PRE-04 | Access to `examples/` execution root for test fixture material | `docs/PLAN.md` Section 2 |

---

## Steps

### Phase A: Implementation

#### Step A1 -- Define Validation Rule Catalog

Review `docs/SPEC.md` Section 6 and enumerate all checkable rules. Categorize each rule as ERROR (MUST-level) or WARNING (SHOULD-level). Cross-reference with `Specification.md` REQ-01 through REQ-16.

**Completeness verification approach:** Do not rely solely on counting requirements. Trace each SPEC Section 6 subsection (6.1 through 6.8) to a catalog entry, and confirm bi-directional traceability: every SPEC rule maps to a catalog entry, and every catalog entry maps to a SPEC rule or is marked **ASSUMPTION**. See Guidance C7 for detailed approach. (Enriched per Semantic Lensing X-003)

**Verification**: Rule catalog covers all specification requirements with bi-directional traceability to SPEC Section 6.

#### Step A2 -- Implement CSV Parser

Implement CSV parsing that handles:
- UTF-8 encoding (with/without BOM).
- Standard CSV quoting rules.
- Header row extraction and column mapping.

Use Python standard library `csv` module. No external dependencies for core parsing.

**Verification**: Parser correctly reads a well-formed Dependencies.csv file.

#### Step A3 -- Implement Column Presence Check (REQ-01, REQ-03)

Validate that all 29 core columns are present. Accept extension columns. Warn on unrecognized columns.

**Verification**: Unit tests per REQ-01 and REQ-03.

#### Step A4 -- Implement Per-Row Validation

For each data row, validate:
- `RegisterSchemaVersion` = `v3.1` (REQ-04).
- Enum columns contain only canonical values (REQ-05).
- Legacy values produce warnings (REQ-06).
- Required fields are non-empty (REQ-12).
- Date fields are valid ISO dates; `LastSeen` >= `FirstSeen` (REQ-10).

**Verification**: Unit tests per REQ-04, REQ-05, REQ-06, REQ-10, REQ-12.

#### Step A5 -- Implement Cross-Row Validation

Validate:
- `DependencyID` uniqueness (REQ-07).
- `FromDeliverableID` consistency across rows (REQ-07).
- `DependencyID` format compliance (REQ-07).
- `TargetDeliverableID` presence/absence rules based on `TargetType` (REQ-07).

**Verification**: Unit tests per REQ-07.

#### Step A6 -- Implement Row Classification Validation (REQ-09)

Validate ANCHOR vs. EXECUTION row rules:
- ANCHOR: `AnchorType` != `NOT_APPLICABLE`; `DependencyType` = `OTHER`.
- EXECUTION: `AnchorType` = `NOT_APPLICABLE`; `DependencyType` uses preferred enums.

**Note:** The error vs. warning classification for non-preferred EXECUTION DependencyType values is TBD pending human ruling on CT-001 (see Guidance Conflict Table). Implement with a configurable severity level if possible.

**Verification**: Unit tests per REQ-09.

#### Step A7 -- Implement Provenance Validation (REQ-08)

Validate that ACTIVE rows have non-empty `EvidenceFile` and `SourceRef` (or explicit `location TBD`). Warn when `EvidenceQuote` is empty.

**Verification**: Unit tests per REQ-08.

#### Step A8 -- Implement Structural Checks (REQ-11)

Warn when the file does not contain exactly one ACTIVE `IMPLEMENTS_NODE` ANCHOR row.

**Verification**: Unit test per REQ-11.

#### Step A9 -- Implement CLI Interface (REQ-13, REQ-14, REQ-15)

Implement command-line interface:
- Single-file mode: `python validate_dependencies.py <path-to-Dependencies.csv>`
- Batch mode: `python validate_dependencies.py --scan <execution-root-path>` (REQ-15) -- **ASSUMPTION (ASMP-BATCH)**
- Output format flag: `--format {text|json}` (REQ-14) -- **ASSUMPTION (ASMP-JSON)**
- Exit codes: 0 (pass), 1 (errors found), 2 (file not found / unreadable) (REQ-13) -- **ASSUMPTION (ASMP-EXIT)**

**Error handling for linter failures:** The CLI MUST handle its own runtime errors (e.g., Python exceptions from severely malformed CSV input that crashes the parser, permission errors, encoding errors) distinctly from validation errors. Recommended behavior: (Enriched per Semantic Lensing C-002)
- Exit code `2` for file-access failures (not found, permission denied, encoding unreadable).
- Exit code `2` (or a distinct code, e.g., `3`) for unexpected internal errors (parser crash on malformed input). The linter SHOULD catch exceptions, report a diagnostic message to stderr, and exit cleanly rather than producing a Python traceback.
- **TBD -- human ruling on whether internal errors use exit code `2` (file-level problem) or a separate exit code `3` (tool failure).**

**Verification**: Integration tests per REQ-13, REQ-14, REQ-15. Include a test with a severely malformed CSV (e.g., binary content) to verify the linter handles parser exceptions gracefully.

### Phase B: Testing

#### Step B1 -- Create Test Fixtures

Create a set of Dependencies.csv fixture files:
- `valid_minimal.csv` -- minimum valid file (core columns, one ANCHOR + one EXECUTION row).
- `valid_full.csv` -- comprehensive valid file (all columns, extension columns, multiple row types).
- `valid_reordered.csv` -- valid file with deliberately shuffled column order (for REQ-02 testing).
- `invalid_missing_columns.csv` -- missing one or more core columns.
- `invalid_enum_values.csv` -- invalid enum values in various columns.
- `invalid_identity.csv` -- duplicate DependencyID; format violations; TargetDeliverableID inconsistencies.
- `invalid_provenance.csv` -- ACTIVE rows with empty EvidenceFile/SourceRef.
- `invalid_classification.csv` -- ANCHOR row with NOT_APPLICABLE AnchorType; EXECUTION row rule violations.
- `invalid_malformed.csv` -- severely malformed content (e.g., binary data or truncated CSV) to test error handling. (Enriched per Semantic Lensing C-002)
- `warning_legacy.csv` -- legacy DependencyType and Direction values.
- `warning_implements_node.csv` -- zero or multiple IMPLEMENTS_NODE rows.

**Verification**: Fixture set covers all specification requirements.

#### Step B2 -- Run Unit Tests

Execute unit test suite. All tests must pass.

**Verification**: Test runner reports 100% pass rate.

#### Step B3 -- Run Integration Tests

Execute integration tests for CLI interface, exit codes, output format, and batch mode. Include error-handling tests for malformed input.

**Verification**: Integration tests pass.

### Phase C: Documentation

#### Step C1 -- Write Usage Documentation

Document:
- CLI invocation syntax (single-file and batch modes).
- Exit code meanings (including error-handling behavior for malformed input).
- Output format (human-readable and JSON).
- CI integration guidance (example pipeline step).
- Known limitations and assumptions (cross-reference Guidance Assumption Register).

**Verification**: Documentation covers all CLI features and is consistent with implementation.

### Phase D: Integration

#### Step D1 -- Place Script in Repository

Place the linter script and test suite in an appropriate location. Candidate location:
- `_Scripts/validate_dependencies.py` (per SPEC Section 1 -- `_Scripts/` for deployment and analysis scripts). **ASSUMPTION (ASMP-C6)** -- see Guidance C6 for decision criteria.
- Tests alongside or in a `tests/` subdirectory.

**Human confirmation required** on script placement before this step. (Enriched per Semantic Lensing D-001)

**Verification**: Script is accessible from execution root.

#### Step D2 -- Validate Against Example Execution Root

Run the linter in batch mode against `examples/` execution root to confirm it works with real project fixtures.

**Verification**: Linter produces expected results on example data.

---

## Verification

| Step | Verification |
|------|-------------|
| A1 | Rule catalog complete with bi-directional SPEC traceability |
| A2 | Parser reads well-formed CSV |
| A3-A8 | Unit tests pass for each requirement |
| A9 | CLI integration tests pass (including error-handling tests) |
| B1 | Fixture set covers requirements (including malformed input) |
| B2 | Unit tests 100% pass |
| B3 | Integration tests pass |
| C1 | Documentation complete and consistent |
| D1 | Script placed in repository (location confirmed by human) |
| D2 | Linter validates example data correctly |

---

## Records

| Record | Description |
|--------|-------------|
| Validation script | `validate_dependencies.py` (or equivalent) committed to repository |
| Test suite | Unit + integration tests committed alongside script |
| Test fixtures | CSV fixture files committed alongside tests (including malformed-input fixtures) |
| Usage documentation | CLI/CI usage doc committed at `execution/_Scripts/README.md` |
| `_STATUS.md` update | State transition recorded upon completion |
