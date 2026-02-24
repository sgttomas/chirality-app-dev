# Working Memory — DEL-02-06

*This file is shared working memory for WORKING_ITEMS and TASK agents operating on this deliverable.*

## Key Decisions

- 2026-02-24: Deliverable created by SCA-003 to implement UI-based API key entry and non-project-truth local secure storage.
- Runtime contract: UI-provided key takes precedence; `ANTHROPIC_API_KEY` remains fallback.
- 2026-02-24: First implementation pass architecture: safeStorage adapter in Electron main → IPC bridge → preload → renderer Settings UI. Server-side key access via process-global variable (shared process in packaged builds). ENV+UI precedence implemented in `readAnthropicApiKey()`.
- 2026-02-24: Human ruling confirmed `safeStorage` as the encryption mechanism for local key storage (REQ-04).
- 2026-02-24: Human ruling selected validate-on-save policy for key entry validation (Guidance T3).
- 2026-02-24: Human ruling approved current UI location in working-root-bar.

## Implementation Inventory (First Pass)

### New Files Created
| File | Purpose |
|------|---------|
| `frontend/electron/api-key-storage.ts` | safeStorage adapter: encrypt/decrypt/persist/load API key in app userData directory |
| `frontend/src/lib/harness/api-key-store.ts` | Server-side accessor: reads UI API key from process global |
| `frontend/src/components/settings/api-key-settings.tsx` | React component: masked key entry, save/remove, status display, graceful degradation |

### Modified Files
| File | Change |
|------|--------|
| `frontend/electron/main.ts` | Added API key IPC handlers (`chirality:api-key-store`, `chirality:api-key-remove`, `chirality:api-key-status`) + `loadStoredKeyIntoGlobal()` on startup |
| `frontend/electron/preload.ts` | Exposed `apiKey.store()`, `apiKey.remove()`, `apiKey.status()` via context bridge |
| `frontend/src/lib/harness/anthropic-agent-sdk-manager.ts` | `readAnthropicApiKey()`: UI key → ANTHROPIC_API_KEY → CHIRALITY_ANTHROPIC_API_KEY. `readConfiguredApiKeys()`: includes UI key in redaction set. Error message updated to reference Settings. |
| `frontend/src/app/api/harness/turn/route.ts` | `hasAnthropicApiKeyConfigured()`: checks `hasUiApiKey()` first. Error message updated. |
| `frontend/src/components/shell/app-shell.tsx` | Integrated `ApiKeySettings` component into working-root-bar |
| `frontend/src/app/globals.css` | Added API key settings styles |

## DEL-03-05 Interface Reconciliation (2026-02-24)

### Code-level reconciliation (DONE)
- `readAnthropicApiKey()` now implements ENV+UI precedence: UI key → env var.
- Error messages in both `anthropic-agent-sdk-manager.ts` and `turn/route.ts` updated to reference Settings UI.
- `readConfiguredApiKeys()` includes UI key in the redaction set, so key material from safeStorage is redacted in error messages (REQ-09 compliance).

### Document-level reconciliation (OUTSTANDING — CONF-01)
- DEL-03-05 `Specification.md` REQ-02 still contains `ENV_ONLY` language (pre-SCA-003).
- Needs update to reflect `ENV+UI` policy when DEL-03-05 enters its next WORKING_ITEMS session.
- Impacted text: REQ-02 lines 43-48 (three references to ENV_ONLY/no-safeStorage).
- This is captured as CONF-01 in DEL-02-06 Guidance.md Conflict Table.

## Open Questions

- CONF-01: DEL-03-05 REQ-02 ENV_ONLY text needs updating (document-level; code is already reconciled).
- REQ-07 ASSUMPTION: Change notification vs re-query-per-turn (human ruling pending; current implementation uses re-query-per-turn and does not emit change events).

## Verification Status (First Pass)

- TypeCheck (Electron): PASS
- TypeCheck (Next.js): PASS
- Test Suite: 260/260 PASS (30 test files)
- Manual verification: TBD (requires Electron runtime)
