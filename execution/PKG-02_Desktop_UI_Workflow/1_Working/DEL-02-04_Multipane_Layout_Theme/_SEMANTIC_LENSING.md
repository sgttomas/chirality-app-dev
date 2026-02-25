# Semantic Lensing Register: DEL-02-04 Multi-pane Layout + Theme Hardening

**Generated:** 2026-02-21
**Deliverable Folder:** /Users/ryan/ai-env/projects/chirality-app-dev/execution/PKG-02_Desktop_UI_Workflow/1_Working/DEL-02-04_Multipane_Layout_Theme/
**Warnings:** None

**Inputs Read:**
- _CONTEXT.md — `execution/PKG-02_Desktop_UI_Workflow/1_Working/DEL-02-04_Multipane_Layout_Theme/_CONTEXT.md`
- _STATUS.md — `execution/PKG-02_Desktop_UI_Workflow/1_Working/DEL-02-04_Multipane_Layout_Theme/_STATUS.md`
- _SEMANTIC.md — `execution/PKG-02_Desktop_UI_Workflow/1_Working/DEL-02-04_Multipane_Layout_Theme/_SEMANTIC.md`
- Datasheet.md — `execution/PKG-02_Desktop_UI_Workflow/1_Working/DEL-02-04_Multipane_Layout_Theme/Datasheet.md`
- Specification.md — `execution/PKG-02_Desktop_UI_Workflow/1_Working/DEL-02-04_Multipane_Layout_Theme/Specification.md`
- Guidance.md — `execution/PKG-02_Desktop_UI_Workflow/1_Working/DEL-02-04_Multipane_Layout_Theme/Guidance.md`
- Procedure.md — `execution/PKG-02_Desktop_UI_Workflow/1_Working/DEL-02-04_Multipane_Layout_Theme/Procedure.md`
- _REFERENCES.md — `execution/PKG-02_Desktop_UI_Workflow/1_Working/DEL-02-04_Multipane_Layout_Theme/_REFERENCES.md`

**Purpose:** Apply CHIRALITY_FRAMEWORK matrix cells as lenses over the production documents, capturing warranted enrichment inputs for a later enrichment pass.

---

## Summary

- Total warranted items: 22
- By document:
  - Datasheet: 7
  - Specification: 8
  - Guidance: 3
  - Procedure: 3
  - Multi: 1
- By matrix:
  - A: 5  B: 3  C: 2  F: 3  D: 2  X: 4  E: 3
- By type:
  - Conflict: 1
  - VerificationGap: 4
  - MissingSlot: 8
  - WeakStatement: 3
  - RationaleGap: 2
  - Normalization: 2
  - TBD_Question: 2
  - MatrixError: 0
- Notable conflicts: 1
- Matrix parse errors: 0

---

## Matrix A -- Orientation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| A:normative:guiding | normative | guiding | prescriptive direction | 1 | HAS_ITEMS | Accessibility requirements lack prescriptive direction |
| A:normative:applying | normative | applying | mandatory practice | 1 | HAS_ITEMS | Keyboard shortcut specifics unresolved |
| A:normative:judging | normative | judging | compliance determination | 1 | HAS_ITEMS | WCAG applicability undetermined |
| A:normative:reviewing | normative | reviewing | regulatory audit | 0 | NO_ITEMS | Verification table covers audit adequately |
| A:operative:guiding | operative | guiding | procedural direction | 1 | HAS_ITEMS | Upstream dependency direction missing |
| A:operative:applying | operative | applying | practical execution | 0 | NO_ITEMS | Steps are present and actionable |
| A:operative:judging | operative | judging | performance assessment | 0 | NO_ITEMS | Verification checks are present |
| A:operative:reviewing | operative | reviewing | process audit | 0 | NO_ITEMS | Records section covers audit trail |
| A:evaluative:guiding | evaluative | guiding | value orientation | 1 | HAS_ITEMS | No rationale for SHOULD vs MUST on REQ-LAYOUT-05 |
| A:evaluative:applying | evaluative | applying | merit application | 0 | NO_ITEMS | Purpose and principles in Guidance adequate |
| A:evaluative:judging | evaluative | judging | worth determination | 0 | NO_ITEMS | Verification provides pass/fail criteria |
| A:evaluative:reviewing | evaluative | reviewing | quality appraisal | 0 | NO_ITEMS | Quality review steps present in Procedure Phase 4 |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A-001 | A:normative:guiding | MissingSlot | Specification | Specification | Add prescriptive direction for accessibility requirements: confirm WCAG 2.1 AA applicability and derive concrete requirements, or record TBD with escalation path | Specification lists WCAG 2.1 AA as "ASSUMPTION: likely applicable" with no prescriptive resolution; this leaves implementers without direction on an entire requirements category | Specification.md | Standards table, WCAG row | -- | Human / project governance | TBD |
| A-002 | A:normative:applying | MissingSlot | Datasheet | Specification | Define specific keyboard shortcuts for pane resize (e.g., modifier + arrow keys) and record in Datasheet attributes | REQ-LAYOUT-03 mandates keyboard resize but no keyboard shortcut conventions are specified anywhere; Procedure Step 2.2 also flags "TBD: Define specific keyboard shortcuts" | Specification.md; Datasheet.md; Procedure.md | REQ-LAYOUT-03; Step 2.2 | -- | Human / UX design | TBD |
| A-003 | A:normative:judging | TBD_Question | Specification | Specification | Resolve WCAG 2.1 AA applicability: confirm or reject, then update Standards table and add/remove corresponding requirements | Cannot determine compliance until applicability is ruled on; this blocks acceptance criteria for accessibility-related behavior (contrast ratios, keyboard navigation announcements, etc.) | Specification.md | Standards table, WCAG row | -- | Human / project governance | TBD |
| A-004 | A:operative:guiding | MissingSlot | Procedure | Procedure | Add prerequisite check or note confirming upstream dependency status (DEL-02-01 FileTree, DEL-02-02 navigation, DEL-02-03 toolkit) before beginning Phase 2 layout implementation | Procedure notes "No upstream dependencies have been declared" and flags this as an ASSUMPTION; no procedural direction exists for how to proceed if implicit dependencies are not met | Procedure.md | Prerequisites > Required Upstream Deliverables | -- | ORCHESTRATOR / dependency resolution | TBD |
| A-005 | A:evaluative:guiding | RationaleGap | Specification | Guidance | Add rationale for why REQ-LAYOUT-05 (minimum pane size) is SHOULD rather than MUST, and clarify conditions under which it could be relaxed | REQ-LAYOUT-05 uses SHOULD while all other layout requirements use MUST; no guidance explains the distinction, which could lead implementers to deprioritize minimum pane size enforcement | Specification.md; Guidance.md | REQ-LAYOUT-05; (no corresponding Guidance section) | -- | Human / design authority | TBD |

---

## Matrix B -- Conceptualization (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| B:data:necessity | data | necessity | essential fact | 1 | HAS_ITEMS | Core layout data points TBD |
| B:data:sufficiency | data | sufficiency | adequate evidence | 1 | HAS_ITEMS | CSS approach and component library unspecified |
| B:data:completeness | data | completeness | comprehensive record | 1 | HAS_ITEMS | Dark mode color values absent |
| B:data:consistency | data | consistency | reliable measurement | 0 | NO_ITEMS | Measurement references are consistent where present |
| B:information:necessity | information | necessity | essential signal | 0 | NO_ITEMS | Core feature signals present in PLAN references |
| B:information:sufficiency | information | sufficiency | adequate context | 0 | NO_ITEMS | Context adequate across documents |
| B:information:completeness | information | completeness | comprehensive account | 0 | NO_ITEMS | Feature accounts are comprehensive for stated scope |
| B:information:consistency | information | consistency | coherent message | 0 | NO_ITEMS | Messaging is coherent across documents |
| B:knowledge:necessity | knowledge | necessity | fundamental understanding | 0 | NO_ITEMS | Domain understanding is adequate |
| B:knowledge:sufficiency | knowledge | sufficiency | competent expertise | 0 | NO_ITEMS | Technical knowledge context sufficient |
| B:knowledge:completeness | knowledge | completeness | thorough mastery | 0 | NO_ITEMS | Mastery level appropriate for current phase |
| B:knowledge:consistency | knowledge | consistency | coherent understanding | 0 | NO_ITEMS | Understanding consistent across docs |
| B:wisdom:necessity | wisdom | necessity | essential discernment | 0 | NO_ITEMS | Trade-off awareness present in Guidance |
| B:wisdom:sufficiency | wisdom | sufficiency | adequate judgment | 0 | NO_ITEMS | Judgment calls documented in Guidance |
| B:wisdom:completeness | wisdom | completeness | holistic insight | 0 | NO_ITEMS | Holistic view adequate for current scope |
| B:wisdom:consistency | wisdom | consistency | principled reasoning | 0 | NO_ITEMS | Reasoning consistent with DIRECTIVE principles |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| B-001 | B:data:necessity | MissingSlot | Datasheet | Datasheet | Record essential data values for: pane configuration (count, nesting), minimum pane dimensions, default pane proportions, and layout state persistence approach | Datasheet Attributes table has four TBD entries for core layout data (Pane configuration, Minimum pane dimensions, Default pane proportions, Persistence of layout state); these are essential facts needed before implementation | Datasheet.md | Attributes > Multi-pane Layout (SOW-026) | -- | Human / codebase analysis | TBD |
| B-002 | B:data:sufficiency | MissingSlot | Datasheet | Datasheet | Record CSS/styling approach, layout mechanism (CSS Grid / Flexbox / custom), component library, and test framework selections in Datasheet Construction table | Datasheet Construction table has four TBD entries covering implementation technology choices; without these, evidence is insufficient to guide implementation decisions | Datasheet.md | Construction | -- | Human / technical lead | TBD |
| B-003 | B:data:completeness | MissingSlot | Datasheet | Datasheet | Add dark mode color values and palette to Datasheet, or reference a design token source if one exists | Datasheet addresses light mode theme attributes but dark mode values are absent; Specification REQ-THEME-07 (SHOULD) and Procedure Step 3.6 both note dark mode color values as TBD | Datasheet.md; Specification.md; Procedure.md | Conditions > Theme modes supported; REQ-THEME-07; Step 3.6 | -- | Human / design authority | TBD |

---

## Matrix C -- Formulation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| C:normative:necessity | normative | necessity | Enforceable Compliance Threshold | 1 | HAS_ITEMS | Lifecycle state inconsistency |
| C:normative:sufficiency | normative | sufficiency | Sufficient Regulatory Competence | 0 | NO_ITEMS | Regulatory references are adequate |
| C:normative:completeness | normative | completeness | Total Prescriptive Coverage | 0 | NO_ITEMS | Prescriptive coverage is complete for stated scope |
| C:normative:consistency | normative | consistency | Harmonized Regulatory Stability | 0 | NO_ITEMS | Regulatory references are stable and consistent |
| C:operative:necessity | operative | necessity | Critical Operational Foundation | 0 | NO_ITEMS | Operational foundation adequately described |
| C:operative:sufficiency | operative | sufficiency | Competent Execution Capacity | 1 | HAS_ITEMS | Test framework unresolved |
| C:operative:completeness | operative | completeness | Comprehensive Workflow Mastery | 0 | NO_ITEMS | Workflow steps comprehensive |
| C:operative:consistency | operative | consistency | Systematic Operational Integrity | 0 | NO_ITEMS | Operations consistently described |
| C:evaluative:necessity | evaluative | necessity | Fundamental Merit Criterion | 0 | NO_ITEMS | Merit criteria present via Guidance principles |
| C:evaluative:sufficiency | evaluative | sufficiency | Competent Worth Assessment | 0 | NO_ITEMS | Worth assessment adequate in Guidance |
| C:evaluative:completeness | evaluative | completeness | Holistic Quality Accounting | 0 | NO_ITEMS | Quality accounting present in verification tables |
| C:evaluative:consistency | evaluative | consistency | Principled Value Coherence | 0 | NO_ITEMS | Value statements consistent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| C-001 | C:normative:necessity | Conflict | Datasheet | Datasheet | Resolve lifecycle state: Datasheet says "OPEN" but _STATUS.md says "SEMANTIC_READY"; update Datasheet to reflect current state | Datasheet Identification table states Lifecycle State = OPEN, while _STATUS.md records Current State = SEMANTIC_READY after CHIRALITY_FRAMEWORK completion; these are incompatible claims about the same fact | Datasheet.md; _STATUS.md | Identification table > Lifecycle State; _STATUS.md > Current State | Datasheet.md#Identification (OPEN) vs _STATUS.md (SEMANTIC_READY) | _STATUS.md is authoritative for lifecycle state | TBD |
| C-002 | C:operative:sufficiency | TBD_Question | Procedure | Datasheet | Select and record test framework (e.g., Jest, Playwright, Vitest) in Datasheet Construction table and reference from Procedure prerequisites | Procedure Prerequisites lists "Test runner (TBD)" and Datasheet Construction lists "Test framework: TBD"; execution capacity cannot be verified without a test framework decision | Procedure.md; Datasheet.md | Prerequisites > Required Tools; Construction > Test framework | -- | Human / technical lead | TBD |

---

## Matrix F -- Requirements (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| F:normative:necessity | normative | necessity | Mandated Conformance Readiness | 0 | NO_ITEMS | Conformance readiness adequate for stated requirements |
| F:normative:sufficiency | normative | sufficiency | Sound Governance Adequacy | 1 | HAS_ITEMS | ASSUMPTION-tagged requirements lack governance resolution |
| F:normative:completeness | normative | completeness | Absolute Directive Accounting | 0 | NO_ITEMS | Directives accounted for |
| F:normative:consistency | normative | consistency | Systematic Mandate Integrity | 0 | NO_ITEMS | Mandates internally consistent |
| F:operative:necessity | operative | necessity | Essential Process Readiness | 1 | HAS_ITEMS | Record location TBDs unresolved |
| F:operative:sufficiency | operative | sufficiency | Verified Operational Competence | 0 | NO_ITEMS | Operational competence adequate for current phase |
| F:operative:completeness | operative | completeness | Total Procedural Command | 0 | NO_ITEMS | Procedural steps are complete |
| F:operative:consistency | operative | consistency | Coherent Execution Standard | 0 | NO_ITEMS | Execution standards coherent |
| F:evaluative:necessity | evaluative | necessity | Core Quality Prerequisite | 1 | HAS_ITEMS | REQ-THEME-07 SHOULD status weakens dark mode quality prerequisite |
| F:evaluative:sufficiency | evaluative | sufficiency | Sufficient Evaluation Competence | 0 | NO_ITEMS | Evaluation competence sufficient |
| F:evaluative:completeness | evaluative | completeness | Comprehensive Quality Mastery | 0 | NO_ITEMS | Quality coverage comprehensive for scope |
| F:evaluative:consistency | evaluative | consistency | Systematic Evaluation Integrity | 0 | NO_ITEMS | Evaluation integrity maintained |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| F-001 | F:normative:sufficiency | WeakStatement | Specification | Specification | Resolve ASSUMPTION-tagged requirements (REQ-LAYOUT-05, REQ-THEME-07) and ASSUMPTION-tagged standards (WCAG 2.1 AA): confirm, reject, or escalate each with documented rationale | Two requirements and one standard are tagged as ASSUMPTIONs; governance adequacy requires these be resolved to binding or explicitly deferred status rather than left as assumptions | Specification.md | REQ-LAYOUT-05; REQ-THEME-07; Standards table WCAG row | -- | Human / project governance | TBD |
| F-002 | F:operative:necessity | MissingSlot | Procedure | Procedure | Define specific output locations for Records: replace all "TBD" Location values in the Records table with concrete paths or naming conventions | Procedure Records table has three "TBD" location entries; without defined locations, process readiness for artifact storage is incomplete | Procedure.md | Records table | -- | Human / project conventions | TBD |
| F-003 | F:evaluative:necessity | WeakStatement | Specification | Guidance | Clarify whether dark mode parity (REQ-THEME-07 SHOULD) is a genuine quality prerequisite or an aspirational target; if prerequisite, elevate to MUST with specific acceptance criteria | REQ-THEME-07 uses SHOULD for dark mode parity; Guidance C5 implies dark mode "should at minimum maintain the same structural improvements" which sounds like a necessity, creating ambiguity about the actual quality floor | Specification.md; Guidance.md | REQ-THEME-07; C5: Theme Mode Coverage | -- | Human / design authority | TBD |

---

## Matrix D -- Objectives (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| D:normative:guiding | normative | guiding | Resolved Directive Authority | 0 | NO_ITEMS | Directive authority adequately referenced |
| D:normative:applying | normative | applying | Obligatory Governance Practice | 1 | HAS_ITEMS | Objective mapping is assumption-tagged |
| D:normative:judging | normative | judging | Enforceable Conformance Ruling | 0 | NO_ITEMS | Conformance rulings are present via verification table |
| D:normative:reviewing | normative | reviewing | Resolved Regulatory Oversight | 0 | NO_ITEMS | Oversight mechanisms present |
| D:operative:guiding | operative | guiding | Resolved Procedural Steering | 0 | NO_ITEMS | Procedural steering adequate |
| D:operative:applying | operative | applying | Resolved Implementation Practice | 0 | NO_ITEMS | Implementation practice is resolved in steps |
| D:operative:judging | operative | judging | Resolved Performance Judgment | 0 | NO_ITEMS | Performance judgment criteria present |
| D:operative:reviewing | operative | reviewing | Resolved Process Examination | 0 | NO_ITEMS | Process examination covered |
| D:evaluative:guiding | evaluative | guiding | Resolved Value Direction | 1 | HAS_ITEMS | No performance/ergonomics targets |
| D:evaluative:applying | evaluative | applying | Resolved Merit Application | 0 | NO_ITEMS | Merit application adequate in Guidance |
| D:evaluative:judging | evaluative | judging | Definitive Quality Ruling | 0 | NO_ITEMS | Quality rulings present in verification |
| D:evaluative:reviewing | evaluative | reviewing | Resolved Quality Appraisal | 0 | NO_ITEMS | Quality appraisal covered |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| D-001 | D:normative:applying | Normalization | Datasheet | Datasheet | Resolve ASSUMPTION tag on OBJ-005 mapping: confirm the objective mapping is correct and remove ASSUMPTION tag, or flag for ORCHESTRATOR resolution | Datasheet Identification table tags OBJ-005 as "ASSUMPTION (best-effort mapping via PKG-02 grouping)" while _CONTEXT.md states "Objectives: OBJ-005" without qualification; the objective mapping should be normalized to a single consistent status | Datasheet.md; _CONTEXT.md | Identification > Objectives; _CONTEXT.md > Objectives | -- | ORCHESTRATOR / decomposition authority | TBD |
| D-002 | D:evaluative:guiding | RationaleGap | Guidance | Guidance | Add a value-direction statement or measurable ergonomics target for what "professional-grade multi-pane workspace" means in practice (e.g., resize latency, layout switch speed, session comfort targets) | Guidance Purpose references "ergonomic, professional-grade multi-pane workspace" but no measurable targets or explicit value-direction criteria exist to evaluate whether the objective is achieved beyond functional pass/fail | Guidance.md | Purpose | -- | Human / UX design | TBD |

---

## Matrix X -- Verification (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| X:guiding:necessity | guiding | necessity | Guided Conformance Foundation | 0 | NO_ITEMS | Conformance foundation adequately guided |
| X:guiding:sufficiency | guiding | sufficiency | Sufficient Governance Direction | 0 | NO_ITEMS | Governance direction sufficient |
| X:guiding:completeness | guiding | completeness | Comprehensive Directive Scope | 0 | NO_ITEMS | Directive scope comprehensive |
| X:guiding:consistency | guiding | consistency | Harmonized Directive Alignment | 1 | HAS_ITEMS | Verification approach terminology inconsistent |
| X:applying:necessity | applying | necessity | Essential Conformance Practice | 1 | HAS_ITEMS | No verification for layout state persistence |
| X:applying:sufficiency | applying | sufficiency | Adequate Implementation Practice | 0 | NO_ITEMS | Implementation practice adequate |
| X:applying:completeness | applying | completeness | Total Implementation Coverage | 1 | HAS_ITEMS | Scope exclusion boundary untested |
| X:applying:consistency | applying | consistency | Coherent Implementation Standard | 0 | NO_ITEMS | Implementation standards coherent |
| X:judging:necessity | judging | necessity | Mandatory Adjudication Threshold | 0 | NO_ITEMS | Adjudication thresholds present |
| X:judging:sufficiency | judging | sufficiency | Competent Adjudication Capacity | 0 | NO_ITEMS | Adjudication capacity adequate |
| X:judging:completeness | judging | completeness | Comprehensive Adjudication Scope | 0 | NO_ITEMS | Adjudication scope covered |
| X:judging:consistency | judging | consistency | Principled Adjudication Uniformity | 0 | NO_ITEMS | Adjudication uniformly structured |
| X:reviewing:necessity | reviewing | necessity | Essential Audit Foundation | 1 | HAS_ITEMS | Regression test scope undefined |
| X:reviewing:sufficiency | reviewing | sufficiency | Adequate Verification Review | 0 | NO_ITEMS | Verification review adequate |
| X:reviewing:completeness | reviewing | completeness | Comprehensive Audit Scope | 0 | NO_ITEMS | Audit scope comprehensive |
| X:reviewing:consistency | reviewing | consistency | Harmonized Audit Coherence | 0 | NO_ITEMS | Audit coherence maintained |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| X-001 | X:guiding:consistency | Normalization | Multi | Specification | Normalize verification approach terminology: Specification Verification table uses mixed terms ("Automated test + manual inspection", "Visual inspection", "Functional test", "State test + manual inspection") while Procedure Phase 4 uses different groupings ("layout tests", "theme tests", "visual regression tests"); align terminology or cross-reference explicitly | Inconsistent verification approach naming between Specification and Procedure could cause confusion about which test types fulfill which verification IDs | Specification.md; Procedure.md | Verification table; Phase 4 | -- | Human / test lead | TBD |
| X-002 | X:applying:necessity | VerificationGap | Specification | Specification | Add verification entry for layout state persistence behavior if persistence is implemented (Datasheet attribute "Persistence of layout state: TBD"); if persistence is descoped, no verification needed | Datasheet lists "Persistence of layout state" as TBD; if implemented, no verification entry exists in Specification or Procedure for testing that layout state persists across sessions | Datasheet.md; Specification.md | Attributes > Persistence of layout state; Verification table | -- | Human / scope decision | TBD |
| X-003 | X:applying:completeness | VerificationGap | Specification | Procedure | Add verification step or smoke test confirming that scope exclusion boundaries hold: pane-hosted functional views (WORKBENCH, PIPELINE content) are not broken by layout changes | Specification Excluded section lists specific scope boundaries (e.g., "Content or internal behavior of pane-hosted functional views... beyond their layout container") but no verification entry confirms these exclusions are respected | Specification.md; Procedure.md | Excluded; Verification table | -- | Human / test lead | TBD |
| X-004 | X:reviewing:necessity | VerificationGap | Procedure | Procedure | Define specific regression test scope for adjacent deliverables (DEL-02-01, DEL-02-02, DEL-02-03): which features to smoke-test, pass criteria, and who executes | Procedure Verification table includes "No regressions in adjacent deliverables" with method "Manual smoke test" but no specific test cases, features, or pass criteria are defined for the regression scope | Procedure.md | Verification table > No regressions row | -- | Human / test lead | TBD |

---

## Matrix E -- Evaluation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| E:normative:necessity | normative | necessity | Mandated Compliance Foundation | 0 | NO_ITEMS | Compliance foundation adequate |
| E:normative:sufficiency | normative | sufficiency | Sufficient Enforcement Capability | 1 | HAS_ITEMS | Enforcement for ANSI rendering underspecified |
| E:normative:completeness | normative | completeness | Total Regulatory Authority | 0 | NO_ITEMS | Regulatory authority complete for scope |
| E:normative:consistency | normative | consistency | Principled Regulatory Harmony | 0 | NO_ITEMS | Regulatory harmony maintained |
| E:operative:necessity | operative | necessity | Essential Execution Conformance | 1 | HAS_ITEMS | GFM scope details missing from Specification |
| E:operative:sufficiency | operative | sufficiency | Adequate Operational Capacity | 0 | NO_ITEMS | Operational capacity adequate |
| E:operative:completeness | operative | completeness | Complete Operational Scope | 0 | NO_ITEMS | Operational scope complete |
| E:operative:consistency | operative | consistency | Principled Operational Coherence | 0 | NO_ITEMS | Operational coherence maintained |
| E:evaluative:necessity | evaluative | necessity | Critical Quality Baseline | 1 | HAS_ITEMS | No contrast ratio or readability metric |
| E:evaluative:sufficiency | evaluative | sufficiency | Competent Quality Judgment | 0 | NO_ITEMS | Quality judgment adequate |
| E:evaluative:completeness | evaluative | completeness | Comprehensive Quality Accounting | 0 | NO_ITEMS | Quality accounting comprehensive |
| E:evaluative:consistency | evaluative | consistency | Principled Quality Consistency | 0 | NO_ITEMS | Quality consistency maintained |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| E-001 | E:normative:sufficiency | WeakStatement | Specification | Specification | Clarify REQ-THEME-04 ANSI rendering scope: specify which ANSI escape sequences must be supported (e.g., SGR color codes, bold/underline, 256-color, true color) and define fallback behavior for unsupported sequences | REQ-THEME-04 requires "ANSI fallback for terminal-style tool output" but does not specify which ANSI sequences must be rendered; enforcement capability is insufficient without a defined scope of ANSI support | Specification.md | REQ-THEME-04 | -- | Human / technical lead | TBD |
| E-002 | E:operative:necessity | VerificationGap | Specification | Specification | Add explicit GFM element list to REQ-THEME-03 acceptance criteria (tables, task lists, strikethrough, autolinks, fenced code blocks with syntax highlighting) or cross-reference Guidance C6 | Guidance C6 enumerates specific GFM extensions (tables, task lists, strikethrough, autolinks, fenced code blocks with language-tagged syntax highlighting) but Specification REQ-THEME-03 only says "GitHub-flavored markdown" and the verification entry REQ-THEME-03-V lists some but not all of these; execution conformance requires normative enumeration | Specification.md; Guidance.md | REQ-THEME-03; REQ-THEME-03-V; C6: Markdown Rendering Scope | -- | Human / specification author | TBD |
| E-003 | E:evaluative:necessity | MissingSlot | Specification | Specification | Add measurable readability criterion for REQ-THEME-01 (e.g., minimum contrast ratio value) or reference applicable standard, to establish a critical quality baseline for "readability" | REQ-THEME-01 requires "non-orange accent text for readability" but provides no measurable criterion for what constitutes readable; verification REQ-THEME-01-V says "text is readable" without a metric; this leaves the quality baseline subjective | Specification.md | REQ-THEME-01; REQ-THEME-01-V | -- | Human / design authority + accessibility lead | TBD |
