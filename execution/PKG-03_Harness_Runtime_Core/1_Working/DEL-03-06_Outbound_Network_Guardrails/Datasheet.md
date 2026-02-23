# Datasheet — DEL-03-06 Outbound Network Guardrails (Anthropic-only) + Verification

## Identification

| Field | Value |
|-------|-------|
| **Deliverable ID** | DEL-03-06 |
| **Name** | Outbound Network Guardrails (Anthropic-only) + Verification |
| **Package** | PKG-03 — Harness Runtime Core |
| **Type** | SECURITY_CONTROL |
| **Context Envelope** | L |
| **Responsible Party** | TBD (human assignment required — see B-003) |
| **Scope Coverage** | SOW-006 |
| **Supported Objectives** | OBJ-002, OBJ-006 |
| **Anticipated Artifacts** | CODE / TEST / DOC |

## Attributes

| Attribute | Value | Source |
|-----------|-------|--------|
| Target Platform | macOS 15+, Apple Silicon only | Decomposition DEC-PLAT-001 |
| Application Framework | Electron + Next.js | PLAN Section 2 (Desktop Frontend) |
| Electron Version | `31.0.2` (from `frontend/package.json` semver range `^31.0.2`) | `frontend/package.json` `devDependencies.electron` |
| Anthropic SDK Version | `0.78.0` (pinned) | `frontend/package.json` `dependencies.@anthropic-ai/sdk` |
| Permitted Outbound Destination | Anthropic API endpoints only | Decomposition DEC-NET-001 |
| Permitted API Domain(s) | `api.anthropic.com` (explicit runtime allowlist enforced for `CHIRALITY_ANTHROPIC_API_URL`) | Guidance C3; Procedure Step 2.1; runtime guardrail pass (2026-02-23) |
| Blocked Outbound Categories | Telemetry, update checks, all non-Anthropic endpoints | Decomposition DEC-NET-001 |
| Enforcement Mechanism | TBD (human ruling required per OI-002) | Decomposition Open Issues OI-002 |
| Verification / Proof Standard | TBD (human ruling required per OI-002) | Decomposition Open Issues OI-002 |
| Network Policy Scope | Electron shell + HTTP client + update/telemetry paths | Decomposition DEL-03-06 ContextEnvelopeNotes |

> **Terminology note (B-004):** Throughout these documents, the term **"enforcement mechanism"** is used consistently to refer to the technical approach for enforcing the outbound network policy. Previous drafts used "enforcement approach," "enforcement posture," and "enforcement and verification method" interchangeably; these have been normalized to **"enforcement mechanism"** except where a distinct meaning is intended (e.g., "verification method" refers specifically to the proof standard, not the enforcement implementation).

## Conditions

| Condition | Details | Source |
|-----------|---------|--------|
| External integrations boundary | External system integration is OUT of scope; Anthropic API is the sole exception per DEC-NET-001 | DIRECTIVE Section 4.2; Decomposition SOW-043 |
| Desktop-first / offline capable | No server requirement; desktop-first design | DIRECTIVE Section 5 (Structural Constraints) |
| No hidden memory | Non-authoritative convenience state (e.g., API key) may exist outside project files but must not be treated as project truth | DIRECTIVE Section 2.5 |
| OCSP/CRL infrastructure traffic | Certificate validation traffic (OCSP/CRL) to non-Anthropic endpoints may be required for TLS operation — see CONF-002 in Guidance | Trade-off analysis in Guidance; Specification REQ-NET-001 note |
| Allowlist maintenance posture | The permitted Anthropic API domain list must be maintained over time as API versions or domains change; new endpoints are blocked by default until explicitly added to the allowlist (see E-003) | Guidance P2; **ASSUMPTION: maintenance responsibility must be defined** |

## Construction

| Surface | Concern | Notes |
|---------|---------|-------|
| Electron main process | Electron auto-update, telemetry, Squirrel, Chromium network calls | Must audit and disable/block any default outbound behavior |
| Next.js / Node HTTP client | Outbound HTTP(S) calls from harness runtime (API provider integration) | Runtime manager now fail-closes non-Anthropic/malformed base URLs before SDK request dispatch |
| Anthropic SDK | SDK-level network behavior | Must confirm SDK does not phone home to non-Anthropic endpoints (see Guidance C3) |
| Chromium renderer | Potential outbound from renderer process (DNS prefetch, safe browsing, etc.) | Must audit Chromium flags and disable non-essential outbound |
| Package manager / build tooling | npm/yarn telemetry, Electron builder telemetry | Build-time only; not runtime — **ASSUMPTION: build-time telemetry is out of scope for this deliverable** (cross-reference: Specification Excluded scope confirms this boundary — see D-001) |

## References

| Reference | Location | Relevance |
|-----------|----------|-----------|
| Software Decomposition | `execution/_Decomposition/ChiralityApp_SoftwareDecomposition_2026-02-21_G7-APPROVED.md` | DEL-03-06 entry, DEC-NET-001, OI-002 |
| DIRECTIVE | `docs/DIRECTIVE.md` | Founding intent, out-of-scope boundaries (Section 4.2), structural constraints |
| CONTRACT | `docs/CONTRACT.md` | Invariants: K-GHOST-1, K-INVENT-1 |
| SPEC | `docs/SPEC.md` | Deliverable folder layout, lifecycle states |
| PLAN | `docs/PLAN.md` | Desktop frontend description (Section 2) |
| Electron security documentation | **location TBD** (external) | Chromium/Electron default network behavior, command-line flags |
| Anthropic API documentation | **location TBD** (external) | Canonical API endpoint domains for allowlist validation |
