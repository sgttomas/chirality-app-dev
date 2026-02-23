# Guidance -- DEL-01-02 Unsigned DMG Packaging Workflow

## Purpose

This deliverable exists to provide a working `.dmg` packaging path so that local builders (developers and operators) can produce distributable macOS disk images of the Chirality desktop application without requiring an Apple Developer account, code signing identity, or notarization workflow.

The "unsigned/unnotarized acceptable" decision (DEC-PLAT-001) is a deliberate simplification: Chirality targets self-builders who compile from source, not end-users downloading from the internet. This removes the signing/notarization infrastructure from the critical path while preserving a functional install experience.

Source: Decomposition DEL-01-02; DEC-PLAT-001; OBJ-001.

## Principles

### P1: Packaging wraps a working build; it does not fix one

This deliverable assumes DEL-01-01 (macOS 15+ Apple Silicon Build Baseline) has produced a working, launchable Electron + Next.js application. If the build is broken, packaging will not help. The boundary is: DEL-01-01 owns "it builds and runs"; DEL-01-02 owns "the built output is wrapped in a `.dmg` that installs correctly."

Source: Decomposition -- DEL-01-01 covers SOW-001 (builds and runs); DEL-01-02 covers SOW-002 (packaged as `.dmg`).

### P2: Unsigned does not mean unverifiable

Although signing and notarization are not required, the packaged application should still be verifiable by the builder:
- The builder compiled it themselves (trust-by-origin).
- Architecture and platform targets can be confirmed via `file` / `lipo -info`.
- Gatekeeper bypass is a conscious, documented step -- not a hidden workaround.

Source: **ASSUMPTION** -- inferred from the professional responsibility model (DIRECTIVE Section 3) and "evidence over plausibility" principle (DIRECTIVE Section 2.4).

### P3: Instruction root integrity through packaging

The Chirality architecture separates instruction root (release-managed, app bundle) from working root (`projectRoot`, user-selected). The packaging step must preserve this separation. Instruction root assets bundled into the `.app` should be complete and accessible at runtime.

Source: DIRECTIVE Section 2.6; SPEC Section 2 (deliverable folder layout context); SOW-013 (mapped to DEL-05-01 but relevant as a packaging constraint).

### P4: Repeatability over automation

Given the local-builder distribution model, the packaging workflow should prioritize clear, repeatable manual steps over complex CI automation. A developer should be able to produce a `.dmg` from a clean checkout by following documented instructions.

**Rationale for REQ-DMG-007:** While the decomposition does not explicitly state a repeatability requirement, the local-builder distribution model (DEC-PLAT-001) inherently depends on it. If the intended user must build from source, the build process must be documentable and reproducible. Without repeatability, the distribution model does not function. The DIRECTIVE's "evidence over plausibility" principle (Section 2.4) further supports requiring that the process be demonstrably repeatable rather than assumed to work. This rationale is marked **ASSUMPTION** -- pending human confirmation that repeatability should remain a binding requirement rather than a best-effort goal.

Source: **ASSUMPTION** -- inferred from the "self-builder installs" model (DEC-PLAT-001), DIRECTIVE Section 2.4, and the absence of CI/CD infrastructure scope items for this deliverable.

## Considerations

### Packaging Tool Selection

The Electron ecosystem offers several packaging tools. Key candidates:

| Tool | Notes |
|------|-------|
| `electron-builder` | Widely used; supports `.dmg` output natively; YAML/JSON config; handles `arm64` targets |
| `@electron/forge` | Official Electron tooling; plugin-based; includes `@electron/forge-maker-dmg` |
| `create-dmg` (standalone) | Lightweight CLI for creating DMGs from `.app` bundles; can be layered on top of any build |

Current baseline selection is `electron-builder` via `frontend/package.json` scripts/config.

Note: The build toolchain selection (A-001 in the semantic lensing register) is a blocking dependency for multiple downstream decisions including DMG layout/branding, installer behavior, application metadata, and artifact file locations.

### Gatekeeper Handling

macOS Gatekeeper will flag unsigned applications downloaded or transferred between machines. For self-built apps, the system typically does not trigger Gatekeeper (the builder's machine trusts locally-built binaries). However, if the `.dmg` is transferred to another machine, the recipient will need to:

1. Open System Settings > Privacy & Security.
2. Allow the unsigned application to run.

**ASSUMPTION** -- this is standard macOS behavior for unsigned apps. Specific UI flow may vary by macOS version. Documentation should include Gatekeeper bypass instructions. The depth of Gatekeeper bypass documentation (brief note vs. detailed walkthrough) is a pending human decision (see Trade-offs table and Conflict Table CON-003). Source: Apple Developer Documentation: "Gatekeeper" (`location TBD`).

### DMG Presentation

DMGs can include custom backgrounds, icon layouts, and Applications folder shortcuts for drag-to-install UX. This is a polish item:
- **Minimum viable:** A plain DMG containing the `.app` bundle.
- **Enhanced:** Branded DMG with background image, icon positioning, and Applications shortcut.

Current baseline uses the minimum viable plain DMG. Enhanced DMG presentation is optional follow-up only.

### Universal Binary Consideration

DEC-PLAT-001 specifies Apple Silicon only. A universal binary (arm64 + x86_64) is explicitly out of scope. If future requirements change, this would affect DEL-01-01 (build baseline) first, and DEL-01-02 would follow.

Source: DEC-PLAT-001 (Decomposition, Decision Log).

### Application Metadata

Application metadata for the current baseline is defined in `frontend/package.json`: `productName=Chirality`, `version=0.1.0`, `appId=com.chirality.app`.

Source: **ASSUMPTION** -- standard Electron packaging requirement; referenced in Procedure Step 1.2 item 7.

## Current Baseline Decisions (2026-02-23)

The following implementation decisions are now active for this repository and supersede earlier "TBD" placeholders for baseline execution:

1. Packaging tool: `electron-builder` via `frontend/package.json`.
2. DMG presentation: plain baseline DMG (no custom layout assets).
3. Installation method: mount DMG and drag `Chirality.app` to `/Applications`.
4. Minimum macOS target: `15.0.0` (`LSMinimumSystemVersion`).
5. Unsigned guardrail: `CSC_IDENTITY_AUTO_DISCOVERY=false` in DMG scripts.
6. Local-builder runbook: `docs/building-dmg.md`.

## Trade-offs

| Trade-off | Option A | Option B | Recommendation |
|-----------|----------|----------|----------------|
| Packaging tool complexity vs. features | Minimal tool (e.g., `create-dmg` wrapping a pre-built `.app`) -- simpler, fewer dependencies | Full packaging tool (e.g., `electron-builder`) -- more features, handles more of the pipeline | Current baseline selects Option B (`electron-builder`) |
| DMG branding | Plain DMG (fast, no design work) | Branded DMG (better UX, requires design assets) | Start with plain; brand later if desired |
| Gatekeeper documentation depth | Brief note ("bypass Gatekeeper in System Settings") | Detailed walkthrough with screenshots per macOS version | **ASSUMPTION** -- brief note sufficient for technical self-builders; pending human confirmation |
| CI integration | Manual-only build | CI pipeline produces `.dmg` on push/tag | Not currently in scope (see Specification, Scope Exclusions); TBD if desired |
| Installation method | Drag-to-Applications (standard macOS convention) | Alternative method (e.g., installer package, command-line copy) | Current baseline selects Option A (drag-to-Applications) |

## Examples

Current baseline examples:

- Packaging configuration location: `frontend/package.json` (`build` section).
- Build invocation: `cd frontend && npm run desktop:dist`.
- Output artifacts:
  - `frontend/dist/Chirality-0.1.0-arm64.dmg`
  - `frontend/dist/mac-arm64/Chirality.app`
- Verification commands:
  - `file frontend/dist/mac-arm64/Chirality.app/Contents/MacOS/Chirality`
  - `/usr/libexec/PlistBuddy -c "Print :LSMinimumSystemVersion" frontend/dist/mac-arm64/Chirality.app/Contents/Info.plist`
  - `codesign -dv --verbose=4 frontend/dist/mac-arm64/Chirality.app 2>&1`

## Conflict Table (for human ruling)

| Conflict ID | Conflict | Source A | Source B | Impacted Sections | Proposed Authority | Human Ruling |
|-------------|----------|----------|----------|--------------------|--------------------|--------------|
| CON-001 | Historical drift (resolved): installer method language previously varied across docs; baseline now standardized to drag-to-Applications | Historical snapshots prior to 2026-02-23 | Datasheet/Specification/Procedure current baseline text | Datasheet Attributes; Specification REQ-DMG-005; Procedure Step 3.3 | Specification (normative document) governs installation contract phrasing | RESOLVED (2026-02-23 baseline: drag-to-Applications) |
| CON-002 | Historical drift (resolved): instruction-root verification depth previously mixed generic spot-check wording with expected-path wording; baseline now uses explicit paths | Historical snapshots prior to 2026-02-23 | Specification/Procedure current baseline text | Specification Verification REQ-DMG-006; Procedure Step 3.1 | Specification (normative document) governs verification depth | RESOLVED (2026-02-23 baseline: explicit `agents/` + `docs/` paths) |
| CON-003 | Gatekeeper bypass: currently handled as a documentation note (DOC artifact) and ASSUMPTION. Should Gatekeeper bypass handling be elevated to a formal requirement? If it is necessary for the install-and-launch experience (REQ-DMG-005), it may warrant its own requirement rather than a documentation-only treatment. | Specification#Documentation "Gatekeeper bypass notes" (DOC artifact) | Guidance#Considerations "Gatekeeper Handling" (**ASSUMPTION**) | Specification Requirements (potential new REQ); Specification Documentation; Guidance Considerations | Human decision -- if Gatekeeper bypass is essential for usability in the transfer case, consider adding REQ-DMG-009 | TBD |
