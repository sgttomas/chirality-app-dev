# Working Memory — DEL-02-06

*This file is shared working memory for WORKING_ITEMS and TASK agents operating on this deliverable.*

## Key Decisions

- 2026-02-24: Deliverable created by SCA-003 to implement UI-based API key entry and non-project-truth local secure storage.
- Runtime contract: UI-provided key takes precedence; `ANTHROPIC_API_KEY` remains fallback.
- 2026-02-24: First implementation pass architecture: safeStorage adapter in Electron main → IPC bridge → preload → renderer Settings UI. Server-side key access via process-global variable (shared process in packaged builds). ENV+UI precedence implemented in `readAnthropicApiKey()`.
- 2026-02-24: Human ruling confirmed `safeStorage` as the encryption mechanism for local key storage (REQ-04).
- 2026-02-24: Human ruling selected validate-on-save policy for key entry validation (Guidance T3).
- 2026-02-24: Human ruling approved current UI location in working-root-bar.
- 2026-02-24: Second implementation pass completed. Added focused tests for storage adapter, IPC handler bridge, and UI/env key precedence paths; reconciled DEL-03-05 Specification REQ-02/REQ-07 language to `ENV+UI`.
- 2026-02-24: Human ruling finalized REQ-07 policy as re-query-per-turn (no `api-key:changed` notification channel required).
- 2026-02-24: REQ-07 ruling propagated through DEL-02-06 docs and lifecycle advanced to `ISSUED`.

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

## Implementation Inventory (Second Pass)

### New Files Created
| File | Purpose |
|------|---------|
| `frontend/electron/api-key-ipc.ts` | Isolated API-key IPC registration/teardown for testable bridge behavior |
| `frontend/src/__tests__/electron/api-key-storage.test.ts` | Unit coverage for secure-storage adapter behavior and failure modes |
| `frontend/src/__tests__/electron/api-key-ipc.test.ts` | Unit coverage for IPC channels and source-precedence status reporting |

### Modified Files
| File | Change |
|------|--------|
| `frontend/electron/main.ts` | Delegates API-key handler registration to `api-key-ipc.ts` |
| `frontend/src/__tests__/lib/harness-anthropic-agent-sdk-manager.test.ts` | Added UI-first precedence and env-fallback-after-clear test coverage |
| `execution/PKG-03_Harness_Runtime_Core/1_Working/DEL-03-05_Anthropic_Provider_Integration/Specification.md` | Reconciled REQ-02/REQ-07/verification text from `ENV_ONLY` to `ENV+UI` |

## DEL-03-05 Interface Reconciliation (2026-02-24)

### Code-level reconciliation (DONE)
- `readAnthropicApiKey()` now implements ENV+UI precedence: UI key → env var.
- Error messages in both `anthropic-agent-sdk-manager.ts` and `turn/route.ts` updated to reference Settings UI.
- `readConfiguredApiKeys()` includes UI key in the redaction set, so key material from safeStorage is redacted in error messages (REQ-09 compliance).

### Document-level reconciliation (DONE — CONF-01 closed, 2026-02-24)
- DEL-03-05 `Specification.md` REQ-02 reconciled to `ENV+UI` contract language.
- DEL-03-05 `Specification.md` REQ-07 ruling-bound storage note reconciled to UI secure storage + env fallback.
- DEL-03-05 verification row for REQ-02 reconciled to UI-first, env-fallback path.

## Open Questions

- None.

## Verification Status

- TypeCheck (Electron): PASS
- TypeCheck (Next.js): PASS
- Focused DEL-02-06 test pass: `npm test -- src/__tests__/electron/api-key-storage.test.ts src/__tests__/electron/api-key-ipc.test.ts src/__tests__/lib/harness-anthropic-agent-sdk-manager.test.ts` -> PASS (91 tests)
- Full frontend typecheck: `npm run typecheck` -> PASS
- Manual verification: TBD (requires Electron runtime)
