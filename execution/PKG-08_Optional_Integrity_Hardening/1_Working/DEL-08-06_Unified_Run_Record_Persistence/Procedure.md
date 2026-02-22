# Procedure — DEL-08-06 Unified Pipeline Run Record Persistence

## Purpose

This procedure describes the steps to produce the deliverable artifacts for DEL-08-06 (Unified Pipeline Run Record Persistence): a schema definition document, a persistence implementation, and a test suite. It also describes the operational procedure for how run records will be used once implemented.

## Prerequisites

| # | Prerequisite | Status | Source |
|---|-------------|--------|--------|
| 1 | SOW-037 scope decision resolved (OI-037 flipped to IN) | TBD | Decomposition Open Issues |
| 2 | `docs/SPEC.md` Section 11 (Snapshot and Pointer Conventions) accessible and current | Available | SPEC.md |
| 3 | `docs/CONTRACT.md` invariant catalog (K-SNAP-1, K-VAL-1, K-STALE-1) accessible | Available | CONTRACT.md |
| 4 | `docs/SPEC.md` Section 6 (Dependencies.csv v3.1) accessible — pattern reference for schema design | Available | SPEC.md |
| 5 | Current Type 2 agent instruction files accessible — for protocol integration design | TBD — agent files in `agents/` or `.claude/agents/` | Agent instruction suite |
| 6 | DEL-08-04 (Dependency Graph Generator) status known — informs whether graph-level SHA computation is available | TBD — depends on OI-035 scope decision | Decomposition |
| 7 | DEL-08-05 (Lock Mechanism) status known — informs whether concurrent execution protection exists | TBD — depends on OI-036 scope decision | Decomposition |

## Steps

### Phase 1: Schema Design (DOC)

#### Step 1.1 — Review Existing Run Tracking Mechanisms

1. Read `_STATUS.md` history format (SPEC Section 3.1) and document what it currently captures.
2. Read `_DEPENDENCIES.md` Run History format (SPEC Section 5.2) and document what it currently captures.
3. Identify the gaps between existing tracking and the unified run record requirements (REQ-01 in Specification).
4. Document the gap analysis in the schema reference document.

**Output:** Gap analysis section in schema reference document.

#### Step 1.2 — Define Run Record Schema

1. Draft the unified run record schema based on REQ-01 field definitions.
2. For each field, specify:
   - Field name, data type, required/optional status.
   - Allowed values (for enum fields).
   - Default value (if applicable).
   - Source/justification.
3. Define the schema version identifier (`v1.0`).
4. Define the RunID format and uniqueness rules.
5. Document the RunStatus lifecycle transitions (valid statuses, trigger conditions, boundary between PARTIAL and FAILED) per the RunStatus Lifecycle definition in Specification REQ-01 (Lensing item B-003).

**Output:** Run Record Schema Reference document (DOC artifact).

#### Step 1.3 — Resolve Storage Location

1. Present the storage location options (REQ-02) with trade-off analysis (Guidance C1).
2. Obtain human ruling on CON-01 (storage location) and CON-02 (file format).
3. Document the chosen location and format in the schema reference.
4. Standardize the run record artifact filename across all documents per Guidance Terminology Note (Lensing item C-002).

**Output:** Storage location and format decision documented.

#### Step 1.4 — Resolve SHA Computation Method

1. Present the SHA computation options (REQ-05) with trade-off analysis (Guidance CON-03).
2. Consider:
   - Git HEAD SHA: simple, captures the state of the entire repo at run start.
   - Per-file content hash: precise, captures exactly what the agent consumed.
   - Composite hash: hash of specific governed input files listed in `_REFERENCES.md` and the deliverable folder.
3. Obtain human ruling on CON-03.
4. Document the chosen method in the schema reference.
5. Update REQ-05 verification criteria to reflect the chosen method (Lensing item C-001).

**Output:** SHA computation method documented.

### Phase 1.5: Prerequisite Gate (Lensing item F-003)

Before proceeding to Phase 2, verify that all Phase 1 design decisions and scope prerequisites have been resolved:

| Gate Check | Condition | Resolution Required |
|------------|-----------|-------------------|
| G1 | OI-037 (SOW-037 scope decision) resolved to IN | Prerequisite #1; REQ-SCOPE-GATE in Specification |
| G2 | CON-01 (storage location) human ruling recorded | Step 1.3 output |
| G3 | CON-02 (file format) human ruling recorded | Step 1.3 output |
| G4 | CON-03 (SHA computation method) human ruling recorded | Step 1.4 output |
| G5 | CON-05 (InputContextSHA MUST vs. SHOULD) human ruling recorded or documented rationale for SHOULD | Specification REQ-01; Guidance CON-05 |
| G6 | CON-06 (K-SNAP-1 applicability to append-only) resolved or accepted as semantic extension | Specification REQ-03; Guidance CON-06 |

**Action:** Review the Conflict Table in Guidance.md. For each gate check, confirm the human ruling is recorded. If any gate is unresolved, do not proceed to Phase 2 — escalate to the human for resolution.

**Rationale (Lensing item F-003):** The Prerequisites table lists several items as TBD, but no procedural step previously enforced checking these gates before implementation. This gate step ensures design decisions are locked before code is written.

**Output:** Gate check log documenting resolution status of each item.

### Phase 2: Implementation (CODE)

#### Step 2.1 — Implement Run Record Writer

1. Implement a run record writing function/module that:
   - Accepts the schema fields as input.
   - Serializes the record in the chosen format (Markdown table or CSV row).
   - Appends the record to the chosen storage location (deliverable-local file or tool-root snapshot).
   - Respects immutability (append-only; no modification of existing records).
2. Handle edge cases:
   - First run (file does not exist — create with header).
   - Concurrent writes: if DEL-08-05 (Lock Mechanism) is in scope and available, use the lock protocol to serialize writes. If DEL-08-05 is not in scope or not yet available, implement a fallback strategy — **PROPOSAL:** use atomic file write (write to temp file, then rename/append) to minimize corruption risk from concurrent access. Document the concurrency limitation and the conditions under which it could produce duplicate or interleaved entries (Lensing item A-003).
   - Write failure (log warning; do not fail the agent run — see Guidance C7 for rationale and risk mitigation).
   - Crash/interruption mid-write: ensure partial writes are detectable — **PROPOSAL:** use a sentinel marker (e.g., a closing delimiter per entry) so that an incomplete entry can be identified during read-back. Alternatively, use atomic write (write complete entry to temp, then append) so partial writes never reach the main file (Lensing item X-003).

**Output:** Run record writer implementation (CODE artifact).

#### Step 2.1.1 — Implement Post-Write Validation (Lensing item X-005)

After each run record is written, perform a validation step:

1. Read back the last written entry from the run record file.
2. Parse it against the schema definition (all MUST fields present, enum values valid, RunID format correct, SchemaVersion matches expected version).
3. If validation fails:
   - Log a warning (do not fail the agent run, consistent with REQ-04).
   - Record the validation failure in the `Notes` field of the run record (if possible) or in ORCHESTRATOR's run summary.
4. If validation succeeds: proceed to report completion.

**Rationale:** Testing covers schema validation, but the operational procedure should include a runtime check to catch issues that testing might not cover (e.g., encoding errors, filesystem-specific formatting issues).

**Output:** Post-write validation logic (CODE artifact).

#### Step 2.2 — Implement SHA Computation

1. Implement the baseline SHA computation method chosen in Step 1.4.
2. Ensure the computation is deterministic and reproducible.
3. Document the computation algorithm.

**Output:** SHA computation implementation (CODE artifact).

#### Step 2.3 — Define Agent Protocol Hook

1. Define a standard protocol step for Type 2 agents to emit a run record.
2. The step should be:
   - Positioned as the last step before reporting completion to ORCHESTRATOR.
   - Non-blocking (failure to write does not fail the run).
   - Parameterized (agent provides its run metadata; the hook handles serialization and persistence).
3. Document the hook interface for agent protocol integration.

**Output:** Agent protocol hook specification and implementation (CODE + DOC artifacts).

#### Step 2.4 — Integrate with Type 2 Agent Protocols

1. For each Type 2 agent (4_DOCUMENTS, DEPENDENCIES, CHIRALITY_FRAMEWORK, CHIRALITY_LENS, and others as identified in the current agent inventory):
   - Add the run record emission step to the agent's protocol.
   - Ensure the step captures accurate metadata (agent name, input files, output files, status transitions) per the accuracy criteria in Specification REQ-04 (Lensing item D-003).
2. Test each integration individually (see Phase 3).

**Output:** Updated agent protocol instructions (DOC artifact); integration code (CODE artifact).

### Phase 3: Testing (TEST)

#### Step 3.1 — Schema Validation Tests

1. Write unit tests that validate:
   - All MUST fields are present in a sample run record.
   - Enum fields contain only valid values (including RunStatus lifecycle values: SUCCESS, PARTIAL, FAILED, SKIPPED).
   - RunID format matches the defined pattern.
   - SchemaVersion is present and correct.
   - Timestamps are valid ISO 8601.
   - RunStatus values conform to the lifecycle definition (Lensing item B-003).
2. Write negative tests for:
   - Missing required fields.
   - Invalid enum values.
   - Malformed RunID or timestamp.
   - Invalid RunStatus values (e.g., values not in the defined enum).

**Output:** Schema validation test suite (TEST artifact).

#### Step 3.2 — Integration Tests

1. Write tests that simulate a Type 2 agent execution and verify:
   - A run record is written to the correct location.
   - The run record content matches the execution metadata (per REQ-04 accuracy criteria — AgentName, InputFiles, OutputFiles, StatusBefore, StatusAfter, RunStatus all verified; Lensing item D-003).
   - The SHA field is populated and corresponds to the input state (verification method per chosen SHA computation method; Lensing item X-001).
   - Subsequent runs append without modifying previous records.
   - Post-write validation succeeds for well-formed records (Lensing item X-005).
2. Write failure-mode tests:
   - Run record write failure does not fail the agent run.
   - Concurrent run record writes produce valid, non-corrupted files (if lock mechanism is available).
   - **Crash/interruption scenario (Lensing item X-003):** simulate agent crash mid-write and verify that (a) the run record file is not corrupted, (b) the incomplete entry is detectable (sentinel marker missing or temp file remains), and (c) subsequent runs can write successfully despite the partial entry.

**Output:** Integration test suite (TEST artifact).

#### Step 3.3 — Regression Tests

1. Write tests confirming that:
   - `_STATUS.md` format is unchanged after run record integration.
   - `_DEPENDENCIES.md` format is unchanged after run record integration.
   - Existing consumers of these files parse correctly after the change.
2. Run against example execution roots (`examples/`).

**Output:** Regression test suite (TEST artifact).

#### Step 3.4 — Conformance Tests

1. Write tests confirming:
   - Run records respect immutability (per the chosen storage model — K-SNAP-1 for snapshots, entry-level immutability for append-only; see CON-06 in Guidance) — existing records are not modified.
   - Run records are plain-file, git-trackable artifacts (DIRECTIVE constraints).
   - No network calls or external dependencies are required (REQ-07).
   - K-PROV-1 coverage: run records contain the fields mapped in the K-PROV-1 Traceability table (Specification REQ-01 enrichment; Lensing item E-002).

**Output:** Conformance test suite (TEST artifact).

### Phase 4: Schema Evolution (Ongoing — Lensing item D-002)

This phase is not part of the initial implementation but documents the operational procedure for when the run record schema evolves.

#### Step 4.1 — Schema Change Assessment

1. Determine the nature of the schema change:
   - **Additive (new optional field):** Does not require a version bump. Add the field definition to the schema reference. Existing records remain valid.
   - **Breaking (field removal, type change, semantic change to existing field):** Requires a SchemaVersion increment.
2. Document the change rationale and impact assessment.

#### Step 4.2 — Version Increment (if breaking change)

1. Increment SchemaVersion (e.g., `v1.0` to `v2.0`).
2. Update the schema reference document with the new version.
3. Existing records are NOT modified (P4: Immutability After Write).
4. Update the run record reader to support parsing all historical schema versions.
5. Update schema validation tests for the new version.

#### Step 4.3 — Migration Documentation

1. Document the migration path: what changed, why, and how readers should handle old-version records.
2. Update the Schema Evolution Guide (Specification Documentation section).

**Output:** Updated schema reference; updated reader; updated tests; migration documentation.

**TBD:** Formal governance rules for triggering and approving schema changes (see Guidance C6).

## Verification

| Step | Verification Check | Pass Criteria |
|------|-------------------|---------------|
| 1.2 | Schema review | Schema reference document exists; all MUST fields defined; RunStatus lifecycle documented; reviewed by human |
| 1.3 | Design review | Storage location decision documented; human ruling recorded for CON-01 and CON-02 |
| 1.4 | Design review | SHA method decision documented; human ruling recorded for CON-03 |
| 1.5 | Gate check | All gate conditions (G1-G6) resolved or explicitly accepted; gate check log produced |
| 2.1 | Code review + unit test | Writer function produces valid records; append-only behavior confirmed; concurrent write handling documented; crash recovery strategy implemented |
| 2.1.1 | Code review + unit test | Post-write validation logic correctly identifies well-formed and malformed records |
| 2.2 | Code review + unit test | SHA computation is deterministic and reproducible |
| 2.3 | Code review | Hook interface is documented; non-blocking behavior confirmed |
| 2.4 | Integration test | Each Type 2 agent emits a valid run record with accurate metadata |
| 3.1 | Test execution | All schema validation tests pass (including RunStatus lifecycle tests) |
| 3.2 | Test execution | All integration tests pass (including content accuracy, crash/interruption scenario, and post-write validation) |
| 3.3 | Test execution | All regression tests pass — existing formats unaffected |
| 3.4 | Test execution | All conformance tests pass — immutability, plain-file, no network, K-PROV-1 coverage |

## Records

| Record | Description | Location |
|--------|-------------|----------|
| Run Record Schema Reference | Formal schema definition (v1.0), including RunStatus lifecycle and K-PROV-1 traceability mapping | `{DEL_FOLDER}/` — TBD filename |
| Storage Location Decision | Human ruling on CON-01, CON-02, CON-03, CON-05, CON-06 | `{DEL_FOLDER}/Guidance.md` Conflict Table + `{DEL_FOLDER}/_MEMORY.md` |
| Prerequisite Gate Log | Resolution status of gate checks G1-G6 before Phase 2 | `{DEL_FOLDER}/_MEMORY.md` |
| Run Record Writer Implementation | Source code for run record persistence (including post-write validation and crash recovery) | TBD — likely `frontend/` or `_Scripts/` depending on implementation language |
| Agent Protocol Updates | Updated Type 2 agent instruction files | `agents/` or `.claude/agents/` |
| Test Suites | Schema, integration, regression, and conformance tests | TBD — likely `frontend/scripts/` or `_Scripts/` |
| Schema Evolution Guide | Governance document for schema version management | `{DEL_FOLDER}/` — TBD (Lensing items D-001, D-002) |
| Run Records (operational) | Actual run records produced during pipeline executions | TBD — per storage location decision (REQ-02) |
