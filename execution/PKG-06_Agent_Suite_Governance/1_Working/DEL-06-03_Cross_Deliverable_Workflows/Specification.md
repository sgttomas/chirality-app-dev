# Specification -- DEL-06-03 Cross-Deliverable Workflow Support

## Scope

### Included

This deliverable covers the documentation and conformance assessment of the four cross-deliverable workflow agents:

1. **AGGREGATION** -- cross-file rollups, estimate collation, and register consolidation
2. **RECONCILIATION** -- cross-deliverable dependency integrity and agent instruction coherence
3. **ESTIMATING** -- automated estimate snapshot generation
4. **SCHEDULING** -- schedule skeleton generation from decomposition and dependency data

The focus is ensuring these workflows are:
- opt-in and human-triggered (SOW-020),
- writing immutable snapshot outputs under correct tool roots (SPEC Section 1.2, Section 11; CONTRACT K-SNAP-1),
- conformant with AGENT_HELPS_HUMANS structure and the governance suite.

Source: decomposition DEL-06-03 entry; SOW-020.

### Excluded

- Implementation of agent runtime code (harness, SDK integration) -- covered by PKG-03
- Deliverable-local workflow agents (PREPARATION, 4_DOCUMENTS, semantic agents) -- covered by DEL-06-02
- Change management workflows -- covered by DEL-06-04
- Future hardening features (locks, staleness, graph tooling) -- covered by PKG-08

---

## Requirements

### Preconditions

#### R-PRE-001: Governing Document Availability (Lensing C-001)

Before conformance assessment can be considered valid, the following governing documents MUST be accessible and their versions recorded:

| Document | Required Location | Version Tracking |
|----------|------------------|-----------------|
| SPEC.md | `docs/SPEC.md` | Record the version/date at assessment time |
| CONTRACT.md | `docs/CONTRACT.md` | Record the version/date at assessment time |
| DIRECTIVE.md | `docs/DIRECTIVE.md` | Record the version/date at assessment time |

If any governing document changes after assessment, the affected conformance findings MUST be re-evaluated against the updated version.

**Rationale:** R-003 references SPEC Section 1.2 and R-005 references CONTRACT K-WRITE-1. Without establishing that these documents exist at a known version, conformance results may be invalidated by subsequent changes. (Source: Specification.md R-003, R-005 evidence citations; version capture recorded in `Cross_Deliverable_Workflow_Conformance_Assessment_2026-02-24.md`.)

**Verification:** Procedure Step 0 (file accessibility check)

---

### R-001: Opt-In Invocation

Each cross-deliverable workflow agent MUST require explicit human initiation. No cross-deliverable workflow SHALL execute automatically (e.g., on commit, on folder change, or on status transition).

**Evidence:**
- SOW-020: "Support cross-deliverable operations as opt-in, human-triggered workflows" (Source: decomposition SSOW table)
- DIRECTIVE Section 2.3: "Agents propose; humans approve" (Source: `docs/DIRECTIVE.md`)

**Verification:** V-001

### R-002: Human-Triggered Execution

Each cross-deliverable workflow agent MUST be triggered through one of the following mechanisms:
- Direct human conversation (`INTERACTION_SURFACE: chat`)
- Human-composed or human-approved brief (`INTERACTION_SURFACE: INIT-TASK`)

No agent in scope SHALL self-trigger or trigger another cross-deliverable workflow without human direction.

**Evidence:**
- SOW-020 (Source: decomposition SSOW table)
- AGENT_HELPS_HUMANS Type classification model (Source: `agents/AGENT_HELPS_HUMANS.md`)

**Verification:** V-002

> **Verification boundary note (Lensing X-001):** V-001 and V-002 address closely related but distinct aspects of human control. V-001 verifies the **absence of automatic triggers** (no commit hooks, no status-change listeners, no scheduled execution). V-002 verifies the **presence of human-mediated invocation surfaces** (chat or INIT-TASK). An agent could satisfy V-001 (no automatic triggers) while failing V-002 (e.g., if it accepted programmatic API calls without human direction). Assessors should evaluate V-001 and V-002 as separate checks with distinct pass/fail conditions.

### R-003: Correct Tool Root Mapping

Each cross-deliverable workflow agent MUST write outputs exclusively to its designated tool root as specified in SPEC Section 1.2:

| Agent | Tool Root |
|-------|-----------|
| AGGREGATION | `_Aggregation/` |
| RECONCILIATION | `_Reconciliation/` |
| ESTIMATING | `_Estimates/` |
| SCHEDULING | `_Schedule/` (**ASSUMPTION** -- see Conflict C-001 in Guidance.md; `_Schedule/` is not yet listed in SPEC Section 1.2) |

**Evidence:**
- SPEC Section 1.2 Tool Roots table (Source: `docs/SPEC.md`)
- Each agent's WRITE_SCOPE declaration (Source: respective instruction files)

**Verification:** V-003

### R-004: Immutable Snapshot Outputs

Cross-deliverable workflow agents that produce snapshot outputs MUST create new, immutable snapshot folders for each run. Snapshot folders MUST NOT be overwritten or modified after creation.

Pointer files (`_LATEST.md`) are the only mutable files and MAY be overwritten per the conditions specified in each agent's instructions.

> **Scope clarification (Lensing A-001):** This requirement applies to agents that produce structured snapshot artifacts (AGGREGATION, ESTIMATING, SCHEDULING). RECONCILIATION produces run summary files (`Reconciliation_Run_Summary_{RunID}.md`) rather than snapshot folders. RECONCILIATION's run summaries are NOT considered "snapshot outputs" under K-SNAP-1, as K-SNAP-1 applies to "task agent outputs to tool roots" and RECONCILIATION is a Type 1 persona agent. RECONCILIATION's run summaries are nonetheless preserved as immutable individual files per `AGENT_RECONCILIATION.md` Step 6. See Guidance C-002 for the design rationale. (Source: `AGENT_RECONCILIATION.md` Output Persistence section; `docs/CONTRACT.md` K-SNAP-1 text.)

**Evidence:**
- SPEC Section 11.1: "Snapshot folders are immutable after creation. Reruns create new snapshot folders." (Source: `docs/SPEC.md`)
- CONTRACT K-SNAP-1: "Task agent outputs to tool roots are immutable snapshots. Pointer files may be overwritten; snapshot folders must not." (Source: `docs/CONTRACT.md`)

**Verification:** V-004

### R-005: Write Quarantine (Source Protection)

No cross-deliverable workflow agent SHALL modify:
- Deliverable working files (any content under deliverable folders)
- Lifecycle files (`_STATUS.md`)
- Decomposition outputs
- Dependency registers

**Evidence:**
- CONTRACT K-WRITE-1: "Every agent has an explicit write scope declared in its header block. No agent writes outside its declared zone." (Source: `docs/CONTRACT.md`)
- Each agent's non-negotiable invariants (Source: respective instruction files)

**Verification:** V-005

### R-006: AGENT_HELPS_HUMANS Structural Conformance

Each cross-deliverable workflow agent instruction file MUST conform to the structural requirements defined in SPEC Section 9:
- Required header (`[[DOC:AGENT_INSTRUCTIONS]]`, AGENT_TYPE line)
- Required Agent Type table (AGENT_TYPE, AGENT_CLASS, INTERACTION_SURFACE, WRITE_SCOPE, BLOCKING, PRIMARY_OUTPUTS)
- Required sections (PROTOCOL, SPEC, STRUCTURE, RATIONALE with section markers)
- Precedence order declared

**Evidence:**
- SPEC Section 9 (Source: `docs/SPEC.md`)
- SOW-031 applies broadly to agent conformance; DEL-06-03 contributes the cross-deliverable subset (Source: decomposition)

**Verification:** V-006

### R-007: No-Autopilot Controls for Type 1 Agents

Cross-deliverable workflow agents classified as Type 1 (RECONCILIATION, SCHEDULING) MUST implement explicit human decision gates that prevent unsupervised multi-step execution:
- RECONCILIATION: no-autopilot rule (at most one Type 2 dispatch per cycle unless human provides explicit multi-step plan)
- SCHEDULING: 5-gate model with human confirmation required at each gate

**Evidence:**
- AGENT_RECONCILIATION.md no-autopilot rule (Source: `agents/AGENT_RECONCILIATION.md`)
- SCHEDULING.md gate model (Source: `.claude/agents/SCHEDULING.md`)

**Verification:** V-007

### R-008: Provenance and Traceability in Outputs

Cross-deliverable workflow agent outputs MUST preserve provenance:
- AGGREGATION: every aggregated record must include `SourcePath` + best-effort `SectionRef` or `location TBD` (Source: `AGENT_AGGREGATION.md` non-negotiable invariants)
- ESTIMATING: every priced line item must include `SourceRef` or `location TBD` (Source: `AGENT_ESTIMATING.md` non-negotiable invariants; CONTRACT K-PROV-1)
- RECONCILIATION: claims must be traceable to Type 2 task artifacts or file locations (Source: `AGENT_RECONCILIATION.md` non-negotiable invariants)
- SCHEDULING: every schedule item must trace to source Package/Deliverable; every constraint edge to dependency rows or human constraints (Source: `SCHEDULING.md` non-negotiable invariants)

**Verification:** V-008

### R-009: No Invention of Facts

Cross-deliverable workflow agents MUST NOT invent scope items, dependency targets, parameter values, rates, quantities, durations, or engineering content. Missing or ambiguous data MUST be recorded as `TBD` or `UNKNOWN`.

**Evidence:**
- CONTRACT K-INVENT-1 (Source: `docs/CONTRACT.md`)
- Each agent's non-negotiable invariants (Source: respective instruction files)

**Verification:** V-009

### R-010: Conflict Transparency

Cross-deliverable workflow agents MUST NOT silently resolve conflicts. Conflicts between sources MUST be surfaced with pointers to conflicting sources.

**Evidence:**
- CONTRACT K-CONFLICT-1 (Source: `docs/CONTRACT.md`)
- AGGREGATION: "Conflict transparency. Never 'resolve' conflicts by deletion" (Source: `AGENT_AGGREGATION.md`)
- RECONCILIATION: "Deterministic synthesis. If Type 2 outputs disagree, report conflicts clearly" (Source: `AGENT_RECONCILIATION.md`)

**Verification:** V-010

### R-011: Error Handling for Unavailable Inputs (Lensing C-002)

Cross-deliverable workflow agents MUST define expected behavior when encountering unavailable or degraded inputs:

| Failure Mode | Expected Behavior |
|-------------|-------------------|
| Source deliverable folder missing or inaccessible | Agent MUST report the missing input and halt or skip the affected scope item; MUST NOT proceed with invented data |
| Dependency target unresolvable | Agent MUST record the dependency as `UNRESOLVABLE` or `TBD` and continue with remaining scope |
| Tool root inaccessible or uncreatable | Agent MUST halt and report the infrastructure failure; MUST NOT write to alternative locations |

**Rationale:** Requirements R-001 through R-010 address normal-path governance but do not address failure modes. Cross-deliverable agents that encounter missing inputs or inaccessible tool roots have no documented expected behavior under the current requirements. (Source: Specification.md requirements scan; **ASSUMPTION** -- specific agent error-handling patterns inferred from general no-invention and write-quarantine invariants.)

**Verification:** V-011

---

## Standards

| Standard/Reference | Applicability | Location |
|-------------------|--------------|----------|
| AGENT_HELPS_HUMANS.md | Structural conformance for all agent instruction files | `agents/AGENT_HELPS_HUMANS.md` |
| SPEC.md Section 1.2 | Tool root layout definitions | `docs/SPEC.md` |
| SPEC.md Section 9 | Agent instruction file structure requirements | `docs/SPEC.md` |
| SPEC.md Section 11 | Snapshot and pointer conventions | `docs/SPEC.md` |
| CONTRACT.md | K-WRITE-1, K-SNAP-1, K-GHOST-1, K-PROV-1, K-INVENT-1, K-CONFLICT-1 | `docs/CONTRACT.md` |
| DIRECTIVE.md Section 2.3 | Human authority at every gate | `docs/DIRECTIVE.md` |
| TYPES.md Section 4 | Agent type classification model | `docs/TYPES.md` |

---

## Verification

| VerificationID | Requirement | Approach | Acceptance Criteria | Status |
|---------------|-------------|----------|-------------------|--------|
| V-001 | R-001 (Opt-In Invocation) | Review each agent instruction file for INTERACTION_SURFACE declaration; confirm no automatic trigger mechanisms exist | PASS: All four agents declare `chat` or `INIT-TASK` as INTERACTION_SURFACE AND no automatic trigger keywords (on commit, on push, on status change, scheduled, cron, automatic) found in instruction files. FAIL: Any agent has an undeclared or automatic invocation surface. | PASS (2026-02-24 assessment) |
| V-002 | R-002 (Human-Triggered Execution) | Review invocation surfaces; confirm all are `chat` or `INIT-TASK`; confirm no self-triggering pathways | PASS: All invocation pathways require human initiation (conversation start or brief composition) AND no agent can invoke itself or another cross-deliverable agent without human direction. FAIL: Any programmatic or agent-to-agent invocation pathway exists without human mediation. | PASS (2026-02-24 assessment) |
| V-003 | R-003 (Correct Tool Root) | Compare each agent's WRITE_SCOPE and actual output paths against SPEC Section 1.2; flag discrepancies | PASS: All output paths match SPEC Section 1.2 tool roots OR discrepancies are documented in Conflict Table with proposed resolution. FAIL: Undocumented tool root divergence. | PASS (C-001 documented; SCHEDULING remains R-003 INDETERMINATE pending SPEC update) |
| V-004 | R-004 (Immutable Snapshots) | Review snapshot creation patterns; confirm new folder per run; confirm no overwrite logic | PASS: Each applicable agent creates new timestamped folder per run AND no overwrite/modify logic exists for prior snapshots AND pointer files are the only mutable files. FAIL: Any snapshot modification or overwrite logic found. | PASS (2026-02-24 assessment) |
| V-005 | R-005 (Write Quarantine) | Review each agent's non-negotiable invariants for source protection declarations; confirm no write paths to deliverable folders | PASS: Each agent explicitly declares write quarantine AND no code paths write to deliverable folders, `_STATUS.md`, decomposition, or dependency files. FAIL: Missing write quarantine declaration OR write path to protected zone found. | PASS (2026-02-24 assessment) |
| V-006 | R-006 (Structural Conformance) | Apply SPEC Section 9 checklist to each instruction file: (a) `[[DOC:AGENT_INSTRUCTIONS]]` header, (b) `AGENT_TYPE` line, (c) Agent Type table with all 6 properties, (d) `[[BEGIN:PROTOCOL]]`/`[[END:PROTOCOL]]` markers, (e) `[[BEGIN:SPEC]]`/`[[END:SPEC]]` markers, (f) `[[BEGIN:STRUCTURE]]`/`[[END:STRUCTURE]]` markers, (g) `[[BEGIN:RATIONALE]]`/`[[END:RATIONALE]]` markers, (h) precedence order declared | PASS: All 8 checklist items present in all four instruction files. FAIL: Any checklist item missing from any instruction file. (Source: Procedure Step 5 enumerates these items; `docs/SPEC.md` Section 9.) | PASS (2026-02-24 assessment) |
| V-007 | R-007 (No-Autopilot Controls) | Review RECONCILIATION no-autopilot rule; review SCHEDULING gate model; confirm human decision gates exist | PASS: RECONCILIATION declares no-autopilot rule with explicit dispatch limit AND SCHEDULING declares gate model with human confirmation at each gate. FAIL: Missing or incomplete human decision gate mechanism. | PASS (2026-02-24 assessment) |
| V-008 | R-008 (Provenance) | Review output schemas for provenance fields; confirm `SourceRef`/`SourcePath` requirements | PASS: Each agent's output schema includes provenance fields (SourcePath, SourceRef, or equivalent) AND non-negotiable invariants require provenance. FAIL: Missing provenance requirements in any agent's output schema. | PASS (2026-02-24 assessment) |
| V-009 | R-009 (No Invention) | Review each agent's non-negotiable invariants for no-invention declarations | PASS: Each agent explicitly declares no-invention invariant covering its domain-specific data types. FAIL: Missing no-invention declaration in any agent. | PASS (2026-02-24 assessment) |
| V-010 | R-010 (Conflict Transparency) | Review each agent's conflict handling declarations; confirm conflicts are surfaced not resolved | PASS: Each agent declares conflict transparency requirement AND instruction file contains mechanism for surfacing conflicts (conflict tables, warning markers, or equivalent). FAIL: Any agent silently resolves or suppresses conflicts. | PASS (2026-02-24 assessment) |
| V-011 | R-011 (Error Handling) | Review each agent's instruction file for error/failure mode handling; confirm degraded-input behavior is defined | PASS: Each agent defines behavior for missing inputs, unresolvable dependencies, and inaccessible tool roots consistent with R-011 table. FAIL: No defined error-handling behavior. (**ASSUMPTION** -- acceptance criteria derived from R-011 requirements.) | PASS (2026-02-24 assessment) |
| V-PRE-001 | R-PRE-001 (Governing Document Availability) | Confirm all three governing documents exist at expected paths and record their versions | PASS: SPEC.md, CONTRACT.md, DIRECTIVE.md all accessible with versions recorded. FAIL: Any governing document missing or version not recorded. | PASS (2026-02-24 assessment) |

> **Note (Lensing A-002):** All verification entries now include explicit acceptance criteria defining PASS vs. FAIL conditions. This enables objective population of the conformance matrix in Procedure Step 7. Prior to enrichment, verification approaches were listed without acceptance criteria.

---

## Documentation

### Required Artifacts (from _CONTEXT.md)

| Artifact Type | Description | Status |
|--------------|-------------|--------|
| DOC | Documentation updates ensuring cross-deliverable workflow conformance | IN_PROGRESS (`Cross_Deliverable_Workflow_Conformance_Assessment_2026-02-24.md` produced) |

### Expected Outputs of This Deliverable

1. Conformance assessment of all four cross-deliverable workflow agent instruction files against SOW-020 requirements
2. Documentation of any gaps, conflicts, or required updates
3. Updated agent instruction files (if changes are needed) or change requests for CHANGE agent

### Output Artifact Register (Lensing F-002)

| Artifact | Filename/Pattern | Format | Acceptance Criteria | Status |
|----------|-----------------|--------|-------------------|--------|
| Completed conformance matrix | Procedure.md Step 7 (populated) | Markdown table | All cells populated with CONFORM, NON-CONFORM, N/A, or INDETERMINATE (no TBD remaining for assessed items) | COMPLETE (2026-02-24) |
| Gap analysis | `Cross_Deliverable_Workflow_Conformance_Assessment_2026-02-24.md` | Markdown list with severity classifications | All non-conformances classified as Critical/Major/Minor with proposed remediations | COMPLETE (2026-02-24; no NON-CONFORM findings, one INDETERMINATE conflict C-001) |
| Change requests (if needed) | `Cross_Deliverable_Workflow_Conformance_Assessment_2026-02-24.md` | Markdown with edit instructions | Each change request specifies target file, exact change, and approval channel | COMPLETE (CR-06-03-001 logged) |
| Updated Conflict Table | Guidance.md Conflict Table | Markdown table | All known conflicts listed; new conflicts from assessment added | COMPLETE (existing C-001 retained) |

> **Note (Lensing F-002):** This register defines the concrete artifacts that constitute "done" for this deliverable's documentation outputs. See also Lensing D-003 for deliverable-level exit criteria.

### Exit Criteria (Lensing D-003)

This deliverable is considered complete when ALL of the following conditions are met:

1. **Conformance matrix populated:** All cells in the Step 7 conformance matrix contain CONFORM, NON-CONFORM, N/A, or INDETERMINATE -- no TBD cells remain for items that have been assessed
2. **Gaps documented:** All non-conformances are documented in Step 8 with severity classification (Critical/Major/Minor) and proposed remediation
3. **Change requests filed:** All required out-of-scope changes have documented change requests (Step 9) with target file, change description, and approval channel identified
4. **Conflict Table current:** Guidance.md Conflict Table reflects all conflicts discovered during assessment
5. **Human review:** The conformance assessment has been reviewed and accepted by the responsible party (recorded in `_STATUS.md`)

> **Note (Lensing D-003):** Criteria 1-4 are verifiable by the agent; criterion 5 requires human action. The deliverable transitions to COMPLETE only after human acceptance. The specific acceptance mechanism (e.g., _STATUS.md state transition, sign-off comment) is TBD -- this is a project governance decision. (Source: Specification.md Documentation section; **ASSUMPTION** -- exit criteria derived from expected outputs and procedure steps.)

### Formal Acceptance Mechanism (Lensing E-001)

The completed conformance assessment MUST be formally accepted before the deliverable can transition to COMPLETE status:

| Step | Action | Actor | Record |
|------|--------|-------|--------|
| 1 | Review completed conformance matrix and gap analysis | Responsible Party (TBD) | Review comments (if any) |
| 2 | Confirm all critical/major non-conformances have remediation plans | Responsible Party | Acceptance recorded in `_STATUS.md` history |
| 3 | Approve deliverable state transition to COMPLETE | Responsible Party | `_STATUS.md` updated per lifecycle rules |

> **Note (Lensing E-001):** Without a formal sign-off mechanism, the assessment lacks certified sufficiency -- the work could be done but never formally acknowledged as complete. The mechanism above is a PROPOSAL; the specific approval workflow depends on project governance. (`location TBD` for formal approval process definition.)
