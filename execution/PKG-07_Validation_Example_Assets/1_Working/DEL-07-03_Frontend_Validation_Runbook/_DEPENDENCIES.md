# Dependencies: DEL-07-03 Frontend Validation & Runbook Baseline

## Coordination (human-owned)
- **Mode:** FULL_GRAPH
- **Notes:** See `execution/_Coordination/_COORDINATION.md`

## Upstream (I need these before I can proceed) -- human-owned declarations
- (None declared yet -- to be populated by human)

## Downstream (These need me) -- human-owned declarations
- (None declared yet -- to be populated by human)

## Extracted Dependency Register

- **Status:** COMPLETE
- **Dependencies.csv:** `Dependencies.csv` (17 rows, schema v3.1)
- **Last Run:** 2026-02-22 (UPDATE from enriched production docs)
- **Summary:**

### ANCHOR edges (5 ACTIVE)

| DependencyID | AnchorType | TargetType | TargetRefID / TargetName | Confidence |
|---|---|---|---|---|
| DEP-07-03-001 | IMPLEMENTS_NODE | WBS_NODE | PKG-07 Validation & Example Assets | HIGH |
| DEP-07-03-002 | TRACES_TO_REQUIREMENT | REQUIREMENT | SOW-048 | HIGH |
| DEP-07-03-003 | TRACES_TO_REQUIREMENT | REQUIREMENT | SOW-049 | HIGH |
| DEP-07-03-004 | TRACES_TO_REQUIREMENT | REQUIREMENT | OBJ-006 | HIGH |
| DEP-07-03-005 | TRACES_TO_REQUIREMENT | REQUIREMENT | OBJ-008 | HIGH |

### EXECUTION edges -- UPSTREAM (7 ACTIVE)

| DependencyID | DependencyType | TargetType | Target | Statement (summary) | Confidence |
|---|---|---|---|---|---|
| DEP-07-03-006 | PREREQUISITE | DELIVERABLE | DEL-01-03 (Frontend Workspace Bootstrap) | frontend/ workspace must be bootstrapped before validation scripts can run; Node.js version blocked on DEL-01-03 | HIGH |
| DEP-07-03-007 | PREREQUISITE | DELIVERABLE | DEL-03-07 (Harness API Baseline) | API route surfaces (/session/list, /session/*, /turn, /interrupt) must be functional for validation | HIGH |
| DEP-07-03-008 | INTERFACE | DOCUMENT | docs/harness/harness_manual_validation.md | Canonical reference for Section 8 matrix, script locations, outputs, local-only boundary | HIGH |
| DEP-07-03-009 | INTERFACE | DOCUMENT | docs/harness/harness_ci_integration.md | Canonical reference for CI workflow, job flow, failure expectations | HIGH |
| DEP-07-03-010 | INTERFACE | DOCUMENT | docs/harness/harness_artifact_mirroring_guidance.md | Canonical reference for artifact mirroring posture and guardrails | HIGH |
| DEP-07-03-016 | CONSTRAINT | EXTERNAL | Anthropic API Key (OI-001) | Live validation requires ANTHROPIC_API_KEY; provisioning contract unresolved; structural validation can proceed without it | HIGH |
| DEP-07-03-017 | INTERFACE | DOCUMENT | docs/PLAN.md Section 2 FE-4 | Existing tooling context and frontend validation acceptance criteria informing scope | MEDIUM |

### EXECUTION edges -- DOWNSTREAM (5 ACTIVE)

| DependencyID | DependencyType | TargetType | Target | Statement (summary) | Confidence |
|---|---|---|---|---|---|
| DEP-07-03-011 | HANDOVER | DELIVERABLE | DEL-07-01 (Harness Validation Suite) | Produces Section 8 validation posture and shared regression checks consumed by DEL-07-01 | HIGH |
| DEP-07-03-012 | ENABLES | DELIVERABLE | DEL-01-01 (macOS Build Baseline) | Pre-tier gate: DEL-01-01 blocked until DEL-07-03 reaches IN_PROGRESS | HIGH |
| DEP-07-03-013 | ENABLES | DELIVERABLE | DEL-03-01 (Working Root Session Boot) | Pre-tier gate: DEL-03-01 blocked until DEL-07-03 reaches IN_PROGRESS | HIGH |
| DEP-07-03-014 | ENABLES | DELIVERABLE | DEL-05-03 (Lifecycle State Handling) | Pre-tier gate: DEL-05-03 blocked until DEL-07-03 reaches IN_PROGRESS | HIGH |
| DEP-07-03-015 | ENABLES | DELIVERABLE | DEL-05-04 (Dependency Tracking Contract) | Pre-tier gate: DEL-05-04 blocked until DEL-07-03 reaches IN_PROGRESS | HIGH |

## Run Notes

- **Run date:** 2026-02-22 (UPDATE run 2 -- re-extraction from enriched production docs post Pass 3 semantic lensing)
- **MODE:** UPDATE
- **STRICTNESS:** CONSERVATIVE
- **CONSUMER_CONTEXT:** NONE
- **DECOMPOSITION_PATH:** `execution/_Decomposition/ChiralityApp_SoftwareDecomposition_2026-02-21_G7-APPROVED.md` (found, SCA-001 amendment present)
- **ANCHOR_DOC:** `Datasheet.md` (selected by heuristic: filename contains "datasheet")
- **EXECUTION_DOC_ORDER:** `Procedure.md`, `Specification.md`, `Guidance.md`
- **SOURCE_DOCS scanned:** `Datasheet.md`, `Specification.md`, `Guidance.md`, `Procedure.md`, `_CONTEXT.md`, `_REFERENCES.md`
- **_REFERENCES.md:** read; used to confirm document paths for DOCUMENT-type targets
- **Decomposition status:** validated; DEL-07-03 confirmed in PKG-07 covering SOW-048/SOW-049 supporting OBJ-006/OBJ-008
- **Parent anchor:** 1 IMPLEMENTS_NODE (PKG-07) -- no warnings
- **Defaults applied:** SOURCE_DOCS=AUTO, DOC_ROLE_MAP=DEFAULT, ANCHOR_DOC=AUTO, EXECUTION_DOC_ORDER=AUTO
- **Warnings:** None
- **Changes from prior run:**
  - DEP-07-03-007 Statement updated: enriched Procedure PR-09 now explicitly includes `/api/harness/interrupt` endpoint in the route surface list (previously only `/api/harness/session/*` and `/api/harness/turn`)
  - DEP-07-03-016 (NEW): UPSTREAM CONSTRAINT from EXTERNAL -- Anthropic API key required for live validation; Procedure PR-05 explicitly requires it; Guidance C3 distinguishes structural vs live validation modes
  - DEP-07-03-017 (NEW): UPSTREAM INTERFACE from DOCUMENT -- docs/PLAN.md Section 2 FE-4; Datasheet R4 explicitly cites it; Specification Standards table references it; provides contextual scope input
  - All existing rows (001-015): Notes fields enriched with additional cross-references found in Pass 3 enriched production documents; no semantic changes to dependency relationships
- **Notes on TargetLocation for DELIVERABLE targets:** Paths are best-effort based on naming conventions; deliverable folders for SCA-001 deliverables (DEL-01-03, DEL-02-05, DEL-03-07) may not yet exist
- **Notes on DEL-07-02 (not extracted):** Datasheet R8 references DEL-07-02 as "conformance fixtures that may be consumed by validation." Under CONSERVATIVE strictness, the hedged "may be consumed" language without a concrete prerequisite or interface statement in any Specification requirement or Procedure step does not meet the information-flow threshold. Not extracted; revisit if future enrichment establishes a concrete data transfer.

## Run History

| Timestamp | Mode | Strictness | Decomposition | Warnings | ACTIVE Rows |
|---|---|---|---|---|---|
| 2026-02-22 | UPDATE | CONSERVATIVE | G7-APPROVED + SCA-001 (found) | None | 15 (5 ANCHOR + 10 EXECUTION) |
| 2026-02-22 | UPDATE | CONSERVATIVE | G7-APPROVED + SCA-001 (found) | None | 17 (5 ANCHOR + 12 EXECUTION) |

## Lifecycle Summary

- **ACTIVE:** 17
- **RETIRED:** 0
- **Closure breakdown:**
  - `TBD`: 11 (5 ANCHOR + 4 DOWNSTREAM ENABLES + 1 DOWNSTREAM HANDOVER + 1 UPSTREAM CONSTRAINT [API key])
  - `PENDING`: 2 (DEP-07-03-006 DEL-01-03 prerequisite, DEP-07-03-007 DEL-03-07 prerequisite)
  - `SATISFIED`: 4 (DEP-07-03-008/009/010 -- docs/harness/* documents; DEP-07-03-017 -- docs/PLAN.md)

## Consumer Handoff Notes (optional)
- CONSUMER_CONTEXT=NONE; no consumer-specific annotations produced.
