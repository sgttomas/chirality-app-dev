# Semantic Lensing Register: DEL-07-01 Harness Validation Suite (local + CI-ready posture)

**Generated:** 2026-02-21
**Deliverable Folder:** /Users/ryan/ai-env/projects/chirality-app-dev/execution/PKG-07_Validation_Example_Assets/1_Working/DEL-07-01_Harness_Validation_Suite/
**Warnings:** None

**Inputs Read:**
- _CONTEXT.md — `execution/PKG-07_Validation_Example_Assets/1_Working/DEL-07-01_Harness_Validation_Suite/_CONTEXT.md`
- _STATUS.md — `execution/PKG-07_Validation_Example_Assets/1_Working/DEL-07-01_Harness_Validation_Suite/_STATUS.md`
- _SEMANTIC.md — `execution/PKG-07_Validation_Example_Assets/1_Working/DEL-07-01_Harness_Validation_Suite/_SEMANTIC.md`
- Datasheet.md — `execution/PKG-07_Validation_Example_Assets/1_Working/DEL-07-01_Harness_Validation_Suite/Datasheet.md`
- Specification.md — `execution/PKG-07_Validation_Example_Assets/1_Working/DEL-07-01_Harness_Validation_Suite/Specification.md`
- Guidance.md — `execution/PKG-07_Validation_Example_Assets/1_Working/DEL-07-01_Harness_Validation_Suite/Guidance.md`
- Procedure.md — `execution/PKG-07_Validation_Example_Assets/1_Working/DEL-07-01_Harness_Validation_Suite/Procedure.md`
- _REFERENCES.md — `execution/PKG-07_Validation_Example_Assets/1_Working/DEL-07-01_Harness_Validation_Suite/_REFERENCES.md`

**Purpose:** Apply CHIRALITY_FRAMEWORK matrix cells as lenses over the production documents, capturing warranted enrichment inputs for a later enrichment pass.

---

## Summary

- Total warranted items: 24
- By document (AppliesToDoc):
  - Datasheet: 3 (A-002, B-001, F-003)
  - Specification: 12 (A-001, A-003, A-005, B-002, B-003, D-001, D-003, E-001, F-001, X-002, X-003, X-004)
  - Guidance: 4 (C-001, C-002, X-001, E-003)
  - Procedure: 5 (A-004, D-002, E-002, F-002, X-005)
- By matrix:
  - A: 5  B: 3  C: 2  F: 3  D: 3  X: 5  E: 3
- By type:
  - Conflict: 0
  - VerificationGap: 6 (A-003, D-003, F-001, F-002, X-003, X-004)
  - MissingSlot: 8 (A-002, A-004, A-005, B-002, E-002, E-003, X-001, X-002)
  - WeakStatement: 4 (A-001, D-001, D-002, E-001)
  - RationaleGap: 3 (C-001, C-002, X-005)
  - Normalization: 2 (B-003, F-003)
  - TBD_Question: 1 (B-001)
  - MatrixError: 0
- Notable conflicts: 0
- Matrix parse errors: 0

---

## Matrix A -- Orientation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| A:normative:guiding | normative | guiding | prescriptive direction | 1 | HAS_ITEMS | REQ structure present but missing acceptance criteria thresholds |
| A:normative:applying | normative | applying | mandatory practice | 1 | HAS_ITEMS | Mandatory practices identified but output format underspecified |
| A:normative:judging | normative | judging | compliance determination | 1 | HAS_ITEMS | Verification table present but approaches lack measurable criteria |
| A:normative:reviewing | normative | reviewing | regulatory audit | 0 | NO_ITEMS | Procedure Phase 5 covers review and handoff adequately |
| A:operative:guiding | operative | guiding | procedural direction | 1 | HAS_ITEMS | Missing explicit error-handling/rollback guidance in Procedure |
| A:operative:applying | operative | applying | practical execution | 0 | NO_ITEMS | Procedure steps are actionable and sequenced |
| A:operative:judging | operative | judging | performance assessment | 0 | NO_ITEMS | Verification checks in Procedure are present |
| A:operative:reviewing | operative | reviewing | process audit | 0 | NO_ITEMS | Phase 5 review steps cover this |
| A:evaluative:guiding | evaluative | guiding | value orientation | 0 | NO_ITEMS | Guidance P5 addresses evidence-over-coverage |
| A:evaluative:applying | evaluative | applying | merit application | 0 | NO_ITEMS | Test approach targets contract boundaries |
| A:evaluative:judging | evaluative | judging | worth determination | 1 | HAS_ITEMS | No quality gate or acceptance threshold for suite itself |
| A:evaluative:reviewing | evaluative | reviewing | quality appraisal | 0 | NO_ITEMS | Procedure Phase 3 covers repeatability check |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A-001 | A:normative:guiding | WeakStatement | Specification | Specification | Clarify what "processes it end-to-end" means in REQ-05 (define observable completion signal or response structure) | REQ-05 uses vague language ("produces a response") without specifying what constitutes a valid response for test assertion purposes | Specification.md | REQ-05: Turn Execution Validation | -- | Specification.md (normative) | TBD |
| A-002 | A:normative:applying | MissingSlot | Datasheet | Datasheet | Add attribute for expected test output format (JSON, TAP, plain text, exit codes) so downstream CI consumers know what to parse | Datasheet Construction table says "Output format: TBD" -- this TBD blocks CI integration | Datasheet.md | Construction table, "Output format" row | -- | Datasheet.md (descriptive) | TBD |
| A-003 | A:normative:judging | VerificationGap | Specification | Specification | Add measurable pass/fail criteria to verification approaches (e.g., "all N tests pass" vs. "tests pass") for REQ-01 through REQ-12 | Verification table uses generic "verify pass/fail results" without quantitative thresholds or specific observable criteria | Specification.md | Verification table | -- | Specification.md (normative) | TBD |
| A-004 | A:operative:guiding | MissingSlot | Procedure | Procedure | Add error-handling/rollback guidance: what to do when test fixtures fail to generate, harness fails to start, or individual phases fail | Procedure steps lack contingency actions; only success paths are documented | Procedure.md | Steps (all phases) | -- | Procedure.md (operational) | TBD |
| A-005 | A:evaluative:judging | MissingSlot | Specification | Specification | Add acceptance criteria for the validation suite itself: minimum number of tests per behavioral area, required documentation sections, or definition of "done" for the deliverable | No threshold exists for judging whether the suite is complete enough to accept | Specification.md | Requirements (general) | -- | Specification.md (normative) | TBD |

---

## Matrix B -- Conceptualization (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| B:data:necessity | data | necessity | essential fact | 1 | HAS_ITEMS | Node.js version not specified |
| B:data:sufficiency | data | sufficiency | adequate evidence | 0 | NO_ITEMS | Source references present throughout |
| B:data:completeness | data | completeness | comprehensive record | 1 | HAS_ITEMS | Missing enumeration of specific K- invariants to test |
| B:data:consistency | data | consistency | reliable measurement | 0 | NO_ITEMS | Size limits and thresholds are consistent across docs |
| B:information:necessity | information | necessity | essential signal | 0 | NO_ITEMS | Key signals (SOW, OBJ, REQ) are present |
| B:information:sufficiency | information | sufficiency | adequate context | 0 | NO_ITEMS | Context is adequate for each requirement |
| B:information:completeness | information | completeness | comprehensive account | 0 | NO_ITEMS | Behavioral areas fully enumerated |
| B:information:consistency | information | consistency | coherent message | 0 | NO_ITEMS | Consistent messaging across documents |
| B:knowledge:necessity | knowledge | necessity | fundamental understanding | 0 | NO_ITEMS | Harness contract surface understanding present |
| B:knowledge:sufficiency | knowledge | sufficiency | competent expertise | 0 | NO_ITEMS | Guidance provides sufficient domain expertise |
| B:knowledge:completeness | knowledge | completeness | thorough mastery | 0 | NO_ITEMS | Coverage of harness behaviors is thorough |
| B:knowledge:consistency | knowledge | consistency | coherent understanding | 1 | HAS_ITEMS | Terminology inconsistency in attachment size references |
| B:wisdom:necessity | wisdom | necessity | essential discernment | 0 | NO_ITEMS | Trade-off awareness present in Guidance |
| B:wisdom:sufficiency | wisdom | sufficiency | adequate judgment | 0 | NO_ITEMS | Guidance trade-off analysis is adequate |
| B:wisdom:completeness | wisdom | completeness | holistic insight | 0 | NO_ITEMS | System-level implications addressed |
| B:wisdom:consistency | wisdom | consistency | principled reasoning | 0 | NO_ITEMS | Reasoning is principled throughout |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| B-001 | B:data:necessity | TBD_Question | Datasheet | Datasheet | Add required Node.js version (or version range) to Attributes or Conditions; currently marked as ASSUMPTION with no version constraint | Node.js version is a prerequisite (PR-02 in Procedure) but no version is specified anywhere; tests may fail silently on incompatible versions | Datasheet.md; Procedure.md | Datasheet: Conditions table "Node.js environment"; Procedure: PR-02 | -- | Human decision needed (depends on Electron/Next.js version) | TBD |
| B-002 | B:data:completeness | MissingSlot | Specification | Specification | Enumerate which CONTRACT.md K- invariants (K-SEAL-1, K-GHOST-1, K-INVENT-1, K-CONFLICT-1) the test suite should validate and map them to specific REQs | Datasheet References R2 lists CONTRACT.md K- invariants as relevant, but Specification requirements do not reference specific invariants to test | Datasheet.md; Specification.md | Datasheet: References R2; Specification: Requirements section | -- | Specification.md (normative) | TBD |
| B-003 | B:knowledge:consistency | Normalization | Specification | Guidance | Normalize size limit notation: use consistent units (bytes vs. MB) and specify whether "10 MB" means 10,000,000 bytes or 10,485,760 bytes (10 MiB) | Specification REQ-09 says "10 MB" and "18 MB"; Guidance example uses "10,000,001 bytes" implying decimal MB; this ambiguity could cause off-by-one test failures | Specification.md; Guidance.md | Specification: REQ-09; Guidance: Example Attachment Resolver Boundary Test | -- | Specification.md (normative definition); Guidance.md (clarification note) | TBD |

---

## Matrix C -- Formulation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| C:normative:necessity | normative | necessity | regulatory imperative | 0 | NO_ITEMS | Core mandates are established |
| C:normative:sufficiency | normative | sufficiency | compliance justification | 1 | HAS_ITEMS | Compliance path for DEC-NET-001 during testing unclear |
| C:normative:completeness | normative | completeness | exhaustive compliance scope | 0 | NO_ITEMS | All behavioral areas in scope are covered |
| C:normative:consistency | normative | consistency | uniform regulatory coherence | 0 | NO_ITEMS | Regulatory references consistent |
| C:operative:necessity | operative | necessity | operational prerequisite | 0 | NO_ITEMS | Prerequisites well-documented in Procedure |
| C:operative:sufficiency | operative | sufficiency | competent operational capacity | 0 | NO_ITEMS | Steps sufficient for execution |
| C:operative:completeness | operative | completeness | comprehensive operational coverage | 0 | NO_ITEMS | All phases covered |
| C:operative:consistency | operative | consistency | reproducible process discipline | 0 | NO_ITEMS | Procedure steps are ordered and repeatable |
| C:evaluative:necessity | evaluative | necessity | intrinsic merit recognition | 0 | NO_ITEMS | Value of suite well-articulated in Guidance Purpose |
| C:evaluative:sufficiency | evaluative | sufficiency | defensible value judgment | 1 | HAS_ITEMS | No criteria for when suite provides sufficient confidence |
| C:evaluative:completeness | evaluative | completeness | holistic value accounting | 0 | NO_ITEMS | Coverage scope aligned with SOW-028 |
| C:evaluative:consistency | evaluative | consistency | principled value coherence | 0 | NO_ITEMS | Principles coherent with stated value |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| C-001 | C:normative:sufficiency | RationaleGap | Guidance | Guidance | Add consideration for how integration tests comply with DEC-NET-001 (Anthropic-only outbound) -- does test infrastructure (e.g., fixture downloads, npm test dependencies) violate this policy? | Guidance C2 acknowledges network policy awareness but does not provide actionable direction on whether test tooling itself must comply | Guidance.md | C2: Network Policy Verification | -- | Guidance.md (directional) | TBD |
| C-002 | C:evaluative:sufficiency | RationaleGap | Guidance | Guidance | Add guidance on minimum confidence threshold: when does the suite provide "enough" validation evidence to approve a harness release? (e.g., all contract tests pass + integration tests pass when API key available) | No document specifies what level of test passage constitutes sufficient validation for release decisions | Guidance.md | entire document scanned | -- | Guidance.md (directional) | TBD |

---

## Matrix F -- Requirements (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| F:normative:necessity | normative | necessity | foundational enforcement mandate | 0 | NO_ITEMS | Core enforcement mandates established in REQ-01 through REQ-12 |
| F:normative:sufficiency | normative | sufficiency | validated governance adequacy | 1 | HAS_ITEMS | Governance test validation sufficiency not specified |
| F:normative:completeness | normative | completeness | total governance coverage | 0 | NO_ITEMS | All governance behavioral areas addressed |
| F:normative:consistency | normative | consistency | disciplined enforcement consistency | 0 | NO_ITEMS | Requirements consistently structured |
| F:operative:necessity | operative | necessity | critical operational foundation | 1 | HAS_ITEMS | Missing dependency ordering between phases |
| F:operative:sufficiency | operative | sufficiency | proven operational competence | 0 | NO_ITEMS | Procedure steps demonstrate competent execution path |
| F:operative:completeness | operative | completeness | total operational readiness | 0 | NO_ITEMS | All phases present |
| F:operative:consistency | operative | consistency | harmonized procedural reliability | 1 | HAS_ITEMS | Inconsistent location references |
| F:evaluative:necessity | evaluative | necessity | essential merit foundation | 0 | NO_ITEMS | Merit foundation established via OBJ-006 link |
| F:evaluative:sufficiency | evaluative | sufficiency | warranted value competence | 0 | NO_ITEMS | Value proposition supported by Guidance |
| F:evaluative:completeness | evaluative | completeness | exhaustive value accounting | 0 | NO_ITEMS | Value scope aligned with deliverable scope |
| F:evaluative:consistency | evaluative | consistency | coherent value integrity | 0 | NO_ITEMS | Value arguments consistent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| F-001 | F:normative:sufficiency | VerificationGap | Specification | Specification | Add explicit pass criteria for REQ-08 governance tests: define what "all governance conditions are met" means in testable terms (enumerate the exact conditions that must simultaneously be true) | REQ-08 says "all governance conditions are met" but does not enumerate exhaustively; test writers must infer from SPEC 9.7 | Specification.md | REQ-08: Subagent Governance Fail-Closed Validation | -- | Specification.md (normative) | TBD |
| F-002 | F:operative:necessity | VerificationGap | Procedure | Procedure | Add explicit dependency gates between phases: Phase 2 requires Phase 1 output (test inventory); Phase 3 requires Phase 2 output (scripts); Phase 4 can partially overlap Phase 2 | Procedure phases are sequenced but no explicit dependency or gate condition is stated; an operator could attempt Phase 2 without completing Phase 1 | Procedure.md | Steps (Phase headers) | -- | Procedure.md (operational) | TBD |
| F-003 | F:operative:consistency | Normalization | Datasheet | Guidance | Normalize script and documentation path references: Datasheet says `frontend/scripts/validate-harness-*.mjs` and `frontend/docs/harness/`; these paths are labeled ASSUMPTION -- confirm or establish canonical paths | Multiple documents reference these paths but always with ASSUMPTION caveat; inconsistency risk if actual paths differ | Datasheet.md; Procedure.md | Datasheet: Construction table "Script location"; Procedure: Phase 5 Step 5.4 | -- | Human decision (confirm actual paths) | TBD |

---

## Matrix D -- Objectives (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| D:normative:guiding | normative | guiding | authoritative regulatory direction | 0 | NO_ITEMS | Regulatory direction clear via SPEC references |
| D:normative:applying | normative | applying | enforced compliance practice | 1 | HAS_ITEMS | Bootstrap policy constraint enforcement underspecified |
| D:normative:judging | normative | judging | definitive compliance ruling | 0 | NO_ITEMS | Verification table provides ruling structure |
| D:normative:reviewing | normative | reviewing | conclusive regulatory review | 0 | NO_ITEMS | Phase 5 review covers this |
| D:operative:guiding | operative | guiding | grounded operational guidance | 0 | NO_ITEMS | Procedure provides grounded steps |
| D:operative:applying | operative | applying | resolved operational execution | 1 | HAS_ITEMS | Fixture generation step lacks specificity |
| D:operative:judging | operative | judging | operational readiness verdict | 0 | NO_ITEMS | Phase 5 verification checks cover readiness |
| D:operative:reviewing | operative | reviewing | settled process audit | 0 | NO_ITEMS | Phase 3 repeatability verification addresses this |
| D:evaluative:guiding | evaluative | guiding | grounded value orientation | 0 | NO_ITEMS | Guidance Purpose section grounds the value |
| D:evaluative:applying | evaluative | applying | resolved merit application | 0 | NO_ITEMS | Merit application aligned with OBJ-006 |
| D:evaluative:judging | evaluative | judging | conclusive worth determination | 1 | HAS_ITEMS | No definition of "done" for the deliverable |
| D:evaluative:reviewing | evaluative | reviewing | settled quality retrospective | 0 | NO_ITEMS | Phase 5 review covers quality check |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| D-001 | D:normative:applying | WeakStatement | Specification | Specification | Clarify "bootstrap policy constraints are enforced" in REQ-04: specify which bootstrap policies exist and what enforcement looks like in test assertions | REQ-04 bullet 3 references "bootstrap policy constraints" without defining them; test authors cannot write assertions without knowing which policies to test | Specification.md | REQ-04: Session Boot Validation | -- | Specification.md (normative) | TBD |
| D-002 | D:operative:applying | WeakStatement | Procedure | Procedure | Specify fixture generation details in Step 2.1: enumerate required fixture types, sizes, and formats (e.g., "create .txt file of exactly 10,000,000 bytes, .txt file of 10,000,001 bytes, .lnk symlink, empty directory") | Step 2.1 says "create test fixture generation scripts" but does not enumerate what fixtures are needed; relies on Guidance C4 which is also non-specific about exact file list | Procedure.md | Phase 2, Step 2.1 | -- | Procedure.md (operational) | TBD |
| D-003 | D:evaluative:judging | VerificationGap | Specification | Specification | Add deliverable acceptance criteria: define minimum conditions for DEL-07-01 to be considered complete (e.g., "all REQs have at least one passing test, documentation per REQ-11 exists, repeatability per REQ-12 confirmed") | No document defines when DEL-07-01 itself is "done"; Phase 5 checks existence but not acceptance thresholds | Specification.md | entire document scanned | -- | Specification.md (normative) | TBD |

---

## Matrix X -- Verification (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| X:guiding:necessity | guiding | necessity | foundational directive requirement | 0 | NO_ITEMS | Foundational directives present |
| X:guiding:sufficiency | guiding | sufficiency | warranted guidance authority | 0 | NO_ITEMS | Guidance authority warranted through source references |
| X:guiding:completeness | guiding | completeness | comprehensive directive stewardship | 1 | HAS_ITEMS | Missing stewardship for test maintenance lifecycle |
| X:guiding:consistency | guiding | consistency | coherent directive uniformity | 0 | NO_ITEMS | Directives uniform across documents |
| X:applying:necessity | applying | necessity | essential practice requirement | 1 | HAS_ITEMS | Missing practice requirement for test isolation |
| X:applying:sufficiency | applying | sufficiency | adequate practice justification | 0 | NO_ITEMS | Practice justifications adequate |
| X:applying:completeness | applying | completeness | total practice coverage | 1 | HAS_ITEMS | Missing coverage of error path testing |
| X:applying:consistency | applying | consistency | reproducible practice integrity | 0 | NO_ITEMS | Practices reproducible per REQ-12 |
| X:judging:necessity | judging | necessity | essential adjudication mandate | 0 | NO_ITEMS | Adjudication mandates present via verification table |
| X:judging:sufficiency | judging | sufficiency | defensible adjudication sufficiency | 1 | HAS_ITEMS | Verification approach for REQ-06 underspecified |
| X:judging:completeness | judging | completeness | comprehensive adjudication scope | 0 | NO_ITEMS | Adjudication scope covers all REQs |
| X:judging:consistency | judging | consistency | principled adjudication coherence | 0 | NO_ITEMS | Adjudication approaches consistent in structure |
| X:reviewing:necessity | reviewing | necessity | essential review mandate | 0 | NO_ITEMS | Review mandate present in Phase 5 |
| X:reviewing:sufficiency | reviewing | sufficiency | adequate review justification | 1 | HAS_ITEMS | Missing review justification for test-to-requirement traceability |
| X:reviewing:completeness | reviewing | completeness | total review coverage | 0 | NO_ITEMS | Review coverage adequate |
| X:reviewing:consistency | reviewing | consistency | principled review reliability | 0 | NO_ITEMS | Review process principled |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| X-001 | X:guiding:completeness | MissingSlot | Guidance | Guidance | Add consideration for test maintenance lifecycle: who updates tests when harness contracts change? How is test-contract drift detected? | Guidance addresses initial development but not ongoing maintenance; validation suite value degrades if tests drift from evolving harness contracts | Guidance.md | entire document scanned | -- | Guidance.md (directional) | TBD |
| X-002 | X:applying:necessity | MissingSlot | Specification | Specification | Add requirement for test isolation: tests MUST NOT depend on execution order, shared mutable state, or side effects from other tests | REQ-12 addresses repeatability but not inter-test isolation; order-independent execution is implied but not mandated | Specification.md | REQ-12: Repeatable Execution | -- | Specification.md (normative) | TBD |
| X-003 | X:applying:completeness | VerificationGap | Specification | Specification | Add verification approach for harness error responses: tests should verify that invalid inputs produce correct error codes (400, 403, etc.) and not just that valid inputs succeed | REQ-05 mentions 400 for empty-message-no-attachments but other REQs do not specify expected error behaviors for invalid inputs | Specification.md | REQ-04 through REQ-10 | -- | Specification.md (normative) | TBD |
| X-004 | X:judging:sufficiency | VerificationGap | Specification | Specification | Strengthen REQ-06 verification: "verify event reception" is insufficient; specify what SSE events to expect (event types, minimum event count, or specific event fields) | Verification for REQ-06 says "verify event reception" without defining what constitutes valid SSE event reception for test assertion purposes | Specification.md | Verification table, REQ-06 row | -- | Specification.md (normative) | TBD |
| X-005 | X:reviewing:sufficiency | RationaleGap | Procedure | Procedure | Add traceability record: a mapping from each test to the REQ(s) it validates, to support review and audit of coverage claims | Phase 5 Step 5.2 says "verify test inventory covers all six behavioral areas" but no traceability artifact is specified in Records | Procedure.md | Phase 5, Step 5.2; Records table | -- | Procedure.md (operational) | TBD |

---

## Matrix E -- Evaluation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| E:normative:necessity | normative | necessity | mandatory governance foundation | 0 | NO_ITEMS | Governance foundation established |
| E:normative:sufficiency | normative | sufficiency | justified regulatory sufficiency | 0 | NO_ITEMS | Regulatory sufficiency justified through SPEC references |
| E:normative:completeness | normative | completeness | total regulatory completeness | 1 | HAS_ITEMS | Incomplete specification of boundary conditions |
| E:normative:consistency | normative | consistency | dependable regulatory uniformity | 0 | NO_ITEMS | Regulatory references uniform |
| E:operative:necessity | operative | necessity | essential operational baseline | 0 | NO_ITEMS | Operational baseline established by prerequisites |
| E:operative:sufficiency | operative | sufficiency | sufficient operational justification | 0 | NO_ITEMS | Operational justification present |
| E:operative:completeness | operative | completeness | exhaustive operational completeness | 1 | HAS_ITEMS | Missing cleanup/teardown steps |
| E:operative:consistency | operative | consistency | reproducible operational reliability | 0 | NO_ITEMS | Reproducibility addressed by REQ-12 and Phase 3 |
| E:evaluative:necessity | evaluative | necessity | fundamental value imperative | 0 | NO_ITEMS | Value imperative grounded in OBJ-006 |
| E:evaluative:sufficiency | evaluative | sufficiency | substantiated value sufficiency | 0 | NO_ITEMS | Value sufficiency substantiated |
| E:evaluative:completeness | evaluative | completeness | comprehensive value completeness | 1 | HAS_ITEMS | Missing consideration of negative-value scenarios |
| E:evaluative:consistency | evaluative | consistency | principled value reliability | 0 | NO_ITEMS | Value reliability consistent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| E-001 | E:normative:completeness | WeakStatement | Specification | Specification | Specify boundary values explicitly in REQ-09: define "10 MB" and "18 MB" in exact bytes; specify whether limits are inclusive or exclusive (e.g., "files of exactly 10,000,000 bytes MUST be accepted; files of 10,000,001 bytes MUST be rejected") | REQ-09 uses "10 MB" and "18 MB" without byte-level precision; boundary tests cannot be written without knowing exact thresholds | Specification.md | REQ-09: Attachment Resolver Validation | -- | Specification.md (normative) | TBD |
| E-002 | E:operative:completeness | MissingSlot | Procedure | Procedure | Add cleanup/teardown phase or step: specify how to clean up test fixtures, terminate harness sessions, and reset state after validation runs | Procedure Step 3.2 checks for side effects but no cleanup procedure is specified; without explicit cleanup, state leakage is possible | Procedure.md | Phase 3: Repeatability Verification | -- | Procedure.md (operational) | TBD |
| E-003 | E:evaluative:completeness | MissingSlot | Guidance | Guidance | Add consideration for false-positive risk: tests that always pass (e.g., due to mocking drift) provide negative value by creating false confidence; include guidance on canary/negative tests that verify the test framework itself can detect failures | Guidance P5 emphasizes evidence over coverage but does not address the risk of tests that pass incorrectly | Guidance.md | P5: Evidence Over Coverage Metrics | -- | Guidance.md (directional) | TBD |
