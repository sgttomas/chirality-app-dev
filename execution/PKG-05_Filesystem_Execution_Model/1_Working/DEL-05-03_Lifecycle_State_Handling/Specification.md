# Specification — DEL-05-03 Lifecycle State Handling

## Scope

### What This Deliverable Covers

This deliverable ensures that `_STATUS.md` is the canonical lifecycle state file for every deliverable folder and that state transitions align with the rules defined in `docs/SPEC.md` Section 3 and enforced by `docs/CONTRACT.md` K-STATUS-1.

**Scope item:** SOW-016 — "Ensure deliverable lifecycle is represented by `_STATUS.md` using canonical states and transition rules." (Source: Decomposition, Scope Ledger)

### What This Deliverable Excludes

- Stage gate tracking (30/60/90/IFC) — tracked separately in coordination records, not in `_STATUS.md` (Source: docs/SPEC.md Section 3.3; docs/TYPES.md Section 5.2)
- Staleness propagation tooling — covered by DEL-08-07 (TBD scope) (Source: Decomposition, PKG-08)
- Deliverable-level lock mechanisms — covered by DEL-08-05 (TBD scope) (Source: Decomposition, PKG-08)
- Execution root scaffolding — covered by DEL-05-02 (Source: Decomposition, PKG-05)
- Dependency tracking mechanics — covered by DEL-05-04 (Source: Decomposition, PKG-05)

## Requirements

### REQ-01: Canonical State File

`_STATUS.md` MUST be the sole authoritative lifecycle state file for each deliverable. No other file determines deliverable state.

- **Source:** docs/CONTRACT.md K-STATUS-1; docs/SPEC.md Section 3
- **Verification:** REQ-01-V (see Verification section)

### REQ-02: Valid Lifecycle States

The system MUST recognize exactly these six lifecycle states in this order:

```
OPEN -> INITIALIZED -> SEMANTIC_READY -> IN_PROGRESS -> CHECKING -> ISSUED
```

| State | Meaning |
|-------|---------|
| `OPEN` | Folder exists with minimum viable fileset; no content yet |
| `INITIALIZED` | Document kit (Datasheet, Specification, Guidance, Procedure) has been drafted |
| `SEMANTIC_READY` | Semantic lens (`_SEMANTIC.md`) has been generated |
| `IN_PROGRESS` | Active human + agent work underway |
| `CHECKING` | Under review |
| `ISSUED` | Released for use |

- **Source:** docs/SPEC.md Section 3.2; docs/TYPES.md Section 5.1

### REQ-03: Transition Rules and Authorized Actors

State transitions MUST follow the authorized-actor table. The term "Actor" encompasses both Humans and Agents. Agents are named system components (PREPARATION, 4_DOCUMENTS, CHIRALITY_FRAMEWORK, WORKING_ITEMS, etc.). See Guidance Terminology Note for the canonical vocabulary.

| Transition | Authorized Actor |
|------------|------------------|
| `-> OPEN` | PREPARATION |
| `OPEN -> INITIALIZED` | 4_DOCUMENTS |
| `INITIALIZED -> SEMANTIC_READY` | CHIRALITY_FRAMEWORK |
| `INITIALIZED -> IN_PROGRESS` | Human, WORKING_ITEMS (when semantic step is skipped) |
| `SEMANTIC_READY -> IN_PROGRESS` | Human, WORKING_ITEMS |
| `IN_PROGRESS -> CHECKING` | Human |
| `CHECKING -> ISSUED` | Human |

No transitions outside this table are valid. Unauthorized actors MUST NOT perform state transitions.

- **Source:** docs/SPEC.md Section 3.3

### REQ-04: Semantic Step Optionality

The `INITIALIZED -> SEMANTIC_READY` transition is optional. Deliverables MAY transition directly from `INITIALIZED -> IN_PROGRESS` when the semantic lensing step is skipped.

- **Source:** docs/SPEC.md Section 3.3; docs/TYPES.md Section 5.3

### REQ-05: Status File Format

`_STATUS.md` MUST conform to the format defined in docs/SPEC.md Section 3.1:

```markdown
# Status: {DEL-ID} {DeliverableName}

**Current State:** {STATE}
**Last Updated:** {YYYY-MM-DD}

## History
- {YYYY-MM-DD} — State set to {STATE} ({AGENT_OR_ACTOR})
```

**Note (pending CON-01 resolution):** The SPEC-prescribed format uses a **list-based** History section. However, PREPARATION-scaffolded `_STATUS.md` files in this execution instance use a **table-based** History format (with Date/From/To/Agent/Notes columns). The implementation MUST handle the SPEC-prescribed list format as the normative target. Until CON-01 is resolved by human ruling, the parser SHOULD also accept the table format for backward compatibility with existing scaffolded files. See Guidance CON-01 and Guidance C4.

- **Source:** docs/SPEC.md Section 3.1; Guidance.md CON-01

### REQ-06: No State Regression by Agents

Agents MUST NOT transition a deliverable to a state earlier in the lifecycle sequence than its current state. Backward transitions are prohibited by design: the forward-only lifecycle enforces auditability and prevents agents from undoing human-reviewed work (see Guidance P2a for rationale).

- **Source:** docs/SPEC.md Section 3.3 (transition table defines only forward transitions); docs/DIRECTIVE.md Section 2.3 (human authority model)

### REQ-07: Human-Only Approval Transitions

Transitions to `CHECKING` and from `CHECKING -> ISSUED` MUST be performed by a human. No agent may claim to certify, approve, sign, seal, or issue work for reliance.

- **Source:** docs/CONTRACT.md K-AUTH-1; docs/SPEC.md Section 3.3

### REQ-08: Approval-SHA Binding

When a deliverable is issued (CHECKING -> ISSUED), the approval binds to a specific git SHA. Content change after approval voids the approval.

- **Source:** docs/CONTRACT.md K-AUTH-2

### REQ-09: Stage Gates Are Not Lifecycle States

Stage gates (30%, 60%, 90%, IFC, etc.) are human-managed milestones and MUST NOT be conflated with `_STATUS.md` lifecycle states. They are tracked separately in coordination records.

- **Source:** docs/SPEC.md Section 3.3; docs/TYPES.md Section 5.2

### REQ-10: History Append-Only

Each state transition MUST append a history entry to `_STATUS.md` with the date, new state, and actor/agent. History entries MUST NOT be deleted or modified.

- **Source:** docs/SPEC.md Section 3.1 (format includes History section with append entries); **ASSUMPTION:** Append-only behavior is implied by the audit-oriented design philosophy (docs/DIRECTIVE.md Section 2.2 "git is the event store").

### REQ-11: Dirty State Detection Support

A deliverable is "dirty" if any governed input has changed since its last approved SHA. The lifecycle state system MUST support (or not impede) future staleness detection tooling.

- **Source:** docs/CONTRACT.md K-VAL-1; docs/PLAN.md Section 3.7

### REQ-12: Transition Rejection Error Behavior

When a transition is rejected (invalid state, unauthorized actor, backward transition, or non-existent transition), the system MUST return a clear, distinguishable error. Silent failure (no-op without error signal) is prohibited. TBD: specific error codes/messages and structured error format.

- **Source:** Guidance.md P2 ("clear error rather than silently ignored"); Specification.md REQ-03 (unauthorized actors rejected), REQ-06 (backward transitions rejected)
- **ASSUMPTION:** The need for explicit error behavior is implied by the combination of P2 guidance and the requirement to reject invalid transitions. Specific error format is TBD pending implementation.

## Standards

| Standard/Contract | Applicability | Location |
|-------------------|---------------|----------|
| docs/SPEC.md Section 3 | Canonical specification for `_STATUS.md` | Accessible |
| docs/CONTRACT.md K-STATUS-1 | Binding invariant: `_STATUS.md` is canonical | Accessible |
| docs/CONTRACT.md K-AUTH-1 | Binding invariant: only humans author approvals | Accessible |
| docs/CONTRACT.md K-AUTH-2 | Binding invariant: approval binds to git SHA | Accessible |
| docs/CONTRACT.md K-STALE-1, K-VAL-1 | Staleness and dirty-state invariants | Accessible |
| docs/TYPES.md Section 5 | Lifecycle state definitions and vocabulary | Accessible |
| docs/DIRECTIVE.md Section 2 | Design philosophy constraints | Accessible |

## Verification

| Verification ID | Requirement(s) | Approach | Description |
|-----------------|-----------------|----------|-------------|
| REQ-01-V | REQ-01 | TEST | Verify that runtime reads lifecycle state exclusively from `_STATUS.md`; no alternative state source is consulted |
| REQ-02-V | REQ-02 | TEST | Verify that all six states are recognized and that invalid state strings are rejected |
| REQ-03-V | REQ-03 | TEST | Verify that each transition is accepted only when performed by an authorized actor; unauthorized transitions are rejected |
| REQ-04-V | REQ-04 | TEST | Verify that `INITIALIZED -> IN_PROGRESS` is accepted (semantic step skipped) and that `INITIALIZED -> SEMANTIC_READY -> IN_PROGRESS` also works |
| REQ-05-V | REQ-05 | TEST + REVIEW | Verify that `_STATUS.md` files conform to the specified format; validate parsing handles expected fields. Confirm parser handles both list and table History formats (pending CON-01 resolution). |
| REQ-06-V | REQ-06 | TEST | Verify that backward transitions (e.g., IN_PROGRESS -> OPEN) are rejected with a clear error |
| REQ-07-V | REQ-07 | TEST + REVIEW | Verify that agent code paths cannot perform CHECKING or ISSUED transitions |
| REQ-08-V | REQ-08 | TEST + REVIEW | Verify that approval workflow binds to git SHA. Concrete acceptance criterion: confirm that the ISSUED transition records or references the current HEAD SHA, and that a content change (new commit) after ISSUED is detectable as an approval-voiding event. **ASSUMPTION:** Full automated enforcement may depend on future tooling per K-AUTH-2; at minimum, the data model must support SHA binding. |
| REQ-09-V | REQ-09 | REVIEW + TEST | Review that stage gate tracking is separate from lifecycle state implementation. Concrete acceptance criterion: confirm that (a) no stage gate strings (e.g., "30%", "60%", "90%", "IFC") appear in the `_STATUS.md` parser/writer logic, and (b) no lifecycle state logic exists in stage gate code paths. If stage gate code does not yet exist, confirm via review that the lifecycle module's public API does not expose stage-gate concepts. (Source: docs/SPEC.md Section 3.3; docs/TYPES.md Section 5.2) |
| REQ-10-V | REQ-10 | TEST | Verify that state transitions append history entries and that existing history is preserved |
| REQ-11-V | REQ-11 | REVIEW + TEST | Review that lifecycle state implementation does not impede future staleness tooling. Concrete acceptance criterion: verify that (a) the `_STATUS.md` format permits adding metadata fields (e.g., SHA, timestamp) without breaking the parser, and (b) the transition function's interface can accept optional metadata parameters for future staleness annotations. (Source: docs/CONTRACT.md K-VAL-1; docs/PLAN.md Section 3.7) |
| REQ-12-V | REQ-12 | TEST | Verify that rejected transitions produce distinguishable error signals (not silent no-ops). Test coverage: unauthorized actor, backward transition, non-existent transition. TBD: specific error code assertions pending REQ-12 finalization. |

## Documentation

| Artifact Type | Description | Status |
|---------------|-------------|--------|
| CODE | Lifecycle state handling implementation (state transitions, validation, authorized-actor enforcement, error handling) | TBD |
| TEST | Unit and integration tests for state validation, transition rules, authorized actors, format conformance, error paths | TBD |
| DOC | Updates to any implementation-level documentation reflecting lifecycle handling behavior | TBD |
