# Procedure — DEL-04-01: Server-side Attachment Resolver + Prompt Mode Selection

## Purpose

This procedure defines the steps to implement, verify, and document the server-side attachment resolver and prompt-mode selection logic for the Chirality Agent Harness. It covers both producing the deliverable artifacts and verifying that they satisfy the requirements in `Specification.md`.

---

## Prerequisites

| # | Prerequisite | Status |
|---|-------------|--------|
| 1 | Access to the Chirality application repository with the `frontend/` source tree | Confirmed |
| 2 | Access to Anthropic SDK content-block contract references (`@anthropic-ai/sdk@0.78.0` local type definitions) | Confirmed (`frontend/node_modules/@anthropic-ai/sdk/resources/messages/messages.d.ts`) |
| 3 | Existing `attachment-resolver.ts` source file in the harness modules layer (referenced in docs/PLAN.md Section 2) | Confirmed |
| 4 | Familiarity with docs/SPEC.md Section 9.8 (Harness Turn Input Contract) | Required reading |
| 5 | Familiarity with docs/harness/chirality_harness_graphs_and_sequence.md (module graph + turn sequence) | Required reading |
| 6 | Node.js / TypeScript development environment for Electron + Next.js | Confirmed |
| 7 | DEL-03-02 turn execution API available or in parallel development | **ASSUMPTION: may be developed concurrently; integration test may require coordination** — see Guidance C7 for coordination strategy |

---

## Steps

### Step 0: Pre-execution Readiness Check

0.1. Before beginning implementation work, confirm the status of all prerequisites in the table above. For each TBD item, verify availability and update the Status column to "Confirmed" or "Blocked."

0.2. If any prerequisite is "Blocked," document the blocker in `MEMORY.md` and escalate to the responsible party or project governance before proceeding.

0.3. Specifically confirm that Anthropic SDK type definitions for content blocks (Prerequisite 2) are accessible before implementing REQ-12 mappings.

> **Lensing note (F-002):** This step was added to enforce prerequisite resolution before execution begins.

### Step 1: Assess Existing Implementation

1.1. Locate the existing `attachment-resolver.ts` file in the `frontend/` source tree. (Source: docs/PLAN.md Section 2 references this file as existing tooling.)

1.2. Review the current implementation against the requirements in `Specification.md` (REQ-01 through REQ-13).

1.3. Document which requirements are already satisfied by the existing code and which require new work or modifications.

1.4. Record findings in deliverable working memory (`MEMORY.md`).

### Step 2: Implement/Verify Attachment Resolver Validation Rules

**Recommended validation order:** The following checks SHOULD be applied in this order to fail fast on inexpensive checks before performing I/O-intensive operations. However, the order is implementation-discretionary provided all checks are applied.

> **Lensing note (C-002):** The recommended order was added because the original listing did not specify whether checks must be applied in a particular order. Order affects which error message the operator sees first and whether expensive I/O (file read) is avoided when an extension check would fail.

2.1. **Extension validation (REQ-03):** Confirm or implement the supported extension allowlist: `.png`, `.jpg`, `.jpeg`, `.gif`, `.webp`, `.pdf`, `.txt`, `.md`, `.csv`. Ensure unsupported extensions produce a clear rejection error. *(Inexpensive string check -- recommended first.)*

2.2. **File accessibility check (REQ-13):** Confirm or implement validation that the path exists and is readable by the server process. Non-existent or unreadable files produce a per-file error with the path and reason.

2.3. **File type validation (REQ-04):** Confirm or implement `stats.isFile()` check. Verify that directories, symlinks, and special files are rejected.

2.4. **Per-file size limit (REQ-05):** Confirm or implement the 10 MB per-file size limit.

2.5. **Total budget enforcement (REQ-06):** Confirm or implement the 18 MB raw-byte total budget per turn using the resolved contract: evaluate attachments in input order, accept only when cumulative accepted bytes remain `<= 18 MB`, reject overflowing files with per-file errors, and continue evaluating later files.

2.6. **Server-side classification (REQ-02):** Confirm that file reading and type classification is performed server-side without relying on client-supplied metadata.

### Step 3: Implement/Verify Content Block Output

3.1. **Content block generation (REQ-12):** Confirm or implement the `resolveAttachmentsToContentBlocks(message, attachmentPaths)` function that returns SDK-compatible content blocks plus per-file error information.

> **Lensing note (E-001):** The function signature `resolveAttachmentsToContentBlocks(message, attachmentPaths)` is used consistently across this Procedure and the Datasheet. The Specification references the function name without parameters for brevity. The authoritative signature with parameters is documented in the Datasheet (Source: docs/harness/chirality_harness_graphs_and_sequence.md, step 108).

3.2. Verify that content blocks match the Anthropic Agent SDK expected input format using local SDK type definitions (`frontend/node_modules/@anthropic-ai/sdk/resources/messages/messages.d.ts`):
   - images -> `ImageBlockParam` (`source.type='base64'` + supported image MIME)
   - PDFs -> `DocumentBlockParam` + `Base64PDFSource`
   - text attachments -> `DocumentBlockParam` + `PlainTextSource` (`media_type='text/plain'`)

3.3. Ensure per-file errors include sufficient detail for operator-facing warning messages (file path, reason for rejection).

### Step 4: Implement/Verify Partial Failure Handling

4.1. **Partial failure, non-fatal (REQ-07):** When at least one attachment resolves (or user text exists), confirm that the runtime proceeds and prepends a warning text block identifying failed attachments. **Note:** Warning text block format is TBD -- see Specification REQ-07 open question and Guidance Conflict Table CT-002. At minimum, include each failed filename and rejection reason.

4.2. **Total failure (REQ-08):** When all attachments fail AND user text is empty, confirm that the request is rejected with HTTP 400. **Note:** Response body format is TBD -- see Specification REQ-08 open question and Guidance Conflict Table CT-003.

4.3. **Text-only with attachments (REQ-09):** Confirm that empty message text with valid attachments produces a successful turn.

### Step 5: Implement/Verify Prompt-mode Selection

5.1. **No-attachment mode (REQ-10):** Confirm or implement that turns without attachments (or where all failed but text exists) use `query({ prompt: string })`.

5.2. **Attachment mode (REQ-11):** Confirm or implement that turns with at least one resolved attachment use `query({ prompt: AsyncIterable<SDKUserMessage> })` with multimodal content blocks.

5.3. Verify that the branch point between the two modes is explicit, tested, and does not allow fallthrough to the wrong mode.

### Step 6: Implement/Verify Turn API Integration

6.1. **Input contract (REQ-01):** Confirm that `POST /api/harness/turn` accepts the optional `attachments` parameter as an array of absolute filesystem path strings.

6.2. Confirm that the turn route calls `resolveAttachmentsToContentBlocks()` when attachments are provided (per the sequence diagram in docs/harness/chirality_harness_graphs_and_sequence.md).

6.3. Confirm that the resolved content blocks are passed to `AgentSdkManager.startTurn()`.

### Step 7: Write and Run Tests

7.1. **Unit tests:** Write tests covering each requirement per the verification matrix in `Specification.md`:
   - Extension allowlist (accept and reject cases)
   - `stats.isFile()` validation (regular files, directories, symlinks)
   - Per-file size limit (boundary: 10 MB exactly, 10 MB + 1 byte)
   - Total budget (boundary: 18 MB exactly, 18 MB + 1 byte)
   - Server-side classification (client metadata ignored)
   - Content block output format
   - Partial failure warning generation
   - Total failure 400 response
   - Empty text with valid attachments
   - File not found / permission denied handling (REQ-13)

7.2. **Integration tests:** Write tests covering end-to-end turn execution:
   - Turn with text + attachments (multimodal mode)
   - Turn with text only (string mode)
   - Turn with attachments only (multimodal mode, empty text)
   - Turn with partial attachment failure (proceeds with warning)
   - Turn with total attachment failure and no text (rejected)
   - Turn where file path does not exist (partial failure with file-not-found error)

7.3. Run all tests and confirm pass status.

### Step 8: Code Review

8.1. **Server-side classification review (V7):** Conduct an explicit code review confirming that client metadata is never used for server-side classification decisions. This is the procedural step corresponding to verification method V7 in the Verification table.

8.2. Review all error paths to confirm they produce defined per-file errors (no unhandled exceptions).

8.3. Review the prompt-mode branch point to confirm it is explicit and does not allow fallthrough.

> **Lensing note (X-004):** Step 8 was expanded into an explicit code review step because the Verification table listed V7 as "Code review" method but no Procedure step previously called for a code review checkpoint.

### Step 9: Update Documentation

9.1. Review and update `Datasheet.md` with any implementation-specific values discovered during development (e.g., actual content block format, actual error message format).

9.2. **Harness validation script assessment:** If harness validation scripts exist (`frontend/scripts/validate-harness-*.mjs`), determine whether they need extension to cover attachment contract behaviors. If validation script updates are required for the deliverable to be considered complete, implement them. If they are optional enhancements, document the decision in `MEMORY.md`.

> **Lensing note (D-002):** Step 9.2 was clarified because the original text left it ambiguous whether validation script updates are a deliverable obligation or optional. The Specification Documentation table marks this as ASSUMPTION. The disposition (required vs. optional) should be confirmed with project governance.

9.3. Record any key decisions, open items, or human rulings in `MEMORY.md`.

---

## Verification

| Check | What to Verify | Method |
|-------|----------------|--------|
| V1 | All 13 requirements (REQ-01 through REQ-13) have corresponding passing tests | Test suite execution |
| V2 | Extension allowlist matches SPEC exactly (9 extensions) | Code review + unit test |
| V3 | Size limits match SPEC exactly (10 MB per-file, 18 MB per-turn) | Code review + unit test |
| V4 | Prompt-mode branch is explicit and covered by tests | Code review + integration test |
| V5 | Partial failure produces warning text block (not silent) | Integration test |
| V6 | Total failure + no text returns 400 | Integration test |
| V7 | Client metadata is never used for server-side classification | Code review (Step 8.1) |
| V8 | Content blocks are SDK-compatible | Unit test + SDK type-definition cross-check |
| V9 | Datasheet values match implementation | Document review |
| V10 | File-not-found and permission-denied paths produce defined per-file errors | Unit test (REQ-13) |
| V11 | Cross-deliverable compatibility with DEL-04-02 | Design review / integration test (XVER-01) |

---

## Records

| Record | Description | Location |
|--------|-------------|----------|
| Test results | Unit and integration test pass/fail report | TBD (test runner output) |
| Code changes | Git diff of implementation changes | Git repository (branch TBD) |
| Working memory | Key decisions, open items, findings | `MEMORY.md` in deliverable folder |
| Requirement traceability | SOW-007/008/009 coverage | `Specification.md` Traceability section |
| Verification evidence | Test coverage mapping to requirements | `Specification.md` Verification matrix |
| Code review record | V7 classification review + error path review | TBD (review tool or `MEMORY.md`) |
| Prerequisite readiness | Step 0 readiness check results | `MEMORY.md` in deliverable folder |
