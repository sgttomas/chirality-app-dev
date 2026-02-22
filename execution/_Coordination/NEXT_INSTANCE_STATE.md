# NEXT INSTANCE STATE — Mutable Handoff Snapshot

This file stores dated/session-changing state for the next agent instance. Update this file at each handoff; keep `NEXT_INSTANCE_PROMPT.md` stable.

**Last Updated:** 2026-02-22 (Post-SCA-001 blocker scan: pre-tier gate wave sequencing computed from Dependencies.csv)

## Current Pointers

| Item | Current pointer |
|---|---|
| Coordination policy | `execution/_Coordination/_COORDINATION.md` |
| Stable startup instructions | `execution/_Coordination/NEXT_INSTANCE_PROMPT.md` |
| Tier 2 control-loop report | `execution/_Coordination/TIER2_CONTROL_LOOP_2026-02-22_PASS5.md` |
| Tier 2 interface reconciliation | `execution/_Reconciliation/TIER2_INTERFACE_RECON_2026-02-22_PASS5.md` |
| Latest closure pointer | `execution/_Reconciliation/DepClosure/_LATEST.md` |
| Full-scope closure snapshot | `execution/_Reconciliation/DepClosure/CLOSURE_AUDIT_DEP_CLOSURE_2026-02-22_2235/` |
| Closure run summary | `execution/_Reconciliation/DepClosure/CLOSURE_AUDIT_DEP_CLOSURE_2026-02-22_2235/RUN_SUMMARY.md` |
| Blocker-subset execution path | `execution/_Reconciliation/DepClosure/CLOSURE_AUDIT_DEP_CLOSURE_2026-02-22_2235/Execution_Path_Blocker_Analysis.md` |
| Machine-readable execution path | `execution/_Reconciliation/DepClosure/CLOSURE_AUDIT_DEP_CLOSURE_2026-02-22_2235/execution_path_summary.json` |
| Strategic roadmap | `docs/PLAN.md` |
| Decomposition scope amendment | `execution/_Decomposition/ChiralityApp_SoftwareDecomposition_2026-02-21_G7-APPROVED.md` (Scope Amendment A1) |
| Decomposition coverage (post-SCA-001) | `execution/_Reconciliation/DecompCoverage/COV_POST_SCA001_FULL_2026-02-22/` |

## Current Program State

- Decomposition Scope Amendment A1 is in effect with 4 new deliverables fully scaffolded, initialized, and dependency-extracted.
- All 4 frontend baseline deliverables (`DEL-01-03`, `DEL-02-05`, `DEL-03-07`, `DEL-07-03`) are at `INITIALIZED` state with production documents (Datasheet, Specification, Guidance, Procedure) and `Dependencies.csv` (v3.1).
- Decomposition coverage audit passed: 7/7 PASS, 0 issues (`COV_POST_SCA001_FULL_2026-02-22`).
- Pre-tier gate internal dependency analysis complete: the 4 frontend baseline deliverables form a 3-wave internal sequence (see tier table below).
- Tier 1 remains active with all four deliverables at `IN_PROGRESS`.
- Tier 2 code-bearing deliverables (`DEL-01-01`, `DEL-03-01`, `DEL-05-03`, `DEL-05-04`) are at `IN_PROGRESS` lifecycle state but remain execution-blocked on pre-tier gate deliverables reaching `IN_PROGRESS`. `DEL-06-02` continues independently (no pre-tier gate edges).
- Latest full-scope closure status remains `WARNINGS` (1 SCC, largest SCC size 31) due to reciprocal interface declarations.
- Blocker-subset execution path remains acyclic (0 SCCs); tier structure is execution-valid under blocker policy.

### Pre-Tier Gate Wave Sequencing (from Dependencies.csv blocker-subset analysis)

The 4 frontend baseline deliverables have the following internal dependency structure under blocker-subset filtering:

| Wave | Deliverables | Upstream Blocker Edges (DELIVERABLE only) | Status |
|------|-------------|-------------------------------------------|--------|
| 0a | `DEL-01-03` | None (no upstream DELIVERABLE blockers in blocker subset) | INITIALIZED — ready to advance to IN_PROGRESS |
| 0b | `DEL-03-07` | `DEL-01-03` (PREREQUISITE) | INITIALIZED — blocked until DEL-01-03 reaches IN_PROGRESS |
| 0c | `DEL-02-05`, `DEL-07-03` | `DEL-01-03` (PREREQUISITE) + `DEL-03-07` (PREREQUISITE) | INITIALIZED — blocked until both DEL-01-03 and DEL-03-07 reach IN_PROGRESS |

Execution order: DEL-01-03 first, then DEL-03-07, then DEL-02-05 and DEL-07-03 in parallel.

### Tier 2 Upstream Blocker Edges (Pre-Tier Gate)

| DEL-ID | Pre-Tier Gate Blockers | Other Blocker-Subset Upstream Edges (already met) |
|--------|------------------------|---------------------------------------------------|
| DEL-01-01 | DEL-01-03 (PREREQUISITE), DEL-03-07 (PREREQUISITE) | DEL-05-01 (CONSTRAINT, MET at IN_PROGRESS) |
| DEL-03-01 | DEL-03-07 (PREREQUISITE), DEL-01-03 (CONSTRAINT) | DEL-05-01 (CONSTRAINT, MET at IN_PROGRESS) |
| DEL-05-03 | DEL-01-03 (PREREQUISITE), DEL-03-07 (CONSTRAINT) | DEL-05-02 (PREREQUISITE, MET at IN_PROGRESS) |
| DEL-05-04 | DEL-01-03 (PREREQUISITE), DEL-03-07 (CONSTRAINT) | DEL-05-02 (PREREQUISITE, MET at IN_PROGRESS) |
| DEL-06-02 | (none) | Already IN_PROGRESS; continues independently |

### Tier 2 Findings Snapshot (Pass 5 — unchanged)

| DEL-ID | Kickoff Finding | Immediate Focus |
|--------|------------------|-----------------|
| DEL-01-01 | Packaging evidence queue assumes runnable desktop build scripts in this repo. | Gate on frontend baseline: complete `DEL-01-03` + `DEL-03-07` to `IN_PROGRESS`, then run `desktop:pack`/`desktop:dist` evidence capture for `instruction-root/docs`. |
| DEL-03-01 | Test-hardening queue assumes session runtime/test files exist in this repo. | Gate on frontend baseline: complete `DEL-03-07` + `DEL-07-03` to `IN_PROGRESS`, then add targeted REQ-11 regression coverage. |
| DEL-05-03 | Lifecycle module path (`frontend/lib/lifecycle/*`) is absent in current repo tree. | Gate on frontend baseline: complete `DEL-01-03` + `DEL-03-07` to `IN_PROGRESS`, then implement parser/writer/transition module + tests. |
| DEL-05-04 | Dependency contract path (`frontend/lib/dependencies/*`) is absent in current repo tree. | Gate on frontend baseline: complete `DEL-01-03` + `DEL-03-07` to `IN_PROGRESS`, then implement v3.1 schema/reader/writer module + tests. |
| DEL-06-02 | Workflow-agent conformance posture remains documentation-driven and local to this repo. | Carry forward REQ-16/CT-001 residuals; keep DEL-06-01 residual watchlist synchronized. |

### Tier 1 Progress Summary

| DEL-ID | Title | Work Done | Remaining |
|--------|-------|-----------|-----------|
| DEL-05-01 | Instruction Root Bundling | Prior pass reports claim repo-local mitigations, but current tracked tree has no runtime implementation surface to verify. | Reconcile/restore runtime tree, rerun packaging evidence, then address SHA-256 integrity, read-only enforcement, and degradation behavior. |
| DEL-05-02 | Execution Root Scaffolding | Repo-local audit; 0% implemented. Implementation plan with module design in MEMORY.md. | Build scaffolding module (`scaffold.ts`, `sanitize.ts`), API endpoint, conformance tests. |
| DEL-06-01 | Agent Instruction Conformance | Audit complete; 7 agent files fixed (REQ-04: 2, REQ-06: 2, REQ-07: 4). Baseline ~90% -> ~96%. | REQ-05 (precedence statement, SHOULD), REQ-09 (CLASS cross-check), REQ-10 (subagent delegation). |
| DEL-07-02 | Example Execution Roots | Example fixture created at `examples/example-project/` (1 pkg, 3 dels, 3 lifecycle states). REQ-01..09 pass. | REQ-10 (validation script compatibility, depends on DEL-07-01). TBDs: root count, Deps.csv inclusion. |

## Active Human Rulings and Assumptions

1. Blocker maturity threshold is `IN_PROGRESS`.
2. Execution sequencing uses blocker-subset filtering from `_COORDINATION.md`; full graph remains audit/reconciliation truth.
3. PKG-08 (`DEL-08-*`) stays traceable but non-driving until SOW-032..038 are explicitly ruled `IN`.
4. TASK dispatch is globally pre-authorized; no per-task human approval gate.
5. TASK execution is one deliverable per session; each session closes after bounded completion and new sessions are booted for queued work.
6. Execution and implementation edits are scoped to this repository only (`/Users/ryan/ai-env/projects/chirality-app-dev`) unless explicitly re-ruled by a human.
7. Frontend baseline deliverables from Scope Amendment A1 (`DEL-01-03`, `DEL-02-05`, `DEL-03-07`, `DEL-07-03`) must reach `IN_PROGRESS` before Tier 2 code-bearing execution resumes.

## Core Development Tiers (Blocker Subset; PKG-08 Excluded)

1. **Pre-Tier Gate Wave 0a:** `DEL-01-03` — **INITIALIZED; UNBLOCKED (no upstream deliverable blockers); ready to advance**
2. **Pre-Tier Gate Wave 0b:** `DEL-03-07` — **INITIALIZED; BLOCKED by DEL-01-03**
3. **Pre-Tier Gate Wave 0c:** `DEL-02-05`, `DEL-07-03` — **INITIALIZED; BLOCKED by DEL-01-03 + DEL-03-07**
4. **Tier 1:** `DEL-05-01`, `DEL-05-02`, `DEL-06-01`, `DEL-07-02` — **IN_PROGRESS (active)**
5. **Tier 2:** `DEL-01-01`, `DEL-03-01`, `DEL-05-03`, `DEL-05-04` — **IN_PROGRESS lifecycle but BLOCKED_BY_PRE_TIER_GATE on DEL-01-03 + DEL-03-07**
6. **Tier 2 (independent):** `DEL-06-02` — **IN_PROGRESS (no pre-tier gate edges; continues independently)**
7. **Tier 3:** `DEL-03-03`
8. **Tier 4:** `DEL-03-05`
9. **Tier 5:** `DEL-03-06`
10. **Tier 6:** `DEL-03-02`
11. **Tier 7:** `DEL-02-03`, `DEL-03-04`, `DEL-04-01`
12. **Tier 8:** `DEL-04-02`, `DEL-07-01`

## Immediate Next Actions

1. **Advance DEL-01-03 to IN_PROGRESS (Wave 0a):** This is the single immediate unblock path. Dispatch TASK for DEL-01-03 to bootstrap the frontend/ workspace (package manifest, build config, TypeScript/Next.js/Electron scaffolding, dev scripts). No upstream deliverable blockers.
2. **Advance DEL-03-07 to IN_PROGRESS (Wave 0b):** Once DEL-01-03 reaches IN_PROGRESS, dispatch TASK for DEL-03-07 to implement baseline harness API routes (session CRUD, turn execution stubs) in the frontend/ workspace.
3. **Advance DEL-02-05 and DEL-07-03 to IN_PROGRESS in parallel (Wave 0c):** Once both DEL-01-03 and DEL-03-07 reach IN_PROGRESS, dispatch parallel TASKs for DEL-02-05 (workflow UI shell) and DEL-07-03 (validation runbook baseline).
4. **Resume Tier 2 code-bearing wave (post-gate):** After all 4 pre-tier gate deliverables reach IN_PROGRESS, Tier 2 code-bearing work is fully unblocked: DEL-05-03 lifecycle module, DEL-05-04 dependency contract module, DEL-03-01 session boot hardening, DEL-01-01 packaging evidence.
5. **Continue Tier 1 and DEL-06-02 in parallel:** These have no pre-tier gate dependencies and can advance concurrently with the pre-tier gate wave.
6. **Post-gate fan-in:** After pre-tier gate completion, rerun DEPENDENCIES on changed deliverables, then RECONCILIATION on touched interfaces; run full-scope closure if dependency rows change.

## Update Protocol

1. Update `Last Updated` date/context.
2. Update snapshot pointers to latest closure outputs.
3. Update `Current Program State` and `Immediate Next Actions`.
4. Keep history/evidence in reconciliation snapshots and control-loop reports; avoid duplicating long evidence blocks here.
