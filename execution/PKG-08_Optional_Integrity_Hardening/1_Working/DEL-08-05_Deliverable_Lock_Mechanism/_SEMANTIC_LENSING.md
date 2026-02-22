# Semantic Lensing Register: DEL-08-05 Deliverable-level Lock Mechanism

**Generated:** 2026-02-21
**Deliverable Folder:** execution/PKG-08_Optional_Integrity_Hardening/1_Working/DEL-08-05_Deliverable_Lock_Mechanism/
**Warnings:** None

**Inputs Read:**
- _CONTEXT.md — `execution/PKG-08_Optional_Integrity_Hardening/1_Working/DEL-08-05_Deliverable_Lock_Mechanism/_CONTEXT.md`
- _STATUS.md — `execution/PKG-08_Optional_Integrity_Hardening/1_Working/DEL-08-05_Deliverable_Lock_Mechanism/_STATUS.md`
- _SEMANTIC.md — `execution/PKG-08_Optional_Integrity_Hardening/1_Working/DEL-08-05_Deliverable_Lock_Mechanism/_SEMANTIC.md`
- Datasheet.md — `execution/PKG-08_Optional_Integrity_Hardening/1_Working/DEL-08-05_Deliverable_Lock_Mechanism/Datasheet.md`
- Specification.md — `execution/PKG-08_Optional_Integrity_Hardening/1_Working/DEL-08-05_Deliverable_Lock_Mechanism/Specification.md`
- Guidance.md — `execution/PKG-08_Optional_Integrity_Hardening/1_Working/DEL-08-05_Deliverable_Lock_Mechanism/Guidance.md`
- Procedure.md — `execution/PKG-08_Optional_Integrity_Hardening/1_Working/DEL-08-05_Deliverable_Lock_Mechanism/Procedure.md`
- _REFERENCES.md — `execution/PKG-08_Optional_Integrity_Hardening/1_Working/DEL-08-05_Deliverable_Lock_Mechanism/_REFERENCES.md`

**Purpose:** Apply CHIRALITY_FRAMEWORK matrix cells as lenses over the production documents, capturing warranted enrichment inputs for a later enrichment pass.

---

## Summary

- Total warranted items: 28
- By document (AppliesToDoc):
  - Datasheet: 6
  - Specification: 15
  - Guidance: 3
  - Procedure: 3
  - Multi: 1
- By matrix:
  - A: 5  B: 4  C: 3  F: 4  D: 3  X: 6  E: 3
- By type:
  - Conflict: 2
  - VerificationGap: 5
  - MissingSlot: 9
  - WeakStatement: 3
  - RationaleGap: 2
  - Normalization: 3
  - TBD_Question: 4
  - MatrixError: 0
- Notable conflicts: 2
- Matrix parse errors: 0

---

## Matrix A -- Orientation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| A:normative:guiding | normative | guiding | prescriptive direction | 1 | HAS_ITEMS | TBD values in Datasheet weaken prescriptive direction |
| A:normative:applying | normative | applying | mandatory practice | 1 | HAS_ITEMS | Lock file location/format/lease TBD blocks mandatory practice |
| A:normative:judging | normative | judging | compliance determination | 1 | HAS_ITEMS | Verification table present but acceptance criteria for atomicity are weak |
| A:normative:reviewing | normative | reviewing | regulatory audit | 0 | NO_ITEMS | Audit trail addressed in Procedure records section |
| A:operative:guiding | operative | guiding | procedural direction | 1 | HAS_ITEMS | Part B operational procedure has TBD prerequisite statuses |
| A:operative:applying | operative | applying | practical execution | 0 | NO_ITEMS | Procedure Part A steps are well-structured |
| A:operative:judging | operative | judging | performance assessment | 0 | NO_ITEMS | Verification checks in Procedure Part B are present |
| A:operative:reviewing | operative | reviewing | process audit | 1 | HAS_ITEMS | No explicit audit/log format defined |
| A:evaluative:guiding | evaluative | guiding | value orientation | 0 | NO_ITEMS | Guidance Purpose section establishes value clearly |
| A:evaluative:applying | evaluative | applying | merit application | 0 | NO_ITEMS | Trade-offs section in Guidance provides merit assessment |
| A:evaluative:judging | evaluative | judging | worth determination | 0 | NO_ITEMS | Coverage adequate via Guidance trade-offs and principles |
| A:evaluative:reviewing | evaluative | reviewing | quality appraisal | 0 | NO_ITEMS | Quality assessment addressed by test suite verification |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A-001 | A:normative:guiding | TBD_Question | Datasheet | Datasheet | Resolve TBD values for Lock File Location, Lock File Format, Maximum Lease Duration, and Retry/Backoff Policy in Attributes table | Four critical design parameters remain TBD, preventing the deliverable from providing prescriptive direction on implementation | Datasheet.md | Attributes table | -- | PROPOSAL: Human ruling on CON-001 and CON-002 in Guidance.md should cascade to Datasheet | TBD |
| A-002 | A:normative:applying | MissingSlot | Specification | Specification | Add a requirement (or note) specifying the lock file naming convention (e.g., `.lock` vs. `_LOCK.json` vs. other) | Lock file name is referenced informally (`.lock` in Guidance examples, Procedure Part B) but no requirement formally mandates the name; mandatory practice requires explicit naming | Specification.md | Requirements section (between REQ-LOCK-001 and REQ-LOCK-002) | -- | PROPOSAL: Specification should contain the binding naming convention | TBD |
| A-003 | A:normative:judging | WeakStatement | Specification | Specification | Strengthen acceptance criteria for REQ-LOCK-003 (Atomic Acquisition): specify the exact mechanism or test conditions that constitute proof of atomicity | "Under simultaneous acquisition attempts, exactly one succeeds" does not specify how many simultaneous attempts, timing constraints, or platform-specific guarantees | Specification.md | Verification table, REQ-LOCK-003 row | -- | PROPOSAL: Add concurrency test parameters (number of parallel attempts, expected pass rate) | TBD |
| A-004 | A:operative:guiding | WeakStatement | Procedure | Procedure | Clarify TBD status of Part B prerequisites (Lock Module Available, Agent Integration Complete, .gitignore Updated) with conditions or cross-references to Part A steps that produce them | Part B prerequisites are listed as operational but have no traceability to Part A production steps that create them | Procedure.md | Part B Prerequisites table | -- | PROPOSAL: Cross-reference each Part B prerequisite to its Part A production step | TBD |
| A-005 | A:operative:reviewing | MissingSlot | Procedure | Procedure | Define a log format or structured record schema for lock acquisition/release and orphan recovery events | Records table references "TBD (agent execution log or _MEMORY.md)" for both acquisition and recovery logs; no format is specified | Procedure.md | Part B Records table | -- | PROPOSAL: Define minimal structured log fields (timestamp, agent, deliverable, action, outcome) | TBD |

---

## Matrix B -- Conceptualization (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| B:data:necessity | data | necessity | essential fact | 1 | HAS_ITEMS | Missing: default lease duration value |
| B:data:sufficiency | data | sufficiency | adequate evidence | 0 | NO_ITEMS | Source citations in Specification and Datasheet are adequate |
| B:data:completeness | data | completeness | comprehensive record | 1 | HAS_ITEMS | Lock file field list may be incomplete |
| B:data:consistency | data | consistency | reliable measurement | 0 | NO_ITEMS | Field types in REQ-LOCK-002 are specified consistently |
| B:information:necessity | information | necessity | essential signal | 1 | HAS_ITEMS | LOCK_CONTENTION reporting format undefined |
| B:information:sufficiency | information | sufficiency | adequate context | 0 | NO_ITEMS | Context established across Guidance and Specification |
| B:information:completeness | information | completeness | comprehensive account | 0 | NO_ITEMS | Cross-document account is thorough |
| B:information:consistency | information | consistency | coherent message | 1 | HAS_ITEMS | Terminology inconsistency: "lock file" vs. ".lock" vs. "lock" |
| B:knowledge:necessity | knowledge | necessity | fundamental understanding | 0 | NO_ITEMS | Guidance Principles section covers this well |
| B:knowledge:sufficiency | knowledge | sufficiency | competent expertise | 0 | NO_ITEMS | Sufficient technical detail for implementation |
| B:knowledge:completeness | knowledge | completeness | thorough mastery | 0 | NO_ITEMS | Comprehensive coverage of concurrency concepts |
| B:knowledge:consistency | knowledge | consistency | coherent understanding | 0 | NO_ITEMS | Consistent understanding across documents |
| B:wisdom:necessity | wisdom | necessity | essential discernment | 0 | NO_ITEMS | Guidance trade-offs provide discernment |
| B:wisdom:sufficiency | wisdom | sufficiency | adequate judgment | 0 | NO_ITEMS | CON-001/CON-002 conflict table supports judgment |
| B:wisdom:completeness | wisdom | completeness | holistic insight | 0 | NO_ITEMS | C5 addresses cross-deliverable interactions |
| B:wisdom:consistency | wisdom | consistency | principled reasoning | 0 | NO_ITEMS | Principles are traced to sources |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| B-001 | B:data:necessity | TBD_Question | Datasheet | Datasheet | Determine and record a default Maximum Lease Duration value (Datasheet Attributes lists TBD; Guidance T1 suggests 15-30 min as assumption) | Essential fact (lease duration) is required for implementation and verification of REQ-LOCK-004 but remains TBD across all documents | Datasheet.md; Guidance.md | Datasheet: Attributes table (Maximum Lease Duration); Guidance: T1 | -- | PROPOSAL: Human decides default; record in Datasheet, reference from Specification REQ-LOCK-004 | TBD |
| B-002 | B:data:completeness | MissingSlot | Specification | Specification | Consider adding a `lock_file_version` or `schema_version` field to REQ-LOCK-002 lock file contents to support future format evolution | REQ-LOCK-002 defines lock file fields but has no versioning; if the format evolves, there is no mechanism to distinguish old from new lock files | Specification.md | REQ-LOCK-002 table | -- | PROPOSAL: Add optional schema_version field to lock file spec | TBD |
| B-003 | B:information:necessity | MissingSlot | Specification | Specification | Define the LOCK_CONTENTION report format or payload (REQ-LOCK-007 says "report LOCK_CONTENTION to ORCHESTRATOR" but does not specify what information the report contains) | The signal content is essential for ORCHESTRATOR to make retry/escalation decisions but is not defined | Specification.md | REQ-LOCK-007 | -- | PROPOSAL: Specify minimum report fields (deliverable_id, holder, lease_remaining, contention_time) | TBD |
| B-004 | B:information:consistency | Normalization | Multi | Guidance | Standardize lock file terminology across documents: "lock file" (Specification), ".lock" (Guidance examples), ".lock file" (Procedure), "lock" (Datasheet) | Inconsistent naming may cause drift between protocol specification and implementation; a single canonical term should be established | Datasheet.md; Specification.md; Guidance.md; Procedure.md | Datasheet: Attributes (Lock Mechanism Type); Specification: REQ-LOCK-001; Guidance: C1; Procedure: Part B | -- | PROPOSAL: Establish canonical term in Guidance and reference throughout | TBD |

---

## Matrix C -- Formulation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| C:normative:necessity | normative | necessity | Regulatory Imperative | 1 | HAS_ITEMS | OBJ-007 mapping marked as ASSUMPTION |
| C:normative:sufficiency | normative | sufficiency | Warranted Mandate | 0 | NO_ITEMS | Requirements are sourced and warranted |
| C:normative:completeness | normative | completeness | Comprehensive Mandate | 1 | HAS_ITEMS | Missing requirement for lock file cleanup on deliverable deletion/archival |
| C:normative:consistency | normative | consistency | Principled Regulation | 0 | NO_ITEMS | Requirements consistently trace to CONTRACT.md invariants |
| C:operative:necessity | operative | necessity | Operational Essential | 0 | NO_ITEMS | Core operations (acquire/release/recover) are all defined |
| C:operative:sufficiency | operative | sufficiency | Competent Practice | 0 | NO_ITEMS | Procedure steps are actionable |
| C:operative:completeness | operative | completeness | Thorough Execution | 1 | HAS_ITEMS | Missing error handling for corrupted lock files in operational procedure |
| C:operative:consistency | operative | consistency | Disciplined Execution | 0 | NO_ITEMS | Steps are sequenced and verified |
| C:evaluative:necessity | evaluative | necessity | Foundational Merit | 0 | NO_ITEMS | Value proposition is clear |
| C:evaluative:sufficiency | evaluative | sufficiency | Defensible Valuation | 0 | NO_ITEMS | Trade-offs are well-defended |
| C:evaluative:completeness | evaluative | completeness | Integral Appraisal | 0 | NO_ITEMS | Cross-deliverable interaction noted in C5 |
| C:evaluative:consistency | evaluative | consistency | Principled Appraisal | 0 | NO_ITEMS | Evaluation criteria aligned across documents |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| C-001 | C:normative:necessity | WeakStatement | Datasheet | Guidance | Strengthen or resolve the ASSUMPTION tag on OBJ-007 mapping ("best-effort mapping via PKG-08 package grouping") with explicit traceability or human confirmation | The regulatory imperative for this deliverable depends on its objective linkage; if OBJ-007 mapping is wrong, the deliverable's mandate is weakened | Datasheet.md; Guidance.md | Datasheet: Identification table (Supports Objectives); Guidance: Purpose paragraph 2 | -- | PROPOSAL: Human confirms OBJ-007 linkage or provides correct objective | TBD |
| C-002 | C:normative:completeness | MissingSlot | Specification | Specification | Add a requirement addressing lock file behavior when a deliverable folder is deleted, moved, or archived (what happens to an active or stale lock?) | The comprehensive mandate lens reveals no requirement covers the lock lifecycle in relation to deliverable lifecycle termination (deletion/archival) | Specification.md | Requirements section (after REQ-LOCK-009) | -- | PROPOSAL: Add REQ-LOCK-012 covering lock cleanup on deliverable removal | TBD |
| C-003 | C:operative:completeness | MissingSlot | Procedure | Procedure | Add a step in Part B Lock Acquisition for handling corrupted or unparseable lock files (e.g., truncated JSON, missing fields) | Procedure Part B step 4a says "Read the existing lock file" but does not address what happens if the file is corrupt; Specification REQ-LOCK-006 only covers stale locks, not corrupt ones | Procedure.md | Part B Steps: Lock Acquisition, step 4a | -- | PROPOSAL: Add error-handling branch for corrupt lock files (treat as recoverable? fail?) | TBD |

---

## Matrix F -- Requirements (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| F:normative:necessity | normative | necessity | Obligatory Foundation | 1 | HAS_ITEMS | REQ-LOCK-003 implementation approach is TBD |
| F:normative:sufficiency | normative | sufficiency | Proven Prescription | 1 | HAS_ITEMS | REQ-LOCK-004 lacks specific lease boundary values |
| F:normative:completeness | normative | completeness | Integral Mandate | 0 | NO_ITEMS | Requirements cover the full protocol lifecycle |
| F:normative:consistency | normative | consistency | Coherent Mandate | 0 | NO_ITEMS | Requirements reference consistent source documents |
| F:operative:necessity | operative | necessity | Essential Function | 1 | HAS_ITEMS | Lock renewal not addressed |
| F:operative:sufficiency | operative | sufficiency | Proficient Operation | 0 | NO_ITEMS | Operational procedures are sufficient for stated scope |
| F:operative:completeness | operative | completeness | Comprehensive Execution | 0 | NO_ITEMS | Production and operational procedures both present |
| F:operative:consistency | operative | consistency | Reliable Operation | 1 | HAS_ITEMS | Inconsistency between Specification and Procedure on recovery trigger |
| F:evaluative:necessity | evaluative | necessity | Core Judgment | 0 | NO_ITEMS | Core value judgment is sound |
| F:evaluative:sufficiency | evaluative | sufficiency | Evidenced Worth | 0 | NO_ITEMS | Trade-offs provide sufficient evidence |
| F:evaluative:completeness | evaluative | completeness | Thorough Valuation | 0 | NO_ITEMS | Complete valuation via Guidance |
| F:evaluative:consistency | evaluative | consistency | Stable Worth | 0 | NO_ITEMS | Value proposition is stable across documents |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| F-001 | F:normative:necessity | RationaleGap | Specification | Guidance | Add rationale or guidance on why `O_CREAT \| O_EXCL` is the recommended atomicity mechanism and what alternatives were considered (e.g., `mkdir`, `link`, `rename`) | REQ-LOCK-003 Implementation Note mentions `O_CREAT \| O_EXCL` but marks it TBD; the obligatory foundation lens requires that the chosen mechanism be justified, not merely suggested | Specification.md | REQ-LOCK-003 Implementation Note | -- | PROPOSAL: Guidance should discuss atomicity mechanism alternatives; Specification should mandate the chosen one | TBD |
| F-002 | F:normative:sufficiency | VerificationGap | Specification | Specification | Add specific boundary values or ranges to REQ-LOCK-004 acceptance criteria (e.g., minimum and maximum acceptable lease durations, tolerance for expiry detection) | "Expired lease is detected and lock is eligible for recovery" does not specify timing precision, detection latency, or acceptable lease duration bounds | Specification.md | Verification table, REQ-LOCK-004 row | -- | PROPOSAL: Add quantitative acceptance criteria once lease duration is decided | TBD |
| F-003 | F:operative:necessity | TBD_Question | Specification | Specification | Determine whether lock lease renewal is required and, if so, add a requirement (REQ-LOCK-012 or similar) | Guidance T1 mentions "optional renewal" as a possibility for short leases but no requirement addresses renewal; if long-running agents need renewal, its absence is a functional gap | Specification.md; Guidance.md | Specification: Requirements section; Guidance: T1 | -- | PROPOSAL: Human decides whether renewal is needed; if yes, add requirement | TBD |
| F-004 | F:operative:consistency | Conflict | Specification | Specification | Reconcile orphan recovery trigger conditions between Specification and Procedure: Specification REQ-LOCK-006 says "at least one must be true" (OR logic); Procedure Part B step 4c says "stale (lease expired OR holder PID is not running)" (also OR). However, Procedure Part B Orphan Recovery (Manual) step 5 says "If either condition is met (PID dead OR lease expired)" while the acquisition flow step 4b says "Check if the lock is stale (lease expired OR holder PID is not running)" -- these are consistent. But the automated path in step 4c recovers immediately on stale detection, while Manual Recovery step 5 requires explicit human confirmation step 6 (record in _MEMORY.md). Clarify whether automated recovery also requires recording. | Automated and manual recovery paths have different recording requirements; this inconsistency could lead to untracked automated recoveries | Specification.md; Procedure.md | Specification: REQ-LOCK-006; Procedure: Part B Lock Acquisition step 4c vs. Part B Orphan Recovery (Manual) step 6 | Specification.md#REQ-LOCK-006; Procedure.md#Steps: Orphan Recovery (Manual) step 6 | PROPOSAL: Add recording requirement to automated recovery path in Procedure or add a requirement in Specification | TBD |

---

## Matrix D -- Objectives (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| D:normative:guiding | normative | guiding | Binding Authority | 0 | NO_ITEMS | Authority established via CONTRACT.md invariants |
| D:normative:applying | normative | applying | Enforced Protocol | 1 | HAS_ITEMS | Enforcement mechanism for write-scope compatibility untested |
| D:normative:judging | normative | judging | Compliance Verdict | 1 | HAS_ITEMS | REQ-LOCK-008 verification is Code Review only |
| D:normative:reviewing | normative | reviewing | Settled Oversight | 0 | NO_ITEMS | Review process defined in Procedure Step 8 |
| D:operative:guiding | operative | guiding | Authoritative Procedure | 0 | NO_ITEMS | Procedure is well-structured |
| D:operative:applying | operative | applying | Settled Practice | 0 | NO_ITEMS | Practice patterns are settled in Guidance examples |
| D:operative:judging | operative | judging | Operational Verdict | 0 | NO_ITEMS | Verification table provides operational verdicts |
| D:operative:reviewing | operative | reviewing | Process Assurance | 0 | NO_ITEMS | Procedure Step 8 covers final review |
| D:evaluative:guiding | evaluative | guiding | Authoritative Worth | 0 | NO_ITEMS | Worth established in Guidance Purpose |
| D:evaluative:applying | evaluative | applying | Demonstrated Merit | 1 | HAS_ITEMS | No concrete evidence of contention frequency to justify merit |
| D:evaluative:judging | evaluative | judging | Merit Judgment | 0 | NO_ITEMS | Judgment supported by trade-off analysis |
| D:evaluative:reviewing | evaluative | reviewing | Enduring Quality | 0 | NO_ITEMS | Quality addressed by test suite |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| D-001 | D:normative:applying | VerificationGap | Specification | Specification | Add an explicit test case or acceptance criterion for REQ-LOCK-008 (Write Scope Compatibility) beyond "Code Review + Test" -- specify what the test validates | Enforced Protocol lens: REQ-LOCK-008 verification says "Code Review + Test" but the acceptance criteria ("No write-scope violations introduced") is not testable without defining what constitutes a violation detection test | Specification.md | Verification table, REQ-LOCK-008 row | -- | PROPOSAL: Define a test that validates lock file writes stay within deliverable-local scope | TBD |
| D-002 | D:normative:judging | VerificationGap | Specification | Specification | Add acceptance criteria for REQ-LOCK-010 (No Ghost Inputs) beyond "Code Review" -- specify what would constitute a ghost input violation for lock files | Compliance Verdict lens: REQ-LOCK-010 verification is "Code Review" only with no testable acceptance criteria; compliance cannot be determined without a clear definition of what "treating lock contents as execution context" means | Specification.md | Verification table, REQ-LOCK-010 row | -- | PROPOSAL: Add a testable criterion (e.g., "no agent reads lock file contents to alter execution decisions beyond contention handling") | TBD |
| D-003 | D:evaluative:applying | RationaleGap | Guidance | Guidance | Add a brief note on the expected frequency or likelihood of lock contention in the current system (single-machine, primarily sequential agent dispatch) to ground the merit argument | Guidance Purpose establishes the gap but does not quantify the risk; without evidence of actual or probable contention, the merit of implementing the mechanism (vs. deferring) is harder to evaluate | Guidance.md | Purpose section | -- | PROPOSAL: Add a sentence noting current contention risk level and scaling trigger | TBD |

---

## Matrix X -- Verification (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| X:guiding:necessity | guiding | necessity | Foundational Directive | 0 | NO_ITEMS | Foundational directives are well-established |
| X:guiding:sufficiency | guiding | sufficiency | Warranted Direction | 1 | HAS_ITEMS | Guidance C1 recommendation lacks verification approach |
| X:guiding:completeness | guiding | completeness | Total Guidance | 0 | NO_ITEMS | Guidance document is comprehensive |
| X:guiding:consistency | guiding | consistency | Principled Direction | 0 | NO_ITEMS | Principles are internally consistent |
| X:applying:necessity | applying | necessity | Enforced Foundation | 1 | HAS_ITEMS | No requirement for lock mechanism self-test or health check |
| X:applying:sufficiency | applying | sufficiency | Warranted Competence | 0 | NO_ITEMS | Implementation approach is sufficient |
| X:applying:completeness | applying | completeness | Complete Enforcement | 1 | HAS_ITEMS | No negative test for lock file permission/ownership issues |
| X:applying:consistency | applying | consistency | Disciplined Practice | 0 | NO_ITEMS | Practice patterns are disciplined |
| X:judging:necessity | judging | necessity | Fundamental Verdict | 1 | HAS_ITEMS | REQ-LOCK-011 verification lacks macOS-specific test criteria |
| X:judging:sufficiency | judging | sufficiency | Sound Adjudication | 0 | NO_ITEMS | Verification table is structured soundly |
| X:judging:completeness | judging | completeness | Complete Adjudication | 1 | HAS_ITEMS | No verification for concurrent recovery attempts |
| X:judging:consistency | judging | consistency | Coherent Adjudication | 0 | NO_ITEMS | Verification methods are coherent |
| X:reviewing:necessity | reviewing | necessity | Mandatory Assurance | 0 | NO_ITEMS | Assurance provided by test suite |
| X:reviewing:sufficiency | reviewing | sufficiency | Justified Assurance | 1 | HAS_ITEMS | Assurance for multi-agent scenarios not specified |
| X:reviewing:completeness | reviewing | completeness | Total Assurance | 0 | NO_ITEMS | Combined production + operational verification covers scope |
| X:reviewing:consistency | reviewing | consistency | Principled Assurance | 0 | NO_ITEMS | Assurance methods consistent with principles |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| X-001 | X:guiding:sufficiency | VerificationGap | Guidance | Specification | Add verification approach for Guidance C1 recommendation (lock file placement inside folder): how will the chosen placement be validated against write-scope requirements? | Warranted Direction lens: the placement recommendation is offered as direction but has no associated verification; the Specification verification table does not test placement correctness specifically | Guidance.md; Specification.md | Guidance: C1; Specification: Verification table | -- | PROPOSAL: Add a test in Specification verification for lock file placement compliance | TBD |
| X-002 | X:applying:necessity | MissingSlot | Specification | Specification | Consider adding a requirement for lock mechanism self-test or startup health check (verify lock acquisition/release works before entering production use) | Enforced Foundation lens: there is no mechanism to verify the lock infrastructure itself is functional before relying on it; a startup check would catch filesystem permission or path issues early | Specification.md | Requirements section | -- | PROPOSAL: Add optional REQ for lock mechanism self-test | TBD |
| X-003 | X:applying:completeness | MissingSlot | Specification | Specification | Add a test case or requirement addressing lock file permission/ownership failures (e.g., lock file created by one user, another user cannot read/delete it) | Complete Enforcement lens: negative cases for filesystem permission issues are not addressed in verification table or requirements | Specification.md | Verification table | -- | PROPOSAL: Add negative test case for permission-related lock failures | TBD |
| X-004 | X:judging:necessity | VerificationGap | Specification | Specification | Specify macOS-specific acceptance criteria for REQ-LOCK-011 (e.g., APFS filesystem behavior, Apple Silicon compatibility validation) | Fundamental Verdict lens: REQ-LOCK-011 verification says "Platform Test" with criteria "Mechanism works on macOS 15+ Apple Silicon" but does not specify what platform-specific behaviors to test (e.g., APFS atomic operations, case sensitivity) | Specification.md | Verification table, REQ-LOCK-011 row | -- | PROPOSAL: Add APFS-specific test criteria | TBD |
| X-005 | X:judging:completeness | MissingSlot | Specification | Specification | Add a test case for concurrent orphan recovery (two agents simultaneously detect a stale lock and attempt recovery) | Complete Adjudication lens: REQ-LOCK-006 tests "stale locks are detected and recovered" but does not address the race condition where two agents both detect the same stale lock and attempt simultaneous recovery | Specification.md | Verification table, REQ-LOCK-006 row | -- | PROPOSAL: Add concurrent recovery test to verification table | TBD |
| X-006 | X:reviewing:sufficiency | Normalization | Datasheet | Datasheet | Clarify Concurrency Unit attribute: "Task agent (Type 2) execution against a single deliverable" should reference whether ORCHESTRATOR (Type 1) is also a potential lock holder or is explicitly excluded | Justified Assurance lens: the Datasheet states the concurrency unit is Type 2 agents but does not clarify whether Type 1 (ORCHESTRATOR) or Type 0 (INIT) agents might also need lock awareness | Datasheet.md | Attributes table (Concurrency Unit) | -- | PROPOSAL: Add clarifying note in Datasheet or Guidance on which agent types interact with locks | TBD |

---

## Matrix E -- Evaluation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| E:normative:necessity | normative | necessity | Mandatory Governance | 1 | HAS_ITEMS | Scope status governance gap |
| E:normative:sufficiency | normative | sufficiency | Justified Enforcement | 0 | NO_ITEMS | Enforcement justification is adequate |
| E:normative:completeness | normative | completeness | Total Compliance | 0 | NO_ITEMS | Compliance coverage is comprehensive |
| E:normative:consistency | normative | consistency | Principled Governance | 0 | NO_ITEMS | Governance principles consistent |
| E:operative:necessity | operative | necessity | Essential Procedure | 0 | NO_ITEMS | Procedures are essential and present |
| E:operative:sufficiency | operative | sufficiency | Justified Operation | 0 | NO_ITEMS | Operational justification adequate |
| E:operative:completeness | operative | completeness | Total Execution | 0 | NO_ITEMS | Execution coverage complete |
| E:operative:consistency | operative | consistency | Coherent Discipline | 0 | NO_ITEMS | Operational discipline is coherent |
| E:evaluative:necessity | evaluative | necessity | Assured Merit | 0 | NO_ITEMS | Merit is assured via Guidance |
| E:evaluative:sufficiency | evaluative | sufficiency | Justified Merit | 1 | HAS_ITEMS | Conflict table entries lack resolution timeline |
| E:evaluative:completeness | evaluative | completeness | Exhaustive Merit | 0 | NO_ITEMS | Merit evaluation is exhaustive |
| E:evaluative:consistency | evaluative | consistency | Coherent Worth | 1 | HAS_ITEMS | Datasheet vs. Specification type terminology |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| E-001 | E:normative:necessity | Conflict | Datasheet | Datasheet | Reconcile Scope Item Status: Datasheet says "TBD (not yet flipped to IN; see OI-036)" while Specification Precondition says "SOW-036 is currently TBD. This specification is a scaffold." These are consistent in substance but use different framing -- Datasheet implies the deliverable may not proceed; Specification implies it is a valid scaffold. Clarify the governance posture: is this deliverable active-scaffold or blocked-pending? | Mandatory Governance lens: the governance status of this deliverable is described with two different framings, which could lead to different interpretations of whether work should continue | Datasheet.md; Specification.md | Datasheet: Conditions table (Scope Status); Specification: Precondition | Datasheet.md#Conditions; Specification.md#Precondition | PROPOSAL: Align framing: both should say "scaffold pending SOW-036 IN decision" | TBD |
| E-002 | E:evaluative:sufficiency | TBD_Question | Guidance | Guidance | Add a target timeline or dependency trigger for resolving CON-001 and CON-002 in the Conflict Table (currently both have HumanRuling=TBD with no resolution path) | Justified Merit lens: the conflict table provides good structure but no indication of when or how the conflicts will be resolved; without a resolution path, the deliverable's justified merit remains hypothetical | Guidance.md | Conflict Table | -- | PROPOSAL: Add "Resolution Trigger" column or note indicating when rulings are expected | TBD |
| E-003 | E:evaluative:consistency | Normalization | Datasheet | Datasheet | Align Type field: Datasheet Identification says "SECURITY_CONTROL" while _CONTEXT.md also says "SECURITY_CONTROL" -- these are consistent. However, Specification does not reference the type classification at all; consider adding a type reference in Specification Scope for traceability | Coherent Worth lens: the type classification exists in Datasheet and _CONTEXT.md but is absent from Specification, creating an incomplete traceability chain for evaluating the deliverable's worth as a security control | Datasheet.md; Specification.md | Datasheet: Identification table (Type); Specification: Scope section | -- | PROPOSAL: Add SECURITY_CONTROL type reference in Specification Scope section | TBD |
