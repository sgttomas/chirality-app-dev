# Procedure — DEL-04-02 UI Attachment Pipeline (Picker, Preview, Rollback, Rehydration)

## Purpose

This procedure describes the steps to **produce and verify** the UI attachment pipeline deliverable, covering the file picker, attachment preview, draft preservation, optimistic send with rollback, and session rehydration.

The procedure is intended for the developer or WORKING_ITEMS session responsible for implementing and testing DEL-04-02.

## Prerequisites

| Prerequisite | Description | Status |
|-------------|-------------|--------|
| DEL-04-01 (Server-side Attachment Resolver) | Server-side resolver must be available or stubbed so that the UI can send attachment paths and receive responses (success/failure). Stubbing is acceptable for initial UI-side implementation (see Guidance C6). | TBD — **ASSUMPTION:** DEL-04-01 is an upstream dependency based on the architectural split described in the decomposition and SPEC.md Section 9.8. Not yet formally declared in `_DEPENDENCIES.md` (PENDING_EXTRACTION). |
| DEL-03-02 (Turn Execution API + SSE Streaming) | Turn API endpoint (`POST /api/harness/turn`) must accept `attachments` array. Stubbing is acceptable for initial UI-side implementation (see Guidance C6). | TBD — **ASSUMPTION:** Inferred from SPEC.md Section 9.8; turn API is DEL-03-02 scope. Not yet formally declared in `_DEPENDENCIES.md` (PENDING_EXTRACTION). |
| Development environment | macOS 15+ with Apple Silicon; repo builds and runs per DEL-01-01. | TBD |
| SPEC.md Section 9.8 | Accessible and reviewed for UI attachment state rules. | Available |
| PLAN.md Section 2 | Accessible and reviewed for existing component inventory. | Available |

## Steps

### Step 0: Verify Dependency Availability (Gate)

0.1. Before proceeding to implementation steps, verify that upstream dependencies are available or appropriately stubbed:
  - **DEL-04-01 (Server-side Attachment Resolver):** Confirm the turn API accepts `attachments` array and returns success/failure responses. If not yet available, create or confirm the existence of a stub/mock that simulates server responses (success, failure, partial failure).
  - **DEL-03-02 (Turn Execution API + SSE Streaming):** Confirm the `POST /api/harness/turn` endpoint is operational or stubbed.

0.2. Document the dependency status (live, stubbed, or unavailable) in `_MEMORY.md` before proceeding.

0.3. If both dependencies are unavailable and cannot be stubbed, **STOP** and escalate to ORCHESTRATOR. Steps 4 (Optimistic Send) and 5 (Rollback) require at minimum a stub to test against.

> **Source:** Lensing item C-003. Dependencies from Specification scope section; Guidance C6 rationale.

### Step 1: Review Existing Implementation

1.1. Locate existing attachment pipeline code.
  - `FilePicker.tsx` — file picker modal component (referenced in PLAN Section 2).
  - ChatPanel attachment pipeline code (referenced in PLAN Section 2).

1.2. Review the existing implementation against the requirements in `Specification.md`.

1.3. Document the current state: which requirements (REQ-PICK-01 through REQ-A11Y-01) are already met, partially met, or not yet implemented.

> **Source:** PLAN Section 2; Specification.md requirements table.

### Step 2: Implement/Update File Picker (REQ-PICK-01)

2.1. Verify `FilePicker.tsx` supports:
  - Multi-select file selection.
  - Extension filtering for supported types: `.png`, `.jpg`, `.jpeg`, `.gif`, `.webp`, `.pdf`, `.txt`, `.md`, `.csv`.
  - Directory navigation.

2.2. If any capability is missing, implement it.

2.3. Verify that the picker produces `Attachment[]` entries with `path`, display name, and client-classified mime/type (REQ-DATA-01).

2.4. Confirm that the extension filter list matches the server-side list in SPEC.md Section 9.8. Document any discrepancy in `_MEMORY.md`.

> **Source:** SPEC.md Section 9.8; Specification.md REQ-PICK-01, REQ-DATA-01.

### Step 3: Implement/Update Attachment Preview (REQ-PREV-01)

3.1. Verify that selected attachments are displayed before send, showing at minimum file name and type indicator.

3.2. Verify that preview uses client-classified metadata only for display (REQ-NOAUTH-01).

3.3. If preview is missing or incomplete, implement it.

> **Source:** SPEC.md Section 9.8; Specification.md REQ-PREV-01, REQ-NOAUTH-01.

### Step 4: Implement/Update Optimistic Send (REQ-OPT-01, REQ-SEND-01)

4.1. **Gate check:** Confirm DEL-04-01/DEL-03-02 dependency status from Step 0. Proceed with stub if live API is unavailable.

4.2. Verify that on send:
  - Attachment paths (not contents) are sent to `POST /api/harness/turn` as an `attachments` array.
  - The user message is rendered optimistically in the chat before server response.
  - Text-free sends (attachments only, empty message text) are supported.

4.3. If any behavior is missing, implement it.

> **Source:** SPEC.md Section 9.8; Specification.md REQ-SEND-01, REQ-OPT-01.

### Step 5: Implement/Update Rollback on Failure (REQ-ROLL-01, REQ-DRAFT-01, REQ-ERR-01)

5.1. Verify that on send failure:
  - The optimistic user message is removed from the chat display.
  - The streaming placeholder is removed from the chat display.
  - Draft text is restored to the input field.
  - Attachment selections are restored.
  - Error information is displayed to the user (REQ-ERR-01; specific UX format TBD, see Guidance C5).

5.2. Verify that draft state (text + attachments) persists during normal UI interaction (REQ-DRAFT-01).

5.3. If any behavior is missing, implement it.

> **Source:** SPEC.md Section 9.8; Specification.md REQ-ROLL-01, REQ-DRAFT-01, REQ-ERR-01.

### Step 6: Implement/Update Session Rehydration (REQ-REHYD-01)

6.1. Verify that on session rehydration:
  - Stored attachment records are validated for shape (required fields present, correct types).
  - Malformed records are silently dropped.
  - Valid records are restored.

6.2. Define and document what constitutes a "malformed" record (see Guidance C3 and Specification REQ-REHYD-01).

6.3. If rehydration validation is missing or incomplete, implement it.

> **Source:** SPEC.md Section 9.8; Specification.md REQ-REHYD-01.

### Step 7: Write Tests

7.1. Write automated tests covering:

| Test | Requirement | Description |
|------|-------------|-------------|
| Picker multi-select | REQ-PICK-01 | Select multiple files; verify all appear in attachment preview area |
| Picker extension filter | REQ-PICK-01 | Verify unsupported extensions are filtered out |
| Picker directory nav | REQ-PICK-01 | Navigate directories; verify correct path resolution |
| Preview display | REQ-PREV-01 | Select files; verify preview renders name and type |
| Data model shape | REQ-DATA-01 | Verify attachment state contains path, display name, mime/type |
| Send paths only | REQ-SEND-01 | Send turn; verify API receives paths, not file contents |
| Text-free send | REQ-SEND-01 | Send with attachments and empty text; verify accepted |
| Optimistic render | REQ-OPT-01 | Send turn; verify message appears before server response |
| Rollback message | REQ-ROLL-01 | Simulate failure; verify optimistic message removed |
| Rollback placeholder | REQ-ROLL-01 | Simulate failure; verify streaming placeholder removed |
| Rollback draft | REQ-ROLL-01 | Simulate failure; verify draft text restored |
| Rollback attachments | REQ-ROLL-01 | Simulate failure; verify attachment selections restored |
| Error display on failure | REQ-ERR-01 | Simulate failure; verify user receives error information |
| Rehydration valid | REQ-REHYD-01 | Store valid records; rehydrate; verify restored |
| Rehydration malformed | REQ-REHYD-01 | Store malformed records; rehydrate; verify dropped |
| Non-authoritative meta (positive) | REQ-NOAUTH-01 | Verify client metadata used for preview rendering |
| Non-authoritative meta (negative) | REQ-NOAUTH-01 | Verify client metadata fields are NOT included in server-bound API payload for classification/execution |
| Draft persistence | REQ-DRAFT-01 | Add draft + attachments; interact with UI; verify preserved |
| Boundary: 0 attachments | REQ-SEND-01 | Send text-only turn (no attachments); verify normal behavior |
| Boundary: 1 attachment | REQ-PICK-01 | Select single file; verify full pipeline |
| Boundary: many attachments | REQ-PICK-01 | Select large number of files; verify picker and preview performance remain acceptable |

7.2. Ensure tests can run locally and in CI (per SOW-028 validation posture).

> **Source:** Specification.md Verification table; Decomposition anticipated artifacts (CODE/TEST). Boundary tests from lensing item X-002. Negative NOAUTH test from lensing item D-001.

### Step 8: Integration Verification

8.1. End-to-end test with server-side resolver (DEL-04-01):
  - Select files via picker.
  - Send turn with attachments.
  - Verify server resolves attachments and turn completes.
  - Verify partial failure scenario: some attachments fail, turn proceeds with warning.

8.2. End-to-end test with SSE streaming (DEL-03-02):
  - Verify streamed assistant response renders correctly after attachment-enabled turn.

8.3. **Pass/fail criteria for integration tests:**

| Scenario | Expected Outcome | Pass Criteria |
|----------|-----------------|---------------|
| Successful attachment send | Server returns 200; assistant response streams | Turn completes; response renders in chat; no console errors |
| All attachments fail (with text) | Server returns success with warning block prepended | Warning text renders in assistant response; turn still executes |
| All attachments fail (no text) | Server returns error | UI rolls back optimistic message; error displayed to user; draft preserved |
| Partial attachment failure | Server returns success with warning | Warning text renders; successful attachments reflected in response |
| Network timeout | No server response within timeout period | TBD — timeout threshold and UI behavior not yet specified |
| SSE stream after attachment turn | Assistant response streams via SSE | Streaming placeholder replaced with streamed content; no rendering artifacts |

> **ASSUMPTION:** Integration tests require DEL-04-01 and DEL-03-02 to be at least partially functional or stubbed. Pass/fail criteria for network timeout scenario are TBD. Lensing item D-002 identified the gap in concrete pass/fail thresholds.

## Verification

| Check | Method | Pass Criteria |
|-------|--------|--------------|
| All requirements covered | Review test matrix (Step 7) against Specification.md | Every REQ-* has at least one test |
| Tests pass | Run test suite | All tests green |
| Rollback correctness | Manual or automated failure simulation | Draft + attachments preserved on failure |
| Rehydration correctness | Automated test with malformed + valid records | Malformed dropped, valid restored |
| No authoritative client metadata | Code review + negative test | Server reclassifies; UI metadata is preview-only; no client metadata in server-bound payload |
| Cross-check with Datasheet | Review Datasheet.md attributes against implementation | Attributes match |
| Dependency gate verified | Review Step 0 outcome in `_MEMORY.md` | Dependencies confirmed available or stubbed before implementation |

## Records

| Record | Description | Location |
|--------|-------------|----------|
| Test results | Automated test output | TBD (project test output directory or CI artifacts — specific path to be determined by project CI configuration) |
| Implementation code | Source files implementing the attachment pipeline | TBD (frontend source tree) |
| `_STATUS.md` update | State transition upon completion | `_STATUS.md` in this deliverable folder |
| `_MEMORY.md` notes | Key decisions and findings during implementation | `_MEMORY.md` in this deliverable folder |
| Dependency status log | Step 0 gate outcome documenting DEL-04-01/DEL-03-02 availability | `_MEMORY.md` in this deliverable folder |
