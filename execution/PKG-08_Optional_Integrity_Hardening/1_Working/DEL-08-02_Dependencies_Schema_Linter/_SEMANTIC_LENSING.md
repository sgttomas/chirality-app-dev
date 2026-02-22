# Semantic Lensing Register: DEL-08-02 Dependencies.csv v3.1 Schema Linter

**Generated:** 2026-02-21
**Deliverable Folder:** execution/PKG-08_Optional_Integrity_Hardening/1_Working/DEL-08-02_Dependencies_Schema_Linter/
**Warnings:** None

**Inputs Read:**
- _CONTEXT.md — `execution/PKG-08_Optional_Integrity_Hardening/1_Working/DEL-08-02_Dependencies_Schema_Linter/_CONTEXT.md`
- _STATUS.md — `execution/PKG-08_Optional_Integrity_Hardening/1_Working/DEL-08-02_Dependencies_Schema_Linter/_STATUS.md`
- _SEMANTIC.md — `execution/PKG-08_Optional_Integrity_Hardening/1_Working/DEL-08-02_Dependencies_Schema_Linter/_SEMANTIC.md`
- Datasheet.md — `execution/PKG-08_Optional_Integrity_Hardening/1_Working/DEL-08-02_Dependencies_Schema_Linter/Datasheet.md`
- Specification.md — `execution/PKG-08_Optional_Integrity_Hardening/1_Working/DEL-08-02_Dependencies_Schema_Linter/Specification.md`
- Guidance.md — `execution/PKG-08_Optional_Integrity_Hardening/1_Working/DEL-08-02_Dependencies_Schema_Linter/Guidance.md`
- Procedure.md — `execution/PKG-08_Optional_Integrity_Hardening/1_Working/DEL-08-02_Dependencies_Schema_Linter/Procedure.md`
- _REFERENCES.md — `execution/PKG-08_Optional_Integrity_Hardening/1_Working/DEL-08-02_Dependencies_Schema_Linter/_REFERENCES.md`

**Purpose:** Apply CHIRALITY_FRAMEWORK matrix cells as lenses over the production documents, capturing warranted enrichment inputs for a later enrichment pass.

## Summary

- Total warranted items: 14
- By document:
  - Datasheet: 3
  - Specification: 5
  - Guidance: 3
  - Procedure: 2
  - Multi: 1
- By matrix:
  - A: 3  B: 1  C: 2  F: 2  D: 2  X: 3  E: 1
- By type:
  - Conflict: 0
  - VerificationGap: 3
  - MissingSlot: 4
  - WeakStatement: 3
  - RationaleGap: 1
  - Normalization: 2
  - TBD_Question: 1
  - MatrixError: 0
- Notable conflicts: 0
- Matrix parse errors: 0

---

## Matrix A -- Orientation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| A:normative:guiding | normative | guiding | prescriptive direction | 1 | HAS_ITEMS | ResponsibleParty TBD weakens prescriptive authority |
| A:normative:applying | normative | applying | mandatory practice | 0 | NO_ITEMS | REQ-01 through REQ-15 provide clear mandatory practices |
| A:normative:judging | normative | judging | compliance determination | 1 | HAS_ITEMS | Verification table covers most but not all requirements uniformly |
| A:normative:reviewing | normative | reviewing | regulatory audit | 0 | NO_ITEMS | Procedure Phase B provides adequate audit trail |
| A:operative:guiding | operative | guiding | procedural direction | 0 | NO_ITEMS | Procedure Phases A-D provide clear procedural direction |
| A:operative:applying | operative | applying | practical execution | 0 | NO_ITEMS | Procedure steps are actionable |
| A:operative:judging | operative | judging | performance assessment | 1 | HAS_ITEMS | No performance/timing criteria for linter execution itself |
| A:operative:reviewing | operative | reviewing | process audit | 0 | NO_ITEMS | Procedure verification table and Records section adequate |
| A:evaluative:guiding | evaluative | guiding | value orientation | 0 | NO_ITEMS | Guidance Purpose section establishes value well |
| A:evaluative:applying | evaluative | applying | merit application | 0 | NO_ITEMS | Guidance P5 addresses value/effort positioning |
| A:evaluative:judging | evaluative | judging | worth determination | 0 | NO_ITEMS | OBJ-007 linkage and SOW-033 contingency adequate |
| A:evaluative:reviewing | evaluative | reviewing | quality appraisal | 0 | NO_ITEMS | Guidance T1-T3 trade-offs cover quality dimensions |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A-001 | A:normative:guiding | WeakStatement | Datasheet | Datasheet | Resolve ResponsibleParty from TBD to an assigned party or document why it remains unassigned | ResponsibleParty=TBD in Datasheet Identification table weakens prescriptive authority -- no one is accountable for the normative direction of this deliverable | Datasheet.md | Identification | | Datasheet.md | TBD |
| A-002 | A:normative:judging | VerificationGap | Specification | Specification | Add acceptance criteria for REQ-02 (Column Order Tolerance) specifying whether ANY order is valid or only permutations of the logical order | REQ-02 uses SHOULD and notes it is an ASSUMPTION; the verification entry says "reordered-column CSV passes" but does not specify what orderings are tested, leaving compliance determination ambiguous | Specification.md | REQ-02; Verification | | Specification.md | TBD |
| A-003 | A:operative:judging | MissingSlot | Specification | Specification | Add performance acceptance criteria for the linter (e.g., maximum execution time per file, maximum memory usage, or state "no performance requirement") | No performance assessment criteria exist for the linter itself; for CI-level tooling, execution time and resource consumption could affect pipeline feasibility | Specification.md | Requirements (entire section scanned) | | Specification.md | TBD |

---

## Matrix B -- Conceptualization (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| B:data:necessity | data | necessity | essential fact | 0 | NO_ITEMS | Datasheet Attributes and Conditions tables enumerate essential facts |
| B:data:sufficiency | data | sufficiency | adequate evidence | 0 | NO_ITEMS | Source column in Datasheet traces evidence adequately |
| B:data:completeness | data | completeness | comprehensive record | 1 | HAS_ITEMS | Python version floor not recorded |
| B:data:consistency | data | consistency | reliable measurement | 0 | NO_ITEMS | Column counts and enum families consistently cited from SPEC |
| B:information:necessity | information | necessity | essential signal | 0 | NO_ITEMS | SOW-033 contingency signal is clear across all docs |
| B:information:sufficiency | information | sufficiency | adequate context | 0 | NO_ITEMS | Guidance Considerations provide adequate context |
| B:information:completeness | information | completeness | comprehensive account | 0 | NO_ITEMS | Cross-references to SPEC, TYPES, CONTRACT, PLAN are comprehensive |
| B:information:consistency | information | consistency | coherent message | 0 | NO_ITEMS | Messages are coherent across the four docs |
| B:knowledge:necessity | knowledge | necessity | fundamental understanding | 0 | NO_ITEMS | Schema structure knowledge is well documented |
| B:knowledge:sufficiency | knowledge | sufficiency | competent expertise | 0 | NO_ITEMS | Sufficient technical detail for implementation |
| B:knowledge:completeness | knowledge | completeness | thorough mastery | 0 | NO_ITEMS | Validation rules enumerated thoroughly |
| B:knowledge:consistency | knowledge | consistency | coherent understanding | 0 | NO_ITEMS | Understanding is consistent across docs |
| B:wisdom:necessity | wisdom | necessity | essential discernment | 0 | NO_ITEMS | Error vs Warning distinction (P2) provides essential discernment |
| B:wisdom:sufficiency | wisdom | sufficiency | adequate judgment | 0 | NO_ITEMS | Trade-offs T1-T3 support adequate judgment |
| B:wisdom:completeness | wisdom | completeness | holistic insight | 0 | NO_ITEMS | Guidance C3-C4 relate this deliverable holistically to PKG-08 |
| B:wisdom:consistency | wisdom | consistency | principled reasoning | 0 | NO_ITEMS | Principles P1-P5 form a consistent reasoning framework |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| B-001 | B:data:completeness | MissingSlot | Datasheet | Datasheet | Record the minimum Python version (e.g., 3.8+) as a Conditions entry, or explicitly mark as TBD with a rationale | Guidance C1 mentions "3.8+ is a reasonable floor" but this is not captured as a data record in Datasheet Conditions; the Python version is listed as "Python 3.x runtime (specific version TBD)" without the floor guidance | Datasheet.md; Guidance.md | Conditions (External Dependencies); Guidance C1 | | Datasheet.md | TBD |

---

## Matrix C -- Formulation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| C:normative:necessity | normative | necessity | Enforceable Standard | 0 | NO_ITEMS | REQ-01 through REQ-15 constitute enforceable standards |
| C:normative:sufficiency | normative | sufficiency | Mandated Adequacy | 1 | HAS_ITEMS | ASSUMPTION-tagged requirements lack adequacy grounding |
| C:normative:completeness | normative | completeness | Exhaustive Compliance Coverage | 0 | NO_ITEMS | 15 requirements with verification entries cover the schema |
| C:normative:consistency | normative | consistency | Harmonized Compliance | 0 | NO_ITEMS | Requirements consistently aligned with SPEC Section 6 |
| C:operative:necessity | operative | necessity | Operational Prerequisite | 0 | NO_ITEMS | Prerequisites PRE-01 through PRE-04 are clear |
| C:operative:sufficiency | operative | sufficiency | Proven Readiness | 0 | NO_ITEMS | Steps specify verification at each phase |
| C:operative:completeness | operative | completeness | Comprehensive Execution | 1 | HAS_ITEMS | No error-handling procedure for linter runtime failures |
| C:operative:consistency | operative | consistency | Reproducible Operation | 0 | NO_ITEMS | Steps are deterministic and repeatable |
| C:evaluative:necessity | evaluative | necessity | Intrinsic Significance | 0 | NO_ITEMS | Purpose well justified in Guidance |
| C:evaluative:sufficiency | evaluative | sufficiency | Justified Appraisal | 0 | NO_ITEMS | P5 and T1-T3 provide justified appraisal framework |
| C:evaluative:completeness | evaluative | completeness | Holistic Valuation | 0 | NO_ITEMS | Value proposition covers CI, drift detection, developer confidence |
| C:evaluative:consistency | evaluative | consistency | Principled Valuation | 0 | NO_ITEMS | Principles P1-P5 are consistent with stated values |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| C-001 | C:normative:sufficiency | WeakStatement | Specification | Guidance | Add rationale in Guidance for why REQ-13 (exit codes), REQ-14 (JSON output), and REQ-15 (batch mode) are included despite being tagged ASSUMPTION with no governance source, or demote them to SHOULD-level recommendations | REQ-13, REQ-14, REQ-15 are stated as requirements but tagged ASSUMPTION with no authoritative source; their mandated adequacy is self-asserted rather than grounded in governance | Specification.md | REQ-13; REQ-14; REQ-15 | | Guidance.md | TBD |
| C-002 | C:operative:completeness | MissingSlot | Procedure | Procedure | Add a step or note covering linter error handling: what happens if the linter itself crashes (e.g., malformed CSV that causes a parser exception vs. a validation error); define expected behavior and exit code for unhandled exceptions | Procedure covers validation-error exit codes but not the linter's own failure modes (e.g., Python exception on severely malformed input); comprehensive execution requires accounting for tool failure distinct from validation failure | Procedure.md | Steps Phase A, Step A9 | | Procedure.md | TBD |

---

## Matrix F -- Requirements (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| F:normative:necessity | normative | necessity | Mandatory Baseline | 0 | NO_ITEMS | 15 requirements form a clear mandatory baseline |
| F:normative:sufficiency | normative | sufficiency | Demonstrable Conformance | 1 | HAS_ITEMS | Some verification approaches lack specific pass/fail criteria |
| F:normative:completeness | normative | completeness | Total Conformance Scope | 0 | NO_ITEMS | All 15 requirements have verification entries |
| F:normative:consistency | normative | consistency | Systematic Coherence | 0 | NO_ITEMS | Requirements consistently reference SPEC sections |
| F:operative:necessity | operative | necessity | Critical Precondition | 0 | NO_ITEMS | Prerequisites are identified |
| F:operative:sufficiency | operative | sufficiency | Capable Fulfillment | 0 | NO_ITEMS | Procedure steps sufficient for implementation |
| F:operative:completeness | operative | completeness | Exhaustive Process Control | 0 | NO_ITEMS | Phases A-D cover full lifecycle |
| F:operative:consistency | operative | consistency | Consistent Execution | 0 | NO_ITEMS | Steps follow logical order with consistent pattern |
| F:evaluative:necessity | evaluative | necessity | Foundational Merit | 0 | NO_ITEMS | Foundational merit established in Guidance Purpose |
| F:evaluative:sufficiency | evaluative | sufficiency | Substantiated Assessment | 0 | NO_ITEMS | Trade-offs and considerations substantiate choices |
| F:evaluative:completeness | evaluative | completeness | Comprehensive Valuation | 1 | HAS_ITEMS | No acceptance criteria for documentation artifact quality |
| F:evaluative:consistency | evaluative | consistency | Grounded Evaluation | 0 | NO_ITEMS | Evaluation criteria grounded in SPEC |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| F-001 | F:normative:sufficiency | VerificationGap | Specification | Specification | Strengthen verification entries for REQ-09 EXECUTION row rules: specify which "preferred execution enums" must be tested and what the pass/fail boundary is | REQ-09 references "preferred execution enums" for EXECUTION rows but does not enumerate them; the verification entry says "EXECUTION with non-preferred type warns" without specifying which types are non-preferred, making demonstrable conformance ambiguous | Specification.md | REQ-09; Verification | | Specification.md | TBD |
| F-002 | F:evaluative:completeness | MissingSlot | Specification | Specification | Add acceptance criteria for the DOC artifact (usage documentation): define what "complete and consistent" means in measurable terms, or cross-reference to Procedure Step C1 checklist | Specification Documentation table lists DOC artifact as TBD with no acceptance criteria; Procedure Step C1 lists documentation topics but Specification Verification table has no entry for documentation quality | Specification.md | Documentation; Verification | | Specification.md | TBD |

---

## Matrix D -- Objectives (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| D:normative:guiding | normative | guiding | Resolved Directive | 0 | NO_ITEMS | Directives are resolved and traceable to SPEC |
| D:normative:applying | normative | applying | Enforced Adherence | 0 | NO_ITEMS | Requirements enforce adherence to schema rules |
| D:normative:judging | normative | judging | Conclusive Conformance | 0 | NO_ITEMS | Verification table provides conformance testing plan |
| D:normative:reviewing | normative | reviewing | Harmonized Examination | 0 | NO_ITEMS | Procedure Phase B provides examination steps |
| D:operative:guiding | operative | guiding | Grounded Guidance | 1 | HAS_ITEMS | Script placement guidance is tentative |
| D:operative:applying | operative | applying | Actualized Implementation | 0 | NO_ITEMS | Implementation steps are concrete |
| D:operative:judging | operative | judging | Settled Performance Verdict | 0 | NO_ITEMS | Verification checks at each step |
| D:operative:reviewing | operative | reviewing | Confirmed Process Regularity | 0 | NO_ITEMS | Process flow is regular and auditable |
| D:evaluative:guiding | evaluative | guiding | Settled Value Direction | 0 | NO_ITEMS | Value direction settled in Guidance Purpose |
| D:evaluative:applying | evaluative | applying | Grounded Merit Practice | 0 | NO_ITEMS | P5 grounds merit in low-effort/high-value positioning |
| D:evaluative:judging | evaluative | judging | Definitive Valuation | 1 | HAS_ITEMS | No definition of "done" for the deliverable as a whole |
| D:evaluative:reviewing | evaluative | reviewing | Confirmed Worth Audit | 0 | NO_ITEMS | SOW-033 contingency provides appropriate review gate |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| D-001 | D:operative:guiding | WeakStatement | Procedure | Guidance | Resolve the script placement location from ASSUMPTION to a decision; state whether `_Scripts/validate_dependencies.py` is the canonical path or if alternatives are acceptable | Procedure Step D1 marks the script location as ASSUMPTION with "Candidate locations" phrasing; grounded guidance requires a settled decision on artifact placement or explicit criteria for choosing | Procedure.md | Steps Phase D, Step D1 | | Guidance.md | TBD |
| D-002 | D:evaluative:judging | TBD_Question | Multi | Specification | Define deliverable-level acceptance criteria: what constitutes "done" for DEL-08-02 as a whole (e.g., all unit tests pass + integration tests pass + documentation reviewed + batch mode validated against examples) | No single document states a definitive completion/acceptance criterion for the deliverable; Procedure has per-step verification but no aggregate "definition of done"; Specification has per-requirement verification but no overall acceptance gate | Specification.md; Procedure.md | Verification (both docs) | | Specification.md | TBD |

---

## Matrix X -- Verification (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| X:guiding:necessity | guiding | necessity | Validated Imperative | 0 | NO_ITEMS | Purpose and necessity validated in Guidance |
| X:guiding:sufficiency | guiding | sufficiency | Substantiated Direction | 0 | NO_ITEMS | Directional choices substantiated with rationale |
| X:guiding:completeness | guiding | completeness | Exhaustive Directional Span | 0 | NO_ITEMS | Guidance covers principles, considerations, trade-offs |
| X:guiding:consistency | guiding | consistency | Principled Coherence | 0 | NO_ITEMS | Principles P1-P5 are internally coherent |
| X:applying:necessity | applying | necessity | Actualized Obligation | 0 | NO_ITEMS | Obligations mapped to implementation steps |
| X:applying:sufficiency | applying | sufficiency | Proven Competence | 1 | HAS_ITEMS | No verification that enum values in Specification match SPEC Section 6.3 exhaustively |
| X:applying:completeness | applying | completeness | Complete Application | 0 | NO_ITEMS | All 15 requirements have implementation steps |
| X:applying:consistency | applying | consistency | Disciplined Consistency | 1 | HAS_ITEMS | Terminology inconsistency in ASSUMPTION labeling |
| X:judging:necessity | judging | necessity | Authoritative Determination | 0 | NO_ITEMS | Requirement sources identified authoritatively |
| X:judging:sufficiency | judging | sufficiency | Verified Satisfaction | 0 | NO_ITEMS | Verification table maps requirements to test approaches |
| X:judging:completeness | judging | completeness | Comprehensive Ruling | 0 | NO_ITEMS | 15 requirements all have verification entries |
| X:judging:consistency | judging | consistency | Principled Adjudication | 0 | NO_ITEMS | Consistent error/warning distinction per P2 |
| X:reviewing:necessity | reviewing | necessity | Foundational Audit | 1 | HAS_ITEMS | No audit/review step for the validation rule catalog itself |
| X:reviewing:sufficiency | reviewing | sufficiency | Calibrated Review | 0 | NO_ITEMS | Phase B testing provides calibrated review |
| X:reviewing:completeness | reviewing | completeness | Exhaustive Scrutiny | 0 | NO_ITEMS | Phase B + Phase D provide exhaustive testing |
| X:reviewing:consistency | reviewing | consistency | Dependable Examination | 0 | NO_ITEMS | Examination process is dependable and repeatable |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| X-001 | X:applying:sufficiency | VerificationGap | Specification | Specification | Cross-verify that the enum values listed in REQ-05 exactly match `docs/SPEC.md` Section 6.3; if verified, add a note confirming the snapshot date; if not yet verified, mark as requiring verification before implementation | REQ-05 enumerates specific enum values inline; these are a snapshot that could drift from the authoritative source; proven competence requires confirming the snapshot is accurate and noting when it was taken | Specification.md | REQ-05 | | Specification.md | TBD |
| X-002 | X:applying:consistency | Normalization | Datasheet | Guidance | Standardize ASSUMPTION labeling across all documents: adopt a consistent format (e.g., always bold `**ASSUMPTION**` with a rationale clause) and consolidate the assumption register in one location | ASSUMPTIONs appear in varying formats across documents: some have explanatory clauses, some do not; Datasheet has 4 inline ASSUMPTIONs, Specification has 5, Guidance has 3, Procedure has 3; no consolidated assumption register exists | Datasheet.md; Specification.md; Guidance.md; Procedure.md | entire document scanned (all four) | | Guidance.md | TBD |
| X-003 | X:reviewing:necessity | RationaleGap | Procedure | Guidance | Add a rationale or review step for the validation rule catalog (Step A1 output): explain how to confirm the rule catalog is complete against SPEC Section 6 before proceeding to implementation | Procedure Step A1 says "Rule catalog covers all 15 specification requirements" but does not describe how to verify completeness against the upstream SPEC (as opposed to just counting to 15); a foundational audit requires traceability from SPEC rules to catalog entries | Procedure.md | Steps Phase A, Step A1 | | Guidance.md | TBD |

---

## Matrix E -- Evaluation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| E:normative:necessity | normative | necessity | Ratified Assurance | 0 | NO_ITEMS | Requirements ratified through governance traceability |
| E:normative:sufficiency | normative | sufficiency | Validated Conformance | 0 | NO_ITEMS | Verification table validates conformance approach |
| E:normative:completeness | normative | completeness | Absolute Oversight | 0 | NO_ITEMS | Comprehensive requirement and verification coverage |
| E:normative:consistency | normative | consistency | Disciplined Uniformity | 1 | HAS_ITEMS | Inconsistent normative keyword usage |
| E:operative:necessity | operative | necessity | Actualized Operational Basis | 0 | NO_ITEMS | Operational basis established through prereqs and steps |
| E:operative:sufficiency | operative | sufficiency | Assured Performance | 0 | NO_ITEMS | Step-level verification provides performance assurance |
| E:operative:completeness | operative | completeness | Total Operational Realization | 0 | NO_ITEMS | Phases A-D cover full realization lifecycle |
| E:operative:consistency | operative | consistency | Methodical Reliability | 0 | NO_ITEMS | Steps follow a methodical pattern |
| E:evaluative:necessity | evaluative | necessity | Ratified Significance | 0 | NO_ITEMS | Significance ratified through OBJ-007 linkage |
| E:evaluative:sufficiency | evaluative | sufficiency | Proven Worth Adequacy | 0 | NO_ITEMS | Worth adequacy established in Guidance Purpose and P5 |
| E:evaluative:completeness | evaluative | completeness | Exhaustive Merit Judgment | 0 | NO_ITEMS | Merit judgment covered across Guidance trade-offs |
| E:evaluative:consistency | evaluative | consistency | Steadfast Valuation | 0 | NO_ITEMS | Valuation is consistent: low-effort/high-value positioning stable |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| E-001 | E:normative:consistency | Normalization | Specification | Specification | Normalize normative keyword usage: REQ-02 uses SHOULD while REQ-09 EXECUTION rule uses MUST but says "preferred execution enums" (a SHOULD-level concept); clarify whether EXECUTION DependencyType validation is MUST (error) or SHOULD (warning) | REQ-09 states the linter "MUST validate EXECUTION row rules" but describes the check as using "preferred execution enums" which implies a SHOULD-level preference, not a MUST-level mandate; this creates ambiguity in whether violations are errors or warnings, undermining disciplined uniformity | Specification.md | REQ-09 | | Specification.md | TBD |
