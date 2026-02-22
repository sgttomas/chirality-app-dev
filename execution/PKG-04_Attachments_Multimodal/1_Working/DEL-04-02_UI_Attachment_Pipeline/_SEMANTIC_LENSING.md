# Semantic Lensing Register: DEL-04-02 UI Attachment Pipeline (Picker, Preview, Rollback, Rehydration)

**Generated:** 2026-02-21
**Deliverable Folder:** execution/PKG-04_Attachments_Multimodal/1_Working/DEL-04-02_UI_Attachment_Pipeline/
**Warnings:** None

**Inputs Read:**
- _CONTEXT.md — `execution/PKG-04_Attachments_Multimodal/1_Working/DEL-04-02_UI_Attachment_Pipeline/_CONTEXT.md`
- _STATUS.md — `execution/PKG-04_Attachments_Multimodal/1_Working/DEL-04-02_UI_Attachment_Pipeline/_STATUS.md` (Current State: SEMANTIC_READY)
- _SEMANTIC.md — `execution/PKG-04_Attachments_Multimodal/1_Working/DEL-04-02_UI_Attachment_Pipeline/_SEMANTIC.md`
- Datasheet.md — `execution/PKG-04_Attachments_Multimodal/1_Working/DEL-04-02_UI_Attachment_Pipeline/Datasheet.md`
- Specification.md — `execution/PKG-04_Attachments_Multimodal/1_Working/DEL-04-02_UI_Attachment_Pipeline/Specification.md`
- Guidance.md — `execution/PKG-04_Attachments_Multimodal/1_Working/DEL-04-02_UI_Attachment_Pipeline/Guidance.md`
- Procedure.md — `execution/PKG-04_Attachments_Multimodal/1_Working/DEL-04-02_UI_Attachment_Pipeline/Procedure.md`
- _REFERENCES.md — `execution/PKG-04_Attachments_Multimodal/1_Working/DEL-04-02_UI_Attachment_Pipeline/_REFERENCES.md`

**Purpose:** Apply CHIRALITY_FRAMEWORK matrix cells as lenses over the production documents, capturing warranted enrichment inputs for a later enrichment pass.

## Summary

- Total warranted items: 18
- By document:
  - Datasheet: 2
  - Specification: 7
  - Guidance: 3
  - Procedure: 3
  - Multi: 3
- By matrix:
  - A: 4  B: 3  C: 3  F: 2  D: 2  X: 2  E: 2
- By type:
  - Conflict: 0
  - VerificationGap: 4
  - MissingSlot: 5
  - WeakStatement: 3
  - RationaleGap: 2
  - Normalization: 2
  - TBD_Question: 2
  - MatrixError: 0
- Notable conflicts: 0
- Matrix parse errors: 0

## Matrix A — Orientation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| A:normative:guiding | normative | guiding | prescriptive direction | 1 | HAS_ITEMS | Extension list synchronization lacks prescriptive mechanism |
| A:normative:applying | normative | applying | mandatory practice | 1 | HAS_ITEMS | Draft preservation scope undefined as mandatory practice |
| A:normative:judging | normative | judging | compliance determination | 1 | HAS_ITEMS | Malformed record definition unspecified for compliance determination |
| A:normative:reviewing | normative | reviewing | regulatory audit | 0 | NO_ITEMS | Audit patterns adequately covered by Verification tables |
| A:operative:guiding | operative | guiding | procedural direction | 0 | NO_ITEMS | Procedure steps are well-directed |
| A:operative:applying | operative | applying | practical execution | 0 | NO_ITEMS | Execution steps are clear and actionable |
| A:operative:judging | operative | judging | performance assessment | 1 | HAS_ITEMS | No performance/latency criteria for optimistic send |
| A:operative:reviewing | operative | reviewing | process audit | 0 | NO_ITEMS | Procedure verification section covers process audit |
| A:evaluative:guiding | evaluative | guiding | value orientation | 0 | NO_ITEMS | Purpose/Principles in Guidance adequately orient value |
| A:evaluative:applying | evaluative | applying | merit application | 0 | NO_ITEMS | UX merit is addressed via examples and trade-offs |
| A:evaluative:judging | evaluative | judging | worth determination | 0 | NO_ITEMS | Quality appraisal addressed by verification table |
| A:evaluative:reviewing | evaluative | reviewing | quality appraisal | 0 | NO_ITEMS | Covered by Procedure verification checks |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A-001 | A:normative:guiding | MissingSlot | Multi | Specification | Add a requirement or note specifying how the picker extension filter list stays synchronized with the server-side supported extension list | Guidance C1 identifies this as TBD but no prescriptive mechanism exists in the Specification to direct how synchronization should occur | Guidance.md, Specification.md | Guidance.md#C1, Specification.md#REQ-PICK-01 | — | Specification.md | TBD |
| A-002 | A:normative:applying | WeakStatement | Specification | Specification | Clarify scope of REQ-DRAFT-01: specify whether draft preservation is required only on send failure, across view switches, across app restarts, or all of these | REQ-DRAFT-01 is marked as TBD with an ASSUMPTION note; the mandatory practice boundary is ambiguous which could change implementation scope | Specification.md | Specification.md#REQ-DRAFT-01 | — | Human decision | TBD |
| A-003 | A:normative:judging | WeakStatement | Specification | Specification | Define what constitutes a "malformed" attachment record for rehydration shape validation (e.g., missing required fields, wrong types, additional criteria) | REQ-REHYD-01 requires validation but the compliance criteria for "malformed" are unspecified; Guidance C3 calls this an ASSUMPTION | Specification.md, Guidance.md | Specification.md#REQ-REHYD-01, Guidance.md#C3 | — | Human decision | TBD |
| A-004 | A:operative:judging | MissingSlot | Specification | Specification | Add performance/latency acceptance criteria for optimistic send rendering (e.g., message must appear within N ms of user action) | No performance assessment criteria exist for the optimistic UI pattern; under this lens, the operative judging perspective reveals no measurable threshold for "immediately" | Specification.md | Specification.md#REQ-OPT-01 | — | Human decision | TBD |

## Matrix B — Conceptualization (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| B:data:necessity | data | necessity | essential fact | 1 | HAS_ITEMS | Size limits documented but budget enforcement boundary unclear at UI |
| B:data:sufficiency | data | sufficiency | adequate evidence | 0 | NO_ITEMS | Attribute values in Datasheet are well-sourced |
| B:data:completeness | data | completeness | comprehensive record | 1 | HAS_ITEMS | Missing file count limit per turn |
| B:data:consistency | data | consistency | reliable measurement | 0 | NO_ITEMS | Data values consistent across documents |
| B:information:necessity | information | necessity | essential signal | 0 | NO_ITEMS | Signals (success/failure/partial) are documented |
| B:information:sufficiency | information | sufficiency | adequate context | 1 | HAS_ITEMS | Error context on send failure underspecified |
| B:information:completeness | information | completeness | comprehensive account | 0 | NO_ITEMS | Flow descriptions in Guidance examples are comprehensive |
| B:information:consistency | information | consistency | coherent message | 0 | NO_ITEMS | Messages are coherent across docs |
| B:knowledge:necessity | knowledge | necessity | fundamental understanding | 0 | NO_ITEMS | Architecture (client/server split) well explained |
| B:knowledge:sufficiency | knowledge | sufficiency | competent expertise | 0 | NO_ITEMS | Sufficient for implementation |
| B:knowledge:completeness | knowledge | completeness | thorough mastery | 0 | NO_ITEMS | Coverage adequate for UI scope |
| B:knowledge:consistency | knowledge | consistency | coherent understanding | 0 | NO_ITEMS | Understanding is coherent across documents |
| B:wisdom:necessity | wisdom | necessity | essential discernment | 0 | NO_ITEMS | Trade-offs in Guidance provide discernment |
| B:wisdom:sufficiency | wisdom | sufficiency | adequate judgment | 0 | NO_ITEMS | Judgment calls documented in Guidance |
| B:wisdom:completeness | wisdom | completeness | holistic insight | 0 | NO_ITEMS | Covered adequately |
| B:wisdom:consistency | wisdom | consistency | principled reasoning | 0 | NO_ITEMS | Reasoning is principled and sourced |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| B-001 | B:data:necessity | TBD_Question | Datasheet | Datasheet | Record whether the UI should display or enforce the per-file (10 MB) and per-turn (18 MB) size limits as pre-send validation, or rely entirely on server-side rejection | Datasheet records size limits as "server-enforced" but does not clarify whether the UI should surface these limits before send; this essential fact affects UI behavior | Datasheet.md | Datasheet.md#Attributes | — | Human decision | TBD |
| B-002 | B:data:completeness | MissingSlot | Datasheet | Datasheet | Add maximum file count per turn (if any) to the Attributes table | Datasheet records per-file and per-turn byte limits but no maximum file count; if a limit exists server-side, the UI may need to enforce or communicate it | Datasheet.md | Datasheet.md#Attributes | — | SPEC.md Section 9.8 | TBD |
| B-003 | B:information:sufficiency | MissingSlot | Specification | Specification | Add a requirement specifying what error information the UI must display to the user on send failure (e.g., error message from server, generic retry prompt) | REQ-ROLL-01 specifies rollback mechanics but not what information the user receives about why the send failed; adequate context for the user is missing | Specification.md | Specification.md#REQ-ROLL-01 | — | Human decision | TBD |

## Matrix C — Formulation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| C:normative:necessity | normative | necessity | enforceable governance | 1 | HAS_ITEMS | Dependency governance gap |
| C:normative:sufficiency | normative | sufficiency | compliance justification | 0 | NO_ITEMS | Sources cited throughout |
| C:normative:completeness | normative | completeness | total regulatory coverage | 0 | NO_ITEMS | Requirements cover the stated scope |
| C:normative:consistency | normative | consistency | harmonized conformance | 1 | HAS_ITEMS | Terminology inconsistency |
| C:operative:necessity | operative | necessity | execution prerequisite | 1 | HAS_ITEMS | Dependency status unresolved |
| C:operative:sufficiency | operative | sufficiency | operational readiness | 0 | NO_ITEMS | Steps are sufficient for the scope |
| C:operative:completeness | operative | completeness | end-to-end process coverage | 0 | NO_ITEMS | Procedure covers full pipeline |
| C:operative:consistency | operative | consistency | reproducible execution | 0 | NO_ITEMS | Steps are reproducible |
| C:evaluative:necessity | evaluative | necessity | intrinsic merit | 0 | NO_ITEMS | Value proposition is clear |
| C:evaluative:sufficiency | evaluative | sufficiency | substantiated appraisal | 0 | NO_ITEMS | Trade-offs substantiated |
| C:evaluative:completeness | evaluative | completeness | comprehensive quality scope | 0 | NO_ITEMS | Quality scope covered by verification |
| C:evaluative:consistency | evaluative | consistency | coherent valuation standard | 0 | NO_ITEMS | Valuation standards are coherent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| C-001 | C:normative:necessity | RationaleGap | Procedure | Guidance | Add rationale for why DEL-04-01 and DEL-03-02 dependencies are marked as ASSUMPTION rather than formally declared; clarify whether stubbing is acceptable for initial implementation | Procedure Prerequisites list DEL-04-01 and DEL-03-02 as ASSUMPTION-based dependencies not yet in _DEPENDENCIES.md; enforceable governance requires these to be formally tracked or the rationale for deferral documented | Procedure.md | Procedure.md#Prerequisites | — | _DEPENDENCIES.md / Human decision | TBD |
| C-002 | C:normative:consistency | Normalization | Multi | Guidance | Harmonize terminology: "attachment bar" (Guidance Example 2, step 7) vs. "attachment list" (Procedure Step 7 test table) — adopt a single term across documents | Documents use "attachment bar" and "attachment list" to refer to what appears to be the same UI element; inconsistency risks drift in implementation | Guidance.md, Procedure.md | Guidance.md#Example 2, Procedure.md#Step 7 | — | Specification.md (as normative source) | TBD |
| C-003 | C:operative:necessity | VerificationGap | Procedure | Procedure | Formalize dependency availability checks as a gating step before implementation begins (e.g., "Verify DEL-04-01 API is available or stubbed before proceeding to Step 4") | Procedure lists DEL-04-01 and DEL-03-02 as prerequisites with TBD status but Step 4 (Optimistic Send) proceeds assuming the turn API exists; no gating check ensures the prerequisite is met | Procedure.md | Procedure.md#Prerequisites, Procedure.md#Step 4 | — | Procedure.md | TBD |

## Matrix F — Requirements (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| F:normative:necessity | normative | necessity | mandatory compliance basis | 0 | NO_ITEMS | Compliance basis is established via source citations |
| F:normative:sufficiency | normative | sufficiency | warranted governance | 0 | NO_ITEMS | Governance is warranted by SPEC references |
| F:normative:completeness | normative | completeness | total compliance fulfillment | 1 | HAS_ITEMS | Accessibility requirement absent |
| F:normative:consistency | normative | consistency | invariant regulatory standard | 0 | NO_ITEMS | Standards table is consistent |
| F:operative:necessity | operative | necessity | foundational process dependency | 0 | NO_ITEMS | Dependencies identified (though as ASSUMPTION) |
| F:operative:sufficiency | operative | sufficiency | verified operational capability | 0 | NO_ITEMS | Operational steps are sufficient |
| F:operative:completeness | operative | completeness | exhaustive process command | 0 | NO_ITEMS | Process steps cover full scope |
| F:operative:consistency | operative | consistency | disciplined workflow coherence | 0 | NO_ITEMS | Workflow is coherent |
| F:evaluative:necessity | evaluative | necessity | grounded quality basis | 0 | NO_ITEMS | Quality basis grounded in verification table |
| F:evaluative:sufficiency | evaluative | sufficiency | competent value assessment | 0 | NO_ITEMS | Assessment approach is competent |
| F:evaluative:completeness | evaluative | completeness | total quality accounting | 1 | HAS_ITEMS | No explicit quality criteria for UX feedback |
| F:evaluative:consistency | evaluative | consistency | principled quality coherence | 0 | NO_ITEMS | Quality approach is coherent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| F-001 | F:normative:completeness | TBD_Question | Specification | Specification | Determine whether accessibility requirements (keyboard navigation, screen reader support, ARIA attributes) apply to the file picker and attachment preview, and if so, add corresponding requirements | Guidance C5 flags accessibility as TBD; total compliance fulfillment lens reveals no accessibility requirements exist for any UI component in this deliverable | Specification.md, Guidance.md | Specification.md#Requirements (entire section), Guidance.md#C5 | — | Human decision / UX review | TBD |
| F-002 | F:evaluative:completeness | MissingSlot | Specification | Specification | Add quality criteria for user-facing error feedback on send failure and picker rejection (e.g., toast notification, inline error, duration of display) | Total quality accounting reveals no specification of how the user experiences errors; Guidance C5 flags this as TBD but no requirement captures it | Specification.md, Guidance.md | Specification.md#REQ-ROLL-01, Guidance.md#C5 | — | Human decision | TBD |

## Matrix D — Objectives (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| D:normative:guiding | normative | guiding | established regulatory mandate | 0 | NO_ITEMS | Mandate is established via SPEC.md |
| D:normative:applying | normative | applying | enforced regulatory practice | 0 | NO_ITEMS | Practices are enforced through requirements |
| D:normative:judging | normative | judging | definitive conformance ruling | 1 | HAS_ITEMS | Verification lacks negative test for NOAUTH |
| D:normative:reviewing | normative | reviewing | anchored compliance inspection | 0 | NO_ITEMS | Verification table provides inspection anchors |
| D:operative:guiding | operative | guiding | grounded procedural guidance | 0 | NO_ITEMS | Procedure is grounded and step-by-step |
| D:operative:applying | operative | applying | validated practical deployment | 0 | NO_ITEMS | Deployment steps are practical |
| D:operative:judging | operative | judging | definitive performance verdict | 1 | HAS_ITEMS | No pass/fail threshold for integration tests |
| D:operative:reviewing | operative | reviewing | systematic process rigor | 0 | NO_ITEMS | Process rigor present in Procedure |
| D:evaluative:guiding | evaluative | guiding | principled quality direction | 0 | NO_ITEMS | Principles P1-P4 provide quality direction |
| D:evaluative:applying | evaluative | applying | realized value deployment | 0 | NO_ITEMS | Value deployment addressed by examples |
| D:evaluative:judging | evaluative | judging | conclusive quality verdict | 0 | NO_ITEMS | Verification pass criteria exist |
| D:evaluative:reviewing | evaluative | reviewing | grounded quality review | 0 | NO_ITEMS | Review approach is grounded |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| D-001 | D:normative:judging | VerificationGap | Specification | Specification | Add a negative verification test for REQ-NOAUTH-01: verify that client metadata is NOT used in any server-bound payload for classification/execution purposes (not just that it is "used only for preview") | Current verification entry for REQ-NOAUTH-01 says "verify client metadata is used only for preview, not sent as authoritative" but does not specify a concrete negative test (e.g., inspect API payload to confirm no mime/type field is sent, or confirm server ignores it) | Specification.md | Specification.md#Verification (REQ-NOAUTH-01 row) | — | Specification.md | TBD |
| D-002 | D:operative:judging | VerificationGap | Procedure | Procedure | Add pass/fail criteria for integration tests in Step 8 (e.g., expected server response codes, expected warning text patterns for partial failure, timeout thresholds) | Step 8 describes integration verification scenarios but provides no concrete pass/fail thresholds; a definitive performance verdict requires measurable criteria | Procedure.md | Procedure.md#Step 8 | — | Procedure.md | TBD |

## Matrix X — Verification (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| X:guiding:necessity | guiding | necessity | foundational governance orientation | 0 | NO_ITEMS | Governance orientation established |
| X:guiding:sufficiency | guiding | sufficiency | substantiated strategic guidance | 0 | NO_ITEMS | Strategic guidance is substantiated |
| X:guiding:completeness | guiding | completeness | total directive breadth | 0 | NO_ITEMS | Directive breadth covers the scope |
| X:guiding:consistency | guiding | consistency | harmonized directive stability | 0 | NO_ITEMS | Directives are harmonized |
| X:applying:necessity | applying | necessity | mandatory activation standard | 1 | HAS_ITEMS | No activation check for attachment pipeline feature flag |
| X:applying:sufficiency | applying | sufficiency | proven implementation threshold | 0 | NO_ITEMS | Implementation thresholds exist in verification table |
| X:applying:completeness | applying | completeness | exhaustive implementation span | 0 | NO_ITEMS | Implementation span covers stated scope |
| X:applying:consistency | applying | consistency | standardized delivery assurance | 0 | NO_ITEMS | Delivery assurance via test suite |
| X:judging:necessity | judging | necessity | binding performance baseline | 1 | HAS_ITEMS | No baseline for attachment count in tests |
| X:judging:sufficiency | judging | sufficiency | warranted evidentiary finding | 0 | NO_ITEMS | Evidence approach is warranted |
| X:judging:completeness | judging | completeness | exhaustive adjudication scope | 0 | NO_ITEMS | Adjudication scope covered |
| X:judging:consistency | judging | consistency | invariant adjudication standard | 0 | NO_ITEMS | Standards are invariant across docs |
| X:reviewing:necessity | reviewing | necessity | fundamental governance scrutiny | 0 | NO_ITEMS | Scrutiny channels exist |
| X:reviewing:sufficiency | reviewing | sufficiency | substantiated readiness review | 0 | NO_ITEMS | Readiness review is substantiated |
| X:reviewing:completeness | reviewing | completeness | exhaustive audit coverage | 0 | NO_ITEMS | Audit coverage is adequate |
| X:reviewing:consistency | reviewing | consistency | dependable assurance audit | 0 | NO_ITEMS | Assurance approach is dependable |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| X-001 | X:applying:necessity | RationaleGap | Guidance | Guidance | Document whether the attachment pipeline is feature-flagged or always active, and rationale for that decision | No document addresses whether the attachment pipeline capability can be disabled or is always present; mandatory activation standard lens reveals this as an undocumented architectural decision | Guidance.md | entire document scanned | — | Human decision | TBD |
| X-002 | X:judging:necessity | VerificationGap | Procedure | Procedure | Add test scenarios with boundary attachment counts (e.g., 0 attachments with text, 1 attachment, many attachments) to establish a performance baseline for the picker and preview components | Procedure test matrix covers functional correctness but not boundary/stress conditions for attachment count; binding performance baseline requires edge-case verification | Procedure.md | Procedure.md#Step 7 | — | Procedure.md | TBD |

## Matrix E — Evaluation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| E:normative:necessity | normative | necessity | obligatory governance floor | 0 | NO_ITEMS | Governance floor established by requirements |
| E:normative:sufficiency | normative | sufficiency | proven regulatory sufficiency | 0 | NO_ITEMS | Regulatory sufficiency proven by source citations |
| E:normative:completeness | normative | completeness | total regulatory jurisdiction | 0 | NO_ITEMS | Jurisdiction covers UI scope; server scope explicitly excluded |
| E:normative:consistency | normative | consistency | enduring compliance dependability | 1 | HAS_ITEMS | OBJ-003 mapping is ASSUMPTION |
| E:operative:necessity | operative | necessity | validated execution imperative | 0 | NO_ITEMS | Execution imperative is validated through procedure |
| E:operative:sufficiency | operative | sufficiency | demonstrated execution fitness | 0 | NO_ITEMS | Fitness demonstrated by verification approach |
| E:operative:completeness | operative | completeness | exhaustive operational reach | 0 | NO_ITEMS | Operational reach covers stated scope |
| E:operative:consistency | operative | consistency | dependable operational standard | 0 | NO_ITEMS | Operational standard is dependable |
| E:evaluative:necessity | evaluative | necessity | irreducible quality obligation | 0 | NO_ITEMS | Quality obligation met by test requirements |
| E:evaluative:sufficiency | evaluative | sufficiency | proven quality threshold | 0 | NO_ITEMS | Threshold proven by verification table |
| E:evaluative:completeness | evaluative | completeness | comprehensive quality authority | 0 | NO_ITEMS | Authority is comprehensive for scope |
| E:evaluative:consistency | evaluative | consistency | enduring quality assurance | 1 | HAS_ITEMS | Test output location TBD |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| E-001 | E:normative:consistency | Normalization | Datasheet | Datasheet | Resolve the ASSUMPTION tag on OBJ-003 mapping: either confirm the objective mapping via decomposition authority or mark as formally TBD pending human ruling | Datasheet Objectives field includes "ASSUMPTION (best-effort mapping via PKG-04 package grouping)" which introduces uncertainty into enduring compliance dependability; if the mapping is wrong, traceability to objectives is broken | Datasheet.md | Datasheet.md#Identification (Objectives row) | — | Decomposition document | TBD |
| E-002 | E:evaluative:consistency | WeakStatement | Procedure | Procedure | Specify concrete test output location and CI artifact path rather than "TBD (project test output directory or CI artifacts)" | Enduring quality assurance requires a stable, known location for test evidence; current "TBD" undermines auditability of quality outcomes over time | Procedure.md | Procedure.md#Records | — | Project CI configuration | TBD |
