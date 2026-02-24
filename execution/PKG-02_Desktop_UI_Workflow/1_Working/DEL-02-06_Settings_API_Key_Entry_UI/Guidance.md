# Guidance -- DEL-02-06 Settings / API Key Entry UI

## Purpose

DEL-02-06 exists because the OI-001 amendment (SCA-003) expanded the Anthropic API key provisioning contract from `ENV_ONLY` to `ENV+UI`. Previously, operators could only provide their API key via the `ANTHROPIC_API_KEY` environment variable. This deliverable adds a user-facing settings interface for key entry and local secure storage, making the key provisioning experience accessible to operators who may not be comfortable with environment variable configuration.

The UI-provided key takes precedence over the environment variable, establishing a layered resolution model: operators who prefer environment variables continue to use them as fallback, while those who prefer a graphical interface can enter their key directly in the application.

Source: Decomposition SCA-003 (OI-001 amendment); SOW-050.

## Principles

### P1: Non-Project-Truth by Design

The API key is explicitly classified as non-authoritative operator convenience state (DIRECTIVE section 2.5). This classification is not incidental -- it is a core design principle:

- The key enables LLM operations but is not part of the project's deliverable state.
- No project execution outcome should depend on which specific key was used.
- The key must never leak into the filesystem-as-state layer (working root, git history).

This means the storage mechanism must be architecturally isolated from the project filesystem. Electron's `safeStorage` API (or equivalent) provides this isolation by storing encrypted data in the OS-level application support directory, completely outside the working root.

Source: DIRECTIVE section 2.5; SPEC section 9.8.

### P2: Precedence Is Explicit and Deterministic

The ENV+UI precedence order (UI key first, env fallback second) must be deterministic and well-documented. Ambiguity in key resolution creates debugging difficulty and potential security confusion.

- When both sources provide a key, the UI-provided key wins -- always.
- When the UI key is removed, the system immediately falls back to the env variable -- no restart, no cache.
- When neither source provides a key, the system degrades gracefully.

Source: Decomposition SCA-003 (OI-001 amendment).

### P3: Key Material Is a Liability

Every location where the key exists in memory or storage is a potential exposure point. The design should minimize the number of such locations:

- One encrypted store (local secure storage).
- One retrieval path (IPC/module interface to the runtime key resolver).
- Zero copies in logs, error messages, serialized state, or renderer-accessible globals.

Source: DEL-03-05 REQ-09; standard security practice (**ASSUMPTION**).

**Authority basis note (lensing item E-001):** The phrase "shared security principle" appears in Specification REQ-06, Datasheet Conditions, and this principle (P3) as a source attribution for key-material protection requirements. Its authority traces to DEL-03-05 REQ-09, which is a peer deliverable -- not a governance document (DIRECTIVE/SPEC/CONTRACT). The underlying governance basis is SPEC section 9.8 (key-material constraints) and DIRECTIVE section 2.5 (convenience state must not compromise security posture). The "shared security principle" label is a convenience shorthand for these combined governance sources. TBD -- human to confirm whether this label should be formalized or replaced with direct governance citations.

## Terminology

*Added per lensing item E-002 (Normalization: stable operational discipline requires consistent terminology).*

The following canonical terms are established for consistent use across all four production documents:

| Concept | Canonical Term | Variants to Avoid | Notes |
|---------|---------------|-------------------|-------|
| The abstract storage capability | **local secure storage** | "Local secure storage adapter" (use only when referring to the code module), "secure local storage" | Used in requirements and architecture prose |
| The concrete storage mechanism | **Electron `safeStorage`** | "safeStorage API", "Electron safeStorage API" (acceptable in full references) | Used when referring to the specific implementation technology |
| The code module that wraps the mechanism | **local secure storage adapter** | "storage adapter", "secure storage module" | Used only when referring to the implementation component in Datasheet Construction and Procedure Steps |
| The interface to the runtime resolver | **key resolution bridge** | "IPC bridge", "key bridge", "resolution interface" | Used in Specification REQ-07, Datasheet Construction, Procedure Step 3 |

## Considerations

### C1: Interface Boundary with DEL-03-05

DEL-02-06 and DEL-03-05 share the key resolution contract. The boundary is:

| Responsibility | Owner |
|---------------|-------|
| UI for key entry, display, removal | DEL-02-06 |
| Local secure storage (write/read/delete) | DEL-02-06 |
| Key resolution bridge (expose stored key to runtime) | DEL-02-06 (provides) / DEL-03-05 (consumes) |
| ENV+UI precedence logic (query UI first, then env) | Shared -- DEL-02-06 exposes availability; DEL-03-05 implements resolution order |
| SDK client initialization with resolved key | DEL-03-05 |
| Error handling for missing/invalid key | DEL-03-05 (runtime errors); DEL-02-06 (UI indicators) |

**Note (resolved 2026-02-24):** DEL-03-05 Specification has been reconciled to `ENV+UI`. The active interface contract is UI key precedence with env fallback.

Source: _DEPENDENCIES.md DEP-02-06-003; DEL-03-05 Specification REQ-02.

### C2: Electron Process Architecture

In Electron applications, the main process and renderer process have different security contexts:

- **Main process:** Has access to Node.js APIs, including `safeStorage`. Key encryption/decryption should happen here.
- **Renderer process:** Runs the Next.js UI. Should only interact with keys via IPC -- never directly accessing the storage or holding decrypted keys longer than necessary for the entry flow.

**ASSUMPTION: The implementation will use Electron IPC for main-renderer communication regarding key operations.** The specific IPC channel design is TBD.

### C3: Storage Mechanism Selection

| Option | Pros | Cons | Notes |
|--------|------|------|-------|
| Electron `safeStorage` + app-local file | OS-level encryption; platform-native; no external dependency | Requires Electron main process; encrypted blob is in app support dir | **ASSUMPTION: preferred approach** |
| OS keychain direct (macOS Keychain) | Maximum platform security | More complex API; harder to test; platform-specific | May be overkill for a single key |
| Encrypted local config file (custom) | Full control over format | Must implement encryption correctly; risk of mistakes | Not recommended -- use platform primitives |

Source: Standard desktop security practice (**ASSUMPTION**).

### C4: Discoverability and Onboarding

The settings UI should be easily discoverable because API key configuration is a prerequisite for core application functionality. Consider:

- A first-run prompt or banner when no key is detected from either source.
- A persistent but non-intrusive indicator in the application chrome showing key status.
- Direct navigation from "no key" error states to the settings panel.

TBD -- specific UX design decisions.

### C5: UI Location Design Decision

*Added per lensing item D-002 (TBD_Question: UI location unresolved).*

The settings UI for API key entry must be located somewhere in the application. This is a prerequisite design decision that affects component architecture, navigation, and integration with DEL-02-05 (Frontend Workflow Shell Baseline). Options include:

| Option | Considerations |
|--------|---------------|
| Dedicated settings page | Clear separation; scalable if more settings are added later; requires navigation route |
| Modal dialog | Lightweight; accessible from any context; may feel transient for a critical configuration |
| Panel within existing view | Integrated; no navigation change; may crowd existing views |
| Section in a general settings view | Most conventional; assumes a settings view exists or will exist |

TBD -- human to decide. The choice affects Datasheet Construction ("Settings panel / page" row), Procedure Step 1.1, and the discoverability patterns described in C4. Source: Datasheet.md#Construction; Procedure.md#Step 1.1.

## Trade-offs

### T1: Security vs. Usability of Key Display

Showing the full key for copy/verification improves usability but increases exposure risk. Showing only a partial mask (last 4 characters) reduces risk but limits verification ability.

**Recommended:** Default to masked display with a partial mask indicator (last 4 characters). Provide an optional reveal toggle that shows the full key temporarily and auto-hides after a short timeout. This is consistent with industry patterns for credential management UIs.

**ASSUMPTION: This trade-off resolution follows standard practice; human to confirm UX specifics.**

### T2: Restart Requirement vs. Implementation Complexity

Requiring an application restart after key changes simplifies the implementation (no runtime re-query needed) but degrades the operator experience.

**Recommended:** No restart required. Re-query-per-turn is the final policy ruling (2026-02-24): runtime re-queries key source on each turn/session bootstrap, so no dedicated change-notification channel is required.

Source: Specification REQ-03 (removal is immediate, no restart).

### T3: Key Validation at Entry Time

The UI could validate the key by making a test API call at entry time, or it could simply store the key and let the first real turn surface any authentication errors.

| Approach | Pros | Cons |
|----------|------|------|
| Validate on save | Immediate feedback; operator knows key works | Requires network call; may fail for non-key reasons (rate limits, network); adds latency to save |
| Store without validation | Simple; fast; no network dependency | Operator discovers invalid key later on first turn |

TBD -- human to decide. Both approaches are compatible with the specification. (Lensing item A-001: this decision is a prerequisite for implementation -- without a ruling, implementers cannot determine whether a network call on save is required. Affects Specification requirements, Procedure Steps 4.1/5.1, and the error/failure mode taxonomy in Specification.)

## Examples

TBD -- UI mockups and interaction flows to be developed during implementation.

## Assumption Register

*Added per lensing item B-003 (WeakStatement: ASSUMPTION density lacks consolidated tracking). This register consolidates all ASSUMPTION annotations scattered across the four production documents for centralized tracking and resolution.*

| Assumption ID | Document | Section | Assumption Statement | Impact if Wrong | Resolution Status |
|---|---|---|---|---|---|
| ASM-01 | Datasheet | Attributes (Storage mechanism) | Electron `safeStorage` is the expected mechanism for local secure key storage | Different storage API needed; adapter design changes | TBD -- human to confirm |
| ASM-02 | Specification | REQ-01 | Standard masked-input UX pattern for key entry | Minor UX variation only | TBD |
| ASM-03 | Specification | REQ-01 | Common UX convention for reveal toggle on credential entry | Toggle may be omitted or designed differently | TBD |
| ASM-04 | Specification | REQ-02 | Partial-mask display (last 4 chars) is standard practice for credential confirmation | Display format may differ | TBD |
| ASM-05 | Specification | REQ-03 | Runtime re-queries key source on each turn or session (no restart needed) | If not true, key change requires restart or notification mechanism | RESOLVED (2026-02-24): re-query-per-turn policy approved |
| ASM-06 | Specification | REQ-04 | Encryption-at-rest is required for locally stored credentials | If not required, simpler storage may suffice; but governance sources (DIRECTIVE 2.5, SPEC 9.8) strongly imply protection is needed | TBD -- human to confirm |
| ASM-07 | Specification | REQ-04 | `safeStorage` is the expected mechanism (same as ASM-01) | See ASM-01 | TBD |
| ASM-08 | Specification | REQ-06 | Electron main-process isolation is used for key operations | If renderer handles keys directly, security model changes significantly | TBD |
| ASM-09 | Specification | REQ-06 | Standard credential-field security practice (autofill prevention) | Minor implementation detail | TBD |
| ASM-10 | Specification | REQ-07 | Change notification is needed for runtime to avoid stale key state | If re-query-per-turn is adopted, change notification is unnecessary; IPC design simplifies | RESOLVED (2026-02-24): re-query-per-turn adopted; no change notification required |
| ASM-11 | Guidance | P3 | Standard security practice for key-material-as-liability principle | Low risk -- principle is well-established | TBD |
| ASM-12 | Guidance | C2 | Electron IPC for main-renderer communication regarding key operations | Core architectural assumption; unlikely to change | TBD |
| ASM-13 | Guidance | C3 | `safeStorage` + app-local file is preferred storage approach | See ASM-01 | TBD |
| ASM-14 | Procedure | Prerequisites | DEL-02-05 (Frontend Workflow Shell) required as mounting point | If shell architecture changes, settings UI mounting changes | TBD |
| ASM-15 | Procedure | Prerequisites | DEL-01-03 (Frontend Workspace Bootstrap) required for build infrastructure | Low risk -- build infra is a standard prerequisite | TBD |
| ASM-16 | Procedure | Step 2 | `safeStorage` as mechanism (same as ASM-01) | See ASM-01 | TBD |
| ASM-17 | Procedure | Step 3.3 | DEL-03-05 key resolver runs in the same main process context | If resolver runs in a different process, IPC bridge design changes | TBD |

**Consolidation note:** ASM-01, ASM-07, ASM-13, and ASM-16 are the same assumption (safeStorage mechanism) appearing in four locations. Resolution of ASM-01 resolves all four. ASM-06 (encryption-at-rest) is closely related but distinct -- it concerns the property, not the mechanism.

## Conflict Table (for human ruling)

| Conflict ID | Conflict | Source A | Source B | Impacted Sections | Proposed Authority | Human Ruling |
|-------------|---------|----------|----------|--------------------|--------------------|--------------|
| CONF-01 | DEL-03-05 REQ-02 had `ENV_ONLY` baseline while OI-001 amendment (SCA-003) established `ENV+UI`. Conflict now closed via document reconciliation. | DEL-03-05 Specification REQ-02 (historical pre-reconciliation state) | Decomposition SCA-003 / SPEC section 9.8 (ENV+UI) | Specification REQ-05, REQ-07; Guidance C1; Datasheet Attributes ("Key provisioning policy" row); Procedure Prerequisites ("DEL-03-05 Specification" row) | Decomposition SCA-003 and SPEC section 9.8 are authoritative | RESOLVED (2026-02-24): DEL-03-05 Spec reconciled to `ENV+UI` |
