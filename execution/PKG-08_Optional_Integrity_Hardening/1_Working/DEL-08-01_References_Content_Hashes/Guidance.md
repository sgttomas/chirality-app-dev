# Guidance -- DEL-08-01

## Purpose

This deliverable exists to close an integrity gap in the Chirality execution model. Currently, `_REFERENCES.md` files list paths and descriptions for reference documents, but there is no mechanism to verify that the referenced content has not changed between context sealing and pipeline execution. This creates a window where an agent could operate on inputs that differ from what the human approved -- a "ghost input" scenario that violates K-GHOST-1.

Content hashing adds a cryptographic verification layer: SHA-256 hashes are computed during PREPARATION workspace scaffolding (after reference entries are written, before the deliverable context is considered sealed) and verified before pipeline runs (by ORCHESTRATOR). This makes the no-ghost-input guarantee enforceable rather than aspirational.

**Source:** PLAN Section 3.1; CONTRACT K-GHOST-1; DIRECTIVE Section 2.4 (Evidence Over Plausibility).

## Principles

### P1: Integrity Verification Must Be Automated and Non-Bypassable

Manual hash comparison is error-prone and unsustainable. The verification step must be automated (integrated into ORCHESTRATOR's pre-pipeline checks) and should not be silently skippable. If verification is bypassed, the bypass must be recorded and visible in audit trails (see Specification REQ-08 for the normative requirement governing bypass recording).

**Source:** PLAN Section 3.1 ("enable automated integrity checking"); DIRECTIVE Section 2.3 (Human Authority at Every Gate -- the human must see the result, not be shielded from it).

**Lensing provenance:** D-001, E-001 (bypass recording now backed by REQ-08 in Specification).

### P2: Backward Compatibility with Existing `_REFERENCES.md` Files

The hash extension to `_REFERENCES.md` must not break existing tooling or workflows that parse the current format. Existing `_REFERENCES.md` files without hashes should remain valid; the absence of a hash field means "not yet hashed" rather than "verification failed."

**Source:** SPEC Section 7 (current format); ASSUMPTION: backward compatibility is required for incremental adoption.

### P3: In-Folder vs Out-of-Folder Distinction

Git already provides SHA-based integrity tracking for files within the repository. Content hashing in `_REFERENCES.md` specifically targets out-of-folder references -- files that exist outside the deliverable's folder and may not be tracked by the same git commit. This avoids redundant work while closing the actual integrity gap.

**Source:** PLAN Section 3.1 ("out-of-folder references"); DIRECTIVE Section 2.1 (Filesystem Is the Database -- git is already the integrity layer for in-repo content).

### P4: TBD Scope -- Defensive Drafting

SOW-032 is currently TBD. This means the feature may be brought IN scope, deferred, or retired. All design decisions documented here are conditional on SOW-032 being flipped to IN. The deliverable is structured to be actionable immediately upon scope activation without requiring re-decomposition.

**Source:** Decomposition Scope Ledger (SOW-032 status = TBD); Open Issue OI-032.

## Considerations

### C1: Hash Storage Location

Two candidate approaches:

1. **Inline in `_REFERENCES.md`:** Add a `ContentHash: <sha256>` field to each reference entry. Keeps everything co-located. Requires extending the SPEC Section 7 format.

2. **Companion file (e.g., `_REFERENCES_HASHES.json`):** Store hashes in a separate machine-readable file. Keeps `_REFERENCES.md` human-readable and unchanged. Adds a second file to track.

**ASSUMPTION:** Inline storage (option 1) is the simpler approach and aligns with the "filesystem is the state" principle (fewer files = fewer sync points). Final decision requires human ruling.

### C2: Verification Failure Policy

When a hash mismatch is detected before a pipeline run, the system needs a policy:

- **Block:** Prevent pipeline execution until the human acknowledges the change and re-seals context. (Stricter; aligns with K-GHOST-1.)
- **Warn:** Allow pipeline execution but log a warning and flag the affected references. (More permissive; may be appropriate for advisory-only references.)

**ASSUMPTION:** Block is the default for references that are part of sealed context; warn may be appropriate for informational references. Final policy requires human decision.

### C3: Hash Recomputation Triggers

Hashes need to be recomputed when:
- PREPARATION creates or updates a deliverable scaffold.
- A human manually updates `_REFERENCES.md` to add or change references.
- A referenced file is known to have been intentionally updated.

The recomputation trigger should be explicit (not automatic on every file touch) to maintain the integrity semantics -- a hash represents "content as approved at seal time." See Specification REQ-09 for the normative requirement governing recomputation behavior.

**Lensing provenance:** F-002 (recomputation workflow now backed by REQ-09).

### C4: Interaction with Staleness Propagation

DEL-08-07 (Staleness Propagation + Triage Tooling) depends on hash-based dirty detection. The content hash computed here feeds into K-VAL-1 dirty detection. The interface between this deliverable and DEL-08-07 should be:
- This deliverable produces: stored hashes + verification results (pass/fail per reference, with stored hash and computed current hash on mismatch).
- DEL-08-07 consumes: verification results to propagate staleness through the dependency graph.

The verification output format must be structured and documented so that DEL-08-07 can consume it programmatically (see Specification Verification table for the DEL-08-07 interface acceptance criterion).

**ASSUMPTION:** DEL-08-07 will consume hash verification output, but the exact interface is not yet defined.

**Lensing provenance:** X-002 (DEL-08-07 interface verification gap).

### C5: Effort and Integration Surface

PLAN Section 3.1 rates effort as "Medium" and identifies three integration points:
1. PREPARATION (hash computation on scaffold)
2. ORCHESTRATOR (hash verification before pipeline runs)
3. Tooling (standalone hash generation/verification scripts)

**Effort justification (ASSUMPTION -- sizing is estimated, not measured):**
- **File count:** Estimated 3--5 new source files (hash computation module, verification module, standalone CLI wrapper, schema extension documentation, integration guide).
- **Integration touch-points:** Three agent boundaries (PREPARATION, ORCHESTRATOR, standalone tooling), each requiring instruction updates and workflow integration. The PREPARATION and ORCHESTRATOR changes touch DEL-06-02 (Local Deliverable Workflow Agents), creating a cross-deliverable coordination requirement.
- **Test surface:** At least 7 verification checks (see Specification Verification table), plus backward compatibility testing.
- **Why "Medium" rather than "Small":** The cross-agent integration (PREPARATION + ORCHESTRATOR) and the need for a canonical hash format that works across standalone scripts and agent contexts pushes this beyond a simple single-module task. However, the core algorithm (SHA-256 of file content) is straightforward with standard library support, keeping it below "Large."

**Source:** PLAN Section 3.1.

**Lensing provenance:** F-003 (RationaleGap -- effort rating lacked concrete sizing).

### C6: Hash Computation Timing -- Terminology Clarification

The hash computation timing has been described with varying terminology across sources:

- Decomposition / PLAN Section 3.1: "hash computation on scaffold"
- Specification REQ-01: "during PREPARATION workspace scaffolding"
- Earlier drafts used: "PREPARATION scaffold time," "time of context sealing or scaffold creation"

**Clarification:** These terms refer to the same event sequence. PREPARATION workspace scaffolding includes writing reference entries to `_REFERENCES.md` and then computing hashes for those references. "Context sealing" refers to the point at which the deliverable's input context is considered fixed for a given pipeline run. Hash computation occurs **during scaffolding, before sealing is complete** -- that is, hashes are part of the seal, not computed after it.

The canonical description is: "Hashes are computed during PREPARATION workspace scaffolding, after reference entries are written and before the deliverable context is considered sealed."

**Lensing provenance:** B-003 (Normalization -- hash computation timing terminology inconsistency).

### C7: FIPS 180-4 and Standard Library Compliance

The SHA-256 algorithm is specified by FIPS 180-4 (NIST). The full standard text is not available in the project's accessible references. However, the accepted approach to FIPS 180-4 compliance for this deliverable is:

- **Use standard library implementations** (e.g., Node.js `crypto.createHash('sha256')` or Python `hashlib.sha256()`) which implement FIPS 180-4 internally.
- **Do not implement SHA-256 from scratch.** Standard library implementations are well-tested, widely audited, and sufficient for this integrity verification use case.
- **If formal FIPS 180-4 conformance certification is ever required** (unlikely for this project's scope), that would require a separate evaluation beyond this deliverable's current scope.

**Source:** FIPS 180-4 (location TBD); standard library documentation for Node.js `crypto` and Python `hashlib`.

**Lensing provenance:** C-001 (MissingSlot -- FIPS 180-4 accessibility gap).

### C8: Security Model and Threat Rationale

This deliverable is typed `SECURITY_CONTROL`. The specific threat model it addresses:

**Threat: Undetected reference content mutation ("ghost inputs").** Between the time a human approves a deliverable's context (including its referenced documents) and the time an agent pipeline executes against that context, the content of out-of-folder referenced files could change. This change could be:
- **Accidental:** Another process or human modifies a shared reference file without awareness of downstream consumers.
- **Uncoordinated:** A reference file is intentionally updated, but consumers are not notified, leading to pipeline runs against stale or inconsistent assumptions.

**What hash verification mitigates:**
- Detects content mutation between seal time and execution time.
- Forces human acknowledgment before proceeding with changed inputs (when block policy is active).
- Creates an audit trail of integrity state at each pipeline execution point.

**What hash verification does NOT mitigate:**
- Malicious tampering by an actor who also controls the hash store (the hash and content are co-located; this is integrity verification, not tamper-proof security).
- Content changes within in-folder files (covered by git SHA tracking).
- Semantic correctness of referenced content (hashes verify identity, not quality).

This threat model aligns with K-GHOST-1 (no ghost inputs), K-PROV-1 (provenance tracking), and the DIRECTIVE Section 2.4 principle (Evidence Over Plausibility).

**Source:** CONTRACT K-GHOST-1; PLAN Section 3.1; DIRECTIVE Section 2.4. ASSUMPTION: the threat model scope (accidental/uncoordinated mutation, not malicious tampering) is inferred from the project's overall security posture as a local-execution development tool.

**Lensing provenance:** E-002 (RationaleGap -- security/threat model absent despite SECURITY_CONTROL type).

## Trade-offs

| Trade-off | Option A | Option B | Current Leaning | Rationale |
|-----------|----------|----------|-----------------|-----------|
| Hash storage | Inline in `_REFERENCES.md` | Companion file | Inline (ASSUMPTION) | Fewer files; co-located with reference entries; aligns with filesystem-as-state |
| Verification failure | Block pipeline | Warn and continue | Block (ASSUMPTION) | Stronger K-GHOST-1 alignment; the human should decide, not be bypassed |
| Hash algorithm | SHA-256 | Other (SHA-512, BLAKE3, etc.) | SHA-256 | Explicitly specified in decomposition; widely supported; sufficient for integrity verification |
| Scope boundary | All references | Out-of-folder only | Out-of-folder only | In-folder content is already git-tracked; avoids redundancy |
| Hash output format | Lowercase hex (no prefix) | Prefixed (e.g., `sha256:...`) | Lowercase hex, no prefix (ASSUMPTION) | Simplest interoperable format; prefix adds parsing complexity without clear benefit for single-algorithm use |

## Examples

### Example 1: `_REFERENCES.md` with ContentHash fields

Below is a candidate example of a `_REFERENCES.md` file after hash extension (ASSUMPTION -- exact schema pending DEC-HASH-001 ruling).

```markdown
# References -- DEL-XX-YY

## Decomposition

- [Decomposition Document](../../../_Decomposition/ChiralityApp_SoftwareDecomposition_2026-02-21_G7-APPROVED.md)
  - ContentHash: a3f2b8c1d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1

## Package References

- [PLAN Section 3.1](../../../../docs/PLAN.md)
  - ContentHash: b4c3d2e1f0a9b8c7d6e5f4a3b2c1d0e9f8a7b6c5d4e3f2a1b0c9d8e7f6a5b4c3

## Deliverable-Specific References

- [CONTRACT K-GHOST-1](../../../../docs/CONTRACT.md)
  - ContentHash: c5d4e3f2a1b0c9d8e7f6a5b4c3d2e1f0a9b8c7d6e5f4a3b2c1d0e9f8a7b6c5d4
```

**Note:** Hash values shown are illustrative placeholders. Actual hashes would be computed from file content at scaffold time.

**Source:** Specification REQ-01, REQ-01-FMT, REQ-02; Guidance C1.

### Example 2: Verification command and output

```bash
# Standalone verification (REQ-07)
$ chirality-hash verify --path ./execution/PKG-08_Optional_Integrity_Hardening/1_Working/DEL-08-01_References_Content_Hashes/_REFERENCES.md

Verifying content hashes for DEL-08-01...
  [PASS] ../../../_Decomposition/ChiralityApp_SoftwareDecomposition_2026-02-21_G7-APPROVED.md
  [FAIL] ../../../../docs/PLAN.md
         Stored:  b4c3d2e1f0a9b8c7d6e5f4a3b2c1d0e9f8a7b6c5d4e3f2a1b0c9d8e7f6a5b4c3
         Current: e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b3c4d5e6f7
  [PASS] ../../../../docs/CONTRACT.md

Result: FAIL (1 of 3 references mismatched)
Exit code: 1
```

**Note:** Command name and output format are illustrative. Actual CLI interface is TBD pending implementation.

**Source:** Specification REQ-03, REQ-07; Guidance P1.

**Lensing provenance:** D-002 (WeakStatement -- Examples section was TBD; populated with concrete illustrations).

## Conflict Table (for human ruling)

No unresolved conflicts detected at this time. The following items require human policy decisions but are not source-to-source conflicts:

| Decision ID | Decision Needed | Impacted Sections | Related Sources |
|-------------|-----------------|-------------------|-----------------|
| DEC-HASH-001 | Hash storage location: inline in `_REFERENCES.md` vs. companion file | Specification REQ-02; Guidance C1 | SPEC Section 7; PLAN Section 3.1 |
| DEC-HASH-002 | Verification failure policy: block vs. warn | Specification REQ-03, REQ-05; Guidance C2 | CONTRACT K-GHOST-1; PLAN Section 3.1 |
| DEC-HASH-003 | SOW-032 scope activation: flip IN or retire | All sections (deliverable is conditional on scope activation) | Decomposition OI-032 |
