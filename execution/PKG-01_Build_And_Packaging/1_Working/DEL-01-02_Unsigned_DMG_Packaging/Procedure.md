# Procedure -- DEL-01-02 Unsigned DMG Packaging Workflow

## Purpose

This procedure describes how to produce, verify, and install a `.dmg` disk image of the Chirality desktop application for macOS 15+ on Apple Silicon. It covers both the production of the deliverable artifacts (CONFIG/SCRIPT/DOC) and the use of those artifacts to package the application.

Source: Decomposition DEL-01-02; SOW-002; OBJ-001; DEC-PLAT-001.

## Prerequisites

### Required Environment

| Prerequisite | Details | Source |
|-------------|---------|--------|
| macOS 15+ | Build machine must run macOS 15 or later | DEC-PLAT-001 (Decomposition) |
| Apple Silicon hardware | Build machine must be Apple Silicon (M1/M2/M3/M4 series) | DEC-PLAT-001 (Decomposition) |
| Node.js runtime | `>=20` | `frontend/package.json` (`engines.node`) |
| Package manager | npm | `frontend/package.json` scripts/lockfile |
| Working build baseline | DEL-01-01 must be satisfied: the application builds and runs in dev and prod modes | Decomposition DEL-01-01 / SOW-001 (**ASSUMPTION** -- logical upstream dependency; not yet formally declared) |
| Packaging tool installed | `electron-builder@25.1.8` (project dev dependency) | `frontend/package.json` |
| Source checkout | Clean checkout of the Chirality application repository | **ASSUMPTION** -- repeatability requirement (REQ-DMG-007) |
| Application metadata | Defined in current config: `productName=Chirality`, `appId=com.chirality.app`, `version=0.1.0` | `frontend/package.json` |

### Upstream Dependencies

| Dependency | Status | Notes |
|-----------|--------|-------|
| DEL-01-01 (macOS 15+ Apple Silicon Build Baseline) | **ASSUMPTION** -- not yet formally declared | The build must work before packaging can wrap it (see Specification, Upstream Dependencies) |

### Required References

| Reference | Purpose |
|-----------|---------|
| Packaging tool documentation | `electron-builder` configuration and invocation reference |
| Decomposition (DEC-PLAT-001) | Platform constraints and signing policy |
| `docs/building-dmg.md` | Canonical local-builder runbook for this repository |
| Apple Developer Documentation: Info.plist | `LSMinimumSystemVersion` and bundle metadata (`location TBD`) |
| Apple Developer Documentation: Gatekeeper | Unsigned app handling on macOS (`location TBD`) |

## Steps

### Phase 1: Establish Packaging Configuration (Artifact: CONFIG)

**Step 1.1: Select Packaging Tool**

Use `electron-builder` for DMG creation in this repository baseline.

- Input: DEL-01-01 build toolchain output; project conventions.
- Output: Tool decision recorded (`electron-builder`).

**Step 1.2: Create Packaging Configuration File**

Create or update the packaging tool configuration to specify:

1. **Output format:** `.dmg`
2. **Target architecture:** `arm64` (Apple Silicon)
3. **Target OS version:** macOS 15+ (set `LSMinimumSystemVersion` to `15.0` or later in `Info.plist` or equivalent packaging tool setting). Source: Apple Developer Documentation (`location TBD`).
4. **Signing:** Disabled / unsigned
5. **Notarization:** Disabled
6. **App bundle contents:** Ensure instruction root assets are included (DIRECTIVE Section 2.6)
7. **Application metadata:** App name, version, bundle identifier (`Chirality`, `0.1.0`, `com.chirality.app`)

- Input: Packaging tool documentation; platform constraints (DEC-PLAT-001).
- Output: Configuration in `frontend/package.json` `build` section.

**Step 1.3: Validate Configuration**

Review the configuration file to confirm:
- [ ] Output format is `.dmg`
- [ ] Architecture target is `arm64`
- [ ] macOS minimum version is 15.0 (via `LSMinimumSystemVersion` or equivalent)
- [ ] No signing identity is referenced
- [ ] No notarization configuration is present
- [ ] Instruction root assets are included in the bundle
- [ ] Application metadata (name, version, bundle ID) is populated

### Phase 2: Create Build/Package Script (Artifact: SCRIPT)

**Step 2.1: Write Packaging Script**

Use the existing npm scripts in `frontend/package.json`:

- `desktop:pack`: directory build (`--dir`) for app-bundle inspection.
- `desktop:dist`: DMG distribution build.

Both scripts:

1. run production build (`npm run build`)
2. invoke `electron-builder`
3. force unsigned mode (`CSC_IDENTITY_AUTO_DISCOVERY=false`)
4. run instruction-root integrity verification (`npm run instruction-root:integrity`)

For a full DMG run:

```bash
cd frontend
npm run desktop:dist
```

- Input: `frontend/package.json` build + script configuration from Phase 1.
- Output: Executable packaging scripts in `frontend/package.json`.

**Step 2.2: Test Script Execution**

Run the packaging script on a qualifying machine:
- [ ] Script completes without errors
- [ ] `.dmg` file is produced at the expected output location
- [ ] `.dmg` file size is within expected bounds: **ASSUMPTION** -- a typical Electron + Next.js application DMG is expected to be in the range of 100-300 MB. A file under 10 MB likely indicates missing content; a file over 500 MB likely indicates unnecessary bundled assets. These thresholds are approximate and should be calibrated after the first successful build.

### Phase 3: Verify DMG Artifact

**Step 3.1: Mount and Inspect DMG**

1. Double-click or use `hdiutil attach <output>.dmg` to mount the disk image.
2. Verify the `.app` bundle is present inside the mounted volume.
3. Verify the `.app` bundle contains expected contents:
   - [ ] Main executable exists
   - [ ] Electron framework is present
   - [ ] Instruction root assets are present at:
     - `Contents/Resources/agents`
     - `Contents/Resources/docs`

**Step 3.2: Verify Architecture**

Run architecture verification on the main binary:

```
file /path/to/Chirality.app/Contents/MacOS/Chirality
```

Expected output should include `arm64` and should NOT include `x86_64` (unless universal binary is produced, which is out of scope per DEC-PLAT-001).

**Step 3.3: Verify macOS Version Target**

Verify the minimum macOS version is set correctly:

```
/usr/libexec/PlistBuddy -c "Print :LSMinimumSystemVersion" /path/to/Chirality.app/Contents/Info.plist
```

Expected output: `15.0` or later. **ASSUMPTION** -- `PlistBuddy` is the appropriate tool; `defaults read` is an alternative. Source: Apple Developer Documentation (`location TBD`).

**Step 3.4: Launch and Functional Check**

1. Copy the `.app` from the mounted DMG to `/Applications/`.
2. Launch the application.
3. Verify:
   - [ ] Application launches without crash
   - [ ] Working root (`projectRoot`) selection interface is accessible
   - [ ] Harness is operational (can start a session against a test working root)

**Step 3.5: Unsigned Verification**

Confirm the build does not require a signing identity:

```
codesign -dv --verbose=4 /Applications/Chirality.app 2>&1
```

Expected baseline: `TeamIdentifier=not set` and `Signature=adhoc` are acceptable (no developer identity/notarization dependency).

### Phase 4: Document the Workflow (Artifact: DOC)

**Step 4.1: Write Local Builder Guide**

Create documentation (e.g., `docs/building-dmg.md` or equivalent) that includes:

1. **Prerequisites:** macOS version, hardware, Node.js version, package manager.
2. **Build steps:** How to produce the `.dmg` from a clean checkout (referencing the script from Phase 2).
3. **Install steps:** How to install from the `.dmg` (mount and drag `Chirality.app` to `/Applications`).
4. **Gatekeeper bypass:** How to handle macOS Gatekeeper warnings if the `.dmg` is transferred to another machine. Source: Apple Developer Documentation: Gatekeeper (`location TBD`).
5. **Troubleshooting:** TBD -- common issues and resolutions should be populated based on execution experience during implementation.

**Step 4.2: Review Documentation Completeness**

- [ ] A developer unfamiliar with the project can follow the guide end-to-end
- [ ] Prerequisites are specific (versions, tools)
- [ ] Gatekeeper bypass instructions are included
- [ ] Output file location is documented

## Verification

### Verification Checklist

| Check | Method | Requirement |
|-------|--------|-------------|
| DMG file produced | Run packaging script | REQ-DMG-001 |
| Architecture is arm64 | `file` or `lipo -info` on binary | REQ-DMG-002 |
| macOS minimum version set | Check `LSMinimumSystemVersion` in `Info.plist` (Step 3.3) | REQ-DMG-003 |
| No signing identity required | Build with `CSC_IDENTITY_AUTO_DISCOVERY=false`; `codesign -dv --verbose=4` shows no team identity requirement | REQ-DMG-004 |
| Installs and launches | Install from DMG; launch; verify working root (`projectRoot`) selection UI | REQ-DMG-005 |
| Instruction root present | Inspect `.app` bundle contents at `Contents/Resources/agents` and `Contents/Resources/docs` | REQ-DMG-006 |
| Repeatable from clean checkout | Follow documented procedure | REQ-DMG-007 |
| All artifact types present | Confirm CONFIG + SCRIPT + DOC exist | REQ-DMG-008 |
| DMG file size sanity | Verify file size is within expected range (**ASSUMPTION** -- 100-300 MB typical) | Sanity check (not a formal requirement) |

## Records

### Deliverable Artifacts Produced

| Artifact | Type | Expected Location |
|----------|------|-------------------|
| Packaging configuration file | CONFIG | `frontend/package.json` (`build` section) |
| Packaging script | SCRIPT | `frontend/package.json` (`desktop:pack`, `desktop:dist`) |
| Local builder guide | DOC | `docs/building-dmg.md` |
| Gatekeeper bypass notes | DOC | `docs/building-dmg.md` (`Gatekeeper Note`) |

Artifact locations are now finalized for the current baseline implementation.

### Evidence of Completion

| Evidence | Description |
|----------|-------------|
| `.dmg` file produced | Output of a successful packaging script run |
| Architecture verification output | Output of `file` or `lipo -info` command confirming `arm64` |
| macOS version verification output | Output of `PlistBuddy` or equivalent confirming `LSMinimumSystemVersion` is `15.0` or later |
| Launch confirmation | Screenshot or log of successful application launch from DMG install |
| Unsigned verification output | Output of `codesign -dv --verbose=4` confirming no team identity / ad-hoc baseline |
| DMG file size | Recorded file size for sanity baseline |
