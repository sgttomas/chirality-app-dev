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

## Open Questions

- OI-002 (enforcement mechanism + proof standard) remains unresolved; this pass is baseline hardening that does not claim closure of full enforcement/verification scope.

## Notes

- Baseline implementation landed in:
  - `frontend/src/lib/harness/anthropic-agent-sdk-manager.ts`
  - `frontend/src/__tests__/lib/harness-anthropic-agent-sdk-manager.test.ts`
- Added regression coverage for:
  - non-allowlisted host rejection (`https://example.com/...`)
  - non-HTTPS rejection (`http://api.anthropic.com/...`)
  - malformed base URL rejection (`not-a-url`)
- Verification:
  - `npm test -- src/__tests__/lib/harness-anthropic-agent-sdk-manager.test.ts` -> PASS (`55` tests)
  - `npm test` -> PASS (`152` tests)
  - `npm run build` -> PASS
  - `npm run typecheck` -> PASS
