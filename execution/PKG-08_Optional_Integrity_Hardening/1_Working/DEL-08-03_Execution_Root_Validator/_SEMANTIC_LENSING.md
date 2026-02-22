# Semantic Lensing Register: DEL-08-03 Execution Root Folder Structure Validator

**Generated:** 2026-02-21
**Deliverable Folder:** /Users/ryan/ai-env/projects/chirality-app-dev1/execution/PKG-08_Optional_Integrity_Hardening/1_Working/DEL-08-03_Execution_Root_Validator/
**Warnings:** None

**Inputs Read:**
- _CONTEXT.md — `execution/PKG-08_Optional_Integrity_Hardening/1_Working/DEL-08-03_Execution_Root_Validator/_CONTEXT.md`
- _STATUS.md — `execution/PKG-08_Optional_Integrity_Hardening/1_Working/DEL-08-03_Execution_Root_Validator/_STATUS.md` (Current State: SEMANTIC_READY)
- _SEMANTIC.md — `execution/PKG-08_Optional_Integrity_Hardening/1_Working/DEL-08-03_Execution_Root_Validator/_SEMANTIC.md`
- Datasheet.md — `execution/PKG-08_Optional_Integrity_Hardening/1_Working/DEL-08-03_Execution_Root_Validator/Datasheet.md`
- Specification.md — `execution/PKG-08_Optional_Integrity_Hardening/1_Working/DEL-08-03_Execution_Root_Validator/Specification.md`
- Guidance.md — `execution/PKG-08_Optional_Integrity_Hardening/1_Working/DEL-08-03_Execution_Root_Validator/Guidance.md`
- Procedure.md — `execution/PKG-08_Optional_Integrity_Hardening/1_Working/DEL-08-03_Execution_Root_Validator/Procedure.md`
- _REFERENCES.md — `execution/PKG-08_Optional_Integrity_Hardening/1_Working/DEL-08-03_Execution_Root_Validator/_REFERENCES.md`

**Purpose:** Apply CHIRALITY_FRAMEWORK matrix cells as lenses over the production documents, capturing warranted enrichment inputs for a later enrichment pass.

## Summary

- Total warranted items: 22
- By document:
  - Datasheet: 4
  - Specification: 10
  - Guidance: 4
  - Procedure: 4
- By matrix:
  - A: 5  B: 3  C: 2  F: 3  D: 2  X: 5  E: 2
- By type:
  - Conflict: 1
  - VerificationGap: 5
  - MissingSlot: 5
  - WeakStatement: 4
  - RationaleGap: 2
  - Normalization: 2
  - TBD_Question: 3
  - MatrixError: 0
- Notable conflicts: 1
- Matrix parse errors: 0

## Matrix A -- Orientation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| A:normative:guiding | normative | guiding | prescriptive direction | 1 | HAS_ITEMS | Language/runtime TBD weakens prescriptive direction |
| A:normative:applying | normative | applying | mandatory practice | 2 | HAS_ITEMS | Dependency-tracked detection mechanism undefined; REQ-06c is assumption-only |
| A:normative:judging | normative | judging | compliance determination | 1 | HAS_ITEMS | No acceptance criteria for REQ-07c output format |
| A:normative:reviewing | normative | reviewing | regulatory audit | 0 | NO_ITEMS | Audit trail approach is covered by exit codes and report |
| A:operative:guiding | operative | guiding | procedural direction | 0 | NO_ITEMS | Procedure provides clear step-by-step direction |
| A:operative:applying | operative | applying | practical execution | 1 | HAS_ITEMS | Procedure Step A5.8 dependency-tracked detection is TBD |
| A:operative:judging | operative | judging | performance assessment | 0 | NO_ITEMS | Verification table in Procedure is clear |
| A:operative:reviewing | operative | reviewing | process audit | 0 | NO_ITEMS | Records section in Procedure is adequate |
| A:evaluative:guiding | evaluative | guiding | value orientation | 0 | NO_ITEMS | Guidance Purpose section establishes clear value orientation |
| A:evaluative:applying | evaluative | applying | merit application | 0 | NO_ITEMS | Trade-offs table in Guidance covers merit application |
| A:evaluative:judging | evaluative | judging | worth determination | 0 | NO_ITEMS | Verification approaches in Specification are adequate |
| A:evaluative:reviewing | evaluative | reviewing | quality appraisal | 0 | NO_ITEMS | Quality criteria implicit in severity model |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A-001 | A:normative:guiding | TBD_Question | Datasheet | Datasheet | Record language/runtime decision (currently "TBD" in Datasheet Attributes "Language / runtime" row) once human decides | The prescriptive direction for this deliverable cannot be fully established until the implementation language is decided; this is a blocking TBD that affects all downstream implementation steps | Datasheet.md | Attributes table, "Language / runtime" row | | Human decision required | TBD |
| A-002 | A:normative:applying | WeakStatement | Specification | Specification | Clarify the mechanism for determining whether a deliverable is "dependency-tracked" (REQ-05 precondition); current text says "TBD" in Procedure A5.8 and Specification REQ-05 Note | Mandatory practice cannot be applied if the triggering condition for REQ-05 checks is undefined; an implementer would not know when to execute these checks | Specification.md; Procedure.md | REQ-05 Note; Step A5.8 | | Specification.md should define the detection rule | TBD |
| A-003 | A:normative:applying | WeakStatement | Specification | Specification | Clarify whether REQ-06c (deliverable ID prefix matches parent package ID) is a confirmed requirement or should be removed; currently marked as ASSUMPTION | REQ-06c is listed as a requirement but flagged as assumption with no SPEC source; an implementer cannot determine if it is mandatory | Specification.md | REQ-06, REQ-06c row | | Human must confirm or remove | TBD |
| A-004 | A:normative:judging | VerificationGap | Specification | Specification | Add acceptance criteria for REQ-07c (report format); currently "TBD (human-readable text, JSON, or both)" with no way to verify compliance | Compliance determination for the report output format is impossible when the format itself is undefined | Specification.md | REQ-07, REQ-07c row | | Human must decide format | TBD |
| A-005 | A:operative:applying | WeakStatement | Procedure | Procedure | Resolve TBD in Procedure Step A5.8: define or reference the mechanism for determining "dependency-tracked" status before implementation proceeds | Practical execution of Step A5.8 is blocked by the undefined detection mechanism for dependency-tracked deliverables | Procedure.md | Step A5, item 8 | | Specification.md should define; Procedure should reference | TBD |

## Matrix B -- Conceptualization (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| B:data:necessity | data | necessity | essential fact | 1 | HAS_ITEMS | Output format is an essential fact that is TBD |
| B:data:sufficiency | data | sufficiency | adequate evidence | 0 | NO_ITEMS | Datasheet references are well-sourced |
| B:data:completeness | data | completeness | comprehensive record | 1 | HAS_ITEMS | Responsible party is TBD |
| B:data:consistency | data | consistency | reliable measurement | 0 | NO_ITEMS | Severity levels consistently use ERROR/WARNING |
| B:information:necessity | information | necessity | essential signal | 0 | NO_ITEMS | Core signals (exit codes, severity) are defined |
| B:information:sufficiency | information | sufficiency | adequate context | 0 | NO_ITEMS | Sources are cited throughout |
| B:information:completeness | information | completeness | comprehensive account | 0 | NO_ITEMS | Requirements cover all SPEC Section 12 items |
| B:information:consistency | information | consistency | coherent message | 1 | HAS_ITEMS | Inconsistent terminology for lifecycle state ordering |
| B:knowledge:necessity | knowledge | necessity | fundamental understanding | 0 | NO_ITEMS | Core domain concepts are well-explained in Guidance |
| B:knowledge:sufficiency | knowledge | sufficiency | competent expertise | 0 | NO_ITEMS | Trade-offs and considerations provide adequate expertise context |
| B:knowledge:completeness | knowledge | completeness | thorough mastery | 0 | NO_ITEMS | Document set covers validation domain thoroughly |
| B:knowledge:consistency | knowledge | consistency | coherent understanding | 0 | NO_ITEMS | Cross-document understanding is coherent |
| B:wisdom:necessity | wisdom | necessity | essential discernment | 0 | NO_ITEMS | Guidance principles provide discernment framework |
| B:wisdom:sufficiency | wisdom | sufficiency | adequate judgment | 0 | NO_ITEMS | Trade-offs table enables judgment |
| B:wisdom:completeness | wisdom | completeness | holistic insight | 0 | NO_ITEMS | Considerations cover relationships to adjacent deliverables |
| B:wisdom:consistency | wisdom | consistency | principled reasoning | 0 | NO_ITEMS | Principles are consistently applied |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| B-001 | B:data:necessity | TBD_Question | Specification | Specification | Resolve REQ-07c: decide output format (human-readable, JSON, or both) and record the decision | Output format is an essential fact for implementation; currently TBD with no resolution path specified | Specification.md | REQ-07, REQ-07c | | Human decision required | TBD |
| B-002 | B:data:completeness | MissingSlot | Datasheet | Datasheet | Add responsible party for this deliverable (currently "TBD" in Identification table) | Comprehensive record requires identifying who is accountable for delivery | Datasheet.md | Identification table, "Responsible Party" row | | Human assignment required | TBD |
| B-003 | B:information:consistency | Normalization | Specification | Specification | Standardize the terminology for lifecycle state ordering: Specification REQ-03c lists states in lifecycle order but REQ-04 uses ">= INITIALIZED" phrasing without defining the ordering relation; Guidance C4 says "shallow content check" while Specification says "valid lifecycle state" | The concept of state ordering (which states are "above" INITIALIZED) is used in REQ-04 but the ordering is not formally defined in this deliverable's documents; it relies on implicit knowledge of SPEC.md Section 3.2 ordering | Specification.md; Guidance.md | REQ-03c; REQ-04 header; C4 | | Specification.md should define the ordering or explicitly reference SPEC.md 3.2 for ordering semantics | TBD |

## Matrix C -- Formulation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| C:normative:necessity | normative | necessity | Binding Compliance Imperative | 0 | NO_ITEMS | Mandatory checks are clearly bound to SPEC sources |
| C:normative:sufficiency | normative | sufficiency | Mandated Due Diligence | 1 | HAS_ITEMS | Dependencies.csv validation boundary needs tightening |
| C:normative:completeness | normative | completeness | Total Compliance Coverage | 1 | HAS_ITEMS | Tool root validation explicitly excluded but rationale could be stronger |
| C:normative:consistency | normative | consistency | Uniform Regulatory Coherence | 0 | NO_ITEMS | MUST/SHOULD mapping is consistently applied |
| C:operative:necessity | operative | necessity | Critical Process Prerequisite | 0 | NO_ITEMS | Prerequisites are listed in Procedure |
| C:operative:sufficiency | operative | sufficiency | Demonstrated Operational Readiness | 0 | NO_ITEMS | Readiness conditions are addressed |
| C:operative:completeness | operative | completeness | End-to-End Process Coverage | 0 | NO_ITEMS | Procedure covers produce, test, document cycle |
| C:operative:consistency | operative | consistency | Disciplined Execution Standard | 0 | NO_ITEMS | Steps follow a consistent pattern |
| C:evaluative:necessity | evaluative | necessity | Intrinsic Value Foundation | 0 | NO_ITEMS | Value proposition is clear in Guidance Purpose |
| C:evaluative:sufficiency | evaluative | sufficiency | Competent Value Judgment | 0 | NO_ITEMS | Trade-offs table provides judgment framework |
| C:evaluative:completeness | evaluative | completeness | Exhaustive Quality Assessment | 0 | NO_ITEMS | Verification approaches cover all requirements |
| C:evaluative:consistency | evaluative | consistency | Consistent Quality Standard | 0 | NO_ITEMS | Quality standards are consistent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| C-001 | C:normative:sufficiency | VerificationGap | Specification | Specification | Add explicit acceptance criterion for what constitutes "valid v3.1 schema headers" in REQ-05b: is it the presence of the RegisterSchemaVersion column only, or a defined set of column headers? The Specification Note and Guidance C2 both say "minimal header check" but REQ-05b says "valid v3.1 schema headers" which is broader | The due diligence threshold for Dependencies.csv header validation is ambiguous; the requirement text (REQ-05b) is stricter than the stated assumption (minimal check), creating an implementation ambiguity | Specification.md; Guidance.md | REQ-05b; REQ-05 Note; C2 | Specification.md#REQ-05b ("valid v3.1 schema headers"); Specification.md#REQ-05-Note ("minimal header check") | Specification.md should tighten the wording to match the intended scope | TBD |
| C-002 | C:normative:completeness | RationaleGap | Guidance | Guidance | Strengthen rationale for excluding tool root validation (C5): currently says "not in the initial scope" and suggests proposing a SPEC update; add rationale for why SPEC Section 12 omits tool roots despite Section 1.2 listing them | Total compliance coverage is intentionally bounded, but the reason SPEC Section 12 does not include tool root checks is not explained; a reader may wonder if this is an oversight | Guidance.md | C5 (Tool Root Validation) | | Guidance.md is the appropriate place for this rationale | TBD |

## Matrix F -- Requirements (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| F:normative:necessity | normative | necessity | Mandated Conformance Threshold | 0 | NO_ITEMS | Conformance thresholds are clear (ERROR = non-conformant) |
| F:normative:sufficiency | normative | sufficiency | Sufficient Conformance Assurance | 1 | HAS_ITEMS | No defined pass/fail summary in report requirements |
| F:normative:completeness | normative | completeness | Comprehensive Obligation Record | 0 | NO_ITEMS | All SPEC 12 obligations are mapped to REQs |
| F:normative:consistency | normative | consistency | Principled Conformance Unity | 0 | NO_ITEMS | Severity model is consistently principled |
| F:operative:necessity | operative | necessity | Essential Workflow Readiness | 1 | HAS_ITEMS | No explicit error handling requirements |
| F:operative:sufficiency | operative | sufficiency | Verified Process Preparation | 0 | NO_ITEMS | Prerequisites cover preparation |
| F:operative:completeness | operative | completeness | Total Operational Inventory | 0 | NO_ITEMS | Operational steps are comprehensive |
| F:operative:consistency | operative | consistency | Uniform Operational Discipline | 0 | NO_ITEMS | Steps follow uniform discipline |
| F:evaluative:necessity | evaluative | necessity | Fundamental Quality Criterion | 1 | HAS_ITEMS | No performance or scalability criteria defined |
| F:evaluative:sufficiency | evaluative | sufficiency | Justified Quality Threshold | 0 | NO_ITEMS | Quality thresholds are justified by SPEC mapping |
| F:evaluative:completeness | evaluative | completeness | Thorough Evaluation Inventory | 0 | NO_ITEMS | Verification table is thorough |
| F:evaluative:consistency | evaluative | consistency | Coherent Quality Ethic | 0 | NO_ITEMS | Quality approach is coherent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| F-001 | F:normative:sufficiency | MissingSlot | Specification | Specification | Add a requirement for the validator to produce a summary line (e.g., "N errors, M warnings") to provide a conformance assurance signal at a glance | The report requirements (REQ-07) specify ERROR/WARNING distinction and exit codes but do not require a summary count, which is the most direct conformance assurance signal for operators and CI consumers | Specification.md | REQ-07 | | Specification.md | TBD |
| F-002 | F:operative:necessity | MissingSlot | Specification | Specification | Add a requirement or note addressing validator behavior when the input path does not exist or is not a directory (error handling for invalid input) | Essential workflow readiness requires handling the most basic failure mode: the user provides a non-existent or non-directory path; no REQ addresses this | Specification.md | REQ-08 (CLI interface section) | | Specification.md | TBD |
| F-003 | F:evaluative:necessity | MissingSlot | Specification | Guidance | Consider documenting whether there are performance expectations for large execution roots (e.g., roots with many packages/deliverables); if none, state that explicitly | No quality criterion for performance or scalability is stated; for a validator that walks filesystems, this is a reasonable consideration even if the answer is "no constraint" | Specification.md; Guidance.md | entire document scanned | | Guidance.md is appropriate for a rationale note; Specification.md if a constraint is needed | TBD |

## Matrix D -- Objectives (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| D:normative:guiding | normative | guiding | Authoritative Compliance Directive | 0 | NO_ITEMS | Guidance P1 establishes clear authoritative directive |
| D:normative:applying | normative | applying | Enforced Adequacy Standard | 0 | NO_ITEMS | Requirements enforce adequate standards |
| D:normative:judging | normative | judging | Definitive Conformance Ruling | 1 | HAS_ITEMS | Verification approach for some REQs is vague |
| D:normative:reviewing | normative | reviewing | Systematic Compliance Verification | 0 | NO_ITEMS | Verification table provides systematic coverage |
| D:operative:guiding | operative | guiding | Established Workflow Guidance | 0 | NO_ITEMS | Procedure establishes clear workflow |
| D:operative:applying | operative | applying | Confirmed Operational Execution | 0 | NO_ITEMS | Steps are actionable |
| D:operative:judging | operative | judging | Resolved Performance Accounting | 0 | NO_ITEMS | Verification section in Procedure accounts for performance |
| D:operative:reviewing | operative | reviewing | Confirmed Workflow Rigor | 0 | NO_ITEMS | Procedure verification is adequately rigorous |
| D:evaluative:guiding | evaluative | guiding | Established Quality Direction | 0 | NO_ITEMS | Guidance principles establish quality direction |
| D:evaluative:applying | evaluative | applying | Committed Merit Standard | 1 | HAS_ITEMS | No explicit acceptance test for the "validate own execution root" scenario |
| D:evaluative:judging | evaluative | judging | Definitive Quality Verdict | 0 | NO_ITEMS | Verification approaches support definitive verdicts |
| D:evaluative:reviewing | evaluative | reviewing | Principled Quality Review | 0 | NO_ITEMS | Quality review approach is principled |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| D-001 | D:normative:judging | VerificationGap | Specification | Specification | Add concrete pass/fail criteria for REQ-08c ("SHOULD support a machine-readable output mode"): what constitutes a valid machine-readable mode? If JSON, specify minimal schema or at least required fields | Definitive conformance ruling for REQ-08c is impossible without specifying what "machine-readable" means; the verification approach says "verify machine-readable output mode if implemented" which defers the definition | Specification.md | REQ-08c; Verification table row for REQ-08 | | Specification.md | TBD |
| D-002 | D:evaluative:applying | VerificationGap | Procedure | Specification | Add an explicit acceptance test: "run validator against the project's own execution root and verify zero false positives"; Procedure Verification "Overall" row mentions this but it is not a formal REQ in Specification | The Procedure's Overall verification row references validating the project's own execution root but this is not captured as a formal requirement or acceptance criterion in Specification; it exists only as an informal check | Procedure.md; Specification.md | Procedure Verification table "Overall" row; Specification Verification table (no corresponding entry) | | Specification.md should formalize as acceptance criterion | TBD |

## Matrix X -- Verification (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| X:guiding:necessity | guiding | necessity | Foundational Directive Mandate | 0 | NO_ITEMS | Foundational directives are established |
| X:guiding:sufficiency | guiding | sufficiency | Adequate Directional Assurance | 0 | NO_ITEMS | Direction is adequate |
| X:guiding:completeness | guiding | completeness | Complete Guidance Saturation | 1 | HAS_ITEMS | Guidance does not address error message design principles |
| X:guiding:consistency | guiding | consistency | Unified Directional Discipline | 0 | NO_ITEMS | Directional discipline is unified |
| X:applying:necessity | applying | necessity | Essential Practice Baseline | 1 | HAS_ITEMS | No requirement for label sanitization validation |
| X:applying:sufficiency | applying | sufficiency | Verified Implementation Capacity | 0 | NO_ITEMS | Implementation capacity is addressed |
| X:applying:completeness | applying | completeness | Fully Implemented Coverage | 1 | HAS_ITEMS | SPEC Section 10 label sanitization not covered |
| X:applying:consistency | applying | consistency | Stable Practice Enforcement | 0 | NO_ITEMS | Practice enforcement is stable |
| X:judging:necessity | judging | necessity | Binding Determination Threshold | 0 | NO_ITEMS | Determination thresholds are bound to severity model |
| X:judging:sufficiency | judging | sufficiency | Adequate Capability Finding | 0 | NO_ITEMS | Capability findings are adequate |
| X:judging:completeness | judging | completeness | Comprehensive Assessment Ruling | 0 | NO_ITEMS | Assessment is comprehensive for in-scope rules |
| X:judging:consistency | judging | consistency | Unified Assessment Consistency | 0 | NO_ITEMS | Assessment consistency is unified |
| X:reviewing:necessity | reviewing | necessity | Mandatory Verification Scrutiny | 1 | HAS_ITEMS | No negative-test verification for false positives |
| X:reviewing:sufficiency | reviewing | sufficiency | Sufficient Rigor Confirmation | 0 | NO_ITEMS | Rigor is sufficient |
| X:reviewing:completeness | reviewing | completeness | Exhaustive Audit Coverage | 1 | HAS_ITEMS | Verification table does not cover edge cases explicitly |
| X:reviewing:consistency | reviewing | consistency | Consistent Inspection Discipline | 0 | NO_ITEMS | Inspection discipline is consistent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| X-001 | X:guiding:completeness | RationaleGap | Guidance | Guidance | Add a consideration or principle about error message quality: validator messages should be actionable (identifying which rule failed, which path is affected, and what was expected) to support human debugging | Guidance provides principles on rule fidelity (P1), severity (P2), read-only (P3), and fail-fast (P4), but does not guide the design of error messages themselves; this is a gap in guidance saturation for a validation tool | Guidance.md | Principles section | | Guidance.md | TBD |
| X-002 | X:applying:necessity | MissingSlot | Specification | Specification | Consider adding a requirement to validate that folder labels conform to SPEC.md Section 10 filesystem-safe sanitization rules (referenced in Datasheet References row 4 but not covered by any REQ) | Datasheet References row 4 lists SPEC.md Section 10 (label sanitization) as relevant, but no requirement in Specification validates label format beyond the ID prefix; this is an essential practice baseline gap if label conformance matters | Datasheet.md; Specification.md | Datasheet References table row 4; Specification Requirements (entire section scanned) | | Human should decide if label sanitization validation is in scope | TBD |
| X-003 | X:applying:completeness | Conflict | Datasheet | Specification | Resolve: Datasheet References row 4 lists SPEC.md Section 10 (label sanitization rules) as relevant to this deliverable, but Specification Requirements contain no check for label sanitization; either add a requirement or remove the reference as not applicable | The Datasheet signals that label sanitization is within this deliverable's concern, but the Specification does not implement any check for it; this is a cross-document inconsistency about scope | Datasheet.md; Specification.md | Datasheet References table row 4; Specification Requirements section | Datasheet.md#References-row-4 ("defines filesystem-safe label sanitization rules"); Specification.md#Requirements (no label sanitization REQ) | Human must decide if label sanitization is in scope | TBD |
| X-004 | X:reviewing:necessity | VerificationGap | Specification | Specification | Add explicit verification approach for false-positive testing: run validator against a fully valid execution root and confirm zero findings | Mandatory verification scrutiny requires confirming the validator does not produce false positives; the Verification table tests for detection of violations but does not explicitly test that a clean root produces zero findings (though the Guidance example implies it) | Specification.md; Guidance.md | Specification Verification table; Guidance Examples "Valid Execution Root" | | Specification.md Verification table | TBD |
| X-005 | X:reviewing:completeness | Normalization | Specification | Specification | Standardize how edge cases are described in the Verification table: some rows list specific fixture scenarios (e.g., "empty directory, directory missing _Decomposition/") while others are generic (e.g., "verify exit codes"); consider adding edge cases for all REQ groups consistently | The Verification table has uneven granularity: REQ-01 and REQ-02 list specific test scenarios while REQ-07 and REQ-08 are generic; exhaustive audit coverage benefits from consistent specificity | Specification.md | Verification table | | Specification.md | TBD |

## Matrix E -- Evaluation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| E:normative:necessity | normative | necessity | Binding Compliance Gate | 0 | NO_ITEMS | Exit code requirement serves as compliance gate |
| E:normative:sufficiency | normative | sufficiency | Verified Regulatory Sufficiency | 0 | NO_ITEMS | Regulatory sufficiency is verified through SPEC mapping |
| E:normative:completeness | normative | completeness | Total Compliance Adjudication | 0 | NO_ITEMS | All SPEC 12 rules are adjudicated |
| E:normative:consistency | normative | consistency | Uniform Compliance Discipline | 0 | NO_ITEMS | Compliance discipline is uniform |
| E:operative:necessity | operative | necessity | Critical Operational Baseline | 1 | HAS_ITEMS | Scope gating prerequisite could be stronger |
| E:operative:sufficiency | operative | sufficiency | Verified Execution Competence | 0 | NO_ITEMS | Execution competence is addressed |
| E:operative:completeness | operative | completeness | Thorough Operational Verification | 0 | NO_ITEMS | Operational verification is thorough |
| E:operative:consistency | operative | consistency | Dependable Operational Alignment | 0 | NO_ITEMS | Operational alignment is dependable |
| E:evaluative:necessity | evaluative | necessity | Core Quality Imperative | 1 | HAS_ITEMS | No explicit quality gate for the deliverable itself |
| E:evaluative:sufficiency | evaluative | sufficiency | Confirmed Value Sufficiency | 0 | NO_ITEMS | Value is confirmed through purpose statement |
| E:evaluative:completeness | evaluative | completeness | Exhaustive Worth Adjudication | 0 | NO_ITEMS | Worth is adequately adjudicated |
| E:evaluative:consistency | evaluative | consistency | Systematic Quality Integrity | 0 | NO_ITEMS | Quality integrity is systematic |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| E-001 | E:operative:necessity | WeakStatement | Procedure | Procedure | Strengthen Procedure Step A1: currently says "Verify that SOW-034 has been flipped to IN (or that the human has authorized work to proceed while TBD)"; the parenthetical escape clause weakens the prerequisite; consider separating the two conditions into distinct decision paths | The critical operational baseline includes scope confirmation; the parenthetical allows bypassing the prerequisite without a clear decision record, which could lead to work on a deliverable that is later retired | Procedure.md | Step A1, item 1 | | Procedure.md | TBD |
| E-002 | E:evaluative:necessity | TBD_Question | Datasheet | Guidance | Define what "done" looks like for this deliverable: is it (a) script passes all tests, (b) script validates the project's own execution root without false positives, (c) CI integration demonstrated, or (d) all of the above? Currently spread across Specification Documentation table and Procedure Verification but not consolidated | The core quality imperative requires a clear definition of done; acceptance criteria are distributed across documents but not unified into a single authoritative checklist | Datasheet.md; Specification.md; Procedure.md | Datasheet (no "Definition of Done" section); Specification Documentation table; Procedure Verification table | | Guidance.md or Specification.md should consolidate acceptance criteria | TBD |
