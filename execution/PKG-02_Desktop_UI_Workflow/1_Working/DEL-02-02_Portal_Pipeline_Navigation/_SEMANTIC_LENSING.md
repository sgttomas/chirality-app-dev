# Semantic Lensing Register: DEL-02-02 Portal->Pipeline Navigation & Deliverable Key Semantics

**Generated:** 2026-02-21
**Deliverable Folder:** /Users/ryan/ai-env/projects/chirality-app-dev1/execution/PKG-02_Desktop_UI_Workflow/1_Working/DEL-02-02_Portal_Pipeline_Navigation/
**Warnings:** None

**Inputs Read:**
- _CONTEXT.md — `execution/PKG-02_Desktop_UI_Workflow/1_Working/DEL-02-02_Portal_Pipeline_Navigation/_CONTEXT.md`
- _STATUS.md — `execution/PKG-02_Desktop_UI_Workflow/1_Working/DEL-02-02_Portal_Pipeline_Navigation/_STATUS.md` (Current State: SEMANTIC_READY)
- _SEMANTIC.md — `execution/PKG-02_Desktop_UI_Workflow/1_Working/DEL-02-02_Portal_Pipeline_Navigation/_SEMANTIC.md`
- Datasheet.md — `execution/PKG-02_Desktop_UI_Workflow/1_Working/DEL-02-02_Portal_Pipeline_Navigation/Datasheet.md`
- Specification.md — `execution/PKG-02_Desktop_UI_Workflow/1_Working/DEL-02-02_Portal_Pipeline_Navigation/Specification.md`
- Guidance.md — `execution/PKG-02_Desktop_UI_Workflow/1_Working/DEL-02-02_Portal_Pipeline_Navigation/Guidance.md`
- Procedure.md — `execution/PKG-02_Desktop_UI_Workflow/1_Working/DEL-02-02_Portal_Pipeline_Navigation/Procedure.md`
- _REFERENCES.md — `execution/PKG-02_Desktop_UI_Workflow/1_Working/DEL-02-02_Portal_Pipeline_Navigation/_REFERENCES.md`

**Purpose:** Apply CHIRALITY_FRAMEWORK matrix cells as lenses over the production documents, capturing warranted enrichment inputs for a later enrichment pass.

---

## Summary

- Total warranted items: 18
- By document (AppliesToDoc):
  - Datasheet: 2
  - Specification: 8
  - Guidance: 2
  - Procedure: 5
  - Multi: 1
- By matrix:
  - A: 4  B: 3  C: 2  F: 2  D: 2  X: 3  E: 2
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

---

## Matrix A — Orientation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| A:normative:guiding | normative | guiding | prescriptive direction | 1 | HAS_ITEMS | Weak prescriptive guidance for state transfer mechanism |
| A:normative:applying | normative | applying | mandatory practice | 1 | HAS_ITEMS | Missing mandatory acceptance criteria for navigation timing |
| A:normative:judging | normative | judging | compliance determination | 0 | NO_ITEMS | Requirements are clearly enumerated with verification mapping |
| A:normative:reviewing | normative | reviewing | regulatory audit | 0 | NO_ITEMS | Standards table in Specification provides adequate audit anchors |
| A:operative:guiding | operative | guiding | procedural direction | 1 | HAS_ITEMS | Procedure lacks upstream dependency verification step |
| A:operative:applying | operative | applying | practical execution | 0 | NO_ITEMS | Procedure steps are sequential and actionable |
| A:operative:judging | operative | judging | performance assessment | 1 | HAS_ITEMS | No performance/timing acceptance criteria defined |
| A:operative:reviewing | operative | reviewing | process audit | 0 | NO_ITEMS | Verification table in Procedure covers all requirements |
| A:evaluative:guiding | evaluative | guiding | value orientation | 0 | NO_ITEMS | Guidance Purpose section adequately frames operator value |
| A:evaluative:applying | evaluative | applying | merit application | 0 | NO_ITEMS | Example flow demonstrates concrete merit realization |
| A:evaluative:judging | evaluative | judging | worth determination | 0 | NO_ITEMS | Verification approach supports worth judgment adequately |
| A:evaluative:reviewing | evaluative | reviewing | quality appraisal | 0 | NO_ITEMS | Test coverage plan in Procedure addresses quality review |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A-001 | A:normative:guiding | WeakStatement | Guidance | Guidance | Clarify whether the state transfer mechanism for navigation (URL params, React context, or other) should be treated as a normative constraint or an implementation-free choice; current ASSUMPTION note in C1 leaves ambiguity about whether downstream deliverables may choose differently | The ASSUMPTION in Guidance C1 explicitly defers the mechanism choice, but Specification REQ-01 requires deterministic pre-selection; without guidance on mechanism, implementers may make incompatible choices across views | Guidance.md | Considerations > C1: Navigation Routing Architecture | — | Guidance.md | TBD |
| A-002 | A:normative:applying | MissingSlot | Specification | Specification | Add acceptance criteria for navigation transition timing (e.g., maximum latency from PORTAL click to PIPELINE view rendering with correct deliverable pre-selected) | REQ-01 mandates navigation routing but specifies no timing or responsiveness threshold; this could allow arbitrarily slow transitions to pass verification | Specification.md | Requirements > REQ-01 | — | docs/SPEC.md Section 14 | TBD |
| A-003 | A:operative:guiding | MissingSlot | Procedure | Procedure | Add a prerequisite verification step to confirm DEL-02-01 (FileTree Refresh) status before starting implementation, given Guidance C4 acknowledges the dependency on re-scan triggers | Guidance C4 notes DEL-02-01 triggers deliverable re-scans affecting shared state, but Procedure P5 only requires reviewing existing code, not confirming the upstream deliverable's readiness | Procedure.md | Prerequisites | — | Guidance.md > C4 | TBD |
| A-004 | A:operative:judging | VerificationGap | Specification | Specification | Add performance assessment criteria for navigation (e.g., target transition time, no visual flicker between PORTAL and PIPELINE) | Verification table maps REQ-01 to functional test but has no performance criteria; an operator could experience multi-second transitions and still "pass" | Specification.md | Verification > REQ-01 | — | docs/SPEC.md Section 14 | TBD |

---

## Matrix B — Conceptualization (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| B:data:necessity | data | necessity | essential fact | 1 | HAS_ITEMS | Missing essential fact: concrete composite key construction rule |
| B:data:sufficiency | data | sufficiency | adequate evidence | 0 | NO_ITEMS | Datasheet attributes are adequately evidenced with sources |
| B:data:completeness | data | completeness | comprehensive record | 0 | NO_ITEMS | Datasheet covers all key attributes from governance docs |
| B:data:consistency | data | consistency | reliable measurement | 0 | NO_ITEMS | Key format and naming are consistent across documents |
| B:information:necessity | information | necessity | essential signal | 1 | HAS_ITEMS | Missing error signal handling specification |
| B:information:sufficiency | information | sufficiency | adequate context | 0 | NO_ITEMS | Context provided is adequate for implementation |
| B:information:completeness | information | completeness | comprehensive account | 0 | NO_ITEMS | Documents provide comprehensive coverage of navigation flow |
| B:information:consistency | information | consistency | coherent message | 0 | NO_ITEMS | Messaging is coherent across all four documents |
| B:knowledge:necessity | knowledge | necessity | fundamental understanding | 1 | HAS_ITEMS | Procedure assumes knowledge not formally documented |
| B:knowledge:sufficiency | knowledge | sufficiency | competent expertise | 0 | NO_ITEMS | Prerequisites in Procedure cover expertise requirements |
| B:knowledge:completeness | knowledge | completeness | thorough mastery | 0 | NO_ITEMS | Guidance considerations provide sufficient depth |
| B:knowledge:consistency | knowledge | consistency | coherent understanding | 0 | NO_ITEMS | Understanding is coherent across documents |
| B:wisdom:necessity | wisdom | necessity | essential discernment | 0 | NO_ITEMS | Trade-offs section in Guidance adequately captures key judgments |
| B:wisdom:sufficiency | wisdom | sufficiency | adequate judgment | 0 | NO_ITEMS | Judgment calls are documented with rationale |
| B:wisdom:completeness | wisdom | completeness | holistic insight | 0 | NO_ITEMS | Guidance covers relationships to adjacent deliverables |
| B:wisdom:consistency | wisdom | consistency | principled reasoning | 0 | NO_ITEMS | Reasoning is principled and consistent throughout |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| B-001 | B:data:necessity | WeakStatement | Datasheet | Datasheet | Clarify the composite key construction rule: Datasheet says `pkg::id` with example `PKG-01_PackageLabel::DEL-01-01` but does not specify whether `pkg` is the PackageID (e.g., `PKG-01`) or the package folder label (e.g., `PKG-01_PackageLabel`); Guidance Example section uses `PKG-02_Desktop_UI_Workflow::DEL-02-02` suggesting folder label | The `pkg` segment in `pkg::id` is ambiguous between PackageID and package folder label; these are different strings and would produce different keys | Datasheet.md, Guidance.md | Datasheet > Attributes > Deliverable Key Format; Guidance > Examples > Example Composite Key | — | docs/PLAN.md Section 2 | TBD |
| B-002 | B:information:necessity | MissingSlot | Specification | Specification | Add specification for error signal handling: what the UI should display when `/api/project/deliverables` returns an error response (as distinct from empty results), and how error state differs from loading and empty states | REQ-03 specifies loading and empty states but does not address API error states; REQ-10 requires API consumption but does not define error handling behavior | Specification.md | Requirements > REQ-03, REQ-10 | — | docs/SPEC.md Section 15 | TBD |
| B-003 | B:knowledge:necessity | RationaleGap | Procedure | Guidance | Add rationale for why Step 1 (Audit Existing Implementation) is structured as a four-part review; clarify what "document findings" in Step 1.5 means concretely (e.g., where to record findings, in what format) | Step 1.5 says "Document findings" but provides no guidance on the format or location for audit results; this could lead to undocumented findings that are lost | Procedure.md | Steps > Step 1 > 1.5 | — | Procedure.md | TBD |

---

## Matrix C — Formulation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| C:normative:necessity | normative | necessity | Authoritative Compliance Imperative | 0 | NO_ITEMS | Compliance imperatives are authoritatively stated in requirements |
| C:normative:sufficiency | normative | sufficiency | Regulatory Competence Threshold | 1 | HAS_ITEMS | Standards table missing threshold for TYPES.md vocabulary compliance |
| C:normative:completeness | normative | completeness | Exhaustive Compliance Coverage | 0 | NO_ITEMS | All SOW items are traced to requirements |
| C:normative:consistency | normative | consistency | Regulatory Conformance Integrity | 0 | NO_ITEMS | Requirements are internally consistent |
| C:operative:necessity | operative | necessity | Operational Capability Prerequisite | 0 | NO_ITEMS | Prerequisites are listed in Procedure |
| C:operative:sufficiency | operative | sufficiency | Operational Competence Baseline | 0 | NO_ITEMS | Competence requirements are adequate |
| C:operative:completeness | operative | completeness | Comprehensive Operational Mastery | 0 | NO_ITEMS | Steps cover all requirements |
| C:operative:consistency | operative | consistency | Operational Process Dependability | 1 | HAS_ITEMS | No rollback/recovery guidance in Procedure |
| C:evaluative:necessity | evaluative | necessity | Essential Valuation Criterion | 0 | NO_ITEMS | Valuation criteria are implicitly covered by verification |
| C:evaluative:sufficiency | evaluative | sufficiency | Appraisal Competence Threshold | 0 | NO_ITEMS | Verification approaches are sufficient |
| C:evaluative:completeness | evaluative | completeness | Comprehensive Worth Assessment | 0 | NO_ITEMS | Worth is assessed through comprehensive test coverage |
| C:evaluative:consistency | evaluative | consistency | Valuation Integrity Standard | 0 | NO_ITEMS | Valuation approach is consistent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| C-001 | C:normative:sufficiency | VerificationGap | Specification | Specification | Add verification that UI vocabulary (MatrixRow, MatrixColumn, PipelineCategory, TaskScopeMode) matches `docs/TYPES.md` Section 9 definitions; current Standards table lists TYPES.md but no requirement or verification item checks conformance | Standards table references `docs/TYPES.md` Section 9 as a canonical vocabulary source, but no REQ or verification row ensures the implementation actually uses these type definitions | Specification.md | Standards; Verification | — | docs/TYPES.md Section 9 | TBD |
| C-002 | C:operative:consistency | MissingSlot | Procedure | Procedure | Add rollback or recovery guidance for each implementation step (e.g., what to do if Step 3 navigation implementation breaks existing PORTAL functionality, how to revert safely) | Procedure defines sequential steps but provides no guidance on what happens if a step fails or introduces a regression; operational dependability requires recovery paths | Procedure.md | Steps | — | Procedure.md | TBD |

---

## Matrix F — Requirements (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| F:normative:necessity | normative | necessity | Binding Regulatory Mandate | 0 | NO_ITEMS | Mandates are binding and clear |
| F:normative:sufficiency | normative | sufficiency | Prescribed Compliance Sufficiency | 1 | HAS_ITEMS | Compliance sufficiency gap in REQ-06 verification |
| F:normative:completeness | normative | completeness | Total Regulatory Completeness | 0 | NO_ITEMS | All identified regulatory items are covered |
| F:normative:consistency | normative | consistency | Mandated Conformance Fidelity | 0 | NO_ITEMS | Conformance is consistent across requirements |
| F:operative:necessity | operative | necessity | Operational Readiness Imperative | 1 | HAS_ITEMS | Missing readiness check for API endpoint availability |
| F:operative:sufficiency | operative | sufficiency | Execution Proficiency Threshold | 0 | NO_ITEMS | Proficiency requirements are sufficient |
| F:operative:completeness | operative | completeness | Total Operational Comprehension | 0 | NO_ITEMS | Operational steps are comprehensive |
| F:operative:consistency | operative | consistency | Consistent Execution Integrity | 0 | NO_ITEMS | Execution steps are consistent |
| F:evaluative:necessity | evaluative | necessity | Essential Worth Imperative | 0 | NO_ITEMS | Worth imperatives are addressed |
| F:evaluative:sufficiency | evaluative | sufficiency | Adequate Appraisal Proficiency | 0 | NO_ITEMS | Appraisal proficiency is adequate |
| F:evaluative:completeness | evaluative | completeness | Exhaustive Valuation Scope | 0 | NO_ITEMS | Valuation scope is addressed |
| F:evaluative:consistency | evaluative | consistency | Principled Valuation Coherence | 0 | NO_ITEMS | Valuation coherence is maintained |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| F-001 | F:normative:sufficiency | VerificationGap | Specification | Specification | REQ-06 verification says "Functional test: change project root; simulate fetch failure; remove deliverable" but only names 3 of the 5 trigger scenarios; add explicit verification steps for trigger 4 (knowledge marker absent) and trigger 5 (knowledge type unresolvable) | REQ-06 lists 5 stale clearing triggers but the verification row only names 3 test scenarios; the remaining 2 triggers have no explicit verification approach | Specification.md | Verification > REQ-06 | — | Specification.md > Requirements > REQ-06 | TBD |
| F-002 | F:operative:necessity | TBD_Question | Procedure | Procedure | Add prerequisite: confirm `/api/project/deliverables` endpoint is implemented and accessible before beginning Step 2; if the endpoint does not yet exist, clarify whether this deliverable owns its implementation or depends on another deliverable | Procedure Step 2 assumes the API endpoint exists but neither the Prerequisites nor _DEPENDENCIES.md confirms this; the endpoint could be part of a different deliverable | Procedure.md | Prerequisites; Steps > Step 2 | — | docs/SPEC.md Section 15; _DEPENDENCIES.md | TBD |

---

## Matrix D — Objectives (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| D:normative:guiding | normative | guiding | Resolved Governance Mandate | 0 | NO_ITEMS | Governance mandate is resolved and clear |
| D:normative:applying | normative | applying | Resolved Obligatory Practice | 0 | NO_ITEMS | Obligatory practices are resolved |
| D:normative:judging | normative | judging | Definitive Compliance Verdict | 0 | NO_ITEMS | Compliance determination criteria are definitive |
| D:normative:reviewing | normative | reviewing | Assured Regulatory Oversight | 0 | NO_ITEMS | Oversight mechanisms are in place |
| D:operative:guiding | operative | guiding | Resolved Operational Steering | 1 | HAS_ITEMS | Operational steering gap for knowledge-type scope boundary |
| D:operative:applying | operative | applying | Resolved Execution Capability | 0 | NO_ITEMS | Execution capabilities are adequately specified |
| D:operative:judging | operative | judging | Settled Performance Evaluation | 0 | NO_ITEMS | Performance evaluation criteria exist |
| D:operative:reviewing | operative | reviewing | Assured Process Reliability | 0 | NO_ITEMS | Process reliability is addressed through stale clearing |
| D:evaluative:guiding | evaluative | guiding | Resolved Value Direction | 1 | HAS_ITEMS | Value direction gap for user experience continuity |
| D:evaluative:applying | evaluative | applying | Resolved Merit Realization | 0 | NO_ITEMS | Merit realization is demonstrated in examples |
| D:evaluative:judging | evaluative | judging | Definitive Worth Judgment | 0 | NO_ITEMS | Worth judgment criteria exist in verification |
| D:evaluative:reviewing | evaluative | reviewing | Assured Quality Appraisal | 0 | NO_ITEMS | Quality appraisal mechanisms are adequate |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| D-001 | D:operative:guiding | WeakStatement | Specification | Guidance | Clarify the boundary of knowledge-type scope implementation in this deliverable; Specification Excluded section uses ASSUMPTION language ("deep knowledge-type pipeline logic may belong to a separate deliverable or future scope") which leaves the implementation boundary ambiguous | The ASSUMPTION in Specification Excluded section is hedged ("may belong to"), leaving implementers uncertain about how much knowledge-type logic to build; this could cause scope creep or under-delivery | Specification.md | Scope > Excluded | — | Decomposition G7-APPROVED | TBD |
| D-002 | D:evaluative:guiding | RationaleGap | Guidance | Guidance | Add rationale for why the PORTAL matrix uses a 3x4 grid specifically and how the OPERATIVE row was chosen as the navigation trigger row (rather than other rows); this context helps implementers understand the design intent | Guidance C1 describes the routing but does not explain why the OPERATIVE row (and not NORMATIVE or EVALUATIVE) is the navigation trigger; understanding this supports correct extension if the matrix evolves | Guidance.md | Considerations > C1 | — | docs/PLAN.md Section 2 | TBD |

---

## Matrix X — Verification (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| X:guiding:necessity | guiding | necessity | Resolved Directional Benchmark | 0 | NO_ITEMS | Directional benchmarks are resolved |
| X:guiding:sufficiency | guiding | sufficiency | Sufficient Guidance Competence | 0 | NO_ITEMS | Guidance competence is sufficient |
| X:guiding:completeness | guiding | completeness | Exhaustive Guidance Scope | 0 | NO_ITEMS | Guidance scope is exhaustive for current deliverable |
| X:guiding:consistency | guiding | consistency | Principled Guidance Fidelity | 1 | HAS_ITEMS | Terminology inconsistency across documents |
| X:applying:necessity | applying | necessity | Essential Practice Foundation | 0 | NO_ITEMS | Practice foundations are essential and present |
| X:applying:sufficiency | applying | sufficiency | Sufficient Practice Competence | 0 | NO_ITEMS | Practice competence is sufficient |
| X:applying:completeness | applying | completeness | Exhaustive Implementation Scope | 1 | HAS_ITEMS | Implementation scope missing code location guidance |
| X:applying:consistency | applying | consistency | Reliable Practice Integrity | 0 | NO_ITEMS | Practice integrity is reliable |
| X:judging:necessity | judging | necessity | Essential Adjudicative Authority | 0 | NO_ITEMS | Adjudicative authority is established |
| X:judging:sufficiency | judging | sufficiency | Sufficient Adjudicative Basis | 0 | NO_ITEMS | Adjudicative basis is sufficient |
| X:judging:completeness | judging | completeness | Exhaustive Adjudicative Scope | 1 | HAS_ITEMS | Missing cross-deliverable integration test guidance |
| X:judging:consistency | judging | consistency | Principled Adjudicative Fidelity | 0 | NO_ITEMS | Adjudicative fidelity is principled |
| X:reviewing:necessity | reviewing | necessity | Essential Oversight Assurance | 0 | NO_ITEMS | Oversight assurance is essential and present |
| X:reviewing:sufficiency | reviewing | sufficiency | Sufficient Oversight Fitness | 0 | NO_ITEMS | Oversight fitness is sufficient |
| X:reviewing:completeness | reviewing | completeness | Exhaustive Review Coverage | 0 | NO_ITEMS | Review coverage is addressed |
| X:reviewing:consistency | reviewing | consistency | Consistent Review Integrity | 0 | NO_ITEMS | Review integrity is consistent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| X-001 | X:guiding:consistency | Normalization | Multi | Guidance | Normalize terminology: Datasheet uses "TASK* Pipeline Category" and "PORTAL Matrix Routing"; Specification uses "TASK* pipeline category" (lowercase); Guidance uses "PIPELINE TASK*" and "TASK*"; align capitalization and phrasing convention across documents, preferably anchored to `docs/TYPES.md` Section 9 canonical vocabulary | Inconsistent capitalization and phrasing of pipeline category names across documents risks terminology drift; a canonical form should be established | Datasheet.md, Specification.md, Guidance.md | Datasheet > Construction; Specification > Requirements > REQ-01, REQ-02; Guidance > Purpose | — | docs/TYPES.md Section 9 | TBD |
| X-002 | X:applying:completeness | TBD_Question | Procedure | Procedure | Add guidance on expected code locations (e.g., which directory/file for navigation routing, which for shared state, which for selector components); Procedure Records section says "specific paths TBD" for both implementation and test code | Procedure Steps reference implementing navigation routing, shared state, and selector components but provide no indication of where in the `frontend/` tree these should be placed; Records section explicitly marks paths as TBD | Procedure.md | Steps; Records | — | Frontend codebase structure | TBD |
| X-003 | X:judging:completeness | VerificationGap | Specification | Procedure | Add cross-deliverable integration test guidance: verify that DEL-02-01 FileTree refresh triggers correctly propagate to DEL-02-02 shared deliverables state (Guidance C4 identifies this coupling but neither Specification nor Procedure define a verification approach for it) | Guidance C4 identifies that DEL-02-01 refresh may trigger state updates in DEL-02-02, but no verification item checks this cross-deliverable interaction | Specification.md, Guidance.md | Specification > Verification; Guidance > Considerations > C4 | — | Guidance.md > C4 | TBD |

---

## Matrix E — Evaluation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| E:normative:necessity | normative | necessity | Mandated Governance Foundation | 0 | NO_ITEMS | Governance foundation is mandated and present |
| E:normative:sufficiency | normative | sufficiency | Prescribed Institutional Fitness | 0 | NO_ITEMS | Institutional fitness is prescribed |
| E:normative:completeness | normative | completeness | Exhaustive Regulatory Enactment | 0 | NO_ITEMS | Regulatory enactment is exhaustive |
| E:normative:consistency | normative | consistency | Mandated Institutional Coherence | 1 | HAS_ITEMS | Normalization gap in key format description |
| E:operative:necessity | operative | necessity | Essential Process Standard | 0 | NO_ITEMS | Process standards are essential and present |
| E:operative:sufficiency | operative | sufficiency | Adequate Operational Fitness | 0 | NO_ITEMS | Operational fitness is adequate |
| E:operative:completeness | operative | completeness | Complete Operational Coverage | 1 | HAS_ITEMS | Missing operational coverage for concurrent navigation |
| E:operative:consistency | operative | consistency | Dependable Operational Coherence | 0 | NO_ITEMS | Operational coherence is dependable |
| E:evaluative:necessity | evaluative | necessity | Essential Merit Foundation | 0 | NO_ITEMS | Merit foundation is established |
| E:evaluative:sufficiency | evaluative | sufficiency | Sufficient Quality Fitness | 0 | NO_ITEMS | Quality fitness is sufficient |
| E:evaluative:completeness | evaluative | completeness | Comprehensive Quality Realization | 0 | NO_ITEMS | Quality realization is comprehensive |
| E:evaluative:consistency | evaluative | consistency | Principled Quality Coherence | 0 | NO_ITEMS | Quality coherence is principled |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| E-001 | E:normative:consistency | Normalization | Datasheet | Datasheet | Normalize composite key example: Datasheet Attributes shows `PKG-01_PackageLabel::DEL-01-01` while Guidance Examples shows `PKG-02_Desktop_UI_Workflow::DEL-02-02`; both are valid examples but the Datasheet example uses a generic placeholder label while Guidance uses a real label; consider using the real deliverable's own key as the canonical example in both places | Using different example keys across documents creates unnecessary cognitive load; a single canonical example anchored to this deliverable would improve coherence | Datasheet.md, Guidance.md | Datasheet > Attributes > Deliverable Key Format; Guidance > Examples > Example Composite Key | — | docs/PLAN.md Section 2 | TBD |
| E-002 | E:operative:completeness | MissingSlot | Specification | Specification | Add requirement or consideration for concurrent/rapid navigation: what happens if the operator clicks multiple deliverable rows in quick succession in PORTAL before PIPELINE finishes loading the first selection; specify whether the latest click wins, whether earlier navigations are cancelled, or whether clicks are debounced | No document addresses the behavior when an operator navigates faster than the UI can render; this is an operational completeness gap that could cause race conditions in shared state | Specification.md | Requirements; entire document scanned | — | docs/SPEC.md Section 14 | TBD |
