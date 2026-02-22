# Specification — DEL-02-03

## Scope

### What This Deliverable Covers

Implement and verify the Operator Toolkit Panel, a sidebar UI component in the Chirality desktop frontend that:

1. Provides operator-facing controls for per-turn harness options (`opts`).
2. Supports local presets for saved option configurations.
3. Persists panel state and presets in local storage (non-authoritative convenience state).
4. Provides a CONFIG-driven visibility toggle ("Show Tool Kit sidebar").

(Source: SOW-025; PLAN Section 2; Decomposition DEL-02-03 entry)

### What This Deliverable Excludes

- Runtime harness execution logic (covered by PKG-03 — Harness Runtime Core).
- Turn options mapping and fallback chain implementation (covered by DEL-03-03).
- Subagent governance enforcement logic (covered by DEL-03-04).
- Governance document or contract modifications.
- Any authoritative project-truth state management.

## Requirements

### REQ-01: Toolkit Panel Rendering

The toolkit panel MUST render as a sidebar component in the desktop frontend.

- **Source:** PLAN Section 2 ("Operator Toolkit panel for per-turn harness options + local presets")
- **Verification:** Visual inspection; component render test.

### REQ-02: CONFIG-Driven Visibility Toggle

The toolkit panel visibility MUST be controlled by a CONFIG setting ("Show Tool Kit sidebar").

- **Source:** PLAN Section 2 ("Visibility is controlled from CONFIG")
- **Verification:** Toggle CONFIG setting and confirm panel shows/hides.

### REQ-03: Local Storage Persistence

The toolkit panel state (visibility, current option values, presets) MUST be persisted in local storage.

- **Source:** PLAN Section 2 ("persisted in local storage")
- **Verification:** Close and reopen the app; confirm state is restored.

### REQ-04: Non-authoritative Convenience State

Toolkit panel state and presets MUST NOT be treated as project truth and MUST NOT override contract/governance enforcement.

- **Source:** DIRECTIVE Section 2.5 ("Such convenience state MUST NOT be treated as project truth and MUST NOT override contract/governance enforcement.")
- **Verification:** Confirm via static analysis or code review that no toolkit state is written to project files (`_STATUS.md`, `_CONTEXT.md`, etc.). Confirm that runtime governance gates function identically regardless of toolkit state.

> **Enrichment (C-001):** Verification for REQ-04 negative case strengthened: the verification approach must include a concrete method (static analysis grep for write calls to execution-root paths, or explicit code review checklist item) to confirm zero project-file writes. "Confirm" alone is underspecified for this governance-critical requirement. Source: CONTRACT K-GHOST-1; DIRECTIVE Section 2.5.

### REQ-05: Governance Non-bypass

The toolkit panel MUST NOT provide any mechanism that bypasses governance enforcement.

- **Source:** SOW-025 ("cannot bypass governance"); Decomposition DEL-02-03 ("ensure it is convenience state only and cannot bypass governance")
- **Verification:** Attempt to use toolkit panel settings to circumvent runtime governance gates (e.g., subagent delegation without valid governance metadata). Confirm enforcement holds.

### REQ-06: Harness `opts` Subset Exposure

The toolkit panel MAY expose any subset of supported `opts` fields. Omitted fields MUST follow runtime fallback chains (persona defaults, global defaults, runtime defaults).

- **Source:** SPEC Section 9.8 ("UI MAY expose any subset of supported opts fields. Omitted fields MUST follow runtime fallback chains.")
- **Verification:** Configure opts via toolkit panel; inspect the API request payload to confirm the selected opts appear in the `POST /api/harness/turn` request body with expected shape. Omit an opt; confirm fallback chain applies by verifying runtime uses the next value in the fallback chain.

> **Enrichment (X-002):** Verification language strengthened from "confirm they are passed" to specify the inspection mechanism (API request payload inspection) and what constitutes acceptance (expected shape present in request body). Source: SPEC Section 9.8.

### REQ-07: UI Visibility Is Not Authorization

UI visibility of an `opts` field in the toolkit panel MUST NOT be interpreted as runtime authorization.

- **Source:** SPEC Section 9.8 ("UI visibility of a field MUST NOT be interpreted as runtime authorization.")
- **Verification:** Display a governance field (e.g., `subagentGovernance`) in the toolkit panel; confirm that runtime gate/seal logic still governs actual behavior.

### REQ-08: Local Preset Management

The toolkit panel SHOULD support creating, selecting, and applying local presets for harness option configurations.

- **Source:** SOW-025 ("local presets"); PLAN Section 2
- **Note:** Preset CRUD operations (create, select, update, delete) and preset format are TBD (design decisions for implementation).
- **Verification:** Create a preset, apply it, confirm opts are populated. Verify that presets persist across app restarts (close and reopen the app; confirm previously-saved presets are still available and loadable). TBD: additional preset management tests.

> **Enrichment (C-002):** REQ-08 uses SHOULD. SOW-025 lists "local presets" as an in-scope item, creating ambiguity about whether presets are required for SOW-025 acceptance or are optional. **TBD (human ruling needed):** If preset management is required for SOW-025 acceptance, upgrade to MUST. If optional, document the acceptance boundary explicitly. See Conflict Table in Guidance.md.
>
> **Enrichment (X-003):** Verification for REQ-08 expanded to include preset persistence across app restarts, which is a distinct behavior from general state persistence (REQ-03). REQ-03 covers panel state restoration; REQ-08 verification must also confirm that saved presets survive restarts. Source: PLAN Section 2 ("persisted in local storage").

### REQ-09: Opts Passed to Harness APIs

Option values set via the toolkit panel MUST be included in the `opts` object sent to:
- `POST /api/harness/turn`
- `POST /api/harness/session/boot` (where applicable)

- **Source:** SPEC Section 9.8
- **Verification:** Set opts via toolkit panel; inspect the API request payload; confirm opts are present.

### REQ-10: Performance Responsiveness

**ASSUMPTION:** The toolkit panel SHOULD meet reasonable responsiveness targets for a primary operator interaction surface.

- Panel render time: TBD (target to be determined during implementation)
- Interaction latency (e.g., selecting an opt, applying a preset): TBD
- **Source:** No specific performance requirements stated in governance docs. Added as non-functional requirement per enrichment A-004 (performance assessment lens).
- **Verification:** TBD — define render time and interaction latency acceptance thresholds during implementation.

> **Enrichment (A-004):** Performance acceptance criteria added as REQ-10. Specific targets are TBD as no source defines them, but the requirement placeholder ensures performance is not overlooked for this primary operator interaction surface.

### REQ-11: Toolkit State Change Observability

**ASSUMPTION:** Toolkit state changes (operator modifying opts before a turn) SHOULD be observable for debugging governance interactions.

- The mechanism (e.g., console logging, structured event logging) is TBD.
- **Source:** No explicit audit requirement in governance docs for toolkit state; added per enrichment A-003 (audit trail lens). Rationale: when investigating governance gate behavior, it is useful to know what opts the operator had set.
- **Verification:** Trigger a toolkit state change; confirm the change is recorded in the observability mechanism (TBD).

> **Enrichment (A-003):** Observability of toolkit state changes added as REQ-11. The specific mechanism is TBD but the requirement ensures that debugging governance interactions is possible by tracing what opts were active at turn time.

## Standards

| Standard/Contract | Relevance | Source |
|-------------------|-----------|--------|
| DIRECTIVE Section 2.5 | Non-authoritative convenience state policy | `docs/DIRECTIVE.md` |
| SPEC Section 9.8 | Harness turn input contract; opts mapping; UI contract rules | `docs/SPEC.md` |
| CONTRACT K-GHOST-1 | No ghost inputs — toolkit state is non-authoritative; agent context limited to folder contents + declared references | `docs/CONTRACT.md` |
| CONTRACT K-INVENT-1 | No invented values — TBD for unknowns | `docs/CONTRACT.md` |
| CONTRACT K-AUTH-1 | Only humans author binding approval records | `docs/CONTRACT.md` |

## Verification

| Requirement | Verification Approach | Status |
|-------------|----------------------|--------|
| REQ-01 | Component render test; visual inspection | TBD |
| REQ-02 | Toggle CONFIG; confirm show/hide | TBD |
| REQ-03 | Close/reopen app; confirm persistence | TBD |
| REQ-04 | Static analysis or code review confirming zero project-file writes; confirm governance independence | TBD |
| REQ-05 | Attempt governance bypass via toolkit; confirm blocked | TBD |
| REQ-06 | Inspect API request payload for opts shape; omit field and verify fallback | TBD |
| REQ-07 | Display governance field; confirm runtime still governs | TBD |
| REQ-08 | Create/apply preset; confirm opts populated; verify preset persistence across restarts | TBD |
| REQ-09 | Inspect API payload with toolkit opts | TBD |
| REQ-10 | TBD — define render time and interaction latency thresholds | TBD |
| REQ-11 | Trigger state change; confirm recorded in observability mechanism | TBD |
| K-GHOST-1 / K-INVENT-1 | Verify toolkit does not inject ghost inputs or invent values: confirm all opts sent originate from explicit operator action or preset selection; confirm no opts are auto-populated without operator intent | TBD |
| End-to-end opts flow | Integration test covering full path: operator sets opts in toolkit -> opts appear in API request -> runtime applies fallback for omitted opts -> governance gates hold | TBD |

> **Enrichment (F-001):** Added explicit verification row for CONTRACT K-GHOST-1 and K-INVENT-1 compliance. The Standards table listed these contracts but the Verification table had no corresponding checks. Source: CONTRACT K-GHOST-1, K-INVENT-1.
>
> **Enrichment (D-002):** Added end-to-end integration verification row covering the full opts flow from UI through runtime. Individual checks existed but no integrated end-to-end step was defined. Source: SPEC Section 9.8 (opts contract); Procedure Phase 3.

## Documentation

### Required Artifacts (from `_CONTEXT.md`)

| Artifact Type | Description | Status |
|---------------|-------------|--------|
| CODE | Toolkit panel component(s), preset logic, CONFIG integration | TBD |
| DOC | Operator guidance for toolkit panel usage and preset management | TBD |
| TEST | Unit tests for panel rendering, integration tests for opts flow, governance bypass tests, K-GHOST-1/K-INVENT-1 compliance tests, end-to-end opts flow tests | TBD |
