# CONF-002 Disposition Decision Input — DEL-03-06 Outbound Network Guardrails

**Date:** 2026-02-24  
**Deliverable:** `DEL-03-06_Outbound_Network_Guardrails`  
**Decision scope:** Resolve CONF-002 wording for TLS infrastructure traffic under `REQ-NET-001`

## Purpose

Provide a concrete disposition text for CONF-002 so `REQ-NET-001` can remain enforceable without conflicting with TLS certificate-validation mechanics.

## Conflict Summary

- `REQ-NET-001` currently states the application must not initiate outbound connections to any endpoint other than Anthropic API endpoints.
- TLS certificate validation may require infrastructure traffic (for example OCSP/CRL/AIA retrieval) to non-Anthropic endpoints.
- Current documentation identified this tension as CONF-002 with previously unresolved (`TBD`) ruling status before this decision record.

Impacted references:
- `Specification.md` (`REQ-NET-001` note C-001)
- `Guidance.md` (Conflict Table `CONF-002`)
- `Datasheet.md` (Conditions: OCSP/CRL infrastructure traffic)
- `OI-002_OptionB_Proof_Report_2026-02-23.md` (records caveat as unresolved)

## Current Evidence Context

- OI-002 Option B proof-standard runbook completed with aggregate `PASS`:
  - `Evidence/OI-002_PROOF_OPTIONB_2026-02-23_PASS6/summary.json`
- All three runs recorded blocked non-allowlisted probe traffic and no explicit non-allowlisted outbound TCP endpoints in run summaries.
- Remaining ambiguity is normative wording, not implementation capability.

## Decision Options

### Option A: Keep strict literal text (no carve-out)
Retain `REQ-NET-001` wording without exception language.

Tradeoff:
- Highest literal strictness, but risks treating TLS infrastructure behavior as policy violation even when required to validate allowlisted Anthropic TLS sessions.

### Option B: Add bounded infrastructure TLS carve-out (recommended)
Amend `REQ-NET-001` with narrow exception language for certificate-validation infrastructure traffic that is required for allowlisted Anthropic TLS sessions.

Tradeoff:
- Preserves enforceable Anthropic-only policy while removing operational contradiction.

### Option C: Defer wording decision
Keep `CONF-002` unresolved and continue treating it as review caveat.

Tradeoff:
- Avoids immediate normative change but leaves acceptance interpretation ambiguous.

## Recommended Disposition

Adopt **Option B**.

### Proposed Normative Text (for `REQ-NET-001`)

"The application MUST NOT initiate outbound connections to non-allowlisted endpoints at runtime, except infrastructure TLS certificate-validation traffic strictly required to establish or validate trust for allowlisted Anthropic API sessions (for example OCSP/CRL/AIA retrieval by platform TLS components). This exception does not authorize application payload exchange with non-allowlisted endpoints."

### Proposed Verification Interpretation Addendum

For DEL-03-06 pass/fail analysis:
1. Non-allowlisted application payload traffic remains a hard failure.
2. Observed certificate-validation infrastructure traffic tied to allowlisted Anthropic TLS sessions is classified as `INFRA_TLS_EXCEPTION` (not a policy failure).
3. Any such classification must be explicitly recorded in proof artifacts.

## Proposed Human Ruling Text

"For DEL-03-06 CONF-002, adopt a bounded infrastructure TLS exception in REQ-NET-001: certificate-validation traffic required for allowlisted Anthropic TLS sessions is permitted, while all non-allowlisted application payload traffic remains prohibited."

## Decision Outcome

- **Status:** APPROVED (2026-02-24)
- **Selected option:** Option B (bounded infrastructure TLS carve-out)
- **Approval evidence (in-session human statements):**
  1. "Approve CONF-002 Option B disposition text."
  2. "Approve IN_PROGRESS -> CHECKING for DEL-03-06."
- **Applied this cycle:** Normative wording was propagated to `Specification.md` (`REQ-NET-001`), `Guidance.md` (Conflict Table `CONF-002`), and `Datasheet.md` (OCSP/CRL condition).
- **Next action:** Carry this approved disposition as the active interpretation for DEL-03-06 `CHECKING` review and final issuance gate evidence.
