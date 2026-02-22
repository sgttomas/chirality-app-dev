# Datasheet — DEL-05-04: Dependency Tracking File Contract (v3.1)

---

## Identification

| Field | Value |
|-------|-------|
| **Deliverable ID** | DEL-05-04 |
| **Name** | Dependency Tracking File Contract (v3.1) |
| **Package** | PKG-05 — Filesystem Execution Model |
| **Type** | DATA_MODEL_CHANGE |
| **Context Envelope** | L |
| **Responsible Party** | TBD — *Assignment criteria: the party responsible for defining and maintaining the dependency tracking contract, including schema governance and integration glue. See Guidance section "Responsible Party Assignment" for criteria.* |
| **Scope Coverage** | SOW-018 |
| **Objective** | OBJ-004 — Filesystem-as-state execution model is SPEC-conformant and auditable (**ASSUMPTION: best-effort mapping via PKG-05 package grouping**) |
| **Anticipated Artifacts** | DOC / CODE / TEST |
| **Decomposition** | `execution/_Decomposition/ChiralityApp_SoftwareDecomposition_2026-02-21_G7-APPROVED.md` |

---

## Attributes

### Dependency Tracking Files

| Attribute | Value | Source |
|-----------|-------|--------|
| Primary summary file | `_DEPENDENCIES.md` | SPEC.md Section 5 |
| Structured register file | `Dependencies.csv` | SPEC.md Section 6 |
| Register schema version | v3.1 | SPEC.md Section 6.1 |
| Register presence requirement | SHOULD (per deliverable) | SPEC.md Section 2.1 |
| Summary file presence requirement | MUST (per deliverable) | SPEC.md Section 2.1 |

### Dependencies.csv v3.1 Schema

| Attribute | Value | Source |
|-----------|-------|--------|
| Total core columns | 29 | SPEC.md Section 6.2 |
| Extension columns | 2 (`EstimateImpactClass`, `ConsumerHint`) | SPEC.md Section 6.2 |
| Dependency classes | 2 (`ANCHOR`, `EXECUTION`) | SPEC.md Section 6.3 |
| Anchor types | 3 (`IMPLEMENTS_NODE`, `TRACES_TO_REQUIREMENT`, `NOT_APPLICABLE`) | SPEC.md Section 6.3 |
| Direction values | 2 (`UPSTREAM`, `DOWNSTREAM`) | SPEC.md Section 6.3 |
| Dependency types (preferred) | 6 (`PREREQUISITE`, `INTERFACE`, `HANDOVER`, `CONSTRAINT`, `ENABLES`, `OTHER`) | SPEC.md Section 6.3 |
| Legacy dependency types (deprecated) | 2 (`COORDINATION`, `INFORMATION`) | SPEC.md Section 6.3 |
| Target types | 8 (`DELIVERABLE`, `PACKAGE`, `WBS_NODE`, `REQUIREMENT`, `DOCUMENT`, `EQUIPMENT`, `EXTERNAL`, `UNKNOWN`) | SPEC.md Section 6.3 |
| Status values | 2 (`ACTIVE`, `RETIRED`) | SPEC.md Section 6.3 |
| Satisfaction status values | 6 (`TBD`, `PENDING`, `IN_PROGRESS`, `SATISFIED`, `WAIVED`, `NOT_APPLICABLE`) | SPEC.md Section 6.3 |
| Confidence values | 3 (`HIGH`, `MEDIUM`, `LOW`) | SPEC.md Section 6.3 |
| Origin values | 2 (`DECLARED`, `EXTRACTED`) | SPEC.md Section 6.3 |
| Explicitness values | 2 (`EXPLICIT`, `IMPLICIT`) | SPEC.md Section 6.3 |

### Dependencies.csv v3.1 Core Column Enumeration

The 29 core columns of the v3.1 schema are listed below in canonical order. This enumeration serves as the in-deliverable reference for REQ-06 column completeness validation.

| # | Column Name | Description | Source |
|---|-------------|-------------|--------|
| 1 | `RegisterSchemaVersion` | Schema version marker (always `v3.1`) | SPEC.md Section 6.1 |
| 2 | `DependencyID` | Unique ID per row (`DEP-{PKG}-{DEL}-{SEQ}`) | SPEC.md Section 6.8 |
| 3 | `FromPackageID` | Source package ID | SPEC.md Section 6.2 |
| 4 | `FromDeliverableID` | Source deliverable ID (must match host) | SPEC.md Section 6.8 |
| 5 | `FromDeliverableName` | Source deliverable name | SPEC.md Section 6.2 |
| 6 | `DependencyClass` | `ANCHOR` or `EXECUTION` | SPEC.md Section 6.3 |
| 7 | `AnchorType` | `IMPLEMENTS_NODE`, `TRACES_TO_REQUIREMENT`, or `NOT_APPLICABLE` | SPEC.md Section 6.3 |
| 8 | `Direction` | `UPSTREAM` or `DOWNSTREAM` | SPEC.md Section 6.3 |
| 9 | `DependencyType` | Preferred: `PREREQUISITE`, `INTERFACE`, `HANDOVER`, `CONSTRAINT`, `ENABLES`, `OTHER` | SPEC.md Section 6.3 |
| 10 | `TargetType` | Target entity classification | SPEC.md Section 6.3 |
| 11 | `TargetPackageID` | Target package ID (if applicable) | SPEC.md Section 6.2 |
| 12 | `TargetDeliverableID` | Target deliverable ID (if `TargetType=DELIVERABLE`) | SPEC.md Section 6.8 |
| 13 | `TargetRefID` | Target reference ID (for non-deliverable targets) | SPEC.md Section 6.2 |
| 14 | `TargetName` | Human-readable target name | SPEC.md Section 6.2 |
| 15 | `Statement` | Dependency relationship statement | SPEC.md Section 6.2 |
| 16 | `EvidenceFile` | Source document filename | SPEC.md Section 6.5 |
| 17 | `SourceRef` | Path + section within evidence file | SPEC.md Section 6.5 |
| 18 | `EvidenceQuote` | Short quote (max 30 words) | SPEC.md Section 6.5 |
| 19 | `Confidence` | `HIGH`, `MEDIUM`, or `LOW` | SPEC.md Section 6.3 |
| 20 | `Origin` | `DECLARED` or `EXTRACTED` | SPEC.md Section 6.3 |
| 21 | `Explicitness` | `EXPLICIT` or `IMPLICIT` | SPEC.md Section 6.3 |
| 22 | `Status` | `ACTIVE` or `RETIRED` | SPEC.md Section 6.3 |
| 23 | `SatisfactionStatus` | Dependency satisfaction state | SPEC.md Section 6.3 |
| 24 | `FirstSeen` | ISO date of first extraction | SPEC.md Section 6.6 |
| 25 | `LastSeen` | ISO date of most recent confirmation | SPEC.md Section 6.6 |
| 26 | `FromDeliverableType` | Type classification of source deliverable | SPEC.md Section 6.2 |
| 27 | `TargetDeliverableType` | Type classification of target deliverable | SPEC.md Section 6.2 |
| 28 | `Notes` | Free-text notes | SPEC.md Section 6.2 |
| 29 | `ConflictFlag` | Conflict indicator | SPEC.md Section 6.2 |

**Note:** Column names and canonical order are derived from SPEC.md Section 6.2. The exact column order and descriptions above are **ASSUMPTION** based on the schema summary data available in the Specification and Datasheet; the authoritative column-by-column specification is in `docs/SPEC.md` Section 6.2 (**location TBD** for precise column-order verification). This enumeration satisfies lensing items B-001, B-002, C-001, and F-001 by providing an in-deliverable column reference.

### _DEPENDENCIES.md Structure

| Attribute | Value | Source |
|-----------|-------|--------|
| Ownership zones | 2 (Human-owned, Agent-owned) | SPEC.md Section 5.1 |
| Tracking modes | 3 (`NOT_TRACKED`, `DECLARED`, `TRACKED`) | SPEC.md Section 5.3 |
| Human-owned sections | Tracking Mode, Declared Upstream, Declared Downstream | SPEC.md Section 5.2 |
| Agent-owned sections | Extracted Register, Run Notes, Lifecycle Summary, Consumer Handoff | SPEC.md Section 5.2 |

### Provenance Requirements

| Attribute | Value | Source |
|-----------|-------|--------|
| `EvidenceFile` | MUST per active row (or `location TBD`) | SPEC.md Section 6.5; CONTRACT K-PROV-1 |
| `SourceRef` | MUST per active row (or `location TBD`) | SPEC.md Section 6.5; CONTRACT K-PROV-1 |
| `EvidenceQuote` | SHOULD (max 30 words) | SPEC.md Section 6.5 |
| `FirstSeen` / `LastSeen` | MUST (ISO date) | SPEC.md Section 6.6 |

### Identity Rules

| Attribute | Value | Source |
|-----------|-------|--------|
| DependencyID format | `DEP-{PKG}-{DEL}-{SEQ}` | SPEC.md Section 6.8 |
| DependencyID uniqueness scope | Within single deliverable register | SPEC.md Section 6.8 |
| `FromDeliverableID` constraint | MUST match host deliverable ID | SPEC.md Section 6.8 |
| ANCHOR IMPLEMENTS_NODE per deliverable | Exactly one SHOULD exist | SPEC.md Section 6.4 |

### SatisfactionStatus Transition Rules

| Attribute | Value | Source |
|-----------|-------|--------|
| Valid transitions | See Specification REQ-21 | SPEC.md Section 6.3 (**location TBD** — transition rules inferred from enum semantics) |
| Transition authority | TBD — human or agent depending on satisfaction type | **ASSUMPTION** |
| Initial state | `TBD` for new rows | SPEC.md Section 6.3 (implied by enum ordering) |

---

## Conditions

| Condition | Detail | Source |
|-----------|--------|--------|
| Authoritative location | Deliverable-local only; no central dependency graph | CONTRACT K-DEP-1 |
| Aggregation method | On-demand via `_Reconciliation/` | CONTRACT K-DEP-1 |
| Target resolution | Must resolve to existing deliverable IDs; unresolvable use `TargetType=UNKNOWN` | CONTRACT K-DEP-2 |
| Rows are never deleted | Unobserved rows marked `RETIRED`, not removed | SPEC.md Section 6.6 |
| Legacy compatibility | `INBOUND` -> `UPSTREAM`; `OUTBOUND` -> `DOWNSTREAM`; add `RegisterSchemaVersion` on write | SPEC.md Section 6.7 |
| Unknown values | Become `TBD`, not guessed | CONTRACT K-INVENT-1 |
| Conflict handling | Surfaced, not silently resolved | CONTRACT K-CONFLICT-1 |
| Row count monotonicity | Total row count (ACTIVE + RETIRED) MUST NOT decrease across extraction runs; the first extraction run establishes the baseline (row count = 0 prior to first run) | SPEC.md Section 6.6 (inferred from no-deletion rule) |

---

## Construction

### File Locations

| File | Path Pattern | Created By |
|------|-------------|------------|
| `_DEPENDENCIES.md` | `{PKG}/1_Working/{DEL}/_DEPENDENCIES.md` | PREPARATION agent |
| `Dependencies.csv` | `{PKG}/1_Working/{DEL}/Dependencies.csv` | DEPENDENCIES agent |

### Agent Interactions

| Agent | Role | Source |
|-------|------|--------|
| PREPARATION | Creates `_DEPENDENCIES.md` with human-owned sections | SPEC.md Section 5 |
| DEPENDENCIES | Populates agent-owned sections in `_DEPENDENCIES.md`; creates/updates `Dependencies.csv` | SPEC.md Section 5.1 |
| RECONCILIATION | Reads dependency registers (read-only aggregation) | CONTRACT K-DEP-1 |
| 4_DOCUMENTS | Reads `_DEPENDENCIES.md` for deliverable context; does not modify | 4_DOCUMENTS protocol |

### Related Deliverables

| Deliverable | Relationship | Source |
|-------------|-------------|--------|
| DEL-05-02 (Execution Root Scaffolding + Layout Conformance) | Establishes the folder structure in which dependency files reside | Decomposition (SOW-014, SOW-015) |
| DEL-05-03 (Lifecycle State Handling) | `_STATUS.md` lifecycle interacts with dependency extraction timing | Decomposition (SOW-016) |
| DEL-08-02 (Dependencies.csv v3.1 Schema Linter) — TBD scope | Would validate Dependencies.csv against v3.1 schema | Decomposition (SOW-033) |
| DEL-08-04 (On-demand Dependency Graph Generator) — TBD scope | Would aggregate local registers into project graph | Decomposition (SOW-035) |
| DEL-08-07 (Staleness Propagation + Triage Tooling) — TBD scope | Would use dependency edges for staleness calculation | Decomposition (SOW-038) |

---

## Documentation

### Required Artifacts

| Artifact Type | Description | Status | Location |
|---------------|-------------|--------|----------|
| DOC | Dependency tracking contract documentation (this document kit) | This deliverable | `DEL-05-04_Dependency_Tracking_Contract/` |
| CODE | Integration glue: file generation, validation, read/write logic for `_DEPENDENCIES.md` and `Dependencies.csv` | TBD | TBD — *codebase path and naming conventions to be determined by human/WORKING_ITEMS during implementation* |
| TEST | Schema conformance tests, provenance enforcement tests, identity rule tests, lifecycle tracking tests | TBD | TBD — *test directory path and naming conventions to be determined by human/WORKING_ITEMS during implementation* |

**Note:** CODE and TEST artifact locations are pending human decision on codebase organization. This is recorded as a TBD_Question (lensing items A-003, F-002). Production triggers and timeline for CODE/TEST artifacts are also TBD.

---

## References

| Reference | Relevance |
|-----------|-----------|
| `docs/SPEC.md` Sections 5, 6 | Authoritative schema and format specification for `_DEPENDENCIES.md` and `Dependencies.csv` v3.1 |
| `docs/CONTRACT.md` K-DEP-1, K-DEP-2, K-PROV-1, K-INVENT-1, K-CONFLICT-1 | Binding invariants governing dependency tracking |
| `docs/TYPES.md` Section 3 | Canonical dependency vocabulary (classes, types, directions, confidence, provenance) |
| `docs/DIRECTIVE.md` Section 2.1, 2.4 | "Filesystem is the database" principle; evidence-over-plausibility philosophy |
| `docs/PLAN.md` Sections 3.1–3.7 | Future hardening candidates that depend on this contract |
| Decomposition (G7-APPROVED) DEL-05-04 entry | Deliverable definition: scope, type, anticipated artifacts |
