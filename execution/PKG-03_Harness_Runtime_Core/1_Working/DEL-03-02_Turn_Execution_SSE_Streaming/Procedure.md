# Procedure -- DEL-03-02 Turn Execution API + SSE Streaming

## Purpose

This procedure describes the steps to produce and verify the Turn Execution API + SSE Streaming deliverable (DEL-03-02). It covers implementation, testing, and documentation of the `/api/harness/turn` endpoint and its streaming behavior.

## Prerequisites

### Required Deliverables / Inputs

> **Lensing enrichment (A-004):** Prerequisite statuses below include concrete verification gates where possible. Where the gate cannot be specified from accessible sources, TBD markers remain with a note to define fallback instructions during Phase 1 assessment.

| Prerequisite | Source | Status | Verification Gate |
|-------------|--------|--------|-------------------|
| Session boot API operational (DEL-03-01) | Decomposition; SOW-004 | **ASSUMPTION:** DEL-03-01 must be at least partially complete for end-to-end testing of turns | Check: `POST /api/harness/session/boot` returns 200 with valid session ID. **Fallback:** If DEL-03-01 is not ready, text-only turn unit tests can proceed with a mock session; integration tests are blocked. |
| Anthropic provider integration available (DEL-03-05) | Decomposition; SOW-006 | **ASSUMPTION:** SDK integration must be available for turn execution to function | Check: Anthropic SDK package is installed and importable; API key is provisioned (OI-001). **Fallback:** If DEL-03-05 is not ready, mock the SDK `query()` call for unit/integration tests; end-to-end tests are blocked. |
| Turn options mapping layer available (DEL-03-03) | Decomposition; SOW-011 | **ASSUMPTION:** At minimum, a pass-through for `opts` must exist | Check: `opts` object can be passed to the mapping layer without error. **Fallback:** If DEL-03-03 is not ready, implement a minimal pass-through stub that returns `opts` unchanged; track stub in `_MEMORY.md`. |
| Attachment resolver available (DEL-04-01) | Decomposition; SOW-007, SOW-008 | **ASSUMPTION:** Required for attachment-capable turns; text-only turns may work without it | Check: Resolver function is callable with a file path array and returns resolved/rejected results. **Fallback:** If DEL-04-01 is not ready, implement text-only turn flow first; defer attachment integration tests. |

### Required References

| Reference | Location | Purpose |
|-----------|----------|---------|
| `docs/SPEC.md` Section 9.7-9.8 | `docs/SPEC.md` | Harness turn input contract, prompt mode selection, attachment rules |
| `docs/CONTRACT.md` | `docs/CONTRACT.md` | Binding invariants governing implementation |
| Anthropic SDK documentation | TBD -- resolve to actual URL or installed package reference before beginning Phase 2 (see F-002) | SDK `query()` API, streaming interface, tool calling protocol |
| Existing source code (if any) | TBD -- locate existing turn endpoint implementation during Step 1.1 | Current implementation state of the turn endpoint |

### Required Tools / Environment

| Tool | Purpose | Specifics |
|------|---------|-----------|
| Node.js / Next.js development environment | API route development | -- |
| Anthropic API key (provisioned per DEL-03-05 contract) | SDK calls during testing | Requires OI-001 resolution |
| macOS 15+ / Apple Silicon test machine | Platform verification (DEC-PLAT-001) | -- |
| SSE-capable test client | Verifying streaming responses | TBD -- identify specific library or tool (e.g., `eventsource`, `curl`, or test framework SSE support) before beginning Phase 3 testing (see X-005) |

## Steps

### Phase 1: Assessment and Planning

**Step 1.1 -- Assess Current Implementation State**

- Locate the existing `/api/harness/turn` route handler in the source code.
- Review current implementation against the requirements in `Specification.md`.
- Identify which requirements are already met, partially met, or unimplemented.
- Record findings in `_MEMORY.md`.

**Step 1.2 -- Define SSE Event Taxonomy**

- Based on Anthropic SDK streaming conventions (**ASSUMPTION: location TBD**), define the SSE event types that the turn endpoint will emit.
- At minimum, consider: turn lifecycle events (start, end), content events (delta, complete), tool events (use, result), and error events.
- Define clean stream termination criteria: final event type, connection close behavior, and timeout semantics (see Specification REQ-03 enrichment D-002).
- Define turn completion semantics: what constitutes a "complete" turn (see Guidance, Turn Completion Semantics section).
- Document the event taxonomy as part of the DOC artifact.

**Step 1.3 -- Identify Integration Points**

- Map the integration surface with each adjacent deliverable:
  - DEL-03-01: session validation (how to check session is active)
  - DEL-03-03: turn options mapping (how `opts` are forwarded and resolved)
  - DEL-03-04: subagent governance (how governance gate results are consumed -- see Guidance P5 for directional guidance on the boundary)
  - DEL-03-05: Anthropic provider (how SDK `query()` is invoked)
  - DEL-04-01: attachment resolver (how resolver is called and results consumed)
- Record integration contracts in `_MEMORY.md`.

### Phase 2: Implementation

**Step 2.1 -- Implement/Verify Turn Endpoint Route**

- Ensure `POST /api/harness/turn` route exists and accepts the request payload: `message`, `opts`, `attachments`.
- Implement request validation:
  - Reject if no session is active (see REQ-10 for failure response -- TBD).
  - Accept empty `message` when `attachments` are non-empty (REQ-09).
  - Pass `opts` to the turn options mapping layer (REQ-07).

**Step 2.2 -- Implement/Verify SSE Streaming Pipeline**

- Ensure the response is configured as an SSE stream (correct `Content-Type`, connection keep-alive, etc.).
- Implement the event emission pipeline:
  - Connect Anthropic SDK streaming output to SSE event emission.
  - Map SDK events to the defined SSE event taxonomy (Step 1.2).
  - Ensure events are flushed to the client in real time.
- Implement clean stream termination on turn completion (success or error) per the criteria defined in Step 1.2.

**Step 2.3 -- Implement/Verify Prompt Mode Selection**

- Implement the routing logic per REQ-05:
  - No attachments: use SDK `query({ prompt: string })`.
  - Attachments present: build multimodal content blocks and use SDK `query({ prompt: AsyncIterable<SDKUserMessage> })`.
- Ensure client-supplied attachment metadata is ignored (REQ-08); use server-side classification.

**Step 2.4 -- Implement/Verify Attachment Integration at Turn Level**

- Integrate with the attachment resolver (DEL-04-01) for server-side validation.
- Implement partial failure handling (REQ-06):
  - At least one resolved attachment (or user text): proceed with warning text block prepended.
  - All attachments fail + no user text: return HTTP 400 before opening SSE stream.

**Step 2.5 -- Implement/Verify Tool Calling and Permissions**

- Ensure tool call requests from the SDK are processed during turn execution.
- Enforce tool permissions per session configuration and `opts`.
- Emit tool-related events through the SSE stream (REQ-04).

**Step 2.6 -- Implement/Verify Error Handling**

- Pre-stream errors (validation failures, no session, full attachment failure): return standard HTTP error codes (see REQ-10, REQ-13 for specific scenarios -- TBD).
- Mid-stream errors (SDK failures, tool errors): emit error events through the SSE stream (see REQ-12 for error event schema -- TBD).
- Client disconnect: detect and clean up (terminate SDK call, release resources -- see Guidance P1 for rationale and resource inventory).

### Phase 3: Testing

**Step 3.1 -- Unit Tests**

- Test prompt mode selection logic in isolation (REQ-05).
- Test request validation logic (empty message acceptance, attachment array handling).
- Test error classification (pre-stream vs. mid-stream).

**Step 3.2 -- Integration Tests**

- Test end-to-end turn execution with a text-only message (REQ-01, REQ-02, REQ-03).
- Test turn execution with attachments: valid, partially failing, fully failing (REQ-06).
- Test `opts` acceptance and forwarding to mapping layer (REQ-07).
- Test SSE event delivery: verify events arrive at client in correct order and timing (REQ-03).
- Test tool calling during a turn (REQ-04).
- Test client-supplied metadata reclassification: submit specific metadata field values and verify server reclassifies each independently (REQ-08; see C-002 for test vector guidance).

**Step 3.3 -- Edge Case Tests**

- Empty message with valid attachments (REQ-09).
- All attachments fail with empty message -> HTTP 400 (REQ-06).
- Client disconnect mid-stream.
- Very large tool call results within a streaming turn.
- Turn with no `opts` provided (defaults apply).
- Session not active -> pre-stream error (REQ-10 -- TBD: define expected response).
- API key not provisioned -> pre-stream error (REQ-13 -- TBD: requires OI-001 resolution).
- Concurrent turn submission for same session (REQ-11 -- TBD: requires policy decision).

**Step 3.4 -- Platform Verification**

- Run integration tests (Step 3.2) and edge case tests (Step 3.3) on macOS 15+ / Apple Silicon (DEC-PLAT-001).
- Verify SSE streaming works within the Electron desktop app context.
- **Scope clarification (D-003):** Platform verification runs the full integration and edge case test suites (Steps 3.2 and 3.3) on the target platform. Unit tests (Step 3.1) are platform-independent and do not require rerun. Pass criteria: all integration and edge case tests pass with no platform-specific failures.

### Phase 4: Documentation

**Step 4.1 -- API Documentation**

- Document the `/api/harness/turn` endpoint: request schema, response behavior, error codes.
- Document the SSE event taxonomy: event names, payload schemas, sequencing.

**Step 4.2 -- Integration Notes**

- Document integration contracts with adjacent deliverables (DEL-03-01, DEL-03-03, DEL-03-04, DEL-03-05, DEL-04-01).
- Update `_MEMORY.md` with implementation decisions and findings.

## Verification

| Check | Method | Pass Criteria |
|-------|--------|---------------|
| Turn endpoint accepts valid requests | Integration test (Step 3.2) | POST returns SSE stream with 200 status |
| SSE events stream in real time | Integration test (Step 3.2) | Events arrive at client during turn execution, not batched at end |
| Prompt mode selected correctly | Unit test (Step 3.1) | String mode for text-only; multimodal mode for attachments |
| Partial attachment failure handled | Integration test (Step 3.2) | Turn proceeds with warning; response includes warning text |
| Full attachment failure rejected | Edge case test (Step 3.3) | HTTP 400 returned when all fail + no text |
| Tool calls processed | Integration test (Step 3.2) | Tool use/result events appear in stream |
| Stream terminates cleanly | Integration test (Step 3.2) | Final event received per defined termination criteria (Step 1.2); connection closes |
| Client disconnect handled | Edge case test (Step 3.3) | Server detects disconnect; resources released |
| Client metadata reclassified | Integration test (Step 3.2) | Server ignores client-supplied metadata fields individually |
| Platform verification | Platform test (Step 3.4) | All integration and edge case tests pass on macOS 15+ Apple Silicon |

## Records

| Record | Location | Purpose |
|--------|----------|---------|
| Implementation decisions | `_MEMORY.md` | Working context for future sessions |
| Test results | TBD -- define output location during Phase 1 assessment (e.g., `test-results/` or CI artifact path; see F-003) | Evidence of verification |
| API documentation | TBD -- define DOC artifact location during Phase 4 (e.g., `docs/api/harness-turn.md` or within deliverable folder; see F-003) | Developer reference |
| SSE event taxonomy | TBD -- define DOC artifact location during Phase 4 (e.g., alongside API documentation; see F-003) | Contract for UI consumers |
| `_STATUS.md` updates | `_STATUS.md` | Lifecycle state transitions |
