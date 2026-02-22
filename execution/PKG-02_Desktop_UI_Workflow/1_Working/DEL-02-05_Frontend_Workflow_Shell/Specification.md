# Specification: DEL-02-05 Frontend Workflow Shell Baseline

---

## Scope

### Included

This deliverable covers the implementation of the baseline frontend workflow shell as defined by SOW-046:

1. **PORTAL/PIPELINE frame** -- The top-level page routing structure that presents PORTAL (matrix-based navigation) and PIPELINE (pipeline execution with category dropdowns) as distinct interaction surfaces.
2. **File tree panel** -- A live project directory browser displaying the contents of the selected Working Root (`projectRoot`).
3. **Chat panel** -- An interactive session panel for persona-mode agent interaction (WORKBENCH surface).
4. **Directory selection** -- A UI surface allowing the operator to select a local Working Root directory.
5. **Project-root wiring** -- Runtime binding that connects the selected `projectRoot` through to downstream harness session boot.

Source: `_CONTEXT.md`; SOW-046 in Decomposition Scope Amendment A1.

### Excluded

- **FileTree refresh behavior** (polling, focus/visibility refresh) -- covered by DEL-02-01 (SOW-022).
- **Portal-to-Pipeline navigation semantics and shared deliverables state** -- covered by DEL-02-02 (SOW-023, SOW-024).
- **Operator Toolkit panel and local presets** -- covered by DEL-02-03 (SOW-025).
- **Multi-pane layout behavior and theme hardening** -- covered by DEL-02-04 (SOW-026, SOW-027).
- **Harness API route implementation** -- covered by DEL-03-07 (SOW-045).
- **Frontend workspace bootstrap and packaging** -- covered by DEL-01-03 (SOW-044, SOW-047).
- **Session boot and turn execution APIs** -- covered by DEL-03-01 and DEL-03-02.

### Boundary Notes

This deliverable provides the **shell** -- the structural frame and panel layout -- that other PKG-02 deliverables populate with their specific behaviors. The file tree panel here is the structural container; refresh behavior is DEL-02-01. The chat panel here is the structural container; the session/turn API backing it is DEL-03-01/DEL-03-02/DEL-03-07.

---

## Requirements

### REQ-01: PORTAL/PIPELINE Frame Rendering

The frontend shall render two distinct top-level page frames:
- **PORTAL** -- presents the 3x4 Agent Matrix for navigation routing.
- **PIPELINE** -- presents pipeline execution UI with OPERATIVE row category dropdown menus.

Source: SOW-046; `AGENTS.md` Section 3; `docs/PLAN.md` Section 2.

### REQ-02: Agent Matrix Navigation Surface

The PORTAL page shall present a 3x4 matrix where:
- Rows are labeled NORMATIVE, OPERATIVE, EVALUATIVE.
- Columns are labeled GUIDING, APPLYING, JUDGING, REVIEWING.
- Each cell displays the agent/category name as defined in `AGENTS.md` Section 3.
- Selecting a NORMATIVE or EVALUATIVE cell opens the WORKBENCH page for that agent.
- Selecting an OPERATIVE cell opens the PIPELINE page with the corresponding category pre-selected.

Source: `AGENTS.md` Section 3; `docs/PLAN.md` Section 2.

### REQ-03: PIPELINE Category Dropdown Menus

The PIPELINE page shall provide dropdown menus for each OPERATIVE category:
- **DECOMP***: SOFTWARE, PROJECT, DOMAIN, BASE (create new)
- **PREP***: PREPARATION, 4_DOCUMENTS, CHIRALITY_FRAMEWORK, CHIRALITY_LENS
- **TASK***: Uses split selectors (Task Agent + Scope), not a single mixed list
- **AUDIT***: AGENTS, DEPENDENCIES, ESTIMATES, REFERENCES, SCHEDULES, SCOPE

Unsupported/unavailable variants shall be rendered as disabled "coming soon" entries (intentionally non-selectable).

Source: `AGENTS.md` Section 3; `docs/PLAN.md` Section 2.

### REQ-04: TASK* Split Selector Model

The TASK* pipeline category shall use split selectors:
- **Task Agent selector** (static options): SCOPE_CHANGE, SCOPE_PREP, ESTIMATE_PREP, AUDIT_PREP, SCHEDULE_PREP, ESTIMATING, SCHEDULING.
- **Scope selectors** (dynamic options):
  - Deliverables scanned from the selected Working Root.
  - Knowledge types scanned from canonical deliverable file types.
- Knowledge-type scope shall be shown only when a knowledge decomposition marker is found in `_Decomposition`.

Source: `docs/PLAN.md` Section 2.

### REQ-05: File Tree Panel

The shell shall include a file tree panel that:
- Displays the directory structure of the currently selected Working Root.
- Serves as the structural container for file browsing (refresh behavior is separately specified in DEL-02-01).

Source: SOW-046; `_CONTEXT.md`.

### REQ-06: Chat Panel

The shell shall include a chat panel that:
- Provides the interactive session surface for WORKBENCH-mode agent interaction.
- Serves as the structural container for message display and input (session/turn API integration is separately specified in DEL-03-01/DEL-03-02/DEL-03-07).

Source: SOW-046; `_CONTEXT.md`.

### REQ-07: Directory Selection

The shell shall provide a directory selection UI that:
- Allows the operator to choose a local filesystem directory as the Working Root (`projectRoot`).
- Validates that the selected path is a valid local directory.
- **ASSUMPTION:** The directory selection UI uses a native OS dialog or equivalent picker appropriate to macOS 15+.

Source: SOW-046; `_CONTEXT.md`.

### REQ-08: Project-Root Wiring

The selected `projectRoot` shall be:
- Bound to the application state such that downstream components (file tree panel, harness session boot, pipeline scoping) can access the current Working Root.
- Persisted across the current application session. **TBD (requires human ruling): Persistence across application restarts** -- determine whether `projectRoot` persists only in-memory (lost on quit) or is stored to local storage/filesystem (restored on relaunch). This choice affects UX flow and implementation scope. (Ref: C-001)
- **TBD: State management approach** -- the mechanism for sharing `projectRoot` across components (e.g., React Context, Zustand, Redux) is unspecified. REQ-08 mandates binding to "application state" but the approach must be selected. (Ref: A-002)

Source: SOW-046; `_CONTEXT.md`; Decomposition vocabulary ("Working Root").

### REQ-09: Platform Target

The frontend workflow shell shall build and run on macOS 15+, Apple Silicon only. No other platform targets are required.

Source: `DEC-PLAT-001` in Decomposition Decision Log.

### REQ-10: Local-Only Execution

The frontend workflow shell shall be executable from this repository only. No external repositories or non-local runtime dependencies shall be required.

Source: OBJ-008 acceptance criteria.

### REQ-11: End-to-End UI Boot Demonstration

A local run shall demonstrate end-to-end UI boot and route wiring against local workspace data. This constitutes the acceptance evidence for DEL-02-05.

**Measurable acceptance criterion:** All sub-steps enumerated in Procedure Step 8 (Steps 8.1 through 8.10) shall pass successfully. A pass/fail rubric is: each sub-step produces the expected visual or behavioral outcome as described; any sub-step failure constitutes an overall REQ-11 failure. (Ref: E-002)

Source: `docs/PLAN.md` Section 2, FE-3 acceptance; `_CONTEXT.md`.

### REQ-12: Default Landing Page (Ref: B-004)

On application boot, the UI shall navigate to the PORTAL page by default.

**ASSUMPTION:** This is assumed based on Guidance Examples and Procedure Step 8.2 but was not previously stated as a requirement. Human ruling should confirm whether PORTAL is the correct default or if a different landing behavior is intended.

Source: Guidance Examples; Procedure Step 8.2; `AGENTS.md` Section 3.

### REQ-13: Error State Handling (Ref: C-002)

The shell shall handle the following error conditions gracefully:
- **Directory selection failure:** If the operator cancels the directory selection dialog or selects an invalid path, the shell shall display an appropriate message and retain the previous `projectRoot` state (or remain in the unset state).
- **Invalid working root:** If the bound `projectRoot` path becomes invalid (e.g., directory deleted while application is running), the shell shall indicate the error state to the operator.
- **Unknown route:** If navigation attempts to reach an undefined route, the shell shall display a fallback page or redirect to PORTAL.

**ASSUMPTION:** Specific error message text, styling, and UX flow for error states are implementation decisions, but the above conditions must be handled rather than producing unhandled exceptions or blank screens.

Source: Standard UI engineering practice; C-002 lensing item.

### REQ-14: Pre-Tier Gate Acceptance Criterion (Ref: D-003)

TBD -- Define what evidence is required to assert that DEL-02-05 has reached `IN_PROGRESS` for the purpose of pre-tier gate evaluation. **ASSUMPTION:** The gate condition "DEL-02-05 must reach at least IN_PROGRESS" (Datasheet Conditions; Guidance P5) requires a concrete definition of what constitutes IN_PROGRESS -- e.g., Step 1 + Step 2 of Procedure complete, or a subset of REQs verified.

Source: Datasheet Conditions; Guidance P5; Scope Amendment A1 Execution Gating Rule.

### REQ-15: Accessibility Considerations (Ref: F-001)

TBD -- Determine whether the baseline shell requires accessibility features such as:
- Keyboard navigation of the Agent Matrix (arrow keys to move between cells, Enter to select).
- Focus management for directory selection dialog (focus returns to trigger element after dialog closes).
- Semantic HTML landmarks or ARIA attributes for the shell layout regions.

**TBD_Question:** Does the baseline shell require accessibility support, or is this deferred to a later deliverable? If deferred, record an explicit scope exclusion. If required, define minimum accessibility requirements.

Source: Standard UI engineering practice; F-001 lensing item.

---

## Standards

| Standard/Reference | Applicability | Accessible | Status / Notes | Source |
|--------------------|---------------|------------|----------------|--------|
| `AGENTS.md` Section 3 | Agent Matrix definition, cell-to-page routing, PIPELINE categories | Yes | Read and incorporated | `AGENTS.md` |
| `docs/PLAN.md` Section 2 | Frontend phased plan (FE-3), matrix navigation, TASK* selector model, option policy | Yes | Read and incorporated | `docs/PLAN.md` |
| `docs/SPEC.md` | Canonical filesystem structures, harness contract | **location TBD** -- referenced but not read for this pass | **Action needed:** Confirm path exists, read relevant sections, and update clause-level applicability. (Ref: A-001) | Decomposition references |
| `docs/TYPES.md` | Canonical vocabulary (Working Root, Execution Root, etc.) | **location TBD** -- referenced but not read for this pass | **Action needed:** Confirm path exists, read to verify vocabulary alignment. (Ref: A-001) | Decomposition vocabulary map |
| `docs/CONTRACT.md` | Binding invariants (K-*) | **location TBD** -- referenced but not read for this pass | **Action needed:** Confirm path exists, read to identify binding invariants applicable to the shell. (Ref: A-001) | Decomposition references |
| Next.js routing conventions | Page/route structure | **ASSUMPTION:** Standard Next.js App Router or Pages Router conventions apply | **Decision needed:** App Router vs. Pages Router choice affects page route structure for PORTAL, PIPELINE, WORKBENCH (see Guidance D-001 for rationale). (Ref: D-001) | Technology stack |
| Electron desktop shell conventions | Window management, native dialogs | **ASSUMPTION:** Standard Electron patterns for macOS apply | -- | Technology stack |

---

## Verification

### Automated Testing Position (Ref: X-002)

**TBD (requires human ruling):** Determine whether automated tests (unit or integration) are expected as part of the acceptance evidence for this baseline deliverable, or whether manual verification is the sole assessment approach. Current verification rows use only "Manual inspection." If automated tests are required, specify minimum coverage expectations (e.g., matrix rendering, route navigation, directory selection flow). If manual-only is intentional, record this as an explicit decision.

### Verification Matrix

| Requirement | Verification Approach | Evidence |
|-------------|----------------------|----------|
| REQ-01 | Manual inspection: PORTAL and PIPELINE pages render as distinct frames | Screenshot or recording of page navigation |
| REQ-02 | Manual inspection: Matrix renders 3x4 with correct labels; cell selection routes correctly | Screenshot showing matrix; recording of navigation flow |
| REQ-03 | Manual inspection: Each OPERATIVE category shows correct dropdown options | Screenshot of each dropdown in expanded state |
| REQ-04 | Manual inspection: TASK* shows split selectors; dynamic scope populates from working root | Screenshot of split selector UI; demonstration with a workspace |
| REQ-05 | Manual inspection: File tree panel renders directory structure of selected working root | Screenshot showing file tree with a local workspace |
| REQ-06 | Manual inspection: Chat panel renders and accepts input | Screenshot of chat panel |
| REQ-07 | Manual inspection: Directory selection dialog opens and selected path is accepted | Screenshot or recording of directory selection flow |
| REQ-08 | Manual inspection: After selecting a directory, file tree and other components reflect the chosen path. **Additionally:** verify `projectRoot` propagation reaches harness session boot context (stub-level confirmation acceptable). (Ref: F-003) | End-to-end demonstration; console log or state inspector showing `projectRoot` value in session boot context |
| REQ-09 | Build-log verification: confirm target architecture is `arm64`/`darwin` in build output; supplemented by manual run confirmation on Apple Silicon hardware. (Ref: A-003) | Build log with architecture indicators + run screenshot |
| REQ-10 | Build-log verification: confirm no external repository fetches during build (review `npm install` output for registry-only dependencies, no git clone operations); supplemented by manual confirmation. (Ref: A-003) | Build log demonstrating local-only execution |
| REQ-11 | End-to-end local run demonstrating UI boot and route wiring; **pass/fail rubric:** all 10 sub-steps in Procedure Step 8 must pass (Ref: E-002) | Recording or screenshot sequence of boot -> matrix -> navigation -> panels |
| REQ-12 | Manual inspection: Application boot lands on PORTAL page | Screenshot of initial application state after launch |
| REQ-13 | Manual inspection: (a) Cancel directory selection -- shell remains stable; (b) Navigate to unknown route -- fallback renders; (c) If feasible, invalidate working root path while running -- error state displays | Screenshots or recording of each error scenario |
| REQ-14 | TBD -- verification approach depends on the definition of IN_PROGRESS evidence | TBD |
| REQ-15 | TBD -- verification approach depends on whether accessibility requirements are confirmed | TBD |

### Non-Functional Verification (Ref: F-002)

| Concern | Verification Approach | Evidence | Status |
|---------|----------------------|----------|--------|
| Initial page load time | TBD -- define acceptable load time budget on target hardware (macOS 15+, Apple Silicon) | Performance measurement (browser dev tools or Electron profiling) | **TBD: No performance requirement currently specified. Human ruling needed on whether a load-time budget applies to the baseline.** |
| Shell rendering performance | TBD -- define acceptable frame rate or rendering latency for matrix interaction | Performance measurement | **TBD: Deferred pending human ruling.** |

---

## Documentation

### Required Artifacts

| Artifact Type | Description | Source |
|---------------|-------------|--------|
| CODE | Frontend source files implementing the workflow shell (page routes, components, wiring) | `_CONTEXT.md` anticipated artifacts |
| CONFIG | Configuration files for routing, build, and shell layout | `_CONTEXT.md` anticipated artifacts |

### Related Documentation

- DEL-01-03 provides the frontend workspace bootstrap (`frontend/` scaffold, package.json, build scripts).
- DEL-03-07 provides the harness API baseline routes that the chat panel and pipeline execution connect to.
- DEL-02-01 through DEL-02-04 provide specific behaviors (refresh, navigation semantics, toolkit, layout) that plug into this shell.
