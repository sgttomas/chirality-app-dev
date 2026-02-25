# Procedure: DEL-01-03 Frontend Workspace Bootstrap & Packaging Baseline

## Purpose

This procedure describes the steps to produce and verify the `frontend/` workspace bootstrap and packaging baseline. It covers both the creation of the workspace (SOW-044) and the establishment of the packaging baseline (SOW-047).

The procedure is structured in two phases corresponding to the two scope items, followed by a combined verification phase.

## Prerequisites

### Required Tools

| Tool | Version | Purpose |
|------|---------|---------|
| Node.js | TBD (20 LTS+ recommended) | JavaScript runtime |
| npm | (bundled with Node.js) | Package management |
| Git | Any recent version | Version control; workspace must be tracked |
| macOS | 15+ (Sequoia) | Target platform |
| Apple Silicon Mac | arm64 | Target architecture |

### Required References

| Reference | Location | Purpose |
|-----------|----------|---------|
| Decomposition | `execution/_Decomposition/ChiralityApp_SoftwareDecomposition_2026-02-21_G7-APPROVED.md` | Scope Amendment A1 defines requirements |
| PLAN.md | `docs/PLAN.md` | Section 2: FE-1 and FE-4 acceptance criteria |
| SPEC.md | `docs/SPEC.md` | Section 1: Execution root layout; instruction root definition |
| Specification.md | This deliverable folder | Requirements REQ-01 through REQ-12 |

### Upstream Dependencies

| Dependency | Status | Notes |
|------------|--------|-------|
| None (foundation deliverable) | -- | `_DEPENDENCIES.md` confirms no upstream deliverable prerequisites. Upstream CONSTRAINT rows reference `docs/SPEC.md`, `docs/DIRECTIVE.md`, and `docs/CONTRACT.md` as document constraints (not blocking deliverables). This is a pre-tier gate foundation deliverable. |

## Steps

### Phase 1: Workspace Bootstrap (SOW-044)

#### Step 1.1: Create Frontend Directory

Create the `frontend/` directory at the repository root.

```bash
mkdir -p frontend
```

Verify: `frontend/` directory exists.

#### Step 1.2: Initialize Package Manifest

Create `frontend/package.json` with:
- Project name and version
- Required dependencies: `next`, `react`, `react-dom`, `electron`
- Required dev dependencies: `typescript`, `@types/react`, `@types/node`, `electron-builder` (**ASSUMPTION: electron-builder selected**)
- Script entries for `dev`, `build`, `desktop:pack`, `desktop:dist`
- `engines` field specifying minimum Node.js version

```bash
cd frontend && npm init -y
# Then edit package.json to add dependencies and scripts
```

Verify: `frontend/package.json` exists and contains required fields (REQ-02).

#### Step 1.3: Install Dependencies

```bash
cd frontend && npm install
```

Verify: `npm install` exits with code 0; `node_modules/` is populated; no errors referencing non-local repositories (REQ-10).

#### Step 1.4: Create TypeScript Configuration

Create `frontend/tsconfig.json` with settings appropriate for Next.js + Electron TypeScript compilation.

Verify: `npx tsc --noEmit` runs without type errors on baseline source files (REQ-03).

#### Step 1.5: Create Next.js Configuration

Create `frontend/next.config.mjs` (or `.js`/`.ts`) with:
- Output mode appropriate for Electron integration (**ASSUMPTION: specific mode TBD**)
- Any necessary Electron compatibility settings

Verify: Next.js config file present (REQ-04).

#### Step 1.6: Create Electron Main Process

Create the Electron main process entry point (e.g., `frontend/electron/main.ts`) with:
- BrowserWindow creation
- Development mode: load from Next.js dev server URL
- Production mode: load from built output path
- Appropriate window size and settings for the Chirality application

Verify: Main process file exists with BrowserWindow creation logic (REQ-05).

#### Step 1.7: Create Electron Preload Script

Create a preload script (e.g., `frontend/electron/preload.ts`) for renderer process security.

**ASSUMPTION:** A preload script is needed for Electron security best practices (contextIsolation).

Verify: Preload file exists.

#### Step 1.8: Create Minimal Next.js Application Scaffold

Create the minimum Next.js application structure using the `frontend/src/app/` convention (see Guidance Vocabulary Notes):
- Root layout file: `frontend/src/app/layout.tsx`
- Root page file: `frontend/src/app/page.tsx`
- Minimal content sufficient to verify the application loads (e.g., a heading element with identifiable text)

Verify: Application source files exist at `frontend/src/app/layout.tsx` and `frontend/src/app/page.tsx`.

#### Step 1.9: Verify Development Scripts

Run the development scripts to confirm they resolve:

**Dev server verification:**
```bash
cd frontend && npm run dev
# Verify ALL of the following:
# 1. Next.js dev server starts (console output shows "ready" or "compiled" message)
# 2. Electron window opens (if dev script includes Electron launch via orchestration -- see Guidance C3)
# 3. The application renders: the root page content (from frontend/src/app/page.tsx) is visible
#    in the browser or Electron window WITHOUT console errors. A blank window or error screen
#    does NOT satisfy this check.
# Ctrl+C to stop
```

**Production build verification:**
```bash
cd frontend && npm run build
# Verify ALL of the following:
# 1. Build completes with exit code 0
# 2. Output directory is created:
#    - If output: 'export' mode: frontend/out/ should contain index.html and static assets
#    - If server mode: frontend/.next/ should contain server and static build artifacts
#    (The expected directory depends on the Next.js output mode -- see Guidance C1 / Specification REQ-04)
# 3. The output directory contains at minimum: an entry HTML file or server entry point,
#    and the compiled JavaScript/CSS chunks
```

Verify: REQ-06 acceptance criteria met. Record the actual output directory path for use in Phase 2.

#### Step 1.10: Create `.gitignore` and Add Frontend to Git Tracking

Create `frontend/.gitignore` with exclusions for transient artifacts:
```
node_modules/
.next/
out/
dist/
*.tsbuildinfo
```

Then add the workspace to version control:
```bash
git add frontend/
```

Verify:
- `frontend/.gitignore` exists with `node_modules/` exclusion (at minimum)
- `frontend/` directory is git-tracked (REQ-01)
- `node_modules/` is NOT tracked

### Phase 2: Packaging Baseline (SOW-047)

#### Step 2.1: Create Electron-Builder Configuration

Add electron-builder configuration (in `frontend/package.json` `"build"` key or a separate `electron-builder.yml`/`electron-builder.json`) with:
- `appId`: Application identifier
- `productName`: "Chirality" (or project-appropriate name)
- `mac.target`: `dmg`
- `mac.arch`: `arm64`
- `extraResources`: Instruction root directories

Example configuration structure (**ASSUMPTION: exact paths TBD**):

```json
{
  "build": {
    "appId": "com.chirality.app",
    "productName": "Chirality",
    "mac": {
      "target": "dmg",
      "arch": ["arm64"]
    },
    "extraResources": [
      { "from": "../agents", "to": "agents" },
      { "from": "../docs", "to": "docs" }
    ]
  }
}
```

Verify: Configuration present with required fields (REQ-11).

#### Step 2.2: Verify `desktop:pack` Script

```bash
cd frontend && npm run desktop:pack
```

**Output path note:** The unpacked application directory will be created under `frontend/dist/<platform-arch>/` (e.g., `frontend/dist/mac-arm64/` for Apple Silicon macOS). The exact subdirectory name is determined by electron-builder's `mac.target` and `mac.arch` configuration from Step 2.1. After running `desktop:pack`, identify the actual output path before proceeding to Steps 2.3 and 2.4.

Verify:
- Command exits successfully
- Unpacked application directory is created under `frontend/dist/<platform-arch>/`
- The unpacked application contains the instruction root directories (`agents/`, `docs/`) (REQ-09)

#### Step 2.3: Verify `desktop:dist` Script

```bash
cd frontend && npm run desktop:dist
```

Verify:
- Command exits successfully
- A `.dmg` file is created under `frontend/dist/` (exact filename determined by electron-builder `productName` and version configuration)
- The `.dmg` targets macOS arm64 (REQ-07, REQ-08)

#### Step 2.4: Instruction Root Inclusion Check

After `desktop:pack`, verify instruction root presence in the packaged output. Use the actual output path identified in Step 2.2:

```bash
# Substitute <PACK_OUTPUT> with the actual path from Step 2.2
# e.g., frontend/dist/mac-arm64/Chirality.app
ls -la "<PACK_OUTPUT>/Contents/Resources/agents/"
ls -la "<PACK_OUTPUT>/Contents/Resources/docs/"
```

**Note:** The `.app` bundle path follows the macOS convention: `<productName>.app/Contents/Resources/`. The `agents/` and `docs/` directories should appear here because `extraResources` content is placed in the `Resources/` directory by electron-builder. At runtime, `process.resourcesPath` resolves to this location (see Guidance C4).

Verify: Both `agents/` and `docs/` directories are present and contain expected content (REQ-09).

### Phase 3: Combined Verification

#### Step 3.1: Full Requirements Verification

Run through the verification matrix from `Specification.md`:

| Req | Check | Pass/Fail |
|-----|-------|-----------|
| REQ-01 | `frontend/` exists and is git-tracked | TBD |
| REQ-02 | `npm install` succeeds from `frontend/` | TBD |
| REQ-03 | `tsconfig.json` present; `tsc --noEmit` passes | TBD |
| REQ-04 | Next.js config file present | TBD |
| REQ-05 | Electron main process entry point present | TBD |
| REQ-06 | `npm run dev` and `npm run build` resolve | TBD |
| REQ-07 | `desktop:pack` and `desktop:dist` produce artifacts | TBD |
| REQ-08 | Output targets macOS arm64 | TBD |
| REQ-09 | Instruction root present in packaged output | TBD |
| REQ-10 | No non-local repo references | TBD |
| REQ-11 | Electron-builder config present with required fields | TBD |
| REQ-12 | Preload script present and wired in BrowserWindow config | TBD |

#### Step 3.2: Clean Checkout Verification

Verify the local-only policy by performing a clean checkout test:

```bash
# In a temporary directory
git clone <repo-url> /tmp/chirality-test
cd /tmp/chirality-test/frontend
npm install
npm run build
npm run desktop:pack
# Verify all steps succeed without external repo dependencies
```

Verify: Clean checkout builds and packages successfully (REQ-10).

#### Step 3.3: Non-Local Dependency Audit

Audit `frontend/package.json` for any non-local dependency references:

```bash
# Check for git+, file:../, link:, or workspace: references
grep -E '(git\+|file:\.\.|link:|workspace:)' frontend/package.json
```

Verify: No non-local references found (REQ-10).

## Verification

| Check | Method | Expected Result |
|-------|--------|-----------------|
| Workspace exists | `ls frontend/package.json` | File present |
| Dependencies install | `cd frontend && npm install` | Exit code 0 |
| Dev server starts | `cd frontend && npm run dev` | Server starts, Electron window opens |
| Production build | `cd frontend && npm run build` | Exit code 0, output directory created |
| Pack succeeds | `cd frontend && npm run desktop:pack` | Unpacked app directory created |
| Dist succeeds | `cd frontend && npm run desktop:dist` | `.dmg` file created |
| Instruction root in package | Inspect unpacked app resources | `agents/` and `docs/` present |
| No non-local deps | Audit `package.json` | No git+/file/link references |
| Platform target correct | Inspect electron-builder output | arm64 macOS binary |
| Preload script wired | Inspect BrowserWindow `webPreferences` for `preload` path, `contextIsolation: true`, `nodeIntegration: false` | Security settings correctly configured |
| Git tracked | `git ls-files frontend/` | Files listed in tracked tree |

## Records

Upon successful completion, the following evidence should be captured:

| Record | Description | Location |
|--------|-------------|----------|
| Verification results | Pass/fail for each requirement check | This deliverable folder (or `_MEMORY.md`) |
| Build output inventory | List of produced artifacts (unpacked app, `.dmg`) | This deliverable folder (or `_MEMORY.md`) |
| `_STATUS.md` update | State transition to `IN_PROGRESS` (by human/WORKING_ITEMS) | `_STATUS.md` |
| Dependency register | Populated by DEPENDENCIES agent after implementation | `Dependencies.csv` |
| Git commit | Bootstrap commit with `frontend/` workspace | Repository history |

## Failure Handling

If a step fails, consult the following troubleshooting guidance before proceeding. Do not skip failed steps.

| Step | Failure Symptom | Troubleshooting |
|------|----------------|-----------------|
| 1.3 (`npm install`) | Non-zero exit code; dependency resolution errors | Verify Node.js version meets minimum (see Guidance C6; Specification REQ-02 `engines` field). Check for network connectivity to npm registry. Verify `package.json` dependencies are spelled correctly and versions exist on the registry. If `ERESOLVE` peer dependency conflicts occur, review framework version compatibility (Next.js + React + Electron version matrix) |
| 1.4 (`tsc --noEmit`) | Type errors on baseline files | Verify `tsconfig.json` includes correct paths and settings for both Next.js (`jsx: "preserve"`) and Electron (`module: "commonjs"` or `"esnext"` depending on configuration). Check that `@types/react` and `@types/node` are installed |
| 1.9 (`npm run dev`) | Dev server fails to start; Electron window blank | Verify the Next.js dev server starts independently (`npx next dev`) before testing the combined dev script. If Electron opens a blank window, the dev server may not be ready; see Guidance C3 for orchestration approach. Check dev server URL/port configuration in the Electron main process matches the Next.js dev server |
| 1.9 (`npm run build`) | Build fails with exit code != 0 | Check Next.js configuration for invalid settings. If using `output: 'export'`, verify no server-side features (API routes, SSR) are used in the minimal scaffold. Review build output for specific error messages |
| 2.2 (`desktop:pack`) | Packaging fails | Verify electron-builder configuration against REQ-11. Check that the `"main"` field in `package.json` points to a valid compiled JavaScript file (see Guidance C8). Verify `extraResources` paths resolve correctly relative to `frontend/` |
| 2.3 (`desktop:dist`) | DMG creation fails | Verify macOS build tools are available. Check disk space. If `desktop:pack` succeeded but `desktop:dist` fails, the issue is likely in DMG-specific configuration rather than the application bundle itself |
| 2.4 (instruction root check) | `agents/` or `docs/` missing from packaged output | Verify `extraResources` `from` paths in electron-builder configuration. The paths should be relative to the directory where electron-builder runs (typically `frontend/`). Verify the source directories exist at the repository root |
