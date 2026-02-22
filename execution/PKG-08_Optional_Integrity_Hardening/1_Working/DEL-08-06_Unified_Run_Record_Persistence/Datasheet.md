# Datasheet — DEL-08-06 Unified Pipeline Run Record Persistence

## Identification

| Field | Value |
|-------|-------|
| **DeliverableID** | DEL-08-06 |
| **Name** | Unified Pipeline Run Record Persistence |
| **PackageID** | PKG-08 |
| **Package** | Optional Integrity Hardening |
| **Type** | DATA_MODEL_CHANGE |
| **ContextEnvelope** | L |
| **Responsible Party** | TBD — **resolution path:** human assignment required; no heuristic available to infer responsible party from decomposition or package context (Lensing item B-001) |
| **Scope Coverage** | SOW-037 |
| **Supports Objectives** | OBJ-007 |
| **Anticipated Artifacts** | DOC / CODE / TEST |
| **Scope Item Status** | TBD (scope decision pending per OI-037) — **NOTE:** documents proceed as if scope will be decided IN, but CODE and TEST artifacts require confirmed scope flip; see Conflict Table CON-04 in Guidance.md and cross-matrix conflict XCON-03 (Lensing item E-001) |

## Attributes

| Attribute | Value | Source |
|-----------|-------|--------|
| Schema name | TBD (unified run record schema) — **Canonical placeholder:** `_RUN_HISTORY.md` or `RunRecords.csv` pending storage location decision (CON-01/CON-02) | PLAN Section 3.6 |
| Schema format | Markdown and/or CSV — **ASSUMPTION: plain-file format consistent with filesystem-as-state constraint** | DIRECTIVE Section 2.1; SPEC Section 11 |
| Storage location | TBD — one of: deliverable-local, tool-root snapshot, or both | PLAN Section 3.6 ("storage location decision") |
| Record immutability | Snapshot semantics apply — once written, a run record MUST NOT be modified | SPEC Section 11.1; K-SNAP-1 (CONTRACT) |
| Record content scope | Per-agent-execution run metadata (agent identity, inputs, outputs, timestamps, status, baseline SHAs) | PLAN Section 3.6; K-VAL-1 (CONTRACT) |
| Baseline SHA tracking | TBD — SHA of governed inputs at run start, enabling staleness detection; computation method unresolved (see CON-03) | K-VAL-1, K-STALE-1 (CONTRACT); PLAN Section 3.7 (downstream consumer) |
| Integration points | Type 2 agent protocols (all current Type 2 agents), `_STATUS.md` history, `_DEPENDENCIES.md` run history | PLAN Section 3.6; SPEC Sections 3, 5 |
| Type 2 agents in scope | 4_DOCUMENTS, DEPENDENCIES, CHIRALITY_FRAMEWORK, CHIRALITY_LENS — **ASSUMPTION (best-effort):** this is the current known set; Guidance C4 says "at minimum," indicating additional agents may exist or be added; definitive enumeration requires current agent inventory review (Lensing item B-002) | PLAN Section 3.6 ("per Agent 2 execution"); Guidance C4 |
| Downstream consumers | DEL-08-07 (Staleness Propagation + Triage Tooling) — depends on run records with baseline SHAs | PLAN Section 3.7; Decomposition PKG-08 notes |
| Git-trackability | MUST produce plain-file artifacts that are git-diffable and git-committable | DIRECTIVE Section 2.2 |
| Provenance coverage | Run records should capture what was consumed (input files, context state) to satisfy provenance requirements — **mapping to K-PROV-1 is implicit via InputFiles and InputContextSHA fields** (Lensing item E-002; see Specification REQ-01 for details) | K-PROV-1 (CONTRACT) |

## Conditions

| Condition | Detail |
|-----------|--------|
| **Scope prerequisite** | SOW-037 must be flipped from TBD to IN before implementation work begins (OI-037). Documents may be prepared in advance; CODE/TEST artifacts are blocked until scope is confirmed. |
| **Design boundary** | Keep bounded to one schema + one storage location (Decomposition ContextEnvelopeNotes for DEL-08-06) |
| **No external database** | Run records MUST persist as filesystem artifacts — no external DB, no server state |
| **Compatibility** | Schema must coexist with existing `_STATUS.md` history entries and `_DEPENDENCIES.md` run history without breaking current consumers |
| **Audit trail** | Run records are the primary mechanism enabling formal audit trails for pipeline executions (PLAN Section 3.6) |
| **Rerun management** | Run records must support identification of prior runs and their outcomes to enable informed rerun decisions (PLAN Section 3.6) |
| **Schema evolution** | Schema includes a `SchemaVersion` field (v1.0 initial); evolution governance (migration path for existing records when version increments) is TBD — see Guidance D-001 enrichment and Procedure schema migration section (Lensing items D-001, D-002) |

## Construction

| Aspect | Detail |
|--------|--------|
| **Schema definition** | Define a unified run record schema covering: agent ID, agent type, run timestamp, deliverable ID, input context hash/SHA, output artifact list, run status (success/failure/partial), error summary, duration. RunStatus lifecycle transitions (valid state progressions, boundary conditions) require definition — see Specification REQ-01 enrichment (Lensing item B-003). |
| **Storage mechanism** | TBD — options include: (a) deliverable-local `_RUN_HISTORY.md` or `RunRecords.csv`, (b) tool-root snapshot folder per run, (c) hybrid (local pointer + snapshot). Canonical placeholder name: `_RUN_HISTORY.md` / `RunRecords.csv` (pending CON-01/CON-02 resolution). |
| **Agent protocol integration** | Modify Type 2 agent protocols to emit a run record on completion — **ASSUMPTION: integration is additive (append-only) and does not change existing agent behavior**. Current known agents: 4_DOCUMENTS, DEPENDENCIES, CHIRALITY_FRAMEWORK, CHIRALITY_LENS. |
| **Post-write validation** | TBD — run records should be validated after write to confirm schema conformance and parsability (Lensing item X-005; see Procedure Phase 2 enrichment). |
| **Validation** | TBD — run-record schema linting (may share infrastructure with DEL-08-02 Dependencies.csv linter approach) |
| **Testing** | Unit tests for schema validation; integration tests for agent run record emission; conformance tests against SPEC snapshot rules; crash/partial-write recovery scenario (Lensing item X-003) |

## References

| Ref | Document | Relevance |
|-----|----------|-----------|
| 1 | `docs/PLAN.md` Section 3.6 | Primary description of run record persistence as a hardening candidate |
| 2 | `docs/PLAN.md` Section 3.7 | Downstream dependency — staleness tooling depends on run records |
| 3 | `docs/PLAN.md` Section 4 | Sequencing rationale — run records are step 5 of 6 |
| 4 | `docs/DIRECTIVE.md` Section 2.1-2.2 | Filesystem-as-state and git-as-event-store constraints |
| 5 | `docs/DIRECTIVE.md` Section 5 | Structural constraints (no external DB, plain files, immutable snapshots) |
| 6 | `docs/SPEC.md` Section 11 | Snapshot and pointer conventions |
| 7 | `docs/SPEC.md` Section 3 | `_STATUS.md` lifecycle state (existing run-tracking mechanism) |
| 8 | `docs/SPEC.md` Section 5 | `_DEPENDENCIES.md` format (existing run history section) |
| 9 | `docs/CONTRACT.md` K-SNAP-1 | Immutable snapshot invariant |
| 10 | `docs/CONTRACT.md` K-VAL-1 | Dirty detection via SHA comparison |
| 11 | `docs/CONTRACT.md` K-STALE-1, K-STALE-2 | Staleness propagation and triage requirements |
| 12 | `docs/CONTRACT.md` K-PROV-1 | Provenance requirements — run records should cite what was consumed |
| 13 | Decomposition DEL-08-06 entry | Deliverable definition and context envelope notes |
| 14 | Decomposition DEL-08-07 entry | Downstream consumer — staleness tooling depends on run records |
| 15 | `_SEMANTIC_LENSING.md` | Pass 3 enrichment source — 23 warranted items applied 2026-02-21 |
