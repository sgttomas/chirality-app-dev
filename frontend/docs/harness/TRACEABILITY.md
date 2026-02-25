# Harness Validation Traceability

## Requirement Mapping (DEL-07-01)

| Requirement | Coverage Artifact(s) |
|---|---|
| REQ-01 Validation Script Coverage | `frontend/scripts/validate-harness-section8.mjs` required check set (`setup.server_reachable`, `regression.session_crud`, `section8.boot_error_taxonomy`, `section8.smoke_stream`, `section8.session_persistence_resume`, `section8.permissions_dontask`, `section8.interrupt_sigint`, `section8.sdk_native_stream`) |
| REQ-02 Local Execution | `npm run harness:validate:section8` from `frontend/` |
| REQ-03 CI-Ready Posture | `npm run harness:validate:premerge` (non-interactive, exit-code based) |
| REQ-04 Session Boot Validation | `section8.boot_error_taxonomy`, plus `frontend/src/__tests__/api/harness/routes.test.ts` boot route tests |
| REQ-05 Turn Execution Validation | `section8.smoke_stream`, `section8.session_persistence_resume`, plus route tests for invalid empty turns |
| REQ-06 SSE Streaming Validation | `section8.smoke_stream`, `section8.sdk_native_stream` |
| REQ-07 Opts Mapping/Fallback | `frontend/src/__tests__/lib/harness-options.test.ts` |
| REQ-08 Subagent Governance Fail-Closed | `section8.permissions_dontask`, `frontend/src/__tests__/lib/harness-subagent-governance.test.ts`, governance route tests |
| REQ-09 Attachment Resolver Validation | `frontend/src/__tests__/lib/harness-attachment-resolver.test.ts`, attachment-focused route tests |
| REQ-10 Prompt Mode Selection Validation | `frontend/src/__tests__/api/harness/routes.test.ts` prompt-mode assertions |
| REQ-11 Validation Documentation | `frontend/docs/harness/README.md`, this file |
| REQ-12 Repeatable Execution | Two consecutive `harness:validate:premerge` runs; deterministic summary schema |
| REQ-13 CONTRACT K-Invariant Coverage | Governance + options + route tests (`harness-subagent-governance.test.ts`, `harness-options.test.ts`, `routes.test.ts`) |
| REQ-14 Test Isolation | Vitest unit tests are independently executable; section8 checks are isolated by per-check setup/cleanup |
| REQ-15 Error Path Validation | `section8.boot_error_taxonomy`, route tests for invalid request/attachment/governance paths |
| REQ-16 Deliverable Acceptance Criteria | `harness:validate:premerge` gate + docs + traceability mapping |

## Notes

- The premerge script enforces required check IDs and fails if legacy IDs appear.
- The suite uses stable machine-readable summary output for CI consumption.
