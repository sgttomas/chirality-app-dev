# Specification — DEL-03-05 Anthropic Provider Integration & Key Provisioning Contract

## Scope

### Covered

This deliverable covers the implementation and documentation of:

1. **Anthropic API provider integration** within the harness runtime — the server-side module that enables the harness to issue requests to the Anthropic (Claude) API and receive responses, including streaming responses.
2. **API key provisioning and storage contract** — a defined mechanism by which an operator provides their Anthropic API key, the runtime retrieves it, and the key is stored as non-project-truth convenience state.

**Scope item coverage:** SOW-006 ("Implement/maintain harness runtime responsibilities: tool calling, permissions, and event streaming") — specifically the Anthropic provider integration slice.

Source: Decomposition DEL-03-05; Scope Ledger SOW-006 row.

### Excluded

- **Outbound network guardrails** (Anthropic-only enforcement, egress policy verification) — covered by DEL-03-06.
- **Turn execution API and SSE streaming protocol** (the generic harness turn pipeline) — covered by DEL-03-02.
- **Turn options mapping and fallback chains** (generic `opts` resolution) — covered by DEL-03-03, although this deliverable integrates with the model fallback chain.
- **Tool calling and permissions** (generic tool dispatch) — covered by DEL-03-02 / PKG-03 scope generally; this deliverable covers only the Anthropic-specific provider layer.
- **Attachment handling and multimodal turns** — attachment resolution, file reading, classification, and budget enforcement are covered by PKG-04 (DEL-04-01, DEL-04-02). This deliverable receives pre-processed content blocks from DEL-04-01 and formats them for the Anthropic API (see REQ-05 for the boundary). *(Clarified per C-002 — the boundary is: DEL-04-01 resolves and classifies attachments; DEL-03-05 formats the resulting content blocks for the Anthropic API.)*

## Requirements

### REQ-01: Anthropic SDK Client Initialization

The provider module MUST initialize an Anthropic SDK client using a resolved API key.

- The client MUST be initialized server-side (Next.js API route or Electron main process context).
- The client MUST NOT be initialized or exposed on the client/renderer side.
- The official SDK package path (`@anthropic-ai/sdk`) is mandatory for DEL-03-05 acceptance.
- Current implementation baseline pins `@anthropic-ai/sdk` to `0.78.0` in `frontend/package.json`.
- Direct HTTP provider integrations MAY exist as interim experiments but MUST NOT be treated as completion evidence for DEL-03-05.

Source: Human ruling record `POLICY_RULING_OI-001_PROVIDER_2026-02-23.md`; security rationale in Guidance Section C6 (F-002).

### REQ-02: API Key Resolution

The runtime MUST resolve the Anthropic API key from a provisioned storage location at startup or on-demand before the first API call.

- The key MUST NOT be stored in the working root (`projectRoot`) or any git-tracked project execution file. (Source: Decomposition DEL-03-05 — "non-project-truth convenience state"; DIRECTIVE Section 2.5.)
- ENV_ONLY baseline is mandatory for current scope: runtime resolves the key from process environment (`ANTHROPIC_API_KEY`).
- Compatibility alias (`CHIRALITY_ANTHROPIC_API_KEY`) MAY be supported for migration, but `ANTHROPIC_API_KEY` remains the canonical operator-facing key contract.
- The runtime MUST NOT depend on keychain, `safeStorage`, or app-local config persistence in current DEL-03-05 scope.
- The key resolver MUST fail gracefully when no key is available (see REQ-06).

**Note (A-001 Resolved, 2026-02-23):** Human ruling set OI-001 to `ENV_ONLY` for this cycle. Persisted secure-storage mechanisms are out of scope unless explicitly re-ruled.

### REQ-03: Model Selection Integration

The provider MUST respect the harness model selection fallback chain:

1. `opts.model` (per-turn override)
2. Global model setting (instruction root configuration)
3. Runtime default

Source: SPEC Section 9.8 (key fallback examples — Model).

### REQ-04: Request Dispatch and Response Handling

The provider MUST translate harness turn requests into Anthropic API requests and return structured responses.

- For non-streaming turns: the provider MUST return the complete response to the harness turn pipeline. **ASSUMPTION: non-streaming mode may be needed for certain turn types.**
- For streaming turns: the provider MUST bridge Anthropic API streaming responses to the harness SSE event protocol. (Source: SOW-005, SOW-006; SPEC Section 9.8 — prompt mode selection.)

### REQ-05: Multimodal Content Block Formatting

The provider MUST support formatting multimodal content blocks (text + image/document content) for the Anthropic API when the harness turn pipeline provides them.

- Prompt mode selection: when attachments are present, the runtime builds multimodal content blocks. (Source: SPEC Section 9.8 — Prompt mode selection.)
- The provider receives pre-processed content blocks from the harness attachment resolver (DEL-04-01) and formats them for the Anthropic API.
- **Scope boundary (C-002):** This deliverable owns the formatting of content blocks into Anthropic API-compatible shapes. Attachment resolution, file reading, classification, and budget enforcement are owned by DEL-04-01 (PKG-04).

### REQ-06: Error Handling

The provider MUST handle and classify Anthropic API errors using a consistent error taxonomy:

| Error Category | Expected Behavior | Acceptance Criteria | Source |
|----------------|-------------------|---------------------|--------|
| Missing API key | Return a clear, actionable error to the UI; do not crash the runtime; LLM-dependent UI elements should indicate unavailability | Error message specifies that no API key is configured and directs operator to provisioning mechanism; non-LLM app functions remain operational (F-001) | **ASSUMPTION** |
| Invalid API key (authentication failure, 401) | Surface error with guidance to check/re-provision key | Error message indicates authentication failure and provides actionable re-provisioning guidance; key value is not included in the error (F-001) | **ASSUMPTION** |
| Rate limiting (429) | TBD — retry strategy or surface to user (A-002: define mandatory retry strategy or explicit no-retry policy) | TBD — acceptance criteria depend on retry policy decision | TBD |
| Network/connection errors | Surface error; respect Anthropic-only network policy (no fallback to other providers) | Error message indicates connectivity issue; no alternative provider is attempted | DEC-NET-001 |
| API response errors (4xx/5xx) | Surface error details to the user via harness event stream | Error details are surfaced without exposing API key material | **ASSUMPTION** |
| Request timeout / stream stall | TBD — handle requests that exceed a reasonable time limit or streams that stall mid-response (X-003) | TBD — timeout threshold and behavior to be defined | TBD |
| User cancellation (mid-stream) | TBD — handle operator-initiated cancellation of an in-progress streaming turn (X-003) | TBD — cancellation mechanism and cleanup behavior to be defined | TBD |

**Error taxonomy note (E-003):** The error categories above use a normalized taxonomy. "Missing API key" and "Invalid API key (authentication failure, 401)" are distinct categories: missing key means no key was configured; invalid key (401) means a key was provided but rejected by the Anthropic API. Downstream documents (Guidance, Procedure) must use these same category names consistently.

### REQ-07: Non-Project-Truth Storage Contract

The API key storage mechanism MUST satisfy DIRECTIVE Section 2.5:

- The key is **non-authoritative operator convenience state**.
- The key MUST NOT be treated as project truth.
- The key MUST NOT override contract/governance enforcement.
- The key MAY be stored outside project files (e.g., OS keychain, environment variable, app-local config).

Source: DIRECTIVE Section 2.5; Decomposition DEL-03-05.

**Ruling-bound storage contract:** For current scope, non-project-truth storage is satisfied via process environment only (`ANTHROPIC_API_KEY`), with no persisted local key store.

### REQ-08: Single Provider Constraint

The runtime MUST support exactly one LLM provider: Anthropic. No abstraction layer for multiple providers is required.

Source: DEC-NET-001 ("Outbound internet access is permitted **only** for **Anthropic API** calls"); SOW-043 states external system integration is OUT of scope, with an explicit exception for Anthropic API per DEC-NET-001 (C-001).

### REQ-09: API Key Log Protection

The provider module MUST ensure that API key material is never written to application logs, console output, error messages, or error telemetry.

- Error messages related to authentication failures MUST NOT include the key value or any substring of it.
- Log statements in the provider module MUST NOT include the key as a parameter.
- If error telemetry is added in the future, key material MUST be excluded from telemetry payloads.

Source: **ASSUMPTION: standard security practice for API key handling.** Supported by REQ-06 error handling (error messages must not expose key) and Procedure Step 2 item 3.4 ("do not expose the key value in error messages or logs"). *(Added per X-002.)*

### REQ-10: Request Timeout and Cancellation Handling

The provider MUST handle request timeout and user-initiated cancellation scenarios:

- **Timeout:** If a streaming response stalls beyond a configurable timeout threshold, the provider MUST terminate the request and surface a timeout error via the harness event stream. TBD — specific timeout value.
- **Cancellation:** If the user cancels a turn mid-stream, the provider MUST cleanly abort the in-progress Anthropic API request and release associated resources. TBD — cancellation signaling mechanism (depends on DEL-03-02 turn pipeline contract).
- In both cases, the provider MUST NOT leave orphaned connections or leaked resources.

Source: **ASSUMPTION: standard concern for streaming API integrations.** Procedure Step 5 mentions "stream interruption and cleanup" but no requirement previously governed it. *(Added per X-003.)*

## Standards

| Standard/Reference | Relevance | Accessible |
|--------------------|-----------|------------|
| Anthropic API documentation | API request/response shapes, authentication, streaming protocol, rate limits, API versioning | No (external; `location TBD`) |
| Anthropic Claude SDK (Node.js / TypeScript) | Mandatory implementation path for DEL-03-05 (`@anthropic-ai/sdk`) including initialization, streaming helpers, and error types. Current dependency pin: `0.78.0` | Partial (local dependency pin is in repo; upstream docs remain external) |
| docs/SPEC.md Section 9.8 | Harness turn input contract, model fallback, prompt mode selection | Yes |
| docs/DIRECTIVE.md Section 2.5 | Non-authoritative convenience state rules | Yes |
| docs/CONTRACT.md | K-GHOST-1, K-INVENT-1 invariants | Yes |

## Verification

| Requirement | Verification Approach | Verification Artifact |
|-------------|----------------------|----------------------|
| REQ-01 | Unit test: official Anthropic SDK client initializes with valid key; fails gracefully with invalid key. Inspection confirms DEL-03-05 completion evidence is SDK-backed (not direct HTTP-only) | TEST / CODE |
| REQ-02 | Unit test: key resolver retrieves key from environment (`ANTHROPIC_API_KEY`, optional compatibility alias) and returns appropriate error when absent | TEST |
| REQ-03 | Integration test: model from `opts.model` is used; fallback to default when omitted | TEST |
| REQ-04 | Integration test: harness turn request produces correct Anthropic API call; response is correctly translated. **Streaming integrity check (X-004):** verify that content reassembled from streamed SSE events matches what a non-streaming call would return for the same input | TEST |
| REQ-05 | Integration test: multimodal content blocks (text + image) are correctly formatted for Anthropic API | TEST |
| REQ-06 | Unit test: each error category (per normalized taxonomy) produces expected error event; runtime does not crash. **Acceptance criteria (F-001):** missing-key error specifies provisioning guidance; invalid-key error directs to re-provisioning; key value never appears in any error output | TEST |
| REQ-07 | Inspection: API key is not present in any file under working root; not committed to git. **Concrete method (A-003):** grep-based scan of `projectRoot` for key patterns + git history search; CI check recommended | TEST / DOC |
| REQ-08 | Inspection: no multi-provider abstraction exists; only Anthropic calls are made. **Enforcement (D-001):** static analysis or code review confirming no non-Anthropic outbound HTTP calls exist in the provider module | CODE / DOC |
| REQ-09 | Unit test: error outputs from authentication failures do not contain key material; log statement audit confirms no key parameters. Code review of all log/error paths in provider module | TEST / CODE |
| REQ-10 | Integration test: streaming response interrupted by timeout produces timeout error event; user cancellation aborts cleanly without resource leaks | TEST |

## Documentation

The following artifacts are anticipated for this deliverable:

| Artifact Type | Description |
|---------------|-------------|
| CODE | Provider module implementation (Anthropic SDK wrapper, key resolver, content block formatter, streaming adapter, error classifier) |
| TEST | Unit and integration tests covering REQ-01 through REQ-10 |
| DOC | API key provisioning guide for operators; provider module architecture notes |
