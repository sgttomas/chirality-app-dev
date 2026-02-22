# Procedure -- DEL-06-05 Governance Coherence + Guardrails (OUT boundaries)

## Purpose

This procedure defines the steps to verify governance document coherence and confirm that OUT-of-scope guardrails remain explicit and enforceable. It is intended to be executed when any of the following trigger conditions are met (REQ-COH-06):

- **(a)** Any governance document (`docs/DIRECTIVE.md`, `docs/CONTRACT.md`, `docs/SPEC.md`, `docs/TYPES.md`, `docs/PLAN.md`) is modified.
- **(b)** A new decomposition revision is approved.
- **(c)** A periodic review interval has elapsed (interval TBD -- to be set by human).

Source: Specification REQ-COH-06; **ASSUMPTION: trigger conditions inferred from the nature of coherence verification.**

## Prerequisites

| Prerequisite | Description | Source |
|-------------|-------------|--------|
| Governance documents accessible | All five governance documents must be readable: `docs/DIRECTIVE.md`, `docs/CONTRACT.md`, `docs/SPEC.md`, `docs/TYPES.md`, `docs/PLAN.md` | `_REFERENCES.md` |
| Governance document versions recorded | Record the git commit hash or revision date for each governance document at the start of the review. This enables traceability of verification results to specific document versions. **(X-003 enrichment)** | **ASSUMPTION: version recording inferred from auditability principles** |
| Decomposition accessible | The approved decomposition document must be readable for scope ledger verification | `_CONTEXT.md` |
| Current decomposition revision known | The decomposition revision (currently G7-APPROVED, 2026-02-21) must be identified for traceability | Decomposition header |
| Execution authority | TBD -- Determine who is authorized to execute this procedure (human only, agent-assisted, or either) and what authority level is required to sign off on PASS/FAIL results. **(E-002 enrichment)** | **ASSUMPTION: execution authority requirement inferred from operational completeness; no explicit authority level is defined in current governance documents** |

## Steps

### Phase 1: Coherence Verification

#### Step 1: Hierarchy consistency check (REQ-COH-01)

1. Open `docs/TYPES.md` Section 1 and note the hierarchy definition (expected: flat `package -> deliverable`, no nesting).
2. Open `docs/SPEC.md` Sections 1-2 and confirm the execution root layout and deliverable folder layout match the TYPES hierarchy.
3. Open `docs/CONTRACT.md` and confirm K-HIER-1 enforces the same flat hierarchy.
4. Open `docs/DIRECTIVE.md` and confirm structural constraints are consistent with the hierarchy model. **Note (B-001/F-001):** The correct DIRECTIVE section for hierarchy constraints is subject to Conflict Table entry CT-001 in Guidance.md. Until resolved, check both DIRECTIVE Section 4 and Section 5 for hierarchy-related statements.
5. Record result: PASS if all four documents agree; FAIL if any discrepancy found (note the discrepancy).

#### Step 2: Vocabulary consistency check (REQ-COH-02)

1. Open `docs/TYPES.md` and identify the canonical definitions for the minimum term set: deliverable, package, lifecycle states (OPEN, INITIALIZED, SEMANTIC_READY, WORKING, ISSUED), dependency classes (ANCHOR, EXECUTION), agent types (Type 0, Type 1, Type 2), artifact. **(A-003/X-002 enrichment: enumerated minimum term set replaces open-ended spot-check.)**
2. Search each governance document for usage of these terms.
3. Confirm usage matches TYPES definitions. Flag any document that uses a term with a different meaning.
4. Record result: PASS if all terms in the minimum set are consistent; FAIL with specific term/document/discrepancy if inconsistent.

#### Step 3: Invariant catalog single-source check (REQ-COH-03)

1. Open `docs/CONTRACT.md` and list all `K-*` invariant IDs.
2. Search `docs/DIRECTIVE.md`, `docs/SPEC.md`, `docs/TYPES.md`, and `docs/PLAN.md` for any `K-*` identifiers.
3. Confirm that other documents only reference invariants (not define or redefine them).
4. Record result: PASS if CONTRACT is the sole definition source; FAIL if another document defines a new invariant or alters the semantics of an existing one.

#### Step 4: Lifecycle state consistency check (REQ-COH-04)

1. Open `docs/TYPES.md` Section 5 and extract the state sequence, state meanings, and transition rules.
2. Open `docs/SPEC.md` Section 3 and extract the same.
3. Compare side by side.
4. Record result: PASS if states, meanings, and transitions match; FAIL with specific discrepancy if not.

#### Step 5: File-based state authority check (REQ-COH-05)

1. Confirm `docs/DIRECTIVE.md` Section 2.1 asserts filesystem-as-state.
2. Confirm `docs/SPEC.md` Section 2 defines file-based deliverable state.
3. Confirm `docs/CONTRACT.md` K-STATUS-1 and K-DEP-1 enforce file-based authority.
4. Record result: PASS if all three assert file-based authority consistently; FAIL if any document contradicts.

### Phase 2: Guardrail Verification

#### Step 6: DIRECTIVE OUT-boundary presence check (REQ-GR-01)

1. Open `docs/DIRECTIVE.md` Section 4.2.
2. Confirm each of the following is listed as out of scope:
   - Automated approval or issuance of deliverables (SOW-039)
   - Financial transactions or binding commitments (SOW-040)
   - Safety-critical decisions without human review (SOW-041)
   - Replacing professional judgment in regulated practice (SOW-042)
   - External system integration (SOW-043)
3. Record result: PASS if all five present; FAIL if any missing.

#### Step 7: Invariant backing check (REQ-GR-02, REQ-GR-03)

1. Open `docs/CONTRACT.md`.
2. Confirm K-AUTH-1 backs SOW-039 (no automated approval) with defined enforcement points.
3. Confirm K-AUTH-1 and K-SEAL-1 back SOW-041 (no safety-critical decisions without review).
4. Confirm the enforcement map (CONTRACT Section 2) includes these invariants.
5. Record result: PASS if invariant backing is present and enforcement points are defined; FAIL if missing.

#### Step 8: Anthropic API exception consistency check (REQ-GR-04)

1. Confirm `docs/DIRECTIVE.md` Section 4.2 lists external integration as out of scope.
2. Confirm the decomposition Decision Log DEC-NET-001 scopes the exception to Anthropic API only.
3. Confirm the Scope Ledger entry for SOW-043 acknowledges the exception.
4. Confirm these three statements are non-contradictory.
5. Record result: PASS if consistent; FAIL with specific contradiction if not.

#### Step 9: Financial and professional-judgment guardrail check (REQ-GR-05)

1. Confirm `docs/DIRECTIVE.md` Section 4.2 lists both SOW-040 and SOW-042 as out of scope.
2. Confirm DIRECTIVE Section 3 (Professional Responsibility Model) provides the backing rationale for SOW-042.
3. Record result: PASS if both present and supported; FAIL if missing.

#### Step 10: Agent instruction constraint check (REQ-GR-06)

1. Identify agent instruction files (`agents/AGENT_*.md`) for agents with write access to governance-adjacent artifacts (e.g., ORCHESTRATOR, 4_DOCUMENTS, PREPARATION, WORKING_ITEMS, CHANGE).
2. For each identified agent, confirm the instruction file includes explicit write-scope constraints that prevent:
   - Automated approval or issuance (SOW-039 / K-AUTH-1 violation)
   - Bypassing human review gates for safety-critical decisions (SOW-041)
3. Record result: PASS if all identified agents have appropriate write-scope constraints; FAIL with specific agent/gap if any are missing.
4. **Note:** This step verifies the existence of constraints in instruction files. It does not verify runtime enforcement (which is covered by PKG-03 deliverables).

### Phase 3: Traceability Verification

#### Step 11: Scope ledger traceability check (REQ-TRACE-01)

1. Open the decomposition Scope Ledger.
2. Confirm each of SOW-030, SOW-039, SOW-040, SOW-041, SOW-042, SOW-043 has:
   - `PackageID = PKG-06`
   - `DeliverableID(s)` includes `DEL-06-05`
3. Record result: PASS if all six scope items are correctly mapped; FAIL if any is missing or incorrectly assigned.

## Verification

| Step | Expected Result | Verification Method |
|------|----------------|---------------------|
| Steps 1-5 | All coherence checks PASS | Manual cross-document review |
| Steps 6-9 | All guardrail checks PASS | Manual document inspection |
| Step 10 | Agent instruction constraints verified | Agent instruction file review |
| Step 11 | All traceability checks PASS | Scope Ledger row verification |
| Overall | All steps PASS | Aggregate result; any FAIL requires remediation |

### Remediation guidance

If any step results in FAIL:
1. Document the specific discrepancy (which documents, which sections, what the conflict is).
2. Determine which document is authoritative for the conflicting content (use the governance document purpose hierarchy: DIRECTIVE for intent, CONTRACT for invariants, SPEC for structures, TYPES for vocabulary).
3. Propose a correction to the non-authoritative document.
4. Submit the correction for human review.
5. Re-run the failed step after correction to confirm resolution.

### Aggregate re-verification (D-002 enrichment)

After all remediation re-runs have been completed:
1. Review the results of all steps (including re-runs) in aggregate.
2. Confirm that every step now shows PASS.
3. If any step still shows FAIL after remediation, escalate to the human with a summary of unresolved issues.
4. Record the aggregate result: ALL_PASS (all steps pass after remediation) or PARTIAL_PASS (some steps remain FAIL with documented reasons).

Source: **ASSUMPTION: aggregate re-verification step inferred from systematic-workflow-verification principles; no explicit aggregate confirmation step exists in the current governance documents.**

## Records

| Record | Description | Location |
|--------|-------------|----------|
| Governance document versions | Git commit hash or revision date for each of the five governance documents at review time (X-003 enrichment) | TBD (to be determined during WORKING_ITEMS -- recommend recording in the deliverable folder or as part of the coherence assessment artifact) |
| Coherence verification results | PASS/FAIL for each step with notes | TBD (A-004 enrichment: define storage location during WORKING_ITEMS -- recommend `{DELIVERABLE_PATH}/` or a designated records subfolder) |
| Guardrail verification results | PASS/FAIL for each guardrail step | TBD (A-004 enrichment: co-locate with coherence results) |
| Remediation log (if needed) | Discrepancies found and corrections proposed | TBD (A-004 enrichment: co-locate with verification results) |
| Aggregate re-verification result | ALL_PASS or PARTIAL_PASS with summary | TBD (co-locate with other records) |
| Execution date and actor | Who performed the review, their authority level, and when (E-002 enrichment) | TBD |
