# Procedure — DEL-02-03

## Purpose

This procedure describes the steps to produce and verify the Operator Toolkit Panel & Local Presets deliverable (DEL-02-03). It covers implementation, integration, and verification of the toolkit panel as a non-authoritative convenience surface within the Chirality desktop frontend.

## Prerequisites

| Prerequisite | Type | Status | Notes |
|-------------|------|--------|-------|
| Desktop frontend (`frontend/`) builds and runs | Environment | TBD | PLAN Section 2 confirms Electron + Next.js desktop app exists |
| Harness Turn API (`POST /api/harness/turn`) is functional or mockable | Dependency | TBD | SPEC Section 9.8; covered by DEL-03-02. **TBD (F-002):** Determine whether mock/stub APIs suffice for development and unit testing, or whether functional APIs from DEL-03-01/DEL-03-02 are required before toolkit panel work can begin |
| Session Boot API (`POST /api/harness/session/boot`) is functional or mockable | Dependency | TBD | SPEC Section 9.8; covered by DEL-03-01. See F-002 note above |
| `docs/SPEC.md` Section 9.8 (harness turn input contract) is accessible | Reference | Available | Defines opts mapping, fallback chains, UI contract rules |
| `docs/DIRECTIVE.md` Section 2.5 (convenience state policy) is accessible | Reference | Available | Defines non-authoritative state boundaries |
| Multi-pane layout sidebar integration point is available (or mockable) | Dependency | TBD | **ASSUMPTION:** covered by DEL-02-04. **Enrichment (B-003):** "Available" means: a component interface or sidebar slot API exists that accepts the toolkit panel component, supports show/hide toggling, and participates in the layout resize system. If DEL-02-04 is incomplete, a mock sidebar container (a simple collapsible panel wrapper) suffices for development. See Guidance D-001 enrichment for coordination protocol |

> **Enrichment (F-002):** The dependency on DEL-03-01 and DEL-03-02 APIs is listed as a prerequisite, but it is unclear whether these must be functionally complete or whether mock/stub APIs are acceptable for development and unit testing. This is a **TBD (human/architecture decision)**. Recommendation: develop against mocked API responses for Phases 1-2, then use functional APIs for Phase 3 integration testing.

## Steps

### Phase 1: Toolkit Panel Component

**Step 1.1 — Implement Toolkit Panel Component**

- Create or update the toolkit panel sidebar component in the desktop frontend.
- The panel MUST render as a sidebar within the existing multi-pane layout.
- The panel MUST support show/hide via CONFIG toggle ("Show Tool Kit sidebar").
- Before implementing, confirm the layout integration point with DEL-02-04 (see Guidance D-001 enrichment for coordination protocol).
- **Source:** PLAN Section 2; REQ-01, REQ-02 in Specification.

**Step 1.2 — Implement CONFIG Visibility Toggle**

- Wire the "Show Tool Kit sidebar" CONFIG setting to control panel visibility.
- Persist the visibility state in local storage.
- **Source:** PLAN Section 2; REQ-02, REQ-03 in Specification.

**Step 1.3 — Implement Opts Controls**

- Implement UI controls for the selected subset of harness `opts` fields.
- Specific fields to expose: TBD (design decision; see Guidance T1).
- Controls MUST populate the `opts` object sent to harness APIs.
- Omitted fields MUST NOT be sent (allowing runtime fallback chains to apply).
- **Source:** SPEC Section 9.8; REQ-06, REQ-09 in Specification.

### Phase 2: Local Presets

**Step 2.1 — Implement Preset Storage**

- Implement local-storage-backed preset storage for harness option configurations.
- Presets are non-authoritative convenience state.
- Storage MUST handle missing/corrupted data gracefully (fall back to defaults).
- Preset format: TBD.
- **Source:** SOW-025; DIRECTIVE Section 2.5; REQ-08 in Specification.

**Step 2.2 — Implement Preset Management UI**

- Implement create, select, and apply operations for presets.
- Update and delete operations: TBD.
- When a preset is applied, populate the toolkit panel controls with the preset values.
- **Source:** SOW-025; REQ-08 in Specification.

### Phase 3: Integration and Wiring

**Step 3.1 — Wire Opts to Harness APIs**

- Ensure that opts values from the toolkit panel are included in `POST /api/harness/turn` requests.
- Ensure that opts values are included in `POST /api/harness/session/boot` where applicable.
- **Source:** SPEC Section 9.8; REQ-09 in Specification.

**Step 3.2 — Confirm Governance Non-bypass**

- Review the integration to confirm that toolkit panel state does not write to any project files.
- Confirm that runtime governance gates operate independently of toolkit panel state.
- Confirm that UI visibility of governance fields does not grant runtime authorization.
- **Source:** DIRECTIVE Section 2.5; SPEC Section 9.8; REQ-04, REQ-05, REQ-07 in Specification.

**Step 3.3 — Implement Toolkit State Observability**

- Implement an observability mechanism for toolkit state changes (operator modifying opts before a turn).
- The mechanism (console logging, structured event logging, or other approach) is TBD.
- At minimum, the mechanism should record: which opts were changed, the new values, and the timestamp, so that governance interaction debugging is possible.
- **Source:** REQ-11 in Specification (enrichment A-003).

### Phase 4: State Persistence

**Step 4.1 — Implement Local Storage Persistence**

- Persist toolkit panel state (visibility, current values, presets) to local storage.
- On app launch, restore state from local storage.
- Handle missing/corrupted storage gracefully.
- **Source:** PLAN Section 2; REQ-03 in Specification.

### Phase 5: Error-State and Resilience Handling

> **Enrichment (C-003):** This phase was added because Guidance P4 describes resilience behaviors but the original Procedure had no corresponding implementation steps for error/degradation paths.

**Step 5.1 — Implement Error-State Handling**

- Handle the case where local storage is unavailable (e.g., storage quota exceeded, storage API blocked): fall back to in-memory defaults for the session.
- Handle the case where stored data is corrupted or has an incompatible schema: reset to defaults with an operator-visible notification (TBD notification pattern).
- Handle the case where a preset references opts fields that are no longer valid (e.g., after a schema change): mark the preset as stale or offer migration (TBD migration strategy).
- **Source:** Guidance P4 (Persistence Must Be Resilient); **ASSUMPTION** for specific error handling patterns.

### Phase 6: Accessibility

> **Enrichment (E-002):** This phase was added because the original Procedure covered functional implementation but had no step addressing accessibility, which is part of complete UX_UI_SLICE realization.

**Step 6.1 — Implement Accessibility for Toolkit Panel**

- Ensure all opts controls support keyboard navigation (tab order, arrow keys for selectors, enter/space for toggles).
- Ensure screen reader support for opts controls (ARIA labels, role attributes, state announcements).
- Ensure sufficient color contrast for all toolkit panel elements in both light and dark themes.
- **Source:** **ASSUMPTION** — no specific accessibility requirement in governance docs, but accessibility is standard practice for UX_UI_SLICE deliverables. Consider adding a formal requirement (see Specification REQ-10 note).

## Verification

| Check | Method | Acceptance Criteria | Covers |
|-------|--------|-------------------|--------|
| Panel renders | Component test | Panel renders as sidebar when visibility is enabled | REQ-01 |
| Visibility toggle | Manual + automated test | CONFIG toggle shows/hides panel | REQ-02 |
| Persistence | Close/reopen test | State restored from local storage on relaunch | REQ-03 |
| No project-file writes | Static analysis or code review | Confirm zero writes to `_STATUS.md`, `_CONTEXT.md`, or any execution-root file | REQ-04 |
| Governance enforcement | Integration test | Runtime governance gates function identically with/without toolkit opts | REQ-05, REQ-07 |
| Opts in API payload | Integration test (payload inspection) | Opts from toolkit panel appear in API request body with expected shape | REQ-06, REQ-09 |
| Fallback chains | Integration test | Omitted opts correctly fall back per SPEC Section 9.8 | REQ-06 |
| Preset management | Manual + automated test | Create, select, apply presets; confirm opts populated | REQ-08 |
| Preset persistence across restarts | Close/reopen test | Previously saved presets available and loadable after restart | REQ-08 |
| K-GHOST-1 / K-INVENT-1 compliance | Code review + test | All opts sent originate from explicit operator action or preset; no auto-populated opts without operator intent | Standards |
| End-to-end opts flow | Integration test | Full path: operator sets opts -> opts in API request -> runtime applies fallback for omitted -> governance gates hold | REQ-06, REQ-09, REQ-05 |
| Error-state handling | Manual + automated test | Storage unavailability, corruption, and schema changes handled gracefully per Phase 5 | REQ-03, P4 |
| Accessibility | Manual + automated test | Keyboard navigation, screen reader support, color contrast for toolkit controls | Phase 6 |

## Records

| Record | Description | Location |
|--------|-------------|----------|
| `_STATUS.md` | Lifecycle state updates as work progresses | `DEL-02-03_Operator_Toolkit_Panel/_STATUS.md` |
| Test results | Verification outputs for all checks above | TBD (test runner output) |
| Code artifacts | Component source, preset logic, CONFIG integration | TBD (frontend source tree) |
| Documentation | Operator-facing guidance for toolkit panel usage | TBD |
