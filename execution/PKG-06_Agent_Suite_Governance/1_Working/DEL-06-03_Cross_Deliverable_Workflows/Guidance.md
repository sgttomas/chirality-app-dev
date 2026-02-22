# Guidance -- DEL-06-03 Cross-Deliverable Workflow Support

## Purpose

This deliverable exists to ensure the four cross-deliverable workflow agents -- AGGREGATION, RECONCILIATION, ESTIMATING, and SCHEDULING -- conform to SOW-020's requirement that cross-deliverable operations are "opt-in, human-triggered workflows writing outputs under tool roots as immutable snapshots."

These agents are the primary mechanisms through which the Chirality system aggregates, reconciles, estimates, and schedules work across deliverable boundaries. Because they operate across deliverables (rather than within a single deliverable), they carry elevated risk of:
- unintended side effects on source files,
- scope creep through automatic triggering,
- silent conflict resolution that bypasses human judgment.

This deliverable verifies and documents the governance controls that prevent these risks.

Source: decomposition DEL-06-03 entry; DIRECTIVE Section 2.3.

---

## Principles

### P-001: Opt-In Over Automatic

Cross-deliverable workflows MUST be explicitly requested by a human. This is a direct expression of DIRECTIVE Section 2.3 ("Agents propose; humans approve") applied to workflows that span multiple deliverables.

**Rationale:** Cross-deliverable operations inherently touch multiple work items. Automatic triggering would create coordination risks (concurrent modifications, unintended staleness propagation) and could undermine the human's ability to control what runs when.

Source: `docs/DIRECTIVE.md` Section 2.3; SOW-020.

### P-002: Tool Root Isolation

Each cross-deliverable workflow agent writes exclusively to its designated tool root. This is the cross-deliverable application of K-WRITE-1 (explicit write scope) and the architectural separation between source truth (deliverable folders) and derived outputs (tool roots).

**Rationale:** Derived outputs in tool roots are expendable and rerunnable. Source truth in deliverable folders is authoritative and human-governed. Mixing the two would break auditability.

Source: `docs/CONTRACT.md` K-WRITE-1; `docs/SPEC.md` Section 1.2.

### P-003: Snapshot Immutability for Audit Trail

Immutable snapshots ensure that every run produces a complete, timestamped, non-destructive record. This supports K-SNAP-1 and enables:
- comparison across runs,
- rollback by selecting a prior snapshot,
- audit trail for estimates, schedules, and reconciliation results.

Source: `docs/CONTRACT.md` K-SNAP-1; `docs/SPEC.md` Section 11.

### P-004: Human Decision Gates for Multi-Step Workflows

Type 1 cross-deliverable agents (RECONCILIATION, SCHEDULING) implement explicit human decision gates:
- RECONCILIATION's no-autopilot rule prevents runaway dispatch chains.
- SCHEDULING's 5-gate model ensures the human validates structure, durations, and the final schedule before publication.

**Rationale:** Multi-step workflows that aggregate or reconcile across deliverables involve judgment calls (scope, classification, conflict resolution) that MUST remain human decisions.

Source: `agents/AGENT_RECONCILIATION.md` no-autopilot rule; `.claude/agents/SCHEDULING.md` Gate Model.

---

## Considerations

### C-001: Agent Instruction File Locations

The four cross-deliverable workflow agents have instruction files in two different locations:

| Agent | Instruction File Location | Naming Pattern |
|-------|--------------------------|---------------|
| AGGREGATION | `agents/AGENT_AGGREGATION.md` | `AGENT_{NAME}.md` |
| RECONCILIATION | `agents/AGENT_RECONCILIATION.md` | `AGENT_{NAME}.md` |
| ESTIMATING | `agents/AGENT_ESTIMATING.md` | `AGENT_{NAME}.md` |
| SCHEDULING | `.claude/agents/SCHEDULING.md` | `{NAME}.md` (no AGENT_ prefix) |

SCHEDULING's instruction file is in `.claude/agents/` rather than `agents/`. This may reflect a different deployment model (`.claude/agents/` for harness-invocable agents vs. `agents/` for reference instruction files) but should be verified for consistency with the project's intended instruction root separation (DIRECTIVE Section 2.6).

**ASSUMPTION:** The dual location pattern (`agents/` vs `.claude/agents/`) is intentional and reflects the instruction root vs. working root separation. The `agents/` directory is the canonical instruction root; `.claude/agents/` provides harness-accessible copies or variants.

> **Naming convention note (Lensing B-002, E-002):** SCHEDULING's filename (`SCHEDULING.md`) does not follow the `AGENT_{NAME}.md` naming convention used by the other three agents. Additionally, references across the four documents should use a consistent canonical name. The following normalization is adopted: use the actual filename as canonical -- `SCHEDULING.md` at `.claude/agents/SCHEDULING.md` -- and note the convention divergence explicitly rather than using `AGENT_SCHEDULING.md` which does not exist. All documents in this deliverable have been normalized to use `SCHEDULING.md` when referring to the file and `.claude/agents/SCHEDULING.md` for the full path. (Source: `.claude/agents/SCHEDULING.md` actual filename; `agents/AGENT_AGGREGATION.md`, `agents/AGENT_RECONCILIATION.md`, `agents/AGENT_ESTIMATING.md` actual filenames.)

### C-002: RECONCILIATION's Non-Snapshot Output Model

RECONCILIATION (Type 1) produces run summaries as individual markdown files rather than timestamped snapshot folders. This is a valid pattern for Type 1 persona agents (which interact in conversation) but differs from the snapshot model used by Type 2 task agents (AGGREGATION, ESTIMATING).

The RECONCILIATION output persistence section explicitly acknowledges this: "RECONCILIATION is a Type 1 persona agent. It does not produce immutable snapshots."

This does not violate K-SNAP-1 (which applies to "task agent outputs to tool roots"), but it means RECONCILIATION's audit trail depends on run summary files and conversation context rather than immutable snapshot folders.

**Design rationale (Lensing D-002):** RECONCILIATION uses run summary files instead of timestamped snapshot folders because its primary outputs are diagnostic rather than archival. As a Type 1 persona agent operating within a conversational cycle, RECONCILIATION identifies dependency conflicts, coherence issues, and recommended actions -- outputs whose value is in their immediacy and actionability rather than their long-term immutability. The other three agents (AGGREGATION, ESTIMATING, SCHEDULING) produce structured data artifacts (rollups, cost tables, Gantt charts) where folder-level immutability provides stronger guarantees of artifact integrity. The choice of output model thus aligns with the agent's Type classification and the nature of its outputs. (**ASSUMPTION** -- rationale inferred from agent type classification in `AGENT_RECONCILIATION.md` Output Persistence section and output model comparison across all four agents.)

Source: `agents/AGENT_RECONCILIATION.md` Output Persistence section.

### C-003: ESTIMATING Pointer File Conditional Update

ESTIMATING has a conditional pointer file update controlled by `UPDATE_LATEST_POINTER` (default: FALSE). This is a more conservative approach than AGGREGATION (which always updates its pointer) or SCHEDULING (which updates after human confirmation at Gate 5).

The variation is intentional and documented in each agent's instructions, but operators should be aware that `_Estimates/_LATEST.md` will NOT be updated by default -- the human must explicitly enable it.

Source: `AGENT_ESTIMATING.md` -- `UPDATE_LATEST_POINTER` parameter.

### C-004: Relationship to DEL-06-01 (Agent Structural Conformance)

DEL-06-01 covers broad agent instruction structural conformance (SOW-031). DEL-06-03 has a narrower focus: ensuring the four cross-deliverable agents satisfy SOW-020's specific requirements (opt-in, human-triggered, immutable snapshots, correct tool roots).

Where structural conformance issues are found in cross-deliverable agent instruction files, DEL-06-03 should document them but may defer remediation to DEL-06-01 if the issue is purely structural (e.g., missing section markers) rather than functional (e.g., incorrect write scope).

### C-005: Relationship to DEL-06-02 (Local Workflow Agents)

DEL-06-02 covers deliverable-local workflow agents (PREPARATION, 4_DOCUMENTS, semantic agents). The boundary between DEL-06-02 and DEL-06-03 is the scope of the workflow:
- DEL-06-02: agents that operate within a single deliverable folder
- DEL-06-03: agents that operate across deliverable boundaries

Some agents interact across this boundary (e.g., AGGREGATION reads deliverable-local files; DEPENDENCIES extraction feeds into RECONCILIATION). The interface points are documented in the Datasheet.

---

## Trade-offs

### T-001: Strictness of Opt-In Enforcement

**Option A (current):** Opt-in is enforced by agent instruction design (INTERACTION_SURFACE declarations, no-autopilot rules). No runtime enforcement mechanism exists beyond agent compliance.

**Option B (future):** Implement runtime enforcement via harness gates that require explicit human approval before any cross-deliverable workflow can execute.

**Current position:** Option A is sufficient for the current system maturity. Option B would require harness runtime changes (PKG-03 scope) and is deferred as a future hardening candidate.

Source: decomposition -- SOW-020 is IN scope; no runtime enforcement SOW exists.

### T-002: _Schedule/ Tool Root Formalization

SCHEDULING writes to `_Schedule/` but this tool root is not listed in SPEC Section 1.2. Two options:

**Option A:** Update SPEC.md to add `_Schedule/` to the Tool Roots table.
**Option B:** Have SCHEDULING write to an existing tool root (none are suitable without semantic drift).

**Recommended:** Option A. The deliverable should propose adding `_Schedule/` to SPEC.md Section 1.2.

---

## Conflict Table (for human ruling)

| Conflict ID | Conflict | Source A | Source B | Impacted Sections | Proposed Authority | Human Ruling |
|-------------|----------|----------|----------|-------------------|-------------------|--------------|
| C-001 | SCHEDULING writes to `_Schedule/` tool root, which is not listed in SPEC Section 1.2 Tool Roots table | `.claude/agents/SCHEDULING.md` (STRUCTURE section -- uses `_Schedule/`) | `docs/SPEC.md` Section 1.2 (does not list `_Schedule/`) | Datasheet: Tool Root Mapping; Specification: R-003 | PROPOSAL: Update SPEC.md Section 1.2 to add `_Schedule/` as a recognized tool root (per T-002 recommendation) | TBD |

> **Note (Lensing F-001):** Until Conflict C-001 is resolved, R-003 conformance for SCHEDULING is formally INDETERMINATE. The Conflict Table entry above was pre-existing; this note elevates its priority: this is a foundational compliance question because if the tool root is not formally recognized, the conformance assessment against R-003 cannot produce a definitive CONFORM/NON-CONFORM judgment for SCHEDULING. Assessors should mark the R-003/SCHEDULING cell in the conformance matrix as INDETERMINATE pending human ruling on C-001. (Source: Specification.md R-003; Guidance.md T-002.)

---

## Examples

### Example: AGGREGATION Snapshot Lifecycle

1. Human initiates estimate collation via INIT-TASK brief specifying `PURPOSE=Estimate_Collation` and `SCOPE=DEL-03-01`
2. AGGREGATION bootstraps `_Aggregation/` tool root (Function 0)
3. AGGREGATION reads the brief (Function 1), locates estimate artifacts (Function 2)
4. AGGREGATION validates format and preserves provenance (Function 3)
5. AGGREGATION collates into project-level artifacts (Function 4)
6. AGGREGATION publishes immutable snapshot: `_Aggregation/AGG_Estimate_Collation_2026-02-21_1430/`
7. AGGREGATION updates pointer: `_Aggregation/_LATEST.md` -> `AGG_Estimate_Collation_2026-02-21_1430`

Source: `agents/AGENT_AGGREGATION.md` PROTOCOL.

### Example: SCHEDULING Gate Sequence

1. Human starts conversation with SCHEDULING
2. **Gate 1:** Agent reads decomposition + dependencies; presents graph health report; human confirms scope and basis
3. **Gate 2:** Agent builds schedule structure; human validates structure
4. **Gate 3:** Agent generates duration template; human provides durations and calendar constraints
5. **Gate 4:** Agent renders Gantt + CSV + analysis; human accepts or adjusts
6. **Gate 5:** Agent packages snapshot under `_Schedule/SCHEDULE_CONSTRAINT_2026-02-21_001/`; human confirms publish

Each gate requires explicit human confirmation before proceeding. No gate may be skipped.

Source: `.claude/agents/SCHEDULING.md` Gate Model and PROTOCOL.
