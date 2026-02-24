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
| `opts.model` | `opts.model` -> global model (instruction root / `CHIRALITY_GLOBAL_MODEL`) -> runtime default | `claude-sonnet-4-20250514` | SPEC.md Section 9.8; `frontend/src/lib/harness/options.ts` |
| `opts.tools` | `opts.tools` -> persona `tools` frontmatter -> runtime preset | `["read", "write", "bash"]` | SPEC.md Section 9.8; `frontend/src/lib/harness/options.ts` |
| `opts.maxTurns` | `opts.maxTurns` -> persona `max_turns` frontmatter -> runtime default | `12` | SPEC.md Section 9.8; `frontend/src/lib/harness/options.ts` |
| `opts.subagentGovernance` | Separate enforcement path (fail-closed gate logic) | N/A (enforcement, not fallback) | SPEC.md Section 9.7 |

**Note on naming convention:** The persona frontmatter field `max_turns` (snake_case) maps to the opts field `maxTurns` (camelCase). This naming convention difference applies at the boundary between persona YAML frontmatter (snake_case per YAML convention) and the runtime opts object (camelCase per JavaScript/TypeScript convention). All documents in this deliverable use `max_turns` when referring to the persona frontmatter field and `maxTurns` when referring to the opts field. *(Lensing item E-001: terminology normalization.)*

**Supported opts surface (implementation):** `model`, `tools`, `maxTurns`, `persona`, `mode`, `subagentGovernance`. Unknown fields are ignored with a warning (`warn-and-continue`) in `resolveRuntimeOptions`.

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
| **Language / Stack** | TypeScript + Node.js runtime modules within Next.js/Electron workspace (`frontend/`) |
| **Integration points** | Turn execution API (`/api/harness/turn`), session boot API (`/api/harness/session/boot`), persona instruction file parsing (YAML frontmatter) |
| **Key modules** | `frontend/src/lib/harness/options.ts`, `frontend/src/app/api/harness/turn/route.ts`, `frontend/src/app/api/harness/session/boot/route.ts`, `frontend/src/__tests__/lib/harness-options.test.ts` |

## References

| Ref | Location | Relevance |
|-----|----------|-----------|
| SPEC.md Section 9.7 | `docs/SPEC.md` | Runtime metadata contract and subagent governance |
| SPEC.md Section 9.8 | `docs/SPEC.md` | Harness turn input contract, opts fields, fallback chain definitions |
| CONTRACT.md | `docs/CONTRACT.md` | Binding invariants (K-INVENT-1, K-GHOST-1 relevant to opts interpretation) |
| DIRECTIVE.md | `docs/DIRECTIVE.md` | Founding intent: human authority, filesystem-as-state |
| Decomposition | `execution/_Decomposition/ChiralityApp_SoftwareDecomposition_2026-02-21_G7-APPROVED.md` | DEL-03-03 entry, SOW-011, OBJ-002 |
| PLAN.md Section 2 | `docs/PLAN.md` | Operator Toolkit panel, harness validation context |
