# Semantic Lensing Register: DEL-05-01 Instruction Root Bundling & Runtime Access

**Generated:** 2026-02-21
**Deliverable Folder:** /Users/ryan/ai-env/projects/chirality-app-dev/execution/PKG-05_Filesystem_Execution_Model/1_Working/DEL-05-01_Instruction_Root_Bundling/
**Warnings:** None

**Inputs Read:**
- _CONTEXT.md — `execution/PKG-05_Filesystem_Execution_Model/1_Working/DEL-05-01_Instruction_Root_Bundling/_CONTEXT.md`
- _STATUS.md — `execution/PKG-05_Filesystem_Execution_Model/1_Working/DEL-05-01_Instruction_Root_Bundling/_STATUS.md`
- _SEMANTIC.md — `execution/PKG-05_Filesystem_Execution_Model/1_Working/DEL-05-01_Instruction_Root_Bundling/_SEMANTIC.md`
- Datasheet.md — `execution/PKG-05_Filesystem_Execution_Model/1_Working/DEL-05-01_Instruction_Root_Bundling/Datasheet.md`
- Specification.md — `execution/PKG-05_Filesystem_Execution_Model/1_Working/DEL-05-01_Instruction_Root_Bundling/Specification.md`
- Guidance.md — `execution/PKG-05_Filesystem_Execution_Model/1_Working/DEL-05-01_Instruction_Root_Bundling/Guidance.md`
- Procedure.md — `execution/PKG-05_Filesystem_Execution_Model/1_Working/DEL-05-01_Instruction_Root_Bundling/Procedure.md`
- _REFERENCES.md — `execution/PKG-05_Filesystem_Execution_Model/1_Working/DEL-05-01_Instruction_Root_Bundling/_REFERENCES.md`

**Purpose:** Apply CHIRALITY_FRAMEWORK matrix cells as lenses over the production documents, capturing warranted enrichment inputs for a later enrichment pass.

---

## Summary

- Total warranted items: 18
- By document (AppliesToDoc):
  - Datasheet: 4
  - Specification: 8
  - Guidance: 3
  - Procedure: 1
  - Multi: 2
- By matrix:
  - A: 4  B: 3  C: 2  F: 2  D: 2  X: 3  E: 2
- By type:
  - Conflict: 1
  - VerificationGap: 4
  - MissingSlot: 5
  - WeakStatement: 3
  - RationaleGap: 2
  - Normalization: 1
  - TBD_Question: 2
  - MatrixError: 0
- Notable conflicts: 1
- Matrix parse errors: 0

---

## Matrix A — Orientation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| A:normative:guiding | normative | guiding | prescriptive direction | 1 | HAS_ITEMS | Lifecycle state inconsistency between Datasheet and _STATUS.md |
| A:normative:applying | normative | applying | mandatory practice | 1 | HAS_ITEMS | Read-only enforcement mechanism unspecified |
| A:normative:judging | normative | judging | compliance determination | 1 | HAS_ITEMS | Verification for REQ-02 lacks specificity on enforcement mechanism |
| A:normative:reviewing | normative | reviewing | regulatory audit | 0 | NO_ITEMS | Verification table in Specification covers audit; Procedure Step 7 covers end-to-end |
| A:operative:guiding | operative | guiding | procedural direction | 0 | NO_ITEMS | Procedure provides clear step-by-step direction |
| A:operative:applying | operative | applying | practical execution | 1 | HAS_ITEMS | Procedure prerequisites all marked ASSUMPTION |
| A:operative:judging | operative | judging | performance assessment | 0 | NO_ITEMS | Verification criteria present in Procedure |
| A:operative:reviewing | operative | reviewing | process audit | 0 | NO_ITEMS | Records table in Procedure covers audit trail |
| A:evaluative:guiding | evaluative | guiding | value orientation | 0 | NO_ITEMS | Guidance Principles section provides value orientation |
| A:evaluative:applying | evaluative | applying | merit application | 0 | NO_ITEMS | Guidance Trade-offs section addresses merit application |
| A:evaluative:judging | evaluative | judging | worth determination | 0 | NO_ITEMS | Covered by Guidance purpose statement and Specification scope |
| A:evaluative:reviewing | evaluative | reviewing | quality appraisal | 0 | NO_ITEMS | Verification table provides quality check points |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A-001 | A:normative:guiding | Conflict | Datasheet | Datasheet | Align Lifecycle State field in Datasheet with _STATUS.md current state (SEMANTIC_READY vs INITIALIZED) | Datasheet Identification table says "INITIALIZED" while _STATUS.md says "SEMANTIC_READY"; inconsistent prescriptive direction on current state | Datasheet.md; _STATUS.md | Datasheet.md#Identification; _STATUS.md#Current State | Datasheet.md#Identification ("INITIALIZED"); _STATUS.md ("SEMANTIC_READY") | _STATUS.md (it tracks transitions) | TBD |
| A-002 | A:normative:applying | WeakStatement | Specification | Specification | Specify the enforcement mechanism for instruction root read-only protection (e.g., filesystem permissions, runtime guard, API restriction) | REQ-02 mandates separation but the mandatory practice for enforcement is ambiguous — "MUST NOT be modified" without specifying how prevention is achieved at runtime | Specification.md | Specification.md#REQ-02: Instruction Root vs Working Root Separation at Runtime | — | — | TBD |
| A-003 | A:normative:judging | VerificationGap | Specification | Specification | Add specific verification mechanism for REQ-02 (how to confirm agents cannot write to instruction root — e.g., test that attempts to write to instruction root path fail with expected error) | Verification for REQ-02 says "verify agents cannot write" but does not specify the expected behavior (error type, rejection mechanism) when a write is attempted | Specification.md | Specification.md#Verification (REQ-02 row) | — | — | TBD |
| A-004 | A:operative:applying | WeakStatement | Procedure | Procedure | Clarify prerequisite dependency status — confirm whether DEL-01-01, DEL-01-02, DEL-03-01 are hard prerequisites or soft prerequisites for this deliverable | All three upstream prerequisites in the Procedure are marked "ASSUMPTION — expected prerequisite; dependency extraction pending"; this weakens practical execution confidence | Procedure.md | Procedure.md#Prerequisites | — | — | TBD |

---

## Matrix B — Conceptualization (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| B:data:necessity | data | necessity | essential fact | 1 | HAS_ITEMS | Instruction root content manifest not exhaustively defined |
| B:data:sufficiency | data | sufficiency | adequate evidence | 0 | NO_ITEMS | Datasheet Attributes table provides adequate evidence for key parameters |
| B:data:completeness | data | completeness | comprehensive record | 1 | HAS_ITEMS | Instruction root location details incomplete |
| B:data:consistency | data | consistency | reliable measurement | 0 | NO_ITEMS | SHA-256 integrity check in REQ-04 verification provides reliable measurement |
| B:information:necessity | information | necessity | essential signal | 0 | NO_ITEMS | Key signals (separation model, network policy) present in Datasheet |
| B:information:sufficiency | information | sufficiency | adequate context | 0 | NO_ITEMS | Guidance Considerations provide adequate context for decisions |
| B:information:completeness | information | completeness | comprehensive account | 0 | NO_ITEMS | Documents collectively provide comprehensive account |
| B:information:consistency | information | consistency | coherent message | 1 | HAS_ITEMS | docs/* content list inconsistency |
| B:knowledge:necessity | knowledge | necessity | fundamental understanding | 0 | NO_ITEMS | Guidance Principles provide fundamental understanding |
| B:knowledge:sufficiency | knowledge | sufficiency | competent expertise | 0 | NO_ITEMS | Guidance C1-C4 provide competent technical expertise |
| B:knowledge:completeness | knowledge | completeness | thorough mastery | 0 | NO_ITEMS | Coverage adequate for current lifecycle state |
| B:knowledge:consistency | knowledge | consistency | coherent understanding | 0 | NO_ITEMS | Understanding is coherent across documents |
| B:wisdom:necessity | wisdom | necessity | essential discernment | 0 | NO_ITEMS | Guidance Trade-offs section provides essential discernment |
| B:wisdom:sufficiency | wisdom | sufficiency | adequate judgment | 0 | NO_ITEMS | Trade-off recommendations are reasonable |
| B:wisdom:completeness | wisdom | completeness | holistic insight | 0 | NO_ITEMS | Guidance provides holistic perspective |
| B:wisdom:consistency | wisdom | consistency | principled reasoning | 0 | NO_ITEMS | Reasoning is principled and consistent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| B-001 | B:data:necessity | MissingSlot | Datasheet | Datasheet | Add explicit enumeration of governance documents within docs/* (currently listed as "governance documents" in Specification but not exhaustively enumerated in Datasheet) | Datasheet Attributes lists "Instruction Root Contents" as `AGENTS.md, README.md, agents/*, docs/*` but Specification REQ-01 additionally enumerates "DIRECTIVE, CONTRACT, SPEC, TYPES, PLAN" — the essential fact of which specific docs/* files are canonical is missing from Datasheet | Datasheet.md; Specification.md | Datasheet.md#Attributes; Specification.md#REQ-01 | — | — | TBD |
| B-002 | B:data:completeness | MissingSlot | Datasheet | Datasheet | Add the expected bundled directory structure (e.g., Resources/instructions/) as a data attribute | Datasheet Construction section records instruction root location for dev and packaged modes but uses ASSUMPTION tags and TBD for the packaged path — the comprehensive record of the target directory structure is incomplete | Datasheet.md | Datasheet.md#Construction | — | — | TBD |
| B-003 | B:information:consistency | Normalization | Multi | Guidance | Normalize the list of docs/* contents across documents — Specification says "DIRECTIVE, CONTRACT, SPEC, TYPES, PLAN" while Procedure Step 2 says "DIRECTIVE.md, CONTRACT.md, SPEC.md, TYPES.md, PLAN.md" (with extensions) and Datasheet says "framework docs (docs/*)" generically | The coherent message about docs/* contents is expressed at different levels of specificity across documents, creating drift risk on what is canonical | Datasheet.md; Specification.md; Procedure.md | Datasheet.md#Attributes; Specification.md#REQ-01; Procedure.md#Step 2 | — | — | TBD |

---

## Matrix C — Formulation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| C:normative:necessity | normative | necessity | Binding Regulatory Standard | 0 | NO_ITEMS | REQ-01 through REQ-06 establish binding standards; well-covered |
| C:normative:sufficiency | normative | sufficiency | Warranted Compliance Proof | 1 | HAS_ITEMS | REQ-04 integrity verification lacks build-time automation detail |
| C:normative:completeness | normative | completeness | Exhaustive Compliance Coverage | 0 | NO_ITEMS | Six requirements cover the scope adequately |
| C:normative:consistency | normative | consistency | Harmonized Regulatory Integrity | 0 | NO_ITEMS | Requirements are internally consistent |
| C:operative:necessity | operative | necessity | Foundational Execution Prerequisite | 1 | HAS_ITEMS | No error handling for missing instruction files |
| C:operative:sufficiency | operative | sufficiency | Demonstrated Process Competence | 0 | NO_ITEMS | Procedure steps demonstrate competence adequately |
| C:operative:completeness | operative | completeness | Complete Operational Accounting | 0 | NO_ITEMS | Seven procedure steps provide complete accounting |
| C:operative:consistency | operative | consistency | Reliable Process Discipline | 0 | NO_ITEMS | Process steps are disciplined and ordered |
| C:evaluative:necessity | evaluative | necessity | Core Merit Foundation | 0 | NO_ITEMS | Guidance Purpose provides merit foundation |
| C:evaluative:sufficiency | evaluative | sufficiency | Substantiated Worth Appraisal | 0 | NO_ITEMS | Trade-offs section provides substantiated appraisal |
| C:evaluative:completeness | evaluative | completeness | Holistic Worth Assessment | 0 | NO_ITEMS | Guidance covers holistic assessment |
| C:evaluative:consistency | evaluative | consistency | Principled Valuation Coherence | 0 | NO_ITEMS | Valuation reasoning is coherent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| C-001 | C:normative:sufficiency | VerificationGap | Specification | Procedure | Add a build-time step or CI check that automatically compares SHA-256 hashes of bundled instruction files against source (REQ-04 verification is described but no automation or tooling is specified) | Warranted compliance proof for content integrity requires a repeatable mechanism; currently described only as a manual hash comparison | Specification.md; Procedure.md | Specification.md#Verification (REQ-04 row); Procedure.md#Step 7 | — | — | TBD |
| C-002 | C:operative:necessity | MissingSlot | Specification | Specification | Add a requirement or guidance on runtime behavior when instruction root files are missing or corrupted (e.g., graceful degradation, error reporting) | No document addresses what happens if instruction root content is absent or damaged at runtime — this is a foundational execution prerequisite for resilience | Specification.md; Guidance.md | entire document scanned | — | — | TBD |

---

## Matrix F — Requirements (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| F:normative:necessity | normative | necessity | Mandatory Conformance Baseline | 0 | NO_ITEMS | REQ-01 through REQ-06 establish mandatory baseline |
| F:normative:sufficiency | normative | sufficiency | Defensible Compliance Adequacy | 1 | HAS_ITEMS | ASSUMPTION tag on REQ-04 source weakens defensibility |
| F:normative:completeness | normative | completeness | Total Conformance Assurance | 0 | NO_ITEMS | Requirements scope is complete for the deliverable |
| F:normative:consistency | normative | consistency | Principled Compliance Constancy | 0 | NO_ITEMS | Requirements are consistently phrased and sourced |
| F:operative:necessity | operative | necessity | Vital Operational Readiness | 0 | NO_ITEMS | Prerequisites identified (even if marked ASSUMPTION) |
| F:operative:sufficiency | operative | sufficiency | Sufficient Execution Capability | 0 | NO_ITEMS | Procedure steps are sufficient for execution |
| F:operative:completeness | operative | completeness | Exhaustive Operational Mastery | 0 | NO_ITEMS | Procedure covers end-to-end workflow |
| F:operative:consistency | operative | consistency | Coherent Operational Constancy | 0 | NO_ITEMS | Operational steps are coherent |
| F:evaluative:necessity | evaluative | necessity | Fundamental Valuation Imperative | 1 | HAS_ITEMS | No explicit acceptance criteria beyond verification table |
| F:evaluative:sufficiency | evaluative | sufficiency | Justified Valuation Adequacy | 0 | NO_ITEMS | Trade-off analysis provides justification |
| F:evaluative:completeness | evaluative | completeness | Comprehensive Worth Accounting | 0 | NO_ITEMS | Worth is accounted for through requirements + verification |
| F:evaluative:consistency | evaluative | consistency | Principled Quality Coherence | 0 | NO_ITEMS | Quality reasoning is coherent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| F-001 | F:normative:sufficiency | RationaleGap | Specification | Guidance | Add rationale for extending K-AUTH-2 (approval integrity) to instruction bundling — REQ-04 source says "ASSUMPTION — extended to instruction bundling by analogy" without explaining why this analogy holds | Defensible compliance adequacy requires the analogy to be explicitly warranted, not just asserted as assumption | Specification.md | Specification.md#REQ-04: Instruction Root Content Integrity | — | — | TBD |
| F-002 | F:evaluative:necessity | MissingSlot | Specification | Specification | Add explicit acceptance criteria that define "done" for DEL-05-01 (beyond the verification table) — e.g., what constitutes a passing state for the deliverable as a whole | The fundamental valuation imperative — what makes this deliverable complete and acceptable — is implicit in the verification table but not stated as explicit acceptance criteria | Specification.md | Specification.md#Verification | — | — | TBD |

---

## Matrix D — Objectives (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| D:normative:guiding | normative | guiding | Definitive Regulatory Mandate | 0 | NO_ITEMS | DIRECTIVE Section 2.6 provides definitive mandate; well-sourced |
| D:normative:applying | normative | applying | Resolved Compliance Enactment | 0 | NO_ITEMS | REQ-01 through REQ-06 enact compliance requirements |
| D:normative:judging | normative | judging | Conclusive Conformance Verdict | 0 | NO_ITEMS | Verification table provides conformance judgment mechanism |
| D:normative:reviewing | normative | reviewing | Definitive Regulatory Scrutiny | 0 | NO_ITEMS | End-to-end verification in Procedure Step 7 covers scrutiny |
| D:operative:guiding | operative | guiding | Resolved Procedural Stewardship | 1 | HAS_ITEMS | No rollback or recovery guidance |
| D:operative:applying | operative | applying | Confirmed Execution Delivery | 0 | NO_ITEMS | Procedure steps provide execution delivery path |
| D:operative:judging | operative | judging | Conclusive Performance Verdict | 0 | NO_ITEMS | Verification criteria in Procedure provide verdict mechanism |
| D:operative:reviewing | operative | reviewing | Definitive Process Examination | 0 | NO_ITEMS | Records table in Procedure covers examination |
| D:evaluative:guiding | evaluative | guiding | Authoritative Value Stewardship | 0 | NO_ITEMS | Guidance Purpose and Principles provide value stewardship |
| D:evaluative:applying | evaluative | applying | Confirmed Merit Delivery | 1 | HAS_ITEMS | No metrics for instruction access performance |
| D:evaluative:judging | evaluative | judging | Conclusive Worth Judgment | 0 | NO_ITEMS | Worth judgment covered by verification outcomes |
| D:evaluative:reviewing | evaluative | reviewing | Definitive Quality Appraisal | 0 | NO_ITEMS | Quality appraisal covered by end-to-end verification |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| D-001 | D:operative:guiding | MissingSlot | Guidance | Guidance | Add guidance on error recovery / rollback if bundling configuration fails or instruction root is misconfigured (e.g., what to do if Step 3 or Step 4 verification fails) | Resolved procedural stewardship requires not just the forward path but also recovery guidance; Procedure steps have verification but no guidance on what to do if verification fails | Guidance.md; Procedure.md | Guidance.md#Considerations; Procedure.md#Steps | — | — | TBD |
| D-002 | D:evaluative:applying | TBD_Question | Multi | Guidance | TBD: Are there performance requirements for instruction root access (e.g., maximum latency for path resolution, file read time)? If so, add to Specification. | Confirmed merit delivery requires knowing whether instruction access speed matters for user experience or agent boot time; no document addresses performance characteristics | Specification.md; Guidance.md | entire document scanned | — | — | TBD |

---

## Matrix X — Verification (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| X:guiding:necessity | guiding | necessity | Foundational Governance Directive | 0 | NO_ITEMS | Governance directives well-sourced to DIRECTIVE, CONTRACT |
| X:guiding:sufficiency | guiding | sufficiency | Warranted Governance Assurance | 0 | NO_ITEMS | Source citations provide governance assurance |
| X:guiding:completeness | guiding | completeness | Comprehensive Stewardship Scope | 1 | HAS_ITEMS | No stewardship for instruction root versioning |
| X:guiding:consistency | guiding | consistency | Unified Directional Constancy | 0 | NO_ITEMS | Directional consistency maintained across documents |
| X:applying:necessity | applying | necessity | Essential Enactment Readiness | 0 | NO_ITEMS | Procedure prerequisites define readiness |
| X:applying:sufficiency | applying | sufficiency | Demonstrated Enactment Adequacy | 1 | HAS_ITEMS | Verification for REQ-05 lacks edge cases |
| X:applying:completeness | applying | completeness | Exhaustive Enactment Coverage | 0 | NO_ITEMS | Seven procedure steps + verification table cover enactment |
| X:applying:consistency | applying | consistency | Disciplined Enactment Integrity | 0 | NO_ITEMS | Steps are disciplined and ordered |
| X:judging:necessity | judging | necessity | Foundational Adjudication Standard | 0 | NO_ITEMS | Verification table provides adjudication standard |
| X:judging:sufficiency | judging | sufficiency | Warranted Adjudication Proof | 0 | NO_ITEMS | Expected results in verification table provide proof framework |
| X:judging:completeness | judging | completeness | Comprehensive Adjudication Scope | 1 | HAS_ITEMS | No adjudication for update/upgrade scenario |
| X:judging:consistency | judging | consistency | Principled Adjudication Integrity | 0 | NO_ITEMS | Adjudication approach is consistent |
| X:reviewing:necessity | reviewing | necessity | Foundational Oversight Imperative | 0 | NO_ITEMS | Records table in Procedure provides oversight basis |
| X:reviewing:sufficiency | reviewing | sufficiency | Demonstrated Oversight Adequacy | 0 | NO_ITEMS | End-to-end verification demonstrates adequacy |
| X:reviewing:completeness | reviewing | completeness | Exhaustive Oversight Coverage | 0 | NO_ITEMS | Coverage is adequate for current scope |
| X:reviewing:consistency | reviewing | consistency | Principled Oversight Constancy | 0 | NO_ITEMS | Oversight approach is consistent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| X-001 | X:guiding:completeness | RationaleGap | Guidance | Guidance | Add consideration for how instruction root content is versioned across app updates (e.g., what happens when a new app version ships updated instructions while user has an older working root) | Comprehensive stewardship scope should address the lifecycle of instruction content across versions — currently only build-time bundling is discussed, not update scenarios | Guidance.md | Guidance.md#Considerations | — | — | TBD |
| X-002 | X:applying:sufficiency | VerificationGap | Specification | Specification | Add edge case verification for REQ-05: working root on a read-only volume, working root on a network mount, working root path with unicode characters | Demonstrated enactment adequacy for working root independence should include edge cases beyond the three currently listed (home dir, spaces, external volume) | Specification.md; Procedure.md | Specification.md#Verification (REQ-05 row); Procedure.md#Step 6 | — | — | TBD |
| X-003 | X:judging:completeness | TBD_Question | Specification | Specification | TBD: Should there be verification criteria for instruction root behavior during app update (old instructions replaced, migration path, backward compatibility)? | Comprehensive adjudication scope should consider whether the update/upgrade scenario requires its own verification criteria or is out of scope for DEL-05-01 | Specification.md | Specification.md#Verification | — | — | TBD |

---

## Matrix E — Evaluation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| E:normative:necessity | normative | necessity | Obligatory Governance Foundation | 0 | NO_ITEMS | Governance foundation well-established via DIRECTIVE, CONTRACT references |
| E:normative:sufficiency | normative | sufficiency | Substantiated Governance Warrant | 0 | NO_ITEMS | Source citations substantiate governance claims |
| E:normative:completeness | normative | completeness | Exhaustive Governance Scope | 0 | NO_ITEMS | Governance scope is exhaustive for the deliverable |
| E:normative:consistency | normative | consistency | Principled Governance Constancy | 0 | NO_ITEMS | Governance references are consistent |
| E:operative:necessity | operative | necessity | Vital Operational Foundation | 1 | HAS_ITEMS | Responsible party unassigned |
| E:operative:sufficiency | operative | sufficiency | Demonstrated Operational Warrant | 0 | NO_ITEMS | Operational warrant demonstrated through procedure |
| E:operative:completeness | operative | completeness | Exhaustive Operational Scope | 0 | NO_ITEMS | Operational scope is exhaustive |
| E:operative:consistency | operative | consistency | Principled Operational Discipline | 0 | NO_ITEMS | Operational discipline is principled |
| E:evaluative:necessity | evaluative | necessity | Fundamental Worth Imperative | 0 | NO_ITEMS | Worth imperative established in Guidance Purpose |
| E:evaluative:sufficiency | evaluative | sufficiency | Substantiated Worth Warrant | 1 | HAS_ITEMS | Pseudocode example unvalidated |
| E:evaluative:completeness | evaluative | completeness | Exhaustive Worth Accounting | 0 | NO_ITEMS | Worth accounting adequate for lifecycle state |
| E:evaluative:consistency | evaluative | consistency | Principled Worth Constancy | 0 | NO_ITEMS | Worth reasoning is constant |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| E-001 | E:operative:necessity | WeakStatement | Datasheet | Datasheet | Assign or explicitly mark "Responsible Party" as requiring human assignment (currently "TBD" with no indication of who should fill it) | Vital operational foundation requires knowing who is accountable; "TBD" for Responsible Party with no further direction weakens operational readiness | Datasheet.md | Datasheet.md#Identification | — | — | TBD |
| E-002 | E:evaluative:sufficiency | VerificationGap | Guidance | Procedure | Add a verification step to confirm that the pseudocode path resolution example (Guidance C2) actually works against the real Electron configuration before relying on it | The pseudocode in Guidance (getInstructionRootPath) is marked ASSUMPTION and illustrative-only, but Procedure Step 4 references implementing this pattern without a step to validate the assumed path structure | Guidance.md; Procedure.md | Guidance.md#C2: Path Resolution Strategy; Procedure.md#Step 4 | — | — | TBD |
