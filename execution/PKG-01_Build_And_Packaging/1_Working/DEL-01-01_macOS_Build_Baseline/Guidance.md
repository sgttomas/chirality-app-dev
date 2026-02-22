# Guidance -- DEL-01-01 macOS 15+ Apple Silicon Build Baseline

## Purpose

This deliverable exists to establish a reliable, repeatable build baseline for the Chirality App on macOS 15+ / Apple Silicon. Without a working build, no other deliverable in the project can be verified or delivered. DEL-01-01 is foundational infrastructure.

The Chirality App is an Electron + Next.js desktop application that serves as a harness for running AI agents against a user-selected filesystem working directory. The build baseline must produce a functioning application in both development and production modes on the target platform.

Source: Decomposition DEL-01-01 entry; _CONTEXT.md; PLAN Section 2.

## Principles

### P1: Platform Narrowing is a Feature, Not a Limitation

DEC-PLAT-001 explicitly narrows the platform target to macOS 15+ / Apple Silicon only. This is a deliberate project decision that reduces build matrix complexity, eliminates cross-compilation concerns, and allows the team to focus on a single, well-defined target.

**Implication:** Do not introduce universal binary support, Windows/Linux compatibility layers, or Intel fallback paths. These would widen scope beyond this deliverable and beyond the project's current platform decision.

Source: DEC-PLAT-001 (Decomposition, Decision Log).

### P2: Build Simplicity Over Build Sophistication

The project is a desktop application for professional use by self-builders (operators who build from source or install a provided `.dmg`). The build system should be as simple as the application allows -- standard tooling, minimal custom build steps, documented prerequisites.

Source: ASSUMPTION: derived from DEC-PLAT-001 ("self-builder installs") and DIRECTIVE Section 2.4 (Evidence Over Plausibility).

### P3: No Ghost Inputs in the Build

The build process should not depend on undocumented environment variables, global tool installations, or implicit system state. All build prerequisites and steps should be explicit and documented.

Source: DIRECTIVE Section 2.4 (Evidence Over Plausibility); CONTRACT K-GHOST-1 concept (no ghost inputs) -- applied here by analogy to build reproducibility.

### P4: Network Policy Starts at Build Time

The Anthropic-only outbound network policy (DEC-NET-001) has build-time implications. Electron's default configuration may include auto-update checks and telemetry. Next.js has its own telemetry. These must be disabled or configured during build setup, not patched after the fact.

Source: DEC-NET-001 (Decomposition, Decision Log).

## Considerations

### C1: Electron + Next.js Integration Pattern

Electron applications embedding Next.js have multiple integration approaches (e.g., standalone export, custom server, or framework-specific Electron adapters). The chosen pattern affects build configuration, hot-reload in development, and production bundling.

**Current state:** The repo already has an Electron + Next.js desktop application per PLAN Section 2. This deliverable should preserve and verify the existing integration pattern rather than replacing it.

**Risk:** If the existing integration pattern has macOS 15+ or arm64 compatibility issues, this deliverable must identify and resolve them.

Source: PLAN Section 2 ("Next.js + Electron desktop app").

### C2: Native Module Compatibility

Node.js native modules (compiled C/C++ addons) must be available for arm64 / macOS 15+. Common issues include:
- Modules with prebuilt binaries that do not include arm64 variants.
- Modules that require `node-gyp` compilation and may fail with Xcode version mismatches on macOS 15.
- Electron's Node.js version may differ from the system Node.js version, requiring `electron-rebuild` or equivalent.

**Current state:** The specific native modules in use are TBD (pending repo dependency audit). Once the audit is complete, a native module inventory should be added to the Datasheet Attributes table (see Lensing B-002).

Source: ASSUMPTION: standard concern for Electron + Apple Silicon builds.

### C3: macOS 15 SDK and Xcode Requirements

macOS 15+ builds may require a minimum Xcode version that ships with the macOS 15 SDK. Build documentation should specify the Xcode version requirement.

**Current state:** TBD. The minimum Xcode Command Line Tools version for macOS 15 SDK compatibility should be determined from Apple developer documentation or macOS 15 SDK release notes (Lensing A-003).

Source: ASSUMPTION: standard macOS development requirement.

### C4: Electron Auto-Updater

Electron's built-in auto-updater (`electron-updater` or `autoUpdater`) typically makes outbound network calls to check for updates. Per DEC-NET-001, this must be disabled or not included. If the project uses `electron-builder` with auto-update support, the auto-update module should be explicitly excluded or disabled.

Source: DEC-NET-001; ASSUMPTION: standard Electron behavior.

### C5: Next.js Telemetry

Next.js collects anonymous telemetry by default. This should be disabled in the build configuration (`NEXT_TELEMETRY_DISABLED=1` or `next telemetry disable`).

Source: DEC-NET-001; ASSUMPTION: standard Next.js behavior.

### C6: Instruction Root Preservation in Production Builds

The Chirality architecture separates the instruction root (release-managed agent instructions and framework docs shipped inside the `.app` bundle) from the working root (user-selected `projectRoot`). The build process must ensure that instruction root contents are correctly bundled into the application's resources directory and remain accessible at runtime. Build tooling that aggressively tree-shakes, minifies, or excludes non-code assets may inadvertently strip instruction root files.

**Current state:** The instruction root bundling mechanism is TBD pending examination of the existing build configuration. The primary owner of instruction root separation is DEL-05-01; this deliverable's responsibility is to ensure the build does not break the contract.

Source: DIRECTIVE Section 2.6; REQ-BUILD-007 (Specification.md).

### C7: Scope Boundary with DEL-01-02 (DMG Packaging)

This deliverable produces a working build (`.app` bundle that launches). The `.dmg` packaging, installer workflow, and distribution concerns belong to DEL-01-02. The boundary is: DEL-01-01 delivers a buildable, runnable application; DEL-01-02 wraps it for distribution.

Source: Decomposition DEL-01-01 vs. DEL-01-02 entries.

### C8: Unsigned Application Launch on macOS (Lensing E-002)

macOS Gatekeeper blocks unsigned applications by default. For self-builder installs (the target use case per DEC-PLAT-001), the standard workaround is right-click > Open or adjusting system security settings. This is acceptable because:

- The target audience is operators who build from source or install a provided `.dmg` -- they are technically capable users who understand unsigned app implications.
- DEC-PLAT-001 explicitly states "signing/notarization not required," which is a deliberate scope decision that trades distribution convenience for build simplicity.
- The Gatekeeper bypass is a one-time action per application; subsequent launches proceed normally.
- This is consistent with P1 (Platform Narrowing) and P2 (Build Simplicity) -- adding code signing would increase build complexity without serving the defined audience.

**Implication for Procedure:** The right-click > Open workaround should be documented as a known step in production build verification, not treated as an anomaly.

Source: DEC-PLAT-001 (Decomposition, Decision Log); OBJ-001 acceptance criteria ("signing/notarization not required").

### C9: Upstream Dependency Status (Lensing X-001)

The `_DEPENDENCIES.md` file for this deliverable is in `PENDING_EXTRACTION` status. It is currently unknown whether DEL-01-01 has true upstream deliverable dependencies or is genuinely dependency-free. The Procedure notes the repository source code as the primary input, with no declared upstream deliverable dependencies.

**Resolution path:** The DEPENDENCIES agent or ORCHESTRATOR should resolve this status. If DEL-01-01 is confirmed as dependency-free (plausible given it is foundational infrastructure), the Datasheet and Procedure should be updated accordingly. If upstream dependencies are identified, they should be added to the Prerequisites.

Source: _DEPENDENCIES.md (PENDING_EXTRACTION status); Lensing X-001.

## Trade-offs

### T1: arm64-Only vs. Universal Binary

| Option | Pros | Cons |
|--------|------|------|
| arm64-only | Simpler build; smaller binary; matches DEC-PLAT-001 exactly | Does not run on Intel Macs (acceptable per project decision) |
| Universal binary (arm64 + x86_64) | Runs on both architectures | Larger binary; more complex build; exceeds stated platform scope |

**Recommendation:** arm64-only, consistent with DEC-PLAT-001. Universal binary is not prohibited but adds scope without project justification.

Source: DEC-PLAT-001.

### T2: Electron Builder vs. Electron Forge vs. Other

The choice of Electron packaging tool affects build configuration, plugin ecosystem, and auto-update behavior. Common options:

| Tool | Notes |
|------|-------|
| electron-builder | Widely used; supports `.dmg`; auto-update built in (must be disabled per DEC-NET-001) |
| electron-forge | Electron's official toolchain; modular; supports multiple makers |
| Custom scripts | Maximum control; maximum maintenance burden |

**Recommendation:** TBD -- depends on what the repo currently uses. Preserve existing tooling unless it has a blocking incompatibility.

**Rationale gap (Lensing B-003):** Once the repo is examined and the packaging tool is identified, this section should be updated with: (a) which tool is in use, (b) why it was selected or why the existing choice is preserved, and (c) any DEC-NET-001 implications (e.g., if electron-builder is used, document how auto-update is disabled). This rationale is deferred until repo examination provides the necessary evidence.

Source: ASSUMPTION: standard Electron ecosystem options.

## Examples

Examples will be populated during WORKING_ITEMS execution when the actual repo build configuration is examined.

**Note (Lensing D-002):** Concrete build configuration snippets (e.g., `package.json` build targets, Electron builder config excerpts, Next.js config for Electron embedding) should be added here once the repo examination is complete. These examples would demonstrate how Principles P1-P4 and the trade-off decisions manifest in actual configuration. Currently TBD pending repo examination.

## Conflict Table (for human ruling)

No conflicts identified at this time. All sources are directionally consistent on platform target (macOS 15+ / Apple Silicon / unsigned) and network policy (Anthropic-only).
