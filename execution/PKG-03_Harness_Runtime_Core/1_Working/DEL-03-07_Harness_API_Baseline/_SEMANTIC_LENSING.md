# Semantic Lensing Register: DEL-03-07 Harness API Baseline in Frontend Runtime

**Generated:** 2026-02-22
**Deliverable Folder:** execution/PKG-03_Harness_Runtime_Core/1_Working/DEL-03-07_Harness_API_Baseline/
**Warnings:** None

**Inputs Read:**
- _CONTEXT.md — `execution/PKG-03_Harness_Runtime_Core/1_Working/DEL-03-07_Harness_API_Baseline/_CONTEXT.md`
- _STATUS.md — `execution/PKG-03_Harness_Runtime_Core/1_Working/DEL-03-07_Harness_API_Baseline/_STATUS.md`
- _SEMANTIC.md — `execution/PKG-03_Harness_Runtime_Core/1_Working/DEL-03-07_Harness_API_Baseline/_SEMANTIC.md`
- Datasheet.md — `execution/PKG-03_Harness_Runtime_Core/1_Working/DEL-03-07_Harness_API_Baseline/Datasheet.md`
- Specification.md — `execution/PKG-03_Harness_Runtime_Core/1_Working/DEL-03-07_Harness_API_Baseline/Specification.md`
- Guidance.md — `execution/PKG-03_Harness_Runtime_Core/1_Working/DEL-03-07_Harness_API_Baseline/Guidance.md`
- Procedure.md — `execution/PKG-03_Harness_Runtime_Core/1_Working/DEL-03-07_Harness_API_Baseline/Procedure.md`
- _REFERENCES.md — `execution/PKG-03_Harness_Runtime_Core/1_Working/DEL-03-07_Harness_API_Baseline/_REFERENCES.md`

**Purpose:** Apply CHIRALITY_FRAMEWORK matrix cells as lenses over the production documents, capturing warranted enrichment inputs for a later enrichment pass.

---

## Summary

- Total warranted items: 28
- By document (AppliesToDoc):
  - Datasheet: 3
  - Specification: 15
  - Guidance: 4
  - Procedure: 4
  - Multi: 2
- By matrix:
  - A: 6  B: 4  C: 4  F: 3  D: 3  X: 5  E: 3
- By type:
  - Conflict: 2
  - VerificationGap: 5
  - MissingSlot: 8
  - WeakStatement: 4
  - RationaleGap: 3
  - Normalization: 3
  - TBD_Question: 3
  - MatrixError: 0
- Notable conflicts: 2
- Matrix parse errors: 0

---

## Matrix A -- Orientation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| A:normative:guiding | normative | guiding | prescriptive direction | 1 | HAS_ITEMS | Error type taxonomy TBD weakens prescriptive direction |
| A:normative:applying | normative | applying | mandatory practice | 1 | HAS_ITEMS | Session create request body conflict |
| A:normative:judging | normative | judging | compliance determination | 1 | HAS_ITEMS | REQ-08 status codes contain multiple TBDs |
| A:normative:reviewing | normative | reviewing | regulatory audit | 1 | HAS_ITEMS | Validation script compatibility verification gap |
| A:operative:guiding | operative | guiding | procedural direction | 0 | NO_ITEMS | Procedure steps are clear and sequenced |
| A:operative:applying | operative | applying | practical execution | 1 | HAS_ITEMS | Stub depth decision unresolved |
| A:operative:judging | operative | judging | performance assessment | 0 | NO_ITEMS | Verification tables present in Specification and Procedure |
| A:operative:reviewing | operative | reviewing | process audit | 0 | NO_ITEMS | CI and validation script integration documented |
| A:evaluative:guiding | evaluative | guiding | value orientation | 1 | HAS_ITEMS | Missing rationale for interrupt route inclusion |
| A:evaluative:applying | evaluative | applying | merit application | 0 | NO_ITEMS | Scope coverage to objectives mapping is clear |
| A:evaluative:judging | evaluative | judging | worth determination | 0 | NO_ITEMS | Acceptance criteria in Procedure align with SOW-045 |
| A:evaluative:reviewing | evaluative | reviewing | quality appraisal | 0 | NO_ITEMS | Quality checks documented in Procedure Step 8 |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A-001 | A:normative:guiding | TBD_Question | Specification | Specification | Resolve TBD error type taxonomy format: string enum vs. string constants. REQ-08 cannot be fully prescriptive until format is decided. | The normative prescriptive direction for typed failure contracts is incomplete because the error type format remains TBD. Implementation cannot proceed to production quality without this decision. | Specification.md; Guidance.md | Specification REQ-08; Guidance T2 | | Guidance.md T2 (PROPOSAL) | TBD |
| A-002 | A:normative:applying | Conflict | Specification | Specification | Session create request body: clarify whether `persona` and `mode` are required at create time or only at boot time. DEL-03-01 REQ-03 says `projectRoot` minimum; DEL-03-01 Guidance C3 example includes additional fields. | Mandatory practice for session create route cannot be unambiguously applied because the required request body fields are contested between sources. | Specification.md; Guidance.md | Specification REQ-01; Guidance CONFLICT-001 | Specification.md#REQ-01, Guidance.md#CONFLICT-001 | DEL-03-01 Specification REQ-03 (PROPOSAL) | TBD |
| A-003 | A:normative:judging | WeakStatement | Specification | Specification | REQ-08 error categories list multiple "TBD (likely ...)" status codes. Compliance determination requires concrete status codes, not "likely" values. Clarify: session-not-found (404?), persona-not-found (?), SDK failure (500/502?), working-root-inaccessible (?). | Compliance determination against REQ-08 is impossible when the expected status codes are expressed as guesses rather than requirements. | Specification.md | REQ-08 (Error Category table) | | Human decision required (PROPOSAL) | TBD |
| A-004 | A:normative:reviewing | VerificationGap | Specification | Specification | Add verification approach for REQ-15 (Platform Constraint) that is more specific than "Manual or CI test." Specify what constitutes a passing platform validation -- compilation only, or full test suite execution on Apple Silicon? | Regulatory audit of REQ-15 has no testable acceptance criterion. "Manual or CI test: build and run on macOS 15+ Apple Silicon" is too vague for consistent review. | Specification.md | Verification table, REQ-15 row | | Specification.md (PROPOSAL) | TBD |
| A-005 | A:operative:applying | TBD_Question | Guidance | Guidance | Resolve T1 (Stub Depth vs. Baseline Fidelity): confirm Option B (module-interface stubs) or Option A (thin stubs). This decision affects Procedure Steps 2 and 5-6. | Practical execution of the baseline cannot start without knowing the stub strategy. Procedure references module interfaces but does not confirm the decision. | Guidance.md; Procedure.md | Guidance T1; Procedure Steps 2, 5, 6 | | Human decision required (PROPOSAL) | TBD |
| A-006 | A:evaluative:guiding | RationaleGap | Specification | Guidance | Add rationale for REQ-12 (Interrupt Route) inclusion in the baseline scope. SOW-045 does not explicitly mention interrupt. The route is sourced from the validation matrix, but no Guidance section explains why it belongs in the baseline API surface rather than a separate deliverable. | Value orientation for the interrupt route is unclear -- it was added based on validation script expectations but the decision rationale is missing from Guidance. | Specification.md; Guidance.md | Specification REQ-12; Guidance (entire document scanned -- no interrupt rationale found) | | Guidance.md (PROPOSAL) | TBD |

---

## Matrix B -- Conceptualization (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| B:data:necessity | data | necessity | essential fact | 1 | HAS_ITEMS | Session storage location TBD |
| B:data:sufficiency | data | sufficiency | adequate evidence | 0 | NO_ITEMS | Datasheet attributes well-sourced |
| B:data:completeness | data | completeness | comprehensive record | 1 | HAS_ITEMS | Missing interrupt endpoint from Datasheet |
| B:data:consistency | data | consistency | reliable measurement | 0 | NO_ITEMS | Source references consistent across Datasheet |
| B:information:necessity | information | necessity | essential signal | 1 | HAS_ITEMS | Boot response shape incomplete |
| B:information:sufficiency | information | sufficiency | adequate context | 0 | NO_ITEMS | Guidance provides sufficient context for implementation decisions |
| B:information:completeness | information | completeness | comprehensive account | 0 | NO_ITEMS | Document set covers scope end-to-end |
| B:information:consistency | information | consistency | coherent message | 1 | HAS_ITEMS | Inconsistent endpoint naming across documents |
| B:knowledge:necessity | knowledge | necessity | fundamental understanding | 0 | NO_ITEMS | Module delegation model is clear |
| B:knowledge:sufficiency | knowledge | sufficiency | competent expertise | 0 | NO_ITEMS | Procedure steps provide sufficient implementation guidance |
| B:knowledge:completeness | knowledge | completeness | thorough mastery | 0 | NO_ITEMS | Cross-deliverable boundaries well-documented in Guidance |
| B:knowledge:consistency | knowledge | consistency | coherent understanding | 0 | NO_ITEMS | Module responsibility partitioning is consistent |
| B:wisdom:necessity | wisdom | necessity | essential discernment | 0 | NO_ITEMS | Trade-offs documented in Guidance T1/T2 |
| B:wisdom:sufficiency | wisdom | sufficiency | adequate judgment | 0 | NO_ITEMS | Conflict table captures known decision points |
| B:wisdom:completeness | wisdom | completeness | holistic insight | 0 | NO_ITEMS | Relationship considerations C1-C6 comprehensive |
| B:wisdom:consistency | wisdom | consistency | principled reasoning | 0 | NO_ITEMS | Reasoning consistent with SCA-001 gating model |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| B-001 | B:data:necessity | TBD_Question | Datasheet | Datasheet | Resolve session storage location: Working Root subdirectory vs. app data directory. SessionManager needs a concrete path to implement persistence (REQ-13). This blocks essential fact establishment for the session record filesystem location. | The essential fact of where session records are stored is missing. Route handlers delegate to SessionManager but SessionManager's storage path is unresolved, making the data foundation incomplete. | Datasheet.md; Guidance.md | Datasheet Conditions (Filesystem-as-state); Guidance CONFLICT-002 | Datasheet.md#Conditions, Guidance.md#CONFLICT-002 | Human ruling required; see DEL-03-01 CONFLICT-001/002 (PROPOSAL) | TBD |
| B-002 | B:data:completeness | MissingSlot | Datasheet | Datasheet | Add interrupt endpoint to Session Endpoints table or create a separate Interrupt Endpoint table. Specification REQ-12 defines this route but Datasheet does not enumerate it alongside the other endpoints. | The Datasheet provides a comprehensive record of session and turn endpoints but omits the interrupt endpoint, creating an incomplete route surface inventory. | Datasheet.md; Specification.md | Datasheet Session Endpoints table; Specification REQ-12 | | Datasheet.md (PROPOSAL) | TBD |
| B-003 | B:information:necessity | MissingSlot | Specification | Specification | Add explicit boot response shape definition to REQ-02. Current text says `200 { session, boot }` but does not define what `boot` contains (only Procedure Step 4.2 lists `claudeSessionId`, `bootFingerprint`, `bootedAt`). The essential signal for boot success response structure should be in the normative document. | The essential signal for what a successful boot response contains is scattered across documents. Specification REQ-02 names the shape but does not define the `boot` object fields, leaving implementers to infer from Procedure. | Specification.md; Procedure.md | Specification REQ-02; Procedure Step 4.2 | | Specification.md (PROPOSAL) | TBD |
| B-004 | B:information:consistency | Normalization | Multi | Guidance | Normalize endpoint path notation: Datasheet uses `/api/harness/session/:id` (Express-style param), Specification uses `/api/harness/session/:id`, but Guidance C6 uses `[id]` (Next.js file-based routing). While both refer to the same endpoint, the mixed notation may confuse readers. Add a vocabulary note in Guidance clarifying the convention. | Coherent messaging requires consistent notation for parameterized route segments. The mix of `:id` and `[id]` conventions across documents could create drift as more contributors join. | Datasheet.md; Specification.md; Guidance.md | Datasheet Session Endpoints; Specification REQ-04/REQ-05; Guidance C6 | | Guidance.md (PROPOSAL) | TBD |

---

## Matrix C -- Formulation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| C:normative:necessity | normative | necessity | obligatory conformance basis | 1 | HAS_ITEMS | REQ-05 delete success response underspecified |
| C:normative:sufficiency | normative | sufficiency | defensible compliance rigor | 1 | HAS_ITEMS | REQ-03 list missing failure cases |
| C:normative:completeness | normative | completeness | total regulatory assurance | 0 | NO_ITEMS | Requirements REQ-01 through REQ-15 cover full route surface |
| C:normative:consistency | normative | consistency | harmonized regulatory discipline | 1 | HAS_ITEMS | REQ-07 event list includes tool:result but verification omits it |
| C:operative:necessity | operative | necessity | critical operational prerequisite | 0 | NO_ITEMS | Prerequisites table in Procedure is complete |
| C:operative:sufficiency | operative | sufficiency | demonstrated operational fitness | 0 | NO_ITEMS | Steps 1-8 provide adequate operational path |
| C:operative:completeness | operative | completeness | end-to-end workflow coverage | 1 | HAS_ITEMS | Missing rollback/cleanup guidance |
| C:operative:consistency | operative | consistency | disciplined operational coherence | 0 | NO_ITEMS | Procedure steps reference correct Specification REQs |
| C:evaluative:necessity | evaluative | necessity | intrinsic value criterion | 0 | NO_ITEMS | Scope aligned to OBJ-002 and OBJ-008 |
| C:evaluative:sufficiency | evaluative | sufficiency | evidenced merit standing | 0 | NO_ITEMS | Verification matrix maps to acceptance criteria |
| C:evaluative:completeness | evaluative | completeness | holistic quality portrait | 0 | NO_ITEMS | Quality dimensions covered: compilation, tests, validation scripts, CI |
| C:evaluative:consistency | evaluative | consistency | principled valuation coherence | 0 | NO_ITEMS | Evaluation criteria consistent across Specification and Procedure |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| C-001 | C:normative:necessity | WeakStatement | Specification | Specification | REQ-05 says "delete the session record and return a success response" but does not specify the response status code or body shape. Other CRUD routes (REQ-01, REQ-04) specify `200` + response shape. Clarify: what status code and body does delete return? | The obligatory conformance basis for session delete is weaker than for sibling routes. "Success response" is ambiguous -- could be `200 {}`, `200 { ok: true }`, or `204 No Content`. | Specification.md | REQ-05 | | Specification.md (PROPOSAL) | TBD |
| C-002 | C:normative:sufficiency | VerificationGap | Specification | Specification | REQ-03 (Session List) has no specified failure cases in the Verification table. The test is only "GET list with `projectRoot`, verify `200` with session array." Add verification for: missing `projectRoot` query param, invalid `projectRoot` (nonexistent path). | Defensible compliance rigor requires that the list route has failure-case testing, consistent with other CRUD routes that test both success and error paths. | Specification.md | REQ-03; Verification table REQ-03 row | | Specification.md (PROPOSAL) | TBD |
| C-003 | C:normative:consistency | Conflict | Specification | Specification | REQ-07 lists `tool:result` as an SSE event type, but the Verification table for REQ-07 only verifies `session:init, chat:delta, chat:complete, session:complete, process:exit`. The `tool:result` event is not mentioned in the verification ordering. Either remove `tool:result` from REQ-07 or add it to verification. | Harmonized regulatory discipline requires that every specified event type has a verification path. The omission of `tool:result` from verification creates an internal inconsistency within Specification. | Specification.md | REQ-07; Verification table REQ-07 row | Specification.md#REQ-07, Specification.md#Verification-REQ-07 | Specification.md (PROPOSAL) | TBD |
| C-004 | C:operative:completeness | MissingSlot | Procedure | Procedure | Add rollback/cleanup step or note: if Step 7 (route-contract tests) fails, what should the implementer do? Other procedures typically include guidance on handling intermediate failures. At minimum, note that failed compilation in Step 8 requires returning to the failing step. | End-to-end workflow coverage should address the failure path, not just the happy path. The Procedure is silent on what happens when intermediate steps fail. | Procedure.md | Steps section (entire section scanned -- no failure recovery guidance found) | | Procedure.md (PROPOSAL) | TBD |

---

## Matrix F -- Requirements (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| F:normative:necessity | normative | necessity | mandated compliance foundation | 1 | HAS_ITEMS | REQ-11 local-only verification is audit-only |
| F:normative:sufficiency | normative | sufficiency | validated regulatory sufficiency | 0 | NO_ITEMS | Requirements are traceable to source documents |
| F:normative:completeness | normative | completeness | exhaustive governance mastery | 0 | NO_ITEMS | REQ-01 through REQ-15 cover all route surface areas |
| F:normative:consistency | normative | consistency | principled compliance uniformity | 1 | HAS_ITEMS | Inconsistent requirement granularity |
| F:operative:necessity | operative | necessity | foundational execution readiness | 0 | NO_ITEMS | Prerequisites clearly stated |
| F:operative:sufficiency | operative | sufficiency | proven operational capability | 0 | NO_ITEMS | Procedure steps align with requirements |
| F:operative:completeness | operative | completeness | total process readiness | 0 | NO_ITEMS | Steps cover full implementation lifecycle |
| F:operative:consistency | operative | consistency | disciplined process reliability | 0 | NO_ITEMS | Procedure verification checks reference correct REQs |
| F:evaluative:necessity | evaluative | necessity | foundational merit evidence | 0 | NO_ITEMS | OBJ-002 and OBJ-008 traceability present |
| F:evaluative:sufficiency | evaluative | sufficiency | sufficient valuation standing | 0 | NO_ITEMS | Acceptance criteria adequate for scope |
| F:evaluative:completeness | evaluative | completeness | exhaustive merit accounting | 1 | HAS_ITEMS | Missing non-functional acceptance criteria |
| F:evaluative:consistency | evaluative | consistency | unified worth discipline | 0 | NO_ITEMS | Evaluation criteria consistent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| F-001 | F:normative:necessity | VerificationGap | Specification | Specification | REQ-11 (Local-Only Implementation) verification is "Audit: verify all route source files reside under `frontend/`." This is not automatable and has no test. Add a CI-verifiable check (e.g., a lint rule or build script that fails if imports reference non-local paths). | The mandated compliance foundation for local-only execution lacks an automated verification mechanism. An audit-only check risks being skipped or inconsistently applied. | Specification.md | REQ-11; Verification table REQ-11 row | | Specification.md (PROPOSAL) | TBD |
| F-002 | F:normative:consistency | WeakStatement | Specification | Specification | Requirement granularity is inconsistent: REQ-01 through REQ-07 specify individual route behaviors in detail, but REQ-08 (Typed Failure Contracts) aggregates all error handling into one requirement with a partially-TBD table. Consider splitting REQ-08 into per-route error contracts or adding sub-requirements (REQ-08a, REQ-08b, etc.) for testability. | Principled compliance uniformity suggests that requirements should be at a consistent granularity. REQ-08 covers 6 error categories across all routes in a single requirement, making verification tracking coarser than sibling requirements. | Specification.md | REQ-08 | | Specification.md (PROPOSAL) | TBD |
| F-003 | F:evaluative:completeness | MissingSlot | Specification | Specification | No non-functional acceptance criteria exist for the baseline. Consider adding: maximum acceptable response time for session CRUD operations, maximum time-to-first-SSE-event for turn route, or at minimum a note that non-functional criteria are deferred to a later deliverable. | Exhaustive merit accounting for a BACKEND_FEATURE_SLICE should at minimum acknowledge whether non-functional requirements (latency, throughput) are in scope or explicitly deferred. The current silence leaves this ambiguous. | Specification.md; Procedure.md | Specification (entire document scanned -- no non-functional requirements found); Procedure Acceptance Criteria table | | Specification.md (PROPOSAL) | TBD |

---

## Matrix D -- Objectives (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| D:normative:guiding | normative | guiding | resolved prescriptive authority | 0 | NO_ITEMS | Specification requirements are authoritative and well-sourced |
| D:normative:applying | normative | applying | validated compulsory practice | 1 | HAS_ITEMS | Interrupt route missing from Procedure test matrix |
| D:normative:judging | normative | judging | conclusive conformance ruling | 0 | NO_ITEMS | Verification table provides clear conformance criteria |
| D:normative:reviewing | normative | reviewing | systematic compliance inspection | 0 | NO_ITEMS | CI validation references adequate |
| D:operative:guiding | operative | guiding | grounded procedural pathway | 0 | NO_ITEMS | Procedure steps are grounded in concrete actions |
| D:operative:applying | operative | applying | validated execution delivery | 0 | NO_ITEMS | Steps 1-8 form a complete execution pathway |
| D:operative:judging | operative | judging | resolved capability determination | 1 | HAS_ITEMS | SDK native stream check lacks route-level verification |
| D:operative:reviewing | operative | reviewing | confirmed workflow stability | 0 | NO_ITEMS | Persistence and restart verification present |
| D:evaluative:guiding | evaluative | guiding | grounded value direction | 0 | NO_ITEMS | Guidance Principles P1-P4 well-grounded |
| D:evaluative:applying | evaluative | applying | validated merit expression | 0 | NO_ITEMS | SOW-045 acceptance criteria clearly mapped |
| D:evaluative:judging | evaluative | judging | definitive worth ruling | 1 | HAS_ITEMS | Missing explicit done-criteria for baseline |
| D:evaluative:reviewing | evaluative | reviewing | confirmed quality assessment | 0 | NO_ITEMS | Quality assessment via test suite and validation scripts |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| D-001 | D:normative:applying | MissingSlot | Procedure | Procedure | Add interrupt route to the test coverage matrix in Step 7.2. Currently the matrix lists session CRUD, boot, and turn but omits interrupt. Step 6 defines interrupt implementation but Step 7 does not include it in test scope. | Validated compulsory practice requires that every implemented route has corresponding test coverage. The interrupt route (REQ-12) is implemented in Step 6 but absent from the Step 7 test matrix. | Procedure.md | Step 7.2 (test coverage matrix) | | Procedure.md (PROPOSAL) | TBD |
| D-002 | D:operative:judging | VerificationGap | Procedure | Specification | The Validation Script Compatibility table includes `section8.sdk_native_stream` with expected result "No `parse:error` logs." However, no Specification requirement corresponds to this check and no Procedure step produces this validation. Add either a requirement or a Procedure step addressing SDK native stream validation. | Resolved capability determination cannot be completed for SDK native stream behavior because it exists only in the validation compatibility table with no corresponding requirement or execution step. | Procedure.md; Specification.md | Procedure Validation Script Compatibility table (section8.sdk_native_stream row); Specification (entire document scanned -- no sdk_native_stream requirement found) | | Specification.md (PROPOSAL) | TBD |
| D-003 | D:evaluative:judging | RationaleGap | Guidance | Guidance | Add a "Definition of Done" or "Baseline Completeness Criteria" section clarifying what it means for DEL-03-07 to be ISSUED vs. merely IN_PROGRESS. Guidance P4 says "baseline means compilable and testable" but the gate condition is IN_PROGRESS. What distinguishes IN_PROGRESS from ISSUED for this deliverable? | Definitive worth ruling requires clarity on when the deliverable is considered complete. The current documents define what baseline means (P4) and what the gate requires (IN_PROGRESS) but not what separates adequate baseline from finished deliverable. | Guidance.md; Procedure.md | Guidance P4; Procedure Execution Gate Verification table | | Guidance.md (PROPOSAL) | TBD |

---

## Matrix X -- Verification (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| X:guiding:necessity | guiding | necessity | authoritative baseline imperative | 1 | HAS_ITEMS | Anthropic SDK documentation location TBD |
| X:guiding:sufficiency | guiding | sufficiency | substantiated directive fitness | 0 | NO_ITEMS | Directives well-substantiated by source references |
| X:guiding:completeness | guiding | completeness | comprehensive directive scope | 0 | NO_ITEMS | Directive scope covers all route categories |
| X:guiding:consistency | guiding | consistency | coherent directive governance | 0 | NO_ITEMS | Governance references consistent across documents |
| X:applying:necessity | applying | necessity | essential implementation verification | 1 | HAS_ITEMS | SSE helper utility not specified |
| X:applying:sufficiency | applying | sufficiency | sufficient practice justification | 0 | NO_ITEMS | Justification for each route present via source references |
| X:applying:completeness | applying | completeness | exhaustive implementation coverage | 1 | HAS_ITEMS | Options mapping verification incomplete |
| X:applying:consistency | applying | consistency | uniform implementation discipline | 1 | HAS_ITEMS | Route handler error handling pattern not standardized |
| X:judging:necessity | judging | necessity | essential adjudication foundation | 0 | NO_ITEMS | Verification approaches defined for all REQs |
| X:judging:sufficiency | judging | sufficiency | defensible adjudicative proof | 0 | NO_ITEMS | Test coverage matrix provides defensible proof basis |
| X:judging:completeness | judging | completeness | comprehensive adjudicative closure | 1 | HAS_ITEMS | Session list failure cases unverified |
| X:judging:consistency | judging | consistency | principled adjudicative consistency | 0 | NO_ITEMS | Verification methods consistent across requirements |
| X:reviewing:necessity | reviewing | necessity | essential examination baseline | 0 | NO_ITEMS | CI pipeline reference provides examination baseline |
| X:reviewing:sufficiency | reviewing | sufficiency | sufficient examination evidence | 0 | NO_ITEMS | Evidence trail table in Procedure is adequate |
| X:reviewing:completeness | reviewing | completeness | exhaustive examination coverage | 0 | NO_ITEMS | Validation script compatibility table covers all checks |
| X:reviewing:consistency | reviewing | consistency | principled examination uniformity | 0 | NO_ITEMS | Examination approach uniform across route categories |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| X-001 | X:guiding:necessity | MissingSlot | Specification | Specification | The Standards table lists "Anthropic Agent SDK" with `location TBD -- SDK documentation external`. Add a concrete reference (URL or local documentation pointer) for the SDK `query()` interface that AgentSdkManager depends on. Without this, the authoritative baseline for SDK integration is ungrounded. | The authoritative baseline imperative for SDK integration cannot be verified when the SDK documentation location is unknown. This is an external dependency that should have at least a pointer. | Specification.md | Standards table (Anthropic Agent SDK row) | | Specification.md (PROPOSAL) | TBD |
| X-002 | X:applying:necessity | MissingSlot | Datasheet | Datasheet | Add an SSE helper/utility to the Construction table. Route handlers for turn execution (REQ-06, REQ-07) need to emit SSE events, which requires either a framework utility or a custom SSE writer. This implementation component is not listed in the Construction section. | Essential implementation verification requires that all implementation components are enumerated. The SSE event streaming mechanism is a necessary implementation element not captured in the Datasheet construction inventory. | Datasheet.md | Construction table | | Datasheet.md (PROPOSAL) | TBD |
| X-003 | X:applying:completeness | VerificationGap | Specification | Specification | REQ-14 (Options Mapping) verification says "Unit test: verify each fallback chain with/without `opts` values." However, the Procedure Step 7.2 test coverage matrix does not include options mapping tests. Add options mapping to the test matrix or create a note linking REQ-14 verification to a specific test location. | Exhaustive implementation coverage requires that the options mapping fallback chain verification is traceable to a concrete test location, not just a general description. | Specification.md; Procedure.md | Specification Verification table REQ-14 row; Procedure Step 7.2 | | Procedure.md (PROPOSAL) | TBD |
| X-004 | X:applying:consistency | Normalization | Guidance | Guidance | Standardize the error handling pattern across route handlers. Guidance P2 establishes typed failures as first-class but does not recommend a shared error handling utility or middleware pattern. Add a recommendation for a shared `handleHarnessError()` utility or Next.js middleware approach to ensure uniform error response formatting across all routes. | Uniform implementation discipline requires a consistent mechanism for producing typed error responses. Without a recommended pattern, each route handler may implement error formatting differently, risking drift. | Guidance.md; Procedure.md | Guidance P2; Procedure Steps 3-6 | | Guidance.md (PROPOSAL) | TBD |
| X-005 | X:judging:completeness | Normalization | Specification | Specification | The Verification table for REQ-03 only tests the success path. Other CRUD routes (REQ-01, REQ-04, REQ-05) include failure case verification. Add failure case verification for REQ-03 (e.g., missing `projectRoot` query param). This is related to C-002 but addresses the normalization angle: verification rigor should be uniform across CRUD routes. | Comprehensive adjudicative closure requires that all CRUD routes have symmetric verification coverage. REQ-03 is the only CRUD route without failure-case testing in the verification table. | Specification.md | Verification table REQ-03 row | | Specification.md (PROPOSAL) | TBD |

---

## Matrix E -- Evaluation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| E:normative:necessity | normative | necessity | absolute regulatory mandate | 0 | NO_ITEMS | Core mandates (REQ-01 through REQ-15) are comprehensive |
| E:normative:sufficiency | normative | sufficiency | justified regulatory adequacy | 1 | HAS_ITEMS | ASSUMPTION tags lack resolution pathway |
| E:normative:completeness | normative | completeness | total regulatory closure | 0 | NO_ITEMS | Regulatory coverage is complete across all route surfaces |
| E:normative:consistency | normative | consistency | unified regulatory coherence | 0 | NO_ITEMS | Requirements cross-reference consistently |
| E:operative:necessity | operative | necessity | critical operational foundation | 0 | NO_ITEMS | Operational prerequisites adequate |
| E:operative:sufficiency | operative | sufficiency | sufficient operational justification | 0 | NO_ITEMS | Steps justified by requirements references |
| E:operative:completeness | operative | completeness | exhaustive operational assurance | 1 | HAS_ITEMS | No Step 8.3/8.4 prerequisite check |
| E:operative:consistency | operative | consistency | dependable operational alignment | 0 | NO_ITEMS | Procedure aligns with Specification consistently |
| E:evaluative:necessity | evaluative | necessity | fundamental value foundation | 0 | NO_ITEMS | Value foundation grounded in OBJ-002, OBJ-008 |
| E:evaluative:sufficiency | evaluative | sufficiency | sound value justification | 0 | NO_ITEMS | Justification adequate for baseline scope |
| E:evaluative:completeness | evaluative | completeness | definitive value realization | 1 | HAS_ITEMS | Missing cross-deliverable integration test plan |
| E:evaluative:consistency | evaluative | consistency | principled value alignment | 0 | NO_ITEMS | Value alignment consistent with SCA-001 phasing |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| E-001 | E:normative:sufficiency | RationaleGap | Multi | Guidance | Multiple ASSUMPTION tags across documents (Datasheet: error response structure, validation errors; Specification: REQ-08 error taxonomy; Guidance: P4 stub strategy, C3 module interfaces, C6 file layout) lack a defined resolution pathway. Add a Guidance section listing all assumptions with their resolution triggers (e.g., "resolved at implementation time" vs. "requires human ruling before implementation"). | Justified regulatory adequacy requires that assumptions are tracked with resolution triggers, not left as permanent open items. The current assumption tags provide transparency but no lifecycle management. | Datasheet.md; Specification.md; Guidance.md | Datasheet Typed Failure Contract table (ASSUMPTION rows); Specification REQ-08 (ASSUMPTION); Guidance P4, C3, C6 (ASSUMPTION tags) | | Guidance.md (PROPOSAL) | TBD |
| E-002 | E:operative:completeness | WeakStatement | Procedure | Procedure | Step 8.3 says "(When server is available) Run validation scripts against the local server" but does not define how to determine whether the server is available, or what to do if it is not. This conditional weakens the exhaustive operational assurance claim. Clarify: is Step 8.3 optional or required? If optional, under what conditions can it be skipped? | Exhaustive operational assurance requires that every verification step has a clear execution condition. The "(When server is available)" qualifier makes the validation script step ambiguous. | Procedure.md | Step 8.3 | | Procedure.md (PROPOSAL) | TBD |
| E-003 | E:evaluative:completeness | MissingSlot | Guidance | Guidance | Add a section on cross-deliverable integration expectations: when DEL-03-01 through DEL-03-06 complete, how should the stubs in DEL-03-07 be replaced? What integration test strategy validates that real module implementations satisfy the same route contracts? This is essential for definitive value realization of the baseline. | Definitive value realization of the baseline requires a forward-looking integration plan. The baseline's value is only fully realized when stubs are replaced with real implementations, but no document describes this transition path. | Guidance.md | Guidance C1-C5 (relationship considerations mention boundaries but not integration transition); entire document scanned | | Guidance.md (PROPOSAL) | TBD |
