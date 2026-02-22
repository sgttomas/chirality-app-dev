# Guidance — DEL-05-03 Lifecycle State Handling

## Purpose

This deliverable exists to ensure that `_STATUS.md` is the single, canonical, human-readable lifecycle state file for every deliverable in the Chirality execution model. It operationalizes the invariant K-STATUS-1 ("No other file determines deliverable state") and the transition rules defined in docs/SPEC.md Section 3.

Without reliable lifecycle state handling, the entire filesystem-as-state model breaks down: agents cannot determine what work has been done, humans cannot audit deliverable progress, and staleness/change propagation has no foundation to build on.

**Objective alignment:** OBJ-004 — "Filesystem-as-state execution model is SPEC-conformant and auditable." Lifecycle state handling is one of the core mechanisms that makes the execution model auditable.

(Source: Decomposition DEL-05-03 entry; docs/CONTRACT.md K-STATUS-1; docs/DIRECTIVE.md Section 2.1)

## Principles

### P1: Single Source of Truth for State

`_STATUS.md` is the one and only indicator of where a deliverable stands in its lifecycle. This principle is a direct consequence of the "filesystem is the database" philosophy (docs/DIRECTIVE.md Section 2.1). If state were tracked in multiple locations, synchronization burden and divergence risk would undermine the entire model.

**Implication for implementation:** Any code that reads deliverable state MUST read `_STATUS.md`. There should be no in-memory state cache that diverges from the file, no database column for status, and no derived status calculation that overrides what the file says.

(Source: docs/CONTRACT.md K-STATUS-1; docs/DIRECTIVE.md Section 2.1)

### P2: Forward-Only Progression with Human Gates

The lifecycle is a forward-only sequence. Agents advance state along defined transitions; humans hold the gate for review-and-issuance transitions. This reflects the authority model: agents propose and do mechanical work; humans approve for reliance.

**Implication for implementation:** The transition validation logic should enforce directionality. If a backward transition is requested, it should be rejected with a clear error rather than silently ignored.

(Source: docs/SPEC.md Section 3.3; docs/CONTRACT.md K-AUTH-1; docs/DIRECTIVE.md Section 2.3)

### P2a: Rationale for Backward-Transition Prohibition

The prohibition on backward transitions (REQ-06) is not merely an accidental omission from the transition table -- it is a deliberate design choice rooted in the system's authority model. Backward transitions would allow agents to undo human-reviewed work, undermining the auditability guarantee that the lifecycle provides. The forward-only constraint ensures that:

1. **Audit trail integrity** -- once a deliverable has progressed through a human gate (e.g., CHECKING -> ISSUED), that progression cannot be reversed by an automated process.
2. **Human authority preservation** -- per docs/DIRECTIVE.md Section 2.3, humans hold final authority over approval decisions. Allowing agents to regress state would effectively allow them to "un-approve" work.
3. **Staleness model compatibility** -- the future staleness propagation model (K-STALE-1, K-VAL-1) depends on lifecycle states being monotonically forward; regression would invalidate staleness assumptions.

If a deliverable needs to be reworked after issuance, the appropriate mechanism is a new change cycle (re-opening as a new version or revision), not state regression.

(Source: docs/SPEC.md Section 3.3; docs/DIRECTIVE.md Section 2.3; docs/CONTRACT.md K-AUTH-1, K-STALE-1; **ASSUMPTION:** The re-opening mechanism for post-issuance rework is not yet defined and may require future governance guidance.)

### P3: Auditability Through History

Every state transition appends to the History section. Combined with git versioning, this creates a double audit trail: the `_STATUS.md` history is human-readable in the file itself, and git commits provide the tamper-evident event store.

**Implication for implementation:** History entries should never be edited or deleted programmatically. The append operation should be atomic with the state update (both happen in the same file write).

(Source: docs/SPEC.md Section 3.1; docs/DIRECTIVE.md Section 2.2)

### P4: Semantic Step Is Optional, Not Skippable-by-Default

The INITIALIZED -> SEMANTIC_READY transition is optional in the specification. However, the semantic lensing step (CHIRALITY_FRAMEWORK writing `_SEMANTIC.md`) provides significant value for complex deliverables. The optionality exists to avoid blocking progress when semantic analysis is not yet available or not applicable, not to encourage skipping it routinely.

(Source: docs/SPEC.md Section 3.3; docs/TYPES.md Section 5.3)

## Considerations

### C1: Interaction with Agent Write Scopes

Each agent has a declared write scope (K-WRITE-1). Lifecycle transitions are performed by specific authorized actors (e.g., 4_DOCUMENTS for OPEN -> INITIALIZED). The implementation must ensure that the transition authorization model aligns with agent write scopes. An agent whose write scope is `deliverable-local` can update `_STATUS.md` within its deliverable, but only for its authorized transitions.

(Source: docs/CONTRACT.md K-WRITE-1; docs/SPEC.md Section 3.3)

### C2: Relationship to Staleness Propagation

K-STALE-1 requires that upstream changes propagate staleness to dependent deliverables. The lifecycle state itself does not encode "stale" — staleness is a separate dimension that depends on dependency edges and git SHAs (docs/CONTRACT.md K-VAL-1). However, the lifecycle handling code should not impede future staleness tooling. The `_STATUS.md` format and transition model should remain extensible enough to support annotations or parallel tracking.

**ASSUMPTION:** Staleness will be tracked as metadata alongside (not within) the lifecycle state sequence. The current six-state model does not need a "STALE" state.

(Source: docs/CONTRACT.md K-STALE-1, K-VAL-1; docs/PLAN.md Section 3.7)

### C3: Concurrent Access

The current system prevents concurrent agent execution on the same deliverable by convention. DEL-08-05 (TBD scope) may formalize a lock mechanism. Until then, lifecycle state handling should assume single-writer semantics. If concurrent writes occur, the last write wins (filesystem semantics), which could produce an inconsistent state.

**ASSUMPTION:** Single-writer assumption is acceptable for the current scope. Lock mechanism is deferred to DEL-08-05 if that scope item is brought IN.

**TBD (F-003):** What is the expected behavior if the concurrent-access assumption is violated before DEL-08-05 provides a lock mechanism? Should the implementation detect concurrent writes and fail, or is "last write wins" acceptable? This requires a human decision on acceptable risk. Consult DEL-08-05 scope when available.

(Source: docs/PLAN.md Section 3.5; Decomposition DEL-08-05)

### C4: Format Parsing Robustness

`_STATUS.md` is a Markdown file parsed by agents and potentially by validation tooling. The implementation should handle:
- Minor formatting variations (extra whitespace, missing blank lines)
- Unknown fields (forward compatibility)
- Missing History section (graceful degradation for legacy files)
- **Both list-format and table-format History sections** (pending CON-01 resolution)

**ASSUMPTION:** A lenient parser with strict writer is the appropriate strategy — read permissively, write to spec.

### C5: Relationship to Execution Root Scaffolding

DEL-05-02 (Execution Root Scaffolding + Layout Conformance) is responsible for ensuring the folder structure exists and matches SPEC. This deliverable (DEL-05-03) focuses on the state handling logic within those folders. The two deliverables are complementary: DEL-05-02 ensures the container exists; DEL-05-03 ensures the lifecycle contract within the container is honored.

(Source: Decomposition DEL-05-02 and DEL-05-03 entries)

### C6: Rationale for Markdown State Persistence

The choice of plain Markdown for `_STATUS.md` (rather than a structured format like JSON or YAML) is a deliberate consequence of the filesystem-as-state philosophy (docs/DIRECTIVE.md Section 2.1, **location TBD** for the specific text establishing this preference). Key reasons:

1. **Human readability** -- any operator can inspect deliverable state with a text editor or `cat` command, with no tooling required.
2. **Git diffability** -- state transitions produce clean, line-oriented diffs that are meaningful in code review and audit contexts.
3. **Tooling independence** -- the state file does not require a JSON/YAML parser to read; the format is simple enough for pattern-matching approaches.
4. **Consistency with the doc-kit model** -- all other deliverable-local files (Datasheet, Specification, Guidance, Procedure, `_CONTEXT.md`, etc.) are Markdown. Using the same format for state avoids introducing a format dependency.

The trade-off is that Markdown is less machine-parseable than JSON/YAML, which is why Consideration C4 emphasizes parser robustness.

(Source: docs/DIRECTIVE.md Section 2.1, **location TBD**; docs/SPEC.md Section 3.1)

## Terminology Note

**Canonical vocabulary for transition actors** (F-002 normalization):

- **Actor** — umbrella term for any entity that performs a lifecycle transition. Actors are either Humans or Agents.
- **Human** — a person operating the system. Humans are the only actors authorized for CHECKING and ISSUED transitions (K-AUTH-1).
- **Agent** — a named system component that performs automated work within declared write scopes. Examples: PREPARATION, 4_DOCUMENTS, CHIRALITY_FRAMEWORK, WORKING_ITEMS.
- **Actor identifier** — the string recorded in the History entry identifying who performed a transition (e.g., "PREPARATION", "Human", "4_DOCUMENTS").

This vocabulary should be used consistently across all four documents. Where previous drafts used "agent" and "actor" interchangeably, prefer "Actor" as the umbrella term and "Agent" only for named automated components.

(Source: cross-document analysis of Specification REQ-03, Procedure Step 4.2, Guidance C1)

## Trade-offs

### T1: Strict vs. Permissive Transition Enforcement

- **Strict enforcement** (reject any transition not in the table): Prevents invalid states but may block edge cases where a human needs to reset a deliverable.
- **Permissive enforcement** (warn but allow non-standard transitions by humans): More flexible but risks undermining the lifecycle contract.
- **Proposed approach:** Strict enforcement for agent-initiated transitions; human-initiated transitions may include an escape hatch (e.g., manual file edit) documented as an exceptional operation. **ASSUMPTION (best-effort mapping).**

### T2: In-Memory State Caching for UI

The desktop UI may want to display deliverable states without re-reading files on every render. A cache is acceptable for display purposes as long as:
- The cache is treated as non-authoritative convenience state (docs/DIRECTIVE.md Section 2.5 clarification)
- The file is re-read before any state-changing operation
- Cache staleness is bounded (e.g., refresh on focus/visibility, similar to FileTree behavior per SOW-022)

### T3: History Format — Table vs. List

SPEC Section 3.1 shows history as a list format (`- {date} -- State set to {STATE} ({ACTOR})`). An alternative would be a Markdown table for machine parseability. The list format is simpler to append and matches the SPEC. **Recommendation:** Follow SPEC list format.

(Source: docs/SPEC.md Section 3.1)

## Examples

### Example 1: Valid `_STATUS.md` File

From docs/SPEC.md Section 3.1:

```markdown
# Status: DEL-05-03 Lifecycle State Handling

**Current State:** INITIALIZED
**Last Updated:** 2026-02-21

## History
- 2026-02-21 — State set to OPEN (PREPARATION)
- 2026-02-21 — State set to INITIALIZED (4_DOCUMENTS)
```

### Example 2: Valid Transition Sequence (with Semantic Step)

```
OPEN -> INITIALIZED -> SEMANTIC_READY -> IN_PROGRESS -> CHECKING -> ISSUED
```

### Example 3: Valid Transition Sequence (Semantic Step Skipped)

```
OPEN -> INITIALIZED -> IN_PROGRESS -> CHECKING -> ISSUED
```

### Example 4: Invalid Transition (Rejected)

An agent attempting `IN_PROGRESS -> OPEN` would be rejected — backward transitions are not in the authorized table. The system returns a clear error identifying the rejection reason (see Specification REQ-06, REQ-12).

## Conflict Table (for human ruling)

| Conflict ID | Conflict | Source A | Source B | Impacted Sections | Proposed Authority | Human Ruling |
|-------------|---------|----------|----------|-------------------|-------------------|-------------|
| CON-01 | `_STATUS.md` History section format: SPEC Section 3.1 specifies a **list format** (`- {date} — State set to {STATE} ({ACTOR})`), but the PREPARATION-scaffolded `_STATUS.md` in this deliverable uses a **table format** (Markdown table with Date/From/To/Agent/Notes columns). The two formats are structurally incompatible for a parser. The Specification (REQ-05) must either accept both formats or prescribe one definitively. | docs/SPEC.md Section 3.1 (list format) | Actual `_STATUS.md` as created by PREPARATION (table format) | Specification REQ-05, Procedure Step 2, Guidance C4, Datasheet History format attribute | **PROPOSAL:** Treat docs/SPEC.md Section 3.1 as authoritative. Either (a) update PREPARATION to emit list format, or (b) update SPEC to accept both formats. The parser (C4) should handle both until resolved. | TBD |
