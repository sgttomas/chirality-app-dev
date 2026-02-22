# Semantic Lensing Register: DEL-02-03 Operator Toolkit Panel & Local Presets (Non-authoritative)

**Generated:** 2026-02-21
**Deliverable Folder:** `execution/PKG-02_Desktop_UI_Workflow/1_Working/DEL-02-03_Operator_Toolkit_Panel/`
**Warnings:** None

**Inputs Read:**
- _CONTEXT.md — `execution/PKG-02_Desktop_UI_Workflow/1_Working/DEL-02-03_Operator_Toolkit_Panel/_CONTEXT.md`
- _STATUS.md — `execution/PKG-02_Desktop_UI_Workflow/1_Working/DEL-02-03_Operator_Toolkit_Panel/_STATUS.md`
- _SEMANTIC.md — `execution/PKG-02_Desktop_UI_Workflow/1_Working/DEL-02-03_Operator_Toolkit_Panel/_SEMANTIC.md`
- Datasheet.md — `execution/PKG-02_Desktop_UI_Workflow/1_Working/DEL-02-03_Operator_Toolkit_Panel/Datasheet.md`
- Specification.md — `execution/PKG-02_Desktop_UI_Workflow/1_Working/DEL-02-03_Operator_Toolkit_Panel/Specification.md`
- Guidance.md — `execution/PKG-02_Desktop_UI_Workflow/1_Working/DEL-02-03_Operator_Toolkit_Panel/Guidance.md`
- Procedure.md — `execution/PKG-02_Desktop_UI_Workflow/1_Working/DEL-02-03_Operator_Toolkit_Panel/Procedure.md`
- _REFERENCES.md — `execution/PKG-02_Desktop_UI_Workflow/1_Working/DEL-02-03_Operator_Toolkit_Panel/_REFERENCES.md`

**Purpose:** Apply CHIRALITY_FRAMEWORK matrix cells as lenses over the production documents, capturing warranted enrichment inputs for a later enrichment pass.

## Summary

- Total warranted items: 21
- By document:
  - Datasheet: 5
  - Specification: 7
  - Guidance: 3
  - Procedure: 4
  - Multi: 2
- By matrix:
  - A: 4  B: 4  C: 3  F: 3  D: 2  X: 3  E: 2
- By type:
  - Conflict: 0
  - VerificationGap: 4
  - MissingSlot: 7
  - WeakStatement: 3
  - RationaleGap: 2
  - Normalization: 3
  - TBD_Question: 2
  - MatrixError: 0
- Notable conflicts: 0
- Matrix parse errors: 0

---

## Matrix A -- Orientation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| A:normative:guiding | normative | guiding | prescriptive direction | 1 | HAS_ITEMS | Governance boundary clarity for operator-facing controls |
| A:normative:applying | normative | applying | mandatory practice | 1 | HAS_ITEMS | TBD items in mandatory practices |
| A:normative:judging | normative | judging | compliance determination | 0 | NO_ITEMS | Governance non-bypass requirements well-stated across docs |
| A:normative:reviewing | normative | reviewing | regulatory audit | 1 | HAS_ITEMS | Audit trail for toolkit state changes |
| A:operative:guiding | operative | guiding | procedural direction | 0 | NO_ITEMS | Procedure provides clear phase structure |
| A:operative:applying | operative | applying | practical execution | 0 | NO_ITEMS | Steps are adequately sequenced |
| A:operative:judging | operative | judging | performance assessment | 1 | HAS_ITEMS | Missing performance criteria |
| A:operative:reviewing | operative | reviewing | process audit | 0 | NO_ITEMS | Verification table covers core checks |
| A:evaluative:guiding | evaluative | guiding | value orientation | 0 | NO_ITEMS | P1-P4 principles provide value orientation |
| A:evaluative:applying | evaluative | applying | merit application | 0 | NO_ITEMS | Trade-offs T1, T2 adequately frame merit considerations |
| A:evaluative:judging | evaluative | judging | worth determination | 0 | NO_ITEMS | Quality criteria covered via verification |
| A:evaluative:reviewing | evaluative | reviewing | quality appraisal | 0 | NO_ITEMS | Covered by verification table |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A-001 | A:normative:guiding | MissingSlot | Guidance | Guidance | Add explicit guidance on what happens when an operator sets opts that the runtime rejects (e.g., error feedback UX) | Prescriptive direction lens reveals that while the governance passthrough principle is stated, there is no guidance on how the UI should communicate rejection/override to the operator | Guidance.md | P2: Governance Passthrough, Not Override | — | Guidance.md | TBD |
| A-002 | A:normative:applying | TBD_Question | Datasheet | Datasheet | Resolve TBD: Preset Format and Preset CRUD Operations scope (create/select/update/delete) | Mandatory practice lens surfaces that core preset operations and format are marked TBD, blocking implementation | Datasheet.md | Local Presets table | — | Human / design decision | TBD |
| A-003 | A:normative:reviewing | MissingSlot | Specification | Specification | Add requirement or verification check for audit/observability of toolkit state changes (e.g., logging when operator changes opts before a turn) | Regulatory audit lens reveals no mechanism for auditing or tracing what toolkit opts were active when a turn was sent, which matters for debugging governance interactions | Specification.md | Verification table | — | Specification.md | TBD |
| A-004 | A:operative:judging | MissingSlot | Specification | Specification | Add performance/responsiveness acceptance criteria for toolkit panel (e.g., render time, interaction latency targets) | Performance assessment lens reveals no non-functional performance requirements for the panel despite it being a primary operator interaction surface | Specification.md | Requirements section | — | Specification.md | TBD |

---

## Matrix B -- Conceptualization (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| B:data:necessity | data | necessity | essential fact | 1 | HAS_ITEMS | Missing essential data points |
| B:data:sufficiency | data | sufficiency | adequate evidence | 0 | NO_ITEMS | Source references are thorough |
| B:data:completeness | data | completeness | comprehensive record | 1 | HAS_ITEMS | Incomplete attribute set |
| B:data:consistency | data | consistency | reliable measurement | 0 | NO_ITEMS | Data attributes consistently cited |
| B:information:necessity | information | necessity | essential signal | 1 | HAS_ITEMS | Missing signal information |
| B:information:sufficiency | information | sufficiency | adequate context | 0 | NO_ITEMS | Context adequate in current state |
| B:information:completeness | information | completeness | comprehensive account | 0 | NO_ITEMS | Accounts are reasonably comprehensive |
| B:information:consistency | information | consistency | coherent message | 0 | NO_ITEMS | Messaging coherent across docs |
| B:knowledge:necessity | knowledge | necessity | fundamental understanding | 0 | NO_ITEMS | Core concepts well explained |
| B:knowledge:sufficiency | knowledge | sufficiency | competent expertise | 0 | NO_ITEMS | Sufficient expertise conveyed |
| B:knowledge:completeness | knowledge | completeness | thorough mastery | 0 | NO_ITEMS | Knowledge domain adequately covered |
| B:knowledge:consistency | knowledge | consistency | coherent understanding | 1 | HAS_ITEMS | Terminology inconsistency |
| B:wisdom:necessity | wisdom | necessity | essential discernment | 0 | NO_ITEMS | Key discernment captured in Guidance principles |
| B:wisdom:sufficiency | wisdom | sufficiency | adequate judgment | 0 | NO_ITEMS | Trade-offs provide adequate judgment framing |
| B:wisdom:completeness | wisdom | completeness | holistic insight | 0 | NO_ITEMS | Holistic view covered by cross-deliverable considerations |
| B:wisdom:consistency | wisdom | consistency | principled reasoning | 0 | NO_ITEMS | Principles P1-P4 provide principled reasoning |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| B-001 | B:data:necessity | MissingSlot | Datasheet | Datasheet | Add attribute for maximum number of presets (or state explicitly unbounded) | Essential fact lens reveals no data about preset quantity limits, which affects storage design and UX | Datasheet.md | Local Presets table | — | Datasheet.md | TBD |
| B-002 | B:data:completeness | MissingSlot | Datasheet | Datasheet | Add attribute for supported opts field types/validation rules (e.g., model is string/enum, maxTurns is positive integer) | Comprehensive record lens reveals that while opts fields are listed, their data types and validation constraints are not recorded | Datasheet.md | Exposed Options table | — | Datasheet.md | TBD |
| B-003 | B:information:necessity | WeakStatement | Procedure | Procedure | Clarify prerequisite: "Multi-pane layout sidebar integration point is available" -- specify what "available" means (API contract, component interface, or just visual slot) | Essential signal lens reveals that this prerequisite is vague; the integration readiness signal is not defined precisely enough to determine when it is satisfied | Procedure.md | Prerequisites table | — | Procedure.md | TBD |
| B-004 | B:knowledge:consistency | Normalization | Multi | Guidance | Normalize terminology: "CONFIG" vs "CONFIG setting" vs "CONFIG toggle" vs "CONFIG sidebar" used inconsistently across documents to refer to the application configuration mechanism | Coherent understanding lens reveals terminology drift around the CONFIG concept that could cause confusion about whether CONFIG is a panel, a settings object, or a toggle control | Datasheet.md, Specification.md, Guidance.md, Procedure.md | Attributes table; REQ-02; Integration Points table; Step 1.2 | — | Guidance.md (define term) | TBD |

---

## Matrix C -- Formulation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| C:normative:necessity | normative | necessity | obligatory compliance basis | 1 | HAS_ITEMS | Gap in compliance basis |
| C:normative:sufficiency | normative | sufficiency | adequate regulatory competence | 0 | NO_ITEMS | Regulatory competence adequately framed |
| C:normative:completeness | normative | completeness | exhaustive compliance coverage | 1 | HAS_ITEMS | Incomplete compliance coverage |
| C:normative:consistency | normative | consistency | harmonized regulatory integrity | 0 | NO_ITEMS | Regulatory references consistent |
| C:operative:necessity | operative | necessity | core operational capacity | 0 | NO_ITEMS | Core operational steps present |
| C:operative:sufficiency | operative | sufficiency | competent operational practice | 0 | NO_ITEMS | Practice steps are competent |
| C:operative:completeness | operative | completeness | total operational coverage | 1 | HAS_ITEMS | Missing operational coverage |
| C:operative:consistency | operative | consistency | disciplined operational uniformity | 0 | NO_ITEMS | Procedure is internally consistent |
| C:evaluative:necessity | evaluative | necessity | foundational merit recognition | 0 | NO_ITEMS | Merit recognized via OBJ-005 mapping |
| C:evaluative:sufficiency | evaluative | sufficiency | grounded quality appraisal | 0 | NO_ITEMS | Quality appraisal grounded in verification table |
| C:evaluative:completeness | evaluative | completeness | exhaustive value assessment | 0 | NO_ITEMS | Value assessment adequate for current scope |
| C:evaluative:consistency | evaluative | consistency | principled valuation coherence | 0 | NO_ITEMS | Valuation principles coherent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| C-001 | C:normative:necessity | VerificationGap | Specification | Specification | Add explicit verification approach for REQ-04 negative case: confirm that no code path in the toolkit component writes to project files (static analysis or code review check) | Obligatory compliance basis lens reveals that REQ-04 verification ("Confirm that no toolkit state is written to project files") lacks a concrete test method -- "confirm" is underspecified for a governance-critical requirement | Specification.md | Verification table, REQ-04 row | — | Specification.md | TBD |
| C-002 | C:normative:completeness | WeakStatement | Specification | Specification | Clarify REQ-08 SHOULD vs MUST: if preset management is required for SOW-025 acceptance, upgrade to MUST; if optional, document the acceptance boundary explicitly | Exhaustive compliance coverage lens reveals that REQ-08 uses "SHOULD" for preset management while SOW-025 lists "local presets" as a scope item, creating ambiguity about whether presets are required for SOW compliance | Specification.md | REQ-08 | — | Human ruling (SOW-025 interpretation) | TBD |
| C-003 | C:operative:completeness | MissingSlot | Procedure | Procedure | Add a phase or step for error-state handling implementation (e.g., what happens when local storage is full, corrupted, or unavailable) | Total operational coverage lens reveals that while Guidance P4 mentions resilience behaviors, the Procedure has no corresponding implementation step for error/degradation paths | Procedure.md | Steps section (all phases) | — | Procedure.md | TBD |

---

## Matrix F -- Requirements (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| F:normative:necessity | normative | necessity | requisite compliance assurance | 1 | HAS_ITEMS | Missing compliance assurance |
| F:normative:sufficiency | normative | sufficiency | warranted compliance competence | 0 | NO_ITEMS | Compliance competence warranted by sources |
| F:normative:completeness | normative | completeness | total governance scope | 0 | NO_ITEMS | Governance scope adequately bounded |
| F:normative:consistency | normative | consistency | stable prescriptive alignment | 0 | NO_ITEMS | Prescriptive alignment stable across docs |
| F:operative:necessity | operative | necessity | critical execution readiness | 1 | HAS_ITEMS | Readiness gap |
| F:operative:sufficiency | operative | sufficiency | demonstrated procedural competence | 0 | NO_ITEMS | Procedure demonstrates competence |
| F:operative:completeness | operative | completeness | total procedural mastery | 0 | NO_ITEMS | Procedures complete for current scope |
| F:operative:consistency | operative | consistency | consistent operational discipline | 1 | HAS_ITEMS | Inconsistency found |
| F:evaluative:necessity | evaluative | necessity | essential quality discernment | 0 | NO_ITEMS | Quality discernment present |
| F:evaluative:sufficiency | evaluative | sufficiency | substantiated quality judgment | 0 | NO_ITEMS | Quality judgment substantiated |
| F:evaluative:completeness | evaluative | completeness | holistic quality mastery | 0 | NO_ITEMS | Quality coverage holistic enough |
| F:evaluative:consistency | evaluative | consistency | principled quality consistency | 0 | NO_ITEMS | Quality principles consistent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| F-001 | F:normative:necessity | VerificationGap | Specification | Specification | Add verification approach for CONTRACT K-GHOST-1 and K-INVENT-1 compliance: specify how to verify that toolkit does not inject ghost inputs or invent values | Requisite compliance assurance lens reveals that Standards table lists K-GHOST-1 and K-INVENT-1 but the Verification table has no corresponding checks for these contract constraints | Specification.md | Standards table; Verification table | — | Specification.md | TBD |
| F-002 | F:operative:necessity | TBD_Question | Procedure | Procedure | Resolve: which harness APIs must be functional before toolkit panel development can begin? Prerequisites list both turn and session boot APIs but it is unclear if toolkit can be developed/tested with mocked APIs | Critical execution readiness lens reveals that prerequisites depend on DEL-03-01 and DEL-03-02 being functional, but no guidance exists on whether mock/stub APIs suffice for development | Procedure.md | Prerequisites table | — | Human / architecture decision | TBD |
| F-003 | F:operative:consistency | Normalization | Multi | Guidance | Normalize API endpoint references: Procedure uses "/api/harness/turn" and "/api/harness/session/boot" while Datasheet uses "Harness turn API" and "Session Boot Integration" -- standardize to one form | Consistent operational discipline lens reveals inconsistent API references across documents that could cause confusion during implementation | Datasheet.md, Procedure.md | Construction table; Step 3.1 | — | Guidance.md (glossary entry) | TBD |

---

## Matrix D -- Objectives (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| D:normative:guiding | normative | guiding | assured prescriptive mandate | 0 | NO_ITEMS | Prescriptive mandate assured via DIRECTIVE and SPEC references |
| D:normative:applying | normative | applying | enforced conformance duty | 0 | NO_ITEMS | Conformance duty enforced through REQ-04, REQ-05 |
| D:normative:judging | normative | judging | definitive compliance ruling | 0 | NO_ITEMS | Compliance ruling framework established |
| D:normative:reviewing | normative | reviewing | settled compliance inspection | 0 | NO_ITEMS | Inspection approach defined in verification table |
| D:operative:guiding | operative | guiding | resolved operational guidance | 1 | HAS_ITEMS | Guidance gap for inter-deliverable coordination |
| D:operative:applying | operative | applying | settled execution practice | 0 | NO_ITEMS | Execution practice settled in procedure phases |
| D:operative:judging | operative | judging | resolved capability assessment | 0 | NO_ITEMS | Capability assessment resolved via verification |
| D:operative:reviewing | operative | reviewing | systematic process verification | 1 | HAS_ITEMS | Gap in systematic verification |
| D:evaluative:guiding | evaluative | guiding | settled value direction | 0 | NO_ITEMS | Value direction settled via principles P1-P4 |
| D:evaluative:applying | evaluative | applying | realized merit practice | 0 | NO_ITEMS | Merit practice realized through trade-off analysis |
| D:evaluative:judging | evaluative | judging | definitive quality ruling | 0 | NO_ITEMS | Quality ruling framework in place |
| D:evaluative:reviewing | evaluative | reviewing | settled merit inspection | 0 | NO_ITEMS | Merit inspection covered by verification |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| D-001 | D:operative:guiding | RationaleGap | Guidance | Guidance | Add guidance on coordination protocol with DEL-02-04 (layout integration): when to coordinate, what interface contract to expect, and how to handle the case where DEL-02-04 is not yet complete | Resolved operational guidance lens reveals that Guidance mentions DEL-02-04 coordination "may be needed" but provides no concrete protocol, leaving implementers without actionable direction | Guidance.md | Relationship to DEL-02-04 | — | Guidance.md | TBD |
| D-002 | D:operative:reviewing | VerificationGap | Procedure | Specification | Add end-to-end integration verification step covering the full path: operator sets opts in toolkit -> opts appear in API request -> runtime applies fallback for omitted opts -> governance gates hold | Systematic process verification lens reveals that while individual verification checks exist, there is no integrated end-to-end verification step that exercises the full opts flow from UI through runtime | Procedure.md | Verification table | — | Specification.md + Procedure.md | TBD |

---

## Matrix X -- Verification (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| X:guiding:necessity | guiding | necessity | anchored directive foundation | 0 | NO_ITEMS | Directive foundation anchored in SPEC and DIRECTIVE |
| X:guiding:sufficiency | guiding | sufficiency | sufficient directive competence | 0 | NO_ITEMS | Directive competence sufficient |
| X:guiding:completeness | guiding | completeness | holistic directive coverage | 1 | HAS_ITEMS | Incomplete directive coverage |
| X:guiding:consistency | guiding | consistency | unified directive coherence | 0 | NO_ITEMS | Directives coherent across docs |
| X:applying:necessity | applying | necessity | requisite practice enactment | 0 | NO_ITEMS | Practice enactment requirements present |
| X:applying:sufficiency | applying | sufficiency | demonstrated implementation adequacy | 1 | HAS_ITEMS | Implementation adequacy gap |
| X:applying:completeness | applying | completeness | exhaustive practice realization | 0 | NO_ITEMS | Practice scope adequate |
| X:applying:consistency | applying | consistency | dependable practice regularity | 0 | NO_ITEMS | Practice consistency maintained |
| X:judging:necessity | judging | necessity | foundational adjudication warrant | 0 | NO_ITEMS | Adjudication warrant established |
| X:judging:sufficiency | judging | sufficiency | justified adjudication standard | 0 | NO_ITEMS | Adjudication standards justified |
| X:judging:completeness | judging | completeness | exhaustive adjudication scope | 1 | HAS_ITEMS | Incomplete adjudication scope |
| X:judging:consistency | judging | consistency | principled adjudication integrity | 0 | NO_ITEMS | Adjudication integrity maintained |
| X:reviewing:necessity | reviewing | necessity | verified foundational baseline | 0 | NO_ITEMS | Baseline verification present |
| X:reviewing:sufficiency | reviewing | sufficiency | justified examination standard | 0 | NO_ITEMS | Examination standards justified |
| X:reviewing:completeness | reviewing | completeness | exhaustive examination scope | 0 | NO_ITEMS | Examination scope adequate |
| X:reviewing:consistency | reviewing | consistency | harmonized examination integrity | 0 | NO_ITEMS | Examination integrity harmonized |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| X-001 | X:guiding:completeness | RationaleGap | Guidance | Guidance | Add rationale for why the ASSUMPTION tag on OBJ-005 mapping is acceptable, or escalate for human confirmation of the objective association | Holistic directive coverage lens reveals that the OBJ-005 association is marked as ASSUMPTION (best-effort mapping) in both Guidance and Datasheet, meaning the deliverable's objective alignment is not authoritatively confirmed | Guidance.md, Datasheet.md | Purpose section; Identification table | — | Human ruling | TBD |
| X-002 | X:applying:sufficiency | WeakStatement | Specification | Specification | Strengthen REQ-06 verification: "Configure opts via toolkit; confirm they are passed to /api/harness/turn" -- specify what "confirm" means (payload inspection method, expected shape, assertion criteria) | Demonstrated implementation adequacy lens reveals that REQ-06 verification language is vague ("confirm they are passed") without specifying the inspection mechanism or acceptance threshold | Specification.md | Verification table, REQ-06 row | — | Specification.md | TBD |
| X-003 | X:judging:completeness | VerificationGap | Specification | Specification | Add verification for preset persistence across app restarts specifically (REQ-08 verification says "Create a preset, apply it, confirm opts are populated" but does not test preset survival across restarts) | Exhaustive adjudication scope lens reveals that REQ-08 verification tests preset creation and application but not preset persistence, which is a distinct behavior from general state persistence (REQ-03) | Specification.md | Verification table, REQ-08 row | — | Specification.md | TBD |

---

## Matrix E -- Evaluation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| E:normative:necessity | normative | necessity | binding compliance foundation | 0 | NO_ITEMS | Compliance foundation binding and clear |
| E:normative:sufficiency | normative | sufficiency | justified regulatory fulfillment | 0 | NO_ITEMS | Regulatory fulfillment justified |
| E:normative:completeness | normative | completeness | exhaustive regulatory assurance | 1 | HAS_ITEMS | Gap in regulatory assurance |
| E:normative:consistency | normative | consistency | coherent regulatory integrity | 0 | NO_ITEMS | Regulatory integrity coherent |
| E:operative:necessity | operative | necessity | verified operational foundation | 0 | NO_ITEMS | Operational foundation verified |
| E:operative:sufficiency | operative | sufficiency | demonstrated operational sufficiency | 0 | NO_ITEMS | Operational sufficiency demonstrated |
| E:operative:completeness | operative | completeness | complete operational realization | 1 | HAS_ITEMS | Incomplete operational realization |
| E:operative:consistency | operative | consistency | dependable operational integrity | 0 | NO_ITEMS | Operational integrity dependable |
| E:evaluative:necessity | evaluative | necessity | foundational quality warrant | 0 | NO_ITEMS | Quality warrant established |
| E:evaluative:sufficiency | evaluative | sufficiency | demonstrated value sufficiency | 0 | NO_ITEMS | Value sufficiency demonstrated |
| E:evaluative:completeness | evaluative | completeness | exhaustive quality realization | 0 | NO_ITEMS | Quality realization adequate |
| E:evaluative:consistency | evaluative | consistency | principled quality integrity | 0 | NO_ITEMS | Quality integrity principled |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| E-001 | E:normative:completeness | Normalization | Datasheet | Datasheet | Normalize the "Authoritative Status" attribute: Datasheet says "Non-authoritative -- convenience state only" while Specification says "MUST NOT be treated as project truth" and Guidance says "non-authoritative by design" -- adopt a single canonical phrasing and reference it consistently | Exhaustive regulatory assurance lens reveals that while all documents agree on the non-authoritative nature, they phrase it differently, which could lead to drift in how this critical boundary is communicated to implementers | Datasheet.md, Specification.md, Guidance.md | Attributes table; REQ-04; P1 | — | Guidance.md (canonical definition) | TBD |
| E-002 | E:operative:completeness | MissingSlot | Procedure | Procedure | Add step or phase for accessibility considerations in toolkit panel implementation (keyboard navigation, screen reader support for opts controls) | Complete operational realization lens reveals that the Procedure covers functional implementation but has no step addressing accessibility, which is part of complete UX_UI_SLICE realization | Procedure.md | Steps section (all phases) | — | Specification.md (add REQ) + Procedure.md | TBD |
