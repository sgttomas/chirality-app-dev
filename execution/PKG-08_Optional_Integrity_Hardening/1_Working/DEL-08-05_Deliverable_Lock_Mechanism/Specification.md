# Specification -- DEL-08-05 Deliverable-level Lock Mechanism

## Scope

### Covered

This specification defines the deliverable-level lock mechanism that prevents concurrent task agent (Type 2) execution against the same deliverable folder. It covers:

- Lock file format, location, and lifecycle semantics
- Acquisition, release, and timeout protocols
- Orphan lock detection and recovery
- Integration requirements for task agent instruction protocols
- Verification approach for lock correctness

**Type classification:** This deliverable is classified as SECURITY_CONTROL (Source: _CONTEXT.md). Requirements and verification criteria below are framed accordingly -- the lock mechanism is a security control preventing unauthorized concurrent write access. (Lensing E-003)

### Excluded

- Locks at package level or execution-root level (this mechanism is deliverable-scoped only)
- Locks for human editing (this mechanism governs agent concurrency, not human file access)
- Distributed locking across multiple machines (the system is single-machine desktop; see DEC-PLAT-001)
- Modifications to `_STATUS.md` lifecycle state machine (lock state is orthogonal to lifecycle state)

### Precondition

SOW-036 is currently **TBD**. This specification is a scaffold pending SOW-036 IN decision (OI-036); requirements below represent the best-effort interpretation from available sources and are subject to revision when SOW-036 is flipped to IN by human decision. (Source: Decomposition Scope Ledger SOW-036)

## Requirements

### REQ-LOCK-001: Lock File Existence as Lock State

The lock state for a deliverable MUST be represented by the presence or absence of a lock file within or adjacent to the deliverable folder.

- **Rationale:** Filesystem-is-database (DIRECTIVE Section 2.1); no external state (DIRECTIVE Section 5).
- **Source:** PLAN Section 3.5 ("e.g., `.lock` file with lease semantics"); DIRECTIVE Section 2.1.
- **Verification note (Lensing X-001):** The verification approach for this requirement should include a specific test for lock file placement compliance -- confirming the lock file resides in a location consistent with write-scope requirements (REQ-LOCK-008). See Verification table.

### REQ-LOCK-001a: Lock File Naming Convention

The lock file MUST use a standardized name. TBD -- the canonical filename (e.g., `.lock` or `_LOCK.json`) must be determined and mandated here. The chosen name must be consistent with the canonical term "lock file" used across all documents.

- **Rationale:** Informal references to `.lock` appear in Guidance and Procedure but no requirement formally mandates the name. A binding naming convention prevents implementation drift. (Lensing A-002)
- **Source:** **ASSUMPTION** -- derived from consistency requirement; human ruling on file format/name needed.

### REQ-LOCK-002: Lock File Contents

The lock file MUST contain at minimum:

| Field | Type | Purpose |
|-------|------|---------|
| `holder` | string | Identifier of the acquiring agent/session |
| `acquired` | ISO 8601 timestamp | When the lock was acquired |
| `lease_duration_s` | integer | Maximum lease duration in seconds |
| `pid` | integer | Process ID of the lock holder |
| `deliverable_id` | string | The deliverable ID being locked (e.g., `DEL-08-05`) |
| `schema_version` | string (optional) | Lock file format version identifier for future evolution. TBD -- recommended to support forward compatibility. (Lensing B-002) |

- **Rationale:** Enables orphan detection (stale PID), lease expiry calculation, and audit. The optional `schema_version` field supports format evolution without ambiguity between old and new lock files (Lensing B-002).
- **Source:** PLAN Section 3.5 (lease semantics, orphan recovery); **ASSUMPTION** on specific fields.

### REQ-LOCK-003: Atomic Acquisition

Lock acquisition MUST be atomic at the filesystem level. If two agents attempt to acquire the lock simultaneously, exactly one MUST succeed and the other MUST fail.

- **Rationale:** Prevents race conditions in concurrent execution.
- **Source:** **ASSUMPTION** (standard concurrency requirement derived from PLAN Section 3.5 intent).
- **Implementation Note:** On macOS/POSIX, `open(O_CREAT | O_EXCL)` or equivalent atomic file creation can provide this guarantee. TBD -- specific implementation approach. See Guidance for rationale on mechanism selection and alternatives considered (Lensing F-001).

### REQ-LOCK-004: Lease-Based Expiry

A lock MUST have a finite lease duration. After the lease expires, the lock is considered stale and eligible for recovery.

- **Rationale:** Prevents permanent deadlock from crashed or abandoned agents.
- **Source:** PLAN Section 3.5 ("lease semantics").
- **Boundary values (Lensing F-002):** TBD -- minimum and maximum acceptable lease durations, tolerance for expiry detection latency, and quantitative acceptance criteria should be specified once the default lease duration is decided. See Guidance T1 for trade-off analysis (ASSUMPTION: 15-30 min range suggested).

### REQ-LOCK-005: Explicit Release

The lock holder MUST explicitly release the lock upon completion (success or failure) of its task execution.

- **Rationale:** Minimizes unnecessary lock contention.
- **Source:** **ASSUMPTION** (standard locking hygiene).

### REQ-LOCK-006: Orphan Lock Recovery

The system MUST provide a mechanism to detect and recover orphan locks (locks where the holder is no longer running or the lease has expired).

Recovery criteria (at least one must be true for recovery):
- The lease duration has elapsed since acquisition time.
- The `pid` field does not correspond to a running process.

**Recording requirement (Lensing F-004):** Both automated and manual recovery paths MUST record the recovery action. The automated recovery path (as described in Procedure Part B Lock Acquisition step 4c) must log the orphan recovery event with the same level of detail as the manual recovery path. This prevents untracked automated recoveries.

- **Rationale:** PLAN Section 3.5 explicitly requires orphan recovery. Recording requirement addresses the inconsistency between automated and manual recovery paths identified by Lensing F-004.
- **Source:** PLAN Section 3.5 ("orphan recovery"); Lensing F-004 (consistency enforcement).

### REQ-LOCK-007: Agent Instruction Integration

Task agent (Type 2) protocols MUST be updated to:
1. Attempt lock acquisition before writing to a deliverable folder.
2. Release the lock on completion (including error paths).
3. Fail gracefully (report `LOCK_CONTENTION` to ORCHESTRATOR) if the lock cannot be acquired.

**LOCK_CONTENTION report format (Lensing B-003):** The LOCK_CONTENTION report MUST contain at minimum:

| Field | Type | Purpose |
|-------|------|---------|
| `deliverable_id` | string | The deliverable the agent attempted to lock |
| `holder` | string | The current lock holder (from lock file) |
| `lease_remaining_s` | integer | Estimated seconds remaining on current lease |
| `contention_time` | ISO 8601 timestamp | When the contention was detected |

TBD -- additional fields may be required based on ORCHESTRATOR retry/escalation logic.

- **Rationale:** PLAN Section 3.5 ("integration into agent instructions"). Report format defined to enable ORCHESTRATOR retry/escalation decisions (Lensing B-003).
- **Source:** PLAN Section 3.5; TYPES.md Section 4.1 (Type 2 agent model).

### REQ-LOCK-008: Write Scope Compatibility

The lock mechanism MUST NOT require any agent to write outside its declared write scope (K-WRITE-1). If the lock file resides inside the deliverable folder, only agents with `deliverable-local` write scope may acquire/release it. If the lock file resides outside the deliverable folder, the placement MUST be justified and scoped appropriately.

- **Source:** CONTRACT.md K-WRITE-1.

### REQ-LOCK-009: Lifecycle Orthogonality

Lock state MUST be independent of `_STATUS.md` lifecycle state. Acquiring or releasing a lock MUST NOT trigger a lifecycle state transition.

- **Source:** CONTRACT.md K-STATUS-1; SPEC.md Section 3.

### REQ-LOCK-010: No Ghost Inputs

The lock file MUST NOT introduce information that agents treat as execution context beyond the lock's concurrency-control purpose. Lock file contents are operational metadata, not sealed context.

- **Source:** CONTRACT.md K-GHOST-1.

### REQ-LOCK-011: Platform Compatibility

The lock mechanism MUST function correctly on macOS 15+ / Apple Silicon (the sole target platform).

- **Source:** DEC-PLAT-001.

### REQ-LOCK-012: Lock File Cleanup on Deliverable Lifecycle Termination

TBD -- A requirement is needed to address lock file behavior when a deliverable folder is deleted, moved, or archived. Specifically: what happens to an active or stale lock file when the deliverable it protects undergoes lifecycle termination (deletion or archival)? **ASSUMPTION** -- the lock file should be removed as part of deliverable cleanup, but this needs human ruling. (Lensing C-002)

- **Rationale:** The comprehensive mandate lens reveals no existing requirement covers the lock lifecycle in relation to deliverable lifecycle termination.
- **Source:** Lensing C-002; **ASSUMPTION**.

### REQ-LOCK-013: Lock Lease Renewal (Conditional)

TBD -- If long-running agents require lease extensions beyond the default lease duration, a renewal mechanism MUST be provided. The decision on whether renewal is required depends on observed agent execution times and the chosen lease duration.

- **Rationale:** Guidance T1 mentions "optional renewal" as a possibility for short leases. If the default lease duration is short (e.g., 15 min) and agents regularly exceed it, renewal becomes a functional necessity. (Lensing F-003)
- **Source:** Guidance T1; **ASSUMPTION** -- human decides whether renewal is needed.

## Standards

| Standard / Invariant | Relevance | Accessible |
|----------------------|-----------|------------|
| K-WRITE-1 (CONTRACT.md) | Agent write scope enforcement | Yes |
| K-STATUS-1 (CONTRACT.md) | Lifecycle state authority | Yes |
| K-GHOST-1 (CONTRACT.md) | No ghost inputs | Yes |
| K-SEAL-1 (CONTRACT.md) | Sealed context before Type 2 execution | Yes |
| POSIX file creation atomicity | Atomic lock acquisition on macOS | **location TBD** (OS-level reference) |

## Verification

| Requirement | Verification Method | Acceptance Criteria |
|-------------|--------------------|--------------------|
| REQ-LOCK-001 | Inspection + Test | Lock state correctly represented by file presence/absence |
| REQ-LOCK-001 (placement) | Test (Lensing X-001) | Lock file resides in a location compliant with write-scope rules (REQ-LOCK-008); test validates placement against deliverable-local scope |
| REQ-LOCK-001a | Inspection | Lock file uses the mandated canonical filename; all references in code use the same name |
| REQ-LOCK-002 | Inspection + Test | Lock file contains all required fields; fields are parseable; optional `schema_version` field is present if implemented |
| REQ-LOCK-003 | Concurrency Test | Under simultaneous acquisition attempts (TBD: specify number of parallel attempts, e.g., 5-10 concurrent agents; expected result: exactly one succeeds per attempt set), exactly one succeeds. (Lensing A-003 -- strengthen acceptance criteria) |
| REQ-LOCK-004 | Test (time-based) | Expired lease is detected and lock is eligible for recovery. TBD: add quantitative criteria once lease duration is decided -- minimum/maximum acceptable lease durations, detection latency tolerance (Lensing F-002) |
| REQ-LOCK-005 | Test | Lock file is removed after task completion (success and failure paths) |
| REQ-LOCK-006 | Test (orphan simulation) | Stale locks are detected and recovered without data loss; recovery action is logged (both automated and manual paths per Lensing F-004) |
| REQ-LOCK-006 (concurrent recovery) | Concurrency Test (Lensing X-005) | When two agents simultaneously detect a stale lock and attempt recovery, exactly one succeeds in acquiring the new lock; the other receives LOCK_CONTENTION or retries safely. No data corruption or double-recovery. |
| REQ-LOCK-007 | Integration Test | Task agents acquire/release locks; contention produces LOCK_CONTENTION report containing required fields (deliverable_id, holder, lease_remaining_s, contention_time) |
| REQ-LOCK-008 | Code Review + Test (Lensing D-001) | No write-scope violations introduced by lock operations. TBD: define specific test that validates lock file writes stay within deliverable-local scope (e.g., verify lock file path is a descendant of the deliverable folder, or that any non-local placement is explicitly authorized). |
| REQ-LOCK-009 | Test | Lock operations do not alter `_STATUS.md` |
| REQ-LOCK-010 | Code Review (Lensing D-002) | Lock file not consumed as agent execution context. Testable criterion: no agent reads lock file contents to alter execution decisions beyond contention handling (acquire/release/recover operations only). |
| REQ-LOCK-011 | Platform Test (Lensing X-004) | Mechanism works on macOS 15+ Apple Silicon. APFS-specific test criteria TBD: verify atomic file creation semantics on APFS, test case-sensitivity behavior, confirm no APFS-specific edge cases (e.g., firmlink or clone interference). |
| REQ-LOCK-012 | TBD | TBD -- pending requirement definition |
| REQ-LOCK-013 | TBD | TBD -- pending decision on renewal necessity |

**Additional verification gap (Lensing X-002):** Consider adding an optional lock mechanism self-test or startup health check that verifies lock acquisition/release works correctly before entering production use. This would catch filesystem permission or path issues early. TBD -- human decides whether this is in scope.

**Additional verification gap (Lensing X-003):** Add a negative test case for lock file permission/ownership failures (e.g., lock file created by one OS user, another user cannot read/delete it). TBD -- relevant if multiple OS users may run agents against the same deliverable folder.

## Documentation

| Artifact | Type | Description |
|----------|------|-------------|
| Lock Protocol Specification | DOC | Formal protocol document (acquire/release/recover semantics) |
| Lock Implementation Module | CODE | Source code for lock file management |
| Agent Integration Guide | DOC | Instructions for integrating lock into task agent protocols |
| Test Suite | TEST | Unit tests + concurrency tests + orphan recovery tests |
| Operational Runbook | DOC | Troubleshooting guide for lock-related issues |
