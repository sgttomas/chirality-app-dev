# Guidance -- DEL-06-01 Agent Instruction Suite Structural Conformance

## Purpose

This deliverable exists because the agent instruction suite (`agents/AGENT_*.md`) is the operational backbone of the Chirality agentic workflow system. Structural conformance ensures:

1. **Harness runtime can parse agent metadata reliably** -- YAML frontmatter and body-level `AGENT_TYPE` lines are consumed by the runtime for agent classification, subagent registry safety, and delegation governance. (Source: SPEC.md Section 9.7)

2. **Human operators can navigate agents predictably** -- Consistent structure (header, type table, four canonical sections) allows operators and reviewers to locate protocol, specification, structure, and rationale in any agent file without searching. (Source: SPEC.md Section 9.3)

3. **Contract enforcement is mechanically verifiable** -- Write scope declarations (K-WRITE-1) and subagent governance rules (SPEC.md Section 9.7) can only be enforced if they are consistently declared and formatted across the suite. (Source: CONTRACT.md Section 1.10)

4. **The agent suite is auditable** -- `AGENT_AUDIT_AGENTS.md` provides a fill-in rubric for checking conformance. Structural consistency is a prerequisite for this rubric to function. (Source: AGENTS.md Section 0)

Source: Decomposition DEL-06-01 narrative; AGENTS.md Section 0; SOW-031.

### OBJ-006 Mapping Rationale (lensing item F-001)

This deliverable is associated with OBJ-006 ("Validation posture and governance/agent-suite conformance enable repeatable operation") via the Scope Ledger, which maps SOW-031 to PKG-06/DEL-06-01 with OBJ-006 linkage. The association is directionally strong because OBJ-006's acceptance criteria explicitly include "agents/* instruction suite conforms to HELPS_HUMANS structure" -- which is precisely this deliverable's scope.

The mapping remains labeled **ASSUMPTION (best-effort mapping via PKG-06 package grouping)** because the decomposition's objective-to-deliverable mapping is best-effort per the decomposition methodology. If the human confirms the mapping, the ASSUMPTION label should be removed from the Datasheet and Specification traceability entries.

Source: Decomposition, Scope Ledger SOW-031 row; OBJ-006 acceptance criteria (Decomposition, Objectives section).

---

## Principles

### P1: Conformance Is Structural, Not Semantic

This deliverable addresses **structural** conformance: the presence and format of required elements (headers, tables, section markers, frontmatter). It does not assess whether the instruction content is semantically correct, complete, or optimal.

Semantic correctness is a separate concern that belongs to human review and domain expert judgment.

Source: HELPS_HUMANS RATIONALE section (non-normative); DIRECTIVE.md Section 2.3 (human authority at every gate).

### P2: The Canonical Standard Is Authoritative

`AGENT_HELPS_HUMANS.md` is the conformance target. Where any other `AGENT_*.md` file disagrees with the structure defined by HELPS_HUMANS, the other file must be edited to conform.

Source: AGENTS.md Section 0 -- "Where any other `AGENT_*` file disagrees, the other file must be edited to conform."

### P3: Minimal Disruption to Instruction Content

Conformance updates should add/restructure required structural elements without unnecessarily altering the semantic content of instruction files. If content must be reorganized to fit the four-section structure, the reorganization should preserve meaning.

Source: **ASSUMPTION** -- derived from DIRECTIVE.md Section 2.4 (evidence over plausibility) and the principle that agents should not introduce unwarranted changes.

### P4: Write Scope Values Must Be Accurate

The `WRITE_SCOPE` property is not merely structural -- it defines an enforceable boundary (K-WRITE-1). When declaring or correcting a write scope value, the value must accurately reflect the agent's actual write behavior as documented in its PROTOCOL section.

Source: CONTRACT.md K-WRITE-1; SPEC.md Section 9.5.

---

## Considerations

### C1: Scope of "Instruction Files" vs. "Harness Agents"

The `agents/` directory contains the instruction-root files shipped with the app bundle. The `.claude/agents/` directory contains harness execution agent configurations. DEL-06-01 targets the instruction-root files only (`agents/AGENT_*.md`).

**ASSUMPTION:** The `.claude/agents/` files are not governed by the same structural conformance requirements as `agents/AGENT_*.md` files. They serve as harness runtime configurations with different structural conventions.

### C2: Template Files

`MEMORY_TEMPLATE.md` and `TASK_ESTIMATING_TEMPLATE.md` in `agents/` are not instruction files. They are template artifacts used by agents during execution. These are excluded from structural conformance checking.

Source: Filesystem scan -- these files do not match the `AGENT_*` naming convention.

### C3: AGENT_HELPS_HUMANS.md Self-Conformance

`AGENT_HELPS_HUMANS.md` is both the conformance target and a member of the instruction suite. It should be checked for conformance to its own structure, since the runtime metadata contract (SPEC.md Section 9.7) applies to all `AGENT_*.md` files.

Source: **ASSUMPTION** -- the standard should be self-consistent.

### C4: Agent Instruction Hardening Status

Per PLAN.md Section 1, QA Contract sections have been added to some agents (PREPARATION, 4_DOCUMENTS, CHIRALITY_FRAMEWORK, CHIRALITY_LENS) and Output Persistence notes have been added to others (ORCHESTRATOR, RECONCILIATION). The current estimated consistency is "92% to estimated 95%+ after hardening."

This deliverable should move the suite from its current state toward full structural conformance. The Datasheet records the baseline conformance level as TBD pending a pre-edit audit (Procedure Step 2).

Source: PLAN.md Section 1 (Agent Instruction Hardening).

### C5: Precedence of SPEC.md Section 9 vs. HELPS_HUMANS

Both SPEC.md Section 9 and `AGENT_HELPS_HUMANS.md` define agent instruction structure. SPEC.md Section 9 is the normative specification; HELPS_HUMANS is the canonical standard that instructions must conform to. If the two disagree, a conflict must be surfaced (per K-CONFLICT-1).

At present, SPEC.md Section 9 appears to be derived from and aligned with HELPS_HUMANS. No conflicts have been identified during this draft. If conflicts are discovered during execution, they should be added to the Conflict Table below.

**Conflict escalation procedure (lensing item E-001):** If a conflict between SPEC.md Section 9 and HELPS_HUMANS is discovered during execution:

1. **Halt conformance edits** for the affected file(s) -- do not force conformance to either source until the conflict is resolved.
2. **Record the conflict** in the Conflict Table below (this document, Guidance.md) with both source references and impacted sections.
3. **Escalate to the human** via the deliverable's working session (WORKING_ITEMS or ORCHESTRATOR), citing K-CONFLICT-1 as the governing rule.
4. **Do not resume edits** for the affected file(s) until the human provides a ruling in the Conflict Table's "Human Ruling" column.

The governing rule for conflict resolution is K-CONFLICT-1 (CONTRACT.md). The escalation target is the human operator responsible for this deliverable. (Source: CONTRACT.md K-CONFLICT-1; AGENTS.md Section 0; **ASSUMPTION**: escalation path follows standard human-authority-at-every-gate principle per DIRECTIVE.md Section 2.3)

Source: AGENTS.md Section 0; CONTRACT.md K-CONFLICT-1.

### C6: AGENT_CLASS Vocabulary Authority (lensing item X-003)

Specification REQ-03 lists `AGENT_CLASS` valid values as `PERSONA` and `TASK`. REQ-09 requires consistency with `AGENTS.md` (Full Agent Type Table). The authoritative source for the AGENT_CLASS vocabulary is:

- **SPEC.md Section 9.2** defines the required Agent Type table structure and its valid values (normative specification).
- **HELPS_HUMANS STRUCTURE section** defines the Agent Header Block including AGENT_CLASS (canonical standard).
- **AGENTS.md Section 2** (Full Agent Type Table) records the classification of each agent (operator-facing index).

If these three sources disagree on valid AGENT_CLASS values, SPEC.md Section 9.2 is the normative authority, HELPS_HUMANS is the conformance target, and AGENTS.md is the operational record. Per K-CONFLICT-1, any disagreement should be surfaced as a conflict.

At present, all three sources appear aligned on `PERSONA` and `TASK` as the valid values. **ASSUMPTION:** No additional AGENT_CLASS values exist beyond `PERSONA` and `TASK`. (Source: SPEC.md Section 9.2; HELPS_HUMANS STRUCTURE; AGENTS.md Section 2)

### C7: Subagent-Capable Agent Identification (lensing item X-002)

REQ-10 (Subagent Governance Compliance) applies only to agents that declare subagent delegation capability. Neither the Specification nor the Datasheet currently identifies which of the 26 in-scope files are subagent-capable.

**To identify the applicable subset**, the operator should:

1. Check each file's YAML frontmatter for a `subagents` field.
2. Check each file's PROTOCOL section for references to spawning, delegating to, or invoking other agents.
3. Cross-reference with AGENTS.md if it records delegation relationships.

The resulting list should be recorded in the conformance audit report (Specification, Documentation section) so that REQ-10 verification has a definitive applicable scope.

**Known subagent-capable agents (ASSUMPTION based on agent descriptions in AGENTS.md and file naming):**
- `AGENT_ORCHESTRATOR.md` -- orchestrates other agents
- **Others:** TBD -- requires file-by-file inspection

Source: SPEC.md Section 9.7; AGENTS.md; **ASSUMPTION**: subset must be confirmed by file inspection.

---

## Trade-offs

### T1: Depth of Conformance Pass

**Option A -- Shallow (structure only):** Check for presence of required elements and add/reformat them. Fastest to execute; minimal risk of introducing semantic errors. Does not improve content quality.

**Option B -- Deep (structure + content alignment):** In addition to structural checks, verify that PROTOCOL/SPEC/STRUCTURE/RATIONALE sections contain content appropriate to their purpose. Slower; risk of scope creep; more valuable long-term.

**Recommendation (PROPOSAL):** Start with Option A (structural conformance) for this deliverable. Content quality improvements can be addressed in a separate iteration or by running AUDIT_AGENTS after structural conformance is achieved.

### T2: Automation vs. Manual Conformance

**Option A -- Automated script:** Build a conformance checking script that reports violations. Then manually fix each violation.

**Option B -- Manual inspection + edit:** Read each file, check against requirements, edit as needed.

**Option C -- AUDIT_AGENTS run:** Use the existing `AGENT_AUDIT_AGENTS.md` agent to produce a conformance report, then address findings.

**Recommendation (PROPOSAL):** Use AUDIT_AGENTS (Option C) as the verification mechanism and perform manual edits (Option B) for the actual conformance updates. Automated scripting (Option A) could be a DEL-08-series hardening candidate but is out of scope for this deliverable.

---

## Examples

### Example: Minimal Conformant Agent Header

The following shows the minimum required structural elements for a conformant agent instruction file (Source: SPEC.md Section 9.1, 9.2, 9.3):

```markdown
---
description: "Brief description of the agent"
---
[[DOC:AGENT_INSTRUCTIONS]]
# AGENT INSTRUCTIONS -- {AGENT_NAME} ({Brief Descriptor})
AGENT_TYPE: {0|1|2}

## Agent Type

| Property | Value |
|---|---|
| **AGENT_TYPE** | TYPE {0|1|2} |
| **AGENT_CLASS** | {PERSONA|TASK} |
| **INTERACTION_SURFACE** | {chat|INIT-TASK|spawned|both} |
| **WRITE_SCOPE** | {scope description} |
| **BLOCKING** | {never|allowed} |
| **PRIMARY_OUTPUTS** | {description} |

[... agent-specific content ...]

[[BEGIN:PROTOCOL]]
## PROTOCOL
[... protocol content ...]
[[END:PROTOCOL]]

[[BEGIN:SPEC]]
## SPEC
[... spec content ...]
[[END:SPEC]]

[[BEGIN:STRUCTURE]]
## STRUCTURE
[... structure content ...]
[[END:STRUCTURE]]

[[BEGIN:RATIONALE]]
## RATIONALE
[... rationale content ...]
[[END:RATIONALE]]
```

---

## Conflict Table (for human ruling)

| Conflict ID | Conflict | Source A | Source B | Impacted Sections | Proposed Authority | Human Ruling |
|-------------|----------|----------|----------|-------------------|--------------------|--------------|
| CT-001 | REQ-05 and REQ-06 use SHOULD (advisory) while REQ-01 through REQ-04 and REQ-07 through REQ-10 use MUST (mandatory). Mixed modality weakens enforceability of the conformance standard as a whole. Should REQ-05 and REQ-06 be elevated to MUST, or should they be explicitly documented as advisory with rationale? | SPEC.md Section 9.4 (REQ-05: "SHOULD include an explicit precedence order") | SPEC.md Section 9.7 (REQ-06: "SHOULD include YAML frontmatter") | Specification REQ-05, REQ-06; Procedure Step 1 checklist; Verification table | Specification.md (PROPOSAL: document the intent -- if SPEC.md uses SHOULD intentionally, preserve it and add a note explaining advisory status; if SHOULD is unintentional, elevate to MUST) | TBD |
