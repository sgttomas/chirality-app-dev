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

| Aspect | Value | Source |
|--------|-------|--------|
| **Content-Type** | `text/event-stream; charset=utf-8` | DEL-03-02 route implementation contract (2026-02-24) |
| **Connection lifecycle** | Long-lived HTTP connection maintained for turn duration; terminates on turn completion | SOW-005; PLAN.md Section 2 |
| **Event format** | SSE `event`/`data` fields with typed taxonomy (`session:init`, `chat:delta`, `chat:complete`, `tool:result`, `session:complete`, `turn:error`, `process:exit`) | Specification REQ-03/REQ-12 |
| **Connection close behavior** | Success: `session:complete` then `process:exit` (`exitCode=0`) then close. Fatal error: `turn:error` (`fatal=true`) then `process:exit` (non-zero `exitCode`) then close. | Specification REQ-03/REQ-12 |

## Error Code Enumeration

| Error Scenario | HTTP Status / Event | Condition | Source |
|----------------|---------------------|-----------|--------|
| Full attachment failure + no text | HTTP 400 (pre-stream) | All attachments fail AND `message` is empty | SPEC.md Section 9.8 |
| Concurrent turn overlap | HTTP 409 (pre-stream), `TURN_IN_PROGRESS` | Second turn submitted while same-session turn is still in flight | DEL-03-02 implementation contract (2026-02-24) |
| Missing Anthropic API key | HTTP 503 (pre-stream), `MISSING_API_KEY` | Provider mode is Anthropic and neither canonical nor compatibility key is configured | DEL-03-05 key policy + DEL-03-02 route contract (2026-02-24) |
| Session not active | HTTP 404 (pre-stream), `SESSION_NOT_FOUND` | `sessionId` does not resolve to an active session record | Specification REQ-10 |
| Mid-stream SDK error | SSE `turn:error` (`fatal=true`) then SSE `process:exit` (`exitCode!=0`) | Anthropic SDK/runtime failure after stream opened | DEL-03-02 implementation contract (2026-02-24) |
| Mid-stream tool error | SSE `turn:error` (`fatal=false`) if recoverable, else `fatal=true` + `process:exit` | Tool execution failure during turn | Specification REQ-12 |
| Client disconnect | N/A (server-side cleanup) | Client closes SSE connection mid-stream | Guidance P1 |

## Conditions

| Condition | Description | Source |
|-----------|-------------|--------|
| **Session Active** | A valid session must be booted before turn execution (session boot is DEL-03-01 scope) | SOW-004; Decomposition DEL-03-01 |
| **Working Root Bound** | `projectRoot` must be bound to the session | SOW-003; Decomposition DEL-03-01 |
| **API Key Available** | Anthropic API key must be provisioned per DEL-03-05 `ENV_ONLY` policy (`ANTHROPIC_API_KEY` canonical, `CHIRALITY_ANTHROPIC_API_KEY` compatibility fallback) | SOW-006; Decomposition DEL-03-05; policy ruling 2026-02-23 |
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
| **Event Types** | `session:init`, `chat:delta`, `chat:complete`, `tool:result`, `session:complete`, `turn:error`, `process:exit` |
| **Error Handling** | Attachment full-failure returns 400; unknown session returns pre-stream 404 `SESSION_NOT_FOUND`; concurrent overlap returns 409 `TURN_IN_PROGRESS`; missing key returns 503 `MISSING_API_KEY` pre-stream; partial failure prepends warning; mid-stream fatal errors emit typed `turn:error` + terminal `process:exit` |

### SSE Event Type Enumeration

| Event Name | Payload Highlights | Terminal | Source |
|------------|--------------------|----------|--------|
| `session:init` | `claudeSessionId`, `model` | No | Runtime stream contract |
| `chat:delta` | `text` chunk | No | Runtime stream contract |
| `chat:complete` | final `text` | No | Runtime stream contract |
| `tool:result` | `name`, `ok`, optional `output` | No | Runtime stream contract |
| `session:complete` | empty object | No | Runtime stream contract |
| `turn:error` | `phase`, `errorType`, `message`, `status`, `severity`, `fatal`, optional `details` | Depends on `fatal` | REQ-12 |
| `process:exit` | `exitCode`, optional `interrupted`, optional error metadata | Yes | Runtime stream contract |

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
