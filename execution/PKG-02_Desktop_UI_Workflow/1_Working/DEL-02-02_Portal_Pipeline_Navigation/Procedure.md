# Procedure — DEL-02-02 Portal->Pipeline Navigation & Deliverable Key Semantics

## Purpose

This procedure describes the steps to implement, verify, and document the portal-to-pipeline navigation and shared deliverables state semantics for the Chirality desktop UI.

---

## Prerequisites

| # | Prerequisite | Status |
|---|-------------|--------|
| P1 | Access to the frontend codebase (`frontend/` directory) | TBD |
| P2 | Familiarity with `docs/SPEC.md` Section 14 (UI Navigation and Selector Contract) and Section 15 (Deliverables API Response Contract) | TBD |
| P3 | Familiarity with `docs/PLAN.md` Section 2 (existing portal-to-pipeline behavior description) | TBD |
| P4 | Working macOS 15+ Apple Silicon development environment with Electron + Next.js build capability | TBD |
| P5 | Understanding of current PORTAL matrix and PIPELINE selector implementation (review existing code) | TBD |
| P6 | Confirm DEL-02-01 (FileTree Refresh) status: verify that DEL-02-01's refresh mechanism is at least initialized or in progress, since Guidance C4 identifies that FileTree refresh triggers may affect shared deliverables state. If DEL-02-01 is not yet started, note this as a coordination risk. | TBD |
| P7 | Confirm `/api/project/deliverables` endpoint availability: verify the endpoint is implemented and accessible, or identify which deliverable owns its implementation. If the endpoint does not yet exist, this deliverable cannot fully implement REQ-10 and shared state fetch logic. TBD — ownership not confirmed in `_DEPENDENCIES.md`. | TBD |

**Upstream dependencies:** No declared upstream dependencies in `_DEPENDENCIES.md` at this time. **ASSUMPTION: DEL-02-02 may depend on foundational UI framework and build baseline (DEL-01-01) being functional, but this is not formally declared. DEL-02-02 also has a coordination dependency on DEL-02-01 for shared state propagation (see P6) and on the `/api/project/deliverables` endpoint (see P7).**

---

## Steps

### Step 1: Audit Existing Implementation

1.1. Review the current PORTAL matrix component to identify how OPERATIVE row cells are rendered and what click handlers exist.

1.2. Review the current PIPELINE view to identify how `TASK*` category is selected, how scope selectors are populated, and how deliverable keys are stored in state.

1.3. Review `page.tsx` (or equivalent page-level component) to identify where deliverables state is currently held and how it is shared between PORTAL and PIPELINE views.

1.4. Review the `/api/project/deliverables` endpoint implementation to confirm it returns the response shape specified in `docs/SPEC.md` Section 15.1 (including `knowledgeDecomposition` and `knowledgeTypes[]`).

1.5. Document findings: what already works, what is missing, and what needs modification. Record audit results in a structured format (e.g., a checklist or table) within the deliverable's working notes or MEMORY.md file. Each finding should reference the specific REQ it relates to and indicate one of: EXISTING (already implemented), PARTIAL (needs modification), or MISSING (needs implementation).

**Rationale for structured audit (from semantic lensing B-003):** A structured audit format ensures findings are not lost and provides a traceable basis for implementation decisions in subsequent steps. Without a defined format, audit results may be informal and difficult to reference later.

**Rollback note:** Step 1 is read-only and does not modify code. No rollback needed.

### Step 2: Implement/Verify Shared Deliverables State (REQ-05, REQ-10)

2.1. Ensure deliverables data is fetched from `/api/project/deliverables` at page-level scope.

2.2. Ensure the fetched data (deliverables list, knowledge decomposition flag, knowledge types) is available to both PORTAL and PIPELINE views without duplication.

2.3. Implement or verify that data refresh occurs appropriately (e.g., on page mount, on root change).

2.4. Implement error state handling: when the API returns an error response, the UI must display a distinct error state (not loading, not empty). TBD — specific error UI treatment. (See REQ-03 note and Guidance P4.)

**Rollback note:** If Step 2 introduces regressions to existing PORTAL or PIPELINE functionality, revert the shared state changes using `git stash` or `git checkout` on affected files and re-assess the integration approach.

### Step 3: Implement/Verify PORTAL-to-PIPELINE Navigation (REQ-01)

3.1. Implement click handler on deliverable rows in the PORTAL OPERATIVE row that navigates to PIPELINE with `TASK*` category.

3.2. Ensure the clicked deliverable's composite key (`pkg::id` format per REQ-04) is passed to and pre-selected in the PIPELINE TASK* scope selector.

3.3. Verify the navigation transition preserves the deliverable selection deterministically.

3.4. Document the state transfer mechanism chosen (URL params, React context, or other) in the Records section so downstream PKG-02 deliverables can coordinate. (See Guidance C1.)

**Rollback note:** If Step 3 breaks existing PORTAL functionality (e.g., matrix rendering, other row click handlers), revert the navigation changes and isolate the issue before re-attempting.

### Step 4: Implement/Verify TASK* Selector Model (REQ-02, REQ-03, REQ-08)

4.1. Implement or verify the split selector model:
- `Task Agent` selector (static options)
- `Scope Mode` selector (`DELIVERABLES` / `KNOWLEDGE_TYPES`)
- `Scope` selector (dynamic list based on mode)
- `Target Deliverable` selector (required when scope mode is `KNOWLEDGE_TYPES`)

4.2. Ensure TASK* uses only dynamic deliverable-scoped options (no fallback static variants per REQ-02).

4.3. Implement explicit loading states (spinner/skeleton) during data fetch, explicit empty states when no deliverables are available (REQ-03), and explicit error states for API failures.

**Rollback note:** If selector changes break other pipeline categories (`DECOMP*`, `PREP*`, `AUDIT*`), revert and ensure TASK*-specific changes are isolated to the TASK* selector component.

### Step 5: Implement/Verify Disabled Option Behavior (REQ-07)

5.1. Ensure unsupported pipeline variants are rendered as visible but disabled entries.

5.2. Ensure disabled entries display "coming soon" (or equivalent) hint text.

5.3. Ensure disabled entries are non-selectable.

**Rollback note:** If disabled option rendering causes layout issues, revert styling changes and address layout separately.

### Step 6: Implement/Verify Knowledge Decomposition Gating (REQ-09)

6.1. Ensure knowledge-type scope mode is shown only when `knowledgeDecomposition.enabled === true` in the API response.

6.2. Ensure knowledge-type scope mode is hidden or disabled when the marker is absent.

**Rollback note:** If gating logic interferes with DELIVERABLES scope mode, revert and ensure gating is conditional on scope mode selection only.

### Step 7: Implement/Verify Stale Selection Clearing (REQ-06)

7.1. Implement stale key clearing when the project root changes.

7.2. Implement stale key clearing when a deliverable fetch fails.

7.3. Implement stale key clearing when the selected deliverable key is no longer present in scan results.

7.4. Implement stale key clearing when knowledge decomposition marker is absent while knowledge-type scope is selected (per `docs/SPEC.md` Section 14.5).

7.5. Implement stale key clearing when a knowledge type no longer resolves to available target deliverables (per `docs/SPEC.md` Section 14.5).

**Rollback note:** If stale clearing logic over-aggressively clears keys (e.g., during normal navigation), revert the clearing triggers and narrow the conditions. Verify each trigger in isolation before combining.

### Step 8: Implement/Verify UI Vocabulary Conformance (REQ-11)

8.1. Review all UI navigation labels, state identifiers, and component names against `docs/TYPES.md` Section 9 canonical vocabulary.

8.2. Normalize any inconsistencies in capitalization or phrasing to match the canonical vocabulary.

**Rollback note:** Vocabulary normalization is a naming-only change. If renaming causes import or reference breakage, revert and update all references before re-applying.

### Step 9: Write Tests

9.1. Write functional/integration tests covering:
- PORTAL row click navigates to PIPELINE TASK* with correct deliverable key (REQ-01)
- TASK* selector shows only dynamic options, no static fallbacks (REQ-02)
- Loading, empty, and error states render correctly (REQ-03)
- Composite key format is correct (REQ-04)
- Shared state consistency between PORTAL and PIPELINE (REQ-05)
- Stale key clearing for all 5 trigger scenarios (REQ-06) — ensure all triggers are individually tested
- Disabled option rendering (REQ-07)
- Split selector controls are present and functional (REQ-08)
- Knowledge decomposition gating logic (REQ-09)
- API consumption and response handling (REQ-10)
- UI vocabulary conformance (REQ-11)
- Concurrent navigation behavior (REQ-12) — TBD pending behavior definition
- Cross-deliverable: DEL-02-01 refresh triggers propagate to shared state (if DEL-02-01 is available)

9.2. Ensure tests are repeatable and can run in local and CI environments.

**Rollback note:** If tests reveal regressions, use test failures as diagnostic signals; revert the specific implementation step that caused the failure and address before re-running.

---

## Verification

| Check | Method | Pass Criteria |
|-------|--------|---------------|
| Navigation routing | Manual + automated test | PORTAL OPERATIVE row click -> PIPELINE TASK* with correct key |
| Navigation performance | TBD — latency measurement | TBD — target transition time to be defined; no visual flicker |
| Shared state | Automated test | PORTAL and PIPELINE read same deliverables data |
| Error state handling | Automated test | API error response produces distinct error UI, not loading or empty state |
| Selector model | Visual + automated test | Split selectors present; no static fallbacks; loading/empty/error states work |
| Stale clearing (trigger 1) | Automated test | Key cleared on root change |
| Stale clearing (trigger 2) | Automated test | Key cleared on fetch failure |
| Stale clearing (trigger 3) | Automated test | Key cleared on scan miss |
| Stale clearing (trigger 4) | Automated test | Key cleared when knowledge marker absent |
| Stale clearing (trigger 5) | Automated test | Key cleared when knowledge type unresolvable |
| Disabled options | Visual inspection | Disabled entries visible, non-selectable, labeled |
| Key format | Assertion test | All keys match `pkg::id` composite pattern |
| Knowledge gating | Conditional test | Scope mode hidden when `enabled=false`; visible when `enabled=true` |
| API consumption | Integration test | Endpoint called; response shape matches `docs/SPEC.md` Section 15.1 |
| Vocabulary conformance | Review + automated lint | UI terms match `docs/TYPES.md` Section 9 canonical vocabulary |
| Concurrent navigation | TBD — automated test | TBD — defined behavior under rapid-succession clicks |
| Cross-DEL integration | Integration test (when DEL-02-01 available) | DEL-02-01 refresh triggers propagate correctly to shared state |

---

## Records

Upon completion of this deliverable, the following records should exist:

| Record | Location | Description |
|--------|----------|-------------|
| Implementation code | `frontend/` (specific paths TBD — see X-002 in `_SEMANTIC_LENSING.md`; expected locations for navigation routing, shared state, and selector components should be documented once the frontend directory structure is inspected in Step 1) | Navigation routing, shared state, selector components |
| Test files | `frontend/` (specific paths TBD — expected test locations should be documented once the test directory structure is inspected in Step 1) | Functional and integration tests for REQ-01 through REQ-12 |
| State transfer mechanism | This deliverable folder or MEMORY.md | Documentation of which mechanism was chosen for PORTAL-to-PIPELINE state transfer (see Step 3.4, Guidance C1) |
| Audit findings | This deliverable folder or MEMORY.md | Structured audit results from Step 1 (see Step 1.5) |
| `_STATUS.md` update | This deliverable folder | State transition reflecting completion progress |
| Git commit(s) | Repository history | Implementation and test commits with meaningful messages |
