# Guidance — DEL-08-04 On-demand Dependency Graph Generator

## Purpose

The On-demand Dependency Graph Generator exists to bridge the gap between the system's intentionally decentralized dependency model and the need for project-level visibility. The Chirality framework stores dependencies in deliverable-local `Dependencies.csv` registers (K-DEP-1, CONTRACT.md) specifically to avoid the synchronization burden of a central graph. However, stakeholders periodically need a unified view for visualization, critical path analysis, and cycle detection.

This tool resolves that tension by generating the project graph **on-demand from the authoritative local registers**, without maintaining a persistent central artifact.

Source: PLAN.md Section 3.4; CONTRACT.md K-DEP-1; DIRECTIVE.md Section 5 ("Deliverable-local dependency registers").

## Principles

### P-01: Read-Only Aggregation, Never Mutation

The graph generator reads `Dependencies.csv` files but never modifies them. This preserves the invariant that deliverable-local registers are authoritative (K-DEP-1) and prevents the tool from becoming a side-channel for unaudited changes.

Source: CONTRACT.md K-DEP-1, K-WRITE-1.

### P-02: On-Demand, Not Persistent

Each invocation produces a fresh graph from current register state. There is no cached or persistent graph to fall out of sync. If output is file-persisted (TBD), it follows snapshot conventions (K-SNAP-1) — immutable after creation, with reruns producing new snapshots.

Source: CONTRACT.md K-DEP-1, K-SNAP-1; SPEC.md Section 11.

### P-03: Transparent Error Reporting

When the tool encounters malformed registers, unresolvable targets, or schema mismatches, it reports them explicitly rather than silently dropping data. This aligns with the framework's evidence-over-plausibility principle (DIRECTIVE.md Section 2.4).

Source: DIRECTIVE.md Section 2.4; CONTRACT.md K-DEP-2, K-INVENT-1.

### P-04: Dual-Format Output for Dual Audiences

JSON serves machine consumers (e.g., downstream staleness tooling in DEL-08-07). Mermaid serves human consumers who need a visual dependency map. Both formats derive from the same aggregated graph to ensure consistency.

Source: Decomposition DEL-08-04 ("JSON/Mermaid").

### P-05: Respect the Two-Class Edge Model

The tool must preserve the distinction between ANCHOR edges (tree/traceability) and EXECUTION edges (information-flow DAG). Conflating these would obscure the system's knowledge-graph architecture where the tree preserves stable intent and the DAG captures execution couplings.

Source: TYPES.md Section 3.1.

## Vocabulary Note

> [Lensing: X-002] The primary input path is the **execution root** — the top-level directory containing package folders. This document kit uses the placeholder `{EXECUTION_ROOT}` (uppercase, braced) as the canonical reference form. When the term appears in prose, "execution root" (lowercase) refers to the same concept. Implementers and documentation authors SHOULD use `{EXECUTION_ROOT}` in path templates and "execution root" in descriptive text, consistently across Datasheet, Specification, Procedure, and Guidance.

## Considerations

### C-01: Scope Contingency

SOW-035 is currently TBD (Open Issue OI-035). All design and implementation work for this deliverable is contingent on the human flipping the scope item to IN. Until then, this document kit serves as a pre-positioned design scaffold.

Source: Decomposition Scope Ledger, SOW-035; Open Issues OI-035.

### C-02: Input Availability

The tool is only useful when at least some deliverables have populated `Dependencies.csv` files. At project inception (all deliverables at OPEN or INITIALIZED state), no registers exist, and the graph will be empty. This is expected behavior, not an error condition.

**ASSUMPTION:** The tool should produce a valid but empty graph (zero nodes, zero edges) when no Dependencies.csv files are found, rather than failing.

### C-03: Scale Characteristics

With 32 deliverables in the current decomposition (8 packages), the graph is small enough that naive traversal, parsing, and rendering will be performant. No indexing or caching infrastructure is anticipated.

**ASSUMPTION:** Performance optimization is not a priority for the initial implementation. No formal performance requirement exists at this time. If scale increases significantly beyond the 32-deliverable baseline, performance assessment criteria should be defined (see Specification for potential future REQ).

> [Lensing: A-004] Added note on the absence of formal performance criteria and the condition under which they should be introduced.

### C-04: Output Location Decision

The decomposition does not specify where generated graph artifacts should be written. Candidates include:

| Option | Pros | Cons |
|--------|------|------|
| `_Aggregation/` (tool root) | Aligns with aggregation concept; snapshot conventions apply | May overlap with AGGREGATION agent scope |
| `_Scripts/` (tool root) | Houses tooling outputs | Semantically incorrect (scripts vs. outputs) |
| stdout only | No persistence questions; consumer pipes as needed | No artifact for git tracking |
| `_Reconciliation/` (tool root) | Graph analysis supports reconciliation | Semantically narrower than graph use cases |

**ASSUMPTION:** `_Aggregation/` is the most natural fit, but this requires a human design decision. This decision gates Specification REQ-13, Procedure Steps A.6 and A.10, and Datasheet output location.

### C-05: Relationship to Downstream Tooling

DEL-08-07 (Staleness Propagation + Triage Tooling) explicitly depends on this graph output (PLAN.md Section 3.7). The JSON output schema should therefore be designed with DEL-08-07's consumption needs in mind, even though DEL-08-07's specific requirements are TBD.

Source: PLAN.md Section 3.7; Decomposition DEL-08-07.

### C-06: Non-Deliverable Targets

EXECUTION rows may reference non-deliverable targets (`TargetType` = `DOCUMENT`, `EXTERNAL`, `REQUIREMENT`, etc.). The graph representation must handle these as peripheral nodes that do not participate in cycle detection but appear in visualization.

Source: SPEC.md Section 6.3 (TargetType enums).

### C-07: Direction Normalization

Legacy registers may contain `INBOUND`/`OUTBOUND` direction values instead of the canonical `UPSTREAM`/`DOWNSTREAM`. The tool MUST normalize these on read per SPEC.md Section 6.7. This behavior is now formalized as Specification REQ-16.

Source: SPEC.md Section 6.7; TYPES.md Section 3.3.

> [Lensing: B-003] C-07 now cross-references Specification REQ-16 where this behavior has been promoted to a formal requirement.

### C-08: Versioning Strategy for JSON Output

When the tool evolves (new output fields, changed CLI flags, modified JSON structure), backward compatibility must be considered for JSON consumers — particularly DEL-08-07 (Staleness Propagation), which depends on the JSON output schema. Considerations include:

- **Schema version field:** The JSON `metadata` object should include a `schemaVersion` field so consumers can detect format changes.
- **Additive changes:** New fields SHOULD be added without removing or renaming existing fields (backward-compatible extension).
- **Breaking changes:** If fields must be removed or renamed, the schema version MUST be incremented and downstream consumers notified.

**ASSUMPTION:** Versioning strategy details are TBD pending initial schema stabilization.

> [Lensing: X-001] Versioning strategy added. Since DEL-08-07 depends on JSON output schema, guidance on forward evolution is needed to prevent breaking downstream consumers.

### C-09: Mermaid Output Accessibility and Usability

The human-readable output format (Mermaid) should be evaluated for usability beyond functional correctness. Considerations include:

- **Subgraph grouping:** Nodes could be grouped by package (`subgraph PKG-01 ... end`) for visual organization.
- **Edge labeling conventions:** ANCHOR edges vs. EXECUTION edges should use consistent, documented visual differentiation (e.g., dashed vs. solid lines).
- **Color-coding:** TBD whether distinct colors should differentiate ANCHOR from EXECUTION edges or highlight cycle participants.
- **Diagram size:** For large graphs, package-scoped filtering (`--package` flag) may be necessary for readable output.

**ASSUMPTION:** Mermaid usability details are TBD pending initial implementation.

> [Lensing: E-002] Accessibility/usability consideration added. The tool's value proposition centers on "project-level visibility" (Purpose section), so the quality of that visibility deserves explicit consideration.

## Trade-offs

### T-01: Dual-Format vs. Single-Format

Producing both JSON and Mermaid increases implementation scope but serves distinct audiences. The decomposition explicitly calls for both formats. If implementation must be staged, JSON should come first (machine-readable, enables DEL-08-07), with Mermaid as a follow-on.

**ASSUMPTION:** Both formats should be available in the initial release, but staging is acceptable.

### T-02: Script Language

The anticipated artifact type is SCRIPT, but the language is unspecified. Considerations:

| Language | Pros | Cons |
|----------|------|------|
| Python | CSV parsing, JSON output, graph libraries (networkx) readily available; most natural fit | Adds Python runtime dependency |
| Node.js | Already in the project stack (Electron + Next.js) | CSV parsing less ergonomic; graph libraries less mature |
| Shell (bash) | Zero dependencies | CSV/JSON manipulation is brittle; cycle detection is impractical |

**ASSUMPTION:** Python or Node.js are the most viable choices. Human design decision needed.

### T-03: ANCHOR Edge Visualization

ANCHOR edges create a tree structure (package-to-deliverable, deliverable-to-requirement). Including these in a Mermaid diagram alongside EXECUTION edges could create visual clutter. Options:

- Include ANCHOR edges with distinct styling (dashed lines, different color).
- Provide a flag to include/exclude ANCHOR edges.
- Always include in JSON, optionally include in Mermaid.

**ASSUMPTION:** Providing a flag or separate output mode for ANCHOR edges is preferable.

## Success Criteria

Functional correctness (all REQ-* requirements pass verification) is necessary but not sufficient. The tool achieves its intended value of "project-level visibility" (Purpose section) when:

- **Accuracy:** The graph output reflects the true state of all deliverable-local registers at the time of invocation (no dropped rows, no invented edges, no stale data).
- **Time-to-insight:** A stakeholder can invoke the tool and understand the project's dependency structure within minutes, not hours — through readable Mermaid diagrams and/or structured JSON amenable to querying.
- **Actionability:** Analysis outputs (cycles, unresolved nodes, warnings) are specific enough to drive corrective action without requiring the operator to manually re-inspect source registers.

**ASSUMPTION:** Formal quantitative thresholds for these criteria are TBD; the above are qualitative benchmarks.

> [Lensing: D-003] Success criteria added to define what "good" graph output looks like beyond functional correctness.

## Examples

No concrete examples are available from source documents at this time. TBD pending implementation.

Example usage patterns anticipated:

1. **Full project graph:** `generate-graph /path/to/execution-root --format json --format mermaid`
2. **Package-scoped graph:** `generate-graph /path/to/execution-root --package PKG-03 --format mermaid`
3. **Cycle check only:** `generate-graph /path/to/execution-root --cycles-only`

**ASSUMPTION:** CLI interface design is illustrative only; actual interface is TBD.
