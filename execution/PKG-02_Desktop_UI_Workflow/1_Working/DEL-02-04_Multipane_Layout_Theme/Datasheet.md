# Datasheet — DEL-02-04: Multi-pane Layout + Theme Hardening

---

## Identification

| Field | Value |
|-------|-------|
| **DeliverableID** | DEL-02-04 |
| **Name** | Multi-pane Layout + Theme Hardening |
| **PackageID** | PKG-02 |
| **Package** | Desktop UI Workflow |
| **Type** | UX_UI_SLICE |
| **ContextEnvelope** | M |
| **ResponsibleParty** | TBD |
| **Scope Items** | SOW-026, SOW-027 |
| **Objectives** | OBJ-005 |
| **Anticipated Artifacts** | CODE/TEST |
| **Lifecycle State** | SEMANTIC_READY |

**Source:** `_CONTEXT.md`; Decomposition `DEL-02-04` entry; `_STATUS.md` (lifecycle state).

**Enrichment notes:**
- Lifecycle State updated from OPEN to SEMANTIC_READY per `_STATUS.md` authoritative record (lensing item C-001).
- OBJ-005 mapping confirmed: decomposition `SupportsObjectives` column explicitly lists OBJ-005 for DEL-02-04 and both SOW-026 and SOW-027 map to OBJ-005 (lensing item D-001; ASSUMPTION tag removed).

## Issuance Hygiene (2026-02-24)

- Lifecycle state is `ISSUED`.
- ANSI-scope and WCAG-applicability questions remain as design/governance follow-up and are non-blocking for issued status.
- Legacy implementation-phase `TBD` and conflict-table text is non-blocking unless explicitly re-opened by human ruling.

---

## Attributes

### Multi-pane Layout (SOW-026)

| Attribute | Value | Source |
|-----------|-------|--------|
| Layout model | Resizable multi-pane | PLAN section 2 "Resizable multi-pane layout improvements" |
| Drag handles | High-visibility drag handles | PLAN section 2 |
| Keyboard resize | Supported | PLAN section 2 |
| Keyboard shortcut conventions | TBD | Not specified in available sources (lensing item A-002) |
| Collapse/expand affordances | Supported | PLAN section 2 |
| Pane configuration (count, nesting, orientation) | TBD | Not specified in available sources (lensing item B-001) |
| Minimum pane dimensions | TBD | Not specified in available sources (lensing item B-001) |
| Default pane proportions | TBD | Not specified in available sources (lensing item B-001) |
| Persistence of layout state | TBD | Not specified in available sources; DIRECTIVE section 2.5 permits non-authoritative convenience state in local storage (lensing item B-001) |

### Theme Hardening (SOW-027)

| Attribute | Value | Source |
|-----------|-------|--------|
| Light mode accent text | Non-orange accent text for readability | PLAN section 2 "Theme hardening" |
| Light mode readability metric (e.g., contrast ratio) | TBD | Not specified in available sources; no measurable criterion defined (lensing item E-003) |
| Chat bubble styling -- assistant | Role-specific low-contrast surface, left-aligned | PLAN section 2 |
| Chat bubble styling -- user | Role-specific low-contrast surface, right-aligned | PLAN section 2 |
| Markdown rendering in chat | GitHub-flavored markdown in-chat for assistant messages | PLAN section 2 |
| GFM elements supported | Tables, task lists, strikethrough, autolinks, fenced code blocks with language-tagged syntax highlighting | Guidance C6 (derived from GFM specification); see also Specification REQ-THEME-03 |
| ANSI fallback | Terminal-style tool output rendering | PLAN section 2 |
| ANSI escape sequence scope | TBD | Not specified in available sources; REQ-THEME-04 does not define which ANSI sequences are supported (lensing item E-001) |
| Top-banner status | Noise removed; update messaging only when update actually available | PLAN section 2 |
| Header brand tile | macOS app icon asset with rounded-square treatment | PLAN section 2 |
| Dark mode color values and palette | TBD | Not specified in available sources; see Specification REQ-THEME-07 and Guidance C5 (lensing item B-003) |

---

## Conditions

| Condition | Value | Source |
|-----------|-------|--------|
| Target platform | macOS 15+, Apple Silicon only | Decomposition DEC-PLAT-001 |
| Application framework | Electron + Next.js | PLAN section 2; DIRECTIVE section 1 |
| Theme modes supported | Light mode explicitly addressed; dark mode TBD | PLAN section 2 (light mode explicitly mentioned) |
| Accessibility requirements (WCAG 2.1 AA) | TBD -- applicability not confirmed | Not explicitly stated in available sources (lensing items A-001, A-003) |
| Browser/renderer engine | Chromium (via Electron) | **ASSUMPTION: Electron uses Chromium** |

---

## Construction

| Aspect | Value | Source |
|--------|-------|--------|
| Implementation technology | React (Next.js) components within Electron shell | **ASSUMPTION: inferred from Electron + Next.js stack** |
| CSS/styling approach | TBD | Not specified in available sources (lensing item B-002) |
| Layout mechanism (CSS Grid / Flexbox / custom) | TBD | Not specified in available sources (lensing item B-002) |
| Component library | TBD | Not specified in available sources (lensing item B-002) |
| Test framework | TBD | Not specified in available sources (lensing items B-002, C-002) |

---

## References

| Reference | Location | Relevance |
|-----------|----------|-----------|
| Software Decomposition | `execution/_Decomposition/ChiralityApp_SoftwareDecomposition_2026-02-21_G7-APPROVED.md` | DEL-02-04 definition, scope items, objectives |
| PLAN | `docs/PLAN.md` section 2 | Feature descriptions for multi-pane layout and theme hardening |
| DIRECTIVE | `docs/DIRECTIVE.md` | Founding intent, design philosophy, constraints |
| SPEC | `docs/SPEC.md` | Physical structures, UI navigation contract (section 14) |
| CONTRACT | `docs/CONTRACT.md` | Binding invariants |
| `_CONTEXT.md` | `execution/PKG-02_Desktop_UI_Workflow/1_Working/DEL-02-04_Multipane_Layout_Theme/_CONTEXT.md` | Deliverable identity and traceability |
| `_STATUS.md` | `execution/PKG-02_Desktop_UI_Workflow/1_Working/DEL-02-04_Multipane_Layout_Theme/_STATUS.md` | Authoritative lifecycle state |
| `_SEMANTIC_LENSING.md` | `execution/PKG-02_Desktop_UI_Workflow/1_Working/DEL-02-04_Multipane_Layout_Theme/_SEMANTIC_LENSING.md` | Enrichment register (Pass 3 source) |
