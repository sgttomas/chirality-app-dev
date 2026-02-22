# Datasheet -- DEL-03-03 Turn Options Mapping & Fallback Chains

## Identification

| Field | Value |
|-------|-------|
| **Deliverable ID** | DEL-03-03 |
| **Name** | Turn Options Mapping & Fallback Chains |
| **Package** | PKG-03 Harness Runtime Core |
| **Type** | BACKEND_FEATURE_SLICE |
| **Context Envelope** | S |
| **Responsible Party** | TBD *(Lensing item E-002: human assignment required -- no authority to assign)* |
| **Scope Coverage** | SOW-011 |
| **Objective** | OBJ-002 |
| **Anticipated Artifacts** | CODE / TEST / DOC |

## Attributes

### Turn Options (`opts`) Fields

The harness runtime accepts a turn options object (`opts`) on session boot and turn execution APIs. The following fields are documented in the harness contract (`docs/SPEC.md` Section 9.8):

| Field | Fallback Chain | Tier 3 Default Value | Source |
|-------|---------------|---------------------|--------|
| `opts.model` | `opts.model` -> **ASSUMPTION:** persona `model` frontmatter (see Specification note) -> global model (instruction root) -> runtime default | TBD *(Lensing item B-002: actual runtime default value requires codebase inspection)* | SPEC.md Section 9.8, 9.7 |
| `opts.tools` | `opts.tools` -> persona `tools` frontmatter -> runtime preset | TBD *(Lensing item B-002: actual runtime preset value requires codebase inspection)* | SPEC.md Section 9.8 |
| `opts.maxTurns` | `opts.maxTurns` -> persona `max_turns` frontmatter -> runtime default | TBD *(Lensing item B-002: actual runtime default value requires codebase inspection)* | SPEC.md Section 9.8 |
| `opts.subagentGovernance` | Separate enforcement path (fail-closed gate logic) | N/A (enforcement, not fallback) | SPEC.md Section 9.7 |

**Note on naming convention:** The persona frontmatter field `max_turns` (snake_case) maps to the opts field `maxTurns` (camelCase). This naming convention difference applies at the boundary between persona YAML frontmatter (snake_case per YAML convention) and the runtime opts object (camelCase per JavaScript/TypeScript convention). All documents in this deliverable use `max_turns` when referring to the persona frontmatter field and `maxTurns` when referring to the opts field. *(Lensing item E-001: terminology normalization.)*

**Note on completeness (Lensing item B-001):** The above are the key fallback examples explicitly documented in SPEC.md Section 9.8. Additional `opts` fields may exist in the implementation; a complete enumeration requires codebase inspection. **ASSUMPTION: The full set of supported opts fields is a superset of the three documented fallback examples.** A complete enumeration is TBD pending codebase audit (see Procedure Step 1).

### API Surfaces

| Endpoint | Accepts `opts` | Notes | Source |
|----------|---------------|-------|--------|
| `POST /api/harness/turn` | Yes | Runtime option mapping applied per turn | SPEC.md Section 9.8 |
| `POST /api/harness/session/boot` | Yes | Bootstrap policy authoritative for bootstrap-only constraints | SPEC.md Section 9.8 |

### UI Contract

| Rule | Description | Source |
|------|-------------|--------|
| Subset exposure | UI MAY expose any subset of supported `opts` fields | SPEC.md Section 9.8 |
| Omitted fields | MUST follow runtime fallback chains | SPEC.md Section 9.8 |
| Visibility != authorization | UI visibility of a field MUST NOT be interpreted as runtime authorization | SPEC.md Section 9.8 |

## Conditions

| Condition | Detail |
|-----------|--------|
| **Runtime platform** | macOS 15+, Apple Silicon (DEC-PLAT-001; Decomposition Decision Log) |
| **Framework** | Electron + Next.js desktop application (PLAN Section 2) |
| **Network policy** | Anthropic-only outbound (DEC-NET-001; enforcement is DEL-03-06 scope) |

## Construction

| Aspect | Detail |
|--------|--------|
| **Language / Stack** | TBD (determined by existing codebase conventions; expected TypeScript/JavaScript per Electron + Next.js stack) |
| **Integration points** | Turn execution API (`/api/harness/turn`), session boot API (`/api/harness/session/boot`), persona instruction file parsing (YAML frontmatter) |
| **Key modules** | TBD (runtime option mapper, fallback chain resolver, persona metadata reader) |

## References

| Ref | Location | Relevance |
|-----|----------|-----------|
| SPEC.md Section 9.7 | `docs/SPEC.md` | Runtime metadata contract and subagent governance |
| SPEC.md Section 9.8 | `docs/SPEC.md` | Harness turn input contract, opts fields, fallback chain definitions |
| CONTRACT.md | `docs/CONTRACT.md` | Binding invariants (K-INVENT-1, K-GHOST-1 relevant to opts interpretation) |
| DIRECTIVE.md | `docs/DIRECTIVE.md` | Founding intent: human authority, filesystem-as-state |
| Decomposition | `execution/_Decomposition/ChiralityApp_SoftwareDecomposition_2026-02-21_G7-APPROVED.md` | DEL-03-03 entry, SOW-011, OBJ-002 |
| PLAN.md Section 2 | `docs/PLAN.md` | Operator Toolkit panel, harness validation context |
