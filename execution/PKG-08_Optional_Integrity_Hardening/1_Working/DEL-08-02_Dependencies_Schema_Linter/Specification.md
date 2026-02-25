# Specification -- DEL-08-02 Dependencies.csv v3.1 Schema Linter

## Scope

### What This Deliverable Covers

This deliverable covers the design, implementation, and testing of a standalone schema linter for `Dependencies.csv` files conforming to the v3.1 register schema defined in `docs/SPEC.md` Section 6. The linter enables CI-level validation of dependency registers across all deliverable folders in an execution root.

(Source: Decomposition DEL-08-02 description; `docs/PLAN.md` Section 3.2)

### What This Deliverable Excludes

- Modification or correction of invalid CSV files (the linter is read-only and reports violations only).
- Dependency extraction or population (that is the DEPENDENCIES agent's responsibility per `docs/CONTRACT.md` K-DEP-1).
- Aggregation of dependency registers into a project-level graph (that is DEL-08-04, SOW-035).
- Validation of folder structure (that is DEL-08-03, SOW-034).
- Runtime integration into the Chirality desktop app (the linter is standalone).

### Scope Contingency

SOW-033 was ruled **IN** by human decision on 2026-02-24 (OI-033 resolved, SCA-002). This deliverable is fully actionable.

---

## Requirements

### REQ-01: Column Presence Validation

The linter MUST validate that all 29 core columns defined in `docs/SPEC.md` Section 6.2 are present in the CSV header row.

**Source:** `docs/SPEC.md` Section 6.2 ("Core Columns (MUST be present)")

### REQ-02: Column Order Tolerance

The linter SHOULD accept core columns in any order (the schema specifies column numbers but does not explicitly mandate physical ordering). **ASSUMPTION** -- the numbering in SPEC Section 6.2 indicates logical ordering; physical CSV column order tolerance is a usability decision.

**Acceptance Criteria:** The linter SHOULD treat any permutation of the 29 core column names in the header row as valid. The verification test MUST exercise at least two distinct column orderings: (a) the logical order from SPEC Section 6.2, and (b) a deliberately shuffled order. Both MUST pass without errors. (Enriched per Semantic Lensing A-002)

### REQ-03: Extension Column Acceptance

The linter MUST accept the defined extension columns (`EstimateImpactClass`, `ConsumerHint`) when present and MUST NOT reject CSV files containing them. The linter SHOULD warn on unrecognized columns that are not in either the core or extension set.

**Source:** `docs/SPEC.md` Section 6.2 ("Extension Columns (MAY be present; non-breaking)")

### REQ-04: RegisterSchemaVersion Validation

The linter MUST validate that every row contains `RegisterSchemaVersion` = `v3.1`.

**Source:** `docs/SPEC.md` Section 6.1 ("MUST be present in every row and set to `v3.1`")

### REQ-05: Enum Value Validation

The linter MUST validate that enum-typed columns contain only canonical values defined in `docs/SPEC.md` Section 6.3. The following enum families MUST be checked:

| Column | Valid Values | Source |
|--------|-------------|--------|
| `DependencyClass` | `ANCHOR`, `EXECUTION` | SPEC 6.3 |
| `AnchorType` | `IMPLEMENTS_NODE`, `TRACES_TO_REQUIREMENT`, `NOT_APPLICABLE` | SPEC 6.3 |
| `Direction` | `UPSTREAM`, `DOWNSTREAM` | SPEC 6.3 |
| `DependencyType` | `PREREQUISITE`, `INTERFACE`, `HANDOVER`, `CONSTRAINT`, `ENABLES`, `OTHER`, `COORDINATION` (legacy), `INFORMATION` (legacy) | SPEC 6.3 |
| `TargetType` | `DELIVERABLE`, `PACKAGE`, `WBS_NODE`, `REQUIREMENT`, `DOCUMENT`, `EQUIPMENT`, `EXTERNAL`, `UNKNOWN` | SPEC 6.3 |
| `Explicitness` | `EXPLICIT`, `IMPLICIT` | SPEC 6.3 |
| `SatisfactionStatus` | `TBD`, `PENDING`, `IN_PROGRESS`, `SATISFIED`, `WAIVED`, `NOT_APPLICABLE` | SPEC 6.3 |
| `Confidence` | `HIGH`, `MEDIUM`, `LOW` | SPEC 6.3 |
| `Origin` | `DECLARED`, `EXTRACTED` | SPEC 6.3 |
| `Status` | `ACTIVE`, `RETIRED` | SPEC 6.3 |

For extension columns:
| Column | Valid Values | Source |
|--------|-------------|--------|
| `EstimateImpactClass` | `BLOCKING`, `ADVISORY`, `INFO`, `TBD` | SPEC 6.2 |
| `ConsumerHint` | `TASK`, `TASK_ESTIMATING`, `AGGREGATION`, `RECONCILIATION`, `TBD` | SPEC 6.2 |

**Snapshot Verification Note:** The enum values listed above are a snapshot from `docs/SPEC.md` Section 6.3 as of the decomposition approval date (2026-02-21). Before implementation, the implementer MUST cross-verify these values against the current `docs/SPEC.md` Section 6.3 to confirm they remain accurate. If any discrepancy is found, update this table and record the verification date. **Status: TBD -- verification not yet performed.** (Enriched per Semantic Lensing X-001)

### REQ-06: Legacy Value Warning

The linter MUST emit a warning (not an error) when legacy `DependencyType` values (`COORDINATION`, `INFORMATION`) are encountered. The linter MUST emit a warning when legacy `Direction` values (`INBOUND`, `OUTBOUND`) are encountered.

**Source:** `docs/SPEC.md` Section 6.3 ("Do not emit in new extractions"); Section 6.7 (legacy compatibility)

### REQ-07: Identity Rule Validation

The linter MUST validate:
- `DependencyID` is unique within the file (SPEC 6.8).
- `DependencyID` format matches `DEP-{PKG}-{DEL}-{SEQ}` pattern (SPEC 6.8).
- `FromDeliverableID` is consistent across all rows (all rows in a single file represent the same host deliverable) (SPEC 6.8).
- When `TargetType=DELIVERABLE`: `TargetDeliverableID` MUST be non-empty (SPEC 6.8).
- When `TargetType` is not `DELIVERABLE`: `TargetDeliverableID` MUST be empty (SPEC 6.8).

**Source:** `docs/SPEC.md` Section 6.8

### REQ-08: Provenance Validation

The linter MUST validate that every ACTIVE row has:
- `EvidenceFile` is non-empty (or explicitly `location TBD`) (SPEC 6.5).
- `SourceRef` is non-empty (or explicitly `location TBD`) (SPEC 6.5).

The linter SHOULD warn when `EvidenceQuote` is empty for ACTIVE rows.

**Source:** `docs/SPEC.md` Section 6.5; `docs/CONTRACT.md` K-PROV-1

### REQ-09: Row Classification Validation

The linter MUST validate ANCHOR row rules:
- ANCHOR rows: `AnchorType` MUST NOT be `NOT_APPLICABLE` (SPEC 6.4).
- ANCHOR rows: `DependencyType` MUST be `OTHER` (SPEC 6.4).

The linter MUST validate EXECUTION row rules:
- EXECUTION rows: `AnchorType` MUST be `NOT_APPLICABLE` (SPEC 6.4).
- EXECUTION rows: `DependencyType` MUST use preferred execution enums (SPEC 6.4).

**Normative Keyword Clarification:** The phrase "preferred execution enums" in SPEC 6.4 creates ambiguity regarding whether use of non-preferred `DependencyType` values in EXECUTION rows is a MUST-level error or a SHOULD-level warning. The linter's treatment of this rule requires clarification. **TBD -- human ruling needed on whether non-preferred EXECUTION DependencyType values produce errors or warnings.** See Conflict Table in `Guidance.md` (CT-001). (Enriched per Semantic Lensing E-001, F-001)

**Verification Criteria for EXECUTION Rules:** Tests MUST enumerate which specific `DependencyType` values constitute "preferred execution enums" (Source: `docs/SPEC.md` Section 6.4 -- **location of preferred enum list TBD**) and verify that the linter correctly classifies uses of each value in an EXECUTION row. (Enriched per Semantic Lensing F-001)

**Source:** `docs/SPEC.md` Section 6.4

### REQ-10: Lifecycle Field Validation

The linter MUST validate:
- `FirstSeen` is a valid ISO date (`YYYY-MM-DD`) (SPEC 6.2).
- `LastSeen` is a valid ISO date (`YYYY-MM-DD`) (SPEC 6.2).
- `LastSeen` >= `FirstSeen` (logical consistency). **ASSUMPTION** -- not explicitly stated but logically required.
- `Status` is `ACTIVE` or `RETIRED` (SPEC 6.2).

**Source:** `docs/SPEC.md` Section 6.2, Section 6.6

### REQ-11: IMPLEMENTS_NODE Cardinality Check

The linter SHOULD warn when a file does not contain exactly one `IMPLEMENTS_NODE` ANCHOR row with `Status=ACTIVE`.

**Source:** `docs/SPEC.md` Section 6.4 ("Exactly one `IMPLEMENTS_NODE` row SHOULD exist per deliverable")

### REQ-12: Required Field Completeness

The linter MUST validate that columns marked "MUST" or "required" in SPEC Section 6.2 are non-empty for every row. Columns marked "optional" or "SHOULD" MAY be empty.

**Source:** `docs/SPEC.md` Section 6.2 (Required column)

### REQ-13: Exit Code Convention

The linter MUST return distinct exit codes:
- `0` = all checks pass (no errors; warnings may be present).
- `1` = one or more validation errors detected.
- `2` = file not found or unreadable.

**ASSUMPTION** -- standard CLI convention; not specified in governance docs. See Guidance section "Rationale for ASSUMPTION-tagged Requirements" for justification. (Cross-ref enriched per Semantic Lensing C-001)

### REQ-14: Machine-Readable Output

The linter SHOULD support machine-readable output (e.g., JSON) in addition to human-readable output, to facilitate CI integration.

**ASSUMPTION** -- best practice for CI-level tooling; not explicitly required by governance. See Guidance section "Rationale for ASSUMPTION-tagged Requirements" for justification. (Cross-ref enriched per Semantic Lensing C-001)

### REQ-15: Batch Mode

The linter SHOULD support scanning all `Dependencies.csv` files under an execution root (walk all `{PKG}/1_Working/{DEL}/Dependencies.csv` paths).

**ASSUMPTION** -- implied by "CI-level validation" and "catch drift across deliverables" (`docs/PLAN.md` Section 3.2). See Guidance section "Rationale for ASSUMPTION-tagged Requirements" for justification. (Cross-ref enriched per Semantic Lensing C-001)

### REQ-16: Performance Criteria

The linter has no formal performance requirement from governance sources. However, as CI-level tooling, the linter SHOULD execute within reasonable time and resource bounds to avoid blocking CI pipelines. **ASSUMPTION** -- no specific performance thresholds (execution time, memory usage) are mandated. If performance becomes a concern during implementation, define explicit thresholds. (Enriched per Semantic Lensing A-003)

---

## Standards

| Standard/Reference | Applicability | Accessible? |
|-------------------|---------------|-------------|
| `docs/SPEC.md` Section 6 (Dependencies.csv v3.1 Schema) | Primary -- defines the schema being linted | Yes |
| `docs/TYPES.md` Section 3 (Dependency Vocabulary) | Supporting -- defines canonical vocabulary | Yes |
| `docs/CONTRACT.md` (K-PROV-1, K-DEP-1, K-DEP-2, K-INVENT-1) | Governing invariants for dependency register integrity | Yes |
| `docs/PLAN.md` Section 3.2 | Describes this deliverable as a future hardening candidate | Yes |

---

## Verification

| Requirement | Verification Approach |
|-------------|----------------------|
| REQ-01 (Column Presence) | Unit test: valid CSV passes; CSV with missing core column fails |
| REQ-02 (Column Order) | Unit test: (a) CSV with SPEC Section 6.2 logical column order passes; (b) CSV with deliberately shuffled column order passes; (c) confirm both produce identical validation results |
| REQ-03 (Extension Columns) | Unit test: CSV with extension columns passes; CSV with unknown columns warns |
| REQ-04 (Schema Version) | Unit test: row with wrong version fails; row with `v3.1` passes |
| REQ-05 (Enum Values) | Unit test per enum family: valid values pass; invalid values fail. **Pre-implementation:** cross-verify enum snapshot against current `docs/SPEC.md` Section 6.3 |
| REQ-06 (Legacy Warning) | Unit test: legacy values produce warning, not error |
| REQ-07 (Identity Rules) | Unit tests: duplicate IDs fail; format mismatch fails; TargetDeliverableID consistency |
| REQ-08 (Provenance) | Unit test: empty EvidenceFile on ACTIVE row fails; `location TBD` passes |
| REQ-09 (Row Classification) | Unit test: ANCHOR with NOT_APPLICABLE AnchorType fails; EXECUTION row tests MUST enumerate specific preferred vs. non-preferred DependencyType values (TBD -- pending clarification of "preferred execution enums" in SPEC 6.4) |
| REQ-10 (Lifecycle Fields) | Unit test: invalid dates fail; LastSeen < FirstSeen fails |
| REQ-11 (IMPLEMENTS_NODE) | Unit test: zero or multiple IMPLEMENTS_NODE rows produce warning |
| REQ-12 (Required Fields) | Unit test: empty required field fails |
| REQ-13 (Exit Codes) | Integration test: verify exit codes for pass/fail/missing-file scenarios |
| REQ-14 (Machine Output) | Integration test: verify JSON output parses correctly |
| REQ-15 (Batch Mode) | Integration test: verify recursive scan finds all Dependencies.csv files |
| REQ-16 (Performance) | **ASSUMPTION** -- no formal performance test required; monitor CI execution time during integration testing |

---

## Deliverable Acceptance Criteria

The following criteria define when DEL-08-02 is considered complete as a deliverable (distinct from individual requirement verification). (Enriched per Semantic Lensing D-002)

| Criterion | Verification | Status |
|-----------|-------------|--------|
| All unit tests pass for REQ-01 through REQ-12 | Test runner reports 100% pass rate | TBD |
| All integration tests pass for REQ-13 through REQ-16 | Test runner reports 100% pass rate | TBD |
| Batch mode validates against `examples/` execution root | Linter produces expected results on example data | TBD |
| Usage documentation covers CLI features, exit codes, output formats, CI integration | Documentation review checklist (see Procedure Step C1) | TBD |
| All ASSUMPTIONs have been reviewed and either confirmed, resolved, or documented as accepted risks | Assumption register in Guidance reviewed | TBD |
| DOC artifact is complete and consistent with implementation | Documentation covers all implemented features and matches actual CLI behavior | TBD |

---

## Documentation

| Artifact | Description | Acceptance Criteria | Status |
|----------|-------------|---------------------|--------|
| SCRIPT | Validation script (Python) | Passes all unit and integration tests; exit codes conform to REQ-13 | TBD |
| TEST | Unit and integration test suite | Covers REQ-01 through REQ-16; fixture set exercises all requirement categories | TBD |
| DOC | Usage instructions (CLI, CI integration, exit codes, output format) | Covers all CLI features; consistent with implementation; reviewed for completeness (see Procedure Step C1 checklist) | TBD |
