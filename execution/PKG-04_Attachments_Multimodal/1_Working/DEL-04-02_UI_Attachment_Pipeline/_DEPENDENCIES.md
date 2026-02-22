# Dependencies -- DEL-04-02

**Tracking Mode:** FULL_GRAPH
**Status:** EXTRACTED

---

## Declared Upstream Dependencies

*No manually declared upstream dependencies. All upstream dependencies were extracted from source documents.*

## Declared Downstream Dependencies

*No manually declared downstream dependencies.*

---

## Extracted Dependency Register

**Register file:** `Dependencies.csv` (v3.1 schema)
**Total ACTIVE rows:** 8
**Total RETIRED rows:** 0

### Summary by Class

| DependencyClass | AnchorType | Count |
|-----------------|------------|-------|
| ANCHOR | IMPLEMENTS_NODE | 1 |
| ANCHOR | TRACES_TO_REQUIREMENT | 1 |
| EXECUTION | NOT_APPLICABLE | 6 |

### ANCHOR Rows (Tree -- Definition Linkage)

| DependencyID | AnchorType | Direction | TargetType | TargetRefID / TargetName | Confidence | Notes |
|---|---|---|---|---|---|---|
| DEP-04-02-001 | IMPLEMENTS_NODE | UPSTREAM | WBS_NODE | SOW-010 | HIGH | FACT. Scope item explicitly mapped in Datasheet and Decomposition. |
| DEP-04-02-002 | TRACES_TO_REQUIREMENT | UPSTREAM | REQUIREMENT | OBJ-003 | HIGH | FACT. Objective explicitly mapped in Datasheet and Decomposition. |

### EXECUTION Rows (DAG -- Information Flow)

| DependencyID | Direction | DependencyType | TargetType | Target | Confidence | Statement (abbreviated) |
|---|---|---|---|---|---|---|
| DEP-04-02-003 | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-04-01 (Server-side Attachment Resolver) | HIGH | UI sends attachment paths; server resolves and returns results. |
| DEP-04-02-004 | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-03-02 (Turn Execution API + SSE Streaming) | HIGH | Turn API endpoint must accept attachments array. |
| DEP-04-02-005 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-03-01 (Working Root Binding & Session Boot) | MEDIUM | Session rehydration implies dependency on session state from session boot. |
| DEP-04-02-006 | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-01-01 (macOS 15+ Apple Silicon Build Baseline) | HIGH | Repo must build/run per DEL-01-01. |
| DEP-04-02-007 | UPSTREAM | CONSTRAINT | DOCUMENT | SPEC.md Section 9.8 | HIGH | Governing contract for UI attachment state rules. |
| DEP-04-02-008 | UPSTREAM | CONSTRAINT | DOCUMENT | CONTRACT.md (K-INVENT-1, K-GHOST-1) | HIGH | Binding invariants constraining implementation approach. |

---

## Lifecycle Summary

| Status | Count |
|--------|-------|
| ACTIVE | 8 |
| RETIRED | 0 |

| SatisfactionStatus | Count |
|--------------------|-------|
| TBD | 4 |
| PENDING | 2 |
| NOT_APPLICABLE | 2 |

**Closure breakdown:**
- **TBD (4):** DEP-04-02-001 (anchor SOW-010), DEP-04-02-002 (anchor OBJ-003), DEP-04-02-005 (DEL-03-01 interface), DEP-04-02-006 (DEL-01-01 build baseline)
- **PENDING (2):** DEP-04-02-003 (DEL-04-01 prerequisite), DEP-04-02-004 (DEL-03-02 prerequisite)
- **NOT_APPLICABLE (2):** DEP-04-02-007 (SPEC.md constraint document), DEP-04-02-008 (CONTRACT.md constraint document)

---

## Run Notes

### Defaults and Paths Used

| Setting | Value |
|---------|-------|
| MODE | UPDATE |
| STRICTNESS | CONSERVATIVE |
| CONSUMER_CONTEXT | NONE |
| DECOMPOSITION_PATH | `execution/_Decomposition/ChiralityApp_SoftwareDecomposition_2026-02-21_G7-APPROVED.md` |
| DECOMPOSITION_STATUS | Available; validated successfully |
| SOURCE_DOCS | AUTO -- scanned deliverable folder |
| ANCHOR_DOC | `Datasheet.md` (matched ANCHOR_DOC heuristic: contains "datasheet") |
| EXECUTION_DOC_ORDER | `Specification.md`, `Procedure.md`, `Guidance.md` |
| Additional docs read | `_CONTEXT.md`, `_REFERENCES.md` |

### Extraction Notes

- **Pass 1 (Anchor):** Extracted 1 IMPLEMENTS_NODE row (SOW-010) and 1 TRACES_TO_REQUIREMENT row (OBJ-003). Both validated against decomposition: SOW-010 confirmed in Scope Ledger with PackageID=PKG-04, DeliverableID=DEL-04-02; OBJ-003 confirmed in PKG-04 deliverable table SupportsObjectives column.
- **Pass 2 (Execution):** Extracted 6 EXECUTION rows.
  - DEL-04-01 and DEL-03-02 are explicit prerequisites named in both Specification and Procedure documents with clear information-flow descriptions.
  - DEL-03-01 is an implicit interface dependency inferred from scope exclusion statement and session rehydration requirement (MEDIUM confidence, marked ASSUMPTION).
  - DEL-01-01 is an explicit prerequisite from Procedure Prerequisites table.
  - SPEC.md Section 9.8 and CONTRACT.md are explicit constraint documents cited across all source docs.
- **Filtered out (CONSERVATIVE):** DEL-03-03 (opts mapping) was mentioned in Specification Excluded section as a scope boundary but no explicit data/artifact transfer to DEL-04-02 was identified. Not extracted under CONSERVATIVE strictness.
- **DIRECTIVE.md Section 2.5** is referenced in Guidance P4 and Datasheet References but as a general principle reference, not as a specific required input/artifact for this deliverable. Not extracted as a dependency row.

### Warnings

*No warnings.*

### Quality Check Results

- Schema: All required columns present; CSV parseable.
- DependencyID uniqueness: Verified (8 unique IDs).
- Evidence: All ACTIVE rows have EvidenceFile and SourceRef populated.
- Enum normalization: All values are canonical write-form.
- Parent anchor check: 1 ACTIVE IMPLEMENTS_NODE row found. PASS.
- Counts: _DEPENDENCIES.md counts (8 ACTIVE, 0 RETIRED) match Dependencies.csv. PASS.
- No duplicate rows detected.
- Referential integrity: All FromDeliverableID values = DEL-04-02. PASS.
- TargetDeliverableID populated only for TargetType=DELIVERABLE rows. TargetRefID used for non-deliverable targets. PASS.

---

## Run History

| Timestamp | Mode | Strictness | DecompositionStatus | Warnings | ACTIVE Count |
|-----------|------|------------|---------------------|----------|-------------|
| 2026-02-21 | UPDATE | CONSERVATIVE | Available (G7-APPROVED) | None | 8 |
