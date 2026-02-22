# Procedure — DEL-08-07 Staleness Propagation + Triage Tooling

## Purpose

This procedure describes the steps to produce and verify the Staleness Propagation + Triage Tooling deliverable, and the steps to use the resulting tooling for staleness detection and human triage.

The procedure is divided into two parts:
- **Part A — Production:** How to build and verify the tooling itself.
- **Part B — Operation:** How to run the tooling and perform triage (the intended user workflow).

## Prerequisites

### Scope Prerequisites

| Prerequisite | Status | Source |
|--------------|--------|--------|
| SOW-038 flipped to IN scope (OI-038 resolved) | TBD | Decomposition, Open Issues |
| OI-035 resolved (DEL-08-04 dependency graph — SOW-035) | TBD | Decomposition, Open Issues |
| OI-037 resolved (DEL-08-06 run records — SOW-037) | TBD | Decomposition, Open Issues |

### Technical Prerequisites

| Prerequisite | Deliverable | Status | Notes |
|--------------|-------------|--------|-------|
| On-demand dependency graph generator is available and produces a consumable graph artifact | DEL-08-04 | TBD | **ASSUMPTION: Must be implemented before this deliverable** |
| Unified pipeline run record schema is defined and run records with baseline SHAs are available | DEL-08-06 | TBD | **ASSUMPTION: Must be implemented before this deliverable** |
| `Dependencies.csv` v3.1 registers exist for deliverables in the project | DEL-05-04 | TBD | Required input for graph generation; SOW-018 is IN scope |
| Git repository is available for SHA comparison | — | Available | Core infrastructure |
| Governed-input definition is established (which files per deliverable are governed inputs) | DEL-08-06 or DEL-08-07 | TBD | Required for dirty detection; see Guidance C3 and Specification REQ-01 (Lensing: B-001, B-002) |

### Reference Prerequisites

| Reference | Purpose |
|-----------|---------|
| `docs/CONTRACT.md` — K-STALE-1, K-STALE-2, K-VAL-1 | Governing invariants for staleness behavior |
| `docs/SPEC.md` Section 6 | Dependencies.csv v3.1 schema (input to graph) |
| `docs/TYPES.md` Section 3 | Dependency vocabulary (edge classes, directions) |
| DEL-08-04 output format specification | Graph artifact format (TBD — not yet available) |
| DEL-08-06 output format specification | Run record schema (TBD — not yet available) |

---

## Part A — Production Steps

### Step A1: Confirm Scope and Dependencies

1. Verify that OI-038 has been resolved and SOW-038 is IN scope. **Observable evidence:** OI-038 status in the decomposition is flipped to IN; SOW-038 InOutStatus is IN. (Lensing: C-001; see Specification REQ-10 Verification)
2. Verify that DEL-08-04 (dependency graph generator) is available or in progress with a defined output format.
3. Verify that DEL-08-06 (run records) is available or in progress with a defined schema including baseline SHAs.
4. Verify that the governed-input definition has been established (see Guidance C3). (Lensing: B-001, B-002)
5. If any prerequisite is unresolved, do not proceed. Record the blocking condition in `_STATUS.md`.

### Step A2: Define Input/Output Contracts

1. Document the expected input format for the dependency graph artifact (from DEL-08-04). TBD — depends on DEL-08-04 output specification.
2. Document the expected input format for run records (from DEL-08-06). TBD — depends on DEL-08-06 output specification.
3. Document the output format for the staleness report. TBD — design decision required. Likely markdown and/or CSV; format choice affects implementation, testing, and consumers. (Lensing: B-003; see Specification REQ-05)
4. Document the output format for the triage queue. TBD — design decision required.
5. Document where outputs are written (tool root snapshot vs. deliverable-local). TBD — see Guidance CONFLICT-02.
6. Document the triage resolution record schema (mandatory fields: who, when, disposition, evidence/rationale). TBD — see Specification REQ-03 and REQ-09. (Lensing: A-002)

### Step A3: Implement Dirty Detection Module

1. Implement SHA computation for governed deliverable files.
   - Use the governed-input definition (established in Step A1 item 4) to determine which files are computed. (Lensing: B-001, B-002)
   - Compute composite SHA (hash of governed file hashes).
2. Implement baseline SHA comparison logic.
   - Read baseline SHA from the most recent run record for the deliverable.
   - Compare against current composite SHA.
   - Produce dirty/clean status with evidence (list of changed files).
3. Handle edge cases:
   - No run record exists for a deliverable -> report as **"no baseline available."** (Lensing: C-002, X-003; see Guidance C7 for canonical terminology)
   - Deliverable folder does not exist -> report as error.
   - Run record is corrupt or unparseable -> report as **"no baseline available"** with an error annotation. (Lensing: X-001; see Specification REQ-11)

### Step A4: Implement Graph Traversal and Propagation Engine

1. Parse the dependency graph artifact from DEL-08-04.
2. Build an in-memory graph representation with nodes (deliverables) and edges (EXECUTION-class dependencies).
3. Implement transitive propagation:
   - For each dirty deliverable, perform a graph traversal (BFS or DFS) along DOWNSTREAM EXECUTION edges.
   - Mark all reachable deliverables as stale.
   - Record the propagation path for each stale deliverable.
4. Implement cycle detection:
   - Track visited nodes during traversal.
   - If a cycle is detected, log a warning and do not re-traverse.
5. Handle partial graph:
   - Deliverables without `Dependencies.csv` data -> report as **"dependency data unavailable"** (not silently clean). (Lensing: X-003; see Guidance C7 for canonical terminology)
6. Handle malformed graph artifact:
   - If the graph artifact cannot be parsed, report a clear error and halt. Do not produce partial staleness output. (Lensing: X-001; see Specification REQ-11)

### Step A5: Implement Triage Queue Generator

1. Collect all dirty and stale deliverables.
2. For each item, assemble triage context:
   - Deliverable ID, name, package, current lifecycle state (from `_STATUS.md`).
   - Staleness type (DIRTY = direct SHA mismatch; PROPAGATED = transitive).
   - Staleness source (which upstream deliverable caused it).
   - Propagation path (chain of edges).
3. Generate triage queue output in the defined format.
4. Include resolution options per item: no impact (clear flag), needs rework, needs review.
5. Include edge-case items with their canonical status terms ("no baseline available," "dependency data unavailable," "staleness indeterminate") in the report for visibility. (Lensing: X-003; see Guidance C7)

### Step A6: Implement CLI/Script Entry Point

1. Create a script/CLI entry point that:
   - Accepts the execution root path as input.
   - Invokes DEL-08-04 graph generation (or reads a pre-generated graph artifact).
   - Reads run records from DEL-08-06.
   - Runs dirty detection across all deliverables.
   - Runs propagation.
   - Produces the staleness report and triage queue.
2. Ensure the entry point is invocable from the project root. TBD — script location and naming convention. (Lensing: F-002; see Datasheet Construction "CLI/Script Entry Point")
3. Implement clean failure behavior: if any step fails, produce an error report indicating which step failed and what was processed, without producing partial staleness output that could be mistaken for a complete report. (Lensing: X-001, X-002; see Guidance C8)

### Step A7: Write Tests

1. **Unit tests — Dirty detection:**
   - Known dirty deliverable correctly identified.
   - Known clean deliverable correctly identified.
   - Missing baseline handled gracefully (reports "no baseline available"). (Lensing: C-002)
   - Corrupt run record handled gracefully (reports "no baseline available" with error annotation). (Lensing: X-001)
2. **Unit tests — Propagation:**
   - Linear chain (A->B->C): A dirty -> B and C stale.
   - Diamond (A->B, A->C, B->D, C->D): A dirty -> B, C, D all stale.
   - Isolated node: not affected by unrelated dirty nodes.
   - Cycle: detected and reported without infinite loop.
3. **Integration tests:**
   - End-to-end run with fixture graph and fixture run records produces expected output.
   - **Minimum fixture specification:** graph with at least a linear chain (3+ nodes), a diamond pattern (4+ nodes), an isolated node, and representative edge counts (15+ edges for a 10+ deliverable graph). Expected output structure validated against the defined output schema. (Lensing: D-002)
   - Determinism: two identical runs produce identical output.
   - Malformed graph input produces a defined error (not partial output). (Lensing: X-001)
4. **Edge case tests:**
   - Empty graph (no deliverables).
   - Graph with no EXECUTION edges.
   - All deliverables clean.
   - All deliverables dirty.
   - Mix of "no baseline available" and "dependency data unavailable" edge-case states. (Lensing: X-003)

### Step A8: Write Documentation

1. Usage documentation: how to invoke the tooling, expected inputs, interpreting outputs.
2. Output format specification: schema for staleness report and triage queue.
3. Triage record schema: mandatory fields and format for resolution records. (Lensing: A-002)
4. Integration notes: how this tooling fits into the broader integrity hardening chain (PLAN Section 4).

---

## Part B — Operation Steps (Using the Tooling)

### Step B1: Invoke Staleness Calculation

1. Ensure the project has current `Dependencies.csv` registers and at least one set of run records with baseline SHAs.
2. Run the staleness calculation script/CLI from the execution root. (See Datasheet Construction "CLI/Script Entry Point" for invocation details.)
3. Wait for output. If the run fails, review the error report (see Guidance C8 on failure modes) and address the underlying issue before re-running.

### Step B2: Review Staleness Report

1. Open the generated staleness report.
2. Review the summary: count of dirty deliverables, count of propagated stale deliverables, count of edge-case items ("no baseline available," "dependency data unavailable," "staleness indeterminate"). (Lensing: X-003)
3. Review individual entries, focusing on propagation paths to understand causality.

### Step B3: Perform Human Triage

For each item in the triage queue:

1. Read the staleness context (source, propagation path, changed files).
2. Assess impact and select a resolution:
   - **No impact** — the upstream change does not materially affect this deliverable. Clear the stale flag.
   - **Needs rework** — the upstream change requires updates to this deliverable. Schedule rework.
   - **Needs review** — the upstream change may or may not affect this deliverable; a review is needed to determine. Schedule review.
3. Record the triage decision using the mandatory triage record schema (who, when, disposition, evidence/rationale). (Lensing: A-002; see Specification REQ-03 and REQ-09)
   - **Persistence location:** TBD — see Guidance CONFLICT-01 for the unresolved design decision on where triage records are stored. (Lensing: A-001, A-004)
   - **Note:** This step is not fully actionable until CONFLICT-01 is resolved by the human. The triage recording mechanism (where and how) depends on that ruling.

### Step B4: Act on Triage Decisions

1. For items marked "needs rework": update the deliverable's `_STATUS.md` if lifecycle state needs to change (e.g., back to IN_PROGRESS).
2. For items marked "needs review": schedule and perform the review.
3. For items cleared as "no impact": confirm the stale flag is removed.
4. Verify triage cycle completion: all items in the triage queue have a recorded resolution conforming to the mandatory schema, and a completion timestamp is present. (Lensing: A-003; see Specification Verification "Triage completion")

---

## Verification

| Check | Validation |
|-------|-----------|
| Dirty detection correctness | Unit tests pass for known dirty/clean scenarios |
| No-baseline handling | Unit tests confirm deliverables without run records are reported as "no baseline available" (Lensing: C-002) |
| Propagation correctness | Unit tests pass for linear, diamond, and cycle scenarios |
| Deterministic output | Two runs with identical inputs produce identical outputs |
| Triage queue completeness | All stale items appear in the triage queue with required context |
| Triage record schema | Resolution records conform to mandatory schema (who, when, disposition, evidence) (Lensing: A-002) |
| Human authority preserved | No automatic resolution; all triage decisions require human input |
| Output is filesystem-representable | Outputs are valid files in the defined format |
| No ghost inputs | Code review + automated scan confirms all inputs are declared and accessible (Lensing: F-001) |
| Cycle handling | Cycles detected and reported; no infinite loops |
| Partial graph handling | Deliverables without dependency data reported as "dependency data unavailable" (Lensing: X-003) |
| Error handling | Malformed inputs, corrupt records, and unavailable git state produce defined error outputs (Lensing: X-001) |
| Scope gate evidence | OI-038 and SOW-038 status verified before implementation begins (Lensing: C-001) |

## Records

| Record | Type | Description |
|--------|------|-------------|
| Staleness report | OUTPUT | Point-in-time snapshot of dirty and stale deliverables with propagation paths |
| Triage queue | OUTPUT | Human-facing triage list with resolution options |
| Triage decision records | OUTPUT | Human triage resolutions per deliverable conforming to mandatory schema (TBD — persistence location per CONFLICT-01) |
| Test results | TEST | Unit, integration, determinism, and error-handling test outputs |
| Code review records | DOC | Review confirming no ghost inputs and correct propagation logic |
| Error reports | OUTPUT | Reports generated on failed runs indicating failure point and partial processing state (Lensing: X-001, X-002) |
