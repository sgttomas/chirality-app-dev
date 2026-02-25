# Working Memory — DEL-05-01

*This file is shared working memory for WORKING_ITEMS and TASK agents operating on this deliverable.*

## Key Decisions & Human Rulings

- Implementation lives in this repo `/Users/ryan/ai-env/projects/chirality-app-dev/` — this deliverable specifies and tracks; code changes apply there.
- Human issuance approval recorded on 2026-02-23 for `CHECKING -> ISSUED`; decision record: `ISSUED_Gate_Decision_Record_2026-02-23.md`.

## Domain Context

### Local Repository Audit (2026-02-22)

**What's already implemented (~70%):**

1. **`extraResources` bundling** (in `frontend/package.json` `"build"` key):
   - `../agents` → `instruction-root/agents`
   - `..` (filter: `["*.md"]`) → `instruction-root/` (root-level .md files)
   - `../design` → `instruction-root/design`
   - `../init` → `instruction-root/init`

2. **Path resolution — main process** (`frontend/electron/main.cjs` lines 222-260):
   - `isInstructionRoot(path)` — sentinel check: `AGENTS.md`, `README.md`, `agents/` dir
   - `resolveInstructionRoot(frontendRoot)`:
     1. `CHIRALITY_INSTRUCTION_ROOT` env var (if valid)
     2. Packaged: `process.resourcesPath + "instruction-root"`
     3. Dev: parent of `frontendRoot` (repo root)
   - Sets `process.env.CHIRALITY_INSTRUCTION_ROOT` before Next.js starts

3. **Path resolution — Next.js server** (`frontend/lib/harness/instruction-root.ts`):
   - `getInstructionRoot()` — cached singleton, reads env var then walks up dirs
   - `isInstructionRootWritable(root)` — checks write permission
   - Same sentinel set: `AGENTS.md`, `README.md`, `agents/`

4. **Build toolchain:** `electron-builder@25.1.8`, Electron `33.3.1`/`33.4.11`, `asar: true`

### Initial gap snapshot (2026-02-22; historical)

| Gap | REQ | Severity | Notes |
|-----|-----|----------|-------|
| `docs/` governance files NOT bundled | REQ-01 | **BLOCKER** | Historical gap closed in Pass 3 (`frontend/package.json` `extraResources` now bundles `../docs`). |
| Sentinel check misses `docs/` | REQ-01 | MEDIUM | Historical gap closed in Pass 3 (instruction-root validation now requires `docs` directory). |
| No SHA-256 integrity verification | REQ-04 | MEDIUM | Historical gap closed in Pass 5 (`verify-instruction-root-integrity.mjs` + packaging gate wiring). |
| Read-only enforcement is documentation-only | REQ-02 | LOW | Historical gap closed in Pass 4/6 (`WORKING_ROOT_CONFLICT` runtime guard at session create/boot). |
| Graceful degradation behavior undefined | REQ-07 | LOW | Historical gap closed in Pass 4/6 (`INSTRUCTION_ROOT_INVALID` fail-fast diagnostic behavior). |
| Working root independence not systematically tested | REQ-05/REQ-06 | LOW | Paths with spaces, unicode, external volumes not tested |

### Proposed fix (BLOCKER — `docs/` bundling):

Add to `package.json` `build.extraResources`:
```json
{ "from": "../docs", "to": "instruction-root/docs" }
```

Add to sentinel check in `main.cjs` `isInstructionRoot()`:
```js
const required = ["AGENTS.md", "README.md", "agents", "docs"];
```

And similarly in `lib/harness/instruction-root.ts`.

## Open Items

- Verify integrity automation stays green as agent-suite/governance files evolve (manifest count/hash deltas expected as source changes).
- Optional hardening question: decide whether additional filesystem-level read-only controls are needed beyond the current runtime path guard.
- Optional policy questions remain open (`TBD-S04`, `TBD-S05`) but are non-blocking for baseline scope.
- Baseline lifecycle is complete (`ISSUED`); remaining items are optional hardening/policy follow-through only.

## Proposal History

- 2026-02-22: Gap analysis complete; blocker and sentinel fixes identified.
- 2026-02-22 (Pass 3): Applied this repo fixes:
  - `frontend/package.json` `build.extraResources` now includes `../docs -> instruction-root/docs`.
  - `frontend/electron/main.cjs` `isInstructionRoot()` now requires `docs` directory in sentinel set.
  - `frontend/lib/harness/instruction-root.ts` `isInstructionRoot()` now requires `docs` directory in sentinel set.
  - `npm run build` passed after changes.
- 2026-02-23 (Pass 5): REQ-04 integrity automation landed:
  - Added `frontend/scripts/verify-instruction-root-integrity.mjs` (SHA-256 manifest + bundled-resource parity verification).
  - Added script tests at `frontend/src/__tests__/scripts/verify-instruction-root-integrity.test.ts`.
  - Wired automation into packaging flows via `frontend/package.json`:
    - `instruction-root:integrity`
    - `desktop:pack` and `desktop:dist` now fail-closed on integrity mismatch.
- 2026-02-23 (Pass 6): Residual rulings closed for REQ-02/REQ-07:
  - `TBD-S01` resolved to API-level runtime path guard (`WORKING_ROOT_CONFLICT`) as baseline enforcement.
  - `TBD-S03` resolved to fail-fast boot refusal with typed diagnostics (`INSTRUCTION_ROOT_INVALID`).
- 2026-02-23 (Pass 8): Checking-prep gate evidence refreshed and decision input recorded:
  - Fresh verification rerun passed in `frontend/` (`npm test` 70, `npm run typecheck`, `npm run build`, `npm run desktop:pack`, `npm run desktop:dist`).
  - Integrity gate remained green (`status=pass`, `checkedFileCount=38`) at:
    - `frontend/artifacts/harness/instruction-root-integrity/latest/summary.json`
  - Checking packet added:
    - `CHECKING_Gate_Decision_Input_2026-02-23.md`
  - Lifecycle recommendation applied in this cycle: `IN_PROGRESS -> CHECKING`.
- 2026-02-23 (Pass 9): Human issuance gate executed:
  - Explicit human approval received in-session for `CHECKING -> ISSUED`.
  - Issuance decision record added:
    - `ISSUED_Gate_Decision_Record_2026-02-23.md`
  - Lifecycle advanced in `_STATUS.md`: `CHECKING -> ISSUED`.

## Interface & Dependency Notes

- Path resolution is already used by `session-manager.ts`, `persona-manager.ts`, and `agent-sdk-manager.ts` in the this repo.
- `extraResources` changes affect the build artifact; test with `desktop:pack` after change.

## Pass-3 Implementation Evidence (2026-02-22)

- Sibling diff confirms `docs` bundling added at `frontend/package.json` `extraResources`.
- Sibling diff confirms instruction-root sentinel hardening in both Electron main process and Next.js server helper:
  - `frontend/electron/main.cjs`
  - `frontend/lib/harness/instruction-root.ts`
- Verified `frontend/package.json` remains valid JSON (`python3 -m json.tool`).
- Verified repo-local `frontend` build succeeds (`npm run build`).

## Pass-4 Implementation Evidence (2026-02-23)

- Runtime instruction-root hardening implemented in current tree:
  - Added `frontend/src/lib/harness/instruction-root.ts` with:
    - deterministic root resolution (`CHIRALITY_INSTRUCTION_ROOT` override + fallback)
    - required resource validation (`AGENTS.md`, `README.md`, `agents/`, `docs/{DIRECTIVE,CONTRACT,SPEC,TYPES,PLAN}.md`)
    - typed failure (`INSTRUCTION_ROOT_INVALID`) with missing/invalid entry diagnostics
    - path-overlap helper used for working-root separation enforcement
  - Updated `frontend/src/lib/harness/persona-manager.ts` to validate instruction root before persona lookup.
  - Updated `frontend/src/lib/harness/session-manager.ts` to reject `projectRoot` paths inside instruction root (`WORKING_ROOT_CONFLICT`, HTTP 409).
  - Updated `frontend/electron/main.ts` to set `process.env.CHIRALITY_INSTRUCTION_ROOT` deterministically for both packaged and dev runs.
- Packaging manifest expanded to include root instruction documents:
  - `frontend/package.json` `build.extraResources` now copies:
    - `AGENTS.md`
    - `README.md`
    - `WHAT-IS-AN-AGENT.md`
    - `PROFESSIONAL_ENGINEERING.md`
  - Existing `agents/` and `docs/` resource copies retained.
- Test coverage refreshed:
  - Added `frontend/src/__tests__/lib/harness-instruction-root.test.ts`
  - Extended `frontend/src/__tests__/api/harness/routes.test.ts` for:
    - `WORKING_ROOT_CONFLICT`
    - `INSTRUCTION_ROOT_INVALID`
  - Extended `frontend/src/__tests__/lib/harness-error-display.test.ts` for instruction-root UI mapping.
- Verification results:
  - `npm test` -> PASS (`66` tests)
  - `npm run typecheck` -> PASS
  - `npm run build` -> PASS
  - `npm run desktop:pack` -> PASS
  - `npm run desktop:dist` -> PASS
- Packaged artifact verification (`frontend/dist/mac-arm64/Chirality.app/Contents/Resources`) confirms required instruction resources are present:
  - `AGENTS.md`, `README.md`, `WHAT-IS-AN-AGENT.md`, `PROFESSIONAL_ENGINEERING.md`
  - `agents/` directory (including `AGENT_WORKING_ITEMS.md`)
  - `docs/` directory (`DIRECTIVE.md`, `CONTRACT.md`, `SPEC.md`, `TYPES.md`, `PLAN.md`)

## Pass-5 Implementation Evidence (2026-02-23)

- Added automated integrity verification script:
  - `frontend/scripts/verify-instruction-root-integrity.mjs`
  - Computes source manifest (SHA-256 + size) for canonical instruction-root set:
    - root docs: `AGENTS.md`, `README.md`, `WHAT-IS-AN-AGENT.md`, `PROFESSIONAL_ENGINEERING.md`
    - governance docs: `docs/{DIRECTIVE,CONTRACT,SPEC,TYPES,PLAN}.md`
    - all `agents/AGENT_*.md` files
  - Verifies packaged `Resources/` hashes match source at build commit.
  - Writes artifacts:
    - `frontend/artifacts/harness/instruction-root-integrity/latest/manifest.json`
    - `frontend/artifacts/harness/instruction-root-integrity/latest/summary.json`
- Added script contract coverage:
  - `frontend/src/__tests__/scripts/verify-instruction-root-integrity.test.ts`
  - Covers pass-path and mismatch fail-path execution.
- Packaging flows now enforce integrity automation:
  - `frontend/package.json` adds `instruction-root:integrity`
  - `desktop:pack` and `desktop:dist` execute integrity verification after packaging.
- Verification results for this pass:
  - `npm test` -> PASS (`68` tests)
  - `npm run typecheck` -> PASS
  - `npm run build` -> PASS
  - `npm run desktop:pack` -> PASS
  - Integrity summary from packaged resources: `status=pass`, `checked files=38`, `git sha=1c65358fbfcea7ea13d47a7766c79d752b07e641`
- Residual impact:
  - **TBD-S02 (REQ-04 automation)** is now closed for baseline scope in this deliverable.

## Pass-8 Checking-Prep Evidence (2026-02-23)

- Verification rerun (current cycle):
  - `npm test` -> PASS (`70` tests)
  - `npm run typecheck` -> PASS
  - `npm run build` -> PASS
  - `npm run desktop:pack` -> PASS
  - `npm run desktop:dist` -> PASS
- Integrity artifact summary:
  - Path: `frontend/artifacts/harness/instruction-root-integrity/latest/summary.json`
  - `status=pass`
  - `checkedFileCount=38`
  - `missingInBundle=[]`
  - `mismatchedFiles=[]`
- Gate artifact:
  - `execution/PKG-05_Filesystem_Execution_Model/1_Working/DEL-05-01_Instruction_Root_Bundling/CHECKING_Gate_Decision_Input_2026-02-23.md`
- Lifecycle outcome for this pass:
  - DEL-05-01 advanced `IN_PROGRESS -> CHECKING`.

## Pass-9 Issuance Evidence (2026-02-23)

- Human approval recorded for issuance gate:
  - `you have my approve to run the DEL-05-01 human gate step next (CHECKING -> ISSUED)`
- Issuance decision artifact:
  - `execution/PKG-05_Filesystem_Execution_Model/1_Working/DEL-05-01_Instruction_Root_Bundling/ISSUED_Gate_Decision_Record_2026-02-23.md`
- Lifecycle outcome for this pass:
  - DEL-05-01 advanced `CHECKING -> ISSUED`.

## Coordination Publish Trace (Transferred 2026-02-24)

Source: `execution/_Coordination/NEXT_INSTANCE_STATE_ARCHIVE_2026-02-24_pre_simplify.md`

- `cf8693f` — instruction-root SHA-256 integrity automation (`verify-instruction-root-integrity.mjs`), packaging-gate wiring (`instruction-root:integrity` on `desktop:pack`/`desktop:dist`), script contract tests, DEL-05-01 status/spec/procedure/dependencies/memory updates, Tier 1 PASS4 control-loop + reconciliation evidence, and handoff pointer refresh.
- `f65b414` — DEL-05-01 REQ-02/REQ-07 residual-ruling closure
- `c21bd34` — DEL-05-01 checking/issuance gate artifacts and deliverable-local lifecycle continuity updates
- `ec5ead8` — coordination handoff refresh after DEL-05-01 issuance
