# Datasheet — DEL-08-04 On-demand Dependency Graph Generator

## Identification

| Field | Value |
|-------|-------|
| **Deliverable ID** | DEL-08-04 |
| **Name** | On-demand Dependency Graph Generator |
| **Package** | PKG-08 — Optional Integrity Hardening |
| **Type** | BACKEND_FEATURE_SLICE |
| **Responsible Party** | TBD — No responsible party assigned; requires human decision (no resolution path currently noted) |
| **Context Envelope** | M |
| **Scope Coverage** | SOW-035 |
| **Supports Objectives** | OBJ-007 |
| **Scope Item Status** | TBD (scope not yet flipped IN; see Open Issue OI-035) |
| **Anticipated Artifacts** | SCRIPT / OTHER / DOC |

> [Lensing: B-001] Responsible Party is an essential identification attribute with no current assignment or decision path. Requires human decision.

## Attributes

| Attribute | Value | Source |
|-----------|-------|--------|
| Input format | `Dependencies.csv` (v3.1 schema) | SPEC.md Section 6; Decomposition DEL-08-04 |
| Input location | `{EXECUTION_ROOT}/PKG-*/1_Working/DEL-*/Dependencies.csv` per deliverable | SPEC.md Section 2.1 |
| Input schema columns (v3.1) | `RegisterSchemaVersion`, `DependencyID`, `FromDeliverableID`, `TargetDeliverableID`, `TargetType`, `DependencyClass`, `DependencyType`, `Direction`, `Confidence`, `Status`, `AnchorType`, `Provenance`, `Notes` | SPEC.md Section 6.2 (**ASSUMPTION** — full column enumeration inferred from SPEC.md Section 6 references; exact column list location TBD) |
| Output formats | JSON graph artifact and/or Mermaid diagram | Decomposition DEL-08-04 description |
| Output location | TBD — requires human design decision; candidates: `_Aggregation/`, `_Scripts/`, stdout, `_Reconciliation/` (see Guidance C-04) | **ASSUMPTION**; gates Specification REQ-13, Procedure Steps A.6/A.10 |
| Execution mode | On-demand (not persistent; no central graph maintained) | CONTRACT.md K-DEP-1; PLAN.md Section 3.4 |
| Graph model | Directed Acyclic Graph (DAG) from EXECUTION rows; tree edges from ANCHOR rows | TYPES.md Section 3.1; SPEC.md Section 6.4 |
| Node identity | Deliverable IDs (`DEL-XX-YY`) | SPEC.md Section 6.8 |
| Edge identity | Dependency IDs (`DEP-XX-YY-NNN`) | SPEC.md Section 6.8 |
| Edge direction | `UPSTREAM` / `DOWNSTREAM` relative to host deliverable | TYPES.md Section 3.3 |
| Dependency classes supported | `ANCHOR` (tree) + `EXECUTION` (DAG) | TYPES.md Section 3.1 |
| Schema version required | `v3.1` | SPEC.md Section 6.1 |
| Platform | macOS 15+, Apple Silicon only | Decomposition DEC-PLAT-001 |
| Language/runtime | TBD — human design decision required (anticipated: script — Python, Node.js, or shell); this decision gates downstream normative specification of dependencies, build steps, and CLI interface | **ASSUMPTION** based on artifact type SCRIPT |

> [Lensing: A-001] Language/runtime remains a blocking TBD: the prescriptive direction for implementation cannot be finalized until this decision is made.
>
> [Lensing: B-002] Input schema columns now enumerated to make the Datasheet self-contained on input schema (previously required consulting SPEC.md Section 6 directly).
>
> [Lensing: D-002] Output location TBD is a cross-cutting decision that gates Specification REQ-13, Procedure Steps A.6/A.10, and Guidance C-04.

## Conditions

| Condition | Detail | Source |
|-----------|--------|--------|
| Scope status | SOW-035 is currently TBD; this deliverable is contingent on scope flip to IN | Decomposition Scope Ledger |
| No central graph invariant | System intentionally avoids a persistent central dependency graph (K-DEP-1); this tool generates on-demand only | CONTRACT.md K-DEP-1 |
| Existing registers required | At least one deliverable-local `Dependencies.csv` must exist for meaningful output | **ASSUMPTION** |
| ID resolution | Dependency references to deliverables must resolve to existing deliverable IDs (K-DEP-2) | CONTRACT.md K-DEP-2 |
| Network policy | No outbound network access required (local filesystem traversal only) | DIRECTIVE.md Section 5; DEC-NET-001 |
| Downstream consumers | DEL-08-07 (Staleness Propagation + Triage Tooling) depends on this graph output | Decomposition DEL-08-07; PLAN.md Section 3.7 |
| Upstream tool relationship | TBD — whether DEL-08-02 (Dependencies.csv Linter) and DEL-08-03 (Folder Structure Validator) are execution prerequisites for this deliverable is undecided; the graph generator excludes their scope but does not specify whether it assumes valid inputs | Specification Scope > Excluded; **ASSUMPTION** — requires human ruling |

> [Lensing: F-003] Upstream tool relationship added as a condition. The graph generator's behavior with invalid register data is underspecified if DEL-08-02/DEL-08-03 have not been run.

## Construction

| Aspect | Detail | Source |
|--------|--------|--------|
| Graph traversal | Walk all `Dependencies.csv` files under `{EXECUTION_ROOT}/PKG-*/1_Working/DEL-*/` | SPEC.md Sections 1, 2; PLAN.md Section 3.4 |
| Row filtering | Include `ACTIVE` rows; exclude `RETIRED` rows | SPEC.md Section 6.6 |
| Node extraction | Each unique `FromDeliverableID` and resolved `TargetDeliverableID` becomes a graph node | SPEC.md Section 6.8 |
| Edge extraction | Each EXECUTION row becomes a directed edge; ANCHOR rows form tree edges | SPEC.md Section 6.4 |
| Direction normalization | Legacy `INBOUND`/`OUTBOUND` values MUST be normalized to `UPSTREAM`/`DOWNSTREAM` on read | SPEC.md Section 6.7; TYPES.md Section 3.3 |
| Cycle detection | Graph generator MUST detect and report cycles in EXECUTION edges | PLAN.md Section 3.4 ("cycle detection"); Specification REQ-09 |
| JSON output schema | TBD (nodes array + edges array + metadata + analysis is anticipated minimum; see Specification REQ-07 and Procedure Step A.2 for proposed schema) | **ASSUMPTION** |
| Mermaid output | TBD (flowchart or graph TD syntax anticipated) | **ASSUMPTION** |
| Error handling | Unresolvable targets reported with `TargetType=UNKNOWN` per K-DEP-2 | CONTRACT.md K-DEP-2 |
| Immutability consideration | If output is written to a tool root, snapshot immutability applies (K-SNAP-1) | CONTRACT.md K-SNAP-1 |

## References

| Ref | Document | Relevance |
|-----|----------|-----------|
| 1 | Decomposition (G7-APPROVED), DEL-08-04 entry | Deliverable definition |
| 2 | `docs/SPEC.md` Section 6 | Dependencies.csv v3.1 schema (input format) |
| 3 | `docs/SPEC.md` Sections 1-2 | Execution root layout, deliverable folder structure |
| 4 | `docs/TYPES.md` Section 3 | Dependency vocabulary (classes, directions, types) |
| 5 | `docs/CONTRACT.md` K-DEP-1, K-DEP-2, K-SNAP-1 | Invariants governing dependency graph and snapshots |
| 6 | `docs/PLAN.md` Section 3.4 | Feature description and rationale |
| 7 | `docs/PLAN.md` Section 3.7 | Downstream dependency (staleness tooling) |
