# Guidance — DEL-07-02: Example Execution Roots + Conformance Fixtures

---

## Purpose

This deliverable exists to provide concrete, SPEC-conformant example execution root directory structures that serve as regression and conformance test fixtures for the Chirality system.

The examples serve three functions:

1. **Regression baseline**: Validation scripts (DEL-07-01) and future automated validators (DEL-08-03, TBD scope) can run against these fixtures to verify that tooling correctly parses and validates SPEC-conformant structures.
2. **Conformance reference**: Developers and operators can inspect the examples to understand the expected physical layout of an execution root without reading the full SPEC.
3. **Semantic artifact samples**: By including `_SEMANTIC.md` and potentially other pipeline artifacts, the examples demonstrate the full deliverable lifecycle, not just the initial scaffolding.

Source: SOW-029 (Decomposition G7-APPROVED); PLAN.md Section 2; OBJ-006.

---

## Principles

### P1: Examples Are Specification Projections

Each example execution root is a physical projection of the structures defined in `docs/SPEC.md`. The examples do not invent new conventions; they instantiate the existing specification with synthetic content.

If an example cannot be constructed without deviating from SPEC, that is a signal the SPEC may need revision -- not that the example should silently diverge. In this case, the executor should follow the error-handling procedure in Procedure Phase 5 (SPEC Ambiguity Escalation) rather than proceeding with a non-conformant example.

Source: SPEC.md (authoritative specification); DIRECTIVE.md Section 2.1.

### P2: Minimal but Complete

Examples should contain the minimum content necessary to demonstrate conformance, but MUST NOT omit required structural elements. A "minimal complete" example is preferable to a "realistic but heavyweight" one, because it reduces maintenance burden and makes structural requirements more visible.

**ASSUMPTION:** This principle is an interpretation of the PLAN.md description ("concrete execution-root samples") balanced against maintainability.

### P3: Synthetic Data Only

All content in examples MUST be synthetic or placeholder. No real project names, proprietary information, or credentials. This enables safe inclusion in version control and potential open-source distribution.

**ASSUMPTION:** Standard practice for test fixtures.

### P4: Stable IDs Within Examples

Example IDs (e.g., `PKG-01`, `DEL-01-01` within the example) are internal to the example and do not need to correspond to the real project's ID space. However, they MUST follow the canonical ID formats defined in `docs/TYPES.md` Section 2.

Source: TYPES.md Section 2 (stable identifier formats).

### P5: Lifecycle Diversity

To be useful for regression testing, the example set should demonstrate multiple lifecycle states and file-presence combinations. At minimum:

- One deliverable at `OPEN` state (minimum viable fileset only).
- One deliverable at `INITIALIZED` state (minimum viable fileset + document kit).
- One deliverable demonstrating a `_SEMANTIC.md` artifact (**ASSUMPTION:** at `SEMANTIC_READY` or later state).

Source: SPEC.md Section 3.2; PLAN.md Section 2.

---

## Considerations

### C1: Relationship to DEL-07-01 (Harness Validation Suite)

DEL-07-01 provides the validation scripts and CI posture; DEL-07-02 provides the test fixtures those scripts run against. The two deliverables are complementary:

- DEL-07-01 consumes DEL-07-02 outputs as test inputs.
- Changes to SPEC that affect folder layout should be reflected in both deliverables.

**ASSUMPTION:** DEL-07-01 is an upstream consumer of DEL-07-02 fixtures. Dependency extraction has not yet been run.

### C2: Relationship to DEL-08-03 (Execution Root Folder Structure Validator)

If DEL-08-03 (TBD scope) is brought IN, its validator should be runnable against the examples from this deliverable. The examples should therefore be structured as known-good inputs for validation tooling.

Source: PLAN.md Section 3.3; Decomposition (DEL-08-03).

### C3: Maintenance Burden

Example execution roots are living artifacts. When `docs/SPEC.md` changes (new required files, renamed folders, schema updates), the examples must be updated to remain conformant. Consider:

- Keeping the number of example roots small (1-2) to limit maintenance surface.
- Documenting update procedures (see Procedure.md Phase 7: Maintenance).
- Ensuring validation scripts from DEL-07-01 catch drift between SPEC and examples.

**Rationale for the 1-2 range:** A single example root with 2-3 deliverables at different lifecycle states covers the minimum regression needs identified by P5 (Lifecycle Diversity) while keeping the maintenance surface bounded. Each additional example root multiplies the update cost when SPEC changes, because every root must be independently brought into conformance. Given that DEL-07-01 validation scripts provide the primary regression coverage, the example roots need only supply known-good fixtures rather than exhaustive scenario coverage. If regression testing reveals gaps that require additional roots (e.g., testing root-level parsing variations), the count can be increased incrementally. (See Lensing Item D-003.)

**ASSUMPTION:** Maintenance burden is a relevant design concern.

### C4: Tool Root Coverage

The validation checklist (SPEC.md Section 12.1) requires `_Decomposition/` and `INIT.md` for a valid execution root but does not require all tool roots to be populated. Examples may include empty or minimal tool-root directories to demonstrate the layout without requiring synthetic snapshot content.

Source: SPEC.md Section 1.2; SPEC.md Section 12.1.

### C5: Dependencies.csv Inclusion

Whether examples should include `Dependencies.csv` files with valid v3.1 schema content is TBD. Including them would provide regression fixtures for the dependency schema linter (DEL-08-02, TBD scope) and the DEPENDENCIES agent. Excluding them keeps examples simpler.

**ASSUMPTION:** This is a scope decision for human ruling.

---

## Trade-offs

### T1: Breadth vs. Depth of Examples

| Option | Pros | Cons |
|--------|------|------|
| **Single example root, multiple deliverables** | Lower maintenance; one structure to keep current; demonstrates diversity within a single root | Less coverage of root-level variations |
| **Multiple example roots, minimal deliverables each** | Tests root-level parsing; demonstrates different project configurations | Higher maintenance burden; more files to update when SPEC changes |

**ASSUMPTION:** The choice depends on what DEL-07-01 validation scripts need. A reasonable starting point is one example root with 2-3 deliverables at different lifecycle states.

### T2: Populated vs. Empty Document Kit Content

| Option | Pros | Cons |
|--------|------|------|
| **Populated with realistic synthetic content** | Better regression testing of content parsing; demonstrates expected document structure | More maintenance; content may drift from current templates |
| **Minimal placeholder content** | Easy to maintain; structural correctness is sufficient for layout validation | Less useful for content-parsing regression tests |

**ASSUMPTION:** Minimal placeholder content is sufficient for initial delivery; content can be enriched later if regression tests require it.

---

## Examples

No external examples are available. The deliverable itself produces the examples.

---

## Vocabulary Note

**Canonical term:** "execution root" (two words, unhyphenated when used as a noun phrase). Use hyphenated form "execution-root" only as a compound modifier before a noun (e.g., "execution-root directory," "execution-root layout"). This convention aligns with SPEC.md usage and avoids inconsistency in automated searches or terminology matching. (See Lensing Item D-001.)

---

## Rationale: SHOULD vs. MUST for REQ-07 (Semantic Artifact Inclusion)

REQ-07 uses SHOULD rather than MUST for including a `_SEMANTIC.md` sample. This modality choice reflects the following considerations:

1. **Dependency on unpublished format:** The `_SEMANTIC.md` file format does not yet have a formally published schema specification. Mandating inclusion of an artifact whose format is still evolving risks creating a fixture that becomes non-conformant as the format stabilizes.
2. **Primary vs. secondary function:** The primary function of this deliverable is structural layout conformance (regression baseline + conformance reference). Semantic artifact inclusion is a secondary enrichment that enhances lifecycle coverage but is not strictly necessary for the primary regression use case.
3. **Incremental elevation path:** If the `_SEMANTIC.md` format is formalized (e.g., via a schema specification in SPEC.md or a dedicated format document), REQ-07 can be elevated to MUST at that time with well-defined acceptance criteria.

The gap between the strong value claim in Purpose (listing "Semantic artifact samples" as one of three core functions) and the weaker SHOULD in REQ-07 is intentional: Purpose describes the deliverable's aspirational scope; requirements reflect what can be normatively enforced given current source availability. (See Lensing Items A-001, E-003.)

---

## Rationale: ASSUMPTION-Sourced Requirements (REQ-09, REQ-10)

REQ-09 (No Real Project Data) and REQ-10 (Regression Test Usability) are sourced from **ASSUMPTION** rather than a binding governance document. This is noted here for transparency:

- **REQ-09:** No explicit data-handling policy exists in the current governance suite. The requirement reflects widely accepted practice for test fixtures in shared/public repositories. If a formal data policy document is established, REQ-09 should be re-sourced to that document.
- **REQ-10:** The "usable as test fixtures" criterion is inferred from SOW-029 ("example execution-root assets ... for regression and conformance testing") and OBJ-006 ("repeatable operation"), but the specific self-containment and no-network constraints are standard engineering practice rather than explicitly mandated.

Both requirements have been retained because their substance is sound; their ASSUMPTION sourcing is a warrant gap rather than a content gap. If challenged during review, the recommended resolution is to add a formal test-fixture policy to the governance suite. (See Lensing Item F-001.)

---

## Conflict Table (for human ruling)

No unresolved conflicts identified at this time.

**Note:** Several TBD items require human decisions before full procedure execution is possible. These are tracked in Datasheet (Attributes table) and Procedure (Prerequisites), not in the Conflict Table, because they represent open scope decisions rather than source contradictions.
