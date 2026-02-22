# Datasheet -- DEL-07-01 Harness Validation Suite

## Identification

| Field | Value |
|-------|-------|
| **DeliverableID** | DEL-07-01 |
| **Name** | Harness Validation Suite (local + CI-ready posture) |
| **PackageID** | PKG-07 |
| **Package** | Validation & Example Assets |
| **Type** | TEST_SUITE |
| **ContextEnvelope** | M |
| **ResponsibleParty** | TBD |
| **Scope Coverage** | SOW-028 |
| **Objective** | OBJ-006 |
| **Decomposition** | `execution/_Decomposition/ChiralityApp_SoftwareDecomposition_2026-02-21_G7-APPROVED.md` |

## Attributes

| Attribute | Value | Source |
|-----------|-------|--------|
| Validation target | Harness runtime (session boot, turn execution, SSE streaming, opts mapping, subagent governance, attachment resolution) | Decomposition DEL-07-01; SOW-028 |
| Execution modes | Local (developer workstation) + CI-ready (headless/automated pipeline) | Decomposition DEL-07-01 description |
| Script runtime | Node.js (`.mjs` modules) | PLAN Section 2 -- references `frontend/scripts/validate-harness-*.mjs`; **ASSUMPTION** |
| Target platform | macOS 15+, Apple Silicon | DEC-PLAT-001 (Decomposition Decision Log) |
| Application stack | Electron + Next.js desktop app | PLAN Section 2 |
| Anticipated artifact types | TEST / SCRIPT / DOC | `_CONTEXT.md` |
| Harness API endpoints under test | `/api/harness/session/boot`, `/api/harness/turn` | SPEC Section 9.8 |
| SSE streaming protocol | Server-Sent Events from runtime to UI during turns | SPEC Section 9.8; SOW-005 |
| Attachment resolver rules | Supported extensions, `isFile()` check, 10 MB (10,000,000 bytes) per-file limit, 18 MB (18,000,000 bytes) total raw budget, partial failure handling. **Note:** byte-level thresholds are **ASSUMPTION** based on decimal MB interpretation; see Specification REQ-09 for normalization details. | SPEC Section 9.8; Lensing B-003, E-001 |
| Subagent governance model | Fail-closed: injection blocked unless `contextSealed`, `pipelineRunApproved`, and `approvalRef` are valid | SPEC Section 9.7 |
| Opts fallback chain | `opts.model` -> global model -> runtime default; `opts.tools` -> persona `tools` frontmatter -> runtime preset; `opts.maxTurns` -> persona `max_turns` -> runtime default | SPEC Section 9.8 |
| Network policy | Anthropic-only outbound (DEC-NET-001) | Decomposition Decision Log |

## Conditions

| Condition | Description | Source |
|-----------|-------------|--------|
| Pre-existing harness runtime | Validation scripts assume a running or startable harness runtime instance | **ASSUMPTION** -- implied by test suite nature |
| API key provisioning | Anthropic API key must be available for live integration tests (provisioning contract is TBD per OI-001) | Decomposition Open Issues OI-001 |
| Working Root available | A valid `projectRoot` directory must be available for session boot tests | SPEC Section 9.8; SOW-003 |
| Node.js environment | Node.js runtime available for `.mjs` script execution. **Required version: TBD** -- no version constraint is specified in governance documents; depends on Electron + Next.js stack version. Human ruling needed to set minimum version. | **ASSUMPTION** -- based on Electron + Next.js stack; Lensing B-001 |

## Construction

| Aspect | Value | Source |
|--------|-------|--------|
| Script location (expected) | `frontend/scripts/validate-harness-*.mjs` -- **ASSUMPTION** based on PLAN Section 2 references; actual paths TBD pending human confirmation. See also Guidance note on path normalization. | PLAN Section 2; Lensing F-003 |
| Documentation location (expected) | `frontend/docs/harness/` -- **ASSUMPTION** based on PLAN Section 2; actual paths TBD pending human confirmation | PLAN Section 2; Lensing F-003 |
| Test categories | Session lifecycle, turn execution, SSE streaming, opts/fallback chains, subagent governance gating, attachment contract behaviors | Decomposition DEL-07-01; SOW-028 |
| CI integration posture | Scripts must be runnable in CI pipelines without interactive input | Decomposition DEL-07-01 description ("CI-ready posture") |
| Output format | TBD -- pass/fail results suitable for CI reporting. **Note:** downstream CI consumers require a defined output format (e.g., JSON, TAP, or plain text with exit codes) to parse results programmatically. Until specified, CI integration is blocked for automated result consumption. | **ASSUMPTION**; Lensing A-002 |
| Coverage of harness contract surface areas | Sessions, turns, SSE, opts, subagent gating, attachments | Decomposition DEL-07-01 description |

## References

| Ref | Document | Relevance |
|-----|----------|-----------|
| R1 | `docs/SPEC.md` Section 9.7-9.8 | Harness turn input contract, subagent governance, attachment rules |
| R2 | `docs/CONTRACT.md` | Binding invariants (K-SEAL-1, K-GHOST-1, K-INVENT-1, K-CONFLICT-1) that tests should validate -- see Specification REQ-13 for K-invariant mapping |
| R3 | `docs/PLAN.md` Section 2 | References existing validation scripts and harness docs |
| R4 | `docs/DIRECTIVE.md` | Design philosophy and responsible-use constraints |
| R5 | Decomposition (G7-APPROVED) | DEL-07-01 entry, SOW-028, OBJ-006 |
| R6 | `docs/TYPES.md` | Canonical vocabulary, lifecycle states, agent roles |
