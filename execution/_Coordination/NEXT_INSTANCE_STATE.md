# NEXT INSTANCE STATE — Mutable Handoff Snapshot (Concise Control-Plane)

This file is intentionally concise. Keep only current pointers, current graph truth, and the immediate execution queue.
Detailed chronology belongs in deliverable-local `MEMORY.md`, tier control-loop reports, reconciliation artifacts, and git history.

**Last Updated:** 2026-02-24 (development history analysis + process improvements + SCA-003 intake)

## History and Archive Policy

- Immutable archived state history:
  - `execution/_Coordination/NEXT_INSTANCE_STATE_ARCHIVE_2026-02-24_pre_simplify.md`
- Archive rule:
  - treat archived state snapshots as immutable historical records.
  - do not append new session logs to archive files.
- Transfer rule (completed):
  - deliverable-specific publish-trace entries from archived state have been transferred into corresponding deliverable `MEMORY.md` files under:
    - `## Coordination Publish Trace (Transferred 2026-02-24)`

## Current Pointers

| Item | Current pointer |
|---|---|
| Coordination policy | `execution/_Coordination/_COORDINATION.md` |
| Stable startup instructions | `execution/_Coordination/NEXT_INSTANCE_PROMPT.md` |
| Strategic roadmap | `docs/PLAN.md` |
| Decomposition scope | `execution/_Decomposition/ChiralityApp_SoftwareDecomposition_2026-02-21_G7-APPROVED.md` |
| Latest immutable closure snapshot pointer | `execution/_Reconciliation/DepClosure/_LATEST.md` |
| Latest immutable closure snapshot | `execution/_Reconciliation/DepClosure/CLOSURE_AUDIT_DEP_CLOSURE_2026-02-24_2123/` |
| Blocker-subset analysis (latest snapshot) | `execution/_Reconciliation/DepClosure/CLOSURE_AUDIT_DEP_CLOSURE_2026-02-24_2123/Execution_Path_Blocker_Analysis.md` |
| Blocker-subset machine summary (latest snapshot) | `execution/_Reconciliation/DepClosure/CLOSURE_AUDIT_DEP_CLOSURE_2026-02-24_2123/execution_path_summary.json` |
| Current dependency audit refresh (this handoff) | `execution/_Coordination/DEPENDENCY_AUDIT_2026-02-24.md` |
| Current dependency audit JSON (this handoff) | `execution/_Coordination/DEPENDENCY_AUDIT_2026-02-24.json` |
| Latest Tier control-loop artifact | `execution/_Coordination/TIER9_CONTROL_LOOP_2026-02-24_PASS15.md` |
| Latest interface reconciliation artifact | `execution/_Reconciliation/TIER9_INTERFACE_RECON_2026-02-24_PASS15.md` |
| Development history analysis | `execution/_Coordination/DEVELOPMENT_HISTORY_ANALYSIS_2026-02-24.md` |

## Current Graph Truth

### Full-Graph Closure (Audit Truth)

- Status: `WARNINGS`
- Active `EXECUTION`/`DELIVERABLE` rows: `141`
- Unique directed edges: `100`
- SCCs: `0` (total SCC nodes: `0`)
- Bidirectional pairs: `0`
- Source: `execution/_Reconciliation/DepClosure/CLOSURE_AUDIT_DEP_CLOSURE_2026-02-24_2123/closure_summary.json`

### Blocker-Subset Topology (Execution Sequencing Truth)

- Status: `PASS` (acyclic)
- Rule: `EXECUTION + DELIVERABLE + ACTIVE + UPSTREAM + (PREREQUISITE|CONSTRAINT) + non-ASSUMPTION`
- Edge count (all/core): `44` / `43`
- Tier count (all/core): `9` / `9`
- Read quality: `0` missing CSV, `0` unreadable, `0` schema-invalid
- Source: `execution/_Reconciliation/DepClosure/CLOSURE_AUDIT_DEP_CLOSURE_2026-02-24_2123/execution_path_summary.json`

### Delta vs Prior Baseline Snapshot (`2026-02-24_2101`)

- Full-graph status: `BLOCKER -> WARNINGS`
- Full-graph SCC count: `1 -> 0` (`-1`)
- Full-graph SCC nodes: `21 -> 0` (`-21`)
- Full-graph bidirectional pairs: `12 -> 0` (`-12`)
- Unique edges: `112 -> 100` (`-12`)
- Blocker-subset edges: `44 -> 44` (`0`)
- Tier assignment changes: none

### Lifecycle and Register Delta Since Prior Baseline Snapshot (`2026-02-24_2101`)

- Lifecycle transitions: none
- Dependency register row updates:
  - 21 direction reorientations applied to non-blocker interface/handover/enables rows to remove residual SCC loops (see `execution/_Coordination/DEPENDENCY_AUDIT_2026-02-24.md` for full list).

## Execution Queue Snapshot (All Active Scope, maturity threshold = `IN_PROGRESS`)

### SPEC_STATUS Format

When deliverables are in the Active Front, each entry carries a `SPEC_STATUS` annotation:
- `SPEC-COMPLETE` — all `REQ-*` entries in `Specification.md` are met. Default next action is lifecycle advancement (not another pass). Elective work beyond spec requires explicit human authorization.
- `PARTIAL (REQ-04, REQ-07 open)` — lists the specific open requirements. Next pass is queued normally, focused on the open REQs.
- Omitted for deliverables already at `ISSUED` or `RETIRED` (spec-completion is implied by issuance).

### Active Front (`IN_PROGRESS`/`CHECKING`)

- *(none)*

### Unblocked but Not Started (`< IN_PROGRESS`)

- *(none)*

### Blocked (`< IN_PROGRESS` with unmet upstreams)

- *(none)*

### Issued (Core, PKG-01..07)

- `DEL-01-01`, `DEL-01-02`, `DEL-01-03`, `DEL-02-01`, `DEL-02-02`, `DEL-02-03`, `DEL-02-04`, `DEL-02-05`, `DEL-03-01`, `DEL-03-02`, `DEL-03-03`, `DEL-03-04`, `DEL-03-05`, `DEL-03-06`, `DEL-03-07`, `DEL-04-01`, `DEL-04-02`, `DEL-05-01`, `DEL-05-02`, `DEL-05-03`, `DEL-05-04`, `DEL-06-01`, `DEL-06-02`, `DEL-06-03`, `DEL-06-04`, `DEL-06-05`, `DEL-07-01`, `DEL-07-02`, `DEL-07-03`

### Issued (PKG-08, IN scope)

- `DEL-08-01`, `DEL-08-02`

### Retired (PKG-08, OUT scope)

- `DEL-08-03`, `DEL-08-04`, `DEL-08-05`, `DEL-08-06`, `DEL-08-07`

## Active Human Rulings (Still in Force)

- Sequencing invariant: full graph closure is audit truth; blocker subset is execution truth.
- `PKG-08` scope resolved (SCA-002, 2026-02-24): DEL-08-01/02 are IN and active; DEL-08-03..07 are OUT and retired.
- `_MEMORY.md` is disabled for this project profile; use deliverable-local `MEMORY.md` only.
- CHECKING -> ISSUED transitions are pre-approved by the human for all deliverables (ruling 2026-02-24).
- DEL-06-05 A-001 issuance precondition is explicitly waived by human decision `HW-DEL-06-05-A001-2026-02-24` (deliverable remains `ISSUED`; responsible-party assignment remains follow-up).
- OI-001 resolved (2026-02-23): API key provisioning is ENV_ONLY (`ANTHROPIC_API_KEY` environment variable). **Amendment pending via SCA-003** — human has requested UI-based API key entry; scope change at Gate 1 (intake validated, awaiting Gate 2 impact assessment).
- OI-002 resolved (2026-02-23): Outbound network enforcement is Option B layered (provider base-URL guardrails + Electron `session.webRequest` egress interception).
- Process improvements implemented (2026-02-24): spec-anchored completion check in AGENT_TASK.md Step 7 + AGENT_WORKING_ITEMS.md Phase 5; category-level coverage check in AGENT_DECOMP_BASE.md Phase 6. See `DEVELOPMENT_HISTORY_ANALYSIS_2026-02-24.md` for rationale.

## Immediate Next Actions

1. **Resume SCA-003 at Gate 2 (Impact Assessment).** Gate 1 intake is validated. The scope change adds UI-based API key entry: `SOW-050` (new scope item), `DEL-02-06` (new deliverable in PKG-02), `MODIFY` to DEL-03-05 (key provisioning contract: ENV_ONLY → ENV+UI), and amends OI-001 resolution. Run as SCOPE_CHANGE agent per `agents/AGENT_SCOPE_CHANGE.md`. Gate 1 parsed actions:
   - ADD SOW-050: UI-based API key entry + local secure storage (non-project-truth convenience state)
   - ADD DEL-02-06: Settings / API Key Entry UI (UX_UI_SLICE, PKG-02)
   - MODIFY DEL-03-05: Key provisioning contract ENV_ONLY → ENV+UI (UI-provided key takes precedence; env var is fallback)
   - MODIFY OI-001: Resolution amended from ENV_ONLY to ENV_PLUS_UI
   - Downstream: `docs/SPEC.md` line 636 and `docs/PLAN.md` lines 60–63 reference ENV_ONLY and need updating after SCA-003 completes
2. After SCA-003 Gate 5 completes: run PREPARATION on new DEL-02-06 folder, then DEPENDENCIES extraction on DEL-02-06 and re-extraction on DEL-03-05.
3. Deferred from prior session: semantic-consistency pass on the 21 reoriented dependency rows (Direction semantics vs. row prose alignment). Lower priority than SCA-003.

## Startup Checklist (Next Session)

1. Read `README.md`.
2. Read `AGENTS.md`.
3. Read `execution/_Coordination/NEXT_INSTANCE_PROMPT.md`.
4. Read this file (`execution/_Coordination/NEXT_INSTANCE_STATE.md`).
5. Verify `execution/_Reconciliation/DepClosure/_LATEST.md` path exists.
6. Read `execution/_Coordination/DEPENDENCY_AUDIT_2026-02-24.md` for current graph status.
