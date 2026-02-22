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

**ASSUMPTION:** The specific dev script orchestration (e.g., `concurrently`, `wait-on`, or manual steps) is TBD.

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

**ASSUMPTION:** Exact paths and configuration TBD based on final directory structure decisions.

### C5: Relationship to DEL-01-01 and DEL-01-02

DEL-01-03 is a prerequisite for both sibling deliverables in PKG-01:

- **DEL-01-01 (macOS Build Baseline):** Needs a buildable `frontend/` to verify that the repo builds and runs reliably on macOS 15+ Apple Silicon. DEL-01-03 provides the workspace; DEL-01-01 verifies and hardens the build process.
- **DEL-01-02 (Unsigned DMG Packaging):** Needs working packaging scripts to establish the full DMG workflow. DEL-01-03 provides the `desktop:pack`/`desktop:dist` baseline; DEL-01-02 verifies the end-to-end DMG packaging path for local builders.

**ASSUMPTION:** These dependency relationships are implicit from the Decomposition structure. The `_DEPENDENCIES.md` register has not yet been populated.

### C6: Node.js Version Expectations

The bootstrap should specify or document the expected Node.js version. Given the macOS 15+ / Apple Silicon constraint and the use of modern frameworks:
- Node.js 20 LTS or later is a reasonable baseline
- The `engines` field in `package.json` should declare the minimum supported version

**ASSUMPTION:** Specific Node.js version TBD.

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
  electron/
    main.ts               # Electron main process
    preload.ts            # Preload script
  src/                    # or app/ -- Next.js application source
    app/
      layout.tsx          # Root layout
      page.tsx            # Root page (minimal)
  public/                 # Static assets
```

## Conflict Table (for human ruling)

No conflicts detected between sources during this pass. If conflicts emerge during implementation, they will be recorded here.

| Conflict ID | Conflict | Source A | Source B | Impacted Sections | Proposed Authority | Human Ruling |
|-------------|----------|----------|----------|-------------------|-------------------|--------------|
| (none) | | | | | | |
