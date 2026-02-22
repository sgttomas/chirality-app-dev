# Datasheet -- DEL-08-01

## Identification

| Field | Value |
|-------|-------|
| **DeliverableID** | DEL-08-01 |
| **Name** | `_REFERENCES.md` Content Hashes + Verification |
| **PackageID** | PKG-08 |
| **Package** | Optional Integrity Hardening |
| **Type** | SECURITY_CONTROL |
| **ContextEnvelope** | M |
| **ResponsibleParty** | TBD (resolution: human assignment required before implementation begins) |
| **Scope Coverage** | SOW-032 |
| **Objectives** | OBJ-007 (ASSUMPTION -- best-effort mapping via PKG-08 package grouping) |
| **Scope Status** | TBD (SOW-032 has not yet been flipped IN; see Open Issue OI-032) |

## Attributes

| Attribute | Value | Source |
|-----------|-------|--------|
| Hash Algorithm | SHA-256 | Decomposition (DEL-08-01 description); PLAN Section 3.1 |
| Hash Output Format | Lowercase hexadecimal string, 64 characters (ASSUMPTION -- standard SHA-256 hex encoding; see Specification REQ-01) | FIPS 180-4 standard practice (location TBD) |
| Hash Target | Out-of-folder references listed in `_REFERENCES.md` | Decomposition (DEL-08-01 description); PLAN Section 3.1 |
| Verification Trigger | Before pipeline runs | Decomposition (DEL-08-01 description); PLAN Section 3.1 |
| Hash Computation Point | During PREPARATION workspace scaffolding, after reference entries are written and before the deliverable context is considered sealed (see Guidance C6 for terminology clarification) | PLAN Section 3.1 |
| Hash Storage Location | Within `_REFERENCES.md` file (ASSUMPTION -- co-located with reference entries) | TBD (pending design decision DEC-HASH-001) |
| Verification Enforcement Point | ORCHESTRATOR (before pipeline runs) | PLAN Section 3.1 |
| Anticipated Artifacts | CODE, SCRIPT, DOC | Decomposition (DEL-08-01) |
| Implementation Language/Runtime | TBD (pending decision based on repo tooling conventions; candidates: Node.js `crypto` module, Python `hashlib`) | Procedure Phase 2 Step 2.1 item 3 |

## Conditions

| Condition | Description | Source |
|-----------|-------------|--------|
| Scope Activation | SOW-032 must be flipped to IN before this deliverable is fully actionable | Decomposition Scope Ledger (SOW-032 status = TBD); Open Issue OI-032 |
| No-Ghost-Input Alignment | Content hashes support K-GHOST-1 enforcement by verifying that referenced content has not changed since context sealing | CONTRACT K-GHOST-1; PLAN Section 3.1 |
| Provenance Alignment | Hashes complement K-PROV-1 by adding integrity verification to provenance tracking | CONTRACT K-PROV-1; PLAN Section 3.1 |
| Dirty Detection Alignment | Hash verification contributes to K-VAL-1 dirty detection (changed inputs since last approved SHA) | CONTRACT K-VAL-1 |
| In-Folder vs Out-of-Folder | Only out-of-folder references require hashing; in-folder files are covered by git SHA tracking | PLAN Section 3.1 (specifies "out-of-folder references") |

## Construction

| Component | Description | Status |
|-----------|-------------|--------|
| Hash Computation Module | Code/script to compute SHA-256 hashes for referenced files | TBD |
| `_REFERENCES.md` Schema Extension | Extended format to store hash values alongside reference entries | TBD |
| Verification Script | Script or module to verify stored hashes against current file content | TBD |
| PREPARATION Integration | Changes to PREPARATION agent to compute hashes during scaffold | TBD |
| ORCHESTRATOR Integration | Changes to ORCHESTRATOR to verify hashes before pipeline execution | TBD |
| Documentation | Usage documentation for hash computation and verification workflow | TBD |

## References

| Reference | Relevance |
|-----------|-----------|
| Decomposition (G7-APPROVED) | DEL-08-01 entry: description, scope, type, artifacts |
| docs/PLAN.md Section 3.1 | Content hash feature description, rationale, effort estimate |
| docs/CONTRACT.md (K-GHOST-1) | No-ghost-input invariant that content hashes support |
| docs/CONTRACT.md (K-PROV-1) | Provenance invariant complemented by integrity hashes |
| docs/CONTRACT.md (K-VAL-1) | Dirty detection invariant supported by hash comparison |
| docs/SPEC.md Section 7 | Current `_REFERENCES.md` format specification |
| docs/DIRECTIVE.md Section 2.4 | Evidence Over Plausibility design principle |
| FIPS 180-4 (NIST) | SHA-256 algorithm specification (location TBD -- standard library implementations serve as accepted proxy; see Guidance C7) |
