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
| **Scope Status** | IN (SCA-002 resolved on 2026-02-24) |

## Attributes

| Attribute | Value | Source |
|-----------|-------|--------|
| Hash Algorithm | SHA-256 | Decomposition (DEL-08-01 description); PLAN Section 3.1 |
| Hash Output Format | Lowercase hexadecimal string, 64 characters (ASSUMPTION -- standard SHA-256 hex encoding; see Specification REQ-01) | FIPS 180-4 standard practice (location TBD) |
| Hash Target | Out-of-folder references listed in `_REFERENCES.md` | Decomposition (DEL-08-01 description); PLAN Section 3.1 |
| Verification Trigger | Before pipeline runs | Decomposition (DEL-08-01 description); PLAN Section 3.1 |
| Hash Computation Point | During PREPARATION workspace scaffolding, after reference entries are written and before the deliverable context is considered sealed (see Guidance C6 for terminology clarification) | PLAN Section 3.1 |
| Hash Storage Location | Within `_REFERENCES.md` file (`ContentHash` nested bullet field for out-of-folder references) | Implemented via `execution/_Scripts/references_hash_tool.py` and documented in `docs/SPEC.md` Section 7 |
| Verification Enforcement Point | ORCHESTRATOR (before pipeline runs) | PLAN Section 3.1 |
| Anticipated Artifacts | CODE, SCRIPT, DOC | Decomposition (DEL-08-01) |
| Implementation Language/Runtime | Python 3.8+ (`hashlib.sha256`) | `execution/_Scripts/references_hash_tool.py` |

## Conditions

| Condition | Description | Source |
|-----------|-------------|--------|
| Scope Activation | SOW-032 is IN (deliverable fully actionable) | SCA-002 (2026-02-24) |
| No-Ghost-Input Alignment | Content hashes support K-GHOST-1 enforcement by verifying that referenced content has not changed since context sealing | CONTRACT K-GHOST-1; PLAN Section 3.1 |
| Provenance Alignment | Hashes complement K-PROV-1 by adding integrity verification to provenance tracking | CONTRACT K-PROV-1; PLAN Section 3.1 |
| Dirty Detection Alignment | Hash verification contributes to K-VAL-1 dirty detection (changed inputs since last approved SHA) | CONTRACT K-VAL-1 |
| In-Folder vs Out-of-Folder | Only out-of-folder references require hashing; in-folder files are covered by git SHA tracking | PLAN Section 3.1 (specifies "out-of-folder references") |

## Construction

| Component | Description | Status |
|-----------|-------------|--------|
| Hash Computation Module | Code/script to compute SHA-256 hashes for referenced files | `execution/_Scripts/references_hash_tool.py` (`compute` / `recompute`) |
| `_REFERENCES.md` Schema Extension | Extended format to store hash values alongside reference entries | `docs/SPEC.md` Section 7; `agents/AGENT_PREPARATION.md` `_REFERENCES.md` schema |
| Verification Script | Script or module to verify stored hashes against current file content | `execution/_Scripts/references_hash_tool.py` (`verify`) |
| PREPARATION Integration | Changes to PREPARATION agent to compute hashes during scaffold | `agents/AGENT_PREPARATION.md` Task Type C/F Step 5 |
| ORCHESTRATOR Integration | Changes to ORCHESTRATOR to verify hashes before pipeline execution | `agents/AGENT_ORCHESTRATOR.md` Phase 2.1a |
| Documentation | Usage documentation for hash computation and verification workflow | `execution/_Scripts/README.md` |

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
