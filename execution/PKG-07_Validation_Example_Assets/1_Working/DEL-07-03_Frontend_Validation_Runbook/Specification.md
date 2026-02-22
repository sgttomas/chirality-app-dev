# Specification -- DEL-07-03 Frontend Validation & Runbook Baseline

## Scope

### Included

This deliverable covers two complementary areas introduced by Scope Amendment A1 (SCA-001):

1. **SOW-048 -- Automated frontend validation baseline:** Implement automated harness validation scripts (`frontend/scripts/validate-harness-*.mjs`) that exercise the Section 8 SDK-native test matrix and produce a deterministic summary artifact at a known, stable path (`frontend/artifacts/harness/section8/latest/summary.json`).

2. **SOW-049 -- Frontend validation runbooks and architecture documentation:** Document frontend architecture and local validation runbooks in repository docs (`docs/` and deliverable-local artifacts) so that any developer can reproduce validation locally without external guidance.

**Harness validation behavioral areas in scope** (Source: `docs/harness/harness_manual_validation.md` Section 8 Matrix):

1. **Smoke stream ordering** -- SSE event sequence: `session:init`, `chat:delta`, `chat:complete`, `session:complete`, `process:exit`
2. **Session persistence + resume continuity** -- session file/API persist `claudeSessionId`; resumed turn emits `session:init`; persisted value matches latest init
3. **Permissions under `dontAsk`** -- deny case does not execute unapproved Bash; allow case emits `tool:result` containing `UNAPPROVED_ALLOW_TEST`
4. **Interrupt behavior** -- `/api/harness/interrupt` returns `200 {"ok":true}`; stream emits terminal `process:exit` with interruption marker
5. **SDK-native stream handling** -- successful turn emits `chat:complete` + `process:exit`; no `parse:error` logs for the session

**Additional regression checks in scope** (Source: `docs/harness/harness_manual_validation.md`):

- `setup.server_reachable`
- `regression.session_crud`

### Excluded

- Harness runtime behavioral coverage beyond Section 8 matrix and session CRUD (covered by DEL-07-01 which addresses the broader harness contract: opts fallback chains, subagent governance, attachment resolver)
- Example execution root maintenance (covered by DEL-07-02)
- Frontend workspace bootstrapping (covered by DEL-01-03)
- Harness API route implementation (covered by DEL-03-07)
- Frontend workflow shell implementation (covered by DEL-02-05)
- Performance benchmarking or load testing
- Signing, notarization, or distribution packaging (covered by DEL-01-02)
- Full artifact mirroring implementation (mirroring guidance is documented but implementation is opt-in diagnostic; see `docs/harness/harness_artifact_mirroring_guidance.md`)

## Requirements

### REQ-01: Section 8 Validation Script Exists

A validation script MUST exist at `frontend/scripts/validate-harness-section8.mjs` that exercises all five Section 8 behavioral checks defined in the Section 8 Matrix.

**Source:** `docs/harness/harness_manual_validation.md` Section 8 Matrix; SOW-048

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

**Source:** `docs/harness/harness_manual_validation.md` Local-Only Boundary; `_CONTEXT.md` description; Decomposition OBJ-008 acceptance criteria

### REQ-06: Section 8 Test Coverage

The Section 8 validation script MUST include tests for all five behavioral checks:

| Test ID | Behavioral Check | Pass Criterion | Source |
|---------|-----------------|----------------|--------|
| `section8.smoke_stream` | Smoke stream ordering | SSE events arrive in sequence: `session:init`, `chat:delta`, `chat:complete`, `session:complete`, `process:exit` | `docs/harness/harness_manual_validation.md` Section 8 Matrix row 1 |
| `section8.session_persistence_resume` | Session persistence + resume | `claudeSessionId` persists across turns; resumed turn emits `session:init` with matching value | `docs/harness/harness_manual_validation.md` Section 8 Matrix row 2 |
| `section8.permissions_dontask` | Permissions under `dontAsk` | Deny case blocks unapproved Bash; allow case emits `tool:result` with `UNAPPROVED_ALLOW_TEST` | `docs/harness/harness_manual_validation.md` Section 8 Matrix row 3 |
| `section8.interrupt_sigint` | Interrupt behavior | `/api/harness/interrupt` returns `200 {"ok":true}`; stream emits terminal `process:exit` with interruption marker | `docs/harness/harness_manual_validation.md` Section 8 Matrix row 4 |
| `section8.sdk_native_stream` | SDK-native stream handling | Turn emits `chat:complete` + `process:exit`; no `parse:error` logs | `docs/harness/harness_manual_validation.md` Section 8 Matrix row 5 |

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

**Source:** `docs/harness/harness_manual_validation.md` Machine-Readable Outputs

### REQ-09: CI-Ready Posture

Validation scripts MUST:
- Exit with code 0 on pass and non-zero on fail
- Run without interactive prompts or GUI dependencies
- Be compatible with the CI job flow defined in `docs/harness/harness_ci_integration.md`

**Source:** `docs/harness/harness_ci_integration.md` Failure Expectations; SOW-048

### REQ-10: CI Workflow Definition

A GitHub Actions workflow file MUST exist at `.github/workflows/harness-premerge.yml` that implements the CI job flow:
1. Checkout repository
2. Setup Node.js
3. Install dependencies (`npm ci`)
4. Start frontend server
5. Poll readiness
6. Run `npm run harness:validate:premerge`
7. Validate summary schema
8. Verify summary exists at stable path
9. Upload summary artifact

**Source:** `docs/harness/harness_ci_integration.md` Job Flow

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

**Source:** SOW-049; `_CONTEXT.md`

### REQ-13: Frontend Architecture Documentation

Documentation MUST be produced that describes:
- The frontend validation architecture (scripts, wrapper, artifact paths, CI workflow)
- The relationship between `validate-harness-section8.mjs` (core) and `validate-harness-premerge.mjs` (wrapper)
- The artifact layout and mirroring posture
- Summary schema validation expectations (required SDK test IDs, legacy exclusions)

**Source:** SOW-049; `docs/harness/harness_manual_validation.md` Artifact Layout; `docs/harness/harness_artifact_mirroring_guidance.md`

### REQ-14: Runtime Surface Missing Detection

If `frontend/` or the validation scripts are missing in the workspace, validation scripts MUST detect this condition and record `RUNTIME_SURFACE_MISSING` in coordination artifacts before continuing with any harness task.

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
| REQ-01 | Verify `frontend/scripts/validate-harness-section8.mjs` exists and is executable; run it against a live harness and confirm all five Section 8 checks execute |
| REQ-02 | Verify `frontend/scripts/validate-harness-premerge.mjs` exists; run it and confirm: stable summary created, schema validated, machine-readable output variables emitted |
| REQ-03 | After `npm run harness:validate:premerge`, verify `frontend/artifacts/harness/section8/latest/summary.json` exists, is valid JSON, and contains per-test results |
| REQ-04 | Inspect `frontend/package.json`; confirm `scripts.harness:validate:premerge` entry exists and points to the wrapper |
| REQ-05 | Execute validation in a clean clone of this repository with no external repos available; confirm all scripts run successfully |
| REQ-06 | Inspect Section 8 script source or test output; confirm all five test IDs (`section8.smoke_stream`, `section8.session_persistence_resume`, `section8.permissions_dontask`, `section8.interrupt_sigint`, `section8.sdk_native_stream`) are present |
| REQ-07 | Inspect script source or test output; confirm `setup.server_reachable` and `regression.session_crud` are present |
| REQ-08 | Run each script; parse stdout for required output variables; confirm format matches specification |
| REQ-09 | Run scripts in headless mode; confirm exit code 0 on pass, non-zero on fail; confirm no interactive prompts |
| REQ-10 | Verify `.github/workflows/harness-premerge.yml` exists; inspect against Job Flow steps 1-9 |
| REQ-11 | Inspect CI workflow for preflight step checking script existence |
| REQ-12 | Review runbook documentation for completeness against all six items listed in REQ-12 |
| REQ-13 | Review architecture documentation for completeness against all four items listed in REQ-13 |
| REQ-14 | Remove `frontend/` directory; run scripts; confirm `RUNTIME_SURFACE_MISSING` is recorded |
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
