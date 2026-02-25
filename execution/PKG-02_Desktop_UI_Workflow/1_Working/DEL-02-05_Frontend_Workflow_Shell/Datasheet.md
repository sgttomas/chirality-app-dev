# Datasheet: DEL-02-05 Frontend Workflow Shell Baseline

---

## Identification

| Field | Value |
|-------|-------|
| **Deliverable ID** | DEL-02-05 |
| **Name** | Frontend Workflow Shell Baseline |
| **Package** | PKG-02 Desktop UI Workflow |
| **Type** | UX_UI_SLICE |
| **Context Envelope** | L |
| **Responsible Party** | TBD -- **TBD_Question: Who owns implementation of this deliverable? To be assigned by project manager.** (Ref: B-001) |
| **Scope Coverage** | SOW-046 |
| **Supports Objectives** | OBJ-005, OBJ-008 |
| **Anticipated Artifacts** | CODE, CONFIG |
| **Amendment** | Scope Amendment A1 (SCA-001, 2026-02-22) |

---

## Attributes

### Technology Stack

| Attribute | Value | Source |
|-----------|-------|--------|
| Framework (rendering) | Next.js | `docs/PLAN.md` Section 2 |
| Desktop shell | Electron | `docs/PLAN.md` Section 2 |
| Language | TypeScript | `docs/PLAN.md` Section 2 |
| Target platform | macOS 15+, Apple Silicon only | Decomposition `DEC-PLAT-001` |
| Navigation model | 3x4 Agent Matrix | `AGENTS.md` Section 3 |
| Routing targets | WORKBENCH (NORMATIVE, EVALUATIVE rows), PIPELINE (OPERATIVE row) | `AGENTS.md` Section 3 |

### UI Component Inventory

| Component | Description | Source |
|-----------|-------------|--------|
| PORTAL page | Top-level page presenting the 3x4 Agent Matrix for navigation routing | SOW-046; `docs/PLAN.md` Section 2; `AGENTS.md` Section 3 |
| PIPELINE page | Top-level page presenting pipeline execution UI with OPERATIVE row category dropdowns | SOW-046; `docs/PLAN.md` Section 2; `AGENTS.md` Section 3 |
| WORKBENCH page | Top-level page hosting agent interaction for NORMATIVE and EVALUATIVE matrix cell selections; receives agent context from matrix routing | `AGENTS.md` Section 3; Specification REQ-01, REQ-02 (Ref: B-003) |
| File tree panel | Live project directory browser for the selected Working Root | SOW-046; `_CONTEXT.md` |
| Chat panel | Interactive session panel for persona-mode agent interaction | SOW-046; `_CONTEXT.md` |
| Directory selection | UI surface for selecting/binding a local Working Root (`projectRoot`) | SOW-046; `_CONTEXT.md` |
| Project-root wiring | Runtime binding from selected `projectRoot` through to harness session boot | SOW-046; `_CONTEXT.md` |

### Agent Matrix Structure (Navigation Source)

The 3x4 Agent Matrix determines how the UI routes operator intent.

| Row | Guiding | Applying | Judging | Reviewing | UI Page |
|-----|---------|----------|---------|-----------|---------|
| **NORMATIVE** | HELP | ORCHESTRATE | WORKING_ITEMS | AGGREGATE | WORKBENCH |
| **OPERATIVE** | DECOMP* | PREP* | TASK* | AUDIT* | PIPELINE |
| **EVALUATIVE** | AGENTS | DEPENDENCIES | CHANGE | RECONCILING | WORKBENCH |

Source: `AGENTS.md` Section 3.

### PIPELINE Category Dropdowns (OPERATIVE Row)

| Category | Dropdown Options | Source |
|----------|------------------|--------|
| DECOMP* | SOFTWARE, PROJECT, DOMAIN, BASE (create new) | `AGENTS.md` Section 3 |
| PREP* | PREPARATION, 4_DOCUMENTS, CHIRALITY_FRAMEWORK, CHIRALITY_LENS | `AGENTS.md` Section 3 |
| TASK* | SCOPE_CHANGE, SCOPE_PREP, ESTIMATE_PREP, AUDIT_PREP, SCHEDULE_PREP, ESTIMATING, SCHEDULING, "all deliverables", "all knowledge types" | `AGENTS.md` Section 3 |
| AUDIT* | AGENTS, DEPENDENCIES, ESTIMATES, REFERENCES, SCHEDULES, SCOPE | `AGENTS.md` Section 3 |

### TASK* Selector Model

| Attribute | Value | Source |
|-----------|-------|--------|
| Selector approach | Split selectors (not mixed list) | `docs/PLAN.md` Section 2 |
| Static selector | Task Agent (fixed options) | `docs/PLAN.md` Section 2 |
| Dynamic selectors | Scope — deliverables from working root, knowledge types from canonical types | `docs/PLAN.md` Section 2 |
| Knowledge-type scope visibility | Only when knowledge decomposition marker found in `_Decomposition` | `docs/PLAN.md` Section 2 |
| Disabled variant policy | Unsupported variants shown as disabled "coming soon" entries | `docs/PLAN.md` Section 2 |

---

## Conditions

| Condition | Value | Source |
|-----------|-------|--------|
| Platform | macOS 15+, Apple Silicon only | `DEC-PLAT-001` |
| Frontend runtime location | `frontend/` in this repository | `docs/PLAN.md` Section 2, Local-Only Source Policy |
| No external repo dependency | All runtime surfaces must be executable from this repository only | OBJ-008 acceptance criteria |
| Outbound network | Anthropic API only (per `DEC-NET-001`) | Decomposition Decision Log |
| Pre-tier gate | DEL-02-05 must reach at least `IN_PROGRESS` before Tier-2 frontend-dependent work proceeds | Scope Amendment A1, Execution Gating Rule |
| Phased plan position | FE-3 (after FE-1 workspace bootstrap DEL-01-03, FE-2 harness API baseline DEL-03-07) | `docs/PLAN.md` Section 2 |

---

## Construction

### Logical Structure

| Layer | Components | Notes |
|-------|------------|-------|
| Page routing | PORTAL page, PIPELINE page, WORKBENCH page | Matrix-driven; NORMATIVE/EVALUATIVE -> WORKBENCH, OPERATIVE -> PIPELINE |
| Navigation | Agent Matrix cell selection, category dropdown menus | 3x4 matrix with composite OPERATIVE categories |
| Panels | File tree panel, chat panel | Positioned within the shell layout |
| Working Root binding | Directory selection UI, `projectRoot` wiring | Connects UI to harness session boot |
| State management | TBD -- the mechanism for sharing `projectRoot` and navigation context across components (e.g., React Context, Zustand, Redux, or other) is unspecified | **ASSUMPTION:** Shared deliverables state (SOW-024, assigned to DEL-02-02) is a sibling concern; this deliverable provides the shell frame that hosts it. However, REQ-08 mandates `projectRoot` binding to "application state" -- the approach for this local shell state is TBD and must be resolved before or during implementation. (Ref: A-002) |

### File Location Expectations

| Path | Purpose | Source |
|------|---------|--------|
| `frontend/` | Root of frontend workspace | `docs/PLAN.md` Section 2 |
| `frontend/package.json` | Package manifest | `docs/PLAN.md` FE-1 acceptance |
| `frontend/app/portal/` (or equivalent) | Next.js page route for PORTAL | **ASSUMPTION:** Standard Next.js App Router conventions; exact path depends on routing architecture decision (see Guidance D-001). (Ref: B-002) |
| `frontend/app/pipeline/` (or equivalent) | Next.js page route for PIPELINE | **ASSUMPTION:** Standard Next.js App Router conventions. (Ref: B-002) |
| `frontend/app/workbench/` (or equivalent) | Next.js page route for WORKBENCH | **ASSUMPTION:** Standard Next.js App Router conventions. (Ref: B-002) |
| `frontend/components/` (or equivalent) | Component files for file tree, chat panel, directory selection, matrix | **ASSUMPTION:** Standard component directory convention; to be confirmed during implementation. (Ref: B-002) |

---

## References

| Ref | Path/ID | Used For |
|-----|---------|----------|
| Decomposition | `execution/_Decomposition/ChiralityApp_SoftwareDecomposition_2026-02-21_G7-APPROVED.md` | Deliverable definition, scope coverage, objectives |
| Strategic plan | `docs/PLAN.md` Section 2 | Frontend phased plan (FE-3), matrix navigation, TASK* selector model |
| Agent framework | `AGENTS.md` Section 3 | Agent Matrix definition, UI page routing, PIPELINE categories |
| Context file | `execution/PKG-02_Desktop_UI_Workflow/1_Working/DEL-02-05_Frontend_Workflow_Shell/_CONTEXT.md` | Deliverable identity and scope statement |
| Dependencies file | `execution/PKG-02_Desktop_UI_Workflow/1_Working/DEL-02-05_Frontend_Workflow_Shell/_DEPENDENCIES.md` | Dependency declarations (none declared yet) |
