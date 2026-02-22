# Datasheet -- DEL-01-02 Unsigned DMG Packaging Workflow

## Identification

| Field | Value |
|-------|-------|
| **Deliverable ID** | DEL-01-02 |
| **Name** | Unsigned DMG Packaging Workflow |
| **Package** | PKG-01 Build & Packaging |
| **Type** | CI_CD_CHANGE |
| **Context Envelope** | M |
| **Responsible Party** | TBD |
| **Scope Items** | SOW-002 |
| **Objectives** | OBJ-001 (**ASSUMPTION** -- best-effort mapping via PKG-01 package grouping) |
| **Decision References** | DEC-PLAT-001 |
| **Anticipated Artifacts** | CONFIG, SCRIPT, DOC |

## Attributes

| Attribute | Value | Source |
|-----------|-------|--------|
| Target Platform | macOS 15+, Apple Silicon only | DEC-PLAT-001 (Decomposition, Decision Log) |
| Packaging Format | `.dmg` (Apple Disk Image) | DEC-PLAT-001; SOW-002 (Decomposition, SSOW) |
| Signing Required | No -- unsigned/unnotarized acceptable | DEC-PLAT-001 (Decomposition, Decision Log) |
| Notarization Required | No -- unsigned/unnotarized acceptable | DEC-PLAT-001 (Decomposition, Decision Log) |
| Distribution Model | Local builder (self-build, self-install) | DEC-PLAT-001: "self-builder installs" (Decomposition, OBJ-001 Acceptance) |
| Application Framework | Electron + Next.js | PLAN Section 2, "Desktop Frontend" |
| Build Toolchain | TBD -- specific packaging tool (e.g., electron-builder, electron-forge) not yet determined | |
| DMG Layout/Branding | TBD -- plain vs. branded DMG; requires human decision (see Guidance, Trade-offs) | |
| Installer Behavior | TBD -- expected drag-to-Applications or equivalent; see Conflict Table CON-001 in Guidance | |
| Output Artifact Location | TBD -- build output path for `.dmg` file | |
| Application Metadata | TBD -- app name, version scheme, and bundle identifier not yet defined | **ASSUMPTION** -- required for packaging tool configuration (Procedure Step 1.2 item 7) |
| Node.js Version | TBD -- check project `package.json` `engines` field | **ASSUMPTION** -- Electron + Next.js project requires Node.js |
| Package Manager | TBD -- npm, yarn, or pnpm as used by the project | **ASSUMPTION** |
| CI/CD Integration | TBD -- whether DMG build is integrated into CI/CD pipeline; currently not in scope (see Specification, Scope Exclusions) | |

## Conditions

| Condition | Value | Source |
|-----------|-------|--------|
| Must launch after install | Yes -- `.dmg` packaging is available and installable | OBJ-001 Acceptance (Decomposition) |
| Must function after launch | Yes -- operator can select a working root (`projectRoot`) and begin using the harness | OBJ-001 narrative (Decomposition); DIRECTIVE Section 2.6 |
| Code signing identity | Not required (unsigned acceptable) | DEC-PLAT-001 (Decomposition, Decision Log) |
| Apple notarization | Not required | DEC-PLAT-001 (Decomposition, Decision Log) |
| Gatekeeper bypass | **ASSUMPTION** -- local builder will need to bypass macOS Gatekeeper for unsigned apps (System Settings > Privacy & Security) | Apple macOS security model (`location TBD`) |
| Upstream dependency on DEL-01-01 | **ASSUMPTION** -- DEL-01-01 (macOS 15+ Apple Silicon Build Baseline) must produce a working build before DMG packaging can wrap it; logical dependency not yet formally declared in decomposition | Decomposition DEL-01-01 / SOW-001 |

## Construction

| Element | Description | Source |
|---------|-------------|--------|
| Packaging configuration | TBD -- configuration file(s) for the chosen packaging tool defining DMG output, architecture (arm64), and macOS target | |
| Build script(s) | TBD -- script(s) to invoke the packaging tool and produce the `.dmg` artifact | |
| Documentation | TBD -- instructions for local builders to produce and install the `.dmg` | |
| Upstream dependency | DEL-01-01 (macOS 15+ Apple Silicon Build Baseline) must produce a working build before DMG packaging can wrap it (**ASSUMPTION** -- logical dependency; not yet formally declared) | Decomposition DEL-01-01 / SOW-001 |
| Instruction root bundling | The packaged `.app` must include the instruction root (release-managed agent instructions and framework docs) per DIRECTIVE Section 2.6, maintaining separation from the working root (`projectRoot`) | DIRECTIVE Section 2.6 |

## References

| Reference | Relevance |
|-----------|-----------|
| Decomposition: `execution/_Decomposition/ChiralityApp_SoftwareDecomposition_2026-02-21_G7-APPROVED.md` | Authoritative source for DEL-01-02 definition, DEC-PLAT-001, SOW-002, OBJ-001 |
| `docs/PLAN.md` Section 2 | Identifies desktop frontend as Electron + Next.js; confirms `.dmg` packaging target |
| `docs/DIRECTIVE.md` | Founding intent and design philosophy; separation of instruction root vs working root (`projectRoot`) |
| `docs/SPEC.md` | Physical structures; not directly governing DMG packaging but defines the execution model the packaged app must support |
| Apple Developer Documentation: App Bundle Structure | macOS `.app` bundle structure conventions (`location TBD`) |
| Apple Developer Documentation: Gatekeeper | macOS Gatekeeper behavior for unsigned applications (`location TBD`) |
