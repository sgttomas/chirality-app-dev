# Datasheet — DEL-04-02 UI Attachment Pipeline (Picker, Preview, Rollback, Rehydration)

## Identification

| Field | Value |
|-------|-------|
| **DeliverableID** | DEL-04-02 |
| **Name** | UI Attachment Pipeline (Picker, Preview, Rollback, Rehydration) |
| **PackageID** | PKG-04 |
| **Package** | Attachments & Multimodal Turns |
| **Type** | UX_UI_SLICE |
| **ContextEnvelope** | M |
| **ResponsibleParty** | TBD |
| **Scope Items** | SOW-010 |
| **Objectives** | OBJ-003 — "Attachment-enabled turns are robust and UX-safe" (directly mapped in Decomposition PKG-04 table: DEL-04-02 row lists OBJ-003 in SupportsObjectives column) |
| **Anticipated Artifacts** | CODE/TEST |

## Attributes

| Attribute | Value | Source |
|-----------|-------|--------|
| Platform | macOS 15+, Apple Silicon (Electron + Next.js desktop app) | Decomposition DEC-PLAT-001 |
| UI framework | Next.js (React) within Electron shell | PLAN Section 2 |
| Attachment data model | `Attachment[]` — path, display name, client-classified mime/type | SPEC.md Section 9.8 |
| Client metadata authority | Non-authoritative; server reclassifies | SPEC.md Section 9.8 |
| File picker component | `FilePicker.tsx` — self-contained modal with multi-select, extension filtering, directory navigation | PLAN Section 2 |
| Attachment pipeline host | ChatPanel attachment pipeline | PLAN Section 2 |
| Supported extensions (server-enforced) | `.png`, `.jpg`, `.jpeg`, `.gif`, `.webp`, `.pdf`, `.txt`, `.md`, `.csv` | SPEC.md Section 9.8 |
| Per-file size limit (server-enforced) | 10 MB | SPEC.md Section 9.8 |
| Total per-turn raw-byte budget (server-enforced) | 18 MB raw (~24 MB base64) | SPEC.md Section 9.8 |
| UI-side size limit enforcement | TBD — whether the UI should display or enforce per-file (10 MB) and per-turn (18 MB) size limits as pre-send validation, or rely entirely on server-side rejection | **TBD** (lensing item B-001; source: SPEC.md Section 9.8 documents limits as "server-enforced" but does not clarify UI-side pre-validation behavior) |
| Maximum file count per turn | TBD — no maximum file count per turn is documented; if a server-side limit exists, the UI may need to enforce or communicate it | **TBD** (lensing item B-002; source: SPEC.md Section 9.8 — specifies byte limits but not count limits) |

## Conditions

| Condition | Description | Source |
|-----------|-------------|--------|
| Send with text | Turn MAY omit text when attachments are present (`message.trim() === ""` with non-empty `attachments`) | SPEC.md Section 9.8 |
| Send failure | UI rolls back optimistic user message and streaming placeholder; preserves draft text and attachment selections for retry | SPEC.md Section 9.8 |
| Rehydration | Session rehydration validates attachment shape; malformed records silently dropped; valid records restored | SPEC.md Section 9.8 |
| Partial attachment failure | Server-side (non-fatal when turn still has executable content); UI receives and displays result/warnings | SPEC.md Section 9.8 |

## Construction

| Aspect | Detail |
|--------|--------|
| Key source files (existing) | `FilePicker.tsx`, ChatPanel attachment pipeline code | PLAN Section 2 |
| Attachment resolver (server-side, not this deliverable) | `attachment-resolver.ts` — classification, budget enforcement, partial failure handling | PLAN Section 2 (server-side is DEL-04-01 scope) |
| State management | UI-local attachment array; preview-only client metadata | SPEC.md Section 9.8 |
| Optimistic UI pattern | User message rendered optimistically on send; rolled back on failure | SPEC.md Section 9.8 |
| Persistence | Session rehydration from stored session state; attachment records validated on restore | SPEC.md Section 9.8 |

## References

| Ref | Location | Relevance |
|-----|----------|-----------|
| SPEC.md Section 9.8 | `docs/SPEC.md` | Harness turn input contract including UI attachment state rules |
| PLAN Section 2 | `docs/PLAN.md` | Existing tooling description including frontend attachment components |
| Decomposition | `execution/_Decomposition/ChiralityApp_SoftwareDecomposition_2026-02-21_G7-APPROVED.md` | DEL-04-02 entry, SOW-010, OBJ-003 |
| CONTRACT.md | `docs/CONTRACT.md` | Invariants K-INVENT-1 (no guessing), K-GHOST-1 (no ghost inputs) |
| DIRECTIVE.md | `docs/DIRECTIVE.md` | Non-authoritative convenience state rules (Section 2.5) |
