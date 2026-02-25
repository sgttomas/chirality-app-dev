# Procedure -- DEL-05-02 Execution Root Scaffolding + Layout Conformance

## Purpose

This procedure describes the steps to produce the code, tests, and documentation artifacts for DEL-05-02. It covers implementing the execution-root scaffolding logic, writing conformance tests, and producing developer documentation.

## Prerequisites

| # | Prerequisite | Status | Notes |
|---|-------------|--------|-------|
| PRE-01 | Access to `docs/SPEC.md` (Sections 1, 10, 11, 12, 13) | Available | Authoritative layout specification |
| PRE-02 | Access to `docs/CONTRACT.md` | Available | Binding invariants (K-HIER-1, K-ID-1, K-SNAP-1) |
| PRE-03 | Access to `docs/TYPES.md` (Section 2) | Available | Stable ID formats and folder label rules |
| PRE-04 | Access to decomposition document | Available | `execution/_Decomposition/ChiralityApp_SoftwareDecomposition_2026-02-21_G7-APPROVED.md` |
| PRE-05 | Familiarity with Chirality desktop app codebase | Available | Integration points confirmed in `frontend/src/app/api/harness/scaffold/route.ts` and `frontend/src/app/pipeline/pipeline-client.tsx` |
| PRE-06 | Understanding of PREPARATION agent scope boundary | Available | Boundary clarified: scaffolding creates structure/templates, PREPARATION owns deliverable metadata files |
| PRE-07 | DEL-05-01 (Instruction Root Bundling) -- understanding of instruction root vs working root (`projectRoot`) separation | Available | Context dependency only (non-blocking) |
| PRE-08 | Technology stack decision for scaffolding implementation | Resolved | Next.js API route + `node:fs/promises` implementation (`frontend/src/lib/harness/scaffold.ts`) |

## Steps

### Step 1: Analyze Existing Codebase for Scaffolding Integration Points

**Objective:** Determine where in the Electron + Next.js codebase the scaffolding logic should be implemented.

**Actions:**
1. Review the existing project structure to identify how the working root (`projectRoot`) is selected and bound to a session.
2. Identify the API or function that currently initializes an execution instance (if any exists).
3. Determine whether scaffolding should be:
   - A server-side API endpoint (e.g., `/api/project/scaffold`).
   - A utility function called during session boot.
   - A standalone script.
4. Document the integration decision.

**Verification:** Integration point is identified and documented.

**Notes:** This step is resolved for DEL-05-02: scaffolding is implemented as `POST /api/harness/scaffold` backed by `frontend/src/lib/harness/scaffold.ts`.

### Step 2: Implement Sanitize(name) Function

**Objective:** Implement the canonical folder-name sanitization function.

**Actions:**
1. Implement `Sanitize(name)` per SPEC Section 10.1, applying steps in the declared order:
   - Step 1: Replace `/`, `\`, `:`, `*`, `?`, `"`, `<`, `>`, `|` with `-`.
   - Step 2: Collapse consecutive whitespace to a single space.
   - Step 3: Trim leading/trailing whitespace.
2. Write unit tests covering:
   - Names with no special characters (passthrough).
   - Names with each special character individually.
   - Names with multiple consecutive special characters.
   - Names with leading/trailing whitespace.
   - Names with consecutive internal whitespace.
   - Empty string edge case (must fail with `INVALID_REQUEST`; no fallback label).
   - Inputs where step ordering matters (e.g., `"a : b"`, `"  :::  "`) -- see Specification note X-002.
   - All-whitespace input (should produce empty string after trim).

**Verification:** Unit tests pass; function matches SPEC Section 10.1 exactly; step ordering is verified.

**Source:** SPEC Section 10.1.

### Step 3: Implement Execution Root Directory Creation

**Objective:** Implement the function that creates a complete execution-root directory tree.

**Actions:**
1. Create a function that accepts an execution root path and creates:
   - `INIT.md` (minimal content -- see Step 5).
   - All tool roots from SPEC Section 1.2 (with sub-structure).
   - `_Coordination/_COORDINATION.md` (template -- see Step 6).
2. Ensure the function is idempotent: existing directories are preserved; missing directories are created.
3. **Error handling (B-002, C-002):** Implement error handling for filesystem failures during creation. If a filesystem error occurs mid-operation:
   - Log the error with the specific directory path that failed.
   - Stop further creation (fail-fast approach per REQ-12).
   - Report the error to the caller with sufficient detail for diagnosis.
   - The caller may re-invoke scaffolding after resolving the error; idempotency (REQ-08) ensures previously-created directories are preserved.
4. Write integration tests verifying the full directory tree is created.

**Verification:** Test creates a fresh directory, runs scaffolding, and verifies all expected directories exist per SPEC Section 1 layout diagram.

**Source:** SPEC Section 1; Specification REQ-01, REQ-06.

### Step 4: Implement Package and Deliverable Folder Creation

**Objective:** Implement logic that reads a decomposition document and creates package/deliverable folders.

**Actions:**
1. Implement decomposition parsing to extract:
   - Package table rows: `PackageID`, `PackageName`.
   - Deliverable table rows: `DeliverableID`, `DeliverableName`, parent `PackageID`.
2. For each package, create `{PKG-ID}_{Sanitize(PackageName)}/` with all required subfolders (SPEC Section 1.1).
3. For each deliverable, create `{PKG-ID}_{PkgLabel}/1_Working/{DEL-ID}_{Sanitize(DeliverableName)}/`.
4. Ensure idempotent behavior: existing folders are not overwritten.
5. **Malformed input handling (C-001):** Handle malformed decomposition input gracefully:
   - Missing required columns (PackageID, DeliverableID, etc.) -- report error, do not create partial structures.
   - Invalid ID formats (not matching `PKG-XX` or `DEL-XX-YY` patterns) -- report error.
   - Duplicate IDs -- report warning, create only one folder per unique ID.
6. Write integration tests using a sample decomposition (or the existing one), including malformed input test cases.

**Verification:** Tests verify correct folder creation for multi-package, multi-deliverable decompositions; special characters in names are correctly sanitized; malformed input is handled gracefully.

**Source:** SPEC Sections 1.1, 2, 10.2; Specification REQ-02, REQ-03, REQ-04.

### Step 5: Define INIT.md Minimal Content

**Objective:** Establish the content for `INIT.md` at the execution root.

**Actions:**
1. Create a minimal `INIT.md` template with:
   - Project name (from decomposition or user input).
   - Decomposition reference (path to decomposition document).
   - Initialization date.
   - Session parameters placeholder.
2. Document the template and any assumptions about future schema evolution.

**Verification:** `INIT.md` is created and contains the minimal required fields.

**Source:** SPEC Section 12.1 + DEL-05-02 minimum template baseline (project/date/decomposition/coordination/session-parameters).

### Step 6: Define _COORDINATION.md Template

**Objective:** Create the initial `_COORDINATION.md` template.

**Actions:**
1. Create a template that:
   - Contains a title heading (e.g., `# Coordination`).
   - Explains the three coordination representations (SCHEDULE_FIRST, DEPENDENCY_TRACKED, HYBRID).
   - Prompts the human to select one.
   - Has a placeholder for the selected representation.
2. Place the template at `_Coordination/_COORDINATION.md` during scaffolding.

**Verification:** Template is created; content matches SPEC Section 13 vocabulary; template contains at minimum a title heading and coordination representation placeholder (per Specification note E-001).

**Source:** SPEC Section 13.

### Step 7: Implement Layout Conformance Checks

**Objective:** Write test-level conformance checks per SPEC Section 12.

**Actions:**
1. Implement checks for:
   - **12.1 Valid Execution Root:** At least one `PKG-XX_{Label}/` exists; `_Decomposition/` exists with >= 1 decomposition doc; `INIT.md` exists.
   - **12.2 Valid Package Folder:** Named correctly; contains `1_Working/`; creation behavior includes `0_References/`, `2_Checking/`, and `3_Issued/` per SPEC Section 1.1.
   - **12.3 Valid Deliverable Folder:** Named correctly; contains `_STATUS.md`, `_CONTEXT.md`, `_DEPENDENCIES.md`, `_REFERENCES.md`.
2. Write tests that:
   - Scaffold from a decomposition, then run all conformance checks.
   - Test negative cases (missing directories, incorrect naming).

**Verification:** All SPEC Section 12 checks pass on a correctly scaffolded root; negative cases are detected.

**Source:** SPEC Section 12; Specification REQ-09.

### Step 8: Write Developer Documentation

**Objective:** Produce documentation describing the scaffolding module.

**Actions:**
1. Document:
   - The scaffolding API/function signature and parameters.
   - Expected inputs (execution root path, decomposition document).
   - Expected outputs (directory tree per SPEC).
   - Idempotency guarantees.
   - Error handling behavior (per REQ-12 ruling).
   - Integration points with the Chirality desktop app.
   - Relationship to PREPARATION agent (scope boundary).
2. Include a layout diagram matching SPEC Section 1.

**Verification:** Documentation exists; covers all aspects listed above.

**Note (E-003):** Developer documentation is currently maintained inline with the implementation and tests (`frontend/src/lib/harness/scaffold.ts`, `frontend/src/lib/harness/sanitize.ts`, route/tests under `frontend/src/__tests__/`).

### Step 9: Final Integration Verification

**Objective:** Verify the complete scaffolding flow end-to-end.

**Actions:**
1. Run the scaffolding logic against the existing decomposition (`ChiralityApp_SoftwareDecomposition_2026-02-21_G7-APPROVED.md`).
2. Verify the resulting directory tree:
   - All 8 packages have correct folders with all required subfolders.
   - All 32 deliverables have folders at the correct paths.
   - All tool roots exist with correct sub-structure.
   - `INIT.md` and `_COORDINATION.md` exist.
3. Run all conformance checks.
4. Re-run scaffolding on the same root; verify no content is lost or overwritten.

**Verification:** Full end-to-end test passes; idempotency is confirmed.

### Step 10: PREPARATION Integration Validation (F-003)

**Objective:** Verify that the scaffolded output is compatible with the PREPARATION agent's input expectations.

**Actions:**
1. After scaffolding is complete (Step 9), invoke the PREPARATION agent (or a test harness simulating PREPARATION) against one or more scaffolded deliverable folders.
2. Verify that PREPARATION:
   - Successfully locates each deliverable folder at the expected path.
   - Can create the minimum viable fileset (`_STATUS.md`, `_CONTEXT.md`, `_DEPENDENCIES.md`, `_REFERENCES.md`, `_SEMANTIC.md`) without errors.
   - Does not encounter missing parent directories or unexpected path structures.
3. If integration issues are found, update scaffolding logic or document interface requirements.

**Verification:** PREPARATION (or its test harness) successfully operates on scaffolded output without path-related errors.

**Notes:** This step validates the interface described in Guidance C2. **ASSUMPTION:** A PREPARATION test harness or the actual PREPARATION agent is available. If not, this step may be deferred until PREPARATION integration is feasible.

**Source:** Inferred from Guidance C2 (Interaction with PREPARATION Agent); Specification scope exclusion note.

## Verification Summary

| Step | Verification | Pass Criteria |
|------|-------------|---------------|
| Step 2 | Unit tests for `Sanitize(name)` | All edge cases pass, including step-ordering and empty-result scenarios |
| Step 3 | Integration test for execution root creation | All tool roots + `INIT.md` present; error handling behaves per REQ-12 |
| Step 4 | Integration test for package/deliverable creation | All packages and deliverables created correctly; malformed input handled gracefully |
| Step 5 | `INIT.md` content check | Minimal fields present |
| Step 6 | `_COORDINATION.md` template check | Template matches SPEC Section 13; contains title heading + representation placeholder |
| Step 7 | Conformance checks | All SPEC Section 12 checks pass (positive and negative) |
| Step 8 | Documentation review | All topics covered; publication location determined |
| Step 9 | End-to-end integration test | Full decomposition scaffolded correctly; idempotent |
| Step 10 | PREPARATION integration test | PREPARATION operates successfully on scaffolded output |

## Records

| Record | Description | Location |
|--------|-------------|----------|
| Test results | Automated test output from conformance and unit tests | CI / local test runner output |
| Developer documentation | Scaffolding module documentation | `frontend/src/lib/harness/scaffold.ts`, `frontend/src/lib/harness/sanitize.ts`, and related test contracts under `frontend/src/__tests__/` |
| Integration decision | Where scaffolding logic lives in the codebase | Documented in Step 1 output |
| Conformance report | Results of SPEC Section 12 checks against scaffolded root | Test runner output |
| PREPARATION integration results | Results of scaffolding-to-PREPARATION handoff validation | Test runner output (Step 10) |
