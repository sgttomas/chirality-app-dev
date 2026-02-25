# Specification -- DEL-06-05 Governance Coherence + Guardrails (OUT boundaries)

## Scope

### Included

This deliverable covers two complementary concerns:

1. **Governance coherence (SOW-030):** Ensure the five governance documents (`DIRECTIVE.md`, `CONTRACT.md`, `SPEC.md`, `TYPES.md`, `PLAN.md`) remain internally aligned on the core model. Internal alignment means consistent hierarchy definitions, consistent vocabulary, consistent invariant references, and no contradictory statements across documents.

2. **OUT-boundary guardrails (SOW-039 through SOW-043):** Ensure the five explicit OUT-of-scope boundaries remain documented, visible, and enforceable. The OUT boundaries prohibit: automated approval/issuance, financial transactions, safety-critical decisions without human review, replacement of professional judgment, and external system integration (with the Anthropic API exception per DEC-NET-001).

Source: Decomposition DEL-06-05 row; `_CONTEXT.md`

### Excluded

- Structural conformance of agent instruction files (covered by DEL-06-01).
- Local deliverable workflow agent documentation (covered by DEL-06-02).
- Cross-deliverable workflow support (covered by DEL-06-03).
- Change management and git hygiene (covered by DEL-06-04).
- Runtime enforcement implementation of guardrails in code (covered by PKG-03 deliverables, particularly DEL-03-04 for subagent governance and DEL-03-06 for network guardrails).

**Note (X-001):** The excluded deliverables listed above cover adjacent governance concerns. For scope-completeness, the boundary between DEL-06-05 and each excluded deliverable should be confirmed bidirectionally during WORKING_ITEMS (i.e., those deliverables should acknowledge what DEL-06-05 covers from their side). This is a **future coherence check** -- not a blocking requirement for this deliverable. Source: **ASSUMPTION: bidirectional scope confirmation inferred from the exhaustive-governance-scope lens; no explicit cross-deliverable scope-acknowledgment requirement exists in the decomposition.**

## Requirements

### REQ-COH-01: Cross-document hierarchy consistency

The governance documents MUST use a consistent hierarchy model: flat `package -> deliverable` with no nesting, no phases layer, and no sub-package levels.

- **Verification:** Check that TYPES Section 1, SPEC Sections 1-2, CONTRACT K-HIER-1, and DIRECTIVE Section 5 (`Structural Constraints` -> `Flat package hierarchy`) all describe the same flat hierarchy.
- **Source:** `docs/PLAN.md` Section 1 ("Governance Alignment"); `docs/CONTRACT.md` K-HIER-1; `docs/TYPES.md` Section 1

### REQ-COH-02: Cross-document vocabulary consistency

Canonical terms defined in `docs/TYPES.md` MUST be used consistently across all governance documents. Where a term is used differently, `docs/TYPES.md` governs.

- **Verification:** Verify the following minimum term set across all five governance documents: deliverable, package, lifecycle states (OPEN, INITIALIZED, SEMANTIC_READY, IN_PROGRESS, CHECKING, ISSUED), dependency classes (ANCHOR, EXECUTION), agent types (Type 0, Type 1, Type 2), artifact. For each term, confirm usage matches `docs/TYPES.md` definitions. Flag any document that uses a term with a different meaning. **(A-003/X-002 enrichment: replaces open-ended "spot-check" with defined minimum verification scope.)**
- **Source:** `docs/TYPES.md` preamble ("All agents and governance documents use the terms defined here. Where a term is used differently, this document governs.")

### REQ-COH-03: Invariant catalog is single-source

All binding invariants (`K-*`) MUST be defined in `docs/CONTRACT.md` and only in `docs/CONTRACT.md`. Other documents may reference invariants but MUST NOT define new ones or redefine existing ones with different semantics.

- **Verification:** Search all governance documents for `K-` identifiers; confirm they reference CONTRACT, not redefine.
- **Source:** `docs/PLAN.md` Section 1 ("Invariant catalog is centralized in `docs/CONTRACT.md`")

### REQ-COH-04: Lifecycle state consistency

Lifecycle states and their transition rules MUST be defined consistently between `docs/TYPES.md` Section 5 and `docs/SPEC.md` Section 3. The state sequence, state meanings, and authorized transition actors MUST agree.

- **Verification:** Compare TYPES Section 5 state table with SPEC Section 3 state table; confirm identical states, meanings, and transitions.
- **Source:** `docs/TYPES.md` Section 5; `docs/SPEC.md` Section 3

### REQ-COH-05: File-based authoritative state consistency

The principle that authoritative execution state is file-based MUST be stated consistently in DIRECTIVE (Section 2.1 "Filesystem Is the Database"), SPEC (Section 2 deliverable folder layout), and CONTRACT (K-STATUS-1, K-DEP-1).

- **Verification:** Confirm that DIRECTIVE, SPEC, and CONTRACT all assert file-based state authority without contradiction.
- **Source:** `docs/PLAN.md` Section 1 ("Authoritative execution state is file-based")

### REQ-COH-06: Coherence review periodicity (C-001 enrichment)

Governance coherence review SHALL be triggered by at least the following events:
- (a) Any governance document (`docs/DIRECTIVE.md`, `docs/CONTRACT.md`, `docs/SPEC.md`, `docs/TYPES.md`, `docs/PLAN.md`) is modified.
- (b) A new decomposition revision is approved.
- (c) A periodic review interval has elapsed (interval to be determined by human -- TBD).

- **Verification:** Confirm that the Procedure specifies these trigger conditions and that they are included in the Prerequisites or Purpose section.
- **Source:** **ASSUMPTION: trigger conditions inferred from the nature of coherence verification (coherence can only drift when documents change or time passes). No explicit periodicity requirement exists in the current governance documents.**

### REQ-GR-01: OUT boundaries are documented in DIRECTIVE

Each OUT-of-scope item (SOW-039 through SOW-043) MUST appear in `docs/DIRECTIVE.md` Section 4.2 ("Out of Scope") as an explicit boundary statement.

- **Verification:** Confirm each guardrail has a matching entry in DIRECTIVE Section 4.2.
- **Current status:** All five OUT items are present in DIRECTIVE Section 4.2. (Verified during document generation from `docs/DIRECTIVE.md`.)
- **Source:** `docs/DIRECTIVE.md` Section 4.2

### REQ-GR-02: Automated approval guardrail has invariant backing (SOW-039)

The prohibition on automated approval or issuance by agents MUST be backed by at least one CONTRACT invariant with a defined enforcement point.

- **Verification:** Confirm K-AUTH-1 exists in CONTRACT and covers the automated-approval boundary.
- **Current status:** K-AUTH-1 states "Only humans author binding approval records. No agent may claim to certify, approve, sign, seal, or issue work for reliance." Enforcement: agent instruction constraints + human review. (Verified from `docs/CONTRACT.md` Section 1.2.)
- **Source:** `docs/CONTRACT.md` Section 1.2 (K-AUTH-1)

### REQ-GR-03: Safety-critical decision guardrail has process backing (SOW-041)

The prohibition on safety-critical decisions without human review MUST be backed by both DIRECTIVE's professional responsibility model (Section 3) and CONTRACT's sealing/authority invariants (K-SEAL-1, K-AUTH-1).

- **Verification:** Confirm DIRECTIVE Section 3 addresses safety-critical human review; confirm K-SEAL-1 requires human seal before Type 2 execution; confirm K-AUTH-1 restricts agent approval authority.
- **Source:** `docs/DIRECTIVE.md` Section 3; `docs/CONTRACT.md` Sections 1.2-1.3

### REQ-GR-04: External integration guardrail acknowledges the Anthropic API exception (SOW-043)

The OUT boundary for external system integration MUST acknowledge the narrow Anthropic API exception per DEC-NET-001. The exception MUST be scoped to outbound API calls only, with no other external connections permitted.

- **Verification:** Confirm DIRECTIVE Section 4.2 lists external integration as out-of-scope; confirm decomposition DEC-NET-001 scopes the exception to Anthropic API only; confirm these are not contradictory.
- **Current status:** DIRECTIVE Section 4.2 lists "External system integration (databases, APIs, cloud services)" as out of scope. Decomposition DEC-NET-001 carves a narrow exception: "Outbound internet access is permitted only for Anthropic API calls." The Scope Ledger entry for SOW-043 notes "Exception: Anthropic API only." These are consistent. (Verified from `docs/DIRECTIVE.md` Section 4.2; Decomposition Decision Log DEC-NET-001; Scope Ledger SOW-043.)
- **Source:** `docs/DIRECTIVE.md` Section 4.2; Decomposition DEC-NET-001

### REQ-GR-05: Financial and professional-judgment guardrails are documented (SOW-040, SOW-042)

The OUT boundaries for financial transactions (SOW-040) and replacement of professional judgment (SOW-042) MUST appear in DIRECTIVE and remain unambiguous.

- **Verification:** Confirm DIRECTIVE Section 4.2 lists both boundaries.
- **Current status:** Both are present in DIRECTIVE Section 4.2. (Verified from `docs/DIRECTIVE.md`.)
- **Source:** `docs/DIRECTIVE.md` Section 4.2

### REQ-GR-06: Agent instruction constraints as enforcement layer (F-002 enrichment)

Agent instruction files (`agents/AGENT_*.md`) that govern agents with write access to governance-adjacent artifacts MUST include explicit write-scope constraints that prevent violation of OUT-boundary guardrails (SOW-039 through SOW-043).

- **Verification:** For each agent type with write access to governance or deliverable artifacts, confirm that the agent's instruction file includes a write-scope section that prohibits actions inconsistent with OUT-boundary guardrails. At minimum: confirm agents cannot auto-approve (SOW-039) and cannot bypass human review gates (SOW-041).
- **Source:** Guidance P3 identifies four enforcement layers (documentation, invariant backing, agent instruction constraints, runtime enforcement). This requirement covers the "agent instruction constraints" layer. **ASSUMPTION: the requirement is inferred from Guidance P3's enforcement layer model; no explicit requirement for agent instruction verification exists in the current governance documents.** See also `docs/SPEC.md` Section 9 (agent instruction file structure) and `docs/CONTRACT.md` K-AUTH-1 enforcement points.

### REQ-TRACE-01: Scope ledger traceability

Every scope item assigned to this deliverable (SOW-030, SOW-039--SOW-043) MUST appear in the decomposition Scope Ledger with `PackageID=PKG-06` and `DeliverableID(s)` including `DEL-06-05`.

- **Verification:** Check Scope Ledger rows for each scope item.
- **Current status:** All six scope items are mapped to DEL-06-05 in the Scope Ledger. (Verified from Decomposition Scope Ledger.)
- **Source:** Decomposition (Scope Ledger)

## Standards

| Standard/Document | Role | Accessibility |
|-------------------|------|---------------|
| `docs/DIRECTIVE.md` | Defines founding intent, out-of-scope boundaries, professional responsibility model | Accessible (read during generation) |
| `docs/CONTRACT.md` | Defines binding invariants and enforcement map | Accessible (read during generation) |
| `docs/SPEC.md` | Defines physical structures and file formats | Accessible (read during generation) |
| `docs/TYPES.md` | Defines canonical vocabulary and lifecycle | Accessible (read during generation) |
| `docs/PLAN.md` | Defines governance alignment status and roadmap | Accessible (read during generation) |
| Decomposition (G7-APPROVED) | Defines scope items, objectives, and deliverable assignments | Accessible (read during generation) |

## Verification

| Requirement | Verification Approach | Pass Criteria |
|-------------|----------------------|---------------|
| REQ-COH-01 | Manual cross-document review (DIRECTIVE Section 5 structural constraints) | Hierarchy is described identically (flat package->deliverable) in TYPES, SPEC, CONTRACT, and DIRECTIVE |
| REQ-COH-02 | Enumerated term verification: check deliverable, package, lifecycle states, dependency classes, agent types, artifact across all governance docs | All terms in the minimum term set match TYPES definitions; no contradictory usage found |
| REQ-COH-03 | Search governance docs for `K-` patterns | All `K-*` identifiers defined only in CONTRACT; others reference only |
| REQ-COH-04 | Side-by-side comparison of TYPES Section 5 and SPEC Section 3 | States, meanings, and transitions match |
| REQ-COH-05 | Cross-document assertion check | DIRECTIVE, SPEC, and CONTRACT all assert file-based authority consistently |
| REQ-COH-06 | Confirm Procedure includes trigger conditions | At least three trigger types (document change, decomposition revision, periodic interval) are specified |
| REQ-GR-01 | Confirm DIRECTIVE Section 4.2 entries | All five OUT items present |
| REQ-GR-02 | Confirm K-AUTH-1 in CONTRACT | Invariant exists with enforcement point |
| REQ-GR-03 | Confirm DIRECTIVE Section 3 + CONTRACT K-SEAL-1, K-AUTH-1 | Both process and invariant backing present |
| REQ-GR-04 | Confirm DIRECTIVE + DEC-NET-001 consistency | Exception acknowledged, scoped, non-contradictory |
| REQ-GR-05 | Confirm DIRECTIVE Section 4.2 entries | Both guardrails present and unambiguous |
| REQ-GR-06 | Agent instruction file review | Write-scope constraints present in governance-adjacent agent instructions; no SOW-039/SOW-041 violations possible |
| REQ-TRACE-01 | Scope Ledger row check | All six SOW items mapped to PKG-06 / DEL-06-05 |

## Documentation

### Required artifacts

| Artifact | Description | Source |
|----------|-------------|--------|
| Governance coherence assessment (within this doc kit) | Confirmation that the five governance docs are internally aligned | `_CONTEXT.md` (anticipated artifacts: DOC) |
| Guardrail inventory (within Datasheet) | Table mapping each OUT-of-scope item to its enforcement mechanism | DEL-06-05 description |
