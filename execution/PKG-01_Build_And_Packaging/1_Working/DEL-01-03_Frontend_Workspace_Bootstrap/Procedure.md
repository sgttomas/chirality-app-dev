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
| Specification.md | This deliverable folder | Requirements REQ-01 through REQ-11 |

### Upstream Dependencies

| Dependency | Status | Notes |
|------------|--------|-------|
| None declared | -- | `_DEPENDENCIES.md` upstream section not yet populated. **ASSUMPTION:** No formal upstream blockers exist for this deliverable since it creates the foundational workspace. |

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

Create the minimum Next.js application structure:
- Root layout file (`frontend/src/app/layout.tsx` or `frontend/app/layout.tsx`)
- Root page file (`frontend/src/app/page.tsx` or `frontend/app/page.tsx`)
- Minimal content sufficient to verify the application loads

Verify: Application source files exist.

#### Step 1.9: Verify Development Scripts

Run the development scripts to confirm they resolve:

```bash
cd frontend && npm run dev
# Verify: Next.js dev server starts; Electron window opens (if dev script includes Electron launch)
# Ctrl+C to stop

cd frontend && npm run build
# Verify: Build completes with exit code 0; output directory is created
```

Verify: REQ-06 acceptance criteria met.

#### Step 1.10: Add Frontend to Git Tracking

```bash
git add frontend/
# Note: ensure node_modules/ is in .gitignore
```

Verify: `frontend/` directory is git-tracked (REQ-01).

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

Verify:
- Command exits successfully
- Unpacked application directory is created in the output location (e.g., `frontend/dist/mac-arm64/`)
- The unpacked application contains the instruction root directories (`agents/`, `docs/`) (REQ-09)

#### Step 2.3: Verify `desktop:dist` Script

```bash
cd frontend && npm run desktop:dist
```

Verify:
- Command exits successfully
- A `.dmg` file is created in the output location (e.g., `frontend/dist/`)
- The `.dmg` targets macOS arm64 (REQ-07, REQ-08)

#### Step 2.4: Instruction Root Inclusion Check

After `desktop:pack`, verify instruction root presence in the packaged output:

```bash
# Check unpacked app for instruction root content
ls -la "frontend/dist/mac-arm64/Chirality.app/Contents/Resources/agents/"
ls -la "frontend/dist/mac-arm64/Chirality.app/Contents/Resources/docs/"
```

**ASSUMPTION:** Exact paths depend on electron-builder output structure and configuration.

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
