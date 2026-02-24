# Guidance — DEL-03-04 Subagent Governance Fail-Closed Enforcement

## Purpose

This deliverable exists because the Chirality harness allows Type 1 (Manager) personas to delegate work to Type 2 (Specialist) subagents. Delegation is powerful but creates a trust boundary: a subagent executes with its own context window, reads/writes within a declared scope, and produces outputs that flow back into the project.

Without governance, subagent injection could occur in contexts where:
- The human has not sealed and approved the execution context (violating K-SEAL-1).
- The subagent could operate outside its declared write scope (risking K-WRITE-1, K-GHOST-1 violations).
- No traceability exists to a human approval record (violating K-AUTH-1, K-AUTH-2).

The fail-closed posture ensures that delegation **never happens by accident**. The default state is "no subagents." Every path to subagent injection requires explicit, verifiable human authorization.

**Source:** Decomposition DEL-03-04 entry; SPEC Section 9.7; CONTRACT K-SEAL-1, K-AUTH-1; DIRECTIVE Section 2.3 (human authority at every gate). **Note:** DIRECTIVE Section 2.5 is also cited in Specification REQ-10 for UI/runtime separation rationale -- see Conflict Table entry CT-001 for normalization of DIRECTIVE section references.

## Implementation Notes (2026-02-24 PASS1)

- Runtime governance evaluation is now implemented in `frontend/src/lib/harness/subagent-governance.ts`.
- Turn-route integration now evaluates governance before SDK execution and propagates `delegatedSubagents` as the runtime delegation eligibility set.
- Shared agent-instruction parsing is centralized in `frontend/src/lib/harness/agent-instruction.ts` and reused by governance + options/persona consumers.
- Current implementation enforces fail-closed gating and registry validation; full runtime subagent fan-out execution remains a follow-through scope item.

## Principles

### Deny by Default

The security model is deny-by-default (fail-closed). Subagent injection is blocked unless every gate condition is affirmatively satisfied. This is the opposite of a fail-open model where injection would proceed unless a specific blocker was detected.

**Rationale:** In a system where AI agents produce drafts for professional reliance, an unintended delegation could produce outputs that bypass human review gates. Deny-by-default eliminates this class of failure. (DIRECTIVE Section 2.3; CONTRACT K-AUTH-1.)

### Gate Independence

Each gate condition (environment, persona allowlist, governance metadata fields) is independently necessary. Satisfying one gate does not reduce the requirements of another. All gates must pass simultaneously.

**Rationale:** Defense-in-depth. A misconfigured environment variable should not be overridable by supplying governance metadata, and vice versa. (SPEC Section 9.7 lists conditions conjunctively.)

### Graceful Degradation

When delegation is denied, the parent turn must continue normally. The operator experiences a turn without subagent capabilities, not a turn failure. This avoids creating pressure to weaken governance in order to prevent operational disruption.

**Rationale:** If governance denial caused visible failures, operators would be incentivized to bypass controls. Graceful degradation removes this incentive. (SPEC Section 9.7 -- "allowing the parent turn to continue normally.")

**Multiple gate failures:** When multiple gate conditions fail simultaneously, the governance gate should evaluate all gates and report the first-failing gate (short-circuit) or all failing gates, depending on the implementation pattern chosen. The trade-off is between diagnostic completeness (reporting all failures aids debugging and operator understanding) and simplicity (short-circuiting is simpler and avoids unnecessary evaluation). **ASSUMPTION:** The choice between all-failure reporting and short-circuit reporting is an implementation decision not prescribed by SPEC. The Procedure prescribes a specific evaluation order (environment first, then persona, then metadata fields) which implies short-circuit behavior, but the Specification does not mandate this ordering (see Conflict Table entry CT-003).

### UI Is Informational, Runtime Is Authoritative

The Operator Toolkit panel may display governance-related fields, but the UI is never authoritative for enforcement. The runtime gate logic is the sole enforcement point. UI-supplied values are inputs to the gate, not overrides of it.

**Rationale:** Prevents the "settings page bypass" pattern where adjusting a UI control circumvents a security gate. (SPEC Section 9.8 -- "Supplying `opts.subagentGovernance` does not guarantee delegation.")

### Sole Enforcement Point

The governance gate must be the single code path through which all subagent injection flows. No alternative route may bypass it. This is distinct from the UI override principle (REQ-10): REQ-10 addresses the UI surface, while the sole enforcement point principle addresses the code architecture.

**Rationale:** If an alternative code path can inject subagents without traversing the governance gate, the fail-closed posture is structurally defeated regardless of how robust the gate logic itself is. (SPEC Section 9.7 implicit; see Specification REQ-13.)

## Considerations

### Strict Type Checking on Gate Fields

The SPEC requires strict equality checks (`=== true`, not truthy). This means:
- `contextSealed: "true"` (string) must fail the gate.
- `pipelineRunApproved: 1` (number) must fail the gate.
- `approvalRef: 0` (number) must fail the gate.

This prevents type coercion vulnerabilities where loosely-typed comparisons could inadvertently pass the gate.

**Source:** SPEC Section 9.7 uses `===` notation for all field checks.

### approvedBy Is Optional

The `approvedBy` field is explicitly optional in SPEC Section 9.7. It provides additional audit context (who approved) but is not a gate condition. Implementations should accept and log it when present but must not require it.

### Subagent Class Warning vs. Block

`AGENT_CLASS: TASK` is preferred but validated at warning level only. This is a deliberate design choice: the system wants to encourage the TASK class pattern for subagents (straight-through, non-interactive) but does not want to block legitimate edge cases where a different class might be needed.

**ASSUMPTION:** Edge cases for non-TASK subagent classes have not been formally identified. The warning exists as a safety signal for future evaluation.

### Body Header Format Clarification

The term "body header" is used across documents (Datasheet Attributes, Specification REQ-07, Procedure Step 3) to refer to the location where `AGENT_TYPE: 2` must be declared. However, the concrete format of this "body header" is not precisely defined in accessible sources: it could be YAML frontmatter, a markdown heading, or a specific line pattern.

**ASSUMPTION:** "Body header" refers to a structured metadata block at the top of an agent instruction file that is parseable for key-value pairs such as `AGENT_TYPE` and `AGENT_CLASS`. TYPES.md Section 4 likely defines the format (**location TBD**). Implementers should confirm the parsing rules before implementing REQ-07 to avoid implementation variance.

### Relationship to DEL-03-03 (Turn Options Mapping)

DEL-03-03 handles the general `opts` mapping and fallback chains. DEL-03-04 consumes one specific field from `opts` (`subagentGovernance`) but does not modify the opts mapping logic itself. The boundary is: DEL-03-03 makes `opts.subagentGovernance` available; DEL-03-04 evaluates it.

**Source:** Decomposition -- DEL-03-03 covers SOW-011 (opts mapping), DEL-03-04 covers SOW-012 (governance enforcement).

### Relationship to DEL-07-01 (Harness Validation Suite)

DEL-07-01 provides the validation infrastructure and CI integration. DEL-03-04 provides the governance-gate-specific unit and integration tests. The governance tests produced here should be compatible with the validation harness defined by DEL-07-01.

**Source:** Decomposition -- DEL-07-01 covers SOW-028; its description explicitly mentions "subagent gating."

### Audit Trail Completeness

The governance gate must produce log records sufficient for audit purposes, but the log record schema is currently TBD. Considerations for the schema include:
- What fields should be logged on allow vs. deny decisions (e.g., timestamp, gate evaluated, decision, approvalRef value, approvedBy value if present).
- At what log level should allow vs. deny decisions be recorded.
- Whether the log record format should be structured (JSON) or unstructured.

**ASSUMPTION:** The log record schema will be defined during implementation. Specification REQ-11 establishes the normative requirement for logging; the schema details are an implementation decision. (SPEC Section 9.7 implicit; CONTRACT K-AUTH-1 supports audit trail need.)

### Concurrency and Atomicity

TBD -- Neither the Specification nor this Guidance currently addresses whether concurrent turns from the same session could create race conditions in governance gate evaluation. For example, if governance metadata is changed between the gate check and the actual subagent injection, the gate decision could be stale. Considerations include:
- Whether the gate evaluation is atomic with respect to the injection action.
- Whether multiple concurrent turns could each independently evaluate the gate using the same governance metadata.
- Whether this is a realistic concern given the expected usage patterns (single-operator, sequential turn submission).

**ASSUMPTION:** The current design assumes sequential turn execution within a session, making concurrency a low-priority concern. If concurrent turn execution is supported in the future, atomicity of the gate-check-then-inject sequence should be revisited.

### Denial Response Format Rationale

The integration test for denial-continuation (Procedure Step 6.2) checks for "200 response, streamed events" as the success signal for a denied turn. The rationale is that a denied turn should be indistinguishable from a normal turn (from the client's perspective) except that no subagent outputs appear in the event stream. The 200 status code confirms the turn executed successfully; streamed events confirm the parent continued normally. This is the observable consequence of REQ-09 (parent turn continuation on denial).

**Source:** SPEC Section 9.7 -- "allowing the parent turn to continue normally"; Procedure.md Step 6.2.

### Security Threat Model

As a SECURITY_CONTROL deliverable, the governance gate protects against specific attack vectors and has known limitations:

**Threats mitigated:**
- **Type coercion injection:** Strict `===` checks prevent truthy values (e.g., `contextSealed: "true"` as string, `pipelineRunApproved: 1` as number) from passing the gate. (SPEC Section 9.7; Specification REQ-04, REQ-05.)
- **Metadata spoofing:** The gate requires a non-empty `approvalRef` string traceable to a human approval record. Without a valid approval reference, injection is blocked. (CONTRACT K-AUTH-1.)
- **Unauthorized persona delegation:** Only personas with explicitly declared `subagents` in frontmatter can trigger delegation, preventing injection from non-allowlisted personas. (SPEC Section 9.7; Specification REQ-02.)
- **Environment misconfiguration:** The environment gate provides a global kill switch for all subagent delegation. (SPEC Section 9.7; Specification REQ-01.)
- **UI bypass:** Runtime gates operate independently of UI-supplied values, preventing the "settings page bypass" pattern. (SPEC Section 9.8; Specification REQ-10.)

**Residual risks / not mitigated:**
- **approvalRef validity:** The gate checks that `approvalRef` is a non-empty string but does not validate that the referenced approval record actually exists or is current. **ASSUMPTION:** Approval record validation is out of scope for the runtime gate and is handled by upstream workflow (human review).
- **Environment variable manipulation:** If an attacker can set `CHIRALITY_ENABLE_SUBAGENTS`, they can pass Gate 1, though all other gates must still pass. The environment gate is defense-in-depth, not a standalone control.
- **Instruction file tampering:** If an attacker can modify the persona instruction file's `subagents` frontmatter or a subagent instruction file's `AGENT_TYPE` declaration, they can influence gate decisions. File integrity is assumed to be managed by the filesystem-as-state model and git hygiene (DEL-06-04).
- **Concurrency race conditions:** See Concurrency and Atomicity consideration above.

**Source:** Analysis based on SPEC Section 9.7, CONTRACT K-SEAL-1, K-AUTH-1, K-GHOST-1; threat categories are **ASSUMPTION** (no formal threat model exists in accessible sources).

## Trade-offs

| Trade-off | Choice Made | Alternative Considered | Rationale |
|-----------|-------------|----------------------|-----------|
| Strict vs. lenient type checking | Strict (`===`) | Truthy checks | Strict prevents type coercion bypass; aligns with SPEC notation |
| Gate denial: error vs. continuation | Parent continues normally | Return error to client | Continuation prevents governance-weakening pressure |
| `AGENT_CLASS: TASK` enforcement level | Warning (non-blocking) | Hard block | Allows flexibility for edge cases while signaling intent |
| Single gate function vs. middleware chain | TBD | TBD | **ASSUMPTION:** Implementation pattern is not prescribed by SPEC; to be decided during implementation |
| Gate evaluation order: prescribed vs. unordered | TBD | TBD | Procedure prescribes order (env, persona, metadata) but Specification does not mandate sequencing; see Conflict Table entry CT-003 |
| Multiple-failure reporting vs. short-circuit | TBD | TBD | Trade-off between diagnostic completeness and simplicity; see Graceful Degradation principle |

## Examples

### Example 1: All Gates Pass (Injection Allowed)

```
Environment: CHIRALITY_ENABLE_SUBAGENTS = "true"
Persona: declares subagents: [PREPARATION, 4_DOCUMENTS]
opts.subagentGovernance:
  contextSealed: true
  pipelineRunApproved: true
  approvalRef: "GATE-2026-02-21-001"
  approvedBy: "ryan"
Candidate subagent: PREPARATION (AGENT_TYPE: 2, AGENT_CLASS: TASK)

Result: Injection allowed. PREPARATION is injected as a subagent.
Gate log: ALLOW — all gates passed — approvalRef: GATE-2026-02-21-001
```

**Source:** SPEC Section 9.7 (all conditions satisfied).

### Example 2: Missing Governance Metadata (Injection Blocked)

```
Environment: CHIRALITY_ENABLE_SUBAGENTS = "true"
Persona: declares subagents: [PREPARATION]
opts: { model: "claude-opus-4-6" }  // no subagentGovernance field

Result: Injection blocked. Parent turn executes normally without subagents.
Gate log: DENY — gate 3 (metadata presence) — subagentGovernance field missing
```

**Source:** SPEC Section 9.7 -- "Missing/invalid governance metadata MUST block subagent injection."

### Example 3: Context Not Sealed (Injection Blocked)

```
Environment: CHIRALITY_ENABLE_SUBAGENTS = "true"
Persona: declares subagents: [4_DOCUMENTS]
opts.subagentGovernance:
  contextSealed: false
  pipelineRunApproved: true
  approvalRef: "GATE-2026-02-21-002"

Result: Injection blocked. contextSealed !== true.
Parent turn continues normally.
Gate log: DENY — gate 4 (contextSealed) — value is false, expected true
```

**Source:** SPEC Section 9.7 -- "`contextSealed === true`" required.

### Example 4: Type Coercion Attempt (Injection Blocked)

```
Environment: CHIRALITY_ENABLE_SUBAGENTS = "true"
Persona: declares subagents: [PREPARATION]
opts.subagentGovernance:
  contextSealed: "true"         // string, not boolean
  pipelineRunApproved: 1        // number, not boolean
  approvalRef: "GATE-2026-02-21-003"

Result: Injection blocked. contextSealed is string "true", not boolean true.
Gate log: DENY — gate 4 (contextSealed) — value is string "true", expected boolean true
```

**Source:** SPEC Section 9.7 uses `===` notation; Specification REQ-04.

## Conflict Table (for human ruling)

| Conflict ID | Conflict | Source A | Source B | Impacted Sections | Proposed Authority (PROPOSAL) | Human Ruling |
|-------------|----------|----------|----------|-------------------|-------------------------------|--------------|
| CT-001 | DIRECTIVE section reference inconsistency: Specification REQ-10 rationale cites "DIRECTIVE Section 2.5 clarification" but Guidance Purpose and Datasheet References cite only DIRECTIVE Section 2.3. It is unclear whether Section 2.5 is a distinct applicable section or a mislabel. | Specification.md REQ-10 (DIRECTIVE Section 2.5) | Guidance.md Purpose / Datasheet.md References (DIRECTIVE Section 2.3) | Specification REQ-10 rationale, Guidance Purpose, Datasheet References, Standards table | DIRECTIVE.md | TBD |
| CT-002 | K-AUTH-2 reference inconsistency: Specification REQ-06 cites K-AUTH-2 in rationale and K-AUTH-2 appears in the Standards table, but K-AUTH-2 is not listed in Datasheet References. K-AUTH-1 is consistently listed everywhere. | Specification.md REQ-06, Standards table (K-AUTH-2 present) | Datasheet.md References (K-AUTH-2 absent in Pass 1 draft, added in Pass 3 as TBD) | Specification REQ-06 rationale, Datasheet References, Standards table | CONTRACT.md | TBD |
| CT-003 | Gate evaluation order: Procedure Step 2 prescribes a specific evaluation order (environment first, then persona, then metadata fields) but Specification lists requirements REQ-01 through REQ-06 without mandating that they be evaluated in that order. This affects short-circuit behavior and logging. | Specification.md Requirements (no ordering mandate) | Procedure.md Step 2 (prescribed order: env, persona, metadata presence, contextSealed, pipelineRunApproved, approvalRef) | Specification Requirements, Procedure Step 2, Guidance Graceful Degradation | SPEC Section 9.7 | TBD |
