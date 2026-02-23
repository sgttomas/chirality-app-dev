# Procedure — DEL-03-06 Outbound Network Guardrails (Anthropic-only) + Verification

## Purpose

This procedure describes the steps to produce and verify the outbound network guardrails for the Chirality desktop application, ensuring only Anthropic API traffic is permitted at runtime.

---

## Prerequisites

| # | Prerequisite | Status | Escalation / Notes |
|---|-------------|--------|-------------------|
| 1 | Access to the Chirality application source code (Electron + Next.js) | TBD | |
| 2 | Human ruling on OI-002 (enforcement mechanism + proof standard) | RESOLVED (2026-02-23): Option B layered enforcement + 3-run capture proof standard selected | Decision artifact: `OI-002_Enforcement_Proof_Decision_Input_2026-02-23.md` |
| 3 | Anthropic API endpoint domain list (canonical, from Anthropic documentation or DEL-03-05) | TBD | Coordinate with DEL-03-05; see Guidance C5 coordination protocol |
| 4 | Knowledge of the Electron version used by the project (record in Datasheet) | TBD | Required for Chromium flag identification (Step 3.4, Guidance C1) |
| 5 | Network traffic capture tooling (e.g., Wireshark, `tcpdump`, mitmproxy, or macOS `nettop`) | TBD | |
| 6 | DEL-03-05 (Anthropic Provider Integration) sufficiently progressed to know which endpoints are called | TBD | Coordination dependency; see Guidance C5 |

---

## Steps

### Step 1: Audit Existing Outbound Behavior

> **Rationale for ordering:** Audit first to establish a complete inventory before making changes. See Guidance C6 for full ordering rationale.

1.1. Identify the Electron version and build configuration in use. Record the version in Datasheet Attributes (see B-002).

**1.1a. Capture pre-hardening network baseline (X-002):** Before any configuration changes, perform a network traffic capture of the application in its default state across the scenarios listed in Step 5.2. This establishes the "before" state for comparison against the post-hardening "after" state in Step 5. Save the baseline capture as a verification artifact.

1.2. Audit the Electron main process for outbound network calls:
- Auto-update mechanism (Squirrel / electron-updater / built-in `autoUpdater`)
- Crash reporter configuration (`crashReporter`)
- Any explicit HTTP/HTTPS calls in main process code
- Protocol handlers that may initiate network requests

1.3. Audit the Chromium renderer configuration:
- DNS prefetch settings
- Safe Browsing settings
- Component update settings
- Spell-check dictionary download settings
- Any `<link rel="preconnect">` or external resource loading in HTML/CSS

1.4. Audit the Next.js runtime:
- Telemetry configuration (`NEXT_TELEMETRY_DISABLED`)
- Any server-side API routes that make outbound calls (beyond Anthropic API)
- Middleware or plugins with network behavior

1.5. Audit the Anthropic SDK:
- Confirm endpoints called (expected: `api.anthropic.com` or configured `baseURL`)
- Check for telemetry, analytics, or non-API network calls in the SDK
- Record findings for Specification Verification table (D-003)

1.6. Audit transitive dependencies:
- Review `node_modules` for packages known to phone home (analytics, error reporting, etc.)
- **Scope boundary (C-003):** The audit should cover at minimum the following known categories of phone-home behavior in npm packages:
  1. Analytics/telemetry libraries (e.g., packages with `telemetry`, `analytics`, `tracking` in name or description)
  2. Error/crash reporting libraries (e.g., Sentry, Bugsnag, Rollbar integrations)
  3. Auto-update/version-check libraries beyond Electron's own
  4. License validation libraries that call home
  5. Font/asset download libraries that fetch from CDNs at runtime
- **ASSUMPTION:** A full transitive dependency audit beyond these known categories is best-effort. The audit scope should be documented so that adequacy can be assessed. See Guidance Residual Risk RR-005.

1.7. Document findings in an audit report artifact.

**Verification:** Audit report exists, catalogs all discovered outbound network surfaces, and includes the pre-hardening baseline capture.

---

### Step 2: Define Anthropic API Domain Allowlist

2.1. Enumerate the Anthropic API domains used by the application. Expected:
- `api.anthropic.com`
- TBD (confirm if additional domains are used, e.g., for streaming, or beta endpoints)

2.2. Record the allowlist in a configuration file or code constant that is:
- Auditable in version control
- Referenced by the enforcement mechanism (Step 4)

2.3. Coordinate with DEL-03-05 to confirm the domain list is complete (see Guidance C5 coordination protocol).

**Verification:** Allowlist is documented, committed, and confirmed against DEL-03-05.

---

### Step 3: Implement Configuration Hardening

*This step can proceed before OI-002 ruling; it is baseline hygiene.*

> **Rationale for ordering:** Configuration hardening before enforcement mechanism because it is independent of OI-002. See Guidance C6.

3.1. Disable Electron auto-update:
- Remove or disable `autoUpdater.checkForUpdates()` calls
- Set appropriate Electron/electron-builder configuration to prevent update polling

3.2. Disable crash reporter (or ensure it does not send outbound):
- Remove `crashReporter.start()` calls or set to a non-functional endpoint
- Confirm no outbound traffic from crash reporter

3.3. Disable Next.js telemetry:
- Set `NEXT_TELEMETRY_DISABLED=1` in production environment
- Confirm via build output

3.4. Harden Chromium flags (as applicable per Electron version):

> **Reference:** See Guidance C1 candidate flags table for known candidates. All flags below are TBD pending verification against the project's Electron version (Prerequisite 4).

- Disable safe browsing: TBD (candidate: `--disable-features=SafeBrowsing` — verify against Electron version)
- Disable component updates: TBD (candidate: `--disable-component-update` — verify against Electron version)
- Disable DNS prefetch: TBD (candidate: `--dns-prefetch-disable` — verify against Electron version)
- Disable spell-check downloads: TBD (candidate: `--disable-features=SpellcheckService` — verify against Electron version)
- Disable background networking: TBD (candidate: `--disable-background-networking` — verify against Electron version; may have broad effects)

3.5. Confirm Anthropic SDK has no non-API outbound calls (from Step 1.5 audit). Record SDK verification findings for the Specification Verification table (D-003).

**Verification:** Each hardening change is committed and linked to the audit finding it addresses.

---

### Step 4: Implement Enforcement Mechanism

4.1. Implement the enforcement mechanism selected by human ruling on OI-002.

4.2. Candidate approaches (see Guidance C4 for trade-off analysis):
- Electron `session.webRequest` allowlist
- Node.js HTTP agent override
- Content Security Policy (CSP) `connect-src` restriction (see Specification REQ-NET-005a)
- OS-level packet filter rule
- Combination approach

4.3. Ensure the enforcement mechanism:
- References the allowlist from Step 2
- Covers both main process and renderer process. If any process cannot be covered by the selected enforcement mechanism, document the gap with rationale per Specification REQ-NET-005 (X-003). Partial coverage MUST be justified and compensated by other layers per Guidance P1.
- Handles blocked connections gracefully (no crash; logged warning/error per REQ-NET-008)

**Verification:** Enforcement mechanism implemented and passes unit tests for allowed and blocked connections.

---

### Step 5: Produce Verification Evidence

5.1. Execute the verification test plan per selected OI-002 proof standard (Option B). The pass/fail criteria must align with Specification REQ-NET-006 (X-004).

5.2. Execute representative application usage scenarios while capturing network traffic:
- Application startup (cold start)
- Session boot with `projectRoot` binding
- Turn execution with Anthropic API call
- Idle period (check for background polling) — **minimum observation window: 10 minutes** (as selected in OI-002 ruling)
- Application shutdown

5.3. Analyze captured traffic:
- Confirm all observed outbound connections are to allowlisted Anthropic API domains
- Confirm no connections to update, telemetry, or other endpoints
- Note any infrastructure traffic (OCSP/CRL) and classify per CONF-002 ruling
- **Compare against pre-hardening baseline** from Step 1.1a to confirm that previously-observed non-Anthropic traffic has been eliminated

5.4. Document results in the verification artifact.

**Verification:** Traffic capture analyzed; results documented; no policy violations found; comparison against baseline demonstrates improvement.

---

### Step 6: Implement Automated Tests

6.1. Create automated tests that verify:
- Auto-update is disabled (configuration test)
- Telemetry is disabled (configuration/environment test)
- Allowlist exists and contains only expected domains (unit test)
- Enforcement mechanism blocks non-allowlisted domains (integration test per REQ-NET-008)
- Enforcement mechanism permits Anthropic API domains (integration test)
- Anthropic SDK does not make non-API network calls (D-003 verification)

6.2. Integrate tests into the project's validation suite (linkage to DEL-07-01 / SOW-028).

**Verification:** Test suite passes; tests are repeatable in CI environment.

---

### Step 7: Document and Close

7.1. Produce final documentation artifacts:
- Egress policy summary (what is allowed, what is blocked, how)
- Enforcement mechanism description and rationale (including OI-002 ruling record)
- Verification results summary
- Known limitations or residual risk items (seeded by Guidance Residual Risk section, F-004)

7.2. Update deliverable status per lifecycle rules.

**Verification:** All required artifacts (CODE/TEST/DOC) exist and are committed.

---

## Verification Summary

| Step | Verification Check |
|------|--------------------|
| Step 1 | Audit report exists, is complete, and includes pre-hardening baseline capture (X-002) |
| Step 2 | Allowlist documented and confirmed with DEL-03-05 |
| Step 3 | Configuration hardening changes committed |
| Step 4 | Enforcement mechanism implemented and unit-tested |
| Step 5 | Network traffic verification evidence produced with baseline comparison |
| Step 6 | Automated test suite passes |
| Step 7 | All CODE/TEST/DOC artifacts committed |

---

## Records

| Record | Description | Location |
|--------|-------------|----------|
| Pre-hardening network baseline | Network capture of default application behavior before any changes | TBD (deliverable folder or linked artifact) |
| Outbound network audit report | Catalog of all outbound surfaces and findings | TBD (deliverable folder or linked artifact) |
| Anthropic API domain allowlist | Explicit list of permitted domains | TBD (source code configuration) |
| OI-002 ruling record | Human decision on enforcement mechanism + proof standard | Deliverable-local decision artifact (for example `OI-002_Enforcement_Proof_Decision_Input_YYYY-MM-DD.md`) plus `MEMORY.md` continuity entry |
| Network traffic capture / analysis | Raw capture + analysis summary from verification | TBD (deliverable folder or linked artifact) |
| Automated test results | Test suite output | TBD (CI artifacts or local test output) |
| Residual risk register | Known limitations persisting after implementation | Guidance Residual Risk section (F-004); final version in Step 7.1 DOC artifact |
