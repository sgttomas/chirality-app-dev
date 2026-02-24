# Development History Analysis: Chirality App Dev

## Context

This analysis examines the development path of the Chirality App Dev project — a SOFTWARE_DECOMP instance that is simultaneously the framework template and its first execution. The analysis snapshot was taken at 194 commits over ~4 days (Feb 21–24, 2026) by a single author, taking 8 packages and 36 deliverables from initial decomposition to 31 active deliverables at `ISSUED` plus 5 optional deliverables at `RETIRED` (SCA-002 disposition).

**Post-analysis update:** The full-graph SCC has been resolved (1→0 SCCs, 21 reorientations) by treating interface links as one-way authority/flow contracts. All 36 `Dependencies.csv` files validate with 0 errors (non-blocking warnings remain on a subset of files).

---

## 1. Timeline Reconstruction

| Phase | Dates | Commits | Character |
|-------|-------|---------|-----------|
| Foundation | Feb 21 (4 commits) | Scaffolding | Agent framework, governance suite, decomposition approval, execution workspace |
| Feature Build | Feb 22 (46 commits) | Steady build-out | Frontend bootstrap, harness API, working-root contracts, lifecycle wiring |
| Intensive Validation | Feb 23 (122 commits) | Peak intensity | 35+ passes on provider coverage, attachment/toolkit hardening, governance assessments |
| Closure & Issuance | Feb 24 (22 commits) | Wrap-up | Mass lifecycle advancement, scope resolution (SCA-002), SCC reduction→elimination |

*Note:* Two additional documentation/scope commits were added after this analysis snapshot (current repo total: 196 commits; Feb 24 count now 24).

---

## 2. What Went Well

### Structural Fidelity
High alignment between planned decomposition and execution after controlled scope amendments. 8 packages remained stable, all 31 active deliverables reached `ISSUED`, and 5 optional deliverables were explicitly retired via SCA-002 rather than silently abandoned. The decomposition held as a reliable execution framework.

### Governance Quality → Low Bug Rate
The uniform documentation kit (4-doc suite + semantic analysis per deliverable) enabled effective discretization of work into bounded loops. **Result (operator-observed): very few bugs throughout the entire process; most tests passed first time.** The governance overhead paid for itself in execution quality.

### Formal Approval Trail
The 50% of commits categorized as "meta-work" are **intentional formal approval records** (operator characterization) — they capture human-reviewed approval/state transitions rather than automated-only state. This creates an auditable chain of human decisions, which is the governance model's core value proposition.

### Scope Change Management
Both SCA-001 and SCA-002 were handled through the formal SCOPE_CHANGE agent. The agent performed well — the amendments were clean, traceable, and didn't disrupt ongoing work beyond a necessary gating rule.

### Dependency Resolution
The blocker-subset/full-graph separation was the correct abstraction. Execution was never blocked by dependency cycles. The final SCC resolution (reorienting 21 non-hard-blocker edges to one-way authority/flow semantics) was a perspective shift, not a data correction — the underlying relationships were accurately captured; it was the *directionality* that needed clarification.

---

## 3. Where the Path Was Suboptimal

### 3.1 Decomposition Completeness

**SCA-001 (day 2):** Missing the frontend baseline entirely was the most impactful gap. The decomposition was intentionally not reviewed by the human author before approval (as an experiment in communicating intent upfront), and this particular omission would have been caught in review.

**SCA-002 (day 4):** Retiring 5 of 7 PKG-08 deliverables meant documentation was prepared for work that was never executed.

**Lesson:** An explicit pre-approval checklist ("Does this cover UI? Backend? Testing? Tooling?") would catch category-level omissions without requiring full document review.

### 3.2 Token Efficiency — The Real Overhead Metric

The commit-level overhead (50% meta-work) understates the actual cost because commits are cheap. The real metric is **token consumption**: approximately **75% of tokens went to context loading, documentation updates, coordination state, and audit runs. Only ~25% were "productive" (feature code, tests, specifications)** (operator-observed estimate from live token/context tracking during execution).

This 75/25 split has three components:
1. **Upfront context** — loading NEXT_INSTANCE_STATE, deliverable docs, governance docs into each session
2. **After-the-fact documentation** — updating _STATUS.md, MEMORY.md, NEXT_INSTANCE_STATE after each pass
3. **Audit/reconciliation runs** — closure analysis, interface reconciliation, dependency validation

**Open question:** Is 50/50 even achievable? The context loading is structural (agents need context to operate correctly). The documentation updates are what enable bounded loops and low bug rates. Reducing either risks quality. A realistic improvement target might be **60/40 overhead-to-productive** rather than 50/50, achievable by:
- Reducing per-pass handoff granularity (batch updates at tier boundaries instead of per-pass)
- Compressing context loading (smaller, more targeted state documents)
- Running audits less frequently (every N passes instead of every pass)

### 3.3 Pass Iteration Depth — The Core Process Gap

**This is the most actionable finding and the one the project owner specifically flagged for deeper analysis.**

DEL-03-05 underwent 35 passes. Passes 1–4 implemented core SDK integration. Passes 5–35 were **pure test coverage expansion** (image MIME subtypes) with no changes to production code. The human was manually triggering each pass continuation but the agent provided no signal that returns were diminishing.

#### Root Cause Analysis

The pass loop has **no built-in saturation detection**. The relevant instruction chain:

| Component | File | What It Does | What's Missing |
|-----------|------|-------------|----------------|
| TASK agent | `agents/AGENT_TASK.md` (Step 7) | 7-step PROTOCOL: read context → execute → QA → return | No "compare this pass to prior passes" logic |
| WORKING_ITEMS | `agents/AGENT_WORKING_ITEMS.md` (Phase 5 wrap-up) | Frame objective → define completion criteria → execute → wrap up | Completion criteria are human-defined but **open-ended by default** |
| Control loop | `execution/_Coordination/NEXT_INSTANCE_PROMPT.md` (tier loop sequence) | 6-step tier loop: scan → work → refresh → reconcile → audit → publish | No saturation check step |

**The only termination signal is explicit human intervention.** The human must:
1. Notice the pattern (reviewing MEMORY.md pass history)
2. Decide it's saturated (subjective judgment)
3. Issue a ruling (formal coverage-saturation freeze)

This happened at PASS35. With a built-in signal, it could have happened at PASS8–10.

#### Resolution: Specification-Anchored Completion Check

The real problem isn't a missing heuristic — it's that the agent **kept finding elective work beyond what the Specification required** without checking back against acceptance criteria. The 4-document kit already defines "done." The fix is enforcing that check at the handover boundary.

**The actual session loop (human-operated):**
```
until work is complete, do:
  --- session start ---
  Read README.md + AGENTS.md (framework context)
  Load NEXT_INSTANCE_PROMPT.md (stable control plane)
  Load NEXT_INSTANCE_STATE.md (mutable state/pointers)
  Proceed with work
  --- session end ---
  Commit + push + complete handover procedure
  (If compaction: finish current task, commit + push, handover)
  /new
```

Each loop iteration is a new Claude session. The "pass" is one session's work on a deliverable. The saturation check belongs at the **handover boundary** — when the session writes NEXT_INSTANCE_STATE.md for the next session.

**The check (now implemented in the agent instruction chain):**

At handover time, before queuing the next pass on the same deliverable:

1. **Specification verification**: Read the deliverable's Specification.md. For each requirement (REQ-\*), assess: is it met, partially met, or not started? If all REQs are met → deliverable is **spec-complete**.

2. **Elective work gate**: If the deliverable is spec-complete but the agent has identified additional work (coverage expansion, hardening, edge cases beyond spec), that work is **elective**. Elective work must be explicitly noted in the handover state:
   ```
   DEL-03-05: SPEC-COMPLETE. Elective work identified: [image-subtype boundary expansion].
   Next pass requires explicit human authorization to continue elective scope.
   ```

3. **Default shifts**: Once a deliverable is spec-complete:
   - Default action changes from "continue with next pass" to "advance lifecycle (CHECKING → ISSUED)"
   - Continuing with elective passes requires the human to override the default
   - The handover explicitly presents: "All REQs met. Advance to ISSUED? Or authorize elective PASS N+1?"

**Where this was implemented:**

| Component | Change | File |
|-----------|--------|------|
| TASK agent Step 7 | Added: REQ coverage assessment — report which REQs are MET/PARTIAL/NOT_STARTED, declare SPEC-COMPLETE when all are met | `agents/AGENT_TASK.md` |
| WORKING_ITEMS Phase 5 | Added: spec-completion assessment (new step 5) before session handoff (now step 6) — gates elective work, shifts default to lifecycle advancement when spec-complete | `agents/AGENT_WORKING_ITEMS.md` |
| Handover state format | Added: SPEC_STATUS annotation format (`SPEC-COMPLETE` / `PARTIAL (REQ-04, REQ-07 open)`) for Active Front entries | `execution/_Coordination/NEXT_INSTANCE_STATE.md` |

**Why this is better than a raw heuristic:**
- Anchored to the deliverable's own acceptance criteria (Specification.md), not arbitrary thresholds
- The 4-document kit already exists and is populated before execution begins — no new artifacts needed
- Distinguishes "meeting the spec" from "going beyond the spec" — the former is mandatory, the latter is a conscious choice
- Would have caught DEL-03-05 by PASS4 (when all 10 REQs were met) rather than PASS35

**Impact estimate:** Would have saved ~31 passes on DEL-03-05 (~89% of its total passes). At the token cost of a full pass (context load + execution + documentation + handoff), this is the single largest efficiency improvement available.

---

## 4. Efficiency Assessment

### Commit-Level View (Intentional but Misleading as Efficiency Metric)

| Category | Commits | % | Notes |
|----------|---------|---|-------|
| Formal approvals (docs/coordination) | ~96 | 49.5% | Intentional audit trail (operator-characterized human-reviewed approvals) |
| Feature work (feat/harness/frontend) | ~41 | 21.1% | Core implementation |
| Blended (tier/pass tracking) | ~57 | 29.4% | Mix of work and coordination |

### Token-Level View (The Real Metric)

| Category | Estimated % | Reducible? |
|----------|-------------|------------|
| Context loading (session startup) | ~25% | Partially — smaller state documents, targeted loading |
| Documentation updates (per-pass) | ~25% | Partially — batch at tier boundaries, not per-pass |
| Audit/reconciliation | ~25% | Yes — run every N passes, not every pass |
| Productive work (code, tests, specs) | ~25% | This is the payload; want to maximize |

### Quality Outcome
Despite the 75/25 token split, the quality outcome was excellent:
- Very few bugs throughout the process
- Most tests passed first time
- All 31 deliverables reached ISSUED without rework loops
- The governance framework held — no deliverable was abandoned or required restart

**This suggests the overhead is not waste — it's the cost of the governance that produces the quality.** The question is whether the same quality could be maintained with less overhead (the 60/40 target).

---

## 5. Summary: Path Optimality

### Was the path optimal?

**For a first instance: no, but close.** The primary inefficiencies were:

1. **Decomposition gap (SCA-001)** — avoidable with a category-level pre-approval checklist
2. **Unbounded pass iterations** — the process gap with highest token impact; now addressed with specification-anchored completion check
3. **Per-pass coordination granularity** — could batch documentation updates at tier boundaries

### What worked and should be preserved:

1. **Uniform documentation** — enables discretization, bounded loops, and low bug rates
2. **Formal approval commits** — intentional audit trail, not overhead
3. **Blocker-subset/full-graph separation** — correct abstraction for execution vs. audit
4. **SCOPE_CHANGE agent** — handled amendments cleanly despite the initial gaps

### Concrete improvements implemented for next instance:

**Priority 1 — Specification-anchored completion check:** At the handover boundary, the TASK agent now reports REQ coverage (MET/PARTIAL/NOT_STARTED) and WORKING_ITEMS assesses spec-completion before queuing the next pass. Once spec-complete, default shifts to "advance lifecycle" and elective work requires explicit human authorization. Changes applied to `AGENT_TASK.md` (Step 7), `AGENT_WORKING_ITEMS.md` (Phase 5), and the `NEXT_INSTANCE_STATE.md` format. This is the highest-ROI change — would have caught DEL-03-05 by PASS4 instead of PASS35, saving ~89% of that deliverable's passes.

**Priority 2 — Pre-approval decomposition checklist:** Added category-level coverage check to `AGENT_DECOMP_BASE.md` Phase 6 — the decomposition agent now presents a domain-specific work-category checklist (UI/Frontend, Backend/API, Testing/Validation, Tooling/Build, Security/Auth, Documentation, Deployment/Ops for SOFTWARE_DECOMP) and flags uncovered categories for human decision. Would have caught the SCA-001 frontend omission at Gate 6.

---

## Appendix: Analysis Methodology

This analysis was conducted in a single session using five parallel research tracks:

1. **Git commit history exploration** — full `git log` analysis (194-commit snapshot), temporal distribution, commit message taxonomy, phase identification
2. **Deliverable folder structure exploration** — filesystem scan of all 36 deliverable folders, cross-referenced against approved decomposition document, status verification
3. **Coordination and governance exploration** — read control-plane documents (NEXT_INSTANCE_PROMPT, NEXT_INSTANCE_STATE), governance suite (DIRECTIVE, CONTRACT, SPEC, TYPES, PLAN), dependency audit artifacts
4. **Iteration pattern and overhead analysis** — tier control loop reports, pass-by-pass MEMORY.md examination (focused on DEL-03-05's 35-pass pattern), handoff overhead quantification
5. **TASK agent pass loop mechanics** — deep read of AGENT_TASK.md, AGENT_WORKING_ITEMS.md, and NEXT_INSTANCE_PROMPT.md to identify where saturation signals could be inserted

The initial analysis identified five inefficiencies. Through iterative discussion with the project owner, three were revised:
- Meta-work commits reframed as intentional formal approvals (the real metric is the 75/25 token split)
- Uniform documentation depth preserved — the project owner confirmed it enables discretization and low bug rates
- Dependency cycles removed from critique — the owner had already resolved them (1→0 SCCs) and the resolution was a perspective shift, not a data correction

The remaining two (decomposition gaps and pass iteration depth) were confirmed as genuine, and both have been addressed with concrete changes to the agent instruction chain.
