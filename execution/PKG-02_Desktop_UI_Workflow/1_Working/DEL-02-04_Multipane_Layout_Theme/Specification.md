# Specification — DEL-02-04: Multi-pane Layout + Theme Hardening

---

## Scope

### Included

This deliverable covers the implementation and verification of:

1. **Resizable multi-pane layout behavior** (SOW-026): drag handles, keyboard resize support, and collapse/expand affordances for the Chirality desktop application's multi-pane UI.
2. **Theme/UX hardening** (SOW-027): visual and interaction quality improvements described in PLAN section 2, including light mode readability, chat bubble role differentiation, markdown rendering in chat, status banner cleanup, and header branding.

### Excluded

- Portal-to-Pipeline navigation logic -- covered by DEL-02-02.
- FileTree refresh behavior -- covered by DEL-02-01.
- Operator Toolkit panel content and behavior -- covered by DEL-02-03. (Layout integration with the toolkit sidebar toggle is in scope here.)
- Harness runtime APIs and streaming -- covered by PKG-03 deliverables.
- Build and packaging workflow -- covered by PKG-01 deliverables.
- Content or internal behavior of pane-hosted functional views (WORKBENCH, PIPELINE, etc.) beyond their layout container.

---

## Requirements

### Multi-pane Layout Requirements

#### REQ-LAYOUT-01: Resizable Multi-pane Layout

The desktop UI MUST provide a resizable multi-pane layout.

- **Source:** PLAN section 2; SOW-026.

#### REQ-LAYOUT-02: High-visibility Drag Handles

Pane boundaries MUST include high-visibility drag handles that allow the operator to resize panes via pointer interaction.

- **Source:** PLAN section 2 ("high-visibility drag handles").

#### REQ-LAYOUT-03: Keyboard Resize Support

The multi-pane layout MUST support keyboard-based resize operations as an alternative to pointer-based drag.

- **Source:** PLAN section 2 ("keyboard resize support").
- **Open item:** Specific keyboard shortcut conventions are TBD (lensing item A-002). See Conflict Table entry CT-002.

#### REQ-LAYOUT-04: Collapse/Expand Affordances

Each resizable pane MUST provide collapse and expand affordances that allow the operator to minimize or restore a pane.

- **Source:** PLAN section 2 ("collapse/expand affordances").

#### REQ-LAYOUT-05: Minimum Pane Size Constraints

Resizable panes SHOULD enforce a minimum size to prevent content from becoming unusable.

- **Source:** **ASSUMPTION** -- standard UX practice for resizable panels; not explicitly stated in available sources.
- **Rationale gap:** The use of SHOULD (rather than MUST) is not explained in available sources. See Guidance for rationale discussion and Conflict Table entry CT-005 (lensing item A-005).

#### REQ-LAYOUT-06: Pane Arrangement Consistency

The pane arrangement MUST be consistent with the desktop application's navigation model: PORTAL matrix, WORKBENCH, and PIPELINE views MUST be accommodated within the layout.

- **Source:** PLAN section 2 (contextual -- layout hosts navigation); SPEC section 14 (navigation contract); exact arrangement TBD.

#### REQ-LAYOUT-07: Toolkit Sidebar Layout Integration

The multi-pane layout MUST accommodate the Operator Toolkit sidebar visibility toggle (controlled from CONFIG, persisted in local storage) without breaking pane resize behavior.

- **Source:** PLAN section 2 (toolkit panel visibility control); DIRECTIVE section 2.5 (non-authoritative convenience state).
- **Note:** Toolkit panel content is DEL-02-03 scope; this requirement covers layout integration only.

### Theme Hardening Requirements

#### REQ-THEME-01: Light Mode Accent Text

Light mode MUST use non-orange accent text for readability.

- **Source:** PLAN section 2 ("Light mode uses non-orange accent text for readability").
- **Open item:** No measurable readability criterion (e.g., minimum contrast ratio) is defined. If WCAG 2.1 AA is confirmed applicable, contrast ratios from WCAG 1.4.3 (minimum 4.5:1 for normal text, 3:1 for large text) would apply. See Conflict Table entry CT-008 (lensing item E-003).

#### REQ-THEME-02: Role-specific Chat Bubble Styling

Assistant and user chat bubbles MUST use role-specific low-contrast surfaces with left/right alignment for quick visual scanning.

- Assistant messages: left-aligned.
- User messages: right-aligned.

- **Source:** PLAN section 2.

#### REQ-THEME-03: GitHub-flavored Markdown Rendering in Chat

Assistant messages MUST render GitHub-flavored markdown (GFM) in-chat.

The following GFM elements MUST be supported:
- Tables
- Task lists
- Strikethrough
- Autolinks
- Fenced code blocks with language-tagged syntax highlighting

- **Source:** PLAN section 2 ("Assistant messages render GitHub-flavored markdown in-chat"); GFM element enumeration derived from Guidance C6 cross-reference (lensing item E-002).

#### REQ-THEME-04: ANSI Fallback for Tool Output

Tool output content MUST render with ANSI fallback for terminal-style output.

- **Source:** PLAN section 2 ("ANSI fallback for terminal-style tool output").
- **Open item:** Specific ANSI escape sequence scope is TBD (e.g., SGR color codes, bold/underline, 256-color, true color). Fallback behavior for unsupported sequences is also TBD. See Conflict Table entry CT-007 (lensing item E-001).

#### REQ-THEME-05: Top-banner Status Cleanup

The top-banner status area MUST suppress extraneous noise. Update messaging MUST appear only when an update is actually available.

- **Source:** PLAN section 2 ("Top-banner status noise was removed; update messaging only appears when an update is actually available").

#### REQ-THEME-06: Header Brand Tile

The header brand tile MUST use the macOS app icon asset with rounded-square treatment.

- **Source:** PLAN section 2 ("Header brand tile uses the macOS app icon asset with rounded-square treatment").

#### REQ-THEME-07: Dark Mode Parity

Dark mode theming SHOULD apply equivalent structural improvements as light mode (chat bubble differentiation, markdown rendering, status behavior, brand tile) where applicable.

- **Source:** **ASSUMPTION** -- dark mode parity is standard UX practice; explicit dark mode requirements are not stated in available sources.
- **Open item:** The use of SHOULD creates ambiguity about whether dark mode parity is a quality prerequisite or an aspirational target. See Conflict Table entry CT-006 (lensing item F-003) and Guidance discussion.

### Conditional Requirement

#### REQ-LAYOUT-08: Layout State Persistence Verification (conditional)

If layout state persistence is implemented (Datasheet attribute "Persistence of layout state" currently TBD), automated verification MUST confirm that pane sizes and collapse/expand states persist across application sessions.

- **Source:** Lensing item X-002; conditional on scope decision for layout state persistence.
- **Note:** This requirement is activated only if persistence is brought into scope. If persistence is descoped, this requirement is void.

---

## Standards

| Standard / Reference | Applicability | Source | Notes |
|---------------------|---------------|--------|-------|
| PLAN section 2 | Primary feature description | Decomposition SOW-026, SOW-027 | Defines existing surface area |
| SPEC section 14 | UI navigation and selector contract | SPEC | Layout must host the navigation model |
| DIRECTIVE section 2.5 | Non-authoritative convenience state | DIRECTIVE | Pane state / toolkit visibility is convenience state |
| CONTRACT K-INVENT-1 | No invented values | CONTRACT | Theme values must be evidence-based |
| WCAG 2.1 AA | TBD -- applicability not confirmed | Not explicitly stated | See Conflict Table entry CT-001 (lensing items A-001, A-003). If confirmed, applies to contrast ratios, keyboard accessibility, screen reader announcements |

---

## Verification

| VerificationID | Requirement(s) | Approach | Acceptance Criteria |
|----------------|----------------|----------|---------------------|
| REQ-LAYOUT-01-V | REQ-LAYOUT-01 | Automated test + manual inspection | Multi-pane layout renders; panes resize via pointer drag |
| REQ-LAYOUT-02-V | REQ-LAYOUT-02 | Automated test + visual inspection | Drag handles visible at pane boundaries; pointer drag resizes panes |
| REQ-LAYOUT-03-V | REQ-LAYOUT-03 | Automated test (keyboard event simulation) | Keyboard shortcuts trigger pane resize; equivalent functionality to pointer drag |
| REQ-LAYOUT-04-V | REQ-LAYOUT-04 | Automated test + manual inspection | Each pane has a collapse/expand control; collapsed pane minimizes; expand restores |
| REQ-LAYOUT-05-V | REQ-LAYOUT-05 | Automated boundary test | Panes cannot be resized below a minimum usable size |
| REQ-LAYOUT-06-V | REQ-LAYOUT-06 | Manual inspection | Pane arrangement hosts PORTAL, WORKBENCH, and PIPELINE views correctly |
| REQ-LAYOUT-07-V | REQ-LAYOUT-07 | Automated functional test (toggle toolkit visibility) | Toolkit sidebar toggle does not break pane resize; pane boundaries remain consistent |
| REQ-LAYOUT-08-V | REQ-LAYOUT-08 (conditional) | Automated state test (session persistence) | Layout state persists across application restart. **Activated only if persistence is in scope.** |
| REQ-THEME-01-V | REQ-THEME-01 | Visual inspection (light mode) | Light mode accent text is not orange; text is readable. TBD: measurable readability criterion (lensing item E-003) |
| REQ-THEME-02-V | REQ-THEME-02 | Visual inspection | Chat bubbles are role-differentiated (left/right, distinct surfaces) |
| REQ-THEME-03-V | REQ-THEME-03 | Automated functional test (GFM sample inputs) | Headers, lists, code blocks, tables, task lists, strikethrough, autolinks, and fenced code blocks with syntax highlighting render correctly in assistant messages |
| REQ-THEME-04-V | REQ-THEME-04 | Automated functional test (ANSI escape sequences) | Tool output with ANSI codes renders with correct styling; TBD: define specific ANSI sequences in scope (lensing item E-001) |
| REQ-THEME-05-V | REQ-THEME-05 | Automated state test + manual inspection | No status banner when no update available; banner appears only for real updates |
| REQ-THEME-06-V | REQ-THEME-06 | Visual inspection | Header brand tile shows macOS app icon with rounded-square treatment |
| REQ-THEME-07-V | REQ-THEME-07 | Visual inspection (dark mode) | Dark mode applies equivalent structural improvements as light mode |
| EXCL-BOUNDARY-V | Scope exclusion boundary | Automated smoke test | Pane-hosted functional views (WORKBENCH, PIPELINE content) are not broken by layout changes; scope exclusion boundaries hold (lensing item X-003) |
| REGRESSION-V | Adjacent deliverable regression | Manual smoke test with defined scope | FileTree (DEL-02-01), navigation (DEL-02-02), toolkit (DEL-02-03) features function as before. See Procedure for specific regression test cases (lensing item X-004) |

---

## Documentation

### Required Artifacts

| Artifact | Type | Description |
|----------|------|-------------|
| Layout component source | CODE | Resizable multi-pane layout implementation (drag handles, keyboard resize, collapse/expand) |
| Theme/styling source | CODE | Theme hardening CSS/component changes (accent text, chat bubbles, markdown, status banner, brand tile) |
| Layout tests | TEST | Automated tests for resize, collapse/expand, keyboard support, minimum pane size, toolkit sidebar integration |
| Theme tests | TEST | Automated and/or visual regression tests for theme hardening requirements |
