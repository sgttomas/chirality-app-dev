# Specification -- DEL-07-03 Frontend Validation & Runbook Baseline

## Scope

### Included

This deliverable covers two complementary areas introduced by Scope Amendment A1 (SCA-001):

1. **SOW-048 -- Automated frontend validation baseline:** Implement automated harness validation scripts (`frontend/scripts/validate-harness-*.mjs`) that exercise the Section 8 SDK-native test matrix and produce a deterministic summary artifact at a known, stable path (`frontend/artifacts/harness/section8/latest/summary.json`).

2. **SOW-049 -- Frontend validation runbooks and architecture documentation:** Document frontend architecture and local validation runbooks in repository docs (`docs/` and deliverable-local artifacts) so that any developer can reproduce validation locally without external guidance.

**Harness validation behavioral areas in scope** (Source: `docs/harness/harness_manual_validation.md` Section 8 Matrix + active script baseline in `frontend/scripts/validate-harness-section8.mjs`):

1. **Smoke stream ordering** -- SSE event sequence: `session:init`, `chat:delta`, `chat:complete`, `session:complete`, `process:exit`
2. **Session persistence + resume continuity** -- session file/API persist `claudeSessionId`; resumed turn emits `session:init`; persisted value matches latest init
3. **Permissions under `dontAsk`** -- deny case does not execute unapproved Bash; allow case emits `tool:result` containing `UNAPPROVED_ALLOW_TEST`
4. **Interrupt behavior** -- `/api/harness/interrupt` returns `200 {"ok":true}`; stream emits terminal `process:exit` with interruption marker
5. **SDK-native stream handling** -- successful turn emits `chat:complete` + `process:exit`; no `parse:error` logs for the session
6. **Boot error taxonomy coverage** -- typed boot failures are asserted for missing session, missing persona, SDK boot failure, and inaccessible working root (`SESSION_NOT_FOUND`, `PERSONA_NOT_FOUND`, `SDK_FAILURE`, `WORKING_ROOT_INACCESSIBLE`)

**Additional regression checks in scope** (Source: `docs/harness/harness_manual_validation.md`):

- `setup.server_reachable`
- `regression.session_crud`

### Excluded

- Harness runtime behavioral coverage beyond Section 8 matrix and session CRUD (covered by DEL-07-01 (Harness Validation Suite) which addresses the broader harness contract: opts fallback chains, subagent governance, attachment resolver)
- Example execution root maintenance (covered by DEL-07-02 (Example Execution Roots))
- Frontend workspace bootstrapping (covered by DEL-01-03)
- Harness API route implementation (covered by DEL-03-07)
- Frontend workflow shell implementation (covered by DEL-02-05)
- Performance benchmarking or load testing
- Signing, notarization, or distribution packaging (covered by DEL-01-02)
- Full artifact mirroring implementation (mirroring guidance is documented but implementation is opt-in diagnostic; see `docs/harness/harness_artifact_mirroring_guidance.md`)

### Pre-Tier Gate Acceptance Criteria

This deliverable occupies a pre-tier gate position per SCA-001. The minimum acceptance threshold for unblocking Tier 2 work is TBD -- it is not yet defined which subset of REQ-01 through REQ-16 must pass to satisfy the gate, nor whether structural validation alone suffices or live validation is required. See Guidance C2 for scope implications and Lensing Item F-001.

**ASSUMPTION:** The gate is satisfied when the deliverable reaches `IN_PROGRESS` status per the SCA-001 blocker maturity policy, but the specific requirement-level acceptance bar for gate passage requires human ruling.

**Source:** Decomposition SCA-001 Execution Gating Rule; Guidance C2

## Requirements

### REQ-01: Section 8 Validation Script Exists

A validation script MUST exist at `frontend/scripts/validate-harness-section8.mjs` that exercises all five Section 8 behavioral checks defined in the Section 8 Matrix. The active implementation baseline also enforces `section8.boot_error_taxonomy` as an additional section8-scoped check in the required-check order.

**Source:** `docs/harness/harness_manual_validation.md` Section 8 Matrix; `frontend/scripts/validate-harness-section8.mjs`; SOW-048

### REQ-02: Pre-Merge Wrapper Script Exists

A pre-merge wrapper script MUST exist at `frontend/scripts/validate-harness-premerge.mjs` that:
- Executes the Section 8 validation
- Copies the summary artifact to the stable path `frontend/artifacts/harness/section8/latest/summary.json`
- Validates the summary schema: required SDK test IDs are present and legacy `regression.api_chat_reachability` is absent
- Emits machine-readable output variables: `HARNESS_PREMERGE_ARTIFACT_PATH`, `HARNESS_PREMERGE_SOURCE_SUMMARY_PATH`, `HARNESS_PREMERGE_STATUS`, `HARNESS_PREMERGE_TEST_COUNT`

**Source:** `docs/harness/harness_manual_validation.md` Machine-Readable Outputs; `docs/harness/harness_ci_integration.md` Job Flow step 7

### REQ-03: Deterministic Summary Artifact

The validation scripts MUST produce a deterministic summary artifact at `frontend/artifacts/harness/section8/latest/summary.json` after a successful pre-merge run. The artifact MUST:
- Exist at the stable path after `npm run harness:validate:premerge` completes
- Contain structured pass/fail results for each test in the Section 8 matrix
- Be parseable as valid JSON

**Source:** SOW-048 ("deterministic summary artifact path"); `docs/harness/harness_ci_integration.md` Job Flow step 8

### REQ-04: npm Run Target

The `frontend/package.json` MUST define a script target `harness:validate:premerge` that executes the pre-merge wrapper.

**Source:** `docs/harness/harness_manual_validation.md` Usage; `docs/harness/harness_ci_integration.md` CI command

### REQ-05: Local Execution Without Non-Local Dependencies

Validation scripts MUST be executable entirely from this repository's local filesystem. No non-local repository, external clone, or remote artifact store is required for execution.

**Verification note:** This requirement can be verified through two distinct modes:
- **Structural validation** (no API key needed): scripts exist, npm targets resolve, artifact paths are correct, no external repository references in script source.
- **Live validation** (API key required): scripts execute against a running harness and produce `pass`/`fail` results in a clean clone with no external repos available.

The verification approach in the table below specifies live validation ("Execute validation in a clean clone"). Structural validation is a necessary-but-not-sufficient subset. See Guidance C3 for the distinction between these modes.

**Source:** `docs/harness/harness_manual_validation.md` Local-Only Boundary; `_CONTEXT.md` description; Decomposition OBJ-008 acceptance criteria

### REQ-06: Section 8 Test Coverage

The Section 8 validation script MUST include tests for all five Section 8 matrix behavioral checks. The active implementation baseline additionally requires `section8.boot_error_taxonomy` as a typed-boot-failure guard.

| Test ID | Behavioral Check | Pass Criterion | Source |
|---------|-----------------|----------------|--------|
| `section8.smoke_stream` | Smoke stream ordering | SSE events arrive in sequence: `session:init`, `chat:delta`, `chat:complete`, `session:complete`, `process:exit` | `docs/harness/harness_manual_validation.md` Section 8 Matrix row 1 |
| `section8.session_persistence_resume` | Session persistence + resume | `claudeSessionId` persists across turns; resumed turn emits `session:init` with matching value | `docs/harness/harness_manual_validation.md` Section 8 Matrix row 2 |
| `section8.permissions_dontask` | Permissions under `dontAsk` | Deny case blocks unapproved Bash; allow case emits `tool:result` with `UNAPPROVED_ALLOW_TEST` | `docs/harness/harness_manual_validation.md` Section 8 Matrix row 3 |
| `section8.interrupt_sigint` | Interrupt behavior | `/api/harness/interrupt` returns `200 {"ok":true}`; stream emits terminal `process:exit` with interruption marker | `docs/harness/harness_manual_validation.md` Section 8 Matrix row 4 |
| `section8.sdk_native_stream` | SDK-native stream handling | Turn emits `chat:complete` + `process:exit`; no `parse:error` logs | `docs/harness/harness_manual_validation.md` Section 8 Matrix row 5 |
| `section8.boot_error_taxonomy` | Boot error taxonomy | Boot path reports typed errors for missing session, missing persona, SDK boot failure, and inaccessible working root | `frontend/scripts/validate-harness-section8.mjs`; `execution/_Reconciliation/TIER2_INTERFACE_RECON_2026-02-23_PASS10.md` |

### REQ-07: Regression Check Coverage

The validation script MUST include the following regression checks:

| Test ID | Check | Source |
|---------|-------|--------|
| `setup.server_reachable` | Verify harness server is reachable at `HARNESS_BASE_URL` | `docs/harness/harness_manual_validation.md` Additional Regression Checks |
| `regression.session_crud` | Verify session create/read/update/delete operations | `docs/harness/harness_manual_validation.md` Additional Regression Checks |

### REQ-08: Machine-Readable Output

The Section 8 script MUST emit the following machine-readable output on stdout:
- `HARNESS_VALIDATION_SUMMARY_PATH=<path>`
- `HARNESS_VALIDATION_STATUS=pass|fail`

The pre-merge wrapper MUST emit:
- `HARNESS_PREMERGE_ARTIFACT_PATH=<stable-path>`
- `HARNESS_PREMERGE_SOURCE_SUMMARY_PATH=<tmp-path>`
- `HARNESS_PREMERGE_STATUS=pass|fail`
- `HARNESS_PREMERGE_TEST_COUNT=<n>`

**Canonical pass/fail vocabulary:** The values `pass` and `fail` are lowercase strings. `pass` indicates all checks in the script's scope succeeded; `fail` indicates one or more checks did not succeed. Exit code 0 corresponds to `pass`; non-zero exit code corresponds to `fail`. This vocabulary is the normative definition used across all four production documents.

**`HARNESS_PREMERGE_TEST_COUNT` semantics:** The value `<n>` is the total number of tests executed by the pre-merge wrapper (Section 8 checks + regression checks). The current Guidance example shows `8` (6 `section8.*` checks + 2 regression checks); however, this count is **informational** and reflects the current test matrix composition. The normative requirement is that the emitted count accurately reflects the number of tests actually executed, not a fixed value. If the Section 8 matrix or regression check set evolves, this count changes accordingly.

**Source:** `docs/harness/harness_manual_validation.md` Machine-Readable Outputs; Lensing Items D-001, X-003

### REQ-09: CI-Ready Posture

Validation scripts MUST:
- Exit with code 0 on `pass` and non-zero on `fail` (see REQ-08 for canonical vocabulary)
- Run without interactive prompts or GUI dependencies (headless-compatible)
- Be compatible with the CI job flow defined in `docs/harness/harness_ci_integration.md`

**Headless compatibility criterion:** Scripts MUST NOT depend on any graphical display, browser window, or interactive terminal input. Verification of headless compatibility MUST confirm that scripts execute successfully in an environment without a display server (e.g., `DISPLAY` unset) and without any TTY attached to stdin. See Procedure Phase 6 for the concrete verification step.

**Source:** `docs/harness/harness_ci_integration.md` Failure Expectations; SOW-048; Lensing Item X-002

### REQ-10: CI Workflow Definition

A GitHub Actions workflow file MUST exist at `.github/workflows/harness-premerge.yml` that implements the CI job flow:
1. Checkout repository
2. Setup Node.js
3. Install dependencies (`npm ci`)
4. Start frontend server
5. Poll readiness (timeout behavior TBD -- see Lensing Item X-001)
6. Run `npm run harness:validate:premerge`
7. Validate summary schema
8. Verify summary exists at stable path
9. Upload summary artifact

**Timeout/retry behavior:** The CI workflow SHOULD specify timeout thresholds for server readiness polling (step 5) and for script execution (step 6). The specific timeout values are TBD. Scripts SHOULD handle transient failures during harness server startup gracefully (e.g., retry with backoff during readiness polling). See Lensing Item X-001.

**Source:** `docs/harness/harness_ci_integration.md` Job Flow; Lensing Item X-001

### REQ-11: Fail-Fast Preflight in CI

The CI workflow MUST include a fail-fast preflight that verifies `frontend/scripts/validate-harness-premerge.mjs` exists before running validation.

**Source:** `docs/harness/harness_ci_integration.md` Local-Only Boundary

### REQ-12: Local Validation Runbook Documentation

Documentation MUST be produced that describes:
- How to run frontend validation locally (prerequisites, server startup, script execution, reading results)
- The Section 8 test matrix and what each check validates
- How to interpret machine-readable output variables
- How to interpret summary artifacts
- Prerequisites for running (Node.js, API key, running harness server)
- The local-only boundary constraint

**Documentation placement:** SOW-049 directs documentation to "repository docs (`docs/` and deliverable-local artifacts)" but does not specify exact file paths. This is tracked as CT-002 in Guidance. See Guidance T1 for the proposed approach (update existing `docs/harness/` files in-place + lightweight index).

**Source:** SOW-049; `_CONTEXT.md`; Lensing Item A-001

### REQ-13: Frontend Architecture Documentation

Documentation MUST be produced that describes:
- The frontend validation architecture (scripts, wrapper, artifact paths, CI workflow)
- The relationship between `validate-harness-section8.mjs` (core) and `validate-harness-premerge.mjs` (wrapper)
- The artifact layout and mirroring posture
- Summary schema validation expectations (required SDK test IDs, legacy exclusions)

**Documentation placement:** Same as REQ-12 -- governed by CT-002. See Guidance T1.

**Source:** SOW-049; `docs/harness/harness_manual_validation.md` Artifact Layout; `docs/harness/harness_artifact_mirroring_guidance.md`; Lensing Item A-001

### REQ-14: Runtime Surface Missing Detection

If `frontend/` or the validation scripts are missing in the workspace, validation scripts MUST detect this condition and record `RUNTIME_SURFACE_MISSING` in coordination artifacts before continuing with any harness task.

**Open question:** The term "coordination artifacts" is not defined in any source document. It is unclear where `RUNTIME_SURFACE_MISSING` should be recorded -- options include stdout, a status file, a log file, or an environment variable. The recording location and format require clarification. See Lensing Item C-001.

**Source:** `docs/harness/harness_manual_validation.md` Local-Only Boundary

### REQ-15: Summary Schema Validation

The pre-merge wrapper MUST validate the summary artifact schema to ensure:
- Required SDK test IDs are present (as enumerated in the Section 8 matrix and regression checks)
- Legacy `regression.api_chat_reachability` test ID is absent (removed from schema)
- Summary is valid JSON

**Source:** `docs/harness/harness_ci_integration.md` Job Flow step 7

### REQ-16: Artifact Mirroring Guidance Documentation

Documentation SHOULD describe the artifact mirroring posture:
- Default: summary-only (`summary.json`)
- On-demand: full mirroring for diagnostics
- When to enable full mirroring (failure investigation, flaky tests, audit, forensics)
- What full mirroring includes (sse, api, logs, mock, cleanup)
- Guardrails (secrets redaction, retention limits, sensitivity treatment)

**Source:** `docs/harness/harness_artifact_mirroring_guidance.md`; SOW-049

## Objective Traceability

### OBJ-008 Acceptance Evidence

OBJ-008 states: "Local frontend runtime baseline exists and is executable from this repository only." At the deliverable level, REQ-05 (Local Execution Without Non-Local Dependencies) is the primary requirement supporting this objective. However, whether REQ-05 verification alone constitutes formal acceptance of OBJ-008, or whether a separate acceptance artifact or sign-off is required, is TBD. See Lensing Item E-001.

**ASSUMPTION:** REQ-05 live verification (execute in a clean clone with no external repos) is sufficient to evidence OBJ-008 at the deliverable level, pending confirmation from the decomposition's acceptance criteria framework.

**Source:** `_CONTEXT.md` Objectives; Specification REQ-05; Decomposition OBJ-008

## Standards

| Standard / Reference | Applicability | Accessible |
|---------------------|---------------|------------|
| `docs/harness/harness_manual_validation.md` | Defines script locations, Section 8 matrix, machine-readable outputs, artifact layout, local-only boundary | Yes |
| `docs/harness/harness_ci_integration.md` | Defines CI workflow, job flow, failure expectations, summary schema validation | Yes |
| `docs/harness/harness_artifact_mirroring_guidance.md` | Defines artifact mirroring posture and guardrails | Yes |
| DEC-PLAT-001 | Target platform (macOS 15+, Apple Silicon) | Yes (Decomposition Decision Log) |
| DEC-NET-001 | Anthropic-only outbound network policy | Yes (Decomposition Decision Log) |
| `docs/PLAN.md` Section 2 FE-4 | Frontend validation + packaging baseline acceptance criteria | Yes |

## Verification

| Requirement | Verification Approach |
|-------------|----------------------|
| REQ-01 | Verify `frontend/scripts/validate-harness-section8.mjs` exists and is executable; run it against a live harness and confirm all five Section 8 matrix checks execute plus the active `section8.boot_error_taxonomy` guard |
| REQ-02 | Verify `frontend/scripts/validate-harness-premerge.mjs` exists; run it and confirm: stable summary created, schema validated, machine-readable output variables emitted |
| REQ-03 | After `npm run harness:validate:premerge`, verify `frontend/artifacts/harness/section8/latest/summary.json` exists, is valid JSON, and contains per-test results |
| REQ-04 | Inspect `frontend/package.json`; confirm `scripts.harness:validate:premerge` entry exists and points to the wrapper |
| REQ-05 | Execute validation in a clean clone of this repository with no external repos available; confirm all scripts run successfully. **Note:** This constitutes live validation; structural validation (scripts exist, npm targets resolve, no external references in source) is a necessary-but-not-sufficient subset. See REQ-05 body for mode definitions. |
| REQ-06 | Inspect Section 8 script source or test output; confirm baseline IDs are present (`section8.smoke_stream`, `section8.session_persistence_resume`, `section8.permissions_dontask`, `section8.interrupt_sigint`, `section8.sdk_native_stream`) plus active implementation ID `section8.boot_error_taxonomy` |
| REQ-07 | Inspect script source or test output; confirm `setup.server_reachable` and `regression.session_crud` are present |
| REQ-08 | Run each script; parse stdout for required output variables; confirm format matches specification. Verify `pass`/`fail` values are lowercase strings. Verify `HARNESS_PREMERGE_TEST_COUNT` accurately reflects the number of tests executed. |
| REQ-09 | Run scripts in a headless environment (no display server, no TTY on stdin); confirm exit code 0 on `pass`, non-zero on `fail`; confirm no interactive prompts or GUI dependencies. See Procedure Step 6.10 for concrete verification. |
| REQ-10 | Verify `.github/workflows/harness-premerge.yml` exists; inspect against Job Flow steps 1-9. Verify timeout configuration is present for readiness polling (or document as TBD if absent). |
| REQ-11 | Inspect CI workflow for preflight step checking script existence |
| REQ-12 | Review runbook documentation for completeness against all six items listed in REQ-12 |
| REQ-13 | Review architecture documentation for completeness against all four items listed in REQ-13 |
| REQ-14 | Remove `frontend/` directory; run scripts; confirm `RUNTIME_SURFACE_MISSING` is recorded. **Note:** Verify the recording location and format are defined (currently TBD; see REQ-14 open question). |
| REQ-15 | Provide a summary missing a required test ID; run pre-merge wrapper; confirm failure. Provide a summary with legacy ID; confirm failure |
| REQ-16 | Review mirroring guidance documentation for completeness against the five items listed in REQ-16 |

## Documentation

### Required Artifacts

| Artifact | Type | Description |
|----------|------|-------------|
| `frontend/scripts/validate-harness-section8.mjs` | SCRIPT | Core Section 8 SDK-native validation script |
| `frontend/scripts/validate-harness-premerge.mjs` | SCRIPT | Pre-merge wrapper with stable artifact copy and schema validation |
| `.github/workflows/harness-premerge.yml` | SCRIPT | CI workflow for automated pre-merge validation |
| `frontend/artifacts/harness/section8/latest/summary.json` | TEST | Deterministic summary artifact (produced by script execution, not committed) |
| Local validation runbook | DOC | How to run validation locally, interpret results, prerequisites |
| Frontend validation architecture document | DOC | Script relationships, artifact layout, mirroring posture, schema expectations |
| Artifact mirroring guidance | DOC | When and how to enable full artifact mirroring (may reference existing `docs/harness/harness_artifact_mirroring_guidance.md`) |
