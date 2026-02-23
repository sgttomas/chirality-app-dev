# Working Memory — DEL-03-06

*This file is shared working memory for WORKING_ITEMS and TASK agents operating on this deliverable.*

## Key Decisions

- Enforced fail-closed Anthropic outbound base-URL policy in runtime manager:
  - `CHIRALITY_ANTHROPIC_API_URL` must be an absolute URL.
  - Protocol is restricted to `https`.
  - Host is restricted to explicit allowlist (`api.anthropic.com`).
  - Embedded credentials are disallowed.
  - Non-default ports are disallowed (only default `443` behavior).
- Policy violations throw typed `SDK_FAILURE` errors with explicit `NETWORK_POLICY_VIOLATION` / `INVALID_BASE_URL` categories and no SDK request dispatch.
- PASS4 follow-through (2026-02-23) expanded guardrail regression boundaries to explicitly verify:
  - embedded credentials in `CHIRALITY_ANTHROPIC_API_URL` are rejected fail-closed
  - non-default HTTPS port values are rejected fail-closed
  - explicit default port `:443` remains accepted and normalizes to canonical origin
- Prepared OI-002 decision packet input artifact:
  - `OI-002_Enforcement_Proof_Decision_Input_2026-02-23.md`
  - includes concrete enforcement/proof options and recommended layered Option B posture for human selection.
- PASS5 follow-through (2026-02-23) resolved OI-002 to Option B for this workspace and started enforcement-path implementation:
  - added renderer egress interception in `frontend/electron/main.ts` via `session.webRequest.onBeforeRequest`
  - allowlist posture is explicit: Anthropic API host (`api.anthropic.com`, `https`) + loopback runtime surfaces (`localhost`, `127.0.0.1`, `[::1]`)
  - non-allowlisted or invalid outbound URLs are blocked fail-closed with runtime diagnostics tagged to `REQ-NET-001`
  - added regression guardrails in `frontend/src/__tests__/scripts/build-network-policy.test.ts`
  - updated DEL-03-06 docs (`Datasheet.md`, `Specification.md`, `Guidance.md`, `Procedure.md`) from OI-002 pending to OI-002 resolved/in-progress execution posture.

## Open Questions

- OI-002 implementation follow-through remains open for proof capture execution (3 independent runs across startup/session boot/turn/10-minute idle/shutdown) and artifact archival.
- CONF-002 (OCSP/CRL infrastructure traffic carve-out wording) remains unresolved and can affect strict interpretation of REQ-NET-001 pass/fail analysis.

## Notes

- Baseline implementation landed in:
  - `frontend/src/lib/harness/anthropic-agent-sdk-manager.ts`
  - `frontend/src/__tests__/lib/harness-anthropic-agent-sdk-manager.test.ts`
- Added regression coverage for:
  - non-allowlisted host rejection (`https://example.com/...`)
  - non-HTTPS rejection (`http://api.anthropic.com/...`)
  - malformed base URL rejection (`not-a-url`)
- PASS4 follow-through landed in:
  - `frontend/src/__tests__/lib/harness-anthropic-agent-sdk-manager.test.ts`
  - `execution/PKG-03_Harness_Runtime_Core/1_Working/DEL-03-06_Outbound_Network_Guardrails/OI-002_Enforcement_Proof_Decision_Input_2026-02-23.md`
  - `execution/PKG-03_Harness_Runtime_Core/1_Working/DEL-03-06_Outbound_Network_Guardrails/Procedure.md`
- Added PASS4 regression coverage for:
  - credentialed base URL rejection (`https://user:pass@api.anthropic.com/...`)
  - non-default HTTPS port rejection (`https://api.anthropic.com:444/...`)
  - explicit default port acceptance (`https://api.anthropic.com:443/...`)
- PASS5 implementation + regression updates:
  - `frontend/electron/main.ts`
  - `frontend/src/__tests__/scripts/build-network-policy.test.ts`
  - `execution/PKG-03_Harness_Runtime_Core/1_Working/DEL-03-06_Outbound_Network_Guardrails/Datasheet.md`
  - `execution/PKG-03_Harness_Runtime_Core/1_Working/DEL-03-06_Outbound_Network_Guardrails/Specification.md`
  - `execution/PKG-03_Harness_Runtime_Core/1_Working/DEL-03-06_Outbound_Network_Guardrails/Guidance.md`
  - `execution/PKG-03_Harness_Runtime_Core/1_Working/DEL-03-06_Outbound_Network_Guardrails/Procedure.md`
  - `execution/PKG-03_Harness_Runtime_Core/1_Working/DEL-03-06_Outbound_Network_Guardrails/OI-002_Enforcement_Proof_Decision_Input_2026-02-23.md`
- Verification:
  - `npm test -- src/__tests__/scripts/build-network-policy.test.ts` -> PASS (`3` tests)
  - `npm test -- src/__tests__/lib/harness-anthropic-agent-sdk-manager.test.ts` -> PASS (`58` tests)
  - `npm test` -> PASS (`176` tests)
  - `npm run build` -> PASS
  - `npm run typecheck` -> PASS (sequential rerun after known parallel `.next/types` race)
