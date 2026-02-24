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
- PASS6 follow-through (2026-02-23) completed OI-002 Option B proof-standard execution:
  - added opt-in renderer probe execution hook in `frontend/electron/main.ts` (`CHIRALITY_NETWORK_POLICY_PROBE_*` env controls)
  - added repeatable capture harness `frontend/scripts/run-network-policy-proof.mjs` + `npm run proof:network-policy`
  - executed 3 independent runs (startup/session boot/turn/10-minute idle/shutdown) with aggregate `PASS`
  - archived proof artifacts under `Evidence/OI-002_PROOF_OPTIONB_2026-02-23_PASS6/`
  - added final report `OI-002_OptionB_Proof_Report_2026-02-23.md`
- PASS7 follow-through (2026-02-24) prepared lifecycle/gating artifacts and applied approvals for DEL-03-06 `CHECKING` entry:
  - drafted CONF-002 disposition input with concrete bounded TLS-infrastructure carve-out text in `CONF-002_Disposition_Decision_Input_2026-02-24.md`
  - drafted lifecycle gate packet in `CHECKING_Gate_Decision_Input_2026-02-24.md`
  - same-session human approvals applied: CONF-002 Option B approved and lifecycle advanced `IN_PROGRESS -> CHECKING`.
- PASS8 follow-through (2026-02-24) closed CHECKING documentation residuals without runtime mutation:
  - produced closure artifact `REQ-NET-004_005a_SDK_REFERENCE_CLOSURE_2026-02-24.md`
  - marked `REQ-NET-004` and `REQ-NET-005a` closure disposition in Specification/Guidance/Procedure continuity docs
  - completed SDK external-reference capture in `_REFERENCES.md` with Electron/Anthropic authoritative links and installed SDK source pointers
- PASS9 follow-through (2026-02-24) drafted issuance gate packet without lifecycle mutation:
  - added `ISSUED_Gate_Decision_Input_2026-02-24.md` with explicit decision options and recommended `CHECKING -> ISSUED` gate statement
  - propagated issuance-packet pointers into continuity docs (`_REFERENCES.md`, Datasheet, Procedure, `_STATUS.md`)

## Open Questions

- Human issuance gate decision is now pending: explicit `CHECKING -> ISSUED` approval is required against `ISSUED_Gate_Decision_Input_2026-02-24.md`.
- No unresolved CHECKING residuals remain for `REQ-NET-004`, `REQ-NET-005a`, or SDK external-reference completeness after PASS8 documentation closure.

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
- PASS6 proof-run automation + evidence updates:
  - `frontend/electron/main.ts` (opt-in renderer probe hook)
  - `frontend/scripts/run-network-policy-proof.mjs`
  - `frontend/package.json` (`proof:network-policy`)
  - `execution/PKG-03_Harness_Runtime_Core/1_Working/DEL-03-06_Outbound_Network_Guardrails/Evidence/OI-002_PROOF_OPTIONB_2026-02-23_PASS6/`
  - `execution/PKG-03_Harness_Runtime_Core/1_Working/DEL-03-06_Outbound_Network_Guardrails/OI-002_OptionB_Proof_Report_2026-02-23.md`
- PASS7 gate decision artifacts:
  - `execution/PKG-03_Harness_Runtime_Core/1_Working/DEL-03-06_Outbound_Network_Guardrails/CONF-002_Disposition_Decision_Input_2026-02-24.md`
  - `execution/PKG-03_Harness_Runtime_Core/1_Working/DEL-03-06_Outbound_Network_Guardrails/CHECKING_Gate_Decision_Input_2026-02-24.md`
- PASS8 closure artifact:
  - `execution/PKG-03_Harness_Runtime_Core/1_Working/DEL-03-06_Outbound_Network_Guardrails/REQ-NET-004_005a_SDK_REFERENCE_CLOSURE_2026-02-24.md`
- PASS9 issuance gate packet:
  - `execution/PKG-03_Harness_Runtime_Core/1_Working/DEL-03-06_Outbound_Network_Guardrails/ISSUED_Gate_Decision_Input_2026-02-24.md`
- Verification:
  - `npm test -- src/__tests__/scripts/build-network-policy.test.ts` -> PASS (`3` tests)
  - `npm run proof:network-policy -- --runs 3 --idle-seconds 600 --idle-sample-seconds 60 --output-dir ../execution/PKG-03_Harness_Runtime_Core/1_Working/DEL-03-06_Outbound_Network_Guardrails/Evidence/OI-002_PROOF_OPTIONB_2026-02-23_PASS6` -> PASS
  - `npm run build` -> PASS
  - `npm run typecheck` -> PASS (sequential rerun after known parallel `.next/types` race)
