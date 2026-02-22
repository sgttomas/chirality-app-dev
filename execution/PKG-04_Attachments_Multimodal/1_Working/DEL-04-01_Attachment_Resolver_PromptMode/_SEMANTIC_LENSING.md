# Semantic Lensing Register: DEL-04-01 Server-side Attachment Resolver + Prompt Mode Selection

**Generated:** 2026-02-21
**Deliverable Folder:** execution/PKG-04_Attachments_Multimodal/1_Working/DEL-04-01_Attachment_Resolver_PromptMode/
**Warnings:** None

**Inputs Read:**
- _CONTEXT.md — `execution/PKG-04_Attachments_Multimodal/1_Working/DEL-04-01_Attachment_Resolver_PromptMode/_CONTEXT.md`
- _STATUS.md — `execution/PKG-04_Attachments_Multimodal/1_Working/DEL-04-01_Attachment_Resolver_PromptMode/_STATUS.md`
- _SEMANTIC.md — `execution/PKG-04_Attachments_Multimodal/1_Working/DEL-04-01_Attachment_Resolver_PromptMode/_SEMANTIC.md`
- Datasheet.md — `execution/PKG-04_Attachments_Multimodal/1_Working/DEL-04-01_Attachment_Resolver_PromptMode/Datasheet.md`
- Specification.md — `execution/PKG-04_Attachments_Multimodal/1_Working/DEL-04-01_Attachment_Resolver_PromptMode/Specification.md`
- Guidance.md — `execution/PKG-04_Attachments_Multimodal/1_Working/DEL-04-01_Attachment_Resolver_PromptMode/Guidance.md`
- Procedure.md — `execution/PKG-04_Attachments_Multimodal/1_Working/DEL-04-01_Attachment_Resolver_PromptMode/Procedure.md`
- _REFERENCES.md — `execution/PKG-04_Attachments_Multimodal/1_Working/DEL-04-01_Attachment_Resolver_PromptMode/_REFERENCES.md`

**Purpose:** Apply CHIRALITY_FRAMEWORK matrix cells as lenses over the production documents, capturing warranted enrichment inputs for a later enrichment pass.

---

## Summary

- Total warranted items: 18
- By document:
  - Datasheet: 3
  - Specification: 6
  - Guidance: 3
  - Procedure: 3
  - Multi: 3
- By matrix:
  - A: 3  B: 2  C: 2  F: 3  D: 2  X: 4  E: 2
- By type:
  - Conflict: 0
  - VerificationGap: 4
  - MissingSlot: 5
  - WeakStatement: 3
  - RationaleGap: 2
  - Normalization: 2
  - TBD_Question: 2
  - MatrixError: 0
- Notable conflicts: 0
- Matrix parse errors: 0

---

## Matrix A — Orientation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| A:normative:guiding | normative | guiding | prescriptive direction | 1 | HAS_ITEMS | Budget accounting strategy is under-prescribed |
| A:normative:applying | normative | applying | mandatory practice | 0 | NO_ITEMS | Requirements are well-specified with SHALL language |
| A:normative:judging | normative | judging | compliance determination | 1 | HAS_ITEMS | SDK content block format compliance undetermined |
| A:normative:reviewing | normative | reviewing | regulatory audit | 0 | NO_ITEMS | Verification matrix covers all requirements |
| A:operative:guiding | operative | guiding | procedural direction | 0 | NO_ITEMS | Procedure steps are clear and sequenced |
| A:operative:applying | operative | applying | practical execution | 1 | HAS_ITEMS | Missing boundary condition for budget enforcement |
| A:operative:judging | operative | judging | performance assessment | 0 | NO_ITEMS | Verification checks are enumerated |
| A:operative:reviewing | operative | reviewing | process audit | 0 | NO_ITEMS | Records table covers audit trail |
| A:evaluative:guiding | evaluative | guiding | value orientation | 0 | NO_ITEMS | Principles section in Guidance covers value orientation |
| A:evaluative:applying | evaluative | applying | merit application | 0 | NO_ITEMS | Trade-offs table justifies design choices |
| A:evaluative:judging | evaluative | judging | worth determination | 0 | NO_ITEMS | Quality criteria are implicit in requirements |
| A:evaluative:reviewing | evaluative | reviewing | quality appraisal | 0 | NO_ITEMS | Verification matrix addresses quality gates |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A-001 | A:normative:guiding | WeakStatement | Guidance | Specification | Clarify whether total budget enforcement uses reject-entire-batch or accept-until-exhausted strategy; add normative requirement to Specification | Guidance C2 identifies two budget strategies but defers the choice as ASSUMPTION; no normative requirement resolves this ambiguity, leaving implementation underdetermined | Guidance.md | Considerations > C2: Budget Accounting Strategy | — | docs/SPEC.md Section 9.8 | TBD |
| A-002 | A:normative:judging | TBD_Question | Specification | Specification | Confirm exact SDK content block format (type/source fields, base64 encoding conventions) and add acceptance criteria for REQ-12-V referencing that format | REQ-12 requires "SDK-compatible content blocks" but neither Specification nor Datasheet defines what SDK-compatible means concretely; Procedure Step 3.2 also flags this as ASSUMPTION | Specification.md | Verification > REQ-12-V | — | Anthropic Agent SDK documentation | TBD |
| A-003 | A:operative:applying | MissingSlot | Specification | Specification | Add requirement specifying budget enforcement behavior at the 18 MB boundary (exact equality: accept or reject?) and whether budget is checked per-file-sequentially or on aggregate | REQ-06 states the budget but not the enforcement algorithm; boundary behavior at exactly 18 MB and the accounting order are unspecified | Specification.md | Requirements > REQ-06 | — | docs/SPEC.md Section 9.8 | TBD |

---

## Matrix B — Conceptualization (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| B:data:necessity | data | necessity | essential fact | 1 | HAS_ITEMS | Missing responsible party |
| B:data:sufficiency | data | sufficiency | adequate evidence | 0 | NO_ITEMS | Sources are cited throughout |
| B:data:completeness | data | completeness | comprehensive record | 1 | HAS_ITEMS | Missing content block format specification |
| B:data:consistency | data | consistency | reliable measurement | 0 | NO_ITEMS | Size limits consistent across documents |
| B:information:necessity | information | necessity | essential signal | 0 | NO_ITEMS | SOW/OBJ traceability established |
| B:information:sufficiency | information | sufficiency | adequate context | 0 | NO_ITEMS | Context sufficient across documents |
| B:information:completeness | information | completeness | comprehensive account | 0 | NO_ITEMS | Document set covers scope adequately |
| B:information:consistency | information | consistency | coherent message | 0 | NO_ITEMS | Messages are coherent across documents |
| B:knowledge:necessity | knowledge | necessity | fundamental understanding | 0 | NO_ITEMS | Domain knowledge is well-established |
| B:knowledge:sufficiency | knowledge | sufficiency | competent expertise | 0 | NO_ITEMS | Technical detail is sufficient |
| B:knowledge:completeness | knowledge | completeness | thorough mastery | 0 | NO_ITEMS | Coverage is thorough for stated scope |
| B:knowledge:consistency | knowledge | consistency | coherent understanding | 0 | NO_ITEMS | Technical model is consistent |
| B:wisdom:necessity | wisdom | necessity | essential discernment | 0 | NO_ITEMS | Key trade-offs are surfaced |
| B:wisdom:sufficiency | wisdom | sufficiency | adequate judgment | 0 | NO_ITEMS | Judgment rationale is adequate in Guidance |
| B:wisdom:completeness | wisdom | completeness | holistic insight | 0 | NO_ITEMS | Cross-deliverable relationships documented |
| B:wisdom:consistency | wisdom | consistency | principled reasoning | 0 | NO_ITEMS | Principles in Guidance are consistent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| B-001 | B:data:necessity | MissingSlot | Datasheet | Datasheet | Populate "Responsible Party" field (currently TBD) | Datasheet Identification table lists Responsible Party as TBD; this is an essential fact for accountability and execution ownership | Datasheet.md | Identification | — | Project governance | TBD |
| B-002 | B:data:completeness | MissingSlot | Datasheet | Datasheet | Add a "Content Block Format" attribute row documenting the expected SDK content block structure (type field values, source encoding, etc.) | The Datasheet enumerates inputs, outputs, extensions, and size limits but does not record the output content block schema; Specification REQ-12 references it without defining it; Procedure Step 3.2 flags it as ASSUMPTION | Datasheet.md | Attributes > Attachment Resolver Module | — | Anthropic Agent SDK documentation | TBD |

---

## Matrix C — Formulation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| C:normative:necessity | normative | necessity | Enforceable Obligation | 0 | NO_ITEMS | All obligations are clear SHALL statements |
| C:normative:sufficiency | normative | sufficiency | Demonstrated Compliance | 1 | HAS_ITEMS | Verification approach for REQ-06 missing boundary detail |
| C:normative:completeness | normative | completeness | Comprehensive Regulatory Scope | 0 | NO_ITEMS | Scope coverage is comprehensive for stated SOW items |
| C:normative:consistency | normative | consistency | Harmonized Enforcement | 0 | NO_ITEMS | Enforcement language is consistent |
| C:operative:necessity | operative | necessity | Operational Readiness | 0 | NO_ITEMS | Prerequisites table covers readiness |
| C:operative:sufficiency | operative | sufficiency | Competent Execution | 0 | NO_ITEMS | Steps are sufficiently detailed |
| C:operative:completeness | operative | completeness | Exhaustive Process Coverage | 0 | NO_ITEMS | Procedure covers all requirement areas |
| C:operative:consistency | operative | consistency | Predictable Operation | 1 | HAS_ITEMS | Procedure does not specify order of validation checks |
| C:evaluative:necessity | evaluative | necessity | Intrinsic Merit | 0 | NO_ITEMS | Merit articulated via OBJ-003 |
| C:evaluative:sufficiency | evaluative | sufficiency | Warranted Valuation | 0 | NO_ITEMS | Trade-offs adequately justify decisions |
| C:evaluative:completeness | evaluative | completeness | Comprehensive Appraisal | 0 | NO_ITEMS | Appraisal criteria covered in verification |
| C:evaluative:consistency | evaluative | consistency | Principled Merit | 0 | NO_ITEMS | Principles are consistent with trade-offs |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| C-001 | C:normative:sufficiency | VerificationGap | Specification | Specification | Enhance REQ-06-V pass criteria to specify boundary behavior: does exactly 18 MB pass or fail? What happens when a file that individually passes pushes the aggregate over? | REQ-06-V says "Aggregate file sizes exceeding 18 MB raw are rejected; within budget passes" but does not define boundary equality or sequential vs. aggregate accounting, making compliance demonstration ambiguous | Specification.md | Verification > REQ-06-V | — | docs/SPEC.md Section 9.8 | TBD |
| C-002 | C:operative:consistency | WeakStatement | Procedure | Procedure | Add a note to Step 2 specifying the required order of validation checks (extension check first, then isFile, then per-file size, then aggregate budget) or state that order is implementation-discretionary | Procedure Step 2 lists validation checks (2.1-2.5) but does not specify whether these must be applied in a particular order; order affects which error message the operator sees first and whether expensive I/O (file read) is avoided when extension check would fail | Procedure.md | Steps > Step 2 | — | Implementation discretion or docs/SPEC.md | TBD |

---

## Matrix F — Requirements (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| F:normative:necessity | normative | necessity | Unconditional Mandate | 0 | NO_ITEMS | Mandates are unconditional and sourced |
| F:normative:sufficiency | normative | sufficiency | Defensible Regulatory Standard | 1 | HAS_ITEMS | SDK API standard not fully defensible |
| F:normative:completeness | normative | completeness | Total Governance Coverage | 0 | NO_ITEMS | SOW items fully traced to requirements |
| F:normative:consistency | normative | consistency | Coherent Regulatory Discipline | 0 | NO_ITEMS | Requirements are internally consistent |
| F:operative:necessity | operative | necessity | Activation Prerequisite | 1 | HAS_ITEMS | Prerequisite status values all TBD |
| F:operative:sufficiency | operative | sufficiency | Demonstrated Capability | 0 | NO_ITEMS | Verification approaches are defined |
| F:operative:completeness | operative | completeness | Total Process Mastery | 0 | NO_ITEMS | Process steps cover full scope |
| F:operative:consistency | operative | consistency | Disciplined Process Reliability | 0 | NO_ITEMS | Process reliability addressed through testing |
| F:evaluative:necessity | evaluative | necessity | Foundational Value Judgment | 1 | HAS_ITEMS | No explicit quality attribute targets |
| F:evaluative:sufficiency | evaluative | sufficiency | Substantiated Quality | 0 | NO_ITEMS | Quality substantiation via verification matrix |
| F:evaluative:completeness | evaluative | completeness | Exhaustive Value Assessment | 0 | NO_ITEMS | Value assessment covered in Guidance |
| F:evaluative:consistency | evaluative | consistency | Integrated Quality Standard | 0 | NO_ITEMS | Quality standards are integrated |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| F-001 | F:normative:sufficiency | TBD_Question | Specification | Specification | Obtain Anthropic Agent SDK documentation for the `query()` API (string vs. AsyncIterable prompt modes) and update Standards table to change accessibility from ASSUMPTION to Accessible with a concrete reference | Specification Standards table marks SDK documentation as "ASSUMPTION: likely applicable" with "location TBD"; this is the normative basis for REQ-10, REQ-11, and REQ-12 but cannot be verified without the actual SDK reference | Specification.md | Standards | — | Anthropic Agent SDK documentation | TBD |
| F-002 | F:operative:necessity | WeakStatement | Procedure | Procedure | Resolve prerequisite Status fields (items 1, 2, 3, 6 are TBD) before execution begins, or add a pre-execution check step that confirms readiness | Procedure Prerequisites table has 4 of 7 items with Status=TBD; these are activation prerequisites that must be confirmed before work begins, but no step enforces their resolution | Procedure.md | Prerequisites | — | Execution team | TBD |
| F-003 | F:evaluative:necessity | MissingSlot | Guidance | Guidance | Add a "Quality Attributes" or "Non-functional Expectations" section identifying performance targets (e.g., resolver latency budget, maximum acceptable I/O time per file) and reliability expectations | Guidance articulates functional principles and trade-offs but does not state any non-functional quality attribute targets; for a backend feature slice processing potentially large files, latency and I/O behavior are evaluatively necessary | Guidance.md | entire document scanned | — | Architecture / Performance requirements | TBD |

---

## Matrix D — Objectives (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| D:normative:guiding | normative | guiding | Resolved Directive Authority | 0 | NO_ITEMS | Directive authority is clear (SPEC.md Section 9.8) |
| D:normative:applying | normative | applying | Established Compliance Method | 0 | NO_ITEMS | Compliance methods established through verification matrix |
| D:normative:judging | normative | judging | Definitive Conformance Ruling | 0 | NO_ITEMS | Conformance rulings will come from test execution |
| D:normative:reviewing | normative | reviewing | Resolved Compliance Audit | 0 | NO_ITEMS | Audit approach defined in Procedure verification table |
| D:operative:guiding | operative | guiding | Resolved Process Guidance | 1 | HAS_ITEMS | Integration coordination guidance missing |
| D:operative:applying | operative | applying | Proven Implementation Method | 0 | NO_ITEMS | Implementation method is assess-then-implement |
| D:operative:judging | operative | judging | Confirmed Performance Verdict | 0 | NO_ITEMS | Performance verdict via test execution |
| D:operative:reviewing | operative | reviewing | Confirmed Process Stability | 0 | NO_ITEMS | Process stability through Records table |
| D:evaluative:guiding | evaluative | guiding | Grounded Value Alignment | 0 | NO_ITEMS | Value alignment grounded in OBJ-003 |
| D:evaluative:applying | evaluative | applying | Realized Quality Standard | 1 | HAS_ITEMS | Validation script update uncertain |
| D:evaluative:judging | evaluative | judging | Conclusive Merit Verdict | 0 | NO_ITEMS | Merit verdict via verification completion |
| D:evaluative:reviewing | evaluative | reviewing | Established Quality Benchmark | 0 | NO_ITEMS | Quality benchmark via pass criteria |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| D-001 | D:operative:guiding | RationaleGap | Procedure | Guidance | Add guidance on coordination strategy with DEL-03-02 for integration testing, given Prerequisite 7 flags concurrent development as ASSUMPTION | Procedure Prerequisite 7 notes DEL-03-02 may be developed concurrently and integration testing "may require coordination," but no guidance exists on how to handle this dependency (mock strategy, integration branch, etc.) | Procedure.md | Prerequisites > item 7 | — | Project scheduling / DEL-03-02 team | TBD |
| D-002 | D:evaluative:applying | WeakStatement | Procedure | Procedure | Clarify whether harness validation script updates (Step 8.2) are required or optional; if required, add as a verification check | Procedure Step 8.2 says "assess whether they need extension" and Specification Documentation table marks it as ASSUMPTION; this leaves it unclear whether validation script updates are a deliverable obligation or optional | Procedure.md | Steps > Step 8 | — | Project governance | TBD |

---

## Matrix X — Verification (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| X:guiding:necessity | guiding | necessity | Directed Essential Imperative | 0 | NO_ITEMS | Essential imperatives are directed through requirements |
| X:guiding:sufficiency | guiding | sufficiency | Substantiated Guidance | 0 | NO_ITEMS | Guidance is substantiated with source citations |
| X:guiding:completeness | guiding | completeness | Holistic Directive Scope | 0 | NO_ITEMS | Directive scope covers all SOW items |
| X:guiding:consistency | guiding | consistency | Harmonized Directive Coherence | 0 | NO_ITEMS | Directives are coherent across documents |
| X:applying:necessity | applying | necessity | Critical Practice Requirement | 1 | HAS_ITEMS | Missing error response body specification |
| X:applying:sufficiency | applying | sufficiency | Validated Application Method | 0 | NO_ITEMS | Application methods are validated through tests |
| X:applying:completeness | applying | completeness | Comprehensive Practice Scope | 1 | HAS_ITEMS | Missing file-not-found handling |
| X:applying:consistency | applying | consistency | Standardized Practice Reliability | 0 | NO_ITEMS | Practice standards are reliable |
| X:judging:necessity | judging | necessity | Critical Adjudication Threshold | 1 | HAS_ITEMS | REQ-07-V missing warning block format |
| X:judging:sufficiency | judging | sufficiency | Evidenced Adjudication | 0 | NO_ITEMS | Adjudication evidence via test results |
| X:judging:completeness | judging | completeness | Exhaustive Verdict Scope | 0 | NO_ITEMS | Verdict scope covers all requirements |
| X:judging:consistency | judging | consistency | Principled Judgment Consistency | 0 | NO_ITEMS | Judgment criteria are consistently principled |
| X:reviewing:necessity | reviewing | necessity | Obligatory Review Standard | 0 | NO_ITEMS | Review standards defined in Procedure |
| X:reviewing:sufficiency | reviewing | sufficiency | Warranted Review Adequacy | 0 | NO_ITEMS | Review adequacy addressed in verification table |
| X:reviewing:completeness | reviewing | completeness | Exhaustive Inspection Scope | 1 | HAS_ITEMS | No code review checkpoint in Procedure |
| X:reviewing:consistency | reviewing | consistency | Standardized Oversight Discipline | 0 | NO_ITEMS | Oversight discipline is standardized |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| X-001 | X:applying:necessity | MissingSlot | Specification | Specification | Add a requirement or clarification for the HTTP 400 response body format (e.g., JSON error object with failed file list and reasons) | REQ-08 specifies HTTP 400 on total failure but does not define the response body structure; DEL-04-02 (UI) needs to parse this response for rollback behavior, making the response contract a critical practice requirement | Specification.md | Requirements > REQ-08 | — | docs/SPEC.md Section 9.8 or architecture decision | TBD |
| X-002 | X:applying:completeness | VerificationGap | Specification | Specification | Add requirement or test case for file-not-found / permission-denied scenarios (path exists in array but file is missing or unreadable) | Requirements cover extension, isFile, size, and budget validation but do not address the case where a path references a non-existent file or a file the process cannot read; this is a practical execution path that must be handled | Specification.md | Requirements (entire section scanned) | — | Implementation / error handling design | TBD |
| X-003 | X:judging:necessity | VerificationGap | Specification | Specification | Specify the expected format/content of the warning text block in REQ-07-V pass criteria (e.g., must list each failed filename and reason) | REQ-07 requires prepending a "warning text block" but neither the requirement nor its verification defines the minimum content of that warning; adjudication of whether a warning is adequate requires a defined format | Specification.md | Requirements > REQ-07 / Verification > REQ-07-V | — | docs/SPEC.md Section 9.8 or UX design | TBD |
| X-004 | X:reviewing:completeness | RationaleGap | Procedure | Procedure | Add an explicit code review step (or checkpoint) in the Procedure referencing Verification V7 ("Client metadata is never used") to ensure server-side-only classification is confirmed by review, not just tests | Procedure Verification table lists V7 as "Code review" method but no Procedure step explicitly calls for a code review checkpoint; the review is listed as a verification method without a corresponding procedural step | Procedure.md | Verification > V7 vs. Steps (entire section) | — | Process governance | TBD |

---

## Matrix E — Evaluation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| E:normative:necessity | normative | necessity | Sovereign Compliance Boundary | 0 | NO_ITEMS | Compliance boundaries are sovereign (SPEC-derived) |
| E:normative:sufficiency | normative | sufficiency | Validated Regulatory Threshold | 0 | NO_ITEMS | Thresholds are validated through verification matrix |
| E:normative:completeness | normative | completeness | Total Regulatory Domain | 1 | HAS_ITEMS | Normalization gap in terminology |
| E:normative:consistency | normative | consistency | Systematic Regulatory Integrity | 0 | NO_ITEMS | Regulatory integrity is systematic |
| E:operative:necessity | operative | necessity | Operational Capability Gate | 0 | NO_ITEMS | Capability gates defined through prerequisites |
| E:operative:sufficiency | operative | sufficiency | Proven Execution Adequacy | 0 | NO_ITEMS | Execution adequacy proven through tests |
| E:operative:completeness | operative | completeness | Total Operational Scope | 0 | NO_ITEMS | Operational scope is total for stated deliverable |
| E:operative:consistency | operative | consistency | Systematic Process Integrity | 0 | NO_ITEMS | Process integrity is systematic |
| E:evaluative:necessity | evaluative | necessity | Foundational Quality Threshold | 0 | NO_ITEMS | Quality thresholds addressed in verification |
| E:evaluative:sufficiency | evaluative | sufficiency | Demonstrated Value Sufficiency | 0 | NO_ITEMS | Value sufficiency demonstrated through trade-offs |
| E:evaluative:completeness | evaluative | completeness | Exhaustive Quality Domain | 1 | HAS_ITEMS | Cross-deliverable verification gap |
| E:evaluative:consistency | evaluative | consistency | Integrated Quality Integrity | 0 | NO_ITEMS | Quality integrity is integrated |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| E-001 | E:normative:completeness | Normalization | Multi | Guidance | Standardize terminology for the resolver function name: Datasheet uses `resolveAttachmentsToContentBlocks(message, attachmentPaths)`, Specification REQ-12 uses `resolveAttachmentsToContentBlocks`, and Procedure Step 3.1 uses the same; however, the function signature parameters differ between Datasheet (two params) and Specification (no params shown) | The function name is consistent but the signature presentation varies: Datasheet shows explicit parameters while Specification omits them; this minor inconsistency could cause confusion about the actual API contract | Datasheet.md, Specification.md | Datasheet: Attributes > Attachment Resolver Module; Specification: Requirements > REQ-12 | — | Implementation source code | TBD |
| E-002 | E:evaluative:completeness | VerificationGap | Multi | Specification | Add a verification item or cross-reference confirming that DEL-04-01 resolver output is compatible with DEL-04-02 UI expectations (error format for rollback, content block format for display) | Guidance C5 documents the DEL-04-01/DEL-04-02 contract but no verification item confirms cross-deliverable compatibility; the quality domain is incomplete without verifying the inter-deliverable interface | Guidance.md, Specification.md | Guidance: Considerations > C5; Specification: Verification (entire section) | — | PKG-04 integration planning | TBD |
