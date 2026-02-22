# Semantic Lensing Register: DEL-08-04 On-demand Dependency Graph Generator

**Generated:** 2026-02-21
**Deliverable Folder:** /Users/ryan/ai-env/projects/chirality-app-dev1/execution/PKG-08_Optional_Integrity_Hardening/1_Working/DEL-08-04_Dependency_Graph_Generator/
**Warnings:** None

**Inputs Read:**
- _CONTEXT.md — `execution/PKG-08_Optional_Integrity_Hardening/1_Working/DEL-08-04_Dependency_Graph_Generator/_CONTEXT.md`
- _STATUS.md — `execution/PKG-08_Optional_Integrity_Hardening/1_Working/DEL-08-04_Dependency_Graph_Generator/_STATUS.md`
- _SEMANTIC.md — `execution/PKG-08_Optional_Integrity_Hardening/1_Working/DEL-08-04_Dependency_Graph_Generator/_SEMANTIC.md`
- Datasheet.md — `execution/PKG-08_Optional_Integrity_Hardening/1_Working/DEL-08-04_Dependency_Graph_Generator/Datasheet.md`
- Specification.md — `execution/PKG-08_Optional_Integrity_Hardening/1_Working/DEL-08-04_Dependency_Graph_Generator/Specification.md`
- Guidance.md — `execution/PKG-08_Optional_Integrity_Hardening/1_Working/DEL-08-04_Dependency_Graph_Generator/Guidance.md`
- Procedure.md — `execution/PKG-08_Optional_Integrity_Hardening/1_Working/DEL-08-04_Dependency_Graph_Generator/Procedure.md`
- _REFERENCES.md — `execution/PKG-08_Optional_Integrity_Hardening/1_Working/DEL-08-04_Dependency_Graph_Generator/_REFERENCES.md`

**Purpose:** Apply CHIRALITY_FRAMEWORK matrix cells as lenses over the production documents, capturing warranted enrichment inputs for a later enrichment pass.

## Summary

- Total warranted items: 22
- By document:
  - Datasheet: 5
  - Specification: 7
  - Guidance: 4
  - Procedure: 3
  - Multi: 3
- By matrix:
  - A: 4  B: 3  C: 3  F: 3  D: 3  X: 4  E: 2
- By type:
  - Conflict: 0
  - VerificationGap: 4
  - MissingSlot: 7
  - WeakStatement: 3
  - RationaleGap: 2
  - Normalization: 3
  - TBD_Question: 3
  - MatrixError: 0
- Notable conflicts: 0
- Matrix parse errors: 0

## Matrix A — Orientation (3x4) — Canonical

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| A:normative:guiding | normative | guiding | prescriptive direction | 1 | HAS_ITEMS | TBD items on language/runtime decision |
| A:normative:applying | normative | applying | mandatory practice | 1 | HAS_ITEMS | Read-only constraint well-covered; gap on exit code behavior |
| A:normative:judging | normative | judging | compliance determination | 0 | NO_ITEMS | REQ-01 through REQ-14 cover compliance well |
| A:normative:reviewing | normative | reviewing | regulatory audit | 1 | HAS_ITEMS | Verification table present but missing acceptance thresholds |
| A:operative:guiding | operative | guiding | procedural direction | 0 | NO_ITEMS | Procedure Part A provides clear step sequence |
| A:operative:applying | operative | applying | practical execution | 0 | NO_ITEMS | Steps A.1-A.10 and B.1-B.3 are actionable |
| A:operative:judging | operative | judging | performance assessment | 1 | HAS_ITEMS | No performance criteria defined |
| A:operative:reviewing | operative | reviewing | process audit | 0 | NO_ITEMS | Verification table in Procedure covers process checks |
| A:evaluative:guiding | evaluative | guiding | value orientation | 0 | NO_ITEMS | Guidance Purpose section adequately frames value |
| A:evaluative:applying | evaluative | applying | merit application | 0 | NO_ITEMS | Trade-offs section covers merit considerations |
| A:evaluative:judging | evaluative | judging | worth determination | 0 | NO_ITEMS | Covered by Guidance T-01 staging rationale |
| A:evaluative:reviewing | evaluative | reviewing | quality appraisal | 0 | NO_ITEMS | Verification checks cover quality dimensions |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A-001 | A:normative:guiding | TBD_Question | Datasheet | Datasheet | Record human design decision for language/runtime (Python, Node.js, or shell) — currently marked ASSUMPTION | The prescriptive direction for implementation cannot be finalized until the language/runtime is decided; this blocks downstream normative specification of dependencies, build steps, and CLI interface | Datasheet.md | Attributes table, "Language/runtime" row | — | Human decision | TBD |
| A-002 | A:normative:applying | MissingSlot | Specification | Specification | Add requirement for exit code behavior: define what exit codes the tool returns for success, cycles-found, parse-errors, and invalid-arguments | Mandatory practice for CLI tool operation requires defined exit codes; without them, automated callers (including DEL-08-07) cannot reliably determine tool outcome | Specification.md | Requirements section (after REQ-14) | — | Specification | TBD |
| A-003 | A:normative:reviewing | VerificationGap | Specification | Specification | Add quantitative acceptance thresholds to verification approaches (e.g., "all N files discovered" should specify how N is determined; cycle detection should specify max detection time or graph size) | Verification table uses qualitative descriptions ("verify all are discovered") without measurable pass/fail thresholds, making audit determination ambiguous | Specification.md | Verification table | — | Specification | TBD |
| A-004 | A:operative:judging | MissingSlot | Specification | Specification | Add performance requirement or guidance note on expected execution time bounds for the 32-deliverable baseline | Guidance C-03 states "naive traversal will be performant" but no performance assessment criteria exist to validate this assumption if scale increases | Guidance.md; Specification.md | Guidance C-03; Specification Requirements | — | Guidance | TBD |

## Matrix B — Conceptualization (4x4) — Canonical

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| B:data:necessity | data | necessity | essential fact | 1 | HAS_ITEMS | Missing essential data point |
| B:data:sufficiency | data | sufficiency | adequate evidence | 0 | NO_ITEMS | Datasheet attributes adequately evidenced with sources |
| B:data:completeness | data | completeness | comprehensive record | 1 | HAS_ITEMS | Datasheet missing some parameter values |
| B:data:consistency | data | consistency | reliable measurement | 0 | NO_ITEMS | Datasheet values internally consistent |
| B:information:necessity | information | necessity | essential signal | 0 | NO_ITEMS | Core signals (scope contingency, K-DEP-1) present across docs |
| B:information:sufficiency | information | sufficiency | adequate context | 0 | NO_ITEMS | Context envelope and descriptions provide adequate framing |
| B:information:completeness | information | completeness | comprehensive account | 0 | NO_ITEMS | Documents cover the feature comprehensively |
| B:information:consistency | information | consistency | coherent message | 0 | NO_ITEMS | Messaging consistent across documents |
| B:knowledge:necessity | knowledge | necessity | fundamental understanding | 0 | NO_ITEMS | Dependency model, graph theory concepts adequately explained |
| B:knowledge:sufficiency | knowledge | sufficiency | competent expertise | 0 | NO_ITEMS | Guidance provides sufficient expertise context |
| B:knowledge:completeness | knowledge | completeness | thorough mastery | 1 | HAS_ITEMS | Direction normalization rules not in Specification |
| B:knowledge:consistency | knowledge | consistency | coherent understanding | 0 | NO_ITEMS | Understanding of two-class edge model consistent |
| B:wisdom:necessity | wisdom | necessity | essential discernment | 0 | NO_ITEMS | Trade-offs section provides essential discernment |
| B:wisdom:sufficiency | wisdom | sufficiency | adequate judgment | 0 | NO_ITEMS | Design decisions flagged as TBD for human judgment |
| B:wisdom:completeness | wisdom | completeness | holistic insight | 0 | NO_ITEMS | Guidance covers full scope of design considerations |
| B:wisdom:consistency | wisdom | consistency | principled reasoning | 0 | NO_ITEMS | Reasoning grounded in framework invariants throughout |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| B-001 | B:data:necessity | MissingSlot | Datasheet | Datasheet | Add "Responsible Party" as a tracked attribute with value (currently TBD in Identification table with no path to resolution) | Essential fact: who is responsible for this deliverable is undefined; this is distinct from the language/runtime TBD because it has no ASSUMPTION or decision path noted | Datasheet.md | Identification table, "Responsible Party" row | — | Human decision | TBD |
| B-002 | B:data:completeness | MissingSlot | Datasheet | Datasheet | Add explicit attribute for supported Dependencies.csv column set (list the v3.1 columns the tool will parse) so the Datasheet is self-contained on input schema | Datasheet references "v3.1 schema" but does not enumerate the columns; a reader must consult SPEC.md Section 6 to know what the tool actually parses | Datasheet.md | Attributes table | — | Datasheet | TBD |
| B-003 | B:knowledge:completeness | Normalization | Guidance | Specification | Promote direction normalization rule (INBOUND/OUTBOUND to UPSTREAM/DOWNSTREAM) from Guidance C-07 into a formal requirement in Specification, or cross-reference it from REQ-02 or a new REQ | Direction normalization is operational knowledge needed for correct implementation but appears only in Guidance (C-07) and Procedure (Step A.3); Specification REQ-02 references schema compliance but does not mention legacy direction handling | Guidance.md; Procedure.md; Specification.md | Guidance C-07; Procedure Step A.3; Specification REQ-02 | — | Specification | TBD |

## Matrix C — Formulation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| C:normative:necessity | normative | necessity | obligatory conformance threshold | 1 | HAS_ITEMS | Scope contingency threshold unclear |
| C:normative:sufficiency | normative | sufficiency | regulatory proof standard | 0 | NO_ITEMS | Standards table in Spec provides proof standard |
| C:normative:completeness | normative | completeness | exhaustive compliance coverage | 1 | HAS_ITEMS | Gap in coverage |
| C:normative:consistency | normative | consistency | regulatory coherence assurance | 0 | NO_ITEMS | Cross-references to CONTRACT.md invariants are consistent |
| C:operative:necessity | operative | necessity | critical operational precondition | 0 | NO_ITEMS | Prerequisites tables in Procedure are comprehensive |
| C:operative:sufficiency | operative | sufficiency | operational readiness validation | 0 | NO_ITEMS | Procedure Part B prerequisites cover readiness |
| C:operative:completeness | operative | completeness | exhaustive operational scope | 0 | NO_ITEMS | Steps A.1-A.10 and B.1-B.3 cover operational scope |
| C:operative:consistency | operative | consistency | systematic operational reliability | 1 | HAS_ITEMS | Procedure gap on error recovery |
| C:evaluative:necessity | evaluative | necessity | intrinsic value criterion | 0 | NO_ITEMS | Value proposition clear in Guidance Purpose |
| C:evaluative:sufficiency | evaluative | sufficiency | justified merit assessment | 0 | NO_ITEMS | Trade-offs section justifies design choices |
| C:evaluative:completeness | evaluative | completeness | holistic merit accounting | 0 | NO_ITEMS | Considerations C-01 through C-07 cover merit dimensions |
| C:evaluative:consistency | evaluative | consistency | principled valuation coherence | 0 | NO_ITEMS | Value framing coherent with framework principles |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| C-001 | C:normative:necessity | WeakStatement | Specification | Specification | Strengthen contingency clause: specify what happens to this specification if SOW-035 is flipped to OUT (is the deliverable cancelled, archived, or deferred?) — currently only says "applies only if scope is flipped to IN" | The obligatory conformance threshold is ambiguous on the negative case; implementers and orchestrators need to know the disposition if scope is rejected, not just the positive activation condition | Specification.md | Scope > Contingency | — | Specification | TBD |
| C-002 | C:normative:completeness | VerificationGap | Specification | Specification | Add verification approach for direction normalization (legacy INBOUND/OUTBOUND values correctly mapped to UPSTREAM/DOWNSTREAM) — Procedure verification table includes this but Specification verification table does not | Exhaustive compliance coverage requires that every behavioral requirement has a verification approach; direction normalization is exercised in Procedure Step A.3 and tested in Procedure verification but absent from Specification verification table | Specification.md; Procedure.md | Specification Verification table; Procedure Verification table, "Legacy direction normalization" row | — | Specification | TBD |
| C-003 | C:operative:consistency | MissingSlot | Procedure | Procedure | Add error recovery/retry guidance to Part B: what should the operator do if the tool crashes mid-traversal or produces partial output? | Systematic operational reliability requires that the procedure address not just the happy path but also failure modes; Part B Steps B.1-B.3 assume successful execution | Procedure.md | Part B — Using the Tool | — | Procedure | TBD |

## Matrix F — Requirements (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| F:normative:necessity | normative | necessity | authoritative compliance mandate | 0 | NO_ITEMS | REQ-01 through REQ-14 constitute clear mandates |
| F:normative:sufficiency | normative | sufficiency | mandated evidentiary sufficiency | 1 | HAS_ITEMS | Evidence gap |
| F:normative:completeness | normative | completeness | saturated regulatory completeness | 1 | HAS_ITEMS | Requirements coverage gap |
| F:normative:consistency | normative | consistency | harmonized regulatory uniformity | 0 | NO_ITEMS | Requirements use consistent SHALL/MUST/SHOULD language |
| F:operative:necessity | operative | necessity | foundational execution dependency | 1 | HAS_ITEMS | Dependency gap |
| F:operative:sufficiency | operative | sufficiency | demonstrated operational preparedness | 0 | NO_ITEMS | Prerequisites tables adequate |
| F:operative:completeness | operative | completeness | exhaustive process completeness | 0 | NO_ITEMS | Procedure steps comprehensive |
| F:operative:consistency | operative | consistency | principled operational consistency | 0 | NO_ITEMS | Procedure consistent with Specification |
| F:evaluative:necessity | evaluative | necessity | fundamental merit imperative | 0 | NO_ITEMS | Value proposition established |
| F:evaluative:sufficiency | evaluative | sufficiency | justified valuation standard | 0 | NO_ITEMS | Trade-offs justify design choices |
| F:evaluative:completeness | evaluative | completeness | comprehensive valuation totality | 0 | NO_ITEMS | Considerations section complete |
| F:evaluative:consistency | evaluative | consistency | unified valuation integrity | 0 | NO_ITEMS | Value framing unified |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| F-001 | F:normative:sufficiency | WeakStatement | Specification | Specification | Clarify REQ-07 JSON schema: the requirement says "at minimum" for nodes/edges/metadata but the actual required fields are partially marked TBD and partially specified in Procedure Step A.2 — consolidate the authoritative field list in the requirement | Mandated evidentiary sufficiency requires that normative requirements be specific enough to verify; REQ-07 defers schema detail while Procedure A.2 proposes a detailed schema, creating ambiguity about which is authoritative | Specification.md; Procedure.md | Specification REQ-07; Procedure Step A.2 | — | Specification | TBD |
| F-002 | F:normative:completeness | MissingSlot | Specification | Specification | Add requirement for logging/reporting behavior: define what the tool outputs to stderr or a log channel for warnings, schema mismatches, and skipped files (distinct from the JSON analysis.warnings output) | Saturated regulatory completeness: REQ-02 says files SHOULD be "reported as warnings" but no requirement specifies the reporting channel, format, or verbosity level for operational diagnostics | Specification.md | REQ-02 Note | — | Specification | TBD |
| F-003 | F:operative:necessity | TBD_Question | Multi | TBD | Determine whether DEL-08-02 (Dependencies.csv Linter) and DEL-08-03 (Folder Structure Validator) are execution dependencies for this deliverable — Specification excludes their scope but does not clarify whether their outputs are prerequisites for meaningful graph generation | Foundational execution dependency: the graph generator excludes linting and structure validation from scope but does not state whether it assumes those tools have already run; if registers contain invalid data, the graph generator's behavior is underspecified | Specification.md; Datasheet.md | Specification Scope > Excluded; Datasheet Conditions table | — | Human decision | TBD |

## Matrix D — Objectives (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| D:normative:guiding | normative | guiding | binding prescriptive governance | 0 | NO_ITEMS | Governance framework (CONTRACT.md invariants) well-referenced |
| D:normative:applying | normative | applying | enforced evidentiary practice | 1 | HAS_ITEMS | Gap in enforcement mechanism |
| D:normative:judging | normative | judging | definitive conformance ruling | 0 | NO_ITEMS | Verification approaches define conformance checks |
| D:normative:reviewing | normative | reviewing | resolved compliance inspection | 0 | NO_ITEMS | Procedure verification table provides inspection steps |
| D:operative:guiding | operative | guiding | resolved procedural foundation | 0 | NO_ITEMS | Procedure Part A provides clear foundation |
| D:operative:applying | operative | applying | confirmed execution delivery | 1 | HAS_ITEMS | Delivery confirmation gap |
| D:operative:judging | operative | judging | resolved performance verdict | 0 | NO_ITEMS | Verification checks adequate for scope |
| D:operative:reviewing | operative | reviewing | systematic consistency examination | 0 | NO_ITEMS | Procedure verification covers consistency |
| D:evaluative:guiding | evaluative | guiding | resolved value direction | 0 | NO_ITEMS | Guidance Purpose resolves value direction |
| D:evaluative:applying | evaluative | applying | enacted merit benchmark | 0 | NO_ITEMS | Trade-offs establish benchmarks |
| D:evaluative:judging | evaluative | judging | definitive worth adjudication | 1 | HAS_ITEMS | Missing success criteria |
| D:evaluative:reviewing | evaluative | reviewing | resolved quality assurance review | 0 | NO_ITEMS | Verification table covers QA review |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| D-001 | D:normative:applying | VerificationGap | Specification | Specification | Add verification approach for REQ-13 (Output Persistence) that addresses the conditional nature: specify how to verify the requirement when file output IS implemented vs. when it is NOT | Enforced evidentiary practice: REQ-13 is conditional ("If the tool writes its output to a file...") but the verification table says "If file output is implemented, verify it follows snapshot conventions" without specifying what constitutes passing verification when file output is NOT implemented | Specification.md | Verification table, REQ-13 row | — | Specification | TBD |
| D-002 | D:operative:applying | TBD_Question | Multi | Datasheet | Record the human design decision on output location (Guidance C-04 options: _Aggregation/, _Scripts/, stdout, _Reconciliation/) — this decision gates Procedure Steps A.6, A.10, and Specification REQ-13 | Confirmed execution delivery requires that the output destination is decided before implementation can proceed; three separate documents reference this TBD | Guidance.md; Specification.md; Procedure.md | Guidance C-04; Specification REQ-13; Procedure Step A.10 | — | Human decision | TBD |
| D-003 | D:evaluative:judging | RationaleGap | Guidance | Guidance | Add success criteria or value metrics: define what "good" graph output looks like beyond functional correctness (e.g., accuracy relative to known dependency state, visualization clarity thresholds, time-to-insight for stakeholders) | Definitive worth adjudication requires criteria for judging whether the tool delivers its intended value; current documents define functional requirements but not how to judge whether the tool achieves its purpose of "project-level visibility" (Guidance Purpose) | Guidance.md | Purpose section | — | Guidance | TBD |

## Matrix K — Transpose of D (4x3)

Note: Matrix K is the transpose of Matrix D. Per the agent instructions, the seven matrices to lens are A, B, C, F, D, X, E. Matrix K is an intermediate construction artifact used to derive X and is not in the required lens set. It is not lensed separately.

## Matrix X — Verification (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| X:guiding:necessity | guiding | necessity | authoritative foundational standard | 0 | NO_ITEMS | Standards table in Spec provides foundational standards |
| X:guiding:sufficiency | guiding | sufficiency | substantiated directional adequacy | 0 | NO_ITEMS | Guidance adequately substantiated with sources |
| X:guiding:completeness | guiding | completeness | exhaustive directional coverage | 1 | HAS_ITEMS | Gap in guidance coverage |
| X:guiding:consistency | guiding | consistency | unified directional coherence | 0 | NO_ITEMS | Direction/guidance consistent across documents |
| X:applying:necessity | applying | necessity | enacted prerequisite enforcement | 1 | HAS_ITEMS | Prerequisite enforcement gap |
| X:applying:sufficiency | applying | sufficiency | confirmed practical sufficiency | 0 | NO_ITEMS | Practice detail sufficient for current scope |
| X:applying:completeness | applying | completeness | exhaustive practical coverage | 0 | NO_ITEMS | Steps and requirements cover practical scope |
| X:applying:consistency | applying | consistency | dependable application discipline | 0 | NO_ITEMS | Application guidance consistent |
| X:judging:necessity | judging | necessity | critical adjudicative threshold | 1 | HAS_ITEMS | Missing threshold definition |
| X:judging:sufficiency | judging | sufficiency | substantiated adjudicative sufficiency | 0 | NO_ITEMS | Verification approaches substantiated |
| X:judging:completeness | judging | completeness | exhaustive adjudicative scope | 0 | NO_ITEMS | Verification covers all requirements |
| X:judging:consistency | judging | consistency | principled adjudicative coherence | 0 | NO_ITEMS | Verification methods coherent |
| X:reviewing:necessity | reviewing | necessity | obligatory scrutiny threshold | 0 | NO_ITEMS | Review obligations defined in verification |
| X:reviewing:sufficiency | reviewing | sufficiency | substantiated scrutiny adequacy | 0 | NO_ITEMS | Review detail adequate |
| X:reviewing:completeness | reviewing | completeness | exhaustive scrutiny coverage | 1 | HAS_ITEMS | Gap in review scope |
| X:reviewing:consistency | reviewing | consistency | principled scrutiny integrity | 0 | NO_ITEMS | Review approach principled and consistent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| X-001 | X:guiding:completeness | RationaleGap | Guidance | Guidance | Add consideration for versioning strategy: when the tool evolves (new output fields, changed CLI flags), how should backward compatibility be handled for JSON consumers like DEL-08-07? | Exhaustive directional coverage: Guidance covers current design considerations but does not address forward evolution; since DEL-08-07 depends on JSON output schema, versioning guidance is needed to prevent breaking downstream consumers | Guidance.md | Considerations section (after C-07) | — | Guidance | TBD |
| X-002 | X:applying:necessity | Normalization | Multi | Guidance | Standardize terminology for "execution root" vs. "EXECUTION_ROOT" — Datasheet uses `{EXECUTION_ROOT}`, Specification uses "execution root" (lowercase), Procedure uses both forms; add a vocabulary note in Guidance | Enacted prerequisite enforcement: inconsistent naming of the primary input path could cause confusion in implementation or documentation references | Datasheet.md; Specification.md; Procedure.md | Datasheet Construction table; Specification REQ-01; Procedure Step A.3 | — | Guidance | TBD |
| X-003 | X:judging:necessity | WeakStatement | Specification | Specification | Clarify REQ-09 cycle detection: specify whether the tool MUST detect ALL cycles or MAY report only the first cycle found; specify whether the tool should halt or continue after detecting a cycle | Critical adjudicative threshold: REQ-09 says "detect cycles" and "report them" but does not specify the completeness of detection or the tool's behavior upon detection, making pass/fail adjudication ambiguous | Specification.md | REQ-09 | — | Specification | TBD |
| X-004 | X:reviewing:completeness | VerificationGap | Procedure | Procedure | Add verification check for package-scoped filtering (--package flag from Step A.8): verify that filtering to a single package produces correct subgraph | Exhaustive scrutiny coverage: Procedure verification table tests full-graph scenarios but does not test the package-scoped filtering capability described in Procedure Step A.8 and Guidance Examples | Procedure.md | Verification table; Step A.8 | — | Procedure | TBD |

## Matrix E — Evaluation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| E:normative:necessity | normative | necessity | mandatory governance checkpoint | 0 | NO_ITEMS | Governance checkpoints (scope flip, K-DEP-1) are defined |
| E:normative:sufficiency | normative | sufficiency | confirmed regulatory sufficiency | 0 | NO_ITEMS | Standards and invariants sufficiently referenced |
| E:normative:completeness | normative | completeness | saturated regulatory scope | 0 | NO_ITEMS | Regulatory scope covered by 14 requirements |
| E:normative:consistency | normative | consistency | unified regulatory integrity | 0 | NO_ITEMS | Regulatory references unified across documents |
| E:operative:necessity | operative | necessity | confirmed operational foundation | 0 | NO_ITEMS | Operational foundation confirmed by prerequisites |
| E:operative:sufficiency | operative | sufficiency | demonstrated execution adequacy | 1 | HAS_ITEMS | Adequacy gap |
| E:operative:completeness | operative | completeness | saturated operational completeness | 0 | NO_ITEMS | Operational steps comprehensive |
| E:operative:consistency | operative | consistency | principled operational dependability | 0 | NO_ITEMS | Operational guidance dependable and consistent |
| E:evaluative:necessity | evaluative | necessity | foundational merit threshold | 0 | NO_ITEMS | Merit threshold established by value proposition |
| E:evaluative:sufficiency | evaluative | sufficiency | demonstrated merit sufficiency | 0 | NO_ITEMS | Merit demonstration adequate for pre-scope-flip state |
| E:evaluative:completeness | evaluative | completeness | holistic merit completeness | 1 | HAS_ITEMS | Gap in holistic accounting |
| E:evaluative:consistency | evaluative | consistency | trustworthy merit coherence | 0 | NO_ITEMS | Merit coherence maintained |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| E-001 | E:operative:sufficiency | Normalization | Datasheet | Datasheet | Normalize ASSUMPTION markers: Datasheet uses **ASSUMPTION** in bold, Specification uses **ASSUMPTION** in parens, Guidance uses **ASSUMPTION:** with colon — adopt a single convention and apply consistently | Demonstrated execution adequacy requires that TBD/ASSUMPTION markers follow a uniform convention so they can be reliably tracked and resolved; three different formats across documents reduce scanability | Datasheet.md; Specification.md; Guidance.md | Datasheet Attributes table; Specification REQ-07 through REQ-14; Guidance Considerations section | — | Guidance | TBD |
| E-002 | E:evaluative:completeness | MissingSlot | Guidance | Guidance | Add consideration for accessibility of Mermaid output: note whether Mermaid diagrams should include alt-text, subgraph grouping by package, or color-coding conventions for ANCHOR vs. EXECUTION edges | Holistic merit completeness: the human-readable output format (Mermaid) is described functionally but not evaluated for usability/accessibility; since the tool's value proposition centers on "project-level visibility" (Guidance Purpose), the quality of that visibility deserves explicit consideration | Guidance.md | Considerations section; also relates to Specification REQ-08 | — | Guidance | TBD |
