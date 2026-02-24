# Datasheet — DEL-05-03 Lifecycle State Handling

## Identification

| Field | Value |
|-------|-------|
| **Deliverable ID** | DEL-05-03 |
| **Name** | Lifecycle State Handling (`_STATUS.md` canonical) |
| **Package** | PKG-05 — Filesystem Execution Model |
| **Type** | BACKEND_FEATURE_SLICE |
| **Context Envelope** | M |
| **Responsible Party** | TBD |
| **Scope Coverage** | SOW-016 |
| **Supports Objectives** | OBJ-004 |
| **Anticipated Artifacts** | CODE / TEST / DOC |

## Issuance Hygiene (2026-02-24)

- Lifecycle state is `ISSUED`.
- Remaining concurrent-access and error-schema precision items are non-blocking follow-up decisions.
- Legacy implementation-phase `TBD`/assumption wording is non-blocking unless explicitly reclassified by human ruling.

## Attributes

| Attribute | Value | Source |
|-----------|-------|--------|
| Canonical lifecycle file | `_STATUS.md` | docs/SPEC.md Section 3; docs/CONTRACT.md K-STATUS-1 |
| Lifecycle state count | 6 | docs/SPEC.md Section 3.2 |
| State sequence | `OPEN -> INITIALIZED -> SEMANTIC_READY -> IN_PROGRESS -> CHECKING -> ISSUED` | docs/SPEC.md Section 3.2 |
| Semantic step optionality | `INITIALIZED -> IN_PROGRESS` is valid (semantic step skippable) | docs/SPEC.md Section 3.3; docs/TYPES.md Section 5.3 |
| Stage gates vs lifecycle | Stage gates (30/60/90/IFC) are NOT lifecycle states; tracked separately in coordination records | docs/SPEC.md Section 3.3; docs/TYPES.md Section 5.2 |
| Status file format | Markdown with Current State, Last Updated, and History section | docs/SPEC.md Section 3.1 |
| History format | **Conflict pending human ruling (see Guidance CON-01):** SPEC Section 3.1 prescribes list format; PREPARATION-scaffolded files use table format. Parser should handle both until resolved. | docs/SPEC.md Section 3.1; Guidance.md CON-01 |
| Authority model | Each transition has an authorized actor; only humans approve CHECKING -> ISSUED | docs/SPEC.md Section 3.3; docs/CONTRACT.md K-AUTH-1 |
| Actor terminology | "Actor" is the umbrella term encompassing both Humans and Agents. Agents include PREPARATION, 4_DOCUMENTS, CHIRALITY_FRAMEWORK, WORKING_ITEMS, etc. See Guidance terminology note. | Specification.md REQ-03; Guidance.md Terminology Note |

## Conditions

| Condition | Description | Source |
|-----------|-------------|--------|
| No alternate state source | No other file determines deliverable state; `_STATUS.md` is authoritative | docs/CONTRACT.md K-STATUS-1 |
| State regression prohibited | Agents must not regress state (e.g., INITIALIZED back to OPEN). This is a design-level prohibition, not merely an omission from the transition table (see Guidance P2a). | docs/SPEC.md Section 3.3 (transition table defines forward-only transitions); Guidance.md P2a |
| Human-only issuance | Only humans may transition to CHECKING and ISSUED | docs/SPEC.md Section 3.3; docs/CONTRACT.md K-AUTH-1 |
| Approval SHA binding | Approvals bind to a specific git SHA; content change after approval voids it | docs/CONTRACT.md K-AUTH-2 |
| Staleness propagation | Upstream changes propagate staleness to dependent deliverables | docs/CONTRACT.md K-STALE-1 |
| Transition rejection behavior | Invalid transitions (unauthorized actor, backward, or non-existent) MUST produce a clear error; silent failure is prohibited. Error behavior specification is TBD (see Specification REQ-12). | Guidance.md P2; Specification.md REQ-12 |

## Construction

| Aspect | Description |
|--------|-------------|
| Platform | macOS 15+, Apple Silicon (Electron + Next.js desktop app) |
| Runtime stack | **ASSUMPTION:** TypeScript/JavaScript within the existing Electron + Next.js codebase |
| State storage | Plain Markdown file (`_STATUS.md`) in each deliverable folder. The choice of Markdown for state (vs. JSON/YAML) follows the filesystem-as-state philosophy: human-readable, git-diffable, and requiring no special tooling to inspect. See Guidance C6. |
| Persistence mechanism | Filesystem write; git-tracked for auditability (see Guidance C6 for rationale) |
| No external DB | All state as plain files per DIRECTIVE Section 2.1; no database dependency |

## References

| Ref | Document | Relevance |
|-----|----------|-----------|
| R1 | docs/SPEC.md Section 3 | Canonical `_STATUS.md` format, valid states, transition rules |
| R2 | docs/CONTRACT.md (K-STATUS-1, K-AUTH-1, K-AUTH-2, K-STALE-1, K-VAL-1) | Binding invariants for lifecycle state |
| R3 | docs/TYPES.md Section 5 | State definitions, stage gates vs lifecycle, semantic step |
| R4 | docs/DIRECTIVE.md Section 2 | Design philosophy (filesystem-as-state, human authority) |
| R5 | Decomposition (DEL-05-03 entry) | Deliverable description and scope mapping |
| R6 | docs/PLAN.md Section 3.7 | Future staleness tooling dependency on lifecycle state |
