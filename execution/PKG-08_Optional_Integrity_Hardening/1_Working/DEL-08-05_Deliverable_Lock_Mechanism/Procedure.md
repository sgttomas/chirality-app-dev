# Procedure -- DEL-08-05 Deliverable-level Lock Mechanism

## Purpose

This procedure defines the steps to **produce** the deliverable-level lock mechanism (design, implement, test, document) and the steps to **operate** the lock mechanism once implemented (acquire, release, recover).

Both aspects are included because this deliverable produces both a protocol specification and operational code/tests (anticipated artifacts: CODE/DOC/TEST).

---

## Part A: Production Procedure (How to Produce This Deliverable)

### Prerequisites

| Prerequisite | Description | Status |
|--------------|-------------|--------|
| Scope Decision | SOW-036 must be flipped to IN by human decision (OI-036) | TBD |
| Governance References | docs/CONTRACT.md, docs/SPEC.md, docs/TYPES.md, docs/DIRECTIVE.md must be accessible | Available |
| Platform Access | macOS 15+ / Apple Silicon development environment | TBD |
| Agent Instruction Access | Current task agent instruction files (`AGENT_*.md`) for integration analysis | TBD |
| Decomposition Approval | Decomposition G7-APPROVED is the accepted basis | Available |

### Steps

#### Step 1: Resolve Open Issues

1. Obtain human ruling on OI-036 (scope decision: IN/OUT/TBD for SOW-036).
2. If OUT: retire this deliverable; update `_STATUS.md` accordingly.
3. If IN: proceed to Step 2.
4. If TBD remains: this deliverable cannot proceed beyond scaffold state.

**Verification:** Human ruling is recorded in the decomposition or `_MEMORY.md`.

#### Step 2: Resolve Design Decisions

1. Review the Conflict Table in `Guidance.md`.
2. Obtain human rulings on:
   - CON-001: Lock file placement (inside folder vs. adjacent).
   - CON-002: Contention response strategy (immediate fail vs. retry).
   - CON-003: Scope governance posture alignment.
3. Determine lease duration default and whether renewal is needed (see Specification REQ-LOCK-013).
4. Determine lock file naming convention (see Specification REQ-LOCK-001a).
5. Confirm OBJ-007 mapping or provide correct objective linkage (see Lensing C-001).
6. Record decisions in `_MEMORY.md`.

**Verification:** All Conflict Table entries have human rulings recorded.

#### Step 3: Write Lock Protocol Specification

1. Using the resolved design decisions, formalize the lock protocol in a protocol specification document.
2. Define: lock file format (JSON), location, field semantics (including optional `schema_version` per REQ-LOCK-002).
3. Define: acquisition protocol (atomic file creation; see Guidance C6 for mechanism rationale).
4. Define: release protocol (file deletion).
5. Define: lease expiry calculation and orphan detection criteria.
6. Define: recovery protocol (stale lock removal and re-acquisition), including recording requirements for both automated and manual paths (REQ-LOCK-006).
7. Define: LOCK_CONTENTION report format (REQ-LOCK-007).
8. Define: lock file cleanup on deliverable lifecycle termination (REQ-LOCK-012), if included.
9. Cross-reference against requirements in `Specification.md`.

**Verification:** Protocol specification covers all requirements (REQ-LOCK-001 through REQ-LOCK-013 as applicable).

#### Step 4: Implement Lock Module

1. Implement lock file creation/read/validate/delete operations.
2. Use atomic file creation (`O_CREAT | O_EXCL` or platform equivalent) for acquisition (see Guidance C6).
3. Implement PID liveness check for orphan detection.
4. Implement lease expiry calculation.
5. Ensure all file operations respect `deliverable-local` write scope.

**Verification:** Code compiles and passes unit tests on macOS 15+ / Apple Silicon.

#### Step 5: Implement Agent Integration Layer

1. Identify task agent (Type 2) instruction files that write to deliverable folders.
2. Add lock acquisition to agent entry protocol (before any deliverable writes).
3. Add lock release to agent exit protocol (on success, failure, and error paths).
4. Add `LOCK_CONTENTION` reporting to ORCHESTRATOR on acquisition failure (with required report fields per REQ-LOCK-007).
5. Ensure integration does not modify agent write scopes.

**Verification:** Modified agent protocols compile and function correctly with lock enabled.

#### Step 6: Write Test Suite

1. Write unit tests for lock file creation, read, validate, and delete.
2. Write concurrency tests simulating simultaneous acquisition attempts (see Specification REQ-LOCK-003 verification criteria for parameters).
3. Write orphan recovery tests (simulate PID death, lease expiry).
4. Write concurrent orphan recovery tests (two agents detect same stale lock simultaneously; see Specification REQ-LOCK-006 concurrent recovery verification).
5. Write integration tests verifying agent lock/unlock lifecycle.
6. Write negative tests (lock contention, invalid lock files, corrupted lock files, permission/ownership failures).
7. Write APFS-specific platform tests (see Specification REQ-LOCK-011 verification criteria).

**Verification:** All tests pass on macOS 15+ / Apple Silicon. Test coverage addresses all requirements.

#### Step 7: Write Documentation

1. Finalize lock protocol specification (from Step 3).
2. Write agent integration guide (how to add locking to new agents).
3. Write operational runbook (troubleshooting stale locks, manual recovery).
4. Update `Specification.md` with final requirement values (lease duration, etc.).

**Verification:** Documentation is complete and cross-referenced with code and tests.

#### Step 8: Final Review

1. Run full test suite.
2. Verify cross-document consistency (Datasheet, Specification, Guidance, Procedure).
3. Verify all TBD items are resolved or explicitly deferred.
4. Submit for human review (transition to CHECKING via `_STATUS.md`).

**Verification:** Deliverable is ready for CHECKING state transition.

---

## Part B: Operational Procedure (How to Use the Lock Mechanism)

> Note: This section describes the intended operational behavior of the completed lock mechanism. All steps below are TBD pending implementation.

### Prerequisites

| Prerequisite | Description | Traceability to Part A |
|--------------|-------------|----------------------|
| Lock Module Available | Lock implementation is deployed and accessible to task agents | Part A Step 4 (Implement Lock Module) |
| Agent Integration Complete | Task agent protocols include lock acquire/release steps | Part A Step 5 (Implement Agent Integration Layer) |
| `.gitignore` Updated | Lock files (e.g., the canonical lock filename) are excluded from git tracking | Part A Step 7 (Write Documentation -- includes `.gitignore` setup) |

**(Lensing A-004):** Each Part B prerequisite is now cross-referenced to its Part A production step for traceability.

### Steps: Lock Acquisition

1. Before writing to a deliverable folder, the task agent calls the lock acquisition function with:
   - `deliverable_id`: the target deliverable ID
   - `holder`: the agent's identity (e.g., `4_DOCUMENTS`)
   - `lease_duration_s`: the requested lease duration
   - `pid`: the current process ID
2. The function attempts atomic creation of the lock file (using `O_CREAT | O_EXCL` or platform equivalent; see Guidance C6).
3. **If successful:** The agent holds the lock. Proceed with deliverable writes.
4. **If file already exists:**
   a. Read the existing lock file. **If the lock file is corrupt or unparseable** (e.g., truncated JSON, missing required fields): treat as a recoverable error. Log the corruption, remove the corrupt lock file, and retry acquisition (go to step 2). Log the corrupt lock file recovery. **(Lensing C-003)** **ASSUMPTION** -- corrupt lock files are treated as recoverable (equivalent to stale lock); human may override to require escalation instead.
   b. If parseable: check if the lock is stale (lease expired OR holder PID is not running).
   c. **If stale:** Remove the orphan lock file. Retry acquisition (go to step 2). **Log orphan recovery** with structured record (see Records section). (Lensing F-004)
   d. **If valid:** Report `LOCK_CONTENTION` to ORCHESTRATOR with required report fields (deliverable_id, holder, lease_remaining_s, contention_time per REQ-LOCK-007). Do not proceed with writes.

### Steps: Lock Release

1. On task completion (success or failure), the agent calls the lock release function.
2. The function verifies the lock file exists and the `holder` matches the releasing agent.
3. The function deletes the lock file.
4. If the lock file does not exist or the holder does not match: log a warning (lock was already released or recovered by another process).

### Steps: Orphan Recovery (Manual)

1. Identify the stale lock file in the deliverable folder.
2. Read the lock file contents (holder, acquired timestamp, lease duration, PID).
3. If the lock file is corrupt or unparseable: skip liveness/lease checks; proceed directly to step 5 (the lock file is unrecoverable as valid state). **(Lensing C-003)**
4. Check PID liveness: `kill -0 {pid}` -- if it returns an error, the holder is not running.
5. Check lease expiry: current time > acquired + lease_duration_s.
6. If **either** condition is met (PID dead OR lease expired) or the file is corrupt: the lock is stale. Delete the lock file.
7. Record the recovery action in `_MEMORY.md` or operational log with structured fields (see Records section). (Lensing F-004)

### Verification

| Check | Expected Result |
|-------|-----------------|
| Lock file exists during agent execution | Lock file present in deliverable folder |
| Lock file removed after agent completion | Lock file absent from deliverable folder |
| Concurrent acquisition blocked | Second agent receives `LOCK_CONTENTION` |
| Orphan lock recovered | Stale lock file removed after lease expiry / PID death |
| Concurrent orphan recovery safe | Two agents detecting same stale lock: exactly one acquires; no data loss |
| Corrupt lock file handled | Corrupt lock file is removed and recovery is logged |
| `_STATUS.md` unaffected | Lifecycle state unchanged by lock operations |
| No git pollution | Lock files not tracked by git |

### Records

| Record | Location | Purpose | Structured Fields (Lensing A-005) |
|--------|----------|---------|----------------------------------|
| Lock acquisition/release log | TBD (agent execution log or `_MEMORY.md`) | Audit trail of lock operations | `timestamp`, `agent`, `deliverable_id`, `action` (acquire/release), `outcome` (success/contention/error) |
| Orphan recovery log | TBD (agent execution log or `_MEMORY.md`) | Record of recovered stale locks (both automated and manual per Lensing F-004) | `timestamp`, `agent`, `deliverable_id`, `action` (orphan_recovery), `recovery_reason` (lease_expired/pid_dead/corrupt), `previous_holder`, `previous_acquired` |
| Contention reports | ORCHESTRATOR log | Record of failed acquisition attempts | Per REQ-LOCK-007 report fields: `deliverable_id`, `holder`, `lease_remaining_s`, `contention_time` |
| Test results | Test suite output | Evidence of lock mechanism correctness | -- (standard test output) |
