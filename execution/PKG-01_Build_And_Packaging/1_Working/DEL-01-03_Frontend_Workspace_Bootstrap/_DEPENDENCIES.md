# Dependencies: DEL-01-03 Frontend Workspace Bootstrap & Packaging Baseline

## Coordination (human-owned)
- **Mode:** FULL_GRAPH
- **Notes:** See `execution/_Coordination/_COORDINATION.md`

## Upstream (I need these before I can proceed) — human-owned declarations
- No upstream deliverable prerequisites. This is a foundation deliverable (pre-tier gate).
- Document constraints: `docs/SPEC.md`, `docs/DIRECTIVE.md`, `docs/CONTRACT.md`, `docs/PLAN.md`
- Integration-pattern interface: DEL-03-07 (Harness API Baseline) -- output mode decision depends on DEL-03-07's API route requirements

## Downstream (These need me) — human-owned declarations
- **DEL-01-01** (macOS Build Baseline) — needs `frontend/` workspace for desktop build
- **DEL-01-02** (Unsigned DMG Packaging) — needs packaging baseline scripts
- **DEL-02-05** (Frontend Workflow Shell) — needs `frontend/` workspace for UI shell
- **DEL-03-07** (Harness API Baseline) — needs `frontend/` workspace for API routes
- **DEL-07-03** (Frontend Validation) — needs `frontend/` workspace for validation scripts

## Extracted Dependency Register

- **Status:** COMPLETE
- **Dependencies.csv:** `Dependencies.csv` (v3.1, 17 rows)
- **Last Run:** 2026-02-22 (re-extraction from enriched production docs)

### Summary

| Metric | Count |
|--------|-------|
| Total rows | 17 |
| ACTIVE | 17 |
| RETIRED | 0 |

### By DependencyClass

| Class | ACTIVE |
|-------|--------|
| ANCHOR | 7 |
| EXECUTION | 10 |

### Anchor Detail

| DependencyID | AnchorType | TargetRefID | TargetName | Confidence |
|--------------|------------|-------------|------------|------------|
| DEP-01-03-001 | IMPLEMENTS_NODE | -- | PKG-01 Build & Packaging | HIGH |
| DEP-01-03-002 | TRACES_TO_REQUIREMENT | SOW-044 | SOW-044: Create in-repo frontend/ workspace baseline | HIGH |
| DEP-01-03-003 | TRACES_TO_REQUIREMENT | SOW-047 | SOW-047: Implement frontend desktop packaging baseline | HIGH |
| DEP-01-03-004 | TRACES_TO_REQUIREMENT | OBJ-001 | OBJ-001: Working macOS desktop build and install path | HIGH |
| DEP-01-03-005 | TRACES_TO_REQUIREMENT | OBJ-008 | OBJ-008: Local frontend runtime baseline | HIGH |
| DEP-01-03-014 | TRACES_TO_REQUIREMENT | SOW-001 | SOW-001: Chirality desktop app builds and runs as Electron + Next.js | HIGH |
| DEP-01-03-015 | TRACES_TO_REQUIREMENT | SOW-013 | SOW-013: Separate Instruction Root vs Working Root | HIGH |

### Execution Detail

| DependencyID | Direction | DependencyType | TargetType | Target | Confidence |
|--------------|-----------|----------------|------------|--------|------------|
| DEP-01-03-006 | UPSTREAM | CONSTRAINT | DOCUMENT | docs/SPEC.md | HIGH |
| DEP-01-03-007 | UPSTREAM | CONSTRAINT | DOCUMENT | docs/DIRECTIVE.md | HIGH |
| DEP-01-03-008 | UPSTREAM | CONSTRAINT | DOCUMENT | docs/CONTRACT.md | MEDIUM |
| DEP-01-03-016 | UPSTREAM | CONSTRAINT | DOCUMENT | docs/PLAN.md | HIGH |
| DEP-01-03-017 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-03-07 (integration-pattern dependency) | HIGH |
| DEP-01-03-009 | DOWNSTREAM | PREREQUISITE | DELIVERABLE | DEL-01-01 (macOS Build Baseline) | HIGH |
| DEP-01-03-010 | DOWNSTREAM | PREREQUISITE | DELIVERABLE | DEL-01-02 (Unsigned DMG Packaging) | HIGH |
| DEP-01-03-011 | DOWNSTREAM | PREREQUISITE | DELIVERABLE | DEL-02-05 (Frontend Workflow Shell) | HIGH |
| DEP-01-03-012 | DOWNSTREAM | PREREQUISITE | DELIVERABLE | DEL-03-07 (Harness API Baseline) | HIGH |
| DEP-01-03-013 | DOWNSTREAM | PREREQUISITE | DELIVERABLE | DEL-07-03 (Frontend Validation) | HIGH |

### Notable: Bidirectional Coupling with DEL-03-07

DEL-03-07 appears in both UPSTREAM (DEP-01-03-017, INTERFACE) and DOWNSTREAM (DEP-01-03-012, PREREQUISITE) edges. This is not a cycle; the two edges represent different information flows:
- **DOWNSTREAM (DEP-01-03-012):** DEL-03-07 needs the `frontend/` workspace artifact that DEL-01-03 produces.
- **UPSTREAM (DEP-01-03-017):** DEL-01-03 needs to know DEL-03-07's API route requirements to choose the correct Next.js output mode (static export vs. custom server).

This bidirectional coupling is explicitly stated in Specification.md REQ-04 and Guidance.md C1.

## Run Notes

### Run 2026-02-22 (re-extraction from enriched production docs)

**Defaults and configuration:**
- MODE: UPDATE
- STRICTNESS: CONSERVATIVE
- CONSUMER_CONTEXT: NONE
- SOURCE_DOCS: Enriched production docs (Datasheet.md, Specification.md, Guidance.md, Procedure.md)
- ANCHOR_DOC: Datasheet.md (selected by DOC_ROLE_MAP heuristic: contains "datasheet")
- EXECUTION_DOC_ORDER: Specification.md, Procedure.md, Guidance.md
- DECOMPOSITION_PATH: `execution/_Decomposition/ChiralityApp_SoftwareDecomposition_2026-02-21_G7-APPROVED.md` (loaded; Scope Amendment A1 confirmed)
- _REFERENCES.md: read (no deliverable-specific references beyond standard pointers)

**Warnings:** None.

**Integrity checks:**
- IMPLEMENTS_NODE count: 1 (OK)
- DependencyID uniqueness: PASS (17 unique IDs)
- All ACTIVE rows have EvidenceFile + SourceRef: PASS
- FromDeliverableID consistency: PASS (all DEL-01-03)
- CSV parseable: PASS (29 columns, 17 data rows)
- TargetDeliverableID placement: PASS (DELIVERABLE rows use TargetDeliverableID; DOCUMENT/WBS_NODE/REQUIREMENT/PACKAGE rows use TargetRefID or TargetName only)

**Delta from prior run (13 rows -> 17 rows):**
- 13 existing rows confirmed ACTIVE; evidence references updated to reflect enriched production doc locations.
- 4 new rows extracted from enriched production docs:
  - DEP-01-03-014 (ANCHOR / SOW-001): Specification.md REQ-05 explicitly traces Electron main process requirement to SOW-001.
  - DEP-01-03-015 (ANCHOR / SOW-013): Specification.md REQ-09 and Guidance.md P3 explicitly trace instruction-root inclusion to SOW-013.
  - DEP-01-03-016 (EXECUTION / UPSTREAM CONSTRAINT / docs/PLAN.md): Enriched Datasheet.md, Specification.md, Procedure.md, and Guidance.md all explicitly reference PLAN.md as a required document constraint with specific sections (FE-1, FE-4 acceptance criteria).
  - DEP-01-03-017 (EXECUTION / UPSTREAM INTERFACE / DEL-03-07): Specification.md REQ-04 and Guidance.md C1 explicitly state the integration pattern depends on DEL-03-07's API route requirements.

**Extraction notes:**
- ANCHOR rows derive from Datasheet.md explicit scope/objective coverage tables and Specification.md requirement source citations, validated against decomposition Scope Amendment A1.
- SOW-001 and SOW-013 are secondary traces: their primary coverage is by DEL-01-01 and DEL-05-01 respectively, but DEL-01-03 explicitly references them as requirement sources in the enriched Specification.md.
- UPSTREAM EXECUTION rows represent document constraints (SPEC, DIRECTIVE, CONTRACT, PLAN) explicitly cited as standards/references in Specification.md, Procedure.md, Guidance.md, and Datasheet.md.
- DOWNSTREAM EXECUTION rows represent explicit information-flow prerequisites stated in Datasheet.md Downstream Consumers table, Specification.md Downstream Consumers table, and Guidance.md C5.
- DEP-01-03-017 (UPSTREAM INTERFACE to DEL-03-07) captures a design-time information dependency, not a build-time artifact dependency. The enriched Specification.md makes this explicit in REQ-04's resolution criteria.
- The Execution Gating Rule in decomposition lists additional deliverables (DEL-03-01, DEL-05-03, DEL-05-04) as blocked by the pre-tier gate set. These were NOT emitted as direct downstream edges from DEL-01-03 because the gating is collective (blocked until all four pre-tier deliverables reach IN_PROGRESS) rather than a direct information-flow from this specific deliverable. Under CONSERVATIVE strictness, only deliverables explicitly stated as consumers of DEL-01-03 output in this deliverable's source documents were registered.
- DEP-01-03-008 (CONTRACT.md) retains MEDIUM confidence because the specific K-* invariants constraining this deliverable are not yet enumerated (Specification.md notes "location TBD" for specific invariants).

### Run 2026-02-22 (initial extraction)

**Defaults and configuration:**
- MODE: UPDATE
- STRICTNESS: CONSERVATIVE
- CONSUMER_CONTEXT: NONE
- SOURCE_DOCS: AUTO (resolved: Datasheet.md, Specification.md, Guidance.md, Procedure.md, _CONTEXT.md)
- ANCHOR_DOC: Datasheet.md (selected by DOC_ROLE_MAP heuristic: contains "datasheet")
- EXECUTION_DOC_ORDER: Specification.md, Procedure.md, Guidance.md
- DECOMPOSITION_PATH: `execution/_Decomposition/ChiralityApp_SoftwareDecomposition_2026-02-21_G7-APPROVED.md` (loaded; Scope Amendment A1 confirmed)
- _REFERENCES.md: read (no deliverable-specific references; used for document location resolution)

**Warnings:** None.

**Integrity checks:**
- IMPLEMENTS_NODE count: 1 (OK)
- DependencyID uniqueness: PASS (13 unique IDs)
- All ACTIVE rows have EvidenceFile + SourceRef: PASS
- FromDeliverableID consistency: PASS (all DEL-01-03)
- CSV parseable: PASS (29 columns, 13 rows)

**Extraction notes:**
- ANCHOR rows derive from _CONTEXT.md and Datasheet.md explicit scope/objective coverage tables, validated against decomposition Scope Amendment A1.
- UPSTREAM EXECUTION rows represent document constraints (SPEC, DIRECTIVE, CONTRACT) explicitly cited as standards/references in Specification.md and Procedure.md.
- DOWNSTREAM EXECUTION rows represent explicit information-flow prerequisites stated in Datasheet.md Sibling Deliverables table, Specification.md Downstream Consumers table, and Guidance.md C5.
- The Execution Gating Rule in decomposition lists additional deliverables (DEL-03-01, DEL-05-03, DEL-05-04) as blocked by the pre-tier gate set. These were NOT emitted as direct downstream edges from DEL-01-03 because the gating is collective (blocked until all four pre-tier deliverables reach IN_PROGRESS) rather than a direct information-flow from this specific deliverable. Under CONSERVATIVE strictness, only deliverables explicitly stated as consumers of DEL-01-03 output in this deliverable's source documents were registered.
- DEP-01-03-008 (CONTRACT.md) assigned MEDIUM confidence because the specific K-* invariants constraining this deliverable are not yet enumerated (Specification.md notes "location TBD" for specific invariants).

## Run History

| Timestamp | Mode | Strictness | Decomposition | Warnings | ACTIVE Count |
|-----------|------|------------|---------------|----------|--------------|
| 2026-02-22 | UPDATE | CONSERVATIVE | Loaded (G7-APPROVED + SCA-001) | None | 13 |
| 2026-02-22 (re-extraction) | UPDATE | CONSERVATIVE | Loaded (G7-APPROVED + SCA-001) | None | 17 |

## Lifecycle Summary

| Status | Count |
|--------|-------|
| ACTIVE | 17 |
| RETIRED | 0 |

### Closure State Breakdown (ACTIVE rows)

| SatisfactionStatus | Count |
|--------------------|-------|
| NOT_APPLICABLE | 7 (all ANCHOR rows) |
| TBD | 5 (UPSTREAM CONSTRAINT + INTERFACE rows) |
| PENDING | 5 (DOWNSTREAM PREREQUISITE rows) |

## Consumer Handoff Notes
- CONSUMER_CONTEXT: NONE. No consumer-specific annotations emitted.
