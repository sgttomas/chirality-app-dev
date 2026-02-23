# Working Memory — DEL-07-02

*This file is shared working memory for WORKING_ITEMS and TASK agents operating on this deliverable.*

## Key Decisions & Human Rulings

- Example inventory: 1 primary execution root (`examples/example-project/`) with 1 package (PKG-99) and 3 deliverables at 3 lifecycle states (OPEN, INITIALIZED, SEMANTIC_READY). **Human ruling (2026-02-22): this is the approved baseline count/scope.**
- Synthetic IDs: PKG-99, DEL-99-01/02/03 chosen to avoid collision with real project IDs (PKG-01..08).
- Dependencies.csv inclusion: **OUT for current baseline** (human ruling 2026-02-22). Revisit only if DEL-08-02 is brought IN and explicit schema-fixture coverage is requested.

## Domain Context

### Fixture Structure (created 2026-02-22)

```
examples/example-project/
  INIT.md
  _Coordination/_COORDINATION.md
  _Decomposition/Example_Decomposition.md
  _Aggregation/, _Change/, _Estimates/, _Reconciliation/, _Archive/, _Scripts/, _Sources/ (tool roots)
  PKG-99_Example_Package/
    0_References/_Archive/
    1_Working/_Archive/
    1_Working/DEL-99-01_Widget_Configuration/  (OPEN — min viable fileset)
    1_Working/DEL-99-02_Service_Integration/   (INITIALIZED — fileset + document kit)
    1_Working/DEL-99-03_Test_Harness/          (SEMANTIC_READY — fileset + kit + _SEMANTIC.md)
    2_Checking/From/, 2_Checking/To/
    3_Issued/_Archive/
```

### SPEC conformance checklist

- [x] REQ-01: Execution root conforms to SPEC Section 1 (PKG, _Decomposition, INIT.md)
- [x] REQ-02: Package folder conforms to SPEC Section 1.1 (all required subfolders)
- [x] REQ-03: Deliverable folders conform to SPEC Section 2 (naming, minimum viable fileset)
- [x] REQ-04: At least one deliverable at INITIALIZED+ with full document kit (DEL-99-02, DEL-99-03)
- [x] REQ-05: Folder names follow SPEC Section 10 sanitization
- [x] REQ-06: Every _STATUS.md has valid state, Last Updated, History
- [x] REQ-07: At least one _SEMANTIC.md with Matrix A and B tables (DEL-99-03)
- [x] REQ-08: Stable IDs consistent across folder names, _CONTEXT.md, _STATUS.md, decomposition
- [x] REQ-09: All content is synthetic (no real project data, credentials, proprietary content)
- [x] REQ-10: Examples usable by DEL-07-01 validation scripts without external setup — verified via runtime-backed runs against `examples/example-project` (`HARNESS_PREMERGE_STATUS=pass`, `HARNESS_PREMERGE_TEST_COUNT=7`, 2026-02-22 and 2026-02-23)

## Open Items

- Non-blocking residual: cold-start interrupt check in `frontend/scripts/validate-harness-section8.mjs` can transiently fail (`/api/harness/interrupt` returning `404`) on first run before route warmup; immediate rerun passed. Track this under DEL-07-01/DEL-03-01 hardening, not as a DEL-07-02 fixture defect.

## Proposal History

- Initial fixture created this session (1 root, 1 package, 3 deliverables, 3 lifecycle states).
- 2026-02-22: REQ-10 dependency posture updated; DEL-07-01 script surface is present, but runtime-backed execution evidence is still pending.
- 2026-02-22: REQ-10 closure achieved via live harness validation run with fixture root `examples/example-project`.
- 2026-02-22: Human rulings applied to close scope TBDs: minimum example root count set to 1; `Dependencies.csv` inclusion set OUT for baseline.
- 2026-02-22: Deliverable advanced to `CHECKING` after acceptance-gate readiness confirmation (`REQ-01..REQ-10` evidence + resolved prerequisite rulings).
- 2026-02-23: Checking decision completed; deliverable advanced to `ISSUED` after runtime-backed REQ-10 validation re-pass (`HARNESS_PREMERGE_STATUS=pass`, `HARNESS_PREMERGE_TEST_COUNT=7`).

## Interface & Dependency Notes

- DEL-07-01 (Harness Validation Scripts) successfully exercised these fixtures in the runtime-backed premerge run on 2026-02-22.
- DEL-08-03 (standalone CI validator) is out of scope but may also consume these fixtures.

## Pass-2 Evidence Refresh (2026-02-22)

- Confirmed DEL-07-01 validation scripts are present:
  - `frontend/scripts/validate-harness-section8.mjs`
  - `frontend/scripts/validate-harness-premerge.mjs`
- Attempted harness API reachability check for fixture root (`examples/example-project`) failed due no active local harness endpoint on `127.0.0.1:3000`; REQ-10 remains open pending runtime-backed validation run.

## Pass-3 Runtime Evidence (2026-02-22)

- Started local harness runtime (`frontend` Next.js dev server) on `http://127.0.0.1:3000`.
- Executed:
  - `HARNESS_PROJECT_ROOT=/Users/ryan/ai-env/projects/chirality-app-dev/examples/example-project HARNESS_BASE_URL=http://127.0.0.1:3000 npm run harness:validate:premerge`
- Final machine-readable outputs:
  - `HARNESS_VALIDATION_STATUS=pass`
  - `HARNESS_PREMERGE_STATUS=pass`
  - `HARNESS_PREMERGE_TEST_COUNT=7`
- Artifact evidence:
  - Temporary summary: `/var/folders/0s/50y7rb796d1bqdxmpcz6qg800000gn/T/chirality-harness-validation/latest/summary.json`
  - Stable summary: `frontend/artifacts/harness/section8/latest/summary.json`
- Robustness hardening applied during closure:
  - `frontend/scripts/validate-harness-section8.mjs` interrupt probe now retries transient `404` responses for up to 2s to avoid startup race before active-turn registration.

## Pass-4 Checking Evidence (2026-02-23)

- Started local harness runtime (`frontend` dev stack) and executed:
  - `HARNESS_PROJECT_ROOT=/Users/ryan/ai-env/projects/chirality-app-dev/examples/example-project HARNESS_BASE_URL=http://127.0.0.1:3000 npm run harness:validate:premerge`
- First run result: `HARNESS_PREMERGE_STATUS=fail` due `section8.interrupt_sigint` reporting `Interrupt endpoint returned 404`.
- Immediate rerun result: `HARNESS_VALIDATION_STATUS=pass`, `HARNESS_PREMERGE_STATUS=pass`, `HARNESS_PREMERGE_TEST_COUNT=7`.
- Stable artifact refreshed at:
  - `frontend/artifacts/harness/section8/latest/summary.json`
- Issuance decision basis:
  - Example fixture remains conformant and usable; observed cold-start flake is assigned to validator/runtime hardening scope (DEL-07-01/DEL-03-01), not fixture structure/content.
