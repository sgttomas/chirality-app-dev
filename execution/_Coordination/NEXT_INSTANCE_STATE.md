# NEXT INSTANCE STATE — Mutable Handoff Snapshot

This file stores dated/session-changing state for the next agent instance. Update this file at each handoff; keep `NEXT_INSTANCE_PROMPT.md` stable.

**Last Updated:** 2026-02-22 (Wave 0a + Wave 0b execution stabilized: `DEL-01-03` and `DEL-03-07` at `IN_PROGRESS`; output-mode conflict resolved; Wave 0c unblocked)

## Current Pointers

| Item | Current pointer |
|---|---|
| Coordination policy | `execution/_Coordination/_COORDINATION.md` |
| Stable startup instructions | `execution/_Coordination/NEXT_INSTANCE_PROMPT.md` |
| Tier 2 control-loop report | `execution/_Coordination/TIER2_CONTROL_LOOP_2026-02-22_PASS6.md` |
| Tier 2 interface reconciliation | `execution/_Reconciliation/TIER2_INTERFACE_RECON_2026-02-22_PASS5.md` |
| Latest closure pointer | `execution/_Reconciliation/DepClosure/_LATEST.md` |
| Full-scope closure snapshot | `execution/_Reconciliation/DepClosure/CLOSURE_AUDIT_DEP_CLOSURE_2026-02-22_0838/` |
| Closure run summary | `execution/_Reconciliation/DepClosure/CLOSURE_AUDIT_DEP_CLOSURE_2026-02-22_0838/RUN_SUMMARY.md` |
| Blocker-subset execution path | `execution/_Reconciliation/DepClosure/CLOSURE_AUDIT_DEP_CLOSURE_2026-02-22_0838/Execution_Path_Blocker_Analysis.md` |
| Machine-readable execution path | `execution/_Reconciliation/DepClosure/CLOSURE_AUDIT_DEP_CLOSURE_2026-02-22_0838/execution_path_summary.json` |
| Strategic roadmap | `docs/PLAN.md` |
| Decomposition scope amendment | `execution/_Decomposition/ChiralityApp_SoftwareDecomposition_2026-02-21_G7-APPROVED.md` (Scope Amendment A1) |
| Decomposition coverage (post-SCA-001) | `execution/_Reconciliation/DecompCoverage/COV_POST_SCA001_FULL_2026-02-22/` |
| Scope-change ledger pointer | `execution/_ScopeChange/_LATEST.md` |

## Next Session Startup Checklist

1. Read `README.md`.
2. Read `AGENTS.md`.
3. Read `execution/_Coordination/NEXT_INSTANCE_PROMPT.md`.
4. Read this file (`execution/_Coordination/NEXT_INSTANCE_STATE.md`).
5. Verify `execution/_Reconciliation/DepClosure/_LATEST.md` and the linked snapshot path.

## Current Program State

- Scope Amendment A1 is in effect with 4 frontend baseline deliverables added and fully scaffolded.
- Frontend baseline gate set is now partially satisfied at two nodes: `DEL-01-03` and `DEL-03-07` are `IN_PROGRESS`; `DEL-02-05` and `DEL-07-03` remain `SEMANTIC_READY`.
- Latest full-scope closure run is `BLOCKER`: 36 deliverables, 154 edges (122 unique), 3 SCCs (28 nodes), 0 orphans, 0 isolated, 14 bidirectional pairs.
- Blocker-subset execution-path analysis is acyclic (0 SCCs) for both full-rule and core (PKG-08-excluded) subsets.
- SCA-001 pre-tier policy gate remains active: the 4 frontend gate deliverables must all reach `IN_PROGRESS` before Tier 2 code-bearing execution resumes.
- Wave 0a implementation and evidence are complete at `frontend/` (Next.js + Electron + packaging baseline; `desktop:pack` and `desktop:dist` artifacts produced; packaged app includes `agents/` and `docs/` resources).
- Wave 0b baseline harness API surface is implemented in `frontend/` with route-contract tests passing (`npm test`, `npm run typecheck`) and `npm run build` passing after switching from static export to server-capable Next runtime for API routes.
- Tier 1 active set remains `IN_PROGRESS`: `DEL-05-01`, `DEL-05-02`, `DEL-06-01`, `DEL-07-02`.
- Tier 2 code-bearing set (`DEL-01-01`, `DEL-03-01`, `DEL-05-03`, `DEL-05-04`) is lifecycle-`IN_PROGRESS` but execution-paused by policy gate.
- `DEL-06-02` remains `IN_PROGRESS` and continues independently.
- Data-quality note: `DEL-01-01` rows `DEP-01-01-010` and `DEP-01-01-011` currently have shifted fields (`Status=2026-02-22`, `Notes=ACTIVE`), so they are excluded by strict blocker-subset parsing; policy gate remains authoritative regardless.

### Pre-Tier Gate Wave Sequencing (SCA-001 policy overlay)

| Wave | Deliverables | Internal blocker edges (subset rule) | Current status |
|------|-------------|----------------------------------------|----------------|
| 0a | `DEL-01-03` | None | `IN_PROGRESS` |
| 0b | `DEL-03-07` | `DEL-01-03` (`DEP-03-07-004`, PREREQUISITE) | `IN_PROGRESS` |
| 0c | `DEL-02-05`, `DEL-07-03` | `DEL-01-03` + `DEL-03-07` (`DEP-0205-004/005`, `DEP-07-03-006/007`) | `SEMANTIC_READY`, `SEMANTIC_READY` |

Execution order: `DEL-01-03` -> `DEL-03-07` -> (`DEL-02-05`, `DEL-07-03` in parallel).

### Tier 2 Upstream Snapshot (Blocker subset + policy overlay)

| DEL-ID | Blocker-subset upstream edges (ACTIVE UPSTREAM PREREQUISITE/CONSTRAINT) | Policy overlay |
|--------|--------------------------------------------|----------------|
| DEL-01-01 | `DEL-05-01` (`DEP-01-01-007`, CONSTRAINT, met at `IN_PROGRESS`) | Blocked by SCA-001 pre-tier gate until all 4 frontend gate deliverables reach `IN_PROGRESS` |
| DEL-03-01 | `DEL-05-01` (`DEP-03-01-008`, CONSTRAINT), `DEL-01-03` (`DEP-03-01-016`, CONSTRAINT), `DEL-03-07` (`DEP-03-01-015`, PREREQUISITE) | Blocked by SCA-001 pre-tier gate |
| DEL-05-03 | `DEL-05-02` (`DEP-05-03-006`, PREREQUISITE), `DEL-01-03` (`DEP-05-03-015`, PREREQUISITE), `DEL-03-07` (`DEP-05-03-016`, CONSTRAINT) | Blocked by SCA-001 pre-tier gate |
| DEL-05-04 | `DEL-05-02` (`DEP-05-04-003`, PREREQUISITE), `DEL-01-03` (`DEP-05-04-011`, PREREQUISITE), `DEL-03-07` (`DEP-05-04-012`, CONSTRAINT) | Blocked by SCA-001 pre-tier gate |
| DEL-06-02 | `DEL-06-01` (`DEP-06-02-006`, PREREQUISITE, met at `IN_PROGRESS`) | Not pre-tier-gated |

### Tier 2 Findings Snapshot (Pass 5 baseline; still open)

| DEL-ID | Kickoff finding | Immediate focus |
|--------|------------------|-----------------|
| DEL-01-01 | Packaging evidence queue assumes runnable desktop build scripts in this repo. | Keep paused until pre-tier gate is met; then run `desktop:pack`/`desktop:dist` evidence capture for `instruction-root/docs`. |
| DEL-03-01 | Test-hardening queue assumes session runtime/test files exist in this repo. | Keep paused until pre-tier gate is met; then add targeted REQ-11 regression coverage. |
| DEL-05-03 | Lifecycle module path (`frontend/lib/lifecycle/*`) is absent in current repo tree. | Keep paused until pre-tier gate is met; then implement parser/writer/transition module + tests. |
| DEL-05-04 | Dependency contract path (`frontend/lib/dependencies/*`) is absent in current repo tree. | Keep paused until pre-tier gate is met; then implement v3.1 schema/reader/writer module + tests. |
| DEL-06-02 | Workflow-agent conformance posture remains documentation-driven and local to this repo. | Carry forward REQ-16/CT-001 residuals; keep DEL-06-01 residual watchlist synchronized. |

### Tier 1 Progress Summary

| DEL-ID | Title | Work done | Remaining |
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
7. Scope Amendment A1 pre-tier gate is authoritative: `DEL-01-03`, `DEL-02-05`, `DEL-03-07`, `DEL-07-03` must reach `IN_PROGRESS` before Tier 2 code-bearing execution resumes.

## Core Development Tiers (Execution Queue View)

1. **Pre-Tier Wave 0a:** `DEL-01-03` — `IN_PROGRESS`; implementation and verification evidence captured.
2. **Pre-Tier Wave 0b:** `DEL-03-07` — `IN_PROGRESS`; route surface + contract tests implemented; output-mode conflict resolved.
3. **Pre-Tier Wave 0c:** `DEL-02-05`, `DEL-07-03` — `SEMANTIC_READY`; now unblocked and next in queue (parallel-eligible).
4. **Tier 1 (active):** `DEL-05-01`, `DEL-05-02`, `DEL-06-01`, `DEL-07-02`.
5. **Tier 2 (code-bearing; policy-paused):** `DEL-01-01`, `DEL-03-01`, `DEL-05-03`, `DEL-05-04`.
6. **Tier 2 (independent):** `DEL-06-02`.
7. **Tier 3+:** follow `execution_path_summary.json`/`Execution_Path_Blocker_Analysis.md` after gate completion.

## Immediate Next Actions

1. **Wave 0c execution:** advance `DEL-02-05` and `DEL-07-03` to `IN_PROGRESS` in parallel.
2. **Resume Tier 2 code-bearing queue only after gate completion:** `DEL-05-03`, `DEL-05-04`, `DEL-03-01`, `DEL-01-01`.
3. **Continue Tier 1 and `DEL-06-02` in parallel** where no gate conflict exists.
4. **Fan-in after any dependency row changes:** rerun DEPENDENCIES on changed deliverables, run RECONCILIATION on touched interfaces, then run periodic full-scope `AUDIT_DEP_CLOSURE`.
5. **When `DEL-01-01` is next touched:** rerun DEPENDENCIES for that deliverable to normalize `DEP-01-01-010/011` status-field alignment.

## Handoff Payload (What Carries to Next Session)

1. Stable invariant instructions: `execution/_Coordination/NEXT_INSTANCE_PROMPT.md`.
2. Mutable state and queue: this file (`execution/_Coordination/NEXT_INSTANCE_STATE.md`).
3. Evidence pointers: latest closure and execution-path artifacts under `execution/_Reconciliation/DepClosure/CLOSURE_AUDIT_DEP_CLOSURE_2026-02-22_0838/`.
4. Deliverable-local continuity: `MEMORY.md` and `_STATUS.md` under each `execution/PKG-*/1_Working/DEL-*/` folder.
5. Scope-control record: `execution/_ScopeChange/_LATEST.md` and `execution/_ScopeChange/SCA-001_2026-02-22_0720/`.

## Update Protocol

1. Update `Last Updated` date/context.
2. Update snapshot pointers to latest closure outputs.
3. Update `Current Program State` and `Immediate Next Actions`.
4. Keep history/evidence in reconciliation snapshots and control-loop reports; avoid duplicating long evidence blocks here.
