# Datasheet: DEL-01-03 Frontend Workspace Bootstrap & Packaging Baseline

## Identification

| Field | Value |
|-------|-------|
| Deliverable ID | DEL-01-03 |
| Name | Frontend Workspace Bootstrap & Packaging Baseline |
| Package | PKG-01 Build & Packaging |
| Type | CI_CD_CHANGE |
| Context Envelope | L |
| Responsible Party | TBD |
| Amendment | Scope Amendment A1 (SCA-001, 2026-02-22) |
| Decomposition | `execution/_Decomposition/ChiralityApp_SoftwareDecomposition_2026-02-21_G7-APPROVED.md` |

## Attributes

| Attribute | Value | Source |
|-----------|-------|--------|
| Target Platform | macOS 15+, Apple Silicon only | Decomposition DEC-PLAT-001 |
| Runtime Framework | Next.js + Electron + TypeScript | `_CONTEXT.md`; PLAN.md Section 2 FE-1 |
| Package Manager | npm | PLAN.md Section 2 FE-1 (acceptance criteria reference `npm run dev`, `npm run build`) |
| Workspace Location | `frontend/` (in-repo, tracked) | `_CONTEXT.md`; SOW-044 |
| Non-local Dependency Policy | No non-local repository dependency allowed for execution | `_CONTEXT.md`; OBJ-008 acceptance criteria |
| Signing/Notarization | Not required | Decomposition DEC-PLAT-001 |
| Distributable Format | `.dmg` (packaging baseline only; full DMG workflow is DEL-01-02) | Decomposition DEL-01-02 context; SOW-047 |
| Instruction Root Inclusion | Instruction root (`agents/`, `docs/`) must be included in packaging artifacts | `_CONTEXT.md`; SOW-047 |

## Conditions

| Condition | Description | Source |
|-----------|-------------|--------|
| Pre-tier Gate | This deliverable blocks Tier-2 code-bearing work that depends on frontend paths (DEL-01-01, DEL-03-01, DEL-05-03, DEL-05-04) | Decomposition, Scope Amendment A1, Execution Gating Rule |
| Local-Only Source Policy | Development guidance and execution evidence must come from files in this repository | PLAN.md, Local-Only Source Policy |
| No `frontend/` Currently Exists | Repository snapshot does not carry a usable `frontend/` runtime surface; this deliverable creates it | PLAN.md Section 2 ("Current state") |

## Construction

### Scope Coverage

| Scope Item | Statement | Source |
|------------|-----------|--------|
| SOW-044 | Create an in-repo `frontend/` workspace baseline (package manifest, build config, TypeScript/Next/Electron scaffolding, and startup scripts) | Decomposition, Scope Amendment A1 |
| SOW-047 | Implement frontend desktop packaging baseline (`desktop:pack`/`desktop:dist`) and instruction-root inclusion checks in local build artifacts | Decomposition, Scope Amendment A1 |

### Objective Mapping

| Objective | Statement | Association |
|-----------|-----------|-------------|
| OBJ-001 | Working macOS desktop build and install path (macOS 15+, Apple Silicon) | Explicit (Decomposition Scope Ledger Overlay) |
| OBJ-008 | Local frontend runtime baseline exists and is executable from this repository only | Explicit (Decomposition Scope Ledger Overlay) |

### Anticipated Artifacts

| Artifact Type | Description |
|---------------|-------------|
| CODE | TypeScript/Next.js/Electron source scaffolding in `frontend/` |
| CONFIG | `package.json`, `tsconfig.json`, `next.config.*`, Electron configuration, electron-builder configuration |
| SCRIPT | Development scripts (`npm run dev`, `npm run build`), packaging scripts (`desktop:pack`, `desktop:dist`) |
| DOC | Deliverable-local documentation (this document kit) |

### Phased Plan Positioning

| Phase | Label | Deliverable(s) | Relevance to DEL-01-03 |
|-------|-------|-----------------|------------------------|
| FE-1 | Workspace Bootstrap | DEL-01-03 | Primary -- creates the `frontend/` workspace, package manifest, baseline scaffolding, and dev/build scripts |
| FE-4 | Validation + Packaging Baseline | DEL-07-03 + DEL-01-03 | Packaging portion -- establishes `desktop:pack`/`desktop:dist` and instruction-root inclusion checks |

Source: PLAN.md Section 2

### Sibling Deliverables in PKG-01

| Deliverable | Name | Relationship |
|-------------|------|--------------|
| DEL-01-01 | macOS 15+ Apple Silicon Build Baseline | Downstream consumer; depends on `frontend/` existing to build reliably |
| DEL-01-02 | Unsigned DMG Packaging Workflow | Downstream consumer; depends on packaging baseline from DEL-01-03 |

## References

| Reference | Location | Relevance |
|-----------|----------|-----------|
| Decomposition | `execution/_Decomposition/ChiralityApp_SoftwareDecomposition_2026-02-21_G7-APPROVED.md` | Scope Amendment A1 defines DEL-01-03 |
| PLAN.md | `docs/PLAN.md` | Section 2: FE-1 and FE-4 phased plan |
| SPEC.md | `docs/SPEC.md` | Physical structure requirements, deliverable folder layout |
| _CONTEXT.md | `execution/PKG-01_Build_And_Packaging/1_Working/DEL-01-03_Frontend_Workspace_Bootstrap/_CONTEXT.md` | Deliverable identity and scope |
| _DEPENDENCIES.md | `execution/PKG-01_Build_And_Packaging/1_Working/DEL-01-03_Frontend_Workspace_Bootstrap/_DEPENDENCIES.md` | Dependency declarations (not yet populated) |
