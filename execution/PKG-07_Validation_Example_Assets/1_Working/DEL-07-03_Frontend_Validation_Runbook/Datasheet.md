# Datasheet -- DEL-07-03 Frontend Validation & Runbook Baseline

## Identification

| Field | Value |
|-------|-------|
| **DeliverableID** | DEL-07-03 |
| **Name** | Frontend Validation & Runbook Baseline |
| **PackageID** | PKG-07 |
| **Package** | Validation & Example Assets |
| **Type** | TEST_SUITE |
| **ContextEnvelope** | M |
| **ResponsibleParty** | TBD -- requires human assignment (see Lensing Item B-001) |
| **Scope Coverage** | SOW-048, SOW-049 |
| **Objectives** | OBJ-006, OBJ-008 |
| **Decomposition** | `execution/_Decomposition/ChiralityApp_SoftwareDecomposition_2026-02-21_G7-APPROVED.md` (Scope Amendment A1, SCA-001) |
| **Amendment** | SCA-001 (2026-02-22) |

## Attributes

| Attribute | Value | Source |
|-----------|-------|--------|
| Validation target | Frontend harness runtime (session lifecycle, turn execution, SSE streaming, permissions, interrupt behavior, SDK-native stream handling) | `docs/harness/harness_manual_validation.md` Section 8 Matrix |
| Execution modes | Local (developer workstation) only; CI-ready posture (scripts must be headless-compatible) | Decomposition DEL-07-03 description; `docs/harness/harness_ci_integration.md` |
| Script runtime | Node.js (`.mjs` modules) | `docs/harness/harness_manual_validation.md` -- references `frontend/scripts/validate-harness-section8.mjs` and `frontend/scripts/validate-harness-premerge.mjs` |
| Script locations | `frontend/scripts/validate-harness-section8.mjs` (core validation), `frontend/scripts/validate-harness-premerge.mjs` (pre-merge wrapper) | `docs/harness/harness_manual_validation.md` |
| Target platform | macOS 15+, Apple Silicon | DEC-PLAT-001 (Decomposition Decision Log) |
| Application stack | Electron + Next.js desktop app | `docs/PLAN.md` Section 2 |
| Anticipated artifact types | TEST, SCRIPT, DOC | `_CONTEXT.md` |
| Deterministic summary artifact path | `frontend/artifacts/harness/section8/latest/summary.json` (stable path); also `${TMPDIR:-/tmp}/chirality-harness-validation/latest/summary.json` (ephemeral) | `docs/harness/harness_manual_validation.md` Summary locations |
| Pre-merge wrapper output variables | `HARNESS_PREMERGE_ARTIFACT_PATH`, `HARNESS_PREMERGE_SOURCE_SUMMARY_PATH`, `HARNESS_PREMERGE_STATUS`, `HARNESS_PREMERGE_TEST_COUNT` | `docs/harness/harness_manual_validation.md` Machine-Readable Outputs |
| Section 8 validation output variables | `HARNESS_VALIDATION_SUMMARY_PATH`, `HARNESS_VALIDATION_STATUS` | `docs/harness/harness_manual_validation.md` Machine-Readable Outputs |
| Harness API base URL | `http://127.0.0.1:3000` (default) | `docs/harness/harness_manual_validation.md` Prerequisites |
| CI workflow file | `.github/workflows/harness-premerge.yml` | `docs/harness/harness_ci_integration.md` |
| Artifact mirroring posture | Summary-only by default; full mirroring opt-in for diagnostics | `docs/harness/harness_artifact_mirroring_guidance.md` Recommended Operating Model |
| Network policy | Anthropic-only outbound (DEC-NET-001) | Decomposition Decision Log |
| Local-only boundary | All validation runs must execute from this repository's local filesystem; no non-local repositories permitted | `docs/harness/harness_manual_validation.md` Local-Only Boundary; `_CONTEXT.md` |
| Runbook documentation scope | Frontend architecture documentation + local validation runbooks in `docs/` and deliverable-local artifacts | SOW-049; `_CONTEXT.md` |
| Pass/fail vocabulary | Canonical form: lowercase `pass` / `fail` as emitted by machine-readable output variables (`HARNESS_PREMERGE_STATUS=pass\|fail`, `HARNESS_VALIDATION_STATUS=pass\|fail`); exit code 0 = `pass`, non-zero = `fail` | `docs/harness/harness_manual_validation.md` Machine-Readable Outputs; `docs/harness/harness_ci_integration.md` Failure Expectations; see Specification REQ-08 for normative definition |

## Harness API Endpoints Exercised

The validation scripts exercise the following harness API route paths during execution. This enumeration is derived from the Section 8 behavioral checks and regression tests.

| Endpoint | Used By | Purpose | Source |
|----------|---------|---------|--------|
| `/api/harness/session/list` | `setup.server_reachable`, readiness polling | Verify harness server is reachable; poll readiness in CI | `docs/harness/harness_manual_validation.md` Prerequisites; `docs/harness/harness_ci_integration.md` Job Flow step 5 |
| `/api/harness/session/*` (CRUD) | `regression.session_crud`, `section8.session_persistence_resume` | Create, read, update, delete sessions; verify `claudeSessionId` persistence | `docs/harness/harness_manual_validation.md` Section 8 Matrix row 2, Additional Regression Checks |
| `/api/harness/turn` | `section8.smoke_stream`, `section8.permissions_dontask`, `section8.sdk_native_stream` | Execute turns to observe SSE event sequences, permission behavior, and SDK-native stream handling | `docs/harness/harness_manual_validation.md` Section 8 Matrix rows 1, 3, 5 |
| `/api/harness/interrupt` | `section8.interrupt_sigint` | Interrupt an active turn; verify `200 {"ok":true}` response and terminal `process:exit` with interruption marker | `docs/harness/harness_manual_validation.md` Section 8 Matrix row 4 |

**Note:** The specific route path patterns above are **ASSUMPTION (inferred from behavioral descriptions)**. The exact API route paths are inferable from the Section 8 behavioral checks and regression test descriptions but are not explicitly enumerated as a consolidated list in any single source document. See Lensing Item B-002.

## Conditions

| Condition | Description | Source |
|-----------|-------------|--------|
| Frontend runtime surface | `frontend/` directory must exist with buildable application; scripts are located under `frontend/scripts/` | `docs/harness/harness_manual_validation.md` Local-Only Boundary (check for `RUNTIME_SURFACE_MISSING`) |
| Harness server reachable | Harness server must be reachable at `HARNESS_BASE_URL` (default `http://127.0.0.1:3000`) | `docs/harness/harness_manual_validation.md` Prerequisites |
| Anthropic API key | `ANTHROPIC_API_KEY` must be available to the server runtime for live validation | `docs/harness/harness_manual_validation.md` Prerequisites |
| Node.js environment | Node.js runtime required for `.mjs` script execution; version TBD -- blocked on DEL-01-03 (Frontend Workspace Bootstrap) establishing the stack version. Tracked as CT-001 in Guidance Conflict Table. | **ASSUMPTION** -- implied by `.mjs` script format and application stack; Lensing Item A-002 |
| Pre-tier gate position | This deliverable is in the pre-tier gate; Tier 2 code-bearing work that depends on frontend paths remains blocked until this deliverable reaches at least `IN_PROGRESS` | Decomposition SCA-001 Execution Gating Rule |
| Repository-only execution | No non-local repository is required for execution; all artifacts produced from this repo | `_CONTEXT.md`; Decomposition OBJ-008 acceptance criteria |

## Construction

| Aspect | Value | Source |
|--------|-------|--------|
| Validation scripts | `frontend/scripts/validate-harness-section8.mjs` (core Section 8 matrix), `frontend/scripts/validate-harness-premerge.mjs` (pre-merge wrapper with stable artifact copy) | `docs/harness/harness_manual_validation.md` |
| npm run target | `npm run harness:validate:premerge` (canonical pre-merge command) | `docs/harness/harness_manual_validation.md` Usage |
| Summary artifact schema | `summary.json` -- must contain required SDK test IDs; legacy `regression.api_chat_reachability` must be absent | `docs/harness/harness_ci_integration.md` Job Flow step 7 |
| Artifact directory layout | `${TMPDIR:-/tmp}/chirality-harness-validation/latest/`: `summary.json`, `sse/*.sse`, `api/*.json`, `logs/*.json`, `cleanup/sessions.json` | `docs/harness/harness_manual_validation.md` Artifact Layout |
| Stable artifact directory | `frontend/artifacts/harness/section8/latest/` (mirrored by pre-merge wrapper) | `docs/harness/harness_manual_validation.md`; `docs/harness/harness_ci_integration.md` |
| Section 8 test matrix | Smoke stream ordering, session persistence + resume, permissions under `dontAsk` (deny + allow), interrupt behavior, SDK-native stream handling | `docs/harness/harness_manual_validation.md` Section 8 Matrix |
| Additional regression checks | `setup.server_reachable`, `regression.session_crud`, `section8.smoke_stream`, `section8.session_persistence_resume`, `section8.permissions_dontask`, `section8.interrupt_sigint`, `section8.sdk_native_stream` | `docs/harness/harness_manual_validation.md` Additional Regression Checks |
| Runbook documents | Local execution instructions, CI integration guide, architecture notes -- to be placed in `docs/` and/or deliverable-local | SOW-049; `_CONTEXT.md` |
| Artifact mirroring (full) | Optional: `sse/*.sse`, `api/*.json`, `logs/*.json`, `mock/**`, `cleanup/sessions.json` mirrored to stable CI path | `docs/harness/harness_artifact_mirroring_guidance.md` What "Full Mirroring" Means |

## References

| Ref | Document | Relevance |
|-----|----------|-----------|
| R1 | `docs/harness/harness_manual_validation.md` | Canonical validation script usage, artifact layout, Section 8 matrix, machine-readable outputs |
| R2 | `docs/harness/harness_ci_integration.md` | CI workflow, job flow, failure expectations, summary schema validation |
| R3 | `docs/harness/harness_artifact_mirroring_guidance.md` | Artifact mirroring posture, when to enable full mirroring, guardrails |
| R4 | `docs/PLAN.md` Section 2 | FE-4 validation + packaging baseline; existing tooling context |
| R5 | Decomposition (G7-APPROVED + SCA-001) | DEL-07-03 entry, SOW-048, SOW-049, OBJ-006, OBJ-008, execution gating rule |
| R6 | `_CONTEXT.md` | Deliverable identity, scope coverage, anticipated artifacts |
| R7 | DEL-07-01 (Harness Validation Suite) production documents | Sibling: broader harness contract validation -- opts fallback chains, subagent governance, attachment resolver |
| R8 | DEL-07-02 (Example Execution Roots) production documents | Sibling: conformance fixtures that may be consumed by validation |
