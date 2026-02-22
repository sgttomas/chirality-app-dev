# Semantic Lensing Register: DEL-06-04 Change Management & Git Hygiene Support

**Generated:** 2026-02-21
**Deliverable Folder:** /Users/ryan/ai-env/projects/chirality-app-dev1/execution/PKG-06_Agent_Suite_Governance/1_Working/DEL-06-04_Change_Management_Git_Hygiene/
**Warnings:** None

**Inputs Read:**
- _CONTEXT.md — `{DEL-06-04}/_CONTEXT.md` (DeliverableID DEL-06-04, Description, SOW-021, OBJ-004/OBJ-006)
- _STATUS.md — `{DEL-06-04}/_STATUS.md` (Current State: SEMANTIC_READY)
- _SEMANTIC.md — `{DEL-06-04}/_SEMANTIC.md` (All 7 matrices: A, B, C, F, D, X, E parsed successfully)
- Datasheet.md — `{DEL-06-04}/Datasheet.md` (Identification, Attributes, Conditions, Construction, References)
- Specification.md — `{DEL-06-04}/Specification.md` (Scope, REQ-01 through REQ-07, Standards, Verification, Documentation)
- Guidance.md — `{DEL-06-04}/Guidance.md` (Purpose, Principles P1-P4, Considerations C1-C5, Trade-offs T1-T2)
- Procedure.md — `{DEL-06-04}/Procedure.md` (Prerequisites, Phase A/B/C steps, Verification V.1-V.8, Records)
- _REFERENCES.md — `{DEL-06-04}/_REFERENCES.md` (Decomposition link; no deliverable-specific references yet)

**Purpose:** Apply CHIRALITY_FRAMEWORK matrix cells as lenses over the production documents, capturing warranted enrichment inputs for a later enrichment pass.

---

## Summary

- Total warranted items: 24
- By document:
  - Datasheet: 5
  - Specification: 7
  - Guidance: 5
  - Procedure: 4
  - Multi: 3
- By matrix:
  - A: 5  B: 3  C: 3  F: 3  D: 3  X: 4  E: 3
- By type:
  - Conflict: 1
  - VerificationGap: 5
  - MissingSlot: 7
  - WeakStatement: 3
  - RationaleGap: 3
  - Normalization: 3
  - TBD_Question: 2
  - MatrixError: 0
- Notable conflicts: 1
- Matrix parse errors: 0

---

## Matrix A — Orientation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| A:normative:guiding | normative | guiding | prescriptive direction | 1 | HAS_ITEMS | Publication workflow direction is TBD |
| A:normative:applying | normative | applying | mandatory practice | 1 | HAS_ITEMS | Change record format not yet codified |
| A:normative:judging | normative | judging | compliance determination | 1 | HAS_ITEMS | Verification approach lacks acceptance criteria precision |
| A:normative:reviewing | normative | reviewing | regulatory audit | 0 | NO_ITEMS | Audit trail well-covered via K-SNAP-1 and session logs |
| A:operative:guiding | operative | guiding | procedural direction | 1 | HAS_ITEMS | Phase B steps reference TBD outputs |
| A:operative:applying | operative | applying | practical execution | 0 | NO_ITEMS | Phase A/B/C steps provide adequate execution detail |
| A:operative:judging | operative | judging | performance assessment | 0 | NO_ITEMS | V.1-V.8 provide verification checks |
| A:operative:reviewing | operative | reviewing | process audit | 1 | HAS_ITEMS | No post-completion audit or retrospective step |
| A:evaluative:guiding | evaluative | guiding | value orientation | 0 | NO_ITEMS | Guidance P1-P4 adequately orient values |
| A:evaluative:applying | evaluative | applying | merit application | 0 | NO_ITEMS | Trade-offs T1/T2 address merit considerations |
| A:evaluative:judging | evaluative | judging | worth determination | 0 | NO_ITEMS | Adequately addressed through verification matrix |
| A:evaluative:reviewing | evaluative | reviewing | quality appraisal | 0 | NO_ITEMS | Quality appraisal covered by V.8 and Conflict Table |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A-001 | A:normative:guiding | MissingSlot | Specification | Specification | Add a requirement (or sub-requirement under REQ-07) specifying the minimum constraints a publication workflow must satisfy, beyond the current reference to K-AUTH-2 and K-MERGE-1 | REQ-07 references publication guidance consistency but the actual constraints a publication workflow must satisfy are not enumerated as requirements; Guidance C1 notes this is TBD | Specification.md, Guidance.md | Specification.md#REQ-07, Guidance.md#C1 | — | Specification | TBD |
| A-002 | A:normative:applying | MissingSlot | Datasheet | Datasheet | Define the change record format in the Construction section, replacing the current TBD for "Change Record Format" | Datasheet Construction section explicitly marks change record format as TBD with an assumption; this is an undischarged mandatory practice slot | Datasheet.md | Datasheet.md#Construction | — | Datasheet | TBD |
| A-003 | A:normative:judging | VerificationGap | Specification | Specification | Add measurable acceptance criteria to the Verification table (e.g., specific text strings to search for, specific sections that must exist, specific cross-reference counts) | Verification approaches are described qualitatively ("Review ... for explicit references") without pass/fail criteria; a compliance determination lens requires unambiguous acceptance thresholds | Specification.md | Specification.md#Verification | — | Specification | TBD |
| A-004 | A:operative:guiding | WeakStatement | Procedure | Procedure | Clarify what "publication guidance section or document" means in Step B.2 — specify whether this is a new document, a new section in AGENT_CHANGE.md, or both; align with the Records table which also says "TBD" for this | Step B.2 says "Draft publication guidance section or document" and Records says "TBD — either a new section in AGENT_CHANGE.md or a separate document"; the ambiguity leaves operators without procedural direction on the output format | Procedure.md | Procedure.md#Phase-B, Procedure.md#Records | — | Guidance | TBD |
| A-005 | A:operative:reviewing | MissingSlot | Procedure | Procedure | Add a Phase D or post-Phase-C step for retrospective review: confirming all TBDs from Datasheet and Guidance have been addressed or explicitly deferred with rationale | No process audit or retrospective step exists after Phase C finalization; there is no mechanism to confirm that the TBDs flagged in Datasheet and Guidance have been resolved or consciously deferred | Procedure.md | Procedure.md#Steps (entire section scanned) | — | Procedure | TBD |

---

## Matrix B — Conceptualization (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| B:data:necessity | data | necessity | essential fact | 1 | HAS_ITEMS | Responsible Party is TBD |
| B:data:sufficiency | data | sufficiency | adequate evidence | 0 | NO_ITEMS | Datasheet references are adequately sourced |
| B:data:completeness | data | completeness | comprehensive record | 1 | HAS_ITEMS | K-WRITE-1 listed but not described |
| B:data:consistency | data | consistency | reliable measurement | 0 | NO_ITEMS | Attribute sources are consistently cited |
| B:information:necessity | information | necessity | essential signal | 0 | NO_ITEMS | Context signals (SOW, OBJ) present |
| B:information:sufficiency | information | sufficiency | adequate context | 0 | NO_ITEMS | Adequate context provided across docs |
| B:information:completeness | information | completeness | comprehensive account | 0 | NO_ITEMS | Cross-document narrative is coherent |
| B:information:consistency | information | consistency | coherent message | 1 | HAS_ITEMS | Terminology inconsistency detected |
| B:knowledge:necessity | knowledge | necessity | fundamental understanding | 0 | NO_ITEMS | Domain knowledge adequately represented |
| B:knowledge:sufficiency | knowledge | sufficiency | competent expertise | 0 | NO_ITEMS | Expertise requirements implicit but adequate |
| B:knowledge:completeness | knowledge | completeness | thorough mastery | 0 | NO_ITEMS | Coverage of invariants is thorough |
| B:knowledge:consistency | knowledge | consistency | coherent understanding | 0 | NO_ITEMS | Understanding is consistently presented |
| B:wisdom:necessity | wisdom | necessity | essential discernment | 0 | NO_ITEMS | Trade-offs T1/T2 provide discernment |
| B:wisdom:sufficiency | wisdom | sufficiency | adequate judgment | 0 | NO_ITEMS | Assumptions are explicitly labeled |
| B:wisdom:completeness | wisdom | completeness | holistic insight | 0 | NO_ITEMS | Principles P1-P4 provide holistic framing |
| B:wisdom:consistency | wisdom | consistency | principled reasoning | 0 | NO_ITEMS | Reasoning is consistently principled |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| B-001 | B:data:necessity | TBD_Question | Datasheet | Datasheet | Resolve "Responsible Party: TBD" — identify the human or role responsible for this deliverable | Responsible Party is an essential fact for accountability and is currently TBD; cannot be resolved by agent | Datasheet.md | Datasheet.md#Identification | — | Human | TBD |
| B-002 | B:data:completeness | MissingSlot | Datasheet | Datasheet | Add a description row for K-WRITE-1 in the Conditions section, or document its relevance in Attributes; currently it is listed in the Governing Invariants attribute but never described in Conditions | K-WRITE-1 appears in the Governing Invariants attribute list but is not described in the Conditions table where the other invariants (K-AUTH-1, K-AUTH-2, K-MERGE-1, K-SNAP-1, K-STALE-1) each have a row | Datasheet.md | Datasheet.md#Attributes, Datasheet.md#Conditions | — | Datasheet | TBD |
| B-003 | B:information:consistency | Normalization | Multi | Guidance | Standardize terminology for the publication workflow output: "publication guidance document or section" (Specification), "publication guidance section or document" (Procedure), "Publication Workflow" (Guidance C1) — choose one canonical term and use it consistently | Three different phrasings are used across documents to refer to the same output artifact, risking drift in understanding of what is being produced | Specification.md, Procedure.md, Guidance.md | Specification.md#Documentation, Procedure.md#Phase-B, Guidance.md#C1 | Specification.md#Documentation, Procedure.md#Phase-B, Guidance.md#C1 | Guidance | TBD |

---

## Matrix C — Formulation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| C:normative:necessity | normative | necessity | Mandated Compliance Imperative | 1 | HAS_ITEMS | ALLOW_EXECUTION default state unclear |
| C:normative:sufficiency | normative | sufficiency | Authoritative Sufficiency Standard | 0 | NO_ITEMS | Sufficiency standards adequately defined via K-invariants |
| C:normative:completeness | normative | completeness | Exhaustive Regulatory Coverage | 1 | HAS_ITEMS | K-STALE-2 coverage gap |
| C:normative:consistency | normative | consistency | Uniform Regulatory Enforcement | 0 | NO_ITEMS | Enforcement model consistently presented |
| C:operative:necessity | operative | necessity | Essential Operational Capability | 0 | NO_ITEMS | Prerequisites adequately listed |
| C:operative:sufficiency | operative | sufficiency | Competent Procedural Execution | 0 | NO_ITEMS | Procedure steps provide sufficient detail |
| C:operative:completeness | operative | completeness | Comprehensive Process Mastery | 0 | NO_ITEMS | Process coverage is comprehensive |
| C:operative:consistency | operative | consistency | Reliable Process Coherence | 0 | NO_ITEMS | Process steps are coherently structured |
| C:evaluative:necessity | evaluative | necessity | Foundational Value Recognition | 0 | NO_ITEMS | Value recognition via Principles P1-P4 |
| C:evaluative:sufficiency | evaluative | sufficiency | Substantiated Quality Judgment | 0 | NO_ITEMS | Quality judgment basis is substantiated |
| C:evaluative:completeness | evaluative | completeness | Comprehensive Value Appraisal | 1 | HAS_ITEMS | Examples section entirely TBD |
| C:evaluative:consistency | evaluative | consistency | Principled Value Consistency | 0 | NO_ITEMS | Values consistently aligned with principles |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| C-001 | C:normative:necessity | WeakStatement | Specification | Specification | Clarify in REQ-02 whether ALLOW_EXECUTION defaults to FALSE or must be explicitly set; current language says "A prohibition on executing state-changing actions when ALLOW_EXECUTION=FALSE" but does not state the default | Under a mandated compliance imperative lens, the default value of the execution gate is a compliance-critical fact; if the default is not FALSE, the gate could be bypassed unintentionally | Specification.md | Specification.md#REQ-02 | — | Specification | TBD |
| C-002 | C:normative:completeness | VerificationGap | Specification | Specification | Add K-STALE-2 to the Standards table and add a verification row confirming that the staleness triage requirement is addressed in guidance | REQ-05 references K-STALE-1, K-STALE-2, and K-VAL-1, but the Standards table only lists "K-STALE-1/2" without distinguishing them; the Verification table for REQ-05 says "Review guidance for staleness acknowledgment" but does not verify the triage-by-human requirement of K-STALE-2 specifically | Specification.md | Specification.md#REQ-05, Specification.md#Standards, Specification.md#Verification | — | Specification | TBD |
| C-003 | C:evaluative:completeness | MissingSlot | Guidance | Guidance | Populate the Examples section (currently "TBD") with at least placeholder descriptions of what examples will cover, to support comprehensive value appraisal | The Examples section in Guidance states "TBD — Examples of publication workflows, change session logs, and git hygiene patterns will be developed during the IN_PROGRESS phase" — this is acceptable as a deferral but the complete absence of even example categories or templates reduces appraisal completeness | Guidance.md | Guidance.md#Examples | — | Guidance | TBD |

---

## Matrix F — Requirements (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| F:normative:necessity | normative | necessity | Mandatory Regulatory Proof | 1 | HAS_ITEMS | Verification lacks proof format |
| F:normative:sufficiency | normative | sufficiency | Proportionate Compliance Evidence | 0 | NO_ITEMS | Evidence proportionality is adequate |
| F:normative:completeness | normative | completeness | Total Governance Documentation | 1 | HAS_ITEMS | AGENT_HELPS_HUMANS location TBD |
| F:normative:consistency | normative | consistency | Coherent Governance Standard | 0 | NO_ITEMS | Governance standard consistently referenced |
| F:operative:necessity | operative | necessity | Operational Readiness Proof | 0 | NO_ITEMS | Prerequisites provide readiness checklist |
| F:operative:sufficiency | operative | sufficiency | Demonstrated Process Competence | 0 | NO_ITEMS | Process competence adequately demonstrated |
| F:operative:completeness | operative | completeness | Total Operational Documentation | 0 | NO_ITEMS | Operational documentation is comprehensive |
| F:operative:consistency | operative | consistency | Coherent Operational Framework | 0 | NO_ITEMS | Framework is coherently presented |
| F:evaluative:necessity | evaluative | necessity | Intrinsic Merit Verification | 0 | NO_ITEMS | Merit verification via trade-off analysis |
| F:evaluative:sufficiency | evaluative | sufficiency | Defensible Quality Appraisal | 0 | NO_ITEMS | Quality appraisal is defensible |
| F:evaluative:completeness | evaluative | completeness | Exhaustive Quality Accounting | 1 | HAS_ITEMS | No quality metrics defined |
| F:evaluative:consistency | evaluative | consistency | Harmonized Quality Standard | 0 | NO_ITEMS | Quality standard is harmonized across docs |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| F-001 | F:normative:necessity | VerificationGap | Specification | Specification | Define what constitutes "proof" for each verification row — e.g., for V.2 "Text search in updated AGENT_CHANGE.md" specify expected search strings or minimum citation count | Under a mandatory regulatory proof lens, verification approaches must produce deterministic proof; current verification methods are reviewer-subjective ("Review ... for ...") | Specification.md | Specification.md#Verification | — | Specification | TBD |
| F-002 | F:normative:completeness | WeakStatement | Specification | Specification | Resolve the "location TBD" annotation for `agents/AGENT_HELPS_HUMANS.md` in the Standards table — identify the specific clauses relevant to CHANGE alignment | Standards table entry for AGENT_HELPS_HUMANS says "Accessible (location TBD for specific clauses relevant to CHANGE alignment)"; under total governance documentation, all referenced standards must be precisely locatable | Specification.md | Specification.md#Standards | — | Specification | TBD |
| F-003 | F:evaluative:completeness | RationaleGap | Guidance | Guidance | Add rationale for why the constraints-based approach was chosen over prescriptive (T1 assumption) — currently the assumption references K-GATE-1 but does not explain the reasoning chain from principle to decision | Trade-off T1 selects constraints-based approach via assumption but the rationale is a parenthetical reference to K-GATE-1; under exhaustive quality accounting, the reasoning chain should be explicit | Guidance.md | Guidance.md#T1 | — | Guidance | TBD |

---

## Matrix D — Objectives (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| D:normative:guiding | normative | guiding | Evidence-Grounded Directive | 1 | HAS_ITEMS | Git hygiene conventions not evidence-grounded |
| D:normative:applying | normative | applying | Proven Mandatory Execution | 0 | NO_ITEMS | Mandatory execution paths defined via approval gates |
| D:normative:judging | normative | judging | Definitive Governance Finding | 0 | NO_ITEMS | Governance findings framework adequate |
| D:normative:reviewing | normative | reviewing | Settled Compliance Examination | 0 | NO_ITEMS | Compliance examination covered by V.1-V.8 |
| D:operative:guiding | operative | guiding | Validated Workflow Direction | 1 | HAS_ITEMS | Upstream dependencies not validated |
| D:operative:applying | operative | applying | Proven Operational Practice | 0 | NO_ITEMS | Operational practice adequately described |
| D:operative:judging | operative | judging | Documented Performance Verdict | 0 | NO_ITEMS | Performance verdicts addressed by verification |
| D:operative:reviewing | operative | reviewing | Settled Workflow Inspection | 0 | NO_ITEMS | Workflow inspection via Phase C |
| D:evaluative:guiding | evaluative | guiding | Confirmed Value Direction | 0 | NO_ITEMS | Value direction confirmed via P1-P4 |
| D:evaluative:applying | evaluative | applying | Justified Value Delivery | 0 | NO_ITEMS | Value delivery justified by principles |
| D:evaluative:judging | evaluative | judging | Definitive Quality Verdict | 1 | HAS_ITEMS | No explicit quality gate |
| D:evaluative:reviewing | evaluative | reviewing | Settled Merit Assessment | 0 | NO_ITEMS | Merit assessment via trade-off analysis |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| D-001 | D:normative:guiding | RationaleGap | Datasheet | Guidance | Add rationale for why git hygiene conventions are listed as TBD in Datasheet Construction rather than derived from existing DIRECTIVE principles; explain the evidence basis for the scope boundary (minimal vs. comprehensive) | Datasheet Construction lists "Git Hygiene Conventions: TBD" with an assumption about deriving from DIRECTIVE; Guidance T2 discusses scope but neither provides evidence-grounded directive for what conventions are needed | Datasheet.md, Guidance.md | Datasheet.md#Construction, Guidance.md#T2 | — | Guidance | TBD |
| D-002 | D:operative:guiding | TBD_Question | Procedure | Procedure | Clarify the governance document stability assumption in Prerequisites — are DIRECTIVE, CONTRACT, SPEC, and TYPES in an approved state? If so, cite the approval; if not, document the risk | Procedure Prerequisites assumption states "This deliverable depends on the governance document suite ... being in a stable, approved state" but does not confirm or cite evidence of that state; under validated workflow direction, prerequisites must be confirmed not assumed | Procedure.md | Procedure.md#Prerequisites | — | Human | TBD |
| D-003 | D:evaluative:judging | VerificationGap | Procedure | Specification | Add an explicit quality gate criterion: define what "complete" means for this deliverable (e.g., all TBDs resolved or explicitly deferred with rationale, all REQs verified, human sign-off recorded) | No definitive quality verdict criterion exists; Phase C ends with "No contradictions; or contradictions captured in Conflict Table" but does not define the threshold for declaring the deliverable complete | Procedure.md | Procedure.md#Phase-C | — | Specification | TBD |

---

## Matrix X — Verification (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| X:guiding:necessity | guiding | necessity | Foundational Directional Authority | 0 | NO_ITEMS | Directional authority established via DIRECTIVE |
| X:guiding:sufficiency | guiding | sufficiency | Substantiated Guidance Threshold | 1 | HAS_ITEMS | Guidance assumptions lack discharge criteria |
| X:guiding:completeness | guiding | completeness | Comprehensive Guidance Coverage | 0 | NO_ITEMS | Guidance covers all identified considerations |
| X:guiding:consistency | guiding | consistency | Harmonized Guidance Alignment | 0 | NO_ITEMS | Guidance aligned with normative documents |
| X:applying:necessity | applying | necessity | Binding Execution Demand | 1 | HAS_ITEMS | Inconsistency in invariant listing |
| X:applying:sufficiency | applying | sufficiency | Sufficient Practice Evidence | 0 | NO_ITEMS | Practice evidence is sufficient |
| X:applying:completeness | applying | completeness | Exhaustive Practice Coverage | 0 | NO_ITEMS | Practice coverage is exhaustive for scope |
| X:applying:consistency | applying | consistency | Uniform Practice Standard | 1 | HAS_ITEMS | Invariant listing inconsistency |
| X:judging:necessity | judging | necessity | Mandatory Adjudicative Ruling | 0 | NO_ITEMS | Adjudicative framework adequate |
| X:judging:sufficiency | judging | sufficiency | Sufficient Adjudicative Finding | 0 | NO_ITEMS | Adjudicative sufficiency adequate |
| X:judging:completeness | judging | completeness | Exhaustive Adjudicative Scope | 0 | NO_ITEMS | Adjudicative scope covers requirements |
| X:judging:consistency | judging | consistency | Principled Adjudicative Alignment | 0 | NO_ITEMS | Adjudicative alignment consistent |
| X:reviewing:necessity | reviewing | necessity | Required Conformance Audit | 1 | HAS_ITEMS | No conformance audit for excluded items |
| X:reviewing:sufficiency | reviewing | sufficiency | Sufficient Review Proficiency | 0 | NO_ITEMS | Review proficiency adequate for scope |
| X:reviewing:completeness | reviewing | completeness | Exhaustive Review Coverage | 0 | NO_ITEMS | Review coverage is comprehensive |
| X:reviewing:consistency | reviewing | consistency | Principled Review Alignment | 0 | NO_ITEMS | Review alignment is principled |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| X-001 | X:guiding:sufficiency | RationaleGap | Guidance | Guidance | Add discharge criteria for the three ASSUMPTION labels in Guidance (C1, C2/C3 scope assumptions, T1 approach selection) — specify when each assumption is confirmed or invalidated and by whom | Assumptions in Guidance C1, C5, T1, and T2 are labeled but lack discharge criteria; under substantiated guidance threshold, each assumption should specify the condition under which it is confirmed, rejected, or superseded | Guidance.md | Guidance.md#C1, Guidance.md#C5, Guidance.md#T1, Guidance.md#T2 | — | Guidance | TBD |
| X-002 | X:applying:necessity | Conflict | Multi | Datasheet | Reconcile the invariant list: Datasheet Attributes lists K-HIER-1 nowhere but Specification REQ-07 references K-HIER-1; Datasheet lists K-WRITE-1 in Attributes but Specification does not reference K-WRITE-1 in any requirement | The set of governing invariants differs between Datasheet (K-AUTH-1, K-AUTH-2, K-MERGE-1, K-SNAP-1, K-STALE-1, K-STALE-2, K-VAL-1, K-WRITE-1) and Specification (K-AUTH-1, K-AUTH-2, K-MERGE-1, K-SNAP-1, K-STALE-1, K-STALE-2, K-VAL-1 plus K-HIER-1 in REQ-07 but not K-WRITE-1); this is an inconsistency in binding execution demand | Datasheet.md, Specification.md | Datasheet.md#Attributes, Specification.md#REQ-07 | Datasheet.md#Attributes (lists K-WRITE-1, omits K-HIER-1), Specification.md#REQ-07 (references K-HIER-1, omits K-WRITE-1) | Human | TBD |
| X-003 | X:applying:consistency | Normalization | Multi | Datasheet | Align the governing invariant set across Datasheet and Specification: ensure both documents reference the same complete set and each invariant appears in both the Attributes/Conditions tables and the Requirements | Same root cause as X-002; under uniform practice standard, the invariant set must be uniform across documents | Datasheet.md, Specification.md | Datasheet.md#Attributes, Specification.md#Requirements | — | Datasheet | TBD |
| X-004 | X:reviewing:necessity | VerificationGap | Specification | Specification | Add a verification check confirming that excluded items (listed in "What This Deliverable Excludes") are genuinely out of scope and not accidentally addressed or contradicted by the deliverable's content | Specification lists five exclusions but no verification step confirms that the deliverable does not inadvertently create obligations in excluded areas; under required conformance audit, exclusion boundaries should be verified | Specification.md | Specification.md#Scope-Excludes, Specification.md#Verification | — | Specification | TBD |

---

## Matrix E — Evaluation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| E:normative:necessity | normative | necessity | Obligatory Governance Authority | 1 | HAS_ITEMS | No explicit authority delegation |
| E:normative:sufficiency | normative | sufficiency | Substantiated Governance Threshold | 0 | NO_ITEMS | Governance threshold substantiated via invariants |
| E:normative:completeness | normative | completeness | Exhaustive Mandate Coverage | 0 | NO_ITEMS | Mandate coverage is exhaustive for M-envelope |
| E:normative:consistency | normative | consistency | Coherent Mandate Uniformity | 0 | NO_ITEMS | Mandate uniformity is coherent |
| E:operative:necessity | operative | necessity | Mandatory Operational Authority | 0 | NO_ITEMS | Operational authority established via procedure |
| E:operative:sufficiency | operative | sufficiency | Demonstrated Operational Adequacy | 1 | HAS_ITEMS | Phase B output verification insufficient |
| E:operative:completeness | operative | completeness | Total Operational Coverage | 0 | NO_ITEMS | Operational coverage is total for scope |
| E:operative:consistency | operative | consistency | Uniform Operational Dependability | 0 | NO_ITEMS | Operational dependability is uniform |
| E:evaluative:necessity | evaluative | necessity | Foundational Quality Authority | 0 | NO_ITEMS | Quality authority established through principles |
| E:evaluative:sufficiency | evaluative | sufficiency | Substantiated Merit Threshold | 0 | NO_ITEMS | Merit threshold substantiated |
| E:evaluative:completeness | evaluative | completeness | Comprehensive Quality Provision | 0 | NO_ITEMS | Quality provision comprehensive for scope |
| E:evaluative:consistency | evaluative | consistency | Principled Merit Coherence | 1 | HAS_ITEMS | Normalization issue in terminology |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| E-001 | E:normative:necessity | MissingSlot | Datasheet | Datasheet | Add a "Governance Authority" or "Decision Rights" row to the Conditions table specifying who has authority to approve the final deliverable outputs and discharge the TBDs | Under obligatory governance authority, the deliverable must identify who holds decision rights; Responsible Party is TBD and no other authority delegation is documented | Datasheet.md | Datasheet.md#Conditions | — | Datasheet | TBD |
| E-002 | E:operative:sufficiency | VerificationGap | Procedure | Procedure | Add verification criteria to Phase B steps — e.g., B.1 "Each REQ traced to a specific CHANGE instruction update" should specify how tracing is recorded (table, comment, reference) and what constitutes a valid trace | Phase B verification column entries describe expected states but not how to produce or validate them; under demonstrated operational adequacy, the procedure must demonstrate its own sufficiency through verifiable intermediate outputs | Procedure.md | Procedure.md#Phase-B | — | Procedure | TBD |
| E-003 | E:evaluative:consistency | Normalization | Datasheet | Guidance | Standardize the term for the CHANGE agent's primary function: "file/git state management" (Guidance P3), "file-state changes" (Specification REQ-01), "change legibility" (Guidance P1/Purpose) — select one canonical term and define it | Three overlapping but distinct terms describe the CHANGE agent's core function; under principled merit coherence, terminology must be uniform to enable consistent evaluation | Datasheet.md, Specification.md, Guidance.md | Datasheet.md#Attributes, Specification.md#REQ-01, Guidance.md#P3 | — | Guidance | TBD |
