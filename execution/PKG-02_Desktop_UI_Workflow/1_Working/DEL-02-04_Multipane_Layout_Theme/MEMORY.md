# Working Memory — DEL-02-04

*This file is shared working memory for WORKING_ITEMS and TASK agents operating on this deliverable.*

## Key Decisions

- 2026-02-24: Implemented pane resizing at the shell level using explicit drag handles (`role="separator"`), keyboard resize support (`ArrowLeft`/`ArrowRight`, `Shift` acceleration), and collapse/expand toggles for each resizable pane (`File Tree`, `Tool Kit`, `Chat`).
- 2026-02-24: Adopted local-storage layout persistence (`chirality.layout.v1`) as non-authoritative convenience state for pane widths and collapsed states, aligned with DIRECTIVE section 2.5 posture.
- 2026-02-24: Adopted `react-markdown` + `remark-gfm` for assistant-message GFM rendering and `ansi_up` class-based fallback for terminal ANSI sequences, with dedicated chat markdown component and focused tests.
- 2026-02-24: Added explicit dark-mode token overrides for structural parity with light-mode theme hardening changes.

## Open Questions

- REQ-THEME-05 update-banner integration remains functionally inert in this pass (shell suppresses noise by default; no updater signal source is currently wired into the frontend runtime).
- REQ-THEME-04 ANSI scope is still broader than currently verified; this pass validates fallback rendering and representative color sequences but does not formalize a full sequence compatibility matrix.

## Notes

- Implementation files:
  - `frontend/src/components/shell/app-shell.tsx`
  - `frontend/src/components/shell/chat-panel.tsx`
  - `frontend/src/components/shell/chat-markdown.tsx`
  - `frontend/src/lib/shell/layout-state.ts`
  - `frontend/src/lib/shell/ansi.ts`
  - `frontend/src/app/globals.css`
  - `frontend/public/chirality-app-icon.svg`
- Verification coverage added:
  - `frontend/src/__tests__/components/chat-markdown.test.ts`
  - `frontend/src/__tests__/lib/layout-state.test.ts`
  - `frontend/src/__tests__/lib/ansi.test.ts`
- Verification results in `frontend/`:
  - `npm test` -> PASS (`244` tests)
  - `npm run typecheck` -> PASS
  - `npm run build` -> PASS
