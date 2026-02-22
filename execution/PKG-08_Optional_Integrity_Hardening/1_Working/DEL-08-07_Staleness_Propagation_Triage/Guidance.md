# Guidance — DEL-08-07 Staleness Propagation + Triage Tooling

## Purpose

This deliverable exists to make the system's staleness and integrity guarantees enforceable rather than aspirational. CONTRACT invariants K-STALE-1 and K-STALE-2 commit the system to transitive staleness propagation and human triage, but currently these rely entirely on human observation. Automated staleness detection from the dependency graph plus git SHAs would close this governance gap. (PLAN Section 3.7)

This is the final link in the integrity hardening chain described in PLAN Section 4: schema linter and folder validator provide structural integrity; content hashes provide reference integrity; the dependency graph provides relational integrity; run records provide temporal integrity; and staleness propagation provides **change-impact integrity** — the ability to know, with confidence, what is affected when something changes.

## Principles

### P1: Staleness is a Property of Evidence, Not a Judgment

A deliverable is stale when its governed inputs have changed since its last approved baseline. This is a factual determination based on SHA comparison, not a qualitative assessment. The tooling should compute staleness mechanically and present it neutrally — the human decides what it means for their project. (CONTRACT K-VAL-1; DIRECTIVE Section 2.4)

### P2: Propagation Must Be Conservative

Transitive propagation should mark all reachable dependents as potentially stale. It is better to flag an item that turns out unaffected (human clears it as "no impact") than to miss a genuinely stale item. Under-reporting staleness undermines the integrity guarantee. (CONTRACT K-STALE-1)

### P3: Triage is Human Authority

The tooling presents staleness facts; the human decides the response. The three resolution modes (no impact, needs rework, needs review) are the minimum vocabulary. The system must never auto-clear staleness flags or auto-assign resolution. (CONTRACT K-STALE-2; CONTRACT K-AUTH-1)

### P4: Outputs Must Be Auditable

Every staleness determination should be traceable to specific inputs: which baseline SHA, which current SHA, which dependency edge caused propagation. An auditor should be able to reproduce the result from the same inputs. (Decomposition notes: "deterministic/auditable"; DIRECTIVE Section 2.2)

### P5: On-Demand, Not Continuous

Consistent with the filesystem-as-state model, staleness calculation is an on-demand operation — invoked by the human when they want to know the current staleness picture. It is not a background service, webhook, or continuous monitoring system. (DIRECTIVE Section 2.1; DIRECTIVE Section 5)

## Considerations

### C1: Dependency on Upstream TBD Deliverables

This deliverable has the deepest dependency chain in PKG-08. Per PLAN Section 4 sequencing rationale:
- DEL-08-04 (dependency graph generation) must exist first to provide the edge data for traversal.
- DEL-08-06 (run records) must exist first to provide baseline SHAs.
- Both are also TBD scope (OI-035, OI-037).

**ASSUMPTION:** If any upstream deliverable is not brought IN scope, this deliverable cannot be implemented as designed. The human should resolve OI-035 and OI-037 before or concurrently with OI-038.

### C2: Graph Format Coupling

The staleness engine must parse the dependency graph format produced by DEL-08-04. If the graph format is not yet defined, the staleness engine risks being designed in a vacuum.

**Recommendation:** Define a minimal graph interchange format (likely JSON with nodes and edges arrays) as part of DEL-08-04, and consume that format here. Avoid tight coupling to visualization formats (Mermaid) for programmatic traversal.

### C3: SHA Granularity and Governed Input Definition

CONTRACT K-VAL-1 states a deliverable is dirty if "any governed input has changed since its last approved SHA." Two interrelated design questions must be resolved:

**Which files are governed inputs?** (Lensing: B-001, B-002)

This is a prerequisite for dirty detection (Specification REQ-01). Candidates:
- **Minimal set:** The four production documents (`Datasheet.md`, `Specification.md`, `Guidance.md`, `Procedure.md`) only.
- **Extended set:** Production documents plus `Dependencies.csv` and metadata files (`_CONTEXT.md`, `_DEPENDENCIES.md`, etc.).
- **Full folder:** All files in the deliverable folder.
- **Declared set:** A per-deliverable manifest listing which files are governed inputs.

**ASSUMPTION:** The specific governed-input definition will be defined during implementation or as part of DEL-08-06. The declared-manifest approach offers the most flexibility but adds complexity. The human or a cross-deliverable design decision (possibly involving DEL-08-04/DEL-08-06) is required.

**What SHA strategy?**

- **Folder-level SHA:** Hash of all files in the deliverable folder. Simple but coarse — any file change (including metadata updates) triggers dirty.
- **Content-file-level SHA:** Hash of individual governed files. More precise but requires the governed-input definition above.
- **Composite SHA:** A deterministic hash of all governed file hashes. Provides a single comparison point with file-level granularity.

**ASSUMPTION:** The composite approach (hash of hashes) is likely the best balance of precision and simplicity, contingent on the governed-input definition.

### C4: Edge Selection for Propagation

The dependency model has two edge classes (TYPES Section 3.1):
- **ANCHOR** (tree edges): Connect deliverables to definition/traceability nodes.
- **EXECUTION** (DAG edges): Capture information flow, prerequisites, handoffs, constraints.

**ASSUMPTION:** Staleness propagates along EXECUTION edges only. ANCHOR edges establish traceability but do not represent information flow that would cause staleness. If a scope item (SOW) changes, that is a decomposition change handled through change management, not staleness propagation.

### C5: Triage Record Persistence

CONTRACT K-STALE-2 requires human triage, but does not specify where triage decisions are recorded. Options:

- **In `_STATUS.md`:** Append a staleness triage entry to the history. Keeps lifecycle state authoritative but mixes staleness with lifecycle.
- **In a separate staleness artifact:** A `_STALENESS.md` or similar file per deliverable. Cleanly separated but adds another file to the deliverable folder.
- **In the staleness report (tool root):** Triage decisions recorded in the snapshot output. Clean for audit but less accessible during active work.

**ASSUMPTION:** TBD — this is a design decision for implementation. The separate artifact approach may be cleanest but requires SPEC amendment. See Conflict Table CONFLICT-01.

### C6: Cycle Detection

Dependency graphs should be acyclic (DAG), but cycles could exist due to data errors. The propagation algorithm must handle cycles gracefully — either detect and report them as errors, or use visited-node tracking to prevent infinite traversal.

### C7: Partial Graph and Missing Data — Edge-Case Staleness States

Not all deliverables may have `Dependencies.csv` files (tracking mode may be `NOT_TRACKED` or `DECLARED`). Additionally, some deliverables may lack run records (no baseline SHA).

**Standardized terminology for edge-case states** (Lensing: X-003, C-002):

| Edge-Case Condition | Canonical Term | Meaning |
|---|---|---|
| No baseline SHA exists (no run record for the deliverable) | **no baseline available** | Cannot determine dirty/clean; staleness status is indeterminate because there is no approved baseline to compare against |
| Deliverable has no `Dependencies.csv` data | **dependency data unavailable** | Cannot determine propagated staleness; direct dirty detection may still be possible if a baseline exists |
| Both conditions (no baseline + no dependency data) | **staleness indeterminate** | Neither direct dirty detection nor propagation analysis is possible |

**Note:** Previous drafts used "baseline unknown" (Procedure) and "staleness unknown" (Guidance) for overlapping situations. The terms above replace both with more precise vocabulary. All documents in this deliverable should use these canonical terms.

The staleness engine should:
- Process available edges.
- Report deliverables with missing dependency data as "dependency data unavailable" rather than silently assuming clean.
- Report deliverables without baselines as "no baseline available."

### C8: Failure Modes and Error Recovery (Lensing: X-002)

The happy-path workflow (invoke, detect, propagate, triage) is well-defined, but failure modes should also be considered:

- **Mid-run failure:** If the staleness calculation fails partway through (e.g., graph parsing succeeds but SHA computation fails for some deliverables), the tooling should not produce partial output that could be mistaken for a complete report. **ASSUMPTION: the tooling should either complete fully or fail cleanly with an error report indicating which step failed and what was processed.**
- **Retry semantics:** Since staleness calculation is on-demand and deterministic (REQ-04), a failed run can simply be re-invoked after the underlying issue is fixed. No rollback mechanism is needed for the calculation itself.
- **Corrupted state:** If a previous staleness report exists and a new run fails, the previous report remains valid as of its generation timestamp. The tooling should not overwrite a valid report with a failed-run artifact.

### C9: Report Lifecycle — Snapshot vs. Overwrite (Lensing: X-004)

Specification REQ-04 requires deterministic output and REQ-05 requires filesystem representation, but neither addresses whether staleness reports accumulate as versioned snapshots or overwrite in place.

- **Snapshot model (tool root):** Each run produces a new timestamped snapshot. Prior snapshots are immutable (per K-SNAP-1). This supports auditability — an auditor can see the staleness picture at any point in time.
- **Overwrite model (deliverable-local or single file):** Each run overwrites the previous report. Simpler but loses historical staleness data.

**ASSUMPTION:** If outputs go to a tool root, the snapshot model is mandatory per K-SNAP-1. If outputs are deliverable-local, the overwrite model is acceptable but loses audit history. See Conflict Table CONFLICT-02 for the output location decision.

### C10: Performance and Scale Expectations (Lensing: F-003)

No performance requirements are formally stated. However, the tooling should be designed with realistic scale expectations:

- **Target graph size:** The current decomposition contains 32 deliverables across 8 packages. The tooling should handle graph sizes of at least this order of magnitude comfortably. **ASSUMPTION: target at least 100 deliverables with proportional edge counts for forward compatibility.**
- **Execution time:** For a graph of 100 deliverables, staleness calculation (including SHA computation) should complete within a reasonable interactive timeframe. **ASSUMPTION: TBD — no formal SLA, but "interactive" suggests seconds, not minutes.**
- **Memory:** Graph traversal for a project of this scale should fit comfortably in memory. No explicit memory constraints are stated.

These are guidance-level expectations, not formal requirements. If formal non-functional requirements are warranted, they should be added to the Specification.

## Trade-offs

| Trade-off | Option A | Option B | Recommendation |
|-----------|----------|----------|----------------|
| **Propagation conservatism** | Flag only direct dependents (shallow) | Flag all transitive dependents (deep) | **Option B** — CONTRACT K-STALE-1 requires transitive propagation |
| **Output location** | Tool root (immutable snapshot) | Deliverable-local file | TBD — depends on whether staleness is a point-in-time report (tool root) or persistent state (local). See CONFLICT-02 |
| **Triage interface** | CLI text output | Structured markdown report | TBD — markdown report is more consistent with filesystem-as-state |
| **Graph format** | JSON (programmatic) | Mermaid (visual) | JSON for programmatic consumption; Mermaid as optional visualization output |
| **SHA strategy** | Folder-level | Composite (hash of governed file hashes) | Composite — more precise, avoids false positives from metadata-only changes |
| **Report lifecycle** | Overwrite in place | Versioned snapshots | Depends on output location; tool root mandates snapshots per K-SNAP-1 (Lensing: X-004) |

## Examples

### Example: Staleness Propagation Chain

Given deliverables with EXECUTION edges:
```
DEL-05-02 (Execution Root Scaffolding)
  +-- DOWNSTREAM -> DEL-06-02 (Local Deliverable Workflow Agents)
       +-- DOWNSTREAM -> DEL-07-02 (Example Execution Roots)
```

If DEL-05-02's folder content changes after its last approved SHA:
1. DEL-05-02 is marked **dirty** (direct SHA mismatch per K-VAL-1).
2. DEL-06-02 is marked **stale** (propagated via EXECUTION edge per K-STALE-1). Propagation path: `DEL-05-02 -> DEL-06-02`.
3. DEL-07-02 is marked **stale** (transitively propagated). Propagation path: `DEL-05-02 -> DEL-06-02 -> DEL-07-02`.

Human triage for each stale item:
- DEL-06-02: "No impact — scaffolding change was cosmetic" -> clear flag.
- DEL-07-02: "Needs review — examples may need updating" -> schedule review.

*Note: This example uses hypothetical dependency edges for illustration. Actual edges are defined in deliverable-local `Dependencies.csv` files.*

### Example: Triage Queue Output (Conceptual)

```markdown
# Staleness Report — 2026-02-21T14:30:00

## Summary
- Dirty deliverables: 1
- Stale deliverables (propagated): 2
- Total requiring triage: 3

## Triage Queue

| # | Deliverable | Package | Status | Staleness Type | Source | Propagation Path | Triage |
|---|------------|---------|--------|---------------|--------|-----------------|--------|
| 1 | DEL-05-02 | PKG-05 | IN_PROGRESS | DIRTY | SHA mismatch | (direct) | TBD |
| 2 | DEL-06-02 | PKG-06 | INITIALIZED | PROPAGATED | DEL-05-02 | DEL-05-02 -> DEL-06-02 | TBD |
| 3 | DEL-07-02 | PKG-07 | INITIALIZED | PROPAGATED | DEL-05-02 | DEL-05-02 -> DEL-06-02 -> DEL-07-02 | TBD |
```

*Note: Output format is illustrative. Actual format TBD during implementation.*

### Example: Edge-Case Staleness States

```markdown
## Edge Cases in Staleness Report

| # | Deliverable | Package | Staleness Type | Notes |
|---|------------|---------|---------------|-------|
| 4 | DEL-08-05 | PKG-08 | no baseline available | No run record exists; cannot determine dirty/clean |
| 5 | DEL-08-03 | PKG-08 | dependency data unavailable | No Dependencies.csv; direct dirty status: clean |
| 6 | DEL-08-01 | PKG-08 | staleness indeterminate | No baseline + no dependency data |
```

*Note: Example illustrates the canonical edge-case terminology defined in Guidance C7.*

## Success Criteria (Lensing: E-002)

The following qualitative success criteria help evaluate whether the tooling achieves its intended value:

| Criterion | Description | Measurement Approach |
|-----------|-------------|---------------------|
| **Detection accuracy** | Dirty detection correctly identifies all deliverables with changed governed inputs | Unit tests with known-dirty and known-clean deliverables; zero false negatives required, zero false positives expected |
| **Propagation correctness** | All transitive dependents of a dirty deliverable are flagged as stale | Integration tests with fixture graphs covering linear, diamond, and isolated-node patterns |
| **False positive tolerance** | Propagation may over-flag (conservative per P2), but the human should not be overwhelmed with irrelevant items | **ASSUMPTION: qualitative — if more than ~50% of flagged items are consistently "no impact," consider refining the governed-input definition or edge selection** |
| **Triage usability** | The triage queue provides sufficient context for a human to make an informed resolution decision without consulting additional sources | **ASSUMPTION: qualitative — assess through usage feedback** |
| **Auditability** | An auditor can reproduce any staleness determination from the same inputs | Determinism test (REQ-04); provenance recorded in output |

If formal measurable acceptance thresholds are warranted, they should be added to the Specification.

## Conflict Table (for human ruling)

| Conflict ID | Conflict | Source A | Source B | Impacted Sections | Proposed Authority | Human Ruling |
|-------------|---------|----------|----------|-------------------|-------------------|--------------|
| CONFLICT-01 | Triage record persistence location is unspecified: `_STATUS.md`, new `_STALENESS.md`, or tool root snapshot. Prescriptive direction for where triage decisions are recorded has not been established. (Lensing: A-001) | CONTRACT K-STALE-2 (requires triage) | SPEC Section 2.1 (deliverable file inventory — no staleness file defined) | Specification REQ-03, Procedure Step B3, Guidance C5 | PROPOSAL: Define new `_STALENESS.md` file or add triage history to `_STATUS.md`; human ruling needed before implementation | TBD |
| CONFLICT-02 | Output location (tool root snapshot vs. deliverable-local) is unspecified. This also determines report lifecycle (snapshot vs. overwrite). (Lensing: D-001, X-004) | CONTRACT K-SNAP-1 (tool root outputs are snapshots) | DIRECTIVE Section 2.1 (filesystem-as-state, files near their context) | Specification REQ-05, Procedure Steps A2/B1, Guidance C9 | PROPOSAL: Staleness report goes to tool root as snapshot; triage resolution records are deliverable-local; human ruling needed before implementation | TBD |
