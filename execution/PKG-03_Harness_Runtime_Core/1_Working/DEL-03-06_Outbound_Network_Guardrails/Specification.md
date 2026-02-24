# Specification — DEL-03-06 Outbound Network Guardrails (Anthropic-only) + Verification

## Scope

### Included

- Define and enforce an outbound network policy that permits only Anthropic API traffic from the Chirality desktop application at runtime.
- Audit and mitigate all default outbound network behavior in the Electron shell, Chromium renderer, Next.js runtime, and any bundled SDKs.
- Provide verification evidence (tests, audit artifacts, documentation) that the policy holds.

**Source:** Decomposition DEL-03-06; DEC-NET-001; SOW-006.

### Excluded

- Build-time network access (npm install, Electron builder downloads) -- **ASSUMPTION: build-time network is out of scope for runtime guardrails.**
- API key provisioning and storage contract (covered by DEL-03-05).
- Anthropic API integration logic beyond egress policy enforcement (covered by DEL-03-05).
- External system integration of any kind other than Anthropic API (SOW-043 OUT; DEC-NET-001 exception).

---

## Requirements

### REQ-NET-001: Anthropic-Only Outbound Policy

The application MUST NOT initiate outbound connections to non-allowlisted endpoints at runtime, except infrastructure TLS certificate-validation traffic strictly required to establish or validate trust for allowlisted Anthropic API sessions (for example OCSP/CRL/AIA retrieval by platform TLS components). This exception does not authorize application payload exchange with non-allowlisted endpoints.

- **Source:** Decomposition DEC-NET-001 (Human ruling, Gate 3).
- **Acceptance:** Outbound application payload connections are limited to Anthropic API only (no non-allowlisted payload endpoints). Infrastructure TLS certificate-validation traffic required for allowlisted Anthropic TLS sessions is permitted and must be classified as `INFRA_TLS_EXCEPTION`.
- **Note (C-001):** CONF-002 is resolved (2026-02-24): Option B bounded infrastructure TLS carve-out approved and recorded in `CONF-002_Disposition_Decision_Input_2026-02-24.md`.
- **Observation window (F-001):** The proof of conformance requires a defined observation window and sample size. OI-002 (2026-02-23) set the baseline to 3 independent runs with a minimum 10-minute idle window included in each run.

### REQ-NET-002: Electron Auto-Update Disabled

The Electron auto-update mechanism (Squirrel / electron-updater) MUST be disabled or blocked so that no update-check traffic leaves the application.

- **Source:** DEC-NET-001 -- "No ... update checks."
- **Acceptance:** No outbound connections to update servers observed during runtime verification.

### REQ-NET-003: Telemetry Disabled

All telemetry, crash reporting, and analytics endpoints MUST be disabled or blocked. This includes Electron/Chromium default telemetry, any Next.js telemetry, and any SDK-level telemetry.

- **Source:** DEC-NET-001 -- "No telemetry."
- **Acceptance:** No outbound connections to telemetry endpoints observed during runtime verification.

### REQ-NET-004: Chromium Renderer Outbound Restricted

Chromium renderer-process outbound behavior (DNS prefetch, safe browsing, component updates, spell-check downloads, etc.) MUST be audited and non-essential outbound connections disabled.

- **Source:** DEC-NET-001 (implied); Decomposition DEL-03-06 ContextEnvelopeNotes -- "Touches multiple runtime surfaces (Electron shell ...)."
- **ASSUMPTION:** Chromium-level network behavior is in-scope for the egress audit because the Electron shell hosts the renderer.
- **Acceptance (A-003):** All identified Chromium renderer outbound behaviors are either disabled via configuration/flags or documented as infrastructure exceptions (per CONF-002 ruling). No non-essential renderer-originated outbound connections observed during runtime verification.

### REQ-NET-005: Enforcement Mechanism

The enforcement mechanism (allowlist, proxy, OS-level firewall rule, CSP, or combination) MUST be defined and implemented. The enforcement mechanism MUST cover both the Electron main process and the renderer process. If any process cannot be covered, the gap MUST be documented with rationale (see X-003).

- **Source:** Decomposition OI-002.
- **Status:** RESOLVED (2026-02-23 human ruling selected Option B layered enforcement).
- **Acceptance template (A-001):** Once OI-002 is resolved, acceptance criteria will follow this structure:
  1. The selected enforcement mechanism is implemented and active at runtime.
  2. The mechanism references the canonical domain allowlist (REQ-NET-007).
  3. Connections to non-allowlisted destinations are blocked (verified per REQ-NET-006).
  4. Coverage scope (main process, renderer process, or both) is documented.
  5. Blocked connections produce logged warnings/errors (per REQ-NET-008).

> **Dependency note (A-002):** OI-002 was the central blocking dependency for this requirement and REQ-NET-006. Human ruling on 2026-02-23 selected Option B layered enforcement + repeatable capture proof standard, unblocking Procedure Steps 4-5. Remaining work is implementation completion and proof artifact capture.

### REQ-NET-005a: Content Security Policy Consideration

If the enforcement mechanism includes a layered approach (per Guidance P1), Content Security Policy (CSP) `connect-src` restriction SHOULD be evaluated as a candidate layer for renderer-process coverage.

- **Source:** Guidance C4 trade-off analysis; Guidance P1 (defense in depth).
- **Status:** TBD -- depends on OI-002 ruling and whether CSP is selected as part of the enforcement combination.
- **ASSUMPTION (X-001):** CSP is a candidate, not a mandated layer. This sub-requirement exists to ensure CSP is evaluated; it does not mandate CSP adoption.

### REQ-NET-006: Verification Evidence

Verification evidence MUST demonstrate that only Anthropic API traffic is observed during representative application usage scenarios.

- **Source:** Decomposition OBJ-002 acceptance criteria; OBJ-006 (validation posture).
- **Status:** RESOLVED (2026-02-23 human ruling selected Option B proof standard).
- **Pass/fail criteria (X-004):**
  - Execute at least 3 independent traffic-capture runs over required scenarios.
  - Pass if no non-allowlisted outbound traffic is observed, except explicitly accepted infrastructure TLS exceptions per approved CONF-002 Option B disposition (2026-02-24).
  - Blocked outbound attempts MUST be observable via runtime diagnostics/logs (REQ-NET-008).
- **Scenario coverage (A-004):** Regardless of OI-002 outcome, verification MUST cover at minimum the following usage scenarios (from Procedure Step 5.2):
  1. Application startup (cold start)
  2. Session boot with `projectRoot` binding
  3. Turn execution with Anthropic API call
  4. Idle period (minimum observation window: TBD -- see X-005)
  5. Application shutdown

### REQ-NET-007: Anthropic API Domain Resolution

The set of permitted Anthropic API domains/endpoints MUST be explicitly enumerated in configuration or code, not implicitly derived.

- **ASSUMPTION:** An explicit allowlist is the minimum viable enforcement posture. This assumption holds regardless of OI-002 outcome.
- **Acceptance:** A documented, auditable list of permitted Anthropic API domains exists in the codebase.

### REQ-NET-008: Graceful Failure on Blocked Egress

If the enforcement mechanism blocks an outbound connection attempt, the application MUST NOT crash. Blocked connections SHOULD produce a logged warning or error; they MUST NOT silently succeed.

- **ASSUMPTION:** Graceful degradation is required for a SECURITY_CONTROL deliverable. Derived from general robustness expectations; not explicitly stated in sources. See Guidance P4 for expanded rationale specific to this deliverable's context.

---

## Standards

| Standard / Governance | Relevance | Accessibility |
|----------------------|-----------|---------------|
| DEC-NET-001 (Human ruling, Gate 3) | Primary policy decision: Anthropic-only outbound | Decomposition (accessible) |
| DIRECTIVE Section 4.2 (Out of Scope) | External system integration boundary | `docs/DIRECTIVE.md` (accessible) |
| CONTRACT K-GHOST-1 | No ghost inputs; sealed context | `docs/CONTRACT.md` (accessible) |
| Electron security documentation | Chromium/Electron default network behavior, command-line flags for disabling outbound features | **location TBD** (external) — C-002: concrete version-matched URL or document identifier needed; must match the Electron version recorded in Datasheet |
| Anthropic API documentation | Canonical API endpoint domains for allowlist validation | **location TBD** (external) — E-001: needed to validate domain allowlist (REQ-NET-007); should be captured in `_REFERENCES.md` once identified |

---

## Verification

| Requirement | Verification Approach | Status |
|-------------|----------------------|--------|
| REQ-NET-001 | Network traffic capture during representative usage; confirm only Anthropic API traffic (observation window per F-001) | PASS (3 independent Option B runs completed in `Evidence/OI-002_PROOF_OPTIONB_2026-02-23_PASS6/`; non-allowlisted probe host blocked in all runs; no non-allowlisted outbound TCP endpoints recorded in run summaries) |
| REQ-NET-002 | Inspect Electron configuration for auto-update disabled; network capture confirms no update traffic | PASS (no `autoUpdater`/release-check paths in main process guard test + no update endpoints observed across proof runs) |
| REQ-NET-003 | Inspect telemetry configuration; network capture confirms no telemetry traffic | PASS (`NEXT_TELEMETRY_DISABLED=1` enforced in build/dev scripts and no telemetry endpoints observed across proof runs) |
| REQ-NET-004 | Audit Chromium flags/settings; network capture confirms no renderer-originated non-Anthropic traffic | IN_PROGRESS (renderer interception layer is active and blocks non-allowlisted host probes; version-specific Chromium flag inventory remains open) |
| REQ-NET-005 | Review enforcement mechanism implementation; confirm it matches Option B layered approach and covers documented process scope | PASS (provider base-URL guardrails + Electron `session.webRequest` egress interception are implemented and exercised in proof runs) |
| REQ-NET-005a | Evaluate CSP `connect-src` as candidate layer; document adoption/rejection rationale | TBD |
| REQ-NET-006 | Verification artifacts (test logs, network captures, audit report) reviewed and accepted by human; pass/fail per X-004 criteria | PASS (run bundle + `OI-002_OptionB_Proof_Report_2026-02-23.md` captured with aggregate `passed=true`) |
| REQ-NET-007 | Code review: explicit allowlist exists and is used by enforcement mechanism | PASS (explicit allowlists in `frontend/electron/main.ts` and `frontend/src/lib/harness/anthropic-agent-sdk-manager.ts`) |
| REQ-NET-008 | Test: simulate blocked egress; confirm no crash and logged error | PASS (blocked egress diagnostics observed in all three proof runs and regression test guard remains green) |
| SDK network behavior (D-003) | Audit Anthropic SDK for non-API network calls (telemetry, analytics); confirm SDK communicates only with configured `baseURL` | IN_PROGRESS (baseURL validation and allowlist enforcement are active; external SDK telemetry audit references remain pending in `_REFERENCES.md`) |

---

## Documentation

### Required Artifacts (from Anticipated Artifacts: CODE/TEST/DOC)

| Artifact | Description | Status |
|----------|-------------|--------|
| Egress policy implementation (CODE) | Code changes to enforce Anthropic-only outbound | PASS (`frontend/src/lib/harness/anthropic-agent-sdk-manager.ts`, `frontend/electron/main.ts`) |
| Electron configuration hardening (CODE) | Disabled auto-update, telemetry, Chromium flags | IN_PROGRESS (auto-update/telemetry controls are in place; version-specific Chromium flag hardening inventory remains open) |
| Anthropic API domain allowlist (CODE/DOC) | Explicit enumeration of permitted domains | PASS (`api.anthropic.com` allowlist is explicit in runtime policy layers) |
| Verification test suite (TEST) | Automated tests for egress policy enforcement | PASS (`frontend/src/__tests__/scripts/build-network-policy.test.ts` + proof-run harness) |
| Network audit procedure / results (DOC) | Documented procedure and captured results demonstrating policy compliance | PASS (`Evidence/OI-002_PROOF_OPTIONB_2026-02-23_PASS6/` + `OI-002_OptionB_Proof_Report_2026-02-23.md`) |
| Enforcement mechanism rationale (DOC) | Record of human ruling on OI-002 and implementation rationale | PASS (`OI-002_Enforcement_Proof_Decision_Input_2026-02-23.md` + proof report) |
