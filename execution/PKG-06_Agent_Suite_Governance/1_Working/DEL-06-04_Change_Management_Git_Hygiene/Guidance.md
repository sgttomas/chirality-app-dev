# Guidance — DEL-06-04: Change Management & Git Hygiene Support

## Purpose

This deliverable exists to ensure that the CHANGE agent's instructions and any publication guidance are fully aligned with two foundational Chirality principles:

1. **Git is the event store** -- if a decision is not in a versioned file, it does not exist for purposes of reliance (DIRECTIVE Section 2.2).
2. **Human authority at every gate** -- agents propose, humans approve; professional liability is personal and non-transferable (DIRECTIVE Section 2.3).

The CHANGE agent is the primary human-facing interface for managing project file state under parallel development. Its instructions must faithfully implement the governance model: legible state, explicit approval, auditable history.

Source: Decomposition DEL-06-04 entry; `docs/DIRECTIVE.md` Sections 2.2, 2.3

## Principles

### P1: Git State Is the Single Source of Truth for Changes

The CHANGE agent treats git (branches, commits, diffs, staging area) as the authoritative record of what changed, when, and by whom. This is not a convention preference; it is a structural constraint (DIRECTIVE Section 2.2).

Implications:
- No change tracking outside of git-tracked files.
- Session logs written to `_Change/` are supplementary audit artifacts, not authoritative state.
- Meaningful commit messages and reviewable diffs are the primary mechanism for change legibility.

### P2: Approval Is Explicit, Bound, and Non-Delegable

The approval gate mechanism in CHANGE exists because of K-AUTH-1 (only humans author binding approval records) and K-AUTH-2 (approvals bind to a specific git SHA). The `APPROVE:` / `APPROVE_DESTRUCTIVE:` token pattern ensures:

- No accidental or implicit execution of state-changing actions.
- The human explicitly names what they are approving.
- Destructive actions receive heightened scrutiny.

### P3: Separation of Change Management from Dependency Governance

CHANGE manages file/git state and change legibility. It does not own dependency extraction (DEPENDENCIES agent), dependency closure review (RECONCILIATION agent), or scope change governance (SCOPE_CHANGE agent). This separation prevents a single agent from accumulating excessive authority and keeps each role auditable.

Source: `agents/AGENT_CHANGE.md` Non-negotiable invariants; Coordination rules

### P4: Immutable Snapshots Preserve Audit Trail

When CHANGE writes outputs to the `_Change/` tool root, those outputs follow the snapshot immutability convention (K-SNAP-1, SPEC Section 11). This means every change management session produces a permanent, immutable record. Reruns do not overwrite previous records.

## Considerations

### C1: Publication Workflow Is Not Yet Fully Codified

The current governance suite defines the invariants for publication (K-AUTH-2, K-MERGE-1) but does not prescribe a specific publication workflow (branch naming conventions, review ceremony, merge process). This deliverable should either:

- Define a minimal publication workflow consistent with the invariants, or
- Document that the publication workflow is project-instance-configurable and specify the constraints any workflow must satisfy.

**ASSUMPTION:** A minimal publication workflow definition is within scope of this deliverable. The workflow will be constraints-based (what any publication path must satisfy) rather than prescriptive (a single mandated branching model).

**Discharge criteria:** This assumption is confirmed when the human approves the publication guidance constraints document produced by Phase B. It is invalidated if the human determines that publication workflow definition belongs to a different deliverable or requires a prescriptive model instead.

### C2: Relationship Between CHANGE Agent and _Change/ Tool Root

The `_Change/` tool root (SPEC Section 1.2) is listed as the typical writer target for the CHANGE agent. However, the current CHANGE agent instructions define session log writing as optional (`WRITE_LOG_TO` parameter). This deliverable should clarify:

- When session logging should be used vs. omitted.
- What constitutes a change record vs. a session log.
- Whether additional record types belong in `_Change/` (e.g., publication records, approval records).

**ASSUMPTION:** This clarification is within scope.

### C3: Git Hygiene Conventions Are Implicit

The current codebase uses git but does not codify git hygiene conventions (branch naming, commit message format, working tree cleanliness expectations). The CHANGE agent's Step 1 collects git state evidence, but the interpretation of "clean" vs. "messy" state is left to agent judgment. This deliverable should consider whether minimal git hygiene conventions should be documented.

**ASSUMPTION:** Minimal conventions (not a full branching strategy) are within scope.

**Discharge criteria:** This assumption is confirmed when the human approves the scope of git hygiene conventions in Phase B output. It is invalidated if the human determines that only invariant-required behaviors (no additional conventions) are appropriate.

### C4: Staleness and Dirty State Are Currently Manual

K-STALE-1 and K-VAL-1 define staleness propagation and dirty-state detection, but automated tooling does not yet exist (see PLAN Section 3.7, DEL-08-07 TBD scope). This deliverable should ensure that CHANGE agent guidance acknowledges the staleness model and supports manual triage workflows, without depending on tooling that does not yet exist.

### C5: AGENT_SCOPE_CHANGE.md Coordination

`agents/AGENT_SCOPE_CHANGE.md` handles scope modifications (adding/removing/modifying scope items, deliverables, packages). This deliverable should ensure clear boundaries between CHANGE (file/git state management) and SCOPE_CHANGE (scope governance). The two agents should not overlap in their authority claims.

**ASSUMPTION:** Reviewing the CHANGE/SCOPE_CHANGE boundary is within scope; modifying AGENT_SCOPE_CHANGE.md is not.

**Discharge criteria:** This assumption is confirmed when Phase A.4 boundary review produces no overlap findings, or when the human approves the boundary clarification in Phase B output. It is invalidated if the review reveals that AGENT_SCOPE_CHANGE.md must be modified to resolve overlaps.

## Trade-offs

### T1: Prescriptive vs. Constraints-Based Publication Guidance

| Option | Pros | Cons |
|--------|------|------|
| **Prescriptive** (define a specific branching model) | Clear, unambiguous, easy to follow | May not fit all project instances; reduces flexibility |
| **Constraints-based** (define what any workflow must satisfy) | Flexible, adaptable to different team sizes and workflows | Requires more judgment from operators; less concrete |

**ASSUMPTION (best-effort mapping):** The constraints-based approach aligns better with the Chirality design philosophy, which defines invariants and lets project instances configure within those bounds. The specific reasoning chain is:

1. K-GATE-1 establishes that "gates are dynamic per project instance" and that additional gates are project-configurable (`docs/CONTRACT.md` Section 1.7).
2. This gate-configurability principle implies that publication workflows (which are a form of gate) should also be configurable rather than mandated.
3. Therefore, the publication guidance should define the invariant constraints (K-AUTH-2 SHA binding, K-MERGE-1 merge precondition, K-HIER-1 flat hierarchy) and allow the specific workflow to be project-configured.

The deliverable should document constraints and optionally provide a reference workflow as a non-binding example.

**Discharge criteria:** This assumption is confirmed when the human approves the constraints-based format. It is invalidated if the human requires a prescriptive branching model for this project instance.

Source: `docs/CONTRACT.md` K-GATE-1, Section 1.7

### T2: Depth of Git Hygiene Conventions

| Option | Pros | Cons |
|--------|------|------|
| **Minimal** (just the invariant-required behaviors) | Keeps scope bounded; avoids overspecification | Leaves operators to develop their own conventions |
| **Comprehensive** (branch naming, commit format, PR templates, etc.) | Provides turnkey git workflow | Exceeds DOC_UPDATE scope; may conflict with team preferences |

**ASSUMPTION:** Minimal conventions that ensure invariant compliance are appropriate for M-envelope scope.

**Rationale for TBD status of git hygiene conventions in Datasheet Construction:** The conventions are listed as TBD because the Chirality governance model intentionally separates invariants (which are binding) from conventions (which are project-configurable). DIRECTIVE Section 2.2 establishes the principle ("git is the event store") but does not prescribe specific hygiene conventions. The scope boundary selected (minimal, invariant-required behaviors only) follows the same reasoning as T1: K-GATE-1's configurability principle extends to conventions that are not themselves invariants.

Source: `docs/DIRECTIVE.md` Section 2.2; `docs/CONTRACT.md` K-GATE-1

**Discharge criteria:** This assumption is confirmed when the human approves the depth of git hygiene conventions in Phase B output. It is invalidated if the human requests comprehensive conventions.

## Examples

**Categories for future examples** (to be developed during IN_PROGRESS phase):

1. **Publication workflow example:** A reference constraints-compliant publication path showing branch creation, approval-SHA binding verification, and merge ceremony -- illustrating how the invariant constraints (K-AUTH-2, K-MERGE-1) are satisfied in practice.
2. **Change session log example:** A sample session log from `_Change/` demonstrating the format, approval token capture, and SHA binding record.
3. **Git hygiene pattern example:** A before/after comparison showing how the CHANGE agent's Step 1 git state evidence collection supports clean working tree assessment.
4. **Staleness triage example:** A scenario demonstrating manual staleness triage per K-STALE-2 resolution modes (no impact, needs rework, needs review).

**ASSUMPTION:** Concrete examples will be populated when the deliverable transitions to IN_PROGRESS and the human provides or approves real-world scenarios. Placeholder categories are provided to support comprehensive value appraisal of the deliverable scope.

## Conflict Table (for human ruling)

| Conflict ID | Conflict | Source A | Source B | Impacted Sections | Proposed Authority (PROPOSAL) | Human Ruling |
|-------------|----------|----------|----------|-------------------|-------------------------------|-------------|
| CT-001 (X-002/X-003) | Governing invariant set mismatch: Datasheet Attributes lists K-WRITE-1 but not K-HIER-1; Specification REQ-07 references K-HIER-1 but no requirement references K-WRITE-1. The complete invariant set must be reconciled across both documents. | Datasheet.md#Attributes (lists K-AUTH-1, K-AUTH-2, K-MERGE-1, K-SNAP-1, K-STALE-1, K-STALE-2, K-VAL-1, K-WRITE-1) | Specification.md#REQ-07 (references K-HIER-1); Specification.md#Standards (lists K-WRITE-1 in CONTRACT row but no REQ references it) | Datasheet#Attributes, Specification#REQ-07, Specification#REQ-08 (new), Specification#Standards | Human -- both K-HIER-1 and K-WRITE-1 appear relevant based on CONTRACT.md evidence; Datasheet has been updated to include both pending human confirmation | TBD |
| CT-002 (B-003) | Terminology inconsistency for the publication workflow output artifact: "publication guidance document or section" (Specification#Documentation), "publication guidance section or document" (Procedure#Phase-B), "Publication Workflow" (Guidance#C1). Three different phrasings refer to the same deliverable output. | Specification.md#Documentation | Procedure.md#Phase-B, Guidance.md#C1 | Specification#Documentation, Procedure#Phase-B, Procedure#Records, Guidance#C1 | Guidance -- proposed canonical term: "publication guidance constraints" (reflecting the constraints-based approach from T1). Specification and Procedure have been updated to use this term pending human confirmation. | TBD |
| CT-003 (E-003) | Terminology inconsistency for the CHANGE agent's primary function: "file/git state management" (Guidance#P3), "file-state changes" (Specification#REQ-01), "change legibility" (Guidance#P1/Purpose). Three overlapping terms describe the core function. | Datasheet.md#Attributes, Specification.md#REQ-01 | Guidance.md#P3, Guidance.md#Purpose | Datasheet#Attributes, Specification#REQ-01, Specification#REQ-06, Guidance#P3, Guidance#Purpose | Guidance -- requires human selection of a single canonical term. Current usage retained pending ruling. | TBD |
