# Scope Change Brief — SCA-003

## Human Request (normalized)
Add UI-based API key entry and local secure storage as non-project-truth convenience state, introduce corresponding UI deliverable scope, and amend OI-001/DEL-03-05 key-provisioning contract from `ENV_ONLY` to `ENV+UI` (UI precedence, env fallback).

## Parsed Atomic Actions

| Seq | ActionType | EntityType | EntityID | Description |
|---|---|---|---|---|
| 1 | ADD | SCOPE_ITEM | SOW-050 | Add scope for UI API key entry + local secure storage convenience state. |
| 2 | ADD | DELIVERABLE | DEL-02-06 | Add PKG-02 deliverable `Settings / API Key Entry UI` (`UX_UI_SLICE`, ContextEnvelope `M`). |
| 3 | MODIFY | DELIVERABLE | DEL-03-05 | Amend key provisioning contract: `ENV_ONLY -> ENV+UI` (UI precedence; env fallback). |
| 4 | MODIFY | OPEN_ISSUE | OI-001 | Amend policy resolution wording from `ENV_ONLY` to `ENV+UI` while preserving non-project-truth boundaries. |

## Variant Resolution

- DECOMP_VARIANT: SOFTWARE
- EXECUTION_ROOT: `execution/`
- DECOMPOSITION_PATH: `execution/_Decomposition/ChiralityApp_SoftwareDecomposition_2026-02-21_G7-APPROVED.md`
