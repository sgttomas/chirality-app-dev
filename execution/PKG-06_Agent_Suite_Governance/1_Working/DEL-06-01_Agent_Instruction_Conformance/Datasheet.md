# Datasheet -- DEL-06-01 Agent Instruction Suite Structural Conformance

## Identification

| Field | Value |
|-------|-------|
| **Deliverable ID** | DEL-06-01 |
| **Name** | Agent Instruction Suite Structural Conformance |
| **Package** | PKG-06 Agent Suite & Governance |
| **Type** | DOC_UPDATE |
| **Context Envelope** | L |
| **Responsible Party** | TBD -- **requires assignment: this deliverable needs an assigned authority for governance accountability** (Lensing item A-001; Source: Datasheet.md Identification) |
| **Scope Coverage** | SOW-031 |
| **Objective Support** | OBJ-006 -- **ASSUMPTION (best-effort mapping via PKG-06 package grouping)**. Rationale: The Scope Ledger row for SOW-031 maps to PKG-06/DEL-06-01 with OBJ-006. OBJ-006 ("Validation posture and governance/agent-suite conformance enable repeatable operation") explicitly includes "agents/* instruction suite conforms to HELPS_HUMANS structure," which is this deliverable's subject. The association is directionally strong but is recorded as ASSUMPTION because the objective-to-deliverable mapping in the decomposition is best-effort. (Source: Decomposition, Scope Ledger SOW-031 row; OBJ-006 acceptance criteria) |
| **Decomposition Ref** | `execution/_Decomposition/ChiralityApp_SoftwareDecomposition_2026-02-21_G7-APPROVED.md` |

## Attributes

| Attribute | Value | Source |
|-----------|-------|--------|
| **Conformance Target Standard** | `AGENT_HELPS_HUMANS.md` (v1.1, 2026-01-30) | AGENTS.md Section 0; SPEC.md Section 9 |
| **Agent Instruction File Count** | 26 `AGENT_*.md` files in `agents/` | Filesystem scan (2026-02-21) |
| **Template File Count** | 2 files (`MEMORY_TEMPLATE.md`, `TASK_ESTIMATING_TEMPLATE.md`) | Filesystem scan (2026-02-21) |
| **Agent Framework Index** | `AGENTS.md` (repo root) | Filesystem scan |
| **Conformance Specification** | `docs/SPEC.md` Section 9 (Agent Instruction File Structure) | SPEC.md |
| **Contract Invariant** | K-WRITE-1 (explicit write scope per agent) | CONTRACT.md Section 1.10 |
| **Baseline Conformance Level** | TBD -- **requires measurement: count of files currently conformant vs. non-conformant has not been established.** Guidance C4 references PLAN.md's "92% to 95%+" estimate but this is a qualitative projection, not a measured baseline. A pre-edit audit (Procedure Step 2) should produce this metric. (Lensing item B-002; Source: Datasheet.md Attributes, Guidance C4, PLAN.md Section 1) |

### Agent Instruction Files in Scope

| File | Agent Role | Expected AGENT_TYPE |
|------|-----------|---------------------|
| `AGENT_4_DOCUMENTS.md` | 4_DOCUMENTS | TYPE 2 |
| `AGENT_AGGREGATION.md` | AGGREGATION | TYPE 2 |
| `AGENT_AUDIT_AGENTS.md` | AUDIT_AGENTS | TYPE 2 |
| `AGENT_AUDIT_DECOMP.md` | AUDIT_DECOMP | TYPE 2 |
| `AGENT_AUDIT_DEP_CLOSURE.md` | AUDIT_DEP_CLOSURE | TYPE 2 |
| `AGENT_CHANGE.md` | CHANGE | TYPE 1 |
| `AGENT_CHIRALITY_FRAMEWORK.md` | CHIRALITY_FRAMEWORK | TYPE 2 |
| `AGENT_CHIRALITY_LENS.md` | CHIRALITY_LENS | TYPE 2 |
| `AGENT_CONTEXT_TRANSPOSE.md` | CONTEXT_TRANSPOSE | TYPE 1 |
| `AGENT_DECOMP_BASE.md` | DECOMP_BASE | TYPE 0 |
| `AGENT_DEPENDENCIES.md` | DEPENDENCIES | TYPE 2 |
| `AGENT_DOMAIN_DECOMP.md` | DOMAIN_DECOMP | TYPE 1 |
| `AGENT_ESTIMATE_PREP.md` | ESTIMATE_PREP | TYPE 2 |
| `AGENT_ESTIMATING.md` | ESTIMATING | TYPE 2 |
| `AGENT_HELPS_HUMANS.md` | HELPS_HUMANS | TYPE 0 |
| `AGENT_HELP_HUMAN.md` | HELP_HUMAN | TYPE 1 |
| `AGENT_ORCHESTRATOR.md` | ORCHESTRATOR | TYPE 1 |
| `AGENT_PREPARATION.md` | PREPARATION | TYPE 2 |
| `AGENT_PROJECT_DECOMP.md` | PROJECT_DECOMP | TYPE 1 |
| `AGENT_RECONCILIATION.md` | RECONCILIATION | TYPE 1 |
| `AGENT_REVIEW.md` | REVIEW | TYPE 1 |
| `AGENT_SCHEDULING.md` | SCHEDULING | TYPE 1 |
| `AGENT_SCOPE_CHANGE.md` | SCOPE_CHANGE | TYPE 1 |
| `AGENT_SOFTWARE_DECOMP.md` | SOFTWARE_DECOMP | TYPE 1 |
| `AGENT_TASK.md` | TASK | TYPE 2 |
| `AGENT_WORKING_ITEMS.md` | WORKING_ITEMS | TYPE 1 |

**Note:** Expected AGENT_TYPE values above are **ASSUMPTION** based on the agent classification in AGENTS.md. Actual values must be confirmed by inspecting each file. (Lensing item B-001: this essential fact remains unverified; confirmation requires cross-referencing AGENTS.md Full Agent Type Table with the `AGENT_TYPE` line in each file's body.) (Source: AGENTS.md Section 2)

## Conditions

| Condition | Description |
|-----------|-------------|
| **Governing Standard** | `AGENT_HELPS_HUMANS.md` is the canonical conformance target. Where any other `AGENT_*.md` file disagrees, the other file must be edited to conform. (Source: AGENTS.md Section 0) |
| **SPEC Section 9 Requirements** | All agent instruction files MUST follow the structure defined by `AGENT_HELPS_HUMANS.md`, including: required header, Agent Type table, four required section markers, precedence order, and YAML frontmatter for harness runtime metadata. (Source: SPEC.md Section 9) |
| **Invariant K-WRITE-1** | Every agent has an explicit write scope declared in its header block. No agent writes outside its declared zone. (Source: CONTRACT.md Section 1.10) |
| **Context Envelope** | L -- likely touches many instruction files; single domain (docs). (Source: Decomposition, DEL-06-01 entry) |

## Construction

| Element | Description |
|---------|-------------|
| **Work Domain** | Agent instruction files (`agents/` directory); documentation conformance |
| **Output Format** | Updated Markdown files (`AGENT_*.md`) |
| **Conformance Checklist Basis** | SPEC.md Section 9.1 (Required Header), 9.2 (Required Agent Type Table), 9.3 (Required Sections), 9.4 (Precedence Order), 9.7 (Runtime Metadata Contract) |
| **Audit Tool** | `AGENT_AUDIT_AGENTS.md` provides the conformance rubric (Source: AGENTS.md Section 0) |
| **Estimated File Count** | Up to 26 instruction files may require updates |

## References

| Reference | Location | Relevance |
|-----------|----------|-----------|
| Software Decomposition (G7-APPROVED) | `execution/_Decomposition/ChiralityApp_SoftwareDecomposition_2026-02-21_G7-APPROVED.md` | DEL-06-01 definition and scope |
| AGENT_HELPS_HUMANS.md | `agents/AGENT_HELPS_HUMANS.md` | Conformance target standard |
| SPEC.md Section 9 | `docs/SPEC.md` | Agent Instruction File Structure specification |
| CONTRACT.md | `docs/CONTRACT.md` | Invariant K-WRITE-1 (write scope enforcement) |
| AGENTS.md | `AGENTS.md` | Agent framework index and classification reference |
| DIRECTIVE.md | `docs/DIRECTIVE.md` | Founding intent and structural constraints |
| TYPES.md | `docs/TYPES.md` | Agent roles vocabulary (Section 4) |
| PLAN.md | `docs/PLAN.md` | Agent instruction hardening status (Section 1) |
