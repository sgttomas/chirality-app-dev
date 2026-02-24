# Specification -- DEL-08-01

## Scope

### What This Deliverable Covers

This deliverable implements SHA-256 content hashes for out-of-folder references listed in `_REFERENCES.md` files and a verification mechanism that checks hash integrity before pipeline runs.

**Source:** Decomposition DEL-08-01 description; PLAN Section 3.1.

### What This Deliverable Excludes

- In-folder files (these are covered by git SHA tracking and do not require separate hash verification).
- Changes to the `Dependencies.csv` schema or dependency tracking mechanics (covered by DEL-05-04 and DEL-08-02).
- Central dependency graph maintenance (explicitly excluded per K-DEP-1).
- Staleness propagation logic (covered by DEL-08-07; depends on this deliverable's hash output -- ASSUMPTION).
- Modifications to approval or issuance workflows (out of scope per SOW-039, K-AUTH-1).

### Scope Status Note

SOW-032 was ruled **IN** by human decision on 2026-02-24 (OI-032 resolved, SCA-002). This deliverable is fully actionable.

## Requirements

### REQ-01: SHA-256 Hash Computation

The system SHALL compute SHA-256 hashes for all out-of-folder references listed in a deliverable's `_REFERENCES.md` file.

- Hash computation SHALL target the referenced file content during PREPARATION workspace scaffolding, after reference entries are written and before the deliverable context is considered sealed (see Guidance C6 for terminology clarification).
- The hash algorithm SHALL be SHA-256 (as specified in the decomposition).
- Hash output SHALL be a lowercase hexadecimal string of 64 characters (ASSUMPTION -- standard SHA-256 hex encoding convention; see REQ-01-FMT below).
- Hash computation SHALL handle file-not-found gracefully by recording the reference as unresolvable rather than failing silently.

**Source:** Decomposition DEL-08-01 description; PLAN Section 3.1.

### REQ-01-FMT: Canonical Hash Output Format

All hash values produced by hash computation modules and consumed by verification modules SHALL use a canonical format:

- Encoding: lowercase hexadecimal.
- Length: 64 characters (256 bits / 4 bits per hex character).
- No prefix (no `0x`, no `sha256:` prefix).
- No whitespace, no line breaks.

This format SHALL be consistent across REQ-01 (computation), REQ-02 (storage), REQ-07 (standalone scripts), and any downstream consumers (including DEL-08-07 interface).

**Source:** FIPS 180-4 standard practice (location TBD -- standard library implementations serve as accepted proxy). ASSUMPTION: lowercase hex without prefix is the simplest interoperable format.

**Lensing provenance:** X-001 (Normalization -- hash output format standardization).

### REQ-02: Hash Storage in `_REFERENCES.md`

The computed hashes SHALL be stored within the `_REFERENCES.md` file in a machine-readable format that extends the existing reference entry schema (SPEC Section 7).

- The extension MUST preserve backward compatibility with the current `_REFERENCES.md` format.
- Each reference entry with an out-of-folder target SHALL include a `ContentHash` field.
- The `ContentHash` field value SHALL conform to the canonical format defined in REQ-01-FMT.
- In-folder references MAY omit the hash field (covered by git tracking).

**Source:** PLAN Section 3.1 (implies hash storage co-located with references). ASSUMPTION: storage within `_REFERENCES.md` itself (pending design decision on exact schema).

### REQ-03: Pre-Pipeline Verification Gate

The system SHALL verify content hashes before pipeline runs.

- Verification SHALL compare stored SHA-256 hashes against current file content for all out-of-folder references.
- A hash mismatch SHALL be reported as a verification failure with:
  - The reference path that failed,
  - The stored hash,
  - The computed current hash.
- Verification failure behavior (block vs. warn) is TBD (pending human policy decision per DEC-HASH-002; see Guidance C2 for options analysis and trade-offs table for current leaning toward "block").

**Source:** Decomposition DEL-08-01 description ("verify before pipeline runs"); PLAN Section 3.1 (ORCHESTRATOR verification before pipeline runs).

**Lensing provenance:** A-001 (WeakStatement -- added DEC-HASH-002 resolution reference and Guidance C2 pointer); A-002 (TBD_Question -- linked mandatory enforcement mode to human decision).

### REQ-04: PREPARATION Integration

PREPARATION agent SHALL compute and store hashes during workspace scaffolding when creating or updating `_REFERENCES.md`.

- Hashes are computed for referenced files that exist at scaffold time.
- References to files that do not exist at scaffold time SHALL have their hash field set to `TBD`.

**Source:** PLAN Section 3.1 ("Requires changes to PREPARATION (hash computation on scaffold)"). ASSUMPTION: exact integration point within PREPARATION workflow.

### REQ-05: ORCHESTRATOR Integration

ORCHESTRATOR SHALL invoke hash verification before authorizing pipeline execution on a deliverable.

- Verification is invoked as part of the pre-pipeline seal check.
- The verification result is reported to the human operator.
- ORCHESTRATOR SHALL NOT silently skip verification failures.
- The enforcement mode (block execution vs. warn and continue) SHALL follow the policy established by human ruling on DEC-HASH-002.

**Source:** PLAN Section 3.1 ("Requires changes to... ORCHESTRATOR (hash verification before pipeline runs)"). ASSUMPTION: integration as part of existing seal/gate checks.

**Lensing provenance:** A-002 (TBD_Question -- linked enforcement mode to DEC-HASH-002).

### REQ-06: No-Ghost-Input Alignment

Content hash verification SHALL support enforcement of K-GHOST-1 (no ghost inputs) by ensuring that out-of-folder referenced content has not changed since the context was sealed.

- If a referenced file has changed (hash mismatch), the system flags it as a potential ghost-input violation.
- Resolution is human-directed (consistent with K-AUTH-1).

**Source:** PLAN Section 3.1 ("aligned with no-ghost-input constraints (K-GHOST-1)"); CONTRACT K-GHOST-1.

### REQ-07: Tooling Scripts

The deliverable SHALL produce hash generation and verification scripts that can be run independently of the agent framework.

- Scripts SHALL be usable in CI pipelines and local validation workflows.
- Scripts SHALL read `_REFERENCES.md` files and perform hash operations without requiring agent context.
- "Without requiring agent context" means: scripts SHALL not depend on active harness sessions, agent instruction files, or any runtime state managed by ORCHESTRATOR, PREPARATION, or other agents. Scripts SHALL operate using only filesystem paths and file content as inputs.
- Scripts SHALL produce hash values conforming to the canonical format defined in REQ-01-FMT.

**Source:** PLAN Section 3.1 ("tooling (hash generation/verification scripts)"); Decomposition DEL-08-01 (anticipated artifacts: CODE/SCRIPT/DOC).

**Lensing provenance:** F-001 (VerificationGap -- added testable definition of "without agent context").

### REQ-08: Verification Bypass Audit Trail

If hash verification is bypassed (e.g., by human override), the bypass event SHALL be recorded with:

- Timestamp of the bypass.
- Actor who authorized the bypass (human identity or session identifier).
- Reason for bypass (free-text or structured category).
- Which specific reference(s) had their verification bypassed.

The bypass record SHALL be visible in audit trails and SHALL NOT be silently discarded.

**Source:** Guidance P1 ("If verification is bypassed, the bypass must be recorded and visible in audit trails"); DIRECTIVE Section 2.3 (Human Authority at Every Gate). ASSUMPTION: bypass recording mechanism (log file, `_STATUS.md` annotation, or dedicated record) is TBD pending implementation design.

**Lensing provenance:** D-001 (MissingSlot -- bypass recording requirement absent from Specification); E-001 (WeakStatement -- Guidance P1 bypass statement lacked normative backing).

### REQ-09: Hash Recomputation on Intentional Updates

The system SHALL support explicit hash recomputation when a referenced file is intentionally updated.

- Recomputation SHALL be triggerable via standalone scripts (REQ-07) or through PREPARATION re-scaffolding.
- After recomputation, the updated hashes SHALL be written to `_REFERENCES.md` and the previous hash values SHALL be superseded.
- Recomputation SHALL NOT occur automatically on every file system change; it requires explicit human or agent invocation (to preserve "content as approved at seal time" semantics).

**Source:** Guidance C3 (hash recomputation triggers). ASSUMPTION: the explicit-invocation model is inferred from Guidance C3's statement that "the recomputation trigger should be explicit."

**Lensing provenance:** F-002 (VerificationGap -- no verification existed for hash recomputation workflow).

## Standards

| Standard/Reference | Applicability | Accessible |
|---------------------|--------------|------------|
| SHA-256 (FIPS 180-4 / NIST) | Hash algorithm specification | No (standard reference -- location TBD; standard library implementations serve as accepted proxy; see Guidance C7) |
| docs/SPEC.md Section 7 | Current `_REFERENCES.md` format that will be extended | Yes |
| docs/CONTRACT.md K-GHOST-1 | No-ghost-input invariant | Yes |
| docs/CONTRACT.md K-PROV-1 | Provenance invariant | Yes |
| docs/CONTRACT.md K-VAL-1 | Dirty detection invariant | Yes |

## Verification

| Requirement | Verification Approach | Expected Evidence |
|-------------|----------------------|-------------------|
| REQ-01 | Test: compute hash of known file, verify SHA-256 output matches expected value | Test script output; hash comparison log |
| REQ-01-FMT | Test: verify hash output is lowercase hex, 64 characters, no prefix/whitespace | Automated format validation in test suite |
| REQ-02 | Inspect: verify `_REFERENCES.md` contains ContentHash fields for out-of-folder references | Sample `_REFERENCES.md` file with hashes |
| REQ-02 (backward compat) | Test: parse an extended `_REFERENCES.md` (with ContentHash fields) using existing tooling and confirm no parse errors; parse a legacy `_REFERENCES.md` (without ContentHash) using new tooling and confirm graceful handling | Parse test logs showing both directions succeed without error |
| REQ-03 | Test: introduce a modified referenced file and confirm verification detects mismatch | Verification failure report showing path, stored hash, current hash |
| REQ-04 | Test: run PREPARATION scaffold and confirm hashes are computed for existing referenced files | Scaffolded `_REFERENCES.md` with populated hash fields |
| REQ-05 | Test: attempt pipeline run with mismatched hash and confirm ORCHESTRATOR reports failure | Pipeline pre-check log showing verification result |
| REQ-06 | Inspect: verify that hash mismatch flags reference as potential ghost-input violation | Verification output message content |
| REQ-07 | Test: run standalone scripts in CI-like environment; confirm scripts execute without active harness session, agent instructions, or ORCHESTRATOR runtime state | Script execution output showing successful hash computation/verification using only filesystem paths as inputs |
| REQ-08 | Test: bypass verification via human override and confirm bypass event is recorded with timestamp, actor, reason, and affected references | Bypass audit record (log entry, `_STATUS.md` annotation, or equivalent) |
| REQ-09 | Test: modify a referenced file, invoke recomputation, verify updated hash is written to `_REFERENCES.md` and subsequent verification passes | Pre/post `_REFERENCES.md` showing updated ContentHash; verification pass log |
| DEL-08-07 interface | Test: verify that hash verification output (pass/fail per reference with stored/computed hash values) is structured in a format consumable by DEL-08-07 staleness propagation | Interface contract document; sample output parsed by DEL-08-07 consumer (ASSUMPTION -- DEL-08-07 interface not yet defined; test deferred until interface is specified) |

**Lensing provenance for verification additions:** A-003 (backward compatibility verification); F-001 (REQ-07 agent-context independence); F-002 (REQ-09 recomputation verification); X-002 (DEL-08-07 interface verification).

## Documentation

| Artifact | Type | Description | Status |
|----------|------|-------------|--------|
| Hash computation module/script | CODE/SCRIPT | Computes SHA-256 hashes for referenced files | TBD |
| Hash verification module/script | CODE/SCRIPT | Verifies stored hashes against current content | TBD |
| `_REFERENCES.md` schema extension | DOC | Documents the extended format with ContentHash field | TBD |
| PREPARATION integration notes | DOC | Documents changes to PREPARATION for hash computation | TBD |
| ORCHESTRATOR integration notes | DOC | Documents changes to ORCHESTRATOR for pre-pipeline verification | TBD |
| Usage guide | DOC | End-to-end workflow for hash generation, storage, and verification | TBD |
| Bypass audit trail specification | DOC | Documents the bypass recording mechanism and audit trail format | TBD |
