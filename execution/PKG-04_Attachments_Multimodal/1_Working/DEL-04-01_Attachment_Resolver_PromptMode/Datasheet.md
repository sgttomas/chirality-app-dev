# Datasheet — DEL-04-01: Server-side Attachment Resolver + Prompt Mode Selection

## Identification

| Field | Value |
|-------|-------|
| **Deliverable ID** | DEL-04-01 |
| **Name** | Server-side Attachment Resolver + Prompt Mode Selection |
| **Package** | PKG-04 — Attachments & Multimodal Turns |
| **Type** | BACKEND_FEATURE_SLICE |
| **Responsible Party** | TBD |
| **Context Envelope** | M |
| **Scope Coverage** | SOW-007, SOW-008, SOW-009 |
| **Objective** | OBJ-003 — Attachment-enabled turns are robust and UX-safe |
| **Anticipated Artifacts** | CODE / TEST / DOC |
| **Decomposition Ref** | `execution/_Decomposition/ChiralityApp_SoftwareDecomposition_2026-02-21_G7-APPROVED.md` |

## Attributes

### Attachment Resolver Module

| Attribute | Value | Source |
|-----------|-------|--------|
| Module name | `AttachmentResolver` | docs/harness/chirality_harness_graphs_and_sequence.md (Module dependency graph) |
| Function signature | `resolveAttachmentsToContentBlocks(message, attachmentPaths)` | docs/harness/chirality_harness_graphs_and_sequence.md (Sequence diagram, step 108) |
| Input | Array of absolute filesystem path strings | docs/SPEC.md Section 9.8 |
| Output | Content blocks (+ per-file errors) | docs/harness/chirality_harness_graphs_and_sequence.md (Sequence diagram, step 109) |
| Classification authority | Server-side only; client-supplied metadata is non-authoritative | docs/SPEC.md Section 9.8 |

### Content Block Output Format

| Attribute | Value | Source |
|-----------|-------|--------|
| Output schema | TBD — expected to include `type` (image/text/document) and `source` (base64-encoded data or text content) fields per SDK content block convention | **ASSUMPTION:** inferred from SDK patterns; `location TBD` (Anthropic Agent SDK documentation not accessed) |
| SDK compatibility contract | Content blocks MUST be compatible with `query({ prompt: AsyncIterable<SDKUserMessage> })` input format | docs/SPEC.md Section 9.8 |
| Per-file error structure | TBD — must include file path and rejection reason for operator-facing warning messages | docs/harness/chirality_harness_graphs_and_sequence.md (Sequence diagram, step 109) |

> **Lensing note (B-002):** This section was added to capture the output content block schema, which is referenced by Specification REQ-12 but not concretely defined. The exact SDK content block structure should be confirmed against Anthropic Agent SDK documentation when accessible.

### Supported Extensions

| Extension | Source |
|-----------|--------|
| `.png` | docs/SPEC.md Section 9.8 |
| `.jpg` | docs/SPEC.md Section 9.8 |
| `.jpeg` | docs/SPEC.md Section 9.8 |
| `.gif` | docs/SPEC.md Section 9.8 |
| `.webp` | docs/SPEC.md Section 9.8 |
| `.pdf` | docs/SPEC.md Section 9.8 |
| `.txt` | docs/SPEC.md Section 9.8 |
| `.md` | docs/SPEC.md Section 9.8 |
| `.csv` | docs/SPEC.md Section 9.8 |

### Size Limits

| Limit | Value | Source |
|-------|-------|--------|
| Per-file size limit | 10 MB | docs/SPEC.md Section 9.8 |
| Total per-turn raw-byte budget | 18 MB raw (~24 MB after base64 encoding) | docs/SPEC.md Section 9.8 |

### Validation Rules

| Rule | Description | Source |
|------|-------------|--------|
| Extension check | Only supported extensions are accepted | docs/SPEC.md Section 9.8 |
| `stats.isFile()` check | Directories, symlinks, and special files are rejected | docs/SPEC.md Section 9.8 |
| Per-file size limit | Files exceeding 10 MB are rejected | docs/SPEC.md Section 9.8 |
| Total budget enforcement | Aggregate raw bytes must not exceed 18 MB | docs/SPEC.md Section 9.8 |
| File accessibility check | Paths referencing non-existent or unreadable files MUST be rejected | **ASSUMPTION:** inferred from practical execution requirements; docs/SPEC.md Section 9.8 does not explicitly address file-not-found scenarios |

> **Lensing note (X-002):** File accessibility check added as a validation rule. While docs/SPEC.md Section 9.8 does not explicitly address the case where a path references a non-existent file or a file the process cannot read, this is a practical execution path that must be handled.

### Prompt Mode Selection

| Condition | SDK Call Mode | Source |
|-----------|--------------|--------|
| No attachments | `query({ prompt: string })` | docs/SPEC.md Section 9.8 |
| Attachments present | `query({ prompt: AsyncIterable<SDKUserMessage> })` — builds multimodal content blocks | docs/SPEC.md Section 9.8 |

### Partial Failure Handling

| Scenario | Behavior | Source |
|----------|----------|--------|
| At least one attachment resolves (or user text exists) | Runtime proceeds; prepends a warning text block to user content | docs/SPEC.md Section 9.8 |
| All attachments fail AND user text is empty | Request is rejected with HTTP 400 | docs/SPEC.md Section 9.8 |

### Turn Input Contract

| Field | Value | Source |
|-------|-------|--------|
| Endpoint | `POST /api/harness/turn` | docs/SPEC.md Section 9.8 |
| Attachments parameter | Optional `attachments` array of absolute filesystem path strings | docs/SPEC.md Section 9.8 |
| Text-only turn with attachments | Permitted (`message.trim() === ""` with non-empty `attachments`) | docs/SPEC.md Section 9.8 |

## Conditions

| Condition | Description | Source |
|-----------|-------------|--------|
| Platform | macOS 15+, Apple Silicon only | Decomposition DEC-PLAT-001 |
| Network | Outbound limited to Anthropic API only | Decomposition DEC-NET-001 |
| Runtime | Electron + Next.js desktop application | docs/PLAN.md Section 2 |
| SDK dependency | Anthropic Agent SDK | docs/harness/chirality_harness_graphs_and_sequence.md |

## Construction

| Aspect | Detail | Source |
|--------|--------|--------|
| Implementation location | Harness Modules layer (`AttachmentResolver`) | docs/harness/chirality_harness_graphs_and_sequence.md |
| Consumer | `POST /api/harness/turn` API route | docs/harness/chirality_harness_graphs_and_sequence.md (Sequence diagram) |
| Filesystem access | `AttachmentResolver` reads from filesystem to resolve paths | docs/harness/chirality_harness_graphs_and_sequence.md |
| Existing reference | `attachment-resolver.ts` mentioned in PLAN as existing tooling | docs/PLAN.md Section 2 |
| Downstream consumer (UI) | DEL-04-02 (UI Attachment Pipeline) depends on resolver behavior | Decomposition PKG-04 deliverables table |

## References

| Ref | Document | Relevance |
|-----|----------|-----------|
| 1 | docs/SPEC.md Section 9.8 | Authoritative specification for attachment handling and prompt-mode selection |
| 2 | docs/harness/chirality_harness_graphs_and_sequence.md | Module dependency graph and turn sequence diagram |
| 3 | docs/PLAN.md Section 2 | Existing tooling inventory mentioning `attachment-resolver.ts` |
| 4 | docs/CONTRACT.md | Binding invariants (K-GHOST-1, K-INVENT-1) |
| 5 | docs/DIRECTIVE.md | Founding intent and scope constraints |
| 6 | Decomposition (G7-APPROVED) | DEL-04-01 entry, SOW-007/008/009, OBJ-003 |
| 7 | Anthropic Agent SDK documentation | SDK content block format and `query()` API contract — `location TBD` |
