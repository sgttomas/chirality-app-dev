# Tier 3 Interface Reconciliation — 2026-02-23 (Pass 3 DEL-03-06 Outbound Base-URL Allowlist Guardrails)

## Scope

- Reconciliation type: interface coherence check after DEL-03-06 outbound base-URL policy hardening
- Tier scope: `DEL-03-06` runtime policy boundary with `DEL-03-05` Anthropic provider integration endpoint contract
- Inputs:
  - `frontend/src/lib/harness/anthropic-agent-sdk-manager.ts`
  - `frontend/src/__tests__/lib/harness-anthropic-agent-sdk-manager.test.ts`
  - `execution/PKG-03_Harness_Runtime_Core/1_Working/DEL-03-06_Outbound_Network_Guardrails/Specification.md`
  - `execution/PKG-03_Harness_Runtime_Core/1_Working/DEL-03-06_Outbound_Network_Guardrails/Procedure.md`

## Interface Set Reviewed

1. `DEL-03-06 -> DEL-03-05` allowlist boundary: provider base URL must stay Anthropic-only (`api.anthropic.com`)
2. `DEL-03-06` fail-closed behavior: invalid/non-compliant base URLs must reject before SDK request dispatch
3. `DEL-03-06` error taxonomy continuity: policy failures should remain typed `SDK_FAILURE` and preserve structured details

## Findings

| Interface | Expected contract | Observed posture | Result |
|---|---|---|---|
| Allowlist boundary (`REQ-NET-001`, `REQ-NET-007`) | Base URL host must be explicitly allowlisted Anthropic domain | Runtime now validates `CHIRALITY_ANTHROPIC_API_URL` host against explicit allowlist (`api.anthropic.com`) and fails closed on mismatch | SATISFIED |
| Fail-closed pre-dispatch behavior | Non-compliant URLs should be rejected before outbound request dispatch | Regression tests verify non-allowlisted host, non-HTTPS protocol, and malformed URL cases reject with no `clientFactory`/SDK calls | SATISFIED |
| Typed error continuity | Policy failures should be surfaced in harness error taxonomy with structured details | Rejections are typed `SDK_FAILURE` with detail categories `NETWORK_POLICY_VIOLATION` / `INVALID_BASE_URL` and policy metadata | SATISFIED |

## Contradictions and Actions

- No cross-deliverable contradiction detected in this pass.
- Carry-forward action:
  - expand enforcement coverage beyond provider base-URL contract after OI-002 ruling selects full mechanism/proof standard.

## Reconciliation Disposition

- Tier 3 DEL-03-06 interface posture is coherent after this baseline hardening pass.
- Deliverable has advanced to `IN_PROGRESS`; OI-002-gated enforcement-method and capture-proof closure remain open.
