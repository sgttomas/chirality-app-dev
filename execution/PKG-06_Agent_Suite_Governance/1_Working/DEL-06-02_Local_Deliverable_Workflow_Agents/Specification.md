# Specification — DEL-06-02 Local Deliverable Workflow Agents

## Scope

### What This Deliverable Covers

This deliverable ensures that the local deliverable workflow agents -- PREPARATION, 4_DOCUMENTS, CHIRALITY_FRAMEWORK, and CHIRALITY_LENS -- collectively support the full local deliverable lifecycle from scaffolding through production document set drafting through optional semantic analysis, producing all required artifacts per `docs/SPEC.md` Section 2.

Specifically, this deliverable covers:

- **SOW-017:** Workspace scaffolding and production document set drafting via the agent framework (PREPARATION + 4_DOCUMENTS).
- **SOW-019:** Optional semantic analysis artifacts (`_SEMANTIC.md` and `_SEMANTIC_LENSING.md`).

### What This Deliverable Excludes

- Cross-deliverable workflows (covered by DEL-06-03).
- Agent instruction structural conformance to HELPS_HUMANS (covered by DEL-06-01).
- Change management and git hygiene support (covered by DEL-06-04).
- Governance coherence and guardrails (covered by DEL-06-05).
- Dependency extraction mechanics (covered by DEL-05-04 for file contract; DEPENDENCIES agent for extraction logic).
- Lifecycle transitions beyond `SEMANTIC_READY` (human-driven or WORKING_ITEMS-driven).

## Requirements

### REQ-01: PREPARATION Produces Complete Minimum Viable Fileset

PREPARATION (Task Type C) must produce all five required metadata files for each deliverable folder.

**Required files** (source: `docs/SPEC.md` Section 2.1, minimum viable fileset definition):
1. `_STATUS.md` -- initialized to `OPEN`
2. `_CONTEXT.md` -- header fields match decomposition exactly
3. `_DEPENDENCIES.md` -- hybrid container with human-owned and agent-owned sections
4. `_REFERENCES.md` -- source document pointers
5. `_SEMANTIC.md` -- placeholder stub (to be overwritten by CHIRALITY_FRAMEWORK)

> **Note (lensing items B-001, X-002):** `MEMORY.md` (no leading underscore) is listed in `docs/SPEC.md` Section 2.1 with SHOULD presence (not MUST). It is not part of the minimum viable fileset. `_MEMORY.md` is disabled in this project profile (`MUST NOT`). `AGENT_PREPARATION.md` Task C Steps 1-6 do not include `MEMORY.md` creation.

**Verification:** After PREPARATION Task C, all five MUST-presence files exist. `_CONTEXT.md` fields match decomposition entry. `_STATUS.md` state is `OPEN`.

### REQ-02: PREPARATION Is Idempotent

PREPARATION must never overwrite existing files. If a target file or folder already exists, PREPARATION skips it and reports the skip.

**Source:** `AGENT_PREPARATION.md` invariant: "Idempotent. If a target file/folder already exists, do not modify it; skip and report."

**Verification:** Running PREPARATION twice on the same deliverable produces identical filesystem state. No existing file content is modified.

### REQ-03: PREPARATION Creates No Engineering Content

PREPARATION is structural only. It must not write Datasheet, Specification, Guidance, or Procedure content. It must not infer dependency edges, scope relationships, or engineering values.

**Source:** `AGENT_PREPARATION.md` invariant: "No engineering content. Do not write Datasheet/Specification/Guidance/Procedure content."

**Verification:** After PREPARATION, no `Datasheet.md`, `Specification.md`, `Guidance.md`, or `Procedure.md` exists in the deliverable folder.

### REQ-04: 4_DOCUMENTS Produces All Four Documents

4_DOCUMENTS must produce `Datasheet.md`, `Specification.md`, `Guidance.md`, and `Procedure.md` after a successful run (for the requested pass set).

**Source:** `AGENT_4_DOCUMENTS.md` invariant: "All four documents, always."

**Verification:** After 4_DOCUMENTS run, all four files exist and contain the default schema sections.

### REQ-05: 4_DOCUMENTS Default Schema Sections Are Stable

Each document retains the default schema headings defined in the 4_DOCUMENTS agent instructions. Additional sections may be added, but defaults must not be removed.

| Document | Default Sections |
|----------|-----------------|
| Datasheet | Identification, Attributes, Conditions, Construction, References |
| Specification | Scope, Requirements, Standards, Verification, Documentation |
| Guidance | Purpose, Principles, Considerations, Trade-offs, Examples |
| Procedure | Purpose, Prerequisites, Steps, Verification, Records |

**Source:** `AGENT_4_DOCUMENTS.md` Step 2; invariant: "Stable interface."

**Verification:** Each document contains all default section headings.

### REQ-06: 4_DOCUMENTS Respects Overwrite Protection

4_DOCUMENTS must check `_STATUS.md` before writing. If `Current State` is not in `ALLOW_OVERWRITE_STATES`, it must not overwrite the four documents and must report `SKIPPED_PROTECT_HUMAN_WORK`.

**Source:** `AGENT_4_DOCUMENTS.md` Step 0; invariant: "Respect human work."

> **Clarification (lensing item A-002):** `ALLOW_OVERWRITE_STATES` is a runtime parameter provided by ORCHESTRATOR at invocation time, not a fixed set. The default value defined in `AGENT_4_DOCUMENTS.md` Runtime parameters table is `OPEN, INITIALIZED, SEMANTIC_READY`. ORCHESTRATOR may override this default when spawning 4_DOCUMENTS. The verification scenario below uses the default value.

**Verification:** Given a deliverable with `_STATUS.md` state `IN_PROGRESS` and `ALLOW_OVERWRITE_STATES` at its default value of `OPEN, INITIALIZED, SEMANTIC_READY`, 4_DOCUMENTS returns `SKIPPED_PROTECT_HUMAN_WORK` without modifying files.

### REQ-07: Source Fidelity and TBD Discipline

All four agents must follow the epistemic integrity rules:
- Unknown values become `TBD`, not guessed (source: `K-INVENT-1`).
- Inferred content is labeled **ASSUMPTION** (source: `docs/TYPES.md` Section 10).
- Non-trivial values cite sources; if exact location is unknown, cite source with `location TBD` (source: `AGENT_4_DOCUMENTS.md` invariants).

**Verification:** Audit of generated documents using an exhaustive scan of all non-trivial assertions finds no unsourced assertions that are not labeled ASSUMPTION or TBD. The audit method is a full-text review of all four production documents (not a spot check), examining each factual claim for either (a) an explicit source citation, (b) an ASSUMPTION label, or (c) a TBD marker.

> **Strengthened (lensing item C-001):** The verification approach now specifies "exhaustive scan" rather than an unqualified "audit" to remove ambiguity about audit scope and make the pass/fail determination repeatable.

### REQ-08: Conflict Surfacing

When 4_DOCUMENTS detects contradictions between sources during cross-reference consistency checking (Pass 2), it must surface them in a Conflict Table in `Guidance.md` rather than silently resolving them.

**Source:** `AGENT_4_DOCUMENTS.md` Step 5; `K-CONFLICT-1`.

**Verification:** If contradictions exist, `Guidance.md` contains a `## Conflict Table (for human ruling)` section.

### REQ-09: Cross-Document Consistency (Pass 2)

4_DOCUMENTS must perform cross-reference consistency checking:
- Datasheet attributes reflected in Specification requirements where appropriate.
- Specification requirements have rationale in Guidance where appropriate.
- Specification requirements have verification hooks in Procedure.
- Terminology and numeric values are consistent across all four documents.

**Source:** `AGENT_4_DOCUMENTS.md` Step 5.

**Verification:** Post-Pass-2, a cross-document comparison covering (a) terminology alignment, (b) numeric value consistency, (c) entity name consistency, and (d) requirement-to-procedure traceability confirms that no inconsistencies remain that are not captured in the Conflict Table. The comparison dimensions are the four check types listed in `AGENT_4_DOCUMENTS.md` Step 5: Datasheet-Specification, Specification-Guidance, Specification-Procedure, and Terminology/Values.

> **Strengthened (lensing item X-003):** The verification now specifies the four comparison dimensions to make the sufficiency of the cross-document comparison deterministic.

### REQ-10: Status Transition Safety

Each agent must follow safe `_STATUS.md` transition rules:
- PREPARATION: sets `OPEN` only on creation.
- 4_DOCUMENTS: advances `OPEN -> INITIALIZED` only (never regresses).
- CHIRALITY_FRAMEWORK: advances `INITIALIZED -> SEMANTIC_READY` only (never regresses).
- CHIRALITY_LENS: does not modify `_STATUS.md`.

No agent may regress the state. If the current state does not match the expected "from" state, the agent must not modify `_STATUS.md`.

**Source:** `docs/SPEC.md` Section 3.3; `K-STATUS-1`; `AGENT_CHIRALITY_LENS.md` write scope (lensing item C-002).

**Verification:** After pipeline run, `_STATUS.md` history shows only forward transitions with correct actor attribution. CHIRALITY_LENS run produces no changes to `_STATUS.md`.

### REQ-11: CHIRALITY_FRAMEWORK Produces Valid Semantic Matrices

CHIRALITY_FRAMEWORK must overwrite the `_SEMANTIC.md` placeholder with populated semantic matrices (A, B, C, F, D, X, E) conditioned by the deliverable perspective.

**Source:** `AGENT_CHIRALITY_FRAMEWORK.md` invariants.

**Verification:** `_SEMANTIC.md` status changes from `PLACEHOLDER` to populated with matrix content.

### REQ-12: CHIRALITY_LENS Produces Lensing Register Without Editing Production Documents

CHIRALITY_LENS must produce `_SEMANTIC_LENSING.md` as a structured extraction register. It must not edit `Datasheet.md`, `Specification.md`, `Guidance.md`, or `Procedure.md`.

**Source:** `AGENT_CHIRALITY_LENS.md` invariants: "Read-only on production documents."

**Verification:** After CHIRALITY_LENS run, `_SEMANTIC_LENSING.md` exists. Production document modification timestamps are unchanged.

### REQ-13: 4_DOCUMENTS Pass 3 Enrichment Uses Lensing as Worklist

When 4_DOCUMENTS runs Pass 3 (`P3_ONLY`), it must treat `_SEMANTIC_LENSING.md` rows as candidate improvements, incorporating only items with citeable underlying sources. Items without sufficient evidence must become `TBD` or Conflict Table entries.

**Source:** `AGENT_4_DOCUMENTS.md` Step 6.

**Verification:** Post-Pass-3 documents contain only enrichments traceable to sources via lensing register, or new TBD/Conflict Table entries.

### REQ-14: Write Scope Enforcement

Each agent must write only within its declared write scope:
- PREPARATION: `workspace-scaffold-only`
- 4_DOCUMENTS: `deliverable-local` (four production documents + `_STATUS.md` safe update)
- CHIRALITY_FRAMEWORK: `deliverable-local` (`_SEMANTIC.md` + `_STATUS.md` safe update)
- CHIRALITY_LENS: `deliverable-local` (`_SEMANTIC_LENSING.md` only)

No agent writes outside its declared zone.

**Source:** `K-WRITE-1`; individual agent headers.

**Verification:** Diff review after each agent run shows writes only within declared scope.

### REQ-15: Metadata File Integrity

4_DOCUMENTS, CHIRALITY_FRAMEWORK, and CHIRALITY_LENS must not modify metadata files created by PREPARATION (`_CONTEXT.md`, `_DEPENDENCIES.md`, `_REFERENCES.md`) except for safe `_STATUS.md` updates.

**Source:** `AGENT_4_DOCUMENTS.md` invariants; `AGENT_CHIRALITY_FRAMEWORK.md` write scope.

**Verification:** After pipeline run, `_CONTEXT.md`, `_DEPENDENCIES.md`, and `_REFERENCES.md` are unchanged from PREPARATION output.

### REQ-16: Pipeline Run Observability

The local workflow pipeline MUST expose run observability at dispatch/completion status level for PREPARATION, 4_DOCUMENTS, CHIRALITY_FRAMEWORK, and CHIRALITY_LENS invocations.

Required observability contract:
- Each run is dispatch-tracked by ORCHESTRATOR/WORKING_ITEMS control flow.
- Each run emits a completion outcome:
  - PREPARATION: completion report
  - 4_DOCUMENTS: `RUN_STATUS` (`COMPLETE`, `SKIPPED_PROTECT_HUMAN_WORK`, `FAILED_INPUTS`, `UNSUPPORTED_VARIANT`, etc.)
  - CHIRALITY_FRAMEWORK: completion report with PASS/FAIL audit result
  - CHIRALITY_LENS: completion report to invoker
- Tier control-loop reporting aggregates completion status summaries for touched deliverables.

Timing SLAs, token budgets, and timeout thresholds are out of scope and remain governance-optional.

**Source:** `agents/AGENT_PREPARATION.md` (report completion), `agents/AGENT_4_DOCUMENTS.md` (`RUN_STATUS` contract), `agents/AGENT_CHIRALITY_FRAMEWORK.md` (Step 7 completion report), `agents/AGENT_CHIRALITY_LENS.md` (Step 5 completion report), `agents/AGENT_ORCHESTRATOR.md` (collect/report per-deliverable run statuses), `execution/_Coordination/NEXT_INSTANCE_PROMPT.md` (TaskCreate/TaskUpdate tracking model).

**Verification:** Confirm agent instruction contracts include completion reporting, and confirm control-loop reports record per-pass run outcomes/status summaries for touched deliverables.

## Standards

| Standard/Reference | Applicability | Accessible |
|--------------------|--------------|------------|
| `docs/SPEC.md` | Canonical file formats, folder layout, lifecycle states, MUST/SHOULD/MAY file presence | Yes |
| `docs/CONTRACT.md` | Binding invariants K-* | Yes |
| `docs/TYPES.md` | Canonical vocabulary, agent roles, lifecycle definitions | Yes |
| `docs/DIRECTIVE.md` | Founding intent, scope boundaries, professional responsibility | Yes |
| `agents/AGENT_HELPS_HUMANS.md` | Agent instruction structural standard | Yes |

## Verification

| Requirement | Verification Approach |
|-------------|----------------------|
| REQ-01 | Folder inspection: five MUST-presence files present; `_CONTEXT.md` field comparison |
| REQ-02 | Re-run PREPARATION; diff shows no changes |
| REQ-03 | Absence check: no production document files after PREPARATION |
| REQ-04 | File existence check after 4_DOCUMENTS |
| REQ-05 | Heading grep against default schema |
| REQ-06 | State-based test: set state to IN_PROGRESS, run 4_DOCUMENTS with default ALLOW_OVERWRITE_STATES, confirm skip |
| REQ-07 | Exhaustive full-text audit: search for unsourced assertions |
| REQ-08 | Presence of Conflict Table when contradictions exist |
| REQ-09 | Cross-document comparison on four dimensions: terminology, values, entity names, requirement-procedure traceability |
| REQ-10 | `_STATUS.md` history review; confirm CHIRALITY_LENS does not modify status |
| REQ-11 | `_SEMANTIC.md` content inspection |
| REQ-12 | File existence + timestamp check |
| REQ-13 | Post-Pass-3 provenance audit |
| REQ-14 | Diff review per agent run |
| REQ-15 | Metadata file hash comparison pre/post pipeline |
| REQ-16 | Instruction-contract audit + control-loop evidence review: completion-status reporting is present for all four agents and aggregated in control-loop artifacts |

## Documentation

### Required Artifacts

Per `_CONTEXT.md`, anticipated artifacts for this deliverable are **DOC**.

The following documentation artifacts are required:

| Artifact | Description |
|----------|-------------|
| This Specification (`Specification.md`) | Requirements for local deliverable workflow agent behavior |
| `Datasheet.md` | Structured attributes of the agent pipeline |
| `Guidance.md` | Design rationale and trade-off analysis |
| `Procedure.md` | Operational procedure for validating or updating the agent pipeline |
| Agent instruction files (existing) | `AGENT_PREPARATION.md`, `AGENT_4_DOCUMENTS.md`, `AGENT_CHIRALITY_FRAMEWORK.md`, `AGENT_CHIRALITY_LENS.md` |

> **Note (lensing item E-001):** The acceptance criteria for this deliverable's own DOC output (the production document set describing the pipeline) are governed by the general deliverable lifecycle: the document set is considered sufficient when all requirements (REQ-01 through REQ-16) are assessable from the documentation and the Procedure gap report can be compiled. Formal acceptance is a human decision at the `CHECKING -> ISSUED` transition. See Conflict Table CT-002 in Guidance.md for the aggregate acceptance gate question and `CT-002_Acceptance_Gate_Decision_Input_2026-02-23.md` for current decision options/recommendation.

### Traceability

| Scope Item | Requirement(s) |
|-----------|----------------|
| SOW-017 | REQ-01, REQ-02, REQ-03, REQ-04, REQ-05, REQ-06, REQ-07, REQ-08, REQ-09, REQ-10 |
| SOW-019 | REQ-11, REQ-12, REQ-13 |
| Both | REQ-14, REQ-15, REQ-16 |
