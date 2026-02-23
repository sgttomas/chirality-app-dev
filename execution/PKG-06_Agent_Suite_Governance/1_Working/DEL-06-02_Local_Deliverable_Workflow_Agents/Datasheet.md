# Datasheet — DEL-06-02 Local Deliverable Workflow Agents

## Identification

| Field | Value |
|-------|-------|
| **Deliverable ID** | DEL-06-02 |
| **Name** | Local Deliverable Workflow Agents (Scaffold -> Doc Kit -> Semantic) |
| **Package** | PKG-06 Agent Suite & Governance |
| **Type** | DOC_UPDATE |
| **Context Envelope** | M |
| **Responsible Party** | TBD |
| **Scope Items** | SOW-017, SOW-019 |
| **Objectives** | OBJ-004, OBJ-006 (**ASSUMPTION: best-effort mapping** via PKG-06 package heuristic; confirmation pending -- see lensing item X-001) |
| **Anticipated Artifacts** | DOC |
| **Decomposition** | `execution/_Decomposition/ChiralityApp_SoftwareDecomposition_2026-02-21_G7-APPROVED.md` |

## Attributes

### Agents in Scope

The local deliverable workflow is implemented by a pipeline of four Type 2 task agents, each with a bounded write scope. This deliverable concerns ensuring these agents collectively cover the full local lifecycle.

| Agent | Instruction File | Role in Pipeline | Write Scope | Actual Write Targets | Primary Output |
|-------|-----------------|------------------|-------------|---------------------|----------------|
| PREPARATION | `AGENT_PREPARATION.md` | Workspace scaffolding (folders + minimum viable fileset) | `workspace-scaffold-only` | Package/deliverable folders + five metadata files | `_STATUS.md`, `_CONTEXT.md`, `_DEPENDENCIES.md`, `_REFERENCES.md`, `_SEMANTIC.md` (placeholder) |
| 4_DOCUMENTS | `AGENT_4_DOCUMENTS.md` | Production document drafting (four-document set) | `deliverable-local` | Four production documents + `_STATUS.md` safe update | `Datasheet.md`, `Specification.md`, `Guidance.md`, `Procedure.md` |
| CHIRALITY_FRAMEWORK | `AGENT_CHIRALITY_FRAMEWORK.md` | Semantic matrix generation | `deliverable-local` | `_SEMANTIC.md` + `_STATUS.md` safe update | `_SEMANTIC.md` (overwrites placeholder) |
| CHIRALITY_LENS | `AGENT_CHIRALITY_LENS.md` | Semantic lensing extraction | `deliverable-local` | `_SEMANTIC_LENSING.md` only | `_SEMANTIC_LENSING.md` |

> **Note (lensing item F-001):** All four agents declare `deliverable-local` or `workspace-scaffold-only` as their write scope. However, actual write targets differ significantly. CHIRALITY_LENS writes only `_SEMANTIC_LENSING.md`, which is narrower than other agents sharing the `deliverable-local` scope label. The scope label describes the *boundary* (deliverable folder), not the *extent* of writes within that boundary. Source: individual agent instruction file headers (`AGENT_CHIRALITY_LENS.md`, `AGENT_4_DOCUMENTS.md`).

### Lifecycle Coverage

The pipeline covers the following `_STATUS.md` state transitions (source: `docs/SPEC.md` Section 3.3):

| Transition | Agent Responsible | Status Behavior Notes |
|------------|-------------------|----------------------|
| `-> OPEN` | PREPARATION | Sets on folder creation |
| `OPEN -> INITIALIZED` | 4_DOCUMENTS | Only when Pass 1/2 ran; only from OPEN |
| `INITIALIZED -> SEMANTIC_READY` | CHIRALITY_FRAMEWORK | Only from INITIALIZED |
| *(no transition)* | CHIRALITY_LENS | Does not modify `_STATUS.md` (source: `AGENT_CHIRALITY_LENS.md` write scope) |

Subsequent transitions (`SEMANTIC_READY -> IN_PROGRESS`, `IN_PROGRESS -> CHECKING`, `CHECKING -> ISSUED`) are human-driven or WORKING_ITEMS-driven and are outside this deliverable's scope.

### Minimum Viable Fileset (PREPARATION output)

Per `docs/SPEC.md` Section 2.1, the minimum viable fileset consists of five MUST-presence files:

| File | Presence | Created By | Purpose |
|------|----------|-----------|---------|
| `_STATUS.md` | MUST | PREPARATION | Lifecycle state and history |
| `_CONTEXT.md` | MUST | PREPARATION | Identity, decomposition pointer, traceability |
| `_DEPENDENCIES.md` | MUST | PREPARATION | Dependency summary (human declarations + agent extractions) |
| `_REFERENCES.md` | MUST | PREPARATION | Source document pointers |
| `_SEMANTIC.md` | MUST | PREPARATION (placeholder); CHIRALITY_FRAMEWORK (populated) | Semantic lens with derivation work |

Additionally, `docs/SPEC.md` Section 2.1 lists the following as SHOULD-presence (not part of the minimum viable fileset):

| File | Presence | Created By | Purpose |
|------|----------|-----------|---------|
| `MEMORY.md` | SHOULD | PREPARATION | Working memory (canonical; shared by WORKING_ITEMS and TASK agents) |
| `Dependencies.csv` | SHOULD | DEPENDENCIES | Structured dependency register (v3.1 schema) |
| `_MEMORY.md` | MUST NOT | N/A | Disabled in this project profile; do not create or maintain |

> **Clarification (lensing items B-001, X-002):** `MEMORY.md` is SHOULD in `docs/SPEC.md` Section 2.1 (not part of the minimum viable fileset). `_MEMORY.md` is disabled for this project profile. PREPARATION Task C currently does not mandate `MEMORY.md` creation.

### Production Document Set (4_DOCUMENTS output)

Per `docs/SPEC.md` Section 2.1 and `docs/TYPES.md` Section 7:

| Document | Purpose |
|----------|---------|
| `Datasheet.md` | Key parameters, identification, structured metadata |
| `Specification.md` | Technical requirements, scope definition, acceptance criteria |
| `Guidance.md` | Design guidance, rationale, best practices, contextual direction |
| `Procedure.md` | Step-by-step execution workflow, sequencing, checklists |

> **Vocabulary note:** This deliverable uses "production document set" (or equivalently "four-document set") as the canonical term for these four files. See Guidance.md Vocabulary section for the full normalization. Source: lensing item B-002.

### Semantic Artifacts (optional pipeline)

Per SOW-019 and `docs/SPEC.md` Section 2.1:

| Artifact | Created By | Presence | Purpose |
|----------|-----------|----------|---------|
| `_SEMANTIC.md` | CHIRALITY_FRAMEWORK | MAY | Semantic matrices as a structured lens |
| `_SEMANTIC_LENSING.md` | CHIRALITY_LENS | MAY | Enrichment-ready extraction register |

## Conditions

| Condition | Value | Source |
|-----------|-------|--------|
| Decomposition variant support | PROJECT_DECOMP, SOFTWARE_DECOMP (4_DOCUMENTS); all three variants for semantic agents | `AGENT_4_DOCUMENTS.md`, `AGENT_CHIRALITY_FRAMEWORK.md` |
| DOMAIN variant (4_DOCUMENTS) | Unsupported; returns `UNSUPPORTED_VARIANT` | `AGENT_4_DOCUMENTS.md` Step 0 |
| Overwrite protection | Agents respect `ALLOW_OVERWRITE_STATES` runtime parameter before modifying documents; default value is `OPEN, INITIALIZED, SEMANTIC_READY` but ORCHESTRATOR may override at invocation time | `AGENT_4_DOCUMENTS.md` Step 0, Runtime parameters table |
| Idempotency (PREPARATION) | Never overwrites existing files; skip and report | `AGENT_PREPARATION.md` invariants |
| No engineering content (PREPARATION) | PREPARATION creates structural scaffolding only | `AGENT_PREPARATION.md` invariants |
| Source fidelity (4_DOCUMENTS) | Non-trivial values cite sources; unknown values become `TBD` | `AGENT_4_DOCUMENTS.md` invariants; `K-INVENT-1` |
| Conflict surfacing | Conflicts surfaced in Conflict Table, not silently resolved | `AGENT_4_DOCUMENTS.md` Step 5; `K-CONFLICT-1` |
| Agent spawning model | All four agents are spawned by ORCHESTRATOR | Agent instruction headers |
| Pass 3 graceful degradation | When `RUN_PASSES=FULL` and `_SEMANTIC_LENSING.md` does not exist, 4_DOCUMENTS runs P1+P2, skips P3, performs mini consistency sweep, and reports the missing lensing file to ORCHESTRATOR | `AGENT_4_DOCUMENTS.md` Step 6: "skip lensing, do a final mini consistency sweep, and report missing lensing file to ORCHESTRATOR" |
| Run observability | Dispatch + completion outcomes are recorded through orchestrator/control-loop reporting (`RUN_STATUS` or completion reports) | `AGENT_PREPARATION.md`, `AGENT_4_DOCUMENTS.md`, `AGENT_CHIRALITY_FRAMEWORK.md`, `AGENT_CHIRALITY_LENS.md`, `AGENT_ORCHESTRATOR.md`, `NEXT_INSTANCE_PROMPT.md` |

## Construction

### Pipeline Sequence

```
ORCHESTRATOR
  |
  +--> PREPARATION (Task C: scaffold deliverable folder)
  |      Output: minimum viable fileset, _STATUS.md = OPEN
  |
  +--> 4_DOCUMENTS (Pass 1 + Pass 2)
  |      Output: Datasheet, Specification, Guidance, Procedure
  |      _STATUS.md: OPEN -> INITIALIZED
  |
  +--> CHIRALITY_FRAMEWORK (semantic matrix generation)
  |      Output: _SEMANTIC.md (populated)
  |      _STATUS.md: INITIALIZED -> SEMANTIC_READY
  |
  +--> CHIRALITY_LENS (semantic lensing)
  |      Output: _SEMANTIC_LENSING.md
  |      _STATUS.md: unchanged (CHIRALITY_LENS does not modify status)
  |
  +--> 4_DOCUMENTS (Pass 3 only, optional)
         Output: enriched production document set using lensing register
```

### Key Integration Points

| Integration | Mechanism |
|-------------|-----------|
| ORCHESTRATOR -> agents | Runtime parameters (`DELIVERABLE_PATH`, `DECOMPOSITION_REF`, `RUN_PASSES`, etc.) |
| PREPARATION -> 4_DOCUMENTS | 4_DOCUMENTS reads `_CONTEXT.md`, `_REFERENCES.md`, `_DEPENDENCIES.md` created by PREPARATION |
| 4_DOCUMENTS -> CHIRALITY_FRAMEWORK | CHIRALITY_FRAMEWORK reads the four production documents as deliverable perspective |
| CHIRALITY_FRAMEWORK -> CHIRALITY_LENS | CHIRALITY_LENS reads `_SEMANTIC.md` as lens input |
| CHIRALITY_LENS -> 4_DOCUMENTS (Pass 3) | 4_DOCUMENTS reads `_SEMANTIC_LENSING.md` as enrichment worklist |

## References

| Reference | Relevance |
|-----------|-----------|
| `docs/SPEC.md` Section 2 | Deliverable folder layout and file inventory (including MUST/SHOULD/MAY presence rules) |
| `docs/SPEC.md` Section 3 | `_STATUS.md` lifecycle states and transitions |
| `docs/TYPES.md` Section 5 | Lifecycle state definitions |
| `docs/TYPES.md` Section 7 | Document kit types and purposes |
| `docs/CONTRACT.md` | Binding invariants (K-INVENT-1, K-CONFLICT-1, K-STATUS-1, K-WRITE-1, K-GHOST-1) |
| `docs/DIRECTIVE.md` Section 4 | In-scope: workspace scaffolding, document kit drafting, semantic analysis |
| `agents/AGENT_PREPARATION.md` | PREPARATION agent instruction file |
| `agents/AGENT_4_DOCUMENTS.md` | 4_DOCUMENTS agent instruction file |
| `agents/AGENT_CHIRALITY_FRAMEWORK.md` | CHIRALITY_FRAMEWORK agent instruction file |
| `agents/AGENT_CHIRALITY_LENS.md` | CHIRALITY_LENS agent instruction file |
| `agents/AGENT_HELPS_HUMANS.md` | Type 0 standard governing all agent instruction design |
| `execution/_Decomposition/ChiralityApp_SoftwareDecomposition_2026-02-21_G7-APPROVED.md` | Software decomposition (DEL-06-02 entry) |
