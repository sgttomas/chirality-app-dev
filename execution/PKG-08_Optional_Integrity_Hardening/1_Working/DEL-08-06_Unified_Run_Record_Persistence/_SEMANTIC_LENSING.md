# Semantic Lensing Register: DEL-08-06 Unified Pipeline Run Record Persistence

**Generated:** 2026-02-21
**Deliverable Folder:** /Users/ryan/ai-env/projects/chirality-app-dev/execution/PKG-08_Optional_Integrity_Hardening/1_Working/DEL-08-06_Unified_Run_Record_Persistence/
**Warnings:** None

**Inputs Read:**
- _CONTEXT.md — DEL-08-06 identity, PKG-08, DATA_MODEL_CHANGE, ContextEnvelope L
- _STATUS.md — Current State: SEMANTIC_READY (2026-02-21)
- _SEMANTIC.md — Matrices A, B, C, F, D, X, E parsed (92 cells total)
- Datasheet.md — DEL-08-06 attributes, conditions, construction, references
- Specification.md — REQ-01 through REQ-07, verification criteria, documentation artifacts
- Guidance.md — Purpose, principles P1-P5, considerations C1-C5, trade-offs, examples, conflict table
- Procedure.md — Phases 1-3, prerequisites, verification, records
- _REFERENCES.md — Decomposition link, package references, no deliverable-specific references yet

**Purpose:** Apply CHIRALITY_FRAMEWORK matrix cells as lenses over the production documents, capturing warranted enrichment inputs for a later enrichment pass.

## Summary

- Total warranted items: 23
- By document:
  - Datasheet: 5
  - Specification: 8
  - Guidance: 4
  - Procedure: 3
  - Multi: 3
- By matrix:
  - A: 3  B: 3  C: 2  F: 3  D: 3  X: 5  E: 4
- By type:
  - Conflict: 3
  - VerificationGap: 4
  - MissingSlot: 5
  - WeakStatement: 3
  - RationaleGap: 2
  - Normalization: 3
  - TBD_Question: 3
  - MatrixError: 0
- Notable conflicts: 3
- Matrix parse errors: 0

---

## Matrix A — Orientation (3x4) — Canonical

### Lens Coverage
| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| A:normative:guiding | normative | guiding | prescriptive direction | 1 | HAS_ITEMS | Storage location TBD weakens prescriptive direction |
| A:normative:applying | normative | applying | mandatory practice | 0 | NO_ITEMS | REQ-01 through REQ-07 provide clear mandatory practice; well covered |
| A:normative:judging | normative | judging | compliance determination | 1 | HAS_ITEMS | Compliance with K-SNAP-1 underspecified for append-only model |
| A:normative:reviewing | normative | reviewing | regulatory audit | 0 | NO_ITEMS | Audit trail rationale well articulated across Guidance and Datasheet |
| A:operative:guiding | operative | guiding | procedural direction | 0 | NO_ITEMS | Procedure provides clear phased direction |
| A:operative:applying | operative | applying | practical execution | 1 | HAS_ITEMS | Concurrent write handling deferred |
| A:operative:judging | operative | judging | performance assessment | 0 | NO_ITEMS | Verification table in Procedure covers assessment adequately |
| A:operative:reviewing | operative | reviewing | process audit | 0 | NO_ITEMS | Regression and conformance tests cover process audit |
| A:evaluative:guiding | evaluative | guiding | value orientation | 0 | NO_ITEMS | Purpose statement in Guidance clearly articulates value |
| A:evaluative:applying | evaluative | applying | merit application | 0 | NO_ITEMS | Trade-offs table in Guidance addresses merit considerations |
| A:evaluative:judging | evaluative | judging | worth determination | 0 | NO_ITEMS | Verification criteria in Specification address worth determination |
| A:evaluative:reviewing | evaluative | reviewing | quality appraisal | 0 | NO_ITEMS | Conformance tests (Step 3.4) address quality appraisal |

### Warranted Items
| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A-001 | A:normative:guiding | WeakStatement | Specification | Specification | Strengthen REQ-02 beyond listing options — add decision criteria or acceptance gate for when the storage location decision must be finalized | REQ-02 presents three options and an assumption but no normative gate for resolving the TBD; prescriptive direction is incomplete until the decision mechanism is specified | Specification.md | REQ-02: Storage Location | — | Human ruling on CON-01 | TBD |
| A-002 | A:normative:judging | VerificationGap | Specification | Specification | Add verification criteria for how append-only immutability (REQ-03) is assessed when Option A is chosen — K-SNAP-1 is a snapshot invariant; clarify how it maps to append-only semantics | REQ-03 cites K-SNAP-1 but K-SNAP-1 governs snapshot immutability, not append-only file semantics; the compliance determination path is ambiguous | Specification.md | REQ-03: Immutability Semantics; Verification table REQ-03 row | — | K-SNAP-1 (CONTRACT) | TBD |
| A-003 | A:operative:applying | TBD_Question | Procedure | Procedure | Resolve how concurrent writes to the run record file are handled when DEL-08-05 (Lock Mechanism) is not available — add a fallback strategy or explicit prerequisite | Step 2.1 says concurrent writes are "TBD — may depend on DEL-08-05 lock mechanism" but no fallback is provided if DEL-08-05 is not in scope | Procedure.md | Step 2.1 — Implement Run Record Writer | — | DEL-08-05 scope decision | TBD |

---

## Matrix B — Conceptualization (4x4) — Canonical

### Lens Coverage
| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| B:data:necessity | data | necessity | essential fact | 1 | HAS_ITEMS | Responsible Party is TBD |
| B:data:sufficiency | data | sufficiency | adequate evidence | 0 | NO_ITEMS | Attributes table provides adequate evidence for schema fields |
| B:data:completeness | data | completeness | comprehensive record | 1 | HAS_ITEMS | Missing enumeration of all Type 2 agents in scope |
| B:data:consistency | data | consistency | reliable measurement | 0 | NO_ITEMS | Schema field definitions are consistent across documents |
| B:information:necessity | information | necessity | essential signal | 0 | NO_ITEMS | The signal chain from run record to staleness detection is documented |
| B:information:sufficiency | information | sufficiency | adequate context | 0 | NO_ITEMS | Guidance provides adequate context for design decisions |
| B:information:completeness | information | completeness | comprehensive account | 1 | HAS_ITEMS | No enumeration of RunStatus transitions or lifecycle |
| B:information:consistency | information | consistency | coherent message | 0 | NO_ITEMS | Cross-document messaging is coherent |
| B:knowledge:necessity | knowledge | necessity | fundamental understanding | 0 | NO_ITEMS | Guidance Purpose section provides fundamental understanding |
| B:knowledge:sufficiency | knowledge | sufficiency | competent expertise | 0 | NO_ITEMS | Schema design rationale is adequately explained |
| B:knowledge:completeness | knowledge | completeness | thorough mastery | 0 | NO_ITEMS | Documents demonstrate thorough domain understanding |
| B:knowledge:consistency | knowledge | consistency | coherent understanding | 0 | NO_ITEMS | Understanding is coherent across documents |
| B:wisdom:necessity | wisdom | necessity | essential discernment | 0 | NO_ITEMS | Trade-offs table exercises discernment |
| B:wisdom:sufficiency | wisdom | sufficiency | adequate judgment | 0 | NO_ITEMS | Judgment calls are explicitly labeled as PROPOSAL/ASSUMPTION |
| B:wisdom:completeness | wisdom | completeness | holistic insight | 0 | NO_ITEMS | Cross-deliverable view (DEL-08-07 dependency) shows holistic insight |
| B:wisdom:consistency | wisdom | consistency | principled reasoning | 0 | NO_ITEMS | Reasoning consistently grounded in CONTRACT invariants |

### Warranted Items
| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| B-001 | B:data:necessity | MissingSlot | Datasheet | Datasheet | Add Responsible Party value (currently TBD) or document TBD rationale | Responsible Party is an essential fact for accountability; listed as TBD with no resolution path | Datasheet.md | Identification table, "Responsible Party" row | — | Human assignment | TBD |
| B-002 | B:data:completeness | MissingSlot | Specification | Datasheet | Add a comprehensive enumeration of all Type 2 agents in scope for run record integration (Guidance C4 lists four but says "at minimum") | The complete set of agents that will emit run records is not definitively listed; "at minimum" leaves the record incomplete | Specification.md; Guidance.md | REQ-04: Agent Protocol Integration; C4: Agent Protocol Integration Scope | — | Current agent inventory | TBD |
| B-003 | B:information:completeness | MissingSlot | Specification | Specification | Define the RunStatus enum lifecycle — document valid transitions (e.g., can a run go directly to SKIPPED? what triggers PARTIAL vs. FAILED?) | RunStatus enum values are listed (SUCCESS, PARTIAL, FAILED, SKIPPED) but transition semantics and boundary conditions are not specified | Specification.md | REQ-01: Run Record Schema Definition, RunStatus field | — | Agent protocol design | TBD |

---

## Matrix C — Formulation (3x4)

### Lens Coverage
| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| C:normative:necessity | normative | necessity | Enforceable Obligation | 0 | NO_ITEMS | Core obligations (REQ-01 through REQ-07) well-defined |
| C:normative:sufficiency | normative | sufficiency | Regulatory Substantiation | 1 | HAS_ITEMS | SHA computation method unsubstantiated |
| C:normative:completeness | normative | completeness | Exhaustive Regulatory Coverage | 0 | NO_ITEMS | Requirements cover the needed regulatory surface |
| C:normative:consistency | normative | consistency | Standardized Compliance | 1 | HAS_ITEMS | Terminology inconsistency in file naming |
| C:operative:necessity | operative | necessity | Critical Process Enabler | 0 | NO_ITEMS | Procedure prerequisites identify critical enablers |
| C:operative:sufficiency | operative | sufficiency | Operational Readiness | 0 | NO_ITEMS | Prerequisite table in Procedure assesses readiness |
| C:operative:completeness | operative | completeness | End-to-End Process Capture | 0 | NO_ITEMS | Procedure phases 1-3 capture end-to-end process |
| C:operative:consistency | operative | consistency | Reproducible Execution | 0 | NO_ITEMS | Procedure steps are sequenced and reproducible |
| C:evaluative:necessity | evaluative | necessity | Intrinsic Value Foundation | 0 | NO_ITEMS | Value proposition clearly stated in Guidance Purpose |
| C:evaluative:sufficiency | evaluative | sufficiency | Defensible Merit | 0 | NO_ITEMS | Trade-offs and conflict table provide defensible merit basis |
| C:evaluative:completeness | evaluative | completeness | Holistic Value Accounting | 0 | NO_ITEMS | Cross-deliverable value chain (DEL-08-07) accounted for |
| C:evaluative:consistency | evaluative | consistency | Principled Value Alignment | 0 | NO_ITEMS | Values aligned with CONTRACT invariants consistently |

### Warranted Items
| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| C-001 | C:normative:sufficiency | TBD_Question | Specification | Specification | Resolve CON-03 (SHA computation method) — the substantiation of REQ-05 depends on knowing whether git HEAD, per-file hash, or composite hash is used; without this, verification criteria for REQ-05 cannot be fully specified | REQ-05 says "SHOULD include" baseline SHA but the specific method is TBD; the verification approach says "hash corresponds to input state" without defining what "corresponds" means for each method | Specification.md | REQ-05: Baseline SHA Tracking; Verification table REQ-05 row | K-VAL-1 implies git SHA; K-GHOST-1 implies per-file hash | Design review | TBD |
| C-002 | C:normative:consistency | Normalization | Multi | Guidance | Standardize the proposed run record filename across documents — Datasheet says "TBD (unified run record schema)"; Specification REQ-02 says "`_RUN_HISTORY.md` or `RunRecords.csv`"; Guidance C1 says "`_RUN_HISTORY.md`" or "`RunRecords.csv`" | Three different phrasings for the storage artifact name appear across documents; while all are labeled TBD/options, a consistent placeholder name would reduce drift | Datasheet.md; Specification.md; Guidance.md | Attributes table "Schema name"; REQ-02; C1 | — | Storage location decision (CON-01/CON-02) | TBD |

---

## Matrix F — Requirements (3x4)

### Lens Coverage
| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| F:normative:necessity | normative | necessity | Mandated Conformance Basis | 1 | HAS_ITEMS | Scope prerequisite gating underspecified |
| F:normative:sufficiency | normative | sufficiency | Prescribed Compliance Threshold | 0 | NO_ITEMS | Verification table provides compliance thresholds |
| F:normative:completeness | normative | completeness | Total Regulatory Inventory | 0 | NO_ITEMS | Standards table in Specification provides regulatory inventory |
| F:normative:consistency | normative | consistency | Harmonized Regulatory Logic | 1 | HAS_ITEMS | MUST vs SHOULD inconsistency for baseline SHA |
| F:operative:necessity | operative | necessity | Essential Execution Prerequisite | 1 | HAS_ITEMS | Prerequisite status tracking gap |
| F:operative:sufficiency | operative | sufficiency | Demonstrated Process Competence | 0 | NO_ITEMS | Procedure steps demonstrate adequate process competence |
| F:operative:completeness | operative | completeness | Exhaustive Workflow Record | 0 | NO_ITEMS | Procedure Records table tracks workflow outputs |
| F:operative:consistency | operative | consistency | Systematic Operational Coherence | 0 | NO_ITEMS | Procedure phases are systematically coherent |
| F:evaluative:necessity | evaluative | necessity | Fundamental Worth Criterion | 0 | NO_ITEMS | DEL-08-07 dependency establishes fundamental worth |
| F:evaluative:sufficiency | evaluative | sufficiency | Competent Value Warrant | 0 | NO_ITEMS | Guidance trade-offs provide competent value warrant |
| F:evaluative:completeness | evaluative | completeness | Exhaustive Merit Accounting | 0 | NO_ITEMS | Documents account for merit comprehensively |
| F:evaluative:consistency | evaluative | consistency | Unified Quality Standard | 0 | NO_ITEMS | Quality standards consistent across documents |

### Warranted Items
| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| F-001 | F:normative:necessity | WeakStatement | Specification | Specification | Strengthen scope prerequisite language — add a SHALL-level gate that blocks Phase 2/3 execution until OI-037 is resolved to IN, rather than relying on the Datasheet condition and Guidance C5 alone | The conformance basis for starting implementation depends on SOW-037 being flipped to IN; the Specification mentions scope exclusions but does not contain a SHALL-level prerequisite gate in the requirements themselves | Specification.md; Datasheet.md | Excluded section ("no UI scope item"); Conditions table "Scope prerequisite"; Guidance C5 | — | OI-037 resolution | TBD |
| F-002 | F:normative:consistency | WeakStatement | Specification | Specification | Harmonize REQ-05 requirement level — InputContextSHA is SHOULD in REQ-01 field table but is architecturally critical per Guidance P5; consider elevating to MUST or documenting why SHOULD is appropriate | Guidance P5 calls baseline SHA "the most architecturally significant field" and DEL-08-07 depends on it, yet REQ-01 marks InputContextSHA as SHOULD (not MUST); this creates tension between stated importance and requirement strength | Specification.md; Guidance.md | REQ-01 field table "InputContextSHA" row; REQ-05; P5: Baseline SHA Is the Bridge to Staleness | — | Specification (normative authority) | TBD |
| F-003 | F:operative:necessity | MissingSlot | Procedure | Procedure | Add a prerequisite check step or gating mechanism at the start of Phase 2 that verifies all Phase 1 decisions (CON-01, CON-02, CON-03) have been resolved before implementation begins | Prerequisites table lists status as TBD for several items but no procedural step enforces checking these gates before proceeding to Phase 2 | Procedure.md | Prerequisites table; Phase 2 header | — | Procedure (operational authority) | TBD |

---

## Matrix D — Objectives (3x4)

### Lens Coverage
| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| D:normative:guiding | normative | guiding | Binding Governance Anchor | 1 | HAS_ITEMS | Missing explicit governance anchor for schema evolution |
| D:normative:applying | normative | applying | Enforced Compliance Benchmark | 0 | NO_ITEMS | REQ-01 through REQ-07 serve as compliance benchmarks |
| D:normative:judging | normative | judging | Definitive Conformance Ruling | 0 | NO_ITEMS | Verification table provides conformance ruling framework |
| D:normative:reviewing | normative | reviewing | Formal Conformance Inspection | 0 | NO_ITEMS | Phase 3 testing steps address conformance inspection |
| D:operative:guiding | operative | guiding | Resolved Process Guidance | 1 | HAS_ITEMS | Unresolved process guidance for schema evolution |
| D:operative:applying | operative | applying | Established Operational Capacity | 0 | NO_ITEMS | Implementation steps establish operational capacity |
| D:operative:judging | operative | judging | Documented Performance Verdict | 0 | NO_ITEMS | Verification table documents performance verdict criteria |
| D:operative:reviewing | operative | reviewing | Rigorous Workflow Inspection | 0 | NO_ITEMS | Test phases (3.1-3.4) provide rigorous inspection |
| D:evaluative:guiding | evaluative | guiding | Established Quality Purpose | 0 | NO_ITEMS | Guidance Purpose section establishes quality purpose |
| D:evaluative:applying | evaluative | applying | Warranted Quality Practice | 0 | NO_ITEMS | Examples in Guidance demonstrate warranted practice |
| D:evaluative:judging | evaluative | judging | Definitive Quality Judgment | 1 | HAS_ITEMS | No quality criteria for run record content accuracy |
| D:evaluative:reviewing | evaluative | reviewing | Resolved Quality Appraisal | 0 | NO_ITEMS | Conformance tests provide quality appraisal mechanism |

### Warranted Items
| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| D-001 | D:normative:guiding | RationaleGap | Guidance | Guidance | Add guidance on schema evolution governance — when SchemaVersion increments, what is the migration path for existing records? How are old-version records handled? | SchemaVersion field is specified (REQ-01) and versioning rationale is in Guidance C2, but no governance anchor for how version transitions are managed or what triggers a version increment | Specification.md; Guidance.md | REQ-01 SchemaVersion field; C2: Schema Versioning | — | Guidance (directional authority) | TBD |
| D-002 | D:operative:guiding | MissingSlot | Procedure | Procedure | Add an operational step or section for schema migration/evolution — what happens when the schema changes and existing run records use an older version | Procedure covers initial implementation (Phases 1-3) but provides no process guidance for ongoing schema evolution or record migration | Procedure.md | entire document scanned | — | Procedure (operational authority) | TBD |
| D-003 | D:evaluative:judging | VerificationGap | Specification | Specification | Add verification criteria for run record content accuracy — how to verify that the metadata in a run record (agent name, input files, output files, status transitions) actually matches what happened during the run | REQ-04 verification says "run record content matches actual execution metadata" but no criteria define what "matches" means or how discrepancies are detected | Specification.md | Verification table REQ-04 row | — | Specification (normative authority) | TBD |

---

## Matrix X — Verification (4x4)

### Lens Coverage
| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| X:guiding:necessity | guiding | necessity | Foundational Governance Driver | 0 | NO_ITEMS | Governance drivers adequately established |
| X:guiding:sufficiency | guiding | sufficiency | Guided Assurance Basis | 1 | HAS_ITEMS | Assurance basis for SHA accuracy undefined |
| X:guiding:completeness | guiding | completeness | Comprehensive Steering Scope | 0 | NO_ITEMS | Steering scope covers the needed areas |
| X:guiding:consistency | guiding | consistency | Stable Governance Continuity | 0 | NO_ITEMS | Governance is consistent across documents |
| X:applying:necessity | applying | necessity | Actionable Compliance Enabler | 1 | HAS_ITEMS | Error handling for partial writes not actionable |
| X:applying:sufficiency | applying | sufficiency | Confirmed Practical Fitness | 0 | NO_ITEMS | Practical fitness confirmed through test phases |
| X:applying:completeness | applying | completeness | Exhaustive Practice Accounting | 1 | HAS_ITEMS | Missing accounting for edge case: agent crash mid-write |
| X:applying:consistency | applying | consistency | Dependable Practice Conformance | 0 | NO_ITEMS | Practice conformance is dependable per procedure |
| X:judging:necessity | judging | necessity | Decisive Adjudicative Authority | 0 | NO_ITEMS | Verification table provides adjudicative authority |
| X:judging:sufficiency | judging | sufficiency | Defensible Ruling Basis | 1 | HAS_ITEMS | REQ-02 verification criteria vague |
| X:judging:completeness | judging | completeness | Exhaustive Judgment Coverage | 0 | NO_ITEMS | Judgment coverage across REQ-01 through REQ-07 is exhaustive |
| X:judging:consistency | judging | consistency | Consistent Ruling Discipline | 0 | NO_ITEMS | Verification approaches are consistently structured |
| X:reviewing:necessity | reviewing | necessity | Mandated Review Imperative | 1 | HAS_ITEMS | No review step for run record content post-write |
| X:reviewing:sufficiency | reviewing | sufficiency | Thorough Audit Substantiation | 0 | NO_ITEMS | Phase 3 tests substantiate audit needs |
| X:reviewing:completeness | reviewing | completeness | Exhaustive Audit Scope | 0 | NO_ITEMS | Audit scope covers schema, integration, regression, conformance |
| X:reviewing:consistency | reviewing | consistency | Reliable Audit Discipline | 0 | NO_ITEMS | Test structure is reliable and disciplined |

### Warranted Items
| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| X-001 | X:guiding:sufficiency | VerificationGap | Specification | Specification | Add verification criteria for SHA accuracy — how to confirm that the InputContextSHA actually represents the input state at run start (not stale or from a different commit) | REQ-05 verification says "hash corresponds to input state at run start (verified against git)" but does not specify how this verification is performed or what constitutes a match | Specification.md | Verification table REQ-05 row | — | Design review for SHA method | TBD |
| X-002 | X:applying:necessity | RationaleGap | Guidance | Guidance | Add rationale for error handling strategy — explain why "log warning; do not fail the agent run" is the right approach and what risks it introduces (e.g., silent data loss of run records) | REQ-04 says run record failure MUST NOT fail the overall run; Procedure Step 2.1 says "log warning" but no rationale explains the risk trade-off of potentially losing run records silently | Specification.md; Procedure.md | REQ-04; Step 2.1 | — | Guidance (directional authority) | TBD |
| X-003 | X:applying:completeness | VerificationGap | Specification | Specification | Add verification scenario for agent crash or interruption mid-write — what state is the run record file left in? Is there a recovery mechanism? | Integration tests (Step 3.2) test "write failure" but not partial/corrupted writes from crashes; the exhaustive practice accounting should cover this edge case | Specification.md; Procedure.md | Verification table REQ-03 row; Step 3.2 | — | Specification (normative authority) | TBD |
| X-004 | X:judging:sufficiency | WeakStatement | Specification | Specification | Strengthen REQ-02 verification criteria — "Storage location is documented; run records are written to the chosen location; files are present after a pipeline run" is vague; add criteria for file format validation and content correctness | The ruling basis for REQ-02 compliance is weak; "files are present" does not confirm they are correctly formatted or contain valid data | Specification.md | Verification table REQ-02 row | — | Specification (normative authority) | TBD |
| X-005 | X:reviewing:necessity | MissingSlot | Procedure | Procedure | Add a post-write review/validation step in Phase 2 — after a run record is written, verify it can be parsed back and matches the expected schema | No review step exists for validating run records after they are written in the operational workflow; testing covers this but the operational procedure does not include a runtime validation check | Procedure.md | Phase 2: Implementation (entire section scanned) | — | Procedure (operational authority) | TBD |

---

## Matrix E — Evaluation (3x4)

### Lens Coverage
| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| E:normative:necessity | normative | necessity | Binding Regulatory Mandate | 1 | HAS_ITEMS | Scope item status TBD creates regulatory ambiguity |
| E:normative:sufficiency | normative | sufficiency | Verified Regulatory Fitness | 0 | NO_ITEMS | Standards table provides regulatory fitness basis |
| E:normative:completeness | normative | completeness | Exhaustive Compliance Panorama | 1 | HAS_ITEMS | K-PROV-1 provenance requirement underaddressed |
| E:normative:consistency | normative | consistency | Harmonized Compliance Standard | 1 | HAS_ITEMS | MUST/SHOULD level inconsistency for critical fields |
| E:operative:necessity | operative | necessity | Critical Operational Foundation | 0 | NO_ITEMS | Operational foundation adequately established |
| E:operative:sufficiency | operative | sufficiency | Demonstrated Operational Fitness | 0 | NO_ITEMS | Procedure demonstrates operational fitness |
| E:operative:completeness | operative | completeness | Comprehensive Process Accounting | 0 | NO_ITEMS | Process accounting is comprehensive |
| E:operative:consistency | operative | consistency | Dependable Execution Standard | 0 | NO_ITEMS | Execution standard is dependable and consistent |
| E:evaluative:necessity | evaluative | necessity | Foundational Quality Imperative | 0 | NO_ITEMS | Quality imperative grounded in audit trail need |
| E:evaluative:sufficiency | evaluative | sufficiency | Verified Merit Confidence | 0 | NO_ITEMS | Merit confidence supported by examples and trade-offs |
| E:evaluative:completeness | evaluative | completeness | Comprehensive Quality Portfolio | 1 | HAS_ITEMS | Missing quality criteria for record completeness |
| E:evaluative:consistency | evaluative | consistency | Sustained Quality Discipline | 0 | NO_ITEMS | Quality discipline sustained across documents |

### Warranted Items
| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| E-001 | E:normative:necessity | Conflict | Datasheet | Guidance | Scope Item Status in Datasheet says "TBD (scope decision pending per OI-037)" while Specification Excluded section and Guidance C5 treat this as a blocking prerequisite — clarify whether documents should be authored assuming scope is IN or whether a conditional framing should be used consistently | Datasheet records the scope status as TBD; Specification proceeds to define requirements as if scope is determined; Guidance C5 notes the prerequisite but does not resolve the tension | Datasheet.md; Specification.md; Guidance.md | Identification table "Scope Item Status"; Excluded section; C5 | Datasheet.md#Identification (TBD); Specification.md#Requirements (proceeds as if IN) | OI-037 resolution | TBD |
| E-002 | E:normative:completeness | Normalization | Specification | Specification | Add explicit traceability from REQ-01 schema fields to K-PROV-1 (provenance requirements) — the Standards table lists K-PROV-1 but no requirement directly addresses what provenance data the run record captures | K-PROV-1 is listed in the Standards table with note "run records should cite what was consumed" but no REQ explicitly maps to this; the InputFiles field partially addresses it but the mapping is implicit | Specification.md | Standards table K-PROV-1 row; REQ-01 field table | — | Specification (normative authority) | TBD |
| E-003 | E:normative:consistency | Conflict | Multi | Specification | Resolve the MUST vs. SHOULD tension for InputContextSHA across REQ-01 (SHOULD) and the architectural significance stated in Guidance P5 and the downstream dependency from DEL-08-07 | If DEL-08-07 depends on baseline SHAs in run records and P5 calls it "the most architecturally significant field," marking it SHOULD (not MUST) creates a consistency risk — downstream may fail if this field is omitted | Specification.md; Guidance.md | REQ-01 InputContextSHA row; REQ-05; P5 | Specification.md#REQ-01 (SHOULD); Guidance.md#P5 (architecturally critical) | Specification (normative authority) | TBD |
| E-004 | E:evaluative:completeness | Normalization | Multi | Guidance | Standardize terminology for the run record artifact — documents variously use "run record," "run-record," "run record entry," "run record schema," and "unified run record"; adopt one canonical term | Multiple hyphenation and phrasing variants appear across all four documents for the core concept; while meaning is clear, terminological drift could compound in downstream deliverables | Datasheet.md; Specification.md; Guidance.md; Procedure.md | entire document scanned (all four) | — | Guidance (vocabulary note) | TBD |

---

## Cross-Matrix Conflict Register

The following conflicts were identified across multiple lenses and are consolidated here for human ruling convenience:

| ConflictID | Related ItemIDs | Core Tension | Documents Involved | Ruling Needed |
|---|---|---|---|---|
| XCON-01 | F-002, E-003 | InputContextSHA is SHOULD in REQ-01 but architecturally critical per Guidance P5 and required by DEL-08-07 | Specification, Guidance | Elevate to MUST or document why SHOULD is acceptable |
| XCON-02 | A-002, C-001 | K-SNAP-1 (snapshot immutability) cited for REQ-03 but delivery model is append-only (Option A), and SHA method is undefined | Specification, CONTRACT | Clarify K-SNAP-1 applicability to append-only; resolve SHA method |
| XCON-03 | E-001 | Scope Item Status TBD vs. documents proceeding as if scope is decided | Datasheet, Specification, Guidance | Resolve OI-037 or adopt conditional framing |
