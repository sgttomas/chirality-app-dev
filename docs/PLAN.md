# PLAN — Development Roadmap

This document captures the development roadmap for the Chirality project execution system. It summarizes what has been codified, identifies future hardening candidates, and provides sequencing rationale.

## Control-Plane Boundary

- `docs/PLAN.md` is strategic: it explains priorities, rationale, and roadmap direction.
- Operational sequencing/blocker policy is governed by `execution/_Coordination/_COORDINATION.md`.
- Current run-state pointers and immediate queue belong in `execution/_Coordination/NEXT_INSTANCE_STATE.md`.

## Local-Only Source Policy

- Development guidance and execution evidence must come from files in this repository.
- Do not rely on non-local repositories or external clones as authoritative sources.
- If a referenced runtime path is absent in this workspace (for example `frontend/`), treat deliverable documents under `execution/PKG-*/1_Working/DEL-*/` as the implementation contract and record a local blocker in coordination artifacts.

---

## 1. Completed: System Hardening

The working system has been codified into formal governance documents and aligned to the active agent framework.

### Governance Documents Written

| Document | Purpose | Status |
|----------|---------|--------|
| `docs/SPEC.md` | Physical structures, file formats, Dependencies.csv v3.1 schema, folder layout, validation checklist | Complete |
| `docs/TYPES.md` | Domain vocabulary, hierarchy, stable IDs, dependency vocabulary, agent roles, lifecycle states | Complete |
| `docs/DIRECTIVE.md` | Founding intent, design philosophy, professional responsibility model, scope, constraints | Complete |
| `docs/CONTRACT.md` | Invariant catalog (20 K-* invariants), change policy, enforcement map | Complete |
| `docs/PLAN.md` | This document | Complete |

### Governance Alignment

Current governance documents are internally aligned on the core model:
- Hierarchy is flat `package->deliverable` across `docs/TYPES.md`, `docs/SPEC.md`, and `docs/CONTRACT.md`
- Authoritative execution state is file-based (`_STATUS.md`, `_DEPENDENCIES.md`, `Dependencies.csv`)
- Invariant catalog is centralized in `docs/CONTRACT.md`
- Agent role boundaries and write scopes are defined by the active `AGENT_*.md` instruction suite

### Agent Instruction Hardening

| Change | Agents Affected |
|--------|-----------------|
| QA Contract sections added | PREPARATION, 4_DOCUMENTS, CHIRALITY_FRAMEWORK, CHIRALITY_LENS |
| Output Persistence notes added | ORCHESTRATOR, RECONCILIATION |

Agent instruction consistency: 92% → estimated 95%+ after hardening.

---

## 2. Existing Tooling

### Validation + Example Assets

- `examples/` provides concrete execution-root samples with package/deliverable structures and semantic artifacts (`_SEMANTIC.md`) for regression and conformance testing.
- `docs/harness/` documents SDK runtime validation and CI integration for harness behavior.
- `frontend/scripts/validate-harness-*.mjs` is now an explicit build target under the frontend baseline scope.

### DEL-03-05 Policy Rulings (2026-02-23)

- OI-001 key provisioning policy is resolved for current scope: `ENV_ONLY`.
- DEL-03-05 provider completion path is explicitly SDK-first (`ADOPT_SDK_NOW`); direct HTTP provider paths are interim-only and not completion evidence.
- This ruling cycle is documentation/scope preparation only; SDK-path implementation is queued for subsequent sessions.

### Desktop Frontend (`frontend/`) — Explicit In-Scope Build Program

Current state: this repository snapshot does not carry a usable `frontend/` runtime surface. Frontend development is now treated as first-class implementation scope, not assumed pre-existing tooling.

Phased baseline plan:

1. **FE-1 Workspace Bootstrap** (`DEL-01-03`)
   - Create tracked `frontend/` workspace with package manifest, Next/Electron/TypeScript baseline, and development/build scripts.
   - Acceptance: `frontend/package.json` exists; `npm run dev` and `npm run build` resolve from `frontend/` without referencing non-local repos.
2. **FE-2 Harness API Baseline** (`DEL-03-07`)
   - Implement baseline `/api/harness/session/*` and `/api/harness/turn` route surfaces with typed failure contracts.
   - Acceptance: route handlers compile and pass baseline route-contract tests.
3. **FE-3 Workflow UI Shell Baseline** (`DEL-02-05`)
   - Implement PORTAL/PIPELINE shell, project-root selection path, file tree panel, and chat panel baseline.
   - Acceptance: local run demonstrates end-to-end UI boot and route wiring against local workspace data.
4. **FE-4 Validation + Packaging Baseline** (`DEL-07-03` + `DEL-01-03`)
   - Implement harness validation scripts and local runbooks; establish packaging baseline (`desktop:pack`/`desktop:dist`).
   - Acceptance: deterministic summary artifact is produced locally and packaging flow yields auditable artifact outputs.

### Matrix Navigation + Pipeline Taxonomy

The desktop UI uses a 3x4 matrix to route operator intent into WORKBENCH or PIPELINE.

- Columns (shared): `GUIDING`, `APPLYING`, `JUDGING`, `REVIEWING`
- Rows:
  - `NORMATIVE` -> opens `WORKBENCH`
  - `OPERATIVE` -> opens `PIPELINE`
  - `EVALUATIVE` -> opens `WORKBENCH`

Matrix cells:

| Row | Guiding | Applying | Judging | Reviewing |
|-----|---------|----------|---------|-----------|
| `NORMATIVE` | `HELP` | `ORCHESTRATE` | `WORKING_ITEMS` | `AGGREGATE` |
| `OPERATIVE` | `DECOMP*` | `PREP*` | `TASK*` | `AUDIT*` |
| `EVALUATIVE` | `AGENTS` | `DEPENDENCIES` | `CHANGE` | `RECONCILING` |

PIPELINE category model:

- `DECOMP*`
- `PREP*`
- `TASK*`
- `AUDIT*`

Option policy:

- Requested but unsupported variants remain visible as disabled entries.
- Disabled entries are intentionally non-selectable and rendered as "coming soon".

`TASK*` selector model:

- Uses split selectors instead of one mixed list:
  - `Task Agent` (static options)
  - `Scope` selectors (dynamic options)
- Dynamic scope sources:
  - Deliverables scanned from the selected working root
  - Knowledge types scanned from canonical deliverable file types
- Knowledge-type scope is shown only when a knowledge decomposition marker is found in `_Decomposition`.

---

## 3. Future Hardening Candidates

Ordered by priority (highest first):

### 3.1 Content Hash Implementation for `_REFERENCES.md`

**What:** Add SHA-256 content hashes for out-of-folder references, aligned with no-ghost-input constraints (`K-GHOST-1`) and provenance requirements (`K-PROV-1`).

**Why:** Currently `_REFERENCES.md` lists paths and descriptions but does not verify that referenced content hasn't changed since sealing. Content hashes would enable automated integrity checking.

**Effort:** Medium. Requires changes to PREPARATION (hash computation on scaffold), ORCHESTRATOR (hash verification before pipeline runs), and tooling (hash generation/verification scripts).

### 3.2 Dependencies.csv Schema Linter

**What:** A validation script that reads `Dependencies.csv` files and checks them against the v3.1 schema defined in `docs/SPEC.md` Section 6.

**Why:** Schema violations are currently caught only by agent-internal quality checks. An external linter would enable CI-level validation and catch drift across deliverables.

**Effort:** Low. The schema is fully specified. Implementation is a Python script that validates column presence, enum values, identity rules, and provenance requirements.

### 3.3 Automated Folder Structure Validator

**What:** A script that walks the execution root and validates each deliverable folder against the checklist in `docs/SPEC.md` Section 12.

**Why:** Missing files or unexpected structures are currently detected only during agent runs. A standalone validator enables pre-run checks and CI integration.

**Effort:** Low. The validation rules are fully defined.

### 3.4 On-Demand Dependency Graph Generation

**What:** A tool that aggregates deliverable-local `Dependencies.csv` files into a project-level dependency graph (JSON or Mermaid).

**Why:** The system intentionally avoids a central dependency graph to prevent sync burden. However, on-demand generation from the authoritative local registers would enable visualization, critical path analysis, and cycle detection without maintaining a separate artifact.

**Effort:** Medium. Requires traversal of all `Dependencies.csv` files, ID resolution, and graph output format.

### 3.5 Lock Mechanism Formalization

**What:** Formalize a deliverable-level lock mechanism for concurrent task execution.

**Why:** Concurrent agent execution on the same deliverable is prevented by convention but not enforced. A lock mechanism (e.g., `.lock` file with lease semantics) would enable safe parallel pipeline execution.

**Effort:** Medium-high. Requires lock acquisition/release protocol, orphan recovery, and integration into agent instructions.

### 3.6 Run Record Persistence

**What:** Formalize a unified pipeline run record schema.

**Why:** Currently, pipeline runs are tracked in `_STATUS.md` history and `_DEPENDENCIES.md` run history, but there is no unified run record per Agent 2 execution. Formal run records would enable better audit trails and rerun management.

**Effort:** Medium. Requires schema definition, storage location decision, and integration into task agent protocols.

### 3.7 Staleness Calculation Tooling

**What:** Implement staleness propagation and triage tooling based on dependency edges and baseline SHAs.

**Why:** Staleness is a contract commitment (K-STALE-1, K-STALE-2) but currently relies on human observation. Automated staleness detection from the dependency graph + git SHAs would make the system's integrity guarantees enforceable.

**Effort:** High. Depends on 3.4 (dependency graph generation) and 3.6 (run records with baseline SHAs).

---

## 4. Sequencing Rationale

The future candidates are ordered to build on each other:

1. **Schema linter + folder validator** (3.2, 3.3) — low effort, high immediate value, no dependencies.
2. **Content hashes** (3.1) — enables no-ghost-inputs enforcement.
3. **Dependency graph generation** (3.4) — enables visualization and analysis.
4. **Lock mechanism** (3.5) — enables safe parallel execution.
5. **Run records** (3.6) — enables audit trails.
6. **Staleness calculation** (3.7) — depends on graph + run records; completes the governance loop.

---

EOF
