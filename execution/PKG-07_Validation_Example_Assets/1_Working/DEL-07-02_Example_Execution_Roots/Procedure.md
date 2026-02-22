# Procedure — DEL-07-02: Example Execution Roots + Conformance Fixtures

---

## Purpose

This procedure defines the steps to create, validate, and maintain the example execution root directory structures under `examples/` that serve as regression and conformance test fixtures for the Chirality system.

---

## Prerequisites

| # | Prerequisite | Status |
|---|-------------|--------|
| 1 | `docs/SPEC.md` is available and current (defines canonical execution root layout, deliverable folder layout, file schemas, and validation checklist) | Available (Source: SPEC.md) |
| 2 | `docs/TYPES.md` is available and current (defines stable ID formats, lifecycle states, canonical vocabulary) | Available (Source: TYPES.md) |
| 3 | `docs/CONTRACT.md` is available and current (defines binding invariants) | Available (Source: CONTRACT.md) |
| 4 | `docs/DIRECTIVE.md` is available and current (defines filesystem-as-state principles) | Available (Source: DIRECTIVE.md) |
| 5 | Decision on number and scope of example execution roots | Resolved — human ruling (2026-02-22): one baseline execution root at `examples/example-project/` |
| 6 | Decision on whether to include `Dependencies.csv` samples | Resolved — human ruling (2026-02-22): OUT for current baseline scope |

---

## Steps

### Phase 1: Planning and Structure Design

**Step 1.1 — Define example inventory**

Determine the number and purpose of example execution roots.

Applied ruling (2026-02-22):

- One primary example execution root demonstrating the full canonical layout (`examples/example-project/`).
- Within that root: 3 deliverables at different lifecycle states (OPEN, INITIALIZED, SEMANTIC_READY).

Artifact: Inventory list (may be captured in `_MEMORY.md`).

**Step 1.2 — Design ID scheme for examples**

Assign synthetic `PKG-XX` and `DEL-XX-YY` IDs for the example content. These are internal to the example and do not collide with the real project's ID space.

Source: TYPES.md Section 2 (stable ID formats).

### Phase 2: Execution Root Scaffolding

**Step 2.1 — Create example root directory**

Create the example execution root directory under `examples/` at the repo root:

```
examples/{example-root-name}/
```

Source: PLAN.md Section 2; SOW-029.

**Step 2.2 — Create INIT.md**

Create `INIT.md` at the example root with synthetic session initialization parameters.

Source: SPEC.md Section 1 (execution root layout); SPEC.md Section 12.1.

**Step 2.3 — Create _Decomposition/ directory**

Create `_Decomposition/` at the example root and populate with a synthetic decomposition document that defines the example packages and deliverables.

Source: SPEC.md Section 1.2; SPEC.md Section 12.1.

**Step 2.4 — Create tool root directories (as needed)**

Create tool root directories per SPEC.md Section 1.2. At minimum, include `_Decomposition/`. Other tool roots may be created as empty directories to demonstrate the layout.

Source: SPEC.md Section 1.2.

### Phase 3: Package and Deliverable Population

**Step 3.1 — Create package folders**

For each example package, create the folder structure per SPEC.md Section 1.1:

```
PKG-XX_{SanitizedLabel}/
  0_References/
    _Archive/
  1_Working/
    _Archive/
  2_Checking/
    From/
    To/
  3_Issued/
    _Archive/
```

Source: SPEC.md Section 1.1; SPEC.md Section 12.2.

**Step 3.2 — Create deliverable folders (OPEN state)**

For each example deliverable at OPEN state, create the minimum viable fileset:

```
DEL-XX-YY_{SanitizedLabel}/
  _STATUS.md      (Current State: OPEN)
  _CONTEXT.md     (fields matching example decomposition)
  _DEPENDENCIES.md
  _REFERENCES.md
```

Ensure internal consistency: folder name ID matches `_CONTEXT.md` deliverable ID matches `_STATUS.md` heading.

Source: SPEC.md Section 2.1; SPEC.md Section 12.3.

**Step 3.3 — Create deliverable folders (INITIALIZED state)**

For each example deliverable at INITIALIZED state, create the minimum viable fileset plus the document kit:

```
DEL-XX-YY_{SanitizedLabel}/
  _STATUS.md        (Current State: INITIALIZED)
  _CONTEXT.md
  _DEPENDENCIES.md
  _REFERENCES.md
  Datasheet.md
  Specification.md
  Guidance.md
  Procedure.md
```

Source: SPEC.md Section 2.1; SPEC.md Section 12.3 (initialized deliverable validation).

**Step 3.4 — Create deliverable folders with semantic artifacts (optional)**

For each example deliverable demonstrating semantic analysis, add:

```
  _SEMANTIC.md      (semantic lens artifact sample)
```

Update `_STATUS.md` to `SEMANTIC_READY` if this is the highest state demonstrated.

Source: PLAN.md Section 2; SPEC.md Section 2.1.

### Phase 4: Content Population

**Step 4.1 — Populate _STATUS.md files**

Each `_STATUS.md` MUST follow the format in SPEC.md Section 3.1:

- Valid `Current State` from canonical lifecycle.
- `Last Updated` date.
- `History` section with at least one entry.

Source: SPEC.md Section 3.1.

**Step 4.2 — Populate _CONTEXT.md files**

Each `_CONTEXT.md` MUST follow the format in SPEC.md Section 4.1:

- Header fields matching the example decomposition document.
- Decomposition reference pointing to the example's `_Decomposition/` document.

Source: SPEC.md Section 4.1.

**Step 4.3 — Populate document kit files (where applicable)**

For INITIALIZED deliverables, populate `Datasheet.md`, `Specification.md`, `Guidance.md`, `Procedure.md` with minimal synthetic content demonstrating the default section schemas:

- Datasheet: Identification, Attributes, Conditions, Construction, References
- Specification: Scope, Requirements, Standards, Verification, Documentation
- Guidance: Purpose, Principles, Considerations, Trade-offs, Examples
- Procedure: Purpose, Prerequisites, Steps, Verification, Records

Source: TYPES.md Section 7; SPEC.md Section 2.1.

**Step 4.4 — Populate _SEMANTIC.md (where applicable)**

For deliverables demonstrating the semantic lens artifact (per REQ-07), create a `_SEMANTIC.md` file containing at minimum:

- Matrix A (Orientation, 3x4) -- canonical matrix with deliverable-specific perspective statement.
- Matrix B (Conceptualization, 4x4) -- canonical matrix.
- A clear identification header (deliverable name, generated date, framework name).

**Rationale for deferral:** The full `_SEMANTIC.md` format (including derived matrices C, F, D, K, X, E) does not yet have a formally published schema specification. The minimum viable sample (Matrices A and B plus identification) demonstrates the artifact type without requiring commitment to an evolving derivation format. This aligns with REQ-07's SHOULD modality and the rationale documented in Guidance. (See Lensing Item A-003.)

**Note:** If a formal `_SEMANTIC.md` schema specification is published before this step is executed, update this step to reference that specification.

Source: REQ-07 acceptance criteria (Specification.md); observed `_SEMANTIC.md` structure (**location TBD** -- formal schema).

### Phase 5: SPEC Ambiguity Escalation (error handling)

**Step 5.1 — Detect construction failures**

During any phase of example construction, if the executor encounters a situation where:

- A SPEC-conformant example cannot be constructed without ambiguity, OR
- The SPEC requirements appear contradictory, OR
- A required structural element is not defined with sufficient precision in SPEC.md

then the executor MUST halt construction of the affected element and proceed to Step 5.2.

Source: Guidance P1 ("If an example cannot be constructed without deviating from SPEC, that is a signal the SPEC may need revision").

**Step 5.2 — Document the ambiguity**

Record the ambiguity in this deliverable's `_MEMORY.md` with:

- Description of the construction step that failed or is ambiguous.
- The specific SPEC section(s) involved.
- The proposed interpretation (if any).
- Classification: `SPEC_AMBIGUITY`, `SPEC_CONTRADICTION`, or `SPEC_UNDERSPECIFICATION`.

**Step 5.3 — Escalate for resolution**

Escalate the documented ambiguity to the responsible party for DEL-06-05 (Governance Coherence) or to the human for ruling. Do not proceed with a non-conformant example.

Source: Lensing Item C-002; Guidance P1.

### Phase 6: Dependencies Artifacts (conditional)

**Step 6.1 — Create Dependencies.csv (if decided)**

If human ruling includes `Dependencies.csv` samples, create them following the v3.1 schema defined in SPEC.md Section 6.

Current ruling (2026-02-22): `Dependencies.csv` samples are OUT for baseline scope, so no Phase 6 artifact creation is required in this pass. Re-open this step only if scope expands (for example DEL-08-02 ruled IN).

### Phase 7: Maintenance (ongoing)

**Step 7.1 — Monitor SPEC changes**

When `docs/SPEC.md` is updated (new required files, renamed folders, schema updates), assess the impact on existing example execution roots.

**Step 7.2 — Update examples for conformance**

For each change that affects example structure or content:

1. Identify all affected files/folders in the example execution root(s).
2. Update the affected elements to match the new SPEC requirements.
3. Re-run the verification checks (Verification section) to confirm continued conformance.
4. Record the update in `_MEMORY.md` and/or git commit history.

**Step 7.3 — Coordinate with DEL-07-01**

Notify DEL-07-01 maintainers of structural changes so validation scripts can be updated if needed. Validation scripts from DEL-07-01 serve as a drift-detection mechanism between SPEC and examples (see Guidance C3).

Source: Guidance C3 (maintenance burden); Lensing Item F-003.

### Phase 8: Acceptance Gate

**Step 8.1 — Pre-acceptance checklist**

Before advancing the deliverable beyond IN_PROGRESS, verify that all of the following are satisfied:

- [ ] All verification checks in Phase 9 pass.
- [ ] All TBD items in Prerequisites have been resolved (human rulings recorded in `_MEMORY.md`).
- [ ] No unresolved SPEC ambiguity escalations remain open (Phase 5).
- [ ] At least one example deliverable demonstrates each lifecycle state specified in Guidance P5 (OPEN, INITIALIZED, and a `_SEMANTIC.md`-bearing state).
- [ ] If `Dependencies.csv` inclusion was decided IN, Phase 6 is complete.

**Step 8.2 — Request state transition**

Upon passing the pre-acceptance checklist, request state transition from the responsible party or ORCHESTRATOR. The target state is `CHECKING` (for review) or `ISSUED` (if review is waived).

Source: SPEC.md Section 3 (lifecycle transitions); Lensing Item E-002.

---

## Verification

| # | Check | Method | Pass Criteria |
|---|-------|--------|---------------|
| 1 | Execution root layout conformance | Inspect against SPEC.md Section 12.1 checklist | All checklist items pass |
| 2 | Package folder conformance | Inspect against SPEC.md Section 12.2 checklist | All required subfolders present |
| 3 | Deliverable folder conformance | Inspect against SPEC.md Section 12.3 checklist | All required files present per lifecycle state |
| 4 | Filesystem-safe naming | Regex validation of all folder names | All names match `{ID}_{SanitizedLabel}` pattern |
| 5 | Lifecycle state validity | Parse all `_STATUS.md` files | All states are in canonical lifecycle enum ({OPEN, INITIALIZED, SEMANTIC_READY, IN_PROGRESS, CHECKING, ISSUED}) |
| 6 | Internal consistency | Cross-check IDs across folder names, `_CONTEXT.md`, `_STATUS.md`, decomposition | No mismatches |
| 7 | No real data | Manual review of all content | All content is synthetic/placeholder |
| 8 | Self-contained | Run DEL-07-01 validation scripts without network access | Scripts exit with status 0; no manual intervention required |
| 9 | Semantic artifact present | Check for `_SEMANTIC.md` in at least one deliverable | File exists, contains Matrix A and Matrix B tables, and parses as valid Markdown (see REQ-07 acceptance criteria in Specification.md) |

---

## Records

| Record | Location | Purpose |
|--------|----------|---------|
| Example execution root(s) | `examples/` at repo root | Primary deliverable output |
| Verification results | TBD — may be captured in DEL-07-01 validation run logs or in this deliverable's `_MEMORY.md`; decision requires coordination with DEL-07-01 maintainers (see Lensing Item D-002) |  Evidence that examples pass conformance checks |
| Update log | `_MEMORY.md` and/or git history | Track changes to examples over time |
| Human rulings | `_MEMORY.md` | Decisions on example count, Dependencies.csv inclusion, and other TBD items |
| SPEC ambiguity escalations | `_MEMORY.md` | Documented construction failures and their resolutions (Phase 5) |
