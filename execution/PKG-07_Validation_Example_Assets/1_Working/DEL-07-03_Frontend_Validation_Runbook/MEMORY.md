# Memory — DEL-07-03

## Key Decisions & Human Rulings

- 2026-02-22: Implemented validation as a two-layer model:
  - Core runner: `validate-harness-section8.mjs` (executes Section 8 + regression checks, produces tmp summary/artifacts).
  - Wrapper: `validate-harness-premerge.mjs` (invokes core runner, validates schema, copies stable artifact, emits premerge machine-readable outputs).
- 2026-02-24: Validation schema baseline is now 8 checks (includes `section8.boot_error_taxonomy` in both core runner ordering and premerge `REQUIRED_TEST_IDS`), and lifecycle advanced to `CHECKING` after repeatable live evidence refresh.
- 2026-02-24: Human issuance approval received and applied; lifecycle advanced `CHECKING -> ISSUED` with decision artifact `ISSUED_Gate_Decision_Record_2026-02-24.md`.
- 2026-02-22: Enforced canonical lowercase `pass|fail` vocabulary and explicit environment-style output lines for CI parsing.
- 2026-02-22: Added deterministic stable summary destination and repo hygiene controls:
  - Stable path: `frontend/artifacts/harness/section8/latest/summary.json`
  - `.gitignore` rule excludes summary file from commits
  - `.gitkeep` preserves folder structure.
- 2026-02-22: Added deterministic interrupt marker path (`INTERRUPT_SIGINT_TEST`) in stub runtime to make interrupt behavior reliably testable in automated runs.

## Domain Context

- DEL-07-03 is the second Wave 0c pre-tier gate deliverable and pairs with DEL-02-05 to satisfy SCA-001 frontend gate progression.
- Validation scope is intentionally local-runtime and contract-driven; this pass focuses on executable baseline + reproducible outputs, not full production hardening.

## Open Items

- Clarify "coordination artifacts" destination for `RUNTIME_SURFACE_MISSING` beyond stdout/logging (REQ-14 open semantics).
- Decide whether to add a dedicated runbook index doc in `docs/harness/` or keep existing three-file doc topology as the primary entry surface.
- Finalize CI timeout tuning if runner characteristics change (current values are conservative defaults).

## Proposal History

- 2026-02-22: Added validation scripts:
  - `frontend/scripts/validate-harness-section8.mjs`
  - `frontend/scripts/validate-harness-premerge.mjs`
- 2026-02-22: Added CI integration:
  - `.github/workflows/harness-premerge.yml`
- 2026-02-22: Updated runtime and package wiring:
  - `frontend/src/lib/harness/agent-sdk-manager.ts` (permission + interrupt test markers)
  - `frontend/package.json` (new `harness:validate:*` scripts)
  - `frontend/.gitignore` (summary artifact exclusion)
  - `frontend/artifacts/harness/section8/latest/.gitkeep`

Verification evidence:
- `npm run harness:validate:premerge` -> PASS
  - `HARNESS_VALIDATION_STATUS=pass`
  - `HARNESS_PREMERGE_STATUS=pass`
  - `HARNESS_PREMERGE_TEST_COUNT=8`
  - Stable summary produced at `frontend/artifacts/harness/section8/latest/summary.json`
- 2026-02-24 repeatability refresh:
  - Run 1: `HARNESS_PREMERGE_STATUS=pass`, `HARNESS_PREMERGE_TEST_COUNT=8`
  - Run 2: `HARNESS_PREMERGE_STATUS=pass`, `HARNESS_PREMERGE_TEST_COUNT=8`
- `npm run test` -> PASS (7/7).
- `npm run typecheck` -> PASS.
- `npm run build` -> PASS.

## Interface & Dependency Notes

- DEL-07-03 now directly exercises DEL-03-07 API surfaces:
  - `/api/harness/session/create`
  - `/api/harness/session/list`
  - `/api/harness/session/:id`
  - `/api/harness/turn`
  - `/api/harness/interrupt`
- Wrapper enforces schema expectations for required test IDs and legacy exclusion (`regression.api_chat_reachability` absent), aligning with CI gate semantics.
- No dependency-row mutation occurred in deliverable dependency ledgers during this implementation pass.
