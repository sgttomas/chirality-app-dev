# Datasheet -- DEL-03-02 Turn Execution API + SSE Streaming

## Identification

| Field | Value |
|-------|-------|
| **Deliverable ID** | DEL-03-02 |
| **Name** | Turn Execution API + SSE Streaming |
| **Package** | PKG-03 Harness Runtime Core |
| **Type** | BACKEND_FEATURE_SLICE |
| **Context Envelope** | M |
| **Responsible Party** | TBD (OI: ownership not yet assigned -- see E-002) |
| **Scope Items** | SOW-004, SOW-005, SOW-006 |
| **Objectives** | OBJ-002 (**ASSUMPTION:** best-effort mapping via PKG-03 package grouping) |
| **Anticipated Artifacts** | CODE / TEST / DOC |

## Attributes

| Attribute | Value | Source |
|-----------|-------|--------|
| **API Endpoint** | `POST /api/harness/turn` | SPEC.md Section 9.8 |
| **Protocol** | Server-Sent Events (SSE) | Decomposition DEL-03-02; PLAN.md Section 2 |
| **Transport** | HTTP (Next.js API route within Electron desktop app) | PLAN.md Section 2 (Next.js + Electron) |
| **Input: Message** | User-provided text string; MAY be empty when attachments are present | SPEC.md Section 9.8 |
| **Input: Turn options (`opts`)** | Turn options object with runtime option mapping; accepted and forwarded to mapping layer (see DEL-03-03) | SPEC.md Section 9.8 |
| **Input: Attachments** | Optional array of absolute filesystem path strings | SPEC.md Section 9.8 |
| **Output: Event Stream** | SSE event stream from runtime to UI during turn execution | SOW-005; SPEC.md Section 9.8 |
| **Runtime Responsibilities** | Tool calling, permissions, event streaming | SOW-006 |
| **Prompt Mode (no attachments)** | SDK `query({ prompt: string })` | SPEC.md Section 9.8 |
| **Prompt Mode (attachments)** | SDK `query({ prompt: AsyncIterable<SDKUserMessage> })` with multimodal content blocks | SPEC.md Section 9.8 |
| **Attachment Validation** | Server-side resolver: extensions, `isFile()`, per-file limit (10 MB), total budget (18 MB raw / ~24 MB base64) | SPEC.md Section 9.8 |
| **Partial Failure Behavior** | Non-fatal when turn still has executable content; prepends warning text block | SPEC.md Section 9.8 |
| **Full Failure (no content)** | Rejected with HTTP 400 | SPEC.md Section 9.8 |
| **Network Policy** | Outbound connections limited to Anthropic API only (DEC-NET-001) | Decomposition DEC-NET-001; SOW-006 |
| **Subagent Governance** | Fail-closed: injection blocked when governance metadata absent/invalid; parent continues | SPEC.md Section 9.7 (delegation governance rule); Note: enforcement is DEL-03-04 scope |

## Request Schema

> **Lensing enrichment (X-001):** The following request schema enumerates the known fields from SPEC.md Section 9.8. A normative JSON schema definition is TBD.

| Field | Type | Required | Constraints | Source |
|-------|------|----------|-------------|--------|
| `message` | `string` | Conditional | MAY be empty when `attachments` is non-empty; otherwise required | SPEC.md Section 9.8 |
| `opts` | `object` | No | Turn options for runtime mapping; omitted fields follow fallback chains | SPEC.md Section 9.8 |
| `attachments` | `array of string` | No | Each element is an absolute filesystem path | SPEC.md Section 9.8 |

**Note:** Formal JSON schema (field-level constraints, additional validation rules) is TBD -- not specified in accessible sources. See Specification REQ-01 for normative statement.

## Response Schema (SSE)

> **Lensing enrichment (X-002):** The following captures known aspects of the SSE response format. A complete normative definition is TBD.

| Aspect | Value | Source |
|--------|-------|--------|
| **Content-Type** | TBD (expected: `text/event-stream`; **ASSUMPTION** based on SSE specification -- **location TBD**) | SSE specification (W3C/WHATWG); **ASSUMPTION: likely applicable; location TBD** |
| **Connection lifecycle** | Long-lived HTTP connection maintained for turn duration; terminates on turn completion | SOW-005; PLAN.md Section 2 |
| **Event format** | SSE `event`/`data` fields; specific event names and payload schemas TBD | SOW-005; **ASSUMPTION** based on SSE specification |
| **Connection close behavior** | Stream MUST terminate cleanly on turn completion (success or error); clean termination criteria TBD (see D-002) | Specification REQ-03 |

## Error Code Enumeration

> **Lensing enrichment (B-002):** The following enumerates known error codes and conditions from accessible sources. Additional mid-stream error event codes are TBD.

| Error Scenario | HTTP Status / Event | Condition | Source |
|----------------|---------------------|-----------|--------|
| Full attachment failure + no text | HTTP 400 (pre-stream) | All attachments fail AND `message` is empty | SPEC.md Section 9.8 |
| Session not active | TBD (pre-stream; **ASSUMPTION:** HTTP 4xx before SSE stream opens -- see X-004) | REQ-02 step 1 validation fails | Specification REQ-02 |
| Mid-stream SDK error | TBD (SSE error event) | Anthropic SDK failure during streaming | **ASSUMPTION:** error event schema not specified in accessible sources |
| Mid-stream tool error | TBD (SSE error event) | Tool execution failure during turn | **ASSUMPTION:** error event schema not specified in accessible sources |
| Client disconnect | N/A (server-side cleanup) | Client closes SSE connection mid-stream | Guidance P1 |

## Conditions

| Condition | Description | Source |
|-----------|-------------|--------|
| **Session Active** | A valid session must be booted before turn execution (session boot is DEL-03-01 scope) | SOW-004; Decomposition DEL-03-01 |
| **Working Root Bound** | `projectRoot` must be bound to the session | SOW-003; Decomposition DEL-03-01 |
| **API Key Available** | Anthropic API key must be provisioned per the key provisioning contract (DEL-03-05 scope; OI-001 open) | SOW-006; Decomposition DEL-03-05; Open Issue OI-001 |
| **Option Fallback Chains** | Model, tools, maxTurns follow fallback chains: `opts` -> persona defaults -> global defaults -> runtime defaults (detailed mapping is DEL-03-03 scope) | SPEC.md Section 9.8 |
| **Platform** | macOS 15+, Apple Silicon only (DEC-PLAT-001) | Decomposition DEC-PLAT-001 |

## Construction

| Aspect | Detail | Source |
|--------|--------|--------|
| **Framework** | Next.js API route within Electron desktop app | PLAN.md Section 2 |
| **SDK Integration** | Anthropic SDK `query()` with prompt mode selection based on attachment presence | SPEC.md Section 9.8 |
| **SSE Implementation** | Server pushes streaming events to UI during turn execution | SOW-005; PLAN.md Section 2 |
| **Attachment Resolver** | Server-side: `attachment-resolver.ts` handles classification, budget enforcement, partial failure | PLAN.md Section 2 (reference only; resolver implementation is DEL-04-01 scope) |
| **Turn Options** | `opts` object accepted on request; runtime mapping applies fallback chains | SPEC.md Section 9.8 (detailed mapping is DEL-03-03 scope) |
| **Event Types** | TBD -- specific SSE event type taxonomy not fully specified in accessible sources |
| **Error Handling** | Attachment full-failure returns 400; partial failure prepends warning; session-not-active behavior TBD; mid-stream error event schema TBD |

### SSE Event Type Enumeration (Candidate)

> **Lensing enrichment (B-001):** The following enumerates candidate SSE event categories. Specific event names and payload schemas are TBD -- not specified in accessible sources. Categories are inferred from Anthropic SDK streaming conventions (**ASSUMPTION**) and turn lifecycle requirements.

| Event Category | Candidate Event Names | Payload Schema | Status | Source |
|----------------|-----------------------|---------------|--------|--------|
| Turn lifecycle | `turn_start`, `turn_end` | TBD | **ASSUMPTION** based on SDK conventions | SOW-005; PLAN.md Section 2 |
| Content | `content_delta` | TBD | **ASSUMPTION** based on SDK conventions | SOW-005 |
| Tool use | `tool_use`, `tool_result` | TBD | **ASSUMPTION** based on SDK conventions | SOW-006; SPEC.md Section 9.8 |
| Error | TBD | TBD | Not specified in accessible sources | -- |
| Progress/Status | TBD | TBD | Not specified in accessible sources | -- |

## References

| Ref | Document | Relevance |
|-----|----------|-----------|
| 1 | `docs/SPEC.md` Section 9.7-9.8 | Harness turn input contract, delegation governance, prompt mode selection, attachment rules |
| 2 | `docs/CONTRACT.md` | Binding invariants (K-INVENT-1, K-GHOST-1, K-PROV-1, K-STATUS-1) |
| 3 | `docs/PLAN.md` Section 2 | Existing tooling description (session/turn API, SSE, attachments) |
| 4 | `docs/DIRECTIVE.md` | Founding intent, filesystem-as-state, no external DB |
| 5 | `docs/TYPES.md` | Domain vocabulary, lifecycle states, agent roles |
| 6 | Decomposition (G7-APPROVED) | DEL-03-02 entry, PKG-03 scope, DEC-NET-001, DEC-PLAT-001 |
| 7 | SSE specification (W3C/WHATWG) | SSE protocol semantics | **ASSUMPTION: likely applicable; location TBD** |
