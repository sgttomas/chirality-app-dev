# Specification — DEL-04-01: Server-side Attachment Resolver + Prompt Mode Selection

## Scope

### Included

This deliverable covers the server-side attachment resolution pipeline and prompt-mode selection logic within the Chirality Agent Harness runtime:

- **Attachment resolver**: Server-side module (`AttachmentResolver`) that accepts an array of absolute filesystem paths, reads/classifies the files, enforces validation rules and budgets, and produces SDK-compatible content blocks (Source: docs/SPEC.md Section 9.8; docs/harness/chirality_harness_graphs_and_sequence.md).
- **Prompt-mode selection**: Runtime logic that selects the correct SDK invocation mode based on whether attachments are present in a turn (Source: docs/SPEC.md Section 9.8).
- **Partial failure handling**: Resilient behavior when some (but not all) attachments fail validation (Source: docs/SPEC.md Section 9.8).
- **Scope items**: SOW-007 (multimodal attachment support), SOW-008 (resolver validation rules), SOW-009 (prompt-mode selection correctness) (Source: Decomposition G7-APPROVED, Scope Ledger).

### Excluded

- **UI attachment pipeline** (picker, preview, rollback, rehydration): covered by DEL-04-02 (Source: Decomposition PKG-04 deliverables table).
- **Session boot and turn API mechanics**: covered by DEL-03-01 and DEL-03-02 in PKG-03 (Source: Decomposition PKG-03 deliverables table).
- **Turn options mapping and fallback chains**: covered by DEL-03-03 (Source: Decomposition PKG-03 deliverables table).
- **Anthropic provider integration**: covered by DEL-03-05 (Source: Decomposition PKG-03 deliverables table).

---

## Requirements

### REQ-01: Attachment Path Input Contract

The turn API (`POST /api/harness/turn`) MUST accept an optional `attachments` parameter as an array of absolute filesystem path strings. Client-supplied attachment metadata (name, MIME type, type classification) is non-authoritative and MUST NOT be trusted for execution decisions.

**Source:** docs/SPEC.md Section 9.8
**Verification:** REQ-01-V

### REQ-02: Server-side File Classification

The `AttachmentResolver` MUST perform server-side file reading and classification. The server re-reads and reclassifies every attachment path; it does not rely on client-provided metadata.

**Source:** docs/SPEC.md Section 9.8 ("Client-supplied attachment metadata... is non-authoritative and MUST NOT be trusted for execution.")

**Verification:** REQ-02-V

### REQ-03: Supported Extension Validation

The resolver MUST accept only files with the following extensions: `.png`, `.jpg`, `.jpeg`, `.gif`, `.webp`, `.pdf`, `.txt`, `.md`, `.csv`. Files with other extensions MUST be rejected.

**Source:** docs/SPEC.md Section 9.8

**Verification:** REQ-03-V

### REQ-04: File Type Validation (`stats.isFile()`)

The resolver MUST verify that each path resolves to a regular file using `stats.isFile()`. Directories, symlinks, and special files MUST be rejected.

**Source:** docs/SPEC.md Section 9.8

**Verification:** REQ-04-V

### REQ-05: Per-file Size Limit

The resolver MUST reject any individual file exceeding 10 MB.

**Source:** docs/SPEC.md Section 9.8

**Verification:** REQ-05-V

### REQ-06: Per-turn Total Budget

The resolver MUST enforce a total per-turn raw-byte budget of 18 MB (18 * 1024 * 1024 bytes; approximately 24 MB after base64 encoding).

**Resolved contract (2026-02-24):**
- Budget accounting is **input-order sequential**: iterate attachments in request order and evaluate each file against the current accepted-byte total.
- A file is accepted only when `acceptedBytes + fileSize <= 18 MB`.
- Files that would exceed the budget are rejected with per-file errors, and evaluation continues for later files.
- Boundary equality is **inclusive**: a file that brings the accepted total to exactly 18 MB MUST be accepted.

**Source:** docs/SPEC.md Section 9.8

**Verification:** REQ-06-V

### REQ-07: Partial Failure — Non-fatal When Executable Content Remains

When at least one attachment resolves successfully (or user text exists), the runtime MUST proceed with the turn and MUST prepend a warning text block to the user content identifying the failed attachments.

**Resolved contract (2026-02-24):**
- Warning text block is a deterministic plain-text structure:
  1. Header line: `Attachment warning: <N> attachment(s) could not be processed. Continuing with available content.`
  2. Section label: `Rejected attachments:`
  3. Up to three bullet lines in input evaluation order, each with filename + reason:
     - `- <basename(path)>: <reason>`
  4. If more than three attachment errors exist, append:
     - `- ... <remainingCount> additional attachment error(s) omitted`
- Minimum content is therefore explicit: every emitted bullet MUST include filename and rejection reason.
- This warning block is prepended to turn content when partial failure is non-fatal.

**Source:** docs/SPEC.md Section 9.8
**Source:** `frontend/src/app/api/harness/turn/route.ts` (`buildAttachmentWarningText`)

**Verification:** REQ-07-V

### REQ-08: Total Failure — Rejection

When all attachments fail validation AND user text is empty (`message.trim() === ""`), the request MUST be rejected with HTTP status 400.

**Resolved contract (2026-02-24):**
- Pre-stream rejection payload is JSON with top-level `error` object:
  - `error.type = "ATTACHMENT_FAILURE"`
  - `error.message = "Turn requires text content or at least one valid attachment"`
  - `error.details = { category: "ALL_ATTACHMENTS_FAILED_NO_TEXT", attachmentErrors: AttachmentError[], rejectedAttachmentCount: number }`
- `attachmentErrors` entries are per-file `{ path, reason }` records.
- `rejectedAttachmentCount` MUST equal the number of rejected attachment records in this rejection path.
- DEL-04-02 consumes this structured details payload for user-facing error-context rendering while preserving rollback behavior.

**Source:** docs/SPEC.md Section 9.8
**Source:** `frontend/src/app/api/harness/turn/route.ts` (`buildAttachmentFailureDetails`)
**Source:** `frontend/src/lib/harness/types.ts` (`AttachmentFailureDetails`)

**Verification:** REQ-08-V

### REQ-09: Text-only Turn with Attachments Permitted

A turn MAY omit text when attachments are present (`message.trim() === ""` with non-empty `attachments`). The resolver and turn handler MUST support this case.

**Source:** docs/SPEC.md Section 9.8

**Verification:** REQ-09-V

### REQ-10: Prompt-mode Selection — No Attachments

When no attachments are present (or all failed and text exists), runtime MUST use SDK `query({ prompt: string })`.

**Source:** docs/SPEC.md Section 9.8

**Verification:** REQ-10-V

### REQ-11: Prompt-mode Selection — Attachments Present

When attachments are present and at least one resolves successfully, runtime MUST build multimodal content blocks and use SDK `query({ prompt: AsyncIterable<SDKUserMessage> })`.

**Source:** docs/SPEC.md Section 9.8

**Verification:** REQ-11-V

### REQ-12: Content Block Output

The resolver function (`resolveAttachmentsToContentBlocks(message, attachmentPaths)`) MUST return content blocks compatible with the Anthropic Agent SDK input format, plus per-file error information for any failed attachments.

**Resolved contract (2026-02-24):**
- Supported image attachments (`image/png`, `image/jpeg`, `image/gif`, `image/webp`) map to SDK `image` content blocks with base64 source:
  - `type: "image"`
  - `source: { type: "base64", media_type: <image mime>, data: <base64 bytes> }`
- PDF attachments (`application/pdf`) map to SDK `document` content blocks with base64 PDF source:
  - `type: "document"`
  - `title: <basename(path)>`
  - `source: { type: "base64", media_type: "application/pdf", data: <base64 bytes> }`
- Text attachments (`text/plain`, `text/markdown`, `text/csv`) map to SDK `document` content blocks with plain-text source:
  - `type: "document"`
  - `title: <basename(path)>`
  - `source: { type: "text", media_type: "text/plain", data: <utf8 text> }`
- Any unexpected non-image MIME outside the supported set remains a guarded fallback text block indicating unmapped multimodal type.

**Source:** docs/harness/chirality_harness_graphs_and_sequence.md (Sequence diagram steps 108-109)
**Source:** `frontend/node_modules/@anthropic-ai/sdk/resources/messages/messages.d.ts` (`DocumentBlockParam`, `Base64PDFSource`, `PlainTextSource`, `ImageBlockParam`)

**Verification:** REQ-12-V

### REQ-13: File Accessibility Validation

The resolver MUST reject any path that references a non-existent file or a file that the server process cannot read (e.g., permission denied). Rejection MUST produce a per-file error with the path and reason.

**ASSUMPTION:** This requirement is inferred from practical execution necessity. docs/SPEC.md Section 9.8 does not explicitly address file-not-found or permission-denied scenarios, but these are unavoidable runtime paths that must produce defined behavior rather than unhandled exceptions.

> **Lensing note (X-002):** This requirement was added because the existing requirement set covers extension, isFile, size, and budget validation but does not address the case where a path references a non-existent file or a file the process cannot read.

**Verification:** REQ-13-V

---

## Standards

| Standard / Document | Relevance | Accessibility |
|---------------------|-----------|---------------|
| docs/SPEC.md Section 9.8 — Harness Turn Input Contract | Authoritative specification for resolver behavior, validation rules, prompt-mode selection, partial failure semantics | Accessible |
| docs/CONTRACT.md — K-GHOST-1 | No ghost inputs; context limited to folder contents + declared references | Accessible |
| docs/CONTRACT.md — K-INVENT-1 | Unknown values become TBD, not guessed | Accessible |
| docs/harness/chirality_harness_graphs_and_sequence.md | Module architecture and turn sequence | Accessible |
| Anthropic SDK message type definitions (`@anthropic-ai/sdk@0.78.0`) | SDK `query()` message content contract and supported request content block shapes | Accessible (`frontend/node_modules/@anthropic-ai/sdk/resources/messages/messages.d.ts`) |

---

## Verification

| Verification ID | Requirement | Approach | Pass Criteria |
|-----------------|-------------|----------|---------------|
| REQ-01-V | REQ-01 | Unit test | Turn API accepts `attachments` as array of strings; client metadata is ignored |
| REQ-02-V | REQ-02 | Unit test | Resolver reads and classifies files server-side; does not use client-supplied MIME/type |
| REQ-03-V | REQ-03 | Unit test | Supported extensions pass; unsupported extensions are rejected with error |
| REQ-04-V | REQ-04 | Unit test | Directories, symlinks, and special files are rejected; regular files pass |
| REQ-05-V | REQ-05 | Unit test | Files > 10 MB are rejected; files <= 10 MB pass |
| REQ-06-V | REQ-06 | Unit test | Confirms ordered sequential accounting: (a) cumulative total exactly 18 MB is accepted, (b) files that would exceed 18 MB are rejected, and (c) input-order changes can change which file is rejected while preserving the same budget rule. |
| REQ-07-V | REQ-07 | Integration test | Partial failure with remaining content proceeds; warning text block is prepended with deterministic format: header + `Rejected attachments:` section + filename/reason bullets, including omission summary when error count exceeds three. |
| REQ-08-V | REQ-08 | Integration test | All attachments fail + empty text returns HTTP 400 with structured payload: `error.type=ATTACHMENT_FAILURE`, `error.details.category=ALL_ATTACHMENTS_FAILED_NO_TEXT`, `error.details.attachmentErrors[]` (`path`, `reason`), and `error.details.rejectedAttachmentCount`. |
| REQ-09-V | REQ-09 | Unit test | Empty message with valid attachments produces a successful turn |
| REQ-10-V | REQ-10 | Unit/integration test | No-attachment turns use `query({ prompt: string })` |
| REQ-11-V | REQ-11 | Unit/integration test | Attachment turns use `query({ prompt: AsyncIterable<SDKUserMessage> })` with multimodal blocks |
| REQ-12-V | REQ-12 | Unit test | Manager formatting tests verify: (a) images map to SDK `image` base64 blocks, (b) PDFs map to SDK `document` base64-PDF blocks, (c) text attachments map to SDK `document` plain-text blocks, and (d) unsupported unexpected MIME remains explicit fallback text. |
| REQ-13-V | REQ-13 | Unit test | Non-existent paths return per-file error with path and "file not found" reason; unreadable paths return per-file error with path and "permission denied" reason. **ASSUMPTION.** |
| XVER-01 | Cross-deliverable | Integration test / design review | DEL-04-01 resolver output (content block format, error response format) is compatible with DEL-04-02 UI expectations (rollback + structured error-context display). Validated via route/error-display regression tests in `frontend/src/__tests__/api/harness/routes.test.ts` and `frontend/src/__tests__/lib/harness-error-display.test.ts`. |

> **Lensing note (E-002):** XVER-01 was added because Guidance C5 documents the DEL-04-01/DEL-04-02 contract but no verification item previously confirmed cross-deliverable compatibility.

---

## Documentation

### Required Artifacts

| Artifact | Type | Description |
|----------|------|-------------|
| `attachment-resolver.ts` (or equivalent) | CODE | Server-side attachment resolver module |
| Prompt-mode selection logic | CODE | Branching logic in turn handler for string vs. multimodal prompt |
| Unit tests | TEST | Cover REQ-01 through REQ-13 per verification matrix |
| Integration tests | TEST | End-to-end turn execution with attachments, partial failure, and prompt-mode switching |
| Harness validation script updates | DOC | Update `frontend/scripts/validate-harness-*.mjs` to cover attachment contract behaviors (**ASSUMPTION: existing validation scripts may need extension** -- see Procedure Step 8.2 for disposition) |

### Traceability

| Scope Item | Requirements Covered |
|------------|---------------------|
| SOW-007 | REQ-01, REQ-02, REQ-09, REQ-11, REQ-12, REQ-13 |
| SOW-008 | REQ-03, REQ-04, REQ-05, REQ-06, REQ-07, REQ-08, REQ-13 |
| SOW-009 | REQ-10, REQ-11 |
