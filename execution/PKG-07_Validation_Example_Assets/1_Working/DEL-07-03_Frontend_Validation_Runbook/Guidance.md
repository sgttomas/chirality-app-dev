# Guidance -- DEL-07-03 Frontend Validation & Runbook Baseline

## Purpose

This deliverable exists because Scope Amendment A1 (SCA-001) recognized that the `frontend/` runtime surface and its validation tooling cannot be treated as pre-existing. Prior execution assumptions relied on `frontend/scripts/validate-harness-*.mjs` being available, but the local-only execution policy requires these scripts and their documentation to be developed and validated from this repository state.

DEL-07-03 directly supports two objectives:
- **OBJ-006:** "Validation posture and governance/agent-suite conformance enable repeatable operation." The validation scripts and runbooks produced here are the mechanism by which harness runtime correctness is evidenced.
- **OBJ-008:** "Local frontend runtime baseline exists and is executable from this repository only." The deliverable ensures that validation artifacts are produced locally with no non-local dependencies.

This deliverable also occupies a **pre-tier gate position**: Tier 2 code-bearing work that depends on frontend paths (including DEL-01-01, DEL-03-01, DEL-05-03, DEL-05-04) remains blocked until DEL-07-03 reaches at least `IN_PROGRESS` per the blocker maturity policy defined in SCA-001.

**Source:** Decomposition SCA-001; SOW-048; SOW-049; OBJ-006; OBJ-008; Execution Gating Rule

## Principles

### P1: Deterministic Outputs Over Rich Diagnostics

The default validation posture prioritizes deterministic, minimal outputs (`summary.json`) over comprehensive artifact collection. This keeps pre-merge gates lightweight and predictable. Full artifact mirroring is available for diagnostics but is opt-in.

**Source:** `docs/harness/harness_artifact_mirroring_guidance.md` Perspective ("summary.json-first"); Recommended Operating Model

### P2: Local-Only Boundary is Non-Negotiable

Validation scripts and runbooks must execute entirely from this repository. The local-only boundary is not a convenience preference; it is a structural constraint derived from DEC-NET-001 (Anthropic-only outbound) and the "filesystem is the state" principle. Scripts must not fetch fixtures from external URLs, reference non-local repos, or assume availability of external infrastructure beyond the Anthropic API.

**Source:** `docs/harness/harness_manual_validation.md` Local-Only Boundary; `docs/harness/harness_ci_integration.md` Local-Only Boundary; `docs/harness/harness_artifact_mirroring_guidance.md` Local-Only Boundary; DIRECTIVE Section 2.1

### P3: Scripts as the Source of Truth for Validation

The validation scripts (`validate-harness-section8.mjs`, `validate-harness-premerge.mjs`) are the authoritative definition of what constitutes a passing harness validation. The runbook documentation describes how to use them, but the scripts themselves define the test matrix, pass criteria, and output format. Documentation that contradicts script behavior should be treated as stale documentation, not a script bug (unless the script violates a Specification requirement).

**Source:** `docs/harness/harness_manual_validation.md` (scripts as primary reference); **ASSUMPTION** -- standard practice that executable tests are authoritative over documentation

### P4: CI is a Verification Gate, Not the Primary Workflow

The CI workflow (`.github/workflows/harness-premerge.yml`) is a gate that catches regressions before merge. The primary developer workflow is local execution. Runbook documentation should orient the developer toward local validation first, with CI as a safety net.

**Source:** `docs/harness/harness_ci_integration.md` (CI as gate); `docs/harness/harness_manual_validation.md` (local validation primary)

### P5: Fail-Fast on Missing Runtime Surface

If the `frontend/` directory or validation scripts do not exist in the workspace, the correct response is to stop and record `RUNTIME_SURFACE_MISSING` rather than proceeding with degraded validation. This prevents false-positive validation results from an incomplete workspace.

**Source:** `docs/harness/harness_manual_validation.md` Local-Only Boundary

### P6: Consistent Pass/Fail Vocabulary

All production documents and validation artifacts use the canonical pass/fail vocabulary defined in Specification REQ-08: lowercase `pass` and `fail` as string values, with exit code 0 corresponding to `pass` and non-zero corresponding to `fail`. Implementers and documentation authors should use this vocabulary consistently rather than synonyms (e.g., "success"/"failure", "PASS"/"FAIL", "all-pass") to prevent ambiguity in automation parsing and human interpretation.

**Source:** `docs/harness/harness_manual_validation.md` Machine-Readable Outputs; `docs/harness/harness_ci_integration.md` Failure Expectations; Lensing Item X-003

## Considerations

### C1: Relationship to DEL-07-01 (Harness Validation Suite)

DEL-07-01 (Harness Validation Suite) covers the broader harness contract validation (opts fallback chains, subagent governance, attachment resolver) as specified in `docs/SPEC.md` Sections 9.7-9.8. DEL-07-03 covers the Section 8 SDK-native test matrix and pre-merge wrapper as specified in `docs/harness/harness_manual_validation.md`.

The two deliverables are complementary:
- DEL-07-01 targets the full harness API contract surface
- DEL-07-03 targets the frontend-facing validation posture (Section 8 matrix + pre-merge workflow + runbooks)

There is intentional overlap at `setup.server_reachable` and `regression.session_crud` which appear in both deliverables' scope. The DEL-07-03 implementations of these checks serve as preflight/regression guards for the Section 8 matrix; DEL-07-01's coverage extends to deeper behavioral contract validation.

**Source:** Decomposition DEL-07-01 vs. DEL-07-03; `docs/harness/harness_manual_validation.md`

### C2: Pre-Tier Gate Implications

This deliverable blocks Tier 2 work. The implication is that DEL-07-03 should be scoped tightly to the minimum needed to unblock downstream work -- the Section 8 matrix, pre-merge wrapper, deterministic summary artifact, and runbook documentation. Expanding scope to cover additional validation areas risks delaying the Tier 2 gate without proportional benefit. Additional validation coverage belongs in DEL-07-01 (Harness Validation Suite).

The specific acceptance criteria for when the pre-tier gate is considered satisfied are TBD at the requirement level (see Specification Pre-Tier Gate Acceptance Criteria section and Lensing Item F-001). Gate reviewers should be aware that the gate passage definition currently relies on status maturity (`IN_PROGRESS`) rather than a requirement-level pass/fail threshold.

**Source:** Decomposition SCA-001 Execution Gating Rule; Lensing Item F-001

### C3: Anthropic API Key Dependency

Live validation (as opposed to structural validation of scripts and artifacts) requires a running harness server and an Anthropic API key. The key provisioning contract is unresolved (OI-001). Runbook documentation should clearly document this dependency and distinguish between:
- **Structural validation:** scripts exist, npm targets resolve, artifact paths are correct (no API key needed)
- **Live validation:** scripts execute against a running harness and produce `pass`/`fail` results (API key required)

This distinction is also relevant to Specification REQ-05 verification, which specifies live validation but where structural validation is a necessary-but-not-sufficient subset. See Specification REQ-05 verification note.

**Source:** `docs/harness/harness_manual_validation.md` Prerequisites; Decomposition OI-001; Lensing Item A-003

### C4: Summary Schema Evolution

The pre-merge wrapper validates the summary schema (required SDK test IDs present, legacy IDs absent). As the Section 8 matrix evolves, the set of required test IDs will change. Runbook documentation should note that the schema validation list is maintained in the pre-merge wrapper script, and changes to the Section 8 matrix require corresponding updates to the schema validation.

**Schema update process and ownership:** When the Section 8 matrix is modified (adding, removing, or renaming behavioral checks), the following artifacts require corresponding updates:

1. **Pre-merge wrapper script** (`validate-harness-premerge.mjs`): Update the required SDK test ID list.
2. **Section 8 validation script** (`validate-harness-section8.mjs`): Update test implementations.
3. **Specification REQ-06 table**: Update test ID rows.
4. **Runbook documentation**: Update Section 8 matrix descriptions.
5. **`HARNESS_PREMERGE_TEST_COUNT`**: The emitted count will change automatically if the count reflects tests actually executed (see Specification REQ-08 semantics).

**Ownership:** TBD -- the owner of the schema update process is not defined. **ASSUMPTION:** The owner is whoever modifies the Section 8 matrix in `docs/harness/harness_manual_validation.md`, and the corresponding script updates are part of the same change. However, if matrix ownership and script ownership are split across deliverables (DEL-07-01 vs. DEL-07-03), a coordination mechanism is needed. See Lensing Item F-003.

**Source:** `docs/harness/harness_ci_integration.md` Job Flow step 7; Lensing Item F-003

### C5: Existing Documentation as Starting Point

Three existing harness documentation files provide substantial content that this deliverable's runbooks should build on rather than duplicate:
- `docs/harness/harness_manual_validation.md` -- local validation procedure
- `docs/harness/harness_ci_integration.md` -- CI workflow
- `docs/harness/harness_artifact_mirroring_guidance.md` -- mirroring posture

The runbook documentation (SOW-049) should reference or incorporate these existing docs. Whether the deliverable consolidates them into a single runbook or supplements them with additional documentation is a design choice. **ASSUMPTION (best-effort mapping):** The existing `docs/harness/` files are the primary content source for the runbook artifacts; the deliverable's DOC artifacts may be updates/enhancements to these files rather than entirely new documents.

**Source:** `_REFERENCES.md`; `docs/harness/` files

### C6: Node.js Version Constraint

No governance document specifies a minimum Node.js version. The validation scripts use `.mjs` (ES modules), which requires Node.js 12+ for basic support and 14+ for stable ESM. The actual minimum depends on the Electron + Next.js stack version pinned by DEL-01-03. Runbook documentation should note this dependency but cannot specify a version until DEL-01-03 establishes the frontend workspace baseline.

**Source:** **ASSUMPTION** -- Node.js ESM requirements; Decomposition DEL-01-03

### C7: Artifact Retention and Sensitivity

`docs/harness/harness_artifact_mirroring_guidance.md` notes that mirrored artifacts should be treated as "potentially sensitive operational data" and that secrets redaction guarantees must remain intact. Runbook documentation should relay these guardrails. The `summary.json` default posture avoids most sensitivity concerns, but full mirroring exposes SSE traces, API responses, and log files that may contain operational context.

**Source:** `docs/harness/harness_artifact_mirroring_guidance.md` Guardrails

### C8: Documentation Placement and REQ-12/REQ-13 Artifact Paths

SOW-049 directs documentation to "repository docs (`docs/` and deliverable-local artifacts)" but does not specify authoritative file paths for the REQ-12 (runbook) and REQ-13 (architecture) documentation artifacts. This ambiguity means downstream implementers cannot determine the correct output locations without a human ruling.

The Guidance T1 trade-off analysis recommends updating existing `docs/harness/` files in-place and producing a lightweight index. If this PROPOSAL is accepted, the REQ-12 artifact maps primarily to updates in `docs/harness/harness_manual_validation.md` and the REQ-13 artifact maps primarily to updates in `docs/harness/harness_ci_integration.md` and `docs/harness/harness_artifact_mirroring_guidance.md`. The index document location is also TBD (see CT-002).

**Source:** SOW-049; `_CONTEXT.md`; Guidance T1; Lensing Item A-001

## Trade-offs

### T1: Consolidate vs. Supplement Existing Harness Docs

| Option | Pros | Cons |
|--------|------|------|
| Consolidate existing `docs/harness/` into one runbook | Single source of truth; easier for new developers | Requires rewriting/merging three existing documents; risks losing nuance |
| Supplement with deliverable-local docs that reference existing | Preserves existing docs; lower effort; reduces duplication | Developers must follow references across multiple files |
| Update existing docs in-place and add a lightweight index | Existing docs stay authoritative; index provides entry point | Index adds one more file to maintain |

**Recommendation (PROPOSAL):** Update existing `docs/harness/` documents in-place where they need enhancement (e.g., adding prerequisites detail, clarifying Section 8 matrix), and produce a lightweight index/entry-point document that serves as the runbook "table of contents." This respects the existing documentation investment while fulfilling SOW-049.

**Rationale for the runbook index document (Procedure Step 5.7):** The index document exists to solve a specific developer-experience problem: the three `docs/harness/` files (`harness_manual_validation.md`, `harness_ci_integration.md`, `harness_artifact_mirroring_guidance.md`) each cover a distinct concern but there is no single entry point that orients a new developer to which file addresses which question. The index provides this orientation without duplicating content. If the human does not approve this PROPOSAL (see CT-002), Procedure Step 5.7 should be skipped and the three existing files should serve as the runbook artifacts directly. See Lensing Item D-002.

**Source:** `_REFERENCES.md`; `docs/harness/` files; SOW-049; Lensing Item D-002

### T2: Summary-Only vs. Full Artifact Default in CI

| Option | Pros | Cons |
|--------|------|------|
| Summary-only default | Fast, lightweight, deterministic, minimal storage | Less diagnostic data on failure |
| Full artifact default | More diagnostic data always available | Larger uploads, more storage, potential sensitivity exposure |
| Summary default + full on failure | Best of both; full data when needed | More complex CI workflow logic |

**Recommendation:** The existing guidance (`docs/harness/harness_artifact_mirroring_guidance.md`) recommends summary-only default. This deliverable should follow that recommendation.

**Source:** `docs/harness/harness_artifact_mirroring_guidance.md` Recommended Operating Model

### T3: DEL-07-03 Scope Boundary Relative to DEL-07-01

The Section 8 matrix and pre-merge wrapper are defined in the existing `docs/harness/` files and are the natural scope of DEL-07-03. Expanding to cover the full SPEC Section 9.7-9.8 contract (opts, subagent governance, attachments) would overlap with DEL-07-01 (Harness Validation Suite). The recommended boundary is: DEL-07-03 owns the Section 8 matrix + pre-merge wrapper + runbooks; DEL-07-01 owns the broader harness contract test suite.

**Source:** Decomposition DEL-07-01 vs. DEL-07-03

## Examples

### Example: Local Validation Run Sequence

The canonical local pre-merge sequence from `docs/harness/harness_manual_validation.md`:

```
1. Start frontend server:
   cd frontend
   npm run dev -- --hostname 127.0.0.1 --port 3000

2. In a second shell, run pre-merge validation:
   cd frontend
   npm run harness:validate:premerge

3. Read stable summary:
   cat frontend/artifacts/harness/section8/latest/summary.json
```

Expected machine-readable output on stdout (using canonical `pass`/`fail` vocabulary per Specification REQ-08):
```
HARNESS_PREMERGE_ARTIFACT_PATH=frontend/artifacts/harness/section8/latest/summary.json
HARNESS_PREMERGE_SOURCE_SUMMARY_PATH=/tmp/chirality-harness-validation/latest/summary.json
HARNESS_PREMERGE_STATUS=pass
HARNESS_PREMERGE_TEST_COUNT=7
```

**Note on `HARNESS_PREMERGE_TEST_COUNT=7`:** This reflects the current composition of 5 Section 8 checks + 2 regression checks. This count is informational and will change if the test matrix evolves (see Specification REQ-08 semantics and Guidance C4).

**Source:** `docs/harness/harness_manual_validation.md` Usage; Machine-Readable Outputs

### Example: CI Job Flow

From `docs/harness/harness_ci_integration.md`:

```
1. Checkout repository
2. Setup Node.js
3. cd frontend && npm ci
4. Start frontend server
5. Poll readiness at /api/harness/session/list?projectRoot=...
6. npm run harness:validate:premerge
7. Wrapper validates summary schema (required IDs present, legacy absent)
8. Verify summary at frontend/artifacts/harness/section8/latest/summary.json
9. Upload summary artifact
```

Failure modes: wrapper exits non-zero (all tests fail), missing stable summary (artifact copy failure), invalid summary shape (schema validation failure).

**Source:** `docs/harness/harness_ci_integration.md` Job Flow; Failure Expectations

## Conflict Table (for human ruling)

| Conflict ID | Conflict | Source A | Source B | Impacted Sections | Proposed Authority | Human Ruling |
|-------------|----------|----------|----------|--------------------|--------------------|--------------|
| CT-001 | Node.js version requirement: no source specifies a minimum version for `.mjs` script execution; tests may fail on incompatible versions | Datasheet Conditions (Node.js version TBD) | DEL-01-03 (Frontend Workspace Bootstrap -- will pin stack versions) | Specification REQ-05; Procedure Prerequisites; Datasheet Conditions | DEL-01-03 should establish the version; this deliverable inherits it | TBD |
| CT-002 | Documentation placement: SOW-049 says "repository docs (`docs/` and deliverable-local artifacts)" but does not specify exact file paths or whether to update existing `docs/harness/` files vs. create new ones | SOW-049 (`_CONTEXT.md`) | Existing `docs/harness/` file locations | Specification REQ-12, REQ-13; Procedure Phase 5; Guidance C8 | Update existing `docs/harness/` in-place + lightweight index (PROPOSAL; see T1) | TBD |
| CT-003 | Schema evolution ownership: when the Section 8 matrix changes, the pre-merge wrapper's required test ID list and related documentation must be updated, but the owner of this update process is undefined; coordination mechanism between DEL-07-01 and DEL-07-03 may be needed if matrix ownership is split | Guidance C4 (schema evolution described) | Decomposition (DEL-07-01 vs DEL-07-03 scope boundary) | Specification REQ-15; Procedure Phase 3 Step 3.3; Guidance C4 | Owner is whoever modifies the Section 8 matrix (PROPOSAL; see C4) | TBD |
