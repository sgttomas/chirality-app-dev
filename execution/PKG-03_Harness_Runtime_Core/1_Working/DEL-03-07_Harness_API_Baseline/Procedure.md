# Procedure — DEL-03-07 Harness API Baseline in Frontend Runtime

## Purpose

This procedure describes the steps to produce the harness API baseline in the local `frontend/` workspace: implementing the route handlers, type definitions, module interfaces, typed failure contracts, and route-contract tests for the session CRUD, boot, turn, and interrupt endpoints. It also describes verification steps to confirm the baseline meets the acceptance criteria defined in SOW-045 and the execution gating requirements of SCA-001.

---

## Prerequisites

### Required Before Starting

| Prerequisite | Source | Status |
|-------------|--------|--------|
| `frontend/` workspace exists with package manifest, TypeScript config, Next.js App Router, and development scripts | DEL-01-03 (FE-1 Workspace Bootstrap); Decomposition SCA-001 execution gating rule | TBD |
| `npm run dev` and `npm run build` resolve from `frontend/` without referencing non-local repos | DEL-01-03 acceptance criteria | TBD |
| Access to `docs/SPEC.md` Section 9.8 (harness turn input contract) | `_REFERENCES.md` | Accessible |
| Access to `docs/harness/chirality_harness_graphs_and_sequence.md` (module graph + sequence diagram) | `_REFERENCES.md` | Accessible |
| Access to `docs/harness/harness_manual_validation.md` (validation matrix) | `_REFERENCES.md` | Accessible |
| Access to DEL-03-01 Specification (session boot contract) | `execution/PKG-03_Harness_Runtime_Core/1_Working/DEL-03-01_Working_Root_Session_Boot/Specification.md` | Accessible |

### Reference Documents

| Document | Location | Usage |
|----------|----------|-------|
| Harness Architecture Graphs & Sequence | `docs/harness/chirality_harness_graphs_and_sequence.md` | Module graph for route-to-module delegation; sequence diagram for turn flow |
| SPEC Section 9.8 | `docs/SPEC.md` | Harness turn input contract, opts mapping, attachment rules |
| DEL-03-01 Specification | `execution/PKG-03_Harness_Runtime_Core/1_Working/DEL-03-01_Working_Root_Session_Boot/Specification.md` | Session CRUD and boot API contract (REQ-03 through REQ-11) |
| Harness Manual Validation | `docs/harness/harness_manual_validation.md` | Validation script expectations, Section 8 matrix |
| Harness CI Integration | `docs/harness/harness_ci_integration.md` | CI workflow, pre-merge validation contract |

---

## Steps

### Step 1: Define Type Definitions and Error Taxonomy

**Objective:** Establish the TypeScript type foundation for all route handlers.

1.1. Create a shared types file (e.g., `frontend/src/lib/harness/types.ts` or equivalent location per workspace conventions).

1.2. Define request types for each endpoint:
   - `SessionCreateRequest`: `{ projectRoot: string; ... }` (TBD: whether `persona`/`mode` are required at create time -- see Conflict Table CONFLICT-001 in Guidance.md)
   - `SessionBootRequest`: `{ sessionId: string; opts?: HarnessOpts; }`
   - `TurnRequest`: `{ sessionId: string; message: string; opts?: HarnessOpts; attachments?: string[]; }`
   - `InterruptRequest`: `{ sessionId: string; }`

1.3. Define response types:
   - `SessionRecord`: `{ sessionId, projectRoot, createdAt, claudeSessionId?, bootFingerprint?, bootedAt?, ... }`
   - `BootResponse`: `{ session: SessionRecord; boot: BootMetadata; }`
   - `SessionListResponse`: `{ sessions: SessionRecord[]; }`

1.4. Define the error type taxonomy:
   - `HarnessErrorType`: string enum or constants for error categories (e.g., `SESSION_NOT_FOUND`, `INVALID_REQUEST`, `SDK_FAILURE`, `WORKING_ROOT_INACCESSIBLE`, `PERSONA_NOT_FOUND`, `ATTACHMENT_FAILURE`)
   - `HarnessErrorResponse`: `{ error: { type: HarnessErrorType; message: string; [contextFields]? } }`
   - TBD: exact format pending human decision (see Guidance.md T2)

1.5. Define SSE event types:
   - `UIEventType`: enum covering `session:init`, `chat:delta`, `chat:complete`, `tool:result`, `session:complete`, `process:exit`
   - `UIEvent`: typed union for each event type

**Verification:** Types file compiles without errors (`tsc --noEmit`).

### Step 2: Define Module Interfaces

**Objective:** Establish TypeScript interfaces for the harness modules that route handlers delegate to.

2.1. Define `ISessionManager` interface:
   - `create(projectRoot: string, ...): Promise<SessionRecord>`
   - `resume(sessionId: string): Promise<SessionRecord>`
   - `save(sessionId: string, updates: Partial<SessionRecord>): Promise<void>`
   - `list(projectRoot: string): Promise<SessionRecord[]>`
   - `delete(sessionId: string): Promise<void>`

2.2. Define `IPersonaManager` interface:
   - `buildSystemPrompt(projectRoot: string, persona: string, mode: string): Promise<string>`
   - `getBootFingerprint(persona: string, mode: string): string`

2.3. Define `IAgentSdkManager` interface:
   - `startTurn(session: SessionRecord, message: string, opts: ResolvedOpts, contentBlocks?: ContentBlock[]): AsyncIterable<UIEvent>`
   - `interrupt(sessionId: string): Promise<void>`

2.4. Define `IAttachmentResolver` interface:
   - `resolveAttachmentsToContentBlocks(message: string, attachmentPaths: string[]): Promise<ResolvedAttachments>`

2.5. Create stub implementations for each interface that return minimal valid responses or throw structured errors for error-path testing.

**Verification:** Interface files compile; stub implementations satisfy the interfaces.

### Step 3: Implement Session CRUD Route Handlers

**Objective:** Implement the session create, list, get, and delete route handlers.

3.1. Create route files following Next.js App Router conventions:
   - `frontend/src/app/api/harness/session/create/route.ts` -- exports `POST`
   - `frontend/src/app/api/harness/session/list/route.ts` -- exports `GET`
   - `frontend/src/app/api/harness/session/[id]/route.ts` -- exports `GET` and `DELETE`

3.2. For each route handler:
   - Parse and validate the request body/params using the types from Step 1.
   - Delegate to `ISessionManager` methods.
   - Return typed success responses with appropriate status codes.
   - Catch and transform errors into `HarnessErrorResponse` format with appropriate error types.

3.3. Implement request validation:
   - Session create: validate `projectRoot` is present and is a string.
   - Session get/delete: validate `:id` param is present.
   - Session list: validate `projectRoot` query parameter.

**Verification:** Each route compiles; manual curl or test invocation returns expected shapes.

### Step 4: Implement Session Boot Route Handler

**Objective:** Implement the session boot route handler per SPEC Section 9.8 and DEL-03-01 REQ-04/REQ-05.

4.1. Create `frontend/src/app/api/harness/session/boot/route.ts` -- exports `POST`.

4.2. Implement the boot sequence:
   1. Parse `{ sessionId, opts? }` from request body.
   2. Resume session via `ISessionManager.resume(sessionId)`.
   3. Compute boot fingerprint via `IPersonaManager.getBootFingerprint(persona, mode)`.
   4. Execute bootstrap turn via `IAgentSdkManager.startTurn(...)`.
   5. Save boot metadata (`claudeSessionId`, `bootFingerprint`, `bootedAt`) via `ISessionManager.save(...)`.
   6. Return `200 { session, boot }`.

4.3. Implement typed error handling for boot failures:
   - Session not found: return typed error with `SESSION_NOT_FOUND`.
   - Persona not found: return typed error with `PERSONA_NOT_FOUND`.
   - SDK failure: return typed error with `SDK_FAILURE`.
   - Working root inaccessible: return typed error with `WORKING_ROOT_INACCESSIBLE`.

**Verification:** Boot route compiles; contract tests (Step 7) exercise success and failure paths.

### Step 5: Implement Turn Execution Route Handler

**Objective:** Implement the turn execution route handler per SPEC Section 9.8 and the sequence diagram.

5.1. Create `frontend/src/app/api/harness/turn/route.ts` -- exports `POST`.

5.2. Implement the turn flow:
   1. Parse `{ sessionId, message, opts?, attachments? }` from request body.
   2. Resume session via `ISessionManager.resume(sessionId)`.
   3. If attachments provided, resolve via `IAttachmentResolver.resolveAttachmentsToContentBlocks(...)`.
   4. Handle partial attachment failure per SPEC rules (proceed with warning if executable content remains; reject with `400` if all fail and text is empty).
   5. Build system prompt via `IPersonaManager.buildSystemPrompt(...)`.
   6. Start turn via `IAgentSdkManager.startTurn(...)`, receiving `AsyncIterable<UIEvent>`.
   7. Stream UIEvents as SSE to the response.
   8. On `session:init` event, save `claudeSessionId`/model to session record.
   9. On `process:exit` event, perform terminal save and close stream.

5.3. Return `200 text/event-stream` response header before streaming begins.

5.4. Implement typed error handling for turn failures (session not found, invalid request, attachment-only failure with no text).

**Verification:** Turn route compiles; SSE stream contract tests exercise the event stream.

### Step 6: Implement Interrupt Route Handler

**Objective:** Implement the interrupt route handler.

6.1. Create `frontend/src/app/api/harness/interrupt/route.ts` -- exports `POST`.

6.2. Implement:
   1. Parse `{ sessionId }` from request body.
   2. Call `IAgentSdkManager.interrupt(sessionId)`.
   3. Return `200 { ok: true }`.

6.3. The interrupted turn's SSE stream (from Step 5) must emit a terminal `process:exit` with interruption marker. This is handled by `IAgentSdkManager` internals, not by the interrupt route itself.

**Verification:** Interrupt route compiles and returns expected response shape.

### Step 7: Implement Route-Contract Tests

**Objective:** Create baseline tests that validate all route contracts.

7.1. Create test files in the appropriate test directory within `frontend/` (e.g., `frontend/src/__tests__/api/harness/` or per workspace conventions).

7.2. Test coverage matrix:

| Route | Success Case | Failure Cases |
|-------|-------------|---------------|
| Session create | Valid `projectRoot` -> `200` + session record | Missing `projectRoot` -> typed error |
| Session list | Valid `projectRoot` -> `200` + session array | TBD |
| Session get | Valid session ID -> `200` + session record | Invalid ID -> typed error |
| Session delete | Valid session ID -> success response | Invalid ID -> typed error |
| Session boot | Valid `sessionId` + `opts` -> `200 { session, boot }` | Invalid `sessionId` -> typed error; persona not found -> typed error |
| Turn execution | Valid turn -> `200 text/event-stream` with ordered events | Invalid request -> typed error; all attachments fail + no text -> `400` |
| Interrupt | Valid `sessionId` -> `200 { ok: true }` | TBD |

7.3. For SSE stream tests, verify the event ordering: `session:init`, `chat:delta`, `chat:complete`, `session:complete`, `process:exit`.

7.4. For typed failure tests, verify the error response shape: `{ error: { type, message } }` with the expected error type identifier.

7.5. Ensure tests are runnable via a standard npm script from `frontend/` (e.g., `npm test` or `npm run test:api`).

**Verification:** All tests pass; test runner exits zero.

### Step 8: Compilation and Integration Verification

**Objective:** Verify the complete baseline compiles and integrates with existing validation tooling.

8.1. Run TypeScript compilation check:
```bash
cd frontend && npx tsc --noEmit
```
Verify zero errors in route and type files.

8.2. Run route-contract tests:
```bash
cd frontend && npm test
```
Verify all tests pass.

8.3. (When server is available) Run validation scripts against the local server:
```bash
cd frontend && npm run dev -- --hostname 127.0.0.1 --port 3000
# In another terminal:
cd frontend && npm run harness:validate:premerge
```
Verify the summary artifact is produced at `frontend/artifacts/harness/section8/latest/summary.json`.

8.4. Verify the summary contains the required SDK test IDs per `docs/harness/harness_ci_integration.md` (Section 7):
   - Required SDK test IDs are present.
   - Legacy `regression.api_chat_reachability` is absent.

---

## Verification

### Acceptance Criteria (from SOW-045)

| Criterion | Verification Method | Status |
|-----------|-------------------|--------|
| Route handlers compile | `tsc --noEmit` from `frontend/` exits zero | TBD |
| Route handlers pass baseline route-contract tests | Test suite from `frontend/` exits zero | TBD |
| All session CRUD routes exist | Route files present at expected paths | TBD |
| Session boot route exists and conforms to SPEC | Boot route matches SPEC Section 9.8 contract | TBD |
| Turn route exists with SSE stream | Turn route returns `text/event-stream` | TBD |
| Typed failure contracts implemented | Error responses include type + message for each failure category | TBD |
| Implementation is local-only | All source files under `frontend/`; no non-local imports | TBD |

### Execution Gate Verification (from SCA-001)

| Gate Criterion | Verification Method | Status |
|----------------|-------------------|--------|
| DEL-03-07 reaches IN_PROGRESS | `_STATUS.md` shows IN_PROGRESS or later | TBD |
| Baseline unblocks Tier 2 work | Compilation + contract tests pass; route surface exists | TBD |

### Validation Script Compatibility

| Check | Script | Expected Result | Status |
|-------|--------|-----------------|--------|
| Session CRUD | `regression.session_crud` | Create, list, get, delete succeed | TBD |
| Smoke stream | `section8.smoke_stream` | Ordered SSE events | TBD |
| Session persistence + resume | `section8.session_persistence_resume` | Session persists across boot cycles | TBD |
| Interrupt | `section8.interrupt_sigint` | `200 { ok: true }` + terminal `process:exit` | TBD |
| SDK native stream | `section8.sdk_native_stream` | No `parse:error` logs | TBD |

---

## Records

### Artifacts Produced

| Artifact | Description | Location |
|----------|-------------|----------|
| Route handler source files | Next.js API route handlers for session CRUD, boot, turn, interrupt | `frontend/src/app/api/harness/` |
| Type definitions | TypeScript types for request/response shapes, error types, SSE events | `frontend/src/lib/harness/` (or equivalent) |
| Module interface definitions | TypeScript interfaces for SessionManager, PersonaManager, AgentSdkManager, AttachmentResolver | `frontend/src/lib/harness/` (or equivalent) |
| Stub implementations | Minimal module implementations for baseline testing | `frontend/src/lib/harness/` (or equivalent) |
| Route-contract tests | Test files validating route contracts | `frontend/src/__tests__/api/harness/` (or equivalent) |
| Validation summary | Harness validation summary artifact (when server available) | `frontend/artifacts/harness/section8/latest/summary.json` |

### Evidence Trail

| Evidence | Purpose |
|----------|---------|
| `tsc --noEmit` output (zero errors) | Proves compilation (SOW-045) |
| Test runner output (all pass) | Proves contract tests pass (SOW-045) |
| Validation summary JSON | Proves compatibility with existing validation tooling |
| Git diff of route files | Proves local-only implementation |
