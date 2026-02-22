# Specification — DEL-03-07 Harness API Baseline in Frontend Runtime

## Scope

### Included

This deliverable covers the implementation of baseline harness API routes in the local `frontend/` workspace, specifically:

1. **Session CRUD routes** -- `POST /api/harness/session/create`, `GET /api/harness/session/list`, `GET /api/harness/session/:id`, `DELETE /api/harness/session/:id` providing session lifecycle management.
2. **Session boot route** -- `POST /api/harness/session/boot` accepting `opts` and initializing a session for agent execution with boot fingerprint computation and SDK bootstrap.
3. **Turn execution route** -- `POST /api/harness/turn` accepting `{ sessionId, message, opts, attachments? }` and returning SSE event streams.
4. **Typed failure contracts** -- Each route surface includes typed error responses with HTTP status codes, error type identifiers, and human-readable messages.
5. **Route-contract tests** -- Baseline tests demonstrating that route handlers compile and pass contract validation.

Source: SOW-045; Decomposition SCA-001 DEL-03-07 entry; `docs/PLAN.md` Section 2 (FE-2).

### Excluded

- Working Root binding UX and directory selection UI (covered by DEL-03-01 and DEL-02-05).
- Turn options mapping and fallback chain internals beyond the route-level acceptance of `opts` (covered by DEL-03-03).
- Subagent governance fail-closed enforcement internals (covered by DEL-03-04).
- Anthropic provider integration and API key provisioning policy (covered by DEL-03-05).
- Outbound network guardrails (covered by DEL-03-06).
- Server-side attachment resolver validation rules and prompt-mode selection internals (covered by DEL-04-01).
- UI attachment pipeline (covered by DEL-04-02).
- SSE streaming protocol internals beyond the route-level event stream response (covered by DEL-03-02).
- Frontend workspace bootstrap, build tooling, and packaging (covered by DEL-01-03).
- Frontend workflow shell UI (covered by DEL-02-05).

---

## Requirements

### REQ-01: Session Create Route

The `frontend/` workspace MUST implement a `POST /api/harness/session/create` route handler.

- The route MUST accept a request body containing at minimum a `projectRoot` field (filesystem path).
- On success, the route MUST return `200` with a response body containing the created session record.
- On validation failure (missing or invalid `projectRoot`), the route MUST return a typed error response (see REQ-08).

**Source:** `docs/harness/chirality_harness_graphs_and_sequence.md` module graph (SessCreate); SOW-045; DEL-03-01 Specification REQ-03.

### REQ-02: Session Boot Route

The `frontend/` workspace MUST implement a `POST /api/harness/session/boot` route handler.

- The route MUST accept a `sessionId` parameter and optional `opts` object.
- Bootstrap policy MUST remain authoritative for bootstrap-only constraints.
- On successful boot, the route MUST return `200 { session, boot }`.
- Boot sequence MUST: resume the session, compute boot fingerprint, execute bootstrap turn via AgentSdkManager, and save boot metadata (`claudeSessionId`, `bootFingerprint`, `bootedAt`).

**Source:** `docs/SPEC.md` Section 9.8; `docs/harness/chirality_harness_graphs_and_sequence.md` sequence diagram (steps 94-99); DEL-03-01 Specification REQ-04, REQ-05.

### REQ-03: Session List Route

The `frontend/` workspace MUST implement a `GET /api/harness/session/list` route handler.

- The route MUST accept a `projectRoot` query parameter.
- The route MUST return `200` with a list of session records for the given project root.

**Source:** Module graph (SessList); `docs/harness/harness_manual_validation.md` (used in readiness polling and `regression.session_crud` check).

### REQ-04: Session Get Route

The `frontend/` workspace MUST implement a `GET /api/harness/session/:id` route handler.

- The route MUST return `200` with the session record for the given session ID.
- If the session ID does not resolve, the route MUST return a typed error response (see REQ-08).

**Source:** Module graph (SessGet).

### REQ-05: Session Delete Route

The `frontend/` workspace MUST implement a `DELETE /api/harness/session/:id` route handler.

- The route MUST delete the session record and return a success response.
- If the session ID does not resolve, the route MUST return a typed error response (see REQ-08).

**Source:** Module graph (SessDel).

### REQ-06: Turn Execution Route

The `frontend/` workspace MUST implement a `POST /api/harness/turn` route handler.

- The route MUST accept `{ sessionId, message, opts, attachments? }`.
- The route MUST return `200` with content type `text/event-stream` (SSE).
- The route MUST support optional `attachments` as an array of absolute filesystem path strings.
- When attachments are present, runtime MUST build multimodal content blocks and use SDK `query({ prompt: AsyncIterable<SDKUserMessage> })`.
- When no attachments are present, runtime MUST use SDK `query({ prompt: string })`.
- A turn MAY omit text when attachments are present (`message.trim() === ""` with non-empty `attachments`).
- If all attachments fail and user text is empty, the request MUST be rejected with `400`.
- Partial attachment failure is non-fatal when executable content remains.

**Source:** `docs/SPEC.md` Section 9.8; `docs/harness/chirality_harness_graphs_and_sequence.md` sequence diagram (steps 100-137).

### REQ-07: Turn SSE Event Stream

The turn route SSE stream MUST emit events in the following ordered categories:

- `session:init` -- emitted when SDK initializes/resumes the claude session
- `chat:delta` -- streaming chat content fragments
- `chat:complete` -- complete chat response
- `tool:result` -- tool execution results (when tools are invoked)
- `session:complete` -- session-level completion
- `process:exit` -- terminal event indicating turn completion

**Source:** `docs/harness/harness_manual_validation.md` Section 8 Matrix (smoke stream ordering: `session:init`, `chat:delta`, `chat:complete`, `session:complete`, `process:exit`); `docs/harness/chirality_harness_graphs_and_sequence.md` sequence diagram.

### REQ-08: Typed Failure Contracts

Every route in the harness API surface MUST implement typed failure responses.

- Error responses MUST include: HTTP status code, an error type identifier (string enum or constant), and a human-readable message.
- **ASSUMPTION:** The specific error type taxonomy is TBD. The following baseline error categories are inferred from the route surface and standard conventions:

| Error Category | Applicable Routes | Expected Status Code | Source |
|----------------|-------------------|---------------------|--------|
| Session not found | boot, get, delete, turn | TBD (likely 404) | DEL-03-01 Specification REQ-11 (analogous) |
| Invalid request body | create, boot, turn | 400 | **ASSUMPTION** -- standard convention |
| Persona not found | boot | TBD | DEL-03-01 Specification REQ-11 (analogous) |
| SDK failure | boot, turn | TBD (likely 500 or 502) | DEL-03-01 Specification REQ-11 (analogous) |
| Working root inaccessible | boot, turn | TBD | DEL-03-01 Specification REQ-11 (analogous) |
| All attachments failed + no text | turn | 400 | `docs/SPEC.md` Section 9.8 |

**Source:** SOW-045 ("typed failure contracts"); DEL-03-01 Specification REQ-11 pattern; `docs/SPEC.md` Section 9.8.

### REQ-09: Route Compilation

All route handlers MUST compile successfully under the `frontend/` TypeScript configuration.

- Routes MUST NOT produce TypeScript compilation errors.
- Type definitions for request/response shapes and error types MUST be part of the codebase.

**Source:** SOW-045 acceptance criteria ("route handlers compile"); Decomposition SCA-001 DEL-03-07 description.

### REQ-10: Route-Contract Tests

Baseline route-contract tests MUST exist and pass.

- Tests MUST validate that each route handler responds with the expected status codes and response shapes for both success and typed failure cases.
- Tests MUST cover: session create (success + validation failure), session list, session get (success + not found), session delete (success + not found), session boot (success + session not found), and turn execution (success stream + invalid request).
- Tests MUST be runnable from the `frontend/` workspace.

**Source:** SOW-045 acceptance criteria ("pass baseline route-contract tests"); Decomposition SCA-001 DEL-03-07 description.

### REQ-11: Local-Only Implementation

All API route implementations MUST reside in the `frontend/` workspace within this repository.

- No route handler code may depend on non-local repositories or external clones.
- The `frontend/` workspace must contain all source files needed for route compilation and testing.

**Source:** SOW-045; Decomposition SCA-001 execution gating rule; `docs/PLAN.md` local-only source policy.

### REQ-12: Interrupt Route

The `frontend/` workspace MUST implement a `POST /api/harness/interrupt` route handler.

- The route MUST return `200 { ok: true }` on successful interrupt.
- The interrupted turn's SSE stream MUST emit a terminal `process:exit` with an interruption marker.

**Source:** `docs/harness/harness_manual_validation.md` Section 8 Matrix (`section8.interrupt_sigint` check); `docs/harness/chirality_harness_graphs_and_sequence.md` module graph (Interrupt).

### REQ-13: Session Persistence via SessionManager

Route handlers MUST delegate session lifecycle operations to a SessionManager module.

- SessionManager MUST support create, resume, save, list, and delete operations.
- Session records MUST be persisted to the local filesystem (no external database).
- Session records MUST survive application restart.

**Source:** Module graph; DEL-03-01 Specification REQ-07; DIRECTIVE Section 2.1 (filesystem-as-state).

### REQ-14: Options Mapping at Route Level

Both boot and turn routes MUST accept an `opts` object and apply runtime option mapping with documented fallback chains.

- Model: `opts.model` -> global model (instruction root) -> runtime default.
- Tools: `opts.tools` -> persona `tools` frontmatter -> runtime preset.
- Max turns: `opts.maxTurns` -> persona `max_turns` frontmatter -> runtime default.
- UI visibility of an option field MUST NOT be interpreted as runtime authorization.

**Source:** `docs/SPEC.md` Section 9.8.

### REQ-15: Platform Constraint

The harness API baseline implementation MUST function correctly on macOS 15+ running on Apple Silicon.

**Source:** DEC-PLAT-001; OBJ-001.

---

## Standards

| Standard / Reference | Applicability | Location |
|---------------------|---------------|----------|
| `docs/SPEC.md` Section 9.8 | Harness turn input contract, session boot, opts mapping, attachment rules | Accessible |
| `docs/SPEC.md` Section 9.7 | Runtime metadata contract (harness), subagent registry safety rules | Accessible |
| `docs/CONTRACT.md` K-GHOST-1 | No ghost inputs; context limited to folder contents + declared references | Accessible |
| `docs/CONTRACT.md` K-INVENT-1 | Unknown values become TBD, not guessed | Accessible |
| `docs/DIRECTIVE.md` Section 2.1 | Filesystem-as-state design philosophy | Accessible |
| `docs/DIRECTIVE.md` Section 2.6 | Instruction root vs working root separation | Accessible |
| Anthropic Agent SDK | SDK `query()` interface used by AgentSdkManager | **location TBD** -- SDK documentation external |
| Next.js App Router API Routes | Route handler conventions for `app/api/` directory | **location TBD** -- Next.js documentation external |

---

## Verification

| Requirement | Verification Approach | Notes |
|-------------|----------------------|-------|
| REQ-01 | API test: POST to create endpoint, verify `200` + session record; POST with missing `projectRoot`, verify typed error | Functional + error contract |
| REQ-02 | API test: POST to boot with valid `sessionId` and `opts`, verify `200 { session, boot }` shape; POST with invalid `sessionId`, verify typed error | Functional + error contract |
| REQ-03 | API test: GET list with `projectRoot`, verify `200` with session array | Functional |
| REQ-04 | API test: GET session by ID, verify `200` + record; GET with invalid ID, verify typed error | Functional + error contract |
| REQ-05 | API test: DELETE session by ID, verify success; DELETE with invalid ID, verify typed error | Functional + error contract |
| REQ-06 | Integration test: POST turn with valid `sessionId` + message, verify `200 text/event-stream`; test with attachments array; test with empty message + failed attachments, verify `400` | Functional + attachment edge cases |
| REQ-07 | Integration test: execute turn, capture SSE events, verify ordered emission of `session:init`, `chat:delta`, `chat:complete`, `session:complete`, `process:exit` | Stream ordering validation; aligns with `section8.smoke_stream` check |
| REQ-08 | API test: trigger each typed failure category, verify response includes status code + error type + message | Error contract coverage |
| REQ-09 | Build test: run `tsc --noEmit` from `frontend/`, verify zero compilation errors in route files | Compilation check |
| REQ-10 | Test suite: run route-contract test suite from `frontend/`, verify all tests pass | Contract test coverage |
| REQ-11 | Audit: verify all route source files reside under `frontend/`; verify no imports from non-local paths | Filesystem boundary check |
| REQ-12 | API test: POST interrupt, verify `200 { ok: true }`; verify interrupted stream emits `process:exit` with interruption marker | Aligns with `section8.interrupt_sigint` check |
| REQ-13 | Integration test: create session, restart app, verify session persists in list | Persistence durability |
| REQ-14 | Unit test: verify each fallback chain with/without `opts` values | Fallback chain coverage |
| REQ-15 | Manual or CI test: build and run on macOS 15+ Apple Silicon | Platform validation |

Validation script reference: `frontend/scripts/validate-harness-section8.mjs` includes `regression.session_crud`, `section8.smoke_stream`, `section8.session_persistence_resume`, `section8.permissions_dontask`, `section8.interrupt_sigint`, and `section8.sdk_native_stream` checks. Source: `docs/harness/harness_manual_validation.md`.

CI validation reference: `.github/workflows/harness-premerge.yml` runs `npm run harness:validate:premerge` and validates the summary artifact at `frontend/artifacts/harness/section8/latest/summary.json`. Source: `docs/harness/harness_ci_integration.md`.

---

## Documentation

### Required Artifacts (from Anticipated Artifacts: CODE, TEST)

| Artifact Type | Description | Status |
|---------------|-------------|--------|
| CODE | Next.js API route handlers for session CRUD, boot, turn, and interrupt in `frontend/`; TypeScript type definitions for request/response shapes and error types; SessionManager, PersonaManager, AgentSdkManager, AgentSdkEventMapper, AttachmentResolver module implementations or stubs | TBD |
| TEST | Route-contract tests validating compilation, status codes, response shapes, and typed failure responses for each endpoint; integration tests for SSE stream ordering and session persistence | TBD |
