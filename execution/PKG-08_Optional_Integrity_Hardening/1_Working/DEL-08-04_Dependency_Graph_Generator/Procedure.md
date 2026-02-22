# Procedure — DEL-08-04 On-demand Dependency Graph Generator

## Purpose

This procedure describes the steps to produce and verify the On-demand Dependency Graph Generator deliverable, and the steps an operator follows to use the tool once implemented.

## Prerequisites

### Production Prerequisites

| Prerequisite | Source | Status |
|-------------|--------|--------|
| SOW-035 scope flip to IN | Decomposition Open Issue OI-035 | TBD |
| Dependencies.csv v3.1 schema finalized | SPEC.md Section 6 | Complete |
| Execution root layout defined | SPEC.md Sections 1-2 | Complete |
| Dependency vocabulary defined | TYPES.md Section 3 | Complete |
| Language/runtime decision | TBD (human design decision) | TBD |
| Output location decision | TBD (see Guidance C-04) | TBD |
| JSON output schema design | TBD (see Specification REQ-07 for authoritative field list) | TBD |

### Usage Prerequisites (for running the tool)

| Prerequisite | Detail |
|-------------|--------|
| Valid execution root | An execution root (`{EXECUTION_ROOT}`) with at least one package folder matching `PKG-*_*/` |
| At least one Dependencies.csv | At least one deliverable with a populated `Dependencies.csv` (v3.1) for meaningful output |
| Script runtime | The chosen language runtime must be installed (TBD) |

## Steps

### Part A — Producing the Deliverable

#### Step A.1: Confirm Scope Status

1. Verify that SOW-035 has been flipped to IN by the human.
2. If SOW-035 remains TBD or OUT, halt production and report to ORCHESTRATOR.

Source: Decomposition Scope Ledger; Open Issue OI-035.

#### Step A.2: Design JSON Output Schema

1. Define the JSON output structure consistent with the authoritative field list in Specification REQ-07:
   - `metadata` object: generation timestamp, execution root path, schema version, counts.
   - `nodes` array: objects with `id`, `name`, `packageId`, `type` (deliverable vs. peripheral), `resolved` (boolean).
   - `edges` array: objects with `id`, `source`, `target`, `dependencyClass`, `dependencyType`, `direction`, `confidence`.
   - `analysis` object: `cycles` (array of cycle arrays), `unresolvedNodes` (array of IDs), `warnings` (array of strings).
2. Document the schema in a usage/reference document.

**ASSUMPTION:** Schema structure above is a proposal consistent with Specification REQ-07; requires human review.

> [Lensing: F-001] Step A.2 now explicitly references Specification REQ-07 as the authoritative field list. This proposal is an implementation-ready expansion, not a competing definition.

#### Step A.3: Implement Register Traversal

1. Implement filesystem traversal of `{EXECUTION_ROOT}/PKG-*/1_Working/DEL-*/Dependencies.csv`.
2. For each discovered file:
   - Parse CSV with v3.1 column headers.
   - Validate `RegisterSchemaVersion` is `v3.1`; warn and skip if not (log to stderr per Specification REQ-17).
   - Filter to `Status = ACTIVE` rows only.
   - Normalize legacy `Direction` values (`INBOUND` to `UPSTREAM`, `OUTBOUND` to `DOWNSTREAM`) per Specification REQ-16 and SPEC.md Section 6.7.
3. Collect all parsed rows into a unified in-memory register.

Source: SPEC.md Sections 1, 2, 6; Specification REQ-02, REQ-03, REQ-16, REQ-17.

#### Step A.4: Implement Graph Construction

1. Build a node set from all unique `FromDeliverableID` and `TargetDeliverableID` values.
2. For non-deliverable targets (`TargetType` != `DELIVERABLE`), create peripheral nodes with the appropriate `TargetType` label.
3. Build an edge set:
   - EXECUTION edges: directed from source to target per `Direction`.
   - ANCHOR edges: directed from deliverable to parent/requirement per `AnchorType`.
4. Mark nodes as "unresolved" when a `TargetDeliverableID` has no corresponding `FromDeliverableID` in any register.

Source: SPEC.md Section 6.4, 6.8; TYPES.md Section 3.1.

#### Step A.5: Implement Cycle Detection

1. Implement cycle detection on the EXECUTION edge subgraph (DAG edges only).
2. Use a standard algorithm (e.g., DFS-based cycle detection, topological sort failure).
3. Report ALL detected cycles as ordered lists of deliverable IDs (per Specification REQ-09).
4. The tool MUST continue processing after detecting cycles and produce complete output.

Source: PLAN.md Section 3.4; Specification REQ-09.

#### Step A.6: Implement JSON Output

1. Serialize the graph to JSON per the schema from Step A.2 (consistent with Specification REQ-07).
2. Include the `analysis` section with cycle results, unresolved nodes, and warnings.
3. Output to stdout or to a snapshot file under the chosen tool root (TBD per Guidance C-04).

Source: Decomposition DEL-08-04; Specification REQ-07.

#### Step A.7: Implement Mermaid Output

1. Generate a Mermaid flowchart string from the graph.
2. Render deliverable nodes as labeled boxes with `DEL-XX-YY` IDs.
3. Render EXECUTION edges as solid arrows with `DependencyType` labels.
4. Render ANCHOR edges (if included) as dashed arrows with `AnchorType` labels.
5. Provide a CLI flag or parameter to include/exclude ANCHOR edges.

Source: Decomposition DEL-08-04; Specification REQ-08.

#### Step A.8: Implement CLI Interface

1. Accept execution root path as a required argument.
2. Accept optional flags for:
   - `--format` (json, mermaid, or both; default: both).
   - `--output` (file path or stdout; default: stdout).
   - `--include-anchors` (include ANCHOR edges; default: false for Mermaid, always included in JSON).
   - `--package` (filter to specific package; default: all packages).
   - `--cycles-only` (output only cycle detection results).
3. Validate that the execution root path exists and contains at least one package folder.
4. Implement defined exit codes per Specification REQ-15.

**ASSUMPTION:** CLI interface design is a proposal; actual interface TBD.

#### Step A.9: Write Documentation

1. Write usage documentation covering invocation, arguments, exit codes, output format, and examples.
2. Write JSON schema reference documentation (consistent with Specification REQ-07 authoritative field list).
3. Create test fixtures (example Dependencies.csv files with known graph shapes).

Source: Specification Documentation section.

#### Step A.10: If Output Is File-Persisted

1. If the design decision (Guidance C-04) is to persist output to a tool root:
   - Write to `{TOOL_ROOT}/{SNAPSHOT_LABEL}_{YYYY-MM-DD}_{HHmm}/` per SPEC.md Section 11.
   - Create or update `_LATEST.md` pointer file per SPEC.md Section 11.2.
   - Ensure snapshot folders are immutable after creation (K-SNAP-1).

Source: SPEC.md Section 11; CONTRACT.md K-SNAP-1.

### Part B — Using the Tool (Operator Procedure)

#### Step B.1: Invoke the Tool

1. Navigate to or specify the execution root path.
2. Run the graph generator with desired options:
   - For a full JSON+Mermaid graph: `TBD_COMMAND /path/to/execution-root`
   - For JSON only: `TBD_COMMAND /path/to/execution-root --format json`
   - For cycle check: `TBD_COMMAND /path/to/execution-root --cycles-only`

#### Step B.2: Review Output

1. Check the exit code to determine overall status (see Specification REQ-15 for exit code definitions).
2. Inspect the JSON output for:
   - Node count matches expected deliverable count.
   - Edge count is reasonable given known dependencies.
   - `analysis.cycles` is empty (no cycles) or contains identified cycles for triage.
   - `analysis.unresolvedNodes` lists any deliverables referenced but not found.
   - `analysis.warnings` lists any schema or parsing issues.
3. Inspect the Mermaid output for visual correctness:
   - Render in a Mermaid-compatible viewer.
   - Verify edge directions match expected information flow.

#### Step B.3: Act on Analysis Results

1. If **cycles detected**: investigate the cycle chain; determine if dependencies are correctly declared or if a register correction is needed. Cycles in a DAG indicate a modeling error.
2. If **unresolved nodes**: verify that the referenced deliverable exists and has a Dependencies.csv file. Missing registers are expected for OPEN-state deliverables.
3. If **warnings**: address schema or parsing issues in the affected Dependencies.csv files.

#### Step B.4: Error Recovery

If the tool crashes mid-traversal or produces partial output:

1. Check stderr / log output for the last successfully processed file to identify the failure point.
2. Verify that the problematic `Dependencies.csv` file is well-formed (consider running DEL-08-02 Dependencies.csv Linter if available).
3. If the issue is a malformed register, correct the register and re-run the tool.
4. If the issue is a tool bug, file a defect and re-run after the fix. No rollback is needed because the tool is read-only (REQ-12); partial output can be discarded.
5. If file output was being written to a tool root and the tool crashed mid-write, delete the incomplete snapshot folder before re-running (incomplete snapshots violate K-SNAP-1 immutability expectations).

> [Lensing: C-003] Error recovery step added. The original procedure addressed only the happy path; systematic operational reliability requires that failure modes are documented.

## Verification

| Check | Method | Expected Result |
|-------|--------|-----------------|
| All Dependencies.csv files discovered | Run against a known execution root with N register files | Tool reports N files parsed |
| ACTIVE-only filtering | Include RETIRED rows in test fixture | RETIRED rows do not appear in graph |
| Cycle detection (all cycles) | Include two or more independent known cycles in test fixture | All cycles reported in analysis.cycles; tool completes successfully |
| Unresolved target handling | Include a reference to non-existent DEL-99-99 | Node marked unresolved in output |
| JSON schema validity | Validate output against schema definition (Specification REQ-07 field list) | Output conforms to defined schema |
| Mermaid renderability | Paste Mermaid output into a viewer (e.g., mermaid.live) | Diagram renders without errors |
| Read-only operation | Compare execution root before/after tool run (checksums) | No files modified |
| Legacy direction normalization | Include INBOUND/OUTBOUND values in test fixture | Normalized to UPSTREAM/DOWNSTREAM in all output formats |
| Empty execution root | Run against root with no Dependencies.csv files | Valid empty graph (0 nodes, 0 edges), no error |
| Snapshot immutability (if applicable) | Run tool twice with file output | Two distinct snapshot folders created; first is unmodified |
| Exit codes | Test each exit condition per Specification REQ-15 | Correct exit code returned for each condition |
| Package-scoped filtering | Run with `--package PKG-03` against execution root with multiple packages | Output graph contains only nodes/edges from the specified package (and their cross-package targets) |
| Logging separation | Run tool and capture stdout and stderr separately | Diagnostic messages appear on stderr only; JSON/Mermaid output appears on stdout only |

> [Lensing: X-004] Package-scoped filtering verification added. The original verification table tested full-graph scenarios but did not test the `--package` filtering capability described in Step A.8 and Guidance Examples.

## Records

| Record | Description |
|--------|-------------|
| Graph generator script | The implemented tool (committed to repository) |
| JSON output schema document | Schema reference for the JSON graph format (consistent with Specification REQ-07) |
| Usage documentation | How to invoke and interpret results (including exit codes per Specification REQ-15) |
| Test fixtures | Example Dependencies.csv files with known graph shapes |
| Test results | Verification results from the checks above |
| Design decisions | Human rulings on language, output location, CLI interface (recorded in `_MEMORY.md`) |
