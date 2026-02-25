# Procedure — DEL-02-04: Multi-pane Layout + Theme Hardening

---

## Purpose

This procedure describes the steps to produce and verify the CODE/TEST artifacts for the multi-pane layout and theme hardening deliverable. It covers both implementation workflow and verification activities.

---

## Prerequisites

### Required References

| Reference | Location | Purpose |
|-----------|----------|---------|
| PLAN section 2 | `docs/PLAN.md` | Feature descriptions for layout and theme |
| SPEC section 14 | `docs/SPEC.md` | UI navigation and selector contract |
| DIRECTIVE section 2.5 | `docs/DIRECTIVE.md` | Non-authoritative convenience state rules |
| Decomposition | `execution/_Decomposition/ChiralityApp_SoftwareDecomposition_2026-02-21_G7-APPROVED.md` | Deliverable definition |
| Specification (this deliverable) | `Specification.md` | Normative requirements (REQ-LAYOUT-*, REQ-THEME-*) |
| Datasheet (this deliverable) | `Datasheet.md` | Attribute values and conditions |

### Required Upstream Deliverables

No upstream dependencies have been declared in `_DEPENDENCIES.md` at this time. Dependency extraction is pending.

**ASSUMPTION:** DEL-02-04 may have implicit dependencies on the existing application structure and on shared UI state (DEL-02-02 shared deliverables state). These should be confirmed during dependency extraction.

**Upstream readiness check (lensing item A-004):** Before beginning Phase 2 (layout implementation), confirm that the following implicit upstream components are in a stable state:

- **DEL-02-01 (FileTree):** The FileTree component must exist as a pane target. Verify the component renders and can be hosted in a layout container.
- **DEL-02-02 (Portal-to-Pipeline navigation):** Navigation routing must be functional so that the main content area can host route destinations.
- **DEL-02-03 (Operator Toolkit):** The toolkit sidebar toggle interface must be defined so that layout integration (REQ-LAYOUT-07) can be implemented.

If any of these are not yet available, document the gap and proceed with layout work using stub/placeholder components where necessary.

### Required Tools and Access

| Tool / Resource | Purpose |
|-----------------|---------|
| Source code repository access | Read and modify frontend code |
| Node.js / npm development environment | Build and run the Electron + Next.js application |
| macOS 15+ on Apple Silicon | Target platform for testing (DEC-PLAT-001) |
| Test runner (TBD -- see Conflict Table CT-004) | Execute automated tests; if framework selection is still unresolved, run the manual verification set and log the framework choice as follow-up |

---

## Steps

### Phase 1: Codebase Assessment

**Step 1.1 -- Identify Existing Layout Components**

1. Locate the existing multi-pane layout implementation in the frontend source tree.
2. Identify the current pane configuration (which panes exist, their arrangement, current resize behavior).
3. Document which layout-related features from `Specification.md` already exist and which need implementation.

**Step 1.2 -- Identify Existing Theme Implementation**

1. Locate theme-related files (CSS, styled components, design tokens, theme provider).
2. Identify which theme hardening items from PLAN section 2 are already implemented.
3. Document the current state of light mode and dark mode theming.

**Step 1.3 -- Map Requirements to Code Locations**

1. For each requirement in `Specification.md`, identify the source file(s) that must be created or modified.
2. Record the mapping for use in subsequent steps.

### Phase 2: Layout Implementation

**Step 2.1 -- Implement Resizable Pane Boundaries (REQ-LAYOUT-01, REQ-LAYOUT-02)**

1. Ensure pane boundaries include high-visibility drag handles.
2. Implement or verify pointer-based drag resize behavior.
3. Verify resize operates correctly for all pane boundaries.

**Step 2.2 -- Implement Keyboard Resize (REQ-LAYOUT-03)**

1. Implement keyboard shortcuts for pane resize as an alternative to pointer-based drag.
2. Ensure keyboard resize provides equivalent functionality to pointer drag.
3. TBD: Define specific keyboard shortcuts (e.g., modifier + arrow keys). See Conflict Table CT-002.

**Step 2.3 -- Implement Collapse/Expand (REQ-LAYOUT-04)**

1. Add collapse/expand controls to each resizable pane.
2. Implement collapse behavior: collapsed pane minimizes, space is redistributed.
3. Implement expand behavior: pane restores to previous size or sensible default.

**Step 2.4 -- Enforce Minimum Pane Size (REQ-LAYOUT-05)**

1. Define minimum size constraints for each pane (TBD: specific values -- see Conflict Table CT-003).
2. Prevent resize below minimum during drag and keyboard resize.
3. Prevent collapse from causing adjacent panes to violate minimum size.

**Step 2.5 -- Verify Pane Arrangement (REQ-LAYOUT-06)**

1. Confirm pane arrangement accommodates PORTAL, WORKBENCH, and PIPELINE views.
2. Verify navigation model from SPEC section 14 functions correctly within the layout.

**Step 2.6 -- Toolkit Sidebar Integration (REQ-LAYOUT-07)**

1. Verify the Operator Toolkit sidebar visibility toggle (CONFIG-controlled) operates without breaking pane resize.
2. Test the interaction between sidebar toggle and pane collapse/expand states.

**Step 2.7 -- Layout State Persistence (conditional -- REQ-LAYOUT-08)**

1. If layout state persistence is in scope (Datasheet attribute currently TBD):
   - Implement persistence of pane sizes and collapse/expand states to local storage.
   - Follow DIRECTIVE section 2.5 constraints: non-authoritative convenience state only.
   - Implement reset-to-defaults capability.
2. If persistence is descoped, skip this step.

### Phase 3: Theme Hardening

**Step 3.1 -- Light Mode Accent Text (REQ-THEME-01)**

1. Identify all accent text elements in light mode.
2. Replace orange accent text with a readable alternative color.
3. Verify readability across all UI surfaces.
4. TBD: Apply measurable readability criterion (e.g., contrast ratio) if defined. See Conflict Table CT-008.

**Step 3.2 -- Chat Bubble Styling (REQ-THEME-02)**

1. Implement role-specific low-contrast surfaces for assistant and user chat bubbles.
2. Ensure assistant messages are left-aligned and user messages are right-aligned.
3. Verify visual distinction between roles is clear.

**Step 3.3 -- Markdown Rendering (REQ-THEME-03, REQ-THEME-04)**

1. Implement or verify GitHub-flavored markdown rendering in assistant messages.
2. Ensure support for GFM elements: tables, task lists, strikethrough, fenced code blocks with language-tagged syntax highlighting, autolinks.
3. Implement ANSI fallback rendering for terminal-style tool output blocks.
   - TBD: Define specific ANSI escape sequence scope (see Conflict Table CT-007).
4. Verify markdown and ANSI rendering do not conflict.

**Step 3.4 -- Status Banner Cleanup (REQ-THEME-05)**

1. Remove or suppress top-banner status noise.
2. Implement conditional display: update banner appears only when an update is actually available.
3. Verify no extraneous banners appear during normal operation.

**Step 3.5 -- Header Brand Tile (REQ-THEME-06)**

1. Set the header brand tile to use the macOS app icon asset.
2. Apply rounded-square treatment to the brand tile.
3. Verify visual consistency with macOS design conventions.

**Step 3.6 -- Dark Mode Parity (REQ-THEME-07)**

1. Review dark mode for structural parity with light mode improvements.
2. Ensure chat bubble differentiation, markdown rendering, banner behavior, and brand tile are consistent in dark mode.
3. TBD: Dark mode color values and palette (see Conflict Table CT-011).

### Phase 4: Testing

**Step 4.1 -- Write Layout Tests**

1. Write automated tests for pane resize behavior (pointer drag simulation).
2. Write automated tests for keyboard resize (keyboard event simulation).
3. Write automated tests for collapse/expand behavior.
4. Write automated boundary tests for minimum pane size enforcement.
5. Write automated integration test for toolkit sidebar toggle + pane resize.
6. If layout state persistence is in scope: write automated session persistence test (REQ-LAYOUT-08-V).

**Step 4.2 -- Write Theme Tests**

1. Write visual regression tests (or manual test protocol) for light mode accent text.
2. Write tests for chat bubble role differentiation.
3. Write automated functional tests for GFM markdown rendering (sample inputs covering: tables, task lists, strikethrough, autolinks, fenced code blocks with syntax highlighting).
4. Write automated functional tests for ANSI escape sequence rendering (scope TBD -- see Conflict Table CT-007).
5. Write automated state test for conditional status banner display.
6. Write visual test for header brand tile rendering.

**Step 4.3 -- Write Boundary and Regression Tests (lensing items X-003, X-004)**

1. Write scope exclusion boundary test (EXCL-BOUNDARY-V): confirm that pane-hosted functional views (WORKBENCH, PIPELINE content) are not broken by layout changes.
2. Define and execute adjacent deliverable regression tests (REGRESSION-V) with the following specific scope:
   - **DEL-02-01 (FileTree):** Verify FileTree renders, expands/collapses folders, and responds to external file changes.
   - **DEL-02-02 (Navigation):** Verify Portal-to-Pipeline navigation transitions function correctly within the layout.
   - **DEL-02-03 (Toolkit):** Verify toolkit panel opens, closes, and displays content without layout corruption.
3. Record pass/fail for each regression target.

---

## Verification

| Check | Method | Pass Criteria |
|-------|--------|---------------|
| All REQ-LAYOUT-* requirements met | Run layout test suite + manual verification against Specification.md | All tests pass; all requirements verified per Specification verification table |
| All REQ-THEME-* requirements met | Run theme test suite + visual inspection against Specification.md | All tests pass; all requirements verified per Specification verification table |
| Scope exclusion boundaries hold (EXCL-BOUNDARY-V) | Automated smoke test of pane-hosted views | WORKBENCH, PIPELINE content not broken by layout changes (lensing item X-003) |
| No regressions in adjacent deliverables (REGRESSION-V) | Manual smoke test with defined scope (see Step 4.3) | DEL-02-01 FileTree, DEL-02-02 navigation, DEL-02-03 toolkit features function as before; specific test cases pass (lensing item X-004) |
| Cross-document consistency | Compare Datasheet attribute values against implemented values | Implemented values match Datasheet |
| Layout state persistence (conditional) | Automated session persistence test (REQ-LAYOUT-08-V) | Layout state persists across restart, if persistence is in scope |

---

## Records

| Record | Format | Location | Description |
|--------|--------|----------|-------------|
| Test results -- layout | Test runner output | TBD (see Conflict Table CT-010) | Automated test results for layout requirements |
| Test results -- theme | Test runner output + screenshots | TBD (see Conflict Table CT-010) | Automated and visual test results for theme requirements |
| Implementation commit(s) | Git commit(s) | Source repository | Code changes implementing layout and theme requirements |
| Verification evidence | Markdown summary or screenshots | TBD (see Conflict Table CT-010) | Evidence that all verification criteria passed |
| Regression test results | Markdown summary | TBD (see Conflict Table CT-010) | Pass/fail results for scope exclusion and adjacent deliverable regression tests |
