# Datasheet — DEL-03-04 Subagent Governance Fail-Closed Enforcement

## Identification

| Field | Value |
|-------|-------|
| **Deliverable ID** | DEL-03-04 |
| **Name** | Subagent Governance Fail-Closed Enforcement |
| **Package** | PKG-03 — Harness Runtime Core |
| **Type** | SECURITY_CONTROL |
| **Context Envelope** | S |
| **Responsible Party** | WORKING_ITEMS / Runtime implementation team |
| **Scope Coverage** | SOW-012 |
| **Supports Objectives** | OBJ-002 |
| **Anticipated Artifacts** | CODE / TEST / DOC |
| **Decomposition** | `execution/_Decomposition/ChiralityApp_SoftwareDecomposition_2026-02-21_G7-APPROVED.md` |

## Issuance Hygiene (2026-02-24)

- Lifecycle state is `ISSUED`.
- REQ-14 performance-bound definition remains a spec-level follow-up and is non-blocking for issued status.
- Legacy implementation-phase `TBD`/assumption wording is non-blocking unless explicitly marked as an issuance blocker by human ruling.

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
| Body header format | Implemented parser supports `AGENT_TYPE: <n>` body-header lines and Agent Type table rows (`| **AGENT_TYPE** | TYPE n |`) for compatibility with current instruction corpus. | `frontend/src/lib/harness/agent-instruction.ts` (`parseAgentType`) |
| Gate result format | Implemented structured result: `allowed`, `gate`, `reason`, `allowlistedSubagents[]`, `delegatedSubagents[]`, optional `approvalRef`, optional `approvedBy`. | `frontend/src/lib/harness/subagent-governance.ts` (`SubagentGovernanceDecision`) |
| Audit log record schema | Implemented runtime log lines include gate disposition (`ALLOW`/`DENY`), persona, gate identifier, reason (deny), delegated set (allow), and approval metadata when present. | `frontend/src/lib/harness/subagent-governance.ts` (`logDecision`) |

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
| Governance gate function | Runtime function that evaluates all conditions above and returns allow/deny | IMPLEMENTED (`frontend/src/lib/harness/subagent-governance.ts`) |
| Subagent registry validator | Validates that candidate subagents declare `AGENT_TYPE: 2` | IMPLEMENTED (`resolveDelegatedSubagents`) |
| Parent turn continuation logic | Ensures denied injection does not abort or error the parent turn | IMPLEMENTED (`frontend/src/app/api/harness/turn/route.ts`) |
| Gate result logging | Logs gate evaluation result including which gate denied and relevant metadata fields | IMPLEMENTED (`logDecision`) |
| Unit test suite | Tests for each gate condition: pass and fail paths | IMPLEMENTED (`frontend/src/__tests__/lib/harness-subagent-governance.test.ts`) |
| Integration test suite | End-to-end test: persona with subagents, valid/invalid governance metadata | IMPLEMENTED (`frontend/src/__tests__/api/harness/routes.test.ts`) |

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
