# Guidance — DEL-03-05 Anthropic Provider Integration & Key Provisioning Contract

## Purpose

This deliverable exists to give the Chirality harness runtime the ability to communicate with the Anthropic (Claude) API — the single permitted LLM provider for the system. It also defines the contract for how operators provision and store their API key, ensuring the key remains non-project-truth convenience state per DIRECTIVE Section 2.5.

The deliverable is a prerequisite for any turn execution that involves LLM interaction: without an operational Anthropic provider, the harness cannot execute agent turns.

Source: Decomposition DEL-03-05; DEC-NET-001; SOW-006; OBJ-002.

## Principles

### P1: Single Provider, No Abstraction Layer

The system has a binding decision (DEC-NET-001) that outbound internet is permitted **only** for Anthropic API calls. This means:

- There is no need for a multi-provider abstraction or plugin architecture.
- The provider module can directly use the Anthropic SDK without an intermediate adapter pattern.
- If a future decision changes the permitted providers, that would be a scope change requiring decomposition revision.

This keeps the implementation simple, testable, and auditable.

Source: DEC-NET-001; SOW-043 (external integrations OUT, exception for Anthropic only).

### P2: Key Is Convenience State, Not Project Truth

The Chirality system's foundational principle is "filesystem is the database" (DIRECTIVE Section 2.1). Project truth lives in git-tracked files. The API key explicitly does **not**:

- Belong in the working root (`projectRoot`)
- Belong in git-tracked execution files
- Constitute project state that agents read/write

It is operator convenience state — similar to UI panel preferences or local presets. This means:

- Losing the key does not corrupt project state.
- Different operators on the same project may use different keys.
- The key does not participate in sealing, approvals, or snapshot integrity.

Source: DIRECTIVE Section 2.5; Decomposition DEL-03-05.

### P3: Fail Clearly, Not Silently

When the API key is missing, invalid, or expired, the runtime must communicate this clearly to the operator rather than failing silently or producing confusing errors. The harness session should remain functional (operators can still browse the filesystem, view deliverables, etc.) — only LLM-dependent operations should be blocked with actionable error messages.

Source: **ASSUMPTION: derived from general usability principles and the desktop-first nature of the application.**

### P4: Server-Side Only

The API key and all Anthropic API communication must remain server-side (Next.js API routes or Electron main process). The key must never be exposed to the renderer process or client-side JavaScript.

Source: **ASSUMPTION: standard security practice for API key handling in Electron + Next.js applications.**

## Considerations

### C1: Key Provisioning Mechanism (OI-001 — Resolved 2026-02-23)

Human ruling for this cycle sets `OI-001 = ENV_ONLY`. The baseline contract is:

- Canonical key source: `ANTHROPIC_API_KEY`
- Compatibility alias allowed: `CHIRALITY_ANTHROPIC_API_KEY`
- Out of scope unless re-ruled: macOS Keychain, Electron `safeStorage`, app-local key config persistence

The option trade-offs remain documented for future re-rulings:

| Mechanism | Pros | Cons |
|-----------|------|------|
| **Environment variable** (`ANTHROPIC_API_KEY`) | Simple; standard practice; works in dev and CI; easy to document | Requires terminal/shell knowledge; not discoverable from the UI; may be forgotten across sessions |
| **macOS Keychain** | Secure; persists across sessions; OS-native; no plaintext storage | macOS-only (aligns with DEC-PLAT-001 but limits future portability); requires Keychain access prompts |
| **Electron `safeStorage`** | Cross-platform encrypted storage; integrated with Electron lifecycle | Tied to Electron; encrypted but app-local; less transparent than env var |
| **App settings file** (outside working root) | Discoverable; can be managed through UI settings panel | Plaintext on disk unless additionally encrypted; must be outside working root |
| **UI prompt on first use** | Most discoverable; zero-config for operators | Requires secure in-memory or persisted storage behind it; session-scoped if in-memory only |

**Decision applied:** Environment-variable provisioning is baseline for current scope. Optional persisted storage mechanisms require a new explicit ruling/scope amendment.

### C2: Model Default Strategy

The harness model fallback chain (SPEC Section 9.8) defines: `opts.model` -> global model -> runtime default. For this deliverable:

- The provider module receives a resolved model string from the harness turn pipeline.
- The provider module should validate that the model string corresponds to an available Anthropic model. **ASSUMPTION: validation approach TBD — could be a static allowlist or dynamic API check.**
- If the model is invalid or unavailable, the provider should return a clear error rather than silently falling back.

### C3: Streaming Architecture

The Anthropic SDK supports streaming responses. The provider must bridge between:

- Anthropic SDK streaming (server-side) — produces incremental text/content chunks
- Harness SSE event protocol (client-facing) — delivers events to the UI

The content block formatting approach should be straightforward since both are stream-based, but the event shapes may differ. The provider's streaming adapter translates Anthropic stream events into harness SSE events.

Source: SPEC Section 9.8 (prompt mode selection); SOW-005; SOW-006.

### C4: Relationship to Adjacent Deliverables

| Deliverable | Relationship |
|-------------|-------------|
| DEL-03-02 (Turn Execution + SSE) | This deliverable provides the Anthropic-specific provider that DEL-03-02's turn pipeline calls. DEL-03-02 owns the generic turn execution; DEL-03-05 owns the provider-specific layer. |
| DEL-03-03 (Turn Options + Fallback) | This deliverable consumes the resolved `opts.model` from DEL-03-03's fallback chain. |
| DEL-03-06 (Outbound Network Guardrails) | DEL-03-06 enforces that only Anthropic API calls are permitted. This deliverable implements the Anthropic provider; DEL-03-06 verifies that nothing else calls out. |
| DEL-04-01 (Attachment Resolver) | This deliverable receives pre-processed multimodal content blocks from the attachment resolver and formats them for the Anthropic API. **Scope boundary (C-002):** DEL-04-01 resolves, reads, classifies, and enforces budgets on attachments; DEL-03-05 formats the resulting content blocks into Anthropic API-compatible shapes. |

### C5: Key Rotation and Revocation (B-003)

Key rotation and revocation are not addressed by any available source for this deliverable. The decomposition does not define rotation requirements, and no Anthropic API documentation is accessible to determine API-side rotation behavior.

**Deferral rationale:** The API key is classified as non-project-truth convenience state (P2). Key rotation is an operational concern that depends on:
- The provisioning mechanism selected in OI-001 (e.g., environment variables are rotated differently than Keychain entries).
- Anthropic's key lifecycle policies (external; `location TBD`).

**TBD items for key rotation/revocation:**
- How the operator replaces a compromised or expired key.
- Whether the runtime detects an expired key proactively or only on API failure.
- Whether the UI provides a "re-provision key" flow.

These items should be addressed after OI-001 resolution, when the provisioning mechanism is known.

### C6: Security Considerations (C-004, F-002)

#### Server-Side Constraint Rationale (F-002)

REQ-01 mandates server-side-only initialization. The security reasoning:

- **Electron renderer isolation:** In Electron applications, the renderer process runs web content. Exposing the API key to the renderer would make it accessible to any client-side JavaScript, including potential XSS vectors or compromised dependencies. The main process and Next.js API routes run in a privileged Node.js context with no direct exposure to rendered web content.
- **API key exposure risk:** If the key were available client-side, it could be extracted via browser developer tools, leaked through client-side error reporting, or captured by malicious browser extensions.

Source: **ASSUMPTION: standard Electron security model; see Electron security documentation (`location TBD` — external).**

#### API Key Exposure Attack Vectors

The following attack vectors are relevant to API key handling:

| Vector | Mitigation | Status |
|--------|------------|--------|
| Key in project files / git history | REQ-07 non-project-truth constraint; REQ-07 verification via grep scan | Addressed |
| Key in application logs / console | REQ-09 log protection requirement | Addressed |
| Key in error messages / telemetry | REQ-09 + REQ-06 error handling taxonomy | Addressed |
| Key in renderer process memory | REQ-01 + P4 server-side only constraint | Addressed |
| Key in client-side JavaScript bundles | REQ-01 + P4 server-side only constraint | Addressed |
| Key in inter-process communication | TBD — depends on Electron IPC architecture and whether key material crosses process boundaries | TBD |
| Key in OS-level process memory dumps | Out of scope — OS-level security is beyond this deliverable's control | Out of scope |

#### Credential Leakage Risk Analysis

The primary credential leakage risks are mitigated by REQ-01 (server-side only), REQ-07 (non-project-truth storage), and REQ-09 (log protection). The remaining TBD risk (IPC key exposure) depends on the OI-001 provisioning decision and the Electron IPC architecture used for the harness.

### C7: SDK Update Lifecycle (X-001)

The Anthropic SDK and API will evolve over time. This deliverable should address the maintenance posture for SDK updates:

**Considerations for SDK update lifecycle:**
- **Version pinning:** The SDK version should be pinned in `package.json` (or equivalent) to ensure reproducible builds. Updates should be deliberate, not automatic.
- **Breaking API changes:** The Anthropic API uses versioned headers (`anthropic-version`). If Anthropic deprecates the API version this deliverable targets, the provider module will need updates. The developer documentation (Procedure Step 9) should describe how to identify and respond to deprecation notices.
- **SDK major version upgrades:** Major version changes in the `@anthropic-ai/sdk` package may change initialization patterns, streaming helpers, or error types. These should be treated as maintenance tasks requiring re-verification of REQ-01 through REQ-10.
- **Governance:** No automated SDK update mechanism should be implemented (aligns with DEC-NET-001 — no update checks). SDK updates are developer-initiated.

Source: **ASSUMPTION: standard concern for API SDK integrations.** Procedure Step 9 mentions developer documentation covering "how to update when the Anthropic SDK or API changes" but no governance direction existed previously. *(Added per X-001.)*

### C8: Provider Lock-in Risk (E-002)

The single-provider design (DEC-NET-001, REQ-08) creates a dependency on Anthropic. This is a **deliberate trade-off**, not an oversight:

- **Rationale for acceptance:** DEC-NET-001 was a human ruling at Gate 3. The narrow outbound network policy is a security and simplicity decision. Building a multi-provider abstraction would add complexity without current benefit.
- **Risk factors:** If Anthropic changes pricing significantly, deprecates the Claude API, imposes new terms, or experiences extended outages, the system has no fallback provider. All LLM-dependent functionality would be unavailable.
- **Mitigation posture:** The provider module is a bounded component (REQ-08 — no abstraction layer). If a future decision changes the permitted providers, the module can be replaced or extended. The absence of an abstraction layer means the refactoring cost is contained to this deliverable and its interfaces with DEL-03-02.
- **Monitoring:** Changes to Anthropic's API, SDK, or terms of service should be tracked as part of the SDK update lifecycle (C7).

Source: DEC-NET-001 (human ruling); REQ-08; P1. *(Added per E-002.)*

### C9: Quality Attribute Targets (A-005, F-005)

No measurable quality attribute targets or performance budgets are currently defined for the provider integration. The following targets should be established during implementation:

| Quality Attribute | Target | Status |
|-------------------|--------|--------|
| Provider initialization time | TBD — expected to be sub-second for SDK client creation | TBD |
| Key resolution latency | TBD — depends on OI-001 provisioning mechanism (env var is near-instant; Keychain may involve OS prompts) | TBD |
| Streaming first-token latency (provider overhead) | TBD — the provider's contribution to first-token latency, excluding Anthropic API response time | TBD |
| Error response time | TBD — time from error detection to harness SSE error event delivery | TBD |
| Content block formatting overhead | TBD — per-block formatting time for multimodal content | TBD |

These targets are relevant because the provider is on the critical path for every LLM interaction. The provider's overhead should be negligible relative to Anthropic API response times, but measurable targets ensure regressions are detectable.

Source: **ASSUMPTION: performance budget is a standard concern for integration components on the critical path.** No source defines specific targets. *(Added per A-005, F-005.)*

## Trade-offs

### T1: Direct SDK Usage vs. HTTP Client

**Option A — Direct Anthropic SDK:** Use the official `@anthropic-ai/sdk` Node.js package. Provides typed interfaces, built-in streaming, and handles authentication/retry.

**Option B — Raw HTTP Client:** Make direct HTTP calls to `api.anthropic.com`. Full control but requires manual handling of auth headers, streaming parsing, retry logic, and API versioning.

**Preferred:** Option A (Direct SDK). The SDK reduces maintenance burden and aligns with Anthropic's supported integration path. Since the system supports exactly one provider, the SDK's opinions do not conflict with a multi-provider abstraction need.

Source: Human ruling record `POLICY_RULING_OI-001_PROVIDER_2026-02-23.md`.

### T2: Eager vs. Lazy Key Resolution

**Eager:** Resolve the API key at app startup and fail early if absent.
**Lazy:** Resolve the API key on first LLM request.

**Preferred:** Lazy resolution with early detection. The app should start and remain functional without a key (for browsing/editing project files). The first attempted LLM operation triggers key resolution and surfaces a clear error if absent. Optionally, the UI can proactively check for key availability and display a status indicator.

Source: **ASSUMPTION: derived from desktop UX principles — the app should not refuse to launch because of a missing API key.**

## Examples

No concrete code examples are available from accessible sources at this time. Examples will be developed during implementation based on the Anthropic SDK documentation (`location TBD` — external reference).

## ASSUMPTION Review Checkpoint (X-005)

The following ASSUMPTION-tagged items exist across the four documents for DEL-03-05. These should be reviewed and either confirmed or replaced with sourced evidence before implementation begins:

| ID | Document | Section | ASSUMPTION Summary | Priority |
|----|----------|---------|-------------------|----------|
| 1 | Datasheet | Attributes: Runtime SDK | SDK package inferred from stack | Medium |
| 2 | Datasheet | Attributes: Anthropic API Version | API versioning inferred | Medium |
| 3 | Datasheet | Construction: Provider Module | Architecture inferred from SPEC 9.8 | Medium |
| 4 | Datasheet | Construction: Key Resolver | Needed for non-project-truth constraint | Low (structurally sound) |
| 5 | Datasheet | Construction: Request/Response Mapping | Inferred from turn architecture | Low |
| 6 | Datasheet | Construction: Content Block Formatter | Inferred from REQ-05 + DEL-04-01 | Low |
| 7 | Specification | REQ-01 | Server-side initialization from security practice | High — foundational |
| 8 | Specification | REQ-04 | Non-streaming mode assumption | Medium |
| 9 | Specification | REQ-06 | Multiple error behaviors assumed | Medium |
| 10 | Specification | REQ-09 | Log protection from security practice | Low (standard practice) |
| 11 | Specification | REQ-10 | Timeout/cancellation from integration practice | Medium |
| 12 | Guidance | P3 | Fail-clearly principle from usability | Low (sound principle) |
| 13 | Guidance | P4 | Server-side only from security practice | High — foundational |
| 14 | Guidance | C2 | Model validation approach TBD | Medium |
| 15 | Guidance | C6 | Electron security model references | Medium |
| 16 | Guidance | T1 | SDK availability inferred | Low |
| 17 | Guidance | T2 | Lazy resolution from UX principles | Low |
| 18 | Procedure | Step 3 | SDK package path now fixed by ruling (`@anthropic-ai/sdk`) | Closed |

**Recommended review process:** Items marked "High" should be confirmed before implementation begins. Items marked "Medium" should be confirmed during the relevant implementation step. Items marked "Low" reflect standard engineering practice and can be confirmed during code review.

Source: Compiled from all four DEL-03-05 documents. *(Added per X-005.)*

## Conflict Table (for human ruling)

| Conflict ID | Conflict | Source A | Source B | Impacted Sections | Proposed Authority | Human Ruling |
|-------------|----------|----------|----------|-------------------|--------------------|--------------|
| CF-01 | Key provisioning mechanism was undefined; multiple candidates existed with different security/UX trade-offs | Decomposition DEL-03-05 ("define API key provisioning and storage contract") | OI-001 (policy decision pending) | Specification REQ-02, REQ-07; Procedure Steps 1-3 | Human (OI-001 resolution) | RESOLVED 2026-02-23: `ENV_ONLY` baseline; persisted storage out of scope unless re-ruled |
| CF-02 | REQ-05 requires multimodal content block formatting, but scope exclusion lists "Attachment handling and multimodal turns" as covered by PKG-04. The boundary (DEL-04-01 resolves; DEL-03-05 formats) is stated in REQ-05 but could be misread as a full exclusion | Specification REQ-05 | Specification Scope > Excluded (attachment handling) | Specification REQ-05, Scope Excluded, Guidance C4 | Specification REQ-05 text (boundary is stated) — PROPOSAL: no conflict if scope exclusion is clarified | TBD |
| CF-03 | Provider-path ambiguity existed between direct HTTP prototype usage and SDK-first completion criteria | Tier-5 prototype runtime notes | DEL-03-05 requirement intent (SDK client initialization) | Specification REQ-01; Procedure Step 3; verification acceptance | Human (provider-path ruling) | RESOLVED 2026-02-23: `ADOPT_SDK_NOW`; direct HTTP is interim-only and non-authoritative for completion |
