# Procedure: DEL-02-05 Frontend Workflow Shell Baseline

---

## Purpose

This procedure describes the steps to produce and verify the Frontend Workflow Shell Baseline deliverable. It covers implementation of the PORTAL/PIPELINE frame, file tree panel, chat panel, directory selection, and project-root wiring as specified in the Specification document.

---

## Prerequisites

### Required Deliverables / Inputs

| Prerequisite | Description | Status |
|-------------|-------------|--------|
| DEL-01-03 (FE-1) | Frontend Workspace Bootstrap -- `frontend/` workspace with package manifest, Next/Electron/TypeScript baseline, and build scripts | **ASSUMPTION:** Must be at least scaffolded before shell implementation begins (per phased plan FE-1 -> FE-2 -> FE-3) |
| DEL-03-07 (FE-2) | Harness API Baseline -- baseline route surfaces for session/turn APIs | **ASSUMPTION:** Should be available or stubbed for end-to-end wiring verification |
| `AGENTS.md` Section 3 | Agent Matrix definition, cell-to-page routing rules, PIPELINE category breakdown | Available (read) |
| `docs/PLAN.md` Section 2 | Frontend phased plan, matrix navigation details, TASK* selector model, option policy | Available (read) |

### Required Environment

| Requirement | Detail | Source |
|-------------|--------|--------|
| macOS 15+ | Apple Silicon hardware | `DEC-PLAT-001` |
| Node.js + npm | Version per `frontend/package.json` engine constraints. **Note:** Pin or cross-reference the expected Node.js version constraint once DEL-01-03 is available. If DEL-01-03 has not yet defined engine constraints, use Node.js LTS (currently v20.x or v22.x) as the default. (Ref: X-001) | **ASSUMPTION:** Defined in DEL-01-03 scaffold |
| This repository | All source and config present in tracked tree; no external repos | OBJ-008 |

### Required References

| Reference | Path | Purpose |
|-----------|------|---------|
| Decomposition | `execution/_Decomposition/ChiralityApp_SoftwareDecomposition_2026-02-21_G7-APPROVED.md` | Deliverable definition, scope boundaries |
| Agent Matrix | `AGENTS.md` Section 3 | Matrix structure and routing rules |
| Frontend Plan | `docs/PLAN.md` Section 2 | Phased plan, acceptance criteria, selector model |
| SPEC | `docs/SPEC.md` | Canonical filesystem structures | **location TBD** for detailed section references |
| TYPES | `docs/TYPES.md` | Canonical vocabulary (Working Root, Execution Root, etc.) | **location TBD** for detailed section references |

---

## Steps

### Step 1: Verify Workspace Prerequisite

**Action:** Confirm that the `frontend/` workspace (DEL-01-03) exists and is buildable.

1. Verify `frontend/package.json` exists.
2. Run `npm install` from `frontend/` to confirm dependencies resolve.
3. Run `npm run dev` or `npm run build` to confirm the baseline builds.

**If prerequisite is not met:** Record a blocker in `_DEPENDENCIES.md` and coordinate with DEL-01-03 progress. Do not proceed with shell implementation until the workspace scaffold is available.

**Failure Recovery (applies to all steps) (Ref: C-003):** If the build breaks during any of Steps 2-7:
1. Check the build error output to identify the failing step/component.
2. Revert the most recent change that introduced the failure (use `git diff` and `git checkout` on affected files).
3. Re-run the build to confirm the previous working state is restored.
4. If the failure is caused by a prerequisite issue (e.g., missing DEL-01-03 scaffold, incompatible Node.js version), consult the prerequisite deliverable's status and `_DEPENDENCIES.md`.
5. If the failure cannot be resolved, record the issue in `MEMORY.md` and escalate to the controlling agent or human.

### Step 2: Implement Page Routing Structure

**Action:** Create the top-level page routes for the three UI surfaces.

1. Create a PORTAL page route (the default/home page -- **ASSUMPTION**).
2. Create a PIPELINE page route.
3. Create a WORKBENCH page route.
4. Implement routing logic such that:
   - NORMATIVE and EVALUATIVE matrix cell selections navigate to WORKBENCH with agent context.
   - OPERATIVE matrix cell selections navigate to PIPELINE with category context.

**Verification:** Pages render and navigation between them works.

### Step 3: Implement Agent Matrix Component

**Action:** Build the 3x4 Agent Matrix as a UI component on the PORTAL page.

1. Render a 3-row by 4-column grid.
2. Label rows: NORMATIVE, OPERATIVE, EVALUATIVE.
3. Label columns: GUIDING, APPLYING, JUDGING, REVIEWING.
4. Populate cells with agent/category names per `AGENTS.md` Section 3:
   - NORMATIVE: HELP, ORCHESTRATE, WORKING_ITEMS, AGGREGATE
   - OPERATIVE: DECOMP*, PREP*, TASK*, AUDIT*
   - EVALUATIVE: AGENTS, DEPENDENCIES, CHANGE, RECONCILING
5. Wire cell click handlers to route to the correct page (WORKBENCH or PIPELINE) with appropriate context.

**Verification:** Matrix renders correctly; clicking each cell navigates to the expected page.

### Step 4: Implement PIPELINE Category Dropdowns

**Action:** Build category dropdown menus for the PIPELINE page.

1. Implement dropdowns for DECOMP*, PREP*, TASK*, AUDIT* with options per `AGENTS.md` Section 3.
2. Implement the TASK* split selector model:
   - Task Agent selector (static options).
   - Scope selectors (dynamic: deliverables from working root, knowledge types when applicable).
3. Render unsupported/unavailable variants as disabled "coming soon" entries.
4. Wire knowledge-type scope visibility to the presence of a knowledge decomposition marker in `_Decomposition`.

**Verification:** Each dropdown expands with correct options; disabled variants are non-selectable; TASK* shows split selectors.

### Step 5: Implement File Tree Panel

**Action:** Build the file tree panel as a structural container within the shell layout.

1. Create a file tree component that accepts a root path prop.
2. Render the directory structure of the provided root path.
3. Position the panel within the shell layout (exact layout slot is TBD -- to be coordinated with DEL-02-04 for multi-pane behavior).

**Verification:** File tree panel renders the directory contents of a selected working root.

### Step 6: Implement Chat Panel

**Action:** Build the chat panel as a structural container within the shell layout.

1. Create a chat panel component that provides a message display area and input surface.
2. Position the panel within the shell layout.
3. Wire basic structure for session context (session/turn API integration is DEL-03-07's scope; this step provides the container only).

**Verification:** Chat panel renders with input area; structural container is present.

### Step 7: Implement Directory Selection and Project-Root Wiring

**Ordering note (Ref: A-004):** Step 7 (directory selection and project-root wiring) is presented sequentially after Steps 2-6 but is logically independent of the UI component implementation in Steps 3-6. Implementers may choose to implement Step 7 in parallel with Steps 3-6, as the directory selection and `projectRoot` binding are orthogonal UI concerns. However, Step 7 depends on Step 2 (page routing structure) being in place for route-level wiring, and the verification in Step 7 requires that at least the file tree panel (Step 5) exists to confirm propagation. Steps 2-7 are therefore **partially parallelizable** but not fully independent.

**Action:** Build the Working Root selection mechanism and wire it through the application.

1. Implement a directory selection trigger (button or menu item).
2. Use native Electron dialog (`dialog.showOpenDialog` with `properties: ['openDirectory']` -- **ASSUMPTION**) to let the operator choose a directory.
3. Validate the selected path is a valid local directory.
4. Bind the selected path to application state as `projectRoot`.
5. Propagate the `projectRoot` to:
   - File tree panel (root path).
   - Pipeline scope selectors (scan working root for deliverables).
   - **ASSUMPTION:** Harness session boot context when sessions are created (integration point with DEL-03-01/DEL-03-07).

**Verification:** Directory selection dialog opens; selected directory is reflected in file tree panel and pipeline scope selectors.

### Step 8: End-to-End Integration Verification

**Action:** Perform the acceptance demonstration defined in the specification (REQ-11).

1. Start the development server from `frontend/` (e.g., `npm run dev`).
2. Application launches and boots to the PORTAL page.
3. Verify the Agent Matrix renders correctly (3x4, correct labels).
4. Select a NORMATIVE cell -- verify navigation to WORKBENCH.
5. Return to PORTAL; select an OPERATIVE cell -- verify navigation to PIPELINE with category context.
6. On PIPELINE, verify category dropdowns render with correct options.
7. On PIPELINE, verify TASK* split selectors render and populate dynamically.
8. Select a Working Root directory -- verify file tree panel populates.
9. Verify chat panel renders within the shell layout.
10. Capture evidence (screenshots, recording, or structured notes) of the end-to-end flow.

**Verification:** All steps above complete successfully on macOS 15+ Apple Silicon, running from this repository only.

---

## Verification

| Check | What to Confirm | Evidence |
|-------|----------------|----------|
| Build success | `frontend/` builds without errors on target platform | Build log |
| Page routing | PORTAL, PIPELINE, WORKBENCH pages render and route correctly | Navigation demonstration |
| Matrix rendering | 3x4 matrix with correct cell labels | Screenshot |
| Matrix routing | Cell clicks route to correct pages | Navigation recording |
| PIPELINE dropdowns | All four categories with correct options | Screenshots |
| TASK* split selectors | Static + dynamic selectors; knowledge-type visibility | Screenshot with workspace |
| File tree panel | Renders directory structure of selected root | Screenshot |
| Chat panel | Renders structural container | Screenshot |
| Directory selection | Dialog opens; path validated; bound to state | Recording |
| Project-root wiring | Selected root propagates to file tree + scope selectors | End-to-end demonstration |
| Platform compliance | Runs on macOS 15+ Apple Silicon | Build + run evidence |
| Local-only execution | No external repos required | Build log showing no external dependencies |

---

## Records

### Required Outputs

| Record | Description | Format / Storage (Ref: X-003) |
|--------|-------------|-------------------------------|
| CODE artifacts | Frontend source files committed to `frontend/` (page routes, components, wiring logic) | Committed to repository under `frontend/` |
| CONFIG artifacts | Configuration files (routing config, build config adjustments, matrix data if externalized) | Committed to repository under `frontend/` |
| Acceptance evidence | Screenshots or recording demonstrating end-to-end UI boot and route wiring per REQ-11 | **ASSUMPTION:** Store as PNG screenshots or MP4/GIF recording in `execution/PKG-02_Desktop_UI_Workflow/1_Working/DEL-02-05_Frontend_Workflow_Shell/evidence/` (create directory if needed). Reference in `_STATUS.md` update and `MEMORY.md`. |
| Build log | Evidence of successful build on macOS 15+ Apple Silicon from this repository only | **ASSUMPTION:** Store as text file in `evidence/` directory or inline in `MEMORY.md` build verification section. |

### Status Update

Upon successful completion of Steps 1-8:
- Update `_STATUS.md` per lifecycle rules (state transition as authorized by the controlling agent).
- Record completion evidence in `MEMORY.md` under appropriate sections.
