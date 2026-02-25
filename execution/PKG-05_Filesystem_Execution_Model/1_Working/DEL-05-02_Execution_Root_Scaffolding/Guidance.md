# Guidance -- DEL-05-02 Execution Root Scaffolding + Layout Conformance

## Vocabulary Note (D-001)

**ASSUMPTION labeling convention:** Throughout this deliverable's documents, assumptions are marked with bold **ASSUMPTION:** prefix followed by the assumption text. All documents in this deliverable use this format consistently. (If automated tooling or review processes need to scan for assumptions, they should match the pattern `**ASSUMPTION:**`.)

**Terminology convention (X-003):** The term "working root" refers to the user-selected filesystem root where agents read/write state. The canonical form is: **working root (`projectRoot`)**. Synonyms in the decomposition vocabulary include "Working Root," "`projectRoot`," and "working directory." This deliverable uses "working root (`projectRoot`)" consistently. See Decomposition Vocabulary Map for the full synonym list.

## Purpose

This deliverable exists to ensure that when a user selects a working root (`projectRoot`) and initializes a Chirality execution instance, the resulting filesystem structure is complete, correct, and SPEC-conformant from the start. Without correct scaffolding, downstream agent workflows (PREPARATION, 4_DOCUMENTS, DEPENDENCIES, AGGREGATION, etc.) will encounter missing directories and fail or produce inconsistent results.

The deliverable also provides verification capability so that existing execution roots can be checked for layout conformance -- catching structural drift before it causes downstream failures.

**Source:** Decomposition entry for DEL-05-02; SOW-014 (filesystem-is-the-state); SOW-015 (layout matches SPEC).

## Principles

### P1: Filesystem Is the Database -- Structure Is Schema

In Chirality, the directory tree serves the role of a database schema. Package folders, deliverable folders, and tool roots are structural invariants. Scaffolding is the "CREATE TABLE" equivalent: it establishes the structural contract that all agents and tools depend on.

**Source:** DIRECTIVE Section 2.1.

### P2: Scaffolding Creates Structure; Agents Populate Content

The scaffolding logic creates directories and minimal initialization files (e.g., `INIT.md`, `_COORDINATION.md`). It does not create deliverable-level metadata files (`_STATUS.md`, `_CONTEXT.md`, etc.) -- that is the PREPARATION agent's responsibility. This separation keeps scaffolding focused on structural correctness and avoids duplicating agent logic.

**ASSUMPTION:** The boundary between scaffolding and PREPARATION is as described. If scaffolding is expected to also create metadata files, the scope of this deliverable would need to expand.

### P3: Idempotency Preserves Human Work

Re-running scaffolding on an existing execution root must be safe. This means creating missing directories without deleting or overwriting existing content. Operators and agents may have added files or modified content in existing directories; scaffolding must respect that state.

**ASSUMPTION:** Inferred from the filesystem-as-state principle and CONTRACT K-SNAP-1 (immutable snapshots). No explicit SPEC requirement for idempotency, but destructive behavior would violate foundational principles.

### P4: Layout Is Enforced by Convention and Verification

The current system enforces layout correctness through agent instruction constraints and human review. This deliverable adds programmatic verification (tests), but does not necessarily produce a standalone external validator (that is DEL-08-03, optional scope). Under the active coordination ruling, PKG-08 remains non-driving while SOW-032..038 are `TBD`, so this deliverable's test suite remains the baseline conformance gate.

**Source:** SPEC Section 12; PLAN Section 3.3.

## Considerations

### C1: Decomposition as Input

Scaffolding requires a decomposition document as input to know which packages and deliverables to create. The scaffolding logic must parse the decomposition table to extract `PackageID`, `PackageName`, `DeliverableID`, and `DeliverableName` values.

**ASSUMPTION:** The decomposition document format is the table structure defined in the Software Decomposition document (deliverables table per package with the column schema used in the G7-APPROVED decomposition). Parsing logic must handle this format.

### C2: Interaction with PREPARATION Agent

PREPARATION creates the minimum viable fileset within each deliverable folder. The scaffolding logic and PREPARATION are likely invoked in sequence:

1. Scaffolding creates execution root structure (directories + `INIT.md`).
2. PREPARATION populates each deliverable folder with metadata files.

The interface between them is the deliverable folder path. Scaffolding guarantees the folder exists; PREPARATION guarantees its contents.

**ASSUMPTION:** This sequence is the intended interaction model. Alternative models (scaffolding does everything, or PREPARATION creates its own folders) would change the scope boundary.

### C3: Tool Root Sub-Structure

Some tool roots have required sub-structure (e.g., `_Aggregation/_Archive/`, `_Aggregation/_Templates/`, `_Decomposition/_Archive/`). The scaffolding logic must create these subdirectories, not just the top-level tool root.

**Source:** SPEC Section 1 (Execution Root Layout diagram).

### C4: INIT.md Content Schema

SPEC Section 12.1 requires `INIT.md` to exist with "session parameters." DEL-05-02 now uses a concrete minimum template (`# Execution Init`, project name, initialized date, decomposition reference, coordination mode, and a session-parameters section) while remaining compatible with future SPEC expansion.

**Source:** SPEC Section 12.1 + implemented scaffold template in `frontend/src/lib/harness/scaffold.ts`.

### C5: Coordination Representation Initialization

`_COORDINATION.md` is shown in the SPEC layout under `_Coordination/`. SPEC Section 13 defines coordination representations (SCHEDULE_FIRST, DEPENDENCY_TRACKED, HYBRID). The scaffolding logic should create a template `_COORDINATION.md` that prompts the human to select a coordination representation.

**Source:** SPEC Section 13.

### C6: Relationship to Existing Codebase

The Chirality app is an Electron + Next.js desktop application. DEL-05-02 is implemented as a server-side API route (`POST /api/harness/scaffold`) backed by `frontend/src/lib/harness/scaffold.ts`, and invoked from PIPELINE PREP controls.

**Source:** `frontend/src/app/api/harness/scaffold/route.ts`; `frontend/src/app/pipeline/pipeline-client.tsx`.

### C7: SPEC Evolution and Scaffolding Maintenance (X-004)

The authoritative SPEC (`docs/SPEC.md`) defines the canonical layout. If the SPEC evolves to add new tool roots, change sub-structure requirements, or modify naming rules, the scaffolding logic must be updated accordingly. Considerations:

- **Versioning:** The scaffolding logic should reference a specific SPEC version or section hash so that changes to the SPEC can be detected.
- **Forward compatibility:** Idempotent scaffolding (REQ-08) provides a natural upgrade path: re-running updated scaffolding on an existing execution root will create newly-required directories without disturbing existing content.
- **Change detection:** No current mechanism alerts maintainers that the SPEC has changed in ways that affect scaffolding. **ASSUMPTION:** This is an operational concern to be addressed by governance/change management processes (DEL-06-04), not by the scaffolding code itself.

**Source:** Inferred from DIRECTIVE Section 2.1 (filesystem-as-state) and the likelihood that SPEC will evolve as the project matures.

## Trade-offs

### T1: Scaffolding Depth vs. Agent Responsibility

**Option A:** Scaffolding creates only directories and `INIT.md`; PREPARATION creates all deliverable-level files.
**Option B:** Scaffolding creates directories AND the minimum viable fileset for each deliverable.

Option A maintains cleaner separation of concerns. Option B reduces the number of sequential steps. This deliverable assumes Option A based on the SPEC distinction between "folder layout" (scaffolding) and "minimum viable fileset" (PREPARATION), but a human ruling may direct otherwise.

### T2: Conformance Testing vs. Standalone Validator

This deliverable provides test-level conformance checks (REQ-09). A standalone CLI validator tool is deferred to DEL-08-03 while SOW-034 remains `TBD`. If SOW-034 is later ruled `IN`, the conformance logic from this deliverable's tests can be extracted into the standalone tool.

**Source:** PLAN Sections 3.3 and 4 (sequencing rationale).

### T3: Decomposition Parsing Scope

The scaffolding logic needs to parse a decomposition document to determine what to scaffold. The parsing could be:
- **Tightly coupled:** Specific to the current Markdown table format.
- **Loosely coupled:** Based on a structured intermediate representation (e.g., JSON).

A loosely coupled approach is more robust but requires defining the intermediate representation. **ASSUMPTION:** Implementation will use the Markdown table format directly, as that is the current canonical form.

### T4: Technology Stack Resolution (D-002)

DEL-05-02 uses a Next.js API route plus Node.js filesystem primitives:

- API surface: `POST /api/harness/scaffold`
- Core implementation: `frontend/src/lib/harness/scaffold.ts` (`node:fs/promises`)
- Consumer path: PIPELINE PREP scaffold trigger in `frontend/src/app/pipeline/pipeline-client.tsx`

This approach preserves typed request/response contracts for UI integration while keeping filesystem mutation logic in a testable library module.

**Source:** implemented code + route/tests in `frontend/src`.

## Examples

### Example 1: Successful Scaffolding from a 2-Package Decomposition (D-003)

**Scenario:** A decomposition document defines PKG-01 (Build & Packaging) with 2 deliverables and PKG-02 (Desktop UI Workflow) with 4 deliverables. The user initializes a new execution root at `/Users/operator/projects/my-project/execution/`.

**Expected result after scaffolding:**

```
/Users/operator/projects/my-project/execution/
├── INIT.md                          (minimal content: date, decomposition ref, project name)
├── _Aggregation/
│   ├── _Archive/
│   └── _Templates/
├── _Change/
├── _Coordination/
│   └── _COORDINATION.md             (template with representation selection prompt)
├── _Decomposition/
│   └── _Archive/
├── _Estimates/
├── _Reconciliation/
├── _Archive/
├── _Scripts/
├── _Sources/
├── PKG-01_Build_-_Packaging/
│   ├── 0_References/
│   │   └── _Archive/
│   ├── 1_Working/
│   │   ├── _Archive/
│   │   ├── DEL-01-01_macOS_15+_Apple_Silicon_Build_Baseline/
│   │   └── DEL-01-02_Unsigned_DMG_Packaging_Workflow/
│   ├── 2_Checking/
│   │   ├── From/
│   │   └── To/
│   └── 3_Issued/
│       └── _Archive/
└── PKG-02_Desktop_UI_Workflow/
    ├── 0_References/
    │   └── _Archive/
    ├── 1_Working/
    │   ├── _Archive/
    │   ├── DEL-02-01_FileTree_Refresh_-_External-Change_Detection/
    │   ├── DEL-02-02_Portal-Pipeline_Navigation_-_Deliverable_Key_Semantics/
    │   ├── DEL-02-03_Operator_Toolkit_Panel_-_Local_Presets_(Non-authoritative)/
    │   └── DEL-02-04_Multi-pane_Layout_+_Theme_Hardening/
    ├── 2_Checking/
    │   ├── From/
    │   └── To/
    └── 3_Issued/
        └── _Archive/
```

**Note:** Deliverable folders are empty at this point; PREPARATION populates them with metadata files in the next pipeline step.

### Example 2: Idempotent Re-scaffolding

**Scenario:** The execution root from Example 1 exists. An operator has added files to `PKG-01_Build_-_Packaging/1_Working/DEL-01-01_macOS_15+_Apple_Silicon_Build_Baseline/` (e.g., `_STATUS.md`, `_CONTEXT.md` written by PREPARATION). The decomposition is updated to add a new deliverable DEL-01-03 to PKG-01.

**Expected result after re-scaffolding:**
- All existing directories and files are preserved (including PREPARATION-written files).
- New folder `DEL-01-03_{Sanitize(Name)}/` is created under `PKG-01_Build_-_Packaging/1_Working/`.
- No content is deleted or overwritten.

### Example 3: Sanitization Edge Case

**Scenario:** A deliverable name contains special characters: `"UI: Login & Auth <v2>"`

**Expected `Sanitize(name)` output** (applying steps in order):
1. Replace special characters: `"UI- Login & Auth -v2-"` (`:`, `<`, `>` replaced with `-`)
2. Collapse whitespace: `"UI- Login & Auth -v2-"` (no consecutive whitespace)
3. Trim: `"UI- Login & Auth -v2-"` (no leading/trailing whitespace)

**Result folder name:** `DEL-XX-YY_UI- Login & Auth -v2-`

## Conflict Table (for human ruling)

| Conflict ID | Conflict | Source A | Source B | Impacted Sections | Proposed Authority | Human Ruling |
|-------------|---------|----------|----------|--------------------|--------------------|-------------|
| CON-01 | Boundary between scaffolding (this deliverable) and PREPARATION agent: does scaffolding create only directories, or also metadata files? | SPEC Section 1 (layout = directories) | SPEC Section 2.1 (deliverable folder file inventory mentions PREPARATION as creator) | Specification REQ-03; Guidance P2; Procedure Steps | SPEC Section 2.1 (PREPARATION creates metadata; scaffolding creates structure) | RESOLVED (DEL-05-02 docs aligned to structure-only scaffolding) |
| CON-02 | `INIT.md` content schema is not fully specified in SPEC | SPEC Section 12.1 (requires existence) | No schema definition found | Specification REQ-05; Procedure Step 5 | DEL-05-02 minimum schema baseline (Execution Init heading + project/date/decomposition/coordination/session-parameters fields) | RESOLVED (local baseline adopted; future SPEC changes may extend) |
| CON-03 | Overlap between this deliverable's conformance tests and DEL-08-03 (standalone folder structure validator, TBD scope) | SOW-015 (layout matches SPEC -- this deliverable) | SOW-034 (folder structure validator -- DEL-08-03) | Specification REQ-09 | Use control-plane scope ruling: DEL-05-02 owns baseline test-level checks; DEL-08-03 remains optional until SOW-034 is explicitly ruled `IN` | RESOLVED for baseline scope (2026-02-23): PKG-08 is non-driving and SOW-034 is `TBD`; revisit only if SOW-034 flips `IN` |
| CON-04 | Normative strength for package subfolders (`0_References/`, `2_Checking/`, `3_Issued/`): SHOULD vs MUST | Datasheet Conditions (SPEC 12.2 checklist context) | Specification REQ-02 creation behavior (SPEC 1.1 scaffold context) | Datasheet Conditions; Specification REQ-02; Procedure Step 7 | Use dual interpretation by context: existing-root validation checklist = SHOULD, scaffolding creation behavior = MUST | RESOLVED (docs harmonized by context) |
| CON-05 | Idempotency normative strength: REQ-08 used SHOULD for overall idempotency while implementation and procedure enforced mandatory non-destructive reruns | Prior Specification REQ-08 wording | Guidance P3 + Procedure Steps 3-4 + implementation tests | Specification REQ-08; Guidance P3; Procedure Steps 3, 4 | Elevate REQ-08 to MUST for DEL-05-02 | RESOLVED (REQ-08 updated to MUST + regression tests) |
