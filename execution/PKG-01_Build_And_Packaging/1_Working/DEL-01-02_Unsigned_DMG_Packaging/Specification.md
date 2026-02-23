# Specification -- DEL-01-02 Unsigned DMG Packaging Workflow

## Scope

### What This Deliverable Covers

This deliverable produces a working `.dmg` packaging path for the Chirality desktop application such that a local builder (developer or operator) can:

1. Build the Electron + Next.js application on macOS 15+ / Apple Silicon.
2. Package the built application into an unsigned, unnotarized `.dmg` disk image.
3. Install and launch the application from the `.dmg`.

Source: Decomposition DEL-01-02 description; SOW-002; OBJ-001; DEC-PLAT-001.

### What This Deliverable Excludes

- **Code signing and notarization** -- explicitly excluded per DEC-PLAT-001.
- **Windows or Linux packaging** -- platform target is macOS only per DEC-PLAT-001.
- **Intel (x86_64) support** -- Apple Silicon only per DEC-PLAT-001.
- **The build baseline itself** -- ensuring the app builds and runs is DEL-01-01's scope (SOW-001). This deliverable assumes a working build exists.
- **Distribution infrastructure** -- no CDN, auto-update, or download service. Distribution model is local builder / self-install.
- **CI/CD integration for DMG builds** -- whether DMG packaging is integrated into a CI/CD pipeline is TBD and not currently in scope for this deliverable. If CI/CD integration is desired, it should be formally scoped as an addition. Source: **ASSUMPTION** -- inferred from the absence of CI/CD scope items in the decomposition for DEL-01-02; see Guidance Trade-offs for context.

### Upstream Dependencies

DEL-01-01 (macOS 15+ Apple Silicon Build Baseline) is a logical prerequisite for this deliverable: the application must build and run reliably before it can be packaged. **ASSUMPTION** -- this dependency is not formally declared in the decomposition but is logically necessary. The decomposition assigns SOW-001 (builds and runs) to DEL-01-01 and SOW-002 (packaged as `.dmg`) to DEL-01-02, implying sequential dependency. Source: Decomposition DEL-01-01 / DEL-01-02 scope split.

## Requirements

### REQ-DMG-001: DMG Artifact Production

The packaging workflow MUST produce a valid `.dmg` file containing the Chirality application bundle (`.app`).

- **Source:** SOW-002 (Decomposition, SSOW); DEC-PLAT-001 (Decomposition, Decision Log).
- **Acceptance:** A `.dmg` file is produced by the packaging script/tool and can be mounted on macOS.

### REQ-DMG-002: Architecture Target

The `.dmg` MUST contain an application built for Apple Silicon (arm64).

- **Source:** DEC-PLAT-001 (Decomposition, Decision Log).
- **Acceptance:** The packaged application binary targets `arm64` architecture. Verification via `file` command or `lipo -info` on the binary. **ASSUMPTION** -- verification method.

### REQ-DMG-003: macOS Version Target

The packaged application MUST run on macOS 15 or later.

- **Source:** DEC-PLAT-001 (Decomposition, Decision Log); OBJ-001 Acceptance.
- **Acceptance:** The packaging configuration specifies macOS 15+ as the minimum target. The `LSMinimumSystemVersion` key in `Info.plist` SHOULD be set to `15.0` or later. Application launches successfully on a macOS 15+ system. Source for `LSMinimumSystemVersion`: Apple developer documentation, `location TBD`.

### REQ-DMG-004: Unsigned/Unnotarized Acceptability

The `.dmg` and contained application MUST NOT require a code signing identity or Apple notarization for production.

- **Source:** DEC-PLAT-001 (Decomposition, Decision Log): "signing/notarization not required."
- **Acceptance:** The packaging configuration does not depend on a signing identity (script-level guard: `CSC_IDENTITY_AUTO_DISCOVERY=false`). The build succeeds without an Apple Developer account. `codesign -dv` output may show `Signature=adhoc` and `TeamIdentifier=not set`; this is acceptable for the unsigned baseline.

### REQ-DMG-005: Installable and Launchable

The application installed from the `.dmg` MUST launch and function such that an operator can select a working root (`projectRoot`) and begin using the harness.

- **Source:** OBJ-001 Acceptance (Decomposition); SOW-002; DIRECTIVE Section 2.6 (terminology).
- **Acceptance:** After mounting the `.dmg` and installing the `.app` (drag `Chirality.app` to `/Applications`), the application launches and presents the working root (`projectRoot`) selection interface.

### REQ-DMG-006: Instruction Root Bundling

The packaged application MUST include the instruction root (release-managed agent instructions and framework docs) inside the app bundle, maintaining separation from the working root (`projectRoot`).

- **Source:** DIRECTIVE Section 2.6 ("Separation of Instruction and Execution"); SOW-013 (mapped to DEL-05-01, but this deliverable's packaging must respect the architecture).
- **ASSUMPTION** -- the packaging configuration must include the instruction root assets in the Electron app bundle. Detailed implementation is DEL-05-01's scope; this requirement ensures the packaging tool does not strip or relocate these assets.
- **Acceptance:** Inspection of the `.app` bundle confirms instruction root assets are present at expected paths. Verification SHOULD enumerate specific expected paths/files rather than relying on a spot check alone (see Conflict Table CON-002 in Guidance for verification depth discussion).

### REQ-DMG-007: Repeatable Build

The packaging workflow MUST be repeatable: a developer following the documented procedure on a qualifying machine (macOS 15+, Apple Silicon) SHOULD be able to produce a `.dmg` from a clean checkout.

- **Source:** **ASSUMPTION** -- inferred from "local builder" distribution model (DEC-PLAT-001) and the general principle of repeatable builds. Not explicitly stated in sources. See Guidance Principles P4 for rationale.
- **Acceptance:** Documentation exists; a developer can follow it end-to-end.

### REQ-DMG-008: Artifact Types

This deliverable MUST produce the following artifact types: CONFIG, SCRIPT, DOC.

- **Source:** Decomposition DEL-01-02 (AnticipatedArtifacts column).
- **Interpretation:**
  - **CONFIG:** Packaging tool configuration file(s) (e.g., electron-builder YAML/JSON, forge config).
  - **SCRIPT:** Build/package script(s) invocable from the command line.
  - **DOC:** Documentation for local builders describing how to produce and install the `.dmg`.

## Standards

| Standard / Tool | Applicability | Source |
|-----------------|---------------|--------|
| Apple Disk Image (`.dmg`) format | Packaging output format | DEC-PLAT-001 |
| Electron packaging conventions | Application bundling framework | PLAN Section 2 ("Desktop Frontend") |
| macOS app bundle structure (`.app`) | Required for macOS application distribution | Apple Developer Documentation: "Bundle Programming Guide" (`location TBD`) |
| Gatekeeper unsigned-app handling | Users must bypass Gatekeeper for unsigned apps | Apple Developer Documentation: "Gatekeeper" (`location TBD`) |
| `Info.plist` configuration | macOS application metadata including `LSMinimumSystemVersion` | Apple Developer Documentation: "Information Property List" (`location TBD`) |

## Verification

| Requirement | Verification Approach |
|-------------|----------------------|
| REQ-DMG-001 | Run packaging script; confirm `.dmg` file is produced; mount it and verify `.app` is present |
| REQ-DMG-002 | Inspect binary architecture via `file` or `lipo -info` on the main executable |
| REQ-DMG-003 | Launch on a macOS 15+ Apple Silicon machine; verify `LSMinimumSystemVersion` in `Info.plist` is set to `15.0` or later |
| REQ-DMG-004 | Confirm build script sets `CSC_IDENTITY_AUTO_DISCOVERY=false`; confirm `codesign -dv` reports no team identity (unsigned/ad-hoc acceptable baseline) |
| REQ-DMG-005 | Launch from installed `.app`; verify working root (`projectRoot`) selection UI appears and is functional |
| REQ-DMG-006 | Inspect `.app` bundle contents; verify instruction root assets at `Contents/Resources/agents` and `Contents/Resources/docs` |
| REQ-DMG-007 | Follow documented procedure from clean checkout on qualifying machine; confirm `.dmg` is produced |
| REQ-DMG-008 | Confirm CONFIG file(s), SCRIPT file(s), and DOC file(s) exist in the deliverable or repo |

## Documentation

### Required Artifacts

Per the decomposition (AnticipatedArtifacts: CONFIG/SCRIPT/DOC):

| Artifact | Type | Description |
|----------|------|-------------|
| Packaging configuration | CONFIG | `frontend/package.json` `build` section (`mac.target`, `mac.minimumSystemVersion`, `extraResources`) |
| Packaging script(s) | SCRIPT | `frontend/package.json` scripts (`desktop:pack`, `desktop:dist`) |
| Local builder guide | DOC | `docs/building-dmg.md` |
| Gatekeeper bypass notes | DOC | Instructions for handling macOS Gatekeeper warnings on unsigned apps (**ASSUMPTION** -- needed for usability; see Conflict Table CON-003 in Guidance for whether this warrants a formal requirement) |

## Implementation Baseline (2026-02-23)

- Packaging tool selected: `electron-builder`.
- Minimum target pinned in config: `mac.minimumSystemVersion=15.0.0`.
- Build scripts enforce unsigned mode with `CSC_IDENTITY_AUTO_DISCOVERY=false`.
- DMG output path confirmed: `frontend/dist/Chirality-0.1.0-arm64.dmg`.
- Architecture and metadata checks confirmed from produced app bundle:
  - binary: `arm64`
  - `LSMinimumSystemVersion=15.0.0`
  - instruction-root resource directories present: `agents/`, `docs/`.
