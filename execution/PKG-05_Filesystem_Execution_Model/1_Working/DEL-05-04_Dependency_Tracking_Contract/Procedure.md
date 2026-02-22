# Procedure — DEL-05-04: Dependency Tracking File Contract (v3.1)

---

## Purpose

This procedure describes the steps to **produce** the Dependency Tracking File Contract deliverable and to **operate** the dependency tracking mechanism it defines. It covers both the creation of the contract artifacts (DOC/CODE/TEST) and the ongoing use of `_DEPENDENCIES.md` and `Dependencies.csv` within the Chirality execution model.

---

## Prerequisites

### Required References

| Reference | Location | Purpose |
|-----------|----------|---------|
| `docs/SPEC.md` Sections 5–6 | `docs/SPEC.md` | Authoritative schema definitions |
| `docs/CONTRACT.md` | `docs/CONTRACT.md` | Binding invariants (K-DEP-1, K-DEP-2, K-PROV-1) |
| `docs/TYPES.md` Section 3 | `docs/TYPES.md` | Canonical dependency vocabulary |
| Decomposition (G7-APPROVED) | `execution/_Decomposition/ChiralityApp_SoftwareDecomposition_2026-02-21_G7-APPROVED.md` | Deliverable definition and scope coverage |

### Required Preconditions

| Precondition | Dependency | Status | Operational Meaning |
|-------------|-----------|--------|---------------------|
| Execution root scaffolding established | DEL-05-02 (SOW-014, SOW-015) | TBD | **Proceed with risk:** dependency file paths assume the standard folder structure exists. If scaffolding is incomplete, file creation may fail or place files in non-standard locations. Verify folder structure before proceeding with Part A Steps A2–A5. |
| Lifecycle state handling defined | DEL-05-03 (SOW-016) | TBD | **Proceed with documentation:** the dependency contract can be defined independently of lifecycle state mechanics, but integration testing (Part A Step A6) requires knowledge of how `_STATUS.md` states interact with extraction timing. |
| Governance documents available and current | `docs/SPEC.md`, `docs/CONTRACT.md`, `docs/TYPES.md` | Available | Ready. |
| Deliverable folder exists with minimum viable fileset | PREPARATION agent | Complete (this folder) | Ready. |

### Upstream Dependency Notes

`_DEPENDENCIES.md` has not yet been populated by the DEPENDENCIES agent (status: `PENDING_EXTRACTION`). Declared upstream/downstream dependencies are not yet present. The preconditions listed above are **ASSUMPTION** based on the logical relationship between DEL-05-02, DEL-05-03, and DEL-05-04 within PKG-05.

---

## Steps

### Part A: Produce the Contract Artifacts

#### Step A0: Determine CODE/TEST Bootstrapping Path

Before implementing or verifying code (Steps A2–A6), determine whether the CODE and TEST artifacts for this deliverable already exist.

1. Check if integration code for `_DEPENDENCIES.md` generation and `Dependencies.csv` write/read logic exists in the codebase.
2. Check if a test directory or test suite for dependency tracking schema conformance exists.
3. If CODE artifacts do **not yet exist:**
   - Record the codebase location decision as TBD.
   - Proceed to Step A1 (requirements confirmation) and then to implementation in Steps A2–A5.
   - The Datasheet "Required Artifacts" table tracks CODE and TEST status.
4. If CODE artifacts **already exist:**
   - Proceed directly to verification mode in Steps A2–A5 (verify existing logic against the contract).

**Output:** Bootstrapping assessment; decision on whether to implement new code or verify existing code.

**Note:** This step addresses the bootstrapping gap identified by lensing (the procedure previously assumed code existed to verify). If code does not yet exist, Steps A2–A5 should be read as "implement" rather than "verify."

#### Step A1: Confirm Contract Requirements

1. Review `docs/SPEC.md` Sections 5 and 6 to confirm the current `_DEPENDENCIES.md` format and `Dependencies.csv` v3.1 schema.
2. Review `docs/CONTRACT.md` invariants K-DEP-1, K-DEP-2, K-PROV-1, K-INVENT-1, and K-CONFLICT-1 to confirm binding constraints.
3. Review `docs/TYPES.md` Section 3 to confirm canonical dependency vocabulary.
4. Confirm that the Specification.md requirements (REQ-01 through REQ-21) accurately reflect the source documents.
5. Identify any gaps between the specification and the current codebase implementation.

**Output:** Confirmed requirements list; gap analysis (if any).

#### Step A2: Implement or Verify `_DEPENDENCIES.md` Generation Logic

1. Locate the PREPARATION agent's `_DEPENDENCIES.md` creation logic (or implement if not yet present — see Step A0).
2. Verify that the generated file matches the SPEC.md Section 5.2 schema:
   - Human-owned sections present: Tracking Mode, Declared Upstream, Declared Downstream.
   - Agent-owned section placeholders present: Extracted Register, Run Notes, Lifecycle Summary, Consumer Handoff Notes.
3. Verify tracking mode enum values are validated (`NOT_TRACKED`, `DECLARED`, `TRACKED`).
4. If the existing logic does not conform, implement corrections.

**Output:** Verified or corrected `_DEPENDENCIES.md` generation code.

#### Step A3: Implement or Verify `Dependencies.csv` Write Logic

1. Locate the DEPENDENCIES agent's `Dependencies.csv` write logic (or implement if not yet present — see Step A0).
2. Verify all 29 core columns are emitted in the correct order per SPEC.md Section 6.2. Cross-reference against the canonical column enumeration in Datasheet.md.
3. Verify `RegisterSchemaVersion` is set to `v3.1` on every row.
4. Verify enum values comply with SPEC.md Section 6.3 canonical values:
   - `DependencyClass`: `ANCHOR` | `EXECUTION`
   - `AnchorType`: `IMPLEMENTS_NODE` | `TRACES_TO_REQUIREMENT` | `NOT_APPLICABLE`
   - `Direction`: `UPSTREAM` | `DOWNSTREAM`
   - `DependencyType`: `PREREQUISITE` | `INTERFACE` | `HANDOVER` | `CONSTRAINT` | `ENABLES` | `OTHER`
   - `TargetType`: `DELIVERABLE` | `PACKAGE` | `WBS_NODE` | `REQUIREMENT` | `DOCUMENT` | `EQUIPMENT` | `EXTERNAL` | `UNKNOWN`
   - `Explicitness`: `EXPLICIT` | `IMPLICIT`
   - `SatisfactionStatus`: `TBD` | `PENDING` | `IN_PROGRESS` | `SATISFIED` | `WAIVED` | `NOT_APPLICABLE`
   - `Confidence`: `HIGH` | `MEDIUM` | `LOW`
   - `Origin`: `DECLARED` | `EXTRACTED`
   - `Status`: `ACTIVE` | `RETIRED`
5. Verify ANCHOR row classification rules (REQ-09).
6. Verify EXECUTION row classification rules (REQ-10).
7. Verify provenance fields are populated (REQ-11, REQ-12).
8. Verify identity rules (REQ-15, REQ-16).
9. Verify legacy compatibility normalization (REQ-17).
10. Verify SatisfactionStatus transition rules (REQ-21) are enforced on write, if applicable.

**Output:** Verified or corrected `Dependencies.csv` write logic.

#### Step A4: Implement or Verify `Dependencies.csv` Read Logic

1. Locate all consumers of `Dependencies.csv` (RECONCILIATION agent, aggregation tooling, any other readers).
2. Verify readers handle:
   - Missing extension columns gracefully (REQ-07).
   - `RETIRED` rows (filter or include based on consumer needs).
   - `location TBD` in provenance fields.
   - Legacy direction values (`INBOUND`, `OUTBOUND`) if encountered in existing files.
3. If reader logic does not conform, implement corrections.

**Output:** Verified or corrected reader logic.

#### Step A5: Implement or Verify `_DEPENDENCIES.md` Agent Write Logic

1. Locate the DEPENDENCIES agent's `_DEPENDENCIES.md` update logic (or implement if not yet present — see Step A0).
2. Verify that agent writes are limited to agent-owned sections only (REQ-02):
   - Extracted Dependency Register
   - Run Notes & History
   - Lifecycle Summary
   - Consumer Handoff Notes
3. Verify that human-owned sections are preserved unmodified during agent writes.
4. Verify append-only behavior for Run History entries.
5. Verify that Consumer Handoff Notes are populated with interface stability notes, data quality caveats, and consumer recommendations (see Guidance section "Consumer Handoff Notes Content").

**Output:** Verified or corrected agent update logic.

#### Step A6: Implement Schema Conformance Tests

1. Create test cases for each requirement (REQ-01 through REQ-21).
2. Priority test areas:
   - **Column completeness** (REQ-06): All 29 core columns present (reference Datasheet column enumeration).
   - **Enum validation** (REQ-08, REQ-09, REQ-10): All enum fields contain only valid values.
   - **Provenance enforcement** (REQ-11): Every ACTIVE row has `EvidenceFile` and `SourceRef`.
   - **Identity rules** (REQ-15): DependencyID uniqueness and format.
   - **Row lifecycle** (REQ-13, REQ-14): Date fields valid; no row deletion; monotonicity baseline from first run.
   - **Legacy compatibility** (REQ-17): Direction normalization; schema version addition.
   - **SatisfactionStatus transitions** (REQ-21): Valid state transitions enforced.
3. Test with:
   - Valid v3.1 data (happy path).
   - Legacy data (missing `RegisterSchemaVersion`, legacy direction values).
   - Invalid data (wrong enums, missing required fields, duplicate DependencyIDs).
   - Edge cases (empty register, single-row register, register with all RETIRED rows).
   - First-run baseline case (no prior extraction; row count starts at 0).

**Output:** Test suite covering REQ-01 through REQ-21.

#### Step A7: Document Integration Points

1. Document how PREPARATION creates `_DEPENDENCIES.md` (including Consumer Handoff Notes placeholder).
2. Document how the DEPENDENCIES agent populates agent-owned sections and creates `Dependencies.csv`.
3. Document how downstream consumers (RECONCILIATION, estimating, staleness tooling) read the register.
4. Document the dual-ownership boundary and conflict resolution expectations.
5. Update this deliverable's document kit to reflect implementation findings.

**Output:** Integration documentation within this deliverable's document kit.

---

### Part B: Operate the Dependency Tracking Mechanism

These steps describe the ongoing operational use of the dependency tracking files.

#### Step B1: PREPARATION Scaffold

When a new deliverable is scaffolded by the PREPARATION agent:
1. Create `_DEPENDENCIES.md` with the schema from SPEC.md Section 5.2, including the Consumer Handoff Notes section.
2. Set tracking mode to `TRACKED` (or `NOT_TRACKED` / `DECLARED` per human direction).
3. Leave agent-owned sections empty with placeholder text.

**Verification:** `_DEPENDENCIES.md` exists and matches the schema template (including Consumer Handoff Notes section).

#### Step B2: DEPENDENCIES Agent Extraction

When the DEPENDENCIES agent runs against a deliverable:
1. Read the deliverable's document kit and accessible references.
2. Extract dependency relationships, classifying each as ANCHOR or EXECUTION.
3. Populate `Dependencies.csv` with all 29 core columns per row.
4. Ensure provenance fields (`EvidenceFile`, `SourceRef`) are filled for every ACTIVE row.
5. Mark previously-seen rows that are no longer observed as `RETIRED` (update `Status`, preserve `LastSeen`).
6. Verify row count monotonicity: total row count (ACTIVE + RETIRED) must be >= prior run's total. **First-run baseline:** If no prior `Dependencies.csv` exists, the baseline is 0 rows; any number of rows in the first extraction satisfies monotonicity.
7. Update agent-owned sections of `_DEPENDENCIES.md` with summary statistics.
8. Populate Consumer Handoff Notes with interface stability notes, data quality caveats, and consumer recommendations.
9. Append a run entry to Run History.

**Verification:** `Dependencies.csv` passes schema conformance checks; `_DEPENDENCIES.md` agent-owned sections are populated; human-owned sections are unmodified.

#### Step B3: Downstream Consumption

When downstream agents or tools consume dependency data:
1. Read `Dependencies.csv` from the target deliverable folder.
2. Filter on `Status=ACTIVE` for current dependencies (unless historical analysis is intended).
3. Handle missing extension columns without failure.
4. Cross-reference `TargetDeliverableID` against known deliverable IDs for resolution validation.

**Verification:** Consumer operates correctly with valid v3.1 data and gracefully handles edge cases.

#### Step B4: Human Override and Conflict Resolution

When human-declared dependencies conflict with agent-extracted dependencies:
1. Review both the Declared Upstream/Downstream sections and the Extracted Register.
2. Determine which source is authoritative for the specific conflict.
3. Record the resolution in `_MEMORY.md` (or equivalent working memory).
4. Update the relevant section (human-owned or agent re-extraction) to reflect the resolution.

**Verification:** Conflict is resolved and documented; no silent resolution.

---

## Verification

### Deliverable-Level Verification Checklist

| Check | Method | Pass Criteria |
|-------|--------|---------------|
| Contract documentation complete | Manual review | Datasheet, Specification, Guidance, Procedure exist and are internally consistent |
| Requirements traceable to sources | Manual review | Every REQ-* cites `docs/SPEC.md`, `docs/CONTRACT.md`, or `docs/TYPES.md` |
| `_DEPENDENCIES.md` generation conforms to SPEC | Automated test | Output matches Section 5.2 schema (including Consumer Handoff Notes section) |
| `Dependencies.csv` write logic conforms to v3.1 | Automated test | All 29 core columns; valid enums; provenance filled |
| `Dependencies.csv` read logic handles edge cases | Automated test | Missing extensions, legacy values, RETIRED rows handled |
| Schema conformance test suite passes | Automated test | All REQ-01 through REQ-21 covered and passing |
| Dual-ownership boundary enforced | Automated or manual test | Agent writes do not modify human-owned sections |
| Legacy compatibility verified | Automated test | Direction normalization; schema version addition on write |
| SatisfactionStatus transition rules enforced | Automated test | Invalid transitions rejected or flagged |
| Manual review protocols executed | Manual review | REQ-18, REQ-19, REQ-20 checklists completed per Guidance.md |

### Integration Verification

| Check | Method | Pass Criteria |
|-------|--------|---------------|
| PREPARATION creates valid `_DEPENDENCIES.md` | Integration test | File exists and matches schema after scaffold (including Consumer Handoff Notes) |
| DEPENDENCIES agent produces valid `Dependencies.csv` | Integration test | File passes schema conformance checks after extraction |
| RECONCILIATION reads register correctly | Integration test | Aggregation output includes data from local registers |
| Row count does not decrease across extraction runs | Regression test | `RETIRED` rows preserved; total row count non-decreasing; first-run baseline = 0 |

---

## Records

### Expected Output Records

| Record | Location | Produced By |
|--------|----------|-------------|
| This document kit (Datasheet, Specification, Guidance, Procedure) | `DEL-05-04_Dependency_Tracking_Contract/` | 4_DOCUMENTS agent |
| Integration code changes (if any) | TBD (codebase — see Step A0 for bootstrapping path) | Human / WORKING_ITEMS |
| Schema conformance test suite | TBD (test directory — see Step A0 for bootstrapping path) | Human / WORKING_ITEMS |
| `_STATUS.md` history entry | `DEL-05-04_Dependency_Tracking_Contract/_STATUS.md` | 4_DOCUMENTS / WORKING_ITEMS |
| `Dependencies.csv` (for this deliverable) | `DEL-05-04_Dependency_Tracking_Contract/Dependencies.csv` | DEPENDENCIES agent (future run) |

### Traceability

| Artifact | Traces To |
|----------|-----------|
| Contract documentation | SOW-018; OBJ-004 |
| Schema conformance tests | REQ-01 through REQ-21 |
| Integration code | SPEC.md Sections 5–6; CONTRACT K-DEP-1, K-DEP-2, K-PROV-1 |
