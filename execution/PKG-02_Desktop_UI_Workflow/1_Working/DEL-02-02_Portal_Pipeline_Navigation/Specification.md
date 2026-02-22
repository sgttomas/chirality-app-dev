# Specification — DEL-02-02 Portal->Pipeline Navigation & Deliverable Key Semantics

## Scope

### Included

This deliverable covers the implementation and verification of:

1. **Portal-to-Pipeline navigation** for deliverable-scoped `TASK*` variants, where clicking a deliverable row in the PORTAL matrix routes the operator to the PIPELINE view with the corresponding deliverable pre-selected. (SOW-023; `docs/PLAN.md` Section 2)
2. **Shared deliverables state** at page-level used by both PORTAL and PIPELINE views, ensuring consistent deliverable data across navigation transitions. (SOW-024; `docs/PLAN.md` Section 2)

### Excluded

- FileTree refresh behavior (covered by DEL-02-01).
- Operator Toolkit panel and local presets (covered by DEL-02-03).
- Multi-pane layout and theme hardening (covered by DEL-02-04).
- Harness session/turn execution (covered by PKG-03 deliverables).
- Knowledge-type scope mode implementation details beyond what is needed for deliverable key semantics. **ASSUMPTION: knowledge-type scope integration is exercised only to the extent that deliverable composite keys are correctly formed and cleared; deep knowledge-type pipeline logic may belong to a separate deliverable or future scope.** See Guidance C5 for clarification of this boundary.

---

## Requirements

### REQ-01: PORTAL Matrix Row Click Routes to PIPELINE

When an operator clicks a deliverable row in the PORTAL OPERATIVE row, the UI MUST navigate to the PIPELINE view with `TASK*` as the active pipeline category and the clicked deliverable's composite key (`pkg::id`) pre-selected in the scope selector.

- **Source:** `docs/PLAN.md` Section 2 ("Deliverable row click in PORTAL routes to PIPELINE TASK* and selects the corresponding deliverable key")
- **Source:** `docs/SPEC.md` Section 14.1 (OPERATIVE row -> PIPELINE destination)
- **Note:** No navigation transition timing threshold (e.g., maximum latency) is specified in governance docs. TBD — a performance target should be established to prevent arbitrarily slow transitions from passing verification. (`docs/SPEC.md` Section 14.1 — **location TBD** for timing requirements)

### REQ-02: TASK* is Deliverables-Only (No Fallback Static Variants)

The TASK* pipeline category MUST present deliverable-scoped dynamic options. There MUST NOT be fallback static variants.

- **Source:** `docs/PLAN.md` Section 2 ("TASK* is deliverables-only (no fallback static variants)")

### REQ-03: Explicit Loading, Empty, and Error States

The TASK* selector MUST show explicit loading states while deliverable data is being fetched and explicit empty states when no deliverables are available.

Additionally, the UI MUST handle API error responses from `/api/project/deliverables` distinctly from loading and empty states. TBD — the specific error state UI (e.g., error message, retry affordance) is not specified in governance docs. (`docs/SPEC.md` Section 15 — **location TBD** for error response contract)

- **Source:** `docs/PLAN.md` Section 2 ("selector shows explicit loading and empty states")
- **Note:** Error state handling is not explicitly specified in `docs/PLAN.md` or `docs/SPEC.md` Section 15; added as a gap identified through semantic lensing. **ASSUMPTION: API error states require distinct UI treatment from loading and empty states.**

### REQ-04: Deliverable Composite Key Format

Deliverable selection state MUST use composite keys in `pkg::id` format (e.g., `PKG-02_Desktop_UI_Workflow::DEL-02-02`).

- **Source:** `docs/PLAN.md` Section 2 ("pkg::id composite keys")
- **Note:** The `pkg` segment is the package folder label (e.g., `PKG-02_Desktop_UI_Workflow`), not the bare PackageID. TBD — confirm canonical key construction rule in `docs/PLAN.md` Section 2. See Datasheet > Attributes > Deliverable Key -- `pkg` Segment.

### REQ-05: Shared Deliverables State at Page Level

Deliverables state MUST be maintained at page-level scope (e.g., in `page.tsx`) and shared between PORTAL and PIPELINE views. Both views MUST read from the same state source.

- **Source:** `docs/PLAN.md` Section 2 ("Shared deliverables state at page-level (page.tsx) used by both PORTAL and PIPELINE views")

### REQ-06: Stale Selection Key Clearing

The UI MUST clear stale deliverable variant keys when:

1. The project root changes.
2. A deliverable fetch fails.
3. The selected deliverable key is no longer present in scan results.
4. Knowledge decomposition marker is absent while knowledge-type scope is selected.
5. A selected knowledge type no longer resolves to available target deliverables.

- **Source:** `docs/PLAN.md` Section 2 ("Stale deliverable variant keys are cleared when root changes or deliverable fetch fails")
- **Source:** `docs/SPEC.md` Section 14.5 (Stale Selection Reset Rules — full trigger list)

### REQ-07: Disabled Option Visibility

Requested but unsupported pipeline variants MUST be visible to operators as disabled entries and labeled as "coming soon" (or equivalent disabled hint). They MUST NOT be silently omitted and MUST NOT be selectable.

- **Source:** `docs/SPEC.md` Section 14.4

### REQ-08: Split Selector Model for TASK*

TASK* MUST use split selectors rather than a single mixed list:

- `Task Agent` (static options)
- `Scope Mode` (`DELIVERABLES` or `KNOWLEDGE_TYPES`)
- `Scope` (dynamic list based on mode)
- `Target Deliverable` (required when scope mode is `KNOWLEDGE_TYPES`)

- **Source:** `docs/PLAN.md` Section 2
- **Source:** `docs/SPEC.md` Section 14.3

### REQ-09: Knowledge Decomposition Gating

Knowledge-type scope MUST be shown only when a knowledge decomposition marker is found in `_Decomposition`. When `knowledgeDecomposition.enabled=false`, clients MUST NOT present knowledge-type scope as an active selection mode.

- **Source:** `docs/PLAN.md` Section 2
- **Source:** `docs/SPEC.md` Section 15.2-15.3

### REQ-10: Deliverables API Consumption

The deliverables data MUST be sourced from the `/api/project/deliverables` endpoint, which returns `deliverables[]`, `knowledgeDecomposition`, and `knowledgeTypes[]` per the contract in `docs/SPEC.md` Section 15.

- **Source:** `docs/SPEC.md` Section 15.1

### REQ-11: UI Vocabulary Conformance

UI element labels, state values, and internal identifiers for navigation constructs (MatrixRow, MatrixColumn, PipelineCategory, TaskScopeMode) MUST use the canonical vocabulary defined in `docs/TYPES.md` Section 9.

- **Source:** `docs/TYPES.md` Section 9
- **Note:** Added to close the gap between Standards table reference and verification coverage. See item C-001 in `_SEMANTIC_LENSING.md`.

### REQ-12: Concurrent Navigation Handling

TBD — the UI MUST define behavior for concurrent or rapid-succession navigation events (e.g., operator clicks multiple deliverable rows before the first PIPELINE render completes). Specify whether the latest click wins, earlier navigations are cancelled, or clicks are debounced.

- **Source:** `docs/SPEC.md` Section 14 — **location TBD** for race condition handling
- **Note:** This is an operational completeness gap. No governance doc specifies this behavior. **ASSUMPTION: Some form of race condition mitigation is needed to prevent shared state corruption.**

---

## Standards

| Standard/Reference | Applicability | Accessible |
|--------------------|---------------|------------|
| `docs/SPEC.md` Section 14 | UI Navigation and Selector Contract (normative) | Yes |
| `docs/SPEC.md` Section 15 | Deliverables API response contract (normative) | Yes |
| `docs/TYPES.md` Section 9 | UI Navigation Vocabulary (canonical terms) — see REQ-11 | Yes |
| `docs/CONTRACT.md` K-INVENT-1 | Unknown values become TBD, not guessed | Yes |
| `docs/CONTRACT.md` K-STATUS-1 | `_STATUS.md` is canonical lifecycle state | Yes |
| `docs/DIRECTIVE.md` Section 2.1 | Filesystem-as-state constraint | Yes |

---

## Verification

| Req | Verification Approach | Pass Criteria |
|-----|----------------------|---------------|
| REQ-01 | Functional test: click deliverable in PORTAL OPERATIVE row | PIPELINE opens with TASK* category and correct deliverable key selected |
| REQ-01 (performance) | TBD — performance test: measure navigation transition latency | TBD — target latency to be defined; no visual flicker between PORTAL and PIPELINE |
| REQ-02 | Inspect TASK* selector options | No static/fallback variants present; only dynamic deliverable-scoped options |
| REQ-03 (loading/empty) | Functional test: observe selector during data fetch and with empty working root | Loading spinner/skeleton shown during fetch; empty state message shown when no deliverables |
| REQ-03 (error) | Functional test: simulate API error response from `/api/project/deliverables` | Error state is visually distinct from loading and empty states; TBD — specific UI treatment |
| REQ-04 | Inspect state values in React devtools or test assertions | Key format is `pkg::id` (e.g., `PKG-02_Desktop_UI_Workflow::DEL-02-02`) |
| REQ-05 | Functional test: navigate between PORTAL and PIPELINE | Both views reflect the same deliverables data; no stale or duplicated state |
| REQ-06 (triggers 1-3) | Functional test: change project root; simulate fetch failure; remove deliverable from scan results | Selection key is cleared in each scenario |
| REQ-06 (trigger 4) | Functional test: remove knowledge decomposition marker while knowledge-type scope is selected | Selection key is cleared when marker is absent |
| REQ-06 (trigger 5) | Functional test: make a selected knowledge type resolve to zero target deliverables | Selection key is cleared when knowledge type is unresolvable |
| REQ-07 | Visual inspection of disabled entries | Disabled entries are visible, non-selectable, and labeled appropriately |
| REQ-08 | Inspect TASK* selector UI | Split controls present: Task Agent, Scope Mode, Scope, Target Deliverable (conditional) |
| REQ-09 | Functional test: with and without knowledge decomposition marker | Knowledge-type scope hidden when marker absent; visible when marker present |
| REQ-10 | Integration test: verify deliverables endpoint is called and response is consumed correctly | Deliverables list, knowledge decomposition flag, and knowledge types are all used |
| REQ-11 | Vocabulary conformance review: compare UI labels and state identifiers against `docs/TYPES.md` Section 9 | All navigation vocabulary matches canonical definitions |
| REQ-12 | TBD — concurrent navigation test | TBD — behavior defined and consistent under rapid-succession clicks |
| Cross-DEL | Integration test: verify DEL-02-01 FileTree refresh triggers correctly propagate to DEL-02-02 shared deliverables state | Shared state updates correctly when DEL-02-01 triggers a deliverable re-scan (see Guidance C4) |

---

## Documentation

### Required Artifacts (from Anticipated Artifacts)

| Artifact | Type | Description |
|----------|------|-------------|
| Navigation implementation code | CODE | Portal-to-Pipeline routing logic, deliverable key selection, stale key clearing |
| Shared state implementation code | CODE | Page-level deliverables state shared between PORTAL and PIPELINE |
| TASK* selector implementation code | CODE | Split selector model with loading/empty/error states |
| Navigation and state tests | TEST | Functional tests verifying REQ-01 through REQ-12 |
