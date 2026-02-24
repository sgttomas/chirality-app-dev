# Dependencies: DEL-03-07 Harness API Baseline in Frontend Runtime

## Coordination (human-owned)
- **Mode:** FULL_GRAPH
- **Notes:** See `execution/_Coordination/_COORDINATION.md`

## Upstream (I need these before I can proceed) -- human-owned declarations
- (None declared yet -- to be populated by human)

## Downstream (These need me) -- human-owned declarations
- (None declared yet -- to be populated by human)

## Extracted Dependency Register

- **Status:** CURRENT
- **Dependencies.csv:** `Dependencies.csv` (v3.1, 18 rows, 18 ACTIVE / 0 RETIRED)
- **Last Run:** 2026-02-24 (UPDATE fan-in refresh, lifecycle/timestamp refresh only)

### Summary by Class

| DependencyClass | Count | Details |
|-----------------|-------|---------|
| ANCHOR | 3 | 1 IMPLEMENTS_NODE (SOW-045), 2 TRACES_TO_REQUIREMENT (OBJ-002, OBJ-008) |
| EXECUTION | 15 | 7 UPSTREAM (4 deliverables, 3 upstream interfaces new this run), 4 DOWNSTREAM, 5 UPSTREAM documents (4 carried forward, 1 new CONSTRAINT) |

### ANCHOR Edges

| DependencyID | AnchorType | TargetRefID / TargetName | Confidence |
|--------------|------------|--------------------------|------------|
| DEP-03-07-001 | IMPLEMENTS_NODE | SOW-045 | HIGH |
| DEP-03-07-002 | TRACES_TO_REQUIREMENT | OBJ-002 | HIGH |
| DEP-03-07-003 | TRACES_TO_REQUIREMENT | OBJ-008 | HIGH |

### EXECUTION Edges -- UPSTREAM (inputs to this deliverable)

| DependencyID | DependencyType | TargetType | Target | Confidence |
|--------------|---------------|------------|--------|------------|
| DEP-03-07-004 | PREREQUISITE | DELIVERABLE | DEL-01-03 (Frontend Workspace Bootstrap) | HIGH |
| DEP-03-07-005 | INTERFACE | DOCUMENT | docs/SPEC.md Section 9.8 | HIGH |
| DEP-03-07-006 | INTERFACE | DOCUMENT | docs/harness/chirality_harness_graphs_and_sequence.md | HIGH |
| DEP-03-07-007 | INTERFACE | DOCUMENT | docs/harness/harness_manual_validation.md | HIGH |
| DEP-03-07-008 | INTERFACE | DOCUMENT | docs/harness/harness_ci_integration.md | MEDIUM |
| DEP-03-07-009 | INTERFACE | DELIVERABLE | DEL-03-01 (Working Root Binding & Session Boot) -- contract conformance | HIGH |
| DEP-03-07-013 | INTERFACE | DELIVERABLE | DEL-03-05 (Anthropic Provider Integration) -- SDK delegation, stubbable | HIGH |
| DEP-03-07-015 | INTERFACE | DELIVERABLE | DEL-04-01 (Attachment Resolver) -- attachment resolution, stubbable | HIGH |
| DEP-03-07-016 | INTERFACE | DELIVERABLE | DEL-03-03 (Turn Options Mapping) -- opts fallback chain internals | MEDIUM |
| DEP-03-07-017 | CONSTRAINT | DOCUMENT | docs/CONTRACT.md -- K-GHOST-1, K-INVENT-1 binding invariants | HIGH |
| DEP-03-07-018 | INTERFACE | DELIVERABLE | DEL-03-02 (Turn Execution / SSE Streaming) -- event mapper module, stubbable | HIGH |

### EXECUTION Edges -- DOWNSTREAM (outputs from this deliverable)

| DependencyID | DependencyType | TargetType | Target | Confidence |
|--------------|---------------|------------|--------|------------|
| DEP-03-07-010 | HANDOVER | DELIVERABLE | DEL-03-02 (Turn Execution API + SSE Streaming) | HIGH |
| DEP-03-07-011 | ENABLES | DELIVERABLE | DEL-02-05 (Frontend Workflow Shell Baseline) | HIGH |
| DEP-03-07-012 | ENABLES | DELIVERABLE | DEL-07-03 (Frontend Validation & Runbook Baseline) | HIGH |
| DEP-03-07-014 | ENABLES | DELIVERABLE | DEL-03-01 (Working Root Binding & Session Boot) -- pre-tier gate | HIGH |

### Bidirectional Relationships (notable)

- **DEL-03-01**: UPSTREAM interface (DEP-03-07-009, contract conformance) + DOWNSTREAM enables (DEP-03-07-014, pre-tier gate). Two distinct information flows.
- **DEL-03-02**: UPSTREAM interface (DEP-03-07-018, event mapper module) + DOWNSTREAM handover (DEP-03-07-010, route surface). Two distinct information flows.

---

## Run Notes

### Defaults Used
- **SOURCE_DOCS:** AUTO -- scanned Datasheet.md, Specification.md, Guidance.md, Procedure.md
- **DOC_ROLE_MAP:** DEFAULT heuristic
- **ANCHOR_DOC:** Datasheet.md (highest-confidence match: contains "datasheet" in filename)
- **EXECUTION_DOC_ORDER:** Specification.md, Guidance.md, Procedure.md
- **MODE:** UPDATE
- **STRICTNESS:** CONSERVATIVE
- **CONSUMER_CONTEXT:** NONE
- **DECOMPOSITION_PATH:** `execution/_Decomposition/ChiralityApp_SoftwareDecomposition_2026-02-21_G7-APPROVED.md` (resolved, includes SCA-001 amendment)

### Decomposition Validation
- Decomposition located and loaded successfully.
- SOW-045 confirmed in Scope Ledger Overlay (Amendment A1 row, PKG-03, DEL-03-07).
- OBJ-002 confirmed in Objectives section.
- OBJ-008 confirmed in Added Objective (Amendment A1).
- DEL-01-03 confirmed as deliverable in Amendment A1 Added Deliverables.
- DEL-03-01, DEL-03-02, DEL-03-03, DEL-03-05, DEL-02-05, DEL-04-01, DEL-07-03 all confirmed in decomposition Deliverables table.

### Warnings
- (none)

### Evidence Quality Notes
- All ANCHOR rows cite explicit identifier fields in Datasheet.md and _CONTEXT.md.
- All EXECUTION rows cite explicit statements in Specification.md, Guidance.md, or Procedure.md.
- No IMPLICIT rows were emitted (CONSERVATIVE strictness).
- DEP-03-07-014 (downstream ENABLES to DEL-03-01) is based on the SCA-001 execution gating rule which explicitly names DEL-03-01 as blocked by DEL-03-07.

### Run 2 Delta (enriched production docs re-extraction)
- 4 new rows added: DEP-03-07-015 (DEL-04-01 attachment resolver), DEP-03-07-016 (DEL-03-03 opts mapping), DEP-03-07-017 (CONTRACT.md constraints), DEP-03-07-018 (DEL-03-02 event mapper upstream).
- All 14 existing rows confirmed ACTIVE with updated SourceRef citations reflecting enriched document content.
- New rows sourced from: Specification Excluded section boundary statements, Guidance E-003 stub replacement table (enrichment note), Specification Standards table (enriched), Procedure Step 5 module delegation, Datasheet Conditions K-GHOST-1 citation.
- DEP-03-07-016 (DEL-03-03) set to MEDIUM confidence because the boundary between route-level opts acceptance and internal mapping is clear but the information flow direction is less direct than other interfaces.

### Integration Fan-In Refresh (2026-02-24)
- Revalidated active lifecycle and interface posture after runtime singleton/error-taxonomy integration fixes.
- Refreshed `Dependencies.csv` `LastSeen` timestamps for all ACTIVE rows to `2026-02-24`.
- No dependency rows were added, retired, reclassified, or had `SatisfactionStatus` transitions.

---

## Run History

| Timestamp | Mode | Strictness | Decomposition | Warnings | ACTIVE Count | Notes |
|-----------|------|------------|---------------|----------|--------------|-------|
| 2026-02-24 (fan-in refresh) | UPDATE | CONSERVATIVE | Loaded (G7-APPROVED + SCA-001) | 0 | 18 | Lifecycle/timestamp refresh only; no edge or status deltas. |
| 2026-02-22 | UPDATE | CONSERVATIVE | Loaded (G7-APPROVED + SCA-001) | 0 | 14 | Initial extraction from scaffolded production docs. |
| 2026-02-22 | UPDATE | CONSERVATIVE | Loaded (G7-APPROVED + SCA-001) | 0 | 18 | Re-extraction from Pass 3 enriched production docs. +4 new rows (DEP-03-07-015..018). |

---

## Lifecycle Summary

| Status | Count |
|--------|-------|
| ACTIVE | 18 |
| RETIRED | 0 |

### Closure State Breakdown (ACTIVE rows)

| SatisfactionStatus | Count |
|--------------------|-------|
| TBD | 9 |
| PENDING | 4 |
| SATISFIED | 5 |

Notes:
- SATISFIED rows: 4 document-type dependencies where source documents are accessible (SPEC, module graph, validation doc, CI doc) + 1 document constraint (CONTRACT.md).
- PENDING rows: 4 deliverable prerequisites/interfaces not yet completed (DEL-01-03 workspace, DEL-03-01 contract, DEL-03-05 SDK integration, DEL-04-01 attachment resolver).
- TBD rows: 3 ANCHOR traces, 4 downstream ENABLES/HANDOVER edges, and 2 upstream interfaces (DEL-03-03 opts mapping, DEL-03-02 event mapper) awaiting execution progress.

---

## Consumer Handoff Notes
- **CONSUMER_CONTEXT:** NONE -- no consumer-specific annotations generated.
