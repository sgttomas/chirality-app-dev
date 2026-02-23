# OI-002 Decision Input — DEL-03-06 Enforcement Mechanism + Proof Standard

**Date:** 2026-02-23  
**Deliverable:** `DEL-03-06_Outbound_Network_Guardrails`  
**Decision scope:** Human ruling for OI-002 (select runtime enforcement mechanism and verification proof standard)

## Purpose

Resolve OI-002 with a concrete, auditable decision that unblocks Specification `REQ-NET-005` and `REQ-NET-006` and Procedure Steps 4-5.

OI-002 source context:
- `execution/_Decomposition/ChiralityApp_SoftwareDecomposition_2026-02-21_G7-APPROVED.md` (DEL-03-06 open issue)
- `execution/PKG-03_Harness_Runtime_Core/1_Working/DEL-03-06_Outbound_Network_Guardrails/Specification.md`
- `execution/PKG-03_Harness_Runtime_Core/1_Working/DEL-03-06_Outbound_Network_Guardrails/Procedure.md`
- `execution/PKG-03_Harness_Runtime_Core/1_Working/DEL-03-06_Outbound_Network_Guardrails/Guidance.md`

## Current Evidence Snapshot (Pre-Ruling Baseline)

- Fail-closed Anthropic base-URL policy is implemented in runtime manager:
  - absolute URL required
  - `https` only
  - host allowlist (`api.anthropic.com`)
  - credentials disallowed
  - non-default ports disallowed
- Regression coverage now includes:
  - non-allowlisted host rejection
  - non-HTTPS rejection
  - malformed URL rejection
  - credentialed URL rejection
  - non-default port rejection
  - explicit default `:443` acceptance
- Current baseline hardening is partial by design:
  - it protects provider-level outbound configuration
  - it does not yet establish full renderer/main-process enforcement coverage
  - it does not yet establish traffic-capture proof criteria

Evidence references:
- `frontend/src/lib/harness/anthropic-agent-sdk-manager.ts`
- `frontend/src/__tests__/lib/harness-anthropic-agent-sdk-manager.test.ts`
- `execution/_Coordination/TIER3_CONTROL_LOOP_2026-02-23_PASS4.md`
- `execution/_Reconciliation/TIER3_INTERFACE_RECON_2026-02-23_PASS4.md`

## Decision Options

### Option A: Provider-surface enforcement only + minimal proof

Enforcement:
1. Keep provider base-URL guardrails as primary runtime control.
2. Keep existing telemetry/update hardening where already present.
3. Defer renderer-process specific enforcement layers.

Proof standard:
1. Focus on unit/integration tests in app code.
2. Single capture run over startup + one turn + shutdown.

Tradeoff:
- Lowest implementation overhead.
- Highest residual risk for renderer-originated or non-provider outbound paths.

### Option B: Recommended layered enforcement + repeatable capture proof

Enforcement:
1. Keep provider base-URL guardrails (already landed).
2. Add renderer/main-process egress interception layer (Electron `session.webRequest` allowlist gate).
3. Keep auto-update/telemetry disable posture as required baseline.
4. Require blocked egress to fail closed with typed diagnostics (no silent bypass).

Proof standard:
1. Capture traffic over required scenarios:
   - cold start
   - session boot
   - turn execution
   - idle window (10 minutes minimum)
   - shutdown
2. Run at least 3 independent runs on baseline fixture usage.
3. Pass criteria:
   - no non-allowlisted outbound traffic except explicitly ruled infrastructure TLS exceptions (if CONF-002 is accepted)
   - all blocked attempts observable in logs/errors
4. Keep artifacts and summary in deliverable-local records.

Tradeoff:
- Strong assurance with manageable complexity.
- Requires implementation and verification work beyond current baseline.

### Option C: OS-level enforcement + strictest proof

Enforcement:
1. Option B layers, plus OS-level packet filtering constraints.
2. Runtime process launched under host firewall policy.

Proof standard:
1. Long-window capture and fault-injection runs.
2. Separate negative testing for bypass attempts.

Tradeoff:
- Highest assurance.
- Operationally heavy for local development and desktop distribution.

## Recommendation

Adopt **Option B** for DEL-03-06.

Rationale:
- Satisfies `REQ-NET-005` process-coverage intent with explicit layered controls.
- Preserves practical operability for this repository and local workflows.
- Produces auditable proof criteria for `REQ-NET-006` without requiring OS-level deployment constraints.

## Proposed Human Ruling Text (OI-002)

"For DEL-03-06, enforcement mechanism is Option B layered control: provider base-URL guardrails plus Electron egress allowlist interception and required telemetry/update disable posture. Verification proof standard is three-run traffic capture across startup, session boot, turn execution, 10-minute idle window, and shutdown; pass requires no non-allowlisted outbound traffic except explicitly accepted infrastructure TLS exceptions and observable fail-closed diagnostics on blocked attempts."

## Decision Outcome

- **Status:** PENDING HUMAN RULING
- **Selected option:** TBD
- **Date of ruling:** TBD

