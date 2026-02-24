# Procedure -- DEL-02-06 Settings / API Key Entry UI

## Purpose

This procedure describes the steps to produce and verify the Settings / API Key Entry UI deliverable (DEL-02-06). The deliverable implements SOW-050: a UI for Anthropic API key entry with local secure storage and the ENV+UI runtime precedence contract.

## Prerequisites

### Required References

| Reference | Location | Purpose |
|-----------|----------|---------|
| SPEC.md section 9.8 | `docs/SPEC.md` | ENV+UI key provisioning baseline; key-material constraints |
| DIRECTIVE.md section 2.5 | `docs/DIRECTIVE.md` | Non-authoritative convenience state rules |
| DEL-03-05 Specification | `execution/PKG-03_Harness_Runtime_Core/1_Working/DEL-03-05_Anthropic_Provider_Integration/Specification.md` | Downstream key resolver interface (REQ-02, REQ-06, REQ-07) |

### Required Upstream Dependencies

| Dependency | Status | Notes |
|-----------|--------|-------|
| DEL-02-05 (Frontend Workflow Shell Baseline) | **ASSUMPTION: required** | Settings UI requires the frontend workflow shell to be available as a mounting point |
| DEL-01-03 (Frontend Workspace Bootstrap) | **ASSUMPTION: required** | Frontend build infrastructure must exist before UI components can be developed |
| Electron `safeStorage` API availability | Platform prerequisite | macOS 15+ with Electron runtime |

### Upstream Constraint Documents

| Constraint Source | Key Constraint |
|-------------------|---------------|
| DIRECTIVE section 2.5 | Key is non-authoritative convenience state; must not be treated as project truth |
| SPEC section 9.8 | Key must not be persisted in working-root files or git-tracked execution documents |
| Decomposition SCA-003 (OI-001 amendment) | UI-provided key takes precedence; `ANTHROPIC_API_KEY` env fallback |

## Steps

### Step 1: Design the Settings UI Surface

1.1. Determine the UI location for API key settings (settings page, modal, dedicated panel, or section within an existing settings view). TBD -- requires UX design decision.

1.2. Design the key entry form:
   - Masked text input for key entry (REQ-01).
   - Optional reveal toggle for temporary key visibility (REQ-01).
   - Save/submit button to persist the key (REQ-01).
   - Clear/remove button to delete the stored key (REQ-03).

1.3. Design the key status indicator:
   - "Key configured" state with partial mask (last 4 characters) (REQ-02).
   - "No key configured" state with guidance on how to proceed (REQ-02, REQ-08).

1.4. Design discoverability elements:
   - Navigation path from main application chrome to settings (REQ-08).
   - First-run or no-key-detected banner/prompt (REQ-08). TBD -- specific pattern.

### Step 2: Implement Local Secure Storage Adapter

2.1. Create a storage adapter module in the Electron main process that uses `safeStorage` (or equivalent) to encrypt and decrypt the API key. **ASSUMPTION: `safeStorage` is the mechanism.**

2.2. Implement the following operations:
   - `storeKey(key: string): Promise<void>` -- encrypt and persist the key.
   - `retrieveKey(): Promise<string | null>` -- decrypt and return the stored key, or `null` if none exists.
   - `removeKey(): Promise<void>` -- delete the stored key.
   - `hasKey(): Promise<boolean>` -- check whether a key is stored without retrieving it.

2.3. Ensure the storage location is:
   - In the Electron app's application support directory (platform-appropriate).
   - Outside the working root (`projectRoot`).
   - Not in any git-tracked location.

2.4. Ensure key material protection:
   - No plaintext key in config files or logs.
   - Key is encrypted at rest via `safeStorage`.
   - Storage adapter does not log key values at any verbosity level.

### Step 3: Implement Key Resolution Bridge (IPC Interface)

3.1. Define IPC channels for renderer-to-main communication:
   - `api-key:store` -- renderer sends key to main for encryption and storage.
   - `api-key:remove` -- renderer requests key removal.
   - `api-key:status` -- renderer queries whether a key is stored (without retrieving the value).

**Policy ruling (2026-02-24):** Re-query-per-turn is the final REQ-07 policy. No `api-key:changed` notification channel is required.

3.2. Implement the IPC handlers in the Electron main process, backed by the storage adapter from Step 2.

3.3. Expose a module-level interface for the DEL-03-05 key resolver to consume:
   - The key resolver (running in the main/server process) should call the storage adapter directly rather than going through IPC. **ASSUMPTION: DEL-03-05 key resolver runs in the same main process context.**
   - The interface must support the query pattern defined in Specification REQ-07 (re-query on each turn).

3.4. Implement no-restart re-query behavior:
   - Ensure DEL-03-05 key resolution re-queries key source on each turn/session bootstrap.
   - Verify save/remove/update operations are visible on the next turn without restart.

### Step 4: Implement Settings UI Components

4.1. Build the settings UI component(s) in the Next.js frontend:
   - Key entry form with masked input.
   - Save and clear actions wired to IPC channels.
   - Status indicator reflecting current key state.
   - Reveal toggle (if included per UX decision).

4.2. Wire the UI to the IPC bridge:
   - On mount/navigation, query key status via `api-key:status`.
   - On save, send key via `api-key:store`.
   - On clear, invoke `api-key:remove`.
   - After save/remove, re-query `api-key:status` to refresh UI state.

4.3. Implement autofill prevention on the key input field (REQ-06):
   - Set `autocomplete="off"` and equivalent attributes.
   - Prevent browser/Electron form persistence for this field.

4.4. Implement graceful degradation indicators (REQ-08):
   - When no key is available, LLM-dependent UI elements should show a key-required message.
   - Provide a link/button from the key-required message to the settings UI.

### Step 4b: Implement Recovery and Degradation Handling

*Added per lensing item C-002 (MissingSlot: missing rollback/recovery procedure for storage mechanism failures).*

4b.1. Implement `safeStorage` availability check on application startup:
   - Call `safeStorage.isEncryptionAvailable()` during main process initialization.
   - If unavailable: disable the key storage feature; set UI to indicate "secure storage unavailable -- use environment variable instead."
   - Log a warning (without key material) noting the unavailability reason.

4b.2. Implement corrupted/unreadable key recovery:
   - If `retrieveKey()` throws a decryption error, catch the error and:
     - Return null (treated as "no UI key stored").
     - Display a UI notification: "Stored key is unreadable. It may need to be re-entered."
     - Do NOT automatically delete the corrupted blob (operator may want to investigate).
   - The system falls back to `ANTHROPIC_API_KEY` environment variable per REQ-05.

4b.3. Implement storage write failure handling:
   - If `storeKey()` throws an encryption or write error:
     - Display a UI error: "Failed to save key. Check system storage availability."
     - Do NOT store the key in plaintext as a fallback (REQ-04, REQ-06).
     - Retain any previously stored key (no data loss on write failure).

4b.4. Reference the error/failure mode taxonomy in Specification.md#Error and Failure Modes for the complete set of anticipated failure conditions.

**Note:** Specific error messages, retry logic, and UX for recovery states are TBD pending implementation design.

### Step 5: Write Tests

5.1. **Storage adapter unit tests:**
   - Store, retrieve, and remove key operations work correctly.
   - `hasKey` returns correct boolean values.
   - Key material does not appear in test logs or console output.

5.2. **IPC bridge tests:**
   - All IPC channels respond correctly.
   - No `api-key:changed` channel is required under re-query-per-turn policy.

5.3. **Key precedence integration tests:**
   - With UI key stored and env key set: runtime uses UI key.
   - With UI key removed and env key set: runtime uses env key.
   - With UI key updated: next turn uses updated UI key without restart.
   - With neither source: graceful degradation occurs.

5.4. **UI component tests:**
   - Key entry form renders with masked input.
   - Save action triggers storage.
   - Clear action removes stored key.
   - Status indicator updates on key state changes.

5.5. **Security tests:**
   - Key value does not appear in any log output (grep-based scan).
   - Key value is not present in working root after storage operations.
   - Input field does not participate in autofill.

### Step 6: Write Documentation

6.1. **Operator-facing key setup guide:**
   - How to enter an API key via the settings UI.
   - How to verify the key is configured (status indicator).
   - How to remove a stored key.
   - How the ENV+UI precedence works (UI key wins, env fallback).

6.2. **Architecture notes:**
   - Storage adapter design and location.
   - IPC channel contracts.
   - Interface contract with DEL-03-05 key resolver.
   - Key material protection measures.

## Verification

| Check | Method | Pass Criteria |
|-------|--------|---------------|
| Key entry works | Manual test | Operator can enter key; it is stored; status indicator updates |
| Key masked by default | Manual test | Key characters not visible in input field |
| Key removal works | Manual test | Operator can clear key; status indicator updates; runtime falls back to env |
| No restart required | Manual test | Key change takes effect on next turn without app restart |
| Key not in working root | Automated scan | `grep` of `projectRoot` finds no key material after storage operations |
| Key not in git | Automated scan | `git log --all -S` search finds no key material |
| Key not in logs | Automated scan | Console/log output during key operations contains no key material |
| ENV+UI precedence | Integration test | With both sources, UI key is used; with UI key removed, env key is used |
| Graceful degradation | Manual test | No key = app functional for non-LLM features; clear error guidance displayed |
| Storage encrypted | Inspection | Storage uses `safeStorage` or equivalent; no plaintext config files |

## Records

*Lensing item F-003: artifact locations should be resolved to enable audit traceability. Recommended default locations are provided below; human to confirm.*

| Record | Description | Location | Location Rationale |
|--------|-------------|----------|--------------------|
| Test results | Unit and integration test output | TBD -- recommended: `execution/PKG-02_Desktop_UI_Workflow/1_Working/DEL-02-06_Settings_API_Key_Entry_UI/2_Verification/` or standard test runner output captured in CI | Deliverable-local verification subfolder keeps evidence co-located with the deliverable |
| Key setup guide | Operator-facing documentation | TBD -- recommended: `docs/guides/api-key-setup.md` (repo-level user docs) or deliverable-local `DOC/` artifact | User-facing docs typically live in `docs/`; deliverable-local is acceptable if no shared docs folder exists |
| Architecture notes | Technical design documentation | TBD -- recommended: deliverable-local `DOC/architecture-notes.md` within `execution/PKG-02_Desktop_UI_Workflow/1_Working/DEL-02-06_Settings_API_Key_Entry_UI/` | Architecture notes are deliverable-specific and should travel with the deliverable |
| Verification evidence | Screenshots, scan logs, test logs | TBD -- recommended: `execution/PKG-02_Desktop_UI_Workflow/1_Working/DEL-02-06_Settings_API_Key_Entry_UI/2_Verification/` | Co-located with deliverable for audit traceability |
| Code changes | Implementation commits | Git history (tracked per "git is the event store") | Already resolved -- git is the canonical location |
