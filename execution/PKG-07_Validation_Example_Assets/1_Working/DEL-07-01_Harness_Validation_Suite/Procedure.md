# Procedure -- DEL-07-01 Harness Validation Suite

## Purpose

This procedure describes the steps to produce, execute, and maintain the Harness Validation Suite. It covers both the development of validation scripts/documentation and the operational execution of the suite for local and CI validation gates.

## Prerequisites

| Prerequisite | Description | Source |
|-------------|-------------|--------|
| PR-01 | macOS 15+ on Apple Silicon development machine | DEC-PLAT-001 |
| PR-02 | Node.js runtime installed (version TBD -- must be compatible with Electron + Next.js stack; no minimum version specified in governance documents; see Guidance CT-003) | **ASSUMPTION** -- implied by application stack; Lensing B-001 |
| PR-03 | Repository cloned and buildable (`frontend/` application runs locally) | SOW-001; Decomposition PKG-01 |
| PR-04 | Harness runtime available (application starts and serves API endpoints) | Implied by test suite target -- requires DEL-03-01 (session boot) and DEL-03-02 (turn execution) to be functional |
| PR-05 | Anthropic API key available (for integration tests only -- provisioning contract TBD per OI-001) | OI-001; DEC-NET-001 |
| PR-06 | Valid working root directory available for session boot tests | SPEC Section 9.8; SOW-003 |
| PR-07 | `docs/SPEC.md` accessible (harness contract reference) | Specification REQ-01 through REQ-10 |
| PR-08 | Upstream deliverables DEL-03-01 through DEL-03-06 and DEL-04-01 provide the harness behaviors to validate | **ASSUMPTION** -- validation suite tests harness runtime outputs from PKG-03 and PKG-04 |

## Steps

### Phase 1: Test Inventory Design

**Objective:** Define the test inventory covering all six harness behavioral areas.

**Entry gate:** PR-01 through PR-07 satisfied. `docs/SPEC.md` Sections 9.7-9.8 accessible.

| Step | Action | Verification | Notes |
|------|--------|-------------|-------|
| 1.1 | Review `docs/SPEC.md` Sections 9.7-9.8 to extract testable contract assertions | List of testable assertions per behavioral area | Source: SPEC |
| 1.2 | Organize assertions into test groups by behavioral area: (a) Session lifecycle, (b) Turn execution, (c) SSE streaming, (d) Opts/fallback chains, (e) Subagent governance, (f) Attachment contract | Test group inventory document | Source: Specification REQ-01 |
| 1.3 | For each test group, identify which tests require a live API key and which can run with mocked/stubbed responses | Classification: "contract tests" vs. "integration tests" | Source: Guidance T1 |
| 1.4 | Document prerequisite fixtures needed (attachment test files, example working roots, governance metadata fixtures) | Fixture requirements list | Source: Guidance C4 |
| 1.5 | Review DEL-07-02 example execution roots for potential reuse as test fixtures | Decision: use shared fixtures or dedicated test fixtures | Source: Guidance C6 |
| 1.6 | Map each planned test to its corresponding REQ(s) and K-invariant(s) to establish traceability | Traceability mapping draft | Source: Specification REQ-13, REQ-16; Lensing X-005 |

**Error handling:** If SPEC Sections 9.7-9.8 are unavailable or incomplete, record missing sections as TBD in the test inventory and report to the human. Do not invent contract assertions. If DEL-07-02 fixtures are not yet available, proceed with dedicated test fixtures (Step 1.4).

### Phase 2: Validation Script Development

**Objective:** Implement the validation scripts.

**Entry gate:** Phase 1 complete -- test inventory document and traceability mapping exist.

| Step | Action | Verification | Notes |
|------|--------|-------------|-------|
| 2.1 | Create test fixture generation scripts producing: (a) `.txt` file of exactly 10,000,000 bytes, (b) `.txt` file of exactly 10,000,001 bytes, (c) `.png` file with valid extension, (d) `.xyz` file with unsupported extension, (e) symlink to a valid file, (f) empty directory, (g) set of files totaling exactly 18,000,000 bytes combined, (h) set of files totaling 18,000,001 bytes combined, (i) governance metadata samples (`contextSealed`/`pipelineRunApproved`/`approvalRef` in valid and invalid combinations), (j) example working root directory with known content | Fixtures generated and verified for correctness (file sizes confirmed, symlink valid, directory exists) | Source: Guidance C4; Specification REQ-09; Lensing D-002. **Note:** byte values assume decimal MB -- see Guidance CT-001. |
| 2.2 | Implement session lifecycle tests: session boot with valid opts, `projectRoot` binding, bootstrap policy enforcement | Tests pass against running harness | Source: Specification REQ-04 |
| 2.3 | Implement turn execution tests: message processing with observable completion signal, empty-message-with-attachments acceptance, empty-message-without-attachments rejection (HTTP 400) | Tests pass against running harness | Source: Specification REQ-05 |
| 2.4 | Implement SSE streaming tests: event delivery verification using event-driven assertions; verify at least one parseable SSE event per turn | Tests pass against running harness | Source: Specification REQ-06; Guidance C5 |
| 2.5 | Implement opts mapping and fallback chain tests: model/tools/maxTurns fallback resolution at each level | Tests pass against running harness | Source: Specification REQ-07 |
| 2.6 | Implement subagent governance fail-closed tests: blocked injection with each invalid governance condition individually, parent turn continuation, successful injection only when all four conditions (a-d per REQ-08) are met | Tests pass against running harness | Source: Specification REQ-08; Guidance C3 |
| 2.7 | Implement attachment resolver tests: extension validation, isFile check, boundary-value size limits (10,000,000 / 10,000,001 bytes), budget enforcement (18,000,000 / 18,000,001 bytes), partial failure, prompt mode selection | Tests pass against running harness | Source: Specification REQ-09, REQ-10 |
| 2.8 | Implement error-path tests: verify invalid inputs produce correct HTTP error codes (400, 403) per REQ-15 | Tests return expected error responses | Source: Specification REQ-15 |
| 2.9 | Implement test isolation: ensure each test/test group can run independently without depending on other tests' execution or side effects | Individual test execution produces same results as full suite | Source: Specification REQ-14 |
| 2.10 | Ensure all scripts exit with code 0 on success and non-zero on failure | CI-compatible exit codes verified | Source: Specification REQ-03 |
| 2.11 | Verify scripts run without interactive prompts | Headless execution confirmed | Source: Specification REQ-03 |

**Error handling:** If test fixtures fail to generate (e.g., filesystem permission errors, disk space), halt Phase 2 and resolve the fixture generation issue before continuing. If the harness fails to start for testing, verify PR-04 (harness runtime available) and report the failure. If individual tests fail unexpectedly, isolate the failure to determine whether it is a test defect or a harness defect before proceeding.

### Phase 3: Repeatability Verification

**Objective:** Confirm the suite produces consistent results.

**Entry gate:** Phase 2 complete -- all validation scripts implemented and passing.

| Step | Action | Verification | Notes |
|------|--------|-------------|-------|
| 3.1 | Run the full validation suite twice consecutively against the same harness state | Identical pass/fail results on both runs | Source: Specification REQ-12 |
| 3.2 | Verify tests do not leave side effects (modified files, leaked sessions, orphaned processes) | Clean state after each run | Source: Specification REQ-12 |
| 3.3 | Run the "contract tests" subset without an API key to verify offline capability | Contract tests pass without network access | Source: Guidance T1 |
| 3.4 | Execute cleanup/teardown: remove generated test fixtures, terminate any harness sessions started by the suite, and reset environment variables (`CHIRALITY_ENABLE_SUBAGENTS`) to their pre-test values | No test artifacts remain in the working directory after cleanup | Source: Lensing E-002; **ASSUMPTION** -- standard practice to prevent state leakage |

**Error handling:** If repeatability verification fails (different results on second run), identify the non-deterministic test(s), isolate the cause (timing, shared state, external dependency), and fix before proceeding. Do not proceed to Phase 4 with known repeatability failures.

### Phase 4: Documentation

**Objective:** Produce validation documentation.

**Entry gate:** Phase 3 complete -- repeatability verified.

| Step | Action | Verification | Notes |
|------|--------|-------------|-------|
| 4.1 | Write local execution instructions (how to run the suite on a developer machine) | Instructions followed successfully by a fresh setup | Source: Specification REQ-11 |
| 4.2 | Write CI integration guide (pipeline configuration, environment variables, exit code handling) | Guide covers CI pipeline setup | Source: Specification REQ-11 |
| 4.3 | Write test descriptions for each test group (what is tested, expected outcomes, pass/fail criteria) | All six behavioral areas documented | Source: Specification REQ-11 |
| 4.4 | Document prerequisites (Node.js version TBD, API key, working root setup) | Prerequisites are actionable and complete | Source: Specification REQ-11 |
| 4.5 | Place documentation in expected location (`frontend/docs/harness/` per PLAN Section 2) | Documentation accessible at expected path | Source: PLAN Section 2; **ASSUMPTION** -- location based on PLAN reference; see Guidance CT-002 |

**Error handling:** If the expected documentation path does not exist in the repository, create it or report to the human for path confirmation before placing files.

### Phase 5: Review and Handoff

**Objective:** Confirm completeness and readiness per Specification REQ-16 (deliverable acceptance criteria).

**Entry gate:** Phase 4 complete -- documentation written and placed.

| Step | Action | Verification | Notes |
|------|--------|-------------|-------|
| 5.1 | Run final full suite execution (local) | All tests pass | -- |
| 5.2 | Verify test inventory covers all six behavioral areas per Specification REQ-01 | Coverage confirmed: 6/6 areas | Source: Specification REQ-01 |
| 5.3 | Review documentation for completeness per Specification REQ-11 | All four documentation items present | Source: Specification REQ-11 |
| 5.4 | Confirm script and documentation locations match expected paths | Files at expected paths (see Guidance CT-002 for path confirmation status) | Source: PLAN Section 2; **ASSUMPTION** |
| 5.5 | Produce test-to-requirement traceability record: a mapping from each test to the REQ(s) and K-invariant(s) it validates | Traceability record complete; every REQ-01 through REQ-16 has at least one test mapped | Source: Specification REQ-13, REQ-16; Lensing X-005 |
| 5.6 | Verify deliverable acceptance criteria per REQ-16 are met | All four acceptance conditions confirmed | Source: Specification REQ-16 |

**Error handling:** If acceptance criteria are not met, identify the gap and return to the relevant phase to address it. Document any exceptions or deferred items with rationale.

## Verification

| Check | What to Verify | Method |
|-------|----------------|--------|
| V-01 | All six behavioral areas have tests | Inspect test inventory against Specification REQ-01 |
| V-02 | Local execution works on macOS 15+ Apple Silicon | Execute suite on target platform |
| V-03 | CI-ready (no interactive prompts, clean exit codes) | Execute in headless mode |
| V-04 | Repeatability (consistent results on rerun) | Run suite twice; compare results |
| V-05 | Documentation complete | Review against Specification REQ-11 criteria |
| V-06 | Contract tests runnable without API key | Execute contract test subset without key |
| V-07 | Test isolation verified | Execute individual tests in isolation; confirm same results as full suite |
| V-08 | Cleanup leaves no artifacts | Verify working directory is clean after Phase 3 Step 3.4 |
| V-09 | Traceability record complete | Review traceability mapping against all REQs |

## Records

| Record | Description | Location |
|--------|-------------|----------|
| Test inventory | Documented list of all tests by behavioral area | TBD -- within `frontend/docs/harness/` (**ASSUMPTION**) |
| Validation run results | Pass/fail output from suite execution | Console output / CI artifact |
| CI integration configuration | Pipeline configuration for automated validation | TBD -- depends on CI platform choice |
| Documentation deliverable | Run instructions, CI guide, test descriptions, prerequisites | `frontend/docs/harness/` (**ASSUMPTION** -- per PLAN Section 2; see Guidance CT-002) |
| Test-to-requirement traceability | Mapping from each test to REQ(s) and K-invariant(s) it validates, supporting review and audit of coverage claims | TBD -- within `frontend/docs/harness/` or alongside test scripts (**ASSUMPTION**); produced in Phase 5 Step 5.5 |
