# Guidance — DEL-06-02 Local Deliverable Workflow Agents

## Purpose

This deliverable exists to ensure that the four local deliverable workflow agents -- PREPARATION, 4_DOCUMENTS, CHIRALITY_FRAMEWORK, and CHIRALITY_LENS -- collectively support the full local deliverable lifecycle from workspace scaffolding through production document set drafting through optional semantic analysis.

The decomposition states (source: `ChiralityApp_SoftwareDecomposition_2026-02-21_G7-APPROVED.md`, DEL-06-02 entry):

> "Ensure PREPARATION + 4_DOCUMENTS + semantic agents support local deliverable lifecycle and required artifacts."

This is an **agent enablement** deliverable. Its output is DOC: it verifies and documents that the agent pipeline works correctly against the governance and specification contracts, rather than producing new code or infrastructure.

## Principles

### P1: Pipeline Composition over Monolithic Agents

The local deliverable workflow deliberately distributes responsibilities across four separate agents rather than combining them into a single agent. This design follows several structural principles:

- **Bounded write scope** (`K-WRITE-1`): Each agent writes only within its declared zone. PREPARATION creates scaffolding; 4_DOCUMENTS writes production documents; CHIRALITY_FRAMEWORK writes `_SEMANTIC.md`; CHIRALITY_LENS writes `_SEMANTIC_LENSING.md`. No agent can accidentally damage another agent's outputs.
- **Incremental lifecycle advancement** (`K-STATUS-1`): Each agent advances the lifecycle state by exactly one step (or, in the case of CHIRALITY_LENS, does not advance it at all). This makes pipeline progress auditable and recoverable -- if a step fails, the previous state is preserved.
- **Rerunnable stages**: Because each agent has bounded scope and reads its predecessors' outputs as immutable inputs, individual stages can be rerun without re-executing the entire pipeline.

Source: `docs/CONTRACT.md` (K-WRITE-1, K-STATUS-1); `docs/DIRECTIVE.md` Section 2.3 (human authority at every gate).

### P2: Scaffolding Before Content

PREPARATION runs first and creates structural scaffolding only -- no engineering content. This ensures:

- Downstream agents have predictable inputs (the minimum viable fileset).
- `_CONTEXT.md` is extracted faithfully from the decomposition before any interpretation occurs.
- The deliverable folder exists with correct naming and metadata before content generation begins.

This separation is a direct implementation of the "evidence over plausibility" principle (`docs/DIRECTIVE.md` Section 2.4): the scaffolding carries only what is known from the decomposition, and content drafting is a separate, clearly-delineated step.

Source: `AGENT_PREPARATION.md` invariants; `docs/DIRECTIVE.md` Section 2.4.

### P3: Semantic Analysis Is Optional

The `INITIALIZED -> SEMANTIC_READY` transition is optional (`docs/TYPES.md` Section 5.3). Deliverables may transition directly from `INITIALIZED -> IN_PROGRESS` when the semantic step is skipped. This means:

- The production document set is a complete, usable scaffold even without semantic analysis.
- Semantic matrices and lensing are enrichment tools, not prerequisites for human work.
- The pipeline gracefully degrades: if CHIRALITY_FRAMEWORK or CHIRALITY_LENS are not run, the deliverable is still in a valid, workable state.

Source: `docs/SPEC.md` Section 3.3; `docs/TYPES.md` Section 5.3.

### P4: Source Fidelity as the Primary Quality Signal

The most important quality attribute of agent-generated documents is not depth or completeness but source fidelity:

- Values that can be cited to sources are included with citations.
- Values that cannot be cited become `TBD`.
- Inferences are labeled `ASSUMPTION`.
- Contradictions are surfaced in Conflict Tables rather than silently resolved.

This principle flows directly from `K-INVENT-1` ("unknown values become TBD, not guessed"), `K-CONFLICT-1` ("conflicts surfaced, not silently resolved"), and `docs/DIRECTIVE.md` Section 2.4 ("evidence over plausibility").

Source: `docs/CONTRACT.md` (K-INVENT-1, K-CONFLICT-1); `docs/DIRECTIVE.md` Section 2.4.

## Vocabulary

> **Added (lensing item B-002):** To reduce terminology drift across documents and downstream references, this section establishes canonical terms.

| Canonical Term | Acceptable Synonyms | Avoid |
|----------------|---------------------|-------|
| **production document set** | four-document set | "document kit" (ambiguous -- could include metadata files), "production documents" (acceptable but less precise as a set reference) |
| **minimum viable fileset** | (none -- use as-is) | "metadata files" (incomplete -- does not convey the MUST-presence requirement) |
| **deliverable folder** | (none -- use as-is) | "workspace" (ambiguous -- could mean execution root) |
| **lensing register** | extraction register | "lensing file" (imprecise) |

Note: This vocabulary normalization applies to this deliverable's documents. Other deliverables may use their own terminology conventions. The terms "four-document set" and "production document set" are used interchangeably in this document set.

## Considerations

### C1: Context Envelope and Agent Complexity

DEL-06-02 has a context envelope of M (Medium). The deliverable is bounded to documentation review and alignment rather than code changes. The primary work involves:

- Reading and verifying four agent instruction files against the governance contracts.
- Documenting the pipeline behavior and integration points.
- Identifying any gaps between agent instructions and SPEC/CONTRACT requirements.

The work does not involve modifying agent instruction files (that is DEL-06-01's scope) but rather verifying their behavior aligns with lifecycle requirements.

### C2: Relationship to DEL-06-01

DEL-06-01 (Agent Instruction Suite Structural Conformance) focuses on HELPS_HUMANS structural conformance across all agent instruction files. DEL-06-02 focuses on functional correctness of the local workflow pipeline. These are complementary:

- DEL-06-01 ensures agents have correct headers, section markers, write scopes declared.
- DEL-06-02 ensures the pipeline produces the right outputs in the right order with the right protections.

If DEL-06-01 identifies structural non-conformance in one of the four workflow agents, that finding is an input to DEL-06-02's completeness assessment.

### C3: Dependency Tracking Agent Is Not in Scope

The DEPENDENCIES agent is responsible for populating `_DEPENDENCIES.md` extracted sections and `Dependencies.csv`. While the dependency file is part of the minimum viable fileset (created by PREPARATION), the extraction mechanics are governed by SOW-018 and DEL-05-04. This deliverable only verifies that PREPARATION creates the structural container correctly.

### C4: 4_DOCUMENTS Pass 3 Dependency on Semantic Pipeline

4_DOCUMENTS Pass 3 requires `_SEMANTIC_LENSING.md` to exist. This creates a soft dependency on the semantic pipeline (CHIRALITY_FRAMEWORK -> CHIRALITY_LENS). If the semantic pipeline is not run, Pass 3 cannot execute.

This is by design: Pass 3 enrichment is an optional enhancement, not a requirement for the production document set to be usable. The `RUN_PASSES` parameter allows ORCHESTRATOR to request `P1_P2` (skipping Pass 3) or `FULL` (including Pass 3 when lensing is available).

> **Clarification (lensing item F-002):** When `RUN_PASSES=FULL` and `_SEMANTIC_LENSING.md` does not exist, 4_DOCUMENTS degrades gracefully: it runs Pass 1 and Pass 2, skips Pass 3, performs a final mini consistency sweep, and reports the missing lensing file to ORCHESTRATOR. It does **not** fail the entire run. This behavior is explicitly defined in `AGENT_4_DOCUMENTS.md` Step 6: "If missing: ... If `RUN_PASSES` is `FULL`: skip lensing, do a final mini consistency sweep, and report missing lensing file to ORCHESTRATOR."

Source: `AGENT_4_DOCUMENTS.md` Step 6, Preconditions subsection.

### C5: DOMAIN Variant Exclusion

4_DOCUMENTS explicitly does not support the DOMAIN decomposition variant (`DECOMP_VARIANT = DOMAIN`). DOMAIN Knowledge Types use variable document schemas rather than the standard production document set. If DOMAIN support is needed in the future, a separate document agent (or an extension to 4_DOCUMENTS) would be required.

This exclusion is documented in `AGENT_4_DOCUMENTS.md` Step 0 and is consistent with the current software decomposition scope.

### C6: TBD Density as a Quality Signal

> **Added (lensing item E-002):** TBD values serve an important function: they make gaps visible and auditable. However, when TBD density is high (many placeholders relative to substantive content), it may signal that the deliverable lacks sufficient input material for productive drafting.

There is no normative threshold defined in any governance source for acceptable TBD density. The following heuristic is offered as **ASSUMPTION (no source):**

- If a production document has more TBD values than substantive assertions, consider whether the deliverable's reference materials are complete enough for meaningful drafting. This may warrant pausing to gather more inputs (additional references, upstream deliverable outputs, or human clarifications) rather than proceeding with a largely placeholder document.
- The decision to pause or proceed remains a human judgment; agents should report TBD counts but not autonomously defer work based on density alone.

This consideration is directional, not prescriptive. No governance source currently establishes TBD density thresholds.

### C7: Run Observability Is a Status Contract, Not a Performance SLA

DEL-06-02 now treats observability as a dispatch/completion status contract across the four workflow agents and ORCHESTRATOR fan-in reporting. This keeps the requirement objectively verifiable without inventing timing targets that have no governance source.

Scope boundary:
- In scope: completion outcomes (`RUN_STATUS`, PASS/FAIL, completion reports), pass-level control-loop summaries.
- Out of scope: latency SLOs, token budgets, timeout thresholds.

This framing preserves auditability while avoiding false precision.

## Trade-offs

### T1: Idempotency vs. Correctability

PREPARATION's strict idempotency (never overwrite existing files) means that if `_CONTEXT.md` is created with incorrect values, PREPARATION cannot fix it on a rerun. The file must be manually deleted or corrected before PREPARATION can recreate it.

**Rationale for idempotency:** Prevents accidental destruction of human edits. The cost of manual correction is lower than the risk of losing work.

**Mitigation:** `_CONTEXT.md` fields are extracted exactly from the decomposition (`AGENT_PREPARATION.md` invariant: "Exact extraction"), minimizing the chance of errors at creation time.

Source: `AGENT_PREPARATION.md` invariants.

### T2: TBD Density vs. Speculative Completeness

The strict `TBD` discipline means generated documents may contain many placeholder values, especially for deliverables with sparse reference materials. This can make documents feel incomplete.

**Rationale for TBD discipline:** Speculative content is worse than acknowledged gaps. `TBD` values are visible, auditable, and actionable; invented values are invisible risks. This follows `K-INVENT-1`.

**Mitigation:** Semantic lensing (Pass 3) provides a structured mechanism for enriching documents after initial generation, guided by matrix-organized analysis rather than speculation.

Source: `docs/CONTRACT.md` (K-INVENT-1); `AGENT_4_DOCUMENTS.md` Step 6.

### T3: Four Separate Agents vs. Pipeline Overhead

Running four agents sequentially introduces coordination overhead (ORCHESTRATOR must manage spawning, parameter passing, and status checking). A single combined agent would be simpler to invoke.

**Rationale for separation:** Write scope isolation (`K-WRITE-1`), incremental state advancement, and rerunnable stages outweigh the coordination cost. The ORCHESTRATOR already manages multi-agent pipelines as a core function.

Source: `docs/CONTRACT.md` (K-WRITE-1); `AGENT_ORCHESTRATOR.md`.

### T4: Gap Severity Classification Rationale

> **Added (lensing item F-003):** The Procedure (Step 10.2) uses a three-level severity classification for gaps: Critical, Major, Minor.

**Rationale for the three-level scheme:** This is a conventional engineering severity classification widely used in audit and review contexts. The specific boundaries applied in this deliverable are:

- **Critical:** Agent instruction contradicts SPEC or CONTRACT invariant -- meaning the pipeline cannot reliably produce correct outputs.
- **Major:** Required behavior is not explicitly stated (implicit only) -- meaning the pipeline may work correctly but is not verifiably compliant.
- **Minor:** Documentation improvement opportunity -- meaning the pipeline works but documentation could be clearer.

**Source for boundaries:** No formal source defines these exact boundaries for this project. The categories are **ASSUMPTION** based on standard engineering review practice. The human reviewer may adjust thresholds or add levels.

## Examples

### Example: Successful Full Pipeline Run

Given a new deliverable DEL-XX-YY with no existing files:

1. ORCHESTRATOR spawns PREPARATION (Task C) with deliverable metadata.
2. PREPARATION creates folder + five metadata files (minimum viable fileset). `_STATUS.md` = `OPEN`.
3. ORCHESTRATOR spawns 4_DOCUMENTS with `RUN_PASSES=P1_P2`.
4. 4_DOCUMENTS reads `_CONTEXT.md`, decomposition, references. Generates four production documents. `_STATUS.md` = `INITIALIZED`.
5. ORCHESTRATOR spawns CHIRALITY_FRAMEWORK.
6. CHIRALITY_FRAMEWORK reads four production documents + `_CONTEXT.md`. Generates `_SEMANTIC.md`. `_STATUS.md` = `SEMANTIC_READY`.
7. ORCHESTRATOR spawns CHIRALITY_LENS.
8. CHIRALITY_LENS reads `_SEMANTIC.md` + four production documents. Generates `_SEMANTIC_LENSING.md`. `_STATUS.md` unchanged.
9. ORCHESTRATOR spawns 4_DOCUMENTS with `RUN_PASSES=P3_ONLY`.
10. 4_DOCUMENTS reads `_SEMANTIC_LENSING.md`. Enriches four production documents with sourced improvements.

### Example: Overwrite Protection

Given a deliverable with `_STATUS.md` state = `IN_PROGRESS`:

1. ORCHESTRATOR spawns 4_DOCUMENTS with `ALLOW_OVERWRITE_STATES = OPEN, INITIALIZED, SEMANTIC_READY`.
2. 4_DOCUMENTS reads `_STATUS.md`, sees `IN_PROGRESS`.
3. 4_DOCUMENTS returns `RUN_STATUS=SKIPPED_PROTECT_HUMAN_WORK` without modifying any files.

### Example: Missing Lensing File for Pass 3

1. ORCHESTRATOR spawns 4_DOCUMENTS with `RUN_PASSES=P3_ONLY`.
2. 4_DOCUMENTS checks for `_SEMANTIC_LENSING.md` -- file does not exist.
3. 4_DOCUMENTS returns `RUN_STATUS=FAILED_INPUTS` without modifying any files.

### Example: FULL Run Without Lensing (Graceful Degradation)

1. ORCHESTRATOR spawns 4_DOCUMENTS with `RUN_PASSES=FULL`.
2. 4_DOCUMENTS runs Pass 1 (generation) and Pass 2 (consistency check) successfully.
3. 4_DOCUMENTS checks for `_SEMANTIC_LENSING.md` -- file does not exist.
4. 4_DOCUMENTS skips Pass 3, performs a final mini consistency sweep, reports the missing lensing file to ORCHESTRATOR.
5. `_STATUS.md` transitions `OPEN -> INITIALIZED` normally.

Source: `AGENT_4_DOCUMENTS.md` Step 6.

## Conflict Table (for human ruling)

| Conflict ID | Conflict | Source A | Source B | Impacted Sections | Proposed Authority (PROPOSAL) | Human Ruling |
|---|---|---|---|---|---|---|
| CT-001 | MEMORY file naming/presence drift in prior drafts (`_MEMORY.md` vs `MEMORY.md`) | `docs/SPEC.md` Section 2.1 (`MEMORY.md` SHOULD; `_MEMORY.md` MUST NOT for this project profile) | Prior DEL-06-02 docs referenced `_MEMORY.md` as SHOULD | Specification REQ-01; Datasheet Minimum Viable Fileset; Procedure Step 1 | Align all DEL-06-02 docs to `MEMORY.md` SHOULD and `_MEMORY.md` MUST NOT | RESOLVED (2026-02-23 docs harmonization pass) |
| CT-002 | No aggregate acceptance gate for the deliverable: individual requirements (REQ-01 through REQ-16) each have verification approaches, but there is no overarching acceptance criterion for when the deliverable itself is considered complete (e.g., "all requirements verified = deliverable can transition to ISSUED"). | Specification.md Verification section (per-requirement verification) | `docs/SPEC.md` Section 3.3 (lifecycle transitions -- `CHECKING -> ISSUED` requires human approval but no explicit acceptance formula) | Specification Documentation section; Procedure Completion Criteria | Human decision: define whether "all 16 requirements pass verification" is sufficient for ISSUED, or whether additional acceptance criteria are needed. Proposed authority: `docs/SPEC.md` lifecycle or human. | PENDING (2026-02-23 decision input prepared: `CT-002_Acceptance_Gate_Decision_Input_2026-02-23.md`) |
