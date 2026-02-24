# Working Memory — DEL-07-01

*This file is shared working memory for WORKING_ITEMS and TASK agents operating on this deliverable.*

## Key Decisions

- 2026-02-24: Executed live harness validation against local routes with two consecutive `harness:validate:premerge` passes (`HARNESS_PREMERGE_STATUS=pass`, `HARNESS_PREMERGE_TEST_COUNT=8`) and refreshed stable artifact output.
- 2026-02-24: Re-ran live premerge validation again (two additional consecutive `8/8` passes) after toolkit persistence-hardening changes and confirmed no regression in runtime/validation interfaces.
- 2026-02-24: Completed readiness review for lifecycle promotion and held `IN_PROGRESS` pending explicit ruling on whether CI workflow codification in `.github/workflows/` is required beyond the current documentation-driven CI-ready posture.
- 2026-02-24: Human ruling received: CI codification requirement is `docs-only` for DEL-07-01 (no mandatory `.github/workflows` codification gate for promotion).
- 2026-02-24: Updated `frontend/scripts/validate-harness-section8.mjs` to auto-stage requested project roots that sit inside instruction root into `${TMPDIR}/chirality-harness-validation/latest/workroots/staged-project-root`, aligning validator behavior with `WORKING_ROOT_CONFLICT` policy.
- 2026-02-24: Added operator-facing harness validation documentation under `frontend/docs/harness/README.md` with local and CI execution steps.
- 2026-02-24: Added requirement-to-artifact mapping in `frontend/docs/harness/TRACEABILITY.md` covering REQ-01 through REQ-16 with script/test references.
- 2026-02-24: Added targeted harness utility coverage tests supporting DEL-07-01 validation posture:
  - `frontend/src/__tests__/lib/harness-toolkit.test.ts`
  - `frontend/src/__tests__/lib/harness-ui-attachments.test.ts`
  - `frontend/src/__tests__/lib/harness-chat-draft.test.ts`
  - attachment-only payload assertion in `frontend/src/__tests__/lib/harness-client.test.ts`

## Open Questions

- Should CI pipeline configuration snippets be codified in `.github/workflows/` as executable workflow steps, or remain documentation-only for now?

## Notes

- Current script surface already includes:
  - `frontend/scripts/validate-harness-section8.mjs`
  - `frontend/scripts/validate-harness-premerge.mjs`
- Verification run (2026-02-24):
  - `npm run typecheck`
  - `npm test -- src/__tests__/lib/harness-client.test.ts src/__tests__/lib/harness-ui-attachments.test.ts src/__tests__/lib/harness-toolkit.test.ts src/__tests__/lib/harness-chat-draft.test.ts`
  - `npm test -- src/__tests__/lib/harness-runtime.test.ts src/__tests__/api/harness/routes.test.ts`
  - `HARNESS_BASE_URL=http://127.0.0.1:3000 npm run harness:validate:premerge` (run twice; both pass)
  - `HARNESS_BASE_URL=http://127.0.0.1:3000 npm run harness:validate:premerge` (second repeat run pair after toolkit persistence hardening; both pass)
  - Stable artifact refreshed: `frontend/artifacts/harness/section8/latest/summary.json`
