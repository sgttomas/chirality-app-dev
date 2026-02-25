# Guidance — DEL-05-01 Instruction Root Bundling & Runtime Access

## Purpose

This deliverable exists to ensure that when the Chirality desktop app is built and distributed as a `.dmg`, the bundled application preserves the foundational separation between the **instruction root** (release-managed agent instructions and governance documents) and the **working root** (user-selected project filesystem).

This separation is a structural constraint of the Chirality architecture (DIRECTIVE Section 2.6; DIRECTIVE Section 5). Without it, the system cannot guarantee that agents operate from a stable, versioned instruction set while users maintain full control over their project data.

**Source:** Decomposition DEL-05-01 description; DIRECTIVE Section 2.6; OBJ-004 acceptance criteria.

---

## Principles

### P1: Instruction Root Is Release-Managed, Not Runtime-Managed

The instruction root content (`AGENTS.md`, `README.md`, `agents/*`, `docs/DIRECTIVE.md`, `docs/CONTRACT.md`, `docs/SPEC.md`, `docs/TYPES.md`, `docs/PLAN.md`) ships with the app and changes only when the app is updated. Agents must not modify instruction content at runtime. This ensures:

- Reproducibility: the same app version always operates from the same instruction set.
- Auditability: instruction content is traceable to a specific git SHA / release.
- Safety: agents cannot self-modify their own instructions.

**Source:** DIRECTIVE Section 2.6; CONTRACT K-AUTH-2 (approvals bind to specific git SHA).

### P2: Working Root Is User-Sovereign

The user selects the working root (`projectRoot`), and all project execution state lives there as plain files. The working root must not depend on app installation location, and the app must not store authoritative project state outside it.

**Source:** DIRECTIVE Section 2.1 (Filesystem Is the Database); DIRECTIVE Section 2.5 (No Hidden Memory); SOW-003.

### P3: Dev/Prod Parity for Instruction Access

The mechanism for accessing instruction root content should work transparently in both development (running from source repo) and production (running from `.dmg`-installed app) environments. Code should not need conditional paths scattered throughout the codebase.

**Source:** **ASSUMPTION** — standard engineering practice; reduces maintenance burden and test surface.

---

## Considerations

### C1: Electron Resource Bundling Patterns

Electron apps typically bundle static resources using one of these approaches:

1. **`extraResources`** — Copies files into the app bundle's `Resources/` directory. Files are accessible via `process.resourcesPath` in the main process.
2. **`extraFiles`** — Copies files into the app bundle root directory.
3. **ASAR archive** — Files packed into the `.asar` archive (default for `app/` contents).

For instruction root content that needs to be read as plain files (not `require`'d as modules), `extraResources` is the most common and appropriate pattern.

**Source:** **ASSUMPTION** — based on standard Electron packaging conventions. Actual mechanism should be confirmed against the existing build configuration.

### C2: Path Resolution Strategy

A centralized path resolution utility (e.g., `getInstructionRootPath()`) should abstract the difference between:

- **Dev mode:** instruction root is the repository root (or a specific subdirectory).
- **Packaged mode:** instruction root is within `process.resourcesPath` or equivalent.

The utility should be deterministic and testable. Environment detection (dev vs packaged) should rely on `app.isPackaged` or equivalent Electron API, not heuristics.

**Important:** The pseudocode example in the Examples section below is illustrative only and marked ASSUMPTION. Before relying on the assumed path structure in implementation, the actual Electron configuration (main process entry point, resource path layout) must be audited and the pseudocode pattern validated against the real build output. See Procedure Step 4 for the implementation step and associated verification.

**Source:** **ASSUMPTION** — standard practice for Electron apps with bundled resources.

> **Enrichment note (E-002):** Added explicit warning that the pseudocode path resolution example must be validated against real Electron configuration before implementation reliance, addressing the gap between an ASSUMPTION-labeled illustration and the Procedure step that references implementing this pattern.

### C3: Instruction Root Content Manifest

Consider whether the build process should generate a manifest of bundled instruction files (filenames + SHA-256 hashes) to support future integrity verification (see DEL-08-01 / SOW-032 for the optional content-hash hardening candidate).

This is not a requirement for DEL-05-01 but is a low-cost preparation step that would simplify later hardening.

**Source:** PLAN Section 3.1 (Content Hash Implementation); SOW-032 (TBD scope).

### C4: Read-Only Enforcement

In packaged mode, instruction root files may be naturally read-only (app bundle is code-signed or filesystem-protected). In dev mode, instruction files are writable (they are source repo files). Consider whether runtime enforcement (beyond filesystem permissions) is needed to prevent accidental writes to the instruction root in dev mode.

Possible enforcement mechanisms include:
- **Filesystem permissions:** Set instruction root files to read-only during dev mode setup (fragile; easily circumvented).
- **Runtime path guard:** The path resolution utility could refuse to return writable file handles for instruction root paths.
- **API-level restriction:** Agent APIs could reject write operations targeting paths within the resolved instruction root.

Baseline enforcement mechanism is now selected: API-level restriction via working-root validation. Session create/boot rejects `projectRoot` paths inside the instruction root (`WORKING_ROOT_CONFLICT`), and runtime writes remain scoped to the validated working root. Filesystem-level read-only behavior in packaged mode is treated as a secondary control.

**Source:** **ASSUMPTION** — pragmatic consideration; Specification REQ-02 requires separation enforcement.

> **Enrichment note (A-002):** C4 now documents the selected baseline enforcement mechanism (API-level runtime path guard) and retains alternatives as contextual background.

### C5: Graceful Degradation on Missing Instruction Content

If instruction root files are missing or corrupted at runtime (e.g., partial install, disk corruption, tampered bundle), the application should detect the condition and provide an actionable error rather than failing silently or producing opaque errors.

Considerations:
- **Startup validation:** Check for the presence of key instruction files (at minimum `AGENTS.md` and `docs/DIRECTIVE.md`) during app startup.
- **Error granularity:** Report which specific files are missing or invalid, not just "instructions unavailable."
- **Degradation vs. refusal:** Baseline behavior is fail-fast boot refusal with typed diagnostics (`INSTRUCTION_ROOT_INVALID`) when required instruction content is missing or invalid.

**Source:** **ASSUMPTION** — no governance source explicitly addresses this scenario. Added based on semantic lensing analysis (C-002) identifying this as a foundational resilience prerequisite.

> **Enrichment note (C-002):** Runtime error-handling posture is now explicit for baseline scope: fail-fast boot refusal with actionable diagnostics when instruction root validation fails.

### C6: Instruction Root Versioning Across App Updates

When a new version of the app is distributed, the instruction root content within the app bundle is replaced by the updated content. Considerations include:

- **No migration required for instruction root:** Since instruction content is immutable and release-managed (not user-modified), updating the app bundle inherently updates the instruction root. No user-side migration step is needed.
- **Working root compatibility:** A user's working root may have been created under a prior instruction root version. Whether backward compatibility or migration guidance is needed for working root content (e.g., `_STATUS.md` schemas, agent instruction references) is TBD and may be addressed by other deliverables (DEL-05-02, DEL-05-03).
- **No rollback mechanism:** If a user installs a new app version and the updated instructions are unsatisfactory, the only rollback path is reinstalling the prior app version. Whether this is acceptable or whether instruction root versioning should be more explicit is TBD.

**Source:** **ASSUMPTION** — no governance source addresses the instruction root update lifecycle. This consideration is forward-looking context for implementation decisions.

> **Enrichment note (X-001):** New consideration added to address the gap in stewardship for how instruction root content evolves across app updates, as distinct from the build-time bundling focus of the current requirements.

### C7: Performance Characteristics of Instruction Root Access

TBD: It is currently unknown whether there are performance requirements for instruction root access (e.g., maximum latency for path resolution, file read time, impact on agent boot time or user experience).

If instruction root access occurs on the critical path of session boot or turn execution, performance characteristics may need to be specified. If access is infrequent (e.g., only during initial agent loading), performance is unlikely to be a concern.

**Source:** **ASSUMPTION** — no governance source addresses performance characteristics for instruction file access. This TBD is recorded for human evaluation during implementation.

> **Enrichment note (D-002):** New TBD consideration added to capture the open question about whether instruction access performance matters for the user experience or agent boot time.

### C8: Error Recovery and Rollback Guidance

If a procedure step fails during implementation (e.g., build configuration does not correctly bundle files, path resolution returns incorrect paths, or verification tests fail), the following recovery approaches are recommended:

- **Step 3 failure (bundling configuration):** Revert build configuration changes and re-audit the existing setup (Step 1). Investigate whether the chosen bundling mechanism (e.g., `extraResources`) conflicts with other build settings.
- **Step 4 failure (path resolution):** Verify the assumed path structure by inspecting the actual packaged app bundle contents. The pseudocode in Examples is illustrative only — the real Electron resource path may differ.
- **Step 5 failure (read-only enforcement):** If the chosen enforcement mechanism is impractical, reconsider alternatives listed in C4 and document the trade-off decision.
- **Step 7 failure (end-to-end verification):** Isolate the failing verification criterion and trace back to the responsible step. Do not proceed to status update until root cause is identified.

**Source:** **ASSUMPTION** — no governance source prescribes specific recovery procedures. This guidance is inferred from the procedure steps and common engineering practice.

> **Enrichment note (D-001):** New consideration added to provide recovery/rollback direction when procedure steps fail, addressing the gap that the forward-path procedure had no guidance on what to do when verification fails.

---

## Trade-offs

| Trade-off | Option A | Option B | Recommendation |
|-----------|----------|----------|----------------|
| **Bundling mechanism** | `extraResources` (explicit file copy to Resources/) | ASAR-packed (inside app archive) | **ASSUMPTION** — `extraResources` is more transparent for plain-file reads; but ASAR may be acceptable if the runtime uses `fs` wrappers. Decision should be informed by existing build config. |
| **Path abstraction layer** | Single utility function | Config-driven (paths in environment/config file) | Single utility function is simpler and more testable; config-driven adds flexibility but also complexity. **ASSUMPTION** — prefer simplicity unless there is a demonstrated need. |
| **Dev mode instruction source** | Repo root | Symlink / copy to a staging directory | Repo root is simpler and avoids sync issues. **ASSUMPTION** — use repo root directly in dev mode. |

---

## Rationale: K-AUTH-2 Analogy for Instruction Bundling

Specification REQ-04 extends CONTRACT K-AUTH-2 (approval integrity: approvals bind to a specific git SHA) to instruction bundling by analogy. The reasoning for why this analogy holds:

1. **K-AUTH-2's core principle** is that approved content is identified by its git SHA, and any process that uses approved content must ensure it is operating on the exact content that was approved — not a modified copy.
2. **Instruction root content is governance-controlled:** The governance documents (`docs/DIRECTIVE.md`, `docs/CONTRACT.md`, etc.) and agent instructions (`agents/*`) are the normative artifacts that define how the system operates. Their content fidelity is at least as important as the content fidelity of deliverable approvals.
3. **The build process is the trust boundary:** When instruction content is copied from the source repository into the app bundle, the build process is the mechanism that must preserve fidelity. If the build process modified, filtered, or transformed instruction content, the running app would operate from an unreviewed instruction set — violating the spirit of K-AUTH-2 even if the letter applies only to deliverable approvals.
4. **The analogy is conservative:** REQ-04 does not claim that K-AUTH-2 *literally* governs build bundling. It applies the same principle (content fidelity at process boundaries) to a context where the rationale is equally compelling.

**Source:** CONTRACT K-AUTH-2; DIRECTIVE Section 2.6. **ASSUMPTION** — this rationale is the agent's articulation of why the analogy holds; the human may refine or override.

> **Enrichment note (F-001):** New rationale section added to explicitly warrant the K-AUTH-2 analogy used in REQ-04, rather than leaving it as an unexplained ASSUMPTION tag.

---

## Examples

### Example: Instruction Root Path Resolution (Pseudocode)

```
function getInstructionRootPath():
  if app.isPackaged:
    return path.join(process.resourcesPath, 'instructions')
  else:
    return path.join(app.getAppPath(), '..', '..')  // or repo root
```

**Note:** This is illustrative pseudocode. The actual implementation should be informed by the existing Electron main process configuration and build tooling. **This pattern must be validated against the real packaged app bundle structure before it is used as a basis for implementation** (see C2 and Procedure Step 4).

**Source:** **ASSUMPTION** — illustrative only; not derived from source evidence.

---

## Conflict Table (for human ruling)

No unresolved conflicts identified at this time. If conflicts arise during implementation (e.g., between existing build configuration and the bundling approach recommended here), they should be added to this table.

| Conflict ID | Conflict | Source A | Source B | Impacted Sections | Proposed Authority | Human Ruling |
|-------------|----------|----------|----------|--------------------|--------------------|--------------|
| *(none)* | | | | | | |
