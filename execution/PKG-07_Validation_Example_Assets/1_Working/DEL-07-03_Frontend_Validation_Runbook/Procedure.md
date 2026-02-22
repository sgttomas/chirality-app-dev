# Procedure -- DEL-07-03 Frontend Validation & Runbook Baseline

## Purpose

This procedure describes the steps to implement the frontend validation scripts, produce the deterministic summary artifact, create the local validation runbooks, and verify the deliverable meets its acceptance criteria. It covers both the development of validation artifacts and the operational execution of the validation workflow.

## Prerequisites

| Prerequisite | Description | Source |
|-------------|-------------|--------|
| PR-01 | macOS 15+ on Apple Silicon development machine | DEC-PLAT-001 |
| PR-02 | Node.js runtime installed (version TBD -- must be compatible with Electron + Next.js stack; see Guidance CT-001) | **ASSUMPTION** -- implied by `.mjs` script format |
| PR-03 | Repository cloned; `frontend/` workspace bootstrapped and buildable (depends on DEL-01-03 completion) | SOW-044; Decomposition DEL-01-03 |
| PR-04 | Harness server startable from `frontend/` (`npm run dev` resolves) | `docs/harness/harness_manual_validation.md` Prerequisites |
| PR-05 | Anthropic API key available (`ANTHROPIC_API_KEY` set in environment; provisioning contract TBD per OI-001) | `docs/harness/harness_manual_validation.md` Prerequisites; OI-001 |
| PR-06 | `docs/harness/harness_manual_validation.md` accessible (canonical reference for script behavior and Section 8 matrix) | `_REFERENCES.md` R1 |
| PR-07 | `docs/harness/harness_ci_integration.md` accessible (canonical reference for CI workflow) | `_REFERENCES.md` R2 |
| PR-08 | `docs/harness/harness_artifact_mirroring_guidance.md` accessible (canonical reference for mirroring posture) | `_REFERENCES.md` R3 |
| PR-09 | DEL-03-07 (Harness API Baseline) functional -- provides the `/api/harness/session/*` and `/api/harness/turn` route surfaces that validation scripts exercise | Decomposition SCA-001; **ASSUMPTION** -- validation requires API surfaces to exist |

## Steps

### Phase 1: Environment Verification

**Objective:** Confirm the workspace is ready for validation script development and execution.

**Entry gate:** PR-01 through PR-09 satisfied.

| Step | Action | Verification | Notes |
|------|--------|-------------|-------|
| 1.1 | Verify `frontend/` directory exists in workspace | Directory present | Source: `docs/harness/harness_manual_validation.md` Local-Only Boundary |
| 1.2 | Verify `frontend/package.json` exists and contains baseline scripts | File present and parseable as JSON | Source: DEL-01-03 output |
| 1.3 | Run `echo "${ANTHROPIC_API_KEY:+set}"` to confirm API key is available | Output: `set` | Source: `docs/harness/harness_manual_validation.md` Prerequisites |
| 1.4 | Start frontend server: `cd frontend && npm run dev -- --hostname 127.0.0.1 --port 3000` | Server starts and listens | Source: `docs/harness/harness_manual_validation.md` Usage step 1 |
| 1.5 | Poll harness readiness: `curl -s "http://127.0.0.1:3000/api/harness/session/list?projectRoot=/tmp" >/dev/null` | Returns successfully (HTTP 200) | Source: `docs/harness/harness_manual_validation.md` Prerequisites |

**Error handling:** If `frontend/` is missing, record `RUNTIME_SURFACE_MISSING` in coordination artifacts and halt. If the harness server does not start, verify PR-03 and PR-04 and report the failure. Do not proceed with script development against a non-functional runtime.

### Phase 2: Section 8 Validation Script Implementation

**Objective:** Implement `frontend/scripts/validate-harness-section8.mjs` covering the Section 8 SDK-native test matrix.

**Entry gate:** Phase 1 complete -- workspace verified and harness server reachable.

| Step | Action | Verification | Notes |
|------|--------|-------------|-------|
| 2.1 | Implement `setup.server_reachable` check: verify harness at `HARNESS_BASE_URL` is reachable before running Section 8 tests | Check passes against running harness | Source: `docs/harness/harness_manual_validation.md` Additional Regression Checks |
| 2.2 | Implement `regression.session_crud` check: verify session create/read/update/delete operations via `/api/harness/session/*` endpoints | CRUD operations succeed | Source: `docs/harness/harness_manual_validation.md` Additional Regression Checks |
| 2.3 | Implement `section8.smoke_stream`: verify SSE event sequence `session:init`, `chat:delta`, `chat:complete`, `session:complete`, `process:exit` | Events arrive in specified order | Source: `docs/harness/harness_manual_validation.md` Section 8 Matrix row 1 |
| 2.4 | Implement `section8.session_persistence_resume`: verify `claudeSessionId` persists; resumed turn emits `session:init` with matching persisted value | Persistence and resume verified | Source: `docs/harness/harness_manual_validation.md` Section 8 Matrix row 2 |
| 2.5 | Implement `section8.permissions_dontask`: verify deny case blocks unapproved Bash; allow case emits `tool:result` with `UNAPPROVED_ALLOW_TEST` | Both deny and allow behaviors verified | Source: `docs/harness/harness_manual_validation.md` Section 8 Matrix row 3 |
| 2.6 | Implement `section8.interrupt_sigint`: verify `/api/harness/interrupt` returns `200 {"ok":true}`; stream emits terminal `process:exit` with interruption marker | Interrupt API and stream behavior verified | Source: `docs/harness/harness_manual_validation.md` Section 8 Matrix row 4 |
| 2.7 | Implement `section8.sdk_native_stream`: verify turn emits `chat:complete` + `process:exit`; no `parse:error` logs | SDK-native stream handling verified | Source: `docs/harness/harness_manual_validation.md` Section 8 Matrix row 5 |
| 2.8 | Implement machine-readable stdout output: `HARNESS_VALIDATION_SUMMARY_PATH=<path>`, `HARNESS_VALIDATION_STATUS=pass|fail` | Output variables emitted on stdout | Source: `docs/harness/harness_manual_validation.md` Machine-Readable Outputs |
| 2.9 | Write summary artifact to `${TMPDIR:-/tmp}/chirality-harness-validation/latest/summary.json` with per-test pass/fail results | Summary file created and valid JSON | Source: `docs/harness/harness_manual_validation.md` Artifact Layout |
| 2.10 | Ensure script exits with code 0 on all-pass and non-zero on any failure | Exit codes verified | Source: Specification REQ-09 |

**Error handling:** If any Section 8 test fails during development, determine whether the failure is a script defect (fix the script) or a harness runtime defect (document as a blocking issue and report). Do not force-pass a failing test. If the harness becomes unreachable during development, restart from Phase 1 Step 1.4.

### Phase 3: Pre-Merge Wrapper Implementation

**Objective:** Implement `frontend/scripts/validate-harness-premerge.mjs` that wraps Section 8 validation with stable artifact copy and schema validation.

**Entry gate:** Phase 2 complete -- Section 8 script implemented and passing.

| Step | Action | Verification | Notes |
|------|--------|-------------|-------|
| 3.1 | Implement wrapper that invokes the Section 8 validation script | Section 8 tests execute through wrapper | Source: `docs/harness/harness_manual_validation.md` Pre-merge wrapper |
| 3.2 | Implement stable artifact copy: copy `summary.json` from `${TMPDIR:-/tmp}/chirality-harness-validation/latest/` to `frontend/artifacts/harness/section8/latest/summary.json` | Stable copy exists after run | Source: `docs/harness/harness_manual_validation.md` Summary locations |
| 3.3 | Implement summary schema validation: verify required SDK test IDs are present; verify legacy `regression.api_chat_reachability` is absent | Schema validation runs and reports pass/fail | Source: `docs/harness/harness_ci_integration.md` Job Flow step 7 |
| 3.4 | Implement machine-readable stdout output: `HARNESS_PREMERGE_ARTIFACT_PATH`, `HARNESS_PREMERGE_SOURCE_SUMMARY_PATH`, `HARNESS_PREMERGE_STATUS`, `HARNESS_PREMERGE_TEST_COUNT` | Output variables emitted | Source: `docs/harness/harness_manual_validation.md` Machine-Readable Outputs |
| 3.5 | Ensure wrapper exits with code 0 on pass and non-zero on fail (including schema validation failure) | Exit codes verified | Source: `docs/harness/harness_ci_integration.md` Failure Expectations |
| 3.6 | Add `harness:validate:premerge` script entry to `frontend/package.json` | `npm run harness:validate:premerge` resolves and executes wrapper | Source: Specification REQ-04 |

**Error handling:** If stable artifact copy fails (permissions, disk space), halt and resolve before proceeding. If schema validation fails on a valid summary, review the required test ID list against the actual Section 8 matrix.

### Phase 4: CI Workflow Implementation

**Objective:** Implement `.github/workflows/harness-premerge.yml` for automated pre-merge validation.

**Entry gate:** Phase 3 complete -- pre-merge wrapper functional.

| Step | Action | Verification | Notes |
|------|--------|-------------|-------|
| 4.1 | Create `.github/workflows/harness-premerge.yml` implementing the job flow: checkout, Node.js setup, `npm ci`, server start, readiness poll, `npm run harness:validate:premerge`, verify summary, upload artifact | Workflow file exists and is valid YAML | Source: `docs/harness/harness_ci_integration.md` Job Flow |
| 4.2 | Add fail-fast preflight step: verify `frontend/scripts/validate-harness-premerge.mjs` exists before running validation | Preflight step present in workflow | Source: `docs/harness/harness_ci_integration.md` Local-Only Boundary; Specification REQ-11 |
| 4.3 | Configure CI environment variables: `HARNESS_BASE_URL`, `ANTHROPIC_API_KEY` (as secret) | Environment variables configured in workflow | Source: `docs/harness/harness_ci_integration.md` CI Prerequisites |
| 4.4 | Configure artifact upload: `frontend/artifacts/harness/section8/latest/summary.json` | Upload step present; artifact name defined | Source: `docs/harness/harness_ci_integration.md` Job Flow step 9 |

**Error handling:** If the CI platform is not yet configured (e.g., GitHub Actions secrets not set), document the remaining configuration steps and mark them as prerequisites for CI activation. The workflow file can be committed before secrets are configured.

### Phase 5: Runbook and Architecture Documentation

**Objective:** Produce local validation runbook and frontend validation architecture documentation per SOW-049.

**Entry gate:** Phase 3 complete (Phase 4 may be parallel).

| Step | Action | Verification | Notes |
|------|--------|-------------|-------|
| 5.1 | Review existing `docs/harness/harness_manual_validation.md` for completeness against Specification REQ-12 criteria | Gap list produced | Source: SOW-049; Specification REQ-12 |
| 5.2 | Update `docs/harness/harness_manual_validation.md` to fill identified gaps: ensure prerequisites are complete, Section 8 matrix is documented, machine-readable output is explained, local-only boundary is clear | Updated document covers all REQ-12 items | Source: Specification REQ-12; Guidance T1 |
| 5.3 | Review existing `docs/harness/harness_ci_integration.md` for completeness against Specification REQ-13 criteria | Gap list produced | Source: SOW-049; Specification REQ-13 |
| 5.4 | Update `docs/harness/harness_ci_integration.md` to fill identified gaps: ensure architecture relationships are documented, schema validation expectations are clear | Updated document covers REQ-13 items | Source: Specification REQ-13 |
| 5.5 | Review existing `docs/harness/harness_artifact_mirroring_guidance.md` against Specification REQ-16 criteria | Gap list produced | Source: Specification REQ-16 |
| 5.6 | Update `docs/harness/harness_artifact_mirroring_guidance.md` if gaps found; ensure mirroring posture, guardrails, and when-to-enable guidance are documented | Updated or confirmed complete | Source: Specification REQ-16 |
| 5.7 | Produce a lightweight runbook index/entry-point document that links to the three `docs/harness/` files and provides orientation for new developers | Index document created | Source: SOW-049; Guidance T1 (PROPOSAL) |

**Error handling:** If existing documentation is found to be substantially incomplete or incorrect relative to the implemented scripts, prioritize documentation updates before Phase 6. Do not mark documentation complete if it contradicts script behavior (see Guidance P3).

### Phase 6: Verification and Handoff

**Objective:** Confirm all deliverable artifacts meet specifications.

**Entry gate:** Phases 2-5 complete.

| Step | Action | Verification | Notes |
|------|--------|-------------|-------|
| 6.1 | Run full local validation sequence: start server, run `npm run harness:validate:premerge`, read summary | All Section 8 tests pass; summary artifact at stable path | Source: `docs/harness/harness_manual_validation.md` Usage |
| 6.2 | Verify deterministic summary: run `npm run harness:validate:premerge` twice consecutively; compare `summary.json` outputs for structural consistency | Same test IDs present in both runs; same pass/fail outcomes | Source: Specification REQ-03; **ASSUMPTION** -- repeatability check |
| 6.3 | Verify machine-readable output: parse stdout of both scripts for required output variables | All variables present and correctly formatted | Source: Specification REQ-08 |
| 6.4 | Verify CI workflow file: inspect `.github/workflows/harness-premerge.yml` against Job Flow steps 1-9 | All steps present | Source: Specification REQ-10 |
| 6.5 | Verify fail-fast preflight: inspect CI workflow for script existence check | Preflight step present | Source: Specification REQ-11 |
| 6.6 | Verify runtime surface missing detection: temporarily rename `frontend/scripts/validate-harness-premerge.mjs`; run scripts; confirm `RUNTIME_SURFACE_MISSING` behavior | Detection works correctly | Source: Specification REQ-14 |
| 6.7 | Verify documentation completeness: review runbook against REQ-12 checklist (6 items), architecture doc against REQ-13 checklist (4 items), mirroring guidance against REQ-16 checklist (5 items) | All items present | Source: Specification REQ-12, REQ-13, REQ-16 |
| 6.8 | Verify all anticipated artifact types produced: TEST (summary.json produced by execution), SCRIPT (validation scripts + CI workflow), DOC (runbook + architecture documentation) | All three artifact types present | Source: `_CONTEXT.md` Anticipated Artifacts |
| 6.9 | Confirm local-only execution: verify no non-local repository or external resource was required during the full validation run | No external dependencies | Source: Specification REQ-05; OBJ-008 |

**Error handling:** If any verification step fails, return to the relevant phase to address the gap. Document any exceptions or deferred items with rationale. Do not proceed to handoff with known verification failures.

## Verification

| Check | What to Verify | Method |
|-------|----------------|--------|
| V-01 | Section 8 validation script exists and covers all 5 behavioral checks | Inspect `frontend/scripts/validate-harness-section8.mjs`; run and confirm 5 test IDs in output |
| V-02 | Pre-merge wrapper exists and produces stable artifact | Run `npm run harness:validate:premerge`; verify `frontend/artifacts/harness/section8/latest/summary.json` |
| V-03 | Deterministic summary is valid JSON with per-test results | Parse summary.json; verify structure |
| V-04 | npm run target resolves | Run `npm run harness:validate:premerge`; confirm execution |
| V-05 | Machine-readable output on stdout | Parse stdout for required variables |
| V-06 | CI workflow covers all 9 job flow steps | Inspect `.github/workflows/harness-premerge.yml` |
| V-07 | Fail-fast preflight in CI | Inspect workflow for script existence check |
| V-08 | Runbook documentation complete | Review against REQ-12 six-item checklist |
| V-09 | Architecture documentation complete | Review against REQ-13 four-item checklist |
| V-10 | Local-only execution verified | Full run with no external dependencies |
| V-11 | Runtime surface missing detection works | Test with missing scripts |
| V-12 | Repeatability: two consecutive runs produce consistent results | Compare summary artifacts from two runs |

## Records

| Record | Description | Location |
|--------|-------------|----------|
| Validation scripts | Core Section 8 script + pre-merge wrapper | `frontend/scripts/validate-harness-section8.mjs`, `frontend/scripts/validate-harness-premerge.mjs` |
| CI workflow | GitHub Actions pre-merge workflow | `.github/workflows/harness-premerge.yml` |
| Deterministic summary artifact | Produced by script execution (not committed) | `frontend/artifacts/harness/section8/latest/summary.json` |
| Ephemeral validation artifacts | Full artifact set in temp directory (not committed) | `${TMPDIR:-/tmp}/chirality-harness-validation/latest/` |
| Local validation runbook | How to run validation, interpret results, prerequisites | `docs/harness/harness_manual_validation.md` (updated per Phase 5) |
| CI integration documentation | CI workflow setup and operation | `docs/harness/harness_ci_integration.md` (updated per Phase 5) |
| Artifact mirroring guidance | When and how to mirror full artifacts | `docs/harness/harness_artifact_mirroring_guidance.md` (updated per Phase 5) |
| Runbook index | Entry-point document linking to harness docs | TBD -- `docs/harness/` or deliverable-local (see Guidance CT-002) |
