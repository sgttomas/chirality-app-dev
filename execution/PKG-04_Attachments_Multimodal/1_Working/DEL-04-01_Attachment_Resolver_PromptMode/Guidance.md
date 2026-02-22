# Guidance — DEL-04-01: Server-side Attachment Resolver + Prompt Mode Selection

## Purpose

This deliverable exists to ensure that the Chirality Agent Harness can robustly handle multimodal turns -- turns where the operator attaches local files (images, PDFs, text documents) alongside or instead of text input. The attachment resolver provides the server-side "last line of defense" that validates, reads, classifies, and transforms file paths into SDK-compatible content blocks before they reach the Anthropic Agent SDK.

The prompt-mode selection logic determines which SDK invocation path to use based on whether resolved attachments are present, ensuring the correct API contract is satisfied at the SDK boundary.

Together, these two concerns fulfill OBJ-003: "Attachment-enabled turns are robust and UX-safe" (Source: Decomposition G7-APPROVED, Objectives).

---

## Principles

### P1: Server Authority Over Classification

Client-supplied attachment metadata (file name, MIME type, type classification) is convenience data for UI preview purposes only. The server MUST re-read and reclassify every file. This principle prevents spoofed or stale client metadata from influencing execution.

**Source:** docs/SPEC.md Section 9.8 ("Client-supplied attachment metadata... is non-authoritative and MUST NOT be trusted for execution.")

### P2: Fail-Safe Budget Enforcement

Size limits (per-file and per-turn) exist to prevent excessively large payloads from reaching the SDK. The raw-byte budget of 18 MB accounts for the base64 encoding overhead (~33%) that produces approximately 24 MB at the API wire. Budget enforcement MUST happen before file content is sent to the SDK, not after.

**Source:** docs/SPEC.md Section 9.8

### P3: Graceful Degradation Over Hard Failure

Partial attachment failure should not block an otherwise valid turn. If the operator sends three files and one is invalid, the turn should proceed with the two valid files and a clear warning. This preserves operator workflow while maintaining transparency about what was excluded.

**Source:** docs/SPEC.md Section 9.8 (partial failure semantics)

### P4: Clear SDK Boundary

The prompt-mode selection is a clean branch point: no attachments means a simple string prompt; attachments present means multimodal content blocks via `AsyncIterable<SDKUserMessage>`. Mixing these modes or falling through to the wrong one is a category error. The boundary should be explicit and testable.

**Source:** docs/SPEC.md Section 9.8

---

## Considerations

### C1: Extension Allowlist vs. MIME Detection

The specification defines a fixed extension allowlist (`.png`, `.jpg`, `.jpeg`, `.gif`, `.webp`, `.pdf`, `.txt`, `.md`, `.csv`). This is simpler and more predictable than MIME-type sniffing but means that valid files with non-standard extensions (e.g., a PNG saved as `.image`) will be rejected. This is an intentional design trade-off favoring predictability. (Source: docs/SPEC.md Section 9.8)

### C2: Budget Accounting Strategy

The total budget of 18 MB raw is enforced across all attachments in a single turn. Implementation should consider whether to:
- **Reject the entire batch** if the total would exceed the budget, or
- **Accept files in order until the budget is exhausted** and reject the remainder.

The specification does not prescribe which strategy to use. **ASSUMPTION: The simpler approach (reject entire batch when total exceeds budget) is likely intended, but this should be confirmed with implementation review.**

Additional open questions:
- **Boundary equality:** Does a file that brings the aggregate to exactly 18 MB pass or fail? TBD.
- **Accounting order:** If the sequential strategy is chosen, does the order of files in the input array determine acceptance priority? TBD.

> **Lensing note (A-001, A-003):** These questions are surfaced as normative gaps. A human ruling or architecture decision is needed to resolve them before implementation can deterministically handle boundary conditions. See also Specification REQ-06 open questions and Conflict Table entry CT-001.

### C3: Error Reporting Granularity

Per-file errors are returned alongside resolved content blocks (Source: docs/harness/chirality_harness_graphs_and_sequence.md, sequence diagram step 109). Error messages should be specific enough for the operator to understand why a file was rejected (e.g., "File exceeds 10 MB limit: 14.2 MB" rather than "File too large") while avoiding exposure of internal filesystem paths beyond what the operator already provided.

### C4: Symlink Rejection Rationale

The `stats.isFile()` check rejects symlinks. This is consistent with the project's "no ghost inputs" principle (K-GHOST-1 in docs/CONTRACT.md): a symlink could point to a file outside the operator's intended context, and following it silently would violate sealed-context expectations. The rejection is security-motivated, not a limitation.

### C5: Relationship to DEL-04-02 (UI Attachment Pipeline)

DEL-04-02 handles the UI-side attachment lifecycle (picker, preview, draft preservation, rollback on failure, session rehydration). The UI stores `Attachment[]` with path, display name, and client-classified metadata for preview purposes. On send, the UI provides only the paths; the server (this deliverable) does all classification work. The contract between DEL-04-01 and DEL-04-02 is:

- **DEL-04-02 provides:** Array of absolute path strings via the turn API.
- **DEL-04-01 provides:** Resolved content blocks (or errors) and appropriate prompt-mode selection.
- **DEL-04-02 reacts to:** Send failure (HTTP 400 on total failure) by rolling back the optimistic UI message.

**Cross-deliverable interface note:** The HTTP 400 response body format (REQ-08 TBD) and the content block output schema (REQ-12 TBD) are the two concrete interface points that DEL-04-02 depends on. These should be co-defined with the DEL-04-02 team. See Specification XVER-01.

(Source: docs/SPEC.md Section 9.8; Decomposition PKG-04 deliverables table)

### C6: Relationship to DEL-03-02 (Turn Execution API)

The attachment resolver is invoked within the turn execution flow managed by DEL-03-02. The integration point is the `POST /api/harness/turn` route, which calls `resolveAttachmentsToContentBlocks()` when attachments are provided before proceeding to `AgentSdkManager.startTurn()`. (Source: docs/harness/chirality_harness_graphs_and_sequence.md, sequence diagram)

### C7: DEL-03-02 Integration Coordination

DEL-03-02 may be developed concurrently with DEL-04-01 (see Procedure Prerequisite 7). Integration testing requires coordination on:
- **Mock strategy:** If DEL-03-02 is not ready, DEL-04-01 integration tests may need to mock the turn execution API or use a test harness.
- **Integration branch:** Determine whether a shared integration branch or feature flags are used for cross-deliverable testing.
- **Contract alignment:** The `resolveAttachmentsToContentBlocks()` function signature and return type must be stable before integration begins.

> **Lensing note (D-001):** This consideration was added because Procedure Prerequisite 7 flags concurrent development but no guidance existed on how to handle this dependency.

**ASSUMPTION: Coordination strategy is TBD and should be resolved with the DEL-03-02 team or project scheduling.**

---

## Quality Attributes

This section captures non-functional quality expectations for the attachment resolver. These are evaluatively necessary for a backend feature slice that processes potentially large files.

| Quality Attribute | Expectation | Status |
|-------------------|-------------|--------|
| Resolver latency budget | TBD — maximum acceptable wall-clock time for resolving N files of maximum size | TBD (architecture / performance requirements) |
| Maximum I/O time per file | TBD — threshold for individual file read operations before timeout | TBD (architecture / performance requirements) |
| Memory overhead | TBD — whether file contents are held in memory or streamed, and the peak memory budget | TBD (architecture decision) |
| Reliability | Resolver MUST NOT crash on malformed inputs; all error paths must produce defined per-file errors | Derived from P3 (Graceful Degradation) and REQ-13 |

> **Lensing note (F-003):** This section was added because the document articulated functional principles and trade-offs but did not state any non-functional quality attribute targets.

---

## Trade-offs

| Decision | Alternative | Rationale |
|----------|-------------|-----------|
| Extension allowlist (fixed list) | MIME-type detection | Predictability and security over flexibility (Source: docs/SPEC.md Section 9.8) |
| Server-side classification only | Trust client classification | Prevents spoofed/stale metadata from influencing execution (Source: docs/SPEC.md Section 9.8) |
| Partial failure is non-fatal | Reject entire turn on any failure | Preserves operator workflow; matches SPEC behavior (Source: docs/SPEC.md Section 9.8) |
| `stats.isFile()` rejects symlinks | Follow symlinks | Aligns with no-ghost-inputs principle K-GHOST-1 (Source: docs/CONTRACT.md) |
| Two SDK modes (string vs. multimodal) | Single unified mode | Matches SDK API contract; avoids unnecessary overhead on text-only turns (Source: docs/SPEC.md Section 9.8) |

---

## Examples

### Example 1: Successful multimodal turn

Operator sends a turn with text "Review this drawing" and attachments `["/path/to/drawing.png", "/path/to/notes.md"]`.

1. Resolver validates both paths: regular files, supported extensions, within size limits.
2. Resolver reads file contents, classifies (image vs. text), produces content blocks.
3. Prompt-mode selection: attachments present, so runtime uses `query({ prompt: AsyncIterable<SDKUserMessage> })` with multimodal content blocks.
4. Turn proceeds normally.

### Example 2: Partial failure

Operator sends attachments `["/path/to/photo.png", "/path/to/archive.zip", "/path/to/spec.pdf"]` with text "Check these files."

1. `photo.png`: resolves successfully (supported extension, regular file, within size).
2. `archive.zip`: rejected (unsupported extension).
3. `spec.pdf`: resolves successfully.
4. Partial failure: 1 of 3 failed, but executable content remains (2 resolved + text).
5. Runtime prepends warning block: "`archive.zip` rejected: unsupported file extension."
6. Turn proceeds with `photo.png` + `spec.pdf` + warning + user text.

### Example 3: Total failure with no text

Operator sends attachments `["/path/to/data.xlsx"]` with empty text.

1. `data.xlsx`: rejected (unsupported extension).
2. Total failure: all attachments failed, no user text.
3. Runtime returns HTTP 400.

### Example 4: File not found

Operator sends attachments `["/path/to/missing.png"]` with text "Check this."

1. `missing.png`: path does not exist on the filesystem -- rejected with error "file not found."
2. Partial failure: 0 of 1 attachments resolved, but user text exists.
3. Runtime prepends warning block: "`missing.png` rejected: file not found."
4. Turn proceeds in text-only mode using `query({ prompt: string })`.

> **Lensing note (X-002):** Example 4 was added to illustrate the file accessibility validation path (REQ-13).

---

## Conflict Table (for human ruling)

| Conflict ID | Conflict | Source A | Source B | Impacted Sections | Proposed Authority (PROPOSAL) | Human Ruling |
|---|---|---|---|---|---|---|
| CT-001 | Budget enforcement strategy (reject-entire-batch vs. accept-until-exhausted) and boundary behavior at exactly 18 MB are unspecified | docs/SPEC.md Section 9.8 (states budget but not algorithm) | Guidance C2 (identifies ambiguity) | Specification REQ-06, REQ-06-V; Procedure Step 2.4; Datasheet Validation Rules | docs/SPEC.md Section 9.8 or architecture decision | TBD |
| CT-002 | Warning text block minimum content/format is unspecified | docs/SPEC.md Section 9.8 (requires warning but not format) | Specification REQ-07 / REQ-07-V | Specification REQ-07, REQ-07-V; Procedure Step 4.1 | docs/SPEC.md Section 9.8 or UX design decision | TBD |
| CT-003 | HTTP 400 response body format for total failure is unspecified; DEL-04-02 needs to parse it | docs/SPEC.md Section 9.8 (requires 400 but not body) | Guidance C5 (identifies cross-deliverable need) | Specification REQ-08, REQ-08-V; XVER-01 | docs/SPEC.md Section 9.8 or architecture decision | TBD |
| CT-004 | SDK content block format is not concretely defined; acceptance criteria for REQ-12 depend on it | Specification REQ-12 ("SDK-compatible content blocks") | Datasheet Content Block Output Format (ASSUMPTION) | Specification REQ-12, REQ-12-V; Procedure Step 3.2 | Anthropic Agent SDK documentation | TBD |
