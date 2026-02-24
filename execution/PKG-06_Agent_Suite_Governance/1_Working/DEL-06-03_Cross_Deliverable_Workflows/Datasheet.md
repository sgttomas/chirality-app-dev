# Datasheet -- DEL-06-03 Cross-Deliverable Workflow Support

## Identification

| Field | Value |
|-------|-------|
| **DeliverableID** | DEL-06-03 |
| **Name** | Cross-deliverable Workflow Support (Aggregation/Reconciliation/Estimating/Scheduling) |
| **PackageID** | PKG-06 |
| **Package** | Agent Suite & Governance |
| **Type** | DOC_UPDATE |
| **ContextEnvelope** | M |
| **ResponsibleParty** | TBD |
| **Scope Coverage** | SOW-020 |
| **Objectives** | OBJ-004, OBJ-006 (confirmed in decomposition DEL-06-03 row) |
| **Anticipated Artifacts** | DOC |

## Issuance Hygiene (2026-02-24)

- Lifecycle state is `ISSUED`.
- Open R-003 (`_Schedule/` tool-root formalization in SPEC) remains human-owned governance follow-up and is non-blocking for issued status.
- Legacy assumption/TBD wording in this deliverable set is non-blocking unless explicitly reclassified by a human ruling.

## Attributes

### Cross-Deliverable Workflow Agents in Scope

| Agent | AGENT_TYPE | AGENT_CLASS | WRITE_SCOPE | Tool Root | Instruction File |
|-------|-----------|-------------|-------------|-----------|-----------------|
| AGGREGATION | TYPE 2 | TASK | tool-root-only | `{EXECUTION_ROOT}/_Aggregation/` | `agents/AGENT_AGGREGATION.md` |
| RECONCILIATION | TYPE 1 | PERSONA | tool-root logs only | `{EXECUTION_ROOT}/_Reconciliation/` | `agents/AGENT_RECONCILIATION.md` |
| ESTIMATING | TYPE 2 | TASK | tool-root-only | `{EXECUTION_ROOT}/_Estimates/` | `agents/AGENT_ESTIMATING.md` |
| SCHEDULING | TYPE 1 | PERSONA | tool-root-only | `{EXECUTION_ROOT}/_Schedule/` | `.claude/agents/SCHEDULING.md` |

Source: decomposition DEL-06-03 entry; agent instruction files enumerated above.

> **Naming note (Lensing E-002):** SCHEDULING's instruction file is named `SCHEDULING.md` (without the `AGENT_` prefix), diverging from the `AGENT_{NAME}.md` pattern used by the other three agents. This reflects the actual filename at `.claude/agents/SCHEDULING.md`. The inconsistency is noted here as a known divergence; assessors should use the paths listed above as canonical. (Source: `.claude/agents/SCHEDULING.md` filename; `agents/AGENT_AGGREGATION.md`, `agents/AGENT_RECONCILIATION.md`, `agents/AGENT_ESTIMATING.md` filenames.)

### Invocation Model

| Agent | Invocation Surface | Triggering Mechanism | Human-Triggered |
|-------|-------------------|---------------------|-----------------|
| AGGREGATION | INIT-TASK | Type 1 agent brief or human brief | Yes (Source: `AGENT_AGGREGATION.md` -- INTERACTION_SURFACE: INIT-TASK) |
| RECONCILIATION | chat | Direct human conversation | Yes (Source: `AGENT_RECONCILIATION.md` -- INTERACTION_SURFACE: chat) |
| ESTIMATING | INIT-TASK | Type 1 agent brief | Yes (Source: `AGENT_ESTIMATING.md` -- INTERACTION_SURFACE: INIT-TASK) |
| SCHEDULING | chat | Direct human conversation | Yes (Source: `SCHEDULING.md` -- INTERACTION_SURFACE: chat) |

### Snapshot Output Model

| Agent | Snapshot Folder Pattern | Pointer File | Immutability |
|-------|------------------------|-------------|-------------|
| AGGREGATION | `_Aggregation/AGG_{PURPOSE}_{YYYY-MM-DD}_{HHMM}/` | `_Aggregation/_LATEST.md` | Snapshots immutable; pointer mutable (Source: `AGENT_AGGREGATION.md` non-negotiable invariants) |
| RECONCILIATION | `_Reconciliation/Reconciliation_Run_Summary_{RunID}.md` | `_Reconciliation/_LATEST.md` | Run summaries preserved; pointer mutable (Source: `AGENT_RECONCILIATION.md` Step 6) |
| ESTIMATING | `_Estimates/EST_{OUTPUT_LABEL}_{YYYY-MM-DD}_{HHMM}/` | `_Estimates/_LATEST.md` (conditional) | Snapshots immutable; pointer mutable only when UPDATE_LATEST_POINTER=TRUE (Source: `AGENT_ESTIMATING.md` non-negotiable invariants) |
| SCHEDULING | `_Schedule/SCHEDULE_{BASIS}_{YYYY-MM-DD}_{sequence}/` | `_Schedule/_LATEST.md` | Snapshots immutable; pointer mutable after human confirmation at Gate 5 (Source: `SCHEDULING.md` Gate 5) |

> **Design rationale for RECONCILIATION's non-snapshot model (Lensing D-002):** RECONCILIATION uses run summary files rather than timestamped snapshot folders because it is a Type 1 persona agent that operates within a conversational cycle. Its primary outputs are diagnostic (identifying dependency conflicts, coherence issues, and recommended actions) rather than archival. The run summary model preserves the audit trail while reflecting the conversational nature of the interaction -- each summary documents a single reconciliation cycle's findings and dispatches. By contrast, AGGREGATION, ESTIMATING, and SCHEDULING produce structured data artifacts (rollups, cost tables, Gantt charts) where folder-level immutability provides stronger guarantees of artifact integrity across reruns. (Source: `AGENT_RECONCILIATION.md` Output Persistence section; **ASSUMPTION** -- rationale inferred from agent type classification and output model differences.)

## Conditions

### Opt-In and Human-Trigger Requirements

Cross-deliverable workflows MUST be opt-in and human-triggered per SOW-020 and DIRECTIVE Section 2.3 (Human Authority at Every Gate).

| Condition | Status | Evidence |
|-----------|--------|----------|
| No cross-deliverable workflow runs automatically on commit/push | Verified (Source: 2026-02-24 conformance assessment scan across `AGENT_AGGREGATION.md`, `AGENT_RECONCILIATION.md`, `AGENT_ESTIMATING.md`, `.claude/agents/SCHEDULING.md`; no automatic trigger pathways declared) |
| Each workflow requires an explicit human brief or conversation initiation | Verified (Source: each agent's INTERACTION_SURFACE is either `chat` or `INIT-TASK`, both requiring human or human-directed initiation) |
| RECONCILIATION uses no-autopilot rule (at most one Type 2 dispatch per cycle) | Verified (Source: `AGENT_RECONCILIATION.md` -- No-autopilot rule) |
| SCHEDULING uses 5-gate model with human confirmation at each gate | Verified (Source: `SCHEDULING.md` -- Gate Model) |

### Assumption Resolution Tracking (Lensing B-001)

The following assumptions are recorded in this deliverable. Each requires confirmation or resolution before the conformance assessment can be considered complete.

| Assumption ID | Location | Statement | Resolution Owner | Resolution Deadline | Status |
|--------------|----------|-----------|-----------------|-------------------|--------|
| ASMP-001 | Datasheet: Identification (Objectives) | OBJ-004, OBJ-006 mapping confirmation | WORKING_ITEMS/TASK | 2026-02-24 | CLOSED (confirmed against decomposition DEL-06-03 row) |
| ASMP-002 | Datasheet: Conditions (Opt-In) | No automatic triggers found -- absence of evidence, not evidence of absence | WORKING_ITEMS/TASK | 2026-02-24 | CLOSED (documented evidence in `Cross_Deliverable_Workflow_Conformance_Assessment_2026-02-24.md`) |
| ASMP-003 | Guidance: C-001 | Dual instruction file location pattern (`agents/` vs `.claude/agents/`) is intentional | Human (architecture decision) | TBD | OPEN |
| ASMP-004 | Specification: R-003 | `_Schedule/` tool root not listed in SPEC Section 1.2 | Human (SPEC update decision) | TBD | OPEN |
| ASMP-005 | Datasheet: Snapshot Output Model | RECONCILIATION non-snapshot model rationale inferred from agent type and output patterns | Human (design confirmation) | TBD | OPEN |

> **Note (Lensing B-001):** This tracking table provides a resolution mechanism for the assumptions scattered throughout the four documents. Until the human confirms or refutes each assumption, dependent conformance judgments remain provisional. (Source: identified from Datasheet.md, Specification.md, and Guidance.md assumption markers.)

### Write Quarantine

All four agents declare explicit write-scope restrictions:

| Invariant | Status |
|-----------|--------|
| K-WRITE-1 (explicit write scope) | Each agent declares WRITE_SCOPE in its Agent Type table (Source: respective agent instruction files) |
| K-SNAP-1 (immutable snapshots) | AGGREGATION, ESTIMATING, SCHEDULING declare snapshot immutability; RECONCILIATION produces run summaries (non-snapshot model) (Source: respective agent instruction files) |
| K-GHOST-1 (no ghost inputs) | ESTIMATING explicitly forbids internet fetch; all agents read from filesystem only (Source: `AGENT_ESTIMATING.md` -- PRICE_SOURCES constraint; general agent design pattern) |

## Construction

### Tool Root Mapping (per SPEC Section 1.2)

| Tool Root | SPEC-Defined Purpose | Agent Writer |
|-----------|---------------------|-------------|
| `_Aggregation/` | Aggregation snapshots and templates | AGGREGATION |
| `_Reconciliation/` | Reconciliation reports, closure analysis | RECONCILIATION (via spawned Type 2 tasks) |
| `_Estimates/` | Cost estimate snapshots | ESTIMATING |
| `_Schedule/` | TBD -- not listed in SPEC Section 1.2 | SCHEDULING |

**Note:** `_Schedule/` is used by SCHEDULING but is not currently listed in SPEC Section 1.2 Tool Roots table. See Conflict Table in Guidance.md (Conflict C-001).

### Required Subfolders per Agent

| Agent | Required Bootstrap Folders | Source |
|-------|---------------------------|--------|
| AGGREGATION | `_Aggregation/`, `_Archive/`, `_Templates/`, `_Pipelines/`, `_LATEST.md` | `AGENT_AGGREGATION.md` Function 0 |
| RECONCILIATION | `_Reconciliation/`, `_Archive/` | `AGENT_RECONCILIATION.md` Step 0 |
| ESTIMATING | `_Estimates/` (creates snapshot folder per run) | `AGENT_ESTIMATING.md` Step 0 |
| SCHEDULING | `_Schedule/` (creates snapshot folder per run) | `SCHEDULING.md` Gate 5 |

## References

| Reference | Location | Relevance |
|-----------|----------|-----------|
| Software Decomposition | `execution/_Decomposition/ChiralityApp_SoftwareDecomposition_2026-02-21_G7-APPROVED.md` | DEL-06-03 entry and SOW-020 definition |
| AGENT_AGGREGATION.md | `agents/AGENT_AGGREGATION.md` | Cross-deliverable aggregation agent instructions |
| AGENT_RECONCILIATION.md | `agents/AGENT_RECONCILIATION.md` | Cross-deliverable reconciliation agent instructions |
| AGENT_ESTIMATING.md | `agents/AGENT_ESTIMATING.md` | Cross-deliverable estimating agent instructions |
| SCHEDULING.md | `.claude/agents/SCHEDULING.md` | Cross-deliverable scheduling agent instructions |
| SPEC.md | `docs/SPEC.md` | Tool root layout, snapshot conventions, pointer file rules |
| CONTRACT.md | `docs/CONTRACT.md` | K-WRITE-1, K-SNAP-1, K-GHOST-1 invariants |
| DIRECTIVE.md | `docs/DIRECTIVE.md` | Human authority, opt-in workflows, scope boundaries |
| TYPES.md | `docs/TYPES.md` | Agent type classification, lifecycle states |
| AGENT_HELPS_HUMANS.md | `agents/AGENT_HELPS_HUMANS.md` | Canonical agent design standard |
