# Specification — DEL-03-04 Subagent Governance Fail-Closed Enforcement

## Scope

### Included

- Runtime governance gate that evaluates subagent injection eligibility on every turn where delegation is attempted.
- Validation of the `opts.subagentGovernance` metadata object against the required schema.
- Enforcement of the fail-closed posture: injection is blocked unless all gate conditions are satisfied.
- Parent turn continuation when injection is denied (the parent turn proceeds normally without subagents).
- Subagent registry safety validation: delegated subagents must declare `AGENT_TYPE: 2`.
- Warning-level validation that delegated subagents declare `AGENT_CLASS: TASK`.
- Structured gate evaluation result reporting (allow/deny with gate identification).
- Gate evaluation logging for audit trail purposes.

### Excluded

- Session boot logic and turn execution APIs (covered by DEL-03-01, DEL-03-02).
- Turn options mapping and fallback chains (covered by DEL-03-03).
- Anthropic API provider integration (covered by DEL-03-05).
- Outbound network guardrails (covered by DEL-03-06).
- UI presentation of governance fields in the Operator Toolkit panel (covered by DEL-02-03; UI fields are informational only per SPEC Section 9.8).
- Harness validation test suite infrastructure (covered by DEL-07-01; this deliverable provides governance-specific tests).

## Implementation Snapshot (2026-02-24 PASS1)

- Runtime governance evaluator implemented in:
  - `frontend/src/lib/harness/subagent-governance.ts`
- Shared instruction parsing + AGENT_TYPE/AGENT_CLASS extraction implemented in:
  - `frontend/src/lib/harness/agent-instruction.ts`
- Turn-route enforcement integration implemented in:
  - `frontend/src/app/api/harness/turn/route.ts`
- Verification evidence:
  - `frontend/src/__tests__/lib/harness-subagent-governance.test.ts`
  - `frontend/src/__tests__/api/harness/routes.test.ts`
  - `frontend/src/__tests__/lib/harness-options.test.ts`

## Requirements

### REQ-01: Environment Gate

The runtime MUST check that the environment variable `CHIRALITY_ENABLE_SUBAGENTS` is strictly equal to the string `"true"` before proceeding with any subagent injection logic.

- **Source:** SPEC Section 9.7 -- "When `CHIRALITY_ENABLE_SUBAGENTS === "true"`"
- **Failure behavior:** If the variable is absent, empty, or any value other than `"true"`, subagent injection MUST NOT occur. The parent turn continues normally.

### REQ-02: Persona Allowlist Gate

The runtime MUST verify that the active Type 1 persona is allowlisted for subagent delegation before evaluating governance metadata.

- **Source:** SPEC Section 9.7 -- "a Type 1 persona is allowlisted for subagents"
- **Mechanism:** The persona's YAML frontmatter `subagents` field declares which subagents are available. Current implementation treats a non-empty `subagents` list (array or comma-delimited string) as allowlisted; the exact canonical shape is not explicitly prescribed by SPEC Section 9.7.
- **Failure behavior:** If the persona is not allowlisted, subagent injection MUST NOT occur. The parent turn continues normally.

### REQ-03: Governance Metadata Presence

The runtime MUST verify that `opts.subagentGovernance` is present and is a non-null object.

- **Source:** SPEC Section 9.7 -- "runtime injects subagents only if `opts.subagentGovernance` is present and valid"
- **Failure behavior:** Missing or null governance metadata MUST block injection. The parent turn continues normally.

### REQ-04: Context Sealed Validation

The runtime MUST verify that `opts.subagentGovernance.contextSealed === true`.

- **Source:** SPEC Section 9.7 -- "`contextSealed === true`"
- **Rationale:** Enforces K-SEAL-1 (no Type 2 agent execution before context is sealed and gate-approved by a human).
- **Failure behavior:** If `contextSealed` is not strictly `true`, subagent injection MUST NOT occur. The parent turn continues normally.

### REQ-05: Pipeline Run Approved Validation

The runtime MUST verify that `opts.subagentGovernance.pipelineRunApproved === true`.

- **Source:** SPEC Section 9.7 -- "`pipelineRunApproved === true`"
- **Rationale:** Enforces K-GATE-1 minimum gate requirement (pipeline run approval). **Note:** K-GATE-1 is referenced but its definition is not confirmed in accessible documents (see TBD in Datasheet References). Confirm from CONTRACT.md whether K-GATE-1 is a valid invariant and its exact scope.
- **Failure behavior:** If `pipelineRunApproved` is not strictly `true`, subagent injection MUST NOT occur. The parent turn continues normally.

### REQ-06: Approval Reference Validation

The runtime MUST verify that `opts.subagentGovernance.approvalRef` is a non-empty string.

- **Source:** SPEC Section 9.7 -- "`approvalRef` is a non-empty string"
- **Rationale:** Provides traceability to the human approval record (supports K-AUTH-1, K-AUTH-2). **Note:** K-AUTH-2 is referenced here but is not consistently listed in the Datasheet References or Specification Standards table. Harmonize references across documents. See Conflict Table entry CT-002.
- **Failure behavior:** If `approvalRef` is missing, empty, or not a string, subagent injection MUST NOT occur. The parent turn continues normally.

### REQ-07: Subagent Registry Type Validation

Before injecting a subagent, the runtime MUST verify that the candidate subagent instruction file declares `AGENT_TYPE: 2` in its body header.

- **Source:** SPEC Section 9.7 -- "Delegated subagents MUST declare `AGENT_TYPE: 2` in the body header."
- **Note:** The term "body header" requires clarification -- see Guidance Considerations section. **ASSUMPTION:** Refers to a structured metadata block at the top of the instruction file, parseable as YAML frontmatter or equivalent. See TYPES.md Section 4 (**location TBD**) for agent type classification properties.
- **Failure behavior:** If a candidate subagent does not declare `AGENT_TYPE: 2`, it MUST NOT be injected.

### REQ-08: Subagent Registry Class Warning

When a candidate subagent does not declare `AGENT_CLASS: TASK`, the runtime SHOULD emit a warning-level log entry but MUST NOT block injection solely on this basis.

- **Source:** SPEC Section 9.7 -- "`AGENT_CLASS: TASK` is preferred and validated as a warning-level rule (non-blocking)."

### REQ-09: Parent Turn Continuation on Denial

When subagent injection is denied for any reason, the parent turn MUST continue to execute normally without subagents. Denial MUST NOT cause a turn error, abort, or user-visible failure.

- **Source:** SPEC Section 9.7 -- "Missing/invalid governance metadata MUST block subagent injection while allowing the parent turn to continue normally."

### REQ-10: No UI Override of Runtime Gates

Supplying `opts.subagentGovernance` via the UI (Operator Toolkit panel or otherwise) MUST NOT bypass runtime gate logic. All runtime gates MUST still pass independently.

- **Source:** SPEC Section 9.8 -- "Supplying `opts.subagentGovernance` does not guarantee delegation; all runtime gates MUST still pass."
- **Rationale:** Enforces separation between UI convenience state and runtime enforcement (DIRECTIVE Section 2.5 clarification). **Note:** DIRECTIVE Section 2.5 is referenced here but other documents reference only DIRECTIVE Section 2.3. See Conflict Table entry CT-001 for normalization.

### REQ-11: Gate Evaluation Result Logging

The runtime MUST log the gate evaluation result (allow or deny with reason) for each governance gate evaluation. The log entry MUST include at minimum the gate decision (allow/deny) and, on denial, an identifier of which gate denied.

- **Source:** Procedure.md Step 2.4 (procedural guidance); SPEC Section 9.7 (implicit: fail-closed enforcement requires auditability).
- **Rationale:** Audit trail completeness requires a normative logging requirement, not just procedural guidance. Without this requirement, logging is optional and audit trail is not guaranteed.
- **Note:** The specific log record schema (fields, format, log level) is TBD. See Datasheet Attributes for the audit log record schema TBD.

### REQ-12: Gate Result Structured Return Format

The governance gate function MUST return a structured result that indicates: (a) the allow/deny decision, and (b) on denial, which gate condition was not satisfied.

- **Source:** Procedure.md Step 2.3 describes "a structured result indicating allow/deny and which gate denied"; SPEC Section 9.7 (implicit: fail-closed behavior requires deterministic, machine-readable gate results for downstream consumers).
- **Rationale:** Consumers of the gate result (logging, turn execution path, integration tests) require a defined output format to reliably interpret the gate decision. TBD -- the specific return schema (e.g., `{ allowed: boolean, deniedBy?: string, reason?: string }`) is not prescribed by SPEC.

### REQ-13: Sole Enforcement Point

The governance gate MUST be the sole enforcement point for subagent injection authorization. No alternative code path may bypass the gate to inject a subagent.

- **Source:** SPEC Section 9.7 (implicit: fail-closed posture requires a single, non-bypassable enforcement point); REQ-10 addresses UI bypass but this requirement addresses code-path bypass.
- **Rationale:** If alternative code paths can inject subagents without traversing the governance gate, the fail-closed posture is defeated. Verification must confirm there is exactly one injection path and it is gated.

### REQ-14: Performance Impact Bounds (TBD)

TBD -- The governance gate evaluation SHOULD NOT introduce latency that materially impacts turn execution time. Specific acceptance criteria (e.g., gate evaluation must not add more than N ms to turn latency) are TBD.

- **Source:** No explicit performance requirement in SPEC Section 9.7.
- **Rationale:** A security gate that introduces significant latency could create operational pressure to bypass or disable it, undermining the fail-closed posture.

## Standards

| Standard / Reference | Applicable Sections | Accessibility |
|---------------------|---------------------|--------------|
| `docs/SPEC.md` | Section 9.7 (Delegation governance rule), Section 9.8 (Turn input contract) | Accessible |
| `docs/CONTRACT.md` | K-SEAL-1, K-GHOST-1, K-AUTH-1, K-AUTH-2, K-GATE-1, K-WRITE-1 | Accessible (K-AUTH-2 and K-GATE-1 definitions TBD -- see Conflict Table) |
| `docs/DIRECTIVE.md` | Section 2.3 (Human authority), Section 2.5 (No hidden memory / UI-runtime separation) | Accessible (Section 2.5 applicability TBD -- see Conflict Table entry CT-001) |
| `docs/TYPES.md` | Section 4 (Agent roles and classification) | Accessible |

## Verification

| Requirement | Verification Approach | Expected Evidence |
|-------------|----------------------|-------------------|
| REQ-01 | Unit test: env variable absent, empty, `"false"`, `"true"` | Test passes; injection only when `"true"` |
| REQ-02 | Unit test: persona with/without `subagents` frontmatter; **include edge case: `subagents: []` (empty array)** | Test passes; injection only when allowlisted with non-empty array |
| REQ-03 | Unit test: `opts` without `subagentGovernance`, with null, with valid object | Test passes; injection only with valid object |
| REQ-04 | Unit test: `contextSealed` = `true`, `false`, missing, string `"true"` | Test passes; only boolean `true` allows injection |
| REQ-05 | Unit test: `pipelineRunApproved` = `true`, `false`, missing, **string `"true"`, number `1`** | Test passes; only boolean `true` allows injection; type-coercion cases explicitly rejected |
| REQ-06 | Unit test: `approvalRef` = valid string, empty string, missing, non-string | Test passes; only non-empty string allows injection |
| REQ-07 | Unit test: candidate subagent with/without `AGENT_TYPE: 2` | Test passes; only Type 2 subagents injected |
| REQ-08 | Unit test: candidate subagent without `AGENT_CLASS: TASK` | Warning logged; injection not blocked |
| REQ-09 | Integration test: trigger denial at each gate; verify parent turn completes | Parent turn returns normally; no error response |
| REQ-10 | Integration test: supply governance via UI opts with invalid runtime state | Injection blocked despite UI-supplied metadata |
| REQ-11 | Unit test: verify log output on allow and deny decisions | Log entries present with correct gate identification |
| REQ-12 | Unit test: verify gate function return value structure on allow and deny | Return value contains `allowed` boolean and denial identification on deny |
| REQ-13 | Code review + static analysis: confirm single injection code path gated by governance gate | No alternative injection path exists; all subagent injection flows through the gate |
| REQ-14 | TBD -- performance benchmark once acceptance criteria are defined | TBD |

## Documentation

### Required Artifacts

| Artifact | Type | Description |
|----------|------|-------------|
| Governance gate implementation | CODE | Runtime function(s) implementing REQ-01 through REQ-13 |
| Governance gate unit tests | TEST | Per-requirement test coverage for all gate conditions including type-coercion edge cases |
| Integration tests | TEST | End-to-end turn execution with governance gate exercised |
| Governance gate documentation | DOC | Developer documentation describing the gate logic, configuration, failure behaviors, and audit logging |
