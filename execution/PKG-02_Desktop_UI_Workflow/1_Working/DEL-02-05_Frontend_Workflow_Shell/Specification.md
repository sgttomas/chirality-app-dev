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
- Persisted across the current application session. **ASSUMPTION:** Persistence across application restarts is TBD (likely convenience state, not project truth).

Source: SOW-046; `_CONTEXT.md`; Decomposition vocabulary ("Working Root").

### REQ-09: Platform Target

The frontend workflow shell shall build and run on macOS 15+, Apple Silicon only. No other platform targets are required.

Source: `DEC-PLAT-001` in Decomposition Decision Log.

### REQ-10: Local-Only Execution

The frontend workflow shell shall be executable from this repository only. No external repositories or non-local runtime dependencies shall be required.

Source: OBJ-008 acceptance criteria.

### REQ-11: End-to-End UI Boot Demonstration

A local run shall demonstrate end-to-end UI boot and route wiring against local workspace data. This constitutes the acceptance evidence for DEL-02-05.

Source: `docs/PLAN.md` Section 2, FE-3 acceptance; `_CONTEXT.md`.

---

## Standards

| Standard/Reference | Applicability | Accessible | Source |
|--------------------|---------------|------------|--------|
| `AGENTS.md` Section 3 | Agent Matrix definition, cell-to-page routing, PIPELINE categories | Yes | `AGENTS.md` |
| `docs/PLAN.md` Section 2 | Frontend phased plan (FE-3), matrix navigation, TASK* selector model, option policy | Yes | `docs/PLAN.md` |
| `docs/SPEC.md` | Canonical filesystem structures, harness contract | **location TBD** -- referenced but not read for this pass | Decomposition references |
| `docs/TYPES.md` | Canonical vocabulary (Working Root, Execution Root, etc.) | **location TBD** -- referenced but not read for this pass | Decomposition vocabulary map |
| `docs/CONTRACT.md` | Binding invariants (K-*) | **location TBD** -- referenced but not read for this pass | Decomposition references |
| Next.js routing conventions | Page/route structure | **ASSUMPTION:** Standard Next.js App Router or Pages Router conventions apply | Technology stack |
| Electron desktop shell conventions | Window management, native dialogs | **ASSUMPTION:** Standard Electron patterns for macOS apply | Technology stack |

---

## Verification

| Requirement | Verification Approach | Evidence |
|-------------|----------------------|----------|
| REQ-01 | Manual inspection: PORTAL and PIPELINE pages render as distinct frames | Screenshot or recording of page navigation |
| REQ-02 | Manual inspection: Matrix renders 3x4 with correct labels; cell selection routes correctly | Screenshot showing matrix; recording of navigation flow |
| REQ-03 | Manual inspection: Each OPERATIVE category shows correct dropdown options | Screenshot of each dropdown in expanded state |
| REQ-04 | Manual inspection: TASK* shows split selectors; dynamic scope populates from working root | Screenshot of split selector UI; demonstration with a workspace |
| REQ-05 | Manual inspection: File tree panel renders directory structure of selected working root | Screenshot showing file tree with a local workspace |
| REQ-06 | Manual inspection: Chat panel renders and accepts input | Screenshot of chat panel |
| REQ-07 | Manual inspection: Directory selection dialog opens and selected path is accepted | Screenshot or recording of directory selection flow |
| REQ-08 | Manual inspection: After selecting a directory, file tree and other components reflect the chosen path | End-to-end demonstration |
| REQ-09 | Build and run on macOS 15+ Apple Silicon machine | Build log + run screenshot |
| REQ-10 | Build and run using only this repository (no external clones) | Build log demonstrating local-only execution |
| REQ-11 | End-to-end local run demonstrating UI boot and route wiring | Recording or screenshot sequence of boot -> matrix -> navigation -> panels |

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
