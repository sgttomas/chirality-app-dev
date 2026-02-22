# Semantic Lensing Register: DEL-06-05 Governance Coherence + Guardrails (OUT boundaries)

**Generated:** 2026-02-21
**Deliverable Folder:** /Users/ryan/ai-env/projects/chirality-app-dev/execution/PKG-06_Agent_Suite_Governance/1_Working/DEL-06-05_Governance_Coherence_Guardrails/
**Warnings:** None

**Inputs Read:**
- _CONTEXT.md — DEL-06-05_Governance_Coherence_Guardrails/_CONTEXT.md
- _STATUS.md — DEL-06-05_Governance_Coherence_Guardrails/_STATUS.md (SEMANTIC_READY)
- _SEMANTIC.md — DEL-06-05_Governance_Coherence_Guardrails/_SEMANTIC.md
- Datasheet.md — DEL-06-05_Governance_Coherence_Guardrails/Datasheet.md
- Specification.md — DEL-06-05_Governance_Coherence_Guardrails/Specification.md
- Guidance.md — DEL-06-05_Governance_Coherence_Guardrails/Guidance.md
- Procedure.md — DEL-06-05_Governance_Coherence_Guardrails/Procedure.md
- _REFERENCES.md — DEL-06-05_Governance_Coherence_Guardrails/_REFERENCES.md

**Purpose:** Apply CHIRALITY_FRAMEWORK matrix cells as lenses over the production documents, capturing warranted enrichment inputs for a later enrichment pass.

## Summary

- Total warranted items: 18
- By document:
  - Datasheet: 4
  - Specification: 5
  - Guidance: 3
  - Procedure: 4
  - Multi: 2
- By matrix:
  - A: 4  B: 2  C: 2  F: 3  D: 2  X: 3  E: 2
- By type:
  - Conflict: 0
  - VerificationGap: 5
  - MissingSlot: 6
  - WeakStatement: 2
  - RationaleGap: 2
  - Normalization: 2
  - TBD_Question: 1
  - MatrixError: 0
- Notable conflicts: 0
- Matrix parse errors: 0

## Matrix A -- Orientation (3x4)

### Lens Coverage (required)
| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| A:normative:guiding | normative | guiding | prescriptive direction | 1 | HAS_ITEMS | Responsible Party TBD in Datasheet |
| A:normative:applying | normative | applying | mandatory practice | 1 | HAS_ITEMS | SOW-040/042 lack invariant backing |
| A:normative:judging | normative | judging | compliance determination | 1 | HAS_ITEMS | No acceptance threshold for vocabulary spot-check |
| A:normative:reviewing | normative | reviewing | regulatory audit | 1 | HAS_ITEMS | Procedure records location TBD |
| A:operative:guiding | operative | guiding | procedural direction | 0 | NO_ITEMS | Procedure Phase 1-3 steps are well-structured |
| A:operative:applying | operative | applying | practical execution | 0 | NO_ITEMS | Steps are actionable as written |
| A:operative:judging | operative | judging | performance assessment | 0 | NO_ITEMS | PASS/FAIL criteria present for each step |
| A:operative:reviewing | operative | reviewing | process audit | 0 | NO_ITEMS | Verification table present in Procedure |
| A:evaluative:guiding | evaluative | guiding | value orientation | 0 | NO_ITEMS | Guidance Purpose section well-articulated |
| A:evaluative:applying | evaluative | applying | merit application | 0 | NO_ITEMS | Trade-offs section addresses merit considerations |
| A:evaluative:judging | evaluative | judging | worth determination | 0 | NO_ITEMS | Guidance T1 and T2 address worth/cost trade-offs |
| A:evaluative:reviewing | evaluative | reviewing | quality appraisal | 0 | NO_ITEMS | Guidance C2 provides enforcement depth assessment |

### Warranted Items
| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A-001 | A:normative:guiding | MissingSlot | Datasheet | Datasheet | Assign Responsible Party (currently "TBD") for this deliverable | The prescriptive-direction lens reveals that the normative authority for this deliverable is unassigned; without a responsible party, prescriptive direction has no accountable owner | Datasheet.md | Identification table, "Responsible Party" row | -- | Datasheet.md | TBD |
| A-002 | A:normative:applying | WeakStatement | Guidance | Guidance | Clarify why SOW-040 and SOW-042 do not warrant CONTRACT invariants beyond "addressed by absence of capability" and "addressed by professional responsibility model" | Under mandatory-practice lens, two of five guardrails rely solely on DIRECTIVE documentation without invariant or runtime enforcement; Guidance T1 acknowledges this trade-off but the rationale for acceptability could be strengthened | Guidance.md | Trade-offs > T1: Guardrail granularity vs. document weight | -- | Guidance.md | TBD |
| A-003 | A:normative:judging | VerificationGap | Specification | Specification | Add quantitative or structural pass criteria for REQ-COH-02 vocabulary spot-check (e.g., minimum number of terms checked, or an exhaustive term list) | Under compliance-determination lens, "spot-check key terms" in the verification approach for REQ-COH-02 is open-ended; a reviewer cannot determine when the check is complete | Specification.md | Verification table, REQ-COH-02 row | -- | Specification.md | TBD |
| A-004 | A:normative:reviewing | MissingSlot | Procedure | Procedure | Define where coherence and guardrail verification results will be recorded (the Records table has "TBD" for all locations) | Under regulatory-audit lens, the Procedure defines what to check but not where results are stored; auditability requires defined record locations | Procedure.md | Records table | -- | Procedure.md | TBD |

## Matrix B -- Conceptualization (4x4)

### Lens Coverage (required)
| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| B:data:necessity | data | necessity | essential fact | 1 | HAS_ITEMS | DIRECTIVE section reference inconsistency |
| B:data:sufficiency | data | sufficiency | adequate evidence | 0 | NO_ITEMS | Datasheet references are well-sourced |
| B:data:completeness | data | completeness | comprehensive record | 1 | HAS_ITEMS | Missing K-WRITE-1 details |
| B:data:consistency | data | consistency | reliable measurement | 0 | NO_ITEMS | Attribute values consistent with sources |
| B:information:necessity | information | necessity | essential signal | 0 | NO_ITEMS | Coherence dimensions clearly signaled |
| B:information:sufficiency | information | sufficiency | adequate context | 0 | NO_ITEMS | Guidance provides adequate context |
| B:information:completeness | information | completeness | comprehensive account | 0 | NO_ITEMS | -- |
| B:information:consistency | information | consistency | coherent message | 0 | NO_ITEMS | -- |
| B:knowledge:necessity | knowledge | necessity | fundamental understanding | 0 | NO_ITEMS | Guidance principles provide foundational knowledge |
| B:knowledge:sufficiency | knowledge | sufficiency | competent expertise | 0 | NO_ITEMS | -- |
| B:knowledge:completeness | knowledge | completeness | thorough mastery | 0 | NO_ITEMS | -- |
| B:knowledge:consistency | knowledge | consistency | coherent understanding | 0 | NO_ITEMS | -- |
| B:wisdom:necessity | wisdom | necessity | essential discernment | 0 | NO_ITEMS | Guidance P2 and examples provide discernment framework |
| B:wisdom:sufficiency | wisdom | sufficiency | adequate judgment | 0 | NO_ITEMS | Trade-offs adequately framed |
| B:wisdom:completeness | wisdom | completeness | holistic insight | 0 | NO_ITEMS | -- |
| B:wisdom:consistency | wisdom | consistency | principled reasoning | 0 | NO_ITEMS | Reasoning is principled throughout |

### Warranted Items
| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| B-001 | B:data:necessity | Normalization | Datasheet | Datasheet | Normalize DIRECTIVE section reference: Datasheet says "Section 4" for hierarchy in Procedure Step 1, but Specification REQ-COH-01 references "Section 4" while Procedure Step 1.4 references "Section 5 structural constraints"; clarify which DIRECTIVE section governs hierarchy | Under essential-fact lens, the DIRECTIVE section number referenced for hierarchy consistency differs between Datasheet (implied Section 4 via coherence table) and Procedure Step 1.4 ("Section 5 structural constraints"); the correct section should be consistent across documents | Datasheet.md; Procedure.md | Datasheet > Conditions > IN-scope coherence domain table; Procedure > Step 1 item 4 | -- | Specification.md | TBD |
| B-002 | B:data:completeness | MissingSlot | Datasheet | Datasheet | Add details for invariants K-INVENT-1, K-CONFLICT-1, K-WRITE-1 in the guardrail enforcement mechanisms table or clarify their relevance; they appear in the Attributes table as "Invariants Relevant" but are not mapped to specific guardrails | Under comprehensive-record lens, the Datasheet lists 10 invariants as relevant in the Attributes table but the Guardrail Enforcement Mechanisms table only maps K-AUTH-1 and K-SEAL-1 to specific guardrails; K-INVENT-1, K-CONFLICT-1, K-WRITE-1 are listed as relevant but not explained | Datasheet.md | Attributes table; Construction > Guardrail enforcement mechanisms table | -- | Datasheet.md | TBD |

## Matrix C -- Formulation (3x4)

### Lens Coverage (required)
| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| C:normative:necessity | normative | necessity | obligatory compliance foundation | 1 | HAS_ITEMS | Missing periodicity requirement |
| C:normative:sufficiency | normative | sufficiency | warranted regulatory competence | 0 | NO_ITEMS | Specification demonstrates regulatory competence |
| C:normative:completeness | normative | completeness | exhaustive regulatory coverage | 0 | NO_ITEMS | All scope items covered |
| C:normative:consistency | normative | consistency | harmonized regulatory integrity | 0 | NO_ITEMS | Requirements are internally consistent |
| C:operative:necessity | operative | necessity | core operational requirement | 1 | HAS_ITEMS | Missing trigger/frequency for procedure |
| C:operative:sufficiency | operative | sufficiency | competent operational practice | 0 | NO_ITEMS | Steps are competently specified |
| C:operative:completeness | operative | completeness | end-to-end process coverage | 0 | NO_ITEMS | Phase 1-3 covers full scope |
| C:operative:consistency | operative | consistency | disciplined operational uniformity | 0 | NO_ITEMS | Steps follow uniform structure |
| C:evaluative:necessity | evaluative | necessity | fundamental value criterion | 0 | NO_ITEMS | Guidance establishes value criteria |
| C:evaluative:sufficiency | evaluative | sufficiency | substantiated merit appraisal | 0 | NO_ITEMS | -- |
| C:evaluative:completeness | evaluative | completeness | comprehensive worth assessment | 0 | NO_ITEMS | -- |
| C:evaluative:consistency | evaluative | consistency | principled evaluation consistency | 0 | NO_ITEMS | -- |

### Warranted Items
| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| C-001 | C:normative:necessity | MissingSlot | Specification | Specification | Add a requirement for coherence review periodicity or triggering events (e.g., "coherence review SHALL be performed after any governance document update") | Under obligatory-compliance-foundation lens, the Specification defines what to check but not when; coherence review without a trigger condition is a compliance obligation that cannot be scheduled or enforced | Specification.md | Requirements section (after REQ-TRACE-01) | -- | Specification.md | TBD |
| C-002 | C:operative:necessity | VerificationGap | Procedure | Procedure | Add explicit trigger conditions to the Procedure (e.g., "Execute this procedure when: (a) any governance document is modified, (b) a new decomposition revision is approved, (c) periodic review interval elapsed") | Under core-operational-requirement lens, the Procedure Purpose says "whenever governance documents are updated or as part of periodic governance review" but this is guidance-level language, not a formal prerequisite or trigger; the procedure has no required invocation condition | Procedure.md | Purpose section; Prerequisites table | -- | Specification.md | TBD |

## Matrix F -- Requirements (3x4)

### Lens Coverage (required)
| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| F:normative:necessity | normative | necessity | mandatory governance prerequisite | 1 | HAS_ITEMS | Missing DIRECTIVE section reference in Specification |
| F:normative:sufficiency | normative | sufficiency | justified regulatory assurance | 0 | NO_ITEMS | Requirements are justified with sources |
| F:normative:completeness | normative | completeness | exhaustive governance completeness | 1 | HAS_ITEMS | Agent instruction constraints not specified |
| F:normative:consistency | normative | consistency | unified conformance standard | 0 | NO_ITEMS | Requirements use consistent format |
| F:operative:necessity | operative | necessity | indispensable process foundation | 0 | NO_ITEMS | Process steps are well-founded |
| F:operative:sufficiency | operative | sufficiency | substantiated execution capability | 0 | NO_ITEMS | Steps are executable |
| F:operative:completeness | operative | completeness | thorough operational completeness | 0 | NO_ITEMS | -- |
| F:operative:consistency | operative | consistency | dependable process coherence | 0 | NO_ITEMS | -- |
| F:evaluative:necessity | evaluative | necessity | indispensable assessment criterion | 1 | HAS_ITEMS | No acceptance criteria for ASSUMPTION tags |
| F:evaluative:sufficiency | evaluative | sufficiency | substantiated value justification | 0 | NO_ITEMS | -- |
| F:evaluative:completeness | evaluative | completeness | exhaustive significance assessment | 0 | NO_ITEMS | -- |
| F:evaluative:consistency | evaluative | consistency | disciplined assessment integrity | 0 | NO_ITEMS | -- |

### Warranted Items
| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| F-001 | F:normative:necessity | Normalization | Specification | Specification | Normalize the DIRECTIVE section reference in REQ-COH-01: currently says "DIRECTIVE Section 4" but Procedure Step 1.4 says "Section 5 structural constraints"; confirm which section is authoritative and use consistently | Under mandatory-governance-prerequisite lens, a prerequisite reference that is ambiguous undermines the mandatory nature of the check; the DIRECTIVE section number must be consistent | Specification.md; Procedure.md | Specification > REQ-COH-01 verification; Procedure > Step 1 item 4 | -- | Specification.md | TBD |
| F-002 | F:normative:completeness | MissingSlot | Specification | Specification | Add a requirement addressing how agent instruction files enforce the guardrails (Guidance P3 lists "agent instruction constraints" as an enforcement layer but no REQ-* covers verification of this layer) | Under exhaustive-governance-completeness lens, Guidance P3 identifies four enforcement layers; the Specification has requirements for documentation (REQ-GR-01) and invariant backing (REQ-GR-02, REQ-GR-03) but no requirement verifying agent instruction constraints as an enforcement layer | Specification.md; Guidance.md | Specification > Requirements section; Guidance > P3: Guardrails require multiple enforcement layers | -- | Specification.md | TBD |
| F-003 | F:evaluative:necessity | TBD_Question | Guidance | Guidance | Determine whether the ASSUMPTION tags in Guidance (P3, C1, C2, T1, T2) require formal validation or human confirmation before the deliverable can advance beyond WORKING_ITEMS | Under indispensable-assessment-criterion lens, Guidance contains five explicit ASSUMPTION tags marking inferred content; there is no stated criterion for whether these must be validated, accepted, or left as-is | Guidance.md | P3, C1, C2, T1, T2 (all marked **ASSUMPTION**) | -- | TBD | TBD |

## Matrix D -- Objectives (3x4)

### Lens Coverage (required)
| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| D:normative:guiding | normative | guiding | settled directive authority | 0 | NO_ITEMS | Directive authority is well-settled in docs |
| D:normative:applying | normative | applying | enforced compliance practice | 1 | HAS_ITEMS | Enforcement depth for SOW-040/042 |
| D:normative:judging | normative | judging | conclusive conformance ruling | 0 | NO_ITEMS | PASS/FAIL criteria are conclusive |
| D:normative:reviewing | normative | reviewing | systematic conformance verification | 0 | NO_ITEMS | Procedure provides systematic verification |
| D:operative:guiding | operative | guiding | established operational guidance | 0 | NO_ITEMS | Guidance principles are well-established |
| D:operative:applying | operative | applying | confirmed operational execution | 0 | NO_ITEMS | Steps are executable |
| D:operative:judging | operative | judging | definitive process assessment | 0 | NO_ITEMS | -- |
| D:operative:reviewing | operative | reviewing | systematic workflow verification | 1 | HAS_ITEMS | Missing re-run verification step |
| D:evaluative:guiding | evaluative | guiding | settled value orientation | 0 | NO_ITEMS | -- |
| D:evaluative:applying | evaluative | applying | confirmed merit enactment | 0 | NO_ITEMS | -- |
| D:evaluative:judging | evaluative | judging | conclusive significance ruling | 0 | NO_ITEMS | -- |
| D:evaluative:reviewing | evaluative | reviewing | systematic evaluation integrity | 0 | NO_ITEMS | -- |

### Warranted Items
| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| D-001 | D:normative:applying | RationaleGap | Guidance | Guidance | Add rationale for why SOW-040 and SOW-042 are considered adequately enforced despite having only a single enforcement layer (DIRECTIVE documentation), when other guardrails have 2-4 layers | Under enforced-compliance-practice lens, Guidance C2 shows enforcement depth varies but does not explain the acceptable minimum; a reader cannot determine whether single-layer enforcement is a conscious design choice or a gap to be addressed | Guidance.md | C2: Guardrail enforcement depth varies by boundary | -- | Guidance.md | TBD |
| D-002 | D:operative:reviewing | VerificationGap | Procedure | Procedure | Add a final verification step that confirms all remediation re-runs have passed (the Remediation guidance says "re-run the failed step" but there is no aggregate re-verification step) | Under systematic-workflow-verification lens, the Procedure remediation guidance (after the Verification table) instructs re-running failed steps but does not require a final aggregate confirmation that all steps now pass after remediation | Procedure.md | Verification > Remediation guidance | -- | Procedure.md | TBD |

## Matrix X -- Verification (4x4)

### Lens Coverage (required)
| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| X:guiding:necessity | guiding | necessity | foundational governance imperative | 0 | NO_ITEMS | Governance imperatives are well-founded |
| X:guiding:sufficiency | guiding | sufficiency | justified governance direction | 0 | NO_ITEMS | -- |
| X:guiding:completeness | guiding | completeness | exhaustive governance scope | 1 | HAS_ITEMS | Excluded scope items not cross-referenced |
| X:guiding:consistency | guiding | consistency | principled governance coherence | 0 | NO_ITEMS | -- |
| X:applying:necessity | applying | necessity | mandatory enforcement prerequisite | 0 | NO_ITEMS | Prerequisites are stated |
| X:applying:sufficiency | applying | sufficiency | verified implementation adequacy | 1 | HAS_ITEMS | Verification approach for some REQs is "manual" |
| X:applying:completeness | applying | completeness | comprehensive implementation scope | 0 | NO_ITEMS | -- |
| X:applying:consistency | applying | consistency | disciplined implementation integrity | 0 | NO_ITEMS | -- |
| X:judging:necessity | judging | necessity | critical compliance determination | 0 | NO_ITEMS | Compliance criteria are defined |
| X:judging:sufficiency | judging | sufficiency | justified adjudication competence | 0 | NO_ITEMS | -- |
| X:judging:completeness | judging | completeness | thorough adjudication coverage | 0 | NO_ITEMS | -- |
| X:judging:consistency | judging | consistency | principled adjudication coherence | 0 | NO_ITEMS | -- |
| X:reviewing:necessity | reviewing | necessity | mandatory verification foundation | 1 | HAS_ITEMS | No version tracking for governance docs |
| X:reviewing:sufficiency | reviewing | sufficiency | justified audit sufficiency | 0 | NO_ITEMS | -- |
| X:reviewing:completeness | reviewing | completeness | comprehensive audit coverage | 0 | NO_ITEMS | -- |
| X:reviewing:consistency | reviewing | consistency | principled audit coherence | 0 | NO_ITEMS | -- |

### Warranted Items
| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| X-001 | X:guiding:completeness | MissingSlot | Specification | Specification | Add cross-references to excluded deliverables (DEL-06-01 through DEL-06-04, DEL-03-04, DEL-03-06) in a way that confirms scope boundaries are understood bidirectionally, or note this as a future coherence check | Under exhaustive-governance-scope lens, the Specification Excluded section lists five other deliverables that cover adjacent concerns but does not confirm that those deliverables acknowledge the boundary from their side; this is a scope-completeness gap | Specification.md | Scope > Excluded | -- | Specification.md | TBD |
| X-002 | X:applying:sufficiency | WeakStatement | Specification | Specification | Strengthen verification approach for REQ-COH-02: replace "spot-check" with a defined minimum verification scope (e.g., enumerated term list or percentage coverage) | Under verified-implementation-adequacy lens, "spot-check" in the Verification table for REQ-COH-02 does not provide a sufficient basis for determining whether implementation is adequate; a verifier cannot know when the check is complete | Specification.md | Verification table, REQ-COH-02 row | -- | Specification.md | TBD |
| X-003 | X:reviewing:necessity | VerificationGap | Multi | Datasheet | Add governance document version identifiers (e.g., git commit hash or revision date) to the Datasheet or Procedure prerequisites so that verification results can be traced to specific document versions | Under mandatory-verification-foundation lens, none of the documents record which version of the five governance documents was reviewed; verification results without version provenance cannot be audited or compared across reviews | Datasheet.md; Procedure.md | Datasheet > Construction > Governance document inventory; Procedure > Prerequisites | -- | Datasheet.md | TBD |

## Matrix E -- Evaluation (3x4)

### Lens Coverage (required)
| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| E:normative:necessity | normative | necessity | sovereign compliance mandate | 0 | NO_ITEMS | Compliance mandate is sovereign and well-grounded |
| E:normative:sufficiency | normative | sufficiency | warranted compliance sufficiency | 0 | NO_ITEMS | -- |
| E:normative:completeness | normative | completeness | universal regulatory completeness | 1 | HAS_ITEMS | Invariant relevance not fully traced |
| E:normative:consistency | normative | consistency | harmonized governance integrity | 0 | NO_ITEMS | Documents are internally harmonized |
| E:operative:necessity | operative | necessity | verified operational foundation | 0 | NO_ITEMS | Operational foundations are verified |
| E:operative:sufficiency | operative | sufficiency | confirmed operational adequacy | 0 | NO_ITEMS | -- |
| E:operative:completeness | operative | completeness | exhaustive operational coverage | 1 | HAS_ITEMS | Procedure missing execution actor guidance |
| E:operative:consistency | operative | consistency | dependable operational coherence | 0 | NO_ITEMS | -- |
| E:evaluative:necessity | evaluative | necessity | foundational evaluative imperative | 0 | NO_ITEMS | -- |
| E:evaluative:sufficiency | evaluative | sufficiency | warranted evaluative sufficiency | 0 | NO_ITEMS | -- |
| E:evaluative:completeness | evaluative | completeness | comprehensive evaluative completeness | 0 | NO_ITEMS | -- |
| E:evaluative:consistency | evaluative | consistency | unified evaluative integrity | 0 | NO_ITEMS | -- |

### Warranted Items
| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| E-001 | E:normative:completeness | RationaleGap | Multi | Guidance | Add a rationale note explaining how invariants K-BIND-1, K-STATUS-1, K-DEP-1, K-HIER-1, K-INVENT-1, K-CONFLICT-1, K-WRITE-1 relate to the governance coherence mission (Datasheet lists them as relevant but no requirement or guidance explains their role) | Under universal-regulatory-completeness lens, the Datasheet Attributes table lists 10 invariants as relevant but the Specification only references K-AUTH-1, K-SEAL-1, K-HIER-1, K-STATUS-1, and K-DEP-1 in requirements; the remaining invariants (K-BIND-1, K-INVENT-1, K-CONFLICT-1, K-WRITE-1) are listed but untraced | Datasheet.md; Specification.md | Datasheet > Attributes > Invariants Relevant; Specification > Requirements section (entire) | -- | Guidance.md | TBD |
| E-002 | E:operative:completeness | VerificationGap | Procedure | Procedure | Add guidance on who should execute the procedure (human only, agent-assisted, or either) and what authority level is required to sign off on results | Under exhaustive-operational-coverage lens, the Procedure defines steps and verification but does not specify who is authorized to execute the review or sign off on PASS/FAIL results; the Records table has "TBD" for execution actor | Procedure.md | Prerequisites; Records table ("Execution date and actor") | -- | Procedure.md | TBD |
