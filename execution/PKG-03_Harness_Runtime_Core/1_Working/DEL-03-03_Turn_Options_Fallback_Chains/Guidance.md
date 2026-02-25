# Guidance -- DEL-03-03 Turn Options Mapping & Fallback Chains

## Purpose

This deliverable ensures that the Chirality harness runtime correctly resolves turn-level options (`opts`) into effective runtime parameters using a deterministic, layered fallback chain. The opts mapping is the mechanism through which operator preferences (via UI), persona-level defaults (via instruction file frontmatter), and global/runtime defaults are composed into a coherent parameter set for each turn execution.

This exists because the harness must be flexible enough to let the UI expose any subset of options while being rigid enough to ensure every turn has a fully resolved, valid parameter set -- regardless of what the operator provides or omits.

Source: SOW-011 (Decomposition); SPEC.md Section 9.8; OBJ-002 acceptance criteria ("Turn options mapping + fallback chains conform to the harness contract").

## Principles

### P1: Fallback Chains Are the Single Resolution Mechanism

All `opts` fields resolve through the same pattern: turn-level value (if provided) -> persona-level default (if present in frontmatter) -> global/runtime default. There is no alternate resolution path for standard opts. Governance fields (e.g., `subagentGovernance`) follow a separate enforcement path but that logic is owned by DEL-03-04.

Source: SPEC.md Section 9.8.

### P2: The UI Is a Convenience Layer, Not an Authority

The UI may expose any subset of opts fields to the operator. But the runtime does not care whether a field was "visible" in the UI. Omitted fields use defaults. Supplied fields are validated by the runtime. This separation is critical: it means the Operator Toolkit panel (DEL-02-03) can evolve its UI surface independently without affecting runtime correctness.

Source: SPEC.md Section 9.8 ("UI visibility of a field MUST NOT be interpreted as runtime authorization").

### P3: Resolution Must Be Deterministic and Auditable

Given the same opts input, persona state, and global config, the runtime must produce the same resolved parameters every time. This supports the broader system goal of auditability (DIRECTIVE.md Section 2.2, 2.4) and ensures that harness validation tests are reproducible.

Source: **ASSUMPTION** (implied by DIRECTIVE.md Sections 2.2, 2.4 and the testability requirement in OBJ-002).

### P4: Bootstrap vs. Turn Opts Are Distinct

Session boot (`/api/harness/session/boot`) and turn execution (`/api/harness/turn`) both accept `opts`, but bootstrap policy is authoritative for bootstrap-only constraints. Turn-level opts cannot override session-level bootstrap constraints. This means the fallback chain may have additional gates at boot time.

Source: SPEC.md Section 9.8.

### P5: Naming Conventions Bridge Domain Boundaries

*(Lensing item E-001)* Persona frontmatter uses snake_case (e.g., `max_turns`, `auto_approve_tools`) per YAML convention, while the runtime opts object uses camelCase (e.g., `maxTurns`). This is not an inconsistency but a deliberate boundary between the persona authoring domain (YAML files) and the runtime execution domain (JavaScript/TypeScript). The opts mapper must handle this translation explicitly, and all documents in this deliverable use the convention appropriate to the domain being discussed.

Source: SPEC.md Section 9.7 (frontmatter fields), SPEC.md Section 9.8 (opts object fields).

## Considerations

### C1: Discovering the Full Opts Surface

SPEC.md Section 9.8 documents key fallback examples (model, tools, maxTurns). Code audit confirms the current supported opts surface is:

- `model`
- `tools`
- `maxTurns`
- `persona`
- `mode`
- `subagentGovernance`

Unknown fields are ignored with warning logging (`warn-and-continue`) so forward-compatible callers do not fail closed while still getting explicit observability.

### C2: Persona Frontmatter as Tier 2 Source

Tier 2 defaults come from the active persona's YAML frontmatter for `tools` and `max_turns`. Model fallback is governed by SPEC 9.8 (`opts.model -> global model -> runtime default`) and does not use a persona tier in DEL-03-03.

**Consideration:** Not all frontmatter fields have a 1:1 mapping to opts fields. For example, `disallowed_tools` and `auto_approve_tools` may be enforcement constraints rather than fallback defaults. The implementation should distinguish between "default value if omitted" and "constraint applied regardless of opts."

*(Lensing item C-002)* This distinction has been promoted to Specification REQ-11 (ASSUMPTION) to ensure it receives normative treatment. Until the classification of each field (fallback default vs. enforcement constraint) is confirmed by codebase inspection or human ruling, the boundary remains TBD.

### C3: Global Model / Runtime Defaults (Tier 3)

Model resolution is explicit in implementation:

- Tier 2.5 source: `CHIRALITY_GLOBAL_MODEL` environment variable (if set, non-empty)
- Tier 3 source: `AGENTS.md` frontmatter `model` value in instruction root (if present, non-empty)
- Runtime default: `claude-sonnet-4-20250514`

### C4: Interaction with DEL-03-01 (Session Boot)

Session boot (DEL-03-01) initializes the session and accepts opts. This deliverable must ensure that boot-time opts are resolved consistently with turn-time opts, while respecting that bootstrap policy is authoritative for certain constraints at boot time. Coordination with DEL-03-01 may be needed.

### C5: Interaction with DEL-02-03 (Operator Toolkit Panel)

The Operator Toolkit panel (DEL-02-03) is the primary UI consumer of opts. It exposes per-turn harness options and local presets. This deliverable defines the runtime resolution contract that the toolkit panel depends on. The interface contract between them is: the toolkit panel submits `opts` (partial or complete); the runtime resolves everything via fallback chains.

## Trade-offs

### T1: Strict Typing vs. Open Extension

**Option A:** Strictly type all supported opts fields with an exhaustive schema. Easier to validate and test, but requires schema updates when adding new opts.

**Option B:** Accept opts as a loosely-typed object and validate individual fields as needed. More extensible, but harder to ensure completeness.

**Proposed direction:** **ASSUMPTION** -- Prefer strict typing for documented fields (model, tools, maxTurns) while supporting a validation/extension pattern for future fields. This balances correctness with extensibility.

*(Lensing item D-001: rationale gap)* **Rationale for proposed direction is TBD.** The current proposal is marked as an assumption without grounding in the governing documents. Relevant considerations: (a) SPEC.md Section 9.8 explicitly enumerates specific fields with specific fallback chains, suggesting the spec authors intended field-level specificity; (b) DIRECTIVE.md Section 2.4 ("evidence over plausibility") favors documented/typed fields over open extension; (c) the harness contract's emphasis on determinism (P3 above) is easier to guarantee with strict typing. However, SPEC.md also uses the generic phrase "opts object," which may imply extensibility. **Human ruling required to resolve.** *(Sources: SPEC.md Section 9.8; DIRECTIVE.md Section 2.4.)*

### T2: Fail-Open vs. Fail-Closed on Unknown Opts Fields

If the runtime receives an opts field it does not recognize:

- **Fail-open:** Ignore unknown fields silently. Risk: operator may believe a field took effect when it did not.
- **Fail-closed:** Reject the request. Risk: breaks forward compatibility.
- **Warn and continue:** Log a warning, proceed with known fields only.

**Proposed direction (implemented in DEL-03-03):** Warn and continue. Unknown opts fields are ignored with explicit warning logging in `resolveRuntimeOptions`; malformed frontmatter also logs a warning and falls through to defaults. This preserves forward compatibility while keeping operator-visible auditability.

*(Lensing item B-003)* **This trade-off has safety implications** and requires a recorded human ruling. Fail-open risks silent failures where an operator believes a field was applied but it was not (violating the spirit of K-GHOST-1 -- no ghost inputs). Fail-closed risks breaking changes on forward-compatible deployments. The "warn and continue" proposal attempts to balance these, but the decision authority rests with the human. *(Sources: Guidance.md T2; CONTRACT.md K-GHOST-1; DIRECTIVE.md Section 2.2.)*

## Examples

### Example 1: Full Fallback Chain (Model)

Given:
- Turn opts: `{ model: undefined }` (not provided)
- Active persona frontmatter: `model: "claude-sonnet-4-20250514"` (not present in this persona)
- Global config: `model: "claude-sonnet-4-20250514"`
- Runtime default: `"claude-sonnet-4-20250514"`

Resolution: Tier 1 absent -> Tier 2 absent -> Tier 3 global config -> effective model = `"claude-sonnet-4-20250514"`.

Source: Constructed from SPEC.md Section 9.8 fallback chain definition. Specific model identifiers are illustrative only.

### Example 2: Turn-Level Override

Given:
- Turn opts: `{ model: "claude-opus-4-20250514" }`
- Active persona frontmatter: `model: "claude-sonnet-4-20250514"`

Resolution: Tier 1 present -> effective model = `"claude-opus-4-20250514"` (persona default not used).

Source: Constructed from SPEC.md Section 9.8 fallback chain definition. Specific model identifiers are illustrative only.

### Example 3: Omitted Fields Default

Given:
- Turn opts: `{ model: "claude-opus-4-20250514" }` (tools and maxTurns omitted)
- Active persona frontmatter: `tools: ["Read", "Write"]`, `max_turns: 5`

Resolution: model resolved from Tier 1; tools resolved from Tier 2 persona; maxTurns resolved from Tier 2 persona.

Source: Constructed from SPEC.md Section 9.8.

## Conflict Table (for human ruling)

| Conflict ID | Conflict | Source A | Source B | Impacted Sections | Proposed Authority | Human Ruling |
|-------------|---------|----------|----------|-------------------|-------------------|-------------|
| CONF-01 | Model fallback chain conflict between SPEC 9.8 example and generic 9.7 machine-field list | SPEC.md Section 9.8 (model fallback skips persona tier) | SPEC.md Section 9.7 (`model` listed as machine-consumed field) | Datasheet (Attributes), Specification (REQ-01), Guidance (C2), Procedure (Step 2) | SPEC 9.8 + implementation behavior | RESOLVED (2026-02-24): model fallback in DEL-03-03 is `opts.model -> global model -> runtime default` (no persona tier) |
| CONF-02 | *(Lensing item C-002)* Enforcement constraints vs. fallback defaults: persona frontmatter fields `disallowed_tools` and `auto_approve_tools` may be enforcement constraints (applied unconditionally) rather than fallback defaults (overridable by turn-level opts), but no source explicitly classifies each field. | SPEC.md Section 9.7 (lists all machine-consumed fields without distinguishing category) | Guidance C2 (identifies the distinction conceptually) | Specification (REQ-07, REQ-11), Guidance (C2), Procedure (Step 3) | Human ruling or codebase inspection -- PROPOSAL | TBD |
