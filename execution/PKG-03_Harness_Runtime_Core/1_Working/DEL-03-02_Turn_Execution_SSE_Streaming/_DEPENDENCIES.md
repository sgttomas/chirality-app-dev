# Dependencies -- DEL-03-02

**Tracking Mode:** FULL_GRAPH
**Status:** EXTRACTED

---

## Declared Upstream Dependencies

*No declared (human-authored) upstream dependencies. See Extracted Dependency Register below.*

## Declared Downstream Dependencies

*No declared (human-authored) downstream dependencies. See Extracted Dependency Register below.*

---

## Extracted Dependency Register

**Schema Version:** v3.1
**Total ACTIVE rows:** 14
**Total RETIRED rows:** 0

### ANCHOR rows (7 ACTIVE)

| DependencyID | AnchorType | TargetType | TargetRefID / TargetName | Confidence | Status |
|---|---|---|---|---|---|
| DEP-03-02-001 | IMPLEMENTS_NODE | WBS_NODE | PKG-03 Harness Runtime Core | HIGH | ACTIVE |
| DEP-03-02-002 | TRACES_TO_REQUIREMENT | REQUIREMENT | SOW-004 | HIGH | ACTIVE |
| DEP-03-02-003 | TRACES_TO_REQUIREMENT | REQUIREMENT | SOW-005 | HIGH | ACTIVE |
| DEP-03-02-004 | TRACES_TO_REQUIREMENT | REQUIREMENT | SOW-006 | HIGH | ACTIVE |
| DEP-03-02-005 | TRACES_TO_REQUIREMENT | REQUIREMENT | OBJ-002 | HIGH | ACTIVE |
| DEP-03-02-013 | TRACES_TO_REQUIREMENT | REQUIREMENT | DEC-NET-001 | HIGH | ACTIVE |
| DEP-03-02-014 | TRACES_TO_REQUIREMENT | REQUIREMENT | DEC-PLAT-001 | HIGH | ACTIVE |

### EXECUTION rows (7 ACTIVE)

| DependencyID | Direction | DependencyType | TargetDeliverableID | TargetName | Confidence | Status |
|---|---|---|---|---|---|---|
| DEP-03-02-006 | UPSTREAM | PREREQUISITE | DEL-03-01 | Working Root Binding & Session Boot | HIGH | ACTIVE |
| DEP-03-02-007 | UPSTREAM | INTERFACE | DEL-03-03 | Turn Options Mapping & Fallback Chains | HIGH | ACTIVE |
| DEP-03-02-008 | UPSTREAM | INTERFACE | DEL-03-04 | Subagent Governance Fail-Closed Enforcement | HIGH | ACTIVE |
| DEP-03-02-009 | UPSTREAM | PREREQUISITE | DEL-03-05 | Anthropic Provider Integration & Key Provisioning Contract | HIGH | ACTIVE |
| DEP-03-02-010 | UPSTREAM | INTERFACE | DEL-04-01 | Server-side Attachment Resolver + Prompt Mode Selection | HIGH | ACTIVE |
| DEP-03-02-011 | UPSTREAM | CONSTRAINT | DEL-03-06 | Outbound Network Guardrails (Anthropic-only) + Verification | MEDIUM | ACTIVE |
| DEP-03-02-012 | DOWNSTREAM | HANDOVER | DEL-04-02 | UI Attachment Pipeline (Picker Preview Rollback Rehydration) | MEDIUM | ACTIVE |

---

## Run Notes

### Defaults and Paths Used

| Setting | Value |
|---|---|
| MODE | UPDATE |
| STRICTNESS | CONSERVATIVE |
| CONSUMER_CONTEXT | NONE |
| DECOMP_VARIANT | SOFTWARE |
| DECOMPOSITION_PATH | `execution/_Decomposition/ChiralityApp_SoftwareDecomposition_2026-02-21_G7-APPROVED.md` |
| SOURCE_DOCS | AUTO (all docs in deliverable folder) |
| ANCHOR_DOC | Datasheet.md (selected: contains Identification table with scope items, objectives, and package) |
| EXECUTION_DOC_ORDER | Specification.md, Guidance.md, Procedure.md (heuristic: specification first for normative requirements, then guidance for directional context, then procedure for prerequisites) |

### Assumptions and Warnings

- No warnings. Decomposition document located and used for validation.
- Parent anchor (IMPLEMENTS_NODE) resolved to PKG-03 Harness Runtime Core -- confirmed in decomposition deliverable table.
- All target deliverable IDs (DEL-03-01, DEL-03-03, DEL-03-04, DEL-03-05, DEL-03-06, DEL-04-01, DEL-04-02) confirmed to exist in the decomposition.
- OBJ-002 mapping noted as ASSUMPTION in the Datasheet (best-effort mapping via PKG-03 grouping); recorded as-is with HIGH confidence because the decomposition confirms the linkage.
- DEP-03-02-012 (DOWNSTREAM HANDOVER to DEL-04-02) marked IMPLICIT / MEDIUM confidence: the SSE stream is consumed by UI components, but the explicit handover contract is not fully specified in sources.
- DEC-NET-001 and DEC-PLAT-001 traced as requirement-class anchors because both are explicitly cited as conditions/constraints in the Datasheet and confirmed in the decomposition Decision Log.

---

## Run History

| Timestamp | Mode | Strictness | Decomposition | Warnings | ACTIVE Anchors | ACTIVE Execution | Total ACTIVE |
|---|---|---|---|---|---|---|---|
| 2026-02-21 | UPDATE | CONSERVATIVE | G7-APPROVED (located) | None | 7 | 7 | 14 |

---

## Lifecycle Summary

| Lifecycle State | Count |
|---|---|
| ACTIVE | 14 |
| RETIRED | 0 |

### Closure State Breakdown (ACTIVE rows)

| SatisfactionStatus | Count |
|---|---|
| TBD | 8 |
| PENDING | 6 |

**Note:** ANCHOR rows have SatisfactionStatus=TBD (traceability anchors; closure not applicable in the same sense as execution dependencies). EXECUTION UPSTREAM rows have SatisfactionStatus=PENDING (dependencies exist but prerequisite deliverables are not yet complete). EXECUTION DOWNSTREAM row (DEP-03-02-012) has SatisfactionStatus=TBD (handover contract not fully specified).
