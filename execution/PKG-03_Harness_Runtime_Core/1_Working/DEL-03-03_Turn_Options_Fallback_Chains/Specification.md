# Specification -- DEL-03-03 Turn Options Mapping & Fallback Chains

## Scope

### Included

This deliverable covers the runtime logic that maps incoming `opts` (turn options) to effective runtime parameters via a deterministic fallback chain. Specifically:

1. **Turn-level option resolution** -- resolving `opts` fields submitted on `POST /api/harness/turn` against persona-level defaults and global/runtime defaults.
2. **Session boot option handling** -- resolving `opts` fields submitted on `POST /api/harness/session/boot`, with bootstrap policy remaining authoritative for bootstrap-only constraints.
3. **Fallback chain correctness** -- ensuring each supported `opts` field resolves through the documented three-tier chain: turn-level -> persona-level -> global/runtime default.
4. **UI contract compliance** -- ensuring that omitted `opts` fields fall through to defaults and that UI visibility does not constitute runtime authorization.
5. **Tests and documentation** for the above behaviors.

Source: SOW-011 ("Implement/maintain the harness turn `opts` mapping + fallback chains (model/tools/maxTurns, etc.), with UI allowed to expose any subset."); Decomposition DEL-03-03 entry.

### Excluded

- Subagent governance enforcement logic (covered by DEL-03-04 per SOW-012).
- Attachment resolver and prompt-mode selection (covered by DEL-04-01 per SOW-007/008/009).
- SSE streaming protocol mechanics (covered by DEL-03-02 per SOW-005).
- Outbound network guardrails (covered by DEL-03-06 per SOW-006).
- Operator Toolkit panel UI implementation (covered by DEL-02-03 per SOW-025). The toolkit panel is a consumer of `opts`; this deliverable covers the runtime resolution side.
- API key provisioning and storage (covered by DEL-03-05).

## Requirements

### REQ-01: Three-Tier Fallback Chain for Documented Fields

The runtime MUST resolve the following `opts` fields through a three-tier fallback chain as documented in `docs/SPEC.md` Section 9.8:

| Field | Tier 1 (Turn-level) | Tier 2 (Persona-level) | Tier 3 (Global/Runtime) |
|-------|---------------------|----------------------|------------------------|
| Model | `opts.model` | **ASSUMPTION:** persona `model` frontmatter (SPEC.md Section 9.7 lists `model` as a machine-consumed field, but the Section 9.8 fallback example skips persona tier for model) | global model (instruction root) -> runtime default |
| Tools | `opts.tools` | persona `tools` frontmatter | runtime preset |
| Max Turns | `opts.maxTurns` | persona `max_turns` frontmatter | runtime default |

**Note on naming convention:** The persona frontmatter uses snake_case (`max_turns`) while the opts object uses camelCase (`maxTurns`). The runtime mapper is responsible for this convention translation at the Tier 1/Tier 2 boundary. *(Lensing item E-001: normalization.)*

**Note on Model fallback chain:** SPEC.md Section 9.8 documents the model fallback as `opts.model -> global model (instruction root) -> runtime default`, which omits a persona-level tier. However, SPEC.md Section 9.7 lists `model` as a machine-consumed YAML frontmatter field. Whether persona-level `model` participates as Tier 2 in the fallback chain is ambiguous and requires codebase inspection or human ruling. *(See Conflict Table CONF-01 in Guidance.md; Lensing item A-001.)*

Source: SPEC.md Section 9.8.

### REQ-02: Deterministic Resolution

For any given combination of turn-level `opts`, active persona, and global configuration, the effective runtime parameters MUST be deterministically computed. The same inputs MUST always produce the same resolved values.

Source: **ASSUMPTION** -- implied by the harness contract's explicit fallback chain documentation and the system's emphasis on auditability (DIRECTIVE.md Section 2.2, 2.4).

### REQ-03: Omitted Fields Default Correctly

When a client omits an `opts` field, the runtime MUST apply the fallback chain (Tier 2, then Tier 3) rather than rejecting the request or using `null`/`undefined`.

Source: SPEC.md Section 9.8 ("Omitted fields MUST follow runtime fallback chains").

### REQ-04: UI Visibility Is Not Authorization

The runtime MUST NOT treat UI visibility of an `opts` field as authorization to use a value. Runtime validation and enforcement remain authoritative regardless of what the UI exposes.

Source: SPEC.md Section 9.8 ("UI visibility of a field MUST NOT be interpreted as runtime authorization").

### REQ-05: Session Boot Opts Handling

`POST /api/harness/session/boot` MUST accept `opts` and apply them, with bootstrap policy remaining authoritative for bootstrap-only constraints. Bootstrap-specific constraints MUST NOT be overridden by turn-level opts.

**Note (Lensing item A-002):** The requirement references "bootstrap-only constraints" but does not enumerate which constraints are bootstrap-only vs. per-turn-overridable. Without an explicit enumeration, implementers cannot distinguish the two categories. TBD: enumerate bootstrap-only constraints via codebase inspection or human ruling. *(Source: Specification.md REQ-05; SPEC.md Section 9.8.)*

Source: SPEC.md Section 9.8 ("bootstrap policy remains authoritative for bootstrap-only constraints").

### REQ-06: Turn API Opts Mapping

`POST /api/harness/turn` MUST accept `opts` and apply runtime option mapping on each turn invocation.

Source: SPEC.md Section 9.8.

### REQ-07: Persona Frontmatter Parsing

The runtime MUST correctly parse persona instruction files' YAML frontmatter to extract Tier 2 defaults. The documented machine-consumed fields are:

- `description`
- `subagents`
- `tools`
- `model`
- `max_turns`
- `disallowed_tools`
- `auto_approve_tools`

Source: SPEC.md Section 9.7 (Runtime metadata contract).

### REQ-08: Governance Fields Separate Path

`opts.subagentGovernance` follows a separate enforcement path (fail-closed gate logic) and is NOT part of the standard three-tier fallback chain. This deliverable MUST NOT break governance enforcement but does not implement it (DEL-03-04 scope).

Source: SPEC.md Section 9.7; Decomposition SOW-012 -> DEL-03-04.

### REQ-09: Additional Opts Fields

**ASSUMPTION:** The runtime may support `opts` fields beyond the three documented fallback examples (model, tools, maxTurns). If additional fields exist in the implementation, they MUST follow the same fallback chain pattern or have their resolution logic explicitly documented.

**Note (Lensing item C-001):** This requirement is currently ASSUMPTION-only with no binding source. Codebase inspection is needed to either confirm (grounding the requirement with evidence) or remove it. Until grounded, this requirement has no normative force; it serves as a reminder for the audit step. *(Source: Specification.md REQ-09.)*

### REQ-10: No Invented Values

Per K-INVENT-1 (CONTRACT.md), unknown or missing values at the end of the fallback chain MUST result in a defined runtime default, not an invented or guessed value. If no valid default exists, the runtime MUST handle the case explicitly (error, skip, or documented no-op).

Source: CONTRACT.md K-INVENT-1.

### REQ-11: Enforcement Constraints vs. Fallback Defaults

**ASSUMPTION (Lensing item C-002):** The runtime MUST distinguish between persona frontmatter fields that serve as fallback defaults (e.g., `tools`, `model`, `max_turns` -- used as Tier 2 in the fallback chain when turn-level opts are absent) and fields that serve as enforcement constraints (e.g., `disallowed_tools`, `auto_approve_tools` -- applied regardless of turn-level opts). The distinction governs whether a persona field can be overridden by turn-level opts or is applied unconditionally.

**Note:** Guidance C2 identifies this distinction, and SPEC.md Section 9.7 lists both categories of fields, but no single source explicitly classifies each field as "fallback default" or "enforcement constraint." This classification requires human ruling or codebase inspection. *(Sources: SPEC.md Section 9.7; Guidance.md C2.)*

## Standards

| Standard / Governance Doc | Applicability | Location |
|--------------------------|---------------|----------|
| `docs/SPEC.md` Section 9.7 | Runtime metadata contract (YAML frontmatter fields, subagent governance) | Accessible |
| `docs/SPEC.md` Section 9.8 | Harness turn input contract (opts, fallback chains, UI contract) | Accessible |
| `docs/CONTRACT.md` K-INVENT-1 | No invented values | Accessible |
| `docs/CONTRACT.md` K-GHOST-1 | No ghost inputs (relevant to ensuring opts resolution uses only declared/visible context) | Accessible |
| `docs/DIRECTIVE.md` Section 2.4 | Evidence over plausibility | Accessible |

## Verification

| Requirement | Verification Approach | Evidence |
|-------------|----------------------|----------|
| REQ-01 | Unit tests for each documented field: supply Tier 1 only, Tier 1+2, Tier 2 only, Tier 3 only; verify resolution | Test results |
| REQ-02 | Property-based or deterministic test: same inputs -> same outputs across N repeated runs. *(Lensing item F-003: concrete pass criteria TBD -- define N (e.g., 100 runs minimum) and failure detection method.)* | Test results |
| REQ-03 | Test with omitted fields; verify Tier 2/3 are applied | Test results |
| REQ-04 | Code review: runtime does not inspect UI-side visibility state | Code review record |
| REQ-05 | Integration test: session boot with opts; verify bootstrap constraints are not overridden | Test results |
| REQ-06 | Integration test: turn with opts; verify mapping applied | Test results |
| REQ-07 | Unit test: parse sample persona YAML frontmatter; verify all documented fields extracted | Test results |
| REQ-08 | Integration test: governance fields are passed through without breaking; confirm DEL-03-04 owns enforcement | Test results + cross-deliverable check |
| REQ-09 | Code audit: identify all supported opts fields; verify each has documented fallback logic | Code review record |
| REQ-10 | Edge-case test: exercise fallback chain with all tiers absent; verify defined default or explicit handling. *(Lensing item F-001: verification should explicitly confirm K-INVENT-1 compliance -- i.e., assert that no value is fabricated/guessed; the runtime either applies a documented default or returns an explicit error/no-op.)* | Test results |
| REQ-10 (K-GHOST-1) | *(Lensing item A-003)* Verify that opts resolution does not introduce inputs from undeclared/invisible context sources, confirming K-GHOST-1 compliance. Verification approach: code review + test confirming all resolution inputs are traceable to declared opts, persona frontmatter, or global config. | Code review record + test results |
| REQ-11 | Code review + unit test: confirm enforcement constraints are applied unconditionally while fallback defaults are overridable by turn-level opts | Code review record + test results |

### Objective Traceability

*(Lensing item D-002)* The verification outcomes for this deliverable trace to OBJ-002 acceptance criterion: "Turn options mapping + fallback chains conform to the harness contract" (Decomposition, OBJ-002). Specifically:

| OBJ-002 Acceptance Criterion | Traced Requirements | Verification Summary |
|------------------------------|--------------------|--------------------|
| Turn options mapping + fallback chains conform to the harness contract | REQ-01, REQ-02, REQ-03, REQ-04, REQ-05, REQ-06, REQ-07, REQ-08, REQ-09, REQ-10, REQ-11 | If all REQ verification checks pass, the deliverable satisfies this OBJ-002 criterion. Any REQ failure blocks OBJ-002 acceptance for this deliverable's scope. |

Source: Decomposition OBJ-002 acceptance criteria; **ASSUMPTION (best-effort mapping)** -- OBJ-002 is associated with this deliverable via PKG-03 package grouping.

## Documentation

### Required Artifacts

| Artifact | Type | Description |
|----------|------|-------------|
| Runtime option mapper implementation | CODE | Source code implementing opts resolution and fallback chains |
| Fallback chain unit tests | TEST | Tests covering all three tiers for documented fields |
| Integration tests | TEST | End-to-end tests for turn and session boot opts handling |
| Opts mapping documentation | DOC | Developer-facing documentation of supported opts fields, fallback chains, and extension points |

Source: _CONTEXT.md Anticipated Artifacts (CODE/TEST/DOC).
