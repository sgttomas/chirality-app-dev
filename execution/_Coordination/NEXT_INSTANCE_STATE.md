# NEXT INSTANCE STATE — Mutable Handoff Snapshot

This file stores dated/session-changing state for the next agent instance. Update this file at each handoff; keep `NEXT_INSTANCE_PROMPT.md` stable.

**Last Updated:** 2026-02-23 (handoff-finalization: scoped AGENT_CHANGE publish completed for Tier 2 integration-consumer pass with commits `3c6f189` (frontend/runtime/tests) and `43d05ea` (execution handoff evidence), both pushed to `origin/devsession-1`; workspace is clean; `_LATEST` pointer and `CLOSURE_AUDIT_DEP_CLOSURE_2026-02-22_1326` alignment re-verified)

## Current Pointers

| Item | Current pointer |
|---|---|
| Coordination policy | `execution/_Coordination/_COORDINATION.md` |
| Stable startup instructions | `execution/_Coordination/NEXT_INSTANCE_PROMPT.md` |
| Tier 2 control-loop report | `execution/_Coordination/TIER2_CONTROL_LOOP_2026-02-22_PASS8.md` |
| Tier 2 interface reconciliation | `execution/_Reconciliation/TIER2_INTERFACE_RECON_2026-02-22_PASS6.md` |
| Latest closure pointer | `execution/_Reconciliation/DepClosure/_LATEST.md` |
| Full-scope closure snapshot | `execution/_Reconciliation/DepClosure/CLOSURE_AUDIT_DEP_CLOSURE_2026-02-22_1326/` |
| Closure run summary | `execution/_Reconciliation/DepClosure/CLOSURE_AUDIT_DEP_CLOSURE_2026-02-22_1326/RUN_SUMMARY.md` |
| Blocker-subset execution path | `execution/_Reconciliation/DepClosure/CLOSURE_AUDIT_DEP_CLOSURE_2026-02-22_1326/Execution_Path_Blocker_Analysis.md` |
| Machine-readable execution path | `execution/_Reconciliation/DepClosure/CLOSURE_AUDIT_DEP_CLOSURE_2026-02-22_1326/execution_path_summary.json` |
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

- AGENT_CHANGE follow-through is complete for this cycle: mixed tracked/untracked workspace state was split into scoped commits (`ff84706` frontend/runtime/tests/CI, `724bd74` execution evidence + closure snapshots, `a8eb8dc` governance conformance, `8b0a85a` INIT/catch-all), then advanced with this session’s scoped publish commits (`3c6f189`, `43d05ea`).
- Publish step is complete: commits through `43d05ea` are pushed to `origin/devsession-1`; repository is clean (`git status` no local changes) at handoff time.
- `_LATEST.md` pointer and the state-file closure pointers were re-validated in this session and remain aligned to `execution/_Reconciliation/DepClosure/CLOSURE_AUDIT_DEP_CLOSURE_2026-02-22_1326/`.
- Handoff procedure is complete for next session startup (`README.md`/`AGENTS.md`/`NEXT_INSTANCE_PROMPT.md`/`NEXT_INSTANCE_STATE.md` + `_LATEST.md` pointer alignment verified in this session).
- Scope Amendment A1 is in effect with 4 frontend baseline deliverables added and fully scaffolded.
- Frontend baseline gate set is now fully satisfied: `DEL-01-03`, `DEL-03-07`, `DEL-02-05`, and `DEL-07-03` are all `IN_PROGRESS`.
- Latest full-scope closure run is `BLOCKER`: 36 deliverables, 156 edges (123 unique), 3 SCCs (28 nodes), 0 orphans, 0 isolated, 14 bidirectional pairs.
- Blocker-subset execution-path analysis is acyclic (0 SCCs) for both full-rule and core (PKG-08-excluded) subsets.
- SCA-001 pre-tier policy gate condition is now met: Tier 2 code-bearing execution may resume under blocker-subset sequencing.
- Wave 0a implementation and evidence are complete at `frontend/` (Next.js + Electron + packaging baseline; `desktop:pack` and `desktop:dist` artifacts produced; packaged app includes `agents/` and `docs/` resources).
- Wave 0b baseline harness API surface is implemented in `frontend/` with route-contract tests passing (`npm test`, `npm run typecheck`) and `npm run build` passing after switching from static export to server-capable Next runtime for API routes.
- Wave 0c DEL-02-05 implementation is complete to `IN_PROGRESS`: PORTAL/PIPELINE/WORKBENCH shell routes, matrix routing, working-root selection/wiring, file tree panel, chat panel, and unknown-route handling are implemented with `npm test`, `npm run typecheck`, and `npm run build` passing.
- Wave 0c DEL-07-03 implementation is complete to `IN_PROGRESS`: Section 8 validation script, premerge wrapper, CI workflow, artifact hygiene, and runtime marker support are implemented; `npm run harness:validate:premerge` returns `HARNESS_PREMERGE_STATUS=pass` with `HARNESS_PREMERGE_TEST_COUNT=7`.
- Tier 1 active set remains `IN_PROGRESS`: `DEL-05-01`, `DEL-05-02`, `DEL-06-01`.
- Tier 1 DEL-06-01 continuation pass landed:
  - `agents/AGENT_HELP_HUMAN.md`: `AGENT_CLASS` normalized to `PERSONA` (REQ-09 alignment).
  - `agents/AGENT_ORCHESTRATOR.md` and `agents/AGENT_RECONCILIATION.md`: explicit subagent-governance fail-closed contract text added (`subagentGovernance.contextSealed`, `subagentGovernance.pipelineRunApproved`, `subagentGovernance.approvalRef`) with dispatch-time validation steps (REQ-10 alignment).
  - DEL-06-01 `_STATUS.md`/`MEMORY.md` updated with REQ-09/REQ-10 closure evidence.
- Tier 2-independent DEL-06-02 continuation pass landed:
  - DEL-06-02 `_STATUS.md`/`MEMORY.md` refreshed to consume DEL-06-01 closure updates.
  - Residual posture remains: REQ-16 OPEN/TBD and CT-001 pending.
- Tier 1 DEL-07-02 continuation pass landed:
  - Validation script surface confirmed present at `frontend/scripts/validate-harness-section8.mjs` and `frontend/scripts/validate-harness-premerge.mjs`.
  - REQ-10 closure completed with runtime-backed evidence: `HARNESS_PROJECT_ROOT=/Users/ryan/ai-env/projects/chirality-app-dev/examples/example-project HARNESS_BASE_URL=http://127.0.0.1:3000 npm run harness:validate:premerge` returned `HARNESS_VALIDATION_STATUS=pass`, `HARNESS_PREMERGE_STATUS=pass`, `HARNESS_PREMERGE_TEST_COUNT=7`; stable artifact at `frontend/artifacts/harness/section8/latest/summary.json`.
  - Remaining scope-TBD rulings closed: minimum example-root count set to 1 (`examples/example-project/`), and `Dependencies.csv` sample inclusion set OUT for current baseline.
  - Lifecycle advanced to `CHECKING` with acceptance-gate readiness evidence recorded in deliverable-local `_STATUS.md` and `MEMORY.md`.
- Tier 2 code-bearing set (`DEL-01-01`, `DEL-03-01`, `DEL-05-03`, `DEL-05-04`) remains lifecycle-`IN_PROGRESS` and is no longer policy-paused.
- DEL-05-03 implementation pass landed in this workspace:
  - `frontend/src/lib/lifecycle/status-parser.ts`
  - `frontend/src/lib/lifecycle/status-writer.ts`
  - `frontend/src/lib/lifecycle/transition.ts`
  - tests: `frontend/src/__tests__/lib/lifecycle-status.test.ts`
- DEL-05-04 implementation pass landed in this workspace:
  - `frontend/src/lib/dependencies/schema.ts`
  - `frontend/src/lib/dependencies/csv-utils.ts`
  - `frontend/src/lib/dependencies/register-reader.ts`
  - `frontend/src/lib/dependencies/register-writer.ts`
  - tests: `frontend/src/__tests__/lib/dependencies-register-contract.test.ts`
- DEL-05-03 + DEL-05-04 integration pass landed in this workspace:
  - `frontend/src/lib/workspace/deliverable-contracts.ts`
  - `frontend/src/app/api/working-root/deliverable/status/route.ts`
  - `frontend/src/app/api/working-root/deliverable/status/transition/route.ts`
  - `frontend/src/app/api/working-root/deliverable/dependencies/route.ts`
  - tests: `frontend/src/__tests__/api/working-root/deliverable-contracts.test.ts`
- Verification for this pass: `npm test`, `npm run typecheck`, and `npm run build` all passed in `frontend/` (31 tests total).
- Tier 2 fan-in control checks for this integration pass are complete:
  - DEPENDENCIES rerun on `DEL-05-03` and `DEL-05-04` with updated evidence and lifecycle closure fields.
  - Gating rows now `SATISFIED`: `DEP-05-03-015`, `DEP-05-03-016`, `DEP-05-04-011`, `DEP-05-04-012`.
  - Reconciliation refresh written to `execution/_Reconciliation/TIER2_INTERFACE_RECON_2026-02-22_PASS6.md`.
- Tier 2 DEL-03-01 hardening pass landed in this workspace:
  - `frontend/src/lib/harness/session-manager.ts` (`assertProjectRootAccessible` export + stronger root accessibility checks)
  - `frontend/src/lib/harness/persona-manager.ts` (instruction-root persona existence checks with `PERSONA_NOT_FOUND`)
  - `frontend/src/lib/harness/agent-sdk-manager.ts` (deterministic bootstrap-failure marker for regression pathing)
  - `frontend/src/app/api/harness/session/boot/route.ts` (boot-time working-root/persona checks + explicit `SDK_FAILURE` mapping)
  - tests: `frontend/src/__tests__/api/harness/routes.test.ts` now includes targeted REQ-11 regression scenarios.
- Tier 2 DEL-01-01 evidence refresh completed in this workspace:
  - `npm run desktop:pack` and `npm run desktop:dist` both passed in `frontend/`.
  - Artifacts refreshed at `frontend/dist/` including `Chirality-0.1.0-arm64.dmg` and `dist/mac-arm64/Chirality.app`.
  - Verified app binary architecture is `arm64` and bundle resources include `agents/` and `docs/`.
- Verification for this pass: `npm test` (36 tests), `npm run typecheck`, and `npm run build` all passed in `frontend/`.
- DEL-01-01 typecheck determinism hardening landed:
  - `frontend/package.json` `typecheck` now runs non-incremental TS checks to avoid stale `.next/types` cache failures between cycles.
- Tier 2 DEL-01-01 + DEL-03-01 DEPENDENCIES fan-in refresh is complete:
  - `DEP-01-01-010`, `DEP-01-01-011`, `DEP-03-01-015`, and `DEP-03-01-016` are now `SatisfactionStatus=SATISFIED`.
  - Deliverable-local `_DEPENDENCIES.md` and `MEMORY.md` updated with fan-in evidence and lifecycle verification references.
- Tier 2 integration-consumer continuation pass landed in this workspace:
  - Added client helper layer at `frontend/src/lib/workspace/deliverable-api.ts` (typed route consumption + dependency summary helpers).
  - PIPELINE surface now consumes `status` + `dependencies` routes and submits `status/transition` updates from selected deliverable scope (`frontend/src/app/pipeline/pipeline-client.tsx`).
  - Added PIPELINE contract panel styling (`frontend/src/app/globals.css`) and helper tests (`frontend/src/__tests__/lib/workspace-deliverable-api.test.ts`).
  - Deliverable-local continuity updated in:
    - `execution/PKG-02_Desktop_UI_Workflow/1_Working/DEL-02-05_Frontend_Workflow_Shell/MEMORY.md`
    - `execution/PKG-05_Filesystem_Execution_Model/1_Working/DEL-05-03_Lifecycle_State_Handling/MEMORY.md`
    - `execution/PKG-05_Filesystem_Execution_Model/1_Working/DEL-05-04_Dependency_Tracking_Contract/MEMORY.md`
  - Verification for this pass: `npm test` (42 tests), `npm run typecheck`, and `npm run build` passed in `frontend/`.
- `DEL-06-02` remains `IN_PROGRESS` and continues independently.
- Periodic full-scope closure rerun completed at `execution/_Reconciliation/DepClosure/CLOSURE_AUDIT_DEP_CLOSURE_2026-02-22_1326/` and `_LATEST.md` now points to this snapshot.
- Data-quality caveat for `DEL-01-01` is resolved: `DEP-01-01-010/011` now parse with aligned v3.1 fields (`Status=ACTIVE`, explanatory text in `Notes`) and are included in blocker-subset analysis.

### Pre-Tier Gate Wave Sequencing (SCA-001 policy overlay)

| Wave | Deliverables | Internal blocker edges (subset rule) | Current status |
|------|-------------|----------------------------------------|----------------|
| 0a | `DEL-01-03` | None | `IN_PROGRESS` |
| 0b | `DEL-03-07` | `DEL-01-03` (`DEP-03-07-004`, PREREQUISITE) | `IN_PROGRESS` |
| 0c | `DEL-02-05`, `DEL-07-03` | `DEL-01-03` + `DEL-03-07` (`DEP-0205-004/005`, `DEP-07-03-006/007`) | `IN_PROGRESS`, `IN_PROGRESS` |

Execution order: `DEL-01-03` -> `DEL-03-07` -> (`DEL-02-05`, `DEL-07-03` in parallel).

### Tier 2 Upstream Snapshot (Blocker subset + policy overlay)

| DEL-ID | Blocker-subset upstream edges (ACTIVE UPSTREAM PREREQUISITE/CONSTRAINT) | Policy overlay |
|--------|--------------------------------------------|----------------|
| DEL-01-01 | `DEL-05-01` (`DEP-01-01-007`, CONSTRAINT, met at `IN_PROGRESS`), `DEL-01-03` (`DEP-01-01-010`, PREREQUISITE), `DEL-03-07` (`DEP-01-01-011`, PREREQUISITE) | SCA-001 pre-tier gate met; eligible for queued execution |
| DEL-03-01 | `DEL-05-01` (`DEP-03-01-008`, CONSTRAINT), `DEL-01-03` (`DEP-03-01-016`, CONSTRAINT), `DEL-03-07` (`DEP-03-01-015`, PREREQUISITE) | SCA-001 pre-tier gate met; eligible for queued execution |
| DEL-05-03 | `DEL-05-02` (`DEP-05-03-006`, PREREQUISITE), `DEL-01-03` (`DEP-05-03-015`, PREREQUISITE), `DEL-03-07` (`DEP-05-03-016`, CONSTRAINT) | SCA-001 pre-tier gate met; eligible for queued execution |
| DEL-05-04 | `DEL-05-02` (`DEP-05-04-003`, PREREQUISITE), `DEL-01-03` (`DEP-05-04-011`, PREREQUISITE), `DEL-03-07` (`DEP-05-04-012`, CONSTRAINT) | SCA-001 pre-tier gate met; eligible for queued execution |
| DEL-06-02 | `DEL-06-01` (`DEP-06-02-006`, PREREQUISITE, met at `IN_PROGRESS`) | Not pre-tier-gated |

### Tier 2 Findings Snapshot (Pass 10 continuation + closure refresh)

| DEL-ID | Kickoff finding | Immediate focus |
|--------|------------------|-----------------|
| DEL-01-01 | Packaging evidence and arm64 artifact checks were re-run successfully in this repo (`desktop:pack`, `desktop:dist`). DEPENDENCIES normalization pass corrected `DEP-01-01-010/011` CSV field alignment and closure pointers were refreshed. | Continue Tier 2 integration consumers; keep DEL-01-01 upstream gating edges (`DEP-01-01-010/011`) tracked in blocker-subset sequencing. |
| DEL-03-01 | REQ-11 regression coverage and boot-time root/persona checks are now implemented in route/runtime code. | Wire the updated boot error taxonomy through any higher-level workflow/reporting surfaces that currently assume generic boot failures. |
| DEL-05-03 | Lifecycle module + route-level API integration are now present under `frontend/src/lib/lifecycle/*` and `frontend/src/app/api/working-root/deliverable/status*`. | Propagate transition endpoint into UI/workflow orchestration paths where state changes are initiated; keep approval-SHA binding traceable on human issuance paths. |
| DEL-05-04 | Dependency contract module + deliverable API integration are now present under `frontend/src/lib/dependencies/*` and `frontend/src/app/api/working-root/deliverable/dependencies`. | Connect dependency route usage to dependency-producing/consuming workflows (DEPENDENCIES/RECONCILIATION path) and keep periodic closure reruns aligned with row updates. |
| DEL-06-02 | Workflow-agent conformance posture remains documentation-driven and local to this repo; latest pass consumed DEL-06-01 REQ-09/REQ-10 closure updates. | Carry forward REQ-16/CT-001 residuals; DEL-06-01 residual watchlist now centers on REQ-05 + WRITE_SCOPE canonical-set conflict. |

### Tier 1 Progress Summary

| DEL-ID | Title | Work done | Remaining |
|--------|-------|-----------|-----------|
| DEL-05-01 | Instruction Root Bundling | Prior pass reports claim repo-local mitigations, but current tracked tree has no runtime implementation surface to verify. | Reconcile/restore runtime tree, rerun packaging evidence, then address SHA-256 integrity, read-only enforcement, and degradation behavior. |
| DEL-05-02 | Execution Root Scaffolding | Repo-local audit; 0% implemented. Implementation plan with module design in MEMORY.md. | Build scaffolding module (`scaffold.ts`, `sanitize.ts`), API endpoint, conformance tests. |
| DEL-06-01 | Agent Instruction Conformance | Audit continuation landed: REQ-09/REQ-10 now closed (`AGENT_HELP_HUMAN.md` class fix + fail-closed governance language in subagent-capable managers). | REQ-05 precedence SHOULD/MUST ruling and WRITE_SCOPE canonical-set conflict (`project-level` vs `workspace-scaffold-only`). |
| DEL-07-02 | Example Execution Roots | Example fixture created at `examples/example-project/` (1 pkg, 3 dels, 3 lifecycle states). DEL-07-01 script surface confirmed present. Runtime-backed REQ-10 validation passed with `HARNESS_PREMERGE_STATUS=pass` and `HARNESS_PREMERGE_TEST_COUNT=7`. Scope rulings applied: minimum root count = 1; `Dependencies.csv` inclusion = OUT for baseline. Deliverable moved to `CHECKING`. | Review outcome and decide `CHECKING -> ISSUED` (or return to `IN_PROGRESS` if findings emerge). |

## Active Human Rulings and Assumptions

1. Blocker maturity threshold is `IN_PROGRESS`.
2. Execution sequencing uses blocker-subset filtering from `_COORDINATION.md`; full graph remains audit/reconciliation truth.
3. PKG-08 (`DEL-08-*`) stays traceable but non-driving until SOW-032..038 are explicitly ruled `IN`.
4. TASK dispatch is globally pre-authorized; no per-task human approval gate.
5. TASK execution is one deliverable per session; each session closes after bounded completion and new sessions are booted for queued work.
6. Execution and implementation edits are scoped to this repository only (`/Users/ryan/ai-env/projects/chirality-app-dev`) unless explicitly re-ruled by a human.
7. Scope Amendment A1 pre-tier gate is authoritative: `DEL-01-03`, `DEL-02-05`, `DEL-03-07`, `DEL-07-03` must reach `IN_PROGRESS` before Tier 2 code-bearing execution resumes.
8. Working-memory authority is deliverable-local only: use `execution/PKG-*/1_Working/DEL-*/MEMORY.md` as the sole memory record; do not use agent/profile memory as project-state authority.
9. `_MEMORY.md` is disabled for this project profile; if encountered in legacy state, migrate needed content into `MEMORY.md` and remove `_MEMORY.md`.
10. DEL-07-02 ruling: baseline example-root count is fixed at 1 (`examples/example-project/`) unless re-ruled.
11. DEL-07-02 ruling: `Dependencies.csv` samples are OUT for current baseline scope unless re-ruled.

## Core Development Tiers (Execution Queue View)

1. **Pre-Tier Wave 0a:** `DEL-01-03` — `IN_PROGRESS`; implementation and verification evidence captured.
2. **Pre-Tier Wave 0b:** `DEL-03-07` — `IN_PROGRESS`; route surface + contract tests implemented; output-mode conflict resolved.
3. **Pre-Tier Wave 0c:** `DEL-02-05`, `DEL-07-03` — `IN_PROGRESS`; implementation and verification evidence captured; pre-tier gate satisfied.
4. **Tier 1 (active):** `DEL-05-01`, `DEL-05-02`, `DEL-06-01`.
5. **Tier 1 (checking):** `DEL-07-02`.
6. **Tier 2 (code-bearing; unpaused):** `DEL-01-01`, `DEL-03-01`, `DEL-05-03`, `DEL-05-04`.
7. **Tier 2 (independent):** `DEL-06-02`.
8. **Tier 3+:** follow `execution_path_summary.json`/`Execution_Path_Blocker_Analysis.md` after gate completion.

## Immediate Next Actions

1. **Start the next cycle from pushed baseline `43d05ea`** (clean workspace; no local carry-over required).
2. **Continue Tier 1 and `DEL-06-02` in parallel** where no blocker conflict exists.
3. **Extend Tier 2 consumer wiring beyond PIPELINE** (DEL-03-01 boot error taxonomy propagation + reconciliation/workflow consumption paths).
4. **Complete DEL-07-02 checking pass** and record decision (`ISSUED` or return to `IN_PROGRESS` with findings).

## Handoff Payload (What Carries to Next Session)

1. Stable invariant instructions: `execution/_Coordination/NEXT_INSTANCE_PROMPT.md`.
2. Mutable state and queue: this file (`execution/_Coordination/NEXT_INSTANCE_STATE.md`).
3. Evidence pointers: latest closure and execution-path artifacts under `execution/_Reconciliation/DepClosure/CLOSURE_AUDIT_DEP_CLOSURE_2026-02-22_1326/`.
4. Deliverable-local continuity: `MEMORY.md` and `_STATUS.md` under each `execution/PKG-*/1_Working/DEL-*/` folder (`_MEMORY.md` disabled in this project profile).
5. Scope-control record: `execution/_ScopeChange/_LATEST.md` and `execution/_ScopeChange/SCA-001_2026-02-22_0720/`.

## Update Protocol

1. Update `Last Updated` date/context.
2. Update snapshot pointers to latest closure outputs.
3. Update `Current Program State` and `Immediate Next Actions`.
4. Keep history/evidence in reconciliation snapshots and control-loop reports; avoid duplicating long evidence blocks here.
