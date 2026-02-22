# Guidance -- DEL-08-05 Deliverable-level Lock Mechanism

## Purpose

This deliverable exists to close a known gap in the Chirality execution model: concurrent task agent (Type 2) execution against the same deliverable folder is currently prevented **by convention** but not **by enforcement** (PLAN Section 3.5). As the system scales to support parallel pipeline execution, convention-only protection becomes insufficient. A formal lock mechanism provides the missing enforcement layer.

This deliverable supports **OBJ-007** (Optional: integrity hardening loop) -- **ASSUMPTION (best-effort mapping via PKG-08 package grouping)**. OBJ-007 is conditional on TBD scope items (SOW-032 through SOW-038) being flipped to IN.

**Contention risk context (Lensing D-003):** In the current system configuration (single-machine, primarily sequential agent dispatch), actual lock contention is expected to be infrequent. The lock mechanism is a **proactive safeguard** for the anticipated transition to parallel agent execution, not a response to observed contention. The scaling trigger for when this mechanism becomes operationally critical is the introduction of concurrent multi-agent pipeline runs against overlapping deliverable sets. **ASSUMPTION** -- current contention risk is low but non-zero (e.g., if ORCHESTRATOR dispatches overlapping task agents or if manual agent runs occur during automated pipeline execution).

## Principles

### P1: Filesystem-Native, Not Service-Dependent

The lock mechanism must use the filesystem as its state store, consistent with the project's foundational constraint that the filesystem is the database (DIRECTIVE Section 2.1). No external lock manager, database, or coordination service is permitted.

- **Source:** DIRECTIVE Section 2.1, Section 5 (Structural Constraints).

### P2: Lease-Based with Bounded Duration

Locks must have a finite, predetermined lease duration. This prevents permanent deadlocks caused by agent crashes, machine restarts, or unexpected termination. The choice of lease duration involves a trade-off (see Trade-offs section).

- **Source:** PLAN Section 3.5 ("lease semantics").

### P3: Fail-Closed for Safety

If a lock cannot be acquired, the requesting agent must **not proceed** with writes to the deliverable folder. Instead, it should report contention to ORCHESTRATOR and allow ORCHESTRATOR to retry, queue, or escalate.

- **Source:** **ASSUMPTION** (derived from the fail-closed pattern established by K-SEAL-1 and the subagent governance model in SPEC.md Section 9.7).

### P4: Minimal Coupling to Existing Protocols

The lock mechanism should be an **additive layer** that wraps existing agent execution protocols, not a rewrite. Existing agents should require minimal changes -- ideally, lock acquire at entry and lock release at exit, with a contention fallback.

- **Source:** PLAN Section 3.5 ("integration into agent instructions"); decomposition note ("keep bounded").

### P5: Orthogonal to Lifecycle

Lock state is a runtime concurrency concern. It must not interfere with or be confused with the `_STATUS.md` lifecycle state machine. A locked deliverable may be in any lifecycle state; an unlocked deliverable may be in any lifecycle state.

- **Source:** CONTRACT.md K-STATUS-1.

## Considerations

### C1: Lock File Placement

**Option A -- Inside the deliverable folder:** e.g., `{DEL_FOLDER}/.lock`

- Pro: Co-located with the deliverable; naturally within `deliverable-local` write scope.
- Pro: Discoverable by any agent already reading the deliverable folder.
- Con: May be accidentally committed to git; requires `.gitignore` entry.
- Con: Visible to human file browsing (minor; could use dotfile convention).

**Option B -- Adjacent to the deliverable folder:** e.g., `{PKG}/1_Working/.locks/{DEL_ID}.lock`

- Pro: Separates transient lock files from deliverable content.
- Con: Requires a broader write scope or a dedicated lock-management scope.
- Con: Adds a new folder convention not currently in SPEC.md.

**Recommendation:** Option A (inside deliverable folder) with `.gitignore` protection. This aligns with the `deliverable-local` write scope model and minimizes architectural changes. **ASSUMPTION -- requires human ruling.**

**Verification consideration (Lensing X-001):** Whichever placement is chosen, a specific verification test should confirm the lock file resides in the correct location and complies with write-scope requirements (REQ-LOCK-008). This test is noted in Specification Verification table.

### C2: Lock File Format

JSON is recommended for the lock file format:
- Human-readable (consistent with DIRECTIVE Section 2.1).
- Parseable by any programming language.
- Consistent with the project's preference for plain files.

**ASSUMPTION** on format choice.

### C3: PID-Based Liveness Check

Using the holder's PID to detect orphan locks is effective on a single machine (the target platform is macOS desktop, DEC-PLAT-001). However:
- PID reuse is possible (though unlikely in short windows).
- On macOS, `kill(pid, 0)` can be used as a non-destructive liveness check.

**ASSUMPTION** on PID-based approach.

### C4: Integration Depth

The decomposition note says "keep bounded." This suggests the lock mechanism should be implementable as a utility module that task agents call, rather than requiring deep changes to every agent's instruction file.

- **Source:** Decomposition DEL-08-05 ContextEnvelopeNotes.

### C5: Interaction with Other PKG-08 Deliverables

PLAN Section 4 (Sequencing Rationale) places the lock mechanism at position 4 of 6 in the hardening sequence. It does not depend on the schema linter (DEL-08-02), folder validator (DEL-08-03), or dependency graph (DEL-08-04), but subsequent deliverables (run records DEL-08-06, staleness DEL-08-07) may need lock awareness.

- **Source:** PLAN Section 4.

### C6: Atomicity Mechanism Selection (Lensing F-001)

The recommended atomicity mechanism for lock acquisition is `open(O_CREAT | O_EXCL)` (or its platform equivalent). This provides atomic file creation on POSIX-compliant filesystems, including APFS on macOS.

**Alternatives considered:**
- `mkdir` (atomic directory creation): Viable but unconventional for lock files; adds directory cleanup complexity.
- `link` (hard link creation): Atomic on most filesystems, but APFS hard link behavior on directories is restricted; adds complexity.
- `rename` (atomic rename from temporary file): Provides atomicity but requires a temporary file location; more complex than `O_CREAT | O_EXCL`.

**Rationale for `O_CREAT | O_EXCL`:** Simplest mechanism with well-understood POSIX semantics. Single system call. Directly creates the lock file (no temporary files or directories needed). Well-supported on APFS (macOS 15+). **ASSUMPTION** on mechanism choice -- implementation may discover platform-specific edge cases that require revision.

- **Source:** Specification REQ-LOCK-003 Implementation Note; POSIX standard (**location TBD** -- OS-level reference).

### C7: Terminology Standardization (Lensing B-004)

The canonical term for the concurrency control artifact is **"lock file"** (two words, no hyphen). All documents use this term as the primary reference. Specific filename conventions (e.g., `.lock`, `_LOCK.json`) refer to implementation-level naming and are subordinate to the canonical term.

Informal usages observed during lensing:
- "lock file" (Specification, Datasheet) -- canonical
- ".lock" (Guidance examples, Procedure Part B) -- filename convention reference
- ".lock file" (Procedure) -- mixed usage, normalized to "lock file"
- "lock" alone (Datasheet attributes) -- acceptable shorthand in context

This standardization does not change the meaning of any existing statement but establishes a consistent baseline for future authoring.

## Trade-offs

### T1: Lease Duration -- Short vs. Long

| Factor | Short Lease (e.g., 5 min) | Long Lease (e.g., 60 min) |
|--------|---------------------------|---------------------------|
| Deadlock recovery | Fast recovery from abandoned locks | Slow recovery; may block other agents |
| Legitimate long tasks | May expire during valid long-running operations | Accommodates long tasks |
| Complexity | May require renewal mechanism | Simpler (no renewal needed) |
| Recommendation | **ASSUMPTION:** A moderate default (e.g., 15-30 min) with optional renewal is a reasonable starting point. TBD -- requires human ruling based on observed agent execution times. |

### T2: Contention Response -- Immediate Fail vs. Retry with Backoff

| Factor | Immediate Fail | Retry with Backoff |
|--------|----------------|-------------------|
| Simplicity | Simple; agent reports LOCK_CONTENTION immediately | More complex; needs retry count and delay logic |
| User experience | Fast feedback; ORCHESTRATOR can decide next step | Transparent retry may succeed without user intervention |
| Resource usage | Minimal | Agent process waits during retry window |
| Recommendation | **ASSUMPTION:** Immediate fail with ORCHESTRATOR-level retry is cleaner (separates concerns). TBD. |

### T3: Git Tracking of Lock Files

Lock files are transient runtime artifacts. They should **not** be committed to git:
- They represent ephemeral concurrency state, not project truth.
- Committing them could cause false conflicts and confusion.
- `.gitignore` entries for lock files are recommended.

This is consistent with DIRECTIVE Section 2.5 (no hidden memory) -- lock files are operational metadata, not authoritative project execution state.

- **Source:** DIRECTIVE Section 2.5 (clarification on non-authoritative convenience state).

## Examples

### Example Lock File Content (ASSUMPTION)

```json
{
  "schema_version": "1.0",
  "deliverable_id": "DEL-08-05",
  "holder": "4_DOCUMENTS",
  "acquired": "2026-02-21T14:30:00-07:00",
  "lease_duration_s": 1800,
  "pid": 42531
}
```

**Note:** The `schema_version` field is included per Lensing B-002 recommendation. It is marked optional in Specification REQ-LOCK-002 pending human decision.

### Example Lock Lifecycle

1. Agent `4_DOCUMENTS` is dispatched to `DEL-08-05` by ORCHESTRATOR.
2. Agent attempts to create the lock file atomically (using `O_CREAT | O_EXCL` or equivalent).
3. File creation succeeds -- agent holds the lock.
4. Agent performs its work (generates four documents).
5. Agent deletes the lock file on completion.
6. If agent crashes: lease expires after `lease_duration_s`; next agent or recovery process detects stale lock and removes it. **Recovery is logged** per REQ-LOCK-006 recording requirement.

### Example Contention Scenario

1. Agent A holds the lock on `DEL-08-05`.
2. Agent B attempts to acquire the lock -- file already exists.
3. Agent B reads the lock file, checks lease expiry and PID liveness.
4. If lock is valid (not expired, PID alive): Agent B reports `LOCK_CONTENTION` to ORCHESTRATOR (with report fields per REQ-LOCK-007).
5. If lock is stale (expired or PID dead): Agent B recovers the orphan lock, **logs the recovery**, and acquires a new one.

## Conflict Table (for human ruling)

| Conflict ID | Conflict | Source A | Source B | Impacted Sections | Proposed Authority | Human Ruling | Resolution Trigger |
|-------------|---------|----------|----------|--------------------|--------------------|--------------|-------------------|
| CON-001 | Lock file placement (inside deliverable folder vs. adjacent) | Guidance C1 Option A (write-scope alignment) | Guidance C1 Option B (content separation) | Specification REQ-LOCK-001, REQ-LOCK-008; Procedure Steps | PROPOSAL: Option A (inside folder) | TBD | SOW-036 IN decision or earlier if design work begins (Lensing E-002) |
| CON-002 | Contention response strategy (immediate fail vs. retry) | Guidance T2 Immediate Fail | Guidance T2 Retry with Backoff | Specification REQ-LOCK-007; Procedure Steps | PROPOSAL: Immediate fail at agent level, retry at ORCHESTRATOR level | TBD | SOW-036 IN decision or earlier if design work begins (Lensing E-002) |
| CON-003 | Scope governance posture: active-scaffold vs. blocked-pending (Lensing E-001) | Datasheet: "TBD (not yet flipped to IN; see OI-036)" (implies may not proceed) | Specification: "scaffold pending SOW-036 IN decision" (implies valid scaffold work) | Datasheet Scope Item Status; Specification Precondition | PROPOSAL: Align framing -- both documents now say "scaffold pending SOW-036 IN decision" | TBD (aligned by 4_DOCUMENTS Pass 3; human confirms framing) | OI-036 resolution |
