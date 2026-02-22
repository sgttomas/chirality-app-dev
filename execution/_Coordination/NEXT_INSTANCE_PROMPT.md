# NEXT INSTANCE PROMPT — Stable Control-Plane Instructions

Use this file as the startup brief for new agent sessions. Keep this file stable; put dated/session-changing details in `execution/_Coordination/NEXT_INSTANCE_STATE.md`.

## Invariant Operating Instructions

1. Each new session startup must first read `README.md` and `AGENTS.md` before loading coordination handoff files.
2. Use `docs/PLAN.md` as strategic roadmap and sequencing rationale, but not as the sole execution controller.
3. Treat decomposition + lifecycle + coordination as operational authority:
   - decomposition scope: `execution/_Decomposition/ChiralityApp_SoftwareDecomposition_2026-02-21_G7-APPROVED.md`
   - lifecycle state: per-deliverable `_STATUS.md`
   - coordination policy: `execution/_Coordination/_COORDINATION.md`
4. Plan every cycle from three perspectives:
   - dependency topology (closure health)
   - objective/value flow (deliverable progress)
   - governance risk (CONTRACT/SPEC compliance)
5. Keep full dependency graph for audit/reconciliation, but drive development sequencing from the blocker subset defined in `_COORDINATION.md`.
6. Run development in tiered waves; each wave is fan-out execution + fan-in control checks.
7. Standard control loop per tier:
   1. ORCHESTRATOR scan/report (blocked/unblocked advisory using blocker-subset policy)
   2. WORKING_ITEMS fan-out on tier deliverables (TASK subagents allowed for bounded parallel work)
   3. DEPENDENCIES rerun only on touched deliverables
   4. RECONCILIATION for cross-deliverable interfaces in that tier
   5. periodic AUDIT_DEP_CLOSURE full-scope health check
   6. CHANGE publish in small coherent commits
8. Sequencing policy is invariant: full dependency graph is audit truth; blocker subset is execution truth.
9. PKG-08 remains traceable in the graph but non-driving for core sequencing until SOW-032..038 are explicitly ruled `IN`.
10. This file is not memory. Session memory stays in deliverable-local `MEMORY.md` files.
11. Agent/profile memory is non-authoritative for project execution: do not store, retrieve, or reconcile project state from agent memory surfaces. Use only filesystem state, with `MEMORY.md` as the sole memory record per deliverable.
12. `_MEMORY.md` is disabled for this project profile. Do not create, update, or rely on `_MEMORY.md`; use `MEMORY.md` only.

## How to Proceed (Execution Recipe)

1. Use the three-perspective planning model each cycle:
   - dependency topology (closure)
   - objective/value flow (deliverable progress)
   - governance risk (CONTRACT/SPEC checks)
2. Keep full-graph closure for audit truth, but drive sequencing from the blocker subset policy in `_COORDINATION.md`.
3. Execute tiered waves from `Execution_Path_Blocker_Analysis.md` with fan-out work in-tier and fan-in checks after tier completion.
4. After each tier, run:
   - DEPENDENCIES on changed deliverables only
   - RECONCILIATION on touched interfaces
   - ORCHESTRATOR scan/report
   - periodic full-scope AUDIT_DEP_CLOSURE rerun
5. Use `docs/PLAN.md` to decide when optional hardening work is pulled into active scope, in roadmap order.
6. Keep PKG-08 traceable but non-driving until SOW-032..038 are ruled `IN`.

## AGENT_TASK Concurrency Model (Explicit)

Two concurrency patterns use TASK agents. Both are tracked via TaskCreate/TaskUpdate.

Global autonomy policy: TASK dispatch is pre-authorized. No per-task approval gate is required for spawning/dispatch.

### Pattern 1: Tier-Local Fan-Out

Within a single tier, WORKING_ITEMS spawns TASK subagents to work on multiple deliverables in parallel. Each TASK agent is scoped to one deliverable.

- ORCHESTRATOR determines the tier and advisory state.
- WORKING_ITEMS runs the tier execution loop and spawns one TASK subagent per deliverable in that tier.
- Each TASK subagent handles one deliverable only, follows that deliverable's Procedure.md, writes only within that deliverable folder, then closes out that task/session.
- The next queued deliverable is handled by a newly booted TASK session (one deliverable per session invariant).
- Fan-in: WORKING_ITEMS collects results, runs control checks, advances the tier.

### Pattern 2: Development-Front Teams

Across the full development front (all currently unblocked deliverables), TASK agents are spawned as concurrent teams to maximize throughput. The development front is derived each cycle from the blocker-subset topology + current lifecycle states — it spans multiple tiers when lower-tier work is complete.

- ORCHESTRATOR scan determines the full set of unblocked deliverables (the development front).
- Multiple TASK agents are spawned to work concurrently across the front, each bounded to one assigned deliverable.
- Each TASK session closes after completing its assigned deliverable; new sessions are booted for newly assigned deliverables as the front evolves.
- This pattern is appropriate when prior tiers are complete and multiple independent deliverables are unblocked simultaneously.

### TASK Operating Boundary (Both Patterns)

- Instruction source: `agents/AGENT_TASK.md`
- Write scope: deliverable-local only (no cross-deliverable edits)
- Mode: recommendation-first by default; applies edits only when explicitly authorized in the brief
- Blocking: never (returns checkable proposals/outputs)
- Tracking: every spawned TASK is a TaskCreate entry; status updated on completion

### WORKING_ITEMS Orchestration Reference

- Instruction source: `agents/AGENT_WORKING_ITEMS.md`
- Owns human-interactive execution and Type 2 task dispatch.
- Responsible for both fan-out patterns above; chooses Pattern 1 or 2 based on development front width.
- Dispatch is globally pre-authorized and does not require per-task human approval.

## Information Placement (Canonical Homes)

| Information type | Canonical location |
|---|---|
| Stable coordination policy and blocker rule | `execution/_Coordination/_COORDINATION.md` |
| New-session stable instructions (invariant) | `execution/_Coordination/NEXT_INSTANCE_PROMPT.md` |
| New-session mutable handoff state (latest pointers, status, next actions) | `execution/_Coordination/NEXT_INSTANCE_STATE.md` |
| Strategic hardening roadmap and sequencing rationale | `docs/PLAN.md` |
| Scope ledger and deliverable definitions | `execution/_Decomposition/ChiralityApp_SoftwareDecomposition_2026-02-21_G7-APPROVED.md` |
| Per-deliverable lifecycle truth | `execution/PKG-*/1_Working/DEL-*/_STATUS.md` |
| Per-deliverable working memory | `execution/PKG-*/1_Working/DEL-*/MEMORY.md` |
| Legacy `_MEMORY.md` files | Disabled in this project profile; if found, migrate useful content to `MEMORY.md` and remove `_MEMORY.md` |
| Closure/audit evidence snapshots | `execution/_Reconciliation/DepClosure/CLOSURE_AUDIT_DEP_CLOSURE_*/` |

## Startup Procedure for Each New Session

1. Read `README.md`.
2. Read `AGENTS.md`.
3. Read this file (`execution/_Coordination/NEXT_INSTANCE_PROMPT.md`) for invariants.
4. Read `execution/_Coordination/NEXT_INSTANCE_STATE.md` for current pointers, current risks, and immediate queue.
5. Verify `execution/_Reconciliation/DepClosure/_LATEST.md` and confirm the linked closure snapshot exists and matches state pointers.
6. Determine session objective and completion criteria from state. Announce to the human and proceed (do not wait for approval unless the human has requested approval-gated sessions).
7. Run the tier control loop using blocker-subset sequencing policy from `_COORDINATION.md`.
8. When completion criteria are met (or the human decides to wrap up early), update only `NEXT_INSTANCE_STATE.md` (not this file), then hand off.

## Copy/Paste Starter Prompt (for next session)

```md
Read `README.md` and `AGENTS.md`.
Then use `execution/_Coordination/NEXT_INSTANCE_PROMPT.md` as stable control-plane instructions.
Then load `execution/_Coordination/NEXT_INSTANCE_STATE.md` for current pointers and next actions.
Treat full-graph closure as audit truth and blocker-subset analysis as execution sequencing truth.
Keep session memory in deliverable-local `MEMORY.md`, not in coordination handoff files.
Treat agent/profile memory as disabled for project-state authority.
Do not create or use `_MEMORY.md` in this project profile.
```
