# Dependencies -- DEL-08-01

**DeliverableID:** DEL-08-01
**Name:** `_REFERENCES.md` Content Hashes + Verification
**PackageID:** PKG-08
**Tracking Mode:** FULL_GRAPH
**Status:** EXTRACTED

---

## Declared Upstream Dependencies

*No human-declared upstream dependencies at this time. See Extracted Dependency Register below.*

## Declared Downstream Dependencies

*No human-declared downstream dependencies at this time. See Extracted Dependency Register below.*

---

## Extracted Dependency Register

**Schema Version:** v3.1
**Total Rows:** 12
**ACTIVE:** 12
**RETIRED:** 0

### ANCHOR Rows (5 ACTIVE)

| DependencyID | AnchorType | TargetType | TargetRefID / TargetName | Confidence | Notes |
|---|---|---|---|---|---|
| DEP-08-01-001 | IMPLEMENTS_NODE | WBS_NODE | SOW-032 | HIGH | Parent scope anchor. SOW-032 status = TBD (OI-032). |
| DEP-08-01-002 | TRACES_TO_REQUIREMENT | REQUIREMENT | OBJ-007 | MEDIUM | Objective trace. ASSUMPTION -- best-effort mapping via PKG-08. |
| DEP-08-01-003 | TRACES_TO_REQUIREMENT | REQUIREMENT | K-GHOST-1 | HIGH | No-ghost-input invariant alignment. |
| DEP-08-01-004 | TRACES_TO_REQUIREMENT | REQUIREMENT | K-PROV-1 | HIGH | Provenance invariant alignment. |
| DEP-08-01-005 | TRACES_TO_REQUIREMENT | REQUIREMENT | K-VAL-1 | HIGH | Dirty detection invariant alignment. |

### EXECUTION Rows (7 ACTIVE)

| DependencyID | Direction | DependencyType | TargetType | Target | Confidence | Notes |
|---|---|---|---|---|---|---|
| DEP-08-01-006 | UPSTREAM | CONSTRAINT | WBS_NODE | SOW-032 Scope Activation | HIGH | Scope gate: SOW-032 must be flipped IN (OI-032). |
| DEP-08-01-007 | UPSTREAM | PREREQUISITE | DOCUMENT | docs/SPEC.md Section 7 | HIGH | Current _REFERENCES.md format spec required for schema extension. |
| DEP-08-01-008 | UPSTREAM | PREREQUISITE | DOCUMENT | docs/CONTRACT.md (K-GHOST-1 / K-PROV-1 / K-VAL-1) | HIGH | Invariant understanding required for alignment verification. |
| DEP-08-01-009 | UPSTREAM | PREREQUISITE | DOCUMENT | docs/PLAN.md Section 3.1 | HIGH | Feature description, rationale, integration points. |
| DEP-08-01-010 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-06-02 (Local Deliverable Workflow Agents) | HIGH | PREPARATION + ORCHESTRATOR integration for hash compute/verify. |
| DEP-08-01-011 | DOWNSTREAM | HANDOVER | DELIVERABLE | DEL-08-07 (Staleness Propagation + Triage Tooling) | HIGH | Hash verification output consumed by DEL-08-07. |
| DEP-08-01-012 | UPSTREAM | CONSTRAINT | EXTERNAL | FIPS 180-4 (NIST SHA-256) | LOW | Algorithm standard; location TBD; standard library proxy accepted. |

---

## Lifecycle Summary

| Category | Count |
|---|---|
| **Total Rows** | 12 |
| **ACTIVE** | 12 |
| **RETIRED** | 0 |

### By DependencyClass

| DependencyClass | ACTIVE | RETIRED |
|---|---|---|
| ANCHOR | 5 | 0 |
| EXECUTION | 7 | 0 |

### By SatisfactionStatus (ACTIVE rows)

| SatisfactionStatus | Count |
|---|---|
| TBD | 10 |
| PENDING | 1 |
| NOT_APPLICABLE | 1 |

### Closure Notes

- DEP-08-01-006 (SOW-032 Scope Activation) is marked PENDING because the scope decision is an outstanding open issue (OI-032).
- DEP-08-01-012 (FIPS 180-4) is marked NOT_APPLICABLE because standard library implementations serve as the accepted compliance proxy (no separate satisfaction action needed).
- All other rows are TBD pending implementation phase.

---

## Run Notes

**Run Date:** 2026-02-21
**Mode:** UPDATE
**Strictness:** CONSERVATIVE
**Consumer Context:** NONE
**Decomposition Path:** `/Users/ryan/ai-env/projects/chirality-app-dev/execution/_Decomposition/ChiralityApp_SoftwareDecomposition_2026-02-21_G7-APPROVED.md`
**Decomposition Status:** Available (G7-APPROVED). Anchor validation and label resolution performed successfully.

### Defaults Used

- **SOURCE_DOCS:** AUTO -- scanned deliverable folder; found: Datasheet.md, Specification.md, Guidance.md, Procedure.md, _CONTEXT.md, _REFERENCES.md
- **ANCHOR_DOC:** Datasheet.md (selected: contains Identification table with Scope Coverage, Objectives, and Conditions)
- **EXECUTION_DOC_ORDER:** Procedure.md, Specification.md, Guidance.md (ordered by workflow signal density)
- **DOC_ROLE_MAP:** DEFAULT heuristic applied

### Assumptions Recorded

1. OBJ-007 mapping is best-effort via PKG-08 package grouping (source: Datasheet, confirmed by Decomposition).
2. DEL-08-07 interface for hash verification output is not yet defined (source: Guidance C4, Specification Verification table).
3. FIPS 180-4 compliance via standard library implementations is the accepted approach (source: Guidance C7).

### Warnings

*None.*

### Integrity Check Results

- **Parent anchor check:** 1 ACTIVE IMPLEMENTS_NODE row found (DEP-08-01-001 -> SOW-032). PASS.
- **Schema check:** All required columns present. PASS.
- **Evidence check:** All ACTIVE rows have EvidenceFile and SourceRef populated. PASS.
- **DependencyID uniqueness:** All 12 IDs unique. PASS.
- **Enum normalization:** All values use canonical write-form enums. PASS.
- **_DEPENDENCIES.md consistency:** Summary counts match Dependencies.csv. PASS.

---

## Run History

| RunTimestamp | Mode | Strictness | DecompositionStatus | Warnings | ActiveCount | RetiredCount |
|---|---|---|---|---|---|---|
| 2026-02-21 | UPDATE | CONSERVATIVE | Available (G7-APPROVED) | None | 12 | 0 |
