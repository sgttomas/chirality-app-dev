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

The application MUST NOT initiate outbound network connections to any endpoint other than Anthropic API endpoints at runtime.

- **Source:** Decomposition DEC-NET-001 (Human ruling, Gate 3).
- **Acceptance:** Outbound network connections are limited to Anthropic API only (no other endpoints). (Decomposition OBJ-002 acceptance criteria.)
- **Note (C-001):** Certificate validation traffic (OCSP/CRL) to non-Anthropic endpoints may be operationally required for TLS. This creates a tension with the literal text of this requirement. See CONF-002 in Guidance Conflict Table. **PROPOSAL: Amend REQ-NET-001 to explicitly carve out infrastructure TLS traffic, pending human ruling on CONF-002.**
- **Observation window (F-001):** The proof of conformance requires a defined observation window and sample size. TBD -- the acceptance criteria should specify whether "zero non-Anthropic connections" means zero in a single test run, across N runs, or under continuous monitoring. **ASSUMPTION: observation parameters will be defined as part of the OI-002 ruling on proof standard.**

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
- **Status:** TBD -- human ruling required to select enforcement mechanism.
- **Acceptance template (A-001):** Once OI-002 is resolved, acceptance criteria will follow this structure:
  1. The selected enforcement mechanism is implemented and active at runtime.
  2. The mechanism references the canonical domain allowlist (REQ-NET-007).
  3. Connections to non-allowlisted destinations are blocked (verified per REQ-NET-006).
  4. Coverage scope (main process, renderer process, or both) is documented.
  5. Blocked connections produce logged warnings/errors (per REQ-NET-008).

> **Open dependency (A-002):** OI-002 resolution is the central blocking dependency for this requirement and REQ-NET-006. No resolution path or target date is currently recorded. The human ruling on OI-002 determines the enforcement mechanism selection, the proof standard, and unblocks Procedure Steps 4-5. See Procedure Prerequisites for escalation tracking.

### REQ-NET-005a: Content Security Policy Consideration

If the enforcement mechanism includes a layered approach (per Guidance P1), Content Security Policy (CSP) `connect-src` restriction SHOULD be evaluated as a candidate layer for renderer-process coverage.

- **Source:** Guidance C4 trade-off analysis; Guidance P1 (defense in depth).
- **Status:** TBD -- depends on OI-002 ruling and whether CSP is selected as part of the enforcement combination.
- **ASSUMPTION (X-001):** CSP is a candidate, not a mandated layer. This sub-requirement exists to ensure CSP is evaluated; it does not mandate CSP adoption.

### REQ-NET-006: Verification Evidence

Verification evidence MUST demonstrate that only Anthropic API traffic is observed during representative application usage scenarios.

- **Source:** Decomposition OBJ-002 acceptance criteria; OBJ-006 (validation posture).
- **Status:** TBD -- human ruling required to select proof standard (OI-002).
- **Pass/fail criteria (X-004):** TBD -- the acceptance criteria must define what constitutes a pass or fail. Candidate definitions:
  - **Strict:** Zero non-allowlisted connections observed across all test scenarios (excluding any CONF-002 infrastructure exceptions).
  - **Pragmatic:** No sustained or intentional non-allowlisted connections; infrastructure exceptions (OCSP/CRL) classified and documented.
  - The human ruling on OI-002 should select or refine these criteria.
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
| REQ-NET-001 | Network traffic capture during representative usage; confirm only Anthropic API traffic (observation window per F-001) | TBD (proof standard per OI-002) |
| REQ-NET-002 | Inspect Electron configuration for auto-update disabled; network capture confirms no update traffic | TBD |
| REQ-NET-003 | Inspect telemetry configuration; network capture confirms no telemetry traffic | TBD |
| REQ-NET-004 | Audit Chromium flags/settings; network capture confirms no renderer-originated non-Anthropic traffic | TBD |
| REQ-NET-005 | Review enforcement mechanism implementation; confirm it matches the human-selected approach (OI-002) and covers documented process scope | TBD |
| REQ-NET-005a | Evaluate CSP `connect-src` as candidate layer; document adoption/rejection rationale | TBD |
| REQ-NET-006 | Verification artifacts (test logs, network captures, audit report) reviewed and accepted by human; pass/fail per X-004 criteria | TBD |
| REQ-NET-007 | Code review: explicit allowlist exists and is used by enforcement mechanism | Code review |
| REQ-NET-008 | Test: simulate blocked egress; confirm no crash and logged error | Automated test |
| SDK network behavior (D-003) | Audit Anthropic SDK for non-API network calls (telemetry, analytics); confirm SDK communicates only with configured `baseURL` | Audit + automated test (see Procedure Steps 1.5, 3.5) |

---

## Documentation

### Required Artifacts (from Anticipated Artifacts: CODE/TEST/DOC)

| Artifact | Description | Status |
|----------|-------------|--------|
| Egress policy implementation (CODE) | Code changes to enforce Anthropic-only outbound | TBD |
| Electron configuration hardening (CODE) | Disabled auto-update, telemetry, Chromium flags | TBD |
| Anthropic API domain allowlist (CODE/DOC) | Explicit enumeration of permitted domains | TBD |
| Verification test suite (TEST) | Automated tests for egress policy enforcement | TBD |
| Network audit procedure / results (DOC) | Documented procedure and captured results demonstrating policy compliance | TBD |
| Enforcement mechanism rationale (DOC) | Record of human ruling on OI-002 and implementation rationale | TBD |
