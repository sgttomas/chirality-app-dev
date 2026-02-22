# Guidance — DEL-02-02 Portal->Pipeline Navigation & Deliverable Key Semantics

## Purpose

This deliverable exists to ensure that the desktop UI provides a coherent navigation path from the PORTAL matrix to the PIPELINE view, with deliverable-scoped `TASK*` variants correctly pre-selected, and that both views share a single source of deliverables state. This is a core part of OBJ-005 ("Desktop UI supports intended operator workflow").

The operator's primary workflow is: scan deliverables in PORTAL -> select a deliverable -> enter PIPELINE TASK* to operate on it. This navigation must be seamless, and the selection state must be stable, predictable, and resilient to external changes (root switches, fetch failures).

**Source:** Decomposition G7-APPROVED, DEL-02-02 entry; SOW-023; SOW-024; OBJ-005.

---

## Principles

### P1: Single Source of Deliverables State

Deliverables data should be fetched and held at the highest common ancestor of PORTAL and PIPELINE (page-level), not duplicated in each view. This prevents inconsistencies where one view shows stale data while the other has refreshed.

**Source:** `docs/PLAN.md` Section 2 ("Shared deliverables state at page-level (page.tsx)")

### P2: Composite Key as the Canonical Selection Token

The `pkg::id` composite key is the canonical format for identifying a deliverable in UI state. The `pkg` segment uses the package folder label (e.g., `PKG-02_Desktop_UI_Workflow`), providing uniqueness across packages and enough context for both display and API resolution.

**TBD: The exact key construction rule (whether `pkg` is the folder label or the bare PackageID) has not been definitively confirmed via an explicit rule in the governance docs.** Both example keys observed in governance docs use the folder label form. See Datasheet > Attributes > Deliverable Key -- `pkg` Segment.

**Source:** `docs/PLAN.md` Section 2 ("pkg::id composite keys"); `docs/SPEC.md` Section 15.1

### P3: Defensive State Management

UI state must be resilient to changes that occur outside the UI: the user switching working roots, external filesystem changes that remove deliverables, or API failures. Stale keys must be cleared proactively rather than left to cause downstream errors.

**Source:** `docs/SPEC.md` Section 14.5 (Stale Selection Reset Rules)

### P4: Explicit UX Feedback for Transient States

Loading, empty, and error states must be explicit (not silent or hidden). An operator should never face a blank selector with no indication of what is happening. API error responses must be distinguished from loading and empty states to provide actionable feedback.

**Source:** `docs/PLAN.md` Section 2 ("selector shows explicit loading and empty states"); error state distinction is **ASSUMPTION** — see REQ-03 note.

### P5: Disabled Options Are Visible, Not Hidden

Unsupported variants must remain visible as disabled entries so operators know the feature exists but is not yet available. Silent omission creates confusion about feature completeness.

**Source:** `docs/SPEC.md` Section 14.4

### P6: Canonical Vocabulary Alignment

All UI navigation terms (MatrixRow, MatrixColumn, PipelineCategory, TaskScopeMode, and related identifiers) should use the canonical vocabulary defined in `docs/TYPES.md` Section 9. Consistent capitalization and phrasing prevents terminology drift across components.

**Normalization note:** The preferred capitalization convention is title case for pipeline categories and matrix constructs (e.g., "TASK* Pipeline Category", "PORTAL Matrix Routing", "OPERATIVE row") as anchored in `docs/TYPES.md` Section 9. Where documents previously used inconsistent casing (e.g., lowercase "TASK* pipeline category"), this has been normalized.

**Source:** `docs/TYPES.md` Section 9

---

## Considerations

### C1: Navigation Routing Architecture

The PORTAL matrix uses a 3x4 grid where the OPERATIVE row routes to PIPELINE. When a specific deliverable row is clicked, the PORTAL must encode the target deliverable's composite key and pass it to the PIPELINE view so that TASK* can pre-select it. This likely involves URL query parameters, shared React state, or a combination.

**ASSUMPTION: The exact state transfer mechanism (URL params vs. React context vs. other) is an implementation choice not specified in governance docs. Any approach is acceptable provided the selection is deterministic and survives view transitions.**

**Clarification (from semantic lensing A-001):** While the mechanism is an implementation choice, downstream deliverables within PKG-02 that interact with the same navigation state should adopt a consistent approach. If this deliverable establishes a mechanism (e.g., URL params), that choice should be documented in the Records section so that DEL-02-03 and DEL-02-04 can coordinate. The mechanism choice, once made, should be treated as a de facto constraint for the package unless explicitly revisited.

### C2: API Data Flow

The deliverables list is served by `/api/project/deliverables` (`docs/SPEC.md` Section 15). The page-level state should call this API once and distribute results to both views. Consider caching/memoization to avoid redundant calls during navigation transitions.

**Note:** The UI must also handle API error responses distinctly from loading/empty states (see REQ-03 and P4). Error recovery strategy (e.g., automatic retry, manual retry button) is TBD.

### C3: Knowledge-Type Scope Gating

Knowledge-type scope mode depends on a knowledge decomposition marker being present in `_Decomposition`. The API response includes `knowledgeDecomposition.enabled` flag (`docs/SPEC.md` Section 15.2). When this is `false`, the KNOWLEDGE_TYPES scope mode selector should be hidden or disabled. This deliverable should ensure the gating logic is correct but need not implement deep knowledge-type pipeline behavior.

### C4: Relationship to Other PKG-02 Deliverables

- **DEL-02-01 (FileTree Refresh):** The FileTree refresh mechanism may trigger deliverable re-scans that affect shared state. This deliverable should handle state updates gracefully but does not own the refresh logic. **Note:** A cross-deliverable integration verification is warranted to confirm that DEL-02-01 refresh triggers correctly propagate to DEL-02-02 shared deliverables state (see Specification Verification > Cross-DEL row).
- **DEL-02-03 (Operator Toolkit Panel):** Toolkit panel is orthogonal to navigation but exists in the same layout. No direct dependency.
- **DEL-02-04 (Multi-pane Layout):** Layout mechanics (resizable panes) surround the PORTAL/PIPELINE views. Navigation logic should not depend on pane sizes or collapse states.

### C5: Knowledge-Type Scope Boundary

The Specification Excluded section notes that "deep knowledge-type pipeline logic may belong to a separate deliverable or future scope" (**ASSUMPTION**). This boundary should be understood as follows: DEL-02-02 is responsible for (a) correctly forming composite keys that include knowledge-type context when applicable, (b) clearing stale keys when knowledge-type conditions change (REQ-06 triggers 4-5), and (c) gating the KNOWLEDGE_TYPES scope mode (REQ-09). It is NOT responsible for implementing the knowledge-type pipeline execution workflow itself. If scope questions arise during implementation, prefer narrower scope (key formation + gating + stale clearing only) and defer pipeline execution to a future deliverable.

**Source:** Decomposition G7-APPROVED, DEL-02-02 entry ("Implement/verify deliverable-scoped navigation and shared state semantics"); Specification Excluded section.

### C6: PORTAL Matrix Design Rationale

The PORTAL matrix uses a 3x4 grid with rows NORMATIVE, OPERATIVE, EVALUATIVE and the OPERATIVE row specifically as the navigation trigger to PIPELINE. TBD — the rationale for why OPERATIVE (rather than another row) serves as the navigation trigger row is not documented in accessible governance sources. Understanding this intent would help implementers extend the matrix correctly if the design evolves.

**Source:** `docs/PLAN.md` Section 2 — **location TBD** for matrix design rationale.

---

## Trade-offs

### T1: Page-Level State vs. Global Store

**Option A:** Maintain deliverables state in a global store (e.g., Zustand, Redux).
**Option B:** Maintain deliverables state at page-level via React props/context.

The governance docs specify "page-level (`page.tsx`)" (`docs/PLAN.md` Section 2), suggesting Option B. This keeps the state co-located with the views that consume it and avoids introducing global store complexity for what is a view-scoped concern.

**Trade-off:** Page-level state may require more explicit prop drilling, but avoids the overhead and indirection of a global store for a bounded concern.

### T2: Eager vs. Lazy Deliverables Fetch

**Option A:** Fetch deliverables eagerly on page mount.
**Option B:** Fetch lazily on first PORTAL or PIPELINE interaction.

Eager fetch (Option A) ensures both views have data ready and avoids flash-of-empty-content on navigation. The cost is a single API call at page load.

**ASSUMPTION: Eager fetch is the intended behavior given the shared state design, but this is an implementation judgment call.**

### T3: Concurrent Navigation Handling Strategy

**Option A:** Latest-click-wins (cancel any in-flight navigation transition and adopt the newest selection).
**Option B:** Debounce (delay navigation until clicks settle).
**Option C:** Queue-and-process (process clicks in order).

TBD — no governance doc specifies behavior for rapid-succession clicks. Option A (latest-click-wins) is the most common UX pattern for navigation and is the recommended starting point, but the choice should be confirmed during implementation.

**ASSUMPTION: Some form of race condition mitigation is needed.**

---

## Examples

### Example Navigation Flow

1. Operator opens the PORTAL view and sees the 3x4 matrix.
2. Operator clicks a cell in the OPERATIVE row (e.g., TASK* under JUDGING column).
3. UI routes to PIPELINE with `TASK*` category selected.
4. Separately, operator clicks a specific deliverable row in PORTAL.
5. UI routes to PIPELINE TASK* with the clicked deliverable's composite key (e.g., `PKG-02_Desktop_UI_Workflow::DEL-02-02`) pre-selected in the scope selector.
6. If the operator then switches the working root, the stale deliverable key is cleared and the selector returns to its default/empty state.

**Source:** `docs/PLAN.md` Section 2 (portal-to-pipeline navigation description)

### Example Composite Key

```
PKG-02_Desktop_UI_Workflow::DEL-02-02
```

Where `PKG-02_Desktop_UI_Workflow` is the package folder label and `DEL-02-02` is the deliverable ID. This format matches the API response `deliverables[].pkg + "::" + deliverables[].id` pattern described in `docs/SPEC.md` Section 15.1.

**Note:** TBD — confirm whether `pkg` is definitively the package folder label or the bare PackageID. See Datasheet > Attributes > Deliverable Key -- `pkg` Segment and Guidance P2.

---

## Conflict Table (for human ruling)

| Conflict ID | Conflict | Source A | Source B | Impacted Sections | Proposed Authority (PROPOSAL) | Human Ruling |
|-------------|----------|----------|----------|-------------------|-------------------------------|-------------|
| CT-001 | Composite key `pkg` segment: folder label (`PKG-02_Desktop_UI_Workflow`) vs. bare PackageID (`PKG-02`). Examples in docs use folder label form but no explicit construction rule has been located. | `docs/PLAN.md` Section 2 (example: `PKG-01_PackageLabel::DEL-01-01`) | `docs/SPEC.md` Section 15.1 (API response field `pkg`) | Datasheet Attributes; Specification REQ-04; Guidance P2; Examples | `docs/PLAN.md` Section 2 | TBD |
