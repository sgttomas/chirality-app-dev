# Semantic Lensing Register: DEL-03-03 Turn Options Mapping & Fallback Chains

**Generated:** 2026-02-21
**Deliverable Folder:** /Users/ryan/ai-env/projects/chirality-app-dev1/execution/PKG-03_Harness_Runtime_Core/1_Working/DEL-03-03_Turn_Options_Fallback_Chains/
**Warnings:** None

**Inputs Read:**
- _CONTEXT.md — `execution/PKG-03_Harness_Runtime_Core/1_Working/DEL-03-03_Turn_Options_Fallback_Chains/_CONTEXT.md`
- _STATUS.md — `execution/PKG-03_Harness_Runtime_Core/1_Working/DEL-03-03_Turn_Options_Fallback_Chains/_STATUS.md`
- _SEMANTIC.md — `execution/PKG-03_Harness_Runtime_Core/1_Working/DEL-03-03_Turn_Options_Fallback_Chains/_SEMANTIC.md`
- Datasheet.md — `execution/PKG-03_Harness_Runtime_Core/1_Working/DEL-03-03_Turn_Options_Fallback_Chains/Datasheet.md`
- Specification.md — `execution/PKG-03_Harness_Runtime_Core/1_Working/DEL-03-03_Turn_Options_Fallback_Chains/Specification.md`
- Guidance.md — `execution/PKG-03_Harness_Runtime_Core/1_Working/DEL-03-03_Turn_Options_Fallback_Chains/Guidance.md`
- Procedure.md — `execution/PKG-03_Harness_Runtime_Core/1_Working/DEL-03-03_Turn_Options_Fallback_Chains/Procedure.md`
- _REFERENCES.md — `execution/PKG-03_Harness_Runtime_Core/1_Working/DEL-03-03_Turn_Options_Fallback_Chains/_REFERENCES.md`

**Purpose:** Apply CHIRALITY_FRAMEWORK matrix cells as lenses over the production documents, capturing warranted enrichment inputs for a later enrichment pass.

## Summary

- Total warranted items: 18
- By document:
  - Datasheet: 3
  - Specification: 7
  - Guidance: 4
  - Procedure: 2
  - Multi: 2
- By matrix:
  - A: 4  B: 3  C: 2  F: 3  D: 2  X: 2  E: 2
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

## Matrix A -- Orientation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| A:normative:guiding | normative | guiding | prescriptive direction | 1 | HAS_ITEMS | Model fallback ambiguity identified |
| A:normative:applying | normative | applying | mandatory practice | 1 | HAS_ITEMS | Bootstrap constraint boundary unclear |
| A:normative:judging | normative | judging | compliance determination | 1 | HAS_ITEMS | K-GHOST-1 compliance verification gap |
| A:normative:reviewing | normative | reviewing | regulatory audit | 0 | NO_ITEMS | Audit mechanisms adequately described in Verification table |
| A:operative:guiding | operative | guiding | procedural direction | 0 | NO_ITEMS | Step sequencing in Procedure is clear |
| A:operative:applying | operative | applying | practical execution | 1 | HAS_ITEMS | Malformed frontmatter handling undefined |
| A:operative:judging | operative | judging | performance assessment | 0 | NO_ITEMS | Verification table in Specification covers performance checks |
| A:operative:reviewing | operative | reviewing | process audit | 0 | NO_ITEMS | Records section in Procedure is adequate |
| A:evaluative:guiding | evaluative | guiding | value orientation | 0 | NO_ITEMS | Purpose and Principles in Guidance convey value orientation |
| A:evaluative:applying | evaluative | applying | merit application | 0 | NO_ITEMS | Trade-offs section addresses merit considerations |
| A:evaluative:judging | evaluative | judging | worth determination | 0 | NO_ITEMS | Verification pass criteria are defined |
| A:evaluative:reviewing | evaluative | reviewing | quality appraisal | 0 | NO_ITEMS | Quality review addressed by code review and test records |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A-001 | A:normative:guiding | Conflict | Multi | Specification | Clarify whether persona-level `model` frontmatter participates as Tier 2 in the model fallback chain; Specification REQ-01 note and Guidance CONF-01 both flag the ambiguity but no resolution is recorded | SPEC.md Section 9.8 shows model fallback skipping persona tier; Section 9.7 lists `model` as machine-consumed frontmatter; documents surface the conflict but do not resolve it | Specification.md, Guidance.md | REQ-01 Note on Model fallback chain; Conflict Table CONF-01 | Specification.md#REQ-01, Guidance.md#Conflict-Table-CONF-01 | Codebase inspection -- PROPOSAL | TBD |
| A-002 | A:normative:applying | WeakStatement | Specification | Specification | Clarify which constraints are "bootstrap-only" in REQ-05; the requirement states bootstrap policy is authoritative for "bootstrap-only constraints" but does not enumerate them | Without an enumeration, implementers cannot distinguish bootstrap-only from per-turn-overridable constraints, risking incorrect enforcement | Specification.md | REQ-05: Session Boot Opts Handling | | SPEC.md or human ruling -- PROPOSAL | TBD |
| A-003 | A:normative:judging | VerificationGap | Specification | Specification | Add verification approach for K-GHOST-1 compliance; REQ-04 references runtime authorization independence from UI but K-GHOST-1 (no ghost inputs) has no explicit verification row | K-GHOST-1 is listed in Standards but has no corresponding verification entry, leaving a compliance gap | Specification.md | Verification table; Standards table | | docs/CONTRACT.md K-GHOST-1 -- PROPOSAL | TBD |
| A-004 | A:operative:applying | MissingSlot | Procedure | Procedure | Add explicit error handling behavior for malformed persona frontmatter in Step 3; currently lists it as "TBD: define error handling behavior" | The procedure acknowledges malformed frontmatter as an edge case but defers behavior definition; this is a concrete operational gap for execution | Procedure.md | Step 3: Implement/Verify Persona Frontmatter Parsing, item 3 | | Human ruling -- PROPOSAL | TBD |

---

## Matrix B -- Conceptualization (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| B:data:necessity | data | necessity | essential fact | 1 | HAS_ITEMS | Full opts field enumeration is TBD |
| B:data:sufficiency | data | sufficiency | adequate evidence | 0 | NO_ITEMS | Documented fields have adequate source citations |
| B:data:completeness | data | completeness | comprehensive record | 1 | HAS_ITEMS | Additional opts fields beyond model/tools/maxTurns not enumerated |
| B:data:consistency | data | consistency | reliable measurement | 0 | NO_ITEMS | Field naming is consistent across documents |
| B:information:necessity | information | necessity | essential signal | 0 | NO_ITEMS | Fallback chain logic is clearly signaled |
| B:information:sufficiency | information | sufficiency | adequate context | 0 | NO_ITEMS | Context for each tier is described |
| B:information:completeness | information | completeness | comprehensive account | 0 | NO_ITEMS | Account of three-tier chain is comprehensive for documented fields |
| B:information:consistency | information | consistency | coherent message | 0 | NO_ITEMS | Messaging is consistent across documents |
| B:knowledge:necessity | knowledge | necessity | fundamental understanding | 0 | NO_ITEMS | Core mechanism (layered fallback) is well understood in all docs |
| B:knowledge:sufficiency | knowledge | sufficiency | competent expertise | 0 | NO_ITEMS | Documents demonstrate competent framing of the domain |
| B:knowledge:completeness | knowledge | completeness | thorough mastery | 0 | NO_ITEMS | Within documented scope, mastery is thorough |
| B:knowledge:consistency | knowledge | consistency | coherent understanding | 0 | NO_ITEMS | Understanding is coherent across all four documents |
| B:wisdom:necessity | wisdom | necessity | essential discernment | 1 | HAS_ITEMS | Fail-open vs fail-closed decision deferred |
| B:wisdom:sufficiency | wisdom | sufficiency | adequate judgment | 0 | NO_ITEMS | Trade-off analysis in Guidance is adequate |
| B:wisdom:completeness | wisdom | completeness | holistic insight | 0 | NO_ITEMS | Considerations section provides holistic view |
| B:wisdom:consistency | wisdom | consistency | principled reasoning | 0 | NO_ITEMS | Reasoning aligns with DIRECTIVE.md principles |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| B-001 | B:data:necessity | TBD_Question | Datasheet | Datasheet | Enumerate the complete set of supported `opts` fields from codebase inspection; currently only model, tools, maxTurns are documented with fallback chains | Datasheet notes "Additional `opts` fields may exist in the implementation; a complete enumeration requires code inspection" -- this essential data is missing | Datasheet.md | Attributes > Turn Options (`opts`) Fields, note | | Codebase inspection -- PROPOSAL | TBD |
| B-002 | B:data:completeness | MissingSlot | Datasheet | Datasheet | Add Tier 3 default values (the actual runtime defaults) for each documented field; currently "runtime default" is named but never specified | Without knowing the actual runtime default values, the fallback chain description is structurally complete but data-incomplete at Tier 3 | Datasheet.md | Attributes > Turn Options (`opts`) Fields | | Codebase inspection -- PROPOSAL | TBD |
| B-003 | B:wisdom:necessity | RationaleGap | Guidance | Guidance | Record a human ruling on T2 (fail-open vs fail-closed on unknown opts fields); Guidance proposes "warn and continue" but notes "Human ruling TBD" | This is a design decision with safety implications (silent failures vs. breaking changes) that lacks a recorded ruling | Guidance.md | Trade-offs > T2: Fail-Open vs. Fail-Closed on Unknown Opts Fields | | Human ruling -- PROPOSAL | TBD |

---

## Matrix C -- Formulation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| C:normative:necessity | normative | necessity | obligatory compliance imperative | 1 | HAS_ITEMS | REQ-09 assumption needs grounding |
| C:normative:sufficiency | normative | sufficiency | justified regulatory sufficiency | 0 | NO_ITEMS | Requirements are justified with source citations |
| C:normative:completeness | normative | completeness | total prescriptive coverage | 1 | HAS_ITEMS | Enforcement constraints vs. fallback defaults boundary |
| C:normative:consistency | normative | consistency | uniform regulatory coherence | 0 | NO_ITEMS | Requirements are internally consistent |
| C:operative:necessity | operative | necessity | indispensable execution process | 0 | NO_ITEMS | Core execution process is defined |
| C:operative:sufficiency | operative | sufficiency | competent operational adequacy | 0 | NO_ITEMS | Procedure steps are operationally adequate |
| C:operative:completeness | operative | completeness | exhaustive operational accounting | 0 | NO_ITEMS | Steps cover audit through documentation |
| C:operative:consistency | operative | consistency | deterministic operational stability | 0 | NO_ITEMS | Determinism is explicitly addressed in REQ-02 |
| C:evaluative:necessity | evaluative | necessity | intrinsic value criterion | 0 | NO_ITEMS | Value criteria aligned with OBJ-002 |
| C:evaluative:sufficiency | evaluative | sufficiency | justified merit appraisal | 0 | NO_ITEMS | Merit criteria are justified |
| C:evaluative:completeness | evaluative | completeness | comprehensive value panorama | 0 | NO_ITEMS | Quality dimensions are covered |
| C:evaluative:consistency | evaluative | consistency | principled valuation coherence | 0 | NO_ITEMS | Valuation principles are coherent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| C-001 | C:normative:necessity | WeakStatement | Specification | Specification | Strengthen REQ-09 from ASSUMPTION to a grounded requirement; currently reads "ASSUMPTION: The runtime may support opts fields beyond the three documented fallback examples" without a binding source | As an assumption-only requirement, REQ-09 has no normative force; if additional fields exist, their resolution pattern must be obligatory, not assumed | Specification.md | REQ-09: Additional Opts Fields | | Codebase inspection to confirm or remove -- PROPOSAL | TBD |
| C-002 | C:normative:completeness | MissingSlot | Specification | Specification | Add requirements distinguishing enforcement constraints (`disallowed_tools`, `auto_approve_tools`) from fallback defaults (`tools`, `model`, `max_turns`); Guidance C2 notes the distinction but no requirement governs it | Guidance identifies that "Not all frontmatter fields have a 1:1 mapping to opts fields" and that some are constraints rather than defaults, but no normative requirement captures this boundary | Specification.md, Guidance.md | REQ-07, Guidance C2 | | Human ruling -- PROPOSAL | TBD |

---

## Matrix F -- Requirements (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| F:normative:necessity | normative | necessity | mandatory governance foundation | 1 | HAS_ITEMS | K-INVENT-1 verification gap |
| F:normative:sufficiency | normative | sufficiency | warranted prescriptive competence | 0 | NO_ITEMS | Requirements are warranted by source citations |
| F:normative:completeness | normative | completeness | total mandate comprehension | 0 | NO_ITEMS | Mandate is comprehensively stated |
| F:normative:consistency | normative | consistency | harmonized regulatory discipline | 0 | NO_ITEMS | No regulatory inconsistencies detected |
| F:operative:necessity | operative | necessity | critical execution readiness | 1 | HAS_ITEMS | Prerequisites are all TBD status |
| F:operative:sufficiency | operative | sufficiency | sufficient process substantiation | 0 | NO_ITEMS | Process is sufficiently substantiated |
| F:operative:completeness | operative | completeness | exhaustive process mastery | 0 | NO_ITEMS | Process steps are complete within scope |
| F:operative:consistency | operative | consistency | harmonized process discipline | 0 | NO_ITEMS | Process discipline is harmonized |
| F:evaluative:necessity | evaluative | necessity | foundational quality imperative | 1 | HAS_ITEMS | Pass criteria partially undefined |
| F:evaluative:sufficiency | evaluative | sufficiency | sufficient merit benchmark | 0 | NO_ITEMS | Benchmarks are sufficient for documented fields |
| F:evaluative:completeness | evaluative | completeness | total valuation authority | 0 | NO_ITEMS | Valuation scope is adequate |
| F:evaluative:consistency | evaluative | consistency | disciplined valuation harmony | 0 | NO_ITEMS | Valuation is harmonized |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| F-001 | F:normative:necessity | VerificationGap | Specification | Specification | Add explicit verification row for REQ-10 (No Invented Values / K-INVENT-1) in the Verification table; REQ-10 edge-case test is listed but not explicitly mapped to K-INVENT-1 compliance | REQ-10 cites K-INVENT-1 as its source, and a verification row exists, but the verification approach ("edge-case test") does not explicitly confirm K-INVENT-1 compliance -- it tests "defined default or explicit handling" without asserting no-invention | Specification.md | Verification table, REQ-10 row | | docs/CONTRACT.md -- PROPOSAL | TBD |
| F-002 | F:operative:necessity | MissingSlot | Procedure | Procedure | Define readiness criteria or gating checks for TBD prerequisites (codebase access, existing turn API, existing session boot API, persona files); all are marked "Status: TBD" | Procedure lists prerequisites but all have TBD status; without readiness criteria, execution cannot confirm critical execution readiness before starting | Procedure.md | Prerequisites table | | Human ruling or dependency tracking -- PROPOSAL | TBD |
| F-003 | F:evaluative:necessity | VerificationGap | Specification | Procedure | Add concrete pass/fail thresholds for the determinism test (REQ-02 verification); "same inputs -> same outputs across repeated runs" does not specify N or how to detect non-determinism | The verification approach for REQ-02 says "Property-based or deterministic test: same inputs -> same outputs across repeated runs" but lacks specific pass criteria (how many runs, what constitutes a failure) | Specification.md | Verification table, REQ-02 row | | Human ruling -- PROPOSAL | TBD |

---

## Matrix D -- Objectives (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| D:normative:guiding | normative | guiding | resolved prescriptive authority | 1 | HAS_ITEMS | Authority for opts schema typing unresolved |
| D:normative:applying | normative | applying | enforced compliance capability | 0 | NO_ITEMS | Compliance enforcement path is defined |
| D:normative:judging | normative | judging | resolved conformance adjudication | 0 | NO_ITEMS | Conformance adjudication via test results |
| D:normative:reviewing | normative | reviewing | resolved regulatory oversight | 0 | NO_ITEMS | Oversight mechanisms in place |
| D:operative:guiding | operative | guiding | resolved procedural guidance | 0 | NO_ITEMS | Procedure steps provide clear guidance |
| D:operative:applying | operative | applying | substantiated operational enactment | 0 | NO_ITEMS | Steps are actionable |
| D:operative:judging | operative | judging | resolved performance verdict | 0 | NO_ITEMS | Performance checks defined in Verification |
| D:operative:reviewing | operative | reviewing | resolved operational audit | 0 | NO_ITEMS | Audit approach defined |
| D:evaluative:guiding | evaluative | guiding | resolved value commitment | 0 | NO_ITEMS | Value commitment clear in Guidance Purpose |
| D:evaluative:applying | evaluative | applying | resolved merit application | 0 | NO_ITEMS | Merit criteria applied consistently |
| D:evaluative:judging | evaluative | judging | definitive valuation ruling | 1 | HAS_ITEMS | OBJ-002 acceptance criteria traceability |
| D:evaluative:reviewing | evaluative | reviewing | resolved quality retrospection | 0 | NO_ITEMS | Quality review mechanisms defined |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| D-001 | D:normative:guiding | RationaleGap | Guidance | Guidance | Add rationale for Trade-off T1 (Strict Typing vs. Open Extension) proposed direction; currently states "ASSUMPTION -- Prefer strict typing for documented fields" without explaining why this best serves the harness contract or how it relates to SPEC.md extensibility | The trade-off section identifies the options but the proposed direction is marked as an assumption with no supporting rationale grounded in the governing documents | Guidance.md | Trade-offs > T1: Strict Typing vs. Open Extension | | Human ruling -- PROPOSAL | TBD |
| D-002 | D:evaluative:judging | MissingSlot | Specification | Specification | Add explicit traceability from verification outcomes to OBJ-002 acceptance criteria ("Turn options mapping + fallback chains conform to the harness contract"); currently OBJ-002 is referenced in Guidance Purpose but not in Specification Verification | The Specification verification table maps requirements to evidence but does not trace back to the objective-level acceptance criteria, making it unclear whether passing all REQ tests satisfies OBJ-002 | Specification.md, Guidance.md | Verification table; Guidance Purpose (OBJ-002 reference) | | Decomposition -- PROPOSAL | TBD |

---

## Matrix X -- Verification (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| X:guiding:necessity | guiding | necessity | purposeful conformance direction | 0 | NO_ITEMS | Conformance direction is purposeful |
| X:guiding:sufficiency | guiding | sufficiency | warranted directional competence | 0 | NO_ITEMS | Directional guidance is warranted |
| X:guiding:completeness | guiding | completeness | comprehensive directional coverage | 0 | NO_ITEMS | Directional coverage is comprehensive |
| X:guiding:consistency | guiding | consistency | unified directional discipline | 0 | NO_ITEMS | Directional discipline is unified |
| X:applying:necessity | applying | necessity | indispensable enforcement practice | 0 | NO_ITEMS | Enforcement practices are defined |
| X:applying:sufficiency | applying | sufficiency | adequate enforcement capability | 0 | NO_ITEMS | Capability is adequate for documented fields |
| X:applying:completeness | applying | completeness | total applied coverage | 1 | HAS_ITEMS | Cross-deliverable verification incomplete |
| X:applying:consistency | applying | consistency | consistent applied discipline | 0 | NO_ITEMS | Applied discipline is consistent |
| X:judging:necessity | judging | necessity | essential conformance verdict | 0 | NO_ITEMS | Verdicts are tied to test results |
| X:judging:sufficiency | judging | sufficiency | sufficient adjudicative warrant | 0 | NO_ITEMS | Warrant for adjudication is sufficient |
| X:judging:completeness | judging | completeness | comprehensive adjudicative scope | 0 | NO_ITEMS | Scope is comprehensive within deliverable boundary |
| X:judging:consistency | judging | consistency | disciplined adjudicative integrity | 0 | NO_ITEMS | Integrity of adjudication is disciplined |
| X:reviewing:necessity | reviewing | necessity | vital oversight examination | 0 | NO_ITEMS | Oversight examination is defined |
| X:reviewing:sufficiency | reviewing | sufficiency | sufficient retrospective warrant | 0 | NO_ITEMS | Retrospective warrant is sufficient |
| X:reviewing:completeness | reviewing | completeness | comprehensive retrospective coverage | 1 | HAS_ITEMS | Test artifact locations are TBD |
| X:reviewing:consistency | reviewing | consistency | dependable retrospective integrity | 0 | NO_ITEMS | Retrospective integrity is dependable |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| X-001 | X:applying:completeness | VerificationGap | Procedure | Procedure | Define concrete verification methods for cross-deliverable checks in Step 8 (DEL-03-04, DEL-04-01, DEL-02-03 interactions); currently states "Verify that opts mapping does not break..." without specifying how | Step 8 lists three cross-deliverable verification checks but provides no method, tool, or evidence type for confirming the checks pass; this undermines total applied coverage | Procedure.md | Step 8: Cross-Deliverable Verification | | Human ruling / dependency tracking -- PROPOSAL | TBD |
| X-002 | X:reviewing:completeness | WeakStatement | Procedure | Procedure | Specify expected locations for test result artifacts and code review records; Records table lists all locations as "TBD" | Without defined artifact locations, retrospective review cannot locate evidence of completion; all four Records entries have "TBD" locations | Procedure.md | Records table | | Existing project conventions -- PROPOSAL | TBD |

---

## Matrix E -- Evaluation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| E:normative:necessity | normative | necessity | binding conformance imperative | 0 | NO_ITEMS | Binding conformance is addressed by requirements |
| E:normative:sufficiency | normative | sufficiency | justified compliance authority | 0 | NO_ITEMS | Compliance authority is justified |
| E:normative:completeness | normative | completeness | total regulatory comprehension | 1 | HAS_ITEMS | Terminology inconsistency |
| E:normative:consistency | normative | consistency | principled regulatory integrity | 0 | NO_ITEMS | Regulatory integrity is principled |
| E:operative:necessity | operative | necessity | critical operational verification | 0 | NO_ITEMS | Operational verification is addressed |
| E:operative:sufficiency | operative | sufficiency | justified operational competence | 0 | NO_ITEMS | Operational competence is justified |
| E:operative:completeness | operative | completeness | exhaustive operational scope | 0 | NO_ITEMS | Operational scope is exhaustive for documented fields |
| E:operative:consistency | operative | consistency | dependable operational integrity | 0 | NO_ITEMS | Operational integrity is dependable |
| E:evaluative:necessity | evaluative | necessity | fundamental quality determination | 1 | HAS_ITEMS | Responsible Party is TBD |
| E:evaluative:sufficiency | evaluative | sufficiency | justified quality sufficiency | 0 | NO_ITEMS | Quality sufficiency is justified |
| E:evaluative:completeness | evaluative | completeness | comprehensive quality panorama | 0 | NO_ITEMS | Quality panorama is comprehensive |
| E:evaluative:consistency | evaluative | consistency | principled quality integrity | 0 | NO_ITEMS | Quality integrity is principled |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| E-001 | E:normative:completeness | Normalization | Multi | Guidance | Normalize terminology for persona frontmatter field `max_turns` vs. opts field `maxTurns`; documents use both naming conventions without explicitly noting the mapping | Datasheet uses `opts.maxTurns` (camelCase) and persona `max_turns` (snake_case); Specification REQ-01 and REQ-07 also use both; no document explicitly states the naming convention mapping between the two | Datasheet.md, Specification.md | Datasheet Attributes table; Specification REQ-01, REQ-07 | | Guidance vocabulary note -- PROPOSAL | TBD |
| E-002 | E:evaluative:necessity | TBD_Question | Datasheet | Datasheet | Assign the Responsible Party field; currently "TBD" in Identification table | Without a responsible party, there is no accountable owner for quality determination and deliverable acceptance | Datasheet.md | Identification table, Responsible Party row | | Human assignment -- PROPOSAL | TBD |
