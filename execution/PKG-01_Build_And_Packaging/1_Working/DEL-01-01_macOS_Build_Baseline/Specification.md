# Specification -- DEL-01-01 macOS 15+ Apple Silicon Build Baseline

## Scope

### Included

This deliverable covers making the Chirality App repository build and run reliably on macOS 15+ and Apple Silicon, in both development and production build modes.

- Development build: the application starts in development mode on macOS 15+ / Apple Silicon and is usable for iterative development.
- Production build: the application compiles to a runnable `.app` bundle targeting arm64 / macOS 15+.
- Build configuration: all build scripts, configuration files, and dependency settings necessary for reliable macOS 15+ / Apple Silicon builds.

Source: _CONTEXT.md description; Decomposition DEL-01-01 entry; SOW-001.

### Excluded

- `.dmg` packaging and distribution workflow (covered by DEL-01-02).
- Code signing and notarization (excluded per DEC-PLAT-001).
- Cross-platform builds (Windows, Linux, Intel Mac) -- platform scope is Apple Silicon + macOS 15+ only per DEC-PLAT-001.
- Runtime behavior of the harness (sessions, turns, streaming) -- covered by PKG-03 deliverables.
- UI functionality -- covered by PKG-02 deliverables.

## Requirements

### REQ-BUILD-001: Development Build Executes on macOS 15+ / Apple Silicon

The development build command (TBD: e.g., `npm run dev`) MUST start the Electron + Next.js application successfully on a macOS 15+ system running on Apple Silicon.

- **Verification:** Manual or scripted execution on target platform; confirm application window opens, Next.js frontend renders, and no fatal errors appear in terminal or DevTools console.
- **Acceptance threshold (Lensing X-003):** "Main window renders" means the Electron BrowserWindow is visible and the Next.js page content is displayed (not a blank or error page). At minimum, the application chrome and initial route content must be present. Specific UI element requirements are outside this deliverable's scope (see PKG-02).
- **Hot-reload note (Lensing X-002):** If the existing repo's development build supports hot-reload (HMR), verification SHOULD confirm that HMR functions without requiring a full restart. If the repo does not currently implement HMR, this is not a blocking requirement for DEL-01-01, but should be noted as a gap for future consideration. ASSUMPTION: hot-reload expectations depend on repo's current dev server configuration.
- **Source:** SOW-001; OBJ-001 acceptance ("Builds and runs on Apple Silicon Macs running macOS 15+").

### REQ-BUILD-002: Production Build Produces Runnable Application

The production build process MUST produce a macOS `.app` bundle that launches and functions on macOS 15+ / Apple Silicon without requiring code signing or notarization.

- **Verification:** Build the production target; launch the resulting `.app` bundle; confirm main window renders (same acceptance threshold as REQ-BUILD-001).
- **Source:** SOW-001; OBJ-001 acceptance; DEC-PLAT-001 ("signing/notarization not required").

### REQ-BUILD-003: Architecture Target is arm64 Only

The build MUST target `arm64` (Apple Silicon). Universal binaries (arm64 + x86_64) are acceptable but not required. Intel-only (x86_64) builds do not satisfy this requirement.

- **Verification:** Inspect the built binary architecture (e.g., `file` or `lipo -info`).
- **Source:** DEC-PLAT-001 ("Apple Silicon only").

### REQ-BUILD-004: macOS Deployment Target is 15.0+

The build configuration MUST set the macOS deployment target to 15.0 or later. The resulting application MUST NOT require features or frameworks unavailable on macOS 15.

- **Verification:** Check build configuration for deployment target; test launch on macOS 15.
- **Source:** DEC-PLAT-001 ("macOS 15+").

### REQ-BUILD-005: Native Dependencies Resolve for arm64

All native Node.js modules and binary dependencies MUST resolve and compile (or be available as prebuilt binaries) for arm64 / macOS 15+.

- **Verification:** Clean install + build with no architecture-related errors.
- **Source:** ASSUMPTION: standard requirement for Apple Silicon Electron builds. Specific native modules are TBD pending repo dependency audit.

### REQ-BUILD-006: No Unauthorized Outbound Network in Built Application

The built application MUST NOT make outbound network connections except to the Anthropic API. This includes no telemetry, no auto-update checks, and no analytics endpoints.

- **Verification:** Review Electron main process configuration for auto-updater module presence or activation; confirm auto-updater is disabled or absent. Review Next.js configuration for telemetry opt-out (`NEXT_TELEMETRY_DISABLED=1` or `next telemetry disable`). Review `package.json` scripts and build configuration for any post-install or startup network calls. (Lensing F-001: specify that a "passing review" means no auto-updater import/instantiation in main process code and no telemetry-enabled flags in Next.js config. The specific tool or method for deeper network audit is TBD; minimal build-time check is configuration review as described.)
- **Source:** DEC-NET-001 ("Outbound internet access is permitted only for Anthropic API calls").
- **Note:** Full network guardrail implementation and runtime proof is DEL-03-06's scope; this deliverable ensures the build configuration does not introduce unauthorized outbound connections (e.g., Electron auto-updater, Next.js telemetry). The scope boundary between DEL-01-01 (build-time config review) and DEL-03-06 (runtime egress enforcement + proof) is intentional.

### REQ-BUILD-007: Instruction Root / Working Root Separation Preserved

The production build MUST preserve the separation of instruction root (release-managed content bundled inside the `.app` bundle) and working root (user-selected `projectRoot`). The build process MUST NOT merge, flatten, or omit the instruction root contents.

- **Verification:** Inspect the built `.app` bundle to confirm instruction root files are present and accessible at runtime.
- **Source:** DIRECTIVE Section 2.6; SOW-013 (primary owner is DEL-05-01, but build must not break this contract).

### REQ-BUILD-008: Build Process is Documented and Repeatable

The build process MUST be documented with clear steps sufficient for a developer to reproduce the build on a clean macOS 15+ / Apple Silicon machine. Build scripts SHOULD be idempotent.

- **Verification:** Follow documented steps on a clean environment; build succeeds.
- **Clean environment definition (Lensing D-001):** "Clean environment" means a macOS 15+ / Apple Silicon machine with only the documented prerequisites installed (Xcode CLT, Node.js, package manager, Git) and no pre-existing `node_modules`, build caches, or project-specific global installations. This does NOT require a fresh OS install or fresh user account -- it requires that no undocumented project state from a previous build attempt is present. At minimum: delete `node_modules/`, any build output directories (e.g., `.next/`, `dist/`, `out/`), and any local caches before following documented steps.
- **Source:** Anticipated artifacts include SCRIPT and DOC (_CONTEXT.md); DIRECTIVE Section 2.4 ("Evidence Over Plausibility").

### REQ-BUILD-009: Filesystem-as-State Constraint Verified at Build Time (Lensing C-001)

The build configuration and application startup MUST NOT introduce external database dependencies, server-side state stores, or any state persistence mechanism other than the local filesystem. This requirement operationalizes the Datasheet Condition "Filesystem-as-State" as a verifiable build-time constraint.

- **Verification:** Review build configuration and application entry point for database drivers, ORM imports, or external state store connections. Confirm none are present or that any detected instances are dead code excluded from the build.
- **Source:** DIRECTIVE Section 2.1; DIRECTIVE Section 5 (Structural Constraints); Datasheet Conditions table (Filesystem-as-State row).
- **Note:** ASSUMPTION: this requirement is derived from the Datasheet Condition which lacked a corresponding verification path (identified by Lensing C-001). Runtime enforcement of filesystem-as-state is a broader architectural concern addressed across multiple deliverables.

## Standards

| Standard / Convention | Applicability | Source | Location |
|----------------------|---------------|--------|----------|
| Electron build best practices (arm64 / macOS) | Build configuration and native module handling | ASSUMPTION: industry standard for Electron + Apple Silicon | location TBD |
| Next.js build conventions | Build output configuration for Electron embedding | ASSUMPTION: standard Next.js + Electron integration pattern | location TBD |
| macOS code signing policy (opt-out) | Signing is not required per project decision | DEC-PLAT-001 | Decomposition, Decision Log |
| Chirality network policy | Anthropic-only outbound connections | DEC-NET-001 | Decomposition, Decision Log |

## Verification

| Requirement | Verification Method | Pass Criteria |
|-------------|-------------------|---------------|
| REQ-BUILD-001 | Execute dev build on macOS 15+ / Apple Silicon | Application starts; main window renders (Electron window visible with Next.js page content -- not blank/error); no fatal errors |
| REQ-BUILD-002 | Build production target; launch `.app` bundle | `.app` bundle launches and main window renders (same threshold as REQ-BUILD-001) |
| REQ-BUILD-003 | `file` or `lipo -info` on built binary | Output includes `arm64` |
| REQ-BUILD-004 | Inspect build config; test on macOS 15 | Deployment target >= 15.0; launches on macOS 15 |
| REQ-BUILD-005 | Clean `npm install` + build | No architecture-related build errors |
| REQ-BUILD-006 | Review Electron main process for auto-updater; review Next.js telemetry config; review `package.json` scripts | No auto-updater import/instantiation; telemetry disabled; no unexpected outbound endpoints in config |
| REQ-BUILD-007 | Inspect `.app` bundle contents | Instruction root files present and accessible |
| REQ-BUILD-008 | Follow documented build steps on clean environment (per definition above) | Build succeeds without undocumented manual steps |
| REQ-BUILD-009 | Review build config and app entry point for DB/ORM/external state imports | No database drivers, ORM, or external state store connections present in build |

## Documentation

### Required Artifacts (from Anticipated Artifacts)

| Artifact Type | Description | Status |
|---------------|-------------|--------|
| CODE | Build-related source changes (scripts, configs) | TBD |
| CONFIG | Build configuration files (Electron builder config, Next.js config, `package.json` build targets) | TBD |
| SCRIPT | Build scripts (dev start, production build) | TBD |
| DOC | Build procedure documentation (setup, prerequisites, commands, verification) | TBD |
