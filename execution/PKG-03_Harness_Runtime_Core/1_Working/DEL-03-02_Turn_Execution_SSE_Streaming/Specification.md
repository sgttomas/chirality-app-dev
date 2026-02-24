# Specification -- DEL-03-02 Turn Execution API + SSE Streaming

## Scope

### Included

This deliverable covers the implementation and verification of the `/api/harness/turn` API endpoint and its SSE streaming behavior, ensuring turns execute end-to-end from the desktop UI with real-time event delivery. Specifically:

- The `POST /api/harness/turn` API route accepts a turn request and returns a streaming SSE response.
- The runtime executes the turn against the Anthropic SDK, performing tool calling and permission enforcement during execution.
- Events are streamed to the UI in real time via SSE during turn execution.
- Prompt mode selection routes correctly based on whether attachments are present or absent.
- The endpoint accepts optional `attachments` (array of absolute filesystem path strings) and optional `opts` (turn options object).
- Attachment validation is performed server-side per the resolver contract.
- Partial attachment failure is non-fatal when executable content remains; full failure with no content returns HTTP 400.

**Source:** SOW-004, SOW-005, SOW-006; SPEC.md Section 9.8; Decomposition DEL-03-02.

### Excluded

| Exclusion | Rationale | Owner |
|-----------|-----------|-------|
| Session boot (`/api/harness/session/*`) | Covered by DEL-03-01 | DEL-03-01 |
| Turn options mapping and fallback chain logic (detailed) | Covered by DEL-03-03 | DEL-03-03 |
| Subagent governance fail-closed enforcement (detailed) | Covered by DEL-03-04 | DEL-03-04 |
| Anthropic provider integration and key provisioning | Covered by DEL-03-05 | DEL-03-05 |
| Outbound network guardrails enforcement | Covered by DEL-03-06 | DEL-03-06 |
| Attachment resolver implementation (classification, budget) | Covered by DEL-04-01 | DEL-04-01 |
| UI attachment pipeline (picker, preview, rollback) | Covered by DEL-04-02 | DEL-04-02 |

### Boundary Notes

This deliverable is the **integration point** for turn execution. It depends on outputs from DEL-03-01 (session must be active), consumes the attachment resolver from DEL-04-01, applies options from DEL-03-03, respects governance from DEL-03-04, and calls the Anthropic provider from DEL-03-05. The focus here is on the turn endpoint itself, the SSE streaming pipeline, and the end-to-end execution flow -- not on the detailed implementation of each subsystem it integrates.

## Requirements

### REQ-01: Turn Endpoint Exists and Accepts Requests

The system MUST expose a `POST /api/harness/turn` endpoint that accepts:
- `message` (string): user text content; MAY be empty when attachments are present.
- `opts` (object, optional): turn options for runtime mapping.
- `attachments` (array of strings, optional): absolute filesystem paths.

**Source:** SPEC.md Section 9.8; SOW-004.

### REQ-02: End-to-End Turn Execution

A turn request MUST execute the following sequence:
1. Validate that a session is active (precondition from DEL-03-01).
2. Resolve attachments server-side if provided (integration with DEL-04-01 resolver).
3. Select prompt mode based on attachment presence (REQ-05).
4. Call the Anthropic SDK to execute the turn.
5. Stream events to the client via SSE (REQ-03).
6. Handle tool calls and permissions during execution (SOW-006).
7. Complete the turn and finalize the SSE stream.

**Source:** SOW-004, SOW-006; SPEC.md Section 9.8; Decomposition DEL-03-02.

### REQ-03: SSE Streaming Protocol

The turn endpoint MUST stream events to the UI using Server-Sent Events (SSE) during turn execution.

- Events MUST be delivered in real time as the runtime produces them.
- The SSE connection MUST be maintained for the duration of the turn.
- The stream MUST terminate cleanly when the turn completes (success or error).
- **ASSUMPTION:** Specific SSE event type taxonomy (event names, payload schemas) is TBD -- not fully specified in accessible sources. Implementation should follow Anthropic SDK streaming conventions.

> **Lensing enrichment (A-001):** A prescriptive SSE event taxonomy (event names, payload schemas, sequencing constraints) SHOULD be defined as part of the DOC artifact for this deliverable. The taxonomy is TBD and should be resolved during Step 1.2 of the Procedure. **Source:** SOW-005; PLAN.md Section 2.

> **Lensing enrichment (A-002):** The ASSUMPTION tag on SSE event taxonomy above should be resolved with either a concrete requirement or a tracked TBD with explicit resolution criteria (e.g., "resolve during implementation Phase 1, before integration testing").

> **Lensing enrichment (D-002):** Clean stream termination criteria are TBD. "Terminates cleanly" SHOULD be defined to include: (a) a specific final event type (e.g., `turn_end`), (b) connection close behavior, and (c) timeout semantics for abnormal termination. **Source:** Specification REQ-03 (self-referential gap).

**Source:** SOW-005; PLAN.md Section 2.

### REQ-04: Tool Calling and Permissions

During turn execution, the runtime MUST:
- Process tool call requests from the Anthropic SDK response.
- Enforce tool permissions per the session configuration and `opts`.
- Stream tool-related events as part of the SSE event stream.

**Source:** SOW-006; SPEC.md Section 9.8.

### REQ-05: Prompt Mode Selection

The runtime MUST select the correct prompt mode based on attachment presence:

| Condition | Prompt Mode | Source |
|-----------|-------------|--------|
| No attachments | SDK `query({ prompt: string })` | SPEC.md Section 9.8 |
| Attachments present | SDK `query({ prompt: AsyncIterable<SDKUserMessage> })` with multimodal content blocks | SPEC.md Section 9.8 |

**Source:** SPEC.md Section 9.8.

### REQ-06: Attachment Handling at Turn Level

When `attachments` are provided:
- Server-side resolver validates: supported extensions, `isFile()`, per-file size limit (10 MB), total budget (18 MB raw / ~24 MB base64).
- **Partial failure:** If at least one attachment resolves (or user text exists), runtime MUST proceed and prepend a warning text block to user content.
- **Full failure:** If all attachments fail and user text is empty, the endpoint MUST return HTTP 400.

**Note:** Resolver implementation details are DEL-04-01 scope. This requirement covers the turn endpoint's integration with the resolver and its response behavior.

**Source:** SPEC.md Section 9.8.

### REQ-07: Turn Options Acceptance

The endpoint MUST accept an `opts` object and pass it to the runtime option mapping layer.

- Omitted `opts` fields MUST follow runtime fallback chains.
- **ASSUMPTION:** Detailed fallback chain logic (model, tools, maxTurns) is implemented in DEL-03-03; this deliverable ensures the plumbing accepts and forwards `opts`.

**Source:** SPEC.md Section 9.8; SOW-004.

### REQ-08: Client-Supplied Metadata Non-Authoritative

Client-supplied attachment metadata (name, mime, type) MUST NOT be trusted for execution. Server-side classification is authoritative.

**Source:** SPEC.md Section 9.8.

### REQ-09: Empty Message with Attachments

A turn MAY omit text when attachments are present (`message.trim() === ""` with non-empty `attachments`). The endpoint MUST accept this as a valid request.

**Source:** SPEC.md Section 9.8.

### REQ-10: Session Validation Failure Response (TBD)

> **Lensing enrichment (X-004):** When REQ-02 step 1 (session validation) fails, the endpoint MUST return an appropriate HTTP error response **before** opening the SSE stream. The specific HTTP status code and error body are TBD -- not specified in accessible sources. **ASSUMPTION:** HTTP 4xx (likely 400 or 409) with a descriptive error body is expected behavior.

**Source:** Specification REQ-02 step 1 (inferred gap).

### REQ-11: Concurrent Turn Handling (Single In-Flight Per Session)

The endpoint MUST enforce single-turn-at-a-time per session:

- If a second `POST /api/harness/turn` request arrives for a session with an active in-flight turn, the endpoint MUST reject it pre-stream with HTTP `409`.
- The rejection payload MUST use typed error `TURN_IN_PROGRESS`.
- The active-turn lock MUST be released when the in-flight turn completes or is interrupted so subsequent turns can proceed.

**Source:** DEL-03-02 implementation contract (2026-02-24) aligned to Guidance C4.

### REQ-12: Error Event Schema (TBD)

> **Lensing enrichment (B-003):** The endpoint SHOULD define an error event schema for mid-stream errors, including: event name, payload fields (error type, message, severity), and behavior on fatal vs. non-fatal errors. This schema is TBD -- not specified in accessible sources. See also Guidance C2 for the distinction between pre-stream and mid-stream errors.

**Source:** Guidance C2 (contextual); no normative source specifies the error event format.

### REQ-13: API Key Absence Pre-Stream Rejection

When provider mode resolves to Anthropic and no API key is configured, the endpoint MUST reject the request before opening SSE:

- Status code: HTTP `503`
- Error type: `MISSING_API_KEY`
- Error message: actionable guidance to set `ANTHROPIC_API_KEY`

Accepted key sources follow the DEL-03-05 key policy contract:

- Canonical: `ANTHROPIC_API_KEY`
- Compatibility fallback: `CHIRALITY_ANTHROPIC_API_KEY`

**Source:** DEL-03-05 key provisioning contract (`ENV_ONLY`, OI-001 resolved 2026-02-23); DEL-03-02 route contract (2026-02-24).

## Performance and Quality Attributes (TBD)

> **Lensing enrichment (A-005, A-006):** The following performance and quality attribute targets are TBD -- not specified in accessible sources. They SHOULD be defined to enable operative assessment and quality determination.

| Attribute | Target | Status | Source |
|-----------|--------|--------|--------|
| Time-to-first-SSE-event | TBD | Not specified | Guidance C5 (contextual) |
| SSE event throughput | TBD | Not specified | Guidance C5 (contextual) |
| SSE event delivery latency | TBD | Not specified | Guidance C5 (contextual) |
| Stream completion reliability target | TBD | Not specified | -- |
| Maximum acceptable event loss rate | TBD | Not specified | -- |

## Standards

| Standard / Reference | Applicability | Accessible |
|---------------------|---------------|------------|
| `docs/SPEC.md` Section 9.7-9.8 | Harness turn input contract, prompt mode, attachment rules, delegation governance | Yes |
| `docs/CONTRACT.md` K-invariants | K-INVENT-1 (no guessing), K-GHOST-1 (sealed context), K-STATUS-1 (lifecycle) | Yes |
| `docs/DIRECTIVE.md` | Founding intent, no external DB, filesystem-as-state | Yes |
| Anthropic SDK documentation | SDK `query()` API, streaming interface, tool calling protocol | **ASSUMPTION: likely applicable; location TBD** (see E-001) |
| Server-Sent Events specification (W3C / WHATWG) | SSE protocol semantics | **ASSUMPTION: likely applicable; location TBD** (see E-001) |
| Next.js API route conventions | Route handler patterns for streaming responses | **ASSUMPTION: likely applicable; location TBD** (see E-001) |

> **Lensing enrichment (E-001):** The three external standards marked as ASSUMPTION above should be either confirmed with specific locations/versions or explicitly excluded with rationale. Resolution criteria: confirm applicability and provide URLs or package references before integration testing begins.

## Verification

| Req ID | Verification Approach | Notes |
|--------|----------------------|-------|
| REQ-01 | Test: send POST to `/api/harness/turn` with valid payload; confirm 200/stream response | Integration test |
| REQ-02 | Test: execute a complete turn from request to stream completion; verify all steps occur | End-to-end test; requires active session (DEL-03-01) |
| REQ-03 | Test: verify SSE events are delivered in real time; stream terminates on completion; verify clean termination criteria (once defined per D-002) | Observe event timing; test normal and error completion |
| REQ-04 | Test: submit a turn that triggers tool calls; verify tool execution and permission enforcement | Requires tool-calling scenario |
| REQ-05 | Test: submit turn without attachments, confirm string prompt mode; submit with attachments, confirm multimodal prompt mode | Unit/integration test on prompt construction |
| REQ-06 | Test: partial attachment failure with valid text proceeds with warning; all-fail + no text returns 400 | Integration test with resolver |
| REQ-07 | Test: submit `opts` and confirm they reach the runtime mapping layer; omit `opts` and confirm defaults apply | Integration test |
| REQ-08 | Test: submit client metadata with specific field values (name, mime, type); verify server reclassifies each field independently and ignores client values | Integration test; test vectors SHOULD cover each metadata field individually (see C-002) |
| REQ-09 | Test: submit empty message with valid attachments; confirm acceptance | Edge case test |
| REQ-10 | Test: submit turn request when no session is active; verify pre-stream HTTP error response with correct status code and body | Integration test (TBD: define expected status code) |
| REQ-11 | Test: submit a second turn while one is in-flight for the same session; verify HTTP 409 + `TURN_IN_PROGRESS`, then verify lock release permits a subsequent turn | Integration test |
| REQ-12 | Test: trigger mid-stream errors (SDK failure, tool error); verify error events conform to defined schema | TBD: requires error event schema definition |
| REQ-13 | Test: with `CHIRALITY_HARNESS_PROVIDER=anthropic` and no configured key, submit turn request and verify HTTP 503 + `MISSING_API_KEY` pre-stream response | Integration test |

## Traceability Matrix

> **Lensing enrichment (E-003):** Consolidated traceability from requirements to scope items and objectives.

| Req ID | SOW Item(s) | Objective(s) | Notes |
|--------|-------------|------------|-------|
| REQ-01 | SOW-004 | OBJ-002 | Endpoint existence |
| REQ-02 | SOW-004, SOW-006 | OBJ-002 | End-to-end execution sequence |
| REQ-03 | SOW-005 | OBJ-002 | SSE streaming protocol |
| REQ-04 | SOW-006 | OBJ-002 | Tool calling and permissions |
| REQ-05 | SOW-004 | OBJ-002 | Prompt mode selection (integration with DEL-04-01) |
| REQ-06 | SOW-004 | OBJ-002, OBJ-003 | Attachment handling at turn level (integration with DEL-04-01) |
| REQ-07 | SOW-004 | OBJ-002 | Turn options acceptance (integration with DEL-03-03) |
| REQ-08 | SOW-004 | OBJ-002 | Server-side authority for metadata |
| REQ-09 | SOW-004 | OBJ-002 | Empty message edge case |
| REQ-10 | SOW-004 | OBJ-002 | Session validation failure (TBD) |
| REQ-11 | SOW-004 | OBJ-002 | Concurrent turn handling (`409 TURN_IN_PROGRESS`; lock release on completion/interrupt) |
| REQ-12 | SOW-005, SOW-006 | OBJ-002 | Error event schema (TBD) |
| REQ-13 | SOW-006 | OBJ-002 | API key absence pre-stream rejection (`503 MISSING_API_KEY`) |

**Coverage assessment:** SOW-004, SOW-005, SOW-006 each have at least one requirement mapping. OBJ-002 acceptance criteria (session/turn endpoints, SSE streaming, options mapping, governance, network policy) are addressed by the requirement set, noting that options mapping (DEL-03-03), governance (DEL-03-04), and network policy (DEL-03-06) are excluded from this deliverable's scope. **ASSUMPTION:** Full OBJ-002 coverage requires all PKG-03 deliverables collectively.

## Documentation

### Required Artifacts (from `_CONTEXT.md`)

| Artifact Type | Description | Status |
|---------------|-------------|--------|
| CODE | Turn execution API route implementation; SSE streaming pipeline | TBD |
| TEST | Integration/end-to-end tests for turn execution and streaming | TBD |
| DOC | API documentation for `/api/harness/turn` endpoint and SSE event protocol (including event taxonomy per A-001) | TBD |
