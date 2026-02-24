# Procedure — DEL-03-04 Subagent Governance Fail-Closed Enforcement

## Purpose

This procedure describes how to produce and verify the subagent governance fail-closed enforcement for the Chirality harness runtime. It covers implementation, testing, and documentation of the governance gate logic.

## Current Execution Snapshot (2026-02-24 PASS1)

- Implemented artifacts:
  - `frontend/src/lib/harness/subagent-governance.ts`
  - `frontend/src/lib/harness/agent-instruction.ts`
  - `frontend/src/app/api/harness/turn/route.ts`
- Verification artifacts:
  - `frontend/src/__tests__/lib/harness-subagent-governance.test.ts`
  - `frontend/src/__tests__/api/harness/routes.test.ts`
  - `frontend/src/__tests__/lib/harness-options.test.ts`
- PASS evidence:
  - `execution/_Coordination/TIER8_CONTROL_LOOP_2026-02-24_PASS1.md`
  - `execution/_Reconciliation/TIER8_INTERFACE_RECON_2026-02-24_PASS1.md`

## Prerequisites

| Prerequisite | Description | Source |
|-------------|-------------|--------|
| SPEC Section 9.7 accessible | Normative specification for delegation governance rule | `docs/SPEC.md` |
| CONTRACT.md accessible | Binding invariants K-SEAL-1, K-AUTH-1, K-AUTH-2, K-GATE-1 | `docs/CONTRACT.md` |
| Harness runtime codebase available | Existing session/turn API implementation (DEL-03-01, DEL-03-02) | **ASSUMPTION:** DEL-03-01 and DEL-03-02 provide the runtime scaffolding in which the governance gate operates |
| Turn options mapping functional | `opts.subagentGovernance` is accessible from the turn execution path (DEL-03-03) | **ASSUMPTION:** DEL-03-03 provides the opts parsing that makes governance metadata available |
| Persona instruction files parseable | Ability to read YAML frontmatter from persona instruction files | **ASSUMPTION:** The runtime already parses persona instruction frontmatter for `subagents`, `tools`, `model`, `max_turns`, etc. (SPEC Section 9.7) |
| Body header parsing rules confirmed | The format for "body header" (where `AGENT_TYPE: 2` is declared) must be understood before implementing REQ-07 | **ASSUMPTION:** "Body header" is a structured metadata block parseable as key-value pairs. Confirm from TYPES.md Section 4 (**location TBD**) before implementation. See Guidance Considerations — Body Header Format Clarification. |
| Test infrastructure available | Unit and integration test runner for the harness runtime | TBD (DEL-07-01 provides infrastructure) |

## Steps

### Step 1: Understand the Gate Logic

1. Read SPEC Section 9.7 in its entirety.
2. Confirm the gate conditions listed in the Specification (REQ-01 through REQ-14).
3. Identify the runtime code location where subagent injection currently occurs or would occur.
   - **ASSUMPTION:** The injection point is in the turn execution path, after opts parsing and before subagent context is prepared.
4. Confirm that the identified injection point is the **sole code path** for subagent injection (Specification REQ-13). If alternative paths exist, they must either be removed or routed through the governance gate.

### Step 2: Implement the Governance Gate Function

1. Create a governance gate function (or module) with the following evaluation order:
   - **Gate 1 -- Environment:** Check `CHIRALITY_ENABLE_SUBAGENTS === "true"`. If not, return deny.
   - **Gate 2 -- Persona allowlist:** Check that the active persona declares a non-empty `subagents` field in YAML frontmatter. If not, return deny. **Note:** An empty array (`subagents: []`) must be treated as "not allowlisted" (see Specification REQ-02 verification).
   - **Gate 3 -- Metadata presence:** Check that `opts.subagentGovernance` is a non-null object. If not, return deny.
   - **Gate 4 -- contextSealed:** Check `opts.subagentGovernance.contextSealed === true`. If not, return deny.
   - **Gate 5 -- pipelineRunApproved:** Check `opts.subagentGovernance.pipelineRunApproved === true`. If not, return deny.
   - **Gate 6 -- approvalRef:** Check that `opts.subagentGovernance.approvalRef` is a non-empty string (typeof === 'string' && length > 0). If not, return deny.
2. If all gates pass, return allow.
3. The function MUST return a structured result (Specification REQ-12) indicating:
   - Allow/deny decision.
   - Which gate denied (for logging/debugging), or all-clear.
   - TBD: the specific return schema (e.g., `{ allowed: boolean, deniedBy?: string, reason?: string }`) is not prescribed by SPEC.
4. Log the gate evaluation result (Specification REQ-11): allow or deny with reason at an appropriate log level. Log the `approvedBy` field when present for audit context.

**Note on evaluation order:** This procedure prescribes a specific evaluation order (environment first, then persona, then metadata fields) for clarity and short-circuit efficiency. However, the Specification does not normatively mandate this order -- see Conflict Table entry CT-003 in Guidance. The implementer should confirm whether ordering is normatively required.

### Step 2a: Handle Gate Function Runtime Errors

1. If the governance gate function itself throws a runtime exception during evaluation (e.g., unexpected null dereference, malformed opts structure, file read error for persona frontmatter):
   - The system MUST fail closed: treat the exception as a denial.
   - Log the error at error level, including the exception details.
   - Return deny with a reason indicating an internal gate evaluation error.
   - Do NOT propagate the exception to the turn execution path in a way that would abort the parent turn.
2. This ensures the fail-closed invariant holds even when the gate code encounters unexpected conditions.

**Source:** SPEC Section 9.7 (fail-closed posture); Guidance Principles -- Deny by Default. **ASSUMPTION:** This error-handling behavior is inferred from the fail-closed design intent, not explicitly stated in SPEC.

### Step 3: Implement Subagent Registry Validation

1. Before injecting each candidate subagent, parse its instruction file.
2. Verify `AGENT_TYPE: 2` is declared in the instruction body header.
   - **Note:** Confirm the parsing rules for "body header" format before implementation. See Guidance Considerations -- Body Header Format Clarification. The term refers to a structured metadata block, but the exact format (YAML frontmatter, markdown heading, specific line pattern) requires confirmation from TYPES.md Section 4 (**location TBD**).
   - If not declared as Type 2: skip this subagent (do not inject). Log at error level.
3. Check for `AGENT_CLASS: TASK` in the Agent Type table.
   - If not TASK: log a warning but proceed with injection.

### Step 4: Integrate Gate into Turn Execution Path

1. Locate the turn execution code path where subagent injection would occur.
2. Confirm this is the **sole injection path** (Specification REQ-13). If other paths exist, refactor to route through the governance gate or remove.
3. Insert the governance gate check before any subagent injection logic.
4. If the gate returns deny:
   - Do not inject subagents.
   - Allow the parent turn to continue execution normally.
   - Do not emit an error response to the client.
5. If the gate returns allow:
   - Proceed with subagent injection using the validated subagent registry.
6. Verify that the `approvedBy` field (when present) is logged for audit purposes.

### Step 5: Write Unit Tests

Write unit tests covering each gate condition. Minimum test cases:

| Test Case | Input | Expected Result |
|-----------|-------|-----------------|
| Env absent | No `CHIRALITY_ENABLE_SUBAGENTS` | Deny |
| Env false | `CHIRALITY_ENABLE_SUBAGENTS = "false"` | Deny |
| Env true | `CHIRALITY_ENABLE_SUBAGENTS = "true"` | Passes gate 1 |
| Persona no subagents | No `subagents` frontmatter | Deny |
| Persona empty subagents | `subagents: []` | Deny |
| Persona with subagents | `subagents: [PREPARATION]` | Passes gate 2 |
| No governance metadata | `opts` without `subagentGovernance` | Deny |
| Null governance metadata | `opts.subagentGovernance: null` | Deny |
| contextSealed false | `contextSealed: false` | Deny |
| contextSealed string | `contextSealed: "true"` | Deny |
| contextSealed true | `contextSealed: true` | Passes gate 4 |
| pipelineRunApproved false | `pipelineRunApproved: false` | Deny |
| pipelineRunApproved string | `pipelineRunApproved: "true"` | Deny |
| pipelineRunApproved number | `pipelineRunApproved: 1` | Deny |
| pipelineRunApproved true | `pipelineRunApproved: true` | Passes gate 5 |
| approvalRef empty | `approvalRef: ""` | Deny |
| approvalRef missing | No `approvalRef` | Deny |
| approvalRef number | `approvalRef: 123` | Deny |
| approvalRef valid | `approvalRef: "GATE-001"` | Passes gate 6 |
| All gates pass | All conditions valid | Allow |
| Subagent not Type 2 | Candidate declares `AGENT_TYPE: 1` | Not injected |
| Subagent Type 2 non-TASK | `AGENT_TYPE: 2`, `AGENT_CLASS: PERSONA` | Injected + warning logged |
| Gate function runtime error | Gate function throws during evaluation | Deny (fail-closed) + error logged |
| Gate result structure (allow) | All conditions valid | Return value contains `allowed: true` |
| Gate result structure (deny) | Missing env variable | Return value contains `allowed: false` + gate identification |
| Gate logging (allow) | All conditions valid | Log entry present with ALLOW decision |
| Gate logging (deny) | Missing metadata | Log entry present with DENY decision + gate ID |

### Step 6: Write Integration Tests

1. **Full-pass test:** Boot a session, submit a turn with valid governance metadata to a persona with declared subagents, and verify subagent injection occurs.
2. **Denial-continuation test:** Submit a turn with invalid/missing governance metadata. Verify:
   - No subagent injection occurs.
   - The parent turn completes normally (200 response, streamed events). **Rationale:** The 200 status code confirms the turn executed successfully; streamed events confirm the parent continued normally. A denied turn should be indistinguishable from a normal turn (from the client's perspective) except that no subagent outputs appear in the event stream. This is the observable consequence of REQ-09. See Guidance Considerations -- Denial Response Format Rationale.
   - No error is returned to the client.
3. **UI-override test:** Supply governance metadata via opts with an invalid runtime state (e.g., environment variable not set). Verify injection is blocked despite UI-supplied metadata.
4. **Sole enforcement point test:** Verify via code review and/or static analysis that no alternative code path exists that can inject subagents without traversing the governance gate (Specification REQ-13).

### Step 7: Write Documentation

1. Document the governance gate logic, configuration requirements, and failure behaviors.
2. Include:
   - How to enable subagent delegation (`CHIRALITY_ENABLE_SUBAGENTS`).
   - How to allowlist a persona for subagents (YAML frontmatter `subagents` field).
   - How to supply governance metadata (`opts.subagentGovernance`).
   - Failure behavior at each gate.
   - Logging and audit trail description, including what is logged on allow/deny and the log record fields.
3. Cross-reference SPEC Section 9.7 and relevant CONTRACT invariants (K-SEAL-1, K-AUTH-1, K-AUTH-2, K-GATE-1).

### Step 8: Verify Against Specification Requirements

1. Walk through each requirement (REQ-01 through REQ-14) in the Specification.
2. Confirm each has:
   - Implementing code (where applicable; REQ-14 is TBD).
   - At least one test case.
   - Documentation coverage.
3. Record any gaps as open items.

## Verification

| Check | Method | Pass Criteria |
|-------|--------|--------------|
| All gate conditions implemented | Code review | Each gate from SPEC 9.7 has a corresponding code path |
| Fail-closed behavior confirmed | Unit tests pass | Denial at each gate; parent turn continues |
| Strict type checking | Unit tests pass | String/number/truthy values correctly rejected |
| Subagent Type 2 enforcement | Unit tests pass | Non-Type-2 candidates are not injected |
| Parent turn continuation | Integration test | Turn completes normally on denial |
| No UI override | Integration test | UI-supplied metadata does not bypass runtime gates |
| Gate result structure | Unit tests pass | Return value matches structured result contract (REQ-12) |
| Gate logging | Unit tests pass | Allow/deny decisions are logged with gate identification (REQ-11) |
| Sole enforcement point | Code review + static analysis | No alternative injection path exists (REQ-13) |
| Gate runtime error handling | Unit tests pass | Gate function exceptions produce denial + error log (Step 2a) |
| Documentation complete | Review | Gate logic, configuration, failure behaviors, and audit logging documented |

## Records

| Record | Type | Description |
|--------|------|-------------|
| Governance gate source code | CODE | Implementation of the gate function, registry validator, and error handling |
| Unit test results | TEST | Test execution results for all gate conditions including type-coercion, error handling, result structure, and logging |
| Integration test results | TEST | End-to-end test results for pass/deny scenarios and sole enforcement point verification |
| Developer documentation | DOC | Gate logic, configuration, failure behavior reference, and audit logging description |
| Code review record | DOC | Review confirming alignment with SPEC Section 9.7 and CONTRACT invariants |
