# Guidance — DEL-03-06 Outbound Network Guardrails (Anthropic-only) + Verification

## Purpose

This deliverable exists to enforce the founding constraint that the Chirality desktop application has **no outbound network connections except to Anthropic API endpoints** (DEC-NET-001). The policy is a deliberate boundary: external integrations are out of scope (DIRECTIVE Section 4.2; SOW-043 OUT), and the Anthropic API is the sole exception granted by human ruling at Gate 3.

The deliverable is classified as a SECURITY_CONTROL because it enforces a trust boundary. Outbound network behavior is a significant attack and data-leakage surface in Electron applications, and an unaudited default configuration could silently violate the stated policy.

---

## Principles

### P1: Defense in Depth (Multiple Enforcement Layers)

A single enforcement point (e.g., only an allowlist in the HTTP client) is insufficient for an Electron application. Electron applications have multiple outbound paths:

- **Main process:** Node.js `http`/`https`, `net`, Electron APIs (`autoUpdater`, `crashReporter`).
- **Renderer process:** Chromium network stack (DNS prefetch, safe browsing, component updates, spell-check, etc.).
- **SDK-level:** Anthropic SDK or any transitive dependency making network calls.

A robust implementation should layer enforcement: (a) disable unnecessary features at configuration level, (b) restrict allowed destinations at the HTTP/network level, and (c) verify with runtime observation.

**Decision update (2026-02-23):** OI-002 selected Option B layered enforcement; defense-in-depth is now the active enforcement posture for this deliverable.

### P2: Explicit Allowlist Over Implicit Deny

The policy is narrow (permit Anthropic API only), so it is more natural and auditable to maintain an explicit allowlist of permitted domains than to maintain a blocklist of everything else. An allowlist approach means:

- New endpoints are blocked by default until explicitly added.
- The allowlist is auditable in code review and version control.
- The burden of proof is on additions, not omissions.

**Maintenance implication:** The allowlist must be maintained over time. If Anthropic introduces new API domains or deprecates existing ones, the allowlist update is an explicit, reviewable change. No document currently defines the maintenance process owner or update cadence -- this should be established when the enforcement mechanism is implemented (see Datasheet Conditions, E-003).

### P3: Separation of Policy and Provider

The outbound network policy (what is allowed) should be separable from the Anthropic API provider integration (how to call the API). DEL-03-05 owns the provider integration; DEL-03-06 owns the egress policy. This separation means:

- If the Anthropic API domain changes, the allowlist update is an explicit, reviewable change.
- The enforcement mechanism does not need to understand API semantics -- only domain-level filtering.

### P4: Graceful Degradation on Blocked Egress

If the enforcement mechanism blocks an outbound connection, the application must not crash. A security control that causes operational failure on policy enforcement is counterproductive -- it incentivizes disabling the control. Blocked connections should produce a logged warning or error, and must not silently succeed (silent success would defeat the purpose of enforcement).

**Rationale specific to this deliverable (F-002):** In the context of outbound network guardrails for a SECURITY_CONTROL deliverable, graceful failure is especially important because:

1. **False positives are possible:** During development and as the Electron/SDK ecosystem evolves, new outbound behaviors may emerge that the enforcement mechanism blocks unexpectedly. If blocking causes crashes, developers are incentivized to weaken or disable the guard.
2. **Diagnostic observability:** Logged warnings on blocked connections serve as a secondary detection mechanism -- they reveal attempted policy violations that can be investigated and addressed (either by updating the allowlist if the connection is legitimate, or by tracing the source if it is not).
3. **User-facing stability:** The Chirality application is a desktop tool; runtime crashes erode user trust and are disproportionately costly compared to a logged warning.

**ASSUMPTION:** This principle is derived from general security-control design practice applied to the specific SECURITY_CONTROL classification of this deliverable; not explicitly stated in decomposition sources.

### P5: Verification as a First-Class Artifact

Proving that the policy holds is as important as implementing it. The verification evidence (network captures, test results, audit documentation) is a required artifact, not an afterthought. OI-002 selected a three-run capture proof standard, and the deliverable must produce evidence to that standard.

**Execution update (2026-02-23 PASS6):** The 3-run Option B proof set is now captured under `Evidence/OI-002_PROOF_OPTIONB_2026-02-23_PASS6/` and summarized in `OI-002_OptionB_Proof_Report_2026-02-23.md`.

---

## Considerations

### C1: Electron / Chromium Default Outbound Behavior

Electron applications inherit Chromium's default network behaviors. Known categories include:

- **Auto-update:** Squirrel (macOS) or electron-updater polling for updates.
- **Crash reporting:** Electron `crashReporter` may send minidumps to a configured URL.
- **Chromium component updates:** Background downloads of components (CRLSets, etc.).
- **Safe Browsing:** Google Safe Browsing lookups.
- **Spell-check:** Dictionary downloads.
- **DNS prefetch / preconnect:** Speculative connections from renderer.
- **Certificate transparency / OCSP:** Certificate validation network calls.

Each of these must be audited. Some can be disabled via Electron/Chromium command-line flags or configuration; others may require explicit suppression.

**Candidate Chromium flags (A-005):** The following are known candidate flags for disabling outbound behavior in Chromium-based applications. Exact flag availability and names are version-dependent and must be verified against the project's Electron version (recorded in Datasheet):

| Category | Candidate Flag(s) | Notes |
|----------|-------------------|-------|
| Safe Browsing | `--disable-features=SafeBrowsing` or `--safebrowsing-disable-auto-update` | Evaluated during CHECKING closure; not adopted for baseline because session-level renderer egress interception already fail-closes non-allowlisted traffic. |
| Component Updates | `--disable-component-update` | Evaluated during CHECKING closure; revisit if Electron version upgrade introduces new observed outbound class. |
| DNS Prefetch | `--dns-prefetch-disable` | Evaluated during CHECKING closure; current proof evidence did not show non-allowlisted renderer egress requiring additional flag controls. |
| Spell-check Downloads | `--disable-features=SpellcheckService` or renderer preference | Evaluated during CHECKING closure; no additional baseline flag required under active Option B posture. |
| Background Networking | `--disable-background-networking` | Evaluated during CHECKING closure; deferred for baseline due broad side-effect surface relative to observed risk profile. |

**CHECKING closure update (2026-02-24):** Candidate flags were explicitly evaluated and documented in `REQ-NET-004_005a_SDK_REFERENCE_CLOSURE_2026-02-24.md`. Current baseline relies on validated session-level renderer egress interception plus proof evidence; flag decisions remain version-sensitive and are revisited on Electron upgrades.

### C2: Next.js Telemetry

Next.js includes opt-in telemetry (`next telemetry`). It is typically disabled by setting the `NEXT_TELEMETRY_DISABLED=1` environment variable or by running `npx next telemetry disable`. This should be confirmed for both development and production builds.

**Verification update:** `NEXT_TELEMETRY_DISABLED=1` is enforced in `frontend/package.json` development/build scripts and guarded by `frontend/src/__tests__/scripts/build-network-policy.test.ts`.

### C3: Anthropic SDK Network Behavior

The Anthropic TypeScript SDK communicates with `api.anthropic.com` (or a configured `baseURL`).

**Verification update (2026-02-24):** SDK external-reference capture is complete for this cycle. Installed package metadata and client source (`frontend/node_modules/@anthropic-ai/sdk/package.json`, `client.mjs`) were audited, and closure findings are recorded in `REQ-NET-004_005a_SDK_REFERENCE_CLOSURE_2026-02-24.md`.

### C4: OI-002 Decision Outcome — Enforcement and Verification Method

OI-002 is resolved (2026-02-23). Option B layered enforcement + repeatable capture proof is selected. Candidate approaches considered during decision intake were:

| Approach | Pros | Cons |
|----------|------|------|
| **Electron session.webRequest allowlist** | In-process; works for renderer; configurable | Does not cover main-process Node.js calls |
| **Node.js HTTP agent override / global fetch hook** | Covers main-process calls | Fragile; may miss native modules; version-dependent |
| **CSP (Content Security Policy) headers** | Standard web security mechanism; covers renderer `connect-src` | Does not cover main-process; limited to HTTP |
| **OS-level packet filter (pf on macOS)** | Strong external enforcement | Requires root/admin; hard to ship as part of app |
| **Proxy (localhost MITM)** | Covers all traffic | Operational complexity; certificate management |
| **Combination: config hardening + allowlist + network capture verification** | Layered; pragmatic | Relies on audit discipline, not runtime enforcement of all paths |

Selected outcome: Option B combination (`session.webRequest` renderer egress allowlist + provider guardrails + telemetry/update disable posture + fail-closed diagnostics), followed by three independent traffic-capture runs across startup/session boot/turn/10-minute idle/shutdown.

Completion status: verification runbook execution is complete for this cycle (`aggregate PASS` in `Evidence/OI-002_PROOF_OPTIONB_2026-02-23_PASS6/summary.json`).

### C5: Relationship to DEL-03-05 (Anthropic Provider Integration)

DEL-03-05 owns the Anthropic API provider integration and key provisioning contract. DEL-03-06 owns the egress boundary. The interface between them is:

- DEL-03-06 provides the permitted domain list.
- DEL-03-05 uses that domain list (or is validated against it).
- If DEL-03-05 introduces a new endpoint (e.g., a different Anthropic service), DEL-03-06's allowlist must be updated.

**Coordination protocol (E-002):** The following coordination mechanisms are TBD and should be defined when both deliverables are in active implementation:

| Aspect | Mechanism | Status |
|--------|-----------|--------|
| Domain list synchronization | TBD -- who initiates updates when DEL-03-05 adds a new endpoint? | TBD |
| Conflict resolution | TBD -- what happens if DEL-03-05 requires a domain that DEL-03-06's enforcement blocks? | TBD |
| Change notification | TBD -- how does DEL-03-05 notify DEL-03-06 of endpoint changes? | TBD |
| Validation gate | TBD -- is there a cross-deliverable check that the domain list matches actual SDK usage? | TBD |

This is a **coordination dependency** that should be tracked once dependency extraction runs.

### C6: Procedure Step Ordering Rationale (D-002)

The Procedure steps follow a deliberate sequence:

1. **Audit first (Step 1)** -- establish a complete inventory of outbound surfaces before making changes. This prevents "whack-a-mole" hardening that misses surfaces.
2. **Define allowlist (Step 2)** -- the allowlist is needed before enforcement can be implemented, and should be confirmed against the audit findings and DEL-03-05.
3. **Configuration hardening (Step 3)** -- disable known unnecessary outbound features. This is baseline hygiene independent of enforcement method.
4. **Enforcement mechanism (Step 4)** -- implement the selected enforcement approach (Option B).
5. **Verification evidence (Step 5)** -- capture proof after enforcement is in place. Verification is meaningless before the enforcement mechanism is active.
6. **Automated tests (Step 6)** -- encode verification as repeatable tests. Follows from having a known-good enforcement state.
7. **Document and close (Step 7)** -- final documentation aggregates all prior artifacts.

Reordering risks: performing hardening before audit may miss surfaces; performing verification before enforcement produces incomplete evidence; implementing enforcement before the allowlist is defined creates a risk of blocking legitimate traffic.

---

## Trade-offs

| Decision Point | Option A | Option B | Recommendation |
|---------------|----------|----------|----------------|
| Enforcement granularity | Domain-level allowlist (simple, auditable) | URL-path-level allowlist (more precise, harder to maintain) | Domain-level is sufficient for Anthropic-only policy -- **ASSUMPTION** |
| Build-time vs. runtime scope | Include build-time telemetry (npm, Electron builder) | Runtime-only (this deliverable) | Runtime-only: build-time is developer-environment, not user-facing -- **ASSUMPTION** |
| Certificate validation traffic | Allow OCSP/CRL traffic (required for TLS) | Block all non-Anthropic (breaks TLS verification) | Allow: blocking OCSP/CRL would break TLS for the permitted Anthropic connection -- **ASSUMPTION** |

---

## Residual Risk / Known Limitations (F-004)

The following risks may persist even after full implementation of the outbound network guardrails. This section seeds the "Known limitations or residual risk items" artifact required by Procedure Step 7.1.

| Risk ID | Risk | Mitigation Status | Notes |
|---------|------|-------------------|-------|
| RR-001 | **DNS-level data exfiltration** — Malicious code could encode data in DNS queries to arbitrary domains; domain-level allowlisting does not inspect DNS payload | TBD | Mitigation would require DNS-level filtering or monitoring, which is outside the current scope. **ASSUMPTION: this risk is accepted at the application level.** |
| RR-002 | **Native module bypass** — Node.js native modules (N-API / node-gyp compiled) could make raw socket calls that bypass HTTP-level enforcement | TBD | Mitigation depends on whether the enforcement mechanism operates at the network level (OS packet filter) or application level (HTTP hooks). OI-002 ruling affects exposure. |
| RR-003 | **Runtime code injection** — If an attacker can inject code into the Electron process, they can bypass application-level enforcement | TBD | This is a broader security concern beyond egress policy. Defense-in-depth (P1) reduces but does not eliminate this risk. |
| RR-004 | **Electron/Chromium version drift** — Future Electron updates may introduce new outbound behaviors not covered by current hardening flags | TBD | Mitigation: re-audit on Electron version upgrades; maintain version-specific flag documentation. |
| RR-005 | **Transitive dependency phone-home** — A future `npm install` could introduce a dependency that phones home at runtime | TBD | Mitigation: periodic dependency audit (Procedure Step 1.6); consider lock-file integrity checks. |

> **Note:** These are identified risks, not confirmed vulnerabilities. Each should be reviewed during OI-002 implementation follow-through to determine whether Option B addresses or accepts them.

---

## Examples

### Example: Disabling Electron Auto-Update

```javascript
// In Electron main process initialization
// Prevent autoUpdater from checking for updates
const { autoUpdater } = require('electron');
autoUpdater.autoInstallOnAppQuit = false;
// Do not call autoUpdater.checkForUpdates()
```

**ASSUMPTION:** The exact API depends on whether the project uses `electron-updater` (electron-builder) or Electron's built-in `autoUpdater`. The codebase must be audited to determine which is in use.

### Example: Next.js Telemetry Disable

```bash
# In build scripts or environment
export NEXT_TELEMETRY_DISABLED=1
```

**Source:** Next.js telemetry docs `https://nextjs.org/telemetry`.

---

## Conflict Table (status tracking)

| Conflict ID | Conflict | Source A | Source B | Impacted Sections | Proposed Authority | Human Ruling |
|-------------|---------|----------|----------|-------------------|-------------------|--------------|
| CONF-001 | Enforcement mechanism selection gap | DEC-NET-001 (policy stated) | OI-002 (method selection) | Specification REQ-NET-005, REQ-NET-006; Procedure Steps 3-5 | Human ruling on OI-002 | RESOLVED (2026-02-23): Option B selected |
| CONF-002 | Certificate validation traffic (OCSP/CRL) may be non-Anthropic but required for TLS; REQ-NET-001 as written would prohibit it | DEC-NET-001 ("no other endpoints"); Specification REQ-NET-001 | TLS operational requirement | Specification REQ-NET-001; Datasheet Conditions; Trade-offs table | Apply approved Option B disposition text in `CONF-002_Disposition_Decision_Input_2026-02-24.md` (bounded infrastructure TLS carve-out with payload-traffic prohibition retained) | RESOLVED (2026-02-24): Option B approved; bounded infrastructure TLS exception accepted for allowlisted Anthropic TLS sessions |
