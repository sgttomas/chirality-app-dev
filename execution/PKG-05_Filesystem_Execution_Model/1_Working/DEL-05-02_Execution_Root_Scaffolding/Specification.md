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
- **Automated folder structure validator** (standalone CI tool) -- covered by DEL-08-03 (TBD scope). This deliverable provides test-level conformance checks, not a standalone external validator. **Note (A-003):** Baseline boundary is resolved for current scope: DEL-05-02 keeps test-level conformance ownership while SOW-034 remains `TBD` and PKG-08 is non-driving; revisit only if SOW-034 is explicitly ruled `IN` (see Guidance CON-03 decision record).
- **Deliverable content files** (Datasheet, Specification, Guidance, Procedure) -- written by agent pipeline (4_DOCUMENTS), not by scaffolding logic.
- **Minimum viable fileset** (`_STATUS.md`, `_CONTEXT.md`, `_DEPENDENCIES.md`, `_REFERENCES.md`, `_SEMANTIC.md`) -- written by PREPARATION agent, not by scaffolding logic directly. Scaffolding creates the folder structure and initialization templates; PREPARATION populates deliverable-level metadata files.

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

**Note (E-002):** SPEC Section 1.1 defines the package scaffold that scaffolding logic must create. SPEC Section 12.2 uses SHOULD language for package-folder validity checks on existing roots, but DEL-05-02 creation behavior remains MUST for all subfolders listed above.

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

**Note (F-001):** If `Sanitize(name)` yields an empty string (for example, whitespace-only input), scaffolding MUST fail with `INVALID_REQUEST` and include field/value diagnostics. No fallback label is generated.

**Source:** SPEC Section 10.1 (Sanitization Rule).

### REQ-05: INIT.md Creation

The scaffolding logic MUST create an `INIT.md` file at the execution root containing session initialization parameters.

**Source:** SPEC Section 12.1 (Valid Execution Root).

**INIT.md minimum schema (DEL-05-02 implementation baseline):**
- Heading: `# Execution Init`
- `**Project Name:**`
- `**Initialized:**` (ISO date)
- `**Decomposition Reference:**` (execution-root-relative path)
- `**Coordination Mode:**` (`SCHEDULE_FIRST | DEPENDENCY_TRACKED | HYBRID`)
- Section: `## Session Parameters`

This schema is the implemented baseline for DEL-05-02 and can be expanded by governance updates.

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
| `_Sources/` | YES | No required sub-structure in current SPEC; directory presence only |

**Source:** SPEC Section 1 (Execution Root Layout); SPEC Section 1.2 (Tool Roots).

### REQ-07: Coordination File Initialization

The `_Coordination/` tool root MUST contain a `_COORDINATION.md` file after scaffolding.

**Source:** SPEC Section 1 (layout shows `_Coordination/_COORDINATION.md`); SPEC Section 13 (Coordination Representation).

**Note:** Content may be a minimal template pending human selection of coordination representation. **ASSUMPTION.**

**Note (E-001):** A valid minimal `_COORDINATION.md` contains a title heading, explicit representation value, dependency tracking mode, and a visible list of the three canonical representation options (`SCHEDULE_FIRST`, `DEPENDENCY_TRACKED`, `HYBRID`).

### REQ-08: Idempotent Scaffolding

Scaffolding MUST be idempotent: re-running scaffolding on an existing execution root MUST NOT delete or overwrite existing content. Missing directories MAY be created; existing directories MUST be preserved.

**Note (A-002):** Idempotency is mandatory for DEL-05-02 because destructive re-scaffolding conflicts with filesystem-as-state operation and has regression coverage in the implementation test suite.

**Source:** **ASSUMPTION** -- inferred from DIRECTIVE Section 2.1 (filesystem is state) and CONTRACT K-SNAP-1 (immutable snapshots). Destructive re-scaffolding would violate the principle that filesystem is authoritative state.

### REQ-09: Layout Conformance Verification

The deliverable MUST include test coverage that verifies a scaffolded execution root matches the structure defined in SPEC Section 12:

- **12.1:** Valid Execution Root checks (package folder exists, `_Decomposition/` exists, `INIT.md` exists).
- **12.2:** Valid Package Folder checks (naming, required subfolders).
- **12.3:** Valid Deliverable Folder checks (naming, required metadata files -- post-PREPARATION).

**Note (A-003):** This deliverable's conformance tests cover test-level verification within the development workflow. The boundary with DEL-08-03 (standalone folder structure validator, SOW-034, TBD scope) is resolved for baseline scope: this deliverable provides developer/CI test assertions; DEL-08-03 remains deferred until SOW-034 is explicitly ruled `IN`.

**Source:** SPEC Section 12; SOW-015.

### REQ-10: Flat Hierarchy Enforcement

Scaffolding MUST NOT create nested packages (packages within packages). The hierarchy is flat: `package -> deliverable`.

**Source:** CONTRACT K-HIER-1; TYPES Section 1.

### REQ-11: Stable ID Preservation

Folder names MUST include the stable deliverable/package ID as a prefix. Folder renames MUST NOT change the ID portion.

**Source:** CONTRACT K-ID-1; TYPES Section 2.

### REQ-12: Fail-Fast Error Handling with Retry Diagnostics

The scaffolding logic MUST fail fast on filesystem conflicts/errors and return deterministic diagnostics that support safe rerun after remediation. On failure, the response MUST include:

- `scaffoldStrategy=FAIL_FAST`
- failure `stage`
- failure `targetPath`
- partial-create snapshot (`created.directories`, `created.files`)
- human-actionable rerun guidance text

No rollback/delete behavior is allowed; partially created paths remain and are reconciled by idempotent rerun.

**Source:** Implemented runtime contract in `frontend/src/lib/harness/scaffold.ts`; DIRECTIVE Section 2.1 (filesystem-as-state); REQ-08 idempotency.

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
| REQ-12 | Test: inject a filesystem conflict and verify fail-fast contract fields (`scaffoldStrategy`, `stage`, `targetPath`, partial-create snapshot, guidance) are preserved through library + API route responses |

## Documentation

| Artifact | Type | Description |
|----------|------|-------------|
| Scaffolding source code | CODE | Implementation of execution-root creation logic |
| Conformance test suite | TEST | Automated tests for layout correctness per SPEC Section 12 |
| Sanitization unit tests | TEST | Tests for the `Sanitize(name)` function including edge cases (empty result, step ordering) |
| Idempotency tests | TEST | Tests verifying non-destructive re-scaffolding |
| Decomposition parsing tests | TEST | Tests verifying correct parsing of decomposition input, including malformed input handling |
| Developer documentation | DOC | Description of scaffolding API/CLI, inputs, outputs, and integration points |
