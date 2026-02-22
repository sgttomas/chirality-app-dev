# Datasheet — DEL-03-04 Subagent Governance Fail-Closed Enforcement

## Identification

| Field | Value |
|-------|-------|
| **Deliverable ID** | DEL-03-04 |
| **Name** | Subagent Governance Fail-Closed Enforcement |
| **Package** | PKG-03 — Harness Runtime Core |
| **Type** | SECURITY_CONTROL |
| **Context Envelope** | S |
| **Responsible Party** | TBD |
| **Scope Coverage** | SOW-012 |
| **Supports Objectives** | OBJ-002 |
| **Anticipated Artifacts** | CODE / TEST / DOC |
| **Decomposition** | `execution/_Decomposition/ChiralityApp_SoftwareDecomposition_2026-02-21_G7-APPROVED.md` |

## Attributes

| Attribute | Value | Source |
|-----------|-------|--------|
| Security posture | Fail-closed (deny by default) | SPEC Section 9.7 |
| Environment gate variable | `CHIRALITY_ENABLE_SUBAGENTS` (must === `"true"`) | SPEC Section 9.7 |
| Persona gate | Type 1 persona must be allowlisted for subagents | SPEC Section 9.7 |
| Governance metadata object | `opts.subagentGovernance` | SPEC Section 9.7 |
| Required field: `contextSealed` | `true` (boolean) | SPEC Section 9.7 |
| Required field: `pipelineRunApproved` | `true` (boolean) | SPEC Section 9.7 |
| Required field: `approvalRef` | Non-empty string | SPEC Section 9.7 |
| Optional field: `approvedBy` | String (optional) | SPEC Section 9.7 |
| Failure behavior | Block subagent injection; allow parent turn to continue normally | SPEC Section 9.7 |
| Subagent type constraint | Delegated subagents MUST declare `AGENT_TYPE: 2` in body header | SPEC Section 9.7 |
| Subagent class constraint | `AGENT_CLASS: TASK` preferred; validated as warning-level (non-blocking) | SPEC Section 9.7 |
| Body header format | TBD — the term "body header" is used across documents but its concrete format (YAML frontmatter, markdown heading, or specific line pattern) is not precisely defined in accessible sources. **ASSUMPTION:** Refers to the metadata block at the top of an instruction file, parsed similarly to YAML frontmatter. See TYPES.md Section 4 for agent type classification properties (**location TBD**). | SPEC Section 9.7; TYPES.md Section 4 (**location TBD**) |
| Gate result format | TBD — the gate function returns a structured result indicating allow/deny and which gate denied, but the specific return schema is not normatively defined. | Procedure.md Step 2.3; Specification.md REQ-12 |
| Audit log record schema | TBD — what fields are included in the governance gate log record (e.g., timestamp, gate evaluated, result, approvalRef, approvedBy) is not defined. | _SEMANTIC_LENSING.md A-004 |

## Conditions

| Condition | Gate Passes When | Gate Fails When |
|-----------|-----------------|-----------------|
| Environment enabled | `CHIRALITY_ENABLE_SUBAGENTS === "true"` | Variable absent, falsy, or !== `"true"` |
| Persona allowlisted | Persona instruction declares subagents in YAML frontmatter `subagents` field | Persona not in allowlist or no `subagents` declared |
| Governance metadata present | `opts.subagentGovernance` is a non-null object | Field is missing, null, or undefined |
| Context sealed | `subagentGovernance.contextSealed === true` | Not `true` |
| Pipeline run approved | `subagentGovernance.pipelineRunApproved === true` | Not `true` |
| Approval reference valid | `subagentGovernance.approvalRef` is a non-empty string | Empty string, missing, or non-string |

## Construction

| Component | Description | Status |
|-----------|-------------|--------|
| Governance gate function | Runtime function that evaluates all conditions above and returns allow/deny | TBD |
| Subagent registry validator | Validates that candidate subagents declare `AGENT_TYPE: 2` | TBD |
| Parent turn continuation logic | Ensures denied injection does not abort or error the parent turn | TBD |
| Gate result logging | Logs gate evaluation result including which gate denied and relevant metadata fields | TBD |
| Unit test suite | Tests for each gate condition: pass and fail paths | TBD |
| Integration test suite | End-to-end test: persona with subagents, valid/invalid governance metadata | TBD |

## References

| Reference | Relevance |
|-----------|-----------|
| `docs/SPEC.md` Section 9.7 | Delegation governance rule (fail closed) — primary normative source |
| `docs/SPEC.md` Section 9.8 | Harness turn input contract — `opts` and governance visibility |
| `docs/CONTRACT.md` K-SEAL-1 | No Type 2 execution before context is sealed and gate-approved |
| `docs/CONTRACT.md` K-GHOST-1 | Type 2 context limited to folder contents + declared references |
| `docs/CONTRACT.md` K-AUTH-1 | Only humans author binding approval records |
| `docs/CONTRACT.md` K-AUTH-2 | TBD — referenced in Specification REQ-06 but not consistently listed across documents. Confirm scope and definition from CONTRACT.md. |
| `docs/CONTRACT.md` K-GATE-1 | TBD — referenced in Specification REQ-05 rationale as "minimum gate requirement" but not defined in accessible documents. Confirm whether this is a valid CONTRACT invariant. |
| `docs/CONTRACT.md` K-WRITE-1 | Every agent has explicit write scope |
| `docs/DIRECTIVE.md` Section 2.3 | Human authority at every gate |
| `docs/DIRECTIVE.md` Section 2.5 | No hidden memory; referenced in Specification REQ-10 rationale for UI/runtime separation (**location TBD** — verify applicability) |
| `docs/TYPES.md` Section 4 | Agent types and classification properties |
| Decomposition DEL-03-04 entry | Deliverable definition, scope item SOW-012, objective OBJ-002 |
