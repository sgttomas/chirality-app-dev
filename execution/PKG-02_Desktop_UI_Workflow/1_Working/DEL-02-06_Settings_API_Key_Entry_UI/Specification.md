# Specification -- DEL-02-06 Settings / API Key Entry UI

## Scope

### Covered

This deliverable covers the implementation and documentation of:

1. **Settings UI for Anthropic API key entry** -- a user-facing interface within the Chirality desktop application that allows an operator to enter, view status of, and remove their Anthropic API key.
2. **Local secure storage of the API key** -- the client-side mechanism that persists the entered key as non-project-truth convenience state, outside the working root and git-tracked files.
3. **Key resolution bridge** -- the interface contract by which the runtime key resolver (DEL-03-05) can query for a UI-provided key and apply the ENV+UI precedence policy.

**Scope item coverage:** SOW-050 ("Provide UI-based API key entry and local secure storage (non-project-truth convenience state) with runtime contract: UI key takes precedence and `ANTHROPIC_API_KEY` remains fallback.")

Source: Decomposition SCA-003 (Scope Amendment A3); Scope Ledger SOW-050 row.

### Excluded

- **Anthropic SDK client initialization, request dispatch, and response handling** -- covered by DEL-03-05.
- **Runtime environment variable resolution (`ANTHROPIC_API_KEY`)** -- the env-var fallback path is owned by DEL-03-05 REQ-02; this deliverable provides only the UI-provided key that takes precedence.
- **Outbound network guardrails** -- covered by DEL-03-06.
- **Turn execution pipeline, SSE streaming, tool calling** -- covered by DEL-03-02 and other PKG-03 deliverables.
- **Operator Toolkit panel and local presets** -- covered by DEL-02-03; this deliverable covers only the API key settings surface.

## Requirements

### REQ-01: API Key Entry Interface

The application MUST provide a settings UI surface where the operator can enter an Anthropic API key.

- The key input MUST use a masked/obscured text field (key characters not visible by default). **ASSUMPTION: standard masked-input UX pattern.**
- The UI SHOULD provide a toggle or reveal mechanism to temporarily view the entered key before saving. **ASSUMPTION: common UX convention for credential entry.**
- The UI MUST provide a save/submit action that persists the key to local secure storage.

Source: SOW-050; Decomposition DEL-02-06 description.

### REQ-02: Key Status Display

The UI MUST indicate to the operator whether an API key is currently configured.

- When a key is stored, the UI SHOULD display a status indicator (e.g., "Key configured" with a partial mask showing the last 4 characters). **ASSUMPTION: partial-mask display is standard practice for credential confirmation.**
- When no key is stored and no environment fallback is detected, the UI SHOULD indicate that no key is available and that LLM-dependent features will be unavailable.

Source: SOW-050; DEL-03-05 REQ-06 (missing-key error handling must provide actionable guidance).

### REQ-03: Key Removal

The UI MUST provide a mechanism to remove/clear a previously stored API key from local secure storage.

- After removal, the runtime MUST fall back to `ANTHROPIC_API_KEY` environment variable resolution (per DEL-03-05 REQ-02 fallback chain).
- Removal MUST be immediate and not require an application restart to take effect. Runtime applies re-query-per-turn policy (human ruling 2026-02-24).

Source: SOW-050; DIRECTIVE section 2.5 (operator controls convenience state).

### REQ-04: Local Secure Storage

The API key MUST be stored using a local secure storage mechanism that satisfies DIRECTIVE section 2.5 non-project-truth requirements.

- The key MUST NOT be stored in the working root (`projectRoot`) or any git-tracked project execution file. (Source: SPEC section 9.8; DIRECTIVE section 2.5.)
- The key MUST NOT be stored in plain text in app-local configuration files. **ASSUMPTION: encryption-at-rest is required for locally stored credentials.**
- The storage mechanism SHOULD use Electron `safeStorage` API or an equivalent platform-native secure storage facility. **ASSUMPTION: `safeStorage` is the expected mechanism; human to confirm.**
- The stored key is classified as **non-authoritative operator convenience state** and MUST NOT be treated as project truth. (Source: DIRECTIVE section 2.5.)
- The stored key MUST NOT override contract/governance enforcement. (Source: DIRECTIVE section 2.5.)

### REQ-05: ENV+UI Key Precedence Contract

The runtime key resolution order MUST be:

1. **UI-provided key** (from local secure storage) -- takes precedence when present.
2. **`ANTHROPIC_API_KEY` environment variable** -- fallback when no UI-provided key is stored.

- This deliverable is responsible for the UI entry, storage, and retrieval side of this contract.
- The runtime resolution logic (checking UI key first, then env) is shared responsibility with DEL-03-05 key resolver.
- The precedence contract is defined by the OI-001 amendment (SCA-003): "runtime first uses UI-provided key from local secure storage (non-project-truth convenience state), with `ANTHROPIC_API_KEY` environment fallback."

Source: Decomposition SCA-003 (OI-001 amendment); SPEC section 9.8 (API key provisioning baseline).

### REQ-06: Key Material Protection

Key material handled by this deliverable's UI and storage components MUST be protected from exposure.

- The key value MUST NOT appear in application logs, console output, or error messages. (Source: DEL-03-05 REQ-09; shared security principle.)
- The key value MUST NOT be transmitted to the renderer process in plaintext outside of the secure entry/retrieval path. **ASSUMPTION: Electron main-process isolation is used for key operations.**
- The key value MUST NOT be included in any state that could be serialized to working-root files or git. (Source: SPEC section 9.8; DIRECTIVE section 2.5.)
- The key input field MUST NOT participate in browser/Electron autofill or form persistence. **ASSUMPTION: standard credential-field security practice.**

### REQ-07: Runtime Integration Interface

This deliverable MUST expose an interface (IPC channel, module API, or equivalent) that allows the DEL-03-05 key resolver to:

- Query whether a UI-provided key is available.
- Retrieve the decrypted key value for use in Anthropic SDK client initialization.
- Re-query key availability/value on each turn (and session bootstrap) so save/remove/update actions take effect without restart.
- Change-notification events are NOT required for this deliverable. Human ruling (2026-02-24): final policy is re-query-per-turn.

Source: _DEPENDENCIES.md DEP-02-06-003 (downstream interface to DEL-03-05).

### REQ-08: Graceful Degradation

When no API key is available from either source (UI storage or environment):

- The application MUST remain functional for non-LLM features (file browsing, project navigation, deliverable viewing).
- LLM-dependent features SHOULD display a clear indication that an API key is required.
- The settings UI SHOULD be easily discoverable from error states (e.g., a link or button from the "no key" indicator to the settings panel).

Source: DEL-03-05 REQ-06 (F-001: missing-key error handling); SOW-050.

## Error and Failure Modes

The following taxonomy enumerates anticipated failure modes for key storage operations. This section was added per lensing item B-002 (comprehensive-record gap). REQ-08 covers graceful degradation for missing keys; this section covers storage mechanism failures.

| Failure Mode | Trigger Condition | Expected Behavior | Requirement Link |
|---|---|---|---|
| Encryption failure | `safeStorage` API returns error during `encryptString()` | Storage operation fails; UI displays error; key is NOT stored in plaintext as fallback. | REQ-04, REQ-06 |
| Decryption failure | `safeStorage` API returns error during `decryptString()` (e.g., corrupted blob) | Retrieval returns null; system falls back to env variable; UI reports stored key is unreadable. | REQ-05, REQ-08 |
| Storage full / write failure | OS-level disk or keychain storage exhaustion | Storage operation fails; UI displays error; operator advised to free space or check system storage. | REQ-04 |
| `safeStorage` unavailable | Electron `safeStorage.isEncryptionAvailable()` returns false (e.g., no keychain on Linux without libsecret) | Key storage feature is disabled; UI indicates unavailability; system operates in env-only mode. | REQ-08 |
| Corrupted stored key | Stored encrypted blob is truncated or tampered | Same as decryption failure; retrieval returns null; fallback to env variable. | REQ-05, REQ-08 |
| Key format invalid | Operator enters a value that is not a syntactically valid API key | TBD -- depends on human ruling on key validation at entry time (see Guidance.md#T3). If validate-on-save: immediate error. If store-without-validation: stored as-is, error surfaces on first API call. | REQ-01 |

**Note:** Specific error messages and recovery UX are TBD pending implementation design. The above establishes the expected behavioral contract for each failure mode.

## Standards

| Standard/Reference | Relevance | Accessible |
|--------------------|-----------|------------|
| SPEC.md section 9.8 | ENV+UI key provisioning baseline; key-material constraints | Yes |
| DIRECTIVE.md section 2.5 | Non-authoritative convenience state rules | Yes |
| Electron `safeStorage` API | Platform-native encrypted storage for sensitive data | No (external Electron docs; `location TBD`). **Note (lensing item A-003):** Until the relevant API documentation is accessible or its requirements are extracted locally, compliance determination against this standard is not possible. Implementers should extract applicable requirements from the Electron documentation during Step 2 of Procedure. |
| DEL-03-05 Specification | Downstream key resolver contract (REQ-02, REQ-06, REQ-07, REQ-09) | Yes (deliverable-local in execution tree) |
| OWASP credential storage guidelines | Best practices for client-side credential management | No (external; `location TBD`). **Note (lensing item A-003):** Until the relevant guidelines are accessible or their applicable requirements are extracted locally, compliance determination against this standard is not possible. Extract applicable requirements during implementation. |

## Verification

| Requirement | Verification Approach | Verification Artifact |
|-------------|----------------------|----------------------|
| REQ-01 | Manual test: operator can enter a key via settings UI; key is masked; save action persists | TEST / CODE |
| REQ-02 | Manual test: status indicator reflects key presence; shows partial mask when stored; shows absent state when cleared | TEST |
| REQ-03 | Manual test: operator can remove key; runtime falls back to env variable; no restart required | TEST |
| REQ-04 | Inspection + Automated scan: (1) key not present in `projectRoot` or git-tracked files (automated grep-based scan of working root); (2) storage uses `safeStorage` or equivalent -- confirm `safeStorage.isEncryptionAvailable()` returns true and encrypted blob is non-plaintext; (3) verify encryption is active by confirming stored blob differs from plaintext key value (lensing item D-001: explicit encryption-at-rest acceptance criterion). **Note:** REQ-04 ASSUMPTION (encryption-at-rest required) remains pending human confirmation. | TEST / DOC |
| REQ-05 | Integration test: with both UI key and env key set, UI key is used; with UI key removed, env key is used; with neither, graceful degradation | TEST |
| REQ-06 | Code review: log/error paths do not expose key; autofill disabled on input; no key in serializable state | TEST / CODE |
| REQ-07 | Integration test with defined scenarios: (1) Store key via UI, query via resolver, verify returned key matches stored key; (2) Remove key via UI, query via resolver, verify resolver returns null; (3) Update key via UI, verify next turn re-query resolves updated key without restart; (4) With no UI key, verify resolver falls through to env fallback. Pass criteria: all scenarios pass and no stale key state persists across turns. | TEST |
| REQ-08 | Manual test: with no key configured, non-LLM features work; LLM features show key-required indicator; settings are discoverable from error state | TEST |

## Documentation

The following artifacts are anticipated for this deliverable:

| Artifact Type | Description |
|---------------|-------------|
| CODE | Settings UI component(s), local secure storage adapter, key resolution bridge (IPC/module interface) |
| TEST | Unit tests for storage adapter, integration tests for key resolution precedence, manual test procedures for UI flows |
| DOC | Operator-facing key setup guide; architecture notes for the UI-to-runtime key resolution interface |
