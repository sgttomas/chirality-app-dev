# Procedure -- DEL-03-03 Turn Options Mapping & Fallback Chains

## Purpose

This procedure describes the steps to produce and verify the Turn Options Mapping & Fallback Chains deliverable. It covers code implementation, testing, and documentation for the runtime `opts` resolution logic.

## Prerequisites

| Prerequisite | Description | Status | Readiness Criteria |
|-------------|-------------|--------|-------------------|
| Codebase access | Access to the Chirality frontend repository (`frontend/`) containing harness runtime code | TBD | *(Lensing item F-002)* Confirm repository is cloned, accessible, and the developer has read/write permissions to the harness runtime source tree |
| Existing turn API | `POST /api/harness/turn` endpoint exists and accepts requests (DEL-03-02 scope) | TBD | *(Lensing item F-002)* Confirm endpoint responds to a health check or basic request; DEL-03-02 status is INITIALIZED or later |
| Existing session boot API | `POST /api/harness/session/boot` endpoint exists and accepts requests (DEL-03-01 scope) | TBD | *(Lensing item F-002)* Confirm endpoint responds to a health check or basic request; DEL-03-01 status is INITIALIZED or later |
| Persona instruction files | At least one persona instruction file with YAML frontmatter exists for Tier 2 testing | TBD | *(Lensing item F-002)* Confirm at least one `.md` persona file with valid YAML frontmatter is present in the instruction root |
| SPEC.md Section 9.7-9.8 | Governing specification for opts fields, fallback chains, and UI contract | Available (`docs/SPEC.md`) | Available |
| CONTRACT.md | Binding invariants relevant to opts resolution (K-INVENT-1, K-GHOST-1) | Available (`docs/CONTRACT.md`) | Available |

**Gating note (Lensing item F-002):** Before beginning Step 1, verify all TBD prerequisites have met their readiness criteria. If any prerequisite cannot be satisfied, record the blocker in `_MEMORY.md` and coordinate with ORCHESTRATOR on dependency resolution.

## Steps

### Step 1: Audit Existing Opts Implementation

1. Locate the current runtime option mapping code in the harness codebase.
   - **ASSUMPTION:** Expected in `frontend/` directory, likely in files related to harness turn execution or session management.
2. Enumerate all `opts` fields currently supported by the runtime.
3. Document the current fallback behavior for each field (if any).
4. Identify gaps between the current implementation and SPEC.md Section 9.8 requirements.
5. Record findings in working memory (`_MEMORY.md`).

### Step 2: Implement/Verify Fallback Chain Resolution

1. For each documented `opts` field (model, tools, maxTurns):
   a. Verify or implement the three-tier fallback chain:
      - Tier 1: Turn-level `opts` value (if provided and non-null).
      - Tier 2: Persona-level default from YAML frontmatter (if active persona has the field).
      - Tier 3: Global/runtime default.
   b. Ensure resolution is deterministic (same inputs -> same outputs).
   c. Ensure omitted fields default correctly (no null/undefined leaking through).
2. For any additional `opts` fields discovered in Step 1:
   a. Verify or implement fallback chain logic following the same pattern.
   b. If a field does not follow the three-tier pattern, document the exception and rationale.
3. Ensure `opts.subagentGovernance` is passed through to the governance enforcement layer without being consumed by the standard fallback chain (DEL-03-04 owns enforcement).

### Step 3: Implement/Verify Persona Frontmatter Parsing

1. Verify that the runtime correctly parses YAML frontmatter from persona instruction files.
2. Confirm the following fields are extracted for Tier 2 resolution:
   - `tools`
   - `model`
   - `max_turns`
   - `disallowed_tools` (enforcement constraint, not fallback default -- verify behavior per REQ-11)
   - `auto_approve_tools` (enforcement constraint -- verify behavior per REQ-11)
3. Handle edge cases:
   - Persona file with no frontmatter (Tier 2 absent; fall through to Tier 3).
   - Persona file with partial frontmatter (only fields present are used).
   - Malformed frontmatter: *(Lensing item A-004)* Define explicit error handling behavior. Options include: (a) treat as "no frontmatter" and fall through to Tier 3 with a logged warning; (b) reject the persona and return an error to the caller; (c) attempt partial parse of well-formed fields. **Human ruling TBD.** Until resolved, implementers should log a warning and fall through to Tier 3 (fail-safe behavior consistent with the "warn and continue" direction proposed in Guidance T2). *(Source: Procedure.md Step 3 item 3; Guidance.md T2.)*

### Step 4: Implement/Verify Session Boot Opts Handling

1. Verify that `POST /api/harness/session/boot` accepts and resolves `opts` using the fallback chain.
2. Verify that bootstrap policy constraints are authoritative and not overridable by turn-level opts.
3. Document which constraints are bootstrap-only vs. per-turn overridable.

### Step 5: Implement/Verify UI Contract Compliance

1. Verify that the runtime does not inspect or depend on UI-side state to resolve opts.
2. Verify that omitted fields (fields not sent by the UI) fall through to defaults.
3. Verify that UI visibility has no effect on runtime authorization.

### Step 6: Write Tests

1. **Unit tests for fallback chain resolution:**
   - Test each documented field (model, tools, maxTurns) with:
     - Only Tier 1 provided.
     - Only Tier 2 available (persona defaults).
     - Only Tier 3 available (global/runtime defaults).
     - All tiers available (Tier 1 wins).
     - No tiers available (verify defined default or explicit error -- must confirm K-INVENT-1 compliance per REQ-10).
   - Test with partial opts (some fields provided, others omitted).
2. **Persona frontmatter parsing tests:**
   - Parse valid frontmatter with all fields.
   - Parse partial frontmatter.
   - Parse absent frontmatter.
   - Parse malformed frontmatter (error handling per Step 3 ruling).
3. **Integration tests:**
   - Submit a turn with explicit opts; verify resolved parameters.
   - Submit a turn with no opts; verify defaults applied.
   - Boot a session with opts; verify bootstrap constraints.
4. **Determinism test:**
   - Run the same resolution N times; verify identical outputs. *(Lensing item F-003: define concrete N -- TBD, recommend minimum 100 iterations; failure = any non-identical output.)*
5. **Edge-case tests:**
   - Unknown opts field (verify warn-and-continue or documented behavior).
   - Null/undefined opts values vs. absent opts keys.
6. **K-GHOST-1 compliance test (Lensing item A-003):**
   - Verify that opts resolution inputs are traceable exclusively to declared sources (turn-level opts, persona frontmatter, global config). Confirm no undeclared/invisible context sources influence the resolved values.

### Step 7: Write Documentation

1. Document all supported `opts` fields and their fallback chains in a developer-facing reference.
2. Document the distinction between fallback defaults (Tier 2) and enforcement constraints (e.g., `disallowed_tools`) per REQ-11.
3. Document bootstrap-only vs. per-turn overridable constraints.
4. Document extension points for adding new opts fields.
5. Document the naming convention translation between persona frontmatter (snake_case) and opts object (camelCase) per Guidance P5.

### Step 8: Cross-Deliverable Verification

*(Lensing item X-001)* For each cross-deliverable check below, define the verification method, tool/evidence, and pass criteria. Until concrete methods are defined, these checks are directional reminders rather than executable verification steps.

1. Verify that the opts mapping does not break subagent governance enforcement (DEL-03-04 scope).
   - **Method:** TBD -- e.g., integration test submitting opts with `subagentGovernance` field; confirm governance enforcement still triggers correctly.
   - **Evidence:** Test results or manual confirmation from DEL-03-04 implementer.
2. Verify that the opts mapping does not interfere with attachment handling (DEL-04-01 scope).
   - **Method:** TBD -- e.g., integration test submitting a turn with both opts and attachment; confirm attachment resolution is unaffected.
   - **Evidence:** Test results or manual confirmation from DEL-04-01 implementer.
3. Verify that the Operator Toolkit panel (DEL-02-03) can submit opts and receive correct resolution.
   - **Method:** TBD -- e.g., end-to-end test from toolkit panel UI through to resolved parameters; confirm round-trip correctness.
   - **Evidence:** Test results or manual confirmation from DEL-02-03 implementer.

## Verification

| Check | Method | Pass Criteria |
|-------|--------|---------------|
| All documented fallback chains work | Unit tests (Step 6.1) | All tests pass; each tier resolves correctly |
| Persona frontmatter parsed correctly | Unit tests (Step 6.2) | All fields extracted; edge cases handled |
| Turn API accepts and resolves opts | Integration test (Step 6.3) | Resolved parameters match expected values |
| Session boot respects bootstrap policy | Integration test (Step 6.3) | Bootstrap constraints not overridden |
| Resolution is deterministic | Determinism test (Step 6.4) | Identical outputs across N runs (N TBD, recommend >= 100) |
| UI contract compliance | Code review + test (Step 5) | No UI-state dependency in runtime resolution |
| K-INVENT-1 compliance | Edge-case test (Step 6.1, no-tier case) | No invented values; defined default or explicit error |
| K-GHOST-1 compliance | Code review + test (Step 6.6) | All resolution inputs traceable to declared sources |
| Documentation complete | Review | All supported fields, chains, and extension points documented |

## Records

| Record | Description | Location |
|--------|-------------|----------|
| Test results | Unit and integration test output | TBD *(Lensing item X-002: define location per project conventions -- expected in `frontend/` test infrastructure, e.g., `frontend/test-results/` or CI output)* |
| Code review record | Review of opts mapper implementation | TBD *(Lensing item X-002: define location -- expected as PR review comments or a dedicated review document)* |
| Developer documentation | Supported opts fields, fallback chains, extension points | TBD *(Lensing item X-002: expected in `frontend/docs/` or inline code documentation)* |
| Working memory notes | Audit findings, decisions, open items | `_MEMORY.md` in this deliverable folder |
