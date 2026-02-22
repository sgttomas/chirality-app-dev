# Semantic Lensing Register: DEL-03-04 Subagent Governance Fail-Closed Enforcement

**Generated:** 2026-02-21
**Deliverable Folder:** execution/PKG-03_Harness_Runtime_Core/1_Working/DEL-03-04_Subagent_Governance_FailClosed/
**Warnings:** None

**Inputs Read:**
- _CONTEXT.md — `execution/PKG-03_Harness_Runtime_Core/1_Working/DEL-03-04_Subagent_Governance_FailClosed/_CONTEXT.md`
- _STATUS.md — `execution/PKG-03_Harness_Runtime_Core/1_Working/DEL-03-04_Subagent_Governance_FailClosed/_STATUS.md`
- _SEMANTIC.md — `execution/PKG-03_Harness_Runtime_Core/1_Working/DEL-03-04_Subagent_Governance_FailClosed/_SEMANTIC.md`
- Datasheet.md — `execution/PKG-03_Harness_Runtime_Core/1_Working/DEL-03-04_Subagent_Governance_FailClosed/Datasheet.md`
- Specification.md — `execution/PKG-03_Harness_Runtime_Core/1_Working/DEL-03-04_Subagent_Governance_FailClosed/Specification.md`
- Guidance.md — `execution/PKG-03_Harness_Runtime_Core/1_Working/DEL-03-04_Subagent_Governance_FailClosed/Guidance.md`
- Procedure.md — `execution/PKG-03_Harness_Runtime_Core/1_Working/DEL-03-04_Subagent_Governance_FailClosed/Procedure.md`
- _REFERENCES.md — `execution/PKG-03_Harness_Runtime_Core/1_Working/DEL-03-04_Subagent_Governance_FailClosed/_REFERENCES.md`

**Purpose:** Apply CHIRALITY_FRAMEWORK matrix cells as lenses over the production documents, capturing warranted enrichment inputs for a later enrichment pass.

## Summary

- Total warranted items: 19
- By document:
  - Datasheet: 3
  - Specification: 7
  - Guidance: 4
  - Procedure: 3
  - Multi: 2
- By matrix:
  - A: 4  B: 3  C: 2  F: 3  D: 2  X: 3  E: 2
- By type:
  - Conflict: 0
  - VerificationGap: 5
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
| A:normative:guiding | normative | guiding | prescriptive direction | 1 | HAS_ITEMS | Gate evaluation order not prescribed in Specification |
| A:normative:applying | normative | applying | mandatory practice | 1 | HAS_ITEMS | Strict equality operator usage is clear |
| A:normative:judging | normative | judging | compliance determination | 1 | HAS_ITEMS | Verification table present but missing acceptance criteria detail |
| A:normative:reviewing | normative | reviewing | regulatory audit | 1 | HAS_ITEMS | Audit trail logging requirements underspecified |
| A:operative:guiding | operative | guiding | procedural direction | 0 | NO_ITEMS | Step-by-step procedure is well-structured |
| A:operative:applying | operative | applying | practical execution | 0 | NO_ITEMS | Implementation steps are actionable |
| A:operative:judging | operative | judging | performance assessment | 0 | NO_ITEMS | Verification checks present in Procedure |
| A:operative:reviewing | operative | reviewing | process audit | 0 | NO_ITEMS | Code review record listed in Records |
| A:evaluative:guiding | evaluative | guiding | value orientation | 0 | NO_ITEMS | Principles section in Guidance covers value orientation well |
| A:evaluative:applying | evaluative | applying | merit application | 0 | NO_ITEMS | Trade-offs table documents choices |
| A:evaluative:judging | evaluative | judging | worth determination | 0 | NO_ITEMS | Rationale provided for key design choices |
| A:evaluative:reviewing | evaluative | reviewing | quality appraisal | 0 | NO_ITEMS | Quality checks embedded in Procedure verification |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A-001 | A:normative:guiding | WeakStatement | Specification | Specification | Clarify whether gate evaluation order (REQ-01 through REQ-06) is normatively prescribed or an implementation recommendation; Procedure Step 2 prescribes a specific order but Specification does not mandate sequencing | Procedure prescribes a specific evaluation order (environment first, then persona, then metadata fields) but Specification lists requirements without mandating order; this could affect short-circuit behavior and logging | Specification.md, Procedure.md | Specification.md#Requirements, Procedure.md#Step 2 | | SPEC Section 9.7 | TBD |
| A-002 | A:normative:applying | MissingSlot | Specification | Specification | Add explicit requirement for logging the gate evaluation result (allow/deny with reason) as a normative mandate, not just procedural guidance | Procedure Step 2.4 says "Log the gate evaluation result" but no corresponding REQ exists in Specification; logging is essential for audit but is not normatively required | Specification.md | Specification.md#Requirements (entire section scanned) | | | TBD |
| A-003 | A:normative:judging | VerificationGap | Specification | Specification | Add acceptance criteria specifying the exact test assertion pattern for strict type checking (e.g., that `contextSealed: "true"` as string is explicitly tested) | REQ-04 and REQ-05 require strict boolean `true` but the Verification table entries do not all enumerate the type-coercion test cases; REQ-04 mentions `string "true"` but REQ-05 does not | Specification.md | Specification.md#Verification (REQ-05 row) | | | TBD |
| A-004 | A:normative:reviewing | MissingSlot | Specification | Specification | Add a requirement or verification criterion for audit trail completeness: what is logged, at what level, and what fields are included in the log record | Regulatory audit perspective reveals no normative requirement for what the audit log record must contain; Procedure mentions logging and Guidance mentions audit context but neither the Datasheet nor Specification defines the log schema | Specification.md, Guidance.md | Specification.md#Requirements (entire section scanned), Guidance.md#Considerations (approvedBy section) | | | TBD |

---

## Matrix B — Conceptualization (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| B:data:necessity | data | necessity | essential fact | 1 | HAS_ITEMS | K-GATE-1 referenced but not defined in accessible documents |
| B:data:sufficiency | data | sufficiency | adequate evidence | 0 | NO_ITEMS | Attributes table provides sufficient data |
| B:data:completeness | data | completeness | comprehensive record | 1 | HAS_ITEMS | Datasheet missing Responsible Party |
| B:data:consistency | data | consistency | reliable measurement | 0 | NO_ITEMS | Consistent SPEC Section 9.7 sourcing throughout |
| B:information:necessity | information | necessity | essential signal | 0 | NO_ITEMS | Gate conditions clearly signal pass/fail |
| B:information:sufficiency | information | sufficiency | adequate context | 0 | NO_ITEMS | Context adequate across documents |
| B:information:completeness | information | completeness | comprehensive account | 0 | NO_ITEMS | Full account of all gate conditions present |
| B:information:consistency | information | consistency | coherent message | 0 | NO_ITEMS | Consistent messaging across all four documents |
| B:knowledge:necessity | knowledge | necessity | fundamental understanding | 0 | NO_ITEMS | Guidance Principles section covers fundamentals |
| B:knowledge:sufficiency | knowledge | sufficiency | competent expertise | 0 | NO_ITEMS | Sufficient for implementation |
| B:knowledge:completeness | knowledge | completeness | thorough mastery | 0 | NO_ITEMS | Comprehensive coverage of governance domain |
| B:knowledge:consistency | knowledge | consistency | coherent understanding | 0 | NO_ITEMS | Understanding is coherent across documents |
| B:wisdom:necessity | wisdom | necessity | essential discernment | 1 | HAS_ITEMS | Graceful degradation rationale could be more explicit about edge cases |
| B:wisdom:sufficiency | wisdom | sufficiency | adequate judgment | 0 | NO_ITEMS | Trade-offs table demonstrates adequate judgment |
| B:wisdom:completeness | wisdom | completeness | holistic insight | 0 | NO_ITEMS | Holistic view present in Guidance |
| B:wisdom:consistency | wisdom | consistency | principled reasoning | 0 | NO_ITEMS | Principled reasoning evident throughout |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| B-001 | B:data:necessity | TBD_Question | Specification | Specification | Clarify the definition and source of K-GATE-1; REQ-05 references "K-GATE-1 minimum gate requirement" but this invariant is not listed in the Standards table or Datasheet References | K-GATE-1 is cited as rationale for REQ-05 but does not appear in the CONTRACT.md references listed in the Datasheet or Specification Standards table; it may be a valid invariant that needs to be confirmed or a reference error | Specification.md, Datasheet.md | Specification.md#REQ-05, Datasheet.md#References | | CONTRACT.md | TBD |
| B-002 | B:data:completeness | MissingSlot | Datasheet | Datasheet | Record the Responsible Party for DEL-03-04 (currently TBD) | Datasheet Identification table lists "Responsible Party: TBD"; this essential descriptive fact is missing | Datasheet.md | Datasheet.md#Identification | | | TBD |
| B-003 | B:wisdom:necessity | RationaleGap | Guidance | Guidance | Add guidance on what happens when multiple gate conditions fail simultaneously: are all failures logged, or only the first? What is the expected operator experience? | Guidance covers graceful degradation at a principle level but does not address the discernment needed when multiple gates fail: should all failures be reported or only the first-failing gate? This affects debugging and operator understanding | Guidance.md | Guidance.md#Graceful Degradation | | | TBD |

---

## Matrix C — Formulation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| C:normative:necessity | normative | necessity | Obligatory Compliance Basis | 0 | NO_ITEMS | Compliance basis well-established |
| C:normative:sufficiency | normative | sufficiency | Mandated Adequacy Proof | 1 | HAS_ITEMS | Proof of adequacy for persona allowlist mechanism underspecified |
| C:normative:completeness | normative | completeness | Exhaustive Regulatory Coverage | 0 | NO_ITEMS | All SPEC 9.7 conditions covered |
| C:normative:consistency | normative | consistency | Uniform Regulatory Discipline | 0 | NO_ITEMS | Consistent discipline across requirements |
| C:operative:necessity | operative | necessity | Critical Operational Capacity | 0 | NO_ITEMS | Operational capacity addressed |
| C:operative:sufficiency | operative | sufficiency | Competent Procedural Adequacy | 0 | NO_ITEMS | Procedure is adequately detailed |
| C:operative:completeness | operative | completeness | Thorough Operational Coverage | 1 | HAS_ITEMS | Missing explicit rollback/recovery procedure |
| C:operative:consistency | operative | consistency | Reliable Process Coherence | 0 | NO_ITEMS | Process is coherent |
| C:evaluative:necessity | evaluative | necessity | Foundational Value Imperative | 0 | NO_ITEMS | Security value clearly articulated |
| C:evaluative:sufficiency | evaluative | sufficiency | Substantiated Value Judgment | 0 | NO_ITEMS | Value judgments substantiated in Guidance |
| C:evaluative:completeness | evaluative | completeness | Holistic Worth Assessment | 0 | NO_ITEMS | Worth assessment holistic in Guidance |
| C:evaluative:consistency | evaluative | consistency | Principled Evaluative Coherence | 0 | NO_ITEMS | Evaluative coherence maintained |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| C-001 | C:normative:sufficiency | WeakStatement | Specification | Specification | Strengthen the persona allowlist mechanism definition: REQ-02 contains an ASSUMPTION about how the allowlist is determined (presence of non-empty `subagents` array); clarify whether this assumption is confirmed or TBD | REQ-02 labels the allowlist mechanism as an ASSUMPTION, which means the mandated adequacy proof for this gate is not fully established; the gate logic depends on an unconfirmed interpretation | Specification.md | Specification.md#REQ-02 | | SPEC Section 9.7 | TBD |
| C-002 | C:operative:completeness | MissingSlot | Procedure | Procedure | Add a step or substep addressing what happens if the governance gate function itself throws an error (runtime exception in gate evaluation); should the system fail-closed (deny) or propagate the error? | Thorough operational coverage requires addressing the error path within the gate function itself, not just the deny path; Procedure does not cover what happens if the gate code encounters an unexpected runtime error | Procedure.md | Procedure.md#Step 2 | | | TBD |

---

## Matrix F — Requirements (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| F:normative:necessity | normative | necessity | Enforceable Compliance Mandate | 1 | HAS_ITEMS | Enforcement point location not specified |
| F:normative:sufficiency | normative | sufficiency | Prescribed Evidence Threshold | 0 | NO_ITEMS | Evidence thresholds clear in Verification table |
| F:normative:completeness | normative | completeness | Total Regulatory Assurance | 0 | NO_ITEMS | Regulatory assurance complete |
| F:normative:consistency | normative | consistency | Harmonized Compliance Integrity | 1 | HAS_ITEMS | K-AUTH-2 referenced but not in Datasheet |
| F:operative:necessity | operative | necessity | Essential Process Competence | 0 | NO_ITEMS | Process competence addressed |
| F:operative:sufficiency | operative | sufficiency | Demonstrated Procedural Fitness | 0 | NO_ITEMS | Procedures demonstrate fitness |
| F:operative:completeness | operative | completeness | Comprehensive Operational Mastery | 0 | NO_ITEMS | Operational mastery comprehensive |
| F:operative:consistency | operative | consistency | Systematic Operational Reliability | 0 | NO_ITEMS | Reliability addressed |
| F:evaluative:necessity | evaluative | necessity | Intrinsic Value Foundation | 0 | NO_ITEMS | Value foundation established |
| F:evaluative:sufficiency | evaluative | sufficiency | Warranted Value Appraisal | 0 | NO_ITEMS | Value appraisal warranted |
| F:evaluative:completeness | evaluative | completeness | Exhaustive Worth Account | 1 | HAS_ITEMS | Concurrency scenario not addressed |
| F:evaluative:consistency | evaluative | consistency | Principled Worth Integrity | 0 | NO_ITEMS | Worth integrity maintained |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| F-001 | F:normative:necessity | VerificationGap | Specification | Specification | Add a verification criterion that confirms the governance gate is the sole enforcement point and cannot be bypassed by alternative code paths to subagent injection | Enforceable compliance mandate requires confidence that the gate is the single enforcement point; REQ-10 addresses UI bypass but no verification exists for alternative code-path bypass | Specification.md | Specification.md#Verification (REQ-10 row) | | | TBD |
| F-002 | F:normative:consistency | Normalization | Multi | Guidance | Harmonize CONTRACT.md invariant references: Specification REQ-06 cites K-AUTH-1 and K-AUTH-2; Datasheet References and Specification Standards list K-AUTH-1 but K-AUTH-2 is only in the Specification body, not consistently listed | Inconsistent listing of K-AUTH-2 across documents risks drift in which invariants are considered in scope | Specification.md, Datasheet.md | Specification.md#REQ-06, Specification.md#Standards, Datasheet.md#References | | CONTRACT.md | TBD |
| F-003 | F:evaluative:completeness | TBD_Question | Guidance | Guidance | Address whether concurrent turns from the same session could create race conditions in governance gate evaluation (e.g., governance metadata changed between gate check and injection) | Exhaustive worth account requires considering concurrency scenarios; neither Guidance nor Specification addresses whether the gate evaluation is atomic with respect to the injection action | Guidance.md | Guidance.md#Considerations (entire section scanned) | | | TBD |

---

## Matrix D — Objectives (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| D:normative:guiding | normative | guiding | Decisive Regulatory Direction | 0 | NO_ITEMS | Direction is decisive |
| D:normative:applying | normative | applying | Binding Practice Standard | 0 | NO_ITEMS | Practice standard is binding |
| D:normative:judging | normative | judging | Conclusive Compliance Ruling | 1 | HAS_ITEMS | No requirement for a machine-readable gate result format |
| D:normative:reviewing | normative | reviewing | Definitive Compliance Audit | 0 | NO_ITEMS | Audit covered |
| D:operative:guiding | operative | guiding | Established Procedural Guidance | 0 | NO_ITEMS | Guidance established |
| D:operative:applying | operative | applying | Proven Operational Execution | 0 | NO_ITEMS | Execution path clear |
| D:operative:judging | operative | judging | Conclusive Performance Appraisal | 1 | HAS_ITEMS | Performance benchmarks absent |
| D:operative:reviewing | operative | reviewing | Verified Process Integrity | 0 | NO_ITEMS | Integrity verification present |
| D:evaluative:guiding | evaluative | guiding | Grounded Value Direction | 0 | NO_ITEMS | Value direction grounded in Guidance |
| D:evaluative:applying | evaluative | applying | Justified Merit Practice | 0 | NO_ITEMS | Merit practice justified |
| D:evaluative:judging | evaluative | judging | Conclusive Value Determination | 0 | NO_ITEMS | Value determination present |
| D:evaluative:reviewing | evaluative | reviewing | Verified Quality Soundness | 0 | NO_ITEMS | Quality soundness addressed |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| D-001 | D:normative:judging | VerificationGap | Specification | Specification | Define the structured result format for the gate function return value; Procedure Step 2.3 mentions "structured result indicating allow/deny and which gate denied" but Specification does not require a specific return schema | Conclusive compliance ruling requires a defined output format so that consumers of the gate result can reliably interpret it; currently the format is procedural guidance, not a normative requirement | Specification.md, Procedure.md | Specification.md#Requirements (entire section scanned), Procedure.md#Step 2 | | | TBD |
| D-002 | D:operative:judging | VerificationGap | Specification | Specification | Add performance or latency acceptance criteria for the governance gate evaluation (e.g., gate evaluation must not add more than N ms to turn latency) | Conclusive performance appraisal requires measurable performance criteria; no requirement or verification criterion addresses gate evaluation performance impact on turn execution | Specification.md | Specification.md#Verification (entire section scanned) | | | TBD |

---

## Matrix X — Verification (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| X:guiding:necessity | guiding | necessity | Foundational Governance Imperative | 0 | NO_ITEMS | Governance imperative well-founded |
| X:guiding:sufficiency | guiding | sufficiency | Justified Directional Adequacy | 0 | NO_ITEMS | Direction adequate |
| X:guiding:completeness | guiding | completeness | Exhaustive Directional Scope | 0 | NO_ITEMS | Directional scope exhaustive |
| X:guiding:consistency | guiding | consistency | Unified Directional Coherence | 0 | NO_ITEMS | Direction coherent |
| X:applying:necessity | applying | necessity | Validated Practice Imperative | 1 | HAS_ITEMS | Validation of gate ordering not covered |
| X:applying:sufficiency | applying | sufficiency | Proven Practice Sufficiency | 0 | NO_ITEMS | Practice sufficient |
| X:applying:completeness | applying | completeness | Comprehensive Practice Coverage | 1 | HAS_ITEMS | Edge case for empty subagents array |
| X:applying:consistency | applying | consistency | Reliable Practice Discipline | 0 | NO_ITEMS | Practice discipline reliable |
| X:judging:necessity | judging | necessity | Decisive Judgment Threshold | 0 | NO_ITEMS | Judgment thresholds clear |
| X:judging:sufficiency | judging | sufficiency | Substantiated Judgment Adequacy | 0 | NO_ITEMS | Judgment adequate |
| X:judging:completeness | judging | completeness | Exhaustive Adjudication Scope | 0 | NO_ITEMS | Adjudication scope exhaustive |
| X:judging:consistency | judging | consistency | Principled Adjudicative Consistency | 0 | NO_ITEMS | Adjudication consistent |
| X:reviewing:necessity | reviewing | necessity | Essential Verification Basis | 0 | NO_ITEMS | Verification basis established |
| X:reviewing:sufficiency | reviewing | sufficiency | Substantiated Review Adequacy | 1 | HAS_ITEMS | Review adequacy gap for negative-path coverage |
| X:reviewing:completeness | reviewing | completeness | Exhaustive Review Coverage | 0 | NO_ITEMS | Review coverage exhaustive |
| X:reviewing:consistency | reviewing | consistency | Dependable Review Integrity | 0 | NO_ITEMS | Review integrity dependable |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| X-001 | X:applying:necessity | WeakStatement | Procedure | Procedure | Clarify in Procedure Step 3.2 what "instruction body header" means concretely: is it the YAML frontmatter, a markdown heading, or a specific line pattern? The term is used in Datasheet and Specification but never precisely defined | Validated practice imperative requires unambiguous instruction for the implementer; "body header" is used across documents but its parsing rules are not specified, which could lead to implementation variance | Procedure.md, Datasheet.md, Specification.md | Procedure.md#Step 3, Datasheet.md#Attributes, Specification.md#REQ-07 | | TYPES.md Section 4 | TBD |
| X-002 | X:applying:completeness | VerificationGap | Specification | Specification | Add a test case for the boundary condition where persona declares `subagents: []` (empty array); Procedure unit test table includes this but Specification Verification table for REQ-02 does not enumerate it | Comprehensive practice coverage requires this edge case to be in the normative verification criteria, not just procedural test suggestions | Specification.md, Procedure.md | Specification.md#Verification (REQ-02 row), Procedure.md#Step 5 | | | TBD |
| X-003 | X:reviewing:sufficiency | RationaleGap | Guidance | Guidance | Add rationale for why the integration test for denial-continuation (Procedure Step 6.2) checks for "200 response, streamed events" specifically; explain the expected response format for denied turns | Substantiated review adequacy requires understanding why specific response characteristics are the success signal; Guidance does not explain the expected HTTP/streaming behavior of denied turns | Guidance.md, Procedure.md | Guidance.md#Graceful Degradation, Procedure.md#Step 6 | | | TBD |

---

## Matrix E — Evaluation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| E:normative:necessity | normative | necessity | Binding Governance Foundation | 0 | NO_ITEMS | Governance foundation binding |
| E:normative:sufficiency | normative | sufficiency | Proven Regulatory Sufficiency | 0 | NO_ITEMS | Regulatory sufficiency proven |
| E:normative:completeness | normative | completeness | Exhaustive Normative Authority | 1 | HAS_ITEMS | DIRECTIVE Section 2.5 referenced but not clearly mapped |
| E:normative:consistency | normative | consistency | Harmonized Normative Integrity | 0 | NO_ITEMS | Normative integrity harmonized |
| E:operative:necessity | operative | necessity | Validated Operational Foundation | 0 | NO_ITEMS | Operational foundation validated |
| E:operative:sufficiency | operative | sufficiency | Demonstrated Operational Adequacy | 0 | NO_ITEMS | Operational adequacy demonstrated |
| E:operative:completeness | operative | completeness | Exhaustive Operational Completeness | 0 | NO_ITEMS | Operational completeness exhaustive |
| E:operative:consistency | operative | consistency | Steadfast Operational Discipline | 0 | NO_ITEMS | Operational discipline steadfast |
| E:evaluative:necessity | evaluative | necessity | Verified Worth Foundation | 0 | NO_ITEMS | Worth foundation verified |
| E:evaluative:sufficiency | evaluative | sufficiency | Substantiated Worth Adequacy | 0 | NO_ITEMS | Worth adequacy substantiated |
| E:evaluative:completeness | evaluative | completeness | Comprehensive Worth Evaluation | 1 | HAS_ITEMS | No explicit security threat model |
| E:evaluative:consistency | evaluative | consistency | Principled Worth Constancy | 0 | NO_ITEMS | Worth constancy principled |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| E-001 | E:normative:completeness | Normalization | Specification | Guidance | Clarify and consistently reference DIRECTIVE Section 2.5 across documents; Specification REQ-10 Rationale cites "DIRECTIVE Section 2.5 clarification" but Guidance and Datasheet reference only DIRECTIVE Section 2.3 | Exhaustive normative authority requires that all cited normative sections are consistently referenced; DIRECTIVE 2.5 appears only in Specification REQ-10 and its relationship to this deliverable is not explained in Guidance | Specification.md, Guidance.md, Datasheet.md | Specification.md#REQ-10, Guidance.md#Purpose, Datasheet.md#References | | DIRECTIVE.md | TBD |
| E-002 | E:evaluative:completeness | MissingSlot | Guidance | Guidance | Add a security considerations or threat model subsection addressing what attack vectors the governance gate protects against (e.g., type coercion injection, metadata spoofing, environment variable manipulation) and any known limitations | Comprehensive worth evaluation of a SECURITY_CONTROL deliverable requires explicit consideration of what threats are mitigated and what residual risks remain; Guidance addresses "why" governance exists but not the threat landscape | Guidance.md | Guidance.md#Considerations (entire section scanned) | | | TBD |
