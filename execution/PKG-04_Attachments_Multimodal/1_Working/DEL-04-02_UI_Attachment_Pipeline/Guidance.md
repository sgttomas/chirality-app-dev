# Guidance — DEL-04-02 UI Attachment Pipeline (Picker, Preview, Rollback, Rehydration)

## Purpose

This deliverable exists to ensure that users of the Chirality desktop app can attach files to harness turns with a reliable, predictable UI experience. The attachment pipeline must handle the full lifecycle from file selection through send, including graceful handling of failures and session continuity across rehydration.

The UI attachment pipeline is the user-facing complement to the server-side attachment resolver (DEL-04-01). Together, they fulfill OBJ-003: "Attachment-enabled turns are robust and UX-safe."

> **Source:** Decomposition OBJ-003 (directly mapped to DEL-04-02 in PKG-04 deliverable table); SOW-010; SPEC.md Section 9.8.

## Principles

### P1: Server Is Authoritative; UI Is for Preview

The fundamental architectural principle is that **client-supplied metadata is non-authoritative**. The server independently classifies, validates, and enforces budgets on attachments (SPEC.md Section 9.8). The UI uses its own classification only for rendering previews (file type icons, display names). This separation ensures that security and correctness are not dependent on client-side logic.

> **Source:** SPEC.md Section 9.8 — "Client-supplied attachment metadata (name/mime/type) is non-authoritative and MUST NOT be trusted for execution."

### P2: Optimistic UI With Safe Rollback

The send flow uses an optimistic pattern: the user's message appears in the chat immediately upon send, before server confirmation. On failure, the UI rolls back cleanly and preserves user input. This pattern prioritizes perceived responsiveness while maintaining correctness.

> **Source:** SPEC.md Section 9.8; PLAN Section 2 — "draft preservation with optimistic UI rollback on send failure."

### P3: Defensive Rehydration

Session rehydration must be defensive: validate the shape of stored records, drop anything malformed, and restore only valid data. This prevents corrupted or stale session state from causing runtime errors or misleading displays.

> **Source:** SPEC.md Section 9.8 — "Session rehydration validates attachment shape — malformed records are silently dropped; valid records are restored."

### P4: Non-Authoritative Convenience State

Attachment selections, draft text, and similar UI state are convenience state (per DIRECTIVE.md Section 2.5). They MUST NOT be treated as project truth and MUST NOT override governance enforcement. This aligns with the broader principle that filesystem is the database and UI state is ephemeral.

> **Source:** DIRECTIVE.md Section 2.5.

## Considerations

### C1: Picker Extension Filtering vs. Server Validation

The file picker filters by supported extensions (`.png`, `.jpg`, `.jpeg`, `.gif`, `.webp`, `.pdf`, `.txt`, `.md`, `.csv`) as a convenience to prevent users from selecting unsupported files. However, the server-side resolver is the enforcement point. If the supported extension list changes server-side, the picker filter should be updated to match. The mechanism for keeping these lists synchronized is TBD.

A prescriptive synchronization mechanism should be established (e.g., a shared constants file imported by both client and server, or a server endpoint that returns the current supported list). Until this is defined, the picker filter must be manually kept in sync with SPEC.md Section 9.8.

> **ASSUMPTION:** The extension list in the picker mirrors the server-side list defined in SPEC.md Section 9.8. No automated synchronization mechanism is currently specified. Lensing item A-001 identified the lack of a prescriptive synchronization mechanism.

### C2: Draft Preservation Scope

The SPEC and PLAN describe "draft preservation" in the context of send-failure rollback. Whether draft state persists across view switches (e.g., navigating from PIPELINE to PORTAL and back) or across app restarts is TBD. The minimum requirement is preservation on send failure.

The scope determination has implementation implications: send-failure-only preservation requires in-memory state, while cross-restart persistence would require durable storage (e.g., local storage, session state file).

> **ASSUMPTION:** Draft preservation is at minimum required for send-failure rollback (REQ-ROLL-01). Broader persistence scope is TBD. Lensing item A-002 identified scope ambiguity.

### C3: Rehydration Shape Validation

The SPEC states that malformed records are "silently dropped." The definition of "malformed" is not further specified. A reasonable interpretation is that a record missing required fields (path, display name) or containing invalid types would be considered malformed.

The Specification (REQ-REHYD-01) now documents the minimum malformed criteria. Implementers should consider whether additional checks are warranted (e.g., verifying that `path` points to an existing file, checking for path traversal patterns, validating character encoding).

> **ASSUMPTION:** "Malformed" means records that do not conform to the `Attachment` type shape (missing required fields or wrong types). Specific validation criteria should be documented in the implementation. Lensing item A-003 identified this as a weak statement requiring human ruling.

### C4: Partial Failure Display

When the server reports partial attachment failure (some attachments resolved, some failed), the server prepends a warning text block to the user content (SPEC.md Section 9.8). The UI should be prepared to render this warning naturally within the assistant or system response. No special UI treatment is specified beyond standard message rendering.

> **Source:** SPEC.md Section 9.8 — partial attachment failure handling.

### C5: Accessibility and Error Communication

Users should receive clear feedback when attachments fail, are removed during rehydration, or are filtered by the picker. While the SPEC specifies "silently dropped" for rehydration, user-facing error messaging for send failures and picker restrictions is a UX judgment call.

Specific UX elements to determine include: toast notification vs. inline error display, duration of error visibility, and whether error messages include server-provided detail or use generic prompts. See REQ-ERR-01 in Specification.

> **ASSUMPTION:** Accessibility and error messaging details are TBD pending UX review. Lensing items F-001 and F-002 identified these gaps.

### C6: Dependency Governance — DEL-04-01 and DEL-03-02

The Procedure lists DEL-04-01 (Server-side Attachment Resolver) and DEL-03-02 (Turn Execution API + SSE Streaming) as prerequisites with ASSUMPTION status. These dependencies are inferred from the architectural split described in the decomposition and SPEC.md Section 9.8 but are not yet formally declared in `_DEPENDENCIES.md` (dependency extraction has not been run for this deliverable).

**Rationale for ASSUMPTION status:** The DEPENDENCIES agent has not yet run for DEL-04-02 (`_DEPENDENCIES.md` shows `PENDING_EXTRACTION`). The dependencies are architecturally self-evident from SPEC.md Section 9.8 (UI sends to server turn API; server resolves attachments) but formal declaration is deferred until DEPENDENCIES runs. Stubbing is acceptable for initial implementation of UI-side behaviors that do not require live server responses (picker, preview, draft preservation, rehydration). Integration tests (Procedure Step 8) require at least partial availability or stubs of DEL-04-01 and DEL-03-02.

> **Source:** Lensing item C-001. Decomposition DEL-04-02 entry; SPEC.md Section 9.8; `_DEPENDENCIES.md` (status: PENDING_EXTRACTION).

### C7: Feature Flag / Activation Model

Whether the attachment pipeline is feature-flagged (can be disabled) or always active is not documented in any source material. This is an architectural decision that affects testing strategy (must test both enabled and disabled states if flagged) and rollout approach.

> **TBD** — No source material addresses activation model. Lensing item X-001 identified this as an undocumented decision requiring human ruling.

## Trade-offs

### T1: Optimistic Rendering vs. Server Round-Trip Wait

**Chosen:** Optimistic rendering (display message immediately, rollback on failure).

**Alternative:** Wait for server confirmation before displaying the message.

**Rationale:** Optimistic rendering improves perceived responsiveness. The cost is added complexity in rollback logic. The SPEC explicitly chooses the optimistic pattern.

> **Source:** SPEC.md Section 9.8.

### T2: Silent Drop vs. User Notification on Rehydration

**Chosen:** Silently drop malformed attachment records during rehydration.

**Alternative:** Notify the user that some attachment records were dropped.

**Rationale:** The SPEC explicitly states "silently dropped." This avoids confusing the user with errors about state they did not create. If future UX review determines notification is preferable, this is a candidate for a Conflict Table entry.

> **Source:** SPEC.md Section 9.8.

### T3: Client-Side vs. Server-Side Extension Filtering

**Chosen:** Both (client-side filtering in picker + server-side enforcement in resolver).

**Rationale:** Client-side filtering provides immediate UX feedback. Server-side enforcement provides security. The two must stay in sync (see C1).

> **Source:** SPEC.md Section 9.8; PLAN Section 2.

## Examples

### Example 1: Successful Attachment Send Flow

1. User opens file picker, selects `diagram.png` and `notes.md`.
2. UI displays preview: two attachment chips with file names and type indicators.
3. User types "Review these files" and clicks Send.
4. UI optimistically renders the user message (text + attachment chips) in the chat.
5. UI shows streaming placeholder for assistant response.
6. Server resolves attachments, classifies them, builds multimodal content blocks, executes the turn.
7. Assistant response streams in via SSE; placeholder is replaced with streamed content.

> **Source:** Derived from SPEC.md Section 9.8 flow description.

### Example 2: Send Failure Rollback Flow

1. User selects attachments and types a message, clicks Send.
2. UI optimistically renders the user message.
3. Server returns an error (e.g., all attachments fail validation + no user text).
4. UI removes the optimistic user message from chat.
5. UI removes the streaming placeholder.
6. Draft text is restored to the input field.
7. Attachment selections are restored to the attachment preview area.
8. User can modify and retry.

> **Source:** SPEC.md Section 9.8 rollback rules.

### Example 3: Rehydration with Malformed Records

1. Session state contains three stored attachment records: two valid, one missing the `path` field.
2. On session rehydration, the UI validates each record's shape.
3. The malformed record (missing `path`) is silently dropped.
4. The two valid records are restored.

> **Source:** SPEC.md Section 9.8 rehydration rules.

## Conflict Table (for human ruling)

| Conflict ID | Conflict | Source A | Source B | Impacted Sections | Proposed Authority (PROPOSAL) | Human Ruling |
|---|---|---|---|---|---|---|
| CT-001 | "Attachment bar" vs. "attachment preview area" — terminology varies across Guidance Example 2 and Procedure Step 7 test table. Normalized to "attachment preview area" in Pass 3 enrichment; original term "attachment bar" was not sourced from any specification. | Guidance.md Example 2 (previously "attachment bar") | Procedure.md Step 7 (previously "attachment list") | Guidance Examples, Procedure Step 7 test table, Specification REQ-PREV-01 | Specification.md (as normative source for UI component terminology) | TBD |
