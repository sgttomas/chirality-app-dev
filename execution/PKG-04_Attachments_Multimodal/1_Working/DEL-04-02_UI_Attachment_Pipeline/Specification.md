# Specification — DEL-04-02 UI Attachment Pipeline (Picker, Preview, Rollback, Rehydration)

## Scope

### Included

This deliverable covers the **UI-side** attachment pipeline in the Chirality desktop app (Electron + Next.js). Specifically:

1. **File picker** — modal UI for selecting files to attach to a turn.
2. **Attachment preview** — displaying selected attachments before send, using client-side metadata for preview purposes only.
3. **Draft preservation** — maintaining attachment selections and draft text across UI interactions.
4. **Optimistic send + rollback** — rendering user message optimistically on send; rolling back the optimistic message and streaming placeholder on failure while preserving draft text and attachment selections for retry.
5. **Session rehydration** — restoring attachment records from stored session state with shape validation; silently dropping malformed records.

### Excluded

- Server-side attachment resolution, classification, and budget enforcement (covered by DEL-04-01).
- Server-side prompt-mode selection logic (covered by DEL-04-01).
- Harness session boot and turn execution APIs (covered by DEL-03-01, DEL-03-02).
- Runtime `opts` mapping and fallback chains (covered by DEL-03-03).

### Boundary with DEL-04-01

The UI sends attachment paths to the server via the turn API. The server (DEL-04-01 scope) performs authoritative classification and validation. This deliverable is responsible for the UI behaviors that surround that interaction: picking, previewing, sending, handling failure, and rehydrating.

> **Source:** Decomposition DEL-04-02 entry; SPEC.md Section 9.8.

## Requirements

### REQ-PICK-01: File Picker Modal

The UI MUST provide a file picker that allows the user to select one or more files for attachment to a turn.

- The picker MUST support multi-select.
- The picker MUST filter by supported extensions: `.png`, `.jpg`, `.jpeg`, `.gif`, `.webp`, `.pdf`, `.txt`, `.md`, `.csv`.
- The picker MUST support directory navigation.
- **Extension list synchronization:** The mechanism for keeping the picker extension filter synchronized with the server-side supported extension list is TBD. If the server-side list (SPEC.md Section 9.8) changes, the picker filter must be updated to match. See Guidance C1 for rationale.

> **Source:** PLAN Section 2 (`FilePicker.tsx` description). Extension list from SPEC.md Section 9.8. Synchronization note from lensing item A-001.

### REQ-PREV-01: Attachment Preview

The UI MUST display selected attachments before send, showing at minimum the display name and client-classified type.

- Client-supplied attachment metadata (name/mime/type) is for **preview purposes only** and is non-authoritative.

> **Source:** SPEC.md Section 9.8 — "UI stores `Attachment[]` (path, display name, client-classified mime/type) for preview purposes only; server reclassifies."

### REQ-DATA-01: Attachment Data Model

The UI attachment state MUST be structured as `Attachment[]` with at least the following fields:
- `path` — absolute filesystem path
- display name — human-readable file name
- client-classified mime/type — for preview rendering

> **Source:** SPEC.md Section 9.8.

### REQ-SEND-01: Attachment Submission

The UI MUST send attachment paths (not file contents) to the server via the turn API.

- A turn MAY omit text when attachments are present (`message.trim() === ""` with non-empty `attachments`).
- The turn API endpoint is `POST /api/harness/turn` which accepts `attachments` as an array of absolute filesystem path strings.

> **Source:** SPEC.md Section 9.8.

### REQ-OPT-01: Optimistic Send

The UI MUST render the user message optimistically upon send (i.e., display it in the chat before server confirmation).

- **Performance criteria:** TBD — specific latency thresholds for optimistic rendering (e.g., message must appear within N ms of user action) are not yet defined. See lensing item A-004.

> **Source:** SPEC.md Section 9.8 — implied by "UI rolls back the optimistic user message." Performance criteria gap identified by lensing item A-004 (location TBD for threshold values).

### REQ-ROLL-01: Rollback on Send Failure

On send failure, the UI MUST:
1. Roll back the optimistic user message (remove from display).
2. Roll back the streaming placeholder (remove from display).
3. Preserve the draft text for retry.
4. Preserve the attachment selections for retry.

> **Source:** SPEC.md Section 9.8 — "On send failure, UI rolls back the optimistic user message and streaming placeholder, preserving the draft text and attachment selections for retry."

### REQ-ERR-01: Error Information on Send Failure

On send failure, the UI MUST display error information to the user indicating that the send failed and providing context for the failure.

- The specific error information to display (e.g., server error message, generic retry prompt, toast notification vs. inline error, duration of display) is TBD pending UX review.
- See also REQ-ROLL-01 for rollback mechanics.

> **Source:** Lensing items B-003 and F-002. REQ-ROLL-01 specifies rollback mechanics but not user-facing error communication. SPEC.md Section 9.8 describes send failure behavior but does not specify error display format.

### REQ-REHYD-01: Session Rehydration — Attachment Validation

On session rehydration, the UI MUST:
1. Validate the shape of stored attachment records.
2. Silently drop malformed records (records that do not conform to expected shape).
3. Restore valid attachment records.

**Malformed record definition:** A record is considered malformed if it does not conform to the `Attachment` type shape. At minimum, this includes records missing required fields (`path`, display name) or containing fields of incorrect types. Specific additional validation criteria (e.g., path existence checks, character encoding validation) should be documented in the implementation. See Guidance C3.

> **Source:** SPEC.md Section 9.8 — "Session rehydration validates attachment shape — malformed records are silently dropped; valid records are restored." Malformed definition clarification from lensing item A-003; Guidance C3 notes this as **ASSUMPTION**.

### REQ-DRAFT-01: Draft Preservation

The UI MUST preserve draft text and attachment selections during normal UI interaction (e.g., navigating within the app, interacting with other panels) such that they are available for the user to send without re-entry.

- **Scope clarification needed:** Whether draft preservation is required only on send failure, across view switches, across app restarts, or all of these is TBD. The minimum confirmed requirement is preservation on send failure (per REQ-ROLL-01). Broader persistence scope requires human clarification.

> **ASSUMPTION:** Inferred from the rollback requirement (REQ-ROLL-01) and PLAN Section 2 ("draft preservation with optimistic UI rollback on send failure"). The exact scope of "draft preservation" is TBD pending human clarification. Scope gap identified by lensing item A-002.

### REQ-NOAUTH-01: Non-Authoritative Client Metadata

Client-supplied attachment metadata (name, mime, type) MUST NOT be treated as authoritative for execution purposes. The server reclassifies independently.

- The UI MAY use client metadata for display/preview rendering.

> **Source:** SPEC.md Section 9.8 — "Client-supplied attachment metadata (name/mime/type) is non-authoritative and MUST NOT be trusted for execution."

### REQ-A11Y-01: Accessibility (TBD)

TBD — Whether accessibility requirements (keyboard navigation, screen reader support, ARIA attributes) apply to the file picker, attachment preview, and error feedback components. If applicable, specific requirements should be added.

> **TBD** pending human decision / UX review. Identified by lensing item F-001. Guidance C5 also flags this as TBD.

## Standards

| Standard / Governance Doc | Relevance | Accessible |
|---------------------------|-----------|------------|
| SPEC.md Section 9.8 | Harness turn input contract; UI attachment state rules | Yes |
| CONTRACT.md K-INVENT-1 | Unknown values become TBD, not guessed | Yes |
| CONTRACT.md K-GHOST-1 | No ghost inputs in Type 2 agent execution | Yes |
| DIRECTIVE.md Section 2.5 | Non-authoritative convenience state rules | Yes |
| PLAN.md Section 2 | Existing frontend implementation notes | Yes |
| React / Next.js conventions | Standard UI framework patterns | **ASSUMPTION: applicable** (location TBD) |
| Electron desktop conventions | Desktop app context (file system access) | **ASSUMPTION: applicable** (location TBD) |

## Verification

| Requirement | Verification Approach | Verification Artifact |
|-------------|----------------------|----------------------|
| REQ-PICK-01 | Test: open picker, verify multi-select, extension filtering, directory navigation | TEST |
| REQ-PICK-01 (sync) | Review: confirm picker extension list matches SPEC.md Section 9.8 server list | CODE REVIEW |
| REQ-PREV-01 | Test: select files, verify preview displays name and type | TEST |
| REQ-DATA-01 | Test: inspect attachment state structure after file selection | TEST |
| REQ-SEND-01 | Test: send turn with attachments, verify paths sent to API (not file contents) | TEST |
| REQ-SEND-01 (text-free) | Test: send turn with attachments and empty text, verify accepted | TEST |
| REQ-OPT-01 | Test: send turn, verify message appears in chat before server response | TEST |
| REQ-ROLL-01 | Test: simulate send failure, verify optimistic message removed, draft + attachments preserved | TEST |
| REQ-ERR-01 | Test: simulate send failure, verify user receives error information | TEST |
| REQ-REHYD-01 | Test: store malformed + valid attachment records, rehydrate session, verify malformed dropped and valid restored | TEST |
| REQ-DRAFT-01 | Test: add attachments + draft text, interact with other UI elements, verify draft + attachments persist | TEST |
| REQ-NOAUTH-01 | Test: verify client metadata is used only for preview; negative test: confirm client metadata fields are NOT included in server-bound API payload for classification/execution purposes (e.g., inspect request body sent to `POST /api/harness/turn` to confirm no mime/type field is transmitted, or confirm server ignores any such field) | TEST |
| REQ-A11Y-01 | TBD — pending requirement definition | TBD |

## Documentation

### Required Artifacts

| Artifact | Type | Description |
|----------|------|-------------|
| UI attachment pipeline code | CODE | Implementation of picker, preview, send, rollback, rehydration |
| Test suite | TEST | Automated tests covering all requirements above |
