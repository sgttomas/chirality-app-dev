# Datasheet — DEL-02-02 Portal->Pipeline Navigation & Deliverable Key Semantics

## Identification

| Field | Value |
|-------|-------|
| **DeliverableID** | DEL-02-02 |
| **Name** | Portal->Pipeline Navigation & Deliverable Key Semantics |
| **PackageID** | PKG-02 |
| **Package** | Desktop UI Workflow |
| **Type** | UX_UI_SLICE |
| **ContextEnvelope** | M |
| **ResponsibleParty** | TBD |
| **Scope Items** | SOW-023, SOW-024 |
| **Objectives** | OBJ-005 |
| **Anticipated Artifacts** | CODE/TEST |

## Attributes

| Attribute | Value | Source |
|-----------|-------|--------|
| UI Framework | Next.js + Electron desktop app | `docs/PLAN.md` Section 2 |
| Navigation Pattern | PORTAL matrix row click routes to PIPELINE with deliverable pre-selected | `docs/PLAN.md` Section 2, `docs/SPEC.md` Section 14.1 |
| Deliverable Key Format | `pkg::id` composite keys (e.g., `PKG-02_Desktop_UI_Workflow::DEL-02-02`) | `docs/PLAN.md` Section 2 |
| Deliverable Key — `pkg` Segment | The `pkg` segment uses the package folder label (e.g., `PKG-02_Desktop_UI_Workflow`), not the bare PackageID (e.g., `PKG-02`). **TBD: Confirm canonical definition in `docs/PLAN.md` Section 2 — the governance docs use both `PKG-01_PackageLabel::DEL-01-01` and `PKG-02_Desktop_UI_Workflow::DEL-02-02` as examples, suggesting the folder label form, but an explicit rule has not been located.** | `docs/PLAN.md` Section 2; `docs/SPEC.md` Section 15.1 — **location TBD** for definitive key construction rule |
| PORTAL Matrix Routing | OPERATIVE row -> PIPELINE destination | `docs/SPEC.md` Section 14.1 |
| TASK* Pipeline Category | Deliverables-only mode (no fallback static variants) | `docs/PLAN.md` Section 2 |
| Selector Model | Split selectors: Task Agent (static), Scope selectors (dynamic) | `docs/PLAN.md` Section 2 |
| Dynamic Scope Sources | Deliverables scanned from selected working root; knowledge types scanned from canonical deliverable file types | `docs/PLAN.md` Section 2 |
| Shared State Scope | Page-level (`page.tsx`) shared between PORTAL and PIPELINE views | `docs/PLAN.md` Section 2 |
| Stale Selection Behavior | Stale deliverable variant keys cleared on root change, deliverable fetch failure, scan miss, absent knowledge marker, or unresolvable knowledge type | `docs/PLAN.md` Section 2, `docs/SPEC.md` Section 14.5 |
| Loading/Empty States | TASK* selector shows explicit loading and empty states | `docs/PLAN.md` Section 2 |
| Navigation Transition Timing | TBD — no latency or responsiveness threshold specified in governance docs | `docs/SPEC.md` Section 14.1 — **location TBD** for timing requirements |
| Concurrent Navigation Behavior | TBD — behavior when operator clicks multiple deliverable rows in rapid succession is not specified | `docs/SPEC.md` Section 14 — **location TBD** for race condition handling |

## Conditions

| Condition | Value | Source |
|-----------|-------|--------|
| Platform | macOS 15+, Apple Silicon | Decomposition DEC-PLAT-001 |
| Runtime Environment | Electron + Next.js desktop build | `docs/PLAN.md` Section 2 |
| State Storage Model | Filesystem-as-state; no external DB | `docs/DIRECTIVE.md` Section 2.1 |
| Deliverable Data Source | `/api/project/deliverables` endpoint | `docs/SPEC.md` Section 15 |
| Knowledge Decomposition Gate | Knowledge-type scope shown only when knowledge decomposition marker found in `_Decomposition` | `docs/PLAN.md` Section 2 |
| API Endpoint Availability | TBD — ownership of `/api/project/deliverables` endpoint implementation not confirmed in `_DEPENDENCIES.md`; may depend on another deliverable | `docs/SPEC.md` Section 15; `_DEPENDENCIES.md` — **ASSUMPTION** |

## Construction

| Aspect | Detail | Source |
|--------|--------|--------|
| PORTAL View | 3x4 matrix routing operator intent; OPERATIVE row routes to PIPELINE | `docs/PLAN.md` Section 2, `docs/SPEC.md` Section 14.1 |
| PIPELINE View | Category-driven selectors: `DECOMP*`, `PREP*`, `TASK*`, `AUDIT*` | `docs/SPEC.md` Section 14.3 |
| TASK* Selector | Split controls: Task Agent, Scope Mode, Scope, Target Deliverable | `docs/SPEC.md` Section 14.3 |
| Scope Modes | `DELIVERABLES` and `KNOWLEDGE_TYPES` | `docs/SPEC.md` Section 14.3 |
| Disabled Option Rendering | Unsupported variants visible but disabled, labeled "coming soon" | `docs/SPEC.md` Section 14.4 |
| Deliverables API Response | Returns `deliverables[]`, `knowledgeDecomposition`, `knowledgeTypes[]` | `docs/SPEC.md` Section 15.1 |
| Stale Reset Triggers | Root change, deliverable scan miss, absent knowledge marker, unresolvable knowledge type | `docs/SPEC.md` Section 14.5 |
| UI Vocabulary Conformance | UI terms (MatrixRow, MatrixColumn, PipelineCategory, TaskScopeMode) MUST conform to `docs/TYPES.md` Section 9 canonical definitions | `docs/TYPES.md` Section 9 |

## References

| Ref | Document | Relevance |
|-----|----------|-----------|
| R1 | `docs/PLAN.md` Section 2 | Existing portal-to-pipeline navigation behavior description |
| R2 | `docs/SPEC.md` Section 14 | UI Navigation and Selector Contract (normative) |
| R3 | `docs/SPEC.md` Section 15 | `/api/project/deliverables` response contract |
| R4 | `docs/TYPES.md` Section 9 | UI Navigation Vocabulary (MatrixRow, MatrixColumn, PipelineCategory, TaskScopeMode) |
| R5 | `docs/DIRECTIVE.md` Section 2.1 | Filesystem-as-state constraint |
| R6 | Decomposition (G7-APPROVED) | DEL-02-02 entry, SOW-023, SOW-024, OBJ-005 |
