# Guidance: DEL-02-05 Frontend Workflow Shell Baseline

---

## Purpose

DEL-02-05 exists to establish the **structural frame** of the Chirality desktop application's frontend. Without this shell, none of the other PKG-02 deliverables (FileTree refresh, Portal-Pipeline navigation, toolkit panel, layout/theme) have a host surface to plug into. Likewise, the harness API baseline (DEL-03-07) has no consumer-facing surface until this shell exists.

This deliverable is positioned as **FE-3** in the phased frontend baseline plan (`docs/PLAN.md` Section 2), meaning it depends on the workspace bootstrap (FE-1, DEL-01-03) and the harness API baseline (FE-2, DEL-03-07) being available. It is part of the pre-tier gate: Tier-2 frontend-dependent work is blocked until DEL-02-05 reaches at least `IN_PROGRESS`.

Source: Decomposition Scope Amendment A1; `docs/PLAN.md` Section 2; `_CONTEXT.md`.

---

## Principles

### P1: Shell First, Behavior Later

This deliverable provides the **structural containers** (frames, panels, wiring) but does not implement the full interactive behaviors that populate them. The file tree panel is a container here; refresh behavior belongs to DEL-02-01. The chat panel is a container here; session/turn integration belongs to DEL-03-01/DEL-03-02. This separation keeps the shell deliverable focused and prevents scope creep.

Source: Decomposition deliverable partitioning (PKG-02 has five deliverables with distinct scope items).

### P2: Matrix-Driven Navigation is the Core UX Pattern

The 3x4 Agent Matrix is the primary navigation model for the desktop UI. Every agent interaction flows through matrix cell selection. The shell must faithfully render this matrix structure and its routing rules (NORMATIVE/EVALUATIVE -> WORKBENCH, OPERATIVE -> PIPELINE). Deviating from the matrix model would break the conceptual alignment between agent architecture and UI surface.

Source: `AGENTS.md` Section 3; `docs/PLAN.md` Section 2.

### P3: Working Root is the Anchor

The Working Root (`projectRoot`) is the foundational context for all agent operations. The shell must ensure that once a directory is selected, all downstream surfaces (file tree, session boot, pipeline scoping) operate against that root. This is not merely a convenience feature -- it is the mechanism by which "filesystem is the state" (`SOW-014`, `docs/DIRECTIVE.md`) becomes operable in the UI.

Source: Decomposition vocabulary map; SOW-003; SOW-046.

### P4: Local-Only Execution Discipline

OBJ-008 requires that the frontend runtime baseline exists and is executable from this repository only. This means:
- No external repository clones are needed to build or run.
- All source, config, and build tooling is present in the tracked tree.
- The `frontend/` workspace (DEL-01-03) is the prerequisite scaffold.

Source: OBJ-008; `docs/PLAN.md` Local-Only Source Policy.

### P5: Pre-Tier Gate Responsibility

This deliverable, together with DEL-01-03, DEL-03-07, and DEL-07-03, forms the pre-tier gate for frontend-dependent Tier-2 work. Progressing this deliverable efficiently unblocks downstream execution. However, speed must not compromise the structural correctness of the shell -- a broken shell frame will create systemic rework across all PKG-02 deliverables.

Source: Scope Amendment A1, Execution Gating Rule.

---

## Considerations

### C1: Relationship to Sibling PKG-02 Deliverables

| Sibling | Relationship | Integration Surface | Suggested Interface Contract (Ref: D-002) |
|---------|-------------|---------------------|--------------------------------------------|
| DEL-02-01 (FileTree Refresh) | DEL-02-05 provides the file tree panel container; DEL-02-01 adds refresh behavior | File tree component API | **ASSUMPTION:** Minimum props: `rootPath: string`, `onFileSelect?: (path: string) => void`. DEL-02-01 would extend with refresh callbacks and configuration. |
| DEL-02-02 (Portal-Pipeline Navigation) | DEL-02-05 provides the PORTAL/PIPELINE frame; DEL-02-02 adds navigation semantics and shared state | Page routing and state hooks | **ASSUMPTION:** Minimum hooks: `useCurrentPage(): PageType`, `useNavigate(): (target: PageType, context?: AgentContext) => void`. DEL-02-02 would extend with shared deliverable state. |
| DEL-02-03 (Operator Toolkit) | DEL-02-05 provides the shell layout; DEL-02-03 adds the toolkit panel | Layout slot or panel region | **ASSUMPTION:** Minimum contract: a named layout slot (e.g., `<ToolkitSlot />` or `children` prop region) that DEL-02-03 can mount into without shell changes. |
| DEL-02-04 (Multipane Layout + Theme) | DEL-02-05 provides the base panel structure; DEL-02-04 adds resizing, collapsing, and theme hardening | Panel container and CSS architecture | **ASSUMPTION:** Minimum contract: panel containers expose `className` or `style` props and use CSS custom properties (variables) for dimensions, allowing DEL-02-04 to override layout behavior. |

**Guidance:** Design the shell with clear component boundaries and well-defined props/interfaces so that sibling deliverables can plug in without requiring shell refactoring. The suggested interface contracts above are **ASSUMPTION (best-effort sketches)** -- the component interface design approach is left to the implementer, but the four integration surfaces above are the minimum interfaces to plan for. Implementers should validate these prop signatures against sibling deliverable specifications as they become available. (Ref: D-002)

### C2: Agent Matrix Data Source

The Agent Matrix structure is defined in `AGENTS.md` Section 3. The shell must render this structure faithfully. Two approaches are plausible:
- **Hard-coded matrix:** Embed the matrix data directly in frontend code. Simple but requires code changes when the agent suite evolves.
- **Configuration-driven matrix:** Load matrix data from a configuration file or structured data source. More maintainable but adds complexity.

**Guidance:** TBD -- this is an implementation decision. Either approach satisfies the specification, but the choice affects how DEL-02-02 (navigation semantics) and future agent additions interact with the shell.

### C2a: Next.js Routing Architecture Decision (Ref: D-001)

A prerequisite decision for page route structure is whether the shell uses Next.js **App Router** or **Pages Router**:

- **App Router** (`frontend/app/` directory): Uses React Server Components by default, supports layouts, loading states, and parallel routes natively. This is the recommended approach for new Next.js projects (Next.js 13+).
- **Pages Router** (`frontend/pages/` directory): Traditional file-based routing, simpler mental model, well-established patterns. No server components.

This choice affects:
- The file path structure for PORTAL, PIPELINE, and WORKBENCH page routes (see Datasheet File Location Expectations).
- How layout slots (shell frame, panel regions) are defined -- App Router uses `layout.tsx` files natively.
- How DEL-02-02 (navigation semantics) integrates with routing hooks.

**Guidance:** **ASSUMPTION:** App Router is the likely choice given the Electron + Next.js stack and the need for layout composition, but this is a decision that should be recorded explicitly. If App Router is selected, the layout hierarchy becomes: root layout (shell frame) -> page-specific layouts (PORTAL, PIPELINE, WORKBENCH) -> content. The Specification Standards table notes this as an open decision.

Source: Next.js documentation; `docs/PLAN.md` Section 2 (mentions Next.js but does not specify router variant); D-001 lensing item.

### C3: Directory Selection Mechanism

The directory selection for Working Root binding could use:
- Native Electron dialog (`dialog.showOpenDialog`) -- platform-appropriate, familiar to macOS users.
- Custom in-app picker -- more control but more implementation effort.

**Guidance:** **ASSUMPTION:** Native Electron dialog is the expected approach given macOS-only target and standard Electron patterns. The specification requires that the selected path be validated as a valid local directory.

### C4: PIPELINE Disabled Variant Rendering

The option policy from `docs/PLAN.md` states: "Requested but unsupported variants remain visible as disabled entries, intentionally non-selectable, rendered as 'coming soon'." This means the shell must handle the distinction between enabled and disabled dropdown options from the start.

Source: `docs/PLAN.md` Section 2.

### C5: Frontend Workspace and Harness API Prerequisites

This deliverable (FE-3) depends on:
1. **DEL-01-03 (FE-1, Frontend Workspace Bootstrap)** providing the `frontend/` scaffold. Procedure Step 1 includes an explicit verification check for this prerequisite.
2. **DEL-03-07 (FE-2, Harness API Baseline)** providing baseline route surfaces for session/turn APIs. The phased plan states FE-1 -> FE-2 -> FE-3 ordering, and REQ-08 references propagation to "harness session boot context" -- this integration depends on FE-2 availability.

**Rationale for FE-2 readiness assessment (Ref: E-001):** The Procedure (Step 1) currently validates only the FE-1 workspace but does not include a readiness check for FE-2. The phased plan ordering implies FE-2 is available before FE-3 proceeds, but this is stated as an ASSUMPTION in Procedure prerequisites. Implementers should assess DEL-03-07 status before beginning Step 7 (project-root wiring to harness session boot). If DEL-03-07 is not available, the harness session boot integration point in Step 7.5 should be implemented as a stub with an explicit deferral note.

**ASSUMPTION:** The phased plan ordering (FE-1 -> FE-2 -> FE-3) implies both DEL-01-03 and DEL-03-07 reach a usable state before DEL-02-05 implementation proceeds in earnest. If FE-2 is not ready, DEL-02-05 can proceed with stub integration for the harness session boot wiring.

Source: `docs/PLAN.md` Section 2; Datasheet Conditions; _DEPENDENCIES.md DEP-0205-004, DEP-0205-005.

---

## Trade-offs

### T1: Shell Completeness vs. Speed to Unblock

**Tension:** The pre-tier gate incentivizes reaching `IN_PROGRESS` quickly. But a structurally incomplete shell creates rework for sibling deliverables.

**Guidance:** Prioritize correct frame structure (PORTAL/PIPELINE routing, panel slots, working root wiring) over polish. A shell that routes correctly but has placeholder content is more useful than a polished shell with wrong routing.

### T2: Structural Container Depth

**Tension:** How much internal structure should the shell provide for containers like the file tree panel and chat panel? Too little and sibling deliverables have no anchor. Too much and the shell overreaches its scope.

**Guidance:** Provide container components with clear mounting points and basic props (e.g., `rootPath` for file tree, `sessionId` for chat panel). Avoid implementing business logic within the shell -- that belongs to the specialized deliverables.

### T3: Static vs. Dynamic Matrix Data

**Tension:** Hard-coding the matrix is faster for the shell baseline but creates maintenance burden. Configuration-driven is more maintainable but adds complexity to a "baseline" deliverable.

**Guidance:** TBD -- either approach is valid for the baseline. If hard-coded, document the location where matrix data would need updating.

---

## Examples

### Example: Matrix Cell Selection Flow

1. Operator opens the application (UI boots to PORTAL page by default -- **ASSUMPTION**).
2. PORTAL page displays the 3x4 Agent Matrix.
3. Operator clicks the "ORCHESTRATE" cell (NORMATIVE/APPLYING).
4. Shell routes to the WORKBENCH page with the ORCHESTRATOR agent context.

Source: `AGENTS.md` Section 3 routing rules.

### Example: PIPELINE Category Selection Flow

1. Operator clicks "TASK*" cell (OPERATIVE/JUDGING) in the matrix.
2. Shell routes to the PIPELINE page with TASK* category pre-selected.
3. PIPELINE page shows the TASK* split selectors: Task Agent (static) and Scope (dynamic).
4. Scope selector enumerates deliverables from the current Working Root.

Source: `AGENTS.md` Section 3; `docs/PLAN.md` Section 2.

### Example: Working Root Selection Flow

1. Operator clicks directory selection control.
2. Native OS dialog opens (macOS Finder-based -- **ASSUMPTION**).
3. Operator selects a folder (e.g., `/Users/operator/projects/my-workspace`).
4. Shell binds the selected path as `projectRoot`.
5. File tree panel populates with the directory structure of the selected root.
6. Pipeline scope selectors scan the working root for deliverables.

Source: SOW-046; SOW-003.

---

## Conflict Table (for human ruling)

| Conflict ID | Conflict | Source A | Source B | Impacted Sections | Proposed Authority (PROPOSAL) | Human Ruling |
|-------------|----------|----------|----------|-------------------|-------------------------------|-------------|
| CONF-001 | **WORKBENCH page cardinality:** Is WORKBENCH a single page that receives different agent contexts (single route, parameterized), or does each agent get its own WORKBENCH page instance (multiple routes)? Specification REQ-02 says "opens the WORKBENCH page for that agent" (suggests single page + context); Datasheet shows one "WORKBENCH" row in UI Page column (suggests single page); Procedure Step 8.4 says "navigation to WORKBENCH" (ambiguous). The cardinality is not explicitly resolved. (Ref: B-005) | Specification REQ-02: "opens the WORKBENCH page for that agent" | Datasheet Agent Matrix Structure: single "WORKBENCH" column | Specification REQ-02; Datasheet Agent Matrix; Procedure Step 8 | **PROPOSAL:** Single WORKBENCH page with agent context parameter (e.g., `/workbench?agent=ORCHESTRATE` or `/workbench/[agent]`). This aligns with the "opens the WORKBENCH page **for** that agent" phrasing and avoids route proliferation. | TBD |

### Notes on Pass 3 Enrichment

The following items from semantic lensing were incorporated as TBD entries, new requirements, or rationale additions rather than conflicts, because they represent missing information rather than contradictory sources:
- A-001: Standards references marked for action (Specification Standards table)
- A-002: State management approach TBD (Specification REQ-08; Datasheet Construction)
- B-004: Default landing page promoted to REQ-12 (Specification)
- C-001: Persistence behavior clarified as TBD requiring human ruling (Specification REQ-08)
- C-002: Error handling promoted to REQ-13 (Specification)
- D-001: Routing architecture decision added as C2a (Guidance)
- D-003: Pre-tier gate acceptance promoted to REQ-14 (Specification)
- E-001: FE-2 readiness rationale added to C5 (Guidance)
- E-002: REQ-11 acceptance rubric defined (Specification)
- F-001: Accessibility promoted to REQ-15 as TBD_Question (Specification)
- F-002: Non-functional verification section added (Specification)
- F-003: Harness session boot verification added to REQ-08 row (Specification)
- X-002: Automated testing position added (Specification Verification section)
