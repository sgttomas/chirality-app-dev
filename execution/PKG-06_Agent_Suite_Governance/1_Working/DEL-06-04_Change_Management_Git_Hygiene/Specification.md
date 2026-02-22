# Specification — DEL-06-04: Change Management & Git Hygiene Support

## Scope

### What This Deliverable Covers

This deliverable ensures that the CHANGE agent's instructions and any associated publication guidance are aligned with the Chirality system's founding principles:

1. **"Git is the event store"** -- version control provides the development record for review, reproducibility, rollback, and audits (DIRECTIVE Section 2.2).
2. **Human approval rules** -- agents propose, humans approve; approvals bind to specific git SHAs (CONTRACT K-AUTH-1, K-AUTH-2).
3. **Merge discipline** -- merge to main is allowed only when branch HEAD equals the approved SHA (CONTRACT K-MERGE-1).

The deliverable covers documentation updates (DOC_UPDATE type) to agent instructions and publication guidance. It does not implement new tooling or automated enforcement mechanisms.

Source: Decomposition DEL-06-04 entry; `_CONTEXT.md`

### What This Deliverable Excludes

- Automated CI enforcement of K-MERGE-1 (future tooling; see `docs/PLAN.md`)
- Staleness propagation tooling (DEL-08-07, TBD scope)
- Content hash verification for references (DEL-08-01, TBD scope)
- Dependency governance (owned by DEPENDENCIES and RECONCILIATION agents)
- Scope change management (owned by AGENT_SCOPE_CHANGE.md)

## Requirements

### REQ-01: CHANGE Agent Alignment with "Git Is the Event Store"

The CHANGE agent instruction file (`agents/AGENT_CHANGE.md`) MUST reflect the principle that git version control is the authoritative development record. Specifically:

- The agent MUST treat git state (branch, HEAD, staging area, working tree) as the primary source of truth for file-state changes.
- The agent MUST produce meaningful, reviewable diffs as its primary output.
- The agent MUST NOT maintain or rely on any private state outside of git-tracked files for change tracking purposes.

Source: `docs/DIRECTIVE.md` Section 2.2 ("Git Is the Event Store"); `docs/DIRECTIVE.md` Section 2.5 ("No Hidden Memory")

### REQ-02: Human Approval Gate for State-Changing Actions

The CHANGE agent MUST require explicit human approval before executing any state-changing action (git commands, file edits). The approval mechanism MUST include:

- An explicit `APPROVE:` token with an action list for standard actions.
- An escalated `APPROVE_DESTRUCTIVE:` token with risk restatement for destructive/irreversible actions.
- A prohibition on executing state-changing actions when `ALLOW_EXECUTION=FALSE`.
- **The `ALLOW_EXECUTION` parameter MUST default to `FALSE`.** When `ALLOW_EXECUTION=FALSE`, CHANGE MUST NOT execute git actions or apply file edits; it may only advise.

Source: `agents/AGENT_CHANGE.md` Approval Gate section and Execution controls (`ALLOW_EXECUTION: FALSE (default)`); `docs/CONTRACT.md` K-AUTH-1

### REQ-03: Approval-SHA Binding

Publication guidance MUST document that approvals bind to a specific git SHA. Content changes after approval void the approval. This aligns with:

- K-AUTH-2: "Approvals bind to a specific git SHA. Content change after approval voids the approval."
- K-MERGE-1: "Merge to main allowed only when branch HEAD == approved SHA for the relevant run."

Source: `docs/CONTRACT.md` K-AUTH-2, K-MERGE-1

### REQ-04: Snapshot Immutability for Change Records

Change management outputs written to `{EXECUTION_ROOT}/_Change/` MUST follow the snapshot immutability convention:

- Snapshot folders MUST NOT be overwritten after creation.
- Pointer files (`_LATEST.md`) MAY be overwritten.
- Reruns create new snapshot folders.

Source: `docs/CONTRACT.md` K-SNAP-1; `docs/SPEC.md` Section 11

### REQ-05: Staleness Awareness

Change management guidance MUST acknowledge the staleness propagation model:

- Upstream changes propagate staleness to all transitive dependent deliverables (K-STALE-1).
- A deliverable is dirty if any governed input has changed since its last approved SHA (K-VAL-1).
- Stale items must be triaged by a human before being considered current (K-STALE-2). Resolution modes: no impact (clear flag), needs rework, or needs review.

Source: `docs/CONTRACT.md` K-STALE-1, K-STALE-2, K-VAL-1

### REQ-06: Separation of Concerns

The CHANGE agent instructions MUST maintain clear separation of concerns:

- CHANGE manages file/git state and change legibility.
- ORCHESTRATOR invokes DEPENDENCIES during project setup.
- RECONCILIATION governs dependency closure review.
- CHANGE implements approved edits requested by other agents but does not substitute for their governance roles.

Source: `agents/AGENT_CHANGE.md` Non-negotiable invariants; Coordination rules

### REQ-07: Publication Guidance Consistency

Any publication guidance produced or updated by this deliverable MUST be consistent with:

- The "filesystem is the database" principle (DIRECTIVE Section 2.1).
- The flat package-deliverable hierarchy (CONTRACT K-HIER-1: "Projects are decomposed as packages containing deliverables -- flat; no nesting; no phases layer").
- The execution root layout and tool root conventions (SPEC Section 1).

Additionally, the publication guidance MUST enumerate the minimum constraints any publication workflow must satisfy (see A-001):

- REQ-07a: Approval-SHA binding per K-AUTH-2 must be documented as a publication constraint.
- REQ-07b: Merge precondition per K-MERGE-1 must be documented as a publication constraint.
- REQ-07c: The publication path must not introduce hierarchy levels beyond the flat package-deliverable structure (K-HIER-1).

Source: `docs/DIRECTIVE.md` Sections 2.1, 2.2; `docs/CONTRACT.md` K-HIER-1, K-AUTH-2, K-MERGE-1; `docs/SPEC.md` Section 1

### REQ-08: Explicit Write Scope Compliance

The CHANGE agent instruction updates MUST maintain compliance with K-WRITE-1: every agent has an explicit write scope declared in its header block and no agent writes outside its declared zone.

Source: `docs/CONTRACT.md` K-WRITE-1, Section 1.9

## Standards

| Standard/Document | Applicability | Accessibility |
|-------------------|---------------|---------------|
| `docs/DIRECTIVE.md` | Founding principles: git-as-event-store, human authority, no hidden memory | Accessible |
| `docs/CONTRACT.md` | Binding invariants: K-AUTH-1/2, K-HIER-1, K-MERGE-1, K-SNAP-1, K-STALE-1, K-STALE-2, K-VAL-1, K-WRITE-1 | Accessible |
| `docs/SPEC.md` | Physical structures: `_Change/` tool root, snapshot conventions, folder layout | Accessible |
| `docs/TYPES.md` | Vocabulary: agent roles, lifecycle states, epistemic labels | Accessible |
| `agents/AGENT_HELPS_HUMANS.md` | Agent instruction structure requirements | Accessible (**location TBD** for specific clauses relevant to CHANGE alignment -- see F-002) |

## Verification

| Requirement | Verification Approach | Acceptance Criteria |
|-------------|----------------------|---------------------|
| REQ-01 | Review `AGENT_CHANGE.md` for explicit references to git as primary state source; confirm no hidden state mechanisms | (a) The phrase "git" or "version control" appears as the stated source of truth for changes; (b) No reference to private/hidden state for change tracking exists |
| REQ-02 | Review `AGENT_CHANGE.md` Approval Gate section for `APPROVE:` and `APPROVE_DESTRUCTIVE:` token requirements; confirm `ALLOW_EXECUTION=FALSE` default | (a) `APPROVE:` token pattern documented; (b) `APPROVE_DESTRUCTIVE:` token pattern documented; (c) `ALLOW_EXECUTION` explicitly defaults to `FALSE` |
| REQ-03 | Review publication guidance for SHA-binding language; trace to K-AUTH-2 and K-MERGE-1 | (a) SHA-binding language present; (b) Explicit cross-reference to K-AUTH-2 and K-MERGE-1 |
| REQ-04 | Review `_Change/` output conventions for snapshot immutability compliance; trace to K-SNAP-1 | (a) Snapshot immutability rule stated; (b) Pointer file exception stated; (c) Rerun behavior (new snapshot) stated |
| REQ-05 | Review guidance for staleness acknowledgment; confirm K-STALE-1 propagation and K-STALE-2 human triage are separately addressed | (a) K-STALE-1 propagation model acknowledged; (b) K-STALE-2 human triage requirement explicitly stated with resolution modes; (c) K-VAL-1 dirty-state definition present |
| REQ-06 | Review `AGENT_CHANGE.md` for separation of concerns with DEPENDENCIES and RECONCILIATION | (a) CHANGE write scope does not overlap with DEPENDENCIES or RECONCILIATION; (b) Coordination rules reference the boundary |
| REQ-07 | Cross-reference publication guidance with DIRECTIVE, CONTRACT, and SPEC for consistency; verify sub-requirements REQ-07a/b/c | (a) K-AUTH-2 constraint enumerated; (b) K-MERGE-1 constraint enumerated; (c) K-HIER-1 structural constraint enumerated |
| REQ-08 | Review `AGENT_CHANGE.md` header block for explicit write scope declaration | (a) WRITE_SCOPE property present in Agent Type table; (b) Write scope matches declared zone |
| V-EXCL | Verify exclusion boundaries: confirm deliverable content does not create obligations in excluded areas (CI enforcement, staleness tooling, hash verification, dependency governance, scope change management) | (a) No automated enforcement mechanisms introduced; (b) No dependency governance rules created; (c) No scope change procedures defined |
| V-QUAL | Verify deliverable completeness: all TBDs are either resolved or explicitly deferred with rationale; all REQs verified; human sign-off recorded | (a) TBD inventory reviewed; (b) Each TBD has either resolution or deferral rationale; (c) Human sign-off artifact exists in Records |

## Documentation

### Required Artifacts

| Artifact | Description |
|----------|-------------|
| Updated `agents/AGENT_CHANGE.md` | CHANGE agent instruction file aligned with all requirements above |
| Publication guidance constraints document | Formalized publication workflow constraints documenting: approval-SHA binding, merge precondition, and flat hierarchy compliance. **Canonical term:** "publication guidance constraints" (see Conflict Table in Guidance.md, B-003) |

### Supporting Context

- `_CONTEXT.md` in deliverable folder
- `_REFERENCES.md` in deliverable folder
- Decomposition G7-APPROVED (DEL-06-04 entry)
