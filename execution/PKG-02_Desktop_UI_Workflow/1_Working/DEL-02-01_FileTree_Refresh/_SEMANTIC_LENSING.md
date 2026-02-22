# Semantic Lensing Register: DEL-02-01 FileTree Refresh & External-Change Detection

**Generated:** 2026-02-21
**Deliverable Folder:** /Users/ryan/ai-env/projects/chirality-app-dev/execution/PKG-02_Desktop_UI_Workflow/1_Working/DEL-02-01_FileTree_Refresh/
**Warnings:** None

**Inputs Read:**
- _CONTEXT.md — `execution/PKG-02_Desktop_UI_Workflow/1_Working/DEL-02-01_FileTree_Refresh/_CONTEXT.md`
- _STATUS.md — `execution/PKG-02_Desktop_UI_Workflow/1_Working/DEL-02-01_FileTree_Refresh/_STATUS.md`
- _SEMANTIC.md — `execution/PKG-02_Desktop_UI_Workflow/1_Working/DEL-02-01_FileTree_Refresh/_SEMANTIC.md`
- Datasheet.md — `execution/PKG-02_Desktop_UI_Workflow/1_Working/DEL-02-01_FileTree_Refresh/Datasheet.md`
- Specification.md — `execution/PKG-02_Desktop_UI_Workflow/1_Working/DEL-02-01_FileTree_Refresh/Specification.md`
- Guidance.md — `execution/PKG-02_Desktop_UI_Workflow/1_Working/DEL-02-01_FileTree_Refresh/Guidance.md`
- Procedure.md — `execution/PKG-02_Desktop_UI_Workflow/1_Working/DEL-02-01_FileTree_Refresh/Procedure.md`
- _REFERENCES.md — `execution/PKG-02_Desktop_UI_Workflow/1_Working/DEL-02-01_FileTree_Refresh/_REFERENCES.md`

**Purpose:** Apply CHIRALITY_FRAMEWORK matrix cells as lenses over the production documents, capturing warranted enrichment inputs for a later enrichment pass.

---

## Summary

- Total warranted items: 24
- By document:
  - Datasheet: 5
  - Specification: 9
  - Guidance: 4
  - Procedure: 3
  - Multi: 3
- By matrix:
  - A: 4  B: 3  C: 3  F: 4  D: 3  X: 4  E: 3
- By type:
  - Conflict: 0
  - VerificationGap: 5
  - MissingSlot: 7
  - WeakStatement: 4
  - RationaleGap: 3
  - Normalization: 3
  - TBD_Question: 2
  - MatrixError: 0
- Notable conflicts: 0
- Matrix parse errors: 0

---

## Matrix A -- Orientation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| A:normative:guiding | normative | guiding | prescriptive direction | 1 | HAS_ITEMS | TBD polling interval lacks prescriptive direction |
| A:normative:applying | normative | applying | mandatory practice | 1 | HAS_ITEMS | REQ-06 performance thresholds are TBD |
| A:normative:judging | normative | judging | compliance determination | 1 | HAS_ITEMS | No acceptance criteria for expand/collapse preservation |
| A:normative:reviewing | normative | reviewing | regulatory audit | 0 | NO_ITEMS | Verification matrix present and traced to requirements |
| A:operative:guiding | operative | guiding | procedural direction | 0 | NO_ITEMS | Procedure steps are well-sequenced |
| A:operative:applying | operative | applying | practical execution | 0 | NO_ITEMS | Implementation steps are actionable |
| A:operative:judging | operative | judging | performance assessment | 1 | HAS_ITEMS | Performance test thresholds are TBD |
| A:operative:reviewing | operative | reviewing | process audit | 0 | NO_ITEMS | Cross-reference verification step exists (Procedure Step 8) |
| A:evaluative:guiding | evaluative | guiding | value orientation | 0 | NO_ITEMS | Guidance clearly articulates value via P1 and P2 |
| A:evaluative:applying | evaluative | applying | merit application | 0 | NO_ITEMS | SOW-022 alignment is clear |
| A:evaluative:judging | evaluative | judging | worth determination | 0 | NO_ITEMS | Trade-offs table in Guidance covers key decisions |
| A:evaluative:reviewing | evaluative | reviewing | quality appraisal | 0 | NO_ITEMS | Quality considerations covered in Guidance C4 |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A-001 | A:normative:guiding | WeakStatement | Specification | Specification | Add a default polling interval value or explicit range constraint to REQ-01 (currently "TBD") | REQ-01 states polling interval "MUST be configurable or set to a reasonable default" but the default is TBD; this leaves prescriptive direction incomplete for implementers | Specification.md | REQ-01: Periodic Polling Refresh | | Specification.md | TBD |
| A-002 | A:normative:applying | TBD_Question | Specification | Specification | Resolve TBD: define threshold values for tree depth/node-count limit in REQ-06 (or explicitly state "no limit") | REQ-06 ASSUMPTION states a tree depth or node-count limit "MAY be needed" with threshold values TBD; mandatory practice cannot be applied without bounds | Specification.md | REQ-06: Performance and Resource Safety | | Human/Implementation profiling | TBD |
| A-003 | A:normative:judging | VerificationGap | Specification | Specification | Add acceptance criterion for expand/collapse state preservation across refresh cycles | Guidance C4 and Procedure Step 2.3 both require preserving expand/collapse state, but the Specification verification matrix has no acceptance criterion for this behavior | Specification.md | Verification table | | Specification.md | TBD |
| A-004 | A:operative:judging | WeakStatement | Procedure | Procedure | Define concrete performance test thresholds in Step 6.4 (file count and max scan duration) instead of "TBD number of files" and "TBD milliseconds" | Procedure Step 6.4 performance tests use TBD for both the directory size and timing thresholds, making the assessment non-executable | Procedure.md | Step 6: Write Tests > 6.4 | | Human/Implementation profiling | TBD |

---

## Matrix B -- Conceptualization (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| B:data:necessity | data | necessity | essential fact | 1 | HAS_ITEMS | Polling interval default value is an essential fact not yet established |
| B:data:sufficiency | data | sufficiency | adequate evidence | 0 | NO_ITEMS | Source references are adequately cited across documents |
| B:data:completeness | data | completeness | comprehensive record | 1 | HAS_ITEMS | Datasheet missing IPC channel/API naming |
| B:data:consistency | data | consistency | reliable measurement | 0 | NO_ITEMS | Consistent references to same source docs |
| B:information:necessity | information | necessity | essential signal | 0 | NO_ITEMS | SOW-022 and PLAN SS 2 signals are present |
| B:information:sufficiency | information | sufficiency | adequate context | 0 | NO_ITEMS | Context is adequate for implementation |
| B:information:completeness | information | completeness | comprehensive account | 0 | NO_ITEMS | Scope included/excluded is clear |
| B:information:consistency | information | consistency | coherent message | 0 | NO_ITEMS | Documents present a coherent message about polling + focus/visibility |
| B:knowledge:necessity | knowledge | necessity | fundamental understanding | 0 | NO_ITEMS | Filesystem-as-database principle is well-established |
| B:knowledge:sufficiency | knowledge | sufficiency | competent expertise | 0 | NO_ITEMS | Sufficient expertise context provided |
| B:knowledge:completeness | knowledge | completeness | thorough mastery | 1 | HAS_ITEMS | Debounce strategy underdefined |
| B:knowledge:consistency | knowledge | consistency | coherent understanding | 0 | NO_ITEMS | Understanding is coherent across documents |
| B:wisdom:necessity | wisdom | necessity | essential discernment | 0 | NO_ITEMS | Trade-offs are surfaced in Guidance |
| B:wisdom:sufficiency | wisdom | sufficiency | adequate judgment | 0 | NO_ITEMS | Judgment calls are flagged as TBD for human |
| B:wisdom:completeness | wisdom | completeness | holistic insight | 0 | NO_ITEMS | Holistic view is present across documents |
| B:wisdom:consistency | wisdom | consistency | principled reasoning | 0 | NO_ITEMS | Reasoning is principled and source-grounded |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| B-001 | B:data:necessity | MissingSlot | Datasheet | Datasheet | Add a row to the Attributes table for "Polling Interval Default" with either a value or an explicit cross-reference to where the value will be determined | Datasheet lists Polling Interval as TBD and Debounce Strategy as TBD; these are essential facts for the data record of this deliverable; the default should be recorded once determined | Datasheet.md | Attributes table: Polling Interval | | Human/Implementation profiling | TBD |
| B-002 | B:data:completeness | MissingSlot | Datasheet | Datasheet | Add attribute rows for the IPC channel name(s) or preload bridge API used for filesystem access | Datasheet Construction section references "Electron main process IPC (or preload bridge)" but does not name the specific IPC channel or API; a comprehensive data record should enumerate these | Datasheet.md | Construction table: Filesystem Access | | Implementation discovery | TBD |
| B-003 | B:knowledge:completeness | WeakStatement | Multi | Guidance | Elaborate the debounce strategy in Guidance (duration, algorithm) and reference it from Specification REQ-06 and Procedure Step 3.3 | Debounce is mentioned in Specification REQ-06 ("SHOULD implement debounce or throttle"), Guidance C3 ("debounce required"), and Procedure Step 3.3 ("e.g., 500ms") but no authoritative specification of the duration or algorithm exists; the 500ms in Procedure is an example, not a requirement | Specification.md; Guidance.md; Procedure.md | REQ-06; C3; Step 3.3 | | Guidance.md (directional) then Specification.md (normative) | TBD |

---

## Matrix C -- Formulation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| C:normative:necessity | normative | necessity | Obligatory Regulatory Foundation | 0 | NO_ITEMS | Foundation is established via SOW-022, DIRECTIVE SS 2.1 |
| C:normative:sufficiency | normative | sufficiency | Mandated Competence Threshold | 1 | HAS_ITEMS | Error recovery behavior undetermined |
| C:normative:completeness | normative | completeness | Mandated Exhaustive Scope | 1 | HAS_ITEMS | Polling-during-hidden-window policy missing |
| C:normative:consistency | normative | consistency | Mandated Uniform Integrity | 0 | NO_ITEMS | Consistent normative framing across documents |
| C:operative:necessity | operative | necessity | Critical Operational Prerequisite | 1 | HAS_ITEMS | Prerequisite status column is all TBD |
| C:operative:sufficiency | operative | sufficiency | Operational Competence Baseline | 0 | NO_ITEMS | Steps are sufficient for a competent developer |
| C:operative:completeness | operative | completeness | Complete Operational Mastery | 0 | NO_ITEMS | Procedure steps cover full implementation lifecycle |
| C:operative:consistency | operative | consistency | Consistent Operational Discipline | 0 | NO_ITEMS | Steps are consistently structured |
| C:evaluative:necessity | evaluative | necessity | Fundamental Worth Criterion | 0 | NO_ITEMS | Worth criterion is clear: accurate filesystem representation |
| C:evaluative:sufficiency | evaluative | sufficiency | Adequate Merit Assessment | 0 | NO_ITEMS | Verification approaches are adequate |
| C:evaluative:completeness | evaluative | completeness | Holistic Merit Comprehension | 0 | NO_ITEMS | Merit is comprehensively addressed |
| C:evaluative:consistency | evaluative | consistency | Principled Value Coherence | 0 | NO_ITEMS | Value coherence is maintained |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| C-001 | C:normative:sufficiency | TBD_Question | Specification | Specification | Resolve TBD in REQ-07: define error recovery behavior (auto-retry, manual retry, root-reset prompt, or combination) | REQ-07 ASSUMPTION marks error recovery behavior as TBD; mandated competence threshold requires knowing what "sufficient" error handling means before implementation can be judged adequate | Specification.md | REQ-07: Graceful Error Handling | | Human decision | TBD |
| C-002 | C:normative:completeness | MissingSlot | Specification | Specification | Add requirement or guidance on whether polling continues, pauses, or slows when the application window is hidden/minimized | Guidance Example (line 122) raises the question "pauses -- TBD policy for hidden windows" but no requirement or decision exists in Specification; this is a gap in exhaustive scope for the polling mechanism | Guidance.md; Specification.md | Examples: Polling Refresh Cycle (line 122); REQ-01 | | Specification.md | TBD |
| C-003 | C:operative:necessity | RationaleGap | Procedure | Guidance | Add rationale for prerequisite sequencing: clarify whether DEL-03-01 (root binding) must be complete before DEL-02-01 work can begin, or if a mock/stub suffices | Procedure Prerequisites table lists "`projectRoot` binding" with status TBD and references DEL-03-01; it is unclear whether this is a hard blocking dependency or can be satisfied with a stub during development | Procedure.md | Prerequisites table | | Human/ORCHESTRATOR (dependency ruling) | TBD |

---

## Matrix F -- Requirements (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| F:normative:necessity | normative | necessity | Mandated Baseline Imperative | 1 | HAS_ITEMS | No requirement for initial scan timing |
| F:normative:sufficiency | normative | sufficiency | Prescribed Adequacy Standard | 1 | HAS_ITEMS | REQ-02 SHOULD vs MUST inconsistency |
| F:normative:completeness | normative | completeness | Total Regulatory Coverage | 0 | NO_ITEMS | Requirements cover the full SOW-022 scope |
| F:normative:consistency | normative | consistency | Mandated Coherence Standard | 1 | HAS_ITEMS | Terminology drift: "scan" vs "refresh" vs "poll" |
| F:operative:necessity | operative | necessity | Foundational Operational Demand | 0 | NO_ITEMS | Core operational demands are captured |
| F:operative:sufficiency | operative | sufficiency | Sufficient Operational Capability | 0 | NO_ITEMS | Capability description is sufficient |
| F:operative:completeness | operative | completeness | Exhaustive Operational Coverage | 1 | HAS_ITEMS | No step for symlink/alias handling |
| F:operative:consistency | operative | consistency | Principled Operational Consistency | 0 | NO_ITEMS | Procedure is consistently structured |
| F:evaluative:necessity | evaluative | necessity | Essential Merit Foundation | 0 | NO_ITEMS | Merit foundation is established |
| F:evaluative:sufficiency | evaluative | sufficiency | Sufficient Value Appraisal | 0 | NO_ITEMS | Value appraisal is sufficient |
| F:evaluative:completeness | evaluative | completeness | Comprehensive Value Mastery | 0 | NO_ITEMS | Value considerations are comprehensive |
| F:evaluative:consistency | evaluative | consistency | Principled Merit Consistency | 0 | NO_ITEMS | Merit consistency is maintained |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| F-001 | F:normative:necessity | MissingSlot | Specification | Specification | Add requirement for initial scan behavior: define whether the first scan happens immediately on root selection or after the first polling interval elapses | Specification REQ-01 defines periodic polling and REQ-04 defines root binding, but neither specifies when the initial scan occurs after a root is set; this is a baseline imperative gap | Specification.md | REQ-01; REQ-04 | | Specification.md | TBD |
| F-002 | F:normative:sufficiency | WeakStatement | Specification | Specification | Strengthen REQ-02 Electron focus event from SHOULD to MUST, or add rationale for why SHOULD is acceptable | REQ-02 uses MUST for `visibilitychange` but SHOULD for Electron `BrowserWindow` focus events; the adequacy standard is unclear -- if the SHOULD-level event is skipped, is the requirement still met? | Specification.md | REQ-02: Focus/Visibility Refresh | | Guidance.md (rationale) then Specification.md (normative) | TBD |
| F-003 | F:normative:consistency | Normalization | Multi | Guidance | Define and standardize terminology: "refresh" (the act of updating tree state), "scan" (filesystem read operation), "poll" (timer-triggered scan), and use consistently across all documents | Documents use "refresh," "scan," "re-scan," "poll," and "polling" with overlapping meanings; e.g., Specification says "poll the filesystem" while Procedure says "filesystem re-scan" and Guidance says "refresh cycle"; inconsistent use risks implementation drift | Specification.md; Guidance.md; Procedure.md | Throughout | | Guidance.md (vocabulary section) | TBD |
| F-004 | F:operative:completeness | MissingSlot | Specification | Specification | Add requirement or explicit exclusion for symlink/alias handling during filesystem scan | REQ-03 requires detecting new files, deleted files, renamed files, and directory structure changes, but does not address symbolic links or macOS aliases; on macOS (the target platform per DEC-PLAT-001), symlinks are common in Node.js projects (node_modules) | Specification.md | REQ-03: External Change Detection | | Specification.md | TBD |

---

## Matrix D -- Objectives (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| D:normative:guiding | normative | guiding | Authoritative Mandate Resolution | 0 | NO_ITEMS | Mandate resolution is clear via SOW-022 |
| D:normative:applying | normative | applying | Resolved Compliance Practice | 1 | HAS_ITEMS | K-STATUS-1 display not addressed |
| D:normative:judging | normative | judging | Definitive Regulatory Ruling | 0 | NO_ITEMS | Regulatory basis is clear |
| D:normative:reviewing | normative | reviewing | Settled Regulatory Examination | 0 | NO_ITEMS | Examination approach is settled |
| D:operative:guiding | operative | guiding | Grounded Procedural Directive | 0 | NO_ITEMS | Procedure is grounded in Specification |
| D:operative:applying | operative | applying | Resolved Execution Capability | 0 | NO_ITEMS | Execution steps are resolute |
| D:operative:judging | operative | judging | Settled Performance Judgment | 1 | HAS_ITEMS | Manual verification lacks repeatability criteria |
| D:operative:reviewing | operative | reviewing | Systematic Consistency Review | 0 | NO_ITEMS | Cross-reference step (Step 8) is systematic |
| D:evaluative:guiding | evaluative | guiding | Grounded Value Direction | 0 | NO_ITEMS | Value direction grounded in filesystem-as-database |
| D:evaluative:applying | evaluative | applying | Resolved Merit Application | 0 | NO_ITEMS | Merit application is resolved |
| D:evaluative:judging | evaluative | judging | Definitive Value Determination | 1 | HAS_ITEMS | No metric for "promptly" reflected |
| D:evaluative:reviewing | evaluative | reviewing | Settled Quality Appraisal | 0 | NO_ITEMS | Quality appraisal is addressed |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| D-001 | D:normative:applying | MissingSlot | Specification | Specification | Clarify whether FileTree should display deliverable lifecycle status indicators (per K-STATUS-1 in Standards table) or whether this is out of scope for DEL-02-01 | Specification Standards table lists CONTRACT K-STATUS-1 ("FileTree may display status indicators for deliverable folders") but no requirement addresses this capability; compliance practice is unresolved -- is it in scope or not? | Specification.md | Standards table: K-STATUS-1 | | Human (scope decision) | TBD |
| D-002 | D:operative:judging | VerificationGap | Procedure | Procedure | Add repeatability criteria to manual verification checks (e.g., number of trials, representative directory specifications, timing requirements) | Procedure Verification table includes manual checks ("Run app; wait for polling interval; observe tree updates") but lacks repeatability criteria; settled performance judgment requires defined conditions for pass/fail | Procedure.md | Verification table | | Procedure.md | TBD |
| D-003 | D:evaluative:judging | RationaleGap | Guidance | Guidance | Define what "promptly" means for external change reflection -- establish a target latency (e.g., "within one polling interval plus debounce window") | Guidance Purpose states changes "must be reflected promptly" but no document defines a measurable latency target; definitive value determination requires a quantifiable criterion | Guidance.md | Purpose section | | Guidance.md | TBD |

---

## Matrix X -- Verification (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| X:guiding:necessity | guiding | necessity | Authoritative Essential Guidance | 0 | NO_ITEMS | Essential guidance is authoritative |
| X:guiding:sufficiency | guiding | sufficiency | Directed Competence Adequacy | 1 | HAS_ITEMS | No guidance on testing approach for Electron IPC |
| X:guiding:completeness | guiding | completeness | Comprehensive Guided Mastery | 0 | NO_ITEMS | Guidance comprehensively covers the domain |
| X:guiding:consistency | guiding | consistency | Principled Guidance Integrity | 0 | NO_ITEMS | Guidance principles are consistently applied |
| X:applying:necessity | applying | necessity | Critical Practice Fulfillment | 0 | NO_ITEMS | Critical practices identified |
| X:applying:sufficiency | applying | sufficiency | Sufficient Practice Competence | 1 | HAS_ITEMS | No mocking strategy for filesystem in tests |
| X:applying:completeness | applying | completeness | Complete Practice Coverage | 0 | NO_ITEMS | Practice coverage is complete |
| X:applying:consistency | applying | consistency | Disciplined Practice Coherence | 0 | NO_ITEMS | Practice is disciplined |
| X:judging:necessity | judging | necessity | Binding Essential Judgment | 1 | HAS_ITEMS | REQ-03 verification needs tighter acceptance criteria |
| X:judging:sufficiency | judging | sufficiency | Settled Sufficiency Verdict | 0 | NO_ITEMS | Sufficiency verdicts are settled where values are defined |
| X:judging:completeness | judging | completeness | Comprehensive Judgment Command | 0 | NO_ITEMS | Judgment coverage is comprehensive |
| X:judging:consistency | judging | consistency | Principled Judgment Uniformity | 0 | NO_ITEMS | Judgment is uniform |
| X:reviewing:necessity | reviewing | necessity | Critical Systematic Scrutiny | 1 | HAS_ITEMS | No review step for Electron security (preload scope) |
| X:reviewing:sufficiency | reviewing | sufficiency | Adequate Systematic Scrutiny | 0 | NO_ITEMS | Scrutiny is adequate |
| X:reviewing:completeness | reviewing | completeness | Exhaustive Scrutiny Command | 0 | NO_ITEMS | Scrutiny is exhaustive |
| X:reviewing:consistency | reviewing | consistency | Principled Scrutiny Alignment | 0 | NO_ITEMS | Scrutiny is aligned |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| X-001 | X:guiding:sufficiency | RationaleGap | Guidance | Guidance | Add a consideration (C6 or similar) on how to test filesystem scanning through Electron IPC boundaries -- mock main process, use temp directories, or both | Guidance provides considerations for polling, visibility events, and tree state but no guidance on how to approach testing across the Electron IPC boundary; directed competence requires knowing how to verify the scan mechanism | Guidance.md | Considerations section | | Guidance.md | TBD |
| X-002 | X:applying:sufficiency | MissingSlot | Procedure | Procedure | Add a sub-step in Step 6 specifying the mocking/stubbing strategy for filesystem operations in unit tests (e.g., mock IPC responses, use temp filesystem, or use in-memory fs) | Procedure Step 6 lists specific tests to write but does not specify how filesystem operations will be mocked or stubbed; sufficient practice competence requires a defined testing strategy | Procedure.md | Step 6: Write Tests | | Procedure.md | TBD |
| X-003 | X:judging:necessity | VerificationGap | Specification | Specification | Tighten REQ-03 acceptance criterion from "Displayed tree matches `ls -R` of projectRoot" to specify timing (within N seconds of refresh trigger) and scope (top-level accuracy, recursive accuracy, metadata accuracy) | REQ-03 verification acceptance criterion is "Displayed tree matches `ls -R` of projectRoot" which is imprecise -- does it include hidden files? symlinks? timestamps? Binding essential judgment requires unambiguous pass/fail | Specification.md | Verification table: REQ-03 | | Specification.md | TBD |
| X-004 | X:reviewing:necessity | VerificationGap | Datasheet | Specification | Add a verification check or note in Specification Standards confirming that filesystem access via preload bridge respects Electron security best practices (contextIsolation, no nodeIntegration in renderer) | Datasheet Construction section assumes "standard Electron architecture for filesystem access" but no verification exists for Electron security posture of the IPC/preload bridge used by FileTree; critical systematic scrutiny should include this | Datasheet.md; Specification.md | Datasheet: Construction > Filesystem Access; Specification: Standards | | Specification.md (security standard) | TBD |

---

## Matrix E -- Evaluation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| E:normative:necessity | normative | necessity | Binding Authoritative Mandate | 0 | NO_ITEMS | Binding mandate is established |
| E:normative:sufficiency | normative | sufficiency | Mandated Sufficiency Standard | 0 | NO_ITEMS | Sufficiency standard is adequate |
| E:normative:completeness | normative | completeness | Total Mandated Command | 1 | HAS_ITEMS | OBJ-005 assumption not resolved |
| E:normative:consistency | normative | consistency | Authoritative Principled Uniformity | 1 | HAS_ITEMS | Assumption markers inconsistent across docs |
| E:operative:necessity | operative | necessity | Critical Operational Authority | 0 | NO_ITEMS | Operational authority is established |
| E:operative:sufficiency | operative | sufficiency | Verified Operational Sufficiency | 0 | NO_ITEMS | Operational sufficiency is verified by procedure |
| E:operative:completeness | operative | completeness | Exhaustive Operational Command | 0 | NO_ITEMS | Operational command is exhaustive |
| E:operative:consistency | operative | consistency | Principled Operational Discipline | 0 | NO_ITEMS | Operational discipline is principled |
| E:evaluative:necessity | evaluative | necessity | Authoritative Worth Standard | 0 | NO_ITEMS | Worth standard is authoritative |
| E:evaluative:sufficiency | evaluative | sufficiency | Verified Value Sufficiency | 0 | NO_ITEMS | Value sufficiency is verified |
| E:evaluative:completeness | evaluative | completeness | Comprehensive Worth Command | 0 | NO_ITEMS | Worth command is comprehensive |
| E:evaluative:consistency | evaluative | consistency | Principled Worth Integrity | 1 | HAS_ITEMS | Governance reference formatting inconsistency |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| E-001 | E:normative:completeness | VerificationGap | Datasheet | Datasheet | Confirm or deny OBJ-005 mapping: either verify that OBJ-005 applies to DEL-02-01 (remove ASSUMPTION label) or note it as unverified | Datasheet Identification table marks OBJ-005 association as "ASSUMPTION (best-effort mapping via PKG-02 package grouping)" and Guidance Purpose repeats this assumption; total mandated command requires confirmed objective traceability | Datasheet.md; Guidance.md | Datasheet: Identification > Objective Association; Guidance: Purpose | | Human (objective verification) | TBD |
| E-002 | E:normative:consistency | Normalization | Multi | Guidance | Standardize ASSUMPTION marker format across all four documents: use a consistent pattern (e.g., always bold "**ASSUMPTION:**" at start of line) | ASSUMPTION markers appear in different formats: Datasheet uses "**ASSUMPTION: ...**" inline, Specification uses "**ASSUMPTION:** ..." as a paragraph, Guidance uses "**ASSUMPTION: ...**" inline, Procedure uses "**ASSUMPTION: ...**" inline; authoritative principled uniformity requires consistent marking | Datasheet.md; Specification.md; Guidance.md; Procedure.md | Multiple locations | | Guidance.md (style convention) | TBD |
| E-003 | E:evaluative:consistency | Normalization | Datasheet | Datasheet | Standardize governance reference notation: use consistent format for document section references (e.g., always "DOC SS N" or "DOC Section N") | Datasheet References table uses varied reference formats: "PLAN SS 2," "DIRECTIVE SS 2.1, SS 2.6," "UI_POLISH_EXECUTION_PLAN SS F," "Decomposition `DEL-02-01` entry"; principled worth integrity benefits from uniform reference notation | Datasheet.md | References table | | Guidance.md (style convention) | TBD |
