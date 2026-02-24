# Procedure — DEL-06-04: Change Management & Git Hygiene Support

## Purpose

This procedure describes the steps to produce the documentation updates required by DEL-06-04: ensuring CHANGE agent instructions and publication guidance constraints match "git is the event store" and human approval rules.

The procedure also describes how the resulting guidance is intended to be used by operators and agents.

## Prerequisites

| # | Prerequisite | Status |
|---|-------------|--------|
| 1 | Access to `agents/AGENT_CHANGE.md` (current CHANGE agent instruction file) | Available |
| 2 | Access to governance documents: `docs/DIRECTIVE.md`, `docs/CONTRACT.md`, `docs/SPEC.md`, `docs/TYPES.md` | Available |
| 3 | Access to `agents/AGENT_SCOPE_CHANGE.md` (for boundary review) | Available |
| 4 | Access to `agents/AGENT_HELPS_HUMANS.md` (for structural conformance requirements) | Available |
| 5 | Decomposition G7-APPROVED reviewed for DEL-06-04 context | Complete |
| 6 | Familiarity with relevant invariants: K-AUTH-1, K-AUTH-2, K-HIER-1, K-MERGE-1, K-SNAP-1, K-STALE-1, K-STALE-2, K-VAL-1, K-WRITE-1 | Required |

### Declared Upstream Dependencies

*No upstream dependencies declared in `_DEPENDENCIES.md`. Dependency extraction has not yet been run.*

**ASSUMPTION:** This deliverable depends on the governance document suite (`docs/DIRECTIVE.md`, `docs/CONTRACT.md`, `docs/SPEC.md`, `docs/TYPES.md`) being in a stable, approved state. The G7-APPROVED decomposition confirms these documents as references. **This assumption requires human confirmation** (see D-002): if the governance documents are not in an approved state, the risk should be documented and the human should confirm whether to proceed.

## Steps

### Phase A: Audit Current State

| Step | Action | Verification |
|------|--------|--------------|
| A.1 | Read `agents/AGENT_CHANGE.md` end-to-end. Identify all references to git state, approval gates, and change management behavior. | Checklist of current CHANGE behaviors documented |
| A.2 | Cross-reference CHANGE agent behaviors against DIRECTIVE Section 2.2 ("Git Is the Event Store"), Section 2.3 ("Human Authority at Every Gate"), and Section 2.5 ("No Hidden Memory"). | Gap list: any DIRECTIVE principles not reflected in CHANGE instructions |
| A.3 | Cross-reference CHANGE agent behaviors against CONTRACT invariants K-AUTH-1, K-AUTH-2, K-HIER-1, K-MERGE-1, K-SNAP-1, K-STALE-1, K-STALE-2, K-VAL-1, K-WRITE-1. | Gap list: any invariants not implemented or referenced |
| A.4 | Review CHANGE agent coordination rules against DEPENDENCIES, RECONCILIATION, and SCOPE_CHANGE agent boundaries. | Boundary clarity confirmed; any overlaps documented |
| A.5 | Review `_Change/` tool root usage in SPEC Section 1.2 and CHANGE agent Step 5 (session log). Identify any gaps between specified tool root purpose and actual CHANGE agent behavior. | Tool root usage gap list |

### Phase B: Draft Updates

| Step | Action | Verification | Intermediate Output Criteria |
|------|--------|--------------|------------------------------|
| B.1 | Draft updates to `agents/AGENT_CHANGE.md` to close gaps identified in Phase A. Ensure all requirements from Specification.md REQ-01 through REQ-08 are addressed. | Each REQ traced to a specific CHANGE instruction update | Tracing recorded as a table: REQ-ID -> CHANGE instruction section -> specific text update. Valid trace = REQ ID maps to an identified section with a described change. |
| B.2 | Draft publication guidance constraints document. At minimum, document: (a) the constraints any publication workflow must satisfy (K-AUTH-2, K-MERGE-1, K-HIER-1), (b) the approval-SHA binding mechanism, and (c) the merge precondition. Output format: a standalone constraints document (not a section within AGENT_CHANGE.md) unless the human directs otherwise. | Publication guidance constraints document exists; traces to K-AUTH-2, K-MERGE-1, K-HIER-1 | Document contains: (a) enumerated constraints with invariant cross-references, (b) at least one reference workflow example (non-binding). Valid = all three invariants cited with specific constraint language. |
| B.3 | Draft minimal git hygiene conventions: (a) working tree cleanliness expectations for CHANGE sessions, (b) commit message expectations (meaningful diffs), (c) any branch management conventions required by the invariants. | Git hygiene conventions documented | Conventions list exists with each convention traced to a source invariant or DIRECTIVE principle. |
| B.4 | Draft staleness awareness section: how CHANGE should surface staleness information and support human triage workflows. Must separately address K-STALE-1 (propagation) and K-STALE-2 (human triage with resolution modes). | Staleness guidance documented; traces to K-STALE-1, K-STALE-2, K-VAL-1 | Guidance text explicitly names K-STALE-2 resolution modes (no impact, needs rework, needs review). |
| B.5 | Review drafts for cross-document consistency with Datasheet.md, Specification.md, and Guidance.md in this deliverable folder. | Terminology, values, and invariant references consistent | Terminology check passed; invariant set matches across all documents (see Conflict Table CT-001 for pending reconciliation). |

### Phase C: Review and Finalize

| Step | Action | Verification |
|------|--------|--------------|
| C.1 | Submit draft updates for human review. The human reviews `AGENT_CHANGE.md` updates and publication guidance constraints for correctness, completeness, and appropriateness. | Human review complete |
| C.2 | Incorporate human feedback. Iterate as needed. | All feedback addressed |
| C.3 | Verify structural conformance of updated `AGENT_CHANGE.md` against `agents/AGENT_HELPS_HUMANS.md` requirements (header block, section markers, Agent Type table). | HELPS_HUMANS conformance check passes |
| C.4 | Final consistency check: confirm that updated documents do not introduce contradictions with DIRECTIVE, CONTRACT, SPEC, or other PKG-06 deliverables. | No contradictions; or contradictions captured in Conflict Table |

### Phase D: Retrospective and TBD Discharge Review

| Step | Action | Verification |
|------|--------|--------------|
| D.1 | Review all TBD items in Datasheet.md and Guidance.md. For each TBD, confirm one of: (a) resolved with evidence, (b) explicitly deferred with rationale and a responsible party, or (c) escalated to a different deliverable with a cross-reference. | TBD inventory complete; each item has a recorded disposition |
| D.2 | Review all ASSUMPTION labels in Guidance.md. For each assumption, confirm whether the discharge criteria (added in Pass 3) have been met, and record the outcome. | Assumption discharge register updated |
| D.3 | Verify that all Conflict Table items have been resolved by human ruling or explicitly deferred. | Conflict Table reviewed; no unaddressed conflicts |
| D.4 | Confirm that the deliverable's exclusion boundaries (Specification#Scope-Excludes) have not been inadvertently crossed by the delivered content. | Exclusion boundary check passed |

## Verification

| Check | What to Verify | Method |
|-------|----------------|--------|
| V.1 | All Specification requirements (REQ-01 through REQ-08) are addressed | Trace each REQ to specific document section |
| V.2 | CHANGE agent instructions reference "git is the event store" principle explicitly | Text search in updated AGENT_CHANGE.md for "git" as source of truth |
| V.3 | Approval gate mechanism includes both standard and destructive approval tokens | Review Approval Gate section for `APPROVE:` and `APPROVE_DESTRUCTIVE:` patterns |
| V.4 | Publication guidance constraints document SHA-binding and merge preconditions | Review publication guidance constraints document for K-AUTH-2 and K-MERGE-1 references |
| V.5 | Snapshot immutability convention is acknowledged for `_Change/` outputs | Review CHANGE agent output conventions for K-SNAP-1 compliance |
| V.6 | Staleness model is acknowledged with K-STALE-1 propagation and K-STALE-2 human triage separately verified | Review staleness guidance section for both invariants |
| V.7 | Separation of concerns between CHANGE, DEPENDENCIES, RECONCILIATION, and SCOPE_CHANGE is clear | Review coordination rules for non-overlapping authority |
| V.8 | No new content is asserted as fact without source citation or ASSUMPTION label | Full document review |
| V.9 | All TBDs resolved or explicitly deferred with rationale (Phase D) | TBD inventory review |
| V.10 | Exclusion boundaries not crossed by deliverable content | Cross-reference deliverable content against Specification exclusion list |

## Records

| Record | Location | Purpose |
|--------|----------|---------|
| Updated `agents/AGENT_CHANGE.md` | `agents/AGENT_CHANGE.md` (repo root) | Primary deliverable artifact |
| Publication guidance constraints | `docs/CHANGE_PUBLICATION_GUIDANCE_CONSTRAINTS.md` | Formalized publication workflow constraints |
| Git hygiene conventions | TBD -- may be embedded in AGENT_CHANGE.md or in a separate guidance document | Minimal git hygiene standards |
| TBD discharge register | `{DEL-06-04 folder}/` or within Datasheet.md | Record of TBD resolution/deferral decisions |
| Assumption discharge register | `{DEL-06-04 folder}/` or within Guidance.md | Record of assumption confirmation/invalidation |
| Human sign-off | TBD -- format to be determined during Phase C | Evidence of human review and approval |
| This Procedure | `{DEL-06-04 folder}/Procedure.md` | Execution workflow record |
| Deliverable status | `{DEL-06-04 folder}/_STATUS.md` | Lifecycle tracking |
