# Semantic Lensing Register: DEL-08-01 `_REFERENCES.md` Content Hashes + Verification

**Generated:** 2026-02-21
**Deliverable Folder:** execution/PKG-08_Optional_Integrity_Hardening/1_Working/DEL-08-01_References_Content_Hashes/
**Warnings:** None

**Inputs Read:**
- _CONTEXT.md — `execution/PKG-08_Optional_Integrity_Hardening/1_Working/DEL-08-01_References_Content_Hashes/_CONTEXT.md`
- _STATUS.md — `execution/PKG-08_Optional_Integrity_Hardening/1_Working/DEL-08-01_References_Content_Hashes/_STATUS.md`
- _SEMANTIC.md — `execution/PKG-08_Optional_Integrity_Hardening/1_Working/DEL-08-01_References_Content_Hashes/_SEMANTIC.md`
- Datasheet.md — `execution/PKG-08_Optional_Integrity_Hardening/1_Working/DEL-08-01_References_Content_Hashes/Datasheet.md`
- Specification.md — `execution/PKG-08_Optional_Integrity_Hardening/1_Working/DEL-08-01_References_Content_Hashes/Specification.md`
- Guidance.md — `execution/PKG-08_Optional_Integrity_Hardening/1_Working/DEL-08-01_References_Content_Hashes/Guidance.md`
- Procedure.md — `execution/PKG-08_Optional_Integrity_Hardening/1_Working/DEL-08-01_References_Content_Hashes/Procedure.md`
- _REFERENCES.md — `execution/PKG-08_Optional_Integrity_Hardening/1_Working/DEL-08-01_References_Content_Hashes/_REFERENCES.md`

**Purpose:** Apply CHIRALITY_FRAMEWORK matrix cells as lenses over the production documents, capturing warranted enrichment inputs for a later enrichment pass.

## Summary

- Total warranted items: 18
- By document:
  - Datasheet: 2
  - Specification: 7
  - Guidance: 4
  - Procedure: 3
  - Multi: 2
- By matrix:
  - A: 4  B: 3  C: 2  F: 3  D: 2  X: 2  E: 2
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

## Matrix A -- Orientation (3x4)

### Lens Coverage
| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| A:normative:guiding | normative | guiding | prescriptive direction | 1 | HAS_ITEMS | Verification failure policy remains TBD; prescriptive direction is incomplete without it |
| A:normative:applying | normative | applying | mandatory practice | 1 | HAS_ITEMS | REQ-03 failure behavior (block vs. warn) is undefined as mandatory practice |
| A:normative:judging | normative | judging | compliance determination | 1 | HAS_ITEMS | No acceptance criteria for backward compatibility claim (REQ-02) |
| A:normative:reviewing | normative | reviewing | regulatory audit | 0 | NO_ITEMS | Audit trail coverage is adequately addressed across docs |
| A:operative:guiding | operative | guiding | procedural direction | 0 | NO_ITEMS | Procedure provides clear phased direction |
| A:operative:applying | operative | applying | practical execution | 1 | HAS_ITEMS | Symbolic link handling is TBD in Procedure Step 2.1 |
| A:operative:judging | operative | judging | performance assessment | 0 | NO_ITEMS | Verification table in Procedure covers performance checks |
| A:operative:reviewing | operative | reviewing | process audit | 0 | NO_ITEMS | Records table in Procedure addresses audit artifacts |
| A:evaluative:guiding | evaluative | guiding | value orientation | 0 | NO_ITEMS | Guidance Purpose section explains value adequately |
| A:evaluative:applying | evaluative | applying | merit application | 0 | NO_ITEMS | Trade-offs table in Guidance covers merit assessment |
| A:evaluative:judging | evaluative | judging | worth determination | 0 | NO_ITEMS | Scope Status Note in Specification addresses conditional worth |
| A:evaluative:reviewing | evaluative | reviewing | quality appraisal | 0 | NO_ITEMS | Verification table in Specification covers quality checks |

### Warranted Items
| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A-001 | A:normative:guiding | WeakStatement | Specification | Specification | Specify default verification failure behavior (block vs. warn) in REQ-03 rather than leaving as TBD, or add explicit TBD marker with resolution criteria | REQ-03 states failure behavior is "TBD (pending human policy decision)" which leaves the prescriptive direction materially incomplete -- implementers cannot proceed without this | Specification.md | REQ-03: Pre-Pipeline Verification Gate | | Guidance C2 documents the options; human ruling needed for DEC-HASH-002 | TBD |
| A-002 | A:normative:applying | TBD_Question | Specification | Specification | Record TBD: What is the verification failure policy (block vs. warn) for mandatory enforcement? Consult human for DEC-HASH-002 ruling | REQ-03 and REQ-05 require ORCHESTRATOR to act on failures but the mandatory practice (block vs. warn) is undefined, preventing implementation | Specification.md | REQ-03; REQ-05 | | Human decision per DEC-HASH-002 | TBD |
| A-003 | A:normative:judging | VerificationGap | Specification | Specification | Add acceptance criteria for backward compatibility of hash extension (REQ-02) -- e.g., existing tooling parses extended _REFERENCES.md without error | REQ-02 states "MUST preserve backward compatibility" but the Verification table only checks for presence of ContentHash fields, not that existing parsers remain functional | Specification.md | REQ-02; Verification table | | Specification.md | TBD |
| A-004 | A:operative:applying | TBD_Question | Procedure | Procedure | Record TBD: Define symbolic link handling policy for hash computation (follow, reject, or record as special case). Consult human or align with existing repo conventions | Procedure Step 2.1 lists "Symbolic links (follow or reject -- TBD)" as an edge case without resolution, blocking complete practical execution | Procedure.md | Phase 2 Step 2.1 item 2 | | Human decision needed | TBD |

## Matrix B -- Conceptualization (4x4)

### Lens Coverage
| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| B:data:necessity | data | necessity | essential fact | 1 | HAS_ITEMS | Implementation language is TBD |
| B:data:sufficiency | data | sufficiency | adequate evidence | 0 | NO_ITEMS | Hash algorithm and target are adequately evidenced |
| B:data:completeness | data | completeness | comprehensive record | 1 | HAS_ITEMS | Datasheet missing ResponsibleParty |
| B:data:consistency | data | consistency | reliable measurement | 0 | NO_ITEMS | SHA-256 is consistently specified across all documents |
| B:information:necessity | information | necessity | essential signal | 0 | NO_ITEMS | K-GHOST-1 alignment signal is clear across docs |
| B:information:sufficiency | information | sufficiency | adequate context | 0 | NO_ITEMS | Context for integration points is adequate |
| B:information:completeness | information | completeness | comprehensive account | 0 | NO_ITEMS | Integration points are comprehensively listed |
| B:information:consistency | information | consistency | coherent message | 1 | HAS_ITEMS | Hash computation timing described inconsistently |
| B:knowledge:necessity | knowledge | necessity | fundamental understanding | 0 | NO_ITEMS | The why/what is well established across Guidance and Specification |
| B:knowledge:sufficiency | knowledge | sufficiency | competent expertise | 0 | NO_ITEMS | Required expertise is inferable from the documents |
| B:knowledge:completeness | knowledge | completeness | thorough mastery | 0 | NO_ITEMS | Domain coverage is adequate for current phase |
| B:knowledge:consistency | knowledge | consistency | coherent understanding | 0 | NO_ITEMS | Understanding is consistent across documents |
| B:wisdom:necessity | wisdom | necessity | essential discernment | 0 | NO_ITEMS | Trade-off discernment is present in Guidance |
| B:wisdom:sufficiency | wisdom | sufficiency | adequate judgment | 0 | NO_ITEMS | Decision framework in Guidance is adequate |
| B:wisdom:completeness | wisdom | completeness | holistic insight | 0 | NO_ITEMS | Cross-deliverable interaction noted (DEL-08-07) |
| B:wisdom:consistency | wisdom | consistency | principled reasoning | 0 | NO_ITEMS | Principles are consistently applied |

### Warranted Items
| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| B-001 | B:data:necessity | MissingSlot | Procedure | Datasheet | Add implementation language/runtime to Datasheet Attributes (e.g., Node.js crypto vs. Python hashlib) -- Procedure Step 2.1 notes this as TBD | The essential fact of which language/runtime will be used is absent; Procedure acknowledges TBD but Datasheet does not record it as an attribute | Procedure.md; Datasheet.md | Phase 2 Step 2.1 item 3; Attributes table | | Human decision based on repo tooling | TBD |
| B-002 | B:data:completeness | MissingSlot | Datasheet | Datasheet | Record ResponsibleParty in Datasheet Identification table (currently TBD with no note on how to resolve) | ResponsibleParty is listed as TBD without resolution criteria or pointer to who decides, leaving the comprehensive record incomplete | Datasheet.md | Identification table | | Human assignment | TBD |
| B-003 | B:information:consistency | Normalization | Multi | Guidance | Normalize hash computation timing terminology: Datasheet says "PREPARATION scaffold time," Specification REQ-01 says "time of context sealing or scaffold creation," Guidance says "during PREPARATION scaffold." Clarify whether "context sealing" and "scaffold creation" are the same event or distinct | The timing of hash computation is described with subtly different language across documents, which could lead to implementation ambiguity about when exactly hashes are computed | Datasheet.md; Specification.md; Guidance.md | Datasheet Attributes (Hash Computation Point); Specification REQ-01; Guidance Purpose | | Guidance should clarify the relationship between context sealing and scaffold creation | TBD |

## Matrix C -- Formulation (3x4)

### Lens Coverage
| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| C:normative:necessity | normative | necessity | Obligatory Compliance Foundation | 0 | NO_ITEMS | Foundational compliance obligations are established |
| C:normative:sufficiency | normative | sufficiency | Adequate Conformance Assurance | 1 | HAS_ITEMS | FIPS 180-4 not accessible |
| C:normative:completeness | normative | completeness | Exhaustive Regulatory Coverage | 0 | NO_ITEMS | Regulatory coverage is adequate for current scope |
| C:normative:consistency | normative | consistency | Principled Regulatory Uniformity | 0 | NO_ITEMS | Uniformity across regulatory references is maintained |
| C:operative:necessity | operative | necessity | Critical Procedural Imperative | 1 | HAS_ITEMS | Missing rollback/recovery guidance |
| C:operative:sufficiency | operative | sufficiency | Competent Operational Capacity | 0 | NO_ITEMS | Operational steps are sufficiently detailed for current phase |
| C:operative:completeness | operative | completeness | Comprehensive Operational Command | 0 | NO_ITEMS | Procedure phases cover the full operational scope |
| C:operative:consistency | operative | consistency | Dependable Process Coherence | 0 | NO_ITEMS | Process steps are internally consistent |
| C:evaluative:necessity | evaluative | necessity | Fundamental Worth Basis | 0 | NO_ITEMS | Value justification is present in Guidance Purpose |
| C:evaluative:sufficiency | evaluative | sufficiency | Sufficient Value Competence | 0 | NO_ITEMS | Value arguments are sufficient |
| C:evaluative:completeness | evaluative | completeness | Holistic Value Accounting | 0 | NO_ITEMS | Value accounting covers K-GHOST-1, K-PROV-1, K-VAL-1 |
| C:evaluative:consistency | evaluative | consistency | Principled Value Coherence | 0 | NO_ITEMS | Value coherence is maintained across documents |

### Warranted Items
| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| C-001 | C:normative:sufficiency | MissingSlot | Specification | Guidance | Add note in Guidance on how to obtain or reference FIPS 180-4 for SHA-256 specification, or confirm that standard library implementations are the accepted proxy | Specification Standards table marks FIPS 180-4 as "No (standard reference -- location TBD)," which means the conformance assurance for the hash algorithm lacks an accessible reference | Specification.md | Standards table | | Guidance should explain the accepted approach to FIPS 180-4 compliance | TBD |
| C-002 | C:operative:necessity | MissingSlot | Procedure | Procedure | Add rollback or recovery steps for failed hash computation or verification integration (e.g., what happens if PREPARATION hash computation fails mid-scaffold, or if ORCHESTRATOR verification encounters an unreadable file at verification time) | Procedure covers happy-path and detection of mismatches but does not address recovery when the hash infrastructure itself fails (computation errors, I/O failures during verification), which is a critical procedural gap | Procedure.md | entire document scanned | | Procedure.md | TBD |

## Matrix F -- Requirements (3x4)

### Lens Coverage
| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| F:normative:necessity | normative | necessity | Binding Regulatory Mandate | 0 | NO_ITEMS | Binding mandates are established through K-GHOST-1 alignment |
| F:normative:sufficiency | normative | sufficiency | Sufficient Compliance Assurance | 1 | HAS_ITEMS | REQ-07 lacks verification for CI environment isolation |
| F:normative:completeness | normative | completeness | Total Regulatory Completeness | 0 | NO_ITEMS | Regulatory requirements are complete for current scope |
| F:normative:consistency | normative | consistency | Consistent Compliance Standard | 0 | NO_ITEMS | Compliance standards are consistently referenced |
| F:operative:necessity | operative | necessity | Fundamental Operational Necessity | 1 | HAS_ITEMS | Missing verification for hash recomputation workflow |
| F:operative:sufficiency | operative | sufficiency | Adequate Execution Readiness | 0 | NO_ITEMS | Execution readiness is adequate for current phase |
| F:operative:completeness | operative | completeness | Complete Operational Mastery | 0 | NO_ITEMS | Operational scope is complete |
| F:operative:consistency | operative | consistency | Stable Operational Consistency | 0 | NO_ITEMS | Operational descriptions are consistent |
| F:evaluative:necessity | evaluative | necessity | Essential Value Foundation | 0 | NO_ITEMS | Value foundation is established |
| F:evaluative:sufficiency | evaluative | sufficiency | Adequate Worth Justification | 1 | HAS_ITEMS | Effort rating lacks justification details |
| F:evaluative:completeness | evaluative | completeness | Comprehensive Value Mastery | 0 | NO_ITEMS | Value coverage is comprehensive |
| F:evaluative:consistency | evaluative | consistency | Unified Value Integrity | 0 | NO_ITEMS | Value integrity is unified across documents |

### Warranted Items
| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| F-001 | F:normative:sufficiency | VerificationGap | Specification | Specification | Add verification criterion for REQ-07 that confirms scripts operate without agent context -- current verification says "run standalone scripts in CI-like environment" but does not define what "without agent context" means in testable terms | REQ-07 requires scripts "usable in CI pipelines" and "without requiring agent context" but the verification approach does not define how to confirm agent-context independence | Specification.md | REQ-07; Verification table | | Specification.md | TBD |
| F-002 | F:operative:necessity | VerificationGap | Procedure | Specification | Add verification step or acceptance criterion for the hash recomputation workflow described in Guidance C3 (manual recomputation after intentional reference updates) | Guidance C3 describes hash recomputation triggers but neither Specification nor Procedure includes a verification check that recomputation works correctly when triggered manually | Guidance.md; Procedure.md | Guidance C3; Procedure entire document scanned | | Specification.md (add requirement); Procedure.md (add verification step) | TBD |
| F-003 | F:evaluative:sufficiency | RationaleGap | Guidance | Guidance | Expand Guidance C5 to justify the "Medium" effort rating with concrete sizing (e.g., estimated file count, LOC, or integration touch-points beyond the three listed) | Guidance C5 mentions PLAN Section 3.1 rates effort as "Medium" and lists three integration points, but provides no rationale for why Medium is appropriate or what the effort boundary conditions are | Guidance.md | C5: Effort and Integration Surface | | Guidance.md | TBD |

## Matrix D -- Objectives (3x4)

### Lens Coverage
| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| D:normative:guiding | normative | guiding | Established Prescriptive Authority | 0 | NO_ITEMS | Prescriptive authority is established through decomposition and PLAN references |
| D:normative:applying | normative | applying | Enforced Compliance Practice | 1 | HAS_ITEMS | Bypass recording requirement is missing |
| D:normative:judging | normative | judging | Conclusive Conformance Ruling | 0 | NO_ITEMS | Conformance ruling criteria are covered in Verification table |
| D:normative:reviewing | normative | reviewing | Systematic Compliance Examination | 0 | NO_ITEMS | Examination approach is documented |
| D:operative:guiding | operative | guiding | Directed Operational Method | 0 | NO_ITEMS | Procedure provides clear directed method |
| D:operative:applying | operative | applying | Prepared Practical Execution | 0 | NO_ITEMS | Prerequisites and phases are well-prepared |
| D:operative:judging | operative | judging | Definitive Performance Determination | 0 | NO_ITEMS | Verification checks provide definitive criteria |
| D:operative:reviewing | operative | reviewing | Stabilized Process Examination | 0 | NO_ITEMS | Records table supports process examination |
| D:evaluative:guiding | evaluative | guiding | Established Value Direction | 0 | NO_ITEMS | Value direction is established in Guidance Purpose |
| D:evaluative:applying | evaluative | applying | Justified Merit Enactment | 1 | HAS_ITEMS | No examples section populated |
| D:evaluative:judging | evaluative | judging | Conclusive Worth Determination | 0 | NO_ITEMS | Worth is tied to K-GHOST-1 enforcement |
| D:evaluative:reviewing | evaluative | reviewing | Integrated Quality Assessment | 0 | NO_ITEMS | Quality assessment is integrated across Verification tables |

### Warranted Items
| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| D-001 | D:normative:applying | MissingSlot | Specification | Specification | Add a requirement for bypass recording: if verification is bypassed (override by human), the bypass event SHALL be recorded with timestamp, actor, and reason. Guidance P1 states this but no corresponding requirement exists in Specification | Guidance P1 states "If verification is bypassed, the bypass must be recorded and visible in audit trails" but this enforcement practice has no corresponding requirement in Specification, creating a gap between guidance intent and normative obligation | Guidance.md; Specification.md | Guidance P1; Specification entire document scanned | | Specification.md | TBD |
| D-002 | D:evaluative:applying | WeakStatement | Guidance | Guidance | Populate the Examples section (currently "TBD") with at least one concrete example of _REFERENCES.md with hash fields and one verification command example, to demonstrate justified merit of the approach | Guidance Examples section says "TBD -- Concrete examples... will be developed during implementation" but examples are needed to justify the merit of the approach and help implementers understand the expected outcome | Guidance.md | Examples | | Guidance.md | TBD |

## Matrix X -- Verification (4x4)

### Lens Coverage
| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| X:guiding:necessity | guiding | necessity | Foundational Directive Authority | 0 | NO_ITEMS | Directive authority is grounded in PLAN and CONTRACT |
| X:guiding:sufficiency | guiding | sufficiency | Sufficient Guidance Assurance | 0 | NO_ITEMS | Guidance is sufficient for current phase |
| X:guiding:completeness | guiding | completeness | Exhaustive Guidance Scope | 0 | NO_ITEMS | Guidance scope covers key considerations |
| X:guiding:consistency | guiding | consistency | Principled Guidance Coherence | 0 | NO_ITEMS | Guidance principles are coherent |
| X:applying:necessity | applying | necessity | Mandatory Practice Enforcement | 1 | HAS_ITEMS | No requirement for hash output format standardization |
| X:applying:sufficiency | applying | sufficiency | Sufficient Practice Competence | 0 | NO_ITEMS | Practice competence is sufficient |
| X:applying:completeness | applying | completeness | Complete Practice Coverage | 0 | NO_ITEMS | Practice coverage is complete across phases |
| X:applying:consistency | applying | consistency | Dependable Practice Uniformity | 0 | NO_ITEMS | Practice is uniform across documents |
| X:judging:necessity | judging | necessity | Binding Judgment Foundation | 0 | NO_ITEMS | Judgment foundations are established |
| X:judging:sufficiency | judging | sufficiency | Sufficient Judgment Adequacy | 0 | NO_ITEMS | Judgment criteria are adequate |
| X:judging:completeness | judging | completeness | Comprehensive Adjudication Scope | 0 | NO_ITEMS | Adjudication scope covers all requirements |
| X:judging:consistency | judging | consistency | Principled Adjudication Consistency | 0 | NO_ITEMS | Adjudication is consistent |
| X:reviewing:necessity | reviewing | necessity | Essential Review Foundation | 1 | HAS_ITEMS | Verification missing for DEL-08-07 interface |
| X:reviewing:sufficiency | reviewing | sufficiency | Adequate Review Competence | 0 | NO_ITEMS | Review competence is adequate |
| X:reviewing:completeness | reviewing | completeness | Comprehensive Review Coverage | 0 | NO_ITEMS | Review coverage is comprehensive |
| X:reviewing:consistency | reviewing | consistency | Principled Review Reliability | 0 | NO_ITEMS | Review reliability is principled |

### Warranted Items
| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| X-001 | X:applying:necessity | Normalization | Specification | Specification | Standardize hash output format across REQ-01 (computation), REQ-02 (storage), and REQ-07 (standalone scripts) -- currently no single definition of the canonical hash string format (e.g., lowercase hex, with/without prefix) | Mandatory practice enforcement requires a uniform hash format definition; without it, the computation module and verification module could produce/expect different formats | Specification.md | REQ-01; REQ-02; REQ-07 | | Specification.md | TBD |
| X-002 | X:reviewing:necessity | VerificationGap | Specification | Specification | Add acceptance criterion for the interface between DEL-08-01 (hash verification output) and DEL-08-07 (staleness propagation input) -- Guidance C4 describes this dependency but no verification exists | Guidance C4 states DEL-08-07 depends on this deliverable's hash verification output, but neither the Specification Verification table nor the Procedure Verification table includes a check that the output format is consumable by DEL-08-07 | Guidance.md; Specification.md | Guidance C4; Specification Verification table | | Specification.md | TBD |

## Matrix E -- Evaluation (3x4)

### Lens Coverage
| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| E:normative:necessity | normative | necessity | Authoritative Compliance Mandate | 0 | NO_ITEMS | Compliance mandate is authoritative and well-grounded |
| E:normative:sufficiency | normative | sufficiency | Adequate Prescriptive Assurance | 0 | NO_ITEMS | Prescriptive assurance is adequate |
| E:normative:completeness | normative | completeness | Total Prescriptive Coverage | 1 | HAS_ITEMS | Guidance P1 bypass requirement not in Specification |
| E:normative:consistency | normative | consistency | Principled Prescriptive Standard | 0 | NO_ITEMS | Prescriptive standard is principled |
| E:operative:necessity | operative | necessity | Essential Operational Authority | 0 | NO_ITEMS | Operational authority is established |
| E:operative:sufficiency | operative | sufficiency | Sufficient Operational Readiness | 0 | NO_ITEMS | Operational readiness is sufficient for current phase |
| E:operative:completeness | operative | completeness | Total Operational Coverage | 0 | NO_ITEMS | Operational coverage is total across Procedure phases |
| E:operative:consistency | operative | consistency | Principled Operational Reliability | 0 | NO_ITEMS | Operational reliability is principled |
| E:evaluative:necessity | evaluative | necessity | Essential Value Authority | 0 | NO_ITEMS | Value authority is essential and grounded |
| E:evaluative:sufficiency | evaluative | sufficiency | Sufficient Value Adequacy | 0 | NO_ITEMS | Value adequacy is sufficient |
| E:evaluative:completeness | evaluative | completeness | Comprehensive Value Scope | 1 | HAS_ITEMS | Missing security-specific evaluation perspective |
| E:evaluative:consistency | evaluative | consistency | Coherent Value Integrity | 0 | NO_ITEMS | Value integrity is coherent |

### Warranted Items
| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| E-001 | E:normative:completeness | WeakStatement | Multi | Specification | Strengthen the Specification to include bypass audit trail requirement (currently only in Guidance P1) as a formal REQ, ensuring total prescriptive coverage of the verification enforcement model | Guidance P1 makes a strong statement about bypass recording ("the bypass must be recorded and visible in audit trails") but this has no corresponding SHALL statement in Specification. Under a Total Prescriptive Coverage lens this is a coverage gap in the normative layer | Guidance.md; Specification.md | Guidance P1; Specification entire document scanned | | Specification.md | TBD |
| E-002 | E:evaluative:completeness | RationaleGap | Guidance | Guidance | Add a brief security-model rationale section in Guidance explaining the threat model this deliverable addresses (e.g., what attack or failure mode does hash verification mitigate beyond the general K-GHOST-1 statement) | The deliverable is typed SECURITY_CONTROL but Guidance does not include an explicit security evaluation perspective or threat model -- the value scope would be more comprehensive with one | Datasheet.md; Guidance.md | Datasheet Identification (Type: SECURITY_CONTROL); Guidance entire document scanned | | Guidance.md | TBD |
