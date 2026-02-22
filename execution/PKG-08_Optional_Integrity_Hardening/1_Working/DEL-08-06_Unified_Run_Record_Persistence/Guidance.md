# Guidance — DEL-08-06 Unified Pipeline Run Record Persistence

## Purpose

This deliverable exists because the Chirality system currently lacks a unified, structured record of individual pipeline executions. Run tracking is fragmented across two existing mechanisms:

1. **`_STATUS.md` history** — records lifecycle state transitions (e.g., "State set to INITIALIZED") but does not capture run-level detail (duration, inputs consumed, outputs produced, baseline SHA).
2. **`_DEPENDENCIES.md` Run History** — records dependency extraction runs specifically, but only for the DEPENDENCIES agent, not for other Type 2 agents.

Without a unified run record, the system cannot:
- Provide a complete audit trail of what agent ran, when, with what inputs, and what it produced.
- Support informed rerun decisions (knowing what changed since the last run).
- Enable downstream staleness detection (which requires baseline SHAs from run records — see K-VAL-1, K-STALE-1).
- Offer the foundation that DEL-08-07 (Staleness Propagation + Triage Tooling) needs to function.

Source: PLAN Section 3.6.

## Principles

### P1: One Schema, One Location

The decomposition explicitly constrains this deliverable: "keep bounded to one schema + one storage location." This is a design discipline constraint, not a technical limitation. The intent is to avoid schema proliferation and multi-location sync burden.

**Implication:** Do not design multiple record formats for different agent types. One schema must accommodate all Type 2 agent runs, with optional fields for agent-specific metadata.

Source: Decomposition ContextEnvelopeNotes for DEL-08-06.

### P2: Additive, Not Replacement

The unified run record is a **new artifact**, not a replacement for `_STATUS.md` history or `_DEPENDENCIES.md` run history. Those existing mechanisms continue to serve their current purposes. The unified record adds a cross-agent, execution-focused view.

**Implication:** Do not modify existing `_STATUS.md` or `_DEPENDENCIES.md` schemas. The run record is a supplementary artifact.

Source: PLAN Section 3.6 (describes the gap, not a replacement need); stability of SPEC Sections 3 and 5.

### P3: Filesystem-Native, Git-Friendly

Run records must be plain files that are human-readable, git-diffable, and git-committable. This follows directly from the system's founding constraints.

**Implication:** Prefer Markdown or CSV format. Avoid binary formats, JSON (less git-diff-friendly for append-only records), or any format requiring special tooling to read.

Source: DIRECTIVE Section 2.1 (filesystem is the database); DIRECTIVE Section 2.2 (git is the event store); DIRECTIVE Section 5 (structural constraints).

### P4: Immutability After Write

Once a run record entry is written, it must not be modified. This aligns with the snapshot immutability invariant (K-SNAP-1) and preserves the audit trail integrity.

**Implication:** Use an append-only model. If a run needs correction, annotate it with a subsequent entry rather than editing the original.

**Note on K-SNAP-1 applicability (Lensing item A-002):** K-SNAP-1 governs snapshot-folder-level immutability. If Option A (append-only file) is chosen, the immutability guarantee is at the individual-entry level within a growing file, which is a semantic extension of K-SNAP-1 rather than a direct application. See REQ-03 in Specification and Conflict Table CON-06 for the applicability question.

Source: K-SNAP-1 (CONTRACT); SPEC Section 11.1.

### P5: Baseline SHA Is the Bridge to Staleness

The most architecturally significant field in the run record schema is the baseline SHA (or content hash). This field bridges run records to staleness detection:

- K-VAL-1 says: "A deliverable is dirty if any governed input has changed since its last approved SHA."
- K-STALE-1 says: "Upstream changes propagate staleness to all transitive dependent deliverables."
- DEL-08-07 (Staleness Propagation + Triage Tooling) explicitly "depends on run records with baseline SHAs" (PLAN Section 3.7).

**Implication:** The SHA computation method must be well-defined and reproducible. Whether it is the git HEAD SHA, a composite hash of input files, or a hash of the deliverable folder, the method must be documented and deterministic.

**Requirement level tension (Lensing items F-002, E-003):** Given the architectural significance of this field and the downstream dependency from DEL-08-07, the current SHOULD requirement level for `InputContextSHA` (REQ-01) may be insufficient. If this field is omitted from a run record, DEL-08-07's staleness detection cannot function for that run. See Conflict Table CON-05 and cross-matrix conflict XCON-01 for human ruling.

Source: K-VAL-1, K-STALE-1 (CONTRACT); PLAN Section 3.7.

## Considerations

### C1: Storage Location Trade-offs

The storage location decision (REQ-02 in Specification) is the most consequential design choice for this deliverable. Key considerations:

**Deliverable-local (Option A: `_RUN_HISTORY.md` or `RunRecords.csv`):**
- Consistent with the deliverable-local-register pattern (`_DEPENDENCIES.md`, `Dependencies.csv`).
- Easy for agents and humans to find — it is in the deliverable folder alongside all other deliverable state.
- Grows over time, but run records are small (a few hundred bytes each) and runs are infrequent enough that file size is unlikely to be a concern.
- Append-only Markdown is human-readable; CSV is machine-parseable.

**Tool-root snapshot (Option B):**
- Strict immutability per K-SNAP-1 (each run is a separate snapshot folder).
- But: dispersed across tool roots; harder to see the run history for a single deliverable without aggregation.
- May conflict with the "one storage location" constraint if the tool root is different from the deliverable folder.

**Recommendation (PROPOSAL):** Option A (deliverable-local) is the most consistent with existing patterns and the "one schema + one storage location" constraint. A Markdown file (`_RUN_HISTORY.md`) is recommended for human readability; a CSV file (`RunRecords.csv`) is recommended if machine parsing is the priority. The choice may depend on whether downstream consumers (DEL-08-07) prefer structured CSV or human-readable Markdown.

### C2: Schema Versioning

Following the pattern established by `Dependencies.csv` v3.1 (SPEC Section 6.1), the run record schema should include a version identifier in every record. This enables future schema evolution without breaking existing records.

**ASSUMPTION:** A `SchemaVersion` field (e.g., `v1.0`) in each record or file header is sufficient.

### C3: RunID Format

The RunID must be unique, sortable, and informative. Consider:
- `RUN-{DEL-ID}-{YYYYMMDD}-{HHmm}-{SEQ}` — includes deliverable, date, time, and sequence number for same-minute collisions.
- Alternatively, use a UUID for global uniqueness, but this sacrifices human readability and sortability.

**ASSUMPTION:** The timestamp-based format is preferred for consistency with existing naming conventions (snapshot folders use `{LABEL}_{YYYY-MM-DD}_{HHmm}` per SPEC Section 11.1).

### C4: Agent Protocol Integration Scope

The requirement to integrate run record emission into Type 2 agent protocols is the largest integration surface. Current Type 2 agents include (at minimum):
- 4_DOCUMENTS
- DEPENDENCIES
- CHIRALITY_FRAMEWORK
- CHIRALITY_LENS

Each agent would need a final step that writes a run record. The implementation should be a shared utility (not copy-pasted into each agent) to ensure consistency.

**ASSUMPTION:** A shared run record emission function/protocol step can be defined once and referenced by all Type 2 agents. The phrase "at minimum" reflects that the current agent inventory may not be exhaustive; a definitive enumeration requires review of the agent instruction suite at implementation time (Lensing item B-002).

### C5: Relationship to OI-037 (Scope Decision)

SOW-037 is currently TBD. The scope decision (OI-037: "Decide whether to include unified run record schema/persistence") must be resolved before implementation work begins. This deliverable's document kit can be prepared in advance to inform that decision, but CODE and TEST artifacts require a scope flip to IN.

**Specification now includes a SHALL-level prerequisite gate (REQ-SCOPE-GATE)** that formalizes this relationship as a normative requirement rather than an advisory note (Lensing item F-001).

### C6: Schema Evolution Governance (Lensing item D-001)

When the `SchemaVersion` field increments (e.g., from `v1.0` to `v2.0`), a governance path is needed for:

1. **Migration of existing records:** Are old-version records migrated in place (violating immutability), left as-is (requiring multi-version parsing), or annotated with a migration note?
2. **Backward compatibility:** Must new schema versions be backward-compatible with older readers? Or is a version gate sufficient (readers check SchemaVersion before parsing)?
3. **Version increment triggers:** What changes constitute a version increment? Adding an optional field may not require a version bump; removing or renaming a MUST field would.

**PROPOSAL:** Existing records are never modified (consistent with P4: Immutability After Write). Schema evolution uses additive changes (new optional fields) without version bumps for minor additions. Major changes (field removal, type changes, semantic changes to existing fields) require a version increment, and the run record reader must support parsing all historical versions. This is consistent with the Dependencies.csv v3.1 evolution pattern.

**TBD:** Formal governance rules. This consideration should be documented in the Schema Evolution Guide (see Specification Documentation section).

Source: Specification REQ-01 SchemaVersion field; Guidance C2; `_SEMANTIC_LENSING.md` item D-001.

### C7: Error Handling Rationale (Lensing item X-002)

REQ-04 states that run record emission failure MUST NOT fail the overall agent run. Procedure Step 2.1 says "log warning; do not fail the agent run." The rationale for this approach:

**Why "log warning; do not fail":**
- Run records are a supplementary audit artifact, not a primary agent output. Failing an otherwise successful agent run because of a metadata write failure would cause unnecessary rework.
- The agent's primary outputs (e.g., the four documents for 4_DOCUMENTS, Dependencies.csv for DEPENDENCIES) are the deliverable artifacts the human and downstream consumers depend on. These are higher priority than the run record.
- K-INVENT-1 (no invented values) is not violated by a missing run record — the record simply does not exist for that run.

**Risks of silent failure:**
- A missing run record means DEL-08-07 (staleness detection) will have no baseline SHA for that run, potentially causing a false-stale assessment.
- Repeated silent failures could go unnoticed, eroding the audit trail.
- If the failure is systemic (e.g., disk full, permissions error), it will affect all subsequent runs.

**Mitigation (PROPOSAL):**
- The warning SHOULD be visible in ORCHESTRATOR's run summary (not just agent-local logging).
- If run record emission fails for N consecutive runs (N TBD), escalate to a human-visible alert rather than continuing silently.
- The `Notes` field in `_STATUS.md` history entries could record "run record emission failed" as a secondary audit trail.

Source: Specification REQ-04; Procedure Step 2.1; `_SEMANTIC_LENSING.md` item X-002.

## Trade-offs

| Trade-off | Option A | Option B | Recommendation |
|-----------|----------|----------|----------------|
| **Format** | Markdown (human-readable, less structured) | CSV (machine-parseable, less readable) | TBD — depends on primary consumer (human audit vs. DEL-08-07 tooling) |
| **Location** | Deliverable-local (consistent, collocated) | Tool-root snapshot (strictly immutable) | Deliverable-local (PROPOSAL) — see C1 |
| **Granularity** | One record per agent run | One record per pass within a run | One per agent run (PROPOSAL) — passes are sub-run detail, not separate audit events |
| **SHA method** | Git HEAD SHA (simple, coarse) | Per-file content hash (precise, expensive) | TBD — precision vs. complexity trade-off requires design review |
| **Scope** | Type 2 agents only | All agent types | Type 2 only (PLAN Section 3.6 specifies "per Agent 2 execution") |

## Examples

### Example Run Record Entry (Markdown format — PROPOSAL)

```markdown
### RUN-DEL-08-06-20260301-1423-001

| Field | Value |
|-------|-------|
| **DeliverableID** | DEL-08-06 |
| **AgentName** | 4_DOCUMENTS |
| **AgentType** | TYPE_2 |
| **RunTimestamp** | 2026-03-01T14:23:00Z |
| **RunDuration** | PT2M34S |
| **RunStatus** | SUCCESS |
| **RunPassDirective** | P1_P2 |
| **InputContextSHA** | abc1234 |
| **InputFiles** | _CONTEXT.md, _DEPENDENCIES.md, _REFERENCES.md, _STATUS.md |
| **OutputFiles** | Datasheet.md, Specification.md, Guidance.md, Procedure.md |
| **StatusBefore** | OPEN |
| **StatusAfter** | INITIALIZED |
| **ErrorSummary** | — |
| **Notes** | — |
| **SchemaVersion** | v1.0 |
```

### Example Run Record Entry (CSV format — PROPOSAL)

```csv
SchemaVersion,RunID,DeliverableID,AgentName,AgentType,RunTimestamp,RunDuration,RunStatus,RunPassDirective,InputContextSHA,InputFiles,OutputFiles,StatusBefore,StatusAfter,ErrorSummary,Notes
v1.0,RUN-DEL-08-06-20260301-1423-001,DEL-08-06,4_DOCUMENTS,TYPE_2,2026-03-01T14:23:00Z,PT2M34S,SUCCESS,P1_P2,abc1234,"_CONTEXT.md;_DEPENDENCIES.md;_REFERENCES.md;_STATUS.md","Datasheet.md;Specification.md;Guidance.md;Procedure.md",OPEN,INITIALIZED,,
```

> Note: These are illustrative examples (PROPOSAL). The final format depends on the storage location and format decisions (TBD).

## Terminology Note (Lensing item E-004)

The canonical term for the core concept in this deliverable is **"run record"** (two words, no hyphen, lowercase unless at start of sentence). Variants that appear in source documents and should be normalized:
- "run record" — **canonical**
- "run-record" (hyphenated) — avoid; use "run record"
- "run record entry" — acceptable when referring to a single entry within a multi-record file
- "run record schema" — acceptable when referring to the schema definition specifically
- "unified run record" — acceptable when distinguishing from the existing fragmented tracking mechanisms

This terminology note applies across all four documents (Datasheet, Specification, Guidance, Procedure).

Source: `_SEMANTIC_LENSING.md` item E-004.

## Conflict Table (for human ruling)

| Conflict ID | Conflict | Source A | Source B | Impacted Sections | Proposed Authority | Human Ruling |
|-------------|---------|----------|----------|-------------------|-------------------|--------------|
| CON-01 | Storage location: deliverable-local vs. tool-root snapshot | PLAN Section 3.6 ("storage location decision" — no preference stated) | SPEC Section 11 (snapshot conventions favor tool-root for immutability) | REQ-02; C1 | PLAN Section 3.6 (defers to design decision) — PROPOSAL: deliverable-local | TBD |
| CON-02 | File format: Markdown vs. CSV | DIRECTIVE Section 2.1 (plain files, human-readable) | SPEC Section 6 (Dependencies.csv pattern favors CSV for structured data) | REQ-01; Trade-offs table | Either is valid; depends on primary consumer — PROPOSAL: Markdown for human readability with optional CSV export | TBD |
| CON-03 | SHA method: git HEAD vs. per-file content hash | K-VAL-1 ("last approved SHA" implies git SHA) | K-GHOST-1 (context is folder contents — suggests per-file hash) | REQ-05 | TBD — requires design review of precision vs. complexity | TBD |
| CON-04 | Scope item status: TBD vs. documents proceeding as if scope is decided | Datasheet Identification "Scope Item Status: TBD" | Specification Requirements (proceed to define requirements as if scope is determined) | Datasheet Identification; Specification Requirements; C5 | OI-037 resolution — PROPOSAL: adopt conditional framing ("if SOW-037 is flipped to IN, then...") or proceed with current approach (document kit prepared in advance) and gate CODE/TEST on scope flip | TBD |
| CON-05 | InputContextSHA requirement level: SHOULD vs. MUST | Specification REQ-01 field table (InputContextSHA: SHOULD) | Guidance P5 ("most architecturally significant field"); DEL-08-07 dependency on baseline SHAs | REQ-01; REQ-05; P5; DEL-08-07 dependency | Specification (normative authority) — PROPOSAL: elevate to MUST, or document why SHOULD is acceptable given downstream dependency risk | TBD |
| CON-06 | K-SNAP-1 applicability to append-only file model | K-SNAP-1 (CONTRACT): governs snapshot folder immutability | REQ-03: append-only file model where the file grows but entries are immutable | REQ-03; P4; Standards table K-SNAP-1 row | K-SNAP-1 (CONTRACT) — PROPOSAL: K-SNAP-1 applies at the entry level by semantic extension; if this is insufficient, define a supplementary invariant (e.g., K-APPEND-1) | TBD |

### Cross-Matrix Conflict Register (from `_SEMANTIC_LENSING.md`)

The following cross-matrix conflicts consolidate items identified across multiple lensing matrices:

| ConflictID | Related ItemIDs | Core Tension | Documents Involved | Ruling Needed |
|---|---|---|---|---|
| XCON-01 | F-002, E-003 | InputContextSHA is SHOULD in REQ-01 but architecturally critical per Guidance P5 and required by DEL-08-07 | Specification, Guidance | Elevate to MUST or document why SHOULD is acceptable — see CON-05 |
| XCON-02 | A-002, C-001 | K-SNAP-1 (snapshot immutability) cited for REQ-03 but delivery model is append-only (Option A), and SHA method is undefined | Specification, CONTRACT | Clarify K-SNAP-1 applicability to append-only — see CON-06; resolve SHA method — see CON-03 |
| XCON-03 | E-001 | Scope Item Status TBD vs. documents proceeding as if scope is decided | Datasheet, Specification, Guidance | Resolve OI-037 or adopt conditional framing — see CON-04 |
