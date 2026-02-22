# Semantic Lensing Register: DEL-08-07 Staleness Propagation + Triage Tooling

**Generated:** 2026-02-21
**Deliverable Folder:** /Users/ryan/ai-env/projects/chirality-app-dev1/execution/PKG-08_Optional_Integrity_Hardening/1_Working/DEL-08-07_Staleness_Propagation_Triage/
**Warnings:** None

**Inputs Read:**
- _CONTEXT.md — `execution/PKG-08_Optional_Integrity_Hardening/1_Working/DEL-08-07_Staleness_Propagation_Triage/_CONTEXT.md`
- _STATUS.md — `execution/PKG-08_Optional_Integrity_Hardening/1_Working/DEL-08-07_Staleness_Propagation_Triage/_STATUS.md` (Current State: SEMANTIC_READY)
- _SEMANTIC.md — `execution/PKG-08_Optional_Integrity_Hardening/1_Working/DEL-08-07_Staleness_Propagation_Triage/_SEMANTIC.md`
- Datasheet.md — `execution/PKG-08_Optional_Integrity_Hardening/1_Working/DEL-08-07_Staleness_Propagation_Triage/Datasheet.md`
- Specification.md — `execution/PKG-08_Optional_Integrity_Hardening/1_Working/DEL-08-07_Staleness_Propagation_Triage/Specification.md`
- Guidance.md — `execution/PKG-08_Optional_Integrity_Hardening/1_Working/DEL-08-07_Staleness_Propagation_Triage/Guidance.md`
- Procedure.md — `execution/PKG-08_Optional_Integrity_Hardening/1_Working/DEL-08-07_Staleness_Propagation_Triage/Procedure.md`
- _REFERENCES.md — `execution/PKG-08_Optional_Integrity_Hardening/1_Working/DEL-08-07_Staleness_Propagation_Triage/_REFERENCES.md`

**Purpose:** Apply CHIRALITY_FRAMEWORK matrix cells as lenses over the production documents, capturing warranted enrichment inputs for a later enrichment pass.

## Summary

- Total warranted items: 21
- By document:
  - Datasheet: 3
  - Specification: 8
  - Guidance: 4
  - Procedure: 3
  - Multi: 3
- By matrix:
  - A: 4  B: 3  C: 2  F: 3  D: 3  X: 4  E: 2
- By type:
  - Conflict: 2
  - VerificationGap: 4
  - MissingSlot: 5
  - WeakStatement: 3
  - RationaleGap: 2
  - Normalization: 2
  - TBD_Question: 3
  - MatrixError: 0
- Notable conflicts: 2
- Matrix parse errors: 0

---

## Matrix A — Orientation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| A:normative:guiding | normative | guiding | prescriptive direction | 1 | HAS_ITEMS | Triage record persistence location is unresolved prescriptive gap |
| A:normative:applying | normative | applying | mandatory practice | 1 | HAS_ITEMS | REQ-09 resolution records lack mandatory format |
| A:normative:judging | normative | judging | compliance determination | 1 | HAS_ITEMS | No acceptance criteria for what constitutes a valid triage resolution |
| A:normative:reviewing | normative | reviewing | regulatory audit | 0 | NO_ITEMS | Audit trail is addressed via REQ-04 determinism and REQ-06 no ghost inputs |
| A:operative:guiding | operative | guiding | procedural direction | 1 | HAS_ITEMS | Procedure Part B Step B3 defers triage persistence to TBD |
| A:operative:applying | operative | applying | practical execution | 0 | NO_ITEMS | Part A and Part B steps are well-structured and actionable |
| A:operative:judging | operative | judging | performance assessment | 0 | NO_ITEMS | Verification table in Procedure covers operational checks adequately |
| A:operative:reviewing | operative | reviewing | process audit | 0 | NO_ITEMS | Procedure verification section covers process audit checks |
| A:evaluative:guiding | evaluative | guiding | value orientation | 0 | NO_ITEMS | Guidance Purpose section adequately frames value proposition |
| A:evaluative:applying | evaluative | applying | merit application | 0 | NO_ITEMS | Guidance Trade-offs table provides merit-based decision framework |
| A:evaluative:judging | evaluative | judging | worth determination | 0 | NO_ITEMS | Cost-benefit of conservative propagation addressed in Guidance P2 |
| A:evaluative:reviewing | evaluative | reviewing | quality appraisal | 0 | NO_ITEMS | Quality dimensions addressed via determinism, auditability, no ghost inputs |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A-001 | A:normative:guiding | Conflict | Multi | Guidance | Clarify where triage decisions are persisted: `_STATUS.md`, new `_STALENESS.md`, or tool root snapshot | Guidance CONFLICT-01 identifies this but no prescriptive direction has been established; Specification REQ-03 and Procedure Step B3 both defer to TBD | Guidance.md, Specification.md, Procedure.md | Guidance.md#C5: Triage Record Persistence, Specification.md#REQ-03, Procedure.md#Step B3 | Guidance.md#C5 vs Specification.md#REQ-03 vs Procedure.md#Step B3 | PROPOSAL: Human ruling needed on persistence location before implementation | TBD |
| A-002 | A:normative:applying | MissingSlot | Specification | Specification | Add mandatory format/schema requirements for triage resolution records (who resolved, when, disposition, evidence) | REQ-09 states resolution records should capture who/when but does not mandate a schema or format; this is a normative gap for a mandatory practice | Specification.md | Specification.md#REQ-09: Human Authority Preserved | — | PROPOSAL: Specification should define triage record schema | TBD |
| A-003 | A:normative:judging | VerificationGap | Specification | Specification | Add acceptance criteria for what constitutes a valid completed triage (e.g., all items resolved, resolution recorded, timestamp present) | Specification Verification table covers triage queue generation (REQ-03) and human authority (REQ-09) but has no criterion for a valid completed triage cycle | Specification.md | Specification.md#Verification | — | PROPOSAL: Add triage-completion verification row | TBD |
| A-004 | A:operative:guiding | WeakStatement | Procedure | Procedure | Strengthen Step B3 item 3 to specify the recording mechanism rather than deferring entirely to "TBD" | Procedure directs user to record triage decision but cannot tell them where or how; the step is not actionable as written | Procedure.md | Procedure.md#Step B3 | — | PROPOSAL: Blocked on A-001 resolution | TBD |

---

## Matrix B — Conceptualization (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| B:data:necessity | data | necessity | essential fact | 1 | HAS_ITEMS | SHA granularity definition is deferred |
| B:data:sufficiency | data | sufficiency | adequate evidence | 0 | NO_ITEMS | Evidence requirements for dirty detection are specified (SHA comparison, changed files list) |
| B:data:completeness | data | completeness | comprehensive record | 1 | HAS_ITEMS | Governed input file list is undefined |
| B:data:consistency | data | consistency | reliable measurement | 0 | NO_ITEMS | Determinism requirement (REQ-04) ensures measurement reliability |
| B:information:necessity | information | necessity | essential signal | 0 | NO_ITEMS | Staleness type (DIRTY vs PROPAGATED) is clearly defined as essential signal |
| B:information:sufficiency | information | sufficiency | adequate context | 0 | NO_ITEMS | Triage queue context fields enumerated in REQ-03 |
| B:information:completeness | information | completeness | comprehensive account | 0 | NO_ITEMS | Propagation path recording provides comprehensive account of causality |
| B:information:consistency | information | consistency | coherent message | 1 | HAS_ITEMS | Output format undefined across report and triage queue |
| B:knowledge:necessity | knowledge | necessity | fundamental understanding | 0 | NO_ITEMS | Guidance Principles P1-P5 provide foundational understanding |
| B:knowledge:sufficiency | knowledge | sufficiency | competent expertise | 0 | NO_ITEMS | Guidance Considerations C1-C7 demonstrate expertise-level coverage |
| B:knowledge:completeness | knowledge | completeness | thorough mastery | 0 | NO_ITEMS | Edge cases addressed in Guidance C6-C7 and Procedure Step A4 |
| B:knowledge:consistency | knowledge | consistency | coherent understanding | 0 | NO_ITEMS | Documents maintain consistent understanding of staleness model |
| B:wisdom:necessity | wisdom | necessity | essential discernment | 0 | NO_ITEMS | Conservative propagation principle (P2) reflects essential discernment |
| B:wisdom:sufficiency | wisdom | sufficiency | adequate judgment | 0 | NO_ITEMS | Trade-offs table in Guidance provides adequate judgment framework |
| B:wisdom:completeness | wisdom | completeness | holistic insight | 0 | NO_ITEMS | Integrity chain positioning in Guidance Purpose provides holistic perspective |
| B:wisdom:consistency | wisdom | consistency | principled reasoning | 0 | NO_ITEMS | Principles consistently derive from CONTRACT invariants |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| B-001 | B:data:necessity | TBD_Question | Datasheet | Specification | Define which files constitute "governed inputs" for a deliverable (the four production docs, Dependencies.csv, metadata files, or all files?) | Datasheet lists "Governed input change since last approved SHA" but does not enumerate which files are governed; Guidance C3 raises this as a design question but defers | Datasheet.md, Guidance.md | Datasheet.md#Attributes (Dirty Detection Basis), Guidance.md#C3: SHA Granularity | — | PROPOSAL: Human or DEL-08-06 design decision required | TBD |
| B-002 | B:data:completeness | MissingSlot | Specification | Specification | Add a requirement defining the canonical list of governed input files per deliverable (or a mechanism to declare them) | REQ-01 references "governed inputs" and "baseline SHA" but never defines what files constitute governed inputs; this is essential for completeness of the data record | Specification.md | Specification.md#REQ-01: Dirty Detection | — | PROPOSAL: Specification should enumerate or provide a mechanism for governed input declaration | TBD |
| B-003 | B:information:consistency | WeakStatement | Specification | Specification | Specify the concrete output format for staleness report and triage queue (REQ-05 says "TBD — likely markdown and/or CSV") | The output format assumption in REQ-05 is materially vague; different format choices would change implementation, testing, and consumer expectations | Specification.md | Specification.md#REQ-05: Filesystem-Representable Output | — | PROPOSAL: Define format before implementation begins | TBD |

---

## Matrix C — Formulation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| C:normative:necessity | normative | necessity | Obligatory Compliance Threshold | 1 | HAS_ITEMS | Scope contingency threshold mechanism incomplete |
| C:normative:sufficiency | normative | sufficiency | Warranted Regulatory Adequacy | 0 | NO_ITEMS | Standards table in Specification adequately maps invariants |
| C:normative:completeness | normative | completeness | Exhaustive Regulatory Coverage | 0 | NO_ITEMS | Standards table covers K-STALE-1/2, K-VAL-1, K-DEP-1, K-GHOST-1, K-SNAP-1, K-AUTH-1, K-PROV-1, K-INVENT-1 |
| C:normative:consistency | normative | consistency | Harmonized Regulatory Integrity | 0 | NO_ITEMS | CONTRACT references are consistent across all four documents |
| C:operative:necessity | operative | necessity | Critical Operational Baseline | 1 | HAS_ITEMS | Missing baseline SHA scenario underspecified |
| C:operative:sufficiency | operative | sufficiency | Calibrated Operational Proficiency | 0 | NO_ITEMS | Procedure steps are sequenced and actionable given prerequisite resolution |
| C:operative:completeness | operative | completeness | Comprehensive Process Coverage | 0 | NO_ITEMS | Part A (production) and Part B (operation) together cover full lifecycle |
| C:operative:consistency | operative | consistency | Reproducible Process Discipline | 0 | NO_ITEMS | Determinism requirement ensures reproducibility |
| C:evaluative:necessity | evaluative | necessity | Foundational Merit Recognition | 0 | NO_ITEMS | Guidance Purpose articulates the foundational value clearly |
| C:evaluative:sufficiency | evaluative | sufficiency | Substantiated Quality Appraisal | 0 | NO_ITEMS | Trade-offs table substantiates design choices |
| C:evaluative:completeness | evaluative | completeness | Exhaustive Value Accounting | 0 | NO_ITEMS | Integrity chain framing accounts for value comprehensively |
| C:evaluative:consistency | evaluative | consistency | Principled Value Coherence | 0 | NO_ITEMS | Principles consistently tied to CONTRACT invariants |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| C-001 | C:normative:necessity | VerificationGap | Specification | Specification | Add acceptance criterion for REQ-10 that specifies how the scope gate is verified programmatically or procedurally (not just "process check") | REQ-10 verification says "process check" but does not define what evidence satisfies the check; the obligatory compliance threshold for scope contingency is unclear | Specification.md | Specification.md#Verification (REQ-10 row) | — | PROPOSAL: Define observable evidence for scope gate satisfaction | TBD |
| C-002 | C:operative:necessity | WeakStatement | Specification | Specification | Clarify REQ-01 handling when no baseline SHA exists: should the deliverable be reported as "dirty," "baseline unknown," or "staleness unknown"? | Specification REQ-01 does not address the no-baseline case; Procedure Step A3 says "baseline unknown" but Guidance C7 says "staleness unknown" for missing dependency data — terminology is inconsistent for the critical operational baseline | Specification.md, Procedure.md, Guidance.md | Specification.md#REQ-01, Procedure.md#Step A3, Guidance.md#C7 | Procedure.md#Step A3 ("baseline unknown") vs Guidance.md#C7 ("staleness unknown") | PROPOSAL: Specification should normatively define the no-baseline behavior | TBD |

---

## Matrix F — Requirements (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| F:normative:necessity | normative | necessity | Imperative Governance Standard | 0 | NO_ITEMS | K-STALE-1, K-STALE-2, K-VAL-1 are clearly imperative and referenced throughout |
| F:normative:sufficiency | normative | sufficiency | Qualified Compliance Assurance | 1 | HAS_ITEMS | Verification approach for REQ-06 is "code review" only |
| F:normative:completeness | normative | completeness | Total Governance Scope Command | 0 | NO_ITEMS | Standards table provides comprehensive invariant mapping |
| F:normative:consistency | normative | consistency | Stable Governance Alignment | 0 | NO_ITEMS | Invariant references are stable across documents |
| F:operative:necessity | operative | necessity | Foundational Operational Capacity | 1 | HAS_ITEMS | CLI entry point location and naming unspecified |
| F:operative:sufficiency | operative | sufficiency | Qualified Procedural Competence | 0 | NO_ITEMS | Procedure steps are detailed enough for qualified execution |
| F:operative:completeness | operative | completeness | Complete Procedural Mastery | 0 | NO_ITEMS | Edge cases, cycle detection, partial graph all addressed |
| F:operative:consistency | operative | consistency | Dependable Process Uniformity | 0 | NO_ITEMS | Procedure and Specification are aligned on process flow |
| F:evaluative:necessity | evaluative | necessity | Essential Quality Recognition | 0 | NO_ITEMS | Quality attributes (determinism, auditability, no ghost inputs) recognized |
| F:evaluative:sufficiency | evaluative | sufficiency | Substantiated Value Judgment | 1 | HAS_ITEMS | Performance/scale expectations absent |
| F:evaluative:completeness | evaluative | completeness | Exhaustive Quality Accounting | 0 | NO_ITEMS | Quality dimensions well-covered across documents |
| F:evaluative:consistency | evaluative | consistency | Principled Quality Consistency | 0 | NO_ITEMS | Quality principles consistent across documents |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| F-001 | F:normative:sufficiency | VerificationGap | Specification | Specification | Strengthen REQ-06 verification beyond "code review" — add a declarative input manifest check or automated scan for undeclared imports/file reads | "Code review" as sole verification for no-ghost-inputs is weak for a compliance assurance claim; a static analysis check or input manifest would provide qualified assurance | Specification.md | Specification.md#Verification (REQ-06 row) | — | PROPOSAL: Add automated input-source verification alongside code review | TBD |
| F-002 | F:operative:necessity | MissingSlot | Datasheet | Datasheet | Add CLI/script entry point location, naming convention, and invocation pattern to Datasheet Construction section | Datasheet Construction section describes inputs and outputs but omits the entry point artifact itself; Procedure Step A6 references it but Datasheet does not record it as a construction aspect | Datasheet.md, Procedure.md | Datasheet.md#Construction, Procedure.md#Step A6 | — | PROPOSAL: Datasheet should record the CLI artifact | TBD |
| F-003 | F:evaluative:sufficiency | MissingSlot | Specification | Guidance | Add guidance on expected performance characteristics: approximate graph size this tooling should handle, acceptable execution time, memory constraints | No performance or scale expectations are stated anywhere; for substantiated value judgment the system should declare whether it targets 10, 100, or 1000 deliverables | Specification.md, Guidance.md | entire document scanned | — | PROPOSAL: Guidance should provide scale/performance expectations; Specification may add non-functional requirements if warranted | TBD |

---

## Matrix D — Objectives (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| D:normative:guiding | normative | guiding | Authoritative Governance Directive | 1 | HAS_ITEMS | Output location conflict unresolved |
| D:normative:applying | normative | applying | Enforced Conformance Practice | 0 | NO_ITEMS | CONTRACT invariants are enforced through requirements |
| D:normative:judging | normative | judging | Conclusive Compliance Verdict | 0 | NO_ITEMS | Verification table maps requirements to acceptance criteria |
| D:normative:reviewing | normative | reviewing | Reconciled Oversight Examination | 0 | NO_ITEMS | Procedure verification section provides review checklist |
| D:operative:guiding | operative | guiding | Established Procedural Direction | 0 | NO_ITEMS | Procedure Part A/B split provides clear procedural direction |
| D:operative:applying | operative | applying | Proven Execution Capability | 0 | NO_ITEMS | Steps are sequenced with prerequisites and checks |
| D:operative:judging | operative | judging | Conclusive Performance Finding | 1 | HAS_ITEMS | No pass/fail threshold for integration tests |
| D:operative:reviewing | operative | reviewing | Confirmed Process Examination | 0 | NO_ITEMS | Procedure Verification table provides process examination checks |
| D:evaluative:guiding | evaluative | guiding | Established Value Priority | 0 | NO_ITEMS | Guidance Purpose establishes value priority (change-impact integrity) |
| D:evaluative:applying | evaluative | applying | Resolved Merit Application | 1 | HAS_ITEMS | Responsible Party is TBD |
| D:evaluative:judging | evaluative | judging | Conclusive Worth Verdict | 0 | NO_ITEMS | Trade-offs table provides worth assessment framework |
| D:evaluative:reviewing | evaluative | reviewing | Confirmed Quality Examination | 0 | NO_ITEMS | Determinism test and code review provide quality examination |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| D-001 | D:normative:guiding | Conflict | Multi | Guidance | Resolve output location: tool root (immutable snapshot per K-SNAP-1) vs deliverable-local (near context per DIRECTIVE 2.1) | Guidance CONFLICT-02 identifies this but no authoritative directive has been issued; Specification REQ-05 and Procedure Step A2 both defer to TBD; this blocks implementation | Guidance.md, Specification.md, Procedure.md | Guidance.md#CONFLICT-02, Specification.md#REQ-05, Procedure.md#Step A2 | Guidance.md#CONFLICT-02 (K-SNAP-1 vs DIRECTIVE 2.1) | PROPOSAL: Human ruling needed before implementation | TBD |
| D-002 | D:operative:judging | VerificationGap | Specification | Specification | Add quantitative or structural acceptance criteria for integration tests (e.g., minimum graph fixture complexity, edge count, expected output structure validation) | Verification for REQ-07 and REQ-08 says "integration test" but does not define what constitutes a conclusive performance finding — no fixture specifications or pass/fail thresholds | Specification.md | Specification.md#Verification (REQ-07, REQ-08 rows) | — | PROPOSAL: Define minimum fixture graph specs and expected outputs | TBD |
| D-003 | D:evaluative:applying | TBD_Question | Datasheet | Datasheet | Assign Responsible Party for DEL-08-07 (currently TBD) | Responsible Party is listed as TBD in Datasheet Identification; no resolved merit application is possible without an accountable party | Datasheet.md | Datasheet.md#Identification (Responsible Party) | — | PROPOSAL: Human assignment needed | TBD |

---

## Matrix X — Verification (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| X:guiding:necessity | guiding | necessity | Imperative Directional Foundation | 0 | NO_ITEMS | Guidance Principles provide imperative directional foundation |
| X:guiding:sufficiency | guiding | sufficiency | Substantiated Directional Adequacy | 0 | NO_ITEMS | Guidance Considerations substantiate direction with design reasoning |
| X:guiding:completeness | guiding | completeness | Comprehensive Directional Scope | 0 | NO_ITEMS | Guidance covers principles, considerations, trade-offs, examples |
| X:guiding:consistency | guiding | consistency | Unified Directional Integrity | 0 | NO_ITEMS | Guidance direction is consistent with Specification and Procedure |
| X:applying:necessity | applying | necessity | Validated Practice Baseline | 1 | HAS_ITEMS | Error handling not in Specification |
| X:applying:sufficiency | applying | sufficiency | Justified Practice Competence | 0 | NO_ITEMS | Procedure steps demonstrate competent practice sequences |
| X:applying:completeness | applying | completeness | Complete Practice Coverage | 1 | HAS_ITEMS | No rollback or error recovery procedure |
| X:applying:consistency | applying | consistency | Disciplined Practice Uniformity | 0 | NO_ITEMS | Procedure and Specification are consistently aligned |
| X:judging:necessity | judging | necessity | Binding Threshold Judgment | 1 | HAS_ITEMS | No definition of staleness severity levels |
| X:judging:sufficiency | judging | sufficiency | Justified Adequacy Determination | 0 | NO_ITEMS | Verification table maps each requirement to a verification approach |
| X:judging:completeness | judging | completeness | Complete Assessment Adjudication | 0 | NO_ITEMS | Verification covers all 10 requirements |
| X:judging:consistency | judging | consistency | Consistent Judgment Integrity | 0 | NO_ITEMS | Verification approaches are consistent in rigor and style |
| X:reviewing:necessity | reviewing | necessity | Verified Inspection Baseline | 1 | HAS_ITEMS | No versioning for triage queue or staleness report |
| X:reviewing:sufficiency | reviewing | sufficiency | Justified Inspection Adequacy | 0 | NO_ITEMS | Procedure Verification table provides adequate inspection checklist |
| X:reviewing:completeness | reviewing | completeness | Complete Inspection Coverage | 0 | NO_ITEMS | Verification covers dirty detection, propagation, determinism, triage, human authority, file format, ghost inputs, cycles, partial graph |
| X:reviewing:consistency | reviewing | consistency | Uniform Inspection Discipline | 0 | NO_ITEMS | Verification checks use consistent validation patterns |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| X-001 | X:applying:necessity | MissingSlot | Specification | Specification | Add error handling requirements: what happens when the graph artifact is malformed, run records are corrupt, or git state is unavailable | Procedure Step A3 and A4 mention some edge cases but there is no normative requirement for error handling behavior; validated practice baseline requires defined error states | Specification.md, Procedure.md | Specification.md#Requirements (entire section), Procedure.md#Step A3, Procedure.md#Step A4 | — | PROPOSAL: Add REQ-11 for error handling behavior | TBD |
| X-002 | X:applying:completeness | RationaleGap | Guidance | Guidance | Add guidance on error recovery and rollback: what should happen if staleness calculation fails mid-run (partial output, corrupted state, retry semantics) | Guidance covers happy-path design considerations thoroughly but provides no guidance on failure modes or recovery; complete practice coverage requires addressing the unhappy path | Guidance.md | entire document scanned | — | PROPOSAL: Add a Considerations section on failure modes | TBD |
| X-003 | X:judging:necessity | Normalization | Multi | Guidance | Standardize terminology for the "no baseline" case across documents: "baseline unknown" (Procedure A3) vs "staleness unknown" (Guidance C7) are used for overlapping but distinct situations | Using different terms for related edge cases risks drift in implementation; binding threshold judgment requires consistent terminology | Procedure.md, Guidance.md | Procedure.md#Step A3, Guidance.md#C7 | Procedure.md#Step A3 vs Guidance.md#C7 | PROPOSAL: Guidance should define a vocabulary for edge-case staleness states | TBD |
| X-004 | X:reviewing:necessity | RationaleGap | Guidance | Guidance | Add rationale for whether staleness reports should be versioned/timestamped snapshots or overwritten in place; this affects auditability of the inspection baseline | Specification REQ-04 requires deterministic output and REQ-05 requires filesystem representation, but neither addresses whether reports accumulate or overwrite; the verified inspection baseline depends on this | Specification.md, Guidance.md | Specification.md#REQ-04, Specification.md#REQ-05 | — | PROPOSAL: Guidance should address report lifecycle (snapshot vs overwrite) | TBD |

---

## Matrix E — Evaluation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| E:normative:necessity | normative | necessity | Authoritative Compliance Imperative | 0 | NO_ITEMS | CONTRACT invariants are authoritatively cited and compliance is structured |
| E:normative:sufficiency | normative | sufficiency | Defensible Governance Sufficiency | 0 | NO_ITEMS | Requirements are traceable to CONTRACT sources |
| E:normative:completeness | normative | completeness | Exhaustive Governance Purview | 0 | NO_ITEMS | Standards table is comprehensive; no missing CONTRACT invariants identified |
| E:normative:consistency | normative | consistency | Harmonized Compliance Discipline | 0 | NO_ITEMS | Compliance references are harmonized across documents |
| E:operative:necessity | operative | necessity | Verified Operational Foundation | 1 | HAS_ITEMS | Upstream dependency format coupling |
| E:operative:sufficiency | operative | sufficiency | Warranted Operational Sufficiency | 0 | NO_ITEMS | Procedure provides sufficient operational detail |
| E:operative:completeness | operative | completeness | Exhaustive Operational Purview | 0 | NO_ITEMS | Both production and operation workflows covered |
| E:operative:consistency | operative | consistency | Disciplined Operational Stability | 0 | NO_ITEMS | Procedure and Specification are operationally consistent |
| E:evaluative:necessity | evaluative | necessity | Verified Value Foundation | 0 | NO_ITEMS | Value foundation (change-impact integrity) is clearly established |
| E:evaluative:sufficiency | evaluative | sufficiency | Warranted Quality Sufficiency | 0 | NO_ITEMS | Quality attributes are addressed across documents |
| E:evaluative:completeness | evaluative | completeness | Exhaustive Value Purview | 1 | HAS_ITEMS | No success metrics defined |
| E:evaluative:consistency | evaluative | consistency | Principled Value Discipline | 0 | NO_ITEMS | Value principles are consistently applied |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| E-001 | E:operative:necessity | TBD_Question | Datasheet | Datasheet | Record the actual graph artifact format and run record schema once DEL-08-04 and DEL-08-06 define them; currently marked as ASSUMPTION throughout | Multiple ASSUMPTION markers across Datasheet, Specification, and Procedure flag that upstream formats are TBD; verified operational foundation requires these to be known | Datasheet.md | Datasheet.md#Construction (Input: Dependency Graph, Input: Run Records) | — | PROPOSAL: Blocked on DEL-08-04 and DEL-08-06 completion; update Datasheet when formats are defined | TBD |
| E-002 | E:evaluative:completeness | Normalization | Specification | Guidance | Define success metrics for the staleness tooling: detection accuracy rate, false positive tolerance for propagation, triage queue usability criteria | No success metrics or KPIs exist for evaluating whether the tooling achieves its intended value; exhaustive value purview requires measurable outcomes | Specification.md, Guidance.md | entire document scanned | — | PROPOSAL: Guidance should define qualitative success criteria; Specification may add measurable acceptance thresholds | TBD |
