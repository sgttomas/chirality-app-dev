# Datasheet — DEL-02-03

## Identification

| Field | Value |
|-------|-------|
| **Deliverable ID** | DEL-02-03 |
| **Name** | Operator Toolkit Panel & Local Presets (Non-authoritative) |
| **Package** | PKG-02 — Desktop UI Workflow |
| **Type** | UX_UI_SLICE |
| **Context Envelope** | M |
| **Responsible Party** | TBD |
| **Scope Coverage** | SOW-025 |
| **Objective Support** | OBJ-005 — **ASSUMPTION (best-effort mapping)**: associated via PKG-02 package grouping in the decomposition objective-to-deliverable mapping |
| **Anticipated Artifacts** | CODE / DOC / TEST |
| **Lifecycle State** | See `_STATUS.md` |

## Attributes

| Attribute | Value | Source |
|-----------|-------|--------|
| UI Component Type | Sidebar panel | PLAN Section 2 ("Operator Toolkit panel") |
| Visibility Control | CONFIG toggle ("Show Tool Kit sidebar") | PLAN Section 2 |
| Persistence Mechanism | Local storage (browser/Electron) | PLAN Section 2 ("persisted in local storage") |
| Authoritative Status | **Non-authoritative** — convenience state only; MUST NOT be treated as project truth and MUST NOT override contract/governance enforcement | DIRECTIVE Section 2.5; SOW-025 |
| Target Platform | macOS 15+, Apple Silicon (Electron + Next.js desktop) | DEC-PLAT-001 (Decomposition Decision Log) |

> **Terminology note:** "Non-authoritative" is the canonical term for this boundary. See Guidance P1 for the full definition. All documents in this deliverable use this term consistently to mean: convenience state that is ephemeral, device-specific, non-versioned, and has no governance authority. (Enrichment: E-001)

### Exposed Options (Harness `opts` Subset)

The toolkit panel MAY expose any subset of the following harness turn options. Omitted fields follow runtime fallback chains. (Source: SPEC Section 9.8)

| Option | Fallback Chain | Data Type / Validation | Source |
|--------|---------------|----------------------|--------|
| `opts.model` | opts.model -> global model (instruction root) -> runtime default | TBD (string — expected model identifier) | SPEC Section 9.8 |
| `opts.tools` | opts.tools -> persona `tools` frontmatter -> runtime preset | TBD (expected array or object — tool configuration) | SPEC Section 9.8 |
| `opts.maxTurns` | opts.maxTurns -> persona `max_turns` frontmatter -> runtime default | TBD (expected positive integer) | SPEC Section 9.8 |
| `opts.subagentGovernance` | Runtime gate/seal logic authoritative; UI fields are informational | TBD (expected object with boolean fields) | SPEC Section 9.8 |

> **Enrichment (B-002):** Data types and validation rules for each opts field are marked TBD. These must be resolved during implementation to ensure proper input validation in the toolkit panel UI controls. Source context: SPEC Section 9.8 defines the opts contract but does not specify UI-side validation constraints.

**Note:** The specific subset of `opts` fields exposed in the toolkit panel is TBD (design decision for implementation).

### Local Presets

| Attribute | Value | Source |
|-----------|-------|--------|
| Preset Scope | Per-turn harness options | SOW-025; PLAN Section 2 |
| Preset Storage | Local storage (non-project-truth) | DIRECTIVE Section 2.5 |
| Preset Format | TBD | — |
| Preset CRUD Operations | TBD (create, select, update, delete) | — |
| Maximum Preset Count | TBD (determine whether to limit or allow unbounded — affects storage design and UX) | — |

> **Enrichment (A-002):** Preset Format and Preset CRUD Operations remain TBD as design decisions that block implementation. These must be resolved before Phase 2 of Procedure can begin. (B-001): Maximum preset count is also TBD — determine whether an upper bound is needed for storage management and UX.

## Conditions

| Condition | Constraint | Source |
|-----------|-----------|--------|
| Governance Bypass | Toolkit panel MUST NOT bypass governance enforcement | SOW-025 ("cannot bypass governance"); DIRECTIVE Section 2.5 |
| Non-authoritative State | Presets and panel state MUST NOT be treated as project truth | DIRECTIVE Section 2.5 |
| Non-authoritative State | Presets and panel state MUST NOT override contract/governance enforcement | DIRECTIVE Section 2.5 |
| Runtime Authorization | UI visibility of a field MUST NOT be interpreted as runtime authorization | SPEC Section 9.8 ("UI contract rules") |
| Fallback Chain Compliance | Omitted fields MUST follow runtime fallback chains | SPEC Section 9.8 |
| No Ghost Inputs | Toolkit state is non-authoritative; agent context limited to folder contents + declared references (K-GHOST-1) | CONTRACT K-GHOST-1 |
| No Invented Values | Unknown values become TBD, not guessed (K-INVENT-1) | CONTRACT K-INVENT-1 |

## Construction

| Aspect | Detail | Source |
|--------|--------|--------|
| Framework | Next.js + Electron desktop app | PLAN Section 2 |
| UI Surface | Sidebar panel within the desktop frontend | PLAN Section 2 |
| State Management | Local storage; non-authoritative convenience state | DIRECTIVE Section 2.5; PLAN Section 2 |
| Harness Turn API | `POST /api/harness/turn` via `opts` object | SPEC Section 9.8 |
| Session Boot API | `POST /api/harness/session/boot` via `opts` object | SPEC Section 9.8 |

> **Terminology note (F-003):** API endpoints are referenced canonically as `POST /api/harness/turn` and `POST /api/harness/session/boot`. See Guidance glossary for the normalized reference forms used across this deliverable's documents.

## References

| Ref | Document | Relevance |
|-----|----------|-----------|
| 1 | `docs/PLAN.md` Section 2 | Describes toolkit panel feature, visibility, persistence |
| 2 | `docs/DIRECTIVE.md` Section 2.5 | Non-authoritative convenience state policy |
| 3 | `docs/SPEC.md` Section 9.8 | Harness turn input contract, opts mapping, fallback chains, UI contract rules |
| 4 | `docs/CONTRACT.md` K-GHOST-1, K-INVENT-1 | Governance constraints that the panel must not circumvent |
| 5 | `docs/CONTRACT.md` K-AUTH-1 | Only humans author binding approval records |
| 6 | Decomposition (G7-APPROVED) — DEL-02-03 entry | Deliverable definition, SOW-025 mapping |
| 7 | Decomposition (G7-APPROVED) — SOW-025 | Scope item: "Provide an Operator Toolkit panel for per-turn opts + local presets (non-authoritative)" |
