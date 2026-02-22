# Guidance -- DEL-08-02 Dependencies.csv v3.1 Schema Linter

## Purpose

This deliverable exists because schema violations in `Dependencies.csv` files are currently caught only by agent-internal quality checks during DEPENDENCIES agent runs. An external, standalone linter enables:

1. **CI-level validation** -- schema conformance can be checked in automated pipelines, independent of agent execution.
2. **Drift detection** -- as the number of deliverables grows, inconsistencies across registers become harder to spot manually. A linter provides systematic coverage.
3. **Developer confidence** -- anyone editing or generating `Dependencies.csv` (agent or human) can validate their output immediately.

(Source: `docs/PLAN.md` Section 3.2)

This deliverable supports **OBJ-007** (optional integrity hardening loop) and covers **SOW-033**. Both are currently TBD scope, meaning this deliverable is a candidate for inclusion but not yet committed.

(Source: Decomposition SSOW; OI-033)

---

## Principles

### P1: Schema Is Fully Specified -- Implement, Do Not Interpret

The v3.1 schema is fully defined in `docs/SPEC.md` Section 6. The linter should implement the schema rules as written, not interpret or extend them. Where the schema is ambiguous (e.g., column ordering), the linter should be permissive and document the choice.

(Source: `docs/SPEC.md` Section 6; `docs/PLAN.md` Section 3.2 -- "The schema is fully specified.")

### P2: Errors vs. Warnings

The linter should distinguish between:
- **Errors**: violations of MUST-level rules (column presence, required fields, enum validity, identity uniqueness, provenance on ACTIVE rows, row classification rules). These cause a non-zero exit code.
- **Warnings**: violations of SHOULD-level rules (IMPLEMENTS_NODE cardinality, EvidenceQuote presence, legacy value usage, unrecognized extension columns). These are reported but do not cause failure.

This distinction aligns with the normative keyword usage in `docs/SPEC.md`.

### P3: Read-Only, Non-Destructive

The linter reads CSV files and produces reports. It MUST NOT modify, correct, or rewrite any file. This keeps it safe for CI integration and consistent with the principle that agents propose and humans approve.

(Source: `docs/DIRECTIVE.md` Section 2.3 -- human authority at every gate)

### P4: Standalone, No Runtime Dependencies on Chirality App

The linter should be invocable as a standalone CLI tool. It should not require the Chirality desktop app, a running server, or any Chirality-specific runtime environment. This makes it suitable for CI pipelines and developer workstations alike.

(Source: Decomposition DEL-08-02 description -- "standalone schema linter"; `docs/PLAN.md` Section 3.2)

### P5: Low Effort, High Immediate Value

Per `docs/PLAN.md` Section 4, the schema linter is positioned as a low-effort, high-value item with no dependencies on other optional hardening deliverables. Implementation should stay bounded and avoid scope creep into graph generation, staleness detection, or other PKG-08 deliverables.

---

## Considerations

### C1: Python as Implementation Language

`docs/PLAN.md` Section 3.2 describes the linter as "a Python script." This is taken as directional guidance rather than a hard requirement. Python is a reasonable choice because:
- Standard `csv` module handles parsing.
- No external dependencies needed for core validation.
- Widely available in CI environments.

**ASSUMPTION (ASMP-C1)**: Python 3.x is the target runtime. Minimum version 3.8+ is a reasonable floor given ecosystem norms, but this is not specified in governance. (Source: `docs/PLAN.md` Section 3.2; ecosystem convention)

### C2: CSV Parsing Edge Cases

`Dependencies.csv` files are standard CSV. The linter should handle:
- UTF-8 encoding (with or without BOM).
- Quoted fields containing commas.
- Empty optional fields (should parse as empty string, not absent).
- Trailing newlines.

These are standard CSV parsing considerations, not specific to the v3.1 schema.

### C3: Relationship to DEL-05-04 (Dependency Tracking File Contract)

DEL-05-04 (PKG-05) covers the dependency tracking file contract itself -- the data model, the integration glue, the generation mechanics. DEL-08-02 is a downstream consumer: it reads the files DEL-05-04 defines and validates them. The linter's validation rules are derived from the same schema (`docs/SPEC.md` Section 6) that DEL-05-04 implements.

**ASSUMPTION (ASMP-C3)**: If DEL-05-04 results in schema changes (unlikely given G7 approval, but possible via change control), the linter would need to be updated accordingly. (Source: Decomposition; `docs/SPEC.md` Section 6)

### C4: Relationship to DEL-08-03 (Execution Root Folder Structure Validator)

Both DEL-08-02 and DEL-08-03 are standalone validation tools in PKG-08. They share a similar pattern (walk filesystem, check rules, report violations) but operate at different levels:
- DEL-08-02: validates the content schema of individual CSV files.
- DEL-08-03: validates the folder structure of the execution root.

There may be an opportunity to share CLI infrastructure (argument parsing, output formatting, exit code conventions) but this is not required.

### C5: CI Integration Pattern

The linter should support CI integration via:
- Non-zero exit code on validation failure (standard for CI checks).
- Machine-readable output (JSON) for programmatic consumption. **ASSUMPTION (ASMP-C5a)**
- Batch mode to scan an entire execution root. **ASSUMPTION (ASMP-C5b)**

Specific CI platform integration (GitHub Actions workflow files, etc.) is TBD and may be out of scope for this deliverable.

### C6: Script Placement Decision

The canonical script location is TBD. Procedure Step D1 identifies `_Scripts/validate_dependencies.py` as a candidate location per SPEC Section 1 (which designates `_Scripts/` for deployment and analysis scripts). However, this has not been confirmed by human decision. (Enriched per Semantic Lensing D-001)

**ASSUMPTION (ASMP-C6)**: `_Scripts/validate_dependencies.py` is the candidate path. The human should confirm this location before integration, considering:
- Whether `_Scripts/` is the correct category for validation/linting tools (vs. analysis scripts).
- Whether the test suite should reside alongside the script or in a separate `tests/` directory.
- Whether a different naming convention is preferred (e.g., `lint_dependencies.py`).

(Source: `docs/SPEC.md` Section 1 -- `_Scripts/` directory purpose; **location TBD** -- specific script placement guidance not found in SPEC)

### C7: Rule Catalog Completeness Verification

When building the validation rule catalog (Procedure Step A1), the implementer should verify completeness by tracing each rule in `docs/SPEC.md` Section 6 to a corresponding entry in the catalog, not merely by counting to 15. A traceability check ensures that no SPEC rule is missed and that each catalog entry has a valid upstream source. (Enriched per Semantic Lensing X-003)

**Recommended approach:**
1. Enumerate all checkable rules from SPEC Section 6 (subsections 6.1 through 6.8).
2. Map each SPEC rule to a Specification requirement (REQ-01 through REQ-16).
3. Confirm bi-directional traceability: every SPEC rule maps to a requirement, and every requirement maps to a SPEC rule (or is explicitly marked **ASSUMPTION**).

(Source: `docs/SPEC.md` Section 6 -- authoritative schema; Specification REQ-01 through REQ-16)

---

## Rationale for ASSUMPTION-tagged Requirements

The following requirements are tagged **ASSUMPTION** because they have no authoritative governance source. They are included based on engineering best practice for CI-level tooling. If they are deemed unnecessary, they may be demoted to optional guidance or removed. (Enriched per Semantic Lensing C-001)

| Requirement | Rationale for Inclusion | Governance Status |
|-------------|------------------------|-------------------|
| **REQ-13** (Exit Codes) | Standard CLI convention for CI integration; without distinct exit codes, CI pipelines cannot distinguish between validation failure and tool failure | No governance source -- **ASSUMPTION**; standard UNIX CLI practice |
| **REQ-14** (Machine-Readable Output) | JSON output enables programmatic consumption by CI systems and downstream tooling; without it, CI integration requires parsing human-readable text | No governance source -- **ASSUMPTION**; CI best practice |
| **REQ-15** (Batch Mode) | Implied by "CI-level validation" and "catch drift across deliverables" (`docs/PLAN.md` Section 3.2); without batch mode, each file must be linted individually | Weak governance signal from `docs/PLAN.md` Section 3.2 -- **ASSUMPTION** |
| **REQ-16** (Performance) | No formal performance requirement exists; included as a SHOULD-level awareness item for CI pipeline feasibility | No governance source -- **ASSUMPTION** |

**Human ruling requested:** Confirm, adjust severity (MUST/SHOULD), or remove these requirements.

---

## Trade-offs

### T1: Strictness vs. Permissiveness

The linter could be strict (reject any deviation from the schema) or permissive (accept common deviations with warnings). The recommended approach is:
- **Strict on MUST rules** (errors).
- **Permissive on SHOULD rules** (warnings).
- **Silent on unspecified behavior** (e.g., column order, whitespace in values).

This balances usability with schema enforcement.

### T2: Single-File vs. Cross-File Validation

The v3.1 schema includes rules that can be checked within a single file (most rules) and rules that conceptually span files (e.g., `TargetDeliverableID` resolves to an existing deliverable per K-DEP-2). Cross-file resolution is closer to DEL-08-04 (dependency graph generation) territory.

**Recommendation**: The linter should validate single-file rules only. Cross-file resolution (target ID existence) should be deferred to graph-level tooling or flagged as an optional enhancement.

### T3: Error Reporting Granularity

Options:
- Report first error and stop (fast but less useful).
- Report all errors (slower but gives a complete picture).

**Recommendation**: Report all errors. For CI use, a complete violation list is more actionable than iterative fix-and-rerun cycles.

---

## Assumption Register

The following consolidated register tracks all ASSUMPTIONs across the four production documents. Each ASSUMPTION uses a consistent format: **ASSUMPTION (ID)**: description. (Enriched per Semantic Lensing X-002)

| ID | Document(s) | Statement | Rationale | Status |
|----|------------|-----------|-----------|--------|
| ASMP-C1 | Datasheet, Guidance, Procedure | Python 3.8+ is the target runtime | `docs/PLAN.md` Section 3.2 says "a Python script"; 3.8+ is ecosystem floor | TBD -- human confirmation needed |
| ASMP-C3 | Guidance | Schema changes from DEL-05-04 would require linter update | G7-approved schema is stable, but change control is possible | Accepted risk |
| ASMP-C5a | Guidance, Specification | Machine-readable (JSON) output for CI integration | Best practice for CI-level tooling; not explicitly required by governance | TBD -- confirm or demote |
| ASMP-C5b | Guidance, Specification | Batch mode for scanning execution root | Implied by `docs/PLAN.md` Section 3.2 "CI-level validation" | TBD -- confirm or demote |
| ASMP-C6 | Guidance, Procedure | Script location is `_Scripts/validate_dependencies.py` | SPEC Section 1 designates `_Scripts/` for deployment/analysis scripts | TBD -- human confirmation needed |
| ASMP-IMP | Datasheet | Implementation language is Python | `docs/PLAN.md` Section 3.2 states "a Python script" | Strong governance signal; likely confirmed |
| ASMP-NET | Datasheet | Linter operates offline; no outbound network | Consistent with DIRECTIVE Section 5 structural constraints | High confidence |
| ASMP-INTEG | Datasheet | Standalone invocation; no import into other runtime code | Decomposition description says "standalone" | High confidence |
| ASMP-ORDER | Specification | Column order tolerance (physical ordering not mandated) | SPEC 6.2 uses column numbers for logical, not physical, ordering | TBD -- human confirmation welcome |
| ASMP-LIFECYCLE | Specification | LastSeen >= FirstSeen (logical consistency) | Not explicitly stated in SPEC but logically required | High confidence |
| ASMP-EXIT | Specification | Exit code convention (0/1/2) | Standard UNIX CLI practice; not in governance | TBD -- confirm or adjust |
| ASMP-JSON | Specification | SHOULD support JSON output | CI best practice | TBD -- confirm or demote |
| ASMP-BATCH | Specification | SHOULD support batch scanning | Implied by PLAN Section 3.2 | TBD -- confirm or demote |

---

## Examples

TBD -- Examples will be derived from the `examples/` execution root fixtures and purpose-built test fixtures once implementation begins.

---

## Conflict Table (for human ruling)

| Conflict ID | Conflict | Source A | Source B | Impacted Sections | Proposed Authority (PROPOSAL) | Human Ruling |
|-------------|---------|----------|----------|-------------------|-------------------------------|-------------|
| CT-001 | REQ-09 EXECUTION row rules: SPEC 6.4 says linter "MUST validate EXECUTION row rules" using "preferred execution enums," but "preferred" implies a SHOULD-level concept. It is unclear whether non-preferred DependencyType values in EXECUTION rows should produce errors (MUST violation) or warnings (SHOULD violation). | `docs/SPEC.md` Section 6.4 (MUST validate) | `docs/SPEC.md` Section 6.4 ("preferred" enums -- SHOULD-level implication) | Specification REQ-09; Verification REQ-09; Guidance P2 | Specification.md -- human should rule on normative level | TBD |
