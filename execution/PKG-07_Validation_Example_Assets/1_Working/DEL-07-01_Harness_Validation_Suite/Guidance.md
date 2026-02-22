# Guidance -- DEL-07-01 Harness Validation Suite

## Purpose

This deliverable exists to provide a repeatable, evidence-based validation posture for the Chirality harness runtime. Without a structured validation suite, correctness of session lifecycle, turn execution, streaming, option handling, subagent governance, and attachment processing can only be verified through manual ad-hoc testing -- which is neither repeatable nor CI-integrable.

The validation suite directly supports OBJ-006: "Validation posture and governance/agent-suite conformance enable repeatable operation." It operationalizes the SOW-028 commitment: "Provide repeatable harness validation scripts and docs suitable for local + CI validation gates."

**Source:** Decomposition OBJ-006; SOW-028

## Principles

### P1: Test the Contract, Not the Implementation

Validation scripts should test against the harness contract defined in `docs/SPEC.md` Sections 9.7-9.8, not against internal implementation details. This makes tests resilient to refactoring while catching genuine contract violations.

**Source:** DIRECTIVE Section 2.4 ("Evidence Over Plausibility"); SPEC Section 9.7-9.8

### P2: Fail-Closed as the Default Posture

Tests for governance and security behaviors (subagent gating, attachment validation) should verify that the system fails closed -- rejecting invalid inputs rather than permitting them. The test suite should treat "passed when it should have blocked" as a more severe failure than "blocked when it should have passed."

**Source:** SPEC Section 9.7 (delegation governance fail-closed rule); SOW-012

### P3: Local-First, CI-Compatible

The suite should be designed for local developer execution first, with CI compatibility achieved through headless-friendly design (no interactive prompts, deterministic outputs, clear exit codes). Local execution is the primary workflow; CI is the verification gate.

**Source:** Decomposition DEL-07-01 ("local + CI-ready posture")

### P4: Filesystem-as-State Awareness

Tests that interact with session boot or working-root binding must respect the "filesystem is the state" principle. Test fixtures should use temporary directories with known content rather than depending on persistent external state.

**Source:** DIRECTIVE Section 2.1; SOW-014

### P5: Evidence Over Coverage Metrics

Validation quality is measured by whether tests catch real contract violations, not by line-coverage percentages. Tests should target behavioral contract boundaries (edge cases at size limits, extension boundaries, fallback chain endpoints) rather than maximizing nominal coverage.

**Source:** DIRECTIVE Section 2.4

### P6: Guard Against False Confidence

Tests that always pass provide negative value by creating false confidence in harness correctness. The suite SHOULD include canary or negative tests that verify the test framework itself can detect failures -- e.g., a test that intentionally submits an invalid input and asserts it is rejected. If such a canary test passes (meaning the rejection was detected), the test framework is functioning correctly. If the canary test itself fails to detect the rejection, this signals mock drift or broken test infrastructure.

**Source:** Lensing E-003; **ASSUMPTION** -- standard practice for test suite integrity; extends P5 (evidence over coverage)

## Considerations

### C1: API Key Dependency

Integration tests that exercise live turn execution require a valid Anthropic API key. The key provisioning and storage contract is unresolved (OI-001). Until resolved, the validation suite should:
- Clearly separate tests requiring a live API key from tests that can run without one (e.g., attachment resolver validation, governance gating with mock data)
- Document the API key requirement as a prerequisite

**Source:** Decomposition Open Issues OI-001; DEC-NET-001

### C2: Network Policy Verification and Test Infrastructure Compliance

SOW-028 includes "attachments contract behaviors" but does not explicitly include outbound network policy verification (that is DEL-03-06's scope). However, the validation suite may need awareness of the Anthropic-only network constraint to avoid test infrastructure that violates the policy.

**Actionable direction:** Test infrastructure (fixture downloads, npm test dependencies, CI runners) should be evaluated for DEC-NET-001 compliance. Specifically:
- Test fixtures SHOULD be generated locally (not downloaded from external URLs) to avoid violating the Anthropic-only outbound policy
- npm dependencies required for test execution should be installed from a pre-populated cache or during an explicit setup phase, not during test execution itself
- If the test suite requires any outbound network calls beyond Anthropic API, this constitutes a DEC-NET-001 exception that requires human ruling

**Note:** Whether test tooling itself must comply with DEC-NET-001 is TBD -- the policy is defined for the application runtime; its applicability to development/CI tooling requires human ruling.

**Source:** DEC-NET-001; Decomposition DEL-03-06; Lensing C-001

### C3: Subagent Governance Test Isolation

Testing subagent governance fail-closed behavior requires controlled conditions: `CHIRALITY_ENABLE_SUBAGENTS` environment variable state, governance metadata presence/absence, and parent turn continuation verification. Tests should be able to set these conditions without affecting other test groups.

**Source:** SPEC Section 9.7

### C4: Attachment Test Fixtures

Attachment resolver tests need fixture files of various types, sizes, and edge conditions (exactly 10,000,000 bytes, just over 10,000,001 bytes, total budget boundary at 18,000,000 bytes, symlinks, directories). These fixtures should be lightweight and reproducible (generated programmatically where possible rather than committed as large binaries).

**Source:** SPEC Section 9.8 (attachment validation rules)

### C5: SSE Event Verification Timing

SSE streaming validation involves asynchronous event delivery. Tests must handle timing sensitivity -- waiting long enough for events to arrive without creating brittle timeout-dependent tests. Consider using event-driven assertions (wait for specific event types) rather than fixed delays.

**Source:** SPEC Section 9.8; SOW-005; **ASSUMPTION** -- standard practice for SSE testing

### C6: Relationship to DEL-07-02 (Example Execution Roots)

DEL-07-02 maintains example execution roots for regression/conformance testing. The validation suite may consume these examples as test fixtures for session boot tests (binding a known-good working root). Coordinate fixture formats to avoid duplication.

**Source:** Decomposition DEL-07-02; SOW-029

### C7: Test Maintenance Lifecycle

The validation suite's value degrades over time if tests drift from evolving harness contracts. Consider the following maintenance concerns:
- **Ownership:** Who updates tests when harness contracts change? Tests covering SPEC Section 9.7-9.8 behaviors should be updated whenever the corresponding SPEC sections change.
- **Drift detection:** How is test-contract drift detected? **ASSUMPTION**: a periodic review step (e.g., at each release) where the test inventory is compared against the current SPEC sections would catch drift. Automated drift detection is TBD.
- **Co-evolution:** Changes to PKG-03 (Runtime Core) deliverables that modify harness API behavior should trigger a review of affected tests in DEL-07-01.

**Source:** Lensing X-001; **ASSUMPTION** -- maintenance lifecycle not specified in governance documents; this consideration is inferred from standard test suite practices

### C8: Size Limit Normalization Note

SPEC Section 9.8 specifies attachment limits as "10 MB" (per-file) and "18 MB" (total budget). This deliverable interprets "MB" as decimal megabytes (1 MB = 1,000,000 bytes), yielding:
- Per-file limit: 10,000,000 bytes
- Total budget: 18,000,000 bytes

This interpretation is consistent with the Guidance example using "10,000,001 bytes" as the boundary-exceeding value. If the implementation uses binary mebibytes (1 MiB = 1,048,576 bytes), the boundary values would differ (10,485,760 and 18,874,368 bytes respectively), and tests would produce off-by-one failures.

**Human ruling needed:** Confirm whether "10 MB" means 10,000,000 bytes (decimal) or 10,485,760 bytes (binary). This ruling affects Specification REQ-09 boundary values and all attachment test fixtures.

**Source:** SPEC Section 9.8; Lensing B-003, E-001

### C9: Minimum Confidence Threshold

No document currently specifies what level of test passage constitutes sufficient validation for harness release decisions. Consider defining:
- **Contract tests:** All must pass (100%) for any release -- these validate binding invariants
- **Integration tests:** TBD pass threshold -- these depend on API availability and may have legitimate environmental failures

Until a minimum confidence threshold is defined, the suite provides evidence but does not gate releases. Human ruling needed on whether this suite serves as a formal release gate or as an advisory validation tool.

**Source:** Lensing C-002; **ASSUMPTION** -- no governance document defines a release-gating threshold for this suite

## Trade-offs

### T1: Live Integration Tests vs. Mocked Tests

| Option | Pros | Cons |
|--------|------|------|
| All live integration | Tests real behavior end-to-end | Requires API key, slower execution, potential rate limits, non-deterministic |
| All mocked | Fast, deterministic, no API key needed | May miss real integration issues; mock drift risk |
| Hybrid (recommended) | Contract boundary tests run mocked; critical path tests run live | More complex test organization; must document which require API key |

**Recommendation (PROPOSAL):** Hybrid approach -- separate test groups into "contract tests" (mocked/unit, no API key) and "integration tests" (live, API key required). CI pipelines can run contract tests always and integration tests conditionally.

### T2: Test Framework Selection

| Option | Pros | Cons |
|--------|------|------|
| Standalone `.mjs` scripts | No framework dependency; matches existing `validate-harness-*.mjs` pattern | No built-in assertion library, test discovery, or reporting |
| Node.js test runner (`node:test`) | Built-in, no dependencies, supports `.mjs` | Newer API; less ecosystem tooling |
| Jest / Vitest | Rich assertion, mocking, reporting | Additional dependency; configuration overhead |

**Recommendation (PROPOSAL):** Follow the existing pattern (`validate-harness-*.mjs` standalone scripts) per PLAN Section 2 references, unless the human decides a framework provides sufficient benefit. The choice is TBD pending review of existing script conventions.

### T3: CI Pipeline Technology

The CI integration approach depends on the project's CI platform choice (not specified in scope). Scripts should output standard exit codes (0 = pass, non-zero = fail) and optionally produce structured output (JSON or TAP) for CI consumption.

**Source:** SOW-028 ("CI-ready"); **ASSUMPTION** -- CI platform not specified

## Examples

### Example: Attachment Resolver Boundary Test (Conceptual)

```
Test: "Rejects file exceeding per-file size limit"
Given: A file of exactly 10,000,001 bytes (.txt extension)
When: Submitted as an attachment in a turn request
Then: Attachment is rejected; turn continues if other content exists

Test: "Accepts file at per-file size limit"
Given: A file of exactly 10,000,000 bytes (.txt extension)
When: Submitted as an attachment in a turn request
Then: Attachment is accepted and processed
```

**Source:** SPEC Section 9.8 (per-file size limit: 10 MB); Lensing E-001, B-003

### Example: Subagent Governance Fail-Closed Test (Conceptual)

```
Test: "Blocks subagent injection when contextSealed is false"
Given: CHIRALITY_ENABLE_SUBAGENTS = "true"
  And: opts.subagentGovernance = { contextSealed: false, pipelineRunApproved: true, approvalRef: "REF-001" }
When: A turn is executed with a persona allowlisted for subagents
Then: Subagent injection is blocked
  And: Parent turn completes normally
```

**Source:** SPEC Section 9.7 (delegation governance fail-closed rule)

## Conflict Table (for human ruling)

| Conflict ID | Conflict | Source A | Source B | Impacted Sections | Proposed Authority | Human Ruling |
|-------------|----------|----------|----------|--------------------|--------------------|--------------|
| CT-001 | "10 MB" and "18 MB" size limits: decimal MB (10,000,000 bytes) vs. binary MiB (10,485,760 bytes) interpretation | SPEC Section 9.8 ("10 MB") | Guidance Example uses "10,000,001 bytes" (implies decimal) | Specification REQ-09; Guidance C8; Datasheet Attributes (attachment resolver rules); Procedure Phase 2 Step 2.1 | SPEC Section 9.8 (normative) -- propose decimal interpretation pending human confirmation | TBD |
| CT-002 | Script and documentation paths (`frontend/scripts/validate-harness-*.mjs`, `frontend/docs/harness/`) are marked ASSUMPTION throughout; no authoritative source confirms these paths | PLAN Section 2 (references scripts) | Actual repository structure (not yet verified) | Datasheet Construction; Procedure Phase 5 Step 5.4 | Human confirmation of actual paths | TBD |
| CT-003 | Node.js version requirement: no source specifies a minimum version; tests may fail silently on incompatible versions | Datasheet Conditions (Node.js environment) | Procedure PR-02 (version TBD) | Datasheet Conditions; Procedure Prerequisites; Specification REQ-02 | Human decision (depends on Electron/Next.js version pinning) | TBD |
