# Datasheet — DEL-05-01 Instruction Root Bundling & Runtime Access

## Identification

| Field | Value |
|-------|-------|
| **Deliverable ID** | DEL-05-01 |
| **Name** | Instruction Root Bundling & Runtime Access |
| **Package** | PKG-05 — Filesystem Execution Model |
| **Type** | BACKEND_FEATURE_SLICE |
| **Context Envelope** | M |
| **Responsible Party** | TBD — requires human assignment |
| **Scope Coverage** | SOW-013 |
| **Supports Objectives** | OBJ-004 |
| **Anticipated Artifacts** | CODE / DOC / TEST |
| **Lifecycle State** | SEMANTIC_READY |

> **Enrichment note (A-001):** Lifecycle State updated from "INITIALIZED" to "SEMANTIC_READY" to align with `_STATUS.md` current state. `_STATUS.md` is the authority for lifecycle transitions.

> **Enrichment note (E-001):** Responsible Party marked as requiring human assignment rather than bare "TBD", to clarify that this is a human-decision dependency, not a missing-data placeholder.

---

## Attributes

| Attribute | Value | Source |
|-----------|-------|--------|
| **Target Platform** | macOS 15+, Apple Silicon | Decomposition DEC-PLAT-001 |
| **Packaging Format** | Electron + Next.js desktop app; `.dmg` distribution | Decomposition DEC-PLAT-001; PLAN Section 2 |
| **Instruction Root Contents** | `AGENTS.md`, `README.md`, `agents/*` (agent instruction files), `docs/DIRECTIVE.md`, `docs/CONTRACT.md`, `docs/SPEC.md`, `docs/TYPES.md`, `docs/PLAN.md` | DIRECTIVE Section 2.6; Specification REQ-01 |
| **Working Root Binding** | User-selected `projectRoot` path | DIRECTIVE Section 2.6; Decomposition Vocabulary Map |
| **Separation Model** | Instruction root is release-managed (app bundle); working root is user-controlled filesystem | DIRECTIVE Section 2.6 |
| **Network Policy** | Outbound Anthropic API only (DEC-NET-001) | Decomposition DEC-NET-001 |
| **Signing/Notarization** | Not required | Decomposition DEC-PLAT-001 |

> **Enrichment note (B-001):** "Instruction Root Contents" now explicitly enumerates individual `docs/*` files (DIRECTIVE, CONTRACT, SPEC, TYPES, PLAN) rather than the generic "framework docs (docs/*)" to match the canonical list in Specification REQ-01 and align with the Decomposition Vocabulary Map definition.

---

## Conditions

| Condition | Detail | Source |
|-----------|--------|--------|
| **Instruction Root Immutability** | Instruction root content is release-managed and must not be modified by agents at runtime | DIRECTIVE Section 2.6 |
| **Working Root Writability** | Agents read/write project state as plain files in the working root | DIRECTIVE Section 2.2; SOW-014 |
| **No External DB** | No database or server required for project state | DIRECTIVE Section 5 (Structural Constraints) |
| **Ghost-Input Prevention** | Type 2 agent context is limited to folder contents + declared references (K-GHOST-1) | CONTRACT K-GHOST-1 |
| **Build Preservation** | Deployable builds must preserve instruction root vs working root separation | Decomposition DEL-05-01 description |

---

## Construction

| Aspect | Detail | Source |
|--------|--------|--------|
| **Runtime Framework** | Electron + Next.js | PLAN Section 2 |
| **Instruction Root Location (Dev)** | Repository root — `AGENTS.md`, `README.md`, `agents/*`, `docs/*` | **ASSUMPTION** — inferred from DIRECTIVE Section 2.6 and repository structure |
| **Instruction Root Location (Packaged)** | Bundled within app resources (Electron `process.resourcesPath` or equivalent resource path) | **ASSUMPTION** — standard Electron bundling pattern; exact mechanism TBD |
| **Expected Bundled Directory Structure** | Instruction root content placed under a predictable subdirectory within the app bundle (e.g., `Resources/instructions/`) preserving the source directory structure (`agents/`, `docs/`, plus root-level files) | **ASSUMPTION** — inferred from Electron `extraResources` convention (see Guidance C1); exact path TBD pending build configuration audit |
| **Working Root Selection** | User selects `projectRoot` via UI; session boot binds it | SPEC Section 9.8; Decomposition SOW-003 |
| **Access Pattern** | In-app read access to instruction root; read/write access to working root | DIRECTIVE Section 2.6 |

> **Enrichment note (B-002):** Added "Expected Bundled Directory Structure" row to make explicit the expected target layout for bundled instruction content within the app package, rather than leaving it entirely implicit.

---

## References

| Ref | Document | Relevance |
|-----|----------|-----------|
| 1 | `docs/DIRECTIVE.md` Section 2.6 | Separation of Instruction and Execution — founding design principle |
| 2 | `docs/SPEC.md` Section 1 | Execution Root Layout specification |
| 3 | `docs/CONTRACT.md` K-GHOST-1 | No ghost inputs — sealed context constraint |
| 4 | `docs/PLAN.md` Section 2 | Desktop frontend technology stack and packaging description |
| 5 | Decomposition (G7-APPROVED) — DEL-05-01 entry | Deliverable description and scope mapping |
| 6 | Decomposition — Vocabulary Map | Canonical terms: Instruction Root, Working Root |
| 7 | Decomposition — DEC-PLAT-001, DEC-NET-001 | Platform and network policy decisions |
