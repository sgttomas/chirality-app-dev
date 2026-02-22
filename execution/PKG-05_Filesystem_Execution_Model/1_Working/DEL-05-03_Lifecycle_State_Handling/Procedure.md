# Procedure — DEL-05-03 Lifecycle State Handling

## Purpose

This procedure describes how to produce and verify the Lifecycle State Handling deliverable (DEL-05-03). It covers the implementation of `_STATUS.md` as the canonical lifecycle state file, transition validation, authorized-actor enforcement, error handling, and the associated test and documentation artifacts.

## Prerequisites

| # | Prerequisite | Source | Status |
|---|-------------|--------|--------|
| PRE-01 | Execution root scaffolding is complete (DEL-05-02) — folder structure exists and matches SPEC | Decomposition DEL-05-02; docs/SPEC.md Section 1 | TBD |
| PRE-02 | docs/SPEC.md Section 3 is accessible and current | docs/SPEC.md | Available |
| PRE-03 | docs/CONTRACT.md invariants (K-STATUS-1, K-AUTH-1, K-AUTH-2) are accessible and current | docs/CONTRACT.md | Available |
| PRE-04 | docs/TYPES.md Section 5 (lifecycle state definitions) is accessible and current | docs/TYPES.md | Available |
| PRE-05 | Development environment (macOS 15+, Apple Silicon, Electron + Next.js stack) is set up | Decomposition DEC-PLAT-001 | TBD |

## Steps

### Step 1: Identify Existing Lifecycle State Handling Code

1.1. Survey the existing codebase for any code that reads or writes `_STATUS.md` files.
   - **ASSUMPTION:** PREPARATION agent and 4_DOCUMENTS agent already write `_STATUS.md` as part of their protocols. Identify where and how.
1.2. Survey for any code that tracks deliverable state outside of `_STATUS.md` (violation of K-STATUS-1).
1.3. Document findings: what exists, what is missing, what needs correction.
1.4. **If violations are found** (Step 1.2 discovers alternate state sources): document each violation with its location, the state data it tracks, and its consumers. Propose a remediation plan: either remove the alternate source or refactor it to read from `_STATUS.md`. Violations must be resolved before Step 5 verification can pass. (Source: docs/CONTRACT.md K-STATUS-1; Specification REQ-01)

**Verification:** Findings documented before proceeding to implementation. If violations were found, remediation plan is included.

### Step 2: Implement (or Verify) Status File Format Handling

2.1. Implement a `_STATUS.md` parser that reads:
   - `Current State` field
   - `Last Updated` field
   - `History` entries (both list format and table format — see Guidance C4, Specification REQ-05 CON-01 note)

2.2. Implement a `_STATUS.md` writer that:
   - Updates `Current State` to the new state
   - Updates `Last Updated` to the current date (YYYY-MM-DD)
   - Appends a history entry: `- {YYYY-MM-DD} — State set to {STATE} ({AGENT_OR_ACTOR})`
   - Preserves existing history entries (append-only)

2.3. Ensure the writer produces output conforming to docs/SPEC.md Section 3.1 format (list-based History). The parser should accept both list and table formats per Guidance C4, pending CON-01 resolution.

**Verification:** Unit tests confirm parse/write round-trip fidelity and format conformance. Tests include both list-format and table-format History inputs for parser.

### Step 3: Implement State Validation

3.1. Define the set of valid states: `OPEN`, `INITIALIZED`, `SEMANTIC_READY`, `IN_PROGRESS`, `CHECKING`, `ISSUED`.

3.2. Implement validation that rejects any state string not in the valid set.

3.3. Implement ordering: states have a defined sequence position. This is used for transition validation (Step 4) and prevents regression (REQ-06).

**Verification:** Unit tests confirm valid states are accepted and invalid states are rejected.

### Step 4: Implement Transition Rules and Authorized-Actor Enforcement

4.1. Encode the transition table from docs/SPEC.md Section 3.3:

| From | To | Authorized Actors |
|------|----|-------------------|
| (none) | OPEN | PREPARATION |
| OPEN | INITIALIZED | 4_DOCUMENTS |
| INITIALIZED | SEMANTIC_READY | CHIRALITY_FRAMEWORK |
| INITIALIZED | IN_PROGRESS | Human, WORKING_ITEMS |
| SEMANTIC_READY | IN_PROGRESS | Human, WORKING_ITEMS |
| IN_PROGRESS | CHECKING | Human |
| CHECKING | ISSUED | Human |

4.2. Implement a transition function that:
   - Accepts: current state, target state, actor identifier (see Guidance Terminology Note for actor vocabulary)
   - Validates: the transition is in the table AND the actor is authorized
   - Rejects: transitions not in the table, unauthorized actors, backward transitions
   - On success: calls the writer (Step 2) to update `_STATUS.md`
   - On rejection: returns a clear, distinguishable error identifying the rejection reason (see Specification REQ-12). The error MUST NOT be a silent no-op.

4.3. Ensure the semantic step optionality is supported: `INITIALIZED -> IN_PROGRESS` is valid when semantic step is skipped (REQ-04).

**Verification:** Tests cover every valid transition, every invalid transition, every unauthorized-actor attempt, and every rejection scenario (with error signal assertion).

### Step 5: Verify No Alternate State Sources

5.1. Confirm that no code path reads deliverable lifecycle state from any source other than `_STATUS.md`. If violations were identified in Step 1.2 and remediated per Step 1.4, verify that all remediations are complete.

5.2. If UI caching is used for display, confirm it follows the non-authoritative convenience state rules (docs/DIRECTIVE.md Section 2.5):
   - Cache is refreshed on focus/visibility
   - File is re-read before state-changing operations
   - Cache is never treated as authoritative

**Verification:** Code review confirms single source of truth. All Step 1.4 remediations verified complete.

### Step 6: Ensure Stage Gates Are Separate

6.1. Confirm that stage gate tracking (30/60/90/IFC) is not conflated with `_STATUS.md` lifecycle states.

6.2. If any code intermixes stage gates with lifecycle states, refactor to separate them.

**Verification:** Code review and/or tests confirm separation. See Specification REQ-09-V for concrete acceptance criteria.

### Step 7: Write Tests

7.1. **Unit tests** for:
   - `_STATUS.md` parsing (valid format, edge cases, minor variations, both list and table History formats)
   - `_STATUS.md` writing (format conformance, history preservation)
   - State validation (valid/invalid states)
   - Transition validation (all valid transitions, all invalid transitions, unauthorized actors)
   - Backward transition rejection (with error signal verification)
   - **Error path coverage:** verify that each rejection type (unauthorized actor, backward transition, non-existent transition) produces a distinguishable error signal (REQ-12)

7.2. **Integration tests** for:
   - End-to-end lifecycle progression: OPEN through ISSUED
   - Semantic-step-skipped path: OPEN -> INITIALIZED -> IN_PROGRESS -> CHECKING -> ISSUED
   - Agent-initiated transitions are limited to authorized transitions
   - `_STATUS.md` file is correctly updated on disk after transitions
   - **Error path integration tests:** verify system-level enforcement of rejection behavior:
     - Unauthorized agent attempts an end-to-end transition sequence that includes a human-only gate (e.g., agent attempts IN_PROGRESS -> CHECKING)
     - Backward transition attempted within a multi-step sequence (e.g., after reaching IN_PROGRESS, attempt to transition to INITIALIZED)
     - (Source: Guidance P2; Specification REQ-03, REQ-06, REQ-12)

7.3. Ensure tests are repeatable and suitable for local + CI validation (per SOW-028 intent).

**Verification:** All tests pass. Coverage addresses every requirement in Specification.md, including REQ-12 error behavior.

### Step 8: Write Documentation

8.1. Produce the following documentation artifacts:
   - **Module-level API documentation** for the lifecycle state handling module: document the parser, writer, and transition function interfaces (function signatures, parameters, return types, error types).
   - **Developer guide section** explaining how lifecycle state handling works in the codebase: where the module lives, how to call it, and how the authorized-actor model is enforced.
   - **Error handling reference:** document the error types/codes returned by the transition function for each rejection scenario.

8.2. Update or create any necessary developer-facing documentation that connects the implementation to the governance docs (docs/SPEC.md Section 3, docs/CONTRACT.md K-STATUS-1).

8.3. **TBD (concurrent access):** If a decision is made regarding concurrent-access behavior before DEL-08-05 (see Guidance C3, F-003), document the chosen approach and any interim safeguards.

(Source: _CONTEXT.md anticipated artifacts: CODE/TEST/DOC)

**Verification:** Documentation exists, is consistent with implementation, and covers the artifacts listed above.

## Verification

| Step | Verification Method | Pass Criteria |
|------|-------------------|---------------|
| Step 1 | Document review | Existing code surveyed; findings recorded; violations (if any) have remediation plan |
| Step 2 | Unit tests | Parse/write round-trip correct; format matches SPEC Section 3.1; parser handles both History formats |
| Step 3 | Unit tests | Valid states accepted; invalid states rejected |
| Step 4 | Unit tests + integration tests | All valid transitions succeed; all invalid/unauthorized transitions rejected with clear error |
| Step 5 | Code review | No alternate state source found; all remediations verified |
| Step 6 | Code review + tests | Stage gates are separate from lifecycle states (REQ-09-V criteria met) |
| Step 7 | Test execution | All tests pass; error path coverage included |
| Step 8 | Document review | API docs, developer guide, and error handling reference exist and are consistent |

## Records

| Record | Description | Location |
|--------|-------------|----------|
| Survey findings (Step 1) | Existing lifecycle code inventory + violation remediation plan (if applicable) | TBD (deliverable folder or `_MEMORY.md`) |
| Test results | Test execution output (unit + integration, including error paths) | TBD (CI artifacts or local test output) |
| Code changes | Implementation diffs | Git commits on the working branch |
| Updated `_STATUS.md` | This deliverable's own status file | `_STATUS.md` in this folder |
| Documentation artifacts | Module API docs, developer guide section, error handling reference | TBD |
