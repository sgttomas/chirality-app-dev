# Chirality App — Software Development Decomposition

**Revision:** G7-APPROVED
**Date:** 2026-02-21 (America/Edmonton)
**Canonical ID formats:** `PKG-XX`, `DEL-XX-YY`, `SOW-NNN`, `OBJ-NNN`

**Recommended location in an execution instance:**
`{EXECUTION_ROOT}/_Decomposition/ChiralityApp_SoftwareDecomposition_2026-02-21.md`

---

## References

Canonical governance and workflow standards used to produce this decomposition:

- `AGENT_HELPS_HUMANS.md` (canonical agent/workflow design standard; precedence anchor).
- `AGENT_SOFTWARE_DECOMP.md` (gate-controlled decomposition procedure and required tables).
- `AGENTS.md` (operator-facing agent framework index and rules).
- `README.md` (product description and conceptual model; **non-canonical for ID formats**).
- `docs/DIRECTIVE.md` (founding intent, constraints, in/out scope, human authority).
- `docs/CONTRACT.md` (binding invariants `K-*` and enforcement map).
- `docs/SPEC.md` (canonical filesystem structures, harness contract, snapshot rules, schemas).
- `docs/TYPES.md` (canonical vocabulary, stable ID formats, lifecycle states).
- `docs/PLAN.md` (implemented surface area + future hardening candidates).

---

## Decision Log

Non-trivial decisions captured during gated decomposition.

| DecisionRef | Decision | Rationale / Notes |
|---|---|---|
| **DEC-PLAT-001** | Target platform = **macOS 15+**, **Apple Silicon only**; packaging target includes **`.dmg`**; **signing/notarization not required**. | Human ruling (Gate 3). |
| **DEC-NET-001** | Outbound internet access is permitted **only** for **Anthropic API** calls. No other outbound network connections (telemetry, update checks, etc.). | Human ruling (Gate 3). Interpreted as a narrow exception to DIRECTIVE “external integrations” boundary while keeping all other integrations OUT. |
| **DEC-PKG-001** | Package partition uses 8 work domains aligned to repo architecture: build/packaging, UI workflow, runtime core, attachments, filesystem model, agent+governance, validation/examples, optional hardening. | Ensures “flat packages” and bounded-context routing per SOFTWARE_DECOMP and CONTRACT invariants.  |

---

## Vocabulary Map

| CanonicalTerm | Synonyms | Notes |
|---|---|---|
| Instruction Root | app bundle instructions; “agent operating system” | Release-managed instructions/docs shipped inside the app bundle. |
| Working Root | `projectRoot`; working directory | User-selected filesystem root where agents read/write state. |
| Execution Root | execution instance; project workspace | `{EXECUTION_ROOT}/` containing packages + tool roots. |
| Tool Roots | `_Aggregation/`, `_Reconciliation/`, `_Estimates/`, `_Change/`, etc. | Derived outputs; snapshots are immutable. |
| Package | work domain; partition | Flat partition of scope (`PKG-XX`). No nesting. |
| Deliverable | working item; unit of production | `DEL-XX-YY` folder under `{PKG}/1_Working/`. |
| Lifecycle State | `_STATUS.md` state | Canonical lifecycle states (`OPEN → … → ISSUED`). |
| Snapshot | immutable snapshot folder | Task agent outputs to tool roots are immutable; reruns create new snapshots. |
| Pointer file | `_LATEST.md` | Mutable pointer to the most recent snapshot. |
| Session | harness session | UI-managed harness session. |
| Turn | harness turn | One user turn with message + optional attachments + opts; supports streaming events. |
| Attachments | multimodal input | UI sends absolute paths; server resolves/reads/classifies and enforces budgets. |
| Sealed Context | “no ghost inputs”; `contextSealed` | Type 2 execution requires sealed, human-approved context. |

Terminology and lifecycle rules are governed by `docs/TYPES.md` and `docs/SPEC.md`.

---

## Structured Scope of Work (SSOW)

Atomic scope items with `IN | OUT | TBD` classification (Gate 2 approved).

> Note: The SSOW is the source of truth for package coverage. Every `SOW-*` item is assigned to exactly one package.

| ScopeItemID | InOutStatus | ScopeItemStatement |
|---|---|---|
| SOW-001 | IN | The Chirality desktop app builds and runs on macOS as the repo’s Electron + Next.js desktop application. |
| SOW-002 | IN | The app can be packaged as a macOS `.dmg` desktop build that launches and functions. |
| SOW-003 | IN | The app lets a user select a local Working Root (`projectRoot`) and run Chirality against that folder (filesystem-as-state). |
| SOW-004 | IN | Implement/maintain session boot and turn execution APIs (`/api/harness/session/*`, `/api/harness/turn`). |
| SOW-005 | IN | Implement/maintain streaming event protocol (SSE) from runtime to UI during turns. |
| SOW-006 | IN | Implement/maintain harness runtime responsibilities: tool calling, permissions, and event streaming. |
| SOW-007 | IN | Support turns with multimodal attachments where UI sends absolute file paths and server resolves/reads/classifies the files. |
| SOW-008 | IN | Enforce attachment resolver validation rules: allowed extensions, reject non-files, per-file size limit, total budget, partial failure handling. |
| SOW-009 | IN | Ensure runtime prompt-mode selection behaves correctly for (a) no attachments and (b) attachments present. |
| SOW-010 | IN | UI attachment behavior: preview + draft preservation + optimistic send + rollback on failure + session rehydration drops malformed records. |
| SOW-011 | IN | Implement/maintain the harness turn `opts` mapping + fallback chains (model/tools/maxTurns, etc.), with UI allowed to expose any subset. |
| SOW-012 | IN | Enforce subagent governance “fail closed” rule: subagent injection only when enabled and governance metadata is present + valid. |
| SOW-013 | IN | Maintain separation of Instruction Root (release-managed, app bundle) vs Working Root (`projectRoot`) where execution files live. |
| SOW-014 | IN | Ensure “filesystem is the state”: agents read/write project truth as plain files; no external DB and no server required for project state. |
| SOW-015 | IN | Ensure execution root layout and tool roots match `docs/SPEC.md`. |
| SOW-016 | IN | Ensure deliverable lifecycle is represented by `_STATUS.md` using canonical states and transition rules. |
| SOW-017 | IN | Support workspace scaffolding and document kit drafting via the agent framework (PREPARATION + 4_DOCUMENTS). |
| SOW-018 | IN | Support deliverable-local dependency tracking: `_DEPENDENCIES.md` + `Dependencies.csv` v3.1 including provenance requirements. |
| SOW-019 | IN | Support optional semantic analysis artifacts: `_SEMANTIC.md` and `_SEMANTIC_LENSING.md`. |
| SOW-020 | IN | Support cross-deliverable operations as opt-in, human-triggered workflows writing outputs under tool roots as immutable snapshots. |
| SOW-021 | IN | Support change management and git hygiene consistent with “git is the event store” intent. |
| SOW-022 | IN | Provide a live project directory FileTree that refreshes periodically and on focus/visibility changes to detect external filesystem changes. |
| SOW-023 | IN | Provide PORTAL → PIPELINE navigation for deliverable-scoped `TASK*` variants. |
| SOW-024 | IN | Maintain shared deliverables state at page-level used by PORTAL and PIPELINE views. |
| SOW-025 | IN | Provide an Operator Toolkit panel for per-turn harness options and local presets; persisted locally (non-authoritative). |
| SOW-026 | IN | Provide resizable multi-pane layout behavior (drag handles, keyboard resize, collapse/expand). |
| SOW-027 | IN | Maintain theme/UX hardening elements described in PLAN. |
| SOW-028 | IN | Provide repeatable harness validation scripts and docs suitable for local + CI validation gates. |
| SOW-029 | IN | Provide example execution-root assets under `examples/` for regression and conformance testing. |
| SOW-030 | IN | Maintain governance documents and their internal alignment on the core model. |
| SOW-031 | IN | Maintain agent instruction suite (`agents/*`) conformance to `AGENT_HELPS_HUMANS.md`. |
| SOW-032 | TBD | Add SHA-256 content hashes for out-of-folder references in `_REFERENCES.md` and enforce verification before pipeline runs. |
| SOW-033 | TBD | Implement a `Dependencies.csv` v3.1 schema linter for CI-level validation. |
| SOW-034 | TBD | Implement automated folder structure validator for execution roots based on SPEC validation checklist. |
| SOW-035 | TBD | Implement on-demand dependency graph generation (aggregate deliverable-local registers to project-level JSON/Mermaid). |
| SOW-036 | TBD | Formalize a deliverable-level lock mechanism for concurrent task execution. |
| SOW-037 | TBD | Formalize unified pipeline run record schema/persistence. |
| SOW-038 | TBD | Implement staleness propagation + triage tooling (dependency edges + git SHAs). |
| SOW-039 | OUT | Automated approval or issuance of deliverables by agents. |
| SOW-040 | OUT | Financial transactions or binding commitments. |
| SOW-041 | OUT | Safety-critical decisions without human review. |
| SOW-042 | OUT | Replacing professional judgment in regulated practice. |
| SOW-043 | OUT | External system integration (databases, APIs, cloud services). *(Exception: Anthropic API only per DEC-NET-001.)* |

---

## Objectives

Objectives are derived from SSOW (Gate 3 approved). IDs follow `OBJ-NNN` per `docs/TYPES.md`.

### OBJ-001 — Working macOS desktop build and install path (macOS 15+, Apple Silicon)
A macOS build of Chirality App that builds, launches, and is distributable as a `.dmg` such that an operator can select a working directory (`projectRoot`) and begin using the harness.

**Acceptance (testable):**
- Builds and runs on **Apple Silicon** Macs running **macOS 15+**
- `.dmg` packaging is available and installable
- Signing/notarization is **not required** (self-builder installs)

### OBJ-002 — Harness runtime correctness (sessions, turns, streaming) + Anthropic-only outbound network policy
The harness runtime supports session boot + turn execution with streaming events, correct option parsing, correct governance behavior, and **Anthropic-only** outbound internet.

**Acceptance (testable):**
- Session/turn endpoints function end-to-end from the desktop UI
- SSE streaming works during turns
- Turn options mapping + fallback chains conform to the harness contract
- Subagent governance is fail-closed
- Outbound network connections are limited to Anthropic API only (no other endpoints)

### OBJ-003 — Attachment-enabled turns are robust and UX-safe
Turns can include multimodal attachments with server-side validation and resilient UI behaviors (rollback/rehydration).

### OBJ-004 — Filesystem-as-state execution model is SPEC-conformant and auditable
Instruction root vs working root separation is maintained; execution roots match SPEC; lifecycle uses `_STATUS.md`; dependency tracking uses v3.1 registers; tool-root outputs are immutable snapshots.

### OBJ-005 — Desktop UI supports intended operator workflow
Portal-to-Pipeline navigation, FileTree refresh, shared deliverables state, toolkit panel, and multi-pane ergonomics work as intended.

### OBJ-006 — Validation posture and governance/agent-suite conformance enable repeatable operation
Validation scripts/docs/examples exist; governance docs stay coherent; `agents/*` instruction suite conforms to HELPS_HUMANS structure.

### OBJ-007 — Optional: integrity hardening loop (TBD scope)
If `SOW-032`…`SOW-038` are brought IN scope, implement integrity hardening features (hashes, linters, validators, graph tooling, locks, run records, staleness tooling).

---

## Packages (work-domain partitions)

Packages are flat work domains (`PKG-XX`) and must not be phases.

| PackageID | Name | ScopeDescription |
|---|---|---|
| PKG-01 | Build & Packaging | Build/run on macOS 15+ Apple Silicon; `.dmg` packaging; local-builder install workflow (no notarization). |
| PKG-02 | Desktop UI Workflow | FileTree refresh, Portal→Pipeline navigation, shared state, toolkit panel, layout + theme ergonomics. |
| PKG-03 | Harness Runtime Core | Session/turn APIs, SSE streaming, tool calling/permissions, opts fallback chains, subagent governance fail-closed, Anthropic-only network policy. |
| PKG-04 | Attachments & Multimodal Turns | Attachment resolver + prompt-mode selection + UI attachment pipeline (preview/rollback/rehydration). |
| PKG-05 | Filesystem Execution Model | Instruction root vs working root separation; filesystem-as-state contract; SPEC layout; lifecycle; dependency register mechanics. |
| PKG-06 | Agent Suite & Governance | Agent instruction conformance; cross-deliverable workflows; change management posture; governance coherence; explicit guardrails (OUT items). |
| PKG-07 | Validation & Example Assets | Validation scripts/docs + example execution roots for regression/conformance checks. |
| PKG-08 | Optional Integrity Hardening (TBD) | Future hardening candidates (hashes, linters, validators, graph, locks, run records, staleness). |

---

## Deliverables

Deliverables are the smallest unit (no internal “task” layer), therefore they are sized for bounded specialist execution and include a required `ContextEnvelope` (`S|M|L|XL`).

### PKG-01 — Build & Packaging

| DeliverableID | Name | Type | ResponsibleParty | Description | AnticipatedArtifacts | CoversScopeItems | SupportsObjectives | ContextEnvelope | ContextEnvelopeNotes |
|---|---|---|---|---|---|---|---|---|---|
| DEL-01-01 | macOS 15+ Apple Silicon Build Baseline | CI_CD_CHANGE | TBD | Make repo build/run reliably on macOS 15+ and Apple Silicon only (dev + prod build). | CODE/CONFIG/SCRIPT/DOC | SOW-001 | OBJ-001 | M |  |
| DEL-01-02 | Unsigned DMG Packaging Workflow | CI_CD_CHANGE | TBD | Produce a working `.dmg` packaging path for local builders (unsigned/unnotarized acceptable). | CONFIG/SCRIPT/DOC | SOW-002 | OBJ-001 | M |  |

### PKG-02 — Desktop UI Workflow

| DeliverableID | Name | Type | ResponsibleParty | Description | AnticipatedArtifacts | CoversScopeItems | SupportsObjectives | ContextEnvelope | ContextEnvelopeNotes |
|---|---|---|---|---|---|---|---|---|---|
| DEL-02-01 | FileTree Refresh & External-Change Detection | UX_UI_SLICE | TBD | Implement/verify FileTree refresh behavior (polling + focus/visibility refresh). | CODE/TEST/DOC | SOW-022 | OBJ-005 | M |  |
| DEL-02-02 | Portal→Pipeline Navigation & Deliverable Key Semantics | UX_UI_SLICE | TBD | Implement/verify deliverable-scoped navigation and shared state semantics. | CODE/TEST | SOW-023, SOW-024 | OBJ-005 | M |  |
| DEL-02-03 | Operator Toolkit Panel & Local Presets (Non-authoritative) | UX_UI_SLICE | TBD | Implement/verify toolkit panel; ensure it is convenience state only and cannot bypass governance. | CODE/DOC/TEST | SOW-025 | OBJ-005 | M |  |
| DEL-02-04 | Multi-pane Layout + Theme Hardening | UX_UI_SLICE | TBD | Implement/verify resizable multi-pane UI and theme hardening described in PLAN. | CODE/TEST | SOW-026, SOW-027 | OBJ-005 | M |  |

### PKG-03 — Harness Runtime Core

| DeliverableID | Name | Type | ResponsibleParty | Description | AnticipatedArtifacts | CoversScopeItems | SupportsObjectives | ContextEnvelope | ContextEnvelopeNotes |
|---|---|---|---|---|---|---|---|---|---|
| DEL-03-01 | Working Root Binding & Session Boot | API_CONTRACT | TBD | Bind a chosen `projectRoot` to a session; session boot accepts `opts` and initializes correctly. | CODE/TEST/DOC | SOW-003, SOW-004 | OBJ-001, OBJ-002 | M |  |
| DEL-03-02 | Turn Execution API + SSE Streaming | BACKEND_FEATURE_SLICE | TBD | Ensure `/api/harness/turn` executes turns end-to-end and streams events via SSE. | CODE/TEST/DOC | SOW-004, SOW-005, SOW-006 | OBJ-002 | M |  |
| DEL-03-03 | Turn Options Mapping & Fallback Chains | BACKEND_FEATURE_SLICE | TBD | Implement/verify runtime `opts` mapping + fallback chains per harness contract. | CODE/TEST/DOC | SOW-011 | OBJ-002 | S |  |
| DEL-03-04 | Subagent Governance Fail-Closed Enforcement | SECURITY_CONTROL | TBD | Enforce delegation governance fail-closed behavior (block injection; parent continues). | CODE/TEST/DOC | SOW-012 | OBJ-002 | S |  |
| DEL-03-05 | Anthropic Provider Integration & Key Provisioning Contract | BACKEND_FEATURE_SLICE | TBD | Implement Anthropic API provider integration; define API key provisioning and storage contract as non-project-truth convenience state. | CODE/TEST/DOC | SOW-006 | OBJ-002 | M |  |
| DEL-03-06 | Outbound Network Guardrails (Anthropic-only) + Verification | SECURITY_CONTROL | TBD | Implement and verify Anthropic-only outbound network policy (no telemetry/update checks/other endpoints). | CODE/TEST/DOC | SOW-006 | OBJ-002, OBJ-006 | L | Touches multiple runtime surfaces (Electron shell + HTTP client + any update/telemetry paths). Keep bounded to “egress policy + proof.” |

### PKG-04 — Attachments & Multimodal Turns

| DeliverableID | Name | Type | ResponsibleParty | Description | AnticipatedArtifacts | CoversScopeItems | SupportsObjectives | ContextEnvelope | ContextEnvelopeNotes |
|---|---|---|---|---|---|---|---|---|---|
| DEL-04-01 | Server-side Attachment Resolver + Prompt Mode Selection | BACKEND_FEATURE_SLICE | TBD | Implement/verify attachment resolver rules + prompt-mode selection per harness contract. | CODE/TEST/DOC | SOW-007, SOW-008, SOW-009 | OBJ-003 | M |  |
| DEL-04-02 | UI Attachment Pipeline (Picker, Preview, Rollback, Rehydration) | UX_UI_SLICE | TBD | Implement/verify UI attachment picker/preview and rollback/rehydration rules. | CODE/TEST | SOW-010 | OBJ-003 | M |  |

### PKG-05 — Filesystem Execution Model

| DeliverableID | Name | Type | ResponsibleParty | Description | AnticipatedArtifacts | CoversScopeItems | SupportsObjectives | ContextEnvelope | ContextEnvelopeNotes |
|---|---|---|---|---|---|---|---|---|---|
| DEL-05-01 | Instruction Root Bundling & Runtime Access | BACKEND_FEATURE_SLICE | TBD | Ensure deployable builds preserve instruction root vs working root separation and in-app access to instructions. | CODE/DOC/TEST | SOW-013 | OBJ-004 | M |  |
| DEL-05-02 | Execution Root Scaffolding + Layout Conformance | BACKEND_FEATURE_SLICE | TBD | Ensure execution-root and tool-root layout matches SPEC; scaffold required folders/files. | CODE/TEST/DOC | SOW-014, SOW-015 | OBJ-004 | M |  |
| DEL-05-03 | Lifecycle State Handling (`_STATUS.md` canonical) | BACKEND_FEATURE_SLICE | TBD | Ensure `_STATUS.md` is the canonical lifecycle file and transitions align to SPEC. | CODE/TEST/DOC | SOW-016 | OBJ-004 | M |  |
| DEL-05-04 | Dependency Tracking File Contract (v3.1) | DATA_MODEL_CHANGE | TBD | Support deliverable-local dependency tracking: `_DEPENDENCIES.md` + `Dependencies.csv v3.1` including provenance fields. | DOC/CODE/TEST | SOW-018 | OBJ-004 | L | May touch multiple surfaces (file generation + validation + ingestion). Split if it expands beyond “contract + minimal integration glue.” |

### PKG-06 — Agent Suite & Governance

| DeliverableID | Name | Type | ResponsibleParty | Description | AnticipatedArtifacts | CoversScopeItems | SupportsObjectives | ContextEnvelope | ContextEnvelopeNotes |
|---|---|---|---|---|---|---|---|---|---|
| DEL-06-01 | Agent Instruction Suite Structural Conformance | DOC_UPDATE | TBD | Bring `AGENT_*.md` instruction files into conformance with HELPS_HUMANS-required structure and headers/write scopes. | DOC | SOW-031 | OBJ-006 | L | Likely touches many instruction files; single domain (docs). Split if it becomes too broad. |
| DEL-06-02 | Local Deliverable Workflow Agents (Scaffold → Doc Kit → Semantic) | DOC_UPDATE | TBD | Ensure PREPARATION + 4_DOCUMENTS + semantic agents support local deliverable lifecycle and required artifacts. | DOC | SOW-017, SOW-019 | OBJ-004, OBJ-006 | M |  |
| DEL-06-03 | Cross-deliverable Workflow Support (Aggregation/Reconciliation/Estimating/Scheduling) | DOC_UPDATE | TBD | Ensure cross-deliverable workflows are opt-in, human-triggered, and write immutable snapshot outputs under correct tool roots. | DOC | SOW-020 | OBJ-004, OBJ-006 | M |  |
| DEL-06-04 | Change Management & Git Hygiene Support | DOC_UPDATE | TBD | Ensure CHANGE/publication guidance matches “git is the event store” and human approval rules. | DOC | SOW-021 | OBJ-004, OBJ-006 | M |  |
| DEL-06-05 | Governance Coherence + Guardrails (OUT boundaries) | DOC_UPDATE | TBD | Maintain governance doc coherence and keep OUT-of-scope boundaries explicit (no auto-approval; no financial commitments; etc.). | DOC | SOW-030, SOW-039, SOW-040, SOW-041, SOW-042, SOW-043 | OBJ-006 | S |  |

### PKG-07 — Validation & Example Assets

| DeliverableID | Name | Type | ResponsibleParty | Description | AnticipatedArtifacts | CoversScopeItems | SupportsObjectives | ContextEnvelope | ContextEnvelopeNotes |
|---|---|---|---|---|---|---|---|---|---|
| DEL-07-01 | Harness Validation Suite (local + CI-ready posture) | TEST_SUITE | TBD | Repeatable validation scripts/docs cover sessions/turns/SSE/opts/subagent gating and attachments contract behaviors. | TEST/SCRIPT/DOC | SOW-028 | OBJ-006 | M |  |
| DEL-07-02 | Example Execution Roots + Conformance Fixtures | TEST_SUITE | TBD | Maintain/update `examples/` execution roots used for regression/conformance testing. | OTHER/DOC/TEST | SOW-029 | OBJ-006 | M |  |

### PKG-08 — Optional Integrity Hardening (TBD scope)

| DeliverableID | Name | Type | ResponsibleParty | Description | AnticipatedArtifacts | CoversScopeItems | SupportsObjectives | ContextEnvelope | ContextEnvelopeNotes |
|---|---|---|---|---|---|---|---|---|---|
| DEL-08-01 | `_REFERENCES.md` Content Hashes + Verification | SECURITY_CONTROL | TBD | Add SHA-256 hashes for out-of-folder references and verify before pipeline runs. | CODE/SCRIPT/DOC | SOW-032 | OBJ-007 | M |  |
| DEL-08-02 | Dependencies.csv v3.1 Schema Linter | TEST_SUITE | TBD | Implement standalone schema linter for v3.1 registers (CI-level validation). | SCRIPT/TEST/DOC | SOW-033 | OBJ-007 | S |  |
| DEL-08-03 | Execution Root Folder Structure Validator | TEST_SUITE | TBD | Implement folder validator per SPEC checklist. | SCRIPT/TEST/DOC | SOW-034 | OBJ-007 | S |  |
| DEL-08-04 | On-demand Dependency Graph Generator | BACKEND_FEATURE_SLICE | TBD | Aggregate deliverable-local registers into a project graph artifact (JSON/Mermaid). | SCRIPT/OTHER/DOC | SOW-035 | OBJ-007 | M |  |
| DEL-08-05 | Deliverable-level Lock Mechanism | SECURITY_CONTROL | TBD | Formalize safe concurrent execution lock protocol and recovery semantics. | CODE/DOC/TEST | SOW-036 | OBJ-007 | L | Medium-high complexity protocol; keep bounded. |
| DEL-08-06 | Unified Pipeline Run Record Persistence | DATA_MODEL_CHANGE | TBD | Define and implement unified run-record schema/persistence for task-agent runs. | DOC/CODE/TEST | SOW-037 | OBJ-007 | L | Cross-pipeline schema choice; keep bounded to one schema + one storage location. |
| DEL-08-07 | Staleness Propagation + Triage Tooling | BACKEND_FEATURE_SLICE | TBD | Implement staleness detection + triage tooling based on dependency edges + baseline SHAs. | CODE/DOC/TEST/OTHER | SOW-038 | OBJ-007 | L | Likely depends on graph + run records; keep outputs deterministic/auditable. |

---

## Scope Ledger

Machine-checkable mapping of every scope item to exactly one package and ≥1 deliverables (best-effort), plus objective linkage.

Columns:
- `ScopeItemID`, `InOutStatus`, `ScopeItemStatement`, `SourceRef`
- `PackageID` (exactly one; hard rule)
- `DeliverableID(s)` (best-effort; OUT items map to governance/guardrail deliverable)
- `ObjectiveID(s)` (best-effort)
- `DecisionRef` (optional)
- `OpenIssue` (`TRUE|FALSE`)
- `Notes`

| ScopeItemID | InOutStatus | ScopeItemStatement | SourceRef | PackageID | DeliverableID(s) | ObjectiveID(s) | DecisionRef | OpenIssue | Notes |
|---|---|---|---|---|---|---|---|---|---|
| SOW-001 | IN | The Chirality desktop app builds and runs on macOS as the repo’s Electron + Next.js desktop application. | PLAN §2 | PKG-01 | DEL-01-01 | OBJ-001 | DEC-PLAT-001 | FALSE | Apple Silicon + macOS 15+. |
| SOW-002 | IN | The app can be packaged as a macOS `.dmg` desktop build that launches and functions. | PLAN §2 | PKG-01 | DEL-01-02 | OBJ-001 | DEC-PLAT-001 | FALSE | Unsigned/unnotarized OK. |
| SOW-003 | IN | The app lets a user select a local Working Root (`projectRoot`) and run Chirality against that folder (filesystem-as-state). | README + DIRECTIVE | PKG-03 | DEL-03-01 | OBJ-001, OBJ-002 |  | FALSE | Root binding treated as runtime behavior. |
| SOW-004 | IN | Implement/maintain session boot and turn execution APIs (`/api/harness/session/*`, `/api/harness/turn`). | PLAN §2 | PKG-03 | DEL-03-01, DEL-03-02 | OBJ-002 |  | FALSE | Boot vs turn/stream slices. |
| SOW-005 | IN | Implement/maintain streaming event protocol (SSE) from runtime to UI during turns. | PLAN §2 | PKG-03 | DEL-03-02 | OBJ-002 |  | FALSE |  |
| SOW-006 | IN | Implement/maintain harness runtime responsibilities: tool calling, permissions, and event streaming. | README + PLAN | PKG-03 | DEL-03-02, DEL-03-05, DEL-03-06 | OBJ-002 | DEC-NET-001 | FALSE | Includes Anthropic integration + egress policy. |
| SOW-007 | IN | Support turns with multimodal attachments where UI sends absolute file paths and server resolves/reads/classifies the files. | PLAN §2 + SPEC | PKG-04 | DEL-04-01 | OBJ-003 |  | FALSE |  |
| SOW-008 | IN | Enforce attachment resolver validation rules. | SPEC harness contract | PKG-04 | DEL-04-01 | OBJ-003 |  | FALSE |  |
| SOW-009 | IN | Ensure runtime prompt-mode selection behaves correctly. | SPEC harness contract | PKG-04 | DEL-04-01 | OBJ-003 |  | FALSE |  |
| SOW-010 | IN | UI attachment behavior (preview/draft/rollback/rehydration). | SPEC + PLAN | PKG-04 | DEL-04-02 | OBJ-003 |  | FALSE |  |
| SOW-011 | IN | Turn `opts` mapping + fallback chains. | SPEC harness contract | PKG-03 | DEL-03-03 | OBJ-002 |  | FALSE |  |
| SOW-012 | IN | Subagent governance “fail closed” rule. | SPEC + CONTRACT | PKG-03 | DEL-03-04 | OBJ-002 |  | FALSE |  |
| SOW-013 | IN | Separate Instruction Root vs Working Root (`projectRoot`). | DIRECTIVE + README | PKG-05 | DEL-05-01 | OBJ-004 |  | FALSE |  |
| SOW-014 | IN | Filesystem is the state; no DB; no server required for project state. | DIRECTIVE | PKG-05 | DEL-05-02 | OBJ-004 |  | FALSE |  |
| SOW-015 | IN | Execution root layout and tool roots match `docs/SPEC.md`. | SPEC §1 | PKG-05 | DEL-05-02 | OBJ-004 |  | FALSE |  |
| SOW-016 | IN | Lifecycle via `_STATUS.md` canonical states. | SPEC §3 + CONTRACT K-STATUS-1 | PKG-05 | DEL-05-03 | OBJ-004 |  | FALSE |  |
| SOW-017 | IN | Workspace scaffolding + document kit drafting via agents (PREPARATION + 4_DOCUMENTS). | DIRECTIVE + SPEC + AGENTS | PKG-06 | DEL-06-02 | OBJ-004, OBJ-006 |  | FALSE | Agent enablement slice. |
| SOW-018 | IN | Deliverable-local dependency tracking (`_DEPENDENCIES.md` + `Dependencies.csv` v3.1) incl. provenance. | SPEC + CONTRACT | PKG-05 | DEL-05-04 | OBJ-004 |  | FALSE |  |
| SOW-019 | IN | Optional semantic artifacts (`_SEMANTIC.md`, `_SEMANTIC_LENSING.md`). | SPEC + AGENTS | PKG-06 | DEL-06-02 | OBJ-004, OBJ-006 |  | FALSE |  |
| SOW-020 | IN | Cross-deliverable workflows output to tool roots as immutable snapshots. | AGENTS + SPEC snapshots | PKG-06 | DEL-06-03 | OBJ-004, OBJ-006 |  | FALSE |  |
| SOW-021 | IN | Change management and git hygiene support. | DIRECTIVE + CONTRACT | PKG-06 | DEL-06-04 | OBJ-004, OBJ-006 |  | FALSE |  |
| SOW-022 | IN | Live project directory FileTree refresh behavior. | PLAN §2 | PKG-02 | DEL-02-01 | OBJ-005 |  | FALSE |  |
| SOW-023 | IN | Portal → Pipeline navigation for deliverable-scoped `TASK*` variants. | PLAN §2 | PKG-02 | DEL-02-02 | OBJ-005 |  | FALSE |  |
| SOW-024 | IN | Shared deliverables state across PORTAL and PIPELINE. | PLAN §2 | PKG-02 | DEL-02-02 | OBJ-005 |  | FALSE |  |
| SOW-025 | IN | Operator Toolkit panel for per-turn opts + local presets (non-authoritative). | PLAN §2 + DIRECTIVE | PKG-02 | DEL-02-03 | OBJ-005 |  | FALSE |  |
| SOW-026 | IN | Resizable multi-pane layout behavior. | PLAN §2 | PKG-02 | DEL-02-04 | OBJ-005 |  | FALSE |  |
| SOW-027 | IN | Theme/UX hardening elements described in PLAN. | PLAN §2 | PKG-02 | DEL-02-04 | OBJ-005 |  | FALSE |  |
| SOW-028 | IN | Harness validation scripts/docs for local + CI-ready posture. | PLAN §2 | PKG-07 | DEL-07-01 | OBJ-006 |  | FALSE |  |
| SOW-029 | IN | Example execution-root assets under `examples/`. | PLAN §2 | PKG-07 | DEL-07-02 | OBJ-006 |  | FALSE |  |
| SOW-030 | IN | Governance documents aligned on core model. | PLAN §1 + CONTRACT | PKG-06 | DEL-06-05 | OBJ-006 |  | FALSE |  |
| SOW-031 | IN | Agent instruction suite conforms to HELPS_HUMANS. | AGENTS + SPEC §9 | PKG-06 | DEL-06-01 | OBJ-006 |  | FALSE |  |
| SOW-032 | TBD | SHA-256 content hashes for out-of-folder references + verification gates. | PLAN §3.1 | PKG-08 | DEL-08-01 | OBJ-007 |  | TRUE | Optional hardening. |
| SOW-033 | TBD | Dependencies.csv v3.1 schema linter (CI-level validation). | PLAN §3.2 | PKG-08 | DEL-08-02 | OBJ-007 |  | TRUE | Optional hardening. |
| SOW-034 | TBD | Folder structure validator per SPEC checklist. | PLAN §3.3 + SPEC §12 | PKG-08 | DEL-08-03 | OBJ-007 |  | TRUE | Optional hardening. |
| SOW-035 | TBD | On-demand dependency graph generation. | PLAN §3.4 | PKG-08 | DEL-08-04 | OBJ-007 |  | TRUE | Optional hardening. |
| SOW-036 | TBD | Deliverable-level lock mechanism formalization. | PLAN §3.5 | PKG-08 | DEL-08-05 | OBJ-007 |  | TRUE | Optional hardening. |
| SOW-037 | TBD | Unified pipeline run record schema/persistence. | PLAN §3.6 | PKG-08 | DEL-08-06 | OBJ-007 |  | TRUE | Optional hardening. |
| SOW-038 | TBD | Staleness propagation + triage tooling (dependency edges + SHAs). | PLAN §3.7 + CONTRACT K-STALE/K-VAL | PKG-08 | DEL-08-07 | OBJ-007 |  | TRUE | Optional hardening; depends on prior optional items. |
| SOW-039 | OUT | Automated approval/issuance by agents. | DIRECTIVE + CONTRACT | PKG-06 | DEL-06-05 |  |  | FALSE | Guardrail. |
| SOW-040 | OUT | Financial transactions or binding commitments. | DIRECTIVE | PKG-06 | DEL-06-05 |  |  | FALSE | Guardrail. |
| SOW-041 | OUT | Safety-critical decisions without human review. | DIRECTIVE | PKG-06 | DEL-06-05 |  |  | FALSE | Guardrail. |
| SOW-042 | OUT | Replacing professional judgment in regulated practice. | DIRECTIVE | PKG-06 | DEL-06-05 |  |  | FALSE | Guardrail. |
| SOW-043 | OUT | External system integration (databases, APIs, cloud services). | DIRECTIVE | PKG-06 | DEL-06-05 |  | DEC-NET-001 | FALSE | Exception: Anthropic API only. |

---

## Coverage & Telemetry

Coverage metrics required by `AGENT_SOFTWARE_DECOMP.md`.

- **Revision:** G7-APPROVED
- **ScopeItemCount:** 43
  - IN: 31
  - OUT: 5
  - TBD: 7
- **PackageCount:** 8
- **DeliverableCount:** 32
- **ObjectiveCount:** 7
- **UnassignedScopeItems:** 0
- **ScopeItemsWithoutDeliverableMapping:** 0
- **UnmappedObjectives:** 0
- **ContextEnvelopeCounts:**
  - S: 5
  - M: 21
  - L: 6
  - XL: 0
- **OpenIssuesByType:**
  - `POLICY_DECISION` (2): OI-001, OI-002
  - `SCOPE_TBD` (7): OI-032, OI-033, OI-034, OI-035, OI-036, OI-037, OI-038

---

## Context Budget QA

All deliverables include a ContextEnvelope; **no XL deliverables** exist (no mandatory splits required).

### L-sized watchlist (may split later if scope expands)
- DEL-03-06 — Outbound Network Guardrails (Anthropic-only) + Verification
- DEL-05-04 — Dependency Tracking File Contract (v3.1)
- DEL-06-01 — Agent Instruction Suite Structural Conformance
- DEL-08-05 — Deliverable-level Lock Mechanism (TBD scope)
- DEL-08-06 — Unified Pipeline Run Record Persistence (TBD scope)
- DEL-08-07 — Staleness Propagation + Triage Tooling (TBD scope)

---

## Open Issues

Open issues are unresolved items requiring human decisions or explicit scope flips (IN/OUT/TBD).

| OpenIssueID | Type | Description | Related Stable IDs | Resolution Path |
|---|---|---|---|---|
| OI-001 | POLICY_DECISION | Define the Anthropic API key provisioning + storage contract (how key is provided; where stored; how it remains non-project-truth). | DEL-03-05; SOW-006; OBJ-002 | Human selects policy → implement in DEL-03-05; document + test. |
| OI-002 | POLICY_DECISION | Define enforcement + verification method for “Anthropic-only outbound network.” | DEL-03-06; SOW-006; OBJ-002; OBJ-006 | Human selects proof standard → implement allowlist/guard + tests + procedure in DEL-03-06. |
| OI-032 | SCOPE_TBD | Decide whether to include `_REFERENCES.md` content hashes + verification gates. | SOW-032; PKG-08; DEL-08-01; OBJ-007 | Flip IN/OUT/TBD. If OUT, retire deliverable. |
| OI-033 | SCOPE_TBD | Decide whether to include Dependencies.csv v3.1 schema linter. | SOW-033; PKG-08; DEL-08-02; OBJ-007 | Flip IN/OUT/TBD. |
| OI-034 | SCOPE_TBD | Decide whether to include execution-root folder structure validator. | SOW-034; PKG-08; DEL-08-03; OBJ-007 | Flip IN/OUT/TBD. |
| OI-035 | SCOPE_TBD | Decide whether to include on-demand dependency graph generation. | SOW-035; PKG-08; DEL-08-04; OBJ-007 | Flip IN/OUT/TBD. |
| OI-036 | SCOPE_TBD | Decide whether to include deliverable-level lock mechanism. | SOW-036; PKG-08; DEL-08-05; OBJ-007 | Flip IN/OUT/TBD. |
| OI-037 | SCOPE_TBD | Decide whether to include unified run record schema/persistence. | SOW-037; PKG-08; DEL-08-06; OBJ-007 | Flip IN/OUT/TBD. |
| OI-038 | SCOPE_TBD | Decide whether to include staleness propagation + triage tooling. | SOW-038; PKG-08; DEL-08-07; OBJ-007 | Flip IN/OUT/TBD (likely depends on OI-035 + OI-037). |

---

## Change Log

- **G7-DRAFT (2026-02-21):** Consolidated Gate 1–6 approved content into a single coherent decomposition artifact; submitted for Gate 7.
- **G7-APPROVED (2026-02-21):** Gate 7 approved; metadata updated; no semantic changes from G7-DRAFT.

---

## Gate 7 — Approved

Gate 7 has been approved. This decomposition is now the accepted basis for downstream work.

**Change control:** If updates are required, produce a revised decomposition document that preserves stable IDs (`PKG-*`, `DEL-*`, `SOW-*`, `OBJ-*`) unless the human explicitly authorizes renumbering.
