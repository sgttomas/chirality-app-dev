# Guidance — DEL-05-04: Dependency Tracking File Contract (v3.1)

---

## Purpose

This deliverable exists because the Chirality execution model requires a **deliverable-local, filesystem-native dependency tracking mechanism** that is auditable, portable, and compatible with the "filesystem is the database" principle (DIRECTIVE Section 2.1).

Dependencies in this system serve two fundamental roles:
1. **ANCHOR edges** — connect each deliverable to the project's definition tree (parent package, traced requirements), preserving stable intent.
2. **EXECUTION edges** — capture information flow, prerequisites, handoffs, and constraints between work items, enabling sequencing, blocker detection, and impact analysis.

Together, these form a knowledge graph where the tree preserves structure and the DAG captures execution couplings (TYPES.md Section 3.1). The dependency tracking contract defined by this deliverable is the mechanism that makes this graph exist as auditable, version-controlled files rather than ephemeral runtime state.

Source: DIRECTIVE Section 2.1; TYPES.md Section 3; CONTRACT K-DEP-1.

---

## Principles

### P1: Deliverable-Local Authority (No Central Graph)

The system intentionally avoids a central dependency graph to eliminate sync burden. Each deliverable maintains its own `_DEPENDENCIES.md` and `Dependencies.csv`, and these local files are the authoritative source for that deliverable's dependency information. Project-level views are produced on-demand by aggregation (via `_Reconciliation/`), never by maintaining a separate master copy.

This means:
- **Consistency is eventual**, not transactional. Two deliverables may temporarily disagree about their mutual relationship until both are re-extracted.
- **Ownership is clear.** The DEPENDENCIES agent writes to one deliverable at a time. There is no multi-file atomic commit requirement.
- **Portability is preserved.** A deliverable folder can be moved, archived, or shared independently because its dependency data travels with it.

Source: CONTRACT K-DEP-1; DIRECTIVE Section 5 (Structural Constraints table: "Deliverable-local dependency registers").

### P2: Provenance Is Non-Negotiable

Every extracted dependency row must cite evidence. This is not a nice-to-have; it is a binding invariant (K-PROV-1). The provenance chain is: `EvidenceFile` -> `SourceRef` -> `EvidenceQuote`. When exact location is unknown, `location TBD` is acceptable; when evidence does not exist, the dependency should not be asserted.

This serves the "evidence over plausibility" philosophy (DIRECTIVE Section 2.4): the system does not accept "sounds right" as a basis for dependency claims.

Source: CONTRACT K-PROV-1; DIRECTIVE Section 2.4.

### P3: Two-Class Edge Model (ANCHOR + EXECUTION)

The distinction between ANCHOR and EXECUTION rows is not cosmetic. ANCHOR rows establish where a deliverable sits in the project's definition tree — they answer "what is this deliverable and why does it exist?" EXECUTION rows capture operational couplings — they answer "what information flows between deliverables and in what order?"

Mixing these concerns (e.g., using EXECUTION rows for traceability, or ANCHOR rows for sequencing) undermines the graph's utility for both structural analysis and execution planning.

Source: SPEC.md Section 6.4; TYPES.md Section 3.1.

### P4: Rows Are Append-Only (Retirement, Not Deletion)

Rows are never deleted from `Dependencies.csv`. When a dependency is no longer observed in source text, it is marked `RETIRED` with `LastSeen` set to the date of the extraction run that no longer found it. This preserves the historical record for audit and enables detection of dependencies that were lost unintentionally.

Source: SPEC.md Section 6.6.

### P5: Dual Ownership in `_DEPENDENCIES.md`

The `_DEPENDENCIES.md` file has a split personality by design. Human-owned sections (Declared Upstream/Downstream) capture deliberate, human-declared dependency decisions. Agent-owned sections (Extracted Register, Run Notes) capture what the DEPENDENCIES agent found by reading the deliverable's documents and references.

Neither zone overrides the other. Human declarations are constraints; agent extractions are evidence. When they disagree, the conflict should be surfaced (K-CONFLICT-1), not silently resolved.

Source: SPEC.md Section 5.1; CONTRACT K-CONFLICT-1.

---

## Considerations

### C1: Context Envelope Sizing

This deliverable is rated `L` (Large) because it "may touch multiple surfaces (file generation + validation + ingestion)" (Decomposition Context Budget QA). The contract itself is well-defined in SPEC.md, but the implementation touches:
- **PREPARATION agent** — creates `_DEPENDENCIES.md` scaffold.
- **DEPENDENCIES agent** — populates agent-owned sections and creates `Dependencies.csv`.
- **Downstream consumers** — RECONCILIATION, estimating, and (TBD) staleness tooling must correctly read the v3.1 schema.
- **Validation** — schema conformance tests must cover all 29 core columns, enum values, provenance rules, and identity rules.

If scope expands beyond "contract + minimal integration glue," the decomposition recommends splitting (Decomposition DEL-05-04 ContextEnvelopeNotes).

Source: Decomposition DEL-05-04 entry.

### C2: Relationship to TBD Hardening Items

Several TBD-scope deliverables in PKG-08 depend on the dependency tracking contract:
- DEL-08-02 (Schema Linter) — would validate `Dependencies.csv` against v3.1 schema (SOW-033).
- DEL-08-04 (Graph Generator) — would aggregate local registers into a project graph (SOW-035).
- DEL-08-07 (Staleness Tooling) — would use dependency edges for change propagation (SOW-038).

These are currently TBD and not in scope for this deliverable. However, the contract defined here must be stable enough to support them if they come into scope.

Source: Decomposition PKG-08 deliverables; PLAN Section 3.

### C3: Legacy Compatibility

The v3.1 schema includes explicit legacy compatibility rules (SPEC.md Section 6.7):
- `INBOUND` normalizes to `UPSTREAM`; `OUTBOUND` normalizes to `DOWNSTREAM`.
- Missing `RegisterSchemaVersion` is added on write.

Implementations should handle legacy data gracefully during reads and normalize on writes, rather than rejecting legacy files outright.

Source: SPEC.md Section 6.7.

### C4: Extension Column Forward Compatibility

The schema permits extension columns (`EstimateImpactClass`, `ConsumerHint`) that MAY be present. The contract requires that their absence does not break readers. This means:
- **Writers** may add extension columns if the consuming context requires them.
- **Readers** must not fail if extension columns are missing.
- **New extension columns** may be introduced without a schema version bump, as long as they follow the non-breaking rule.

Source: SPEC.md Section 6.2.

### C5: Interaction with `_STATUS.md` Lifecycle

Dependency extraction timing interacts with the deliverable lifecycle:
- At `OPEN` state, `_DEPENDENCIES.md` exists but is unpopulated (PREPARATION scaffold only).
- At `INITIALIZED` or later, the document kit exists and the DEPENDENCIES agent can extract from it.
- Re-extraction may occur at any state after `INITIALIZED` when source documents change.

The DEPENDENCIES agent should not require a specific lifecycle state to run, but the quality and completeness of extraction will vary with deliverable maturity.

**ASSUMPTION:** The DEPENDENCIES agent can run against deliverables at any state >= `INITIALIZED`, but results at early states will contain more `TBD` and `location TBD` entries.

### C6: Responsible Party Assignment

The `Responsible Party` field in the Datasheet is currently TBD. Assignment criteria should consider:
- Who has authority over the dependency tracking schema and its evolution (schema governance).
- Who maintains the integration glue code (PREPARATION and DEPENDENCIES agent logic).
- Whether responsibility is split between contract definition (governance owner) and implementation (code owner).

This is a human decision that cannot be inferred from available sources.

### C7: Consumer Handoff Notes Content

The Consumer Handoff Notes section in `_DEPENDENCIES.md` (REQ-02, agent-owned) is intended to provide downstream consumers with actionable guidance. Expected content includes:

- **Interface stability notes** — which aspects of this deliverable's outputs are stable vs. evolving.
- **Data quality caveats** — known limitations of the current extraction (e.g., high `TBD` count, low confidence rows).
- **Consumer recommendations** — how downstream agents or tools should filter, interpret, or validate the dependency data.

The DEPENDENCIES agent populates this section during extraction runs. The format is free-form markdown within the agent-owned zone.

Source: SPEC.md Section 5.2 (section listed as agent-owned); content expectations are **ASSUMPTION** based on the section's name and placement.

---

## Trade-offs

### T1: Local Authority vs. Global Consistency

**Choice:** Deliverable-local registers with on-demand aggregation (no central graph).
**Pro:** Clear ownership, no sync burden, portable deliverable folders, simple write model.
**Con:** Temporary inconsistencies between deliverables are possible; project-level views require aggregation runs.
**Rationale:** The sync burden of a central graph would undermine the "filesystem is the database" principle and create a coordination bottleneck. On-demand aggregation is acceptable because project-level dependency analysis is an infrequent, human-triggered operation.

Source: CONTRACT K-DEP-1; DIRECTIVE Section 5.

### T2: Append-Only Rows vs. Clean Registers

**Choice:** Rows are never deleted; only marked `RETIRED`.
**Pro:** Full audit trail; accidental dependency loss is detectable; historical record is preserved.
**Con:** Register files grow over time; retired rows add noise for readers.
**Rationale:** The audit trail value outweighs the noise cost. Readers can filter on `Status=ACTIVE` to see only current dependencies.

Source: SPEC.md Section 6.6.

### T3: Dual Ownership vs. Single Authority

**Choice:** `_DEPENDENCIES.md` has human-owned and agent-owned sections.
**Pro:** Humans can declare intent; agents can extract evidence; both coexist without overwriting each other.
**Con:** Disagreements between human declarations and agent extractions must be surfaced and resolved.
**Rationale:** The alternative (single authority) would either prevent human input or lose agent-extracted evidence. The hybrid model respects both sources and requires explicit conflict resolution (K-CONFLICT-1).

Source: SPEC.md Section 5.1; CONTRACT K-CONFLICT-1.

### T4: 29 Core Columns vs. Minimal Schema

**Choice:** A comprehensive 29-column core schema with provenance, lifecycle, and classification fields.
**Pro:** Supports full traceability, lifecycle tracking, and downstream analysis without schema extensions.
**Con:** High column count creates initial complexity for writers and validators.
**Rationale:** The provenance fields (EvidenceFile, SourceRef, EvidenceQuote) are required by K-PROV-1. The lifecycle fields (FirstSeen, LastSeen, Status) enable the append-only model. The classification fields (DependencyClass, AnchorType, Direction, DependencyType) enable the two-class edge model. Removing any of these would weaken a contract commitment.

Source: SPEC.md Section 6.2; CONTRACT K-PROV-1.

### T5: REQ-04 SHOULD Level vs. MUST Level

**Choice:** `Dependencies.csv` presence is SHOULD (not MUST) when tracking mode is `TRACKED`.
**Pro:** Allows a transitional state where `_DEPENDENCIES.md` declares `TRACKED` mode but the DEPENDENCIES agent has not yet run, without creating a hard validation failure.
**Con:** A deliverable can remain in `TRACKED` mode indefinitely without a `Dependencies.csv` file, which weakens enforcement.
**Rationale:** The SHOULD level is sourced directly from SPEC.md Section 2.1. The transitional state is legitimate because PREPARATION sets tracking mode during scaffolding, but the DEPENDENCIES agent runs later. Elevating to MUST would require a SPEC amendment and would create false-positive validation failures during the scaffolding-to-first-extraction window.

Source: SPEC.md Section 2.1; Decomposition DEL-05-04 entry (context envelope notes on multi-surface touchpoints).

---

## SHOULD-Level Governance Threshold

The deliverable uses both MUST and SHOULD normative levels. The governance threshold for SHOULD-level requirements is:

- **SHOULD failures are advisory warnings**, not hard blockers during automated verification.
- **SHOULD failures are tracked** and reported in verification output, but they do not prevent a deliverable from passing automated checks.
- **SHOULD failures become review items** during manual review (REQ-18/19/20 scope) — a reviewer should assess whether the SHOULD gap is acceptable or indicates a quality issue.
- **Affected requirements:** REQ-04 (Dependencies.csv presence), REQ-09 partial (exactly one IMPLEMENTS_NODE), REQ-12 (EvidenceQuote presence).

This interpretation aligns with the standard IETF RFC 2119 semantics for SHOULD: "there may exist valid reasons in particular circumstances to ignore a particular item, but the full implications must be understood and carefully weighed before choosing a different course."

Source: SPEC.md Section 2.1 (normative levels used); RFC 2119 semantics (**ASSUMPTION** — SPEC.md does not explicitly define SHOULD interpretation, so RFC 2119 is applied as the conventional default).

---

## Quality Acceptance Criteria

The following measurable quality thresholds apply to the dependency tracking contract deliverable and its outputs:

### Contract Documentation Quality

| Metric | Threshold | Rationale |
|--------|-----------|-----------|
| TBD count in Datasheet | Track and report; no hard ceiling | TBDs decrease as implementation proceeds |
| Requirements with source citations | 100% of REQ-* entries | Non-negotiable per K-PROV-1 philosophy |
| Cross-document terminology consistency | Zero unresolved inconsistencies | Verified during Pass 2 consistency sweep |

### Dependencies.csv Output Quality

| Metric | Threshold | Rationale |
|--------|-----------|-----------|
| ACTIVE rows with `EvidenceFile` populated | 100% (MUST per REQ-11) | K-PROV-1 binding invariant |
| ACTIVE rows with `EvidenceQuote` populated | >= 80% target (**ASSUMPTION** — no explicit threshold in SPEC.md) | Best-effort traceability; SHOULD-level |
| ACTIVE rows with `Confidence = HIGH` | Track and report; no hard floor | Quality signal for downstream consumers |
| `ConflictFlag` rows resolved | Track and report per extraction run | K-CONFLICT-1 requires surfacing, not necessarily resolution |

### Manual Review Acceptance

| Metric | Threshold | Rationale |
|--------|-----------|-----------|
| REQ-18 (architecture review) pass | Binary pass/fail per review protocol | See Manual Review Protocols below |
| REQ-19 (no invented content) pass | Zero unsourced assertions found in sample | See Manual Review Protocols below |
| REQ-20 (conflict surfacing) pass | Zero hidden resolutions found in review | See Manual Review Protocols below |

Source: CONTRACT K-PROV-1; SPEC.md Section 6.5. Thresholds marked **ASSUMPTION** are proposed by this document kit and await human confirmation.

---

## Manual Review Protocols

The three manual-review requirements (REQ-18, REQ-19, REQ-20) require defined review procedures to be actionable. The following checklists provide the review protocol for each.

### REQ-18: Architecture Review Protocol (Deliverable-Local Authority)

**Objective:** Confirm that no central dependency graph exists and that local registers are authoritative.

**Checklist:**

1. Verify that no file matching a central dependency graph pattern exists at the execution root (e.g., no `dependencies.json`, `dependency_graph.*`, or similar at `{EXECUTION_ROOT}/`).
2. Verify that `_Reconciliation/` outputs (if any) are read-only snapshots produced by aggregation, not maintained as authoritative state.
3. Verify that the DEPENDENCIES agent writes only to the target deliverable's local folder (no cross-deliverable writes in a single run).
4. Verify that the RECONCILIATION agent reads local registers without modifying them.

**Pass criteria:** All four checks pass. Any failure requires investigation and remediation.

Source: CONTRACT K-DEP-1.

### REQ-19: No Invented Content Review Protocol

**Objective:** Confirm that no unsourced assertions exist in dependency data.

**Checklist:**

1. Sample at least 20% of ACTIVE rows (minimum 5 rows, or all rows if fewer than 5 exist).
2. For each sampled row, verify that `EvidenceFile` points to a real, accessible document.
3. For each sampled row, verify that `SourceRef` identifies a specific location within the evidence file that supports the `Statement`.
4. For any row where `EvidenceFile` or `SourceRef` is `location TBD`, verify that the `Statement` is a reasonable inference (not an invention) and that the TBD is tracked for resolution.
5. Verify that no `Statement` text contains claims not supported by any cited or inferrable source.

**Pass criteria:** Zero unsourced assertions found in the sample. Any failure is a K-INVENT-1 violation.

Source: CONTRACT K-INVENT-1.

### REQ-20: Conflict Surfacing Review Protocol

**Objective:** Confirm that no conflicts were silently resolved.

**Checklist:**

1. Check the `ConflictFlag` column for any flagged rows; verify each flagged conflict is documented (in the register's `Notes` column, in `_MEMORY.md`, or in the Conflict Table).
2. Compare human-declared dependencies (Declared Upstream/Downstream in `_DEPENDENCIES.md`) against agent-extracted dependencies for contradictions.
3. If contradictions exist, verify they are surfaced in the Conflict Table or equivalent documentation.
4. Verify that no dependency was silently dropped or silently added to resolve a disagreement.

**Pass criteria:** All identified conflicts are documented with pointers to both sources. Zero hidden resolutions found.

Source: CONTRACT K-CONFLICT-1.

---

## Examples

### Example: Minimal `_DEPENDENCIES.md` (PREPARATION scaffold)

```markdown
# Dependencies: DEL-05-04 Dependency Tracking File Contract (v3.1)

## Dependency Tracking Mode
- **Mode:** TRACKED
- **Register:** Dependencies.csv (schema v3.1)

---

## Declared Upstream (I need these before I can proceed)
Dependencies coordinated externally by humans.

## Declared Downstream (These need me)
Dependencies coordinated externally by humans.

---

## Extracted Dependency Register
*Dependency extraction has not yet been run for this deliverable.*

---

## Lifecycle Summary
*Not yet populated.*

---

## Run Notes
*Not yet populated.*

## Run History
*No runs yet.*

## Consumer Handoff Notes
*Not yet populated.*
```

Source: SPEC.md Section 5.2 (schema template). Consumer Handoff Notes section added per REQ-02.

### Example: ANCHOR Row (IMPLEMENTS_NODE)

| Column | Value |
|--------|-------|
| RegisterSchemaVersion | v3.1 |
| DependencyID | DEP-05-04-001 |
| FromPackageID | PKG-05 |
| FromDeliverableID | DEL-05-04 |
| FromDeliverableName | Dependency Tracking File Contract (v3.1) |
| DependencyClass | ANCHOR |
| AnchorType | IMPLEMENTS_NODE |
| Direction | UPSTREAM |
| DependencyType | OTHER |
| TargetType | PACKAGE |
| TargetPackageID | PKG-05 |
| TargetDeliverableID | |
| TargetRefID | PKG-05 |
| TargetName | Filesystem Execution Model |
| Statement | DEL-05-04 implements a component of the Filesystem Execution Model package |
| EvidenceFile | ChiralityApp_SoftwareDecomposition_2026-02-21_G7-APPROVED.md |
| SourceRef | Decomposition > PKG-05 Deliverables table |

Source: Derived from SPEC.md Section 6.4 rules and Decomposition DEL-05-04 entry. Values shown are illustrative of the ANCHOR row pattern.

### Example: EXECUTION Row (PREREQUISITE)

| Column | Value |
|--------|-------|
| RegisterSchemaVersion | v3.1 |
| DependencyID | DEP-05-04-010 |
| FromPackageID | PKG-05 |
| FromDeliverableID | DEL-05-04 |
| FromDeliverableName | Dependency Tracking File Contract (v3.1) |
| DependencyClass | EXECUTION |
| AnchorType | NOT_APPLICABLE |
| Direction | UPSTREAM |
| DependencyType | PREREQUISITE |
| TargetType | DELIVERABLE |
| TargetPackageID | PKG-05 |
| TargetDeliverableID | DEL-05-02 |
| TargetRefID | |
| TargetName | Execution Root Scaffolding + Layout Conformance |
| Statement | Folder structure must exist before dependency files can be placed |
| EvidenceFile | docs/SPEC.md |
| SourceRef | SPEC.md > Section 2 (Deliverable Folder Layout) |

Source: Derived from SPEC.md Section 2 and Decomposition relationship between DEL-05-02 and DEL-05-04. Values shown are illustrative of the EXECUTION row pattern.

---

## Conflict Table (for human ruling)

| Conflict ID | Conflict | Source A | Source B | Impacted sections | Proposed authority (PROPOSAL) | Human ruling |
|---|---|---|---|---|---|---|
| CONF-001 | REQ-21 SatisfactionStatus transition rules are inferred from enum semantics but not explicitly specified in SPEC.md | Specification.md REQ-21 (inferred) | SPEC.md Section 6.3 (enum definition only, no transitions) | Specification REQ-21; Datasheet SatisfactionStatus Transition Rules | `docs/SPEC.md` — if transitions are to be normative, they should be added to SPEC.md | TBD |
| CONF-002 | REQ-04 SHOULD level: SPEC.md says SHOULD for Dependencies.csv presence, but TRACKED mode semantically implies the file should exist; tension between spec-as-written and user expectation | Specification.md REQ-04 | SPEC.md Section 2.1 (File Inventory table) | Specification REQ-04; Guidance T5 | `docs/SPEC.md` — normative level should match the authoritative source | TBD |
