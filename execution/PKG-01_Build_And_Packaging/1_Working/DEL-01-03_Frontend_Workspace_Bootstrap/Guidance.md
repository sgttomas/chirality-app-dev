# Guidance: DEL-01-03 Frontend Workspace Bootstrap & Packaging Baseline

## Purpose

This deliverable exists because the repository does not currently carry a usable `frontend/` runtime surface (PLAN.md Section 2, "Current state"). Prior execution assumptions treated `frontend/` as already available; the local-only execution policy requires that frontend runtime and packaging surfaces be developed from this repository state.

DEL-01-03 is the foundational enabler for all frontend-dependent work. It was added via Scope Amendment A1 (SCA-001) specifically to resolve the gap between the decomposition's implicit assumption of a working frontend and the repository's actual state. Until this deliverable reaches at least `IN_PROGRESS`, Tier-2 code-bearing work that depends on frontend paths remains blocked per the Execution Gating Rule.

Source: Decomposition Scope Amendment A1; PLAN.md Section 2

## Principles

### P1: Bootstrap, Not Feature-Complete

This deliverable establishes the **minimum viable frontend workspace** -- enough scaffolding that downstream deliverables (DEL-01-01, DEL-01-02, DEL-02-05, DEL-03-07, DEL-07-03) can begin their work. It is explicitly not the place to implement:
- Harness API routes (DEL-03-07)
- UI workflow shell (DEL-02-05)
- Validation scripts (DEL-07-03)
- Full build optimization (DEL-01-01)

The acceptance bar is: `npm run dev` starts, `npm run build` succeeds, `desktop:pack`/`desktop:dist` produce artifacts with instruction-root content included.

Source: PLAN.md Section 2 FE-1 acceptance criteria

### P2: Self-Contained Repository Execution

All execution must work from a single `git clone` of this repository plus standard npm registry access. No workspace links to external repos, no git submodules pointing elsewhere, no assumed pre-existing global installations beyond Node.js and npm.

This principle derives from OBJ-008 ("no non-local repository is required for execution") and the Local-Only Source Policy in PLAN.md.

Source: OBJ-008 acceptance criteria; PLAN.md Local-Only Source Policy

### P3: Instruction Root Is Part of the Product

The instruction root (`agents/`, `docs/`) is not auxiliary documentation -- it is release-managed content that ships inside the app bundle. The packaging baseline must include it from the start, not as an afterthought.

This principle derives from SOW-047 ("instruction-root inclusion checks") and the Vocabulary Map entry for "Instruction Root" which defines it as "Release-managed instructions/docs shipped inside the app bundle."

Source: Decomposition Vocabulary Map; SOW-047; SOW-013

### P4: Platform Narrowness Is Intentional

Targeting only macOS 15+ Apple Silicon is a deliberate decision (DEC-PLAT-001), not an oversight. Do not add Windows or Linux targets, Intel architecture support, or cross-compilation infrastructure. This keeps the packaging baseline simple and the test matrix bounded.

Source: Decomposition DEC-PLAT-001

## Vocabulary Notes

The following terminology conventions apply across all four documents for this deliverable. Where inconsistencies are found, these are the authoritative forms.

| Term | Convention | Notes |
|------|-----------|-------|
| Next.js application source directory | `frontend/src/app/` | The App Router convention using `src/` prefix. All documents should use this form, not `frontend/app/` or `app/` alone. If the `src/` directory is not used, update this convention before implementation |
| Packaging output directory | `frontend/dist/` | Generic reference to the electron-builder output root. Specific subdirectories (e.g., `mac-arm64/`) depend on electron-builder configuration and should be referenced as `frontend/dist/<platform-arch>/` or parameterized when exact paths are unknown |
| Instruction root directories | `agents/` and `docs/` (relative to repository root) | Packaged into app resources via `extraResources` (see C4). At runtime, accessible via `process.resourcesPath` in the Electron main process |
| Electron entry point source | `frontend/electron/main.ts` | TypeScript source file. The compiled JavaScript output path depends on the build toolchain and `package.json` `"main"` field configuration (see C8) |

Source: Normalization items B-004, F-002 from `_SEMANTIC_LENSING.md`; cross-document terminology audit

## Considerations

### C1: Next.js + Electron Integration Pattern

There are multiple approaches for combining Next.js with Electron:

| Approach | Description | Trade-offs |
|----------|-------------|------------|
| Static export + file:// | Next.js `output: 'export'`, Electron loads static files | Simplest; no SSR; limited API routes in production |
| Custom server in main process | Next.js custom server started by Electron main | Full SSR/API routes; more complexity; port management |
| nextron / electron-next patterns | Community wrappers for Next+Electron | Convenience; additional dependency; may conflict with local-only policy |

**ASSUMPTION:** The specific integration pattern is TBD. The bootstrap should choose the simplest viable approach that supports the harness API routes needed by DEL-03-07 (which requires `POST /api/harness/session/*` and `POST /api/harness/turn` endpoints). This likely means a custom server approach rather than pure static export, since API routes need a server runtime.

### C2: Electron-Builder vs. Alternatives

`electron-builder` is the most commonly used packaging tool for Electron applications and supports `.dmg` output natively. Alternatives include:
- `electron-forge`: Officially supported by Electron; plugin-based; may require more configuration
- `electron-packager` + custom DMG tooling: Lower-level; more manual work

**ASSUMPTION:** electron-builder is assumed as the packaging tool. This assumption should be validated during implementation.

### C3: Development Workflow Ergonomics

The bootstrap should support a development workflow where:
1. `npm run dev` starts both the Next.js dev server and Electron in development mode
2. Hot reload works for renderer (Next.js) changes
3. Main process changes require a restart (standard Electron behavior)

**ASSUMPTION:** The specific dev script orchestration (e.g., `concurrently`, `wait-on`, or manual steps) is TBD. **Resolution criteria:** The mechanism must start the Next.js dev server first, then launch Electron once the dev server is ready (to avoid Electron loading a blank page). Common approaches:

| Approach | Pros | Cons |
|----------|------|------|
| `concurrently` + `wait-on` | Single `npm run dev` command; automatic coordination | Two additional dev dependencies |
| Manual two-terminal workflow | No extra dependencies | Poor ergonomics; not scriptable |
| Custom Node.js launcher script | No extra deps; full control | More custom code to maintain |

Human or architect ruling needed before implementation. The chosen approach should be reflected in Procedure Step 1.9.

### C4: Instruction Root Inclusion Mechanism

For REQ-09 (instruction root in packaging artifacts), the likely approach is `electron-builder`'s `extraResources` configuration:

```json
{
  "build": {
    "extraResources": [
      { "from": "../agents", "to": "agents" },
      { "from": "../docs", "to": "docs" }
    ]
  }
}
```

This would place the instruction root content alongside the application resources, accessible at runtime via `process.resourcesPath`.

At runtime within the packaged Electron application, the instruction root content would be accessible via:

```javascript
const path = require('path');
const agentsPath = path.join(process.resourcesPath, 'agents');
const docsPath = path.join(process.resourcesPath, 'docs');
```

This is the standard Electron mechanism for accessing `extraResources` content. The `agents/` and `docs/` directories specifically constitute the instruction root because they contain release-managed instructions and documentation that must ship inside the app bundle (SOW-047; SOW-013; Vocabulary Map "Instruction Root" entry). REQ-09 mandates their inclusion and verification; the `extraResources` approach makes them available at a predictable path without exposing them to renderer-process `require()` calls.

**ASSUMPTION:** Exact `from` paths in `extraResources` depend on final directory structure decisions. The `../agents` and `../docs` paths assume electron-builder runs from `frontend/` and the instruction root lives at the repository root.

### C5: Relationship to DEL-01-01 and DEL-01-02

DEL-01-03 is a prerequisite for both sibling deliverables in PKG-01:

- **DEL-01-01 (macOS Build Baseline):** Needs a buildable `frontend/` to verify that the repo builds and runs reliably on macOS 15+ Apple Silicon. DEL-01-03 provides the workspace; DEL-01-01 verifies and hardens the build process.
- **DEL-01-02 (Unsigned DMG Packaging):** Needs working packaging scripts to establish the full DMG workflow. DEL-01-03 provides the `desktop:pack`/`desktop:dist` baseline; DEL-01-02 verifies the end-to-end DMG packaging path for local builders.

These dependency relationships are confirmed by the `_DEPENDENCIES.md` register (COMPLETE; 13 rows), which includes DOWNSTREAM PREREQUISITE edges for all five consumers (DEP-01-03-009 through DEP-01-03-013). The DEL-01-01 and DEL-01-02 dependencies were initially implicit from the Decomposition structure and are now formally registered.

### C6: Node.js Version Expectations

The bootstrap should specify or document the expected Node.js version. Given the macOS 15+ / Apple Silicon constraint and the use of modern frameworks:
- Node.js 20 LTS or later is a reasonable baseline
- The `engines` field in `package.json` should declare the minimum supported version

**ASSUMPTION:** Specific Node.js version TBD.

### C7: Electron Security Baseline

The Electron preload script (`frontend/electron/preload.ts`, listed as a required artifact in Specification REQ-12) exists to enforce Electron's security best practices. The bootstrap should establish the following security posture from the start:

| Setting | Value | Rationale |
|---------|-------|-----------|
| `contextIsolation` | `true` | Prevents renderer-process code from accessing Electron/Node.js internals directly; the preload script is the only bridge |
| `nodeIntegration` | `false` | Prevents renderer-process code from using Node.js APIs; all Node.js access must go through the preload script's exposed API |
| `sandbox` | `true` (recommended) | Further restricts renderer process capabilities; standard for modern Electron apps |

The preload script's role is to selectively expose main-process capabilities to the renderer via `contextBridge.exposeInMainWorld()`. At bootstrap scope, the preload script MAY be minimal (e.g., exposing no APIs), but the security configuration (`contextIsolation: true`, `nodeIntegration: false`) MUST be set in the BrowserWindow `webPreferences` from the beginning.

This is not an afterthought optimization -- retrofitting security settings into an application that assumed `nodeIntegration: true` is significantly harder than starting with the secure defaults.

Source: Electron security documentation (public); Procedure Step 1.7 (ASSUMPTION on contextIsolation); Specification REQ-12

### C8: Electron Entry Point Location and Build Toolchain Resolution

The Electron main process source file (`frontend/electron/main.ts`) is a TypeScript file that must be compiled to JavaScript before Electron can execute it. The `package.json` `"main"` field must point to the compiled output, not the TypeScript source.

**ASSUMPTION:** The build toolchain for the Electron main process is TBD. Options include:
- `tsc` (direct TypeScript compilation) -- simple but requires separate build step
- `electron-builder` with a `beforeBuild` hook -- integrates into packaging but couples compilation to packaging
- `tsup` or `esbuild` -- fast bundlers that can compile TypeScript for Electron main process

The `"main"` field in `package.json` should point to the compiled entry point (e.g., `"main": "electron/main.js"` or `"main": "dist/electron/main.js"` depending on output configuration). This must be reconciled with how `npm run dev` launches Electron in development mode (where `ts-node` or `tsx` might be used to run TypeScript directly).

Human or architect ruling needed on the compilation approach before implementation.

Source: Procedure Step 1.6; Specification REQ-05; _SEMANTIC_LENSING.md E-001

## Trade-offs

### T1: Scaffold Depth vs. Speed

**Tension:** A deeper scaffold (more pages, components, utility libraries) would give downstream deliverables a head start, but takes longer to produce and may introduce opinions that conflict with downstream implementation decisions.

**Guidance:** Prefer minimal scaffolding. The bootstrap should include only what is needed to prove the workspace works: a single page or minimal app shell, the Electron main process, and the packaging configuration. Downstream deliverables own the implementation content.

### T2: Dev Dependency Breadth

**Tension:** Including dev dependencies for linting, formatting, testing, and other tooling makes the workspace more complete, but adds configuration burden and may conflict with project-level tooling decisions.

**Guidance:** Include only the minimum dev dependencies needed for the workspace to function: TypeScript, Next.js, Electron, and the packaging tool. Additional dev tooling can be added by downstream deliverables or project-level decisions.

### T3: Monorepo Structure

**Tension:** The `frontend/` workspace could be structured as an npm workspace (part of a root `package.json`) or as an independent project directory.

**Guidance:** Since the repository root currently has no `package.json`, and the local-only policy discourages complex monorepo tooling, the `frontend/` directory should be a standalone project with its own `package.json`. If a root `package.json` is later needed for monorepo orchestration, that is a separate concern.

**ASSUMPTION:** No root `package.json` currently exists (confirmed). The workspace is standalone.

## Examples

No examples are available from sources for this specific deliverable type. The following is a structural reference only.

### Expected File Structure After Bootstrap

**ASSUMPTION:** This is a proposed structure, not a source-derived requirement. Actual structure will be determined during implementation.

```
frontend/
  package.json            # Package manifest with deps + scripts
  tsconfig.json           # TypeScript configuration
  next.config.mjs         # Next.js configuration
  .gitignore              # Excludes node_modules/, .next/, out/, dist/
  electron/
    main.ts               # Electron main process (see C8 for compilation)
    preload.ts            # Preload script (see C7 for security rationale)
  src/                    # Next.js application source (using src/ prefix convention)
    app/
      layout.tsx          # Root layout
      page.tsx            # Root page (minimal)
  public/                 # Static assets
```

**Note on directory convention:** This deliverable uses `frontend/src/app/` as the canonical Next.js App Router source path (see Vocabulary Notes above). The `src/` prefix is the Next.js convention for separating application code from configuration files at the project root.

## Open Assumptions Register

The following ASSUMPTION items are scattered across the Specification and Guidance documents. They are consolidated here with proposed resolution criteria so that directive authority can be established before or during implementation. Each must receive a human or architect ruling.

| ID | Assumption | Location(s) | Resolution Criteria | Impact If Unresolved |
|----|-----------|-------------|--------------------|--------------------|
| OA-1 | Next.js output mode (static export vs. custom server) | Specification REQ-04; Guidance C1 | Determine whether DEL-03-07 API routes require a server runtime; if yes, custom server; if no, `output: 'export'` | Affects entire integration pattern, build output structure, and dev workflow |
| OA-2 | electron-builder as packaging tool | Specification REQ-11; Guidance C2 | Evaluate electron-builder vs. electron-forge vs. electron-packager; confirm selection | Affects all packaging configuration, REQ-07/REQ-09/REQ-11 specifics |
| OA-3 | Node.js minimum version | Specification REQ-02; Guidance C6 | Confirm >= 20 LTS or specify exact version; update `engines` field | Affects reproducibility of `npm install` and framework compatibility |
| OA-4 | Instruction root inclusion mechanism (`extraResources` paths) | Specification REQ-09; Guidance C4 | Confirm `from`/`to` paths after directory structure is established | Affects runtime accessibility of `agents/` and `docs/` in packaged app |
| OA-5 | Dev script orchestration mechanism | Guidance C3 | Choose `concurrently` + `wait-on`, manual workflow, or custom launcher | Affects developer ergonomics and `npm run dev` behavior |
| OA-6 | Electron main process compilation approach | Guidance C8 | Choose `tsc`, `tsup`/`esbuild`, or dev-time `tsx`; set `package.json` `"main"` field accordingly | Affects build pipeline, dev workflow, and `package.json` configuration |
| OA-7 | Preload script necessity | Specification REQ-12; Guidance C7 | Confirm Electron security posture (`contextIsolation: true`); if confirmed, preload script is mandatory | Affects security baseline and BrowserWindow configuration |

Source: _SEMANTIC_LENSING.md D-001; cross-document audit of ASSUMPTION markers

## Conflict Table (for human ruling)

No conflicts detected between sources during this pass. If conflicts emerge during implementation, they will be recorded here.

| Conflict ID | Conflict | Source A | Source B | Impacted Sections | Proposed Authority | Human Ruling |
|-------------|----------|----------|----------|-------------------|-------------------|--------------|
| (none) | | | | | | |
