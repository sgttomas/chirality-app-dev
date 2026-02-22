# Dependencies: DEL-01-03 Frontend Workspace Bootstrap & Packaging Baseline

## Coordination (human-owned)
- **Mode:** FULL_GRAPH
- **Notes:** See `execution/_Coordination/_COORDINATION.md`

## Upstream (I need these before I can proceed) — human-owned declarations
- No upstream deliverable prerequisites. This is a foundation deliverable (pre-tier gate).
- Document constraints: `docs/SPEC.md`, `docs/DIRECTIVE.md`, `docs/CONTRACT.md`

## Downstream (These need me) — human-owned declarations
- **DEL-01-01** (macOS Build Baseline) — needs `frontend/` workspace for desktop build
- **DEL-01-02** (Unsigned DMG Packaging) — needs packaging baseline scripts
- **DEL-02-05** (Frontend Workflow Shell) — needs `frontend/` workspace for UI shell
- **DEL-03-07** (Harness API Baseline) — needs `frontend/` workspace for API routes
- **DEL-07-03** (Frontend Validation) — needs `frontend/` workspace for validation scripts

## Extracted Dependency Register

- **Status:** COMPLETE
- **Dependencies.csv:** `Dependencies.csv` (v3.1, 13 rows)
- **Last Run:** 2026-02-22

### Summary

| Metric | Count |
|--------|-------|
| Total rows | 13 |
| ACTIVE | 13 |
| RETIRED | 0 |

### By DependencyClass

| Class | ACTIVE |
|-------|--------|
| ANCHOR | 5 |
| EXECUTION | 8 |

### Anchor Detail

| DependencyID | AnchorType | TargetRefID | TargetName | Confidence |
|--------------|------------|-------------|------------|------------|
| DEP-01-03-001 | IMPLEMENTS_NODE | -- | PKG-01 Build & Packaging | HIGH |
| DEP-01-03-002 | TRACES_TO_REQUIREMENT | SOW-044 | SOW-044: Create in-repo frontend/ workspace baseline | HIGH |
| DEP-01-03-003 | TRACES_TO_REQUIREMENT | SOW-047 | SOW-047: Implement frontend desktop packaging baseline | HIGH |
| DEP-01-03-004 | TRACES_TO_REQUIREMENT | OBJ-001 | OBJ-001: Working macOS desktop build and install path | HIGH |
| DEP-01-03-005 | TRACES_TO_REQUIREMENT | OBJ-008 | OBJ-008: Local frontend runtime baseline | HIGH |

### Execution Detail

| DependencyID | Direction | DependencyType | TargetType | Target | Confidence |
|--------------|-----------|----------------|------------|--------|------------|
| DEP-01-03-006 | UPSTREAM | CONSTRAINT | DOCUMENT | docs/SPEC.md | HIGH |
| DEP-01-03-007 | UPSTREAM | CONSTRAINT | DOCUMENT | docs/DIRECTIVE.md | HIGH |
| DEP-01-03-008 | UPSTREAM | CONSTRAINT | DOCUMENT | docs/CONTRACT.md | MEDIUM |
| DEP-01-03-009 | DOWNSTREAM | PREREQUISITE | DELIVERABLE | DEL-01-01 (macOS Build Baseline) | HIGH |
| DEP-01-03-010 | DOWNSTREAM | PREREQUISITE | DELIVERABLE | DEL-01-02 (Unsigned DMG Packaging) | HIGH |
| DEP-01-03-011 | DOWNSTREAM | PREREQUISITE | DELIVERABLE | DEL-02-05 (Frontend Workflow Shell) | HIGH |
| DEP-01-03-012 | DOWNSTREAM | PREREQUISITE | DELIVERABLE | DEL-03-07 (Harness API Baseline) | HIGH |
| DEP-01-03-013 | DOWNSTREAM | PREREQUISITE | DELIVERABLE | DEL-07-03 (Frontend Validation) | HIGH |

## Run Notes

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

## Lifecycle Summary

| Status | Count |
|--------|-------|
| ACTIVE | 13 |
| RETIRED | 0 |

### Closure State Breakdown (ACTIVE rows)

| SatisfactionStatus | Count |
|--------------------|-------|
| NOT_APPLICABLE | 5 (all ANCHOR rows) |
| TBD | 3 (UPSTREAM CONSTRAINT rows) |
| PENDING | 5 (DOWNSTREAM PREREQUISITE rows) |

## Consumer Handoff Notes
- CONSUMER_CONTEXT: NONE. No consumer-specific annotations emitted.
