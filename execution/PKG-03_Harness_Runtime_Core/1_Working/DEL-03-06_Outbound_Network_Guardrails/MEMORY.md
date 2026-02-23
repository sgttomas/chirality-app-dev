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

## Open Questions

- OI-002 (enforcement mechanism + proof standard) remains unresolved pending human selection from `OI-002_Enforcement_Proof_Decision_Input_2026-02-23.md`; current implementation remains baseline hardening and does not claim closure of full enforcement/verification scope.

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
- Verification:
  - `npm test -- src/__tests__/lib/harness-anthropic-agent-sdk-manager.test.ts` -> PASS (`58` tests)
  - `npm test` -> PASS (`155` tests)
  - `npm run build` -> PASS
  - `npm run typecheck` -> PASS (sequential rerun after known parallel `.next/types` race)
