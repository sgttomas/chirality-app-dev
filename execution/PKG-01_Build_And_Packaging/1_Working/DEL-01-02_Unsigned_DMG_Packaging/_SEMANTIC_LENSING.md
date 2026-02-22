# Semantic Lensing Register: DEL-01-02 Unsigned DMG Packaging Workflow

**Generated:** 2026-02-21
**Deliverable Folder:** /Users/ryan/ai-env/projects/chirality-app-dev1/execution/PKG-01_Build_And_Packaging/1_Working/DEL-01-02_Unsigned_DMG_Packaging/
**Warnings:** None

**Inputs Read:**
- _CONTEXT.md — `execution/PKG-01_Build_And_Packaging/1_Working/DEL-01-02_Unsigned_DMG_Packaging/_CONTEXT.md`
- _STATUS.md — `execution/PKG-01_Build_And_Packaging/1_Working/DEL-01-02_Unsigned_DMG_Packaging/_STATUS.md` (Current State: SEMANTIC_READY)
- _SEMANTIC.md — `execution/PKG-01_Build_And_Packaging/1_Working/DEL-01-02_Unsigned_DMG_Packaging/_SEMANTIC.md`
- Datasheet.md — `execution/PKG-01_Build_And_Packaging/1_Working/DEL-01-02_Unsigned_DMG_Packaging/Datasheet.md`
- Specification.md — `execution/PKG-01_Build_And_Packaging/1_Working/DEL-01-02_Unsigned_DMG_Packaging/Specification.md`
- Guidance.md — `execution/PKG-01_Build_And_Packaging/1_Working/DEL-01-02_Unsigned_DMG_Packaging/Guidance.md`
- Procedure.md — `execution/PKG-01_Build_And_Packaging/1_Working/DEL-01-02_Unsigned_DMG_Packaging/Procedure.md`
- _REFERENCES.md — `execution/PKG-01_Build_And_Packaging/1_Working/DEL-01-02_Unsigned_DMG_Packaging/_REFERENCES.md`

**Purpose:** Apply CHIRALITY_FRAMEWORK matrix cells as lenses over the production documents, capturing warranted enrichment inputs for a later enrichment pass.

## Summary

- Total warranted items: 21
- By document:
  - Datasheet: 5
  - Specification: 4
  - Guidance: 2
  - Procedure: 3
  - Multi: 7
- By matrix:
  - A: 5  B: 3  C: 3  F: 3  D: 2  X: 3  E: 2
- By type:
  - Conflict: 1
  - VerificationGap: 3
  - MissingSlot: 3
  - WeakStatement: 2
  - RationaleGap: 1
  - Normalization: 2
  - TBD_Question: 9
  - MatrixError: 0
- Notable conflicts: 1
- Matrix parse errors: 0

## Matrix A -- Orientation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| A:normative:guiding | normative | guiding | prescriptive direction | 1 | HAS_ITEMS | Build toolchain TBD blocks prescriptive direction |
| A:normative:applying | normative | applying | mandatory practice | 1 | HAS_ITEMS | Packaging tool selection unresolved |
| A:normative:judging | normative | judging | compliance determination | 1 | HAS_ITEMS | Instruction root verification depth ambiguous |
| A:normative:reviewing | normative | reviewing | regulatory audit | 0 | NO_ITEMS | Unsigned/unnotarized policy is clear and consistent |
| A:operative:guiding | operative | guiding | procedural direction | 1 | HAS_ITEMS | Node.js and package manager versions TBD |
| A:operative:applying | operative | applying | practical execution | 0 | NO_ITEMS | Procedure phases are well-structured for execution |
| A:operative:judging | operative | judging | performance assessment | 0 | NO_ITEMS | Verification checklist adequately maps requirements |
| A:operative:reviewing | operative | reviewing | process audit | 0 | NO_ITEMS | Records section captures evidence adequately |
| A:evaluative:guiding | evaluative | guiding | value orientation | 0 | NO_ITEMS | Purpose and value rationale clear in Guidance |
| A:evaluative:applying | evaluative | applying | merit application | 1 | HAS_ITEMS | Responsible Party TBD |
| A:evaluative:judging | evaluative | judging | worth determination | 0 | NO_ITEMS | Trade-offs documented in Guidance |
| A:evaluative:reviewing | evaluative | reviewing | quality appraisal | 0 | NO_ITEMS | Quality criteria implicit in verification checklist |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A-001 | A:normative:guiding | TBD_Question | Multi | Datasheet | Record TBD: Select packaging tool (electron-builder, @electron/forge, or create-dmg) and document the decision | The prescriptive direction for this deliverable cannot be fully established until the packaging tool is selected. Multiple documents reference this as TBD. | Datasheet.md; Guidance.md; Procedure.md | Datasheet#Attributes "Build Toolchain"; Guidance#Considerations "Packaging Tool Selection"; Procedure#Steps "Step 1.1" | -- | Human / DEL-01-01 outcome | TBD |
| A-002 | A:normative:applying | TBD_Question | Datasheet | Datasheet | Record TBD: Determine DMG layout/branding scope (plain vs. branded) and installer behavior (drag-to-Applications or other) | Mandatory practice cannot be fully codified while DMG Layout/Branding and Installer Behavior remain TBD in the Datasheet. | Datasheet.md | Datasheet#Attributes "DMG Layout/Branding"; Datasheet#Attributes "Installer Behavior" | -- | Human decision | TBD |
| A-003 | A:normative:judging | WeakStatement | Specification | Specification | Clarify REQ-DMG-006 acceptance criteria: define what constitutes adequate verification of instruction root assets (specific paths/files to check vs. "spot check") | Specification acceptance says "verify instruction root assets are present at expected paths" but Procedure Step 3.1 says "spot check." The verification depth is ambiguous, which could lead to inconsistent compliance determination. | Specification.md; Procedure.md | Specification#Verification REQ-DMG-006; Procedure#Steps "Step 3.1" | -- | Specification should govern | TBD |
| A-004 | A:operative:guiding | TBD_Question | Procedure | Multi | Record TBD: Specify required Node.js version and package manager (npm/yarn/pnpm) in Prerequisites | Procedural direction is incomplete without specifying the runtime version and package manager. Currently both are TBD. | Procedure.md | Procedure#Prerequisites "Required Environment" | -- | Project package.json / DEL-01-01 | TBD |
| A-005 | A:evaluative:applying | TBD_Question | Datasheet | Datasheet | Record TBD: Assign Responsible Party for DEL-01-02 | The Datasheet lists Responsible Party as TBD. Merit application (who owns and is accountable for this deliverable) cannot be assessed without assignment. | Datasheet.md | Datasheet#Identification "Responsible Party" | -- | Human / project governance | TBD |

## Matrix B -- Conceptualization (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| B:data:necessity | data | necessity | essential fact | 1 | HAS_ITEMS | Output artifact location is an essential fact that is TBD |
| B:data:sufficiency | data | sufficiency | adequate evidence | 0 | NO_ITEMS | Source references and decision provenance are adequate |
| B:data:completeness | data | completeness | comprehensive record | 1 | HAS_ITEMS | Application metadata incomplete |
| B:data:consistency | data | consistency | reliable measurement | 0 | NO_ITEMS | Architecture target consistently stated as arm64 |
| B:information:necessity | information | necessity | essential signal | 0 | NO_ITEMS | Key signals (unsigned OK, macOS 15+, arm64) are clear |
| B:information:sufficiency | information | sufficiency | adequate context | 0 | NO_ITEMS | Context is adequate across documents |
| B:information:completeness | information | completeness | comprehensive account | 0 | NO_ITEMS | Scope inclusions and exclusions well documented |
| B:information:consistency | information | consistency | coherent message | 1 | HAS_ITEMS | Terminology for working directory concept is inconsistent |
| B:knowledge:necessity | knowledge | necessity | fundamental understanding | 0 | NO_ITEMS | Packaging concepts adequately explained in Guidance |
| B:knowledge:sufficiency | knowledge | sufficiency | competent expertise | 0 | NO_ITEMS | Tool options documented with sufficient context |
| B:knowledge:completeness | knowledge | completeness | thorough mastery | 0 | NO_ITEMS | Guidance covers considerations thoroughly |
| B:knowledge:consistency | knowledge | consistency | coherent understanding | 0 | NO_ITEMS | Understanding of unsigned distribution model is coherent |
| B:wisdom:necessity | wisdom | necessity | essential discernment | 0 | NO_ITEMS | Key trade-offs identified in Guidance |
| B:wisdom:sufficiency | wisdom | sufficiency | adequate judgment | 0 | NO_ITEMS | Judgment calls appropriately surfaced as TBD |
| B:wisdom:completeness | wisdom | completeness | holistic insight | 0 | NO_ITEMS | Holistic view of packaging in context is present |
| B:wisdom:consistency | wisdom | consistency | principled reasoning | 0 | NO_ITEMS | Principles (P1-P4) in Guidance provide principled reasoning |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| B-001 | B:data:necessity | TBD_Question | Datasheet | Datasheet | Record TBD: Define output artifact location (build output path for .dmg file) | The output path for the .dmg file is an essential fact needed for both procedure execution and verification. Currently TBD in Datasheet. | Datasheet.md | Datasheet#Attributes "Output Artifact Location" | -- | Implementation decision / DEL-01-01 output structure | TBD |
| B-002 | B:data:completeness | TBD_Question | Multi | Multi | Record TBD: Define application metadata -- app name, version scheme, bundle identifier | Procedure Step 1.2 item 7 lists "Application metadata: App name, version, bundle identifier (TBD)." These are essential packaging configuration parameters. | Procedure.md; Datasheet.md | Procedure#Steps "Step 1.2" item 7; Datasheet#Attributes (not present) | -- | Project-level decision | TBD |
| B-003 | B:information:consistency | Normalization | Multi | Guidance | Normalize terminology: "working root" vs "projectRoot" vs "working directory" -- adopt one canonical term across all four documents | Three different terms are used for the same concept: Specification uses "working directory (projectRoot)," Guidance uses "working root," _CONTEXT.md uses "working directory." This inconsistency could cause drift in later documentation and implementation. | Specification.md; Guidance.md; Procedure.md; _CONTEXT.md | Specification#Requirements REQ-DMG-005; Guidance#Principles P3; Procedure#Steps "Step 3.3" | -- | DIRECTIVE Section 2.6 terminology | TBD |

## Matrix C -- Formulation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| C:normative:necessity | normative | necessity | obligatory conformance baseline | 1 | HAS_ITEMS | Upstream dependency not formally declared |
| C:normative:sufficiency | normative | sufficiency | defensible compliance assurance | 0 | NO_ITEMS | Verification table maps all requirements |
| C:normative:completeness | normative | completeness | total compliance coverage | 1 | HAS_ITEMS | CI integration scope undefined |
| C:normative:consistency | normative | consistency | harmonized regulatory standard | 0 | NO_ITEMS | Standards table is present and consistent |
| C:operative:necessity | operative | necessity | essential process capacity | 0 | NO_ITEMS | Prerequisite table covers essential inputs |
| C:operative:sufficiency | operative | sufficiency | qualified execution readiness | 0 | NO_ITEMS | Phases logically sequenced |
| C:operative:completeness | operative | completeness | thorough operational accounting | 0 | NO_ITEMS | Four phases cover CONFIG/SCRIPT/verification/DOC |
| C:operative:consistency | operative | consistency | disciplined execution uniformity | 0 | NO_ITEMS | Consistent checklist pattern across phases |
| C:evaluative:necessity | evaluative | necessity | foundational quality criterion | 1 | HAS_ITEMS | Gatekeeper bypass docs scope unresolved |
| C:evaluative:sufficiency | evaluative | sufficiency | justified value standing | 0 | NO_ITEMS | Value proposition clear in Guidance Purpose |
| C:evaluative:completeness | evaluative | completeness | comprehensive worth assessment | 0 | NO_ITEMS | Trade-offs table present |
| C:evaluative:consistency | evaluative | consistency | principled worth coherence | 0 | NO_ITEMS | Principles coherent and traceable |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| C-001 | C:normative:necessity | MissingSlot | Multi | Specification | Add formal upstream dependency declaration: DEL-01-01 is a prerequisite for DEL-01-02 (currently marked as ASSUMPTION in multiple documents) | The obligatory conformance baseline requires formal dependency declaration. Datasheet, Specification, and Procedure all reference DEL-01-01 dependency but mark it as ASSUMPTION rather than a formal requirement. | Datasheet.md; Specification.md; Procedure.md | Datasheet#Construction "Upstream dependency"; Specification#Scope "What This Deliverable Excludes"; Procedure#Prerequisites "Upstream Dependencies" | -- | Decomposition / ORCHESTRATOR | TBD |
| C-002 | C:normative:completeness | TBD_Question | Datasheet | Specification | Record TBD: Determine whether CI/CD integration for DMG builds is in scope or formally excluded | Total compliance coverage requires explicit scope boundaries. CI integration is flagged as TBD in the Datasheet Conditions and as a trade-off in Guidance, but it is neither a requirement nor formally excluded in the Specification. | Datasheet.md; Guidance.md; Specification.md | Datasheet#Conditions "CI integration"; Guidance#Trade-offs "CI integration"; Specification#Scope (absent) | -- | Human / project scope decision | TBD |
| C-003 | C:evaluative:necessity | WeakStatement | Guidance | Guidance | Clarify Gatekeeper bypass documentation depth: the ASSUMPTION that "brief note sufficient for technical self-builders" should be confirmed or revised | The foundational quality criterion for user-facing documentation depends on knowing the audience's technical level. Guidance trade-off table notes this as ASSUMPTION but no decision is recorded. | Guidance.md | Guidance#Trade-offs "Gatekeeper documentation depth" | -- | Human decision | TBD |

## Matrix F -- Requirements (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| F:normative:necessity | normative | necessity | binding conformance threshold | 1 | HAS_ITEMS | REQ-DMG-007 source is ASSUMPTION |
| F:normative:sufficiency | normative | sufficiency | warranted compliance mandate | 0 | NO_ITEMS | Requirements have adequate source traceability |
| F:normative:completeness | normative | completeness | exhaustive compliance mandate | 1 | HAS_ITEMS | Gatekeeper bypass not a formal requirement |
| F:normative:consistency | normative | consistency | coherent regulatory alignment | 0 | NO_ITEMS | Requirements aligned with DEC-PLAT-001 |
| F:operative:necessity | operative | necessity | foundational execution requirement | 0 | NO_ITEMS | Execution prerequisites adequately specified |
| F:operative:sufficiency | operative | sufficiency | demonstrated execution capability | 0 | NO_ITEMS | Script testing step addresses this |
| F:operative:completeness | operative | completeness | comprehensive process inventory | 0 | NO_ITEMS | Four-phase procedure covers full lifecycle |
| F:operative:consistency | operative | consistency | unified process standard | 0 | NO_ITEMS | Process steps follow consistent pattern |
| F:evaluative:necessity | evaluative | necessity | essential worth grounding | 0 | NO_ITEMS | Value grounding present via OBJ-001 traceability |
| F:evaluative:sufficiency | evaluative | sufficiency | substantiated value judgment | 0 | NO_ITEMS | Trade-offs adequately frame value judgments |
| F:evaluative:completeness | evaluative | completeness | exhaustive value accounting | 1 | HAS_ITEMS | Examples section entirely TBD |
| F:evaluative:consistency | evaluative | consistency | consistent evaluation standard | 0 | NO_ITEMS | Evaluation criteria consistent across verification table |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| F-001 | F:normative:necessity | RationaleGap | Specification | Guidance | Add rationale for REQ-DMG-007 (Repeatable Build) -- currently sourced as ASSUMPTION with no authoritative backing | This requirement's binding conformance threshold is weakened by its ASSUMPTION-only sourcing. The Guidance should document why repeatability is considered a binding requirement for this deliverable, even though the decomposition does not explicitly state it. | Specification.md | Specification#Requirements REQ-DMG-007 "Source" | -- | Human confirmation | TBD |
| F-002 | F:normative:completeness | MissingSlot | Specification | Specification | Consider whether Gatekeeper bypass handling should be elevated to a formal requirement (currently only in Guidance considerations and Specification Documentation section) | Exhaustive compliance mandate lens suggests that if Gatekeeper bypass is necessary for the install-and-launch experience, it may warrant a requirement rather than just a documentation note. Currently it is described in Guidance and mentioned in Specification Documentation but is not a numbered requirement. | Specification.md; Guidance.md | Specification#Documentation "Gatekeeper bypass notes"; Guidance#Considerations "Gatekeeper Handling" | -- | Human decision | TBD |
| F-003 | F:evaluative:completeness | MissingSlot | Guidance | Guidance | Add concrete examples (sample config, sample script invocation, sample output) -- currently "TBD" in Examples section | The Examples section in Guidance is entirely TBD. For exhaustive value accounting, worked examples would substantiate the guidance and aid downstream execution. | Guidance.md | Guidance#Examples | -- | Can be populated after tool selection (A-001) | TBD |

## Matrix D -- Objectives (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| D:normative:guiding | normative | guiding | authoritative compliance directive | 0 | NO_ITEMS | Compliance direction clear via DEC-PLAT-001 |
| D:normative:applying | normative | applying | enforced compliance practice | 0 | NO_ITEMS | Requirements enforceable once tool is selected |
| D:normative:judging | normative | judging | conclusive conformance verdict | 1 | HAS_ITEMS | Verification approach for REQ-DMG-003 has gap |
| D:normative:reviewing | normative | reviewing | settled oversight verification | 0 | NO_ITEMS | Verification checklist is comprehensive |
| D:operative:guiding | operative | guiding | established procedural guidance | 0 | NO_ITEMS | Procedure phases provide clear guidance |
| D:operative:applying | operative | applying | resolved practical deployment | 0 | NO_ITEMS | Deployment steps logically ordered |
| D:operative:judging | operative | judging | conclusive performance accounting | 0 | NO_ITEMS | Evidence of Completion section addresses this |
| D:operative:reviewing | operative | reviewing | systematic process verification | 0 | NO_ITEMS | Checklist-based approach is systematic |
| D:evaluative:guiding | evaluative | guiding | principled worth direction | 0 | NO_ITEMS | Principles P1-P4 provide value direction |
| D:evaluative:applying | evaluative | applying | justified merit deployment | 0 | NO_ITEMS | Merit framework implicit in trade-offs |
| D:evaluative:judging | evaluative | judging | conclusive worth verdict | 0 | NO_ITEMS | Trade-offs table supports worth assessment |
| D:evaluative:reviewing | evaluative | reviewing | settled quality examination | 1 | HAS_ITEMS | Troubleshooting section TBD in DOC artifact |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| D-001 | D:normative:judging | VerificationGap | Specification | Specification | Strengthen REQ-DMG-003 verification: add check for LSMinimumSystemVersion in Info.plist (currently conditional: "if set") | Conclusive conformance verdict for macOS 15+ target requires deterministic verification. The Specification verification says "check LSMinimumSystemVersion in Info.plist if set" -- the conditional "if set" means verification could pass without actually confirming the minimum OS version. | Specification.md | Specification#Verification REQ-DMG-003 | -- | Specification | TBD |
| D-002 | D:evaluative:reviewing | TBD_Question | Procedure | Procedure | Record TBD: Populate troubleshooting section in the Local Builder Guide (Step 4.1 item 5 lists "Common issues and resolutions (TBD)") | Settled quality examination requires that known failure modes are documented. The troubleshooting section is currently TBD. | Procedure.md | Procedure#Steps "Step 4.1" item 5 | -- | Execution experience | TBD |

## Matrix X -- Verification (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| X:guiding:necessity | guiding | necessity | foundational directive imperative | 0 | NO_ITEMS | Foundational directives established |
| X:guiding:sufficiency | guiding | sufficiency | sufficient directional assurance | 0 | NO_ITEMS | Direction sufficiently assured by decomposition traceability |
| X:guiding:completeness | guiding | completeness | exhaustive directive scope | 0 | NO_ITEMS | Scope boundaries well defined |
| X:guiding:consistency | guiding | consistency | uniform directive discipline | 0 | NO_ITEMS | Directives consistently applied |
| X:applying:necessity | applying | necessity | essential deployment foundation | 1 | HAS_ITEMS | Installer behavior not deterministically specified |
| X:applying:sufficiency | applying | sufficiency | justified deployment readiness | 0 | NO_ITEMS | Readiness criteria present in prerequisites |
| X:applying:completeness | applying | completeness | comprehensive deployment accounting | 1 | HAS_ITEMS | Artifact locations all TBD |
| X:applying:consistency | applying | consistency | disciplined deployment coherence | 0 | NO_ITEMS | Deployment approach coherent within each doc |
| X:judging:necessity | judging | necessity | fundamental verdict foundation | 0 | NO_ITEMS | Verdict foundations present in verification table |
| X:judging:sufficiency | judging | sufficiency | defensible verdict warrant | 0 | NO_ITEMS | Verification approaches defensible |
| X:judging:completeness | judging | completeness | comprehensive verdict coverage | 0 | NO_ITEMS | All 8 requirements have verification entries |
| X:judging:consistency | judging | consistency | principled verdict uniformity | 0 | NO_ITEMS | Verification pattern is uniform |
| X:reviewing:necessity | reviewing | necessity | essential verification baseline | 1 | HAS_ITEMS | No baseline for DMG file size validation |
| X:reviewing:sufficiency | reviewing | sufficiency | sufficient verification assurance | 0 | NO_ITEMS | Verification assurance adequate given TBDs |
| X:reviewing:completeness | reviewing | completeness | exhaustive verification scope | 0 | NO_ITEMS | Verification scope covers all requirements |
| X:reviewing:consistency | reviewing | consistency | uniform verification discipline | 0 | NO_ITEMS | Verification checklist consistently formatted |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| X-001 | X:applying:necessity | Conflict | Multi | Specification | Resolve installer behavior: Datasheet says "TBD -- expected drag-to-Applications or equivalent" but Specification REQ-DMG-005 and Procedure Step 3.3 assume drag-to-Applications as the installation method | Essential deployment foundation requires a settled installation method. The Datasheet marks this TBD while Specification and Procedure assume a specific method. | Datasheet.md; Specification.md; Procedure.md | Datasheet#Attributes "Installer Behavior"; Specification#Requirements REQ-DMG-005 "Acceptance"; Procedure#Steps "Step 3.3" | Datasheet.md#Attributes "Installer Behavior" vs Specification.md#Requirements REQ-DMG-005 vs Procedure.md#Steps "Step 3.3" | Specification (normative document) | TBD |
| X-002 | X:applying:completeness | VerificationGap | Procedure | Multi | Add expected artifact file locations to Records table -- all three artifact locations (CONFIG, SCRIPT, DOC) are TBD | Comprehensive deployment accounting requires knowing where produced artifacts reside. The Procedure Records section lists all three artifact locations as TBD. | Procedure.md | Procedure#Records "Deliverable Artifacts Produced" | -- | Implementation decision | TBD |
| X-003 | X:reviewing:necessity | VerificationGap | Procedure | Procedure | Add DMG file size sanity check threshold or range to Step 2.2 -- currently says "not empty, not unexpectedly large" without defining acceptable bounds | Essential verification baseline for the DMG artifact lacks quantitative or qualitative bounds. "Not unexpectedly large" is subjective and could lead to inconsistent verification. | Procedure.md | Procedure#Steps "Step 2.2" | -- | Implementation experience | TBD |

## Matrix E -- Evaluation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| E:normative:necessity | normative | necessity | binding authority foundation | 0 | NO_ITEMS | Authority foundation established via DEC-PLAT-001 |
| E:normative:sufficiency | normative | sufficiency | warranted mandate assurance | 0 | NO_ITEMS | Mandate assurance present via requirement sourcing |
| E:normative:completeness | normative | completeness | total mandate coverage | 1 | HAS_ITEMS | Normalization gap in terminology |
| E:normative:consistency | normative | consistency | uniform mandate discipline | 0 | NO_ITEMS | Mandate discipline uniform across documents |
| E:operative:necessity | operative | necessity | fundamental operational requirement | 0 | NO_ITEMS | Operational requirements captured |
| E:operative:sufficiency | operative | sufficiency | sufficient operational assurance | 0 | NO_ITEMS | Operational assurance adequate |
| E:operative:completeness | operative | completeness | total operational scope | 0 | NO_ITEMS | Operational scope covered by four phases |
| E:operative:consistency | operative | consistency | consistent operational discipline | 0 | NO_ITEMS | Operational discipline consistent |
| E:evaluative:necessity | evaluative | necessity | fundamental value grounding | 0 | NO_ITEMS | Value grounding present |
| E:evaluative:sufficiency | evaluative | sufficiency | defensible value assurance | 0 | NO_ITEMS | Value assurance defensible |
| E:evaluative:completeness | evaluative | completeness | comprehensive value scope | 1 | HAS_ITEMS | Standards table incomplete |
| E:evaluative:consistency | evaluative | consistency | consistent value governance | 0 | NO_ITEMS | Value governance consistent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| E-001 | E:normative:completeness | Normalization | Multi | Multi | Normalize ASSUMPTION markers: adopt consistent formatting and tracking for items marked as ASSUMPTION across all documents (currently inconsistent use of bold, parenthetical, and inline ASSUMPTION tags) | Total mandate coverage lens reveals that ASSUMPTION markers are used extensively but without a consistent format or tracking mechanism. Some are bold, some parenthetical, some inline. A normalization pass would improve auditability. | Datasheet.md; Specification.md; Guidance.md; Procedure.md | entire document scanned (all four) | -- | Governance convention | TBD |
| E-002 | E:evaluative:completeness | MissingSlot | Specification | Specification | Add reference to specific Apple documentation for macOS app bundle structure and Gatekeeper behavior in Standards table (currently marked ASSUMPTION with "location TBD") | Comprehensive value scope requires that standards references be traceable. The Standards table in Specification cites "Apple platform conventions (ASSUMPTION)" and "Apple macOS security model (ASSUMPTION)" without specific document references. | Specification.md | Specification#Standards | -- | Apple developer documentation | TBD |
