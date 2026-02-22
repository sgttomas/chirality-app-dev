# Datasheet -- DEL-01-01 macOS 15+ Apple Silicon Build Baseline

## Identification

| Field | Value |
|-------|-------|
| **Deliverable ID** | DEL-01-01 |
| **Name** | macOS 15+ Apple Silicon Build Baseline |
| **Package** | PKG-01 Build & Packaging |
| **Type** | CI_CD_CHANGE |
| **Context Envelope** | M |
| **Responsible Party** | TBD (ASSUMPTION: requires human assignment per project governance) |
| **Scope Coverage** | SOW-001 |
| **Supports Objective** | OBJ-001 -- Working macOS desktop build and install path (ASSUMPTION: best-effort mapping via PKG-01 package heuristic) |
| **Anticipated Artifacts** | CODE / CONFIG / SCRIPT / DOC |

## Attributes

| Attribute | Value | Source | Enrichment Notes |
|-----------|-------|--------|------------------|
| Target OS | macOS 15+ (Sequoia and later) | DEC-PLAT-001 (Decomposition, Decision Log) | |
| Target Architecture | Apple Silicon (arm64) only | DEC-PLAT-001 (Decomposition, Decision Log) | |
| Application Framework | Electron + Next.js desktop application | PLAN Section 2 "Desktop Frontend" | |
| Build Modes | Development build + Production build | _CONTEXT.md description: "dev + prod build" | |
| Signing Requirement | Not required (self-builder installs) | DEC-PLAT-001 (Decomposition, Decision Log); OBJ-001 acceptance criteria | |
| Notarization Requirement | Not required | DEC-PLAT-001 (Decomposition, Decision Log); OBJ-001 acceptance criteria | |
| Outbound Network Policy | Anthropic API only; no other outbound connections | DEC-NET-001 (Decomposition, Decision Log) | |
| Node.js Version | TBD | Not specified in accessible sources | Lensing A-001: foundational prescriptive parameter; resolve via repo dependency audit (e.g., inspect `package.json` `engines` field or `.node-version`) |
| Electron Version | TBD | Not specified in accessible sources | Lensing A-001: foundational prescriptive parameter; resolve via repo dependency audit (e.g., inspect `package.json` dependencies) |
| Next.js Version | TBD | Not specified in accessible sources | Lensing A-001: foundational prescriptive parameter; resolve via repo dependency audit |
| Package Manager | TBD | Not specified in accessible sources | Lensing A-001: foundational prescriptive parameter; resolve via repo lockfile detection (presence of `package-lock.json`, `yarn.lock`, or `pnpm-lock.yaml`) |
| Native Module Handling | TBD | ASSUMPTION: arm64-native modules may be needed; specifics depend on repo dependencies | Lensing B-002: a native module inventory table should be added here once the repo dependency audit is complete (see also Guidance C2) |

## Conditions

| Condition | Description | Source |
|-----------|-------------|--------|
| Platform Exclusivity | Build targets macOS 15+ / Apple Silicon only; no cross-platform targets in this deliverable | DEC-PLAT-001; SOW-001 |
| Filesystem-as-State | The built application must operate on the filesystem-as-state model; no external database dependency | DIRECTIVE Section 2.1; DIRECTIVE Section 5 (Structural Constraints) |
| Instruction Root Separation | Built application must support separation of instruction root (app bundle) and working root (user-selected projectRoot) | DIRECTIVE Section 2.6 |
| No Telemetry / Update Checks | No outbound network except Anthropic API | DEC-NET-001 |

## Construction

| Aspect | Description | Source |
|--------|-------------|--------|
| Build Toolchain | Electron + Next.js; specific build tooling (electron-builder, electron-forge, etc.) is TBD | PLAN Section 2 (desktop packaging reference); specifics not in accessible sources |
| Development Build | `npm run dev` or equivalent; must start and render on macOS 15+ / Apple Silicon | ASSUMPTION: standard Electron + Next.js dev workflow |
| Production Build | Produces a runnable `.app` bundle; `.dmg` packaging is handled by DEL-01-02 | _CONTEXT.md; Decomposition DEL-01-02 scope boundary |
| Architecture Target | `arm64` only; universal binary is not required | DEC-PLAT-001 |
| Native Dependencies | Any native Node.js modules must be compiled or available for arm64/macOS 15+ | ASSUMPTION: standard requirement for Apple Silicon builds |

**Terminology note (Lensing E-001):** The canonical term for the production build output of this deliverable is "`.app` bundle". All references to the build output across the four documents use this term consistently. "`.app`" alone is acceptable shorthand where context is unambiguous.

## References

| Ref | Document | Relevance |
|-----|----------|-----------|
| 1 | Decomposition (ChiralityApp_SoftwareDecomposition_2026-02-21_G7-APPROVED.md) | DEL-01-01 entry, DEC-PLAT-001, DEC-NET-001, OBJ-001 |
| 2 | docs/DIRECTIVE.md | Founding intent, filesystem-as-state, structural constraints, instruction root separation |
| 3 | docs/PLAN.md | Existing tooling description (Electron + Next.js desktop app), desktop packaging reference |
| 4 | docs/SPEC.md | Execution root layout, deliverable folder structure, harness contract |
| 5 | _CONTEXT.md | Deliverable identity, scope, anticipated artifacts |
