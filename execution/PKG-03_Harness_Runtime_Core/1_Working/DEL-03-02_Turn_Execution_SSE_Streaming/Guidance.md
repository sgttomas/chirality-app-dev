# Guidance -- DEL-03-02 Turn Execution API + SSE Streaming

## Purpose

This deliverable exists because the Chirality desktop app needs a reliable, streaming turn execution pipeline. The harness runtime accepts a user's turn (message + optional attachments + options), executes it against the Anthropic API, and streams events back to the UI in real time. Without this, the desktop app cannot function as an interactive AI harness.

DEL-03-02 is the central integration point in PKG-03 (Harness Runtime Core). It connects session management (DEL-03-01), option mapping (DEL-03-03), subagent governance (DEL-03-04), provider integration (DEL-03-05), and attachment resolution (DEL-04-01) into a single end-to-end flow. Its correctness is a prerequisite for the UI's ability to display streaming agent responses.

**Source:** Decomposition DEL-03-02; SOW-004, SOW-005, SOW-006; OBJ-002.

## Principles

### P1: Streaming-First Architecture

The turn endpoint is designed around SSE streaming, not request-response. The UI receives events as the runtime produces them. This means:

- The response is a long-lived HTTP connection, not a single JSON payload.
- Error handling must work within a streaming context (errors mid-stream are different from errors before streaming starts).
- Client disconnection should be handled gracefully (the runtime should detect and clean up).

> **Lensing enrichment (B-004):** Client disconnect handling rationale: The detect-and-cleanup approach is chosen because an abandoned SSE connection leaves the Anthropic SDK call in flight, consuming API quota and potentially producing tool-call side effects against the filesystem. On client cancellation, the runtime SHOULD abort the in-flight SDK call and release associated resources (open file handles, in-progress tool executions). The expected SDK behavior on cancellation is TBD -- depends on Anthropic SDK cancellation API (**ASSUMPTION: location TBD**). The specific resources at risk include: (a) the active Anthropic API request/connection, (b) any in-progress tool executions that may be writing to the filesystem, and (c) the SSE connection itself.

**Source:** SOW-005; PLAN.md Section 2 (SSE streaming).

### P2: Server-Side Authority

The turn endpoint enforces a clear trust boundary:

- Client-supplied metadata (attachment names, MIME types) is non-authoritative. The server reclassifies everything.
- The UI sends paths; the server reads, validates, and classifies files.
- Runtime option mapping and fallback chains are server-side logic, not client logic.
- Governance enforcement (subagent gates, permission checks) is server-side.

This follows the DIRECTIVE's principle that the filesystem is the state and the server is the authority for runtime behavior.

**Source:** SPEC.md Section 9.8; DIRECTIVE.md Section 2.1.

### P3: Fail-Open for Partial Content, Fail-Closed for No Content

The attachment handling model distinguishes between degraded-but-usable and completely-empty turns:

- If some attachments fail but the turn still has content (text or other resolved attachments), the runtime proceeds with a warning.
- If all attachments fail and there is no text, the turn is rejected (400).

This avoids both silent data loss (proceeding with no content at all) and unnecessary rigidity (rejecting a turn because one of several attachments had an issue).

**Source:** SPEC.md Section 9.8.

### P4: Separation of Concerns Across PKG-03 Deliverables

DEL-03-02 is an integration deliverable. It should not re-implement logic owned by adjacent deliverables:

| Concern | Owner | DEL-03-02 Role |
|---------|-------|----------------|
| Session lifecycle | DEL-03-01 | Assumes session is active; validates precondition |
| Turn options mapping + fallback | DEL-03-03 | Accepts `opts`; passes to mapping layer |
| Subagent governance | DEL-03-04 | Respects governance gate results; does not implement gate logic |
| Anthropic provider + key | DEL-03-05 | Calls provider; does not manage key provisioning |
| Network guardrails | DEL-03-06 | Operates within policy; does not enforce egress rules |
| Attachment resolver | DEL-04-01 | Calls resolver; handles partial/full failure at turn level |

**Source:** Decomposition PKG-03, PKG-04 deliverable table.

### P5: Subagent Governance Boundary at Turn Level

> **Lensing enrichment (D-001):** The turn endpoint's relationship to subagent governance requires directional clarification. The decomposition assigns enforcement to DEL-03-04 and this deliverable's Specification excludes detailed governance logic. However, the turn endpoint is the execution context in which governance gate results are consumed. The prescriptive direction is:

- DEL-03-02 SHOULD **consume** governance gate outputs (pass/fail signals) but SHOULD NOT implement the gate logic itself.
- When the governance gate reports "blocked" (fail-closed), the turn endpoint SHOULD prevent subagent injection and allow the parent agent to continue.
- The exact contract between DEL-03-02 and DEL-03-04 (function signature, return type, error propagation) is TBD -- to be resolved when both deliverables are under active development.

**Source:** SPEC.md Section 9.7 (delegation governance rule); Datasheet Attributes (Subagent Governance row); Decomposition DEL-03-04.

## Considerations

### C1: SSE Event Taxonomy

This deliverable now uses the following event taxonomy for `/api/harness/turn`:

- `session:init` - turn stream initialized with provider/session metadata
- `chat:delta` - incremental assistant text
- `chat:complete` - final assistant text
- `tool:result` - tool execution result surfaced by runtime
- `session:complete` - turn flow complete at runtime level
- `turn:error` - typed mid-stream error event (REQ-12 contract)
- `process:exit` - terminal stream disposition (`exitCode`/interrupt/failure metadata)

**Status:** RESOLVED in implementation + tests.

### C2: Error Handling in Streaming Context

Errors during a streaming turn present different challenges than pre-stream errors:

- **Pre-stream errors** (invalid request, session not active, full attachment failure, missing Anthropic key in provider mode): respond with standard HTTP error codes before opening the SSE stream.
- **Mid-stream errors** (SDK failure, tool execution error, network interruption): are communicated with `turn:error` payloads because HTTP status has already been sent (200).
- **Client disconnect**: the server should detect and terminate the turn cleanly to avoid resource leaks.

Session validation taxonomy for turn start is now explicit:

- Unknown/missing turn `sessionId` returns pre-stream HTTP `404` with typed error `SESSION_NOT_FOUND` and `error.details.sessionId`.

Fatal/non-fatal rule:

- Fatal mid-stream errors emit `turn:error` with `fatal=true`, then `process:exit` with non-zero `exitCode`, then stream close.
- Non-fatal mid-stream errors (if used) emit `turn:error` with `fatal=false` and stream continuation is allowed.

**Status:** RESOLVED for fatal path; non-fatal path codified as contract for forward compatibility.

### C3: Anthropic SDK Integration Surface

The turn execution flow depends on the Anthropic SDK's `query()` method with two prompt modes. Key integration questions:

- How does the SDK surface streaming events? (stream of typed events, async iterator, callback-based?)
- What is the SDK's tool-calling protocol? (tool_use content blocks, tool_result responses?)
- How are SDK-level errors surfaced during streaming?

**ASSUMPTION:** The Anthropic SDK provides a streaming interface compatible with SSE event delivery. Specific SDK API details are not available in the accessible governance documents.

### C4: Concurrent Turn Handling

Concurrent turn handling is codified for this deliverable:

- The endpoint enforces one in-flight turn per session.
- A second overlapping turn is rejected pre-stream with HTTP `409` and typed error `TURN_IN_PROGRESS`.
- Session lock release occurs on stream completion and interrupt so follow-on turns are not starved.

Reference implementation: `frontend/src/app/api/harness/turn/route.ts` and `frontend/src/__tests__/api/harness/routes.test.ts`.

### C5: Performance and Backpressure

SSE streaming to an Electron desktop app over localhost should have minimal latency, but consider:

- Whether the SSE implementation needs backpressure handling (unlikely for localhost, but worth considering for robustness).
- Whether large tool call results or long-running tool executions need progress events.
- Whether the UI can handle high-frequency events without rendering degradation.

**Status:** TBD -- performance requirements not specified in accessible sources.

### C6: Network Policy Verification Scope at Turn Level

> **Lensing enrichment (C-001):** The turn endpoint's obligation with respect to the outbound network policy (DEC-NET-001: Anthropic API only) is unclear. The Datasheet lists DEC-NET-001 as a condition, and the Specification exclusions assign enforcement to DEL-03-06. The question is whether DEL-03-02 has any verification or detection obligation at the turn level, or whether it simply operates within the policy enforced by DEL-03-06.

**Directional guidance:** DEL-03-02 SHOULD NOT duplicate network enforcement logic (that is DEL-03-06 scope). However, if the turn endpoint can detect an obvious policy violation (e.g., an SDK configuration pointing to a non-Anthropic endpoint), it SHOULD log or surface this as a pre-stream error rather than silently proceeding. The specific contract is TBD. **Source:** Datasheet Conditions; Specification Excluded (DEL-03-06).

## Vocabulary Note

> **Lensing enrichment (X-003):** The turn options object is referred to with minor variations across documents:
> - Datasheet: "Turn options object with runtime option mapping"
> - Specification: "`opts` (object, optional): turn options for runtime mapping"
> - Guidance: "`opts`" and "options mapping"
>
> **Standardized term:** The canonical reference SHOULD be **`opts`** (the field name) when referring to the request payload field, and **"turn options"** when referring to the concept. "Options mapping" refers to the runtime processing of `opts` by DEL-03-03. Documents in this set have been normalized to this convention where feasible.

## Trade-offs

### T1: Thin Integration Layer vs. Rich Turn Orchestration

| Option | Description | Pros | Cons |
|--------|-------------|------|------|
| **Thin layer** | DEL-03-02 is a thin pass-through that wires together session, options, resolver, SDK, and streaming | Clear separation of concerns; easier to test each subsystem independently | Turn-level error coordination may be complex if distributed across many modules |
| **Rich orchestrator** | DEL-03-02 owns the full turn lifecycle and inlines some logic | Easier to reason about the complete turn flow in one place | Risks duplicating or conflicting with DEL-03-03, DEL-03-04, DEL-04-01 scope |

**ASSUMPTION:** The thin integration layer approach aligns better with the decomposition's separation into distinct deliverables. The turn endpoint should be a coordinator, not a monolith.

### T2: SSE vs. WebSocket for Streaming

| Option | Description | Rationale |
|--------|-------------|-----------|
| **SSE (chosen)** | Server-Sent Events over HTTP | Unidirectional server-to-client fits the turn model; simpler than WebSocket; native browser support; aligns with Next.js API route patterns |
| **WebSocket** | Full-duplex connection | Not needed -- client sends one request and receives a stream of events; additional complexity for no benefit in this use case |

The decomposition and PLAN.md explicitly specify SSE. This is not a decision to revisit.

**Source:** SOW-005; PLAN.md Section 2.

## Examples

No concrete code examples are available in the accessible reference materials. The following illustrative patterns are drawn from the governance document descriptions.

### Example: Turn Request Shape (Illustrative)

Based on SPEC.md Section 9.8:

```
POST /api/harness/turn
Content-Type: application/json

{
  "message": "Analyze the project structure and suggest improvements.",
  "opts": {
    "model": "claude-sonnet-4-20250514",
    "maxTurns": 5
  },
  "attachments": [
    "/Users/operator/project/docs/requirements.md",
    "/Users/operator/project/diagrams/architecture.png"
  ]
}
```

**Note:** Exact payload schema is TBD; this is illustrative based on SPEC.md descriptions.

### Example: SSE Event Stream

```
event: session:init
data: {"claudeSessionId":"claude_123","model":"claude-sonnet-test"}

event: chat:delta
data: {"text":"Based on my analysis..."}

event: tool:result
data: {"name":"Read","ok":true,"output":"..."}

event: chat:complete
data: {"text":"Based on my analysis..."}

event: session:complete
data: {}

event: process:exit
data: {"exitCode":0}
```

Failure-mode addition: fatal stream failures emit `turn:error` before `process:exit`.

## Success Metrics

> **Lensing enrichment (C-003):** The following defines what constitutes a successful implementation of this deliverable, beyond test pass/fail.

| Metric | Target | Measurement | Status |
|--------|--------|-------------|--------|
| End-to-end turn completion | A text-only turn executes from request to final SSE event with all steps in REQ-02 | Integration test | TBD |
| Attachment-capable turn | A turn with valid attachments selects multimodal prompt mode and streams results | Integration test | TBD |
| Failure mode correctness | Pre-stream errors return HTTP error codes; mid-stream errors emit error events | Test coverage of error paths | TBD |
| All REQ-* verifications pass | REQ-01 through REQ-10 verification approaches produce passing results | Verification table | TBD |
| DOC artifact produced | API documentation + SSE event taxonomy are complete and internally consistent | Review | TBD |

## Turn Completion Semantics

A turn is complete when:

- Runtime emits terminal stream disposition via `process:exit`.
- Success path includes `session:complete` then `process:exit` with `exitCode=0`.
- Fatal failure path includes `turn:error` (`fatal=true`) then `process:exit` with non-zero `exitCode`.
- SSE connection closes after terminal `process:exit`.

## Conflict Table (for human ruling)

| Conflict ID | Conflict | Source A | Source B | Impacted Sections | Proposed Authority (PROPOSAL) | Human Ruling |
|-------------|----------|----------|----------|-------------------|-------------------------------|-------------|
| CF-001 | Network policy verification scope at turn level: does DEL-03-02 have any verification obligation for DEC-NET-001, or is this purely DEL-03-06 scope? | Datasheet Conditions (DEC-NET-001 listed) | Specification Excluded (DEL-03-06 owns enforcement) | Guidance C6; Specification Scope | Human ruling needed: clarify DEL-03-02 vs DEL-03-06 boundary for network policy | TBD |
