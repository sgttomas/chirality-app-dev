# Procedure -- DEL-08-01

## Purpose

This procedure describes the steps to produce and verify the artifacts for DEL-08-01: SHA-256 content hashes for out-of-folder references in `_REFERENCES.md`, with pre-pipeline verification. It covers implementation, integration, and validation of the hash computation and verification mechanism.

## Prerequisites

| Prerequisite | Description | Status |
|--------------|-------------|--------|
| SOW-032 Scope Decision | SOW-032 must be flipped to IN before full implementation proceeds (Open Issue OI-032) | TBD |
| Current `_REFERENCES.md` Format | Understanding of SPEC Section 7 format for `_REFERENCES.md` | Available (docs/SPEC.md Section 7) |
| K-GHOST-1 / K-PROV-1 / K-VAL-1 | Understanding of the invariants this deliverable supports | Available (docs/CONTRACT.md) |
| PLAN Section 3.1 | Feature description and integration points | Available (docs/PLAN.md Section 3.1) |
| PREPARATION Agent Instructions | Required for integration of hash computation during scaffold | Available (AGENT_PREPARATION.md -- location TBD) |
| ORCHESTRATOR Agent Instructions | Required for integration of hash verification before pipeline runs | Available (AGENT_ORCHESTRATOR.md -- location TBD) |

## Steps

### Phase 1: Schema Design

**Step 1.1 -- Define `_REFERENCES.md` Hash Extension Schema**

1. Review the current `_REFERENCES.md` format (SPEC Section 7).
2. Define the extended format that includes a `ContentHash` field for each out-of-folder reference entry.
3. Ensure backward compatibility: existing `_REFERENCES.md` files without hash fields remain valid.
4. Define the canonical hash output format: lowercase hexadecimal, 64 characters, no prefix, no whitespace (per Specification REQ-01-FMT).
5. Document the schema extension (candidate format TBD -- see Guidance C1 for storage location decision).

**Step 1.2 -- Define Verification Result Format**

1. Define the output format for hash verification results (pass/fail per reference).
2. Include: reference path, stored hash, computed hash (on mismatch), verification status.
3. Ensure the output format is structured (JSON or equivalent) so that DEL-08-07 (Staleness Propagation) can consume it programmatically (see Guidance C4).
4. Determine how results are reported to the operator (log, console, structured output -- TBD).

**Lensing provenance:** X-002 (DEL-08-07 interface requirement added to Step 1.2).

### Phase 2: Core Implementation

**Step 2.1 -- Implement Hash Computation Module**

1. Implement a module or script that:
   - Reads a `_REFERENCES.md` file.
   - Identifies out-of-folder references.
   - Computes SHA-256 hash for each referenced file that exists.
   - Produces hash values in the canonical format (lowercase hex, 64 characters, no prefix -- per REQ-01-FMT).
   - Records `TBD` for references to files that do not exist at computation time.
   - Writes the hashes back to `_REFERENCES.md` (or companion file, per design decision DEC-HASH-001).
2. Handle edge cases:
   - File not found at reference path.
   - File permissions preventing read access.
   - Empty file (valid -- hash the empty content).
   - Symbolic links: TBD (resolution: decide whether to follow the link and hash the target content, reject symbolic links as unsupported, or record the link as a special case with both link target path and target content hash. Decision should align with existing repo conventions for symbolic link handling. Consult human or check repo `.gitattributes`/`.gitignore` for precedent).
3. Use standard library SHA-256 implementation (Node.js `crypto` module or Python `hashlib` -- language TBD based on repo tooling; see Guidance C7 for FIPS 180-4 compliance approach).

**Lensing provenance:** A-004 (TBD_Question -- symbolic link handling resolution criteria added); B-001 (implementation language TBD recorded in Datasheet).

**Step 2.2 -- Implement Hash Verification Module**

1. Implement a module or script that:
   - Reads a `_REFERENCES.md` file with stored hashes.
   - For each reference with a `ContentHash` value (not TBD):
     - Reads the current file content.
     - Computes current SHA-256 hash (in canonical format per REQ-01-FMT).
     - Compares against stored hash.
   - Reports: matched, mismatched, or file-not-found per reference.
2. Return a structured result (exit code + output) suitable for CI integration.
3. Define failure behavior per design decision DEC-HASH-002 (block vs. warn).

**Step 2.3 -- Implement Bypass Recording**

1. Implement a mechanism to record verification bypass events (per Specification REQ-08):
   - Timestamp of the bypass.
   - Actor identity (human or session identifier).
   - Reason for bypass.
   - Affected reference(s).
2. Define the recording location (log file, `_STATUS.md` annotation, or dedicated bypass record -- TBD).
3. Ensure bypass records are durable and visible in audit trails.

**Lensing provenance:** D-001, E-001 (bypass recording requirement).

### Phase 3: Agent Integration

**Step 3.1 -- Integrate with PREPARATION**

1. Modify PREPARATION agent workflow to invoke hash computation when creating or updating `_REFERENCES.md` during scaffold.
2. Hash computation occurs after reference entries are written but before the deliverable context is considered sealed (see Guidance C6 for timing clarification).
3. Update PREPARATION agent instructions to document the new step.
4. Verify: scaffold a new deliverable and confirm `_REFERENCES.md` contains hash values for existing out-of-folder references.

**Step 3.2 -- Integrate with ORCHESTRATOR**

1. Modify ORCHESTRATOR pre-pipeline check to invoke hash verification.
2. Verification occurs after context seal check and before pipeline run authorization.
3. On verification failure:
   - Report the specific reference(s) that failed.
   - Apply failure policy (block or warn, per DEC-HASH-002).
   - Do not silently skip (consistent with DIRECTIVE Section 2.4 and K-CONFLICT-1).
4. On verification bypass:
   - Record bypass event per Specification REQ-08 and Step 2.3.
5. Update ORCHESTRATOR agent instructions to document the new verification step.

### Phase 4: Standalone Tooling

**Step 4.1 -- Create Standalone Scripts**

1. Package hash computation and verification as standalone scripts runnable outside the agent framework.
2. Scripts SHALL:
   - Accept a deliverable folder path (or `_REFERENCES.md` path) as input.
   - Operate without requiring agent context or session state (per Specification REQ-07: no dependency on active harness sessions, agent instruction files, or ORCHESTRATOR runtime state).
   - Produce hash values in the canonical format (REQ-01-FMT).
   - Produce structured output (JSON or plain text) suitable for CI consumption.
3. Document CLI usage (arguments, exit codes, output format).

**Step 4.2 -- CI Integration Guide**

1. Document how to integrate the standalone scripts into CI pipelines.
2. Include: example CI step, expected exit codes, failure handling guidance.

### Phase 5: Hash Recomputation Workflow

**Step 5.1 -- Implement Recomputation Support**

1. Implement explicit hash recomputation for intentional reference updates (per Specification REQ-09):
   - Support recomputation via standalone scripts (same tool as Step 4.1, with a "recompute" or "update" mode).
   - Support recomputation via PREPARATION re-scaffolding.
2. After recomputation, updated hashes are written to `_REFERENCES.md` and previous values are superseded.
3. Recomputation does NOT occur automatically on file system changes -- it requires explicit invocation.

**Step 5.2 -- Verify Recomputation Workflow**

1. Modify a referenced file intentionally.
2. Invoke recomputation (standalone script or PREPARATION re-scaffold).
3. Confirm updated hash is written to `_REFERENCES.md`.
4. Run verification and confirm it passes with the new hash.

**Lensing provenance:** F-002 (VerificationGap -- recomputation workflow had no verification).

### Phase 6: Documentation

**Step 6.1 -- Write Usage Documentation**

1. Document the end-to-end workflow:
   - When hashes are computed (during PREPARATION workspace scaffolding, after reference entries are written, before context sealing -- see Guidance C6).
   - When hashes are verified (pre-pipeline, by ORCHESTRATOR).
   - How to manually recompute hashes after intentional reference updates (see Phase 5).
   - How to interpret verification results.
   - How bypass events are recorded and where to find audit trails.
2. Document the schema extension for `_REFERENCES.md`.
3. Include worked examples (see Guidance Examples section for illustrative samples).

### Phase 7: Error Recovery

**Step 7.1 -- Handle Hash Infrastructure Failures**

Define and document recovery procedures for failure modes in the hash infrastructure itself:

1. **Hash computation failure during PREPARATION scaffold:**
   - If an I/O error prevents reading a referenced file during hash computation, record the hash field as `ERROR: <reason>` (not `TBD`, to distinguish from "file does not exist yet").
   - PREPARATION scaffold should complete with a warning rather than aborting entirely (ASSUMPTION -- failing the entire scaffold for one unreadable reference may be disproportionate; human should be notified).
   - Log the failure with the reference path and error details.

2. **Verification failure due to infrastructure (not content mismatch):**
   - If verification cannot read a referenced file (permissions, file moved, I/O error), report as `UNVERIFIABLE` rather than `FAIL` or `PASS`.
   - `UNVERIFIABLE` references should be treated as verification failures for policy purposes (block or warn per DEC-HASH-002) but distinguished in reporting so the human can see the difference between "content changed" and "content could not be checked."

3. **Corrupt or malformed hash values in `_REFERENCES.md`:**
   - If a stored hash value does not conform to the canonical format (REQ-01-FMT), report it as a format error and treat as `UNVERIFIABLE`.
   - Suggest recomputation as the recovery action.

**Lensing provenance:** C-002 (MissingSlot -- rollback/recovery steps for hash infrastructure failures).

## Verification

| Step | Verification Check | Expected Result |
|------|-------------------|-----------------|
| 1.1 | Schema extension preserves backward compatibility | Existing `_REFERENCES.md` files parse correctly with and without hash fields |
| 2.1 | Compute hash of a known file | SHA-256 output matches independently computed value; format is lowercase hex, 64 chars |
| 2.1 | Attempt hash of nonexistent file | Graceful handling; hash field set to `TBD` or error recorded |
| 2.2 | Verify matching hashes | All references pass; exit code 0 |
| 2.2 | Verify mismatched hash (modified reference file) | Mismatch detected and reported with paths + hashes |
| 2.2 | Verify with missing reference file | File-not-found reported; verification does not crash |
| 2.3 | Bypass verification and check audit trail | Bypass event recorded with timestamp, actor, reason, affected references |
| 3.1 | Scaffold new deliverable with out-of-folder references | `_REFERENCES.md` contains populated ContentHash fields |
| 3.2 | Pipeline run with valid hashes | ORCHESTRATOR verification passes; pipeline proceeds |
| 3.2 | Pipeline run with mismatched hash | ORCHESTRATOR reports failure; applies failure policy |
| 4.1 | Run standalone script on deliverable folder | Correct hash computation/verification without agent context |
| 4.2 | Run CI integration example | CI step executes and reports results correctly |
| 5.2 | Modify reference, recompute, re-verify | Updated hash written; subsequent verification passes |
| 7.1 | Trigger I/O error during hash computation | Error recorded; scaffold completes with warning |
| 7.1 | Trigger I/O error during verification | Reference reported as UNVERIFIABLE; distinguished from content mismatch |

## Records

| Record | Description | Location |
|--------|-------------|----------|
| Schema extension document | Extended `_REFERENCES.md` format with ContentHash field | TBD (within deliverable folder or SPEC update) |
| Hash computation module/script | Source code for SHA-256 computation | TBD (repo location) |
| Hash verification module/script | Source code for verification | TBD (repo location) |
| Bypass recording module | Source code or configuration for bypass audit trail | TBD (repo location) |
| PREPARATION instruction update | Modified PREPARATION agent instructions | AGENT_PREPARATION.md (location TBD) |
| ORCHESTRATOR instruction update | Modified ORCHESTRATOR agent instructions | AGENT_ORCHESTRATOR.md (location TBD) |
| CI integration guide | Documentation for CI pipeline integration | TBD (within deliverable folder) |
| Test results | Verification test outputs | TBD (test execution records) |
| Recomputation workflow documentation | Steps for manual hash recomputation after intentional updates | TBD (within usage guide) |
