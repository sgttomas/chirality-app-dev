# Guidance -- DEL-06-05 Governance Coherence + Guardrails (OUT boundaries)

## Purpose

This deliverable exists to ensure that the Chirality governance suite remains internally consistent and that OUT-of-scope boundaries stay explicit and enforceable. As the system evolves, governance documents may drift -- new invariants may be added to CONTRACT without updating TYPES, or SPEC may introduce structures that conflict with DIRECTIVE constraints. This deliverable provides the review mechanism that detects and corrects such drift.

The OUT-boundary guardrails exist because the system is designed to support professional responsibility, not replace it. Automated approval, financial commitments, unsupervised safety-critical decisions, replacement of professional judgment, and unbounded external integration would undermine the core design philosophy. These boundaries are foundational constraints, not temporary limitations.

Source: `docs/DIRECTIVE.md` Sections 1-4; Decomposition DEL-06-05 description

## Principles

### P1: Coherence is a cross-cutting concern

Governance coherence is not owned by any single document. It is the property that emerges when all five governance documents (DIRECTIVE, CONTRACT, SPEC, TYPES, PLAN) describe the same system consistently. When a change is made to any governance document, the coherence of the entire suite must be re-verified.

Source: `docs/PLAN.md` Section 1 ("Governance Alignment")

### P2: OUT boundaries are design decisions, not omissions

The five OUT-of-scope items (SOW-039 through SOW-043) are deliberate design constraints rooted in the founding intent. They are not features deferred for later -- they are boundaries that define what the system fundamentally is not. Changes to these boundaries require human decision with full understanding of the implications.

Source: `docs/DIRECTIVE.md` Section 4.2; Section 2.3 ("Human Authority at Every Gate")

### P3: Guardrails require multiple enforcement layers

A guardrail documented only in DIRECTIVE is a statement of intent. To be effective, guardrails should have:
- **Documentation:** explicit listing in DIRECTIVE Section 4.2
- **Invariant backing:** where applicable, a CONTRACT `K-*` invariant with enforcement points
- **Agent instruction constraints:** write scopes and behavioral constraints in agent instructions (see REQ-GR-06 in Specification for the verification requirement covering this layer)
- **Runtime enforcement:** where applicable, code-level enforcement (e.g., subagent governance fail-closed)

Not all guardrails require all layers. SOW-040 (no financial transactions) has no runtime enforcement because the system has no financial capabilities to constrain. SOW-039 (no automated approval) has multiple layers: DIRECTIVE, K-AUTH-1, agent instruction constraints, and human review gates.

Source: `docs/CONTRACT.md` Section 2 (Enforcement Map Summary); **ASSUMPTION: the multi-layer enforcement model is inferred from the pattern in CONTRACT's enforcement map, not explicitly stated as a design principle.**

### P4: The Anthropic API exception is narrow and bounded

DEC-NET-001 permits outbound internet access only for Anthropic API calls. This is not a general relaxation of the external integration boundary (SOW-043). The exception is scoped to:
- Outbound API calls to the Anthropic API only
- No other outbound connections (telemetry, update checks, other endpoints)
- No inbound connections

The exception exists because AI agent execution requires API access to the model provider. It does not establish a pattern for future integrations.

Source: Decomposition Decision Log DEC-NET-001; Scope Ledger SOW-043 notes

## Considerations

### C1: Coherence verification is currently manual

There is no automated tooling to verify cross-document coherence. Verification depends on human review (or agent-assisted review during WORKING_ITEMS sessions). This is appropriate for the current scale (five documents), but may need tooling if the governance suite grows.

Source: **ASSUMPTION: inferred from the absence of coherence-checking tooling in `docs/PLAN.md` Section 3 (future hardening candidates).**

### C2: Guardrail enforcement depth varies by boundary

| Guardrail | Documentation | Invariant | Agent Instructions | Runtime Code |
|-----------|--------------|-----------|-------------------|-------------|
| SOW-039 (no auto-approval) | DIRECTIVE 4.2 | K-AUTH-1 | Write scope constraints | Human review gates |
| SOW-040 (no financial) | DIRECTIVE 4.2 | -- | -- | -- (no financial capability exists) |
| SOW-041 (no safety-critical without review) | DIRECTIVE 3, 4.2 | K-AUTH-1, K-SEAL-1 | Seal check | Subagent governance fail-closed |
| SOW-042 (no replacing judgment) | DIRECTIVE 3, 4.2 | -- | -- | -- (addressed by professional responsibility model) |
| SOW-043 (no external integration) | DIRECTIVE 4.2 | -- | -- | Network guardrails (DEL-03-06) |

**Enforcement depth rationale (D-001 enrichment):** The enforcement depth is not uniform by design. Guardrails SOW-040 and SOW-042 have only a single enforcement layer (DIRECTIVE documentation) because:

- **SOW-040 (no financial):** The system has no financial capabilities to constrain. There is no payment API, no transaction mechanism, and no wallet or account integration. Adding a CONTRACT invariant or runtime check would guard against a capability that does not exist. If financial capabilities were ever introduced (which would require a scope change flipping SOW-040 from OUT to IN), invariant and runtime enforcement would be required at that time.
- **SOW-042 (no replacing judgment):** This boundary is inherently about human agency in professional contexts, which cannot be enforced through code or invariants alone. The professional responsibility model in DIRECTIVE Section 3 establishes the principle; enforcement is structural (the system presents analysis for human consideration rather than making decisions on behalf of the human). Adding a runtime check is not meaningful because the boundary is about the nature of the human-system relationship, not about a specific technical action.

Single-layer enforcement for these two guardrails is a conscious design choice: enforcement layers should match the nature of the boundary. Guardrails with technical enforcement points (SOW-039, SOW-041, SOW-043) have correspondingly technical enforcement layers. Source: `docs/CONTRACT.md` Sections 1.2-1.3 (enforcement map pattern); `docs/DIRECTIVE.md` Sections 3-4. **ASSUMPTION: the rationale for single-layer acceptability is inferred from the system architecture and the nature of each boundary; it is not explicitly stated in any governance document.**

### C3: Governance documents serve different audiences

| Document | Primary Audience | Register |
|----------|-----------------|----------|
| DIRECTIVE | Project stakeholders; anyone asking "why does this system exist and what are its boundaries?" | Foundational / philosophical |
| CONTRACT | Agent developers; anyone needing to know "what MUST the system always do or never do?" | Normative / enforceable |
| SPEC | Implementers; anyone asking "what do the files look like and how are they structured?" | Technical / structural |
| TYPES | Everyone; the shared vocabulary reference | Definitional / canonical |
| PLAN | Decision-makers; anyone asking "what is built and what could be built next?" | Descriptive / planning |

Source: Derived from each document's stated purpose. `docs/DIRECTIVE.md` preamble; `docs/CONTRACT.md` preamble; `docs/SPEC.md` preamble; `docs/TYPES.md` preamble; `docs/PLAN.md` preamble.

### C4: Invariant relevance traceability (E-001 enrichment)

The Datasheet lists 10 CONTRACT invariants as relevant to this deliverable. Of these, five (K-HIER-1, K-AUTH-1, K-SEAL-1, K-STATUS-1, K-DEP-1) are directly traced to Specification requirements. The remaining five (K-AUTH-2, K-BIND-1, K-INVENT-1, K-CONFLICT-1, K-WRITE-1) are listed as contextually relevant because their domain (authority, binding, invention prohibition, conflict resolution, write scope) intersects with the governance coherence and guardrail enforcement mission.

The contextually relevant invariants do not currently have dedicated requirements in the Specification. Whether they should be elevated to explicit requirements depends on:
- Whether the coherence review should verify that these invariants are correctly referenced across documents (expanding REQ-COH-03's scope), or
- Whether their relevance is limited to informing the reviewer's understanding of the governance context.

This is a design decision for the human during WORKING_ITEMS. See the Datasheet's invariant relevance mapping table for details.

Source: `docs/CONTRACT.md`; Datasheet (Invariant relevance mapping). **ASSUMPTION: the contextual-relevance classification is inferred from invariant naming conventions and governance domain analysis; the exact text of K-AUTH-2, K-BIND-1, K-INVENT-1, K-CONFLICT-1, and K-WRITE-1 should be confirmed.**

## Trade-offs

### T1: Guardrail granularity vs. document weight

More granular guardrail documentation (e.g., one CONTRACT invariant per OUT boundary) would provide stronger enforcement traceability. However, not all OUT boundaries warrant invariants. SOW-040 (no financial transactions) is adequately addressed by the absence of financial capabilities -- adding an invariant would add governance weight without enforcement value. Similarly, SOW-042 (no replacing professional judgment) is addressed by the professional responsibility model in DIRECTIVE, which operates at a conceptual level that an invariant cannot meaningfully encode.

**Current approach:** Invariants exist for boundaries that require active enforcement (K-AUTH-1 for approval, K-SEAL-1 for context sealing). Boundaries that are addressed by system design absence (no financial capability, no external integration capability) rely on DIRECTIVE documentation. This is a deliberate trade-off: governance weight is applied proportionally to enforcement value. **(A-002 enrichment: strengthened rationale for SOW-040/SOW-042 single-layer enforcement.)**

Source: `docs/CONTRACT.md` Section 2 (Enforcement Map Summary); **ASSUMPTION: this trade-off is inferred from the current state of CONTRACT (which has invariants for some but not all OUT boundaries).**

### T2: Centralized vs. distributed coherence checking

Coherence could be verified centrally (a single coherence report) or distributedly (each document self-checks against others). The current model is distributed: this deliverable (DEL-06-05) provides the review framework, but the actual coherence is maintained by human review during governance document updates.

Source: **ASSUMPTION: inferred from the absence of a centralized coherence artifact in SPEC or PLAN.**

## ASSUMPTION validation pathway (F-003 enrichment)

This document contains explicit ASSUMPTION tags in the following locations: P3, C1, C2, C4, T1, T2. These assumptions mark content that is inferred from available sources rather than directly stated in governance documents.

**Validation disposition options:**
- **Accept as-is:** The assumption is reasonable and does not require formal confirmation. Leave the ASSUMPTION tag as documentation of provenance.
- **Confirm and promote:** The human confirms the assumption is correct. Remove the ASSUMPTION tag and update the source citation to include the human's confirmation.
- **Reject and revise:** The human determines the assumption is incorrect. Revise the content and update the source citation.

**Whether ASSUMPTION tags must be formally resolved before this deliverable advances beyond WORKING_ITEMS was treated as TBD.** For this issuance cycle, human waiver `HW-DEL-06-05-A001-2026-02-24` permits `ISSUED` without making unresolved assumption tags lifecycle blockers. **ASSUMPTION resolution remains a human judgment call unless a stricter gate is explicitly introduced in project governance.**

Source: This enrichment addresses lensing item F-003.

## Examples

### Example: Detecting a coherence drift

If `docs/SPEC.md` were updated to add a new lifecycle state (e.g., `SEALED`) without updating `docs/TYPES.md` Section 5, this would be a coherence violation detectable by REQ-COH-04. The fix would be to update TYPES to include the new state, or revert SPEC if the state is not approved.

### Example: Guardrail boundary challenge

If a future feature request asks for "automated deliverable issuance for low-risk items," this would directly conflict with SOW-039 and K-AUTH-1. The correct response is to surface the conflict to the human decision-maker, who may choose to:
- Reject the request (boundary holds)
- Accept the request with a formal scope change (SOW-039 moves from OUT to IN; K-AUTH-1 is modified or retired with rationale)

In no case should an agent silently accommodate the request.

Source: `docs/CONTRACT.md` K-AUTH-1; `docs/DIRECTIVE.md` Section 2.3

## Conflict Table (for human ruling)

| Conflict ID | Conflict | Source A | Source B | Impacted Sections | Proposed Authority (PROPOSAL) | Human Ruling |
|-------------|---------|----------|----------|-------------------|-------------------------------|-------------|
| CT-001 | DIRECTIVE hierarchy section reference required normalization between deliverable-local docs. | Previous Specification wording (REQ-COH-01 note) | Previous Procedure wording (Step 1 item 4) | Specification REQ-COH-01; Procedure Step 1 item 4 | Specification.md / Procedure.md normalization | RESOLVED (2026-02-24): Use DIRECTIVE Section 5 (`Structural Constraints` -> `Flat package hierarchy`) as the authoritative hierarchy reference. |
