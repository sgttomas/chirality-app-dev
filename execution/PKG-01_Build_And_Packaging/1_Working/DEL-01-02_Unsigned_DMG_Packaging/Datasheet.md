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
| Build Toolchain | `electron-builder@25.1.8` via `frontend/package.json` `build` config and `desktop:dist` script | `frontend/package.json` |
| DMG Layout/Branding | Plain DMG (no custom background/layout assets in current baseline) | `frontend/package.json`; `docs/building-dmg.md` |
| Installer Behavior | Mount DMG, drag `Chirality.app` to `/Applications`, then launch | `docs/building-dmg.md` |
| Output Artifact Location | `frontend/dist/Chirality-0.1.0-arm64.dmg` (`.app` at `frontend/dist/mac-arm64/Chirality.app`) | `docs/building-dmg.md` |
| Application Metadata | `productName=Chirality`, `appId=com.chirality.app`, version `0.1.0` | `frontend/package.json` |
| Node.js Version | `>=20` | `frontend/package.json` (`engines.node`) |
| Package Manager | npm | `frontend/package.json` scripts and lockfile |
| CI/CD Integration | Local/manual workflow only for DMG build (CI currently validates harness, not DMG packaging) | `docs/building-dmg.md`; `.github/workflows/harness-premerge.yml` |

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
| Packaging configuration | `frontend/package.json` `build` section (`mac.target=dmg/arm64`, `mac.minimumSystemVersion=15.0.0`, instruction-root `extraResources`) | `frontend/package.json` |
| Build script(s) | `frontend/package.json` scripts `desktop:pack` and `desktop:dist` (explicit unsigned mode via `CSC_IDENTITY_AUTO_DISCOVERY=false`) | `frontend/package.json` |
| Documentation | Local builder runbook for DMG build/install and verification | `docs/building-dmg.md` |
| Upstream dependency | DEL-01-01 (macOS 15+ Apple Silicon Build Baseline) must produce a working build before DMG packaging can wrap it (**ASSUMPTION** -- logical dependency; not yet formally declared) | Decomposition DEL-01-01 / SOW-001 |
| Instruction root bundling | The packaged `.app` must include the instruction root (release-managed agent instructions and framework docs) per DIRECTIVE Section 2.6, maintaining separation from the working root (`projectRoot`) | DIRECTIVE Section 2.6 |

## References

| Reference | Relevance |
|-----------|-----------|
| Decomposition: `execution/_Decomposition/ChiralityApp_SoftwareDecomposition_2026-02-21_G7-APPROVED.md` | Authoritative source for DEL-01-02 definition, DEC-PLAT-001, SOW-002, OBJ-001 |
| `docs/PLAN.md` Section 2 | Identifies desktop frontend as Electron + Next.js; confirms `.dmg` packaging target |
| `docs/DIRECTIVE.md` | Founding intent and design philosophy; separation of instruction root vs working root (`projectRoot`) |
| `docs/building-dmg.md` | Canonical local-builder DMG workflow, verification commands, and install steps |
| `docs/SPEC.md` | Physical structures; not directly governing DMG packaging but defines the execution model the packaged app must support |
| Apple Developer Documentation: App Bundle Structure | macOS `.app` bundle structure conventions (`location TBD`) |
| Apple Developer Documentation: Gatekeeper | macOS Gatekeeper behavior for unsigned applications (`location TBD`) |
