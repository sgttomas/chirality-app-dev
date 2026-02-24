# Datasheet -- DEL-02-06 Settings / API Key Entry UI

## Identification

| Field | Value |
|-------|-------|
| **DeliverableID** | DEL-02-06 |
| **Name** | Settings / API Key Entry UI |
| **PackageID** | PKG-02 |
| **Package** | Desktop UI Workflow |
| **Type** | UX_UI_SLICE |
| **ContextEnvelope** | M |
| **Scope Item** | SOW-050 |
| **Objective** | OBJ-005 |
| **Responsible Party** | TBD -- assign responsible party for deliverable ownership (lensing item F-002) |
| **Lifecycle State** | ISSUED |

## Attributes

| Attribute | Value | Source |
|-----------|-------|--------|
| Runtime platform | macOS 15+, Apple Silicon (Electron + Next.js) | Decomposition DEC-PLAT-001 |
| UI framework | Next.js (frontend) within Electron shell | Decomposition PKG-02 description |
| Key provisioning policy | ENV+UI: UI-provided key takes precedence; `ANTHROPIC_API_KEY` env fallback | Decomposition SCA-003; OI-001 amendment |
| Key storage classification | Non-project-truth convenience state | DIRECTIVE section 2.5; Decomposition DEL-02-06 description |
| Storage mechanism | Local secure storage via Electron `safeStorage` (or equivalent platform-native facility) | **ASSUMPTION: Electron `safeStorage` is the expected mechanism for local secure key storage; human to confirm.** Canonical term: "local secure storage" for the abstract capability; "Electron `safeStorage`" for the concrete mechanism. See Guidance.md#Terminology for normalization (lensing item E-002). |
| Persisted key location | App-local config outside working root; not git-tracked | DIRECTIVE section 2.5; SPEC section 9.8 |
| Downstream consumer | DEL-03-05 Anthropic Provider Integration (key resolver) | _DEPENDENCIES.md DEP-02-06-003 |
| SDK dependency baseline | `@anthropic-ai/sdk@0.78.0` | SPEC section 9.8 |
| Anticipated artifacts | CODE / TEST / DOC | _CONTEXT.md |

## Conditions

| Condition | Constraint | Source |
|-----------|-----------|--------|
| Key material MUST NOT appear in working-root files | Hard constraint | SPEC section 9.8; DIRECTIVE section 2.5 |
| Key material MUST NOT be committed to git | Hard constraint | SPEC section 9.8 |
| Key material MUST NOT appear in logs, console, or error messages | Hard constraint | DEL-03-05 REQ-09 (shared security principle) |
| Convenience state MUST NOT override governance/contract enforcement | Hard constraint | DIRECTIVE section 2.5 |
| UI-provided key takes precedence over env variable | Runtime contract | Decomposition SCA-003; OI-001 amendment |
| `ANTHROPIC_API_KEY` env variable remains fallback | Runtime contract | Decomposition SCA-003; OI-001 amendment |
| Single provider: Anthropic only | Architectural constraint | DEC-NET-001; SOW-043 exception |

## Construction

| Component | Description | Notes |
|-----------|-------------|-------|
| Settings panel / page | UI surface for API key entry, display, and management | TBD -- specific UI location (settings page, modal, panel) |
| Key input field | Masked text input for API key entry | **ASSUMPTION: standard masked-input pattern** |
| Key status indicator | Visual indicator showing whether a valid key is configured | TBD -- design specifics |
| Save / clear controls | Buttons to persist or remove the stored key | TBD |
| Local secure storage adapter | Module interfacing with Electron `safeStorage` or equivalent | **ASSUMPTION: `safeStorage` as mechanism** |
| Key resolution bridge | Interface contract enabling DEL-03-05 key resolver to query UI-provided key. Renderer IPC channels: `api-key:store`, `api-key:remove`, `api-key:status`. Main-process module interface provides resolver key retrieval. | Final REQ-07 policy ruling (2026-02-24): re-query-per-turn; no `api-key:changed` notification channel required. |

## References

| Reference | Location | Relevance |
|-----------|----------|-----------|
| Decomposition (G7-APPROVED + SCA-003) | `execution/_Decomposition/ChiralityApp_SoftwareDecomposition_2026-02-21_G7-APPROVED.md` | Scope Amendment A3: DEL-02-06 definition, SOW-050, OI-001 amendment |
| SPEC.md section 9.8 | `docs/SPEC.md` | Provider policy, ENV+UI key provisioning baseline, key-material constraints |
| DIRECTIVE.md section 2.5 | `docs/DIRECTIVE.md` | Non-authoritative convenience state requirements |
| DEL-03-05 Specification | `execution/PKG-03_Harness_Runtime_Core/1_Working/DEL-03-05_Anthropic_Provider_Integration/Specification.md` | Downstream key resolver contract (REQ-02, REQ-06, REQ-07, REQ-09) |
| _CONTEXT.md | Deliverable-local | Identity, scope coverage, objectives |
| _DEPENDENCIES.md | Deliverable-local | Dependency register (5 ACTIVE rows) |
