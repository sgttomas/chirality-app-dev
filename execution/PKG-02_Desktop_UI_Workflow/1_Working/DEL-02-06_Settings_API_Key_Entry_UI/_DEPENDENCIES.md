# Dependencies -- DEL-02-06

**Tracking Mode:** FULL_GRAPH
**Status:** EXTRACTED
**RegisterSchemaVersion:** v3.1

## Declared Upstream Dependencies

*No human-declared upstream dependencies. See Extracted Dependency Register below.*

## Declared Downstream Dependencies

*No human-declared downstream dependencies. See Extracted Dependency Register below.*

---

## Extracted Dependency Register

**Total ACTIVE rows:** 5
**Total RETIRED rows:** 0

### ANCHOR rows (2 ACTIVE)

| DependencyID | AnchorType | TargetRefID | TargetName | Confidence |
|---|---|---|---|---|
| DEP-02-06-001 | IMPLEMENTS_NODE | SOW-050 | SOW-050 -- UI API key entry + local secure storage | HIGH |
| DEP-02-06-002 | TRACES_TO_REQUIREMENT | OBJ-005 | OBJ-005 -- Desktop UI supports intended operator workflow | HIGH |

### EXECUTION rows (3 ACTIVE)

| DependencyID | Direction | DependencyType | TargetType | TargetDeliverableID / TargetRefID | TargetName | Confidence |
|---|---|---|---|---|---|---|
| DEP-02-06-003 | DOWNSTREAM | INTERFACE | DELIVERABLE | DEL-03-05 | Anthropic Provider Integration & Key Provisioning Contract | HIGH |
| DEP-02-06-004 | UPSTREAM | CONSTRAINT | DOCUMENT | DIRECTIVE-2.5 | DIRECTIVE Section 2.5 -- Non-authoritative convenience state | HIGH |
| DEP-02-06-005 | UPSTREAM | CONSTRAINT | DOCUMENT | SPEC-9.8 | SPEC Section 9.8 -- Harness turn/provider contract | HIGH |

---

## Lifecycle Summary

| Status | Count |
|--------|-------|
| ACTIVE | 5 |
| RETIRED | 0 |

| SatisfactionStatus | Count |
|--------------------|-------|
| TBD | 4 |
| PENDING | 1 |
| IN_PROGRESS | 0 |
| SATISFIED | 0 |
| WAIVED | 0 |
| NOT_APPLICABLE | 0 |

| DependencyClass | Count |
|-----------------|-------|
| ANCHOR | 2 |
| EXECUTION | 3 |

---

## Run Notes

**Run date:** 2026-02-24
**MODE:** UPDATE
**STRICTNESS:** CONSERVATIVE
**CONSUMER_CONTEXT:** NONE

### Defaults and paths used

- **RUN_ROOT:** `/Users/ryan/ai-env/projects/chirality-app-dev/execution/`
- **DECOMPOSITION_PATH:** `/Users/ryan/ai-env/projects/chirality-app-dev/execution/_Decomposition/ChiralityApp_SoftwareDecomposition_2026-02-21_G7-APPROVED.md`
- **DECOMP_VARIANT:** SOFTWARE
- **SOURCE_DOCS (AUTO):** _CONTEXT.md, _REFERENCES.md
- **ANCHOR_DOC (AUTO):** _CONTEXT.md
- **EXECUTION_DOC_ORDER (AUTO):** _REFERENCES.md, _CONTEXT.md

### Decomposition validation

- Decomposition file found and read successfully.
- DEL-02-06 confirmed in decomposition Scope Amendment A3 under PKG-02.
- SOW-050 confirmed in Scope Amendment A3 scope-item table and scope-ledger overlay.
- Target deliverable DEL-03-05 confirmed in decomposition deliverables/open-issue amendment context.

### Extraction decisions

- **ANCHOR parent (IMPLEMENTS_NODE):** SOW-050 selected as primary scope anchor from DEL-02-06 context scope coverage.
- **ANCHOR trace:** OBJ-005 selected as objective trace from DEL-02-06 context objective mapping.
- **DEL-03-05:** Classified as DOWNSTREAM INTERFACE because DEL-02-06 provides UI key-entry/state interface consumed by runtime provider policy.
- **DIRECTIVE 2.5 and SPEC 9.8:** Classified as UPSTREAM DOCUMENT CONSTRAINT rows from deliverable references and amended policy contract.

### Integrity check results

- Parent anchor check: 1 ACTIVE row with DependencyClass=ANCHOR and AnchorType=IMPLEMENTS_NODE. PASS.
- DependencyID uniqueness: All 5 IDs unique. PASS.
- Schema completeness: All required columns present. PASS.
- Evidence coverage: All ACTIVE rows have EvidenceFile and SourceRef. PASS.
- No invented targets: all target IDs/refs confirmed in decomposition or references. PASS.

### Warnings

- New deliverable scaffold has no implementation docs yet (4_DOCUMENTS not yet run); dependency evidence currently derives from context/reference metadata only.

---

## Run History

| RunDate | Mode | Strictness | DecompositionStatus | Warnings | ActiveAnchors | ActiveExecution | ActiveTotal |
|---------|------|------------|---------------------|----------|---------------|-----------------|-------------|
| 2026-02-24 (SCA-003 initial extraction) | UPDATE | CONSERVATIVE | FOUND (G7-APPROVED + SCA-001 + SCA-002 + SCA-003) | Metadata-only evidence base pending 4_DOCUMENTS | 2 | 3 | 5 |

---

## Downstream Handoff Notes

*CONSUMER_CONTEXT is NONE. No downstream handoff notes generated.*
