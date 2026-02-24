# Guidance -- DEL-02-01 FileTree Refresh & External-Change Detection

---

## Purpose

This deliverable ensures operators always see an accurate representation of the project filesystem when using the Chirality desktop application. Because the system treats the filesystem as the database (DIRECTIVE SS 2.1), the FileTree is the operator's primary window into project state. External changes (made by editors, CLI tools, other agents, or the OS) must be reflected promptly without requiring the operator to manually trigger a refresh.

**Latency target for "promptly":** Changes should be reflected within one polling interval plus one debounce window of the triggering event. For focus/visibility-triggered refreshes, changes should appear within one debounce window (the refresh is immediate). Specific numeric values are TBD pending polling interval and debounce duration decisions (see C1 and C3). **ASSUMPTION:** This definition of "promptly" is inferred from the refresh mechanism design; governance sources do not specify a numeric latency target.

The FileTree refresh behavior directly supports OBJ-005 (Desktop UI supports intended operator workflow) -- confirmed via decomposition (SupportsObjectives column explicitly lists OBJ-005 for DEL-02-01).

**Source:** SOW-022 (Decomposition SSOW); PLAN SS 2; DIRECTIVE SS 2.1; Decomposition DEL-02-01 entry

---

## Terminology

To ensure consistent usage across all four production documents, the following terms are defined:

| Term | Definition | Usage |
|------|-----------|-------|
| **Refresh** | The act of updating the FileTree's displayed state to match the current filesystem. A refresh may be triggered by polling, focus/visibility events, or root changes. | Use when referring to the overall update action. |
| **Scan** | The filesystem read operation that traverses `projectRoot` and returns the current directory structure. A scan is the mechanism by which a refresh obtains new data. | Use when referring to the filesystem I/O operation itself. |
| **Poll** / **Polling** | A timer-triggered scan. Polling is one of two refresh triggers (the other being focus/visibility events). | Use when referring specifically to the periodic timer mechanism. |
| **Re-scan** | A subsequent scan after the initial scan. Equivalent to "scan" in the context of a refresh cycle. | Avoid where "scan" suffices; use only when emphasizing repetition. |

**Source:** Enrichment F-003 (terminology normalization)

---

## ASSUMPTION Marker Convention

All documents in this deliverable use a consistent format for marking assumptions:

- Format: **ASSUMPTION:** followed by the assumption text, as a standalone sentence or paragraph.
- Example: **ASSUMPTION:** This separation is consistent with the component architecture observed in UI_POLISH_EXECUTION_PLAN but has not been verified against the actual codebase.

This convention applies to Datasheet.md, Specification.md, Guidance.md, and Procedure.md.

**Source:** Enrichment E-002 (ASSUMPTION marker normalization)

---

## Principles

### P1: Filesystem Is the Source of Truth

The tree display MUST reflect the actual filesystem, not a cached or derived model. This aligns with DIRECTIVE SS 2.1 ("if the filesystem is the database, architecture is a state-and-authority specification") and CONTRACT K-GHOST-1 (no ghost inputs). Stale tree state would constitute a visual "ghost" -- showing files that no longer exist or hiding files that do.

**Source:** DIRECTIVE SS 2.1; CONTRACT K-GHOST-1

### P2: Responsiveness Without Resource Abuse

Polling frequency must balance two concerns:
- **Too slow:** Operator sees stale state, undermining trust in the filesystem-as-database model.
- **Too fast:** Unnecessary CPU and I/O load, especially on large project directories.

Focus/visibility refresh provides a good middle ground: aggressive refresh when the operator is actively looking, relaxed polling otherwise.

**Source:** PLAN SS 2 (describes the dual-trigger approach)

### P3: Graceful Degradation

The FileTree must handle edge cases without crashing:
- Very large directories (thousands of files).
- Deleted or inaccessible project roots (removable media, permission changes).
- Rapid context switches (multiple focus/blur cycles).

**ASSUMPTION:** Specific thresholds and fallback behaviors are TBD and should be determined during implementation based on performance profiling.

### P4: Minimal Coupling

The refresh mechanism should be independent of:
- The chat/harness session state (refresh works even when no session is active).
- The specific view mode (PORTAL, WORKBENCH, PIPELINE -- refresh runs whenever FileTree is rendered).
- File content rendering (FilePreview is a separate concern).

**ASSUMPTION:** This separation is consistent with the component architecture observed in UI_POLISH_EXECUTION_PLAN but has not been verified against the actual codebase.

---

## Considerations

### C1: Polling Interval Selection

| Interval | Responsiveness | Resource Cost | Notes |
|----------|---------------|---------------|-------|
| 1-2 seconds | High | Higher CPU/IO | Suitable for small-to-medium projects |
| 5-10 seconds | Moderate | Low | Common default for filesystem watchers |
| 30+ seconds | Low | Minimal | Too slow for active development |

**ASSUMPTION:** A default in the 5-10 second range is likely appropriate, but this should be validated against typical Chirality project directory sizes. Operator configurability may be desirable.

### C2: Polling vs. Native Filesystem Watchers

An alternative to polling is using native filesystem watchers (e.g., `fs.watch`, `chokidar`, or macOS FSEvents via Electron). The decomposition and PLAN explicitly describe "polling" as the mechanism, so this deliverable implements polling. Native watchers could be considered as a future enhancement.

**Source:** PLAN SS 2 explicitly states "Periodic polling" as the mechanism.

### C3: Visibility and Focus Event Sources

Multiple event sources exist:

| Event Source | When It Fires | Reliability |
|-------------|---------------|-------------|
| `document.visibilitychange` | Tab/window shown/hidden by OS | High (standard Web API) |
| `window.focus` / `window.blur` | Window gains/loses OS focus | High (standard Web API) |
| Electron `BrowserWindow.on('focus')` | Electron window focus event | High (Electron API) |

Using multiple sources provides defense-in-depth. A single refresh should be triggered regardless of how many events fire simultaneously (debounce required).

**Debounce strategy elaboration:** When multiple focus/visibility events fire in rapid succession (e.g., the operator switches away and back within milliseconds, or both `visibilitychange` and `BrowserWindow.focus` fire for the same OS event), the implementation should coalesce these into a single scan. Recommended approach:

- **Duration:** TBD (e.g., 300-500ms is a common range for UI debounce; Procedure Step 3.3 uses 500ms as an example).
- **Algorithm:** Trailing-edge debounce -- wait for the debounce window to elapse after the last event, then fire one scan. This prevents premature scanning if events continue to arrive.
- **Timer reset on polling:** After a debounced focus/visibility scan completes, reset the polling interval timer to avoid a redundant poll.

**ASSUMPTION:** The specific debounce duration should be validated during implementation. The 300-500ms range is a common UI convention, not derived from a governance source.

**Source:** PLAN SS 2; enrichment B-003

### C4: Tree State During Refresh

During a refresh cycle, the component should:
- **Not** clear and re-render the entire tree (causes visual flicker).
- **Prefer** a diff-and-update approach if technically feasible.
- **Preserve** the user's expand/collapse state across refreshes (see Specification REQ-08).

**ASSUMPTION:** This is a UX best practice but is not explicitly stated in governance sources.

### C5: Interaction with Shared Deliverables State

PLAN SS 2 describes "Shared deliverables state at page-level (`page.tsx`) used by both PORTAL and PIPELINE views." The FileTree refresh is a separate concern (filesystem tree display) but may need to signal when deliverable-relevant filesystem changes occur (e.g., new deliverable folders appearing). The boundary between FileTree refresh and shared deliverables state refresh should be clearly defined.

**Source:** PLAN SS 2; SOW-024 (shared state -- assigned to DEL-02-02)

### C6: Testing Across the Electron IPC Boundary

The FileTree scan mechanism operates across the Electron IPC boundary (renderer process requests filesystem data from the main process via IPC or preload bridge). Testing this requires a strategy for verifying behavior at the boundary:

- **Mock main process responses:** Unit tests can mock the IPC response to simulate filesystem state. This isolates the renderer-side refresh logic from the actual filesystem.
- **Use temp directories:** Integration tests can create temporary directory structures and verify that the scan returns accurate results through the actual IPC path.
- **Combine both approaches:** Mock-based tests for rapid feedback on refresh logic; temp-directory tests for end-to-end verification of the scan-through-IPC path.

**ASSUMPTION:** The specific testing approach depends on the existing IPC architecture discovered during Step 1 (audit). If the preload bridge exposes a clean API, mocking is straightforward. If filesystem access uses low-level IPC channels, a temp-directory approach may be more practical.

**Source:** Enrichment X-001

---

## Trade-offs

| Trade-off | Option A | Option B | Recommendation |
|-----------|----------|----------|----------------|
| Polling interval | Short (1-3s): faster detection | Long (10-30s): lower resource cost | TBD -- profile against representative directories |
| Refresh scope | Full tree re-scan | Incremental diff | Full re-scan is simpler and aligns with "polling" language in PLAN; incremental diff is a future optimization |
| Expand/collapse preservation | Preserve across refresh | Reset on refresh | Preserve -- better UX, standard practice (now REQ-08) |
| Error display | Inline error in tree area | Modal/toast notification | Inline error in tree area -- non-blocking, contextual |
| Debounce duration | Short (100-300ms): more responsive | Long (500-1000ms): fewer redundant scans | TBD -- 300-500ms is a reasonable starting point; validate during implementation |
| Hidden window polling | Continue at normal rate | Pause entirely | TBD -- pausing saves resources; continuing ensures freshness on restore; a reduced-rate compromise is also possible (see REQ-02a) |

---

## Examples

### Example: Polling Refresh Cycle

**ASSUMPTION:** This is an illustrative sequence, not derived from a specific source.

1. Operator selects `projectRoot` at `/Users/operator/my-project`.
2. FileTree performs initial scan immediately (REQ-01a) and renders tree.
3. Polling timer starts (interval = TBD seconds).
4. At each tick: scan filesystem, diff against current state, update changed nodes.
5. Operator switches to another application.
6. Polling continues, pauses, or slows per hidden-window policy (REQ-02a -- TBD).
7. Operator returns to Chirality window.
8. `visibilitychange` fires; immediate refresh triggered (debounced per C3); polling timer resets.
9. Tree reflects any changes made while Chirality was in the background.

### Example: Root Change

1. FileTree is displaying `/Users/operator/project-a`.
2. Operator selects new root `/Users/operator/project-b`.
3. FileTree clears current state, performs full scan of new root (REQ-01a), renders new tree.
4. Polling timer restarts for new root.

---

## Prerequisite Sequencing Rationale

The Procedure Prerequisites table lists "`projectRoot` binding" (DEL-03-01) as a prerequisite with status TBD. Clarification on the dependency:

- **Dependency edge-case:** If DEL-03-01 is ever reclassified as a strict prerequisite for future revisions, FileTree refresh changes would wait on root selection UI readiness.
- **Stub/mock sufficiency:** If a hardcoded or environment-variable-based `projectRoot` can stand in during development, DEL-02-01 can proceed in parallel with DEL-03-01.

**ASSUMPTION:** A stub/mock `projectRoot` is likely sufficient for initial development and testing, since the refresh mechanism is independent of how the root is selected. The dependency is on the *value* of `projectRoot`, not on the *UI* for selecting it. This should be confirmed by ORCHESTRATOR or the human.

**Source:** Procedure Prerequisites table; enrichment C-003

---

## Conflict Table (for human ruling)

*No conflicts identified between sources at this time. TBD items requiring human decisions are tracked in Specification requirements (REQ-01 polling interval, REQ-02a hidden window policy, REQ-03a symlink handling, REQ-07 error recovery, REQ-09 K-STATUS-1 scope).*
