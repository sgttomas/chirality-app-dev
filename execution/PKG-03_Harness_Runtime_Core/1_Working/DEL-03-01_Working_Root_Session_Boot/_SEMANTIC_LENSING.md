# Semantic Lensing Register: DEL-03-01 Working Root Binding & Session Boot

**Generated:** 2026-02-21
**Deliverable Folder:** `/Users/ryan/ai-env/projects/chirality-app-dev1/execution/PKG-03_Harness_Runtime_Core/1_Working/DEL-03-01_Working_Root_Session_Boot/`
**Warnings:** None

**Inputs Read:**
- _CONTEXT.md — `execution/PKG-03_Harness_Runtime_Core/1_Working/DEL-03-01_Working_Root_Session_Boot/_CONTEXT.md`
- _STATUS.md — `execution/PKG-03_Harness_Runtime_Core/1_Working/DEL-03-01_Working_Root_Session_Boot/_STATUS.md`
- _SEMANTIC.md — `execution/PKG-03_Harness_Runtime_Core/1_Working/DEL-03-01_Working_Root_Session_Boot/_SEMANTIC.md`
- Datasheet.md — `execution/PKG-03_Harness_Runtime_Core/1_Working/DEL-03-01_Working_Root_Session_Boot/Datasheet.md`
- Specification.md — `execution/PKG-03_Harness_Runtime_Core/1_Working/DEL-03-01_Working_Root_Session_Boot/Specification.md`
- Guidance.md — `execution/PKG-03_Harness_Runtime_Core/1_Working/DEL-03-01_Working_Root_Session_Boot/Guidance.md`
- Procedure.md — `execution/PKG-03_Harness_Runtime_Core/1_Working/DEL-03-01_Working_Root_Session_Boot/Procedure.md`
- _REFERENCES.md — `execution/PKG-03_Harness_Runtime_Core/1_Working/DEL-03-01_Working_Root_Session_Boot/_REFERENCES.md`

**Purpose:** Apply CHIRALITY_FRAMEWORK matrix cells as lenses over the production documents, capturing warranted enrichment inputs for a later enrichment pass.

---

## Summary

- Total warranted items: 20
- By document:
  - Datasheet: 4
  - Specification: 7
  - Guidance: 4
  - Procedure: 3
  - Multi: 2
- By matrix:
  - A: 4  B: 2  C: 2  F: 3  D: 2  X: 4  E: 3
- By type:
  - Conflict: 1
  - VerificationGap: 4
  - MissingSlot: 5
  - WeakStatement: 3
  - RationaleGap: 3
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
| A:normative:guiding | normative | guiding | prescriptive direction | 1 | HAS_ITEMS | Boot idempotency principle is assumption-flagged; needs normative backing |
| A:normative:applying | normative | applying | mandatory practice | 1 | HAS_ITEMS | Working Root validation rules are assumption-gated |
| A:normative:judging | normative | judging | compliance determination | 1 | HAS_ITEMS | Error response codes/shapes not specified normatively |
| A:normative:reviewing | normative | reviewing | regulatory audit | 0 | NO_ITEMS | Validation script alignment is addressed in Procedure |
| A:operative:guiding | operative | guiding | procedural direction | 0 | NO_ITEMS | Boot flow is well-described across Guidance and Procedure |
| A:operative:applying | operative | applying | practical execution | 0 | NO_ITEMS | Procedure steps cover implementation path |
| A:operative:judging | operative | judging | performance assessment | 0 | NO_ITEMS | Verification table in Specification covers each requirement |
| A:operative:reviewing | operative | reviewing | process audit | 0 | NO_ITEMS | Procedure includes validation script alignment step |
| A:evaluative:guiding | evaluative | guiding | value orientation | 0 | NO_ITEMS | Guidance Purpose section articulates value well |
| A:evaluative:applying | evaluative | applying | merit application | 0 | NO_ITEMS | Trade-offs section covers design merit |
| A:evaluative:judging | evaluative | judging | worth determination | 1 | HAS_ITEMS | No acceptance criteria for boot performance/latency |
| A:evaluative:reviewing | evaluative | reviewing | quality appraisal | 0 | NO_ITEMS | Quality coverage adequate through verification table |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A-001 | A:normative:guiding | WeakStatement | Guidance | Specification | Promote P3 (Boot Is Idempotent Configuration, Not Mutation) from assumption to normative requirement, or record explicit TBD for human ruling | P3 is labeled as an ASSUMPTION inferred from architecture; if boot idempotency is a binding constraint, it should appear as a requirement in Specification | Guidance.md | P3: Boot Is Idempotent Configuration, Not Mutation | — | Specification.md (new REQ) | TBD |
| A-002 | A:normative:applying | TBD_Question | Specification | Specification | Clarify whether Working Root validation accepts any valid directory or requires specific structure (e.g., existing `.chirality/` folder) | REQ-02 includes an explicit ASSUMPTION about empty-directory acceptance; mandatory practice is undefined until this is resolved | Specification.md | REQ-02: Working Root Validation | — | Human decision required | TBD |
| A-003 | A:normative:judging | MissingSlot | Specification | Specification | Add normative error response codes and shapes for session boot failures (session not found, persona not found, SDK failure, Working Root inaccessible) | Guidance C3 enumerates error scenarios but no requirement specifies required HTTP status codes or error response schemas; compliance cannot be determined without them | Specification.md; Guidance.md | REQ-04; C3: Error Handling at Boot | — | Specification.md | TBD |
| A-004 | A:evaluative:judging | MissingSlot | Specification | Specification | Add acceptance criteria or quality threshold for boot latency/performance (e.g., maximum acceptable time from boot request to 200 response) | No performance requirement exists for the boot sequence; worth determination requires measurable thresholds for session boot responsiveness | Specification.md | Verification section (entire) | — | Specification.md | TBD |

---

## Matrix B -- Conceptualization (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| B:data:necessity | data | necessity | essential fact | 1 | HAS_ITEMS | Session storage path is ambiguous |
| B:data:sufficiency | data | sufficiency | adequate evidence | 0 | NO_ITEMS | Datasheet attributes are well-sourced |
| B:data:completeness | data | completeness | comprehensive record | 0 | NO_ITEMS | Datasheet covers all relevant attributes |
| B:data:consistency | data | consistency | reliable measurement | 0 | NO_ITEMS | Source references are consistent |
| B:information:necessity | information | necessity | essential signal | 0 | NO_ITEMS | API contracts provide essential signals |
| B:information:sufficiency | information | sufficiency | adequate context | 0 | NO_ITEMS | Context is adequate across documents |
| B:information:completeness | information | completeness | comprehensive account | 1 | HAS_ITEMS | Boot fingerprint composition undocumented |
| B:information:consistency | information | consistency | coherent message | 0 | NO_ITEMS | Messages are coherent across documents |
| B:knowledge:necessity | knowledge | necessity | fundamental understanding | 0 | NO_ITEMS | Core concepts well-explained in Guidance |
| B:knowledge:sufficiency | knowledge | sufficiency | competent expertise | 0 | NO_ITEMS | Procedure provides sufficient implementation guidance |
| B:knowledge:completeness | knowledge | completeness | thorough mastery | 0 | NO_ITEMS | Cross-deliverable relationships documented |
| B:knowledge:consistency | knowledge | consistency | coherent understanding | 0 | NO_ITEMS | Understanding is coherent |
| B:wisdom:necessity | wisdom | necessity | essential discernment | 0 | NO_ITEMS | Trade-offs in Guidance address discernment |
| B:wisdom:sufficiency | wisdom | sufficiency | adequate judgment | 0 | NO_ITEMS | Trade-off tables provide adequate basis for judgment |
| B:wisdom:completeness | wisdom | completeness | holistic insight | 0 | NO_ITEMS | Holistic view covered via cross-deliverable notes |
| B:wisdom:consistency | wisdom | consistency | principled reasoning | 0 | NO_ITEMS | Reasoning is principled and traced to sources |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| B-001 | B:data:necessity | WeakStatement | Datasheet | Datasheet | Clarify whether `.chirality/sessions/` is relative to the Working Root, the app data directory, or another base path | Datasheet states session storage at `.chirality/sessions/` with "location TBD -- exact path to be confirmed"; this is an essential fact for implementation that remains ambiguous | Datasheet.md | Working Root Binding > Session storage location | — | Human decision + implementation review | TBD |
| B-002 | B:information:completeness | RationaleGap | Guidance | Guidance | Document boot fingerprint composition: what inputs feed `getBootFingerprint(persona, mode)` and how the hash is constructed | Guidance C2 flags this as an ASSUMPTION; comprehensive account of boot fingerprinting is absent, preventing downstream consumers from understanding change detection semantics | Guidance.md | C2: Boot Fingerprinting | — | Guidance.md | TBD |

---

## Matrix C -- Formulation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| C:normative:necessity | normative | necessity | mandatory awareness | 0 | NO_ITEMS | Requirements are clearly stated |
| C:normative:sufficiency | normative | sufficiency | regulated competence | 1 | HAS_ITEMS | SDK interface contract location is TBD |
| C:normative:completeness | normative | completeness | exhaustive mandate | 0 | NO_ITEMS | Requirements cover the full scope |
| C:normative:consistency | normative | consistency | normative coherence | 1 | HAS_ITEMS | Session create payload inconsistency |
| C:operative:necessity | operative | necessity | operational prerequisite | 0 | NO_ITEMS | Prerequisites table in Procedure is adequate |
| C:operative:sufficiency | operative | sufficiency | execution readiness | 0 | NO_ITEMS | Procedure steps are sufficient for execution |
| C:operative:completeness | operative | completeness | operational thoroughness | 0 | NO_ITEMS | Procedure covers all three phases |
| C:operative:consistency | operative | consistency | procedural reliability | 0 | NO_ITEMS | Procedure steps map consistently to requirements |
| C:evaluative:necessity | evaluative | necessity | value imperative | 0 | NO_ITEMS | Value is articulated in Guidance Purpose |
| C:evaluative:sufficiency | evaluative | sufficiency | evaluative adequacy | 0 | NO_ITEMS | Trade-offs provide adequate evaluative framing |
| C:evaluative:completeness | evaluative | completeness | comprehensive valuation | 0 | NO_ITEMS | All relevant trade-offs addressed |
| C:evaluative:consistency | evaluative | consistency | evaluative integrity | 0 | NO_ITEMS | Evaluative perspective is consistent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| C-001 | C:normative:sufficiency | TBD_Question | Specification | Specification | Obtain and reference Anthropic Agent SDK documentation for the `query()` interface used by AgentSdkManager | Specification Standards table lists Anthropic Agent SDK with "location TBD -- SDK documentation external"; regulated competence cannot be confirmed without access to the external standard | Specification.md | Standards table > Anthropic Agent SDK | — | External documentation required | TBD |
| C-002 | C:normative:consistency | Normalization | Multi | Guidance | Align session create payload between Guidance example (shows `{ projectRoot, persona, mode }`) and Specification REQ-03 (mentions only `projectRoot` binding requirement) | Guidance Example shows `POST /api/harness/session/create { projectRoot, persona, mode }` but Specification REQ-03 only requires the session record to include `projectRoot`; the `persona` and `mode` parameters at create-time are not normatively specified | Specification.md; Guidance.md | REQ-03; Example: Minimal Session Boot Flow | Specification.md#REQ-03; Guidance.md#Example: Minimal Session Boot Flow | Specification.md | TBD |

---

## Matrix F -- Requirements (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| F:normative:necessity | normative | necessity | compulsory assurance | 1 | HAS_ITEMS | Error handling requirements absent |
| F:normative:sufficiency | normative | sufficiency | sufficient governance | 0 | NO_ITEMS | Governance through fallback chains is well-specified |
| F:normative:completeness | normative | completeness | exhaustive authority | 1 | HAS_ITEMS | Session record schema not fully specified |
| F:normative:consistency | normative | consistency | regulatory harmony | 0 | NO_ITEMS | Requirements are internally consistent |
| F:operative:necessity | operative | necessity | foundational readiness | 0 | NO_ITEMS | Prerequisites are established |
| F:operative:sufficiency | operative | sufficiency | proven capability | 0 | NO_ITEMS | Verification approaches cover capability proof |
| F:operative:completeness | operative | completeness | total operational coverage | 0 | NO_ITEMS | Procedure covers implementation, testing, documentation |
| F:operative:consistency | operative | consistency | operational consistency | 0 | NO_ITEMS | Procedure steps map reliably to requirements |
| F:evaluative:necessity | evaluative | necessity | essential standard | 0 | NO_ITEMS | Standards table references the needed standards |
| F:evaluative:sufficiency | evaluative | sufficiency | substantiated merit | 0 | NO_ITEMS | Justifications are substantiated |
| F:evaluative:completeness | evaluative | completeness | total valuation scope | 1 | HAS_ITEMS | No requirement for concurrent session handling |
| F:evaluative:consistency | evaluative | consistency | uniform valuation | 0 | NO_ITEMS | Valuation criteria are uniform |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| F-001 | F:normative:necessity | MissingSlot | Specification | Specification | Add a requirement (e.g., REQ-11) specifying error handling behavior for boot failures: required HTTP status codes, error response schema, and session state after failure | Guidance C3 identifies four error scenarios but no normative requirement ensures these are handled; compulsory assurance for failure paths is missing | Specification.md; Guidance.md | entire Requirements section; C3: Error Handling at Boot | — | Specification.md | TBD |
| F-002 | F:normative:completeness | MissingSlot | Specification | Datasheet | Define the complete session record schema (all required fields, types, and persistence format) as a normative artifact | Multiple documents reference session record fields (projectRoot, claudeSessionId, bootFingerprint, bootedAt, sessionId) but no single authoritative schema lists all fields and their types; exhaustive authority requires a complete definition | Specification.md; Datasheet.md | REQ-03; REQ-05; REQ-07; Session Boot API attributes | — | Datasheet.md (descriptive) + Specification.md (normative reference) | TBD |
| F-003 | F:evaluative:completeness | RationaleGap | Guidance | Guidance | Add consideration for concurrent session behavior: can multiple sessions be booted simultaneously, and how does the runtime handle concurrent boot requests? | The Specification defines CRUD for sessions (multiple can exist) but neither Specification nor Guidance addresses concurrent boot behavior; total valuation scope requires understanding whether this is in-scope or explicitly excluded | Guidance.md | Considerations section (entire) | — | Guidance.md | TBD |

---

## Matrix D -- Objectives (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| D:normative:guiding | normative | guiding | definitive prescription | 0 | NO_ITEMS | Prescriptions are clearly stated |
| D:normative:applying | normative | applying | enforced conformance | 1 | HAS_ITEMS | Bootstrap turn behavior underspecified |
| D:normative:judging | normative | judging | conclusive adjudication | 0 | NO_ITEMS | Verification approaches support adjudication |
| D:normative:reviewing | normative | reviewing | reconciled oversight | 0 | NO_ITEMS | Oversight mechanisms adequate |
| D:operative:guiding | operative | guiding | prepared guidance | 0 | NO_ITEMS | Guidance adequately prepares implementers |
| D:operative:applying | operative | applying | validated execution | 0 | NO_ITEMS | Execution steps are validated through verification |
| D:operative:judging | operative | judging | definitive assessment | 0 | NO_ITEMS | Assessment criteria defined |
| D:operative:reviewing | operative | reviewing | stabilized review | 0 | NO_ITEMS | Review path through validation scripts established |
| D:evaluative:guiding | evaluative | guiding | grounded value direction | 0 | NO_ITEMS | Value direction well-grounded in Guidance Purpose |
| D:evaluative:applying | evaluative | applying | demonstrated worth | 0 | NO_ITEMS | Worth demonstrated through examples |
| D:evaluative:judging | evaluative | judging | conclusive valuation | 1 | HAS_ITEMS | Missing success/failure criteria for bootstrap turn |
| D:evaluative:reviewing | evaluative | reviewing | calibrated reflection | 0 | NO_ITEMS | Reflection calibrated through trade-offs |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| D-001 | D:normative:applying | WeakStatement | Specification | Specification | Clarify what constitutes a successful bootstrap turn in REQ-05 step 3: what does AgentSdkManager.startTurn return, and what conditions indicate success vs failure? | REQ-05 step 3 says "Execute a bootstrap turn via AgentSdkManager" but does not specify success/failure criteria for the bootstrap turn itself; enforced conformance requires unambiguous pass/fail | Specification.md | REQ-05: Boot Initialization Sequence | — | Specification.md | TBD |
| D-002 | D:evaluative:judging | VerificationGap | Specification | Specification | Add verification criteria for bootstrap turn success: what observable outcome confirms the bootstrap turn completed correctly? | REQ-05 verification says "verify boot fingerprint, claudeSessionId, and bootedAt are persisted" but does not verify the bootstrap turn's own output or side effects; conclusive valuation of the boot sequence requires observable success criteria for the SDK interaction | Specification.md | Verification table > REQ-05 | — | Specification.md | TBD |

---

## Matrix X -- Verification (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| X:guiding:necessity | guiding | necessity | orienting prerequisite | 0 | NO_ITEMS | Prerequisites are well-oriented |
| X:guiding:sufficiency | guiding | sufficiency | sufficient orientation | 0 | NO_ITEMS | Guidance provides sufficient orientation |
| X:guiding:completeness | guiding | completeness | comprehensive direction | 0 | NO_ITEMS | Direction is comprehensive |
| X:guiding:consistency | guiding | consistency | steadfast direction | 0 | NO_ITEMS | Direction is consistent |
| X:applying:necessity | applying | necessity | verified prerequisite | 1 | HAS_ITEMS | Missing prerequisite for session create before boot |
| X:applying:sufficiency | applying | sufficiency | confirmed competence | 0 | NO_ITEMS | Competence confirmation adequate |
| X:applying:completeness | applying | completeness | exhaustive implementation | 1 | HAS_ITEMS | No negative/boundary test for boot without prior create |
| X:applying:consistency | applying | consistency | dependable conformance | 0 | NO_ITEMS | Conformance is dependable |
| X:judging:necessity | judging | necessity | decisive criterion | 1 | HAS_ITEMS | Missing acceptance criteria for REQ-09 |
| X:judging:sufficiency | judging | sufficiency | adjudicated sufficiency | 0 | NO_ITEMS | Sufficiency is adjudicated through verification table |
| X:judging:completeness | judging | completeness | exhaustive adjudication | 1 | HAS_ITEMS | Verification approach for REQ-06 incomplete |
| X:judging:consistency | judging | consistency | principled adjudication | 0 | NO_ITEMS | Adjudication principles are consistent |
| X:reviewing:necessity | reviewing | necessity | essential retrospection | 0 | NO_ITEMS | Retrospection adequately supported |
| X:reviewing:sufficiency | reviewing | sufficiency | tempered sufficiency | 0 | NO_ITEMS | Sufficiency is tempered appropriately |
| X:reviewing:completeness | reviewing | completeness | thorough reconciliation | 0 | NO_ITEMS | Reconciliation is thorough |
| X:reviewing:consistency | reviewing | consistency | sustained coherence | 0 | NO_ITEMS | Coherence is sustained |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| X-001 | X:applying:necessity | VerificationGap | Procedure | Procedure | Add explicit prerequisite check: verify session exists (via prior create call) before attempting boot in integration test steps | Procedure Step 8 integration tests list "Full session lifecycle: create -> boot -> verify..." but do not include a negative test for booting a non-existent session as a verified prerequisite; the happy-path assumes create precedes boot without verifying the guard | Procedure.md | Step 8: Integration Tests | — | Procedure.md | TBD |
| X-002 | X:applying:completeness | VerificationGap | Procedure | Procedure | Add integration test case: attempt boot on a session that was never created (distinct from invalid sessionId); verify error response and session state | Procedure Step 8 lists "Boot with invalid sessionId (error handling)" but does not distinguish between a malformed sessionId and a well-formed but non-existent one; exhaustive implementation verification requires both cases | Procedure.md | Step 8: Integration Tests | — | Procedure.md | TBD |
| X-003 | X:judging:necessity | VerificationGap | Specification | Specification | Add concrete acceptance criteria for REQ-09 (Instruction Root vs Working Root Separation): specify what file/path patterns constitute each root and how to verify separation programmatically | REQ-09 verification says "verify persona prompt loaded from instruction root, agent executes against working root" but provides no decisive criterion for what constitutes "loaded from" or "executes against" in a testable manner | Specification.md | Verification table > REQ-09 | — | Specification.md | TBD |
| X-004 | X:judging:completeness | MissingSlot | Specification | Specification | Add verification for opts fallback chain edge case: what happens when all three levels of a chain are absent (no opts value, no persona frontmatter, no runtime default)? | REQ-06 verification says "verify each fallback chain with/without opts values" but does not address the case where the entire chain resolves to nothing; exhaustive adjudication requires this boundary | Specification.md | Verification table > REQ-06 | — | Specification.md | TBD |

---

## Matrix E -- Evaluation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| E:normative:necessity | normative | necessity | binding foundation | 0 | NO_ITEMS | Foundation is binding and well-established |
| E:normative:sufficiency | normative | sufficiency | governed sufficiency | 0 | NO_ITEMS | Sufficiency is governed |
| E:normative:completeness | normative | completeness | total prescriptive scope | 1 | HAS_ITEMS | Responsible party is TBD |
| E:normative:consistency | normative | consistency | enduring compliance | 1 | HAS_ITEMS | Terminology inconsistency across documents |
| E:operative:necessity | operative | necessity | validated foundation | 0 | NO_ITEMS | Foundation validated through prerequisites |
| E:operative:sufficiency | operative | sufficiency | demonstrated readiness | 0 | NO_ITEMS | Readiness demonstrated |
| E:operative:completeness | operative | completeness | total operational assurance | 0 | NO_ITEMS | Operational assurance is total |
| E:operative:consistency | operative | consistency | sustained reliability | 0 | NO_ITEMS | Reliability sustained |
| E:evaluative:necessity | evaluative | necessity | authoritative standard | 0 | NO_ITEMS | Standards are authoritative |
| E:evaluative:sufficiency | evaluative | sufficiency | substantiated sufficiency | 0 | NO_ITEMS | Sufficiency is substantiated |
| E:evaluative:completeness | evaluative | completeness | integral valuation | 0 | NO_ITEMS | Valuation is integral |
| E:evaluative:consistency | evaluative | consistency | enduring value fidelity | 1 | HAS_ITEMS | Session storage path conflict across documents |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| E-001 | E:normative:completeness | RationaleGap | Datasheet | Datasheet | Assign Responsible Party (currently TBD) for this deliverable | Datasheet Identification table lists Responsible Party as TBD; total prescriptive scope requires accountability assignment for the deliverable | Datasheet.md | Identification table > Responsible Party | — | Human decision | TBD |
| E-002 | E:normative:consistency | Normalization | Multi | Guidance | Standardize session storage path terminology: use a single canonical term and location across all documents | Datasheet says ".chirality/sessions/ under the app's state path" (with TBD caveat), Guidance T2 discusses "Under Working Root" vs "Under app data directory" as unresolved trade-off, and Specification REQ-07 says only "local filesystem" without specifying path; enduring compliance requires a single canonical answer | Datasheet.md; Guidance.md; Specification.md | Datasheet: Session storage location; Guidance: T2; Specification: REQ-07 | Datasheet.md#Session-storage-location; Guidance.md#T2; Specification.md#REQ-07 | Human decision (depends on T2 resolution) | TBD |
| E-003 | E:evaluative:consistency | Conflict | Guidance | Guidance | Resolve whether session storage is under the Working Root or under the app data directory; Guidance T2 presents both as open options while Datasheet assumes `.chirality/sessions/` under app state path | Guidance T2 explicitly presents this as an unresolved trade-off with an ASSUMPTION annotation, while Datasheet records a specific path; enduring value fidelity requires these to agree | Datasheet.md; Guidance.md | Datasheet: Working Root Binding > Session storage location; Guidance: T2: Session Storage Location | Datasheet.md#Working-Root-Binding; Guidance.md#T2-Session-Storage-Location | Human decision | TBD |
