# Working Memory — DEL-06-01

*This file is shared working memory for WORKING_ITEMS and TASK agents operating on this deliverable.*

## Key Decisions & Human Rulings

- REQ-05 remains SHOULD (SPEC modality unchanged), but explicit precedence declarations are now present across all 26 `agents/AGENT_*.md` files.
- WRITE_SCOPE canonicalization: HELP_HUMAN → `none`, CHANGE → `tool-root-only`, RECONCILIATION → `tool-root-only`, REVIEW → `project-level` (compound scope documented in parenthetical).
- Canonical WRITE_SCOPE enum set is now aligned across governance sources to 7 values: `repo-wide`, `project-level`, `deliverable-local`, `tool-root-only`, `workspace-scaffold-only`, `repo-metadata-only`, `none`.

## Domain Context

### Baseline Conformance (2026-02-22 audit)

| REQ | Description | Pre-fix | Post-fix |
|-----|-------------|---------|----------|
| REQ-01 | `[[DOC:AGENT_INSTRUCTIONS]]` header | 26/26 | 26/26 |
| REQ-02 | `AGENT_TYPE:` line | 26/26 | 26/26 |
| REQ-03 | Agent Type table (6 properties) | 26/26 | 26/26 |
| REQ-04 | 4 section marker pairs | 24/26 | 26/26 |
| REQ-05 | Precedence statement (SHOULD) | 0/26 | 26/26 |
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

### Files fixed (session 3)

- **AGENT_HELPS_HUMANS.md** (REQ-05 + REQ-07 alignment): Added explicit `## Precedence` section and expanded WRITE_SCOPE enumerations to include both `project-level` and `workspace-scaffold-only`.
- **AGENT_TASK.md** (REQ-05): Added explicit `## Precedence` section.
- **AGENTS.md** (classification metadata alignment): Expanded `WRITE_SCOPE` property list to include `workspace-scaffold-only`.
- **docs/SPEC.md** (canonical enum alignment): Updated Section 9.5 WRITE_SCOPE valid-values list to include `project-level`.
- **docs/TYPES.md** (canonical enum alignment): Updated Section 4.2 WRITE_SCOPE value list to include `project-level`.
- **DEL-06-01 Specification.md** (local enforceability alignment): Updated REQ-03/REQ-07 WRITE_SCOPE enumeration and definitions to the same 7-value canonical set.

### REQ-09 / REQ-10 Audit Evidence (session 2)

- AGENT_CLASS cross-check against `AGENTS.md` now returns no mismatches across `agents/AGENT_*.md`.
- Subagent-capable files identified by YAML `subagents` field:
  - `AGENT_ORCHESTRATOR.md` → `PREPARATION`, `4_DOCUMENTS`, `DEPENDENCIES`, `CHIRALITY_FRAMEWORK`, `CHIRALITY_LENS`
  - `AGENT_RECONCILIATION.md` → `AUDIT_DEP_CLOSURE`, `AUDIT_AGENTS`, `AUDIT_DECOMP`
- All delegated subagents declare `AGENT_TYPE: 2` and `AGENT_CLASS: TASK`.

### REQ-05 / REQ-07 Audit Evidence (session 3)

- Precedence check (`for f in agents/AGENT_*.md; do rg \"^## Precedence\" ...`) now returns no missing files: 26/26 include a precedence section with PROTOCOL/SPEC/STRUCTURE/RATIONALE ordering.
- WRITE_SCOPE token validation across all 26 agent files passes against canonical enum set `{repo-wide, project-level, deliverable-local, tool-root-only, workspace-scaffold-only, repo-metadata-only, none}`.
- Canonical-set cross-document alignment is now consistent across:
  - `AGENTS.md`
  - `docs/SPEC.md` Section 9.5
  - `docs/TYPES.md` Section 4.2
  - `agents/AGENT_HELPS_HUMANS.md`
  - `execution/.../DEL-06-01.../Specification.md`

## Open Items

- No blocking DEL-06-01 structural conformance items remain in active scope.
- Optional governance follow-up: CT-001 modality harmonization decision (whether REQ-05/REQ-06 SHOULD should remain advisory or be elevated) can be handled as a separate policy pass.

## Proposal History

- All 7 structural fixes applied this session (see "Files fixed" above).
- Session 2 completed REQ-09 and REQ-10 remediation in subagent-capable manager files.
- Session 3 closed REQ-05 implementation and WRITE_SCOPE canonical-set conflict by aligning agent/gov docs to a unified 7-value enum set.

## Interface & Dependency Notes

- AGENTS.md Full Agent Type Table may need update if any WRITE_SCOPE or AGENT_CLASS values were corrected. Current changes are consistent with existing AGENTS.md entries.
