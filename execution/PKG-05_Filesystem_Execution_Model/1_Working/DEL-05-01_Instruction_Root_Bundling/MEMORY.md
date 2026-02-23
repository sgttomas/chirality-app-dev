# Working Memory — DEL-05-01

*This file is shared working memory for WORKING_ITEMS and TASK agents operating on this deliverable.*

## Key Decisions & Human Rulings

- Implementation lives in this repo `/Users/ryan/ai-env/projects/chirality-app-dev/` — this deliverable specifies and tracks; code changes apply there.

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

### Gaps requiring implementation:

| Gap | REQ | Severity | Notes |
|-----|-----|----------|-------|
| `docs/` governance files NOT bundled | REQ-01 | **BLOCKER** | `extraResources` filter `["*.md"]` only catches root `.md` files; `docs/DIRECTIVE.md`, `docs/CONTRACT.md`, `docs/SPEC.md`, `docs/TYPES.md`, `docs/PLAN.md` are NOT included |
| Sentinel check misses `docs/` | REQ-01 | MEDIUM | `isInstructionRoot()` checks `AGENTS.md`, `README.md`, `agents/` but not `docs/` dir |
| No SHA-256 integrity verification | REQ-04 | MEDIUM | Build-time hash computation and runtime verification not implemented |
| Read-only enforcement is documentation-only | REQ-02 | LOW | `getInstructionRoot()` is documented as read-only but no runtime guard prevents writes |
| Graceful degradation behavior undefined | REQ-07 | LOW | No error handling for missing/corrupted instruction files at startup |
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
- **TBD-S01**: Read-only enforcement mechanism — document-only vs runtime guard vs filesystem permissions.
- **TBD-S03**: Degradation behavior — refuse to start vs diagnostic mode vs reduced mode.

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
