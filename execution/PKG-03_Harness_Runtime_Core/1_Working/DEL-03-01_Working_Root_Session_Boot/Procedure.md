# Procedure — DEL-03-01 Working Root Binding & Session Boot

## Purpose

This procedure describes the steps to **produce** the Working Root Binding & Session Boot deliverable (CODE/TEST/DOC artifacts) and to **verify** that the implementation satisfies the specification requirements (REQ-01 through REQ-12).

---

## Prerequisites

| Prerequisite | Description | Source |
|-------------|-------------|--------|
| Development environment | macOS 15+ on Apple Silicon with Node.js, Electron, and Next.js development toolchain | DEC-PLAT-001 |
| Anthropic API key | Valid API key for Anthropic Agent SDK calls during testing | `docs/harness/harness_manual_validation.md` |
| Repository access | Local clone of the Chirality application repository | General |
| Governance documents | Access to `docs/SPEC.md`, `docs/CONTRACT.md`, `docs/DIRECTIVE.md`, `docs/TYPES.md` | _REFERENCES.md |
| Harness architecture docs | Access to `docs/harness/chirality_harness_graphs_and_sequence.md` | _REFERENCES.md |
| Specification reviewed | `Specification.md` for this deliverable reviewed and understood (including REQ-11 error handling and REQ-12 performance threshold) | This deliverable |
| Related deliverables awareness | Understanding of DEL-03-02 (turn execution), DEL-03-03 (opts mapping), DEL-05-01 (instruction root separation) interfaces | Decomposition |
| Conflict Table reviewed | Guidance.md Conflict Table entries (CONFLICT-001 through CONFLICT-004) reviewed; human rulings obtained where possible before implementation | This deliverable |

---

## Steps

### Phase 1: Implementation (CODE artifact)

#### Step 1: Implement or Verify SessionManager

1. Confirm the SessionManager module supports: `create`, `resume`, `save`, `list`, `delete` operations.
2. Verify session records are persisted to the filesystem (not an external database) per REQ-07.
3. Verify session records include `projectRoot` binding per REQ-01.
4. Verify session records survive application restart per REQ-07.
5. **[F-002]** Verify session record includes all fields from the Session Record Schema in Datasheet.md. Document any fields present in implementation but absent from the schema, and any schema fields absent from implementation.

**Verification:** Unit tests for each SessionManager operation. Integration test for persistence across restart.

#### Step 2: Implement or Verify Working Root Validation

1. Implement validation that the provided `projectRoot` is an accessible directory on the local filesystem per REQ-02.
2. Handle error cases: path does not exist, path is a file (not directory), path is inaccessible (permissions).
3. **ASSUMPTION [A-002]:** Determine whether the runtime should validate that the directory is a valid execution root (has required structure) or accept any valid directory. This requires a human decision.

**Verification:** Unit tests for valid directory, invalid directory, non-existent path, file-instead-of-directory cases.

#### Step 3: Implement or Verify Session Creation Endpoint

1. Implement `POST /api/harness/session/create` per REQ-03.
2. The endpoint must create a session record that includes the bound `projectRoot`.
3. Return the created `sessionId` in the response.
4. **[C-002]** Clarify whether `persona` and `mode` are required at session creation time or only at boot time (see Conflict Table CONFLICT-003). Implement accordingly.

**Verification:** API test: POST to create endpoint, verify response contains `sessionId`, verify session record exists on filesystem.

#### Step 4: Implement or Verify Session Boot Endpoint

1. Implement `POST /api/harness/session/boot` per REQ-04 and REQ-05.
2. The endpoint must:
   - Accept `sessionId` and optional `opts`.
   - Resume the session via SessionManager.
   - Compute boot fingerprint via PersonaManager.
   - Execute bootstrap turn via AgentSdkManager.
   - Save `claudeSessionId`, `bootFingerprint`, `bootedAt` to the session record.
   - Return `200 { session, boot }`.
3. Apply opts fallback chains per REQ-06 (model, tools, maxTurns).
4. **[A-003, F-001]** Implement error handling per REQ-11 for all four failure scenarios (session not found, persona not found, SDK failure, Working Root inaccessible).
5. **[D-001]** Document the success/failure criteria for the bootstrap turn (what AgentSdkManager.startTurn returns on success vs failure).

**Verification:** API test: POST to boot endpoint with valid session, verify 200 response shape and persisted boot metadata. Error path tests per REQ-11.

#### Step 5: Implement or Verify Session CRUD Endpoints

1. Implement or verify the remaining session management endpoints per REQ-08:
   - `GET /api/harness/session/list`
   - `GET /api/harness/session/:id`
   - `DELETE /api/harness/session/:id`
2. Verify correct HTTP response codes and shapes.

**Verification:** API tests for each endpoint.

#### Step 6: Verify Instruction Root vs Working Root Separation

1. Confirm that the boot sequence resolves the Instruction Root correctly (persona definitions, framework docs from app bundle) per REQ-09.
2. Confirm that the boot sequence resolves the Working Root correctly (execution context from `projectRoot`).
3. Verify that boot does not write to the Instruction Root.
4. **[X-003]** Define concrete, testable acceptance criteria for what constitutes "loaded from Instruction Root" and "executes against Working Root" (e.g., specific file/path patterns for each root).

**Verification:** Integration test: boot with a known projectRoot, verify persona loaded from instruction root, execution context references working root.

### Phase 2: Testing (TEST artifact)

#### Step 7: Unit Tests

Write or verify unit tests covering:

- [ ] Working Root validation (valid dir, invalid dir, non-existent, file-not-dir, inaccessible)
- [ ] SessionManager CRUD operations (create, resume, save, list, delete)
- [ ] Opts fallback chain resolution (model, tools, maxTurns -- each with and without explicit values)
- [ ] **[X-004]** Opts fallback chain all-absent case: test behavior when all three levels of a chain are absent (no opts value, no persona frontmatter, no runtime default)
- [ ] Boot fingerprint computation (TBD -- depends on implementation details)
- [ ] **[A-003, F-001]** Error response shapes/statuses for each REQ-11 scenario:
  - `404/SESSION_NOT_FOUND`
  - `404/PERSONA_NOT_FOUND`
  - `500/SDK_FAILURE`
  - `404/WORKING_ROOT_INACCESSIBLE`

#### Step 8: Integration Tests

Write or verify integration tests covering:

- [ ] Full session lifecycle: create -> boot -> verify persisted state -> list -> get -> delete
- [ ] Session persistence across application restart
- [ ] Boot with various `opts` combinations (empty opts, partial opts, full opts)
- [ ] Boot with invalid `sessionId` (error handling -- malformed sessionId)
- [ ] **[X-002]** Boot with well-formed but non-existent `sessionId` (distinct from malformed): verify error response and session state. This tests the case where the sessionId format is valid but no corresponding session record exists.
- [ ] **[X-001]** Boot without prior create: verify that attempting to boot a session that was never created produces the correct error response and does not create orphaned state. This is a negative test that validates the session-existence prerequisite.
- [ ] Working Root binding survives session resume
- [ ] **[D-002]** Bootstrap turn verification: after boot, verify observable evidence that the bootstrap turn completed successfully (TBD -- specific observable outcomes depend on D-001 resolution)

#### Step 9: Validation Script Alignment

Verify that existing validation scripts cover session boot:

- [ ] `section8.session_persistence_resume` -- session persistence and resume continuity
- [ ] `regression.session_crud` -- session CRUD operations
- [ ] `section8.boot_error_taxonomy` -- boot error status/type contract coverage

Source: `docs/harness/harness_manual_validation.md`

#### Step 10: Platform Verification

- [ ] Run all tests on macOS 15+ Apple Silicon per REQ-10.
- [ ] Verify session boot functions correctly in both dev mode (`npm run dev`) and packaged app (`.dmg`).

### Phase 3: Documentation (DOC artifact)

#### Step 11: API Contract Documentation

Document the session API contract:

- [ ] Request/response schemas for each endpoint (create, boot, list, get, delete)
- [ ] Error response shapes and codes (per REQ-11)
- [ ] Opts fallback chain behavior at boot
- [ ] Boot fingerprint semantics (per Guidance C2 open questions)
- [ ] **[F-002]** Complete session record schema (all fields, types, persistence format)

#### Step 12: Architecture Integration Notes

Document how session boot integrates with:

- [ ] Turn execution (DEL-03-02) -- what state the boot produces that turns consume
- [ ] Opts mapping (DEL-03-03) -- which opts are boot-relevant vs turn-relevant
- [ ] Instruction Root bundling (DEL-05-01) -- how persona resolution works at boot
- [ ] **[F-003]** Concurrent session behavior: document whether concurrent boots are supported, and if so, how resource contention is handled

---

## Verification

| Check | Expected Result |
|-------|----------------|
| All unit tests pass | Green on macOS 15+ Apple Silicon |
| All integration tests pass | Session lifecycle works end-to-end |
| Validation script checks pass | `regression.session_crud`, `section8.session_persistence_resume`, and `section8.boot_error_taxonomy` pass |
| API contract is documented | Request/response schemas for all session endpoints |
| Working Root validation rejects invalid paths | Error responses for non-directory, non-existent, and inaccessible paths |
| Opts fallback chains produce correct values | Each chain resolves per SPEC Section 9.8, including all-absent boundary case |
| Boot persists required metadata | `claudeSessionId`, `bootFingerprint`, `bootedAt` present in session record |
| Instruction/Working Root separation holds | Persona from instruction root; execution against working root |
| No external database dependency | All session state on filesystem |
| Error handling covers all REQ-11 scenarios | Each failure path returns correct HTTP status and error body |
| Boot-without-create produces correct error | Negative test passes (no orphaned state) |
| Session record schema is complete | All fields documented in Datasheet match implementation |

---

## Records

| Record | Location | Format |
|--------|----------|--------|
| Unit test results | TBD (test runner output) | Test framework report |
| Integration test results | TBD (test runner output) | Test framework report |
| Validation script output | `frontend/artifacts/harness/section8/latest/summary.json` | JSON summary |
| API contract documentation | TBD (within deliverable folder or `docs/`) | Markdown |
| Implementation review notes | `MEMORY.md` (this deliverable) | Markdown |
| Conflict Table rulings | Guidance.md Conflict Table (this deliverable) | Markdown |
