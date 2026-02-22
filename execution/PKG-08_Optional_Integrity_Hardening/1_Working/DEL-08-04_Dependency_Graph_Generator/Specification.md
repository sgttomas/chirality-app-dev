# Specification — DEL-08-04 On-demand Dependency Graph Generator

## Scope

### Included

This deliverable covers the implementation of an on-demand tool that:

1. Traverses all deliverable folders in an execution root to locate `Dependencies.csv` files.
2. Parses each `Dependencies.csv` according to the v3.1 schema (SPEC.md Section 6).
3. Aggregates parsed dependency rows into a unified project-level graph structure.
4. Outputs the graph in at least one machine-readable format (JSON) and one human-readable format (Mermaid diagram).
5. Reports graph analysis results including cycle detection and unresolvable targets.

Source: Decomposition DEL-08-04 description; PLAN.md Section 3.4.

### Excluded

- Maintaining a persistent central dependency graph (prohibited by K-DEP-1, CONTRACT.md).
- Modifying any `Dependencies.csv` file (read-only traversal).
- Modifying any deliverable-local metadata files (`_STATUS.md`, `_CONTEXT.md`, `_DEPENDENCIES.md`, `_REFERENCES.md`).
- Staleness propagation logic (belongs to DEL-08-07).
- Dependencies.csv schema validation/linting (belongs to DEL-08-02).
- Folder structure validation (belongs to DEL-08-03).

### Contingency

SOW-035 is currently TBD (Open Issue OI-035). This specification applies only if scope is flipped to IN. If SOW-035 is flipped to OUT, this deliverable SHOULD be retired or archived per the decomposition's change control process; the disposition (cancelled, archived, or deferred) is TBD and requires a human ruling.

Source: Decomposition Scope Ledger, SOW-035.

> [Lensing: C-001] Contingency clause strengthened to specify the negative case (what happens if SOW-035 is OUT), not just the positive activation condition.

## Requirements

### REQ-01: Input Traversal

The tool MUST traverse the execution root filesystem to discover all `Dependencies.csv` files matching the path pattern `{EXECUTION_ROOT}/PKG-*/1_Working/DEL-*/Dependencies.csv`.

- **Source:** SPEC.md Section 1 (execution root layout), Section 2 (deliverable folder layout).
- **Rationale:** Deliverable-local registers are the authoritative source (K-DEP-1).

### REQ-02: Schema Compliance

The tool MUST parse `Dependencies.csv` files conforming to the v3.1 schema as defined in SPEC.md Section 6.2.

- **Source:** SPEC.md Section 6.1-6.2.
- **Note:** Files missing the `RegisterSchemaVersion` column or containing an unrecognized version SHOULD be reported as warnings and excluded from aggregation, not silently ignored.

### REQ-03: Row Filtering

The tool MUST include only rows where `Status = ACTIVE`. Rows where `Status = RETIRED` MUST be excluded from the graph output.

- **Source:** SPEC.md Section 6.6 (lifecycle tracking).

### REQ-04: Graph Construction — Nodes

The tool MUST construct graph nodes from:

- Each unique `FromDeliverableID` encountered across all parsed registers.
- Each unique `TargetDeliverableID` (when `TargetType = DELIVERABLE`) encountered across all parsed registers.

Node metadata SHOULD include at minimum: deliverable ID, deliverable name, and package ID.

- **Source:** SPEC.md Section 6.8 (identity rules); TYPES.md Section 3.

### REQ-05: Graph Construction — Edges (EXECUTION)

For each `ACTIVE` row where `DependencyClass = EXECUTION`:

- An edge MUST be created from `FromDeliverableID` to `TargetDeliverableID` (when `TargetType = DELIVERABLE`).
- Edge metadata MUST include at minimum: `DependencyID`, `DependencyType`, `Direction`, and `Confidence`.

- **Source:** SPEC.md Section 6.4; TYPES.md Section 3.1.

### REQ-06: Graph Construction — Edges (ANCHOR)

For each `ACTIVE` row where `DependencyClass = ANCHOR`:

- A tree edge MUST be created connecting the deliverable to its parent node or traced requirement.
- Tree edges MUST be distinguishable from EXECUTION edges in the output.

- **Source:** SPEC.md Section 6.4; TYPES.md Section 3.1.

### REQ-07: JSON Output Format

The tool MUST produce a JSON output containing at minimum:

- A `nodes` array with node objects (deliverable ID, name, package ID, type, resolved status).
- An `edges` array with edge objects (source, target, dependency ID, class, type, direction, confidence).
- A `metadata` object with generation timestamp, execution root path, schema version, and counts (nodes, edges, files parsed).
- An `analysis` object with `cycles` (array of cycle arrays), `unresolvedNodes` (array of IDs), and `warnings` (array of strings).

The authoritative field list for each JSON object type is defined above. Procedure Step A.2 provides an implementation-ready schema proposal that is consistent with these fields; implementers SHOULD use Procedure Step A.2 as the starting point for schema design. Any field additions beyond those listed here require documentation in the JSON output schema reference document.

- **Source:** Decomposition DEL-08-04 ("JSON"); specific field-level schema is **ASSUMPTION** (TBD pending human design decision).

> [Lensing: F-001] JSON schema field list consolidated here as the authoritative source. Procedure Step A.2 is cross-referenced as a consistent implementation proposal rather than a competing definition.

### REQ-08: Mermaid Output Format

The tool MUST produce a Mermaid-compatible diagram string that:

- Renders deliverable nodes with their IDs and names.
- Renders EXECUTION edges with directional arrows.
- Distinguishes ANCHOR edges from EXECUTION edges (e.g., via line style).

- **Source:** Decomposition DEL-08-04 ("Mermaid"); specific rendering is **ASSUMPTION**.

### REQ-09: Cycle Detection

The tool MUST detect cycles in the EXECUTION edge set. The tool MUST report ALL detected cycles (not only the first cycle found). Cycles SHOULD be reported as ordered lists of deliverable IDs forming each cycle.

Upon detecting one or more cycles, the tool MUST:
- Include the cycle data in the `analysis.cycles` output.
- Continue processing and produce the complete graph output (the tool MUST NOT halt on cycle detection).

- **Source:** PLAN.md Section 3.4 ("cycle detection"); completeness and continuation behavior are **ASSUMPTION**.

> [Lensing: X-003] Clarified that the tool MUST detect all cycles (not just the first), and MUST continue processing after detection rather than halting.

### REQ-10: Unresolvable Target Handling

When a `TargetDeliverableID` references a deliverable ID that does not appear as a `FromDeliverableID` in any parsed register (i.e., the deliverable folder/register does not exist), the tool MUST:

- Include the node as an "unresolved" node in the graph.
- Report the unresolved reference in the output metadata.

- **Source:** CONTRACT.md K-DEP-2.

### REQ-11: On-Demand Execution Only

The tool MUST operate on-demand (invoked explicitly). It MUST NOT maintain a persistent central graph artifact that requires synchronization.

- **Source:** CONTRACT.md K-DEP-1; DIRECTIVE.md Section 5 ("Deliverable-local dependency registers").

### REQ-12: Read-Only Operation

The tool MUST NOT modify any files in the execution root. It is a read-only aggregation tool.

- **Source:** K-DEP-1 (no central graph); K-WRITE-1 (explicit write scope).

### REQ-13: Output Persistence (Optional)

If the tool writes its output to a file (rather than stdout), the output SHOULD be written to a tool root (e.g., `_Aggregation/` or `_Scripts/`) as an immutable snapshot per K-SNAP-1.

- **Source:** CONTRACT.md K-SNAP-1; SPEC.md Section 11.
- **Note:** Whether output is file-persisted or stdout-only is TBD pending design decision (see Guidance C-04).

### REQ-14: Non-Deliverable Targets

For EXECUTION rows where `TargetType` is not `DELIVERABLE` (e.g., `DOCUMENT`, `EXTERNAL`, `REQUIREMENT`), the tool SHOULD include these as labeled peripheral nodes, distinguishable from deliverable nodes.

- **Source:** SPEC.md Section 6.3 (TargetType enums); representation detail is **ASSUMPTION**.

### REQ-15: Exit Code Behavior

The tool MUST return defined exit codes for the following conditions:

| Exit Code | Condition |
|-----------|-----------|
| `0` | Success — graph generated without cycles or errors |
| TBD | Cycles detected — graph generated but cycles found in EXECUTION edges |
| TBD | Parse errors — one or more `Dependencies.csv` files could not be parsed |
| TBD | Invalid arguments — CLI arguments are malformed or missing |

The specific non-zero exit code values are TBD pending human design decision. Automated callers (including DEL-08-07) depend on deterministic exit codes to reliably determine tool outcome.

- **Source:** **ASSUMPTION** — exit code behavior is inferred as a mandatory practice for CLI tool operation.

> [Lensing: A-002] Exit code requirement added. Without defined exit codes, automated callers cannot reliably determine tool outcome.

### REQ-16: Direction Normalization

The tool MUST normalize legacy direction values on read: `INBOUND` MUST be mapped to `UPSTREAM`, and `OUTBOUND` MUST be mapped to `DOWNSTREAM`, per SPEC.md Section 6.7.

- **Source:** SPEC.md Section 6.7; TYPES.md Section 3.3.
- **Cross-reference:** This requirement formalizes the behavior described in Guidance C-07 and Procedure Step A.3.

> [Lensing: B-003] Direction normalization promoted from Guidance C-07 to a formal requirement. This behavior is operational knowledge needed for correct implementation and was previously absent from the normative Specification.

### REQ-17: Logging and Diagnostic Reporting

The tool MUST report operational diagnostics (warnings, schema mismatches, skipped files) to stderr or a dedicated log channel. This reporting is distinct from the structured `analysis.warnings` array in the JSON output.

- The log channel MUST be separate from the primary JSON/Mermaid output channel (stdout or file).
- The verbosity level and format of log messages are TBD pending design decision.

- **Source:** REQ-02 Note references warning reporting; logging channel and format are **ASSUMPTION**.

> [Lensing: F-002] Logging/reporting requirement added. REQ-02 says files SHOULD be "reported as warnings" but no requirement previously specified the reporting channel, format, or separation from structured output.

## Standards

| Standard / Governance | Relevance | Accessible |
|----------------------|-----------|------------|
| `docs/SPEC.md` Section 6 (Dependencies.csv v3.1) | Defines input schema | Yes |
| `docs/SPEC.md` Sections 1-2 (Execution root + deliverable layout) | Defines traversal paths | Yes |
| `docs/SPEC.md` Section 11 (Snapshot conventions) | Governs output persistence | Yes |
| `docs/CONTRACT.md` K-DEP-1 | No central graph; on-demand aggregation | Yes |
| `docs/CONTRACT.md` K-DEP-2 | Target ID resolution requirement | Yes |
| `docs/CONTRACT.md` K-SNAP-1 | Immutable snapshots for tool outputs | Yes |
| `docs/CONTRACT.md` K-WRITE-1 | Explicit write scope | Yes |
| `docs/CONTRACT.md` K-INVENT-1 | No invented values | Yes |
| `docs/TYPES.md` Section 3 | Dependency vocabulary | Yes |

## Verification

| Requirement | Verification Approach |
|-------------|----------------------|
| REQ-01 (Input traversal) | Test with example execution root containing N packages/deliverables with Dependencies.csv files; verify tool reports exactly N files parsed and all expected file paths are included in metadata |
| REQ-02 (Schema compliance) | Test with valid v3.1 files and files with missing/wrong schema version; verify correct parsing and warning behavior; verify non-v3.1 files are excluded from aggregation and reported to stderr |
| REQ-03 (Row filtering) | Test with mixed ACTIVE/RETIRED rows; verify only ACTIVE rows appear in output; verify row counts in metadata reflect filtering |
| REQ-04 (Nodes) | Verify all unique deliverable IDs from parsed registers appear as nodes with correct metadata; verify node count in JSON metadata matches expected count |
| REQ-05 (EXECUTION edges) | Verify EXECUTION rows produce directed edges with required metadata fields (DependencyID, DependencyType, Direction, Confidence all present and non-null) |
| REQ-06 (ANCHOR edges) | Verify ANCHOR rows produce tree edges distinguishable from EXECUTION edges in both JSON (class field) and Mermaid (line style) output |
| REQ-07 (JSON output) | Validate JSON output against the field list in REQ-07; verify nodes, edges, metadata, and analysis sections are all present with correct types |
| REQ-08 (Mermaid output) | Render Mermaid output in a compatible viewer (e.g., mermaid.live); verify nodes and edges are present, correctly directed, and ANCHOR/EXECUTION edges are visually distinguishable |
| REQ-09 (Cycle detection) | Test with a register set containing two or more known independent cycles; verify ALL cycles are detected, reported in analysis.cycles, and the tool completes successfully (does not halt) |
| REQ-10 (Unresolvable targets) | Test with a register referencing a non-existent deliverable ID; verify unresolved node appears in graph and in analysis.unresolvedNodes |
| REQ-11 (On-demand) | Verify tool does not create persistent state, background processes, or require prior invocations |
| REQ-12 (Read-only) | Compute checksums of all files in execution root before and after tool execution; verify no files are modified, created, or deleted |
| REQ-13 (Output persistence) | If file output is implemented: verify output follows snapshot conventions (immutable folder, `_LATEST.md` pointer updated). If file output is NOT implemented: verify tool produces output to stdout only and does not write files; document this as the passing condition |
| REQ-14 (Non-deliverable targets) | Test with EXTERNAL/DOCUMENT/REQUIREMENT targets; verify peripheral nodes appear with correct TargetType labels and are distinguishable from deliverable nodes |
| REQ-15 (Exit codes) | Test each exit condition (success, cycles-found, parse-errors, invalid-arguments); verify the tool returns the defined exit code for each condition |
| REQ-16 (Direction normalization) | Include INBOUND/OUTBOUND values in test fixture; verify they are normalized to UPSTREAM/DOWNSTREAM in all output formats (JSON and Mermaid) |
| REQ-17 (Logging/diagnostics) | Verify warnings, schema mismatches, and skipped files are reported to stderr (or log channel) and NOT interleaved with primary JSON/Mermaid output on stdout |

> [Lensing: A-003] Verification approaches now include quantitative or measurable pass/fail thresholds (e.g., "exactly N files parsed," "all present and non-null," "two or more known cycles," "checksums match").
>
> [Lensing: C-002] Verification row for direction normalization (REQ-16) added to close the gap between Procedure verification (which already tested this) and Specification verification (which did not).
>
> [Lensing: D-001] REQ-13 verification approach now addresses both the implemented and not-implemented cases for file output, specifying the passing condition for each.

## Documentation

### Required Artifacts

| Artifact | Type | Description |
|----------|------|-------------|
| Graph generator script | SCRIPT | The executable tool (language TBD) |
| JSON output schema definition | DOC | Schema documentation for the JSON graph format (authoritative field list per REQ-07) |
| Usage documentation | DOC | Invocation instructions, CLI arguments, exit codes, output format description |
| Test fixtures | OTHER | Example Dependencies.csv files and expected graph outputs |

Source: Decomposition DEL-08-04 anticipated artifacts (SCRIPT/OTHER/DOC).
