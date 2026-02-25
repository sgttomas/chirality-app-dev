# Datasheet -- DEL-06-05 Governance Coherence + Guardrails (OUT boundaries)

## Identification

| Field | Value |
|-------|-------|
| **Deliverable ID** | DEL-06-05 |
| **Name** | Governance Coherence + Guardrails (OUT boundaries) |
| **Package** | PKG-06 -- Agent Suite & Governance |
| **Type** | DOC_UPDATE |
| **Context Envelope** | S |
| **Responsible Party** | TBD -- **Note (A-001):** Accountable-owner assignment remains open follow-up. Human waiver `HW-DEL-06-05-A001-2026-02-24` permits `ISSUED` without treating A-001 as a lifecycle blocker. |
| **Anticipated Artifacts** | DOC |

## Issuance Hygiene (2026-02-24)

- Lifecycle state is `ISSUED`.
- Human waiver `HW-DEL-06-05-A001-2026-02-24` explicitly overrides A-001 as an issuance precondition.
- Legacy `TBD`/assumption language in this deliverable set is non-blocking unless explicitly reclassified by a new human ruling.

## Attributes

| Attribute | Value | Source |
|-----------|-------|--------|
| **Scope Items Covered** | SOW-030, SOW-039, SOW-040, SOW-041, SOW-042, SOW-043 | Decomposition (Scope Ledger) |
| **Objectives Supported** | OBJ-006 | Decomposition (DEL-06-05 row) |
| **Governing Documents** | `docs/DIRECTIVE.md`, `docs/CONTRACT.md`, `docs/SPEC.md`, `docs/TYPES.md`, `docs/PLAN.md` | Decomposition (References) |
| **Invariants Relevant** | K-HIER-1, K-AUTH-1, K-AUTH-2, K-BIND-1, K-SEAL-1, K-STATUS-1, K-DEP-1, K-INVENT-1, K-CONFLICT-1, K-WRITE-1 | `docs/CONTRACT.md` |
| **Decomposition Revision** | G7-APPROVED (2026-02-21) | Decomposition header |

### Invariant relevance mapping (B-002, E-001)

The Attributes table lists 10 invariants as relevant to this deliverable. The following table maps each invariant to its role in the governance coherence and guardrail mission. Invariants that are directly referenced by Specification requirements are marked as **traced**; others are marked as **contextually relevant** with an explanation.

| Invariant | Traceability | Role in DEL-06-05 |
|-----------|-------------|-------------------|
| K-HIER-1 | **Traced** (REQ-COH-01) | Enforces the flat `package -> deliverable` hierarchy that coherence verification checks. Source: `docs/CONTRACT.md` |
| K-AUTH-1 | **Traced** (REQ-GR-02, REQ-GR-03) | Backs the no-automated-approval guardrail (SOW-039) and contributes to safety-critical review (SOW-041). Source: `docs/CONTRACT.md` Section 1.2 |
| K-AUTH-2 | **Contextually relevant** | Extends K-AUTH-1's authority constraints to additional approval contexts. Source: `docs/CONTRACT.md` Section 1.2 |
| K-SEAL-1 | **Traced** (REQ-GR-03) | Requires human seal before Type 2 execution; backs safety-critical review guardrail (SOW-041). Source: `docs/CONTRACT.md` Section 1.3 |
| K-STATUS-1 | **Traced** (REQ-COH-05) | Enforces file-based authoritative state, which coherence verification confirms is stated consistently. Source: `docs/CONTRACT.md` |
| K-DEP-1 | **Traced** (REQ-COH-05) | Enforces file-based dependency authority, consistent with the filesystem-as-state coherence dimension. Source: `docs/CONTRACT.md` |
| K-BIND-1 | **Contextually relevant** | Governs binding between governance artifacts; relevant to coherence because cross-document references must respect binding rules. Source: `docs/CONTRACT.md` Section 1.2 |
| K-INVENT-1 | **Contextually relevant** | Prohibits invention of content not in sources; relevant to guardrail integrity (agents must not fabricate guardrail exceptions). Source: `docs/CONTRACT.md` Section 1.9 |
| K-CONFLICT-1 | **Contextually relevant** | Governs conflict resolution between governance documents; directly relevant to the coherence mission when documents disagree. Source: `docs/CONTRACT.md` Section 1.9 |
| K-WRITE-1 | **Contextually relevant** | Governs write-scope constraints for agents; relevant to guardrail enforcement because write-scope violations could undermine documented boundaries. Source: `docs/CONTRACT.md` Section 1.10 |

**Note:** Section references for contextually relevant invariants were verified in the 2026-02-24 coherence review (`Governance_Coherence_Verification_Report_2026-02-24.md`). Contextual relevance remains a governance judgment, but section locations are no longer TBD.

## Conditions

### IN-scope coherence domain (SOW-030)

The five governance documents must remain internally aligned on the core model:

| Coherence Dimension | Documents Involved | Source |
|---------------------|--------------------|--------|
| Hierarchy model (flat `package->deliverable`) | TYPES, SPEC, CONTRACT | `docs/PLAN.md` Section 1 ("Governance Alignment") |
| Authoritative execution state is file-based | SPEC, CONTRACT, DIRECTIVE | `docs/PLAN.md` Section 1 ("Governance Alignment") |
| Invariant catalog centralized in CONTRACT | CONTRACT (primary), all others (consumers) | `docs/PLAN.md` Section 1 ("Governance Alignment") |
| Agent role boundaries and write scopes | Agent instructions + SPEC Section 9 | `docs/PLAN.md` Section 1 ("Governance Alignment") |

### OUT-of-scope guardrails

| Guardrail | Scope Item | Status | Source |
|-----------|------------|--------|--------|
| No automated approval or issuance of deliverables by agents | SOW-039 | OUT | `docs/DIRECTIVE.md` Section 4.2; `docs/CONTRACT.md` K-AUTH-1 |
| No financial transactions or binding commitments | SOW-040 | OUT | `docs/DIRECTIVE.md` Section 4.2 |
| No safety-critical decisions without human review | SOW-041 | OUT | `docs/DIRECTIVE.md` Section 4.2 |
| No replacing professional judgment in regulated practice | SOW-042 | OUT | `docs/DIRECTIVE.md` Section 4.2 |
| No external system integration (exception: Anthropic API per DEC-NET-001) | SOW-043 | OUT | `docs/DIRECTIVE.md` Section 4.2; Decomposition DEC-NET-001 |

## Construction

### Governance document inventory (X-003 enrichment: version provenance)

| Document | Path | Primary Purpose | Version Identifier | Source |
|----------|------|-----------------|-------------------|--------|
| DIRECTIVE | `docs/DIRECTIVE.md` | Founding intent, constraints, in/out scope, human authority | `2026-02-21 / fb7fe065e0492f5221714d7921f7bd453746e9fa` | Decomposition (References) |
| CONTRACT | `docs/CONTRACT.md` | Binding invariants (`K-*`) and enforcement map | `2026-02-21 / fb7fe065e0492f5221714d7921f7bd453746e9fa` | Decomposition (References) |
| SPEC | `docs/SPEC.md` | Canonical filesystem structures, harness contract, snapshot rules, schemas | `2026-02-23 / 6d3f37cbb9082fbfba255bd40637810e7e23e542` | Decomposition (References) |
| TYPES | `docs/TYPES.md` | Canonical vocabulary, stable ID formats, lifecycle states | `2026-02-22 / 819b3f245db43c70711f1dcc39654d16682e97b5` | Decomposition (References) |
| PLAN | `docs/PLAN.md` | Implemented surface area + future hardening candidates | `2026-02-23 / 6d3f37cbb9082fbfba255bd40637810e7e23e542` | Decomposition (References) |

**Note (X-003):** Version identifiers (git commit hash or document revision date) should be recorded at the time of each coherence review execution. Without version provenance, verification results cannot be traced to specific document states and audits cannot be compared across reviews. Source: **ASSUMPTION: version tracking inferred from auditability principles; no explicit version-recording requirement exists in the current governance documents.**

### Guardrail enforcement mechanisms

| Guardrail (SOW) | Primary Enforcement | Backing Invariant | Source |
|------------------|--------------------|--------------------|--------|
| SOW-039 | Agent instruction constraints; K-AUTH-1 | K-AUTH-1: Only humans author binding approval records | `docs/CONTRACT.md` Section 1.2 |
| SOW-040 | DIRECTIVE out-of-scope declaration | None specific (covered by DIRECTIVE Section 4.2) | `docs/DIRECTIVE.md` Section 4.2 |
| SOW-041 | DIRECTIVE professional responsibility model; human review gates | K-AUTH-1, K-SEAL-1 | `docs/DIRECTIVE.md` Section 3; `docs/CONTRACT.md` Sections 1.2, 1.3 |
| SOW-042 | DIRECTIVE professional responsibility model | None specific (covered by DIRECTIVE Section 3) | `docs/DIRECTIVE.md` Section 3 |
| SOW-043 | DIRECTIVE out-of-scope declaration; DEC-NET-001 exception | None specific (covered by DIRECTIVE Section 4.2 + decision log) | `docs/DIRECTIVE.md` Section 4.2; Decomposition DEC-NET-001 |

## References

| Ref | Document | Relevance |
|-----|----------|-----------|
| 1 | `execution/_Decomposition/ChiralityApp_SoftwareDecomposition_2026-02-21_G7-APPROVED.md` | Decomposition entry for DEL-06-05; scope ledger; decision log |
| 2 | `docs/DIRECTIVE.md` | Out-of-scope boundaries (Section 4.2); professional responsibility model (Section 3); founding intent |
| 3 | `docs/CONTRACT.md` | Invariant catalog (K-AUTH-1, K-BIND-1, K-SEAL-1, etc.); enforcement map |
| 4 | `docs/SPEC.md` | Physical structures and mechanics; agent instruction file structure (Section 9) |
| 5 | `docs/TYPES.md` | Canonical vocabulary; lifecycle states; agent roles |
| 6 | `docs/PLAN.md` | Governance alignment status (Section 1); future hardening candidates (Section 3) |
