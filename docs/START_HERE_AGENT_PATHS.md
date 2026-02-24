# Start Here: Learning Paths for Working with Agents

This document is the onboarding entry point for newcomers who want to learn how to work with and build with agents in this project.

You can start from one of three context levels:

1. `docs/` only
2. `docs/` + decomposition file
3. `docs/` + decomposition file + semantically enriched deliverable folders

Each path gives a different view of agent behavior and a different level of operational depth.

---

## Project Objective (What Completion Produces)

If this project is taken to completion, the result is:

- A working Chirality desktop harness that runs agents against a user-selected working root (`projectRoot`) with filesystem-as-state.
- A governed, auditable agent operating system (agent instructions + governance docs + decomposition + lifecycle + dependency records).
- A complete in-scope deliverable set progressed through lifecycle to issuance, with immutable evidence under tool roots (reconciliation, closure, change, estimates/schedule where applicable).

In short: a deployable agent execution environment plus the full governance and execution artifacts needed to operate it responsibly.

---

## Choose a Start Path

| Path | Use When | What You Will Learn | Typical Agent Interaction Depth |
|---|---|---|---|
| Path 1: `docs/` only | You are brand new and want the mental model first | Governance, invariants, vocabulary, lifecycle, and role boundaries | Conceptual and policy-level interactions |
| Path 2: `docs/` + decomposition | You want to see how scope is operationalized | How scope becomes packages/deliverables/objectives/open issues and change control | Structure and sequencing interactions |
| Path 3: `docs/` + decomposition + deliverables | You want real execution behavior | How agents perform local work, manage dependencies, run control loops, and produce evidence | Full execution interactions |

---

## Path 1: `docs/` Only

### Inputs

- `docs/DIRECTIVE.md`
- `docs/CONTRACT.md`
- `docs/SPEC.md`
- `docs/TYPES.md`
- `docs/PLAN.md`

### What to Do with Agents

Use persona agents to interpret and explain the framework:

- `HELP_HUMAN`: ask for a newcomer briefing, glossary, and workflow checklist.
- `HELPS_HUMANS`: ask why the instruction architecture is structured as Type 0/1/2.
- `ORCHESTRATOR`: ask for a simulated control-loop walkthrough without execution writes.

### Expectations

- You will understand intent, constraints, and terminology.
- You will not yet have execution truth (no scoped package/deliverable graph context).
- You can reason about what should happen, but not yet verify what is happening in a concrete instance.

### Exit Criteria

You can explain:

- what “filesystem is the state” means,
- why humans remain final authority,
- how lifecycle and dependency tracking work,
- how Type 0/1/2 responsibilities differ.

---

## Path 2: `docs/` + Decomposition File

### Inputs

- All Path 1 inputs
- Active decomposition file under `execution/_Decomposition/`
  - Current project example: `execution/_Decomposition/ChiralityApp_SoftwareDecomposition_2026-02-21_G7-APPROVED.md`

### What to Do with Agents

Use persona agents to work from real scoped structure:

- `ORCHESTRATOR`: request tier/blocker-front summaries from decomposition + coordination policy.
- `SCOPE_CHANGE`: simulate or perform amendment flow (intake -> impact -> propagation).
- `RECONCILIATION`: review cross-deliverable coherence at graph/interface level.

### Expectations

- You gain scope truth: stable IDs, package boundaries, deliverable responsibilities, objective mappings, open-issue traceability.
- You can understand sequencing intent and change-control behavior.
- You still do not have full implementation truth unless deliverable folders are present and populated.

### Exit Criteria

You can:

- trace any `SOW-*` to `PKG-*` and `DEL-*`,
- explain current scope IN/OUT decisions and their implications,
- describe how an amendment propagates without breaking ID stability.

---

## Path 3: `docs/` + Decomposition + Enriched Deliverable Folders

### Inputs

- All Path 1 and Path 2 inputs
- Deliverable folders under `execution/PKG-*/1_Working/DEL-*` including metadata and production docs
  - `_CONTEXT.md`, `_STATUS.md`, `_REFERENCES.md`, `_DEPENDENCIES.md`, `Dependencies.csv`, `MEMORY.md`
  - production docs (PROJECT/SOFTWARE: Datasheet/Specification/Guidance/Procedure)
  - optional semantic artifacts (`_SEMANTIC.md`, `_SEMANTIC_LENSING.md`)

### What to Do with Agents

Use full operational workflow:

- `WORKING_ITEMS` + `TASK`: execute deliverable-local work in bounded sessions.
- `DEPENDENCIES`: extract and refresh dependency registers.
- `RECONCILIATION` + `AUDIT_DEP_CLOSURE`: validate cross-deliverable graph health.
- `CHANGE`: publish coherent commits after verification.

### Expectations

- You see actual agent execution behavior: local writes, evidence-backed updates, reruns, lifecycle movement, and control-loop fan-in/fan-out.
- You can compare policy intent vs implementation state and detect drift.
- You can run real progression cycles from unblocked work through checking/issuance with auditability.

### Exit Criteria

You can:

- execute a tier control loop end-to-end,
- validate dependency and reconciliation outputs,
- produce a clean handoff state for the next session.

---

## Recommended Learning Progression

1. Start in Path 1 to establish vocabulary and constraints.
2. Move to Path 2 to understand decomposition as operational authority.
3. Move to Path 3 to run real agent workflows and produce verifiable outputs.

---

## Safety and Responsibility Notes

- Treat agent output as draft or structured assistance until reviewed.
- Keep project truth on disk; do not rely on hidden memory.
- Respect write scopes and lifecycle authority (`_STATUS.md`).
- Use `MEMORY.md` for deliverable-local memory; do not create `_MEMORY.md` in this project profile.

