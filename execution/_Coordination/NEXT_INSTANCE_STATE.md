# NEXT INSTANCE STATE — Mutable Handoff Snapshot

This file stores dated/session-changing state for the next agent instance. Update this file at each handoff; keep `NEXT_INSTANCE_PROMPT.md` stable.

**Last Updated:** 2026-02-22 (Scope amendment A1 + frontend baseline gating update)

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

## Current Program State

- Decomposition Scope Amendment A1 is now in effect: frontend baseline is explicit `IN` scope (`SOW-044..049`) with new objective `OBJ-008` and deliverables `DEL-01-03`, `DEL-02-05`, `DEL-03-07`, `DEL-07-03`.
- Frontend baseline deliverables are not yet scaffolded in the execution tree; this is now the primary unblock path.
- Tier 1 remains active with all four deliverables at `IN_PROGRESS`.
- Tier 2 control-loop pass 5 remains the latest control-loop artifact for Tier 2.
- Tier 2 code-bearing queue remains blocked in this repository until frontend baseline deliverables (`DEL-01-03`, `DEL-02-05`, `DEL-03-07`, `DEL-07-03`) reach blocker maturity threshold (`IN_PROGRESS`).
- Latest full-scope closure status remains `WARNINGS` (1 SCC, largest SCC size 31) due to reciprocal interface declarations.
- Data quality checks remain clean in the latest closure run (schema/orphan/misplaced-field/anchor checks pass).
- Blocker-subset execution path remains acyclic (0 SCCs); Tier 2 remains execution-valid under blocker policy.
- Pass-3 code-bearing claims remain non-reproducible in this tracked tree because required runtime paths are not present.
- No `Dependencies.csv` content changed in pass 5; no new full-scope closure snapshot was generated.

### Tier 2 Findings Snapshot (Pass 5)

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

1. Pre-Tier Gate: `DEL-01-03`, `DEL-02-05`, `DEL-03-07`, `DEL-07-03` — **NEW (frontend baseline; not yet scaffolded; must reach `IN_PROGRESS`)**
2. Tier 1: `DEL-05-01`, `DEL-05-02`, `DEL-06-01`, `DEL-07-02` — **IN_PROGRESS**
3. Tier 2: `DEL-01-01`, `DEL-03-01`, `DEL-05-03`, `DEL-05-04`, `DEL-06-02` — **BLOCKED_BY_PRE_TIER_GATE**
4. Tier 3: `DEL-03-03`
5. Tier 4: `DEL-03-05`
6. Tier 5: `DEL-03-06`
7. Tier 6: `DEL-03-02`
8. Tier 7: `DEL-02-03`, `DEL-03-04`, `DEL-04-01`
9. Tier 8: `DEL-04-02`, `DEL-07-01`

## Immediate Next Actions

1. **Propagate Scope Amendment A1 into execution workspace**: initialize new deliverable folders and metadata for `DEL-01-03`, `DEL-02-05`, `DEL-03-07`, `DEL-07-03` under their packages.
2. **Execute frontend baseline wave (local-only)**: advance the four new frontend baseline deliverables to `IN_PROGRESS` with concrete in-repo implementation plans and initial artifacts.
3. **Re-run ORCHESTRATOR blocker scan after baseline advancement**: recompute Tier 2 advisory once pre-tier gate maturity is met.
4. **Resume Tier 2 code-bearing wave (post-gate)**: implement DEL-05-03 lifecycle module and DEL-05-04 dependency contract module, then DEL-03-01 hardening and DEL-01-01 packaging evidence.
5. **Tier 2 fan-in after code-bearing edits**: rerun DEPENDENCIES on changed deliverables only, then RECONCILIATION on touched interfaces; run full-scope closure only if dependency rows change.

## Update Protocol

1. Update `Last Updated` date/context.
2. Update snapshot pointers to latest closure outputs.
3. Update `Current Program State` and `Immediate Next Actions`.
4. Keep history/evidence in reconciliation snapshots and control-loop reports; avoid duplicating long evidence blocks here.
