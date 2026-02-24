# Procedure -- DEL-06-03 Cross-Deliverable Workflow Support

## Purpose

This procedure describes the steps to assess and ensure conformance of the four cross-deliverable workflow agents (AGGREGATION, RECONCILIATION, ESTIMATING, SCHEDULING) against the requirements of SOW-020: opt-in, human-triggered workflows producing immutable snapshot outputs under correct tool roots.

---

## Prerequisites

### Required References

| Reference | Location | Purpose |
|-----------|----------|---------|
| Software Decomposition (G7-APPROVED) | `execution/_Decomposition/ChiralityApp_SoftwareDecomposition_2026-02-21_G7-APPROVED.md` | SOW-020 definition and deliverable context |
| AGENT_AGGREGATION.md | `agents/AGENT_AGGREGATION.md` | Agent instruction review |
| AGENT_RECONCILIATION.md | `agents/AGENT_RECONCILIATION.md` | Agent instruction review |
| AGENT_ESTIMATING.md | `agents/AGENT_ESTIMATING.md` | Agent instruction review |
| SCHEDULING.md | `.claude/agents/SCHEDULING.md` | Agent instruction review |
| SPEC.md | `docs/SPEC.md` | Tool root layout (Section 1.2), snapshot conventions (Section 11), agent structure (Section 9) |
| CONTRACT.md | `docs/CONTRACT.md` | Invariants K-WRITE-1, K-SNAP-1, K-GHOST-1, K-PROV-1, K-INVENT-1, K-CONFLICT-1 |
| DIRECTIVE.md | `docs/DIRECTIVE.md` | Human authority principles (Section 2.3) |
| AGENT_HELPS_HUMANS.md | `agents/AGENT_HELPS_HUMANS.md` | Canonical agent design standard |

### Required State

- DEL-06-03 deliverable folder exists with minimum viable fileset
- All four agent instruction files are accessible at the locations listed above
- Governing documents (SPEC.md, CONTRACT.md, DIRECTIVE.md) are accessible (per R-PRE-001)

---

## Steps

### Step 0: Verify File Accessibility (Lensing C-003)

Before beginning the conformance assessment, verify that all required input files exist and are readable. This fail-fast check prevents discovering missing files mid-review.

- [ ] **0a.** Verify all four agent instruction files exist at the paths listed in Required References:
  - `agents/AGENT_AGGREGATION.md` -- exists and readable
  - `agents/AGENT_RECONCILIATION.md` -- exists and readable
  - `agents/AGENT_ESTIMATING.md` -- exists and readable
  - `.claude/agents/SCHEDULING.md` -- exists and readable
- [ ] **0b.** Verify governing documents exist:
  - `docs/SPEC.md` -- exists and readable; record version/date
  - `docs/CONTRACT.md` -- exists and readable; record version/date
  - `docs/DIRECTIVE.md` -- exists and readable; record version/date
- [ ] **0c.** Record file versions/dates in the assessment record:

| Document | Path | Accessible | Version/Date |
|----------|------|-----------|-------------|
| AGENT_AGGREGATION.md | `agents/AGENT_AGGREGATION.md` | YES | 2026-02-21 (`dfb8f2a6e7df79da4720e259c354e068e5b9fa95`) |
| AGENT_RECONCILIATION.md | `agents/AGENT_RECONCILIATION.md` | YES | 2026-02-22 (`64026eff7c9637d05f14ad51ecc84716d3344f65`) |
| AGENT_ESTIMATING.md | `agents/AGENT_ESTIMATING.md` | YES | 2026-02-21 (`dfb8f2a6e7df79da4720e259c354e068e5b9fa95`) |
| SCHEDULING.md | `.claude/agents/SCHEDULING.md` | YES | 2026-02-21 (`fe6e12a7cd41fedb697c3b4611c47cba80bc8405`) |
| SPEC.md | `docs/SPEC.md` | YES | 2026-02-23 (`6d3f37cbb9082fbfba255bd40637810e7e23e542`) |
| CONTRACT.md | `docs/CONTRACT.md` | YES | 2026-02-21 (`fb7fe065e0492f5221714d7921f7bd453746e9fa`) |
| DIRECTIVE.md | `docs/DIRECTIVE.md` | YES | 2026-02-21 (`fb7fe065e0492f5221714d7921f7bd453746e9fa`) |

- [ ] **0d.** If any required file is missing or inaccessible: STOP. Document the missing file(s) and report that the assessment cannot proceed until the file is available.

**Expected result:** All required files are accessible and versions recorded.

> **Note (Lensing C-003):** This step was added because the Prerequisites section states "All four agent instruction files are accessible" as a required state but no procedural step previously validated this. Failing fast at Step 0 prevents wasted effort and produces a clear record of input availability. (Source: Procedure.md Prerequisites; Specification.md R-PRE-001.)

### Step 1: Review Invocation Model (R-001, R-002)

For each of the four agents, verify:

- [ ] **1a.** Read the Agent Type table and confirm `INTERACTION_SURFACE` is `chat` or `INIT-TASK`
- [ ] **1b.** Search the instruction file for any automatic trigger mechanism (e.g., "on commit", "on status change", "automatic", "scheduled")
- [ ] **1c.** Confirm no self-triggering pathways exist (agent cannot invoke itself or another cross-deliverable agent without human direction)
- [ ] **1d.** Record findings per agent in the conformance matrix (Step 7)

**Input:** Four agent instruction files (Agent Type tables, PROTOCOL sections).
**Output:** Conformance matrix R-001 and R-002 cells populated per agent.

**Expected result:** All four agents require explicit human initiation. No automatic triggers found.

> **Verification boundary (Lensing X-001):** Steps 1a-1b address R-001 (absence of automatic triggers). Steps 1a, 1c address R-002 (presence of human-mediated invocation). Evaluate R-001 and R-002 as separate checks: an agent could have no automatic triggers (R-001 CONFORM) but still allow programmatic invocation without human mediation (R-002 NON-CONFORM).

### Step 2: Review Tool Root Mapping (R-003)

For each of the four agents, verify:

- [ ] **2a.** Read the `WRITE_SCOPE` declaration in the Agent Type table
- [ ] **2b.** Read the PROTOCOL section to identify actual output paths
- [ ] **2c.** Compare output paths against SPEC Section 1.2 Tool Roots table
- [ ] **2d.** Flag any tool root used by an agent that is not listed in SPEC Section 1.2
- [ ] **2e.** Record findings per agent in the conformance matrix (Step 7)

**Input:** Four agent instruction files (WRITE_SCOPE, PROTOCOL), SPEC.md Section 1.2.
**Output:** Conformance matrix R-003 cells populated per agent.

**Expected result:** AGGREGATION -> `_Aggregation/`, RECONCILIATION -> `_Reconciliation/`, ESTIMATING -> `_Estimates/` all match SPEC. SCHEDULING -> `_Schedule/` requires SPEC update (see Conflict C-001). Mark SCHEDULING R-003 as INDETERMINATE pending C-001 resolution.

### Step 3: Review Snapshot Immutability (R-004)

For each of the four agents, verify:

- [ ] **3a.** Confirm the agent creates a new snapshot folder per run (or new run summary file for RECONCILIATION)
- [ ] **3b.** Confirm the agent's non-negotiable invariants include snapshot immutability declaration
- [ ] **3c.** Confirm pointer files (`_LATEST.md`) are the only mutable files
- [ ] **3d.** Review pointer file update conditions (always, conditional, after human confirmation)
- [ ] **3e.** Record findings per agent in the conformance matrix (Step 7)

**Input:** Four agent instruction files (non-negotiable invariants, snapshot creation logic, pointer update conditions).
**Output:** Conformance matrix R-004 cells populated per agent.

**Expected result:** AGGREGATION, ESTIMATING, SCHEDULING create immutable snapshot folders. RECONCILIATION creates run summary files (valid for Type 1 agents per Specification R-004 scope clarification and Guidance C-002).

### Step 4: Review Write Quarantine (R-005)

For each of the four agents, verify:

- [ ] **4a.** Read the non-negotiable invariants section for write quarantine declarations
- [ ] **4b.** Confirm explicit prohibition against modifying deliverable files, `_STATUS.md`, decomposition outputs, and dependency registers
- [ ] **4c.** Search the PROTOCOL section for any write operations outside the declared tool root
- [ ] **4d.** Record findings per agent in the conformance matrix (Step 7)

**Input:** Four agent instruction files (non-negotiable invariants, PROTOCOL write operations).
**Output:** Conformance matrix R-005 cells populated per agent.

**Expected result:** All four agents explicitly declare write quarantine protecting source files.

### Step 5: Review Structural Conformance (R-006)

For each of the four agents, apply the SPEC Section 9 checklist:

- [ ] **5a.** `[[DOC:AGENT_INSTRUCTIONS]]` header present
- [ ] **5b.** `AGENT_TYPE: {N}` line present in body
- [ ] **5c.** Agent Type table present with all required properties (AGENT_TYPE, AGENT_CLASS, INTERACTION_SURFACE, WRITE_SCOPE, BLOCKING, PRIMARY_OUTPUTS)
- [ ] **5d.** `[[BEGIN:PROTOCOL]]` ... `[[END:PROTOCOL]]` section markers present
- [ ] **5e.** `[[BEGIN:SPEC]]` ... `[[END:SPEC]]` section markers present
- [ ] **5f.** `[[BEGIN:STRUCTURE]]` ... `[[END:STRUCTURE]]` section markers present
- [ ] **5g.** `[[BEGIN:RATIONALE]]` ... `[[END:RATIONALE]]` section markers present
- [ ] **5h.** Precedence order declared
- [ ] **5i.** Record findings per agent in the conformance matrix (Step 7)

**Input:** Four agent instruction files (full file scan for structural elements).
**Output:** Conformance matrix R-006 cells populated per agent.

> **Note (Lensing D-001):** The checklist items above (5a-5h) correspond to the SPEC Section 9 requirements and match the V-006 acceptance criteria in Specification.md. This explicit enumeration ensures assessors apply a consistent checklist rather than independently deriving items from SPEC Section 9. (Source: `docs/SPEC.md` Section 9; Specification.md V-006.)

**Expected result:** All four agents have required structural elements. Any gaps are documented for remediation (potentially deferred to DEL-06-01).

### Step 6: Review Governance Controls (R-007, R-008, R-009, R-010)

For Type 1 agents (RECONCILIATION, SCHEDULING):

- [ ] **6a.** Confirm human decision gate mechanism exists (no-autopilot rule or gate model)
- [ ] **6b.** Confirm the mechanism prevents unsupervised multi-step execution

For all four agents:

- [ ] **6c.** Confirm provenance requirements are declared (SourceRef, SourcePath, or equivalent)
- [ ] **6d.** Confirm no-invention invariant is declared
- [ ] **6e.** Confirm conflict transparency requirement is declared
- [ ] **6f.** Record findings per agent in the conformance matrix (Step 7)

**Input:** Four agent instruction files (governance controls, non-negotiable invariants).
**Output:** Conformance matrix R-007, R-008, R-009, R-010 cells populated per agent.

### Step 7: Compile Conformance Matrix

Compile findings from Steps 0-6 into a conformance matrix. Use the following status values:

| Status | Meaning |
|--------|---------|
| CONFORM | Requirement is satisfied with evidence |
| NON-CONFORM | Requirement is not satisfied; gap documented in Step 8 |
| N/A | Requirement does not apply to this agent (with justification) |
| INDETERMINATE | Cannot be determined due to unresolved conflict or missing input |
| TBD | Not yet assessed |

| Agent | R-PRE-001 | R-001 | R-002 | R-003 | R-004 | R-005 | R-006 | R-007 | R-008 | R-009 | R-010 | R-011 | Notes |
|-------|-----------|-------|-------|-------|-------|-------|-------|-------|-------|-------|-------|-------|-------|
| AGGREGATION | CONFORM | CONFORM | CONFORM | CONFORM | CONFORM | CONFORM | CONFORM | N/A (Type 2) | CONFORM | CONFORM | CONFORM | CONFORM | See `Cross_Deliverable_Workflow_Conformance_Assessment_2026-02-24.md` |
| RECONCILIATION | CONFORM | CONFORM | CONFORM | CONFORM | N/A (Type 1 run-summary model) | CONFORM | CONFORM | CONFORM | CONFORM | CONFORM | CONFORM | CONFORM | See `Cross_Deliverable_Workflow_Conformance_Assessment_2026-02-24.md` |
| ESTIMATING | CONFORM | CONFORM | CONFORM | CONFORM | CONFORM | CONFORM | CONFORM | N/A (Type 2) | CONFORM | CONFORM | CONFORM | CONFORM | See `Cross_Deliverable_Workflow_Conformance_Assessment_2026-02-24.md` |
| SCHEDULING | CONFORM | CONFORM | CONFORM | INDETERMINATE | CONFORM | CONFORM | CONFORM | CONFORM | CONFORM | CONFORM | CONFORM | CONFORM | R-003 indeterminate pending Guidance Conflict C-001 |

**N/A Justifications (Lensing X-002):**

| Agent | Requirement | N/A Justification |
|-------|------------|-------------------|
| AGGREGATION | R-007 | Type 2 TASK agent; runs straight-through without multi-step decision gates. No-autopilot controls are a Type 1 concern. (Source: `AGENT_AGGREGATION.md` Agent Type table -- AGENT_TYPE: TYPE 2) |
| ESTIMATING | R-007 | Type 2 TASK agent; runs straight-through without multi-step decision gates. No-autopilot controls are a Type 1 concern. (Source: `AGENT_ESTIMATING.md` Agent Type table -- AGENT_TYPE: TYPE 2) |

> **Systematic N/A review (Lensing X-002):** The above N/A justifications have been reviewed for completeness. R-010 (Conflict Transparency) applies equally to all four agents because all agents may encounter conflicting sources regardless of their Type classification. No additional N/A determinations are warranted beyond R-007 for Type 2 agents. Assessors should confirm this determination during the assessment and document any additional N/A findings with justification.

### Step 8: Document Gaps and Conflicts

- [ ] **8a.** List all non-conformances found
- [ ] **8b.** For each non-conformance, classify severity using the criteria below:

| Severity | Definition | Examples |
|----------|-----------|---------|
| **Critical** | Violates a CONTRACT invariant (K-WRITE-1, K-SNAP-1, K-GHOST-1, K-PROV-1, K-INVENT-1, K-CONFLICT-1) | Agent writes outside declared scope; agent invents data; agent silently resolves conflicts |
| **Major** | Violates a SPEC requirement, SOW-020 intent, or creates a conformance gap that blocks assessment | Missing INTERACTION_SURFACE declaration; tool root mismatch without conflict documentation; missing provenance fields in output schema |
| **Minor** | Structural gap, documentation inconsistency, or naming convention divergence that does not affect functional conformance | Missing section marker; inconsistent terminology; naming pattern divergence |

> **Note (Lensing A-004):** The severity criteria above replace the prior brief descriptions with measurable definitions and concrete examples. Different assessors should now classify the same finding consistently. When in doubt, escalate to the higher severity level and note the uncertainty.

- [ ] **8c.** For each non-conformance, propose a remediation:
  - Update to agent instruction file (scope of DEL-06-03)
  - Update to SPEC.md (requires change request via CHANGE)
  - Deferred to DEL-06-01 (structural conformance)

### Step 9: Prepare Change Requests (if needed)

If remediation requires changes to files outside this deliverable's scope:

- [ ] **9a.** Document the required change with exact edit/patch instructions
- [ ] **9b.** Identify the appropriate channel:
  - Agent instruction file updates: may be done directly if within DOC_UPDATE scope
  - SPEC.md updates: require change request via CHANGE agent
  - CONTRACT.md updates: require human approval and change request
- [ ] **9c.** Record the change request in this deliverable's documentation

---

## Verification

After completing Steps 0-9, verify:

- [x] All four agents have been reviewed against all applicable requirements
- [x] Conformance matrix is complete (no TBD cells remain for verified items)
- [x] All gaps are documented with severity and proposed remediation
- [x] Conflict Table in Guidance.md is current (all known conflicts listed)
- [x] Required change requests are documented
- [x] Governing document versions are recorded (Step 0c)

---

## Records

### Expected Records from This Deliverable

| Record | Description | Location |
|--------|-------------|----------|
| File Accessibility Record | Verification that all input files exist and version tracking | `Cross_Deliverable_Workflow_Conformance_Assessment_2026-02-24.md` |
| Conformance Matrix | Requirement-by-agent compliance assessment | Step 7 table in this file + `Cross_Deliverable_Workflow_Conformance_Assessment_2026-02-24.md` |
| N/A Justifications | Documented rationale for each N/A cell | Step 7 N/A Justifications table + `Cross_Deliverable_Workflow_Conformance_Assessment_2026-02-24.md` |
| Gap Analysis | Non-conformances with severity and remediation proposals | `Cross_Deliverable_Workflow_Conformance_Assessment_2026-02-24.md` |
| Change Requests | Required changes to out-of-scope files | `Cross_Deliverable_Workflow_Conformance_Assessment_2026-02-24.md` (CR-06-03-001) |
| Conflict Table | Unresolved conflicts requiring human ruling | `Guidance.md` Conflict Table |
