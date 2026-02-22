# Semantic Lensing Register: DEL-03-02 Turn Execution API + SSE Streaming

**Generated:** 2026-02-21
**Deliverable Folder:** execution/PKG-03_Harness_Runtime_Core/1_Working/DEL-03-02_Turn_Execution_SSE_Streaming/
**Warnings:** None

**Inputs Read:**
- _CONTEXT.md — `execution/PKG-03_Harness_Runtime_Core/1_Working/DEL-03-02_Turn_Execution_SSE_Streaming/_CONTEXT.md`
- _STATUS.md — `execution/PKG-03_Harness_Runtime_Core/1_Working/DEL-03-02_Turn_Execution_SSE_Streaming/_STATUS.md`
- _SEMANTIC.md — `execution/PKG-03_Harness_Runtime_Core/1_Working/DEL-03-02_Turn_Execution_SSE_Streaming/_SEMANTIC.md`
- Datasheet.md — `execution/PKG-03_Harness_Runtime_Core/1_Working/DEL-03-02_Turn_Execution_SSE_Streaming/Datasheet.md`
- Specification.md — `execution/PKG-03_Harness_Runtime_Core/1_Working/DEL-03-02_Turn_Execution_SSE_Streaming/Specification.md`
- Guidance.md — `execution/PKG-03_Harness_Runtime_Core/1_Working/DEL-03-02_Turn_Execution_SSE_Streaming/Guidance.md`
- Procedure.md — `execution/PKG-03_Harness_Runtime_Core/1_Working/DEL-03-02_Turn_Execution_SSE_Streaming/Procedure.md`
- _REFERENCES.md — `execution/PKG-03_Harness_Runtime_Core/1_Working/DEL-03-02_Turn_Execution_SSE_Streaming/_REFERENCES.md`

**Purpose:** Apply CHIRALITY_FRAMEWORK matrix cells as lenses over the production documents, capturing warranted enrichment inputs for a later enrichment pass.

## Summary

- Total warranted items: 28
- By document:
  - Datasheet: 5
  - Specification: 10
  - Guidance: 4
  - Procedure: 5
  - Multi: 4
- By matrix:
  - A: 6  B: 4  C: 3  F: 3  D: 4  X: 5  E: 3
- By type:
  - Conflict: 0
  - VerificationGap: 6
  - MissingSlot: 10
  - WeakStatement: 4
  - RationaleGap: 3
  - Normalization: 2
  - TBD_Question: 3
  - MatrixError: 0
- Notable conflicts: 0
- Matrix parse errors: 0

---

## Matrix A -- Orientation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| A:normative:guiding | normative | guiding | prescriptive direction | 1 | HAS_ITEMS | SSE event taxonomy lacks prescriptive direction |
| A:normative:applying | normative | applying | mandatory practice | 1 | HAS_ITEMS | REQ-03 SSE event types TBD |
| A:normative:judging | normative | judging | compliance determination | 1 | HAS_ITEMS | No acceptance criteria for concurrent turn rejection |
| A:normative:reviewing | normative | reviewing | regulatory audit | 0 | NO_ITEMS | Verification table covers all REQs adequately |
| A:operative:guiding | operative | guiding | procedural direction | 1 | HAS_ITEMS | Procedure prerequisites rely on assumptions about DEL readiness |
| A:operative:applying | operative | applying | practical execution | 0 | NO_ITEMS | Implementation steps are well-structured |
| A:operative:judging | operative | judging | performance assessment | 1 | HAS_ITEMS | No performance criteria for SSE latency or throughput |
| A:operative:reviewing | operative | reviewing | process audit | 0 | NO_ITEMS | Verification checks in Procedure are adequate |
| A:evaluative:guiding | evaluative | guiding | value orientation | 0 | NO_ITEMS | Guidance P1-P4 principles are well-articulated |
| A:evaluative:applying | evaluative | applying | merit application | 0 | NO_ITEMS | Documents are consistent on value proposition |
| A:evaluative:judging | evaluative | judging | worth determination | 1 | HAS_ITEMS | No quality attribute targets defined |
| A:evaluative:reviewing | evaluative | reviewing | quality appraisal | 0 | NO_ITEMS | Verification approach covers quality aspects |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A-001 | A:normative:guiding | MissingSlot | Specification | Specification | Add a requirement (or annex) prescribing the SSE event taxonomy: event names, payload schemas, sequencing constraints | REQ-03 notes SSE event taxonomy is TBD with an ASSUMPTION tag; no prescriptive direction exists for event naming or payload structure | Specification.md | REQ-03: SSE Streaming Protocol | — | Specification.md (normative home for event contract) | TBD |
| A-002 | A:normative:applying | WeakStatement | Specification | Specification | Strengthen REQ-03 ASSUMPTION on SSE event taxonomy to either a concrete requirement or a tracked TBD with resolution criteria | REQ-03 contains "ASSUMPTION: Specific SSE event type taxonomy ... is TBD" which defers a mandatory practice without a resolution path | Specification.md | REQ-03: SSE Streaming Protocol | — | Specification.md | TBD |
| A-003 | A:normative:judging | MissingSlot | Specification | Specification | Add acceptance criteria for concurrent turn handling: specify whether the endpoint MUST reject a second in-flight turn for the same session | Guidance C4 raises the concurrent turn question but no normative requirement or acceptance criterion exists to determine compliance | Specification.md; Guidance.md | Specification.md#Requirements (absent); Guidance.md#C4 | — | Specification.md | TBD |
| A-004 | A:operative:guiding | WeakStatement | Procedure | Procedure | Clarify prerequisite statuses: replace ASSUMPTION tags on DEL-03-01, DEL-03-03, DEL-03-05, DEL-04-01 readiness with concrete "check X before proceeding" gates or fallback instructions | Procedure prerequisites are all marked ASSUMPTION with no procedural direction for how to verify or work around unavailable dependencies | Procedure.md | Prerequisites > Required Deliverables / Inputs | — | Procedure.md | TBD |
| A-005 | A:operative:judging | MissingSlot | Specification | Specification | Add performance/latency requirements for SSE event delivery (e.g., max time-to-first-event, event throughput targets) | Guidance C5 raises performance and backpressure concerns but no operative assessment criteria exist in the Specification | Specification.md; Guidance.md | Specification.md#Verification (absent); Guidance.md#C5 | — | Specification.md | TBD |
| A-006 | A:evaluative:judging | MissingSlot | Specification | Specification | Define quality attribute targets: reliability target for stream completion, maximum acceptable event loss rate | No quality attribute thresholds are stated anywhere in the document set; worth determination cannot be made without them | Specification.md | entire document scanned | — | Specification.md | TBD |

---

## Matrix B -- Conceptualization (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| B:data:necessity | data | necessity | essential fact | 1 | HAS_ITEMS | Event type enumeration missing |
| B:data:sufficiency | data | sufficiency | adequate evidence | 0 | NO_ITEMS | Datasheet attributes are well-sourced |
| B:data:completeness | data | completeness | comprehensive record | 1 | HAS_ITEMS | Datasheet Construction Event Types TBD |
| B:data:consistency | data | consistency | reliable measurement | 0 | NO_ITEMS | Data references are internally consistent |
| B:information:necessity | information | necessity | essential signal | 1 | HAS_ITEMS | Error handling signal taxonomy missing |
| B:information:sufficiency | information | sufficiency | adequate context | 0 | NO_ITEMS | Context provided for each requirement is adequate |
| B:information:completeness | information | completeness | comprehensive account | 0 | NO_ITEMS | Scope and boundary notes are comprehensive |
| B:information:consistency | information | consistency | coherent message | 0 | NO_ITEMS | Documents present a coherent message on architecture |
| B:knowledge:necessity | knowledge | necessity | fundamental understanding | 0 | NO_ITEMS | Integration architecture is well-explained in Guidance |
| B:knowledge:sufficiency | knowledge | sufficiency | competent expertise | 0 | NO_ITEMS | SDK integration considerations in Guidance C3 are adequate |
| B:knowledge:completeness | knowledge | completeness | thorough mastery | 0 | NO_ITEMS | Coverage is sufficient for an integration deliverable |
| B:knowledge:consistency | knowledge | consistency | coherent understanding | 0 | NO_ITEMS | All documents share a coherent understanding of the turn pipeline |
| B:wisdom:necessity | wisdom | necessity | essential discernment | 0 | NO_ITEMS | Trade-offs T1 and T2 demonstrate adequate discernment |
| B:wisdom:sufficiency | wisdom | sufficiency | adequate judgment | 1 | HAS_ITEMS | Client disconnect handling rationale missing |
| B:wisdom:completeness | wisdom | completeness | holistic insight | 0 | NO_ITEMS | Guidance provides adequate holistic perspective |
| B:wisdom:consistency | wisdom | consistency | principled reasoning | 0 | NO_ITEMS | Reasoning across documents is principled and consistent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| B-001 | B:data:necessity | MissingSlot | Datasheet | Datasheet | Add an enumeration of SSE event types to the Datasheet Construction or Attributes table (even if initially TBD with placeholders) | Datasheet Construction section records "Event Types: TBD" but does not enumerate even the known categories; this is an essential fact for the deliverable | Datasheet.md | Construction > Event Types | — | Datasheet.md | TBD |
| B-002 | B:data:completeness | MissingSlot | Datasheet | Datasheet | Add error code enumeration to the Datasheet: HTTP status codes returned by the endpoint (400, 200, others) and mid-stream error event codes | Datasheet records partial/full failure behavior descriptively but does not provide a comprehensive record of error codes | Datasheet.md | Attributes; Construction > Error Handling | — | Datasheet.md | TBD |
| B-003 | B:information:necessity | MissingSlot | Specification | Specification | Add a requirement specifying the error event schema for mid-stream errors (event name, payload fields, severity indicators) | Guidance C2 identifies mid-stream vs. pre-stream error distinction as essential, but no requirement in Specification defines the error event signal format | Specification.md; Guidance.md | Specification.md#Requirements (absent); Guidance.md#C2 | — | Specification.md | TBD |
| B-004 | B:wisdom:sufficiency | RationaleGap | Guidance | Guidance | Add rationale for client disconnect handling strategy: why detect-and-cleanup is chosen, what resources are at risk, and what the expected SDK behavior is on cancellation | Guidance P1 mentions client disconnect handling but does not explain the judgment behind the chosen approach or what happens to in-flight SDK calls | Guidance.md | P1: Streaming-First Architecture | — | Guidance.md | TBD |

---

## Matrix C -- Formulation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| C:normative:necessity | normative | necessity | Compulsory Regulatory Foundation | 1 | HAS_ITEMS | Binding foundation for network policy enforcement unclear at turn level |
| C:normative:sufficiency | normative | sufficiency | Prescribed Compliance Adequacy | 0 | NO_ITEMS | Compliance scope is adequately prescribed |
| C:normative:completeness | normative | completeness | Total Compliance Coverage | 1 | HAS_ITEMS | Verification gap for REQ-08 |
| C:normative:consistency | normative | consistency | Harmonized Regulatory Discipline | 0 | NO_ITEMS | Requirements are internally consistent |
| C:operative:necessity | operative | necessity | Operational Execution Demand | 0 | NO_ITEMS | Execution demands are well-specified |
| C:operative:sufficiency | operative | sufficiency | Competent Operational Practice | 0 | NO_ITEMS | Procedure steps are competently structured |
| C:operative:completeness | operative | completeness | Exhaustive Operational Mastery | 0 | NO_ITEMS | Procedure covers all phases adequately |
| C:operative:consistency | operative | consistency | Synchronized Process Coherence | 0 | NO_ITEMS | Procedure aligns with Specification requirements |
| C:evaluative:necessity | evaluative | necessity | Foundational Worth Discernment | 0 | NO_ITEMS | Value proposition is clear |
| C:evaluative:sufficiency | evaluative | sufficiency | Grounded Merit Judgment | 0 | NO_ITEMS | Merit arguments are grounded |
| C:evaluative:completeness | evaluative | completeness | Comprehensive Worth Accounting | 1 | HAS_ITEMS | No success metrics for the deliverable itself |
| C:evaluative:consistency | evaluative | consistency | Principled Worth Coherence | 0 | NO_ITEMS | Worth reasoning is coherent across documents |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| C-001 | C:normative:necessity | TBD_Question | Specification | Specification | Clarify: Does DEL-03-02 need to enforce or verify the network policy (DEC-NET-001: outbound to Anthropic API only) at the turn endpoint level, or is this purely DEL-03-06 scope? | Datasheet lists DEC-NET-001 as a condition and the Specification exclusions list DEL-03-06 for enforcement, but it is unclear whether the turn endpoint has any verification obligation | Datasheet.md; Specification.md | Datasheet.md#Conditions; Specification.md#Excluded | — | Human ruling needed | TBD |
| C-002 | C:normative:completeness | VerificationGap | Specification | Specification | Add verification approach for REQ-08 (client-supplied metadata non-authoritative): the verification table entry says "submit client metadata; verify server reclassifies" but lacks detail on what metadata fields to test and how to confirm server reclassification | REQ-08 verification is stated at a high level but may be insufficient to confirm total compliance -- specific test vectors needed | Specification.md | Verification table, REQ-08 row | — | Specification.md | TBD |
| C-003 | C:evaluative:completeness | MissingSlot | Guidance | Guidance | Add success metrics or definition of "done" for the deliverable: what constitutes a complete, successful implementation of the turn execution pipeline | No comprehensive worth accounting exists -- the documents describe what to build but not how to measure whether the result is adequate beyond test pass/fail | Guidance.md | entire document scanned | — | Guidance.md | TBD |

---

## Matrix F -- Requirements (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| F:normative:necessity | normative | necessity | Non-Negotiable Statutory Mandate | 1 | HAS_ITEMS | API key availability not verified at turn level |
| F:normative:sufficiency | normative | sufficiency | Justified Conformance Authority | 0 | NO_ITEMS | Conformance authority is justified |
| F:normative:completeness | normative | completeness | Total Prescriptive Mastery | 0 | NO_ITEMS | Requirements cover the scope |
| F:normative:consistency | normative | consistency | Consistent Statutory Enforcement | 0 | NO_ITEMS | Enforcement is consistent |
| F:operative:necessity | operative | necessity | Essential Workflow Readiness | 1 | HAS_ITEMS | SDK documentation location TBD |
| F:operative:sufficiency | operative | sufficiency | Contextualized Execution Capability | 0 | NO_ITEMS | Execution context is sufficient |
| F:operative:completeness | operative | completeness | Exhaustive Workflow Command | 0 | NO_ITEMS | Workflow steps are exhaustive |
| F:operative:consistency | operative | consistency | Stable Process Synchronization | 0 | NO_ITEMS | Process is synchronized across documents |
| F:evaluative:necessity | evaluative | necessity | Core Appraisal Imperative | 0 | NO_ITEMS | Core value is clear |
| F:evaluative:sufficiency | evaluative | sufficiency | Justified Appraisal Competence | 0 | NO_ITEMS | Appraisal competence is justified |
| F:evaluative:completeness | evaluative | completeness | Total Appraisal Scope | 1 | HAS_ITEMS | Test result storage location TBD |
| F:evaluative:consistency | evaluative | consistency | Principled Appraisal Harmony | 0 | NO_ITEMS | Appraisal reasoning is harmonious |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| F-001 | F:normative:necessity | VerificationGap | Specification | Specification | Add verification step for API key availability: how should the turn endpoint behave when an API key is not provisioned (given OI-001 is open)? Should it return a specific error before opening the SSE stream? | Datasheet Conditions list "API Key Available" with an open issue (OI-001), but no requirement in Specification addresses turn-level behavior when the key is absent, and no verification entry covers this scenario | Specification.md; Datasheet.md | Specification.md#Requirements (absent); Datasheet.md#Conditions | — | Specification.md | TBD |
| F-002 | F:operative:necessity | TBD_Question | Procedure | Procedure | Resolve "location TBD" for Anthropic SDK documentation in Procedure prerequisites; record actual URL or package reference | Procedure lists Anthropic SDK documentation as a required reference with "location TBD"; this blocks essential workflow readiness | Procedure.md | Prerequisites > Required References | — | Human ruling needed | TBD |
| F-003 | F:evaluative:completeness | WeakStatement | Procedure | Procedure | Replace TBD placeholders in Records table (test output location, DOC artifact location, SSE event taxonomy location) with concrete paths or resolution criteria | Procedure Records section has three "TBD" entries for output locations, making total appraisal scope impossible to verify | Procedure.md | Records table | — | Procedure.md | TBD |

---

## Matrix D -- Objectives (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| D:normative:guiding | normative | guiding | Enforceable Prescriptive Course | 1 | HAS_ITEMS | Subagent governance boundary vague |
| D:normative:applying | normative | applying | Obligatory Compliance Execution | 0 | NO_ITEMS | Compliance execution is clearly specified |
| D:normative:judging | normative | judging | Definitive Conformance Ruling | 1 | HAS_ITEMS | Verification for stream termination |
| D:normative:reviewing | normative | reviewing | Systematic Compliance Inspection | 0 | NO_ITEMS | Verification table provides systematic inspection |
| D:operative:guiding | operative | guiding | Resolved Process Navigation | 0 | NO_ITEMS | Process navigation is resolved in Procedure |
| D:operative:applying | operative | applying | Settled Functional Enactment | 0 | NO_ITEMS | Functional implementation steps are settled |
| D:operative:judging | operative | judging | Decisive Performance Verdict | 1 | HAS_ITEMS | Platform verification scope unclear |
| D:operative:reviewing | operative | reviewing | Settled Workflow Scrutiny | 0 | NO_ITEMS | Workflow scrutiny is adequately addressed |
| D:evaluative:guiding | evaluative | guiding | Settled Quality Bearing | 0 | NO_ITEMS | Quality bearing is settled via principles |
| D:evaluative:applying | evaluative | applying | Grounded Worth Enactment | 0 | NO_ITEMS | Worth is grounded in scope coverage |
| D:evaluative:judging | evaluative | judging | Comprehensive Merit Ruling | 1 | HAS_ITEMS | No definition of what constitutes a "complete" turn |
| D:evaluative:reviewing | evaluative | reviewing | Congruent Quality Inspection | 0 | NO_ITEMS | Quality inspection is congruent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| D-001 | D:normative:guiding | WeakStatement | Specification | Guidance | Clarify the prescriptive boundary for subagent governance at the turn level: Specification notes "enforcement is DEL-03-04 scope" and Datasheet says "Fail-closed ... Note: enforcement is DEL-03-04 scope" but the turn endpoint must presumably detect and act on governance results -- what is the exact contract? | The prescriptive course for governance at the turn level is ambiguous; documents say enforcement is elsewhere but the turn endpoint must still respond to governance gate outputs | Specification.md; Datasheet.md | Specification.md#Excluded; Datasheet.md#Attributes (Subagent Governance row) | — | Guidance.md (directional clarification) | TBD |
| D-002 | D:normative:judging | VerificationGap | Specification | Specification | Add specific verification criteria for SSE stream termination: define what "terminates cleanly" means (final event type, connection close behavior, timeout) | REQ-03 says "stream MUST terminate cleanly" and verification says "test normal and error completion" but no definitive criteria exist for what constitutes clean termination | Specification.md | REQ-03; Verification table REQ-03 row | — | Specification.md | TBD |
| D-003 | D:operative:judging | VerificationGap | Procedure | Procedure | Clarify platform verification scope: does Step 3.4 require all tests to be rerun on macOS 15+ Apple Silicon, or only specific integration tests? Define pass criteria more precisely | Procedure Step 3.4 says "Run tests on macOS 15+ / Apple Silicon" but does not specify which tests or whether this is a full rerun or targeted verification | Procedure.md | Phase 3 > Step 3.4 | — | Procedure.md | TBD |
| D-004 | D:evaluative:judging | RationaleGap | Guidance | Guidance | Add definition of turn completion semantics: what constitutes a "complete" turn (all tool calls resolved? final assistant message emitted? explicit turn_end event?) for merit evaluation purposes | No document defines what a complete turn looks like from an evaluative standpoint; this affects how success is measured | Guidance.md | entire document scanned | — | Guidance.md | TBD |

---

## Matrix X -- Verification (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| X:guiding:necessity | guiding | necessity | Authoritative Execution Ground | 1 | HAS_ITEMS | Request body schema not normatively defined |
| X:guiding:sufficiency | guiding | sufficiency | Competent Directive Threshold | 0 | NO_ITEMS | Directive threshold is competent |
| X:guiding:completeness | guiding | completeness | Holistic Prescriptive Span | 1 | HAS_ITEMS | Response body schema undefined |
| X:guiding:consistency | guiding | consistency | Harmonized Directive Unity | 1 | HAS_ITEMS | Terminology inconsistency |
| X:applying:necessity | applying | necessity | Compulsory Implementation Ground | 0 | NO_ITEMS | Implementation ground is established |
| X:applying:sufficiency | applying | sufficiency | Competent Implementation Adequacy | 0 | NO_ITEMS | Implementation adequacy is competent |
| X:applying:completeness | applying | completeness | Total Implementation Enactment | 0 | NO_ITEMS | Implementation scope is total |
| X:applying:consistency | applying | consistency | Synchronized Implementation Delivery | 0 | NO_ITEMS | Implementation delivery is synchronized |
| X:judging:necessity | judging | necessity | Vital Adjudication Basis | 1 | HAS_ITEMS | No requirement for session validation failure behavior |
| X:judging:sufficiency | judging | sufficiency | Substantiated Adjudication Finding | 0 | NO_ITEMS | Adjudication findings are substantiated |
| X:judging:completeness | judging | completeness | Total Adjudication Command | 0 | NO_ITEMS | Adjudication command is adequate |
| X:judging:consistency | judging | consistency | Disciplined Adjudication Order | 0 | NO_ITEMS | Adjudication order is disciplined |
| X:reviewing:necessity | reviewing | necessity | Compulsory Examination Ground | 1 | HAS_ITEMS | Test infrastructure TBD |
| X:reviewing:sufficiency | reviewing | sufficiency | Competent Examination Breadth | 0 | NO_ITEMS | Examination breadth is competent |
| X:reviewing:completeness | reviewing | completeness | Total Examination Coverage | 0 | NO_ITEMS | Examination coverage is adequate for current scope |
| X:reviewing:consistency | reviewing | consistency | Harmonized Examination Discipline | 0 | NO_ITEMS | Examination discipline is harmonized |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| X-001 | X:guiding:necessity | MissingSlot | Specification | Datasheet | Add a normative request body schema (JSON schema or equivalent) for `POST /api/harness/turn` including field names, types, required/optional, and constraints | REQ-01 lists field names and types in prose but no formal schema exists; the Guidance example is marked illustrative; authoritative execution ground requires a definitive schema | Specification.md; Guidance.md | Specification.md#REQ-01; Guidance.md#Examples | — | Datasheet.md (descriptive; schema enumeration) | TBD |
| X-002 | X:guiding:completeness | MissingSlot | Multi | Datasheet | Define the SSE response schema: Content-Type header value, event format (id/event/data fields), and connection lifecycle headers | No document provides a holistic definition of the SSE response format; Guidance example is illustrative only; Specification REQ-03 says "using SSE" but not how | Specification.md; Guidance.md; Datasheet.md | Specification.md#REQ-03; Guidance.md#Examples; Datasheet.md#Construction | — | Datasheet.md (descriptive enumeration) | TBD |
| X-003 | X:guiding:consistency | Normalization | Multi | Guidance | Harmonize terminology for the options object: Datasheet uses "Turn options object with runtime option mapping," Specification uses "`opts` (object, optional): turn options for runtime mapping," Guidance uses "`opts`" and "options mapping"; standardize on one term and definition | Minor terminological variance across documents risks drift as implementation proceeds | Datasheet.md; Specification.md; Guidance.md | Datasheet.md#Attributes; Specification.md#REQ-07; Guidance.md#P4 | — | Guidance.md (vocabulary note) | TBD |
| X-004 | X:judging:necessity | VerificationGap | Specification | Specification | Add a requirement and verification criterion for session-not-active behavior: what HTTP status code and error body does the endpoint return when REQ-02 step 1 fails? | REQ-02 says "validate that a session is active" but no requirement specifies the failure response; adjudication of session validation failure has no basis | Specification.md | REQ-02 step 1 | — | Specification.md | TBD |
| X-005 | X:reviewing:necessity | TBD_Question | Procedure | Procedure | Identify and document the test infrastructure for SSE consumption: what HTTP client or test library will be used to verify streaming responses? Record in Procedure prerequisites | Procedure lists "Test harness or HTTP client capable of SSE consumption" with no specific tool identified; compulsory examination ground requires this to be resolved before testing | Procedure.md | Prerequisites > Required Tools / Environment | — | Human ruling needed | TBD |

---

## Matrix E -- Evaluation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| E:normative:necessity | normative | necessity | Obligatory Regulatory Bedrock | 0 | NO_ITEMS | Regulatory bedrock is established via K-invariants |
| E:normative:sufficiency | normative | sufficiency | Substantiated Regulatory Threshold | 1 | HAS_ITEMS | Standards table has unverified assumptions |
| E:normative:completeness | normative | completeness | Comprehensive Regulatory Command | 0 | NO_ITEMS | Regulatory command is comprehensive for current scope |
| E:normative:consistency | normative | consistency | Disciplined Regulatory Uniformity | 1 | HAS_ITEMS | Responsible party TBD |
| E:operative:necessity | operative | necessity | Definitive Operational Obligation | 0 | NO_ITEMS | Operational obligations are definitive |
| E:operative:sufficiency | operative | sufficiency | Substantiated Operational Capacity | 0 | NO_ITEMS | Operational capacity is substantiated |
| E:operative:completeness | operative | completeness | Total Operational Enactment | 0 | NO_ITEMS | Operational enactment scope is total |
| E:operative:consistency | operative | consistency | Synchronized Operational Discipline | 0 | NO_ITEMS | Operational discipline is synchronized |
| E:evaluative:necessity | evaluative | necessity | Fundamental Quality Bedrock | 0 | NO_ITEMS | Quality bedrock is established |
| E:evaluative:sufficiency | evaluative | sufficiency | Substantiated Merit Capacity | 0 | NO_ITEMS | Merit capacity is substantiated |
| E:evaluative:completeness | evaluative | completeness | Comprehensive Merit Command | 1 | HAS_ITEMS | No traceability from REQs to SOW items |
| E:evaluative:consistency | evaluative | consistency | Harmonized Quality Discipline | 0 | NO_ITEMS | Quality discipline is harmonized |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| E-001 | E:normative:sufficiency | VerificationGap | Specification | Specification | Resolve the three "ASSUMPTION: likely applicable; location TBD" entries in the Standards table (Anthropic SDK docs, SSE spec, Next.js conventions): either confirm applicability and provide locations, or remove with rationale | Standards table includes three unverified external standards marked as assumptions; substantiated regulatory threshold requires confirmed or excluded standards | Specification.md | Standards table | — | Specification.md | TBD |
| E-002 | E:normative:consistency | Normalization | Datasheet | Datasheet | Resolve "Responsible Party: TBD" in the Datasheet Identification table; assign ownership to maintain disciplined regulatory uniformity across the deliverable | Datasheet has "Responsible Party: TBD" which leaves ownership undefined; this is a uniformity gap in regulatory discipline | Datasheet.md | Identification table | — | Datasheet.md | TBD |
| E-003 | E:evaluative:completeness | RationaleGap | Multi | Specification | Add a traceability matrix from REQ-01 through REQ-09 back to SOW items and OBJ-002: while Source tags exist per-requirement, no consolidated traceability table demonstrates comprehensive merit command | Individual requirements cite sources but no single view confirms that all SOW-004, SOW-005, SOW-006 obligations and OBJ-002 objectives are fully addressed by the requirement set | Specification.md | Requirements section | — | Specification.md | TBD |
