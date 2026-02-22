# Specification — DEL-05-04: Dependency Tracking File Contract (v3.1)

---

## Scope

### What This Deliverable Covers

This deliverable defines and implements the contract for deliverable-local dependency tracking in the Chirality filesystem-as-state execution model. It encompasses:

1. **`_DEPENDENCIES.md` file format** — the hybrid summary file with human-owned and agent-owned sections (SPEC.md Section 5).
2. **`Dependencies.csv` v3.1 schema** — the structured dependency register with 29 core columns, 2 extension columns, and full provenance requirements (SPEC.md Section 6).
3. **Integration glue** — minimal code and configuration required for the DEPENDENCIES agent, PREPARATION agent, and downstream consumers (RECONCILIATION, estimating, staleness tooling) to correctly read and write these files.
4. **Validation and testing** — test coverage confirming schema conformance, provenance enforcement, lifecycle tracking, and identity rules.

**Scope item coverage:** SOW-018 — "Support deliverable-local dependency tracking: `_DEPENDENCIES.md` + `Dependencies.csv v3.1` including provenance requirements."

Source: Decomposition DEL-05-04 entry; SPEC.md Sections 5–6; CONTRACT K-DEP-1, K-DEP-2.

### What This Deliverable Excludes

- **Central dependency graph maintenance** — there is no central graph; aggregation is on-demand via `_Reconciliation/` (CONTRACT K-DEP-1).
- **CI-level schema linter** — covered by DEL-08-02 (TBD scope; SOW-033).
- **On-demand dependency graph generation** — covered by DEL-08-04 (TBD scope; SOW-035).
- **Staleness propagation tooling** — covered by DEL-08-07 (TBD scope; SOW-038).
- **Content hash verification for references** — covered by DEL-08-01 (TBD scope; SOW-032).
- **Deliverable lifecycle state management** — covered by DEL-05-03 (SOW-016).
- **Execution root scaffolding** — covered by DEL-05-02 (SOW-014, SOW-015).

---

## Requirements

### REQ-01: `_DEPENDENCIES.md` File Existence

Every deliverable folder MUST contain a `_DEPENDENCIES.md` file.

- **Normative level:** MUST
- **Source:** SPEC.md Section 2.1 (File Inventory table — `_DEPENDENCIES.md` Presence: MUST)
- **Verification:** File existence check per deliverable folder.

### REQ-02: `_DEPENDENCIES.md` Dual-Ownership Structure

`_DEPENDENCIES.md` MUST be structured as a hybrid container with two ownership zones:

- **Human-owned sections:** Dependency Tracking Mode, Declared Upstream, Declared Downstream.
- **Agent-owned sections:** Extracted Dependency Register, Run Notes & History, Lifecycle Summary, Consumer Handoff Notes.

The Consumer Handoff Notes section provides a structured location for the DEPENDENCIES agent to record guidance for downstream consumers of this deliverable's outputs. Expected content includes: interface stability notes, known caveats about dependency data quality, and recommendations for consumers reading this deliverable's register. See Guidance section "Consumer Handoff Notes Content" for format expectations.

- **Normative level:** MUST
- **Source:** SPEC.md Section 5.1
- **Verification:** Section heading check; ownership boundary enforcement in agent write logic.

### REQ-03: `_DEPENDENCIES.md` Tracking Modes

The `_DEPENDENCIES.md` tracking mode field MUST accept exactly three values: `NOT_TRACKED`, `DECLARED`, `TRACKED`.

| Mode | Meaning |
|------|---------|
| `NOT_TRACKED` | Dependencies coordinated externally by humans |
| `DECLARED` | Human-declared upstream/downstream only; no agent extraction |
| `TRACKED` | Full agent extraction; `Dependencies.csv` present |

- **Normative level:** MUST
- **Source:** SPEC.md Section 5.3
- **Verification:** Enum validation.

### REQ-04: `Dependencies.csv` Presence

Each deliverable SHOULD have a `Dependencies.csv` file when the tracking mode is `TRACKED`.

- **Normative level:** SHOULD
- **Source:** SPEC.md Section 2.1 (File Inventory table — `Dependencies.csv` Presence: SHOULD)
- **Verification:** File existence check when mode is `TRACKED`.
- **Governance note:** See Guidance section "SHOULD-Level Governance Threshold" for the interpretation of SHOULD-level failures during verification. The SHOULD level is sourced directly from SPEC.md Section 2.1; any elevation to MUST would require a SPEC amendment.

### REQ-05: Schema Version Marker

Every row in `Dependencies.csv` MUST include a `RegisterSchemaVersion` column set to `v3.1`.

- **Normative level:** MUST
- **Source:** SPEC.md Section 6.1
- **Verification:** Column + value check per row (automated).

### REQ-06: Core Column Completeness

`Dependencies.csv` MUST contain all 29 core columns as specified in SPEC.md Section 6.2.

- **Normative level:** MUST
- **Source:** SPEC.md Section 6.2
- **Verification:** Column header validation against the canonical column list. The canonical column enumeration is reproduced in Datasheet.md section "Dependencies.csv v3.1 Core Column Enumeration" for in-deliverable reference. The authoritative source remains `docs/SPEC.md` Section 6.2.

### REQ-07: Extension Column Non-Breaking Compatibility

Extension columns (`EstimateImpactClass`, `ConsumerHint`) MAY be present. Their absence MUST NOT break readers.

- **Normative level:** MAY (extension columns); MUST NOT (break on absence)
- **Source:** SPEC.md Section 6.2
- **Verification:** Reader robustness test with and without extension columns.

### REQ-08: Dependency Class Enum Compliance

`DependencyClass` values MUST be one of: `ANCHOR`, `EXECUTION`.

- **Normative level:** MUST
- **Source:** SPEC.md Section 6.3
- **Verification:** Enum validation per row.

### REQ-09: ANCHOR Row Rules

ANCHOR rows MUST satisfy:
- `AnchorType` is `IMPLEMENTS_NODE` or `TRACES_TO_REQUIREMENT` (NOT `NOT_APPLICABLE`).
- `DependencyType` is `OTHER`.
- Exactly one `IMPLEMENTS_NODE` row SHOULD exist per deliverable.

- **Normative level:** MUST (first two rules); SHOULD (exactly one IMPLEMENTS_NODE)
- **Source:** SPEC.md Section 6.4
- **Verification:** Row classification validation.

### REQ-10: EXECUTION Row Rules

EXECUTION rows MUST satisfy:
- `DependencyClass` is `EXECUTION`.
- `AnchorType` is `NOT_APPLICABLE`.
- `DependencyType` uses preferred execution enums (`PREREQUISITE`, `INTERFACE`, `HANDOVER`, `CONSTRAINT`, `ENABLES`, `OTHER`).

- **Normative level:** MUST
- **Source:** SPEC.md Section 6.4
- **Verification:** Row classification validation.

### REQ-11: Provenance — EvidenceFile and SourceRef

Every ACTIVE row MUST include:
- `EvidenceFile`: the source document filename (or `location TBD`).
- `SourceRef`: path + heading/section within the evidence file (or `location TBD`).

- **Normative level:** MUST
- **Source:** SPEC.md Section 6.5; CONTRACT K-PROV-1
- **Verification:** Non-empty check on `EvidenceFile` and `SourceRef` for all ACTIVE rows.

### REQ-12: Provenance — EvidenceQuote

`EvidenceQuote` SHOULD be provided for traceability (max 30 words).

- **Normative level:** SHOULD
- **Source:** SPEC.md Section 6.5
- **Verification:** Presence check (advisory); length check (<= 30 words).

### REQ-13: Lifecycle Tracking Fields

Each row MUST track extraction lifecycle via:
- `FirstSeen`: ISO date of first extraction.
- `LastSeen`: ISO date of most recent confirmation.
- `Status`: `ACTIVE` or `RETIRED`.

- **Normative level:** MUST
- **Source:** SPEC.md Section 6.6
- **Verification:** Date format validation; enum validation for `Status`.

### REQ-14: No Row Deletion

Rows MUST NOT be deleted. Rows no longer observed in source text are marked `RETIRED`.

- **Normative level:** MUST NOT (delete)
- **Source:** SPEC.md Section 6.6
- **Verification:** Row count monotonicity check across extraction runs (no decreases). **Baseline initialization:** The first extraction run establishes the baseline; prior to the first run, the baseline row count is zero. The monotonicity invariant applies from the first run onward (i.e., run N+1 row count >= run N row count for all N >= 1).

### REQ-15: DependencyID Uniqueness and Format

- `DependencyID` MUST be unique within a single deliverable's register.
- `DependencyID` format: `DEP-{PKG}-{DEL}-{SEQ}` (e.g., `DEP-01-01-001`).
- `FromDeliverableID` MUST match the host deliverable's ID.

- **Normative level:** MUST
- **Source:** SPEC.md Section 6.8
- **Verification:** Uniqueness check; format regex validation; host ID match.

### REQ-16: Target Resolution

- For `TargetType=DELIVERABLE`: `TargetDeliverableID` MUST contain the target's stable deliverable ID.
- For non-deliverable targets: `TargetDeliverableID` MUST be empty; use `TargetRefID` and `TargetName`.
- Unresolvable targets MUST use `TargetType=UNKNOWN`.

- **Normative level:** MUST
- **Source:** SPEC.md Section 6.8; CONTRACT K-DEP-2
- **Verification:** Conditional field presence validation.

### REQ-17: Legacy Compatibility on Write

On write:
- `Direction`: `INBOUND` normalizes to `UPSTREAM`; `OUTBOUND` normalizes to `DOWNSTREAM`.
- If `RegisterSchemaVersion` is missing from an existing file, add it and set to `v3.1`.

- **Normative level:** MUST (on write)
- **Source:** SPEC.md Section 6.7
- **Verification:** Legacy normalization integration test.

### REQ-18: Deliverable-Local Authority

Deliverable-local `_DEPENDENCIES.md` and `Dependencies.csv` are authoritative for dependencies. There is no central dependency graph.

- **Normative level:** Invariant
- **Source:** CONTRACT K-DEP-1
- **Verification:** Architecture review (manual). **Review protocol:** Verify that no file matching a central dependency graph pattern exists (e.g., no `dependencies.json` or `dependency_graph.*` at project root); verify that aggregation outputs in `_Reconciliation/` are read-only snapshots. See Guidance section "Manual Review Protocols" for the review checklist.

### REQ-19: No Invented Content

Unknown values MUST become `TBD`, not guessed. Agents MUST NOT invent scope items, dependency targets, parameter values, or engineering content.

- **Normative level:** Invariant
- **Source:** CONTRACT K-INVENT-1
- **Verification:** Review for unsourced assertions (manual). **Review protocol:** Sample ACTIVE rows and verify that `EvidenceFile` and `SourceRef` point to real, accessible sources; verify that `Statement` text is supported by cited evidence. See Guidance section "Manual Review Protocols" for the review checklist.

### REQ-20: Conflict Surfacing

Conflicts between sources MUST be surfaced, not silently resolved. Agents expose disagreements with pointers to the conflicting sources.

- **Normative level:** Invariant
- **Source:** CONTRACT K-CONFLICT-1
- **Verification:** Review for hidden conflict resolution (manual). **Review protocol:** Examine `ConflictFlag` column for any flagged rows; verify that conflicts between human-declared and agent-extracted dependencies are documented in the Conflict Table or `_MEMORY.md`. See Guidance section "Manual Review Protocols" for the review checklist.

### REQ-21: SatisfactionStatus Transition Rules

`SatisfactionStatus` transitions MUST follow a defined progression. Valid transitions are:

| From State | Allowed To States |
|------------|-------------------|
| `TBD` | `PENDING`, `NOT_APPLICABLE`, `WAIVED` |
| `PENDING` | `IN_PROGRESS`, `NOT_APPLICABLE`, `WAIVED` |
| `IN_PROGRESS` | `SATISFIED`, `WAIVED` |
| `SATISFIED` | *(terminal — no forward transitions)* |
| `WAIVED` | *(terminal — no forward transitions)* |
| `NOT_APPLICABLE` | *(terminal — no forward transitions)* |

- **Normative level:** MUST (**ASSUMPTION** — transition rules are inferred from the enum semantics in SPEC.md Section 6.3; the authoritative transition specification is **location TBD** in `docs/SPEC.md`)
- **Source:** SPEC.md Section 6.3 (enum definition); transition rules inferred
- **Verification:** State machine validation on `SatisfactionStatus` changes across extraction runs.
- **Transition authority:** TBD — whether transitions are agent-initiated, human-initiated, or both is a governance question for human ruling.

---

## Standards

| Standard/Document | Applicability | Accessible | Source |
|-------------------|--------------|------------|--------|
| `docs/SPEC.md` Sections 5–6 | Authoritative schema for `_DEPENDENCIES.md` and `Dependencies.csv` v3.1 | Yes | Governance |
| `docs/CONTRACT.md` K-DEP-1, K-DEP-2, K-PROV-1, K-INVENT-1, K-CONFLICT-1 | Binding invariants | Yes | Governance |
| `docs/TYPES.md` Section 3 | Canonical dependency vocabulary | Yes | Governance |
| `docs/DIRECTIVE.md` Section 2.1, 2.4 | Design philosophy (filesystem-as-database, evidence-over-plausibility) | Yes | Governance |

---

## Verification

| Requirement | Verification Approach | Artifact |
|-------------|----------------------|----------|
| REQ-01 | Folder structure validator (automated) | TEST |
| REQ-02 | Section heading check + Consumer Handoff content presence (automated or manual) | TEST |
| REQ-03 | Enum validation (automated) | TEST |
| REQ-04 | Conditional file existence check (automated); SHOULD-level — advisory warning, not hard failure | TEST |
| REQ-05 | Column + value check per row (automated) | TEST |
| REQ-06 | Column header validation against canonical column list (automated); reference list in Datasheet.md | TEST |
| REQ-07 | Reader robustness test (automated) | TEST |
| REQ-08 | Enum validation per row (automated) | TEST |
| REQ-09 | Row classification validation (automated) | TEST |
| REQ-10 | Row classification validation (automated) | TEST |
| REQ-11 | Non-empty check on provenance fields (automated) | TEST |
| REQ-12 | Presence + length check (automated, advisory); SHOULD-level — advisory warning, not hard failure | TEST |
| REQ-13 | Date format + enum validation (automated) | TEST |
| REQ-14 | Row count monotonicity across runs (automated); baseline = 0 before first run | TEST |
| REQ-15 | Uniqueness + format regex + host ID match (automated) | TEST |
| REQ-16 | Conditional field presence validation (automated) | TEST |
| REQ-17 | Legacy normalization integration test (automated) | TEST |
| REQ-18 | Architecture review (manual) — see Manual Review Protocols in Guidance.md | DOC |
| REQ-19 | Review for unsourced assertions (manual) — see Manual Review Protocols in Guidance.md | DOC |
| REQ-20 | Review for hidden conflict resolution (manual) — see Manual Review Protocols in Guidance.md | DOC |
| REQ-21 | State machine validation on SatisfactionStatus transitions (automated) | TEST |

---

## Documentation

### Required Artifacts (from `_CONTEXT.md` Anticipated Artifacts)

| Artifact Type | Description | Status |
|---------------|-------------|--------|
| DOC | Dependency tracking contract documentation (this document kit) | This deliverable |
| CODE | Integration glue: file generation, validation, read/write logic for `_DEPENDENCIES.md` and `Dependencies.csv` | TBD — production trigger and codebase location to be determined |
| TEST | Schema conformance tests, provenance enforcement tests, identity rule tests, lifecycle tracking tests | TBD — production trigger and test directory location to be determined |

### Governing Documents

- `docs/SPEC.md` — Physical structures and mechanics (Sections 5–6 are primary)
- `docs/CONTRACT.md` — Invariant catalog (K-DEP-1, K-DEP-2, K-PROV-1 are primary)
- `docs/TYPES.md` — Domain vocabulary (Section 3 is primary)
- `docs/DIRECTIVE.md` — Design philosophy and constraints
