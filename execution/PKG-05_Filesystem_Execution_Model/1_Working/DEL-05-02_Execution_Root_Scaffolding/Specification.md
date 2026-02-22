# Specification -- DEL-05-02 Execution Root Scaffolding + Layout Conformance

## Scope

### Covered

This deliverable covers:

1. **Scaffolding** -- Logic that creates a valid execution-root directory tree from a decomposition document, including all required package subfolders, tool roots, and initialization files.
2. **Layout conformance** -- Verification that an existing execution root matches the canonical layout defined in `docs/SPEC.md` Section 1.
3. **Folder naming** -- Correct application of the `Sanitize(name)` rule (SPEC Section 10) when creating package and deliverable folders.
4. **Tool root presence** -- All tool roots listed in SPEC Section 1.2 are created and structurally correct.

### Excluded

- **Instruction root bundling and runtime access** -- covered by DEL-05-01.
- **Lifecycle state handling** (`_STATUS.md` transitions) -- covered by DEL-05-03.
- **Dependency tracking file contract** (v3.1 schema) -- covered by DEL-05-04.
- **Automated folder structure validator** (standalone CI tool) -- covered by DEL-08-03 (TBD scope). This deliverable provides test-level conformance checks, not a standalone external validator. **Note (A-003):** Acceptance criteria for this deliverable's conformance tests should explicitly delineate the boundary with DEL-08-03's standalone validator scope. See CON-03 in Guidance Conflict Table.
- **Deliverable content files** (Datasheet, Specification, Guidance, Procedure) -- written by agent pipeline (4_DOCUMENTS), not by scaffolding logic.
- **Minimum viable fileset** (`_STATUS.md`, `_CONTEXT.md`, `_DEPENDENCIES.md`, `_REFERENCES.md`, `_SEMANTIC.md`) -- written by PREPARATION agent, not by scaffolding logic directly. **ASSUMPTION:** Scaffolding creates the folder structure; PREPARATION populates deliverable-level metadata files. The boundary between scaffolding and PREPARATION is TBD and requires human ruling if overlapping.

## Requirements

### REQ-01: Execution Root Directory Tree Creation

The scaffolding logic MUST create the following top-level structure at the execution root:

```
{EXECUTION_ROOT}/
├── INIT.md
├── _Aggregation/
│   ├── _Archive/
│   └── _Templates/
├── _Change/
├── _Coordination/
├── _Decomposition/
│   └── _Archive/
├── _Estimates/
├── _Reconciliation/
├── _Archive/
├── _Scripts/
└── _Sources/
```

**Note (X-001):** `_Archive/` at the execution root is a top-level tool root, distinct from the `_Archive/` sub-directories that appear within `_Aggregation/`, `_Decomposition/`, and package subfolders. Both the top-level `_Archive/` and the sub-directory instances are required. Verify against SPEC Section 1 that these are indeed distinct entities with separate purposes.

**Source:** SPEC Section 1 (Execution Root Layout); SPEC Section 1.2 (Tool Roots).

### REQ-02: Package Folder Creation

For each package in the decomposition, the scaffolding logic MUST create a package folder with all required subfolders:

```
PKG-XX_{Sanitize(PackageName)}/
├── 0_References/
│   └── _Archive/
├── 1_Working/
│   └── _Archive/
├── 2_Checking/
│   ├── From/
│   └── To/
└── 3_Issued/
    └── _Archive/
```

**Note (E-002):** The normative strength for `0_References/`, `2_Checking/`, and `3_Issued/` subfolders is currently inconsistent across documents. This Specification shows them as part of the MUST-create structure (matching SPEC Section 1.1), but Datasheet Conditions and Procedure Step 7 use SHOULD. See CON-04 in Guidance Conflict Table for human ruling. Until resolved, scaffolding logic MUST create all subfolders listed above per the SPEC Section 1.1 layout diagram, which is the authoritative source.

**Source:** SPEC Section 1.1 (Package Folders).

### REQ-03: Deliverable Folder Creation

For each deliverable in the decomposition, the scaffolding logic MUST create a deliverable folder at the correct path:

```
{PKG-ID}_{PkgLabel}/1_Working/{DEL-ID}_{Sanitize(DeliverableName)}/
```

**Source:** SPEC Section 2 (Deliverable Folder Layout); SPEC Section 10.2 (Folder Naming).

**Note:** The deliverable folder itself is an empty container at scaffolding time. Population of metadata files (`_STATUS.md`, `_CONTEXT.md`, etc.) is performed by PREPARATION. **ASSUMPTION:** Scaffolding and PREPARATION may be invoked sequentially or as a single operation; the boundary is implementation-dependent.

### REQ-04: Folder Naming Sanitization

All folder names MUST apply the `Sanitize(name)` function defined in SPEC Section 10.1. The steps MUST be applied in the following declared order:

1. Replace any of `/`, `\`, `:`, `*`, `?`, `"`, `<`, `>`, `|` with `-`.
2. Collapse consecutive whitespace to a single space.
3. Trim leading/trailing whitespace.

**Note (X-002):** The sequential ordering is significant. For example, an input like `"a : b"` would first become `"a - b"` (step 1), then remain `"a - b"` (step 2, no consecutive whitespace), then remain `"a - b"` (step 3). Implementers must apply steps in the stated sequence, not simultaneously.

**Note (F-001):** **[TBD_QUESTION:]** Define expected behavior when `Sanitize(name)` produces an empty string (e.g., input consisting entirely of special characters such as `":::**"` would become `"---"` after step 1, which is non-empty; but an input of all whitespace like `"   "` would become `""` after trim). The specification should define whether an empty result is an error condition or produces a fallback label. Human ruling required.

**Source:** SPEC Section 10.1 (Sanitization Rule).

### REQ-05: INIT.md Creation

The scaffolding logic MUST create an `INIT.md` file at the execution root containing session initialization parameters.

**Source:** SPEC Section 12.1 (Valid Execution Root).

**Note:** The content schema of `INIT.md` is TBD. SPEC requires its existence but does not fully specify its content format. **ASSUMPTION:** Minimal content (e.g., date, decomposition reference, project name) is sufficient until a formal schema is defined.

**[TBD_QUESTION (A-001):]** Define the content schema for `INIT.md` beyond minimal existence. Specifically: what fields are mandatory vs optional? Is there a required Markdown structure (e.g., YAML frontmatter, heading hierarchy)? Does the schema need to support machine-parsing for downstream agents? Human ruling or SPEC amendment required.

### REQ-06: Tool Root Completeness

All tool roots listed in SPEC Section 1.2 MUST be present at the execution root after scaffolding:

| Tool Root | Required | Sub-structure |
|-----------|----------|---------------|
| `_Aggregation/` | YES | `_Archive/`, `_Templates/` |
| `_Change/` | YES | None documented |
| `_Coordination/` | YES | None documented (but see REQ-07 for `_COORDINATION.md`) |
| `_Decomposition/` | YES | `_Archive/` |
| `_Estimates/` | YES | None documented |
| `_Reconciliation/` | YES | None documented |
| `_Archive/` | YES | None documented (top-level tool root) |
| `_Scripts/` | YES | None documented |
| `_Sources/` | YES | TBD -- **[TBD_QUESTION (F-002):]** Check SPEC Section 1.2 for whether `_Sources/` requires any sub-structure (e.g., `_Archive/`). Other tool roots with documented content have sub-structure; completeness requires confirming `_Sources/` does not. |

**Source:** SPEC Section 1 (Execution Root Layout); SPEC Section 1.2 (Tool Roots).

### REQ-07: Coordination File Initialization

The `_Coordination/` tool root MUST contain a `_COORDINATION.md` file after scaffolding.

**Source:** SPEC Section 1 (layout shows `_Coordination/_COORDINATION.md`); SPEC Section 13 (Coordination Representation).

**Note:** Content may be a minimal template pending human selection of coordination representation. **ASSUMPTION.**

**Note (E-001):** Verification for this requirement should confirm not only the existence of `_COORDINATION.md` but also that it contains at minimum a recognizable template structure (e.g., a heading or placeholder that references SPEC Section 13 coordination representations). The acceptance criterion for "minimal template" should be defined. **[TBD_QUESTION:]** What constitutes a valid minimal `_COORDINATION.md`? Proposed minimum: a Markdown file containing at least a title heading and a placeholder for the human to select from SCHEDULE_FIRST, DEPENDENCY_TRACKED, or HYBRID.

### REQ-08: Idempotent Scaffolding

Scaffolding SHOULD be idempotent: re-running scaffolding on an existing execution root MUST NOT delete or overwrite existing content. Missing directories MAY be created; existing directories MUST be preserved.

**Note (A-002):** The normative strength of idempotency is ambiguous. This requirement uses SHOULD for the overall idempotency property but MUST NOT for the destructive sub-constraint. Guidance P3 and Procedure Steps 3-4 treat idempotency as mandatory behavior. See CON-05 in Guidance Conflict Table for human ruling on whether SHOULD should be elevated to MUST.

**Source:** **ASSUMPTION** -- inferred from DIRECTIVE Section 2.1 (filesystem is state) and CONTRACT K-SNAP-1 (immutable snapshots). Destructive re-scaffolding would violate the principle that filesystem is authoritative state.

### REQ-09: Layout Conformance Verification

The deliverable MUST include test coverage that verifies a scaffolded execution root matches the structure defined in SPEC Section 12:

- **12.1:** Valid Execution Root checks (package folder exists, `_Decomposition/` exists, `INIT.md` exists).
- **12.2:** Valid Package Folder checks (naming, required subfolders).
- **12.3:** Valid Deliverable Folder checks (naming, required metadata files -- post-PREPARATION).

**Note (A-003):** This deliverable's conformance tests cover test-level verification within the development workflow. The boundary with DEL-08-03 (standalone folder structure validator, SOW-034, TBD scope) is: this deliverable provides developer/CI test assertions; DEL-08-03 (if brought in scope) provides a standalone CLI tool. See CON-03 in Guidance Conflict Table.

**Source:** SPEC Section 12; SOW-015.

### REQ-10: Flat Hierarchy Enforcement

Scaffolding MUST NOT create nested packages (packages within packages). The hierarchy is flat: `package -> deliverable`.

**Source:** CONTRACT K-HIER-1; TYPES Section 1.

### REQ-11: Stable ID Preservation

Folder names MUST include the stable deliverable/package ID as a prefix. Folder renames MUST NOT change the ID portion.

**Source:** CONTRACT K-ID-1; TYPES Section 2.

### REQ-12: Error Handling During Scaffolding

**[TBD_QUESTION (B-002):]** The scaffolding logic SHOULD handle filesystem errors encountered during directory creation (e.g., permission denied, disk full, partial creation). The expected behavior is TBD. Candidate approaches:

- **Option A:** Atomic scaffolding -- roll back all created directories if any creation fails.
- **Option B:** Best-effort scaffolding -- create what is possible, report failures, and rely on idempotent re-run to complete.
- **Option C:** Fail-fast -- stop at first error and report; rely on idempotent re-run after the error condition is resolved.

**ASSUMPTION:** Option C (fail-fast) is most consistent with the idempotency requirement (REQ-08), as incomplete scaffolding can be safely re-run. Human ruling required for final approach.

**Source:** Inferred from REQ-08 (idempotency) and DIRECTIVE Section 2.1 (filesystem-as-state).

## Standards

| Standard / Governance Doc | Relevance | Accessibility |
|---------------------------|-----------|---------------|
| `docs/SPEC.md` Section 1 | Execution root layout definition | Accessible |
| `docs/SPEC.md` Section 10 | Filesystem-safe label sanitization | Accessible |
| `docs/SPEC.md` Section 11 | Snapshot and pointer conventions | Accessible |
| `docs/SPEC.md` Section 12 | Folder structure validation checklist | Accessible |
| `docs/CONTRACT.md` K-HIER-1 | Flat package hierarchy invariant | Accessible |
| `docs/CONTRACT.md` K-ID-1 | Stable ID invariant | Accessible |
| `docs/CONTRACT.md` K-SNAP-1 | Immutable snapshot invariant | Accessible |
| `docs/CONTRACT.md` K-WRITE-1 | Explicit write scope invariant | Accessible |
| `docs/DIRECTIVE.md` Section 2.1 | Filesystem-as-state design philosophy | Accessible |
| `docs/DIRECTIVE.md` Section 5 | Structural constraints table | Accessible |
| `docs/TYPES.md` Section 2 | Stable identifier formats | Accessible |

## Verification

| Requirement | Verification Approach |
|-------------|----------------------|
| REQ-01 | Test: scaffold a fresh execution root; verify all top-level directories and `INIT.md` exist |
| REQ-02 | Test: scaffold from a multi-package decomposition; verify each package has all required subfolders |
| REQ-03 | Test: scaffold from a decomposition with multiple deliverables; verify each deliverable folder exists at the correct path. **Note (C-001):** Include negative test with malformed decomposition input (e.g., missing columns, invalid IDs, duplicate entries) to verify parser robustness. |
| REQ-04 | Test: use package/deliverable names containing special characters; verify folder names are correctly sanitized. **Note (F-001):** Include edge case where sanitization would produce an empty string or whitespace-only result. **Note (X-002):** Verify step ordering produces correct output for inputs where order matters (e.g., `"a : b"`, `"  :::  "`). |
| REQ-05 | Test: verify `INIT.md` exists at execution root after scaffolding and contains at minimum the required fields (date, decomposition reference, project name) |
| REQ-06 | Test: verify all tool roots from SPEC Section 1.2 exist after scaffolding, including documented sub-structure (`_Aggregation/_Archive/`, `_Aggregation/_Templates/`, `_Decomposition/_Archive/`) |
| REQ-07 | Test: verify `_Coordination/_COORDINATION.md` exists after scaffolding and contains a recognizable template structure (at minimum: title heading and coordination representation placeholder per SPEC Section 13) |
| REQ-08 | Test: scaffold, add content to folders, re-scaffold; verify existing content is preserved |
| REQ-09 | Test: run validation checks from SPEC Section 12 against a scaffolded root; verify all checks pass |
| REQ-10 | Test: attempt to scaffold a decomposition with nested packages (if possible); verify rejection or flat creation |
| REQ-11 | Test: verify folder names include stable ID prefix; verify renaming human-label portion preserves ID |
| REQ-12 | TBD -- verification approach depends on human ruling for error handling strategy (see REQ-12) |

## Documentation

| Artifact | Type | Description |
|----------|------|-------------|
| Scaffolding source code | CODE | Implementation of execution-root creation logic |
| Conformance test suite | TEST | Automated tests for layout correctness per SPEC Section 12 |
| Sanitization unit tests | TEST | Tests for the `Sanitize(name)` function including edge cases (empty result, step ordering) |
| Idempotency tests | TEST | Tests verifying non-destructive re-scaffolding |
| Decomposition parsing tests | TEST | Tests verifying correct parsing of decomposition input, including malformed input handling |
| Developer documentation | DOC | Description of scaffolding API/CLI, inputs, outputs, and integration points |
