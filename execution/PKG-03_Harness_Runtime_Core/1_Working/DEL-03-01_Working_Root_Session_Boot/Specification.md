# Specification — DEL-03-01 Working Root Binding & Session Boot

## Scope

### Included

This deliverable covers the API contract and runtime behavior for:

1. **Working Root binding** -- allowing a user to select a local filesystem directory (`projectRoot`) and bind it to a harness session so that agents operate against that directory (SOW-003).
2. **Session boot** -- the `POST /api/harness/session/boot` endpoint that accepts `opts`, initializes the session for agent execution, and returns a boot confirmation (SOW-004, session boot portion).
3. **Session creation** -- the `POST /api/harness/session/create` endpoint as the prerequisite to session boot.
4. **Session CRUD** -- list, get, and delete operations on sessions as supporting API surface.

Source: Decomposition DEL-03-01 entry; SOW-003; SOW-004.

### Excluded

- Turn execution and SSE streaming (covered by DEL-03-02).
- Turn options mapping and fallback chains beyond the boot-relevant subset (covered by DEL-03-03).
- Subagent governance (covered by DEL-03-04).
- Anthropic provider integration and key provisioning (covered by DEL-03-05).
- Outbound network guardrails (covered by DEL-03-06).
- Attachment handling during turns (covered by DEL-04-01).

---

## Requirements

### REQ-01: Working Root Selection and Binding

The application MUST allow a user to select a local filesystem directory as the Working Root (`projectRoot`).

- The selected directory MUST be bound to the session and persisted in the session record.
- The Working Root is the directory where agents read/write execution state (filesystem-as-state).
- The Working Root MUST be distinct from the Instruction Root (release-managed app bundle).

**Source:** SOW-003; DIRECTIVE Section 2.1, 2.6; Vocabulary Map ("Working Root" = `projectRoot`; working directory).

### REQ-02: Working Root Validation

The runtime MUST validate that the selected `projectRoot`:

- Is an accessible directory on the local filesystem.
- **ASSUMPTION [A-002]:** Is not empty validation (i.e., the runtime does not require the directory to be a pre-existing execution root -- it may be an empty or new directory). This assumption requires confirmation from implementation.
- TBD: Does the runtime accept **any** valid directory, or does it require a specific structure (e.g., an existing `.chirality/` folder)? **Human decision required.** (Lensing item A-002: `A:normative:applying`)

**Source:** DIRECTIVE Section 2.1 (filesystem is the database); **ASSUMPTION** for specific validation rules.

### REQ-03: Session Creation API

The runtime MUST provide a `POST /api/harness/session/create` endpoint that creates a new session record.

- The session record MUST include the bound `projectRoot`.
- Session records MUST be persisted to the filesystem (no external database).
- **[C-002]** TBD: The Guidance example shows the create endpoint accepting `{ projectRoot, persona, mode }`, but this requirement only mandates `projectRoot` in the session record. If `persona` and `mode` are required at session creation time (not just at boot), this requirement must be updated. See Conflict Table CONFLICT-003 in Guidance.md.

**Source:** harness architecture module graph (`SessCreate`); DIRECTIVE Section 5 (no external database dependency).

### REQ-04: Session Boot API

The runtime MUST provide a `POST /api/harness/session/boot` endpoint.

- The endpoint MUST accept a `sessionId` parameter identifying the session to boot.
- The endpoint MUST accept an optional `opts` object for runtime options.
- Bootstrap policy MUST remain authoritative for bootstrap-only constraints.
- On successful boot, the endpoint MUST return `200 { session, boot }`.

**Source:** SPEC Section 9.8; harness sequence diagram.

### REQ-05: Boot Initialization Sequence

On session boot, the runtime MUST:

1. Resume the session via SessionManager (`resume(sessionId)`).
2. Compute a boot fingerprint via PersonaManager (`getBootFingerprint(persona, mode)`).
3. Execute a bootstrap turn via AgentSdkManager (`startTurn(bootstrap message, plan mode)`).
   - **[D-001]** TBD: What constitutes a successful bootstrap turn? What does `AgentSdkManager.startTurn` return on success, and what conditions indicate failure? Enforced conformance requires unambiguous pass/fail criteria for this step. Human decision required.
4. Save boot metadata to the session record (`claudeSessionId`, `bootFingerprint`, `bootedAt`).

**Source:** harness sequence diagram (steps 94-99 in the sequence).

### REQ-06: Session Options (`opts`) Handling at Boot

The session boot endpoint MUST apply runtime option mapping with the following fallback chains:

| Option | Chain | Source |
|--------|-------|--------|
| Model | `opts.model` -> global model (instruction root) -> runtime default | SPEC Section 9.8 |
| Tools | `opts.tools` -> persona `tools` frontmatter -> runtime preset | SPEC Section 9.8 |
| Max turns | `opts.maxTurns` -> persona `max_turns` frontmatter -> runtime default | SPEC Section 9.8 |

- UI visibility of an option field MUST NOT be interpreted as runtime authorization.
- **[X-004]** TBD: What is the behavior when **all three levels** of a fallback chain are absent (no `opts` value, no persona frontmatter, no runtime default)? The runtime MUST define behavior for the fully-absent case -- either a hard error or a documented sentinel value. Human decision required.

**Source:** SPEC Section 9.8.

### REQ-07: Session Persistence

Session records MUST be persisted to the local filesystem.

- The persistence mechanism MUST NOT require an external database.
- Session records MUST survive application restart (persistence is durable).
- The SessionManager MUST support create, resume, save, list, and delete operations.

**Source:** DIRECTIVE Section 2.1, Section 5; harness architecture module graph.

### REQ-08: Session CRUD API Surface

The runtime MUST provide the following session management endpoints:

| Endpoint | Method | Purpose | Source |
|----------|--------|---------|--------|
| `/api/harness/session/create` | POST | Create a new session | harness architecture module graph |
| `/api/harness/session/boot` | POST | Boot a session | harness architecture module graph |
| `/api/harness/session/list` | GET | List sessions | harness architecture module graph |
| `/api/harness/session/:id` | GET | Get session details | harness architecture module graph |
| `/api/harness/session/:id` | DELETE | Delete a session | harness architecture module graph |

**Source:** harness architecture module graph.

### REQ-09: Instruction Root vs Working Root Separation

The runtime MUST maintain separation between:

- **Instruction Root:** Release-managed agent instructions and framework docs shipped inside the app bundle.
- **Working Root (`projectRoot`):** User-selected filesystem location where agents execute.

The session boot sequence MUST correctly resolve both roots: Instruction Root for persona/prompt construction, and Working Root for agent execution context.

**Source:** DIRECTIVE Section 2.6; SOW-013 (covered by DEL-05-01 but constrains this deliverable's implementation).

### REQ-10: Platform Constraint

The session boot implementation MUST function correctly on macOS 15+ running on Apple Silicon.

**Source:** DEC-PLAT-001; OBJ-001.

### REQ-11: Boot Error Handling -- **[A-003, F-001]**

The session boot endpoint MUST define normative error handling for the following failure scenarios:

| Failure Scenario | Required Behavior | Source |
|-----------------|-------------------|--------|
| Session not found (`sessionId` does not resolve) | Return `404` with error type `SESSION_NOT_FOUND` | Guidance C3 |
| Persona not found (persona referenced in session is unavailable) | Return `404` with error type `PERSONA_NOT_FOUND` (persona is treated as a missing instruction-root resource, not a syntactically invalid request) | Guidance C3 |
| SDK failure (AgentSdkManager fails during bootstrap turn) | Return `500` with error type `SDK_FAILURE`; include diagnostic details when available and keep session resumable | Guidance C3 |
| Working Root inaccessible (`projectRoot` no longer accessible at boot time) | Return `404` with error type `WORKING_ROOT_INACCESSIBLE` before attempting SDK boot turn | Guidance C3 |

- Error response MUST include HTTP status code and JSON body: `{"error":{"type":"<HarnessErrorType>","message":"<human-readable>", "details": <object|null>}}`.
- Status/code mappings in the table above are normative and test-enforced.

**Source:** Guidance.md C3 (error scenario enumeration); _SEMANTIC_LENSING.md items A-003, F-001.

### REQ-12: Boot Performance Threshold -- **[A-004]**

TBD: The session boot sequence SHOULD complete within a defined maximum latency threshold (e.g., maximum acceptable time from boot request to `200` response). No performance requirement currently exists.

- **ASSUMPTION:** A performance threshold is desirable for user experience (OBJ-001 requires a "working" desktop build), but no specific value is stated in source documents.
- Human decision required to set a concrete threshold or explicitly exclude performance requirements from this deliverable's scope.

**Source:** _SEMANTIC_LENSING.md item A-004; OBJ-001 (working macOS desktop build implies usable responsiveness).

---

## Standards

| Standard / Reference | Applicability | Location |
|---------------------|---------------|----------|
| `docs/SPEC.md` Section 9.8 | Harness turn input contract including session boot | Accessible |
| `docs/CONTRACT.md` K-GHOST-1 | No ghost inputs; context limited to folder contents + declared references | Accessible |
| `docs/CONTRACT.md` K-STATUS-1 | `_STATUS.md` is canonical lifecycle indicator | Accessible |
| `docs/DIRECTIVE.md` Section 2 | Design philosophy (filesystem-as-database, no external DB, instruction/working root separation) | Accessible |
| Anthropic Agent SDK | SDK `query()` interface used by AgentSdkManager. **[C-001]** TBD: SDK documentation is external and has not been accessed. Regulated competence for the AgentSdkManager interface contract cannot be confirmed without this reference. The `startTurn` / `query()` interface semantics remain inferred from architecture diagrams. | **location TBD** -- SDK documentation external |

---

## Verification

| Requirement | Verification Approach | Notes |
|-------------|----------------------|-------|
| REQ-01 | Integration test: select projectRoot, verify session record contains it | Verify binding persists |
| REQ-02 | Unit test: attempt boot with invalid/missing directory, confirm error | Boundary testing |
| REQ-03 | API test: POST to create endpoint, verify session record created on filesystem | Functional |
| REQ-04 | API test: POST to boot endpoint with valid sessionId and opts, verify 200 response shape | Functional |
| REQ-05 | Integration test: boot session, verify boot fingerprint, claudeSessionId, and bootedAt are persisted. **[D-002]** Additionally verify the bootstrap turn's own output or observable side effects to confirm it completed correctly (TBD -- success criteria for the SDK interaction must be defined per D-001 before this can be fully specified). | Sequence verification; bootstrap turn verification gap noted |
| REQ-06 | Unit test: verify each fallback chain with/without opts values. **[X-004]** Additionally test the all-absent case: remove opts value, persona frontmatter, AND runtime default for one chain, verify defined behavior (error or sentinel). | Fallback chain coverage including boundary case |
| REQ-07 | Integration test: create session, restart app, verify session list includes it | Persistence durability |
| REQ-08 | API test: exercise all CRUD endpoints, verify correct HTTP responses | Surface coverage |
| REQ-09 | Integration test: verify persona prompt loaded from instruction root, agent executes against working root. **[X-003]** Concrete acceptance criteria TBD: define what file/path patterns constitute each root and how to verify separation programmatically (e.g., assert that persona markdown is resolved from `<app-bundle>/instructions/` and execution writes land in `<projectRoot>/`). | Separation verification; testable criteria TBD |
| REQ-10 | Manual or CI test: build and run on macOS 15+ Apple Silicon | Platform validation |
| REQ-11 | API test: for each failure scenario (session not found, persona not found, SDK failure, Working Root inaccessible), trigger the condition and verify the exact status/type pairs (`404/SESSION_NOT_FOUND`, `404/PERSONA_NOT_FOUND`, `500/SDK_FAILURE`, `404/WORKING_ROOT_INACCESSIBLE`) | Error handling coverage |
| REQ-12 | Performance test: measure elapsed time from boot request to 200 response under standard conditions; compare against threshold (TBD) | Performance threshold TBD |

Validation script reference: `frontend/scripts/validate-harness-section8.mjs` includes `regression.session_crud`, `section8.session_persistence_resume`, and `section8.boot_error_taxonomy` checks. Source: `docs/harness/harness_manual_validation.md`.

---

## Documentation

### Required Artifacts (from Anticipated Artifacts: CODE/TEST/DOC)

| Artifact Type | Description | Status |
|---------------|-------------|--------|
| CODE | Implementation of session creation, boot, and CRUD API routes + SessionManager + PersonaManager boot path | TBD |
| TEST | Unit tests for Working Root validation, opts fallback chains; integration tests for session CRUD, boot sequence, persistence; error handling tests (REQ-11); performance baseline (REQ-12) | TBD |
| DOC | API contract documentation for session endpoints; boot sequence documentation; error response catalog; session record schema | TBD |
