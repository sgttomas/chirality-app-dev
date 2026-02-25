# Dependencies -- DEL-03-05

**Tracking Mode:** FULL_GRAPH
**Status:** EXTRACTED
**RegisterSchemaVersion:** v3.1

## Declared Upstream Dependencies

*No human-declared upstream dependencies. See Extracted Dependency Register below.*

## Declared Downstream Dependencies

*No human-declared downstream dependencies. See Extracted Dependency Register below.*

---

## Extracted Dependency Register

**Total ACTIVE rows:** 13
**Total RETIRED rows:** 0

### ANCHOR rows (3 ACTIVE)

| DependencyID | AnchorType | TargetRefID | TargetName | Confidence |
|---|---|---|---|---|
| DEP-03-05-001 | IMPLEMENTS_NODE | SOW-006 | SOW-006 -- Harness runtime responsibilities | HIGH |
| DEP-03-05-002 | TRACES_TO_REQUIREMENT | OBJ-002 | OBJ-002 -- Harness runtime correctness + Anthropic-only network | HIGH |
| DEP-03-05-003 | TRACES_TO_REQUIREMENT | DEC-NET-001 | DEC-NET-001 -- Anthropic-only outbound network | HIGH |

### EXECUTION rows (10 ACTIVE)

| DependencyID | Direction | DependencyType | TargetType | TargetDeliverableID / TargetRefID | TargetName | Confidence |
|---|---|---|---|---|---|---|
| DEP-03-05-004 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-03-02 | Turn Execution API + SSE Streaming | HIGH |
| DEP-03-05-005 | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-03-03 | Turn Options Mapping & Fallback Chains | HIGH |
| DEP-03-05-006 | DOWNSTREAM | INTERFACE | DELIVERABLE | DEL-03-06 | Outbound Network Guardrails (Anthropic-only) | HIGH |
| DEP-03-05-007 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-04-01 | Attachment Resolver + Prompt Mode Selection | HIGH |
| DEP-03-05-008 | UPSTREAM | CONSTRAINT | EXTERNAL | OI-001 | API key provisioning policy decision | HIGH |
| DEP-03-05-009 | UPSTREAM | PREREQUISITE | EXTERNAL | ANTHROPIC-API-DOCS | Anthropic API Documentation | MEDIUM |
| DEP-03-05-010 | UPSTREAM | PREREQUISITE | EXTERNAL | ANTHROPIC-SDK | Anthropic Claude SDK (Node.js/TypeScript) | MEDIUM |
| DEP-03-05-011 | UPSTREAM | CONSTRAINT | DOCUMENT | DIRECTIVE-2.5 | DIRECTIVE Section 2.5 -- Non-authoritative convenience state | HIGH |
| DEP-03-05-012 | UPSTREAM | CONSTRAINT | DOCUMENT | SPEC-9.8 | SPEC Section 9.8 -- Harness turn input contract | HIGH |
| DEP-03-05-013 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-02-06 | Settings / API Key Entry UI | HIGH |

---

## Lifecycle Summary

| Status | Count |
|--------|-------|
| ACTIVE | 13 |
| RETIRED | 0 |

| SatisfactionStatus | Count |
|--------------------|-------|
| TBD | 6 |
| PENDING | 3 |
| IN_PROGRESS | 0 |
| SATISFIED | 3 |
| WAIVED | 0 |
| NOT_APPLICABLE | 1 |

| DependencyClass | Count |
|-----------------|-------|
| ANCHOR | 3 |
| EXECUTION | 10 |

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
- **SOURCE_DOCS (AUTO):** Datasheet.md, Specification.md, Guidance.md, Procedure.md, _CONTEXT.md, _REFERENCES.md
- **ANCHOR_DOC (AUTO):** Datasheet.md (selected: contains Identification fields with Scope Coverage, Objectives, and traceability attributes)
- **EXECUTION_DOC_ORDER (AUTO):** Procedure.md, Specification.md, Guidance.md, Datasheet.md, _CONTEXT.md

### Decomposition validation

- Decomposition file found and read successfully.
- DEL-03-05 confirmed in decomposition under PKG-03 with CoversScopeItems=SOW-006, SupportsObjectives=OBJ-002.
- SOW-006 confirmed in Scope Ledger (InOutStatus=IN, PackageID=PKG-03, DeliverableIDs=DEL-03-02/DEL-03-05/DEL-03-06).
- OBJ-002 confirmed in Objectives section.
- DEC-NET-001 confirmed in Decision Log.
- All target deliverable IDs (DEL-03-02, DEL-03-03, DEL-03-06, DEL-04-01, DEL-02-06) confirmed in decomposition Deliverables tables.
- OI-001 confirmed in Open Issues table (Type=POLICY_DECISION).

### Extraction decisions

- **ANCHOR parent (IMPLEMENTS_NODE):** SOW-006 selected as the primary scope item anchor. The Datasheet explicitly lists `Scope Coverage: SOW-006`. Although the deliverable also traces to OBJ-002 and DEC-NET-001, SOW-006 is the direct scope coverage anchor. One parent anchor emitted.
- **ANCHOR traces:** OBJ-002 (objective) and DEC-NET-001 (binding decision) both explicitly stated in sources and confirmed in decomposition.
- **DEL-03-02 and DEL-03-03:** Listed as prerequisites in Procedure Prerequisites table. `DEP-03-05-004` remains reclassified to `INTERFACE` by human ruling (2026-02-22); `DEP-03-05-005` remains `PREREQUISITE`.
- **DEL-03-06:** Classified as DOWNSTREAM INTERFACE. DEL-03-05 produces the provider; DEL-03-06 inspects/verifies it. The information flow is FROM DEL-03-05 TO DEL-03-06.
- **DEL-04-01:** Classified as UPSTREAM INTERFACE. Specification REQ-05 explicitly states content blocks flow from DEL-04-01 to DEL-03-05.
- **OI-001:** Classified as UPSTREAM CONSTRAINT (EXTERNAL). Human ruling on 2026-02-23 was amended by SCA-003 on 2026-02-24 to `ENV+UI`; dependency remains traceable with `SatisfactionStatus=SATISFIED`.
- **Anthropic API docs and SDK:** Both listed as explicit prerequisites in Procedure and Specification Standards. Classified as EXTERNAL PREREQUISITE. Location TBD for both.
- **DIRECTIVE 2.5 and SPEC 9.8:** Both referenced as mandatory compliance constraints in Specification requirements. Classified as DOCUMENT CONSTRAINT.
- **DEL-02-06:** Classified as UPSTREAM INTERFACE. DEL-03-05 consumes UI-provided key convenience state from DEL-02-06 when present and falls back to `ANTHROPIC_API_KEY` when absent.

### Integrity check results

- Parent anchor check: 1 ACTIVE row with DependencyClass=ANCHOR, AnchorType=IMPLEMENTS_NODE. PASS.
- DependencyID uniqueness: All 13 IDs unique. PASS.
- Schema completeness: All required columns present. PASS.
- Evidence coverage: All ACTIVE rows have EvidenceFile and SourceRef. PASS.
- No invented targets: All target IDs confirmed in decomposition or marked EXTERNAL. PASS.
- Enum normalization: All values use canonical write-form enums. PASS.

### Warnings

- `DEP-03-05-005` refreshed to `SatisfactionStatus=SATISFIED` with `RequiredMaturity=IN_PROGRESS` after upstream deliverable `DEL-03-03` reached lifecycle `IN_PROGRESS`.
- `DEP-03-05-008` refreshed to reflect SCA-003 amendment (`ENV_ONLY -> ENV+UI`) while preserving `SatisfactionStatus=SATISFIED`.
- `DEP-03-05-010` refreshed to `SatisfactionStatus=SATISFIED` after SDK-path implementation landed (`@anthropic-ai/sdk@0.78.0`) under the `ADOPT_SDK_NOW` ruling.
- `DEP-03-05-013` added to capture UI key-entry interface from DEL-02-06 into DEL-03-05 runtime key resolution contract.
- DEL-03-05 four-document set still contains pre-amendment `ENV_ONLY` wording and requires a follow-on implementation/document alignment pass under the new SCA-003 contract.

---

## Run History

| RunDate | Mode | Strictness | DecompositionStatus | Warnings | ActiveAnchors | ActiveExecution | ActiveTotal |
|---------|------|------------|---------------------|----------|---------------|-----------------|-------------|
| 2026-02-24 (SCA-003 re-extraction) | UPDATE | CONSERVATIVE | FOUND (G7-APPROVED + SCA-001 + SCA-002 + SCA-003) | OI-001 resolution amended to ENV+UI; added DEL-02-06 interface row DEP-03-05-013 | 3 | 10 | 13 |
| 2026-02-23 (Tier 5 PASS3 SDK implementation) | UPDATE | CONSERVATIVE | FOUND (G7-APPROVED) | Dependency refresh (`DEP-03-05-010` SDK prerequisite closure after implementation pin) | 3 | 9 | 12 |
| 2026-02-23 | UPDATE | CONSERVATIVE | FOUND (G7-APPROVED) | Dependency refresh (`DEP-03-05-005` maturity closure + `DEP-03-05-008` OI-001 ruling closure + `DEP-03-05-010` SDK-path pending) | 3 | 9 | 12 |
| 2026-02-21 | UPDATE | CONSERVATIVE | FOUND (G7-APPROVED) | None | 3 | 9 | 12 |

---

## Downstream Handoff Notes

*CONSUMER_CONTEXT is NONE. No downstream handoff notes generated.*
