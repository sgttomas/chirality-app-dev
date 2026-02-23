# Specification — DEL-05-01 Instruction Root Bundling & Runtime Access

## Scope

### Covered

This deliverable covers the mechanisms that ensure deployable builds of the Chirality desktop app preserve the separation between:

- **Instruction Root** — release-managed content (agent instructions, framework docs, `AGENTS.md`, `README.md`) bundled inside the app.
- **Working Root (`projectRoot`)** — user-selected filesystem directory where agents read/write project execution state.

It also covers in-app runtime access to instruction root content so that agents and runtime components can locate and read bundled instructions at runtime.

**Source:** Decomposition DEL-05-01 description; SOW-013; DIRECTIVE Section 2.6.

### Excluded

- Working root scaffolding and layout conformance (covered by DEL-05-02).
- Lifecycle state handling (covered by DEL-05-03).
- Dependency tracking file contract (covered by DEL-05-04).
- Session boot and `projectRoot` binding API (covered by DEL-03-01).
- `.dmg` packaging mechanics (covered by DEL-01-02).
- Build baseline (covered by DEL-01-01).

---

## Requirements

### REQ-01: Instruction Root Content Bundling

The build/packaging process MUST include the instruction root content in the deployable app bundle so that instruction files are available without requiring access to the source repository.

**Instruction root content includes:**
- `AGENTS.md` (agent framework index)
- `README.md` (product description)
- `agents/*` (agent instruction files)
- `docs/DIRECTIVE.md`, `docs/CONTRACT.md`, `docs/SPEC.md`, `docs/TYPES.md`, `docs/PLAN.md` (governance documents)

**Source:** DIRECTIVE Section 2.6; Decomposition Vocabulary Map ("Instruction Root" definition).

> **Enrichment note (B-003):** docs/* contents normalized to enumerate individual files consistently. This canonical enumeration (`DIRECTIVE.md`, `CONTRACT.md`, `SPEC.md`, `TYPES.md`, `PLAN.md`) applies across all four production documents.

### REQ-02: Instruction Root vs Working Root Separation at Runtime

At runtime, the system MUST maintain a clear separation between instruction root (read-only, release-managed) and working root (read/write, user-selected).

- Instruction root content MUST NOT be modified by agents during runtime execution.
- Working root content is the only location where agents create, update, or delete project state files.
- **Enforcement mechanism:** The mechanism by which write prevention is achieved at runtime (e.g., filesystem permissions, runtime path guard, API-level restriction) is TBD — to be determined during implementation based on the actual architecture. See Guidance C4 for considerations.

**Source:** DIRECTIVE Section 2.6; DIRECTIVE Section 5 (Structural Constraints: "Instruction root separate from working root").

> **Enrichment note (A-002):** Added explicit acknowledgment that the enforcement mechanism is TBD, with pointer to Guidance C4, rather than leaving "MUST NOT be modified" without specifying how prevention is achieved.

### REQ-03: Runtime Instruction Root Path Resolution

The runtime MUST provide a deterministic mechanism for resolving the instruction root path so that:

1. Agents and runtime components can locate instruction files (agent instructions, governance docs) without hard-coded paths.
2. The resolution works correctly in both development mode (source repo) and packaged mode (`.dmg` / app bundle).

**Source:** Decomposition DEL-05-01 description ("in-app access to instructions"); **ASSUMPTION** — resolution mechanism specifics are TBD (implementation detail).

### REQ-04: Instruction Root Content Integrity

The bundled instruction root content MUST be the same content that was present in the source repository at build time. The build process MUST NOT modify, filter, or transform instruction file content during bundling.

**Source:** CONTRACT K-AUTH-2 (approvals bind to specific git SHA — content fidelity is required); **ASSUMPTION** — extended to instruction bundling by analogy with the approval integrity principle. See Guidance section "Rationale: K-AUTH-2 Analogy for Instruction Bundling" for the reasoning behind this analogy.

> **Enrichment note (F-001):** Added cross-reference to the rationale in Guidance that explains why K-AUTH-2 (approval integrity) is extended by analogy to instruction bundling.

### REQ-05: Working Root Independence

The system MUST function correctly when the working root is located at any user-chosen filesystem path. The working root MUST NOT depend on being co-located with the instruction root or the app installation directory.

**Source:** DIRECTIVE Section 2.6; SOW-003 ("select a local Working Root and run Chirality against that folder").

### REQ-06: No External State Dependencies

The instruction root bundling mechanism MUST NOT introduce dependencies on external databases, servers, or network connectivity for instruction access. Instruction content must be locally available in the app bundle.

**Source:** DIRECTIVE Section 5 (Structural Constraints: "No external database dependency", "No server requirement").

### REQ-07: Graceful Degradation on Missing or Corrupted Instruction Content

The runtime SHOULD detect and report errors when instruction root files are missing, inaccessible, or corrupted at runtime. The system SHOULD provide a clear error message identifying which instruction files are affected rather than failing silently or with an opaque error.

**Source:** **ASSUMPTION** — no governance source explicitly addresses runtime behavior when instruction root content is absent or damaged. This requirement is inferred as a foundational resilience prerequisite. Exact degradation behavior (e.g., whether the app refuses to start, shows a diagnostic, or operates in a reduced mode) is TBD.

> **Enrichment note (C-002):** Added REQ-07 to address the gap identified by semantic lensing: no prior requirement covered runtime behavior when instruction root files are missing or corrupted. Labeled ASSUMPTION because no existing governance source mandates specific graceful-degradation behavior for this scenario.

---

## Standards

| Standard / Invariant | Applicability | Source |
|----------------------|---------------|--------|
| K-GHOST-1 — No ghost inputs | Type 2 agent context is limited to folder contents + declared references; instruction root provides the declared instruction set | CONTRACT K-GHOST-1 |
| K-WRITE-1 — Explicit write scope | Agents have declared write scopes; instruction root is never a write target | CONTRACT K-WRITE-1 |
| K-SNAP-1 — Immutable snapshots | Tool root outputs are immutable; instruction root is analogously immutable (release-managed) | CONTRACT K-SNAP-1 |
| DIRECTIVE Section 2.6 | Separation of Instruction and Execution | DIRECTIVE |
| SPEC Section 1 — Execution Root Layout | Defines the canonical execution root structure that agents operate against within the working root | SPEC |

---

## Verification

| Req ID | Verification Approach | Expected Result |
|--------|----------------------|-----------------|
| REQ-01 | Build a packaged app and verify instruction files are present in the app bundle resources | All instruction root files (`AGENTS.md`, `README.md`, `agents/*`, `docs/DIRECTIVE.md`, `docs/CONTRACT.md`, `docs/SPEC.md`, `docs/TYPES.md`, `docs/PLAN.md`) are present and readable |
| REQ-02 | During a runtime session, attempt to write a file to the instruction root path (e.g., create a temp file via agent code); verify the write is rejected or prevented | Write attempt fails with an identifiable error or is blocked by the enforcement mechanism; working root writes succeed normally |
| REQ-03 | Test instruction path resolution in both dev mode and packaged mode | Instruction files resolve correctly in both environments; paths are deterministic and stable |
| REQ-04 | Compare SHA-256 hashes of bundled instruction files against source repository versions at the build commit using automated packaging-gate verification (`npm run instruction-root:integrity`) | All hashes match; no content modification during bundling |
| REQ-05 | Run the app with working roots at different filesystem locations: (a) home directory, (b) path with spaces, (c) external volume, (d) read-only volume (**ASSUMPTION** — edge case), (e) network mount (**ASSUMPTION** — edge case), (f) path with unicode characters (**ASSUMPTION** — edge case) | Session boots and agents execute correctly in all standard cases (a-c); edge cases (d-f) produce clear errors or succeed gracefully |
| REQ-06 | Run the app in airplane mode (no network) and verify instruction access | All instruction files are accessible; no network errors related to instruction loading |
| REQ-07 | Delete or corrupt one or more instruction root files and launch the app | App detects the issue and reports a clear, actionable error message identifying affected files (**ASSUMPTION** — exact expected behavior TBD) |

> **Enrichment note (A-003):** REQ-02 verification now specifies the concrete test action (attempt a write) and the expected failure behavior (identifiable error or blocked), rather than the generic "verify agents cannot write."

> **Enrichment note (C-001):** REQ-04 verification path is now automated as a packaging-gate step (`instruction-root:integrity`) producing hash manifest/summary artifacts.

> **Enrichment note (X-002):** REQ-05 verification expanded with additional edge cases (read-only volume, network mount, unicode path characters), each marked ASSUMPTION since no source evidence mandates these specific scenarios.

---

## Acceptance Criteria

The following criteria define "done" for DEL-05-01 as a whole. All must be satisfied for the deliverable to be considered complete:

1. **All six core requirements (REQ-01 through REQ-06) pass verification** as described in the Verification table above.
2. **REQ-07 (graceful degradation) verification** produces acceptable results (exact acceptance threshold is TBD pending human ruling on degradation behavior).
3. **All three anticipated artifact types are produced:**
   - CODE: Build configuration and runtime path resolution utility exist and are committed.
   - DOC: Developer documentation for instruction bundling mechanism and path resolution API exists.
   - TEST: Test suite covering verification approaches for REQ-01 through REQ-07 exists and passes.
4. **Content integrity confirmed:** SHA-256 hash comparison between source and bundled instruction files shows no discrepancies at the build commit.
5. **Cross-deliverable interface validated:** Working root binding (DEL-03-01) functions correctly with the instruction root mechanism (tested via end-to-end verification in Procedure Step 7).

**Source:** Derived from Specification requirements and verification table; Decomposition anticipated artifacts (CODE/DOC/TEST). **ASSUMPTION** — these criteria synthesize existing requirements into an explicit acceptance checklist; the human may add, refine, or override.

> **Enrichment note (F-002):** Added explicit acceptance criteria section so that "done" for DEL-05-01 is stated as a testable checklist rather than being implicit in the verification table alone.

---

## Documentation

### Required Artifacts (from Anticipated Artifacts: CODE / DOC / TEST)

| Artifact Type | Description | Status |
|---------------|-------------|--------|
| **CODE** | Build configuration and runtime code implementing instruction root bundling and path resolution | TBD |
| **DOC** | Developer documentation describing the instruction root bundling mechanism, path resolution API, and dev vs packaged mode differences | TBD |
| **TEST** | Test suite covering REQ-01 through REQ-07 verification approaches | TBD |

---

## TBD Register

Items requiring resolution before or during implementation:

| TBD ID | Description | Source | Impacted Requirements |
|--------|-------------|--------|-----------------------|
| TBD-S01 | REQ-02 enforcement mechanism (filesystem permissions, runtime guard, or API restriction) | A-002 | REQ-02 |
| TBD-S02 | REQ-04 build-time/CI automation for SHA-256 integrity comparison | C-001 | REQ-04 (**RESOLVED 2026-02-23**: implemented via `frontend/scripts/verify-instruction-root-integrity.mjs` and packaging-script gating) |
| TBD-S03 | REQ-07 exact graceful-degradation behavior (refuse to start, diagnostic mode, reduced mode) | C-002 | REQ-07 |
| TBD-S04 | Whether instruction root behavior during app update requires its own verification criteria (old instructions replaced, migration, backward compatibility) — may be out of scope for DEL-05-01 | X-003 | Verification scope |
| TBD-S05 | Whether performance requirements exist for instruction root access (latency, file read time) — if so, add as a requirement | D-002 | Potential new requirement |

> **Enrichment note (X-003, D-002):** TBD-S04 and TBD-S05 capture open questions raised by semantic lensing that cannot be resolved without human input or additional source evidence.
