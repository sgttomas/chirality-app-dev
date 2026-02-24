# Dependencies -- DEL-07-01 Harness Validation Suite

**Tracking Mode:** FULL_GRAPH
**Status:** EXTRACTED
**RegisterSchemaVersion:** v3.1

---

## Declared Upstream Dependencies

*No declared (human-authored) upstream dependencies yet. All current upstream edges are extracted.*

## Declared Downstream Dependencies

*No declared (human-authored) downstream dependencies yet.*

---

## Extracted Dependency Register

**Total rows:** 15
**ACTIVE:** 15 | **RETIRED:** 0
**Last Run:** 2026-02-24 (UPDATE fan-in refresh, no edge deltas)

### ANCHOR Rows (4 ACTIVE)

| DependencyID | AnchorType | TargetType | TargetRefID | TargetName | Confidence |
|---|---|---|---|---|---|
| DEP-07-01-001 | IMPLEMENTS_NODE | WBS_NODE | SOW-028 | Provide repeatable harness validation scripts and docs suitable for local + CI validation gates | HIGH |
| DEP-07-01-002 | IMPLEMENTS_NODE | WBS_NODE | OBJ-006 | Validation posture and governance/agent-suite conformance enable repeatable operation | HIGH |
| DEP-07-01-003 | TRACES_TO_REQUIREMENT | REQUIREMENT | DEC-PLAT-001 | Target platform = macOS 15+ Apple Silicon only | HIGH |
| DEP-07-01-004 | TRACES_TO_REQUIREMENT | REQUIREMENT | DEC-NET-001 | Outbound internet access permitted only for Anthropic API calls | HIGH |

### EXECUTION Rows (11 ACTIVE)

| DependencyID | Direction | DependencyType | TargetType | Target | Confidence |
|---|---|---|---|---|---|
| DEP-07-01-005 | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-03-01 Working Root Binding & Session Boot | HIGH |
| DEP-07-01-006 | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-03-02 Turn Execution API + SSE Streaming | HIGH |
| DEP-07-01-007 | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-03-03 Turn Options Mapping & Fallback Chains | HIGH |
| DEP-07-01-008 | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-03-04 Subagent Governance Fail-Closed Enforcement | HIGH |
| DEP-07-01-009 | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-03-05 Anthropic Provider Integration & Key Provisioning Contract | HIGH |
| DEP-07-01-010 | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-03-06 Outbound Network Guardrails (Anthropic-only) + Verification | MEDIUM |
| DEP-07-01-011 | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-04-01 Server-side Attachment Resolver + Prompt Mode Selection | HIGH |
| DEP-07-01-012 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-07-02 Example Execution Roots + Conformance Fixtures | MEDIUM |
| DEP-07-01-013 | UPSTREAM | PREREQUISITE | DOCUMENT | docs/SPEC.md (Sections 9.7-9.8) | HIGH |
| DEP-07-01-014 | UPSTREAM | INTERFACE | DOCUMENT | docs/CONTRACT.md (K-invariants) | HIGH |
| DEP-07-01-015 | UPSTREAM | CONSTRAINT | PACKAGE | PKG-03 Harness Runtime Core (co-evolution trigger) | MEDIUM |

---

## Lifecycle Summary

| Status | Count |
|--------|-------|
| ACTIVE | 15 |
| RETIRED | 0 |

| SatisfactionStatus | Count |
|--------------------|-------|
| TBD | 15 |

| DependencyClass | Count |
|-----------------|-------|
| ANCHOR | 4 |
| EXECUTION | 11 |

| Confidence | Count |
|------------|-------|
| HIGH | 12 |
| MEDIUM | 3 |
| LOW | 0 |

---

## Run Notes

### Defaults Used
- **MODE:** UPDATE
- **STRICTNESS:** CONSERVATIVE
- **CONSUMER_CONTEXT:** NONE
- **SOURCE_DOCS:** AUTO -- scanned deliverable folder; identified Datasheet.md, Specification.md, Guidance.md, Procedure.md, _CONTEXT.md, _REFERENCES.md
- **ANCHOR_DOC:** Datasheet.md (selected: contains Identification table with Scope Coverage, Objective, and decomposition references)
- **EXECUTION_DOC_ORDER:** Procedure.md, Guidance.md, Specification.md (Procedure has explicit prerequisites; Guidance has considerations with named deliverables; Specification has excluded-scope boundaries and requirement traces)
- **DECOMPOSITION_PATH:** `/Users/ryan/ai-env/projects/chirality-app-dev/execution/_Decomposition/ChiralityApp_SoftwareDecomposition_2026-02-21_G7-APPROVED.md`
- **DECOMPOSITION_STATUS:** Available and read successfully. G7-APPROVED revision. All target IDs validated against decomposition.

### Warnings

- [WARNING] AMBIGUOUS_ANCHOR: Two IMPLEMENTS_NODE rows found (DEP-07-01-001 for SOW-028 and DEP-07-01-002 for OBJ-006). Both are explicitly stated in the Datasheet Identification table. SOW-028 is the scope coverage item; OBJ-006 is the supported objective. Both are distinct definition-node types (scope item vs. objective). Downstream consumers should treat SOW-028 as the primary scope anchor and OBJ-006 as the objective anchor. This is a legitimate dual-anchor pattern for software decompositions where scope items and objectives are tracked separately.

### Assumptions Logged
- DEP-07-01-010 (DEL-03-06): Confidence MEDIUM because the relationship is more about test infrastructure compliance than direct behavioral prerequisite. Procedure PR-08 lists DEL-03-06 in the range DEL-03-01 through DEL-03-06.
- DEP-07-01-012 (DEL-07-02): Confidence MEDIUM because Guidance C6 uses conditional language ("may consume") rather than mandatory language.
- DEP-07-01-015 (PKG-03 constraint): Classified as ASSUMPTION because Guidance C7 describes a co-evolution maintenance concern rather than a hard build-time gate.

### Extraction Decisions
- **Scope boundary exclusions not registered as dependencies:** Specification Excluded section names DEL-06-05 and DEL-06-01 as covering out-of-scope testing areas. These are scope boundaries (what this deliverable does NOT test), not information-flow edges. Not extracted.
- **PR-03 (Repository cloned and buildable) not registered:** This is a general environmental prerequisite (SOW-001 / PKG-01), not a specific information/artifact transfer to this deliverable. Not extracted per information-flow-only rule.
- **PR-01 (macOS 15+ platform) captured as ANCHOR trace to DEC-PLAT-001 rather than execution dependency:** Platform constraint is a definition-level requirement, not an information flow between deliverables.
- **PR-05 (API key provisioning) subsumed by DEP-07-01-009 (DEL-03-05):** The key provisioning contract is resolved by DEL-03-05; separate document dependency not warranted.
- **PR-06 (Valid working root) not registered as separate dependency:** Working root availability is a runtime environment condition, not an artifact transfer. Session boot testing prerequisite is covered by DEP-07-01-005 (DEL-03-01).
- **No DOWNSTREAM edges extracted:** No source document explicitly states that another deliverable consumes an artifact produced by DEL-07-01. CONSERVATIVE mode does not infer downstream consumers.

### Integration Fan-In Refresh (2026-02-24)
- Revalidated validation-suite/runtime interface assumptions after two consecutive `harness:validate:premerge` pass runs (`8/8` each).
- Refreshed `Dependencies.csv` `LastSeen` timestamps for all ACTIVE rows to `2026-02-24`.
- No dependency rows were added, retired, reclassified, or had `SatisfactionStatus` transitions.

---

## Run History

| Timestamp | Mode | Strictness | DecompositionStatus | Warnings | ACTIVE_ANCHOR | ACTIVE_EXECUTION | ACTIVE_Total |
|---|---|---|---|---|---|---|---|
| 2026-02-24 (fan-in refresh) | UPDATE | CONSERVATIVE | Available (G7-APPROVED) | AMBIGUOUS_ANCHOR (dual anchor: SOW-028 + OBJ-006) | 4 | 11 | 15 |
| 2026-02-21 | UPDATE | CONSERVATIVE | Available (G7-APPROVED) | AMBIGUOUS_ANCHOR (dual anchor: SOW-028 + OBJ-006) | 4 | 11 | 15 |

---

## Downstream Handoff Notes

*CONSUMER_CONTEXT is NONE. No downstream handoff notes generated.*
