# Datasheet — DEL-06-04: Change Management & Git Hygiene Support

## Identification

| Field | Value |
|-------|-------|
| **DeliverableID** | DEL-06-04 |
| **Name** | Change Management & Git Hygiene Support |
| **PackageID** | PKG-06 |
| **Package** | Agent Suite & Governance |
| **Type** | DOC_UPDATE |
| **ContextEnvelope** | M |
| **Responsible Party** | TBD (requires human assignment -- see B-001) |
| **Scope Coverage** | SOW-021 |
| **Objectives** | OBJ-004, OBJ-006 (**ASSUMPTION:** best-effort mapping via PKG-06 package grouping) |
| **Anticipated Artifacts** | DOC |
| **Decomposition** | `execution/_Decomposition/ChiralityApp_SoftwareDecomposition_2026-02-21_G7-APPROVED.md` |

## Attributes

| Attribute | Value | Source |
|-----------|-------|--------|
| **Primary Subject** | CHANGE agent instruction alignment with "git is the event store" intent and human approval rules | Decomposition DEL-06-04 entry |
| **Artifact Class** | Documentation update (agent instructions + publication guidance) | `_CONTEXT.md` -- Type: DOC_UPDATE |
| **Governing Design Principle** | "Git is the event store" -- version control provides the development record: meaningful diffs for review, reproducibility, rollback, and audits (DIRECTIVE Section 2.2) | `docs/DIRECTIVE.md` Section 2.2 |
| **Governing Invariants** | K-AUTH-1, K-AUTH-2, K-HIER-1, K-MERGE-1, K-SNAP-1, K-STALE-1, K-STALE-2, K-VAL-1, K-WRITE-1 (see Conflict Table in Guidance.md -- X-002/X-003 for invariant set reconciliation) | `docs/CONTRACT.md` Sections 1.2, 1.5, 1.6, 1.8, 1.9, 1.10 |
| **Primary Agent** | CHANGE (Type 1, PERSONA class) | `agents/AGENT_CHANGE.md` |
| **Tool Root** | `{EXECUTION_ROOT}/_Change/` | `docs/SPEC.md` Section 1.2 |
| **Current CHANGE Write Scope** | Tool-root logs (`_Change/`); repo files only with Approval Gate | `agents/AGENT_CHANGE.md` Agent Type table |
| **Canonical Function Term** | TBD -- see Conflict Table in Guidance.md (E-003) for terminology normalization of the CHANGE agent's primary function | Specification.md#REQ-01, Guidance.md#P3 |

## Conditions

| Condition | Detail | Source |
|-----------|--------|--------|
| **Human Approval Gate** | All state-changing actions (git commands, file edits) require explicit `APPROVE:` token from the human | `agents/AGENT_CHANGE.md` Approval Gate section |
| **Destructive Action Escalation** | Force pushes, hard resets, clean operations require `APPROVE_DESTRUCTIVE:` token with risk restatement | `agents/AGENT_CHANGE.md` Heightened approval |
| **Approval-SHA Binding** | Approvals bind to a specific git SHA; content change after approval voids it | `docs/CONTRACT.md` K-AUTH-2 |
| **Merge Precondition** | Merge to main allowed only when branch HEAD == approved SHA | `docs/CONTRACT.md` K-MERGE-1 |
| **Snapshot Immutability** | Task agent outputs to tool roots are immutable snapshots; pointer files may be overwritten | `docs/CONTRACT.md` K-SNAP-1; `docs/SPEC.md` Section 11 |
| **Staleness Propagation** | Upstream changes propagate staleness to all transitive dependents | `docs/CONTRACT.md` K-STALE-1 |
| **Staleness Triage** | Stale items must be triaged by a human before being considered current; resolution modes: no impact, needs rework, or needs review | `docs/CONTRACT.md` K-STALE-2 |
| **Explicit Write Scope** | Every agent has an explicit write scope declared in its header block; no agent writes outside its declared zone | `docs/CONTRACT.md` K-WRITE-1, Section 1.9 |
| **Flat Hierarchy** | Projects are decomposed as packages containing deliverables (flat; no nesting; no phases layer); publication guidance must respect this structure | `docs/CONTRACT.md` K-HIER-1, Section 1.5 |
| **Governance Authority** | TBD -- the human or role authorized to approve the final deliverable outputs and discharge TBDs has not been designated (see E-001) | **ASSUMPTION:** authority delegation will be resolved when Responsible Party is assigned |

## Construction

| Aspect | Detail | Source |
|--------|--------|--------|
| **Publication Flow** | TBD -- the specific publication workflow (branch strategy, review process, merge ceremony) is not yet codified beyond the K-MERGE-1 invariant. At minimum, the publication flow must satisfy: (a) approval-SHA binding per K-AUTH-2, (b) merge precondition per K-MERGE-1, and (c) flat hierarchy per K-HIER-1 | **ASSUMPTION:** publication guidance will formalize the branch-to-merge path consistent with K-AUTH-2, K-MERGE-1, and K-HIER-1; Source: `docs/CONTRACT.md` K-AUTH-2, K-MERGE-1, K-HIER-1 |
| **Session Log Persistence** | CHANGE writes optional session logs to `{EXECUTION_ROOT}/_Change/` when `WRITE_LOG_TO` is provided | `agents/AGENT_CHANGE.md` Step 5 |
| **Change Record Format** | TBD -- no formal change record schema is defined beyond the session log markdown and `_Change/` tool root. The format should address: (a) action identification, (b) approval token linkage, (c) SHA binding record, (d) outcome status. Must comply with K-SNAP-1 immutability for records written to tool roots. | **ASSUMPTION:** DEL-06-04 will define or reference change record conventions; Source: `agents/AGENT_CHANGE.md` Step 5, `docs/CONTRACT.md` K-SNAP-1 |
| **Git Hygiene Conventions** | TBD -- specific branch naming, commit message, and working tree hygiene conventions are not yet codified. See Guidance.md T2 for scope boundary rationale and D-001 for evidence basis discussion. | **ASSUMPTION:** conventions will be derived from DIRECTIVE principles and existing CHANGE agent behavior; Source: `docs/DIRECTIVE.md` Section 2.2 |

## References

| Reference | Relevance |
|-----------|-----------|
| `docs/DIRECTIVE.md` Section 2.2 | "Git is the event store" founding principle |
| `docs/DIRECTIVE.md` Section 2.3 | Human authority at every gate |
| `docs/CONTRACT.md` | Invariants K-AUTH-1, K-AUTH-2, K-HIER-1, K-MERGE-1, K-SNAP-1, K-STALE-1, K-STALE-2, K-VAL-1, K-WRITE-1 |
| `docs/SPEC.md` Section 1.2 | `_Change/` tool root definition |
| `docs/SPEC.md` Section 11 | Snapshot and pointer conventions |
| `agents/AGENT_CHANGE.md` | CHANGE agent instruction file (primary subject of this deliverable) |
| `agents/AGENT_SCOPE_CHANGE.md` | Scope change agent (related; handles scope modifications) |
| Decomposition (G7-APPROVED) | DEL-06-04 entry, SOW-021, OBJ-004, OBJ-006 |
