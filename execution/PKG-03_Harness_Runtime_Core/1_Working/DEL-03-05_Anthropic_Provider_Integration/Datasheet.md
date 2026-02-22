# Datasheet — DEL-03-05 Anthropic Provider Integration & Key Provisioning Contract

## Identification

| Field | Value |
|-------|-------|
| **DeliverableID** | DEL-03-05 |
| **Name** | Anthropic Provider Integration & Key Provisioning Contract |
| **PackageID** | PKG-03 |
| **Package** | Harness Runtime Core |
| **Type** | BACKEND_FEATURE_SLICE |
| **ContextEnvelope** | M |
| **ResponsibleParty** | TBD — **requires human assignment** (see E-001) |
| **Scope Coverage** | SOW-006 |
| **Objectives** | OBJ-002 |
| **Anticipated Artifacts** | CODE / TEST / DOC |
| **Open Issues** | OI-001 (API key provisioning + storage contract — POLICY_DECISION pending) |

## Attributes

| Attribute | Value | Source |
|-----------|-------|--------|
| Target LLM Provider | Anthropic (Claude API) | Decomposition DEL-03-05; DEC-NET-001 |
| Permitted Outbound Endpoints | Anthropic API only | DEC-NET-001 (Decomposition Decision Log) |
| API Key Classification | Non-project-truth convenience state | Decomposition DEL-03-05 description |
| Runtime SDK | Anthropic Claude SDK — specific package version TBD (must be pinned for reproducible builds; see B-001) | **ASSUMPTION: inferred from Electron + Next.js stack** |
| Anthropic API Version | TBD — the target `anthropic-version` header value must be recorded once selected (see B-002) | **ASSUMPTION: Anthropic API uses versioned headers; version selection not yet made** |
| Platform | macOS 15+, Apple Silicon only | DEC-PLAT-001 (Decomposition Decision Log) |
| App Architecture | Electron + Next.js desktop application | PLAN Section 2 |
| Model Selection Fallback | `opts.model` -> global model (instruction root) -> runtime default | SPEC Section 9.8 |
| Streaming Protocol | SSE (Server-Sent Events) | SPEC Section 9.8; Decomposition PKG-03 description |

## Conditions

| Condition | Description | Source |
|-----------|-------------|--------|
| Network Policy | Outbound connections limited to Anthropic API only; no telemetry, update checks, or other endpoints | DEC-NET-001 |
| Key Storage Boundary | API key MUST NOT be stored as project truth (i.e., not in git-tracked project execution files) | DIRECTIVE Section 2.5; Decomposition DEL-03-05 |
| Key Provisioning Method | TBD — pending OI-001 resolution | OI-001 (Decomposition Open Issues) |
| Key Storage Location | TBD — pending OI-001 resolution (candidates: environment variable, OS keychain, local storage, config file outside working root) | OI-001 |
| Key Rotation/Revocation | TBD — no source defines rotation/revocation requirements; deferral rationale and analysis documented in Guidance Section C5 (see B-003) | No source available; see Guidance C5 for deferral rationale |
| Error Handling for Missing Key | The runtime must return a clear, actionable error to the UI without crashing; LLM-dependent operations are blocked while non-LLM functionality remains available (see F-001 for acceptance criteria) | **ASSUMPTION: derived from P3 principle (Fail Clearly, Not Silently)** |
| API Key Log Protection | API key material MUST NOT appear in application logs, console output, or error telemetry (see X-002) | **ASSUMPTION: standard security practice; see Specification REQ-09** |

## Construction

| Component | Description | Source |
|-----------|-------------|--------|
| Provider Module | Server-side module that wraps Anthropic SDK client initialization, authentication, and request dispatch | **ASSUMPTION: inferred from harness architecture (SPEC Section 9.8)** |
| Key Resolver | Component that retrieves the API key from the provisioned storage location at runtime | **ASSUMPTION: needed to satisfy non-project-truth constraint** |
| Model Configuration | Integration with harness `opts.model` fallback chain | SPEC Section 9.8 |
| Request/Response Mapping | Translation between harness turn contract and Anthropic API request/response shapes | **ASSUMPTION: inferred from turn execution architecture (SPEC Section 9.8)** |
| Streaming Adapter | Bridge between Anthropic API streaming responses and harness SSE event protocol | **ASSUMPTION: inferred from SSE streaming requirement (SOW-005, SOW-006)** |
| Content Block Formatter | Formatting of multimodal content blocks (text + image/document) from harness format to Anthropic API format | **ASSUMPTION: inferred from REQ-05 and attachment resolver interface (DEL-04-01)** |
| Error Classifier | Mapping of Anthropic API errors (rate limits, auth failures, network errors) to harness-level error events using a consistent error taxonomy | **ASSUMPTION: standard provider integration concern** |

## References

| Reference | Relevance |
|-----------|-----------|
| Decomposition (G7-APPROVED) | DEL-03-05 entry, DEC-NET-001, OI-001, SOW-006, OBJ-002 |
| docs/SPEC.md Section 9.8 | Harness turn input contract, model fallback chain, opts mapping |
| docs/DIRECTIVE.md Section 2.5 | Non-authoritative convenience state rules |
| docs/CONTRACT.md K-GHOST-1 | No ghost inputs; context limited to folder + declared references |
| docs/CONTRACT.md K-INVENT-1 | Unknown values become TBD |
| docs/PLAN.md Section 2 | Existing tooling: Electron + Next.js, session/turn APIs, SSE |
| Anthropic API documentation | API versioning, authentication, rate limits, streaming protocol (`location TBD` — external) |
| Anthropic Claude SDK (Node.js/TypeScript) | Client library initialization, streaming helpers, error types (`location TBD` — external) |
