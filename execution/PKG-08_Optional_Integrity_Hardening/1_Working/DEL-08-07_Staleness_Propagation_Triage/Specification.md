# Specification — DEL-08-07 Staleness Propagation + Triage Tooling

## Scope

### Covered

This deliverable covers the implementation of staleness detection, transitive propagation, and human triage tooling for the Chirality project execution system. Specifically:

- **Staleness detection:** Determine which deliverables are "dirty" by comparing current git SHAs of governed inputs against baseline SHAs from pipeline run records. (CONTRACT K-VAL-1)
- **Staleness propagation:** Propagate staleness transitively along dependency edges (upstream changes mark all transitive dependents as stale). (CONTRACT K-STALE-1)
- **Triage tooling:** Present stale items to a human for triage with resolution modes: no impact (clear flag), needs rework, or needs review. (CONTRACT K-STALE-2)
- **Deterministic, auditable output:** All staleness calculation outputs must be reproducible from the same inputs and representable as filesystem artifacts. (Decomposition notes; DIRECTIVE Section 2.1)
- **Error handling:** The tooling must handle malformed inputs, missing data, and partial graph availability gracefully with defined error states. (Lensing: X-001; see REQ-11)

**Scope item:** SOW-038 (currently TBD; requires human scope decision OI-038).

### Excluded

- Automated resolution of staleness (human triage is mandatory per K-STALE-2).
- Modification of the dependency graph structure (this deliverable consumes graphs, does not produce them).
- Pipeline run record creation or management (consumed from DEL-08-06).
- Central dependency graph maintenance (on-demand aggregation only, per K-DEP-1).
- Any approval or issuance authority (per DIRECTIVE Section 4.2; CONTRACT K-AUTH-1).

## Requirements

### REQ-01: Dirty Detection

The tooling MUST determine whether a deliverable is dirty by comparing the current state of its governed inputs against a baseline SHA. (CONTRACT K-VAL-1)

- **Input:** Baseline SHA per deliverable (from run records). **ASSUMPTION: provided by DEL-08-06 unified run record schema.**
- **Input:** Current git SHA(s) for the deliverable folder contents.
- **Output:** Boolean dirty/clean status per deliverable with evidence (which files changed).
- **Governed inputs:** TBD — which files constitute "governed inputs" per deliverable must be defined (either enumerated or declared via a mechanism). **ASSUMPTION: a governed-input declaration mechanism or canonical list is required before implementation.** (Lensing: B-002; see also Datasheet Attributes "Governed Input Definition" and Guidance C3)
- **No-baseline handling:** When no baseline SHA exists for a deliverable (no run record), the deliverable MUST be reported as **"no baseline available"** rather than silently assumed clean. (Lensing: C-002; CONTRACT K-VAL-1 — cannot determine dirty/clean without a baseline)
- **Source:** CONTRACT K-VAL-1: "A deliverable is dirty if any governed input has changed since its last approved SHA."

### REQ-02: Transitive Staleness Propagation

The tooling MUST propagate staleness transitively to all dependent deliverables when an upstream deliverable is found to be dirty or stale. (CONTRACT K-STALE-1)

- **Input:** Project-level dependency graph (EXECUTION edges). **ASSUMPTION: provided by DEL-08-04 on-demand graph generator.**
- **Processing:** For each dirty deliverable, traverse all DOWNSTREAM EXECUTION edges and mark reachable deliverables as stale.
- **Output:** Staleness status per deliverable with propagation path (chain of edges that caused the stale flag).
- **Source:** CONTRACT K-STALE-1: "Upstream changes propagate staleness to all transitive dependent deliverables."

### REQ-03: Triage Queue Generation

The tooling MUST produce a human-facing triage queue listing all stale deliverables with sufficient context for human resolution. (CONTRACT K-STALE-2)

- **Per-item context:** Deliverable ID, name, package, current lifecycle state, staleness source (direct dirty or propagated), propagation path.
- **Resolution modes:** No impact (clear flag), needs rework, needs review.
- **Triage record schema:** Resolution records MUST capture: who resolved, when (timestamp), disposition (resolution mode selected), and evidence/rationale for the decision. **ASSUMPTION: a mandatory schema or format for triage records is needed; specific format TBD.** (Lensing: A-002; CONTRACT K-STALE-2; CONTRACT K-AUTH-1 — human authority requires traceable decisions)
- **Source:** CONTRACT K-STALE-2: "Stale items must be triaged by a human before being considered current."

### REQ-04: Deterministic Output

Given identical inputs (dependency graph, run records, git state), the staleness calculation MUST produce identical outputs. (Decomposition notes: "keep outputs deterministic/auditable")

- No randomness or non-deterministic ordering in output.
- Output must be reproducible for audit purposes.

### REQ-05: Filesystem-Representable Output

All outputs MUST be representable as plain files suitable for git tracking. (DIRECTIVE Section 2.1; DIRECTIVE Section 5)

- **Output format:** TBD — the concrete format for the staleness report and triage queue must be defined before implementation begins. Likely candidates are markdown (human-readable, git-diffable) and/or CSV (machine-parseable). Different format choices affect implementation, testing, and consumer expectations. (Lensing: B-003)
- If outputs are written to a tool root, they MUST follow immutable snapshot conventions per CONTRACT K-SNAP-1.

### REQ-06: No Ghost Inputs

The staleness calculation MUST operate only on declared, accessible inputs. No hidden state or undeclared data sources may influence the result. (CONTRACT K-GHOST-1)

- Inputs: dependency graph artifact, run record artifact, git repository state.
- All inputs must be traceable and declared.

### REQ-07: Dependency Graph Consumption

The tooling MUST consume the project-level dependency graph produced by DEL-08-04. (PLAN Section 3.7)

- **ASSUMPTION: DEL-08-04 produces a JSON or Mermaid graph artifact from aggregated `Dependencies.csv` files.**
- The tooling must handle the graph format defined by DEL-08-04.
- Edge classes: primarily EXECUTION edges (DAG); ANCHOR edges (tree) for context but not for staleness propagation. **ASSUMPTION: propagation follows EXECUTION edges only.**

### REQ-08: Run Record Consumption

The tooling MUST consume unified pipeline run records from DEL-08-06 to obtain baseline SHAs. (PLAN Section 3.7)

- **ASSUMPTION: DEL-08-06 defines a run record schema that includes per-deliverable baseline SHAs.**
- The tooling must handle the run record format defined by DEL-08-06.

### REQ-09: Human Authority Preserved

The tooling MUST NOT automatically resolve staleness. All triage decisions are human authority. (CONTRACT K-STALE-2; CONTRACT K-AUTH-1)

- The tooling presents information and options; a human makes the decision.
- Resolution records MUST capture: who resolved, when (timestamp), disposition, and evidence/rationale. (Lensing: A-002; CONTRACT K-AUTH-1)

### REQ-10: Scope Contingency

This deliverable is contingent on SOW-038 being flipped to IN scope by a human decision (OI-038). Implementation MUST NOT proceed until scope is confirmed. (Decomposition, Scope Ledger)

- Additionally, OI-038 likely depends on OI-035 (DEL-08-04) and OI-037 (DEL-08-06) being resolved.

### REQ-11: Error Handling (Lensing: X-001)

The tooling MUST define and handle error states for malformed or unavailable inputs. (Lensing: X-001; CONTRACT K-GHOST-1 — inputs must be declared and accessible)

- **Malformed graph artifact:** If the dependency graph artifact cannot be parsed, the tooling MUST report a clear error and not produce partial staleness output. **ASSUMPTION: specific error behavior TBD during implementation.**
- **Corrupt or missing run records:** If run records are unavailable or corrupt for some deliverables, the affected deliverables MUST be reported as "no baseline available" (see REQ-01 no-baseline handling) rather than silently skipped.
- **Unavailable git state:** If git state cannot be determined for a deliverable folder, the deliverable MUST be reported as an error condition.
- **Partial graph:** Deliverables without `Dependencies.csv` data are reported as "dependency data unavailable" (see REQ-02 and Procedure Step A4).

## Standards

| Standard/Invariant | Applicability | Source |
|---------------------|--------------|--------|
| K-STALE-1 | Staleness propagation algorithm | CONTRACT Section 1.6 |
| K-STALE-2 | Human triage requirement | CONTRACT Section 1.6 |
| K-VAL-1 | Dirty detection definition | CONTRACT Section 1.6 |
| K-DEP-1 | No central graph; deliverable-local registers authoritative | CONTRACT Section 1.4 |
| K-GHOST-1 | No ghost inputs | CONTRACT Section 1.3 |
| K-SNAP-1 | Immutable snapshot outputs | CONTRACT Section 1.10 |
| K-AUTH-1 | Human-only approval authority | CONTRACT Section 1.2 |
| K-PROV-1 | Provenance required for dependency rows | CONTRACT Section 1.9 |
| K-INVENT-1 | TBD over invention | CONTRACT Section 1.9 |
| Dependencies.csv v3.1 | Input schema for graph edges | SPEC Section 6 |

## Verification

| Req ID | Verification Approach | Acceptance Criterion |
|--------|----------------------|---------------------|
| REQ-01 | Unit test | Given a deliverable with known baseline SHA and known current SHA, correctly identifies dirty/clean status |
| REQ-01 (no-baseline) | Unit test | Given a deliverable with no run record, reports "no baseline available" rather than clean (Lensing: C-002) |
| REQ-02 | Integration test with fixture graph | Given a graph with A->B->C and A dirty, correctly marks B and C as stale with propagation paths. **Minimum fixture specification:** graph must include at least a linear chain (3+ nodes), a diamond pattern (4+ nodes), and an isolated node. Expected output structure must be validated against the defined output schema. (Lensing: D-002) |
| REQ-03 | Output inspection | Triage queue contains all stale items with required context fields and resolution options |
| REQ-03 (records) | Schema validation | Triage resolution records conform to the mandatory schema (who, when, disposition, evidence) when populated (Lensing: A-002) |
| REQ-04 | Determinism test | Two runs with identical inputs produce byte-identical outputs |
| REQ-05 | File format validation | Outputs are valid files in the defined format; snapshot convention followed if tool root is used |
| REQ-06 | Code review + automated scan | No undeclared data sources; all inputs are from declared artifacts. **ASSUMPTION: an automated input-manifest check or static analysis scan for undeclared imports/file reads should supplement code review.** (Lensing: F-001; CONTRACT K-GHOST-1) |
| REQ-07 | Integration test | Correctly parses and traverses DEL-08-04 graph artifact format. **Minimum fixture specification:** fixture graph must include at least the edge count and node types representative of a small project (10+ deliverables, 15+ edges). (Lensing: D-002) |
| REQ-08 | Integration test | Correctly reads baseline SHAs from DEL-08-06 run record format. **Minimum fixture specification:** fixture run records must cover deliverables with known-dirty, known-clean, and no-baseline states. (Lensing: D-002) |
| REQ-09 | Behavioral test | No automatic resolution occurs; all triage decisions require explicit human input |
| REQ-10 | Process check | Implementation does not begin until OI-038 is resolved as IN scope. **Observable evidence:** OI-038 status in the decomposition is flipped to IN; SOW-038 InOutStatus is IN. (Lensing: C-001) |
| REQ-11 | Unit test + integration test | Malformed graph, corrupt run records, and unavailable git state each produce defined error outputs (not silent failures or partial results) (Lensing: X-001) |
| Triage completion | Process check | A triage cycle is considered valid/complete when: all items in the triage queue have a recorded resolution, each resolution record conforms to the mandatory schema, and a completion timestamp is present. (Lensing: A-003) |

## Documentation

### Required Artifacts

| Artifact | Type | Description |
|----------|------|-------------|
| Staleness detection module | CODE | Core logic for dirty detection (SHA comparison) |
| Propagation engine | CODE | Graph traversal for transitive staleness propagation |
| Triage queue generator | CODE | Produces human-facing triage output |
| CLI/script interface | CODE/SCRIPT | Entry point for running staleness calculation (see Datasheet Construction "CLI/Script Entry Point") |
| Unit tests | TEST | Tests for dirty detection, propagation logic, no-baseline handling, and error handling |
| Integration tests | TEST | Tests with fixture graphs and run records meeting minimum fixture specifications |
| Determinism tests | TEST | Verify identical outputs from identical inputs |
| Usage documentation | DOC | How to run staleness detection, interpret output, perform triage |
| Output format specification | DOC/OTHER | Schema for staleness report and triage queue artifacts |
| Triage record schema | DOC/OTHER | Mandatory fields and format for triage resolution records (Lensing: A-002) |
