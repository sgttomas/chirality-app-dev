# Working Memory — DEL-06-01

*This file is shared working memory for WORKING_ITEMS and TASK agents operating on this deliverable.*

## Key Decisions & Human Rulings

- REQ-05 (precedence statement) is SHOULD, not MUST (pending CT-001 elevation ruling). Deferred for now.
- WRITE_SCOPE canonicalization: HELP_HUMAN → `none`, CHANGE → `tool-root-only`, RECONCILIATION → `tool-root-only`, REVIEW → `project-level` (compound scope documented in parenthetical).

## Domain Context

### Baseline Conformance (2026-02-22 audit)

| REQ | Description | Pre-fix | Post-fix |
|-----|-------------|---------|----------|
| REQ-01 | `[[DOC:AGENT_INSTRUCTIONS]]` header | 26/26 | 26/26 |
| REQ-02 | `AGENT_TYPE:` line | 26/26 | 26/26 |
| REQ-03 | Agent Type table (6 properties) | 26/26 | 26/26 |
| REQ-04 | 4 section marker pairs | 24/26 | 26/26 |
| REQ-05 | Precedence statement (SHOULD) | 0/26 | 0/26 (deferred) |
| REQ-06 | YAML frontmatter `description:` | 24/26 | 26/26 |
| REQ-07 | Canonical WRITE_SCOPE | 22/26 | 26/26 |
| REQ-08 | `AGENT_*` filename prefix | 26/26 | 26/26 |
| REQ-09 | CLASS consistent with AGENTS.md | Not audited | PASS (26/26; mismatch fixed in `AGENT_HELP_HUMAN.md`) |
| REQ-10 | Subagent delegation rules | Not audited | PASS (subagent-capable files audited + fail-closed governance language added) |

### Files fixed (session 1)

- **AGENT_TASK.md** (REQ-04): Added `[[BEGIN:SPEC]]`/`[[END:SPEC]]`, `[[BEGIN:STRUCTURE]]`/`[[END:STRUCTURE]]`, `[[BEGIN:RATIONALE]]`/`[[END:RATIONALE]]` markers
- **AGENT_CHIRALITY_FRAMEWORK.md** (REQ-04): Added missing `[[END:STRUCTURE]]` and `[[BEGIN:RATIONALE]]` markers between STRUCTURE and RATIONALE sections
- **AGENT_ORCHESTRATOR.md** (REQ-06): Added `description:` to YAML frontmatter
- **AGENT_RECONCILIATION.md** (REQ-06 + REQ-07): Added `description:` to frontmatter; canonicalized WRITE_SCOPE to `tool-root-only`
- **AGENT_HELP_HUMAN.md** (REQ-07): Canonicalized WRITE_SCOPE to `none`
- **AGENT_CHANGE.md** (REQ-07): Canonicalized WRITE_SCOPE to `tool-root-only`
- **AGENT_REVIEW.md** (REQ-07): Canonicalized WRITE_SCOPE to `project-level`

### Files fixed (session 2)

- **AGENT_HELP_HUMAN.md** (REQ-09): Normalized `AGENT_CLASS` to canonical `PERSONA` to match `AGENTS.md`.
- **AGENT_ORCHESTRATOR.md** (REQ-10): Added explicit subagent governance contract (Type-2 registry check + fail-closed metadata rule using `subagentGovernance.contextSealed`, `subagentGovernance.pipelineRunApproved`, `subagentGovernance.approvalRef`) and dispatch-time validation step.
- **AGENT_RECONCILIATION.md** (REQ-10): Added explicit subagent governance contract (Type-2 registry check + fail-closed metadata rule using `subagentGovernance.contextSealed`, `subagentGovernance.pipelineRunApproved`, `subagentGovernance.approvalRef`) and dispatch-time validation step.

### REQ-09 / REQ-10 Audit Evidence (session 2)

- AGENT_CLASS cross-check against `AGENTS.md` now returns no mismatches across `agents/AGENT_*.md`.
- Subagent-capable files identified by YAML `subagents` field:
  - `AGENT_ORCHESTRATOR.md` → `PREPARATION`, `4_DOCUMENTS`, `DEPENDENCIES`, `CHIRALITY_FRAMEWORK`, `CHIRALITY_LENS`
  - `AGENT_RECONCILIATION.md` → `AUDIT_DEP_CLOSURE`, `AUDIT_AGENTS`, `AUDIT_DECOMP`
- All delegated subagents declare `AGENT_TYPE: 2` and `AGENT_CLASS: TASK`.

## Open Items

- **REQ-05**: Precedence statement `PROTOCOL > SPEC > STRUCTURE > RATIONALE` not yet added to any file. Pending CT-001 human ruling on SHOULD → MUST elevation. When approved, add to all 26 files.
- **CONFLICT**: Canonical WRITE_SCOPE value set discrepancy — DEL-06-01 Specification lists 6 values (`repo-wide`, `deliverable-local`, `tool-root-only`, `workspace-scaffold-only`, `repo-metadata-only`, `none`) but HELPS_HUMANS canonical standard lists 6 values with `project-level` instead of `workspace-scaffold-only`. Both values are used in practice (7 total). Needs human ruling on canonical set.

## Proposal History

- All 7 structural fixes applied this session (see "Files fixed" above).
- Session 2 completed REQ-09 and REQ-10 remediation in subagent-capable manager files.

## Interface & Dependency Notes

- AGENTS.md Full Agent Type Table may need update if any WRITE_SCOPE or AGENT_CLASS values were corrected. Current changes are consistent with existing AGENTS.md entries.
