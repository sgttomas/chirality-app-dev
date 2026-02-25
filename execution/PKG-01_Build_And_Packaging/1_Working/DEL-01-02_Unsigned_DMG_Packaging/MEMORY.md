# Working Memory — DEL-01-02

*This file is shared working memory for WORKING_ITEMS and TASK agents operating on this deliverable.*

## Key Decisions & Human Rulings

- 2026-02-23: DMG packaging baseline is now pinned to `electron-builder` using `frontend/package.json` (`build` config + `desktop:pack`/`desktop:dist` scripts).
- 2026-02-23: macOS minimum target is now explicit in config (`mac.minimumSystemVersion=15.0.0`).
- 2026-02-23: Unsigned packaging is now deterministic across machines by forcing `CSC_IDENTITY_AUTO_DISCOVERY=false` in desktop packaging scripts.
- 2026-02-23: Unsigned acceptance for this scope allows ad-hoc signatures (`codesign -dv` showing `Signature=adhoc`, `TeamIdentifier=not set`) as long as no developer signing/notarization infrastructure is required.

## Domain Context

- DEL-01-02 is the WS-1 tail deliverable in the no-parallelism plan (`DEL-01-03 -> DEL-03-07 -> DEL-02-05 -> DEL-07-03 -> DEL-01-01 -> DEL-03-01 -> DEL-01-02`).
- DEL-01-02 remains packaging-focused and consumes upstream maturity from:
  - DEL-01-01 build baseline
  - DEL-05-01 instruction-root bundling/runtime-access architecture

## Open Items

- Optional polish only: electron-builder warning for missing `author` and default icon remains non-blocking for unsigned baseline.
- Optional future policy question: whether Gatekeeper handling should be elevated from documentation guidance into a formal requirement.

## Proposal History

- 2026-02-23: Added packaging hardening and guardrail coverage:
  - `frontend/package.json`
    - `desktop:pack` and `desktop:dist` now enforce `CSC_IDENTITY_AUTO_DISCOVERY=false`
    - `build.mac.minimumSystemVersion` set to `15.0.0`
  - `frontend/src/__tests__/scripts/dmg-packaging-policy.test.ts`
    - asserts unsigned script guardrail
    - asserts macOS min version + arm64 DMG target
    - asserts instruction-root resource bundling (`agents`, `docs`)
- 2026-02-23: Added local-builder documentation artifact:
  - `docs/building-dmg.md`
- 2026-02-23: Updated DEL-01-02 production docs and references with implemented baseline values:
  - `Datasheet.md`
  - `Specification.md`
  - `Guidance.md`
  - `Procedure.md`
  - `_REFERENCES.md`

Verification evidence (2026-02-23, `frontend/`):
- `npm test` -> PASS (138 tests)
- `npm run typecheck` -> PASS
- `npm run build` -> PASS
- `npm run desktop:dist` -> PASS
- Artifact checks:
  - DMG produced: `dist/Chirality-0.1.0-arm64.dmg` (~170 MB)
  - Binary architecture: `Mach-O 64-bit executable arm64`
  - `LSMinimumSystemVersion`: `15.0.0`
  - Instruction-root resource dirs present: `Contents/Resources/agents`, `Contents/Resources/docs`
  - `codesign -dv --verbose=4` shows `Signature=adhoc`, `TeamIdentifier=not set`

## Interface & Dependency Notes

- Upstream dependency satisfaction was refreshed for this pass:
  - `DEP-01-02-004` (`DEL-01-01`) -> `SATISFIED`
  - `DEP-01-02-005` (`DEL-05-01`) -> `SATISFIED`
- No dependency row add/retire/reclassify churn was introduced in this pass.

## Coordination Publish Trace (Transferred 2026-02-24)

Source: `execution/_Coordination/NEXT_INSTANCE_STATE_ARCHIVE_2026-02-24_pre_simplify.md`

- `2c1a148` — Tier 2 DEL-01-02 unsigned DMG baseline hardening (policy/script/config/docs), Tier 2 PASS16 control-loop + PASS12 reconciliation evidence, deliverable-local continuity updates, and coordination pointer refresh.
