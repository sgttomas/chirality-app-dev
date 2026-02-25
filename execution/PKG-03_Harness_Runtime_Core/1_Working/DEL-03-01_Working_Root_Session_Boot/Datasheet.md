# Datasheet — DEL-03-01 Working Root Binding & Session Boot

## Identification

| Field | Value |
|-------|-------|
| **Deliverable ID** | DEL-03-01 |
| **Name** | Working Root Binding & Session Boot |
| **Package** | PKG-03 Harness Runtime Core |
| **Type** | API_CONTRACT |
| **Context Envelope** | M |
| **Responsible Party** | TBD -- **[E-001]** Human decision required to assign accountability for this deliverable |
| **Scope Coverage** | SOW-003, SOW-004 |
| **Objectives** | OBJ-001, OBJ-002 |
| **Anticipated Artifacts** | CODE / TEST / DOC |
| **Decomposition Ref** | `execution/_Decomposition/ChiralityApp_SoftwareDecomposition_2026-02-21_G7-APPROVED.md` |

---

## Attributes

### Working Root Binding

| Attribute | Value | Source |
|-----------|-------|--------|
| Binding target | User-selected local filesystem directory (`projectRoot`) | DIRECTIVE Section 2.1; SOW-003 |
| Binding persistence | Session-scoped; stored in session record on filesystem | SPEC Section 9.8; harness architecture docs |
| Session storage location | TBD -- **[B-001, E-002, E-003]** The canonical base path for `.chirality/sessions/` is unresolved. Guidance T2 presents "Under Working Root" vs "Under app data directory" as an open trade-off. Datasheet previously assumed app state path; Specification REQ-07 says only "local filesystem." Human ruling required to establish a single canonical location. See Conflict Table in Guidance.md (CONFLICT-001, CONFLICT-002). | harness architecture sequence diagram; Guidance T2 |
| Root validation | Must be a valid accessible directory on the local filesystem. **ASSUMPTION** -- inferred from filesystem-as-state design. **[A-002]** TBD: Does the runtime accept any valid directory (including empty directories), or require a specific structure (e.g., existing `.chirality/` folder)? Human decision required. | **ASSUMPTION** |
| Root type | Working Root (`projectRoot`) as distinguished from Instruction Root (app bundle) | DIRECTIVE Section 2.6; Vocabulary Map |

### Session Boot API

| Attribute | Value | Source |
|-----------|-------|--------|
| Endpoint | `POST /api/harness/session/boot` | SPEC Section 9.8; harness architecture docs |
| Input payload | `{ sessionId }` plus optional `opts` | SPEC Section 9.8; harness sequence diagram |
| Related session creation endpoint | `POST /api/harness/session/create` | harness architecture module graph |
| Bootstrap policy | Authoritative for bootstrap-only constraints | SPEC Section 9.8 |
| Boot fingerprint | Computed via `getBootFingerprint(persona, mode)` | harness sequence diagram |
| Boot persistence | Saves `claudeSessionId`, `bootFingerprint`, `bootedAt` | harness sequence diagram |
| Response shape | `200 { session, boot }` | harness sequence diagram |
| Error response shape | `{"error":{"type":"<HarnessErrorType>","message":"<human-readable>","details":<object|null>}}`; REQ-11 status/type pairs: `404/SESSION_NOT_FOUND`, `404/PERSONA_NOT_FOUND`, `500/SDK_FAILURE`, `404/WORKING_ROOT_INACCESSIBLE` | Specification REQ-11; Guidance C3 |

### Session Management APIs (related surface)

| Attribute | Value | Source |
|-----------|-------|--------|
| Session create | `POST /api/harness/session/create` | harness architecture module graph |
| Session list | `GET /api/harness/session/list` | harness architecture module graph |
| Session get | `GET /api/harness/session/:id` | harness architecture module graph |
| Session delete | `DELETE /api/harness/session/:id` | harness architecture module graph |

### Runtime Option Mapping (boot-relevant subset)

| Attribute | Value | Source |
|-----------|-------|--------|
| `opts` acceptance | Session boot accepts `opts` object | SPEC Section 9.8 |
| Model fallback chain | `opts.model` -> global model (instruction root) -> runtime default | SPEC Section 9.8 |
| Tools fallback chain | `opts.tools` -> persona `tools` frontmatter -> runtime preset | SPEC Section 9.8 |
| Max turns fallback chain | `opts.maxTurns` -> persona `max_turns` frontmatter -> runtime default | SPEC Section 9.8 |

### Session Record Schema -- **[F-002]**

The following table consolidates all session record fields referenced across documents. A complete normative schema is TBD pending implementation review.

| Field | Type | Set By | Source |
|-------|------|--------|--------|
| `sessionId` | string | Session creation (`POST /api/harness/session/create`) | harness architecture module graph |
| `projectRoot` | string (filesystem path) | Session creation (user-selected Working Root) | SPEC Section 9.8; DIRECTIVE Section 2.1 |
| `claudeSessionId` | string | Boot sequence (from Anthropic Agent SDK `query()` response) | harness sequence diagram |
| `bootFingerprint` | string | Boot sequence (`PersonaManager.getBootFingerprint(persona, mode)`) | harness sequence diagram |
| `bootedAt` | string (timestamp) | Boot sequence | harness sequence diagram |
| `persona` | TBD | TBD -- referenced in boot fingerprint computation and Guidance example, but not normatively required in session record by Specification | **ASSUMPTION** -- inferred from Guidance Example |
| `mode` | TBD | TBD -- referenced in boot fingerprint computation, but not normatively required in session record by Specification | **ASSUMPTION** -- inferred from Guidance Example |

**Note:** This schema is descriptive (best-effort consolidation from available sources). The normative definition of required fields belongs in Specification.md. Fields marked TBD require human confirmation.

---

## Conditions

| Condition | Requirement | Source |
|-----------|-------------|--------|
| Platform | macOS 15+, Apple Silicon only | DEC-PLAT-001 |
| Network policy | Outbound connections limited to Anthropic API only | DEC-NET-001 |
| Desktop runtime | Electron + Next.js desktop application | SOW-001; PLAN Section 2 |
| Filesystem-as-state | Session data stored as plain files; no external database | DIRECTIVE Section 2.1; K-GHOST-1 |
| No server requirement | Desktop-first; works without external server infrastructure | DIRECTIVE Section 5 |

---

## Construction

| Component | Role | Source |
|-----------|------|--------|
| SessionManager | Create/resume/save/list/delete sessions; persists session records to filesystem | harness architecture module graph |
| PersonaManager | Build append prompt + model selection; provides boot fingerprint | harness architecture module graph |
| AgentSdkManager | Start turns / interrupt / kill; interfaces with Anthropic Agent SDK | harness architecture module graph |
| API Routes (Next.js) | HTTP endpoints for session CRUD and boot | harness architecture module graph |
| Filesystem (`.chirality/sessions`) | Session state persistence (exact base path TBD -- see Conflict Table in Guidance.md) | harness architecture module graph |

---

## References

| Reference | Location | Relevance |
|-----------|----------|-----------|
| Software Decomposition (G7-APPROVED) | `execution/_Decomposition/ChiralityApp_SoftwareDecomposition_2026-02-21_G7-APPROVED.md` | DEL-03-01 definition, scope items, objectives |
| SPEC -- Physical Structures and Mechanics | `docs/SPEC.md` Section 9.8 | Harness turn input contract, session boot API, opts mapping |
| DIRECTIVE -- Founding Intent | `docs/DIRECTIVE.md` Section 2.1, 2.6 | Filesystem-as-state, instruction root vs working root separation |
| CONTRACT -- Invariant Catalog | `docs/CONTRACT.md` | K-GHOST-1, K-STATUS-1 binding invariants |
| Harness Architecture Graphs & Sequence | `docs/harness/chirality_harness_graphs_and_sequence.md` | Module dependency graph, session boot sequence diagram |
| Harness Manual Validation | `docs/harness/harness_manual_validation.md` | Validation script references, session persistence checks |
| PLAN -- Development Roadmap | `docs/PLAN.md` Section 2 | Existing tooling and desktop frontend description |
| _SEMANTIC_LENSING.md | This deliverable folder | Pass 3 enrichment inputs (items A-001 through E-003) |
