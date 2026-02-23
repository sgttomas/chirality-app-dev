# Procedure — DEL-06-02 Local Deliverable Workflow Agents

## Purpose

This procedure describes how to verify and validate that the local deliverable workflow agents (PREPARATION, 4_DOCUMENTS, CHIRALITY_FRAMEWORK, CHIRALITY_LENS) correctly support the local deliverable lifecycle and required artifacts as specified in `Specification.md`.

Since this deliverable's type is DOC_UPDATE, the procedure focuses on **verification and documentation** rather than code implementation.

## Prerequisites

### Required References

| Reference | Location | Purpose |
|-----------|----------|---------|
| Software Decomposition | `execution/_Decomposition/ChiralityApp_SoftwareDecomposition_2026-02-21_G7-APPROVED.md` | DEL-06-02 entry and pipeline context |
| SPEC | `docs/SPEC.md` | Canonical file formats, folder layout, lifecycle states |
| CONTRACT | `docs/CONTRACT.md` | Binding invariants |
| TYPES | `docs/TYPES.md` | Canonical vocabulary and lifecycle definitions |
| DIRECTIVE | `docs/DIRECTIVE.md` | Founding intent and scope |
| AGENT_PREPARATION.md | `agents/AGENT_PREPARATION.md` | PREPARATION agent instructions |
| AGENT_4_DOCUMENTS.md | `agents/AGENT_4_DOCUMENTS.md` | 4_DOCUMENTS agent instructions |
| AGENT_CHIRALITY_FRAMEWORK.md | `agents/AGENT_CHIRALITY_FRAMEWORK.md` | CHIRALITY_FRAMEWORK agent instructions |
| AGENT_CHIRALITY_LENS.md | `agents/AGENT_CHIRALITY_LENS.md` | CHIRALITY_LENS agent instructions |

### Required Conditions

- Access to the execution workspace (`execution/`) with at least one package and deliverable scaffolded.
- Access to all four agent instruction files.
- Access to `docs/SPEC.md`, `docs/CONTRACT.md`, `docs/TYPES.md`, and `docs/DIRECTIVE.md`.

### Upstream Dependencies

- DEL-06-01 (Agent Instruction Suite Structural Conformance) -- **ASSUMPTION:** If DEL-06-01 identifies structural non-conformance in workflow agent instructions, those findings are inputs here. However, this procedure can be executed independently of DEL-06-01's completion status because it reads agent instruction files directly rather than depending on DEL-06-01's output artifacts.

> **Clarification (lensing item X-004):** DEL-06-01 is a **non-blocking contextual dependency**, not a hard prerequisite. This procedure reads agent instruction files directly and does not require DEL-06-01 to be completed first. If DEL-06-01 has been completed, its findings (e.g., structural non-conformance in agent headers) should be reviewed as supplementary input during Step 9.

## Steps

### Step 1: Verify PREPARATION Minimum Viable Fileset Contract

**Objective:** Confirm that PREPARATION Task C produces all required files per `docs/SPEC.md` Section 2.1.

**Actions:**

1.1. Read `agents/AGENT_PREPARATION.md`, Task Type C section.

1.2. Verify the following files are listed as PREPARATION Task C outputs (these constitute the minimum viable fileset per `docs/SPEC.md` Section 2.1):
   - [ ] `_STATUS.md` (initialized to `OPEN`)
   - [ ] `_CONTEXT.md` (fields match decomposition)
   - [ ] `_DEPENDENCIES.md` (hybrid container with human-owned and agent-owned sections)
   - [ ] `_REFERENCES.md` (source document pointers)
   - [ ] `_SEMANTIC.md` (placeholder stub)

1.3. Additionally, note whether `MEMORY.md` is addressed by PREPARATION. Per `docs/SPEC.md` Section 2.1, `MEMORY.md` has SHOULD presence (not MUST). `_MEMORY.md` is disabled (`MUST NOT`) for this project profile. Record whether PREPARATION Task C includes or excludes `MEMORY.md` creation.

1.4. Verify the `_CONTEXT.md` schema matches `docs/SPEC.md` Section 4.1 format.

1.5. Verify the `_DEPENDENCIES.md` schema matches `docs/SPEC.md` Section 5.2 format.

1.6. Verify the `_STATUS.md` schema matches `docs/SPEC.md` Section 3.1 format.

1.7. Record findings. If any MUST-presence file is missing from PREPARATION's output list, record as a gap with reference to the SPEC requirement.

**Maps to:** REQ-01, REQ-02, REQ-03 (Specification.md).

### Step 2: Verify PREPARATION Idempotency and No-Engineering-Content Constraints

**Objective:** Confirm that PREPARATION enforces idempotency and structural-only output.

**Actions:**

2.1. Verify `AGENT_PREPARATION.md` contains an explicit idempotency invariant.

2.2. Verify `AGENT_PREPARATION.md` contains an explicit no-engineering-content invariant.

2.3. Verify that PREPARATION's Task C actions include "if missing" guards on all file creation steps.

2.4. Verify that PREPARATION does not list `Datasheet.md`, `Specification.md`, `Guidance.md`, or `Procedure.md` as outputs.

2.5. Record findings.

**Maps to:** REQ-02, REQ-03 (Specification.md).

### Step 3: Verify 4_DOCUMENTS Production Document Set Output and Schema Stability

**Objective:** Confirm that 4_DOCUMENTS produces all four production documents with stable default schema sections.

**Actions:**

3.1. Read `agents/AGENT_4_DOCUMENTS.md`, Step 2 (Establish DOMAIN) and Step 4 (Generate Four Documents).

3.2. Verify the default schema sections table exists and lists:
   - Datasheet: Identification, Attributes, Conditions, Construction, References
   - Specification: Scope, Requirements, Standards, Verification, Documentation
   - Guidance: Purpose, Principles, Considerations, Trade-offs, Examples
   - Procedure: Purpose, Prerequisites, Steps, Verification, Records

3.3. Verify the "All four documents, always" invariant is present.

3.4. Verify the "Stable interface" invariant (do not rename documents; do not remove default headings) is present.

3.5. Record findings.

**Maps to:** REQ-04, REQ-05 (Specification.md).

### Step 4: Verify 4_DOCUMENTS Overwrite Protection and Status Transition Safety

**Objective:** Confirm that 4_DOCUMENTS enforces overwrite protection and safe status transitions.

**Actions:**

4.1. Read `agents/AGENT_4_DOCUMENTS.md`, Step 0 (Preconditions & Safety Checks).

4.2. Verify that Step 0 reads `_STATUS.md` and checks `Current State` against `ALLOW_OVERWRITE_STATES`.

4.3. Verify that non-matching states produce `SKIPPED_PROTECT_HUMAN_WORK`.

4.4. Read Step 7 (Update Status). Verify:
   - Status update is `OPEN -> INITIALIZED` only.
   - Update occurs only when Pass 1/2 ran.
   - No state regression is possible.

4.5. Verify that `ALLOW_OVERWRITE_STATES` is documented as a runtime parameter (not a fixed set) in the Runtime parameters table, with a default value of `OPEN, INITIALIZED, SEMANTIC_READY`.

4.6. Record findings.

**Maps to:** REQ-06, REQ-10 (Specification.md).

### Step 5: Verify Source Fidelity and Conflict Surfacing

**Objective:** Confirm that 4_DOCUMENTS enforces TBD discipline, ASSUMPTION labeling, and conflict surfacing.

**Actions:**

5.1. Verify the following invariants exist in `AGENT_4_DOCUMENTS.md`:
   - [ ] "Source-anchored with explicit assumptions"
   - [ ] TBD for unknown values
   - [ ] ASSUMPTION labeling for inferred content

5.2. Verify Step 5 (Cross-Reference Consistency Check) includes the Conflict Table schema.

5.3. Verify the Conflict Table columns include: Conflict ID, Conflict, Source A, Source B, Impacted sections, Proposed authority, Human ruling.

5.4. Verify alignment with `K-INVENT-1` and `K-CONFLICT-1` in `docs/CONTRACT.md`.

5.5. Record findings.

**Maps to:** REQ-07, REQ-08, REQ-09 (Specification.md).

### Step 6: Verify CHIRALITY_FRAMEWORK Semantic Matrix Output

**Objective:** Confirm that CHIRALITY_FRAMEWORK produces valid `_SEMANTIC.md` and advances lifecycle state correctly.

**Actions:**

6.1. Read `agents/AGENT_CHIRALITY_FRAMEWORK.md`, focusing on:
   - Write scope declaration
   - Primary outputs
   - Status transition (`INITIALIZED -> SEMANTIC_READY`)

6.2. Verify that `_SEMANTIC.md` overwrites the PREPARATION placeholder.

6.3. Verify that CHIRALITY_FRAMEWORK does not modify production documents (Datasheet, Specification, Guidance, Procedure).

6.4. Verify that status transition is `INITIALIZED -> SEMANTIC_READY` only, with no regression.

6.5. Record findings.

**Maps to:** REQ-11, REQ-10, REQ-14 (Specification.md).

### Step 7: Verify CHIRALITY_LENS Read-Only Behavior and Lensing Output

**Objective:** Confirm that CHIRALITY_LENS produces `_SEMANTIC_LENSING.md` without editing production documents and without modifying `_STATUS.md`.

**Actions:**

7.1. Read `agents/AGENT_CHIRALITY_LENS.md`, focusing on:
   - Write scope declaration
   - Primary outputs
   - "Read-only on production documents" invariant

7.2. Verify that `_SEMANTIC_LENSING.md` is the only file written.

7.3. Verify that the "no invention" invariant is present.

7.4. Verify that provenance requirements (SourcePath, SectionRef) are enforced.

7.5. Verify that CHIRALITY_LENS does not modify `_STATUS.md` (lensing item C-002). Source: `AGENT_CHIRALITY_LENS.md` write scope declaration -- confirm it does not list `_STATUS.md` as a write target.

7.6. Record findings.

**Maps to:** REQ-12, REQ-14, REQ-10 (Specification.md).

### Step 8: Verify 4_DOCUMENTS Pass 3 Integration with Lensing

**Objective:** Confirm that 4_DOCUMENTS Pass 3 correctly uses `_SEMANTIC_LENSING.md` as an enrichment worklist.

**Actions:**

8.1. Read `agents/AGENT_4_DOCUMENTS.md`, Step 6 (Semantic Lensing Enrichment).

8.2. Verify:
   - [ ] `_SEMANTIC_LENSING.md` must exist for P3_ONLY runs.
   - [ ] Each row is treated as a "candidate improvement, not evidence."
   - [ ] Incorporation requires citeable underlying sources.
   - [ ] Insufficient evidence results in TBD or Conflict Table entries.

8.3. Verify the `FAILED_INPUTS` behavior when `_SEMANTIC_LENSING.md` is missing for P3_ONLY.

8.4. Verify the graceful degradation behavior when `RUN_PASSES=FULL` and `_SEMANTIC_LENSING.md` is missing: confirm Step 6 states that 4_DOCUMENTS skips lensing, performs mini consistency sweep, and reports to ORCHESTRATOR.

8.5. Record findings.

**Maps to:** REQ-13 (Specification.md).

### Step 9: Verify Write Scope Enforcement Across Pipeline

**Objective:** Confirm that all four agents declare and respect their write scopes per `K-WRITE-1`.

**Actions:**

9.1. For each agent, extract the `WRITE_SCOPE` from the Agent Type table and the actual write targets:

| Agent | Expected Write Scope | Expected Write Targets |
|-------|---------------------|----------------------|
| PREPARATION | `workspace-scaffold-only` | Package/deliverable folders + five metadata files |
| 4_DOCUMENTS | `deliverable-local` | Four production documents + `_STATUS.md` safe update |
| CHIRALITY_FRAMEWORK | `deliverable-local` | `_SEMANTIC.md` + `_STATUS.md` safe update |
| CHIRALITY_LENS | `deliverable-local` | `_SEMANTIC_LENSING.md` only |

9.2. Verify each agent's write actions are bounded to their declared scope.

9.3. Verify that no agent modifies `_CONTEXT.md`, `_DEPENDENCIES.md`, or `_REFERENCES.md` after PREPARATION creates them (except human edits).

9.4. If DEL-06-01 findings are available, review them for any write scope declaration issues in agent instruction headers.

9.5. Record findings.

**Maps to:** REQ-14, REQ-15 (Specification.md).

### Step 9A: Verify Run Observability Contract

**Objective:** Confirm that pipeline run outcomes are observable through orchestrator/control-loop reporting.

**Actions:**

9A.1. Verify completion-report expectations in each workflow agent instruction:
- PREPARATION reports completion.
- 4_DOCUMENTS emits `RUN_STATUS`.
- CHIRALITY_FRAMEWORK reports PASS/FAIL completion.
- CHIRALITY_LENS reports completion to invoker.

9A.2. Verify `AGENT_ORCHESTRATOR.md` includes per-deliverable run-status collection/reporting behavior.

9A.3. Verify control-loop artifacts under `execution/_Coordination/` include pass-level outcome summaries for touched deliverables.

9A.4. Record findings.

**Maps to:** REQ-16 (Specification.md).

### Step 10: Compile Gap Report and Document Findings

**Objective:** Produce a summary of compliance findings and any identified gaps.

**Actions:**

10.1. Compile all findings from Steps 1-9A into a gap report structured as:

| Requirement | Status | Findings | Gap (if any) | Recommendation |
|-------------|--------|----------|-------------|----------------|
| REQ-01 | TBD | TBD | TBD | TBD |
| ... | ... | ... | ... | ... |
| REQ-16 | PASS/FAIL | Completion-status observability contract audited in agent instructions and control-loop reports | If missing, document gap | Align orchestrator/reporting artifacts |

10.2. For each gap, classify severity:
   - **Critical:** Agent instruction contradicts SPEC or CONTRACT invariant (pipeline cannot reliably produce correct outputs).
   - **Major:** Required behavior is not explicitly stated, only implicit (pipeline may work but is not verifiably compliant).
   - **Minor:** Documentation improvement opportunity (pipeline works but documentation could be clearer).

> **Note (lensing item F-003):** This severity classification is **ASSUMPTION** -- no governance source defines these exact boundaries. See Guidance.md Trade-off T4 for rationale. The human reviewer may adjust severity definitions.

10.3. If gaps are found, propose corrective actions:
   - Agent instruction updates (refer to DEL-06-01 for structural changes).
   - SPEC/CONTRACT clarifications (escalate to governance).
   - Test case additions (refer to DEL-07-01).

## Verification

### Completion Criteria

This procedure is complete when:

- [ ] All procedure steps have been executed (including Step 9A observability verification).
- [ ] All 16 requirements from `Specification.md` have been assessed.
- [ ] Findings are documented with specific references to source files and sections.
- [ ] Any gaps are classified by severity.
- [ ] Recommendations are proposed for identified gaps.

> **Note (lensing item D-002):** These completion criteria define procedural completeness (all steps executed, all requirements assessed). They do not define deliverable acceptance. Deliverable acceptance is a human decision at the `CHECKING -> ISSUED` lifecycle transition. See Conflict Table CT-002 in Guidance.md for the aggregate acceptance gate question. The gap report should be reviewed by the responsible party (currently TBD), who determines whether the gap count and severity warrant remediation before the deliverable can advance.

### Quality Checks

| Check | Criterion |
|-------|-----------|
| Coverage | All requirements in Specification.md are addressed (REQ-01 through REQ-16) |
| Traceability | Each finding cites the specific agent instruction file, section, and line |
| Actionability | Each gap has a proposed corrective action or escalation path |
| Consistency | Findings are consistent across Steps (no contradictory conclusions) |

## Records

### Required Records

| Record | Format | Location |
|--------|--------|----------|
| Gap Report | Markdown table | This deliverable folder (or `MEMORY.md`) |
| Verification checklist (completed) | Markdown with checked boxes | This procedure document (updated copy) |
| Agent instruction file review notes | Markdown | `MEMORY.md` |

### Retention

All records are retained in the deliverable folder and tracked by git version control per `docs/DIRECTIVE.md` Section 2.2 ("git is the event store").
