# Procedure — DEL-05-01 Instruction Root Bundling & Runtime Access

## Purpose

This procedure describes the steps to produce and verify the instruction root bundling and runtime access mechanism for the Chirality desktop app.

The goal is to ensure that deployable builds preserve instruction root vs working root separation and provide deterministic in-app access to instruction content.

**Source:** Decomposition DEL-05-01 description; Specification REQ-01 through REQ-07.

---

## Prerequisites

| Prerequisite | Detail | Status |
|--------------|--------|--------|
| **Build baseline** | macOS 15+ Apple Silicon build functioning (DEL-01-01) | **ASSUMPTION** — expected prerequisite; dependency extraction pending. Prerequisite type (hard vs. soft) is TBD pending DEPENDENCIES agent output. |
| **Packaging workflow** | `.dmg` packaging path available (DEL-01-02) | **ASSUMPTION** — expected prerequisite; dependency extraction pending. Prerequisite type (hard vs. soft) is TBD pending DEPENDENCIES agent output. |
| **Working root binding** | Session boot binds `projectRoot` (DEL-03-01) | **ASSUMPTION** — expected prerequisite for runtime testing; dependency extraction pending. Prerequisite type (hard vs. soft) is TBD pending DEPENDENCIES agent output. |
| **Governance documents** | `docs/DIRECTIVE.md`, `docs/SPEC.md`, `docs/CONTRACT.md`, `docs/TYPES.md`, `docs/PLAN.md` available for reference | Available (current repo) |
| **Agent instruction files** | `AGENTS.md`, `README.md`, `agents/*` available for bundling | Available (current repo) |

> **Enrichment note (A-004):** Prerequisite rows now explicitly note that the hard vs. soft classification is TBD pending DEPENDENCIES agent output, rather than leaving the ASSUMPTION tags as the only indicator that dependency status is unresolved.

---

## Steps

### Step 1: Audit Existing Build Configuration

1. Review the current Electron build configuration (e.g., `electron-builder.yml`, `package.json` build section, or equivalent).
2. Identify how instruction-related files (`AGENTS.md`, `README.md`, `agents/*`, `docs/DIRECTIVE.md`, `docs/CONTRACT.md`, `docs/SPEC.md`, `docs/TYPES.md`, `docs/PLAN.md`) are currently handled during packaging.
3. Document findings:
   - Are instruction files currently bundled? If so, where?
   - What bundling mechanism is used (`extraResources`, `extraFiles`, ASAR, or none)?
   - Is there an existing path resolution utility for instruction content?

**Verification:** Findings documented; current state of bundling is understood.

### Step 2: Define Instruction Root Content Manifest

1. Define the explicit list of files/directories that constitute the instruction root:
   - `AGENTS.md`
   - `README.md`
   - `agents/` (all `AGENT_*.md` files)
   - `docs/DIRECTIVE.md`, `docs/CONTRACT.md`, `docs/SPEC.md`, `docs/TYPES.md`, `docs/PLAN.md`
2. Confirm this list against DIRECTIVE Section 2.6 and the Decomposition Vocabulary Map ("Instruction Root" definition).
3. Record the canonical manifest for use in build configuration and verification.

**Verification:** Manifest is complete and matches governance-defined instruction root content.

> **Enrichment note (B-003):** docs/* contents normalized to enumerate individual files (`DIRECTIVE.md`, `CONTRACT.md`, `SPEC.md`, `TYPES.md`, `PLAN.md`) consistently with Specification REQ-01 and Datasheet Attributes.

### Step 3: Configure Build to Bundle Instruction Root

1. Update the build configuration to include all instruction root content in the packaged app bundle.
2. Use the appropriate Electron bundling mechanism (see Guidance C1 for options; `extraResources` recommended as default unless existing config dictates otherwise).
3. Ensure the bundled content structure is predictable (e.g., `Resources/instructions/AGENTS.md`, not flattened or renamed).

**Verification:** Build succeeds; instruction files are present in the expected location within the app bundle.

**If verification fails:** See Guidance C8 for recovery guidance.

### Step 4: Implement Instruction Root Path Resolution

1. Create or update a utility function that resolves the instruction root path at runtime.
2. The utility MUST handle:
   - **Packaged mode:** resolve to the bundled resource location (e.g., `process.resourcesPath/instructions/`).
   - **Development mode:** resolve to the source repository location.
3. The utility MUST be deterministic (same input conditions always produce the same path).
4. Expose the utility for use by runtime components that need to read instruction files (e.g., agent loader, governance doc reader).
5. **Validate the assumed path structure:** Before relying on the pseudocode pattern from Guidance C2, inspect the actual packaged app bundle to confirm the real resource path layout. Do not assume the illustrative pseudocode is accurate for this codebase.

**Verification:** Utility returns correct paths in both dev and packaged modes; instruction files are readable at resolved paths. Validation confirms the path structure matches the real app bundle layout.

**If verification fails:** See Guidance C8 for recovery guidance.

> **Enrichment note (E-002):** Added sub-step 5 requiring validation of the assumed path structure against the real app bundle before relying on the pseudocode pattern, addressing the gap between illustrative pseudocode and implementation reliance.

### Step 5: Enforce Read-Only Instruction Root at Runtime

1. Ensure that runtime code does not write to instruction root paths.
2. At minimum, the path resolution utility should be clearly documented as providing read-only access.
3. Consider adding runtime guards if the existing architecture has code paths that could inadvertently write to instruction locations.
4. Implement and verify the selected baseline enforcement mechanism from Guidance C4: API-level runtime path guard that rejects `projectRoot` values inside instruction root (`WORKING_ROOT_CONFLICT`).

**Note:** In packaged mode, macOS app bundle protections provide some natural enforcement. Dev mode requires discipline or explicit guards.

**Verification:** No agent or runtime code writes to instruction root paths during normal operation. Attempted writes to instruction root are rejected with an identifiable error (per Specification REQ-02 verification).

**If verification fails:** See Guidance C8 for recovery guidance.

### Step 6: Verify Working Root Independence

1. Test the application with working roots at different filesystem locations:
   - User home directory
   - A subdirectory with spaces in the path
   - An external volume (if available)
   - A read-only volume (**ASSUMPTION** — edge case; see Specification REQ-05 verification)
   - A network mount (**ASSUMPTION** — edge case; see Specification REQ-05 verification)
   - A path with unicode characters (**ASSUMPTION** — edge case; see Specification REQ-05 verification)
2. Confirm that session boot, agent execution, and file operations function correctly regardless of working root location.
3. Confirm that the working root has no dependency on the instruction root location or app installation directory.

**Verification:** All standard-case tests pass; edge case tests either pass or produce clear, actionable error messages. Working root is location-independent.

### Step 7: Build, Package, and Verify End-to-End

1. Build the app in production mode.
2. Package as `.dmg`.
3. Install on a clean test environment (or a different directory from the build location).
4. Verify:
   - Instruction files are present and readable in the installed app.
   - Session boot with a user-selected working root succeeds.
   - Agents can locate and read instruction files.
   - Agents read/write only in the working root, not the instruction root.
5. Verify content integrity: compare SHA-256 hashes of bundled instruction files against source versions at the build commit (automated via `npm run instruction-root:integrity` in packaging flow).
6. Verify graceful degradation (REQ-07): temporarily remove or corrupt an instruction file and confirm boot fails closed with `INSTRUCTION_ROOT_INVALID` and actionable missing/invalid-entry diagnostics.

**Verification:** End-to-end test passes; instruction root content matches source; working root operations function correctly; graceful degradation fails closed with actionable typed diagnostics (`INSTRUCTION_ROOT_INVALID`).

**If verification fails:** See Guidance C8 for recovery guidance. Do not proceed to status update until root cause is identified and resolved.

> **Enrichment note (C-001):** Step 7 sub-step 5 is now implemented as an automated build-time/CI-capable packaging gate (`instruction-root:integrity`) with manifest + summary artifacts.

---

## Verification

| Step | Verification Criteria | Pass/Fail |
|------|----------------------|-----------|
| 1 | Existing build config audited and documented | TBD |
| 2 | Instruction root content manifest defined and confirmed | TBD |
| 3 | Build configuration updated; instruction files present in app bundle | TBD |
| 4 | Path resolution utility works in dev + packaged modes; path structure validated against real bundle | TBD |
| 5 | No runtime writes to instruction root paths; write attempts rejected | TBD |
| 6 | Working root independence verified at multiple locations (standard + edge cases) | TBD |
| 7 | End-to-end build, package, install, and verify passes; content integrity confirmed; graceful degradation verified | TBD |

---

## Records

| Record | Description | Location |
|--------|-------------|----------|
| **Build configuration diff** | Changes to Electron build config for instruction bundling | Git commit in repo |
| **Path resolution utility** | Source code for `getInstructionRootPath()` or equivalent | TBD — location in codebase |
| **Test results** | Verification results for Steps 1-7 | TBD — test report or CI output |
| **Content integrity check** | SHA-256 hash comparison between source and bundled instruction files | `frontend/artifacts/harness/instruction-root-integrity/latest/{manifest.json,summary.json}` |
| **_STATUS.md update** | Lifecycle state updates as work progresses | `_STATUS.md` in this deliverable folder |
