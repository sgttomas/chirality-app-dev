# Procedure -- DEL-06-01 Agent Instruction Suite Structural Conformance

## Purpose

This procedure describes the steps to bring the agent instruction suite (`agents/AGENT_*.md`) into structural conformance with `AGENT_HELPS_HUMANS.md` and `docs/SPEC.md` Section 9, and to verify the result.

---

## Prerequisites

| Prerequisite | Source | Status |
|-------------|--------|--------|
| `AGENT_HELPS_HUMANS.md` (v1.1) is accessible at `agents/AGENT_HELPS_HUMANS.md` | AGENTS.md Section 0 | Available |
| `docs/SPEC.md` Section 9 is accessible | SPEC.md | Available |
| `docs/CONTRACT.md` is accessible (for K-WRITE-1 reference) | CONTRACT.md | Available |
| `AGENTS.md` is accessible (for classification cross-reference) | AGENTS.md | Available |
| `AGENT_AUDIT_AGENTS.md` is accessible (for conformance rubric) | AGENTS.md Section 0 | Available |
| All 26 `AGENT_*.md` files in `agents/` are accessible for reading and writing | Filesystem | Available |
| Deliverable DEL-06-01 is in an active state (OPEN, INITIALIZED, SEMANTIC_READY, or IN_PROGRESS) | `_STATUS.md` | SEMANTIC_READY |

**Note (lensing item E-002):** The prerequisite status check originally listed only "OPEN, INITIALIZED, or IN_PROGRESS" as valid active states. The deliverable lifecycle includes SEMANTIC_READY as a valid active state between INITIALIZED and IN_PROGRESS. The prerequisite condition has been updated to include SEMANTIC_READY. (Source: _STATUS.md; TYPES.md lifecycle states)

**Upstream dependencies:** None declared at this time. (Source: `_DEPENDENCIES.md` -- PENDING_EXTRACTION)

**ASSUMPTION:** No upstream deliverables block execution of this work. SOW-031 is self-contained within the agent instruction files. If dependencies are later identified by the DEPENDENCIES agent, they should be reviewed before proceeding.

---

## Steps

### Step 1 -- Establish Conformance Checklist

**Action:** Create a checklist derived from the requirements in Specification.md (REQ-01 through REQ-10).

**Conformance checklist items per file:**

- [ ] `[[DOC:AGENT_INSTRUCTIONS]]` header marker present (REQ-01)
- [ ] `AGENT_TYPE: {0|1|2}` line present in body (REQ-02)
- [ ] Agent Type table present with all six properties (REQ-03):
  - [ ] `AGENT_TYPE` -- valid value
  - [ ] `AGENT_CLASS` -- `PERSONA` or `TASK`
  - [ ] `INTERACTION_SURFACE` -- `chat`, `INIT-TASK`, `spawned`, or `both`
  - [ ] `WRITE_SCOPE` -- canonical value from SPEC.md Section 9.5 (see REQ-07 enumeration)
  - [ ] `BLOCKING` -- `never` or `allowed`
  - [ ] `PRIMARY_OUTPUTS` -- description present
- [ ] All four section markers present (REQ-04):
  - [ ] `[[BEGIN:PROTOCOL]]` / `[[END:PROTOCOL]]`
  - [ ] `[[BEGIN:SPEC]]` / `[[END:SPEC]]`
  - [ ] `[[BEGIN:STRUCTURE]]` / `[[END:STRUCTURE]]`
  - [ ] `[[BEGIN:RATIONALE]]` / `[[END:RATIONALE]]`
- [ ] Precedence order stated or inferable (REQ-05)
- [ ] YAML frontmatter present with `description` field (REQ-06)
- [ ] `WRITE_SCOPE` uses canonical value (REQ-07)
- [ ] File naming follows `AGENT_*` convention (REQ-08)
- [ ] `AGENT_CLASS` consistent with AGENTS.md (REQ-09)
- [ ] Subagent governance compliance (if applicable) (REQ-10)

**Output:** Conformance checklist ready for use.

### Step 2 -- Audit Current State

**Action:** For each of the 26 `AGENT_*.md` files, evaluate against the conformance checklist.

**Recommended approach:**
1. Open each file and check for the presence of each structural element.
2. Record findings in an audit table with columns: `File`, `REQ-01`...`REQ-10`, `Notes`.
3. Identify the set of files requiring changes and the specific changes needed.
4. Record the baseline conformance count (total conformant / total files) as the Datasheet "Baseline Conformance Level" attribute.

**Alternative approach:** Run `AGENT_AUDIT_AGENTS.md` as a pre-work audit to generate a machine-readable conformance report. (Source: AGENTS.md Section 0)

**Output:** Audit findings table identifying all non-conformances; baseline conformance metric.

### Step 3 -- Prioritize and Plan Changes

**Action:** Group the identified non-conformances by type:

| Priority | Change Type | Description |
|----------|-----------|-------------|
| 1 (Critical) | Missing header marker | Add `[[DOC:AGENT_INSTRUCTIONS]]` |
| 1 (Critical) | Missing AGENT_TYPE line | Add `AGENT_TYPE: {N}` line |
| 1 (Critical) | Missing/incomplete Agent Type table | Add or complete table with all six properties |
| 2 (High) | Missing section markers | Add `[[BEGIN:*]]`/`[[END:*]]` markers around existing content |
| 2 (High) | Missing WRITE_SCOPE or non-canonical value | Add or correct write scope declaration |
| 3 (Medium) | Missing YAML frontmatter | Add frontmatter block |
| 3 (Medium) | Naming convention violations | Correct file references in prose |
| 4 (Low) | Missing precedence statement | Add precedence order |

**Output:** Prioritized change plan.

### Step 4 -- Apply Structural Conformance Edits

**Action:** For each file requiring changes, apply the minimum edits necessary to achieve structural conformance.

**Rules:**
- Preserve existing instruction content. Do not alter semantic meaning.
- When adding section markers, wrap existing content that corresponds to the section's purpose.
- When adding an Agent Type table, derive values from:
  - The AGENTS.md Full Agent Type Table (for `AGENT_CLASS`, `INTERACTION_SURFACE`, `PRIMARY_OUTPUTS`)
  - The file's existing content (for `WRITE_SCOPE` if documented elsewhere in the file)
  - CONTRACT.md K-WRITE-1 intent (for `WRITE_SCOPE` if not documented)
- When adding YAML frontmatter, include at minimum a `description` field.
- Label any inferred values as **ASSUMPTION** in commit notes or the audit report.

**Semantic integrity safeguard (lensing item D-001):** If a structural edit is discovered to have inadvertently altered semantic meaning (e.g., wrapping content in a section marker changes the interpretation of that content, or reorganizing content to fit the four-section structure changes its contextual meaning):

1. **Revert the specific edit** to restore the original semantic meaning. Use `git diff` to identify the unintended change and `git checkout -- <file>` or manual revert for the affected section only.
2. **Record the issue** in the conformance audit report with: file name, requirement being addressed, description of the semantic impact, and reason the structural change could not be applied without semantic alteration.
3. **Attempt an alternative structural approach** that achieves conformance without semantic disruption (e.g., different section placement, additional explanatory markers).
4. If no alternative exists, **document the file as a partial non-conformance** per the pass/fail threshold defined in Specification.md (Verification section, "Partial conformance handling").

Source: Procedure.md Step 4 Rules; **ASSUMPTION**: error-recovery path derived from P3 (Minimal Disruption to Instruction Content) in Guidance.md.

**Output:** Updated agent instruction files.

### Step 5 -- Cross-Reference Verification

**Action:** After all edits, verify cross-document consistency:

| Check | What to Verify |
|-------|---------------|
| `AGENT_CLASS` in each file vs. AGENTS.md | Values match |
| `AGENT_TYPE` in each file vs. AGENTS.md | Values match |
| `WRITE_SCOPE` in each file vs. actual documented write behavior | Values are accurate |
| `INTERACTION_SURFACE` in each file vs. AGENTS.md | Values match |
| Naming conventions | All files use `AGENT_*` prefix; prose uses role names |

**Output:** Cross-reference verification results.

### Step 6 -- Post-Edit Audit (Verification)

**Action:** Re-run the conformance checklist (Step 1) against all updated files.

**Acceptance criteria:**
- All 26 files pass all checklist items (REQ-01 through REQ-10), OR partial conformance is documented per the threshold defined in Specification.md
- No new semantic content was introduced (only structural additions)
- AGENTS.md cross-reference is consistent

**Alternative:** Run `AGENT_AUDIT_AGENTS.md` as a post-edit verification pass.

**Output:** Verification report confirming conformance achieved.

### Step 7 -- Update AGENTS.md if Needed

**Action:** If any classification values were corrected during conformance work (e.g., an incorrect `AGENT_CLASS` was found and fixed), update the AGENTS.md Full Agent Type Table to match.

**Note:** AGENTS.md is the operator-facing index. It must remain consistent with the instruction files it indexes.

**Output:** Updated `AGENTS.md` (if changes were required).

---

## Verification

| Check | Method | Pass Criteria |
|-------|--------|---------------|
| All 26 files have `[[DOC:AGENT_INSTRUCTIONS]]` marker | File inspection | Marker present in every file |
| All 26 files have `AGENT_TYPE` line | File inspection | Line present in every file body |
| All 26 files have complete Agent Type table | File inspection | All six properties present with valid values |
| All 26 files have four section markers | File inspection | All eight markers (`BEGIN`+`END` x 4) present per file |
| All WRITE_SCOPE values are canonical | Enum check | Every value matches SPEC.md Section 9.5 list (see REQ-07 enumeration in Specification.md) |
| AGENTS.md consistency | Cross-reference | All classification values match between AGENTS.md and individual files |
| No semantic content changes | Diff review | Git diff shows only structural additions (headers, markers, tables, frontmatter). **Clarification (lensing item D-002):** "Only structural additions" means the diff contains exclusively: (a) new `[[DOC:AGENT_INSTRUCTIONS]]` markers, (b) new or corrected Agent Type table rows, (c) new `[[BEGIN:*]]`/`[[END:*]]` section markers, (d) new YAML frontmatter blocks, (e) new `AGENT_TYPE:` lines, (f) new precedence order statements, and (g) whitespace/formatting changes required to accommodate the above. If content was **reorganized** (moved between sections to fit the four-section structure), the diff will show deletions and additions of the same text in different locations -- this is acceptable provided the moved text is semantically identical (verified by human review of the diff). Any diff hunks that alter the wording, logic, or meaning of instruction content are **not** structural and must be reverted or documented as exceptions. |

---

## Records

| Record | Location | Purpose |
|--------|----------|---------|
| Pre-edit audit report | Deliverable folder (`DEL-06-01_Agent_Instruction_Conformance/`) as a Markdown file, or as part of the conformance audit report artifact | Baseline conformance state before changes |
| Post-edit verification report | Deliverable folder (`DEL-06-01_Agent_Instruction_Conformance/`) as a Markdown file, or as part of the conformance audit report artifact | Confirmed conformance after changes |
| Git commit(s) with conformance edits | Repository history | Auditable record of all changes |
| Updated `AGENTS.md` (if changed) | `AGENTS.md` | Consistent agent classification index |
| Updated `AGENT_*.md` files | `agents/` directory | Conformant instruction files |

**Note (lensing item A-003):** Record locations have been specified as the deliverable folder for pre-edit and post-edit reports. If a different convention is established (e.g., commit messages, a dedicated reports subfolder), update this table accordingly. (Source: Procedure.md Records)
