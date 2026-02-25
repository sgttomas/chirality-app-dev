# Semantic Lensing Register: DEL-02-06 Settings / API Key Entry UI

**Generated:** 2026-02-24
**Deliverable Folder:** `execution/PKG-02_Desktop_UI_Workflow/1_Working/DEL-02-06_Settings_API_Key_Entry_UI/`
**Warnings:** none

**Inputs Read:**
- _CONTEXT.md — `execution/PKG-02_Desktop_UI_Workflow/1_Working/DEL-02-06_Settings_API_Key_Entry_UI/_CONTEXT.md`
- _STATUS.md — `execution/PKG-02_Desktop_UI_Workflow/1_Working/DEL-02-06_Settings_API_Key_Entry_UI/_STATUS.md`
- _SEMANTIC.md — `execution/PKG-02_Desktop_UI_Workflow/1_Working/DEL-02-06_Settings_API_Key_Entry_UI/_SEMANTIC.md`
- Datasheet.md — `execution/PKG-02_Desktop_UI_Workflow/1_Working/DEL-02-06_Settings_API_Key_Entry_UI/Datasheet.md`
- Specification.md — `execution/PKG-02_Desktop_UI_Workflow/1_Working/DEL-02-06_Settings_API_Key_Entry_UI/Specification.md`
- Guidance.md — `execution/PKG-02_Desktop_UI_Workflow/1_Working/DEL-02-06_Settings_API_Key_Entry_UI/Guidance.md`
- Procedure.md — `execution/PKG-02_Desktop_UI_Workflow/1_Working/DEL-02-06_Settings_API_Key_Entry_UI/Procedure.md`
- _REFERENCES.md — `execution/PKG-02_Desktop_UI_Workflow/1_Working/DEL-02-06_Settings_API_Key_Entry_UI/_REFERENCES.md`

**Purpose:** Apply CHIRALITY_FRAMEWORK matrix cells as lenses over the production documents, capturing warranted enrichment inputs for a later enrichment pass.

## Summary

- Total warranted items: 18
- By document:
  - Datasheet: 4
  - Specification: 7
  - Guidance: 0
  - Procedure: 3
  - Multi: 4
- By matrix:
  - A: 4  B: 3  C: 2  F: 3  D: 2  X: 2  E: 2
- By type:
  - Conflict: 1
  - VerificationGap: 4
  - MissingSlot: 4
  - WeakStatement: 3
  - RationaleGap: 2
  - Normalization: 2
  - TBD_Question: 2
  - MatrixError: 0
- Notable conflicts: 1
- Matrix parse errors: 0

---

## Matrix A — Orientation (3x4) — Canonical

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| A:normative:guiding | normative | guiding | prescriptive direction | 1 | HAS_ITEMS | Key validation decision unresolved |
| A:normative:applying | normative | applying | mandatory practice | 1 | HAS_ITEMS | Lifecycle state inconsistency in Datasheet |
| A:normative:judging | normative | judging | compliance determination | 1 | HAS_ITEMS | External standard accessibility gap |
| A:normative:reviewing | normative | reviewing | regulatory audit | 0 | NO_ITEMS | Verification table in Specification covers audit paths adequately |
| A:operative:guiding | operative | guiding | procedural direction | 0 | NO_ITEMS | Procedure Step 1-6 provides clear procedural direction |
| A:operative:applying | operative | applying | practical execution | 1 | HAS_ITEMS | IPC retrieve channel security undetermined |
| A:operative:judging | operative | judging | performance assessment | 0 | NO_ITEMS | Verification table and Procedure checks are consistent |
| A:operative:reviewing | operative | reviewing | process audit | 0 | NO_ITEMS | Process audit paths are covered via Procedure verification table |
| A:evaluative:guiding | evaluative | guiding | value orientation | 0 | NO_ITEMS | Guidance Principles P1-P3 provide clear value orientation |
| A:evaluative:applying | evaluative | applying | merit application | 0 | NO_ITEMS | Trade-offs T1-T3 in Guidance apply merit considerations adequately |
| A:evaluative:judging | evaluative | judging | worth determination | 0 | NO_ITEMS | Acceptance criteria link to value via security and usability |
| A:evaluative:reviewing | evaluative | reviewing | quality appraisal | 0 | NO_ITEMS | Quality checks distributed across Procedure verification table |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A-001 | A:normative:guiding | TBD_Question | Multi | Guidance | Record human decision on key validation at entry time (validate-on-save vs store-without-validation). Guidance T3 leaves this TBD; Specification has no requirement either way. | The prescriptive direction for key validation behavior is absent -- Guidance T3 explicitly marks it TBD and defers to human. Without a ruling, implementers cannot determine whether a network call on save is required. | Guidance.md; Specification.md | Guidance.md#T3: Key Validation at Entry Time; Specification.md#Requirements (entire section scanned) | — | Human ruling needed | TBD |
| A-002 | A:normative:applying | Normalization | Datasheet | Datasheet | Update Datasheet Lifecycle State from "INITIALIZED" to "SEMANTIC_READY" to match _STATUS.md current state. | Datasheet Identification table says "INITIALIZED" but _STATUS.md records current state as SEMANTIC_READY. This is a mandatory-practice inconsistency that could cause confusion about deliverable readiness. | Datasheet.md; _STATUS.md | Datasheet.md#Identification; _STATUS.md#Current State | Datasheet.md#Identification ("INITIALIZED"); _STATUS.md ("SEMANTIC_READY") | _STATUS.md is authoritative for lifecycle state (PROPOSAL) | TBD |
| A-003 | A:normative:judging | MissingSlot | Specification | Specification | Add accessibility information or a local copy reference for the Electron safeStorage API and OWASP credential storage guidelines listed in the Standards table. | Two standards in the Specification Standards table are marked "Accessible: No" with "location TBD". Compliance determination against these standards is not possible until they are accessible or their relevant requirements are extracted. | Specification.md | Specification.md#Standards | — | — | TBD |
| A-004 | A:operative:applying | WeakStatement | Procedure | Specification | Clarify whether the renderer process should ever receive the decrypted key, or whether only the main process should hold it. Procedure Step 3.1 marks this TBD. | Procedure Step 3.1 explicitly states "TBD -- determine if renderer should receive the decrypted key or if only the main process should hold it." This is an open practical execution question that affects the IPC channel design and security posture. Specification REQ-06 requires main-process isolation (ASSUMPTION) but does not resolve the retrieve channel question. | Procedure.md; Specification.md | Procedure.md#Step 3: Implement Key Resolution Bridge; Specification.md#REQ-06 | — | — | TBD |

---

## Matrix B — Conceptualization (4x4) — Canonical

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| B:data:necessity | data | necessity | essential fact | 1 | HAS_ITEMS | Key resolution bridge API contract undefined |
| B:data:sufficiency | data | sufficiency | adequate evidence | 0 | NO_ITEMS | Datasheet Attributes table provides adequate evidence for key attributes |
| B:data:completeness | data | completeness | comprehensive record | 1 | HAS_ITEMS | Missing error taxonomy |
| B:data:consistency | data | consistency | reliable measurement | 0 | NO_ITEMS | Data values consistent across documents |
| B:information:necessity | information | necessity | essential signal | 0 | NO_ITEMS | Key status signals defined in REQ-02 and REQ-08 |
| B:information:sufficiency | information | sufficiency | adequate context | 0 | NO_ITEMS | Context for key provisioning is adequately provided across docs |
| B:information:completeness | information | completeness | comprehensive account | 0 | NO_ITEMS | Information flows are comprehensively described |
| B:information:consistency | information | consistency | coherent message | 1 | HAS_ITEMS | ASSUMPTION density lacks consolidated tracking |
| B:knowledge:necessity | knowledge | necessity | fundamental understanding | 0 | NO_ITEMS | Guidance provides sufficient architectural understanding |
| B:knowledge:sufficiency | knowledge | sufficiency | competent expertise | 0 | NO_ITEMS | Electron safeStorage pattern is well-documented in Guidance C2-C3 |
| B:knowledge:completeness | knowledge | completeness | thorough mastery | 0 | NO_ITEMS | Domain coverage is thorough for the scope |
| B:knowledge:consistency | knowledge | consistency | coherent understanding | 0 | NO_ITEMS | Understanding is coherent across docs |
| B:wisdom:necessity | wisdom | necessity | essential discernment | 0 | NO_ITEMS | Trade-offs T1-T3 capture necessary discernment points |
| B:wisdom:sufficiency | wisdom | sufficiency | adequate judgment | 0 | NO_ITEMS | Judgment calls are adequately supported by rationale |
| B:wisdom:completeness | wisdom | completeness | holistic insight | 0 | NO_ITEMS | Holistic view is maintained via Guidance principles and considerations |
| B:wisdom:consistency | wisdom | consistency | principled reasoning | 0 | NO_ITEMS | Reasoning is principled and consistent across documents |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| B-001 | B:data:necessity | MissingSlot | Datasheet | Datasheet | Add a data record for the key resolution bridge API contract (IPC channel names, method signatures, return types). Procedure Step 3 defines channel names but Datasheet Construction table has "TBD -- specific API/IPC contract". | The essential fact of the API contract between DEL-02-06 and DEL-03-05 is described in Procedure (channel names) but absent from Datasheet as a data record. The Datasheet Construction table notes "TBD" for the key resolution bridge specifics. | Datasheet.md; Procedure.md | Datasheet.md#Construction ("Key resolution bridge" row); Procedure.md#Step 3 | — | — | TBD |
| B-002 | B:data:completeness | MissingSlot | Specification | Specification | Add an error/failure mode taxonomy for key storage operations (encryption failure, storage full, safeStorage unavailable, corrupted stored key). | No document enumerates what happens when storage operations themselves fail. REQ-08 covers graceful degradation for missing keys but not for storage mechanism failures. This is a comprehensive-record gap. | Specification.md; Procedure.md | Specification.md#REQ-08; Procedure.md#Step 2 (entire section scanned) | — | — | TBD |
| B-003 | B:information:consistency | WeakStatement | Multi | Guidance | Consolidate the ASSUMPTION annotations scattered across all four documents into a single tracked register (e.g., in Guidance or Datasheet) with resolution status. | Multiple ASSUMPTIONs are distributed across Datasheet (2), Specification (6), Guidance (3), and Procedure (3). These are not cross-referenced or tracked for resolution. The coherent-message lens reveals that an implementer must scan all four docs to find all assumptions. | Datasheet.md; Specification.md; Guidance.md; Procedure.md | Datasheet.md#Attributes, #Construction; Specification.md#REQ-01 through REQ-07; Guidance.md#P3, C2, C3; Procedure.md#Prerequisites, Steps 2-3 | — | — | TBD |

---

## Matrix C — Formulation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| C:normative:necessity | normative | necessity | regulatory imperative | 0 | NO_ITEMS | DIRECTIVE 2.5 and SPEC 9.8 constraints are well-captured in Conditions table and REQs |
| C:normative:sufficiency | normative | sufficiency | substantiated mandate | 1 | HAS_ITEMS | REQ-07 change notification is ASSUMPTION-only |
| C:normative:completeness | normative | completeness | comprehensive obligation coverage | 0 | NO_ITEMS | All SOW-050 obligations are traced through REQ-01 to REQ-08 |
| C:normative:consistency | normative | consistency | coherent regulatory standard | 0 | NO_ITEMS | Regulatory references are consistent across documents |
| C:operative:necessity | operative | necessity | fundamental operational capacity | 0 | NO_ITEMS | Procedure prerequisites and steps cover operational necessities |
| C:operative:sufficiency | operative | sufficiency | competent process execution | 0 | NO_ITEMS | Process steps are sufficiently detailed for execution |
| C:operative:completeness | operative | completeness | thorough operational coverage | 1 | HAS_ITEMS | Missing rollback/recovery procedure |
| C:operative:consistency | operative | consistency | reliable process discipline | 0 | NO_ITEMS | Process steps are consistent with specification requirements |
| C:evaluative:necessity | evaluative | necessity | intrinsic value recognition | 0 | NO_ITEMS | Value propositions are clear (security, usability, operator convenience) |
| C:evaluative:sufficiency | evaluative | sufficiency | grounded value assessment | 0 | NO_ITEMS | Trade-offs are grounded in evidence and rationale |
| C:evaluative:completeness | evaluative | completeness | holistic value accounting | 0 | NO_ITEMS | Value dimensions (security, usability, maintainability) are covered |
| C:evaluative:consistency | evaluative | consistency | principled value coherence | 0 | NO_ITEMS | Value principles are coherent across Guidance and Specification |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| C-001 | C:normative:sufficiency | WeakStatement | Specification | Specification | Strengthen REQ-07 change notification from ASSUMPTION to a substantiated requirement, or record as TBD pending human decision. Currently the "ASSUMPTION: change notification is needed" provides insufficient mandate basis. | REQ-07 third bullet states change notification is an ASSUMPTION. This is a substantiated-mandate gap: the requirement exists but its justification is assumption-level, not evidence-level. If change notification is not actually needed (e.g., if the resolver re-queries on each turn), the IPC design changes significantly. | Specification.md | Specification.md#REQ-07 | — | — | TBD |
| C-002 | C:operative:completeness | MissingSlot | Procedure | Procedure | Add a recovery/rollback step or note for what to do when safeStorage becomes unavailable after a key was stored (e.g., OS upgrade, Electron version change, corrupted keychain). | Procedure covers the happy path thoroughly but has no step for operational recovery when the secure storage mechanism itself fails or becomes inaccessible. This is a thorough-operational-coverage gap. | Procedure.md | Procedure.md#Steps (entire section scanned) | — | — | TBD |

---

## Matrix F — Requirements (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| F:normative:necessity | normative | necessity | enforceable governance mandate | 1 | HAS_ITEMS | DEL-03-05 ENV_ONLY vs ENV+UI conflict |
| F:normative:sufficiency | normative | sufficiency | legitimate duty stewardship | 0 | NO_ITEMS | Duty stewardship is legitimate; sources are cited throughout |
| F:normative:completeness | normative | completeness | total regulatory command | 0 | NO_ITEMS | Regulatory command is complete for in-scope constraints |
| F:normative:consistency | normative | consistency | uniform compliance assurance | 1 | HAS_ITEMS | Responsible Party TBD in Datasheet |
| F:operative:necessity | operative | necessity | critical operational readiness | 0 | NO_ITEMS | Prerequisites are enumerated; upstream dependencies noted |
| F:operative:sufficiency | operative | sufficiency | proven process competence | 0 | NO_ITEMS | Process steps demonstrate competent coverage |
| F:operative:completeness | operative | completeness | exhaustive process mastery | 1 | HAS_ITEMS | Verification artifact locations all TBD |
| F:operative:consistency | operative | consistency | dependable operational order | 0 | NO_ITEMS | Steps are ordered logically; no ordering conflicts |
| F:evaluative:necessity | evaluative | necessity | essential merit criterion | 0 | NO_ITEMS | Merit criteria embedded in verification pass criteria |
| F:evaluative:sufficiency | evaluative | sufficiency | warranted quality stewardship | 0 | NO_ITEMS | Quality approach is warranted by security and usability rationale |
| F:evaluative:completeness | evaluative | completeness | exhaustive value accounting | 0 | NO_ITEMS | Value dimensions are accounted for |
| F:evaluative:consistency | evaluative | consistency | principled quality assurance | 0 | NO_ITEMS | Quality assurance approach is principled and consistent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| F-001 | F:normative:necessity | Conflict | Multi | NA | DEL-03-05 REQ-02 specifies ENV_ONLY key resolution; DEL-02-06 and Decomposition SCA-003 establish ENV+UI. This is already surfaced in Guidance CONF-01 but has HumanRuling=TBD. Confirm: is DEL-03-05 REQ-02 to be updated to ENV+UI? | Enforceable governance mandate requires consistency between the two deliverables sharing the key resolution contract. Guidance CONF-01 correctly identifies this conflict but it remains unresolved. | Guidance.md; Specification.md | Guidance.md#Conflict Table (CONF-01); Specification.md#REQ-05 | Guidance.md#CONF-01 Source A: "DEL-03-05 Specification REQ-02 (ENV_ONLY)"; Guidance.md#CONF-01 Source B: "Decomposition SCA-003 / SPEC section 9.8 (ENV+UI)" | Decomposition SCA-003 and SPEC section 9.8 (PROPOSAL) | TBD |
| F-002 | F:normative:consistency | RationaleGap | Datasheet | Datasheet | Assign the Responsible Party field (currently TBD) in the Datasheet Identification table. | Uniform compliance assurance requires a named responsible party. The Datasheet records "TBD" for Responsible Party, leaving ownership ambiguous. | Datasheet.md | Datasheet.md#Identification ("Responsible Party" row) | — | — | TBD |
| F-003 | F:operative:completeness | VerificationGap | Procedure | Procedure | Resolve TBD locations for test results, key setup guide, architecture notes, and verification evidence in the Procedure Records table. | Exhaustive process mastery requires that verification artifacts have defined locations. All four Records table rows have "TBD" locations, making it impossible to locate or audit verification evidence after execution. | Procedure.md | Procedure.md#Records | — | — | TBD |

---

## Matrix D — Objectives (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| D:normative:guiding | normative | guiding | resolved prescriptive authority | 0 | NO_ITEMS | Prescriptive authority is resolved via DIRECTIVE 2.5 and SPEC 9.8 citations |
| D:normative:applying | normative | applying | enforced obligation fulfillment | 1 | HAS_ITEMS | REQ-04 encryption-at-rest ASSUMPTION |
| D:normative:judging | normative | judging | definitive conformance ruling | 0 | NO_ITEMS | Conformance paths defined in Verification table |
| D:normative:reviewing | normative | reviewing | assured compliance verification | 0 | NO_ITEMS | Compliance verification is covered by Specification Verification table |
| D:operative:guiding | operative | guiding | resolved operational guidance | 0 | NO_ITEMS | Guidance C1-C4 provides resolved operational guidance |
| D:operative:applying | operative | applying | resolved execution deployment | 1 | HAS_ITEMS | UI location unresolved |
| D:operative:judging | operative | judging | definitive performance verdict | 0 | NO_ITEMS | Performance criteria are defined in Procedure verification table |
| D:operative:reviewing | operative | reviewing | resolved procedural examination | 0 | NO_ITEMS | Procedure verification checks are clear |
| D:evaluative:guiding | evaluative | guiding | resolved value direction | 0 | NO_ITEMS | Value direction resolved in Guidance Principles |
| D:evaluative:applying | evaluative | applying | resolved merit enactment | 0 | NO_ITEMS | Merit criteria enacted through verification approach |
| D:evaluative:judging | evaluative | judging | definitive worth adjudication | 0 | NO_ITEMS | Worth adjudication criteria are defined |
| D:evaluative:reviewing | evaluative | reviewing | assured quality examination | 0 | NO_ITEMS | Quality examination approach is clear |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| D-001 | D:normative:applying | VerificationGap | Specification | Specification | Add explicit acceptance criterion for encryption-at-rest. REQ-04 states "MUST NOT be stored in plain text" with ASSUMPTION that encryption-at-rest is required, but the Verification table for REQ-04 only checks for "safeStorage or equivalent" and "no plaintext config files" -- it does not verify encryption is actually active. | Enforced obligation fulfillment requires that the encryption-at-rest ASSUMPTION in REQ-04 be either confirmed as a requirement with a verifiable criterion, or explicitly deferred. Currently the verification approach inspects the mechanism but not the encryption property itself. | Specification.md | Specification.md#REQ-04; Specification.md#Verification (REQ-04 row) | — | — | TBD |
| D-002 | D:operative:applying | TBD_Question | Datasheet | Guidance | Resolve the UI location for settings (settings page, modal, panel, or section within existing view). Datasheet Construction and Procedure Step 1.1 both mark this TBD. | Resolved execution deployment cannot proceed until the UI surface location is decided. This is a prerequisite design decision that affects component architecture and navigation. | Datasheet.md; Procedure.md | Datasheet.md#Construction ("Settings panel / page" row); Procedure.md#Step 1.1 | — | Human ruling needed | TBD |

---

## Matrix X — Verification (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| X:guiding:necessity | guiding | necessity | foundational steering imperative | 0 | NO_ITEMS | Steering imperatives are foundational and well-sourced |
| X:guiding:sufficiency | guiding | sufficiency | justified directional leadership | 0 | NO_ITEMS | Directional leadership is justified via Guidance principles |
| X:guiding:completeness | guiding | completeness | comprehensive guidance scope | 0 | NO_ITEMS | Guidance scope is comprehensive for deliverable concerns |
| X:guiding:consistency | guiding | consistency | harmonized directional discipline | 0 | NO_ITEMS | Directional consistency is maintained |
| X:applying:necessity | applying | necessity | vital implementation mandate | 1 | HAS_ITEMS | Missing automated test for key-not-in-working-root |
| X:applying:sufficiency | applying | sufficiency | substantiated implementation delivery | 0 | NO_ITEMS | Implementation steps are substantiated |
| X:applying:completeness | applying | completeness | comprehensive delivery scope | 0 | NO_ITEMS | Delivery scope covers all required components |
| X:applying:consistency | applying | consistency | principled implementation discipline | 0 | NO_ITEMS | Implementation discipline is consistent |
| X:judging:necessity | judging | necessity | binding adjudication criterion | 1 | HAS_ITEMS | REQ-07 integration test scope underspecified |
| X:judging:sufficiency | judging | sufficiency | substantiated adjudication verdict | 0 | NO_ITEMS | Adjudication verdicts are substantiated |
| X:judging:completeness | judging | completeness | exhaustive adjudication scope | 0 | NO_ITEMS | Adjudication scope is exhaustive for requirements |
| X:judging:consistency | judging | consistency | principled adjudication order | 0 | NO_ITEMS | Adjudication order is principled |
| X:reviewing:necessity | reviewing | necessity | mandatory review criterion | 0 | NO_ITEMS | Review criteria defined in Procedure verification |
| X:reviewing:sufficiency | reviewing | sufficiency | substantiated review assurance | 0 | NO_ITEMS | Review assurance is substantiated |
| X:reviewing:completeness | reviewing | completeness | exhaustive review coverage | 0 | NO_ITEMS | Review coverage is exhaustive |
| X:reviewing:consistency | reviewing | consistency | dependable audit discipline | 0 | NO_ITEMS | Audit discipline is dependable |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| X-001 | X:applying:necessity | VerificationGap | Specification | Specification | Add an automated verification criterion for REQ-04/REQ-06: the key-not-in-working-root check is described as "grep-based scan" in Procedure but is listed as "Inspection" in Specification Verification. Clarify whether this is automated or manual and ensure the verification artifact type matches. | Vital implementation mandate for key material protection requires unambiguous verification. Specification says "Inspection" for REQ-04; Procedure says "Automated scan" (grep of projectRoot). The verification approach descriptions diverge. | Specification.md; Procedure.md | Specification.md#Verification (REQ-04 row); Procedure.md#Verification ("Key not in working root" row) | Specification.md#Verification REQ-04: "Inspection"; Procedure.md#Verification: "Automated scan" | — | TBD |
| X-002 | X:judging:necessity | VerificationGap | Specification | Specification | Specify what "successfully queries UI-provided key" means in the REQ-07 verification row. Define the expected integration test scenario (e.g., store key via UI, query via resolver, verify match; remove key, verify resolver returns null). | Binding adjudication criterion for REQ-07 integration test is vague: "DEL-03-05 key resolver successfully queries UI-provided key; receives change notifications." This does not define pass/fail boundaries or test scenarios. | Specification.md | Specification.md#Verification (REQ-07 row) | — | — | TBD |

---

## Matrix E — Evaluation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| E:normative:necessity | normative | necessity | binding regulatory threshold | 0 | NO_ITEMS | Regulatory thresholds are bound to DIRECTIVE/SPEC sources |
| E:normative:sufficiency | normative | sufficiency | legitimate conformance warrant | 1 | HAS_ITEMS | Shared security principle lacks formal authority |
| E:normative:completeness | normative | completeness | total compliance fulfillment | 0 | NO_ITEMS | Compliance paths are complete for in-scope constraints |
| E:normative:consistency | normative | consistency | principled regulatory order | 0 | NO_ITEMS | Regulatory order is principled and consistent |
| E:operative:necessity | operative | necessity | critical execution baseline | 0 | NO_ITEMS | Execution baseline is defined through prerequisites and steps |
| E:operative:sufficiency | operative | sufficiency | demonstrated operational competence | 0 | NO_ITEMS | Operational competence is demonstrated through procedure detail |
| E:operative:completeness | operative | completeness | comprehensive operational breadth | 0 | NO_ITEMS | Operational breadth covers all requirement areas |
| E:operative:consistency | operative | consistency | stable operational discipline | 1 | HAS_ITEMS | Terminology inconsistency for storage mechanism |
| E:evaluative:necessity | evaluative | necessity | definitive quality threshold | 0 | NO_ITEMS | Quality thresholds are defined in verification |
| E:evaluative:sufficiency | evaluative | sufficiency | substantiated quality warrant | 0 | NO_ITEMS | Quality warrants are substantiated |
| E:evaluative:completeness | evaluative | completeness | exhaustive quality realization | 0 | NO_ITEMS | Quality realization is exhaustive for scope |
| E:evaluative:consistency | evaluative | consistency | principled quality order | 0 | NO_ITEMS | Quality order is principled and consistent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| E-001 | E:normative:sufficiency | RationaleGap | Specification | Guidance | Add a rationale note explaining the authority basis for "shared security principle" cited in REQ-06 and Datasheet Conditions. This phrase appears 3 times across docs as a source attribution but is not traced to a specific governance document. | Legitimate conformance warrant requires that security obligations trace to identifiable authority. "Shared security principle" is used as a source but is not defined in DIRECTIVE, SPEC, or any referenced standard. Its legitimacy rests on DEL-03-05 REQ-09 citation, which is a peer deliverable, not governance. | Specification.md; Datasheet.md; Guidance.md | Specification.md#REQ-06; Datasheet.md#Conditions ("Key material MUST NOT appear in logs" row); Guidance.md#P3 | — | — | TBD |
| E-002 | E:operative:consistency | Normalization | Multi | Guidance | Normalize terminology: "local secure storage" (Specification, Guidance), "Local secure storage adapter" (Datasheet, Procedure), "Electron safeStorage" (all docs as mechanism detail). Establish a canonical term in Guidance and use it consistently. | Stable operational discipline requires consistent terminology for the storage mechanism. Three variants appear across documents. While each usage is locally clear, the inconsistency could cause drift in implementation naming. | Datasheet.md; Specification.md; Guidance.md; Procedure.md | Datasheet.md#Construction; Specification.md#REQ-04; Guidance.md#P1, C3; Procedure.md#Step 2 | — | — | TBD |
