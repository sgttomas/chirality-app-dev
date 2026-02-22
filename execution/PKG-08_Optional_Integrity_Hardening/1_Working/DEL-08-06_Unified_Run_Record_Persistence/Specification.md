# Specification — DEL-08-06 Unified Pipeline Run Record Persistence

## Scope

### Included

- Define a unified run record schema for Type 2 (specialist) agent pipeline executions.
- Define the storage location and persistence mechanism for run records within the filesystem-as-state model.
- Define the integration contract for Type 2 agent protocols to emit run records.
- Provide documentation (schema reference), code (persistence implementation), and tests (schema validation + integration).

Source: Decomposition DEL-08-06 entry; PLAN Section 3.6.

### Excluded

- Staleness propagation and triage tooling (covered by DEL-08-07; that deliverable depends on this one).
- On-demand dependency graph generation (covered by DEL-08-04).
- Modification of existing `_STATUS.md` or `_DEPENDENCIES.md` schemas — this deliverable adds a new artifact, not a replacement for existing tracking.
- UI-level run record visualization (no UI scope item is assigned to PKG-08).
- Run records for Type 0 or Type 1 agents — **ASSUMPTION: scope is limited to Type 2 task-agent executions per PLAN Section 3.6 ("per Agent 2 execution")**.

### Design Boundary

> Keep bounded to one schema + one storage location.
> -- Decomposition ContextEnvelopeNotes for DEL-08-06

### Scope Prerequisite Gate

**REQ-SCOPE-GATE:** Implementation phases (Phase 2 and Phase 3 in Procedure) SHALL NOT commence until SOW-037 has been flipped from TBD to IN (OI-037 resolved). Documentation artifacts (Phase 1) may proceed in advance to inform the scope decision.

**Rationale:** The conformance basis for starting implementation depends on OI-037 resolution. The Datasheet condition and Guidance C5 note this prerequisite, but a SHALL-level gate in the normative document ensures it is enforceable, not merely advisory (Lensing item F-001).

Source: Decomposition Open Issues OI-037; Datasheet Conditions "Scope prerequisite."

## Requirements

### REQ-01: Run Record Schema Definition

A unified schema MUST be defined that captures the following fields for each Type 2 agent pipeline execution:

| Field | Type | Required | Description | Source |
|-------|------|----------|-------------|--------|
| `RunID` | string | MUST | Unique identifier for the run (e.g., `RUN-{DEL-ID}-{YYYYMMDD}-{HHmm}-{SEQ}`) | **ASSUMPTION** — format TBD; must be unique and sortable |
| `DeliverableID` | string | MUST | Stable deliverable ID (`DEL-XX-YY`) | TYPES Section 2 |
| `AgentName` | string | MUST | Name of the Type 2 agent that executed (e.g., `4_DOCUMENTS`, `DEPENDENCIES`, `CHIRALITY_FRAMEWORK`) | SPEC Section 9.1 |
| `AgentType` | enum | MUST | `TYPE_2` (may extend to other types in future) | TYPES Section 4.1 |
| `RunTimestamp` | ISO 8601 datetime | MUST | UTC timestamp when the run started | **ASSUMPTION** — UTC for consistency |
| `RunDuration` | string | SHOULD | Duration of the run (ISO 8601 duration or human-readable) | PLAN Section 3.6 |
| `RunStatus` | enum | MUST | `SUCCESS`, `PARTIAL`, `FAILED`, `SKIPPED` — see RunStatus Lifecycle below | **ASSUMPTION** — derived from common agent outcomes |
| `RunPassDirective` | string | SHOULD | Pass directive provided (e.g., `FULL`, `P1_P2`, `P3_ONLY`) | Agent protocol conventions |
| `InputContextSHA` | string | SHOULD | Git SHA or content hash of the governed input state at run start — **NOTE:** architectural significance is high (Guidance P5; DEL-08-07 dependency); see Conflict Table CON-05 in Guidance.md and cross-matrix conflict XCON-01 regarding MUST vs. SHOULD elevation (Lensing items F-002, E-003) | K-VAL-1 (CONTRACT); PLAN Section 3.7 |
| `InputFiles` | list | SHOULD | List of input files consumed (paths relative to deliverable folder) — contributes to K-PROV-1 provenance coverage | K-GHOST-1 (CONTRACT); K-PROV-1 (CONTRACT) |
| `OutputFiles` | list | SHOULD | List of output files produced or modified (paths relative to deliverable folder) | PLAN Section 3.6 ("output artifact list") |
| `StatusBefore` | string | SHOULD | `_STATUS.md` state before the run | K-STATUS-1 (CONTRACT) |
| `StatusAfter` | string | SHOULD | `_STATUS.md` state after the run | K-STATUS-1 (CONTRACT) |
| `ErrorSummary` | string | MAY | Brief error description if `RunStatus` is `FAILED` or `PARTIAL` | PLAN Section 3.6 |
| `Notes` | string | MAY | Free-text notes or warnings from the run | General |
| `SchemaVersion` | string | MUST | Run record schema version identifier (e.g., `v1.0`) | Pattern from Dependencies.csv v3.1 (SPEC Section 6.1) |

Source for schema need: PLAN Section 3.6 ("schema definition").

#### RunStatus Lifecycle (Lensing item B-003)

The `RunStatus` enum values and their transition semantics:

| Status | Meaning | Trigger Condition | Transition From |
|--------|---------|-------------------|-----------------|
| `SUCCESS` | Agent completed all requested passes with no errors | All pass steps completed; all outputs produced | (initial state on run completion) |
| `PARTIAL` | Agent completed some but not all requested work | Some outputs produced; others failed or were skipped due to missing inputs (e.g., `FAILED_INPUTS` for a pass) | (initial state on run completion) |
| `FAILED` | Agent encountered an error that prevented meaningful output | Fatal error; no usable outputs produced | (initial state on run completion) |
| `SKIPPED` | Agent did not execute because preconditions were not met | `SKIPPED_PROTECT_HUMAN_WORK`, `UNSUPPORTED_VARIANT`, or other precondition check failure before any work began | (initial state on run completion) |

**Notes:**
- RunStatus is set once at run completion and is immutable thereafter (per REQ-03).
- A run cannot transition between statuses after recording — each run produces exactly one record with one final status.
- The boundary between `PARTIAL` and `FAILED` is: `PARTIAL` means some usable outputs were produced; `FAILED` means none were.
- `SKIPPED` is distinct from `FAILED` in that no work was attempted (precondition gate prevented execution).

**TBD:** Whether sub-run detail (per-pass status within a multi-pass run) should be captured in a separate field or is adequately covered by `RunPassDirective` + `Notes`. **ASSUMPTION:** One record per agent invocation is sufficient; per-pass detail goes in `Notes` if needed.

#### K-PROV-1 Traceability (Lensing item E-002)

The run record schema addresses K-PROV-1 (provenance requirements: "run records should cite what was consumed") through the following field mappings:

| K-PROV-1 Aspect | Run Record Field | Coverage |
|------------------|-----------------|----------|
| What was consumed | `InputFiles` | Lists input files consumed (paths relative to deliverable folder) |
| Context state at consumption | `InputContextSHA` | Captures hash of governed input state at run start |
| Who consumed it | `AgentName`, `AgentType` | Identifies the consuming agent |
| When it was consumed | `RunTimestamp` | Captures run start time |
| What was produced | `OutputFiles` | Lists output files produced or modified |

**Note:** The Standards table lists K-PROV-1 with the note "run records should cite what was consumed." This traceability table makes the mapping explicit rather than implicit (Lensing item E-002).

Source: K-PROV-1 (CONTRACT); `_SEMANTIC_LENSING.md` item E-002.

### REQ-02: Storage Location

Run records MUST be persisted as plain-file, git-trackable artifacts within the filesystem-as-state model.

**Storage location decision is TBD.** The following options are under consideration:

| Option | Location | Pros | Cons |
|--------|----------|------|------|
| A — Deliverable-local | `{DEL_FOLDER}/_RUN_HISTORY.md` or `RunRecords.csv` | Collocated with deliverable; easy to find; consistent with `_DEPENDENCIES.md` pattern | File grows over time; may need rotation |
| B — Tool-root snapshot | `{TOOL_ROOT}/{SNAPSHOT}/run-record.md` | Immutable per K-SNAP-1; clean separation | Dispersed; harder to aggregate for a single deliverable |
| C — Hybrid | Deliverable-local summary + tool-root detail | Best of both; summary enables quick lookup | More complex; two files to maintain |

**ASSUMPTION:** Option A (deliverable-local) is the most consistent with existing patterns (`_DEPENDENCIES.md` run history, `_STATUS.md` history) and the deliverable-local-register design principle (K-DEP-1). Final decision requires human ruling.

**Decision gate (Lensing item A-001):** The storage location decision (CON-01) MUST be finalized and documented in the Conflict Table (Guidance.md) before Phase 2 implementation begins. Acceptance criteria: human ruling recorded for CON-01 and CON-02; chosen location documented in the Run Record Schema Reference (Phase 1 output). Until this gate is satisfied, REQ-02 verification criteria cannot be fully evaluated.

Source: PLAN Section 3.6 ("storage location decision"); DIRECTIVE Section 2.1; K-DEP-1 (CONTRACT); `_SEMANTIC_LENSING.md` item A-001.

### REQ-03: Immutability Semantics

Once a run record is written for a completed execution, its content MUST NOT be modified.

- If the storage model is append-only (Option A), new runs append; existing entries are immutable.
- If the storage model uses snapshots (Option B), snapshot immutability per K-SNAP-1 applies.
- Run records MUST NOT be deleted. Superseded or invalid runs may be annotated but not removed.

**K-SNAP-1 applicability note (Lensing item A-002):** K-SNAP-1 governs snapshot immutability (a snapshot folder, once written, is not modified). If Option A (append-only file) is chosen, the immutability guarantee operates at the record-entry level rather than the file level — the file grows via append, but individual entries within it are immutable. This is a semantic distinction from K-SNAP-1's folder-level immutability. The compliance determination path for Option A is: verify that no existing entry content is altered when a new entry is appended (byte-level comparison of pre-existing content). **TBD:** Whether K-SNAP-1 formally covers append-only file semantics or whether a supplementary invariant is needed — see Conflict Table CON-06 in Guidance.md and cross-matrix conflict XCON-02.

Source: K-SNAP-1 (CONTRACT); SPEC Section 11.1; `_SEMANTIC_LENSING.md` item A-002.

### REQ-04: Agent Protocol Integration

Type 2 agent protocols MUST be extended to emit a run record upon completion of a pipeline execution.

- Run record emission MUST be the **last step** before reporting completion to ORCHESTRATOR.
- Run record emission MUST NOT block or alter the primary agent outputs.
- If run record emission fails, the agent SHOULD report the failure to ORCHESTRATOR but MUST NOT fail the overall run.

**ASSUMPTION:** Integration is additive — existing agent behavior is unchanged; run record writing is appended to the protocol.

**Content accuracy verification (Lensing item D-003):** The run record metadata (AgentName, InputFiles, OutputFiles, StatusBefore, StatusAfter, RunStatus) MUST accurately reflect the actual execution. Verification criteria for "matches actual execution metadata" (from the Verification table):
- `AgentName` matches the agent's self-reported identity.
- `InputFiles` matches the set of files the agent read during execution (as determinable from the agent's protocol).
- `OutputFiles` matches the set of files the agent wrote or modified.
- `StatusBefore` and `StatusAfter` match `_STATUS.md` state at run start and run end respectively.
- `RunStatus` accurately reflects the agent's completion outcome per the RunStatus Lifecycle definition.

**TBD:** How discrepancies between recorded metadata and actual execution are detected at runtime (as opposed to during testing). **ASSUMPTION:** Testing validates accuracy; runtime validation may be added as part of post-write validation (see Procedure Phase 2 enrichment, Lensing item X-005).

Source: PLAN Section 3.6 ("integration into task agent protocols"); `_SEMANTIC_LENSING.md` items D-003, X-005.

### REQ-05: Baseline SHA Tracking

Run records SHOULD include the git SHA (or content hash) of the governed input state at the start of the run.

- This enables downstream staleness detection (K-VAL-1: "a deliverable is dirty if any governed input has changed since its last approved SHA").
- The specific method of SHA computation (git HEAD, per-file hashes, or composite hash) is TBD — see CON-03 in Guidance.md Conflict Table.

**Substantiation note (Lensing item C-001):** The verification approach for REQ-05 ("hash corresponds to input state at run start") cannot be fully specified until the SHA computation method is resolved (CON-03). The three candidate methods have different verification implications:
- **Git HEAD SHA:** verify by comparing recorded SHA to `git rev-parse HEAD` at run start.
- **Per-file content hash:** verify by recomputing hashes of InputFiles and comparing.
- **Composite hash:** verify by recomputing the composite over governed inputs.

Until CON-03 is resolved, REQ-05 verification criteria remain partially TBD.

**Requirement level note (Lensing items F-002, E-003):** InputContextSHA is currently SHOULD. Guidance P5 describes it as "the most architecturally significant field" and DEL-08-07 depends on baseline SHAs for staleness detection. This creates tension between the SHOULD requirement level and the field's architectural criticality. See Conflict Table CON-05 in Guidance.md and cross-matrix conflict XCON-01 for human ruling.

Source: K-VAL-1, K-STALE-1 (CONTRACT); PLAN Section 3.7 (staleness tooling depends on baseline SHAs in run records); `_SEMANTIC_LENSING.md` items C-001, F-002, E-003.

### REQ-06: Compatibility with Existing Tracking

The unified run record MUST NOT replace or break:

- `_STATUS.md` history entries (which record lifecycle state transitions).
- `_DEPENDENCIES.md` Run History section (which records dependency extraction runs).

The unified run record is an **additional** artifact that provides a comprehensive, cross-agent view of all pipeline executions for a deliverable.

Source: SPEC Sections 3, 5; existing file format stability.

### REQ-07: No External Dependencies

Run record persistence MUST NOT require:

- External databases or servers.
- Network access.
- Non-standard tooling beyond what the Chirality desktop app provides.

Source: DIRECTIVE Section 5 (structural constraints); DEC-NET-001 (Anthropic-only outbound).

## Standards

| Standard / Reference | Applicability | Accessible |
|---------------------|---------------|------------|
| `docs/SPEC.md` Section 11 (Snapshot and Pointer Conventions) | Governs immutability semantics for run record storage; note K-SNAP-1 applicability question for append-only model (Lensing item A-002) | Yes |
| `docs/SPEC.md` Section 6 (Dependencies.csv v3.1) | Pattern reference for schema versioning and CSV-based structured data | Yes |
| `docs/CONTRACT.md` K-SNAP-1 | Immutable snapshot invariant — applicability to append-only file semantics is TBD (see REQ-03 enrichment) | Yes |
| `docs/CONTRACT.md` K-VAL-1 | Dirty detection via SHA comparison | Yes |
| `docs/CONTRACT.md` K-STALE-1, K-STALE-2 | Staleness propagation and triage | Yes |
| `docs/CONTRACT.md` K-PROV-1 | Provenance requirements — run records should cite what was consumed; explicit traceability mapping added in REQ-01 enrichment (Lensing item E-002) | Yes |
| `docs/CONTRACT.md` K-INVENT-1 | No invented values | Yes |
| `docs/TYPES.md` Section 4 (Agent Roles) | Defines Type 2 agent classification | Yes |
| `docs/TYPES.md` Section 10 (Epistemic Labels) | Labels for assumptions/proposals in schema design | Yes |

## Verification

| ReqID | Verification Approach | Criteria |
|-------|----------------------|----------|
| REQ-SCOPE-GATE | Process gate | OI-037 resolved to IN before Phase 2/3 execution begins; documented in Conflict Table or `_MEMORY.md` |
| REQ-01 | Schema review + unit test | Schema document exists; all MUST fields are defined; unit tests validate schema parsing; RunStatus lifecycle transitions are documented and testable (Lensing item B-003) |
| REQ-02 | Design review + integration test | Storage location decision documented (CON-01/CON-02 human ruling recorded); run records are written to the chosen location; files are present after a pipeline run; files conform to the chosen format (Markdown table structure or CSV schema); file content is parseable by a schema validator (Lensing item X-004) |
| REQ-03 | Integration test | Existing run records are not modified by subsequent runs; append-only or snapshot behavior confirmed; **crash/interruption scenario:** verify that a partial write (e.g., agent crash mid-write) leaves the file in a recoverable state — either the incomplete entry is detectable and skippable, or a write-ahead/atomic-write strategy prevents corruption (Lensing item X-003) |
| REQ-04 | Integration test | Type 2 agent run produces a run record; run record content matches actual execution metadata per the accuracy criteria defined in REQ-04 (AgentName, InputFiles, OutputFiles, StatusBefore, StatusAfter, RunStatus all verified against actual execution state); failure to write does not fail the run (Lensing item D-003) |
| REQ-05 | Integration test | Run record includes a SHA/hash field; hash corresponds to input state at run start — **verification method depends on SHA computation method (CON-03):** for git HEAD SHA, compare to `git rev-parse HEAD` at run start; for per-file hash, recompute and compare; for composite hash, recompute over governed inputs (Lensing items C-001, X-001) |
| REQ-06 | Regression test | `_STATUS.md` and `_DEPENDENCIES.md` formats are unchanged after run record integration; existing consumers still parse correctly |
| REQ-07 | Design review + test | No network calls, no DB connections, no non-standard tooling required for run record persistence |

## Documentation

### Required Artifacts

| Artifact | Type | Description |
|----------|------|-------------|
| Run Record Schema Reference | DOC | Formal schema definition document (field names, types, enums, versioning rules, RunStatus lifecycle, K-PROV-1 traceability mapping) |
| Run Record Persistence Implementation | CODE | Implementation of run record writing (file I/O, schema serialization, agent protocol hook, post-write validation) |
| Schema Validation Tests | TEST | Unit tests for schema correctness (required fields, enum values, format validation, RunStatus transition validity) |
| Integration Tests | TEST | End-to-end tests for run record emission during Type 2 agent execution, including content accuracy verification and crash/partial-write scenarios |
| Regression Tests | TEST | Tests confirming `_STATUS.md` and `_DEPENDENCIES.md` are unaffected |
| Agent Protocol Update Guide | DOC | Documentation of changes to Type 2 agent protocols for run record emission |
| Schema Evolution Guide | DOC | TBD — governance document for schema version increments, migration path for existing records, and backward compatibility rules (Lensing items D-001, D-002) |
