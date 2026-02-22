# Guidance — DEL-02-04: Multi-pane Layout + Theme Hardening

---

## Purpose

This deliverable exists to ensure the Chirality desktop application provides an ergonomic, professional-grade multi-pane workspace with consistent theme behavior. The multi-pane layout and theme hardening collectively support **OBJ-005** (Desktop UI supports intended operator workflow) by enabling operators to efficiently navigate between views, resize workspace regions, and work comfortably across extended sessions.

**Source:** Decomposition DEL-02-04 entry; PLAN section 2; SOW-026, SOW-027.

**Open item -- Measurable ergonomics targets:** The phrase "ergonomic, professional-grade multi-pane workspace" currently lacks measurable criteria beyond functional pass/fail. Consider defining targets such as resize latency, layout switch speed, or session comfort benchmarks to evaluate whether the objective is achieved in practice (lensing item D-002). These targets are TBD.

---

## Principles

### P1: Layout Serves the Operator's Context-Switching Needs

The multi-pane layout is the spatial container for the navigation model (PORTAL matrix, WORKBENCH, PIPELINE). Layout decisions should optimize for the operator's primary workflow: selecting a work mode, working within it, and occasionally referencing adjacent information (FileTree, toolkit sidebar) without losing context.

**Source:** PLAN section 2 (contextual); SPEC section 14 (navigation contract).

### P2: Theme Hardening is Readability and Scanability

Theme hardening is not aesthetic polish -- it directly affects operator efficiency. Role-differentiated chat bubbles, readable accent text, and clean markdown rendering reduce cognitive load. The changes described in PLAN section 2 are functional improvements to information density and scan speed.

**Source:** PLAN section 2 (theme hardening items).

### P3: Convenience State, Not Project Truth

Pane positions, collapse states, and toolkit sidebar visibility are non-authoritative convenience state per DIRECTIVE section 2.5. They MAY be persisted in local storage for operator comfort but MUST NOT be treated as project truth and MUST NOT be stored in project files.

**Source:** DIRECTIVE section 2.5 ("Non-authoritative operator convenience state... MAY be stored outside project files").

### P4: Platform-Specific Design Decisions

The target platform is macOS 15+ on Apple Silicon only (DEC-PLAT-001). Layout and theme implementation can leverage macOS-specific behaviors (e.g., native window chrome, system-level dark mode detection) without cross-platform abstraction overhead.

**Source:** Decomposition DEC-PLAT-001.

---

## Considerations

### C1: Pane Configuration

PLAN section 2 describes "resizable multi-pane layout improvements" but does not specify the pane count, orientation, or nesting. The existing application structure (PLAN section 2: FileTree, PORTAL/WORKBENCH/PIPELINE views, ChatPanel, Operator Toolkit) suggests a configuration with at minimum:

- A navigation/file tree pane (left)
- A main content area (center -- hosting WORKBENCH or PIPELINE views)
- A chat/interaction pane (right or bottom)
- The optional toolkit sidebar

The exact configuration is TBD and should be determined by examining the existing codebase layout.

### C2: Drag Handle Visibility vs. Visual Noise

"High-visibility drag handles" must balance discoverability with visual quietness. The handles should be visible enough for first-time users to discover resize capability, but not so prominent that they distract from content during normal operation. Consider hover-activated prominence or subtle persistent indicators.

### C3: Keyboard Resize Accessibility

Keyboard resize support serves both accessibility needs and power-user efficiency. The implementation should use standard keyboard conventions (e.g., arrow keys with a modifier) and support the same operations available via pointer drag. Screen reader announcements for pane size changes should be considered if WCAG 2.1 AA compliance is confirmed as applicable (see Conflict Table CT-001).

### C4: Collapse/Expand Behavior

Collapsed panes should free their space for adjacent panes. On expand, panes should restore to their previous size (or a sensible default if no previous size is known). Consider whether collapse/expand should animate or be instant -- animation aids spatial understanding but must not delay interaction.

### C5: Theme Mode Coverage

PLAN section 2 explicitly describes light mode improvements. Dark mode behavior is not explicitly documented. Dark mode should at minimum maintain the same structural improvements (role-differentiated bubbles, markdown rendering, banner behavior, brand tile) even if dark mode color values themselves require separate specification.

**Open item:** The distinction between SHOULD (REQ-THEME-07) and what sounds like a necessity in this consideration creates ambiguity. If dark mode structural parity is a genuine quality prerequisite, REQ-THEME-07 should be elevated to MUST with specific acceptance criteria. If it is an aspirational target, the SHOULD is appropriate but should be documented as such. See Conflict Table CT-006 (lensing item F-003).

### C6: Markdown Rendering Scope

"GitHub-flavored markdown in-chat" implies support for GFM extensions: tables, task lists, strikethrough, autolinks, and fenced code blocks with language-tagged syntax highlighting. The rendering library choice should support these features. ANSI fallback for tool output is a separate concern -- tool output blocks may contain ANSI escape sequences that should be rendered as colored/styled terminal output rather than as markdown.

**Note:** Specification REQ-THEME-03 has been enriched with an explicit GFM element enumeration derived from this consideration (lensing item E-002).

### C7: Interaction with Other PKG-02 Deliverables

This deliverable shares UI surface area with DEL-02-01 (FileTree), DEL-02-02 (Portal-to-Pipeline navigation), and DEL-02-03 (Operator Toolkit panel). Layout changes here must not break behaviors owned by those deliverables. Coordinate interface boundaries carefully:

- FileTree pane is a layout container managed here; FileTree refresh logic is DEL-02-01 scope.
- Navigation routing is DEL-02-02 scope; layout provides the container for route destinations.
- Toolkit sidebar layout integration is in scope here; toolkit content and behavior is DEL-02-03 scope.

**Note:** Specification now includes EXCL-BOUNDARY-V (scope exclusion boundary verification) and REGRESSION-V (adjacent deliverable regression test with defined scope) to verify these boundaries (lensing items X-003, X-004).

### C8: REQ-LAYOUT-05 -- SHOULD vs. MUST Rationale

REQ-LAYOUT-05 (minimum pane size constraints) uses SHOULD while all other layout requirements use MUST. The rationale for this distinction is not documented in available sources. Possible justifications include:

- Some content panes may legitimately need to be reduced below a "minimum usable" threshold during extreme resize operations.
- The minimum size itself is TBD and may vary by pane type; enforcing a hard MUST before values are defined could over-constrain the implementation.

The human/design authority should confirm whether SHOULD is the correct strength or whether MUST with defined minimum values is required. See Conflict Table CT-005 (lensing item A-005).

### C9: Upstream Dependency Awareness

No upstream dependencies have been declared in `_DEPENDENCIES.md` (extraction pending). However, this deliverable likely has implicit dependencies on:

- DEL-02-01 (FileTree) -- the FileTree component exists as a layout pane target.
- DEL-02-02 (Portal-to-Pipeline navigation) -- navigation routing determines what content fills the main content area.
- DEL-02-03 (Operator Toolkit) -- the toolkit sidebar toggle integrates with pane layout.

The Procedure includes a prerequisite note about this (lensing item A-004). Implementers should confirm that shared UI state and component interfaces are stable before beginning layout modifications.

---

## Trade-offs

### T1: Pane Persistence vs. Simplicity

Persisting pane layout state (sizes, collapsed/expanded) across sessions improves operator comfort but adds complexity (local storage schema, migration, reset-to-defaults). Given DIRECTIVE section 2.5 permits non-authoritative convenience state in local storage, persistence is likely worthwhile but should be implemented simply (flat JSON in localStorage, no versioning burden).

### T2: CSS-native Layout vs. Library-based Layout

CSS Grid and Flexbox can support resizable layouts natively (with JavaScript for drag interaction), while libraries like `react-resizable-panels` provide pre-built resize behavior with drag handles and keyboard support. A library reduces implementation risk for the resize/collapse/keyboard requirements but adds a dependency. The trade-off should be evaluated against the existing codebase's dependency posture.

### T3: Markdown Rendering Library

GitHub-flavored markdown can be rendered via several React-compatible libraries (e.g., `react-markdown` with `remark-gfm`, or a pre-built chat component). The choice should prioritize: GFM compliance, code block syntax highlighting, ANSI rendering compatibility (or a separate renderer for tool output), and bundle size.

---

## Examples

### Example: Pane Layout Configuration (Conceptual)

Based on the application structure described in PLAN section 2, a representative pane layout might be:

```
+------------------+-----------------------------+------------------+
| FileTree         | Main Content Area           | ChatPanel        |
| (collapsible)    | (WORKBENCH or PIPELINE)     | (collapsible)    |
|                  |                             |                  |
|                  |                             |                  |
+--drag-handle-----+------drag-handle-----------+--drag-handle-----+
                                                 | Toolkit Sidebar  |
                                                 | (toggle from     |
                                                 |  CONFIG)         |
                                                 +------------------+
```

**Note:** This is illustrative only. The actual pane arrangement is TBD and must be determined from the existing codebase and operator workflow analysis.

### Example: Chat Bubble Role Differentiation (from PLAN section 2)

```
[Left-aligned, low-contrast surface A]      <- Assistant message
                                               (GFM markdown rendered)

        [Right-aligned, low-contrast surface B] <- User message
```

---

## Conflict Table (for human ruling)

| ConflictID | Conflict | Source A | Source B | Impacted Sections | Proposed Authority (PROPOSAL) | Human Ruling |
|------------|----------|----------|----------|-------------------|-------------------------------|--------------|
| CT-001 | WCAG 2.1 AA applicability undetermined -- blocks accessibility requirements derivation (contrast ratios, keyboard announcements, screen reader support) | Specification Standards table (ASSUMPTION: likely applicable) | No explicit governance ruling in available sources | Specification: Standards, REQ-THEME-01, REQ-LAYOUT-03; Datasheet: Conditions (Accessibility); Procedure: Phase 2, Phase 3 | Human / project governance (lensing items A-001, A-003) | TBD |
| CT-002 | Keyboard shortcut conventions for pane resize are unspecified -- REQ-LAYOUT-03 mandates keyboard resize but no shortcuts are defined | Specification REQ-LAYOUT-03 | Datasheet Attributes (Keyboard shortcut conventions: TBD); Procedure Step 2.2 | Specification: REQ-LAYOUT-03; Datasheet: Attributes; Procedure: Step 2.2 | Human / UX design (lensing item A-002) | TBD |
| CT-003 | Core layout data values unresolved -- pane configuration, minimum dimensions, default proportions, and persistence approach are all TBD | Datasheet Attributes (4 TBD entries for layout) | No source provides these values | Datasheet: Attributes (SOW-026); Specification: REQ-LAYOUT-05, REQ-LAYOUT-06; Procedure: Steps 2.1-2.4 | Human / codebase analysis (lensing item B-001) | TBD |
| CT-004 | Construction technology decisions unresolved -- CSS approach, layout mechanism, component library, and test framework are all TBD | Datasheet Construction (4 TBD entries) | No source provides these values | Datasheet: Construction; Procedure: Prerequisites (test runner); all implementation steps | Human / technical lead (lensing items B-002, C-002) | TBD |
| CT-005 | REQ-LAYOUT-05 uses SHOULD while all other layout requirements use MUST; no rationale for the distinction | Specification REQ-LAYOUT-05 (SHOULD) | Specification REQ-LAYOUT-01 through 04, 06, 07 (all MUST) | Specification: REQ-LAYOUT-05; Guidance: C8 | Human / design authority (lensing item A-005) | TBD |
| CT-006 | Dark mode parity strength ambiguous -- REQ-THEME-07 uses SHOULD but Guidance C5 implies necessity ("should at minimum maintain the same structural improvements") | Specification REQ-THEME-07 (SHOULD, ASSUMPTION) | Guidance C5 (implies stronger necessity) | Specification: REQ-THEME-07; Guidance: C5; Datasheet: dark mode color values (TBD) | Human / design authority (lensing item F-003) | TBD |
| CT-007 | ANSI escape sequence scope undefined -- REQ-THEME-04 requires ANSI fallback but does not define which sequences must be supported or fallback behavior for unsupported sequences | Specification REQ-THEME-04 | No source defines ANSI scope | Specification: REQ-THEME-04; Datasheet: ANSI escape sequence scope (TBD); Procedure: Step 3.3 | Human / technical lead (lensing item E-001) | TBD |
| CT-008 | No measurable readability criterion for REQ-THEME-01 -- "readability" is subjective without a contrast ratio or equivalent metric | Specification REQ-THEME-01 ("non-orange accent text for readability") | REQ-THEME-01-V ("text is readable" -- no metric) | Specification: REQ-THEME-01, REQ-THEME-01-V; Datasheet: Light mode readability metric (TBD) | Human / design authority + accessibility lead (lensing item E-003) | TBD |
| CT-009 | ASSUMPTION-tagged requirements and standards require governance resolution -- REQ-LAYOUT-05, REQ-THEME-07, and WCAG 2.1 AA are all tagged as ASSUMPTIONs | Specification: REQ-LAYOUT-05, REQ-THEME-07, Standards WCAG row | No governance ruling in available sources | Specification: Requirements, Standards | Human / project governance (lensing item F-001) | TBD |
| CT-010 | Record output locations undefined -- Procedure Records table has three TBD location entries | Procedure Records table (3 TBD locations) | No project convention specified | Procedure: Records | Human / project conventions (lensing item F-002) | TBD |
| CT-011 | Dark mode color values and palette absent -- needed for REQ-THEME-07 implementation if dark mode parity is in scope | Datasheet: dark mode color values (TBD) | No design token source or palette in available sources | Datasheet: Attributes (SOW-027); Specification: REQ-THEME-07; Procedure: Step 3.6 | Human / design authority (lensing item B-003) | TBD |
