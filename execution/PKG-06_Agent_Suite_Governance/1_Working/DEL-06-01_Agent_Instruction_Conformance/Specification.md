# Specification -- DEL-06-01 Agent Instruction Suite Structural Conformance

## Scope

### What This Deliverable Covers

This deliverable covers bringing all `AGENT_*.md` instruction files in the `agents/` directory into structural conformance with the `AGENT_HELPS_HUMANS.md` canonical standard (v1.1) and `docs/SPEC.md` Section 9.

**In scope:**
- Structural conformance of agent instruction file headers, Agent Type tables, required section markers, and YAML frontmatter
- Write scope declaration compliance (CONTRACT invariant K-WRITE-1)
- Naming convention compliance (`AGENT_*` for files, role names for agent references)
- Precedence order compliance (PROTOCOL > SPEC > STRUCTURE > RATIONALE)

**Out of scope:**
- Semantic correctness of instruction content (covered by human review and AUDIT_AGENTS)
- Agent behavioral changes or capability modifications
- Template files (`MEMORY_TEMPLATE.md`, `TASK_ESTIMATING_TEMPLATE.md`) -- these are not instruction files
- Files in `.claude/agents/` -- these are harness execution agents, not instruction-root files

Source: Decomposition DEL-06-01 entry; AGENTS.md Section 0; SPEC.md Section 9.

### Scope Item Traceability

| Scope Item | Statement | Coverage |
|------------|-----------|----------|
| SOW-031 | Maintain agent instruction suite (`agents/*`) conformance to `AGENT_HELPS_HUMANS.md`. | Full -- this is the sole scope item for DEL-06-01. |

Source: Scope Ledger row for SOW-031 (Decomposition).

---

## Requirements

### REQ-01: Required Header Marker

Every `AGENT_*.md` instruction file MUST include the document type marker:

```
[[DOC:AGENT_INSTRUCTIONS]]
```

Source: SPEC.md Section 9.1.

### REQ-02: Required AGENT_TYPE Line

Every `AGENT_*.md` instruction file MUST include an `AGENT_TYPE` line in the body:

```
AGENT_TYPE: {0|1|2}
```

This line is consumed by harness runtime metadata parsing (SPEC.md Section 9.7).

Source: SPEC.md Section 9.1; SPEC.md Section 9.7.

### REQ-03: Required Agent Type Table

Every `AGENT_*.md` instruction file MUST include an Agent Type table with all six required properties:

| Property | Valid Values |
|----------|-------------|
| `AGENT_TYPE` | `TYPE 0`, `TYPE 1`, `TYPE 2` |
| `AGENT_CLASS` | `PERSONA`, `TASK` |
| `INTERACTION_SURFACE` | `chat`, `INIT-TASK`, `spawned`, `both` |
| `WRITE_SCOPE` | `repo-wide`, `deliverable-local`, `tool-root-only`, `workspace-scaffold-only`, `repo-metadata-only`, `none` |
| `BLOCKING` | `never`, `allowed` |
| `PRIMARY_OUTPUTS` | (free-form description) |

**Note on AGENT_CLASS vocabulary:** The valid values `PERSONA` and `TASK` are defined in this table per SPEC.md Section 9.2 and HELPS_HUMANS STRUCTURE. See Guidance X-003 note for vocabulary authority clarification. (Source: SPEC.md Section 9.2; HELPS_HUMANS STRUCTURE)

Source: SPEC.md Section 9.2; HELPS_HUMANS STRUCTURE section (Agent Header Block).

### REQ-04: Required Section Markers

Every `AGENT_*.md` instruction file MUST include four section markers:

| Section | Open Marker | Close Marker |
|---------|-------------|--------------|
| PROTOCOL | `[[BEGIN:PROTOCOL]]` | `[[END:PROTOCOL]]` |
| SPEC | `[[BEGIN:SPEC]]` | `[[END:SPEC]]` |
| STRUCTURE | `[[BEGIN:STRUCTURE]]` | `[[END:STRUCTURE]]` |
| RATIONALE | `[[BEGIN:RATIONALE]]` | `[[END:RATIONALE]]` |

Source: SPEC.md Section 9.3.

### REQ-05: Precedence Order Statement

Every `AGENT_*.md` instruction file SHOULD include an explicit precedence order statement:

```
PROTOCOL > SPEC > STRUCTURE > RATIONALE
```

**Modality note (lensing items A-002, C-002):** This requirement uses SHOULD (advisory) while REQ-01 through REQ-04 and REQ-07 through REQ-10 use MUST (mandatory). This creates mixed enforceability. See Conflict Table entry CT-001 in Guidance.md for human ruling on whether this should be elevated to MUST or explicitly documented as advisory. (Source: SPEC.md Section 9.4)

Source: SPEC.md Section 9.4.

### REQ-06: YAML Frontmatter for Harness Runtime

Agent instruction files that participate in harness runtime SHOULD include YAML frontmatter with machine-parseable fields:

- `description` (recommended for all)
- `subagents` (when applicable)
- `tools` (when applicable)
- `model` (when applicable)
- `max_turns` (when applicable)
- `disallowed_tools` (when applicable)
- `auto_approve_tools` (when applicable)

**Modality note (lensing item C-002):** This requirement uses SHOULD (advisory), consistent with REQ-05. See Conflict Table entry CT-001 in Guidance.md for human ruling on modality harmonization. (Source: SPEC.md Section 9.7)

Source: SPEC.md Section 9.7.

### REQ-07: Write Scope Declaration (K-WRITE-1)

Every agent MUST have an explicit `WRITE_SCOPE` declared in its Agent Type table. The declared scope must use one of the canonical values from SPEC.md Section 9.5.

**Canonical WRITE_SCOPE values** (lensing item C-001; enumerated here for local enforceability):

| Value | Meaning |
|-------|---------|
| `repo-wide` | Agent may write anywhere in the repository |
| `deliverable-local` | Agent may write only within the deliverable folder it is operating on |
| `tool-root-only` | Agent may write only to designated tool root directories |
| `workspace-scaffold-only` | Agent may write only when creating workspace scaffolding |
| `repo-metadata-only` | Agent may write only to repository-level metadata files |
| `none` | Agent produces no file outputs |

**Note:** The values above are sourced from the REQ-03 Agent Type Table valid values list, which is derived from SPEC.md Section 9.5 and HELPS_HUMANS STRUCTURE. If SPEC.md Section 9.5 defines additional or different values, that section is authoritative. (Source: SPEC.md Section 9.5, location TBD for exact enumeration; CONTRACT.md K-WRITE-1)

Source: CONTRACT.md K-WRITE-1; SPEC.md Section 9.5.

### REQ-08: Naming Convention Compliance

All agent instruction files MUST:
- Use the `AGENT_*` prefix for filenames (e.g., `AGENT_CHANGE.md`)
- Use the role name when referring to the agent in prose (e.g., `CHANGE`)
- Include the naming convention statement

Source: SPEC.md Section 9.6; HELPS_HUMANS preamble; AGENTS.md Section 0.

### REQ-09: AGENT_CLASS Consistency with AGENTS.md

The `AGENT_CLASS` value declared in each instruction file MUST be consistent with the classification recorded in `AGENTS.md` (Full Agent Type Table).

Source: AGENTS.md Section 2; SPEC.md Section 9.2.

### REQ-10: Subagent Governance Compliance

Agent instruction files declaring subagent delegation capability MUST comply with the delegation governance rule:
- Delegated subagents MUST declare `AGENT_TYPE: 2`
- `AGENT_CLASS: TASK` is preferred for delegated subagents (warning-level)
- Missing/invalid governance metadata MUST block subagent injection

**Applicable scope (lensing item X-002):** REQ-10 applies only to agent instruction files that declare subagent delegation capability (i.e., those with a `subagents` field in YAML frontmatter or those that reference spawning/delegating to other agents in their PROTOCOL section). The specific subset of the 26 in-scope files that are subagent-capable is TBD -- **requires identification by inspecting each file's YAML frontmatter and PROTOCOL section for delegation references.** See Guidance note X-002 for further detail. (Source: SPEC.md Section 9.7; **ASSUMPTION**: applicable subset must be determined by file inspection)

Source: SPEC.md Section 9.7.

---

## Standards

| Standard / Document | Relevance | Accessibility |
|---------------------|-----------|---------------|
| `AGENT_HELPS_HUMANS.md` (v1.1, 2026-01-30) | Canonical conformance target for all agent instruction files | Accessible (`agents/AGENT_HELPS_HUMANS.md`) |
| `docs/SPEC.md` Section 9 | Agent Instruction File Structure specification | Accessible |
| `docs/CONTRACT.md` K-WRITE-1 | Write scope invariant | Accessible |
| `docs/TYPES.md` Section 4 | Agent role vocabulary and classification | Accessible |
| `AGENTS.md` | Agent framework index and classification reference | Accessible |

---

## Verification

| Req ID | Verification Approach | Verification Detail |
|--------|----------------------|---------------------|
| REQ-01 | Inspection | Confirm `[[DOC:AGENT_INSTRUCTIONS]]` marker present in each file |
| REQ-02 | Inspection | Confirm `AGENT_TYPE: {0\|1\|2}` line present in each file body |
| REQ-03 | Inspection | Confirm Agent Type table present with all six properties using valid enum values |
| REQ-04 | Inspection | Confirm all four section markers (`[[BEGIN:*]]`/`[[END:*]]`) present in each file |
| REQ-05 | Inspection | Confirm precedence order statement present or inferable |
| REQ-06 | Inspection | Confirm YAML frontmatter present where applicable; validate field names |
| REQ-07 | Inspection | Confirm `WRITE_SCOPE` present and uses a canonical value from the enumerated list in REQ-07 |
| REQ-08 | Inspection | Confirm `AGENT_*` file naming and role-name usage in prose |
| REQ-09 | Inspection (cross-reference) | Confirm `AGENT_CLASS` values match AGENTS.md Full Agent Type Table. **Note (lensing item X-004):** The verification method for REQ-09 was previously labeled "Cross-reference" while all other REQs used "Inspection." Cross-referencing AGENTS.md is a sub-method of Inspection; the approach is unified here as "Inspection (cross-reference)" for consistency across the verification table. (Source: AGENTS.md Section 2) |
| REQ-10 | Inspection | Confirm subagent-capable agents comply with delegation governance rules. **Verification detail (lensing item X-001):** (1) Identify which of the 26 files declare subagent capability (check YAML `subagents` field and PROTOCOL section for delegation references). (2) For each identified file, confirm delegated agents declare `AGENT_TYPE: 2`. (3) Confirm `AGENT_CLASS: TASK` preference is documented or warned. (4) Confirm missing/invalid governance metadata blocks injection. **Pass criterion:** all identified subagent-capable files comply; files without subagent capability are N/A for this requirement. (Source: SPEC.md Section 9.7) |

**Verification tool:** `AGENT_AUDIT_AGENTS.md` provides a structured conformance rubric that can be used as the primary audit mechanism. (Source: AGENTS.md Section 0)

### Pass/Fail Threshold (lensing item F-003)

**Full conformance (target):** All 26 files pass all applicable checklist items (REQ-01 through REQ-10).

**Partial conformance handling:** If one or more files cannot be fully conformed during this deliverable's execution (e.g., because a conflict between SPEC.md Section 9 and HELPS_HUMANS is discovered, or because a file's structural change would unavoidably alter semantic meaning), the following applies:

- Each non-conformant file must be individually documented with the specific requirement(s) it fails and the reason conformance was not achieved.
- The deliverable is considered **conditionally passed** if:
  - All non-conformances are documented with rationale,
  - A remediation path is identified for each, and
  - The total non-conformant file count does not exceed TBD (human to set threshold).
- The deliverable is considered **failed** if non-conformances are undocumented or if no remediation path exists.

**ASSUMPTION:** The pass/fail threshold for partial conformance requires human ruling on the maximum acceptable non-conformant file count. (Source: Specification Verification section; Procedure Step 6)

---

## Documentation

### Required Artifacts

| Artifact | Format | Description |
|----------|--------|-------------|
| Updated `AGENT_*.md` files | Markdown | Agent instruction files brought into structural conformance |
| Conformance audit report | TBD -- **format decision required (lensing item F-002).** Options: (a) Markdown table in the deliverable folder summarizing per-file pass/fail across REQ-01 through REQ-10, or (b) CSV file with columns `File, REQ-01, ..., REQ-10, Notes` for machine-parseable consumption, or (c) output of `AGENT_AUDIT_AGENTS.md` run in its native format. **ASSUMPTION: production method is running AUDIT_AGENTS as a verification step; format will follow AUDIT_AGENTS output conventions.** (Source: AGENTS.md Section 0) |

### Traceability

| Trace Target | Trace Type |
|--------------|------------|
| SOW-031 | Scope item coverage |
| OBJ-006 | Objective support -- **ASSUMPTION (best-effort mapping)** |
| K-WRITE-1 | Contract invariant enforcement |
| SPEC.md Section 9 | Specification conformance |
