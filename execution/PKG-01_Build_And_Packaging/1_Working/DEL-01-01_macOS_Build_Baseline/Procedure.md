# Procedure -- DEL-01-01 macOS 15+ Apple Silicon Build Baseline

## Purpose

This procedure describes the steps to produce and verify the macOS 15+ / Apple Silicon build baseline for the Chirality App. It covers both the development build and production build workflows, and the verification checks that confirm the build meets requirements.

**Interpretation note:** This procedure describes steps to **produce** the deliverable (i.e., establish and verify the build baseline). Once the baseline is established, the build commands themselves become the operational procedure for day-to-day development.

## Prerequisites

### Environment

| Prerequisite | Requirement | Status |
|-------------|-------------|--------|
| Operating System | macOS 15+ (Sequoia or later) | Required |
| Hardware | Apple Silicon (M1, M2, M3, M4 series or later) | Required |
| Xcode Command Line Tools | Version compatible with macOS 15 SDK (TBD: specific version -- resolve via Apple developer documentation or macOS 15 SDK release notes; see Lensing A-003 and Guidance C3) | Required |
| Node.js | TBD (version must be compatible with the project's Electron version; resolve via repo `package.json` `engines` field or `.node-version`) | Required |
| Package Manager | TBD (npm, yarn, or pnpm as used by the repo; resolve via lockfile detection) | Required |
| Git | Standard installation | Required |

### Upstream Dependencies

| Dependency | Source | Status |
|-----------|--------|--------|
| Repository source code | Git repository | Available |
| Upstream deliverable dependencies | None declared (_DEPENDENCIES.md is PENDING_EXTRACTION; see Guidance C9) | TBD -- resolve via DEPENDENCIES agent or ORCHESTRATOR |

### Reference Materials

| Reference | Purpose |
|-----------|---------|
| Decomposition (G7-APPROVED) | Deliverable scope, platform decisions |
| docs/DIRECTIVE.md | Structural constraints, network policy |
| docs/PLAN.md | Existing tooling description |
| Specification.md (this deliverable) | Requirements to verify against |

## Steps

### Phase 1: Environment Setup

**Step 1.1 -- Verify Target Platform**

Confirm the build machine meets platform requirements.

- [ ] macOS version is 15.0 or later: `sw_vers -productVersion`
- [ ] Architecture is arm64: `uname -m` (expect `arm64`)
- [ ] Xcode Command Line Tools installed: `xcode-select -p`

**Step 1.2 -- Verify Toolchain**

Confirm required development tools are installed.

- [ ] Node.js installed and version recorded: `node --version`
- [ ] Package manager installed and version recorded: TBD (`npm --version` / `yarn --version` / `pnpm --version`)
- [ ] Git installed: `git --version`

**Step 1.3 -- Clone / Access Repository**

- [ ] Repository is accessible and up to date on the target branch.

### Phase 2: Dependency Installation

**Step 2.1 -- Install Node.js Dependencies**

- [ ] Run package install command (TBD: `npm install` / `yarn install` / `pnpm install`)
- [ ] Confirm no architecture-related errors (no `node-gyp` failures for arm64)
- [ ] If native modules fail: troubleshoot arm64 compatibility (see Guidance C2; see also Phase 8 Failure Recovery)

**Step 2.2 -- Verify Native Module Compatibility**

- [ ] List native modules (TBD: method depends on tooling)
- [ ] Confirm each native module has arm64 / macOS 15+ support
- [ ] If `electron-rebuild` or equivalent is needed, run it and record results

### Phase 3: Development Build

**Step 3.1 -- Start Development Build**

- [ ] Execute the development start command (TBD: e.g., `npm run dev`)
- [ ] Confirm the Electron application window opens
- [ ] Confirm the Next.js frontend renders in the application window (not a blank or error page; initial route content is visible)
- [ ] Confirm no fatal errors in terminal output or Electron DevTools console
- [ ] If hot-reload (HMR) is supported by the repo's dev server: confirm a source file change triggers an in-place reload without requiring a full restart (ASSUMPTION: depends on repo's current dev server configuration; see Lensing X-002)

**Step 3.2 -- Verify Development Build Functionality**

- [ ] Application allows selection of a working root (`projectRoot`)
- [ ] Basic navigation works (PORTAL/PIPELINE views render)
- [ ] Application responds to user input without crashes

**REQ-BUILD-001 verification point:** If Steps 3.1-3.2 pass, REQ-BUILD-001 is satisfied.

### Phase 4: Production Build

**Step 4.1 -- Execute Production Build**

- [ ] Run the production build command (TBD: e.g., `npm run build` or equivalent Electron build script)
- [ ] Confirm build completes without errors
- [ ] Locate the output `.app` bundle (TBD: path depends on build tooling)

**Step 4.2 -- Verify Production Binary Architecture**

- [ ] Check architecture of the main binary: `file path/to/Chirality.app/Contents/MacOS/*` or `lipo -info path/to/binary`
- [ ] Confirm output includes `arm64`

**REQ-BUILD-003 verification point.**

**Step 4.3 -- Launch Production Build**

- [ ] Double-click or `open` the built `.app` bundle
- [ ] If macOS Gatekeeper blocks the unsigned application: right-click the `.app` bundle > Open (this is expected for unsigned builds; see Guidance C8 for rationale)
- [ ] Confirm the application launches (main window renders: Electron window visible with Next.js page content)
- [ ] Confirm no fatal errors

**REQ-BUILD-002 verification point.**

**Step 4.4 -- Verify Instruction Root Presence**

- [ ] Navigate into the `.app` bundle: `ls path/to/Chirality.app/Contents/Resources/`
- [ ] Confirm instruction root files are present (TBD: exact file list depends on build configuration)

**REQ-BUILD-007 verification point.**

### Phase 5: Build Configuration Audit

**Step 5.1 -- Verify macOS Deployment Target**

- [ ] Inspect build configuration for macOS deployment target setting
- [ ] Confirm target is >= 15.0

**REQ-BUILD-004 verification point.**

**Step 5.2 -- Verify Network Configuration**

- [ ] Check Electron main process code for auto-updater module: confirm no `autoUpdater` import/instantiation, or confirm it is explicitly disabled
- [ ] Check Next.js telemetry: confirm `NEXT_TELEMETRY_DISABLED=1` in environment or `next telemetry disable` has been run
- [ ] Check `package.json` scripts for any post-install or startup network calls
- [ ] Check for any other outbound network endpoints in build configuration

**REQ-BUILD-006 verification point.**

**Step 5.3 -- Verify Native Dependency Resolution**

- [ ] Perform a clean install (delete `node_modules`, reinstall)
- [ ] Confirm all native modules resolve without architecture errors

**REQ-BUILD-005 verification point.**

**Step 5.4 -- Verify Filesystem-as-State Constraint (Lensing C-001)**

- [ ] Review build configuration and application entry point for database driver imports (e.g., `sqlite3`, `better-sqlite3`, `pg`, `mysql2`, `mongoose`, `prisma`)
- [ ] Review for ORM imports or external state store connections
- [ ] Confirm no database dependencies are included in the production build
- [ ] If any are found: determine whether they are dead code excluded from the build or active dependencies (escalate if active)

**REQ-BUILD-009 verification point.**

### Phase 6: Documentation

**Step 6.1 -- Document Build Procedure**

- [ ] Record all prerequisites (exact versions of Node.js, Xcode, package manager)
- [ ] Record all build commands (development and production)
- [ ] Record any non-obvious configuration steps
- [ ] Record known issues or workarounds (including Gatekeeper bypass for unsigned builds)

**Step 6.2 -- Verify Reproducibility**

- [ ] Have a second operator (or clean environment per REQ-BUILD-008 definition) follow the documented steps
- [ ] Clean environment means: documented prerequisites installed, no pre-existing `node_modules/`, build output directories (`.next/`, `dist/`, `out/`), or project-specific caches
- [ ] Confirm build succeeds without undocumented manual intervention

**REQ-BUILD-008 verification point.**

### Phase 7: Post-Build Artifact Management (Lensing F-002)

**Step 7.1 -- Label and Store Build Output**

- [ ] Record the `.app` bundle output path
- [ ] Label the build output with version information (TBD: versioning convention -- e.g., `Chirality-<version>-arm64.app` or as determined by build tooling)
- [ ] If the `.app` bundle is to be retained for DEL-01-02 (DMG packaging), move or copy it to a known staging location (TBD: convention)

**Step 7.2 -- Clean Intermediate Artifacts**

- [ ] Identify intermediate build artifacts (e.g., `.next/` output, `dist/` staging, temporary build directories)
- [ ] Determine which artifacts should be retained (for debugging or DEL-01-02 input) vs. cleaned
- [ ] Document the cleanup convention

**Step 7.3 -- Archive Build Evidence**

- [ ] Store build logs (dev and prod) per the Records table below
- [ ] Store architecture verification output
- [ ] Confirm all records are accessible for downstream audit

### Phase 8: Failure Recovery (Lensing C-002)

This phase describes recovery actions when build steps fail. It is not executed sequentially but referenced as needed during Phases 2-4.

**8.1 -- Dependency Installation Failure**

If Step 2.1 fails with native module compilation errors:
1. Check the error output for the specific module name and failure reason.
2. Verify Xcode Command Line Tools version is compatible (see Guidance C3).
3. Try `electron-rebuild` (or equivalent) to recompile native modules against Electron's Node.js headers.
4. If a specific module lacks arm64 support: check for an updated version, an alternative module, or file an issue. Document the finding.
5. If the failure persists: perform a clean slate recovery (delete `node_modules/`, clear npm/yarn/pnpm cache, reinstall).

**8.2 -- Development Build Failure**

If Step 3.1 fails (application does not start):
1. Check terminal output for error messages; record the full error.
2. Verify Node.js version compatibility with the project's Electron version.
3. Check for port conflicts (if the dev server uses a specific port).
4. Try a clean reinstall of dependencies (Phase 8.1, step 5).
5. If the failure is macOS 15-specific: check for known Electron issues with macOS 15 and document the finding.

**8.3 -- Production Build Failure**

If Step 4.1 fails (build does not complete):
1. Check build output for the specific error.
2. Verify build tooling configuration (electron-builder/electron-forge config) is correct for arm64 / macOS 15+.
3. Check for missing build dependencies (e.g., `dmg-license`, platform-specific native tools).
4. Try building with verbose logging enabled to capture additional detail.
5. If the failure is architecture-related: verify the build target is explicitly set to `arm64` in the build configuration.

**8.4 -- Production `.app` Bundle Launch Failure**

If Step 4.3 fails (`.app` bundle does not launch):
1. Check Console.app for crash reports or launch errors.
2. Verify the `.app` bundle is not quarantined: `xattr -l path/to/Chirality.app` (remove quarantine with `xattr -cr path/to/Chirality.app` if needed).
3. Check code signing status: `codesign -dvvv path/to/Chirality.app` (unsigned is expected; this checks for corrupted signatures).
4. Try launching from terminal: `open path/to/Chirality.app` or `path/to/Chirality.app/Contents/MacOS/Chirality` to see stdout/stderr output.

## Verification

### Summary Verification Matrix

| Requirement | Verification Step | Pass Criteria |
|-------------|------------------|---------------|
| REQ-BUILD-001 | Steps 3.1-3.2 | Dev build starts; main window renders (Electron window visible with Next.js content); no fatal errors |
| REQ-BUILD-002 | Step 4.3 | Production `.app` bundle launches; main window renders (same threshold as REQ-BUILD-001) |
| REQ-BUILD-003 | Step 4.2 | Binary includes `arm64` |
| REQ-BUILD-004 | Step 5.1 | Deployment target >= 15.0 |
| REQ-BUILD-005 | Steps 2.1-2.2, 5.3 | Clean install succeeds; no arch errors |
| REQ-BUILD-006 | Step 5.2 | No auto-updater import/instantiation; telemetry disabled; no unexpected outbound endpoints in config |
| REQ-BUILD-007 | Step 4.4 | Instruction root files present in `.app` bundle |
| REQ-BUILD-008 | Steps 6.1-6.2 | Documented steps reproduce the build on clean environment (per definition) |
| REQ-BUILD-009 | Step 5.4 | No database drivers, ORM, or external state store connections in build |

## Records

Upon completion, the following records should exist:

| Record | Description | Location |
|--------|-------------|----------|
| Build log (dev) | Terminal output of development build | `{DELIVERABLE_FOLDER}/records/build-log-dev.txt` (TBD: confirm convention with team; Lensing X-004) |
| Build log (prod) | Terminal output of production build | `{DELIVERABLE_FOLDER}/records/build-log-prod.txt` (TBD: confirm convention with team; Lensing X-004) |
| Architecture verification | Output of `file` or `lipo -info` on production binary | `{DELIVERABLE_FOLDER}/records/arch-verification.txt` (TBD: confirm convention with team; Lensing X-004) |
| Build procedure document | Documented prerequisites + steps | CODE/DOC artifact within deliverable scope |
| Environment specification | Exact versions of macOS, Xcode, Node.js, package manager | Included in build procedure document |
| Verification checklist | Completed checklist (this procedure with checkboxes marked) | This document, updated during execution |
