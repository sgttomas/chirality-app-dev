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
- SDK-path implementation landed in current cycle:
  - `@anthropic-ai/sdk` pinned to `0.78.0`
  - default `anthropic-version` header baseline set to `2023-06-01` (env override supported)
- Key provisioning contract for current scope is environment-only (`ANTHROPIC_API_KEY`, optional compatibility alias `CHIRALITY_ANTHROPIC_API_KEY`) with no persisted secure-storage mechanism.
- Alias policy follow-through (2026-02-23): retain compatibility alias fallback for migration, but enforce canonical-precedence (`ANTHROPIC_API_KEY` wins when both keys are set).
- PASS5 fixture-boundary expansion (2026-02-23): provider tests now explicitly cover DEL-04-01-style fixture boundaries, including resolver-provided MIME precedence and warning/document fallback ordering.
- PASS6 fixture-boundary expansion (2026-02-23): provider tests now cover inverse MIME-authority behavior, confirming resolver-provided non-image MIME remains authoritative even when file extension is image-like.
- PASS7 fixture-boundary expansion (2026-02-23): provider now normalizes resolver MIME metadata (case/spacing) before classification; coverage verifies non-canonical resolver image MIME remains authoritative and uppercase `application/octet-stream` still routes through extension fallback.
- PASS8 error-surface hardening (2026-02-23): provider now redacts configured API-key material from surfaced SDK failure messages, stream error events, and network error detail payloads to enforce REQ-09 log/error protection boundaries.
- PASS9 fixture/error-surface hardening (2026-02-23): provider now strips MIME parameters before classification (for example `image/png; charset=binary`) and uses one longest-key-first redaction pass to prevent overlap-driven key-suffix leakage artifacts in surfaced errors.
- PASS10 error-surface hardening (2026-02-23): provider now includes URL-encoded configured key variants in the redaction candidate set (including `+`-encoded spaces) so encoded key material cannot leak through SDK/stream/network surfaced errors.

## Open Questions

*None currently.*

## Notes

- Tier 5 PASS9 follow-through (2026-02-23) landed in:
  - `frontend/src/lib/harness/anthropic-agent-sdk-manager.ts`
  - `frontend/src/__tests__/lib/harness-anthropic-agent-sdk-manager.test.ts`
  - evidence:
    - `execution/_Coordination/TIER5_CONTROL_LOOP_2026-02-23_PASS9.md`
    - `execution/_Reconciliation/TIER5_INTERFACE_RECON_2026-02-23_PASS9.md`
- Tier 5 PASS10 follow-through (2026-02-23) landed in:
  - `frontend/src/lib/harness/anthropic-agent-sdk-manager.ts`
  - `frontend/src/__tests__/lib/harness-anthropic-agent-sdk-manager.test.ts`
  - evidence:
    - `execution/_Coordination/TIER5_CONTROL_LOOP_2026-02-23_PASS10.md`
    - `execution/_Reconciliation/TIER5_INTERFACE_RECON_2026-02-23_PASS10.md`
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
  - server-side Anthropic SDK client initialization with baseURL/version contract wiring and typed error classification.
  - SDK stream translation to harness `chat:delta` / `chat:complete` / `process:exit` events.
  - timeout + interrupt handling via `AbortController`.
  - multimodal image block formatting (`image/*` to base64); unsupported non-image attachments degrade to explicit text notice.
  - marker compatibility retained for existing harness baseline tests (`__BOOT_SDK_FAIL__`, `TURN_SDK_FAIL_TEST`, dontAsk permission markers).
- Dependency refresh applied:
  - `DEP-03-05-005` updated to `RequiredMaturity=IN_PROGRESS`, `SatisfactionStatus=SATISFIED` (upstream DEL-03-03 now `IN_PROGRESS`).
  - `DEP-03-05-010` updated to `SatisfactionStatus=SATISFIED` (SDK prerequisite closed after implementation pin).
- Verification evidence in `frontend/`:
  - `npm test -- src/__tests__/lib/harness-anthropic-agent-sdk-manager.test.ts` -> PASS (22 tests)
  - alias-policy coverage now explicit:
    - canonical absent + alias present -> alias used
    - canonical + alias both present -> canonical used
  - multimodal formatting coverage now explicit:
    - image attachment (`.png`) -> Anthropic `image` content block with base64 source
    - non-image attachment -> explicit text fallback block
    - resolver-classified image MIME with non-image extension remains image-mapped
    - resolver-classified non-image MIME with image-like extension remains fallback-text mapped
    - resolver-classified image MIME with non-canonical casing/spacing remains image-mapped after normalization
    - resolver-classified uppercase `application/octet-stream` remains extension-fallback input
    - resolver-classified parameterized image MIME (for example `image/png; charset=binary`) is normalized to canonical image media type
    - resolver-classified parameterized `application/octet-stream` remains extension-fallback input
    - resolver warning text and document fallback order preserved in Anthropic request content
    - SDK/stream/network surfaced error payloads redact configured API-key material (`[REDACTED_API_KEY]`) including overlapping canonical/alias and URL-encoded key scenarios
  - `npm test -- src/__tests__/lib/harness-runtime.test.ts src/__tests__/lib/harness-anthropic-agent-sdk-manager.test.ts` -> PASS (6 tests)
  - `npm test` -> PASS (115 tests)
  - `npm run typecheck` -> PASS (sequential rerun after build due known `.next/types` race when run concurrently)
  - `npm run build` -> PASS
