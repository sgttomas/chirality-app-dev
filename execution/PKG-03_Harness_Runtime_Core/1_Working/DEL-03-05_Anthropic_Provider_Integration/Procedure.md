# Procedure — DEL-03-05 Anthropic Provider Integration & Key Provisioning Contract

## Purpose

This procedure describes the steps to produce the Anthropic provider integration and API key provisioning contract for the Chirality harness runtime. It covers implementation, testing, and documentation of the provider module and key storage mechanism.

**Current cycle mode (2026-02-23):** SDK-path implementation pass completed (`@anthropic-ai/sdk@0.78.0`) with provider streaming + error taxonomy verification in `frontend/`.

## Prerequisites

| Prerequisite | Description | Satisfaction Criteria | Status |
|--------------|-------------|----------------------|--------|
| OI-001 Resolution | Human must decide the API key provisioning mechanism before key resolver implementation can be finalized | Human ruling record confirms `ENV_ONLY` baseline and associated constraints are documented | SATISFIED (Resolved 2026-02-23) |
| DEL-03-02 Turn Pipeline Interface | The turn execution API must define the interface that the provider module will implement (request/response shapes, streaming contract) | DEL-03-02 `Specification.md` defines request/response types and streaming event contract; provider interface type is importable or documented (F-003) | TBD |
| DEL-03-03 Model Fallback Chain | The opts model resolution must be defined so the provider receives a resolved model string | DEL-03-03 `Specification.md` defines `opts.model` resolution logic; the resolved model type/shape is documented (F-003) | SATISFIED (`DEL-03-03` lifecycle `IN_PROGRESS`) |
| Anthropic SDK Documentation | External reference required for SDK initialization, streaming API, and error codes | `location TBD` (external) | `location TBD` |
| Anthropic API Key | A valid Anthropic API key is required for integration testing | Operator-provisioned | Operator-provisioned |
| Development Environment | macOS 15+, Apple Silicon, Node.js, project repo cloned | Per DEC-PLAT-001 | Per DEC-PLAT-001 |

**Note (F-003):** Prerequisites DEL-03-02 and DEL-03-03 have status TBD. To determine when these prerequisites are satisfied, check for the existence and content of each deliverable's `Specification.md` — specifically, look for defined interface types (request/response shapes for DEL-03-02) and documented model resolution logic (for DEL-03-03). If these deliverables are not yet complete, implementation may proceed with provisional interfaces and mocks (see D-002 note in Step 8).

## Steps

### Step 1: Resolve OI-001 — Key Provisioning Policy

**Actor:** Human (policy decision)

1. Record ruling outcome:
   - `OI-001 = ENV_ONLY`
2. Document policy constraints:
   - canonical key source is `ANTHROPIC_API_KEY`
   - compatibility alias may be accepted as fallback (`CHIRALITY_ANTHROPIC_API_KEY`), but canonical key remains precedence source when both are present
   - no keychain, `safeStorage`, or app-local key persistence in current scope
3. Update Specification (REQ-02, REQ-07), Guidance (C1), and Datasheet Conditions to reflect the ruling.
4. Store the decision artifact:
   - `POLICY_RULING_OI-001_PROVIDER_2026-02-23.md`

**Completion criterion:** OI-001 is resolved and represented consistently across DEL-03-05 docs.

### Step 2: Implement Key Resolver

**Actor:** Developer

1. Create a key resolver module in the server-side codebase (Next.js API layer or Electron main process).
2. Implement ENV_ONLY key retrieval:
   2.1. Read `ANTHROPIC_API_KEY` as canonical source.
   2.2. Accept `CHIRALITY_ANTHROPIC_API_KEY` only as compatibility fallback (use it only when canonical key is unset).
   2.3. Do not read from keychain, `safeStorage`, or app-local config in this scope.
3. Implement graceful failure behavior:
   3.1. Return a typed error when no key is available (error category: "Missing API key" per REQ-06 taxonomy).
   3.2. Do not throw unhandled exceptions.
   3.3. Return a typed error when the key format is invalid (error category: "Invalid API key" per REQ-06 taxonomy).
   3.4. Do not expose the key value in error messages or logs (REQ-09).
4. Ensure the key is never:
   - Written to the working root (`projectRoot`).
   - Committed to git.
   - Sent to the renderer/client process.
   - Written to application logs or console output (REQ-09).

**Completion criterion:** Key resolver retrieves a valid key from the provisioned location or returns a clear, categorized error without exposing the key value.

### Step 3: Implement Anthropic SDK Client Initialization

**Actor:** Developer

1. Install the Anthropic SDK package (`@anthropic-ai/sdk`).
2. Pin the SDK version in `package.json` for reproducible builds (see Guidance C7).
3. Create a provider module that:
   - Uses the key resolver (Step 2) to obtain the API key.
   - Initializes the Anthropic SDK client with the resolved key.
   - Exposes a function interface compatible with the harness turn pipeline (DEL-03-02).
4. Ensure the client is initialized server-side only (REQ-01).
5. Direct HTTP-only provider implementations are not acceptance evidence for DEL-03-05 completion.

**Completion criterion:** SDK client initializes successfully with a valid key; fails gracefully with a missing/invalid key.

### Step 4: Implement Request/Response Mapping

**Actor:** Developer

1. Define the translation between harness turn request shapes and Anthropic API message format:
   1.1. Map `opts.model` (resolved by fallback chain) to Anthropic `model` parameter.
   1.2. Map harness message content (text and multimodal content blocks) to Anthropic `messages` array.
   1.3. Map harness system prompt to Anthropic `system` parameter. TBD — system prompt handling depends on whether the harness turn contract includes a system prompt field. **If the turn contract (DEL-03-02) includes a system prompt field:** map it to the Anthropic `system` parameter. **If not:** this deliverable does not generate a system prompt; system prompt is excluded from the provider's scope. **ASSUMPTION: system prompt handling TBD pending DEL-03-02 interface definition.**
   1.4. Map relevant turn options (e.g., `max_tokens`, `temperature`) to Anthropic API parameters. TBD — specific option mappings depend on harness opts contract (DEL-03-03).
2. Define the translation of Anthropic API responses back to harness turn response shapes.

**Completion criterion:** A harness turn request can be translated to an Anthropic API request and the response translated back.

### Step 5: Implement Streaming Adapter

**Actor:** Developer

1. Implement a streaming adapter that bridges Anthropic SDK streaming responses to harness SSE events.
2. Handle the following stream events (specific event names depend on Anthropic SDK documentation — `location TBD`):
   - Content delta events (incremental text chunks) -> harness SSE content events.
   - Message completion event -> harness SSE completion event.
   - Error events -> harness SSE error events.
3. Implement stream interruption handling:
   - **Timeout:** If the stream stalls beyond the configured timeout threshold, terminate the connection and emit a timeout error event (REQ-10).
   - **User cancellation:** If a cancellation signal is received (mechanism TBD — depends on DEL-03-02 turn pipeline), abort the Anthropic API request and emit a cancellation event (REQ-10).
   - **Cleanup:** In all interruption cases, release associated resources (HTTP connections, stream readers) without leaving orphaned connections.

**Completion criterion:** Streaming turn produces incremental SSE events visible in the UI; stream completes, errors, times out, or is cancelled cleanly.

### Step 6: Implement Error Classifier

**Actor:** Developer

1. Map Anthropic API error types to harness-level error categories using the normalized error taxonomy from REQ-06:
   - Missing API key (no key configured) -> "Missing API key" error with provisioning guidance.
   - `401 Unauthorized` -> "Invalid API key" error with re-provisioning guidance. *(Note: this is a distinct category from "Missing API key" per E-003 taxonomy normalization.)*
   - `429 Rate Limited` -> "Rate limiting" error (TBD: retry or surface).
   - `400 Bad Request` -> "API response error" (request validation subset).
   - `500+` -> "API response error" (server error subset).
   - Network/connection error -> "Network/connection error."
   - Timeout / stream stall -> "Request timeout" error (REQ-10).
   - User cancellation -> "User cancellation" (not an error; clean shutdown).
2. Ensure all error paths produce harness SSE error events rather than unhandled exceptions.
3. Ensure error messages do not leak the API key value (REQ-09).

**Completion criterion:** Each error category produces a typed, actionable error event using the normalized taxonomy; runtime remains stable; key material never appears in error output.

### Step 7: Implement Content Block Formatting

**Actor:** Developer

1. Implement formatting of multimodal content blocks for the Anthropic API:
   - Text blocks -> Anthropic text content.
   - Image blocks (base64-encoded) -> Anthropic image content blocks.
   - Document blocks -> TBD (depends on Anthropic API support for document types; `location TBD` — external).
2. Ensure content block formatting respects Anthropic API size limits and content type requirements.
3. **Scope boundary (C-002):** This step formats content blocks received from the attachment resolver (DEL-04-01). It does not perform attachment resolution, file reading, classification, or budget enforcement.

**Completion criterion:** Multimodal turns with text + images produce correct Anthropic API requests; content block formatting is limited to the provider's formatting responsibility.

### Step 8: Write Tests

**Actor:** Developer

1. **Unit tests:**
   - Key resolver: retrieves key from provisioned location; returns categorized error when absent ("Missing API key"); does not expose key in errors (REQ-09).
   - SDK client initialization: succeeds with valid key; fails gracefully with invalid key ("Invalid API key" category).
   - Request/response mapping: correct translation of harness shapes to/from Anthropic shapes.
   - Error classifier: each error type maps to expected harness error event per normalized taxonomy.
   - Log protection: verify no log/error path includes key material (REQ-09).
2. **Integration tests:**
   - End-to-end turn execution through the Anthropic provider (requires valid API key).
   - Streaming turn produces incremental SSE events.
   - **Streaming integrity (X-004):** Verify that content reassembled from streamed SSE events matches what a non-streaming call would return for the same input.
   - Model selection via `opts.model` override.
   - Multimodal turn with text + image attachment.
   - Non-image attachment block degrades to explicit text fallback without breaking Anthropic request shape.
   - Missing key produces actionable error in UI (acceptance criteria per F-001).
   - Timeout behavior when stream stalls (REQ-10).
3. Ensure tests do not commit or hardcode API keys. Use environment variable or test fixtures.

**Note (D-002):** If DEL-03-02 and/or DEL-03-03 are not yet complete when testing begins, use mock/stub interfaces that conform to the expected contract shapes. Unit tests can run independently of other deliverables. Integration tests that require the full turn pipeline should be deferred until DEL-03-02 is available, or use a test harness that simulates the turn pipeline interface. Document which tests require mocks vs. real dependencies.

**Completion criterion:** All unit and integration tests pass. Test coverage addresses REQ-01 through REQ-10. Mock dependencies are documented.

### Step 9: Write Documentation

**Actor:** Developer

1. **Operator documentation:**
   - How to provision the Anthropic API key (step-by-step for the chosen mechanism).
   - How to verify the key is working (e.g., send a test turn).
   - How to re-provision or rotate a key (see Guidance C5 for rotation considerations).
   - Troubleshooting: missing key, invalid key, rate limits, network errors (using normalized error taxonomy).
2. **Developer documentation:**
   - Provider module architecture: key resolver, SDK client, request mapper, content block formatter, streaming adapter, error classifier.
   - Interface contract with the turn pipeline (DEL-03-02).
   - How to update when the Anthropic SDK or API changes (see Guidance C7 for lifecycle considerations).
   - SDK version pinning rationale and update procedure.

**Completion criterion:** An operator can provision a key and successfully send a test turn using only the operator documentation. A developer can understand the provider module architecture, update the SDK, and modify error handling using only the developer documentation. *(Strengthened per D-003.)*

### Step 10: Integration Verification

**Actor:** Developer + Reviewer

1. Verify the provider integrates correctly with:
   - DEL-03-02 turn pipeline (turns execute end-to-end).
   - DEL-03-03 model fallback chain (`opts.model` is respected).
   - DEL-04-01 attachment resolver (multimodal content blocks are formatted correctly).
2. Verify that the API key is not present in:
   - Any file under the working root (grep-based scan per A-003).
   - Git history.
   - Renderer/client-side code.
   - Application logs or console output (REQ-09).
3. Verify that error states are handled gracefully and do not crash the runtime.
4. Verify that all error messages use the normalized error taxonomy (E-003).

**Completion criterion:** Provider functions correctly within the harness turn pipeline; key storage contract is satisfied; no key material leaks detected.

### Step 11: Rollback and Recovery (F-004)

**Actor:** Developer

If the provider module breaks an existing turn pipeline or introduces regressions:

1. **Isolate:** The provider module should be behind a feature flag or conditional import during development so it can be disabled without removing code.
2. **Revert:** If isolation is not possible, revert the provider module changes via git to restore the previous turn pipeline behavior.
3. **Diagnose:** Use unit tests (Step 8) to identify which component (key resolver, SDK client, request mapper, content block formatter, streaming adapter, error classifier) introduced the regression.
4. **Re-integrate:** Fix the identified component and re-run the integration verification (Step 10) before re-enabling the provider.

**Completion criterion:** A clear rollback path exists; the developer can disable or revert the provider module without affecting other harness functionality.

## Verification

| Check | Method | Expected Result |
|-------|--------|-----------------|
| Provider initializes with valid key | Unit test | SDK client created; no errors |
| Provider fails gracefully without key | Unit test | Typed "Missing API key" error returned; no crash; key not in error output |
| Provider fails gracefully with invalid key | Unit test | Typed "Invalid API key" error returned; no crash; key not in error output |
| Model selection respects fallback chain | Integration test | `opts.model` override is used; default used when omitted |
| Streaming turn produces SSE events | Integration test | Incremental content events received by UI |
| Streaming integrity verified | Integration test | Reassembled streamed content matches non-streaming response (X-004) |
| Multimodal content blocks formatted correctly | Integration test | Anthropic API accepts image + text content |
| API key not in working root | File inspection (grep scan) | No key material in `projectRoot` or git (A-003) |
| API key not exposed client-side | Code review | Key resolver and SDK client are server-side only |
| API key not in logs or errors | Unit test + log audit | No key material in any log or error output (REQ-09) |
| Errors produce actionable UI messages | Manual test | Each error category (per normalized taxonomy) shows clear guidance |
| Timeout/cancellation handled cleanly | Integration test | Stalled stream times out; cancelled stream aborts; no resource leaks (REQ-10) |

## Records

| Record | Location | Description |
|--------|----------|-------------|
| OI-001 Resolution | `POLICY_RULING_OI-001_PROVIDER_2026-02-23.md` + `MEMORY.md` | Human decision on key provisioning mechanism and provider-path ruling |
| Test Results | `execution/_Coordination/TIER5_CONTROL_LOOP_2026-02-23_PASS3.md` | Focused + full frontend verification outcomes for SDK-path implementation |
| Code Review | Git history | Review of provider module implementation |
| Key Storage Verification | `execution/_Coordination/TIER5_CONTROL_LOOP_2026-02-23_PASS3.md` | Evidence summary for server-side env-only key handling and non-project-truth posture |
| ASSUMPTION Review | `MEMORY.md` or Guidance ASSUMPTION Review Checkpoint | Confirmation or replacement of ASSUMPTION-tagged items (X-005) |
