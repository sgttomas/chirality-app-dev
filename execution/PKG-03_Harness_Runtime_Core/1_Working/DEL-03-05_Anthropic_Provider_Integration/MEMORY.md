# Working Memory — DEL-03-05

*This file is shared working memory for WORKING_ITEMS and TASK agents operating on this deliverable.*

## Key Decisions

- Introduced an explicit provider-mode switch in runtime bootstrap:
  - `CHIRALITY_HARNESS_PROVIDER=anthropic` -> use Anthropic-backed manager.
  - unset/other values -> keep deterministic stub manager.
- Kept stub mode as default to preserve section8/premerge deterministic validation behavior while DEL-03-05 matures.
- Human ruling applied (2026-02-23):
  - `OI-001 = ENV_ONLY`
  - provider implementation path = `ADOPT_SDK_NOW`
  - documentation/scope prep only in this cycle (no added implementation)
- Key provisioning contract for current scope is environment-only (`ANTHROPIC_API_KEY`, optional compatibility alias `CHIRALITY_ANTHROPIC_API_KEY`) with no persisted secure-storage mechanism.

## Open Questions

- Which SDK version pin should be adopted first in `frontend/package.json` for DEL-03-05 implementation (`@anthropic-ai/sdk`).
- Whether compatibility alias support (`CHIRALITY_ANTHROPIC_API_KEY`) should remain after SDK-path implementation or be retired to canonical `ANTHROPIC_API_KEY` only.

## Notes

- Documentation/ruling closure pass (2026-02-23) added:
  - `POLICY_RULING_OI-001_PROVIDER_2026-02-23.md`
  - DEL-03-05 docs aligned to rulings (`Datasheet.md`, `Specification.md`, `Guidance.md`, `Procedure.md`)
  - dependency refresh:
    - `DEP-03-05-008` -> `SATISFIED` (OI-001 resolved)
    - `DEP-03-05-010` remains `PENDING` (SDK integration still required completion work)
  - pass evidence:
    - `execution/_Coordination/TIER5_CONTROL_LOOP_2026-02-23_PASS2.md`
    - `execution/_Reconciliation/TIER5_INTERFACE_RECON_2026-02-23_PASS2.md`
  - No additional implementation was applied in this pass.
- Tier 5 implementation pass (2026-02-23) landed in:
  - `frontend/src/lib/harness/anthropic-agent-sdk-manager.ts`
  - `frontend/src/lib/harness/runtime.ts`
  - `frontend/src/__tests__/lib/harness-anthropic-agent-sdk-manager.test.ts`
  - `frontend/src/__tests__/lib/harness-runtime.test.ts`
- Provider manager behavior added:
  - server-side Anthropic request dispatch (`/v1/messages`) with API-key resolution and typed error classification.
  - SSE stream translation from Anthropic deltas to harness `chat:delta` / `chat:complete` / `process:exit` events.
  - timeout + interrupt handling via `AbortController`.
  - multimodal image block formatting (`image/*` to base64); unsupported non-image attachments degrade to explicit text notice.
  - marker compatibility retained for existing harness baseline tests (`__BOOT_SDK_FAIL__`, `TURN_SDK_FAIL_TEST`, dontAsk permission markers).
- Dependency refresh applied:
  - `DEP-03-05-005` updated to `RequiredMaturity=IN_PROGRESS`, `SatisfactionStatus=SATISFIED` (upstream DEL-03-03 now `IN_PROGRESS`).
- Verification evidence in `frontend/`:
  - `npm test -- src/__tests__/lib/harness-runtime.test.ts src/__tests__/lib/harness-anthropic-agent-sdk-manager.test.ts` -> PASS (5 tests)
  - `npm test` -> PASS (96 tests)
  - `npm run typecheck` -> PASS
  - `npm run build` -> PASS
