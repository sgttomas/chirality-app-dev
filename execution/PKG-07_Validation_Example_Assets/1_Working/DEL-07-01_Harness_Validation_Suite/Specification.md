# Specification -- DEL-07-01 Harness Validation Suite

## Scope

### Included

This deliverable covers the creation and maintenance of repeatable validation scripts and documentation that verify the correctness of the Chirality harness runtime behaviors. The validation suite must be executable both locally (developer workstation) and in CI pipelines (headless, automated).

**Harness behavioral areas in scope** (Source: Decomposition DEL-07-01 description; SOW-028):

1. **Session lifecycle** -- session boot via `/api/harness/session/boot`, session initialization with `opts`, `projectRoot` binding
2. **Turn execution** -- turn submission via `/api/harness/turn`, end-to-end message processing
3. **SSE streaming** -- Server-Sent Events delivery from runtime to UI during turns
4. **Opts mapping and fallback chains** -- runtime option parsing, fallback chain resolution (model, tools, maxTurns)
5. **Subagent governance gating** -- fail-closed enforcement of delegation governance (contextSealed, pipelineRunApproved, approvalRef validation)
6. **Attachment contract behaviors** -- attachment resolver validation (extensions, isFile, size limits, budget, partial failure), prompt-mode selection (no-attachment vs. attachment-present paths)

### Excluded

- End-to-end UI testing (covered by other deliverables or manual testing)
- Performance benchmarking or load testing
- Testing of governance document content (covered by DEL-06-05)
- Testing of agent instruction conformance (covered by DEL-06-01)
- Example execution root maintenance (covered by DEL-07-02)
- Optional hardening features in PKG-08 (TBD scope)

## Requirements

### REQ-01: Validation Script Coverage

Validation scripts MUST cover all six harness behavioral areas listed in scope. Each area MUST have at least one dedicated test or test group.

**Source:** Decomposition DEL-07-01 description; SOW-028

### REQ-02: Local Execution

Validation scripts MUST be executable on a developer workstation running macOS 15+ on Apple Silicon without requiring external CI infrastructure.

**Source:** Decomposition DEL-07-01 ("local"); DEC-PLAT-001

### REQ-03: CI-Ready Posture

Validation scripts MUST be executable in a CI pipeline environment without interactive input (no prompts, no GUI dependencies for test execution).

**Source:** Decomposition DEL-07-01 ("CI-ready posture"); SOW-028

### REQ-04: Session Boot Validation

Tests MUST verify that:
- `/api/harness/session/boot` accepts `opts` and initializes a session correctly
- A valid `projectRoot` can be bound to a session
- Bootstrap policy constraints are enforced -- specifically, tests MUST verify that session boot behavior conforms to the initialization contract defined in SPEC Section 9.8 (the specific bootstrap policies enforced are TBD pending further enumeration from the runtime implementation; **ASSUMPTION**: bootstrap policies include at minimum `projectRoot` validation and `opts` schema conformance)

**Source:** SPEC Section 9.8; SOW-004; Lensing D-001

### REQ-05: Turn Execution Validation

Tests MUST verify that:
- `/api/harness/turn` accepts a turn with message content and processes it end-to-end, producing a complete response (observable completion signal: the SSE stream terminates with a final event, or the HTTP response completes with status 200 and a parseable response body)
- Turn execution produces a response that can be asserted against (response structure TBD pending runtime contract stabilization; at minimum, a non-empty response body)
- Turns with empty message but valid attachments are accepted
- Turns with empty message and no attachments are rejected (HTTP 400)

**Source:** SPEC Section 9.8; SOW-004, SOW-005, SOW-006; Lensing A-001

### REQ-06: SSE Streaming Validation

Tests MUST verify that:
- Turn execution produces SSE events delivered via the Server-Sent Events protocol
- SSE event stream is consumable by a client (events can be parsed as valid SSE format)
- At least one SSE event is received per turn execution (**ASSUMPTION** -- minimum event count; actual event types and fields TBD pending runtime contract specification of the SSE event schema)

**Source:** SPEC Section 9.8; SOW-005; Lensing X-004

### REQ-07: Opts Mapping and Fallback Chain Validation

Tests MUST verify that:
- `opts.model` falls back through: opts -> global model (instruction root) -> runtime default
- `opts.tools` falls back through: opts -> persona `tools` frontmatter -> runtime preset
- `opts.maxTurns` falls back through: opts -> persona `max_turns` frontmatter -> runtime default
- Omitted fields follow runtime fallback chains without error

**Source:** SPEC Section 9.8; SOW-011

### REQ-08: Subagent Governance Fail-Closed Validation

Tests MUST verify that:
- Subagent injection is blocked when `CHIRALITY_ENABLE_SUBAGENTS` is not `"true"`
- Subagent injection is blocked when `opts.subagentGovernance` is missing or invalid (missing `contextSealed`, `pipelineRunApproved`, or `approvalRef`)
- Parent turn continues normally when subagent injection is blocked
- Subagent injection proceeds only when **all** of the following governance conditions are simultaneously true: (a) `CHIRALITY_ENABLE_SUBAGENTS === "true"`, (b) `opts.subagentGovernance.contextSealed === true`, (c) `opts.subagentGovernance.pipelineRunApproved === true`, (d) `opts.subagentGovernance.approvalRef` is a non-empty string referencing a valid approval record

**Source:** SPEC Section 9.7; SOW-012; Lensing F-001

### REQ-09: Attachment Resolver Validation

Tests MUST verify that:
- Supported extensions are accepted (`.png`, `.jpg`, `.jpeg`, `.gif`, `.webp`, `.pdf`, `.txt`, `.md`, `.csv`)
- Unsupported extensions are rejected
- Directories, symlinks, and special files are rejected (`stats.isFile()` check)
- Per-file size limit is enforced: files of exactly 10,000,000 bytes (10 MB, decimal) MUST be accepted; files of 10,000,001 bytes MUST be rejected (**ASSUMPTION** -- decimal MB interpretation based on SPEC Section 9.8 "10 MB" notation; see Guidance for normalization note)
- Total per-turn raw-byte budget is enforced: combined attachment size up to 18,000,000 bytes (18 MB, decimal) MUST be accepted; exceeding this budget MUST be rejected (**ASSUMPTION** -- decimal MB interpretation)
- Partial attachment failure is non-fatal when executable content remains
- All-attachments-fail with empty text produces 400

**Source:** SPEC Section 9.8; SOW-007, SOW-008; Lensing E-001, B-003

### REQ-10: Prompt Mode Selection Validation

Tests MUST verify that:
- No attachments: runtime uses `query({ prompt: string })`
- Attachments present: runtime builds multimodal content blocks and uses `query({ prompt: AsyncIterable<SDKUserMessage> })`

**Source:** SPEC Section 9.8; SOW-009

### REQ-11: Validation Documentation

Documentation MUST describe:
- How to run the validation suite locally
- How to integrate the validation suite into a CI pipeline
- What each test validates and its expected pass/fail criteria
- Prerequisites for running (environment, API key, working root setup)

**Source:** Decomposition DEL-07-01 anticipated artifacts (DOC); SOW-028

### REQ-12: Repeatable Execution

Validation scripts MUST produce consistent results when run multiple times against the same harness state. Tests MUST NOT have order-dependent side effects that cause failures on rerun.

**Source:** Decomposition DEL-07-01 ("repeatable"); **ASSUMPTION** -- standard test suite quality requirement

### REQ-13: CONTRACT.md K-Invariant Coverage

Tests SHOULD validate harness behaviors against the following CONTRACT.md binding invariants, mapped to relevant behavioral areas:

| K-Invariant | Description | Relevant Behavioral Area | Relevant REQs |
|-------------|-------------|--------------------------|----------------|
| K-SEAL-1 | Sealed context: no ghost inputs; subagent injection requires contextSealed | Subagent governance gating | REQ-08 |
| K-GHOST-1 | No ghost inputs: all inputs traceable to human-visible sources | Session lifecycle, Turn execution | REQ-04, REQ-05 |
| K-INVENT-1 | Epistemic integrity: tests should not invent expected values; assertions based on contract specifications | All areas | REQ-01 through REQ-12 |
| K-CONFLICT-1 | Conflict resolution: when test expectations conflict with observed behavior, report as a finding rather than force-passing | All areas | REQ-01 through REQ-12 |

**Note:** Specific test assertions per K-invariant are TBD pending detailed mapping during test inventory design (Procedure Phase 1).

**Source:** `docs/CONTRACT.md` K-SEAL-1, K-GHOST-1, K-INVENT-1, K-CONFLICT-1; Datasheet R2; Lensing B-002

### REQ-14: Test Isolation

Tests MUST NOT depend on execution order, shared mutable state, or side effects from other tests. Each test or test group MUST be independently executable and produce the same result regardless of which other tests have run before it.

**Source:** Lensing X-002; **ASSUMPTION** -- standard test engineering practice extending REQ-12 (repeatability) to inter-test independence

### REQ-15: Error Path Validation

Tests SHOULD verify that invalid inputs to harness endpoints produce appropriate error responses (HTTP status codes such as 400 and 403) and do not cause unhandled exceptions or silent failures. At minimum, the following error paths MUST be tested:
- Empty message with no attachments (400) -- per REQ-05
- Unsupported attachment extensions (rejection) -- per REQ-09
- Subagent injection with invalid governance metadata (blocked) -- per REQ-08

Additional error paths per REQ (e.g., malformed `opts`, invalid `projectRoot`) are TBD pending enumeration from SPEC Section 9.8.

**Source:** SPEC Section 9.8; Lensing X-003; **ASSUMPTION** -- error codes inferred from contract behaviors described in SPEC

### REQ-16: Deliverable Acceptance Criteria

The validation suite deliverable (DEL-07-01) SHALL be considered complete when **all** of the following conditions are met:
- All REQs (REQ-01 through REQ-15) have at least one test or verification artifact addressing them
- Validation documentation per REQ-11 exists and is reviewable
- Repeatability per REQ-12 has been demonstrated (two consecutive identical runs)
- Test-to-requirement traceability mapping exists (see Procedure Phase 5)

**Note:** Quantitative pass-rate thresholds (e.g., "100% of contract tests pass") are TBD pending human ruling on acceptable partial-pass scenarios.

**Source:** Lensing A-005, D-003

## Standards

| Standard / Reference | Applicability | Accessible |
|---------------------|---------------|------------|
| `docs/SPEC.md` Section 9.7-9.8 | Defines the harness turn input contract, subagent governance, and attachment rules that tests validate | Yes |
| `docs/CONTRACT.md` K-SEAL-1, K-GHOST-1 | Sealing and context invariants relevant to subagent governance testing | Yes |
| `docs/CONTRACT.md` K-INVENT-1, K-CONFLICT-1 | Epistemic integrity invariants -- tests should not invent expected values | Yes |
| DEC-PLAT-001 | Target platform constraint (macOS 15+, Apple Silicon) | Yes (Decomposition Decision Log) |
| DEC-NET-001 | Anthropic-only outbound network policy -- relevant to integration test constraints | Yes (Decomposition Decision Log) |

## Verification

| Requirement | Verification Approach |
|-------------|----------------------|
| REQ-01 | Inspect test inventory; confirm each of the six behavioral areas has at least one dedicated test or test group. Pass criterion: 6/6 areas covered. |
| REQ-02 | Execute validation suite on macOS 15+ Apple Silicon developer machine; confirm all tests execute without platform-related failures |
| REQ-03 | Execute validation suite in headless CI environment; confirm no interactive prompts and all tests produce exit codes (0=pass, non-zero=fail) |
| REQ-04 | Run session boot tests; verify session initializes with valid `opts` and `projectRoot`; verify bootstrap policy enforcement per SPEC Section 9.8 |
| REQ-05 | Run turn execution tests; verify HTTP 200 response with parseable body for valid turns; verify HTTP 400 for empty-message-no-attachments |
| REQ-06 | Run SSE streaming tests; verify at least one SSE event is received per turn; verify events are parseable as valid SSE format |
| REQ-07 | Run opts fallback tests; verify correct resolution at each fallback level by providing opts at each level and asserting resolved value |
| REQ-08 | Run subagent governance tests; verify fail-closed behavior for each of the four governance conditions (a-d) individually and in combination |
| REQ-09 | Run attachment resolver tests with boundary-value inputs (10,000,000 bytes, 10,000,001 bytes, 18,000,000 bytes cumulative); verify accept/reject at each boundary |
| REQ-10 | Run prompt mode selection tests; verify `query({ prompt: string })` for no-attachment path and `query({ prompt: AsyncIterable<SDKUserMessage> })` for attachment path |
| REQ-11 | Review documentation for completeness: local run instructions, CI guide, test descriptions, prerequisites -- all four items present and actionable |
| REQ-12 | Run validation suite twice consecutively against same harness state; confirm identical pass/fail outcomes on both runs |
| REQ-13 | Review test assertions against K-invariant mapping table; confirm each listed K-invariant has at least one corresponding test or test group |
| REQ-14 | Execute tests in randomized order (if framework supports) or execute individual tests in isolation; confirm same results as full-suite run |
| REQ-15 | Run error-path tests; confirm expected HTTP error codes (400, 403) are returned for invalid inputs |
| REQ-16 | Review deliverable against acceptance criteria checklist; confirm all four conditions are met |

## Documentation

### Required Artifacts

| Artifact | Type | Description |
|----------|------|-------------|
| Validation scripts | SCRIPT | `.mjs` modules covering all six behavioral areas (**ASSUMPTION** -- file type based on PLAN Section 2) |
| Validation documentation | DOC | Run instructions, CI integration guide, test descriptions, prerequisites |
| Test result output | TEST | Pass/fail reporting suitable for local review and CI consumption |
| Test-to-requirement traceability | DOC | Mapping from each test to the REQ(s) it validates (see Procedure Phase 5, Records) |
