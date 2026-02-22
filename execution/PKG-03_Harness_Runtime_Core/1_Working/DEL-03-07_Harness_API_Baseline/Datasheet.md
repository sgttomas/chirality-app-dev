# Datasheet — DEL-03-07 Harness API Baseline in Frontend Runtime

## Identification

| Field | Value |
|-------|-------|
| **Deliverable ID** | DEL-03-07 |
| **Name** | Harness API Baseline in Frontend Runtime |
| **Package** | PKG-03 Harness Runtime Core |
| **Type** | BACKEND_FEATURE_SLICE |
| **Context Envelope** | L |
| **Responsible Party** | TBD |
| **Scope Coverage** | SOW-045 |
| **Objectives** | OBJ-002, OBJ-008 |
| **Anticipated Artifacts** | CODE, TEST |
| **Decomposition Ref** | `execution/_Decomposition/ChiralityApp_SoftwareDecomposition_2026-02-21_G7-APPROVED.md` (Scope Amendment A1, SCA-001) |
| **Amendment** | SCA-001 (2026-02-22) |

---

## Attributes

### API Route Surface

| Attribute | Value | Source |
|-----------|-------|--------|
| Route namespace | `/api/harness/session/*` and `/api/harness/turn` | SOW-045; Decomposition SCA-001 DEL-03-07 entry |
| Runtime framework | Next.js API routes | Decomposition Vocabulary Map ("Chirality GUI (Next.js)"); `docs/harness/chirality_harness_graphs_and_sequence.md` module graph |
| Implementation location | `frontend/` workspace (local, in-repo) | SOW-045; Decomposition SCA-001 execution gating rule; `docs/PLAN.md` Section 2 (FE-2) |
| Failure contract type | Typed failure contracts (error types + status codes) | SOW-045; Decomposition SCA-001 DEL-03-07 entry |

### Session Endpoints

| Endpoint | Method | Purpose | Source |
|----------|--------|---------|--------|
| `/api/harness/session/create` | POST | Create a new harness session | `docs/harness/chirality_harness_graphs_and_sequence.md` module graph |
| `/api/harness/session/boot` | POST | Boot a session (accepts `opts`) | `docs/SPEC.md` Section 9.8; module graph |
| `/api/harness/session/list` | GET | List existing sessions | Module graph; `docs/harness/harness_manual_validation.md` (used in readiness polling) |
| `/api/harness/session/:id` | GET | Retrieve session details | Module graph |
| `/api/harness/session/:id` | DELETE | Delete a session | Module graph |

### Turn Endpoint

| Attribute | Value | Source |
|-----------|-------|--------|
| Endpoint | `POST /api/harness/turn` | `docs/SPEC.md` Section 9.8; module graph |
| Input payload | `{ sessionId, message, opts, attachments? }` | `docs/SPEC.md` Section 9.8; sequence diagram |
| Response type | `200 text/event-stream` (SSE) | Sequence diagram step 102 |
| Optional attachments | Array of absolute filesystem path strings | `docs/SPEC.md` Section 9.8 |

### Typed Failure Contract (Baseline)

| Attribute | Value | Source |
|-----------|-------|--------|
| Error response structure | HTTP status code + error type identifier + human-readable message | **ASSUMPTION** -- inferred from standard API contract conventions and DEL-03-01 Specification REQ-11 pattern |
| Session-not-found error | Route returns appropriate HTTP error when `sessionId` does not resolve | DEL-03-01 Specification REQ-11 (analogous pattern) |
| Validation errors | Route returns `400` for malformed request bodies | **ASSUMPTION** -- inferred from standard Next.js API route conventions |
| Turn with no content | Returns `400` when all attachments fail and user text is empty | `docs/SPEC.md` Section 9.8 (attachment handling rules) |

### Runtime Integration Points

| Attribute | Value | Source |
|-----------|-------|--------|
| SessionManager | create/resume/save/list/delete sessions | Module graph |
| PersonaManager | Build append prompt + model selection; boot fingerprint | Module graph |
| AttachmentResolver | Paths to content blocks (turn endpoint) | Module graph |
| AgentSdkManager | startTurn/interrupt/kill; interfaces with Anthropic Agent SDK | Module graph |
| AgentSdkEventMapper | SDKMessage to UIEvent mapping (turn endpoint SSE) | Module graph |

### Options Mapping (Boot + Turn)

| Attribute | Value | Source |
|-----------|-------|--------|
| `opts` acceptance | Both boot and turn endpoints accept `opts` | `docs/SPEC.md` Section 9.8 |
| Model fallback chain | `opts.model` -> global model (instruction root) -> runtime default | `docs/SPEC.md` Section 9.8 |
| Tools fallback chain | `opts.tools` -> persona `tools` frontmatter -> runtime preset | `docs/SPEC.md` Section 9.8 |
| Max turns fallback chain | `opts.maxTurns` -> persona `max_turns` frontmatter -> runtime default | `docs/SPEC.md` Section 9.8 |

---

## Conditions

| Condition | Requirement | Source |
|-----------|-------------|--------|
| Platform | macOS 15+, Apple Silicon only | DEC-PLAT-001 |
| Network policy | Outbound connections limited to Anthropic API only | DEC-NET-001 |
| Local-only execution | All code implemented in `frontend/` workspace within this repository | SOW-045; Decomposition SCA-001; `docs/PLAN.md` local-only source policy |
| Prerequisite: frontend workspace | `frontend/` workspace must exist with package manifest, build config, and startup scripts (DEL-01-03) | Decomposition SCA-001 execution gating rule |
| Pre-tier gate | DEL-03-07 must reach at least IN_PROGRESS before Tier 2 code-bearing work depending on frontend paths can proceed | Decomposition SCA-001 execution gating rule |
| Filesystem-as-state | Session data stored as plain files; no external database | DIRECTIVE Section 2.1; K-GHOST-1 |
| No server requirement | Desktop-first; works without external server infrastructure | DIRECTIVE Section 5 |

---

## Construction

| Component | Role | Source |
|-----------|------|--------|
| Next.js API Route Handlers | HTTP endpoint implementations for session CRUD, boot, and turn | Module graph; SOW-045 |
| SessionManager module | Session lifecycle operations (create/resume/save/list/delete) | Module graph |
| PersonaManager module | Persona prompt construction and boot fingerprint computation | Module graph |
| AgentSdkManager module | SDK query execution, turn management, interrupt/kill | Module graph |
| AgentSdkEventMapper module | Transform SDK stream messages to UI events | Module graph |
| AttachmentResolver module | Resolve file paths to content blocks for multimodal turns | Module graph |
| Observability Logger | JSONL logging with rotation | Module graph |
| Type definitions | TypeScript types for request/response shapes, error types, and failure contracts | **ASSUMPTION** -- inferred from BACKEND_FEATURE_SLICE type and TypeScript baseline |
| Route-contract tests | Baseline tests validating route compilation and contract conformance | SOW-045 acceptance criteria |

---

## References

| Reference | Location | Relevance |
|-----------|----------|-----------|
| Software Decomposition (G7-APPROVED + SCA-001) | `execution/_Decomposition/ChiralityApp_SoftwareDecomposition_2026-02-21_G7-APPROVED.md` | DEL-03-07 definition, scope items, objectives, execution gating rule |
| SPEC -- Physical Structures and Mechanics | `docs/SPEC.md` Section 9.8 | Harness turn input contract, session boot API, opts mapping, attachment rules |
| DIRECTIVE -- Founding Intent | `docs/DIRECTIVE.md` | Filesystem-as-state, instruction root vs working root separation |
| CONTRACT -- Invariant Catalog | `docs/CONTRACT.md` | K-GHOST-1, K-INVENT-1, K-STATUS-1 binding invariants |
| Harness Architecture Graphs & Sequence | `docs/harness/chirality_harness_graphs_and_sequence.md` | Module dependency graph, session boot sequence, turn sequence diagram |
| Harness Manual Validation | `docs/harness/harness_manual_validation.md` | Validation script references, session CRUD checks, Section 8 matrix |
| Harness CI Integration | `docs/harness/harness_ci_integration.md` | CI workflow, pre-merge validation, summary artifact requirements |
| PLAN -- Development Roadmap | `docs/PLAN.md` Section 2 | FE-2 Harness API Baseline phasing; local-only source policy |
| DEL-03-01 Specification | `execution/PKG-03_Harness_Runtime_Core/1_Working/DEL-03-01_Working_Root_Session_Boot/Specification.md` | Session CRUD and boot contract interface context |
| DEL-03-01 Datasheet | `execution/PKG-03_Harness_Runtime_Core/1_Working/DEL-03-01_Working_Root_Session_Boot/Datasheet.md` | Session record schema, options mapping attributes |
