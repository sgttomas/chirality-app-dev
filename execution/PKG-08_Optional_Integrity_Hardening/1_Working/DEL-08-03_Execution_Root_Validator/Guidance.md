# Guidance — DEL-08-03

## Purpose

This deliverable exists to close a gap identified in PLAN.md Section 3.3: "Missing files or unexpected structures are currently detected only during agent runs. A standalone validator enables pre-run checks and CI integration."

The execution root folder structure is the physical substrate of the entire Chirality filesystem-as-state model (DIRECTIVE.md Section 2.1). Without automated validation, structural violations are caught late (during agent execution) or not at all (silent drift). An automated validator serves two roles:

1. **Pre-run gating:** Verify that an execution root is structurally sound before agent pipeline runs, preventing agents from failing mid-execution due to missing files or malformed folders.
2. **CI integration:** Enable continuous integration pipelines to catch structural regressions as part of the development workflow.

Source: PLAN.md Section 3.3; DIRECTIVE.md Section 2.1 (filesystem-as-state); CONTRACT.md K-STATUS-1 (canonical lifecycle indicator).

## Principles

### P1: Rules Are Already Defined -- Do Not Invent New Ones

The validation rules are fully specified in SPEC.md Section 12. The validator's job is to faithfully implement those rules, not to extend them. Any desire to add rules beyond what SPEC.md defines should result in a proposal to update SPEC.md first, then implement.

Source: PLAN.md Section 3.3 ("The validation rules are fully defined.").

### P2: Severity Follows Normative Keywords

SPEC.md uses MUST and SHOULD keywords (per AGENT_HELPS_HUMANS.md conventions). The validator should map these to ERROR and WARNING respectively:

- **MUST** rules (violation = ERROR): structural problems that make the execution root non-conformant.
- **SHOULD** rules (violation = WARNING): recommended structures whose absence is tolerable but worth flagging.

Source: SPEC.md Section 12 (implicit from MUST/SHOULD language in Sections 12.1, 12.2, 12.3).

### P3: Read-Only, Non-Destructive

The validator MUST NOT modify the filesystem. It reads and reports only. This aligns with the principle that agents and tools should not silently alter state (DIRECTIVE.md Section 2.4, evidence over plausibility).

**ASSUMPTION: this principle is inferred from the tool's nature as a validator, not from an explicit statement in sources.**

### P4: Fail Fast, Report All

The validator should collect all findings across the entire execution root before reporting, rather than stopping at the first error. This enables operators to fix multiple issues in a single pass.

**ASSUMPTION: standard validation tool behavior; not explicitly stated in sources.**

### P5: Error Messages Should Be Actionable

> **[Lensing X-001]** Validator output messages should be designed to support human debugging. Each finding should identify: (a) which rule failed (e.g., REQ-01b), (b) which path is affected (e.g., `/path/to/execution-root/_Decomposition/`), and (c) what was expected (e.g., "directory must exist"). This enables operators to locate and resolve issues without needing to cross-reference the specification manually.

**ASSUMPTION: standard validation tool design principle; not explicitly stated in sources. Complements P4 (Fail Fast, Report All) by ensuring that the collected findings are individually useful.**

Source: Guidance.md Principles section (gap identified by semantic lensing -- no existing principle addressed error message design).

## Considerations

### C1: Scope Status Is TBD

SOW-034 is currently in TBD status (Decomposition SSOW; Open Issue OI-034). This deliverable can be drafted and scaffolded, but should not be ISSUED until the human flips SOW-034 to IN. If SOW-034 is flipped to OUT, this deliverable should be retired.

Source: Decomposition SSOW (SOW-034: TBD); Open Issues table (OI-034).

### C2: Relationship to DEL-08-02 (Dependencies.csv Schema Linter)

Both DEL-08-02 and DEL-08-03 are validation tools in PKG-08. Their scopes are complementary:

- **DEL-08-02** validates the *content* of `Dependencies.csv` files against the v3.1 schema.
- **DEL-08-03** validates the *folder structure* of the execution root, including file presence.

The boundary question is: how deeply should DEL-08-03 inspect `Dependencies.csv`? The Specification proposes that DEL-08-03 performs only a minimal header check (presence of `RegisterSchemaVersion` column with value `v3.1`), deferring full schema linting to DEL-08-02.

> **[Lensing C-001]** The phrase "valid v3.1 schema headers" in REQ-05b is broader than the implementation assumption of "minimal header check." The Specification should tighten the wording to match the intended scope. If only `RegisterSchemaVersion` presence/value is checked, the requirement text should say so explicitly. If a defined set of column headers is required, those should be enumerated.

Source: SPEC.md Section 12.3 ("Dependencies.csv with valid v3.1 schema headers"); Decomposition DEL-08-02 and DEL-08-03 descriptions.

### C3: Relationship to DEL-07-02 (Example Execution Roots)

DEL-07-02 maintains example execution roots under `examples/` for regression and conformance testing. These examples could serve as test fixtures for this validator. Conversely, this validator could be used to validate that the example execution roots themselves remain conformant.

Source: Decomposition DEL-07-02 ("Maintain/update `examples/` execution roots used for regression/conformance testing").

### C4: Lifecycle State Depth

SPEC.md Section 12.3 requires checking that `_STATUS.md` contains "a valid lifecycle state." The validator must parse `_STATUS.md` to extract the `Current State` field and check it against the valid state enum. This is a shallow content check, not full format validation.

> **[Lensing B-003]** The concept of state ordering (which states are "above" INITIALIZED) is used in REQ-04 but the ordering semantics should be explicitly referenced. The canonical ordering is defined in SPEC.md Section 3.2: `OPEN` < `INITIALIZED` < `SEMANTIC_READY` < `IN_PROGRESS` < `CHECKING` < `ISSUED`. Implementers should reference SPEC.md Section 3.2 directly rather than relying on implicit ordering knowledge.

The question of whether to also validate `_CONTEXT.md` header fields against the decomposition is a deeper check that goes beyond SPEC Section 12's explicit requirements. **ASSUMPTION: `_CONTEXT.md` presence is checked; content validation of `_CONTEXT.md` fields is out of scope for this deliverable.**

Source: SPEC.md Section 12.3; SPEC.md Section 3.2 (valid states and ordering).

### C5: Tool Root Validation

SPEC.md Section 1.2 lists expected tool roots (`_Aggregation/`, `_Change/`, `_Coordination/`, etc.) but Section 12 does not include tool root validation as an explicit checklist item. The validator MAY choose to validate tool root presence as a WARNING-level check, but this would be an extension beyond the current SPEC checklist.

> **[Lensing C-002]** The reason SPEC.md Section 12 omits tool root validation despite Section 1.2 listing expected tool roots is not documented in the sources. Possible explanations include: (a) tool roots are created on-demand by agents and may not exist in a newly scaffolded execution root, making their absence non-indicative of a structural problem; (b) tool root presence is a runtime concern rather than a structural one; or (c) it is an oversight. **ASSUMPTION: tool root validation is intentionally excluded from SPEC Section 12 because tool roots are dynamic/optional structures; this assumption cannot be confirmed without human input.** If this is an oversight, a SPEC.md Section 12 update should be proposed.

**ASSUMPTION: tool root validation is not in the initial scope. If desired, it should be proposed as an addition to SPEC.md Section 12.**

### C6: Language and Runtime Choice

The decomposition and PLAN.md do not specify an implementation language. The repo includes JavaScript/TypeScript (Next.js + Electron) and validation scripts in `.mjs`. Python is mentioned in PLAN.md Section 3.2 as a candidate for the schema linter. The choice should align with the project's existing tooling and CI environment.

**ASSUMPTION: implementation language is TBD, pending human decision.**

### C7: Performance and Scalability

> **[Lensing F-003]** No performance or scalability criteria are defined for this validator. For a tool that walks filesystems, performance with large execution roots (many packages, many deliverables) is a reasonable consideration. However, given the "Low" effort estimate (PLAN.md Section 3.3) and the typical size of Chirality execution roots (tens of packages, hundreds of deliverables at most), performance constraints are unlikely to be a concern. **ASSUMPTION: no explicit performance requirement is needed. If a constraint is later identified (e.g., execution root with thousands of deliverables), it should be added to the Specification.**

Source: PLAN.md Section 3.3 (effort estimate); Decomposition (S context envelope suggests low complexity).

## Trade-offs

| Trade-off | Option A | Option B | Recommendation |
|-----------|----------|----------|----------------|
| Validation depth for `Dependencies.csv` | Full v3.1 schema validation | Minimal header presence check | Option B (defer full validation to DEL-08-02) |
| Tool root validation | Include as WARNING checks | Exclude (not in SPEC Section 12) | Option B for initial implementation; propose SPEC update if desired |
| `_STATUS.md` validation depth | State enum only | Full format validation (heading, date, history) | Option A initially (matches SPEC 12.3 language); deeper checks can be added later |
| Output format | Human-readable text only | JSON + human-readable | TBD -- depends on CI integration requirements |
| `_CONTEXT.md` validation | Presence only | Field-level validation against decomposition | Presence only (SPEC 12.3 does not require field-level checks) |
| Label sanitization checks | Include (SPEC Section 10) | Exclude (not in SPEC Section 12 checklist) | TBD -- human must decide if in scope (see Conflict Table CT-001) |

## Examples

### Example: Valid Execution Root (Passing)

```
my-project/
  INIT.md
  _Decomposition/
    ProjectDecomposition_2026-01-01.md
  PKG-01_Build/
    0_References/
    1_Working/
      DEL-01-01_Build_Baseline/
        _STATUS.md          (Current State: INITIALIZED)
        _CONTEXT.md
        _DEPENDENCIES.md
        _REFERENCES.md
        Datasheet.md
        Specification.md
        Guidance.md
        Procedure.md
    2_Checking/
    3_Issued/
```

Expected output: 0 errors, 0 warnings.

Source: SPEC.md Section 12 (all checklist items satisfied).

### Example: Structural Violations (Failing)

```
my-project/
  _Decomposition/               (empty -- no decomposition document)
  PKG-01_Build/
    1_Working/
      DEL-01-01_Build_Baseline/
        _STATUS.md              (Current State: INITIALIZED)
        _CONTEXT.md
                                 (missing: _DEPENDENCIES.md, _REFERENCES.md)
                                 (missing: Datasheet.md -- required for INITIALIZED state)
```

Expected output:
- ERROR: `INIT.md` missing (REQ-01d)
- ERROR: `_Decomposition/` contains no decomposition documents (REQ-01c)
- WARNING: `0_References/` missing in PKG-01_Build (REQ-02c)
- WARNING: `2_Checking/` missing in PKG-01_Build (REQ-02d)
- WARNING: `3_Issued/` missing in PKG-01_Build (REQ-02e)
- ERROR: `_DEPENDENCIES.md` missing in DEL-01-01 (REQ-03e)
- ERROR: `_REFERENCES.md` missing in DEL-01-01 (REQ-03f)
- ERROR: `Datasheet.md` missing in DEL-01-01 (state is INITIALIZED) (REQ-04a)
- ERROR: `Specification.md` missing in DEL-01-01 (state is INITIALIZED) (REQ-04b)
- ERROR: `Guidance.md` missing in DEL-01-01 (state is INITIALIZED) (REQ-04c)
- ERROR: `Procedure.md` missing in DEL-01-01 (state is INITIALIZED) (REQ-04d)

Source: SPEC.md Section 12 (rule-by-rule application).

### Example: Invalid Input Path

```
$ validate-structure /nonexistent/path
ERROR: Input path does not exist or is not a directory: /nonexistent/path
Exit code: 1
```

Source: REQ-08d **[Lensing F-002]**.

## Conflict Table (for human ruling)

| Conflict ID | Conflict | Source A | Source B | Impacted sections | Proposed Authority (PROPOSAL) | Human Ruling |
|-------------|----------|----------|----------|-------------------|-------------------------------|--------------|
| CT-001 | Datasheet References row 4 lists SPEC.md Section 10 (label sanitization rules) as relevant, but Specification contains no requirement to validate label sanitization. Either add a label sanitization requirement or clarify the reference as context-only. | Datasheet.md, References table row 4 ("defines filesystem-safe label sanitization rules") | Specification.md, Requirements section (no label sanitization REQ) | Datasheet References row 4; Specification Scope (Excludes); Specification REQ-06; Guidance Trade-offs table | Human must decide if label sanitization validation is in scope. If yes, add REQ to Specification. If no, annotate Datasheet reference as context-only. **[Lensing X-002, X-003]** | TBD |
