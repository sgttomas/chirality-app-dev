# Guidance — DEL-02-03

## Purpose

The Operator Toolkit Panel exists to give the operator a convenient, persistent control surface for per-turn harness options (`opts`) and saved presets, without introducing any authoritative state that could conflict with the governance model.

This deliverable supports **OBJ-005** (Desktop UI supports intended operator workflow) by providing an ergonomic way to configure harness turns without manually editing API payloads or relying on persona defaults alone. **ASSUMPTION (best-effort mapping):** OBJ-005 association is via PKG-02 package grouping.

> **Enrichment (X-001):** The OBJ-005 association is based on the decomposition's objective-to-deliverable mapping, which groups objectives by parent package. PKG-02 deliverables are mapped to OBJ-005. This association has not been authoritatively confirmed by a human. The ASSUMPTION tag is appropriate and should remain until the human either confirms or corrects the objective mapping. If the association is incorrect, the Purpose section and Datasheet Identification table must both be updated.

(Source: SOW-025; Decomposition DEL-02-03 entry; PLAN Section 2)

## Glossary

> **Enrichment (B-004, F-003):** This glossary normalizes terminology used across all four documents for this deliverable. When in doubt, use these canonical forms.

| Term | Canonical Form | Meaning | Notes |
|------|---------------|---------|-------|
| CONFIG | CONFIG setting | The application-level configuration mechanism that stores user preferences, including the "Show Tool Kit sidebar" toggle | Not a panel, sidebar, or toggle by itself -- CONFIG is the settings system; the toolkit panel visibility is one setting within CONFIG |
| Non-authoritative | Non-authoritative convenience state | Ephemeral, device-specific, non-versioned state stored in local storage that has no governance authority | Canonical phrasing per DIRECTIVE Section 2.5. MUST NOT be treated as project truth and MUST NOT override contract/governance enforcement |
| Harness Turn API | `POST /api/harness/turn` | The API endpoint that accepts a turn options object (`opts`) for harness turn execution | Source: SPEC Section 9.8 |
| Session Boot API | `POST /api/harness/session/boot` | The API endpoint that accepts `opts` on session bootstrap | Source: SPEC Section 9.8 |
| Opts | `opts` object | The per-turn harness options object passed to harness APIs, containing fields like `model`, `tools`, `maxTurns`, `subagentGovernance` | Source: SPEC Section 9.8 |

## Principles

### P1: Non-authoritative by Design

The foundational principle of this deliverable is the separation between **convenience state** and **project truth**.

- The toolkit panel stores state in local storage (browser/Electron local storage), which is ephemeral, device-specific, and non-versioned.
- No toolkit state is written to project files or the execution root.
- This aligns with DIRECTIVE Section 2.5: "Non-authoritative operator convenience state... MAY be stored outside project files. Such convenience state MUST NOT be treated as project truth and MUST NOT override contract/governance enforcement."

> **Canonical phrasing (E-001):** "Non-authoritative" means: convenience state that is ephemeral, device-specific, non-versioned, and has no governance authority. All documents in this deliverable use this single canonical phrasing. The Datasheet Attributes table, Specification REQ-04, and this principle all reference the same DIRECTIVE Section 2.5 policy.

(Source: DIRECTIVE Section 2.5)

### P2: Governance Passthrough, Not Override

The toolkit panel is a **passthrough** to the harness `opts` interface, not a governance mechanism. The runtime remains authoritative for all enforcement decisions.

- Opts set via the toolkit are included in the API request, but the runtime applies its own gate/seal logic regardless of what the UI provides.
- "Supplying `opts.subagentGovernance` does not guarantee delegation; all runtime gates MUST still pass." (SPEC Section 9.8)
- "UI visibility of a field MUST NOT be interpreted as runtime authorization." (SPEC Section 9.8)

This means the toolkit cannot weaken governance even if it exposes every available opt field.

> **Enrichment (A-001):** When the operator sets opts that the runtime rejects or overrides (e.g., attempting subagent delegation without valid governance metadata), the toolkit panel should provide clear feedback to the operator. The specific UX pattern for communicating rejection/override is TBD (design decision), but the principle is: the operator should not be left wondering why their settings were ignored. Possible approaches include inline status indicators, toast notifications, or turn-result annotations. Source context: SPEC Section 9.8 (fail-closed delegation governance rule); SPEC Section 9.7 (missing/invalid governance metadata MUST block subagent injection while allowing the parent turn to continue normally).

(Source: SPEC Section 9.8; CONTRACT K-AUTH-1)

### P3: Subset Exposure with Fallback Safety

The toolkit panel MAY expose any subset of harness opts. The design should consider which opts are useful for operator workflow and which would add complexity without benefit.

When an opt is not exposed (or not set), the runtime fallback chain provides safe defaults:
- Model: `opts.model` -> global model (instruction root) -> runtime default
- Tools: `opts.tools` -> persona `tools` frontmatter -> runtime preset
- Max turns: `opts.maxTurns` -> persona `max_turns` frontmatter -> runtime default

This means the panel can start with a small, useful subset and expand over time without breaking anything.

(Source: SPEC Section 9.8)

### P4: Persistence Must Be Resilient

Local storage persistence should handle:
- Missing or corrupted data gracefully (fall back to defaults).
- Schema changes between app versions (migrate or reset).
- No assumption that stored presets are valid across different working roots or project contexts.

**ASSUMPTION:** These resilience behaviors are standard practice for local-storage-backed UI state in Electron/Next.js apps, but no specific requirement is stated in the governance docs.

## Considerations

### Integration Points

The toolkit panel integrates with the desktop app at these points:

| Integration | Direction | Notes | Source |
|-------------|-----------|-------|--------|
| CONFIG setting | Panel -> CONFIG | Visibility toggle ("Show Tool Kit sidebar") | PLAN Section 2 |
| Harness Turn API | Panel -> `POST /api/harness/turn` | Opts included in request body | SPEC Section 9.8 |
| Session Boot API | Panel -> `POST /api/harness/session/boot` | Opts included where applicable | SPEC Section 9.8 |
| Multi-pane layout | Panel <-> Layout | Panel is a sidebar pane within the resizable layout | PLAN Section 2 (layout context); **ASSUMPTION** based on sidebar description |

### Relationship to DEL-03-03 (Turn Options Mapping & Fallback Chains)

DEL-03-03 covers the runtime-side opts mapping and fallback chain implementation. This deliverable (DEL-02-03) covers the UI-side exposure of those opts. The two deliverables form a producer-consumer pair:

- DEL-02-03 **produces** opts values in the API request.
- DEL-03-03 **consumes** opts values and applies fallback chains.

Testing should confirm end-to-end behavior across both deliverables, but each deliverable can be developed and unit-tested independently.

**ASSUMPTION:** This producer-consumer relationship is inferred from scope alignment (SOW-025 vs. SOW-011) and the harness contract in SPEC Section 9.8. No explicit dependency declaration exists in `_DEPENDENCIES.md`.

### Relationship to DEL-02-04 (Multi-pane Layout + Theme Hardening)

The toolkit panel is described as a sidebar, which implies it participates in the multi-pane layout system. DEL-02-04 covers resizable multi-pane layout and theme hardening. Coordination may be needed for:

- Drag handle behavior when the toolkit panel is collapsed/expanded.
- Theme consistency (light/dark mode rendering of toolkit controls).

> **Enrichment (D-001):** Coordination protocol with DEL-02-04 is currently undefined. The following guidance applies:
> - **When to coordinate:** Before implementing the sidebar container component (Phase 1, Step 1.1 in Procedure), confirm the layout integration point with DEL-02-04 (component interface, slot registration, resize behavior contract).
> - **What interface contract to expect:** TBD -- this depends on DEL-02-04's layout system design. At minimum, expect a sidebar slot API that accepts a React component and supports show/hide toggling.
> - **If DEL-02-04 is not yet complete:** The toolkit panel can be developed against a mock/stub sidebar container. When DEL-02-04 is ready, integration testing should cover: sidebar registration, resize handle interaction, theme consistency, and collapse/expand behavior.
> - Source context: PLAN Section 2 (both deliverables reference sidebar and multi-pane layout).

**ASSUMPTION:** Layout integration dependency inferred from PLAN Section 2 context. Not explicitly declared.

### Subagent Governance Fields

The toolkit panel MAY present delegation governance fields (`opts.subagentGovernance`). If it does, the following guidance applies:

- Present these fields as informational/convenience controls, not as authorization mechanisms.
- Clearly indicate to the operator that runtime gate/seal logic remains authoritative.
- Consider whether displaying these fields adds operator value or creates confusion.

(Source: SPEC Section 9.8 — "UI MAY present delegation governance fields for operator use. Runtime gate/seal logic remains authoritative.")

## Trade-offs

### T1: Subset Size vs. Operator Flexibility

| Option | Pro | Con |
|--------|-----|-----|
| Expose minimal opts (model, maxTurns) | Simple UI; low confusion risk | Operators may want more control |
| Expose all supported opts | Maximum flexibility | UI complexity; risk of operator confusion with governance fields |
| Progressive disclosure (basic + advanced) | Balances simplicity with power | More complex to implement and test |

**PROPOSAL:** Start with a focused subset (model, maxTurns, tools) and add governance fields later if operator demand justifies it. This is a design decision for implementation.

### T2: Preset Scope (Global vs. Per-Root)

| Option | Pro | Con |
|--------|-----|-----|
| Global presets (all working roots) | Simpler; presets always available | May not make sense across different project contexts |
| Per-working-root presets | Context-appropriate | More complex storage; presets lost if root changes |
| Global with per-root overrides | Flexible | Most complex to implement |

**PROPOSAL:** Start with global presets stored in local storage. Per-root scoping can be added later if needed. This is a design decision for implementation.

## Examples

### Example: Operator Sets Model Via Toolkit Panel

1. Operator opens CONFIG, enables "Show Tool Kit sidebar."
2. Toolkit panel appears as a sidebar.
3. Operator selects `claude-sonnet-4-20250514` from the model selector.
4. Operator sends a turn in WORKBENCH.
5. The turn API request includes `opts.model = "claude-sonnet-4-20250514"`.
6. Runtime uses the operator-selected model for this turn.

(Source: SPEC Section 9.8 — model fallback chain; **ASSUMPTION** for specific UI interaction flow.)

### Example: Governance Enforcement Holds Despite Toolkit State

1. Operator sets `opts.subagentGovernance.contextSealed = true` via toolkit panel.
2. Actual context has NOT been sealed by a human gate approval.
3. Runtime evaluates governance metadata: `contextSealed` in `opts` does not match runtime state.
4. Subagent injection is blocked; parent turn continues normally.

(Source: SPEC Section 9.8 — delegation governance rule; SPEC Section 9.7 — fail closed.)

## Conflict Table (for human ruling)

| Conflict ID | Conflict | Source A | Source B | Impacted Sections | Proposed Authority (PROPOSAL) | Human Ruling |
|------------|---------|----------|----------|-------------------|-------------------------------|-------------|
| CT-001 | REQ-08 uses SHOULD for preset management, but SOW-025 lists "local presets" as an in-scope item -- ambiguous whether presets are required for SOW-025 acceptance or optional | Specification REQ-08 (SHOULD) | Decomposition SOW-025 ("Operator Toolkit panel for per-turn opts + local presets") | Specification REQ-08; Procedure Phase 2; Datasheet Local Presets table | Human ruling on SOW-025 interpretation: if presets are required for acceptance, upgrade REQ-08 to MUST | TBD |

> **Enrichment (C-002):** This conflict was surfaced by the exhaustive compliance coverage lens. The SHOULD/MUST ambiguity for preset management needs human ruling because it affects whether Phase 2 of the Procedure is mandatory for SOW-025 acceptance.
