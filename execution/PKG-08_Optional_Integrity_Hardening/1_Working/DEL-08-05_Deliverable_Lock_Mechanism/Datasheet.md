# Datasheet -- DEL-08-05 Deliverable-level Lock Mechanism

## Identification

| Field | Value |
|-------|-------|
| **DeliverableID** | DEL-08-05 |
| **Name** | Deliverable-level Lock Mechanism |
| **PackageID** | PKG-08 |
| **Package** | Optional Integrity Hardening |
| **Type** | SECURITY_CONTROL |
| **ContextEnvelope** | L |
| **Responsible Party** | TBD |
| **Scope Coverage** | SOW-036 |
| **Supports Objectives** | OBJ-007 -- **ASSUMPTION (best-effort mapping via PKG-08 package grouping)**. See Guidance section on OBJ-007 linkage for discussion; human confirmation is needed to resolve this assumption (Lensing C-001). |
| **Anticipated Artifacts** | CODE / DOC / TEST |
| **Scope Item Status** | TBD -- scaffold pending SOW-036 IN decision (OI-036). This deliverable cannot proceed to full implementation until scope is flipped IN. (Source: Decomposition Scope Ledger SOW-036; aligned per Lensing E-001.) |

## Attributes

| Attribute | Value | Source |
|-----------|-------|--------|
| Lock Scope | Deliverable-level (one lock per deliverable folder) | PLAN Section 3.5 |
| Concurrency Unit | Task agent (Type 2) execution against a single deliverable. **Note:** Whether ORCHESTRATOR (Type 1) or INIT (Type 0) agents require lock awareness is TBD; the current specification targets Type 2 task agents only. (Lensing X-006) | PLAN Section 3.5; TYPES.md Section 4.1 |
| Lock Mechanism Type | Filesystem-based lock file | PLAN Section 3.5 |
| Lock Semantics | Lease-based (time-bounded) | PLAN Section 3.5 |
| Orphan Recovery | Required (handle abandoned locks) | PLAN Section 3.5 |
| Integration Surface | Agent instruction protocols (Type 2 task agents) | PLAN Section 3.5 |
| Platform Target | macOS 15+, Apple Silicon | DEC-PLAT-001 |
| State Storage | Filesystem (consistent with K-GHOST-1, DIRECTIVE Section 2.1) | CONTRACT.md; DIRECTIVE.md |
| Lock File Location | TBD (within or adjacent to deliverable folder) -- see Guidance CON-001 for analysis; human ruling required (Lensing A-001) | -- |
| Lock File Format | TBD (contents: holder ID, timestamp, lease duration, PID, deliverable_id) -- see Guidance C2 and Specification REQ-LOCK-002 for proposed fields (Lensing A-001) | -- |
| Maximum Lease Duration | TBD -- Guidance T1 suggests 15-30 min as an **ASSUMPTION**; human ruling required based on observed agent execution times (Lensing B-001) | -- |
| Retry / Backoff Policy | TBD -- see Guidance CON-002 / T2 for analysis; human ruling required (Lensing A-001) | -- |

**Terminology note (Lensing B-004):** The canonical term for the lock artifact across all documents is "lock file." Informal references such as ".lock" refer to the filename convention and are subordinate to this canonical term. See Guidance section on terminology standardization.

## Conditions

| Condition | Description | Source |
|-----------|-------------|--------|
| Scope Status | SOW-036 is TBD; deliverable cannot proceed to full implementation until scope is flipped IN | Decomposition Scope Ledger (SOW-036) |
| Open Issue | OI-036 requires human decision to include/exclude this deliverable | Decomposition Open Issues |
| No External DB | Lock must use filesystem only; no external services or databases | DIRECTIVE Section 5 (Structural Constraints) |
| Git-Trackable | Lock metadata (protocol docs, tests) must be git-trackable; transient lock files themselves need not be committed | DIRECTIVE Section 2.2 |
| Agent Write Scope | Lock acquisition/release must respect agent write-scope boundaries (K-WRITE-1) | CONTRACT.md K-WRITE-1 |
| Lifecycle Compatibility | Lock mechanism must not conflict with `_STATUS.md` lifecycle transitions (K-STATUS-1) | CONTRACT.md K-STATUS-1 |

## Construction

| Component | Description | Status |
|-----------|-------------|--------|
| Lock Protocol Specification | Formal definition of acquire/release/timeout/recovery semantics | TBD |
| Lock File Implementation | Code to create, read, validate, and remove lock files | TBD |
| Agent Integration Layer | Modifications to task agent protocols to acquire/release locks | TBD |
| Orphan Recovery Module | Logic to detect and safely recover stale/abandoned locks | TBD |
| Test Suite | Unit + integration tests for lock lifecycle, contention, and recovery | TBD |
| Documentation | Protocol specification, integration guide, and operational procedure | TBD |

## References

| Reference | Relevance |
|-----------|-----------|
| docs/PLAN.md Section 3.5 | Lock mechanism intent, effort estimate, and sequencing position |
| docs/CONTRACT.md | Invariants governing write scope (K-WRITE-1), status (K-STATUS-1), sealed context (K-SEAL-1), no ghost inputs (K-GHOST-1) |
| docs/SPEC.md Section 2 | Deliverable folder layout (lock file placement context) |
| docs/SPEC.md Section 3 | `_STATUS.md` lifecycle (interaction with locking) |
| docs/TYPES.md Section 4 | Agent type model (lock holders are Type 2 task agents) |
| docs/DIRECTIVE.md Section 2.1, 5 | Filesystem-is-database constraint; no external DB |
| Decomposition (G7-APPROVED) | DEL-08-05 entry, SOW-036, OBJ-007, OI-036 |
