# Specification: DEL-01-03 Frontend Workspace Bootstrap & Packaging Baseline

## Scope

### Included

This deliverable covers the creation of a tracked `frontend/` workspace within the repository and the establishment of a frontend desktop packaging baseline. Specifically:

1. **Workspace Bootstrap (SOW-044):** Create the `frontend/` directory as a tracked in-repo workspace containing:
   - Package manifest (`package.json`) with all required dependencies
   - TypeScript configuration (`tsconfig.json`)
   - Next.js configuration (`next.config.*`)
   - Electron main process scaffolding
   - Development startup scripts (`npm run dev`, `npm run build`)

2. **Packaging Baseline (SOW-047):** Establish frontend desktop packaging:
   - `desktop:pack` script (creates unpacked distributable for local testing)
   - `desktop:dist` script (creates distributable `.dmg` artifact)
   - Instruction-root inclusion checks ensuring `agents/` and `docs/` are present in packaging artifacts

Source: `_CONTEXT.md`; Decomposition Scope Amendment A1

### Excluded

- Full DMG signing/notarization workflow (covered by DEL-01-02; signing not required per DEC-PLAT-001)
- Harness API route implementation (covered by DEL-03-07)
- UI shell implementation (covered by DEL-02-05)
- Validation scripts and runbooks (covered by DEL-07-03)
- Non-macOS platform support (explicitly out per DEC-PLAT-001)
- Any non-local repository dependency for execution (per OBJ-008)

## Requirements

### REQ-01: Frontend Workspace Existence

The `frontend/` directory MUST exist as a tracked directory in the repository.

- `frontend/package.json` MUST be present and valid.
- The directory MUST be under version control (git-tracked).

Source: PLAN.md Section 2 FE-1 acceptance criteria; SOW-044

### REQ-02: Package Manifest Completeness

`frontend/package.json` MUST declare all dependencies required for:
- Next.js framework operation
- Electron desktop shell operation
- TypeScript compilation

All dependencies MUST be installable via `npm install` from the `frontend/` directory without referencing non-local repositories other than the public npm registry.

The `package.json` SHOULD declare a minimum Node.js version via the `engines` field. **ASSUMPTION (best-effort): Node.js >= 20 LTS is the expected baseline given macOS 15+ / Apple Silicon constraint and modern framework requirements (see Guidance C6). Specific version TBD -- human or architect ruling needed.**

Source: SOW-044; OBJ-008 acceptance criteria; Guidance C6 (Node.js version rationale)

### REQ-03: TypeScript Configuration

A `tsconfig.json` MUST be present in `frontend/` with configuration suitable for Next.js + Electron TypeScript compilation.

Source: SOW-044 ("TypeScript/Next/Electron scaffolding")

### REQ-04: Next.js Configuration

A Next.js configuration file (`next.config.js`, `next.config.mjs`, or `next.config.ts`) MUST be present in `frontend/` with:
- Output mode appropriate for Electron packaging (e.g., `output: 'export'` or equivalent for static export, or server mode if using custom server) -- **ASSUMPTION: specific output mode TBD based on Electron integration pattern. Resolution criteria: if DEL-03-07 (Harness API Baseline) requires server-side API routes (`POST /api/harness/session/*`, `POST /api/harness/turn`), a custom server approach is likely needed; if only static rendering is required, `output: 'export'` is sufficient. See Guidance C1 for trade-off analysis. Human or architect ruling required before implementation.**
- Any necessary configuration for Electron compatibility

Source: SOW-044 ("build config"); Guidance C1 (integration pattern trade-offs)

### REQ-05: Electron Main Process

An Electron main process entry point MUST exist in the `frontend/` workspace that:
- Launches a BrowserWindow loading the Next.js application
- Supports development mode (loading from dev server)
- Supports production mode (loading from built output)

Source: SOW-044 ("Electron scaffolding"); SOW-001 ("Electron + Next.js desktop application")

### REQ-06: Development Scripts

The following npm scripts MUST be defined in `frontend/package.json` and resolve successfully:

| Script | Purpose | Acceptance |
|--------|---------|------------|
| `npm run dev` | Start development server with hot reload | Resolves from `frontend/` without referencing non-local repos |
| `npm run build` | Produce production build output | Resolves from `frontend/` without referencing non-local repos |

Source: PLAN.md Section 2 FE-1 acceptance criteria

### REQ-07: Desktop Packaging Scripts

The following npm scripts MUST be defined in `frontend/package.json`:

| Script | Purpose | Acceptance |
|--------|---------|------------|
| `desktop:pack` | Create unpacked distributable for local testing | Produces unpacked app directory |
| `desktop:dist` | Create distributable `.dmg` artifact | Produces `.dmg` file for macOS |

Source: PLAN.md Section 2 FE-4 acceptance criteria; SOW-047

### REQ-08: Target Platform Constraints

All build and packaging artifacts MUST target:
- macOS 15+ (Sequoia or later)
- Apple Silicon (arm64) architecture only
- Signing and notarization are NOT required

Source: Decomposition DEC-PLAT-001

### REQ-09: Instruction Root Inclusion in Packaging Artifacts

Packaging scripts (`desktop:pack`, `desktop:dist`) MUST include the instruction root in build artifacts. Specifically:
- The `agents/` directory MUST be present in the packaged application
- The `docs/` directory MUST be present in the packaged application
- A verification check MUST confirm inclusion after packaging

**ASSUMPTION:** The specific mechanism for inclusion (e.g., electron-builder `extraResources`, `extraFiles`, or custom copy step) is TBD. The requirement is that the instruction root content is accessible from within the packaged application at runtime.

Source: SOW-047; SOW-013 (instruction root vs working root separation)

### REQ-10: No Non-Local Repository Dependency

The `frontend/` workspace MUST NOT require cloning, linking, or referencing any external repository for execution. All source code, configuration, and build scripts needed for `npm run dev`, `npm run build`, `desktop:pack`, and `desktop:dist` MUST reside within this repository.

**Note:** Standard npm registry dependencies (downloaded via `npm install`) are permitted. The constraint prohibits dependencies on other git repositories, monorepo links to external workspaces, or similar non-local source dependencies.

Source: OBJ-008 acceptance criteria; PLAN.md Local-Only Source Policy

### REQ-11: Electron Builder Configuration

An electron-builder configuration MUST be present (in `package.json` or a separate config file) specifying:
- macOS as the target platform
- arm64 as the target architecture
- `.dmg` as a distributable target
- Instruction-root directories as extra resources

**ASSUMPTION:** electron-builder is the assumed packaging tool. If a different tool is selected (e.g., `electron-forge`, see Guidance C2 for alternatives), the equivalent configuration requirements apply. **Resolution criteria: confirm tool selection before implementation. If electron-builder is confirmed, remove this assumption qualifier and treat REQ-11 as a binding obligation. If an alternative is chosen, update this requirement to reflect the selected tool's equivalent configuration fields.** Human or architect ruling required.

Source: SOW-047; DEC-PLAT-001; Guidance C2 (tool alternatives)

### REQ-12: Electron Preload Script

An Electron preload script MUST exist in the `frontend/` workspace (e.g., `frontend/electron/preload.ts`) that:
- Is referenced by the Electron main process BrowserWindow configuration via the `preload` property
- Enables `contextIsolation` security best practice by serving as the bridge between main and renderer processes

**ASSUMPTION:** The preload script is needed for Electron security best practices (`contextIsolation: true`, `nodeIntegration: false`). See Guidance C7 for security rationale.

The preload script content MAY be minimal at bootstrap scope (e.g., an empty or near-empty file), but the file MUST exist and be correctly wired.

Source: Specification Documentation - Required Artifacts (lists "Electron preload file"); Procedure Step 1.7; Electron security best practices (Guidance C7)

## Standards

| Standard/Tool | Relevance | Version Constraint | Accessibility |
|---------------|-----------|-------------------|---------------|
| Node.js | JavaScript runtime | >= 20 LTS (**ASSUMPTION -- TBD, human ruling needed**) | Public documentation |
| Next.js framework conventions | Application framework for frontend | **TBD -- pin to specific major version before implementation** | Public documentation; `location TBD` for specific version |
| Electron framework conventions | Desktop shell framework | **TBD -- pin to specific major version before implementation** | Public documentation; `location TBD` for specific version |
| TypeScript compiler configuration | Type system and compilation | (compatible with chosen Next.js + Electron versions) | Public documentation |
| electron-builder conventions | Packaging and distribution tool | **TBD -- pin to specific version** | Public documentation; **ASSUMPTION: tool selection** |
| npm workspace conventions | Package management | (bundled with Node.js) | Public documentation |
| `docs/SPEC.md` | Chirality physical structure spec (instruction root layout, deliverable folder layout) | -- | `docs/SPEC.md` (accessible) |
| `docs/CONTRACT.md` | Invariant catalog (K-* invariants) | -- | `docs/CONTRACT.md` (`location TBD` -- not read in this pass) |

**Note on version pinning:** Without pinned major versions for Next.js, Electron, and electron-builder, compliance determination lacks fixed baselines. The implementer or architect SHOULD pin these before implementation begins. (Source: _SEMANTIC_LENSING.md A-003; Specification Standards table)

## Verification

| Requirement | Verification Approach | Expected Result |
|-------------|----------------------|-----------------|
| REQ-01 | Check `frontend/` exists and is git-tracked; check `frontend/package.json` exists | Directory and file present in tracked tree |
| REQ-02 | Run `npm install` in `frontend/`; verify exit code 0 | Dependencies install without error |
| REQ-03 | Check `frontend/tsconfig.json` exists; run `npx tsc --noEmit` | No type errors on baseline scaffolding |
| REQ-04 | Check Next.js config file exists in `frontend/`; verify output mode setting is present and consistent with the chosen Electron integration pattern (see Guidance C1). If output mode is still TBD, verify the config file exists with a placeholder and note the TBD in verification results | Config file present; output mode setting present and consistent with integration pattern (or explicitly marked TBD) |
| REQ-05 | Check Electron main process entry point exists; verify it (a) imports `electron` and creates a `BrowserWindow`, (b) includes a dev-mode code path that loads from a dev server URL (e.g., `http://localhost:*`), and (c) includes a production-mode code path that loads from the built output path. Both mode paths must be present and testable | Entry point file present with BrowserWindow creation, dev-mode URL loading, and production-mode file loading as distinct verifiable code paths |
| REQ-06 | Run `npm run dev` from `frontend/` (verify startup); run `npm run build` (verify exit code 0) | Both commands resolve and complete |
| REQ-07 | Run `desktop:pack` and `desktop:dist` from `frontend/`; verify output artifacts | Unpacked app directory and `.dmg` file produced |
| REQ-08 | Inspect electron-builder config for platform/arch targets; inspect output binary architecture | arm64 macOS binary produced |
| REQ-09 | After `desktop:pack`, inspect output directory for `agents/` and `docs/` presence | Instruction root directories present in packaged output |
| REQ-10 | Grep `package.json` for `git+`, `file:../`, `link:` or similar non-local references; attempt build in clean checkout | No non-local repo references; clean checkout builds |
| REQ-11 | Inspect electron-builder configuration for required fields | Configuration present with macOS/arm64/.dmg/extraResources settings |
| REQ-12 | Check preload script exists (e.g., `frontend/electron/preload.ts`); verify BrowserWindow configuration references it via `preload` property; verify `contextIsolation: true` and `nodeIntegration: false` are set | Preload script present and correctly wired in BrowserWindow configuration |

## Documentation

### Required Artifacts

| Artifact | Type | Description |
|----------|------|-------------|
| `frontend/package.json` | CONFIG | Package manifest with dependencies and scripts |
| `frontend/tsconfig.json` | CONFIG | TypeScript compiler configuration |
| `frontend/next.config.*` | CONFIG | Next.js framework configuration |
| Electron main process file | CODE | Main process entry point (e.g., `frontend/electron/main.ts` or similar) |
| Electron preload file | CODE | Preload script for renderer security (**ASSUMPTION: needed for Electron best practices**) |
| electron-builder config | CONFIG | Packaging configuration (in `package.json` `"build"` key or separate file) |
| `frontend/src/app/` | CODE | Next.js App Router application scaffolding (layout, pages/routes). Uses the `src/` prefix convention per Guidance Vocabulary Notes |
| `frontend/.gitignore` | CONFIG | Git ignore rules for `node_modules/`, build output directories (`.next/`, `out/`, `dist/`), and other generated files. Required to ensure REQ-01 (git-tracked workspace) does not include transient artifacts |
| Deliverable document kit | DOC | This Datasheet, Specification, Guidance, and Procedure |

### Downstream Consumers

These deliverables are expected to consume artifacts produced by DEL-01-03:

| Consumer | What It Needs | Source |
|----------|---------------|--------|
| DEL-01-01 (macOS Build Baseline) | Working `frontend/` with buildable code | Decomposition PKG-01; **ASSUMPTION: implicit dependency** |
| DEL-01-02 (Unsigned DMG Packaging) | Working packaging scripts | Decomposition PKG-01; **ASSUMPTION: implicit dependency** |
| DEL-02-05 (Frontend Workflow Shell) | Baseline `frontend/` workspace to build UI into | Decomposition Scope Amendment A1 |
| DEL-03-07 (Harness API Baseline) | Baseline `frontend/` workspace for API route development | Decomposition Scope Amendment A1 |
| DEL-07-03 (Frontend Validation) | Baseline `frontend/` workspace for validation scripts | Decomposition Scope Amendment A1 |
