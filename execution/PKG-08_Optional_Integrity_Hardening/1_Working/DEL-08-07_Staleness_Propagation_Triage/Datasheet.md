# Datasheet — DEL-08-07 Staleness Propagation + Triage Tooling

## Identification

| Field | Value |
|-------|-------|
| **Deliverable ID** | DEL-08-07 |
| **Name** | Staleness Propagation + Triage Tooling |
| **Package** | PKG-08 — Optional Integrity Hardening |
| **Type** | BACKEND_FEATURE_SLICE |
| **Responsible Party** | TBD — **human assignment needed before implementation begins** (Lensing: D-003) |
| **Context Envelope** | L |
| **Scope Item** | SOW-038 (TBD) |
| **Objective** | OBJ-007 — Optional: integrity hardening loop |
| **Lifecycle State** | OPEN |

## Attributes

| Attribute | Value | Source |
|-----------|-------|--------|
| **Scope Status** | TBD — requires human decision to bring IN scope | Decomposition, Scope Ledger (SOW-038) |
| **Effort Estimate** | High | PLAN Section 3.7 |
| **Anticipated Artifacts** | CODE / DOC / TEST / OTHER | Decomposition (DEL-08-07 row) |
| **Staleness Model** | Transitive propagation along dependency edges using baseline SHAs | CONTRACT K-STALE-1; PLAN Section 3.7 |
| **Triage Model** | Human-triaged queue with resolution modes: no impact (clear flag), needs rework, needs review | CONTRACT K-STALE-2 |
| **Dirty Detection Basis** | Governed input change since last approved SHA | CONTRACT K-VAL-1 |
| **Governed Input Definition** | TBD — which files constitute "governed inputs" per deliverable is undefined. Candidates include: the four production documents, `Dependencies.csv`, metadata files (`_STATUS.md`, `_CONTEXT.md`, etc.), or all files in the deliverable folder. **ASSUMPTION: design decision required, likely as part of DEL-08-06 or this deliverable's implementation.** (Lensing: B-001; see also Guidance C3 and Specification REQ-01) | CONTRACT K-VAL-1; Guidance.md C3 |
| **Graph Input Source** | On-demand dependency graph aggregated from deliverable-local `Dependencies.csv` registers | PLAN Section 3.4; **ASSUMPTION: provided by DEL-08-04** |
| **SHA Baseline Source** | Unified pipeline run records with baseline SHAs per deliverable | PLAN Section 3.6; **ASSUMPTION: provided by DEL-08-06** |
| **Output Determinism Requirement** | Outputs must be deterministic and auditable | Decomposition (DEL-08-07 ContextEnvelopeNotes) |
| **Platform** | macOS 15+, Apple Silicon only | DEC-PLAT-001 |
| **Network Policy** | Anthropic API only (no other outbound connections) | DEC-NET-001 |

## Conditions

| Condition | Description | Source |
|-----------|-------------|--------|
| **Scope Gate** | SOW-038 is TBD; this deliverable is contingent on a human scope decision (OI-038) | Decomposition, Open Issues |
| **Dependency Gate** | Likely depends on OI-035 (dependency graph) and OI-037 (run records) also being brought IN scope | Decomposition (OI-038 Notes); PLAN Section 4 |
| **No Central Graph** | System intentionally avoids a central dependency graph; aggregation is on-demand from local registers | CONTRACT K-DEP-1; DIRECTIVE Section 5 |
| **Human Authority** | Staleness triage resolution is a human decision; agents cannot auto-resolve | CONTRACT K-STALE-2 |
| **Filesystem-as-State** | All staleness state must be representable as plain files; no external database | DIRECTIVE Section 2.1 |
| **Immutable Snapshots** | If staleness calculation outputs go to a tool root, they must be immutable snapshots | CONTRACT K-SNAP-1 |
| **Upstream Format Dependency** | Graph artifact format (from DEL-08-04) and run record schema (from DEL-08-06) are not yet defined; this deliverable's implementation is blocked until those formats stabilize. **ASSUMPTION: update this Datasheet when DEL-08-04 and DEL-08-06 formats are defined.** (Lensing: E-001) | PLAN Section 3.4, PLAN Section 3.6 |

## Construction

| Aspect | Description | Source |
|--------|-------------|--------|
| **Input: Dependency Graph** | Project-level dependency graph (JSON/Mermaid) aggregated from `Dependencies.csv` files. **ASSUMPTION: DEL-08-04 output format is TBD; update when defined.** (Lensing: E-001) | PLAN Section 3.4; **ASSUMPTION: DEL-08-04 output** |
| **Input: Run Records** | Unified pipeline run records containing baseline SHAs per deliverable. **ASSUMPTION: DEL-08-06 schema is TBD; update when defined.** (Lensing: E-001) | PLAN Section 3.6; **ASSUMPTION: DEL-08-06 output** |
| **Input: Git SHAs** | Current git SHAs for deliverable folder contents | Git repository |
| **Processing: Staleness Detection** | Compare current SHAs against baseline SHAs from run records; flag dirty deliverables per K-VAL-1 | CONTRACT K-VAL-1 |
| **Processing: Propagation** | Traverse DOWNSTREAM EXECUTION edges from dirty deliverables to propagate staleness transitively to all reachable dependents per K-STALE-1 | CONTRACT K-STALE-1 |
| **Output: Staleness Report** | Report listing stale deliverables with propagation paths and triage status | **ASSUMPTION: artifact type TBD** |
| **Output: Triage Queue** | Human-facing triage queue with per-item resolution options (no impact, rework, review) | CONTRACT K-STALE-2 |
| **Output Format** | TBD — must be deterministic, auditable, and filesystem-representable | Decomposition notes; DIRECTIVE Section 2.1 |
| **CLI/Script Entry Point** | TBD — a CLI or script entry point is required, invocable from the project root, that orchestrates graph loading, dirty detection, propagation, and report/triage-queue generation. Location, naming convention, and invocation pattern to be defined during implementation. (Lensing: F-002; see also Procedure Step A6) | PLAN Section 3.7; Procedure.md Step A6 |

## References

| Reference | Relevance |
|-----------|-----------|
| Decomposition (G7-APPROVED) | DEL-08-07 definition, SOW-038, OBJ-007, Open Issue OI-038 |
| `docs/CONTRACT.md` | K-STALE-1, K-STALE-2, K-VAL-1, K-DEP-1, K-SNAP-1 invariants |
| `docs/PLAN.md` Section 3.7 | Staleness Calculation Tooling — effort, dependencies, rationale |
| `docs/PLAN.md` Section 3.4 | On-Demand Dependency Graph Generation (upstream dependency) |
| `docs/PLAN.md` Section 3.6 | Run Record Persistence (upstream dependency) |
| `docs/PLAN.md` Section 4 | Sequencing Rationale — staleness depends on graph + run records |
| `docs/DIRECTIVE.md` | Filesystem-as-state, git-as-event-store, human authority constraints |
| `docs/SPEC.md` Section 6 | Dependencies.csv v3.1 schema (input to graph traversal) |
| `docs/TYPES.md` Section 3 | Dependency vocabulary (edge classes, directions, types) |
