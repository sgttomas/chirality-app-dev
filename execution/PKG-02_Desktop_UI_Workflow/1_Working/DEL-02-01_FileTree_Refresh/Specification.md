# Specification -- DEL-02-01 FileTree Refresh & External-Change Detection

---

## Scope

### Included

This deliverable covers the implementation and verification of the FileTree component's refresh behavior within the Chirality desktop application, specifically:

1. **Periodic polling** of the project directory to detect filesystem changes.
2. **Focus/visibility-triggered refresh** to detect external changes when the application regains attention.
3. **Correct tree state update** so that the displayed file hierarchy reflects actual filesystem contents after refresh.

Source: SOW-022 -- "Provide a live project directory FileTree that refreshes periodically and on focus/visibility changes to detect external filesystem changes." (Decomposition SSOW)

### Excluded

- FileTree visual styling and interaction polish (covered by DEL-02-04 and UI_POLISH_EXECUTION_PLAN workstream F).
- File content preview (covered by `FilePreview.tsx` in a separate concern).
- Working root binding and selection UI (covered by DEL-03-01 and `ResizableLayout.tsx` root selector).
- Filesystem write operations by agents (FileTree is read-only display).

---

## Requirements

### REQ-01: Periodic Polling Refresh

The FileTree component MUST periodically poll the filesystem under the active `projectRoot` to update its displayed hierarchy.

- The polling interval MUST be configurable or set to a reasonable default. **Value: TBD** (see Guidance C1 for trade-off analysis; to be determined via implementation profiling).
- Polling MUST NOT block the UI thread.
- Polling MUST NOT trigger when no `projectRoot` is selected (empty/null root).

**Source:** PLAN SS 2 ("Periodic polling plus focus/visibility refresh to pick up external filesystem changes")

### REQ-01a: Initial Scan Timing

When a `projectRoot` is set or changed, the FileTree MUST perform an initial filesystem scan immediately (without waiting for the first polling interval to elapse). The polling timer MUST begin after the initial scan completes.

**ASSUMPTION:** This requirement is inferred from the combined intent of REQ-01 (periodic polling) and REQ-04 (root binding behavior). The decomposition and PLAN do not explicitly specify initial scan timing, but immediate scan on root selection is the expected UX behavior.

**Source:** REQ-01 + REQ-04 (inferred); PLAN SS 2

### REQ-02: Focus/Visibility Refresh

The FileTree component MUST trigger a refresh when the application window regains focus or becomes visible after being hidden.

- MUST listen for browser `visibilitychange` events (document becomes visible).
- SHOULD listen for Electron `BrowserWindow` focus events (window gains OS-level focus). **Rationale for SHOULD:** The browser-level `visibilitychange` API is the primary mechanism and is reliable in Electron's renderer process. The Electron-specific `BrowserWindow` focus event provides defense-in-depth but may not be available in all Electron configurations (e.g., if the renderer does not have access to the `BrowserWindow` API via preload). The SHOULD level allows implementers to omit it if integration is not straightforward, while the MUST on `visibilitychange` ensures the core behavior is always present. See Guidance C3 for further analysis.
- A refresh triggered by focus/visibility SHOULD reset the polling timer to avoid a redundant immediate poll.

**Source:** PLAN SS 2 ("focus/visibility refresh"); SOW-022

### REQ-02a: Hidden Window Polling Policy

TBD -- define whether polling continues at the normal interval, pauses entirely, or reduces to a slower interval when the application window is hidden or minimized.

**ASSUMPTION:** This is a gap identified via Guidance Examples (line 122: "pauses -- TBD policy for hidden windows") and enrichment item C-002. The policy affects resource consumption when the application is not visible. A decision is needed before implementation.

**Source:** Guidance.md Examples section; enrichment C-002

### REQ-03: External Change Detection

After any refresh (periodic or focus-triggered), the displayed tree MUST reflect the current state of the filesystem, including:

- New files and folders created by external processes.
- Deleted files and folders removed by external processes.
- Renamed files and folders.
- Changes to directory structure (new subdirectories, moved items).

**Source:** SOW-022 ("detect external filesystem changes"); DIRECTIVE SS 2.1 ("Filesystem is the database")

### REQ-03a: Symlink and Alias Handling

TBD -- define the behavior when the filesystem scan encounters symbolic links or macOS aliases under `projectRoot`. Options include:

- Follow symlinks and display target contents (risk: infinite loops with circular symlinks).
- Display symlinks as leaf nodes with a visual indicator (no traversal).
- Exclude symlinks from the tree entirely.

**ASSUMPTION:** On macOS (the target platform per DEC-PLAT-001), symlinks are common in Node.js projects (e.g., `node_modules/.package-name`). A policy is needed. This does not affect the core refresh mechanism but affects scan completeness and correctness of the "displayed tree matches filesystem" criterion.

**Source:** Decomposition DEC-PLAT-001 (macOS target); enrichment F-004

### REQ-04: Working Root Binding

The FileTree MUST display the directory tree rooted at the currently selected `projectRoot` (Working Root).

- When `projectRoot` changes, the FileTree MUST re-scan from the new root.
- When `projectRoot` is null/empty, the FileTree MUST display an appropriate empty state.

**Source:** DIRECTIVE SS 2.6 (instruction root vs working root separation); PLAN SS 2

### REQ-05: No Network Dependency

The FileTree refresh mechanism MUST operate entirely via local filesystem access. No network calls are permitted for tree refresh operations.

**Source:** DEC-NET-001 (Anthropic-only outbound); DIRECTIVE SS 5 ("No external database dependency", "No server requirement")

### REQ-06: Performance and Resource Safety

- Polling MUST NOT cause perceptible UI lag during normal operation.
- The component SHOULD implement debounce or throttle logic to prevent rapid successive refreshes (e.g., multiple focus/visibility events in quick succession). See Guidance C3 and the debounce strategy elaboration for duration and algorithm considerations.
- **ASSUMPTION:** A tree depth or node-count limit MAY be needed for very large project directories. Threshold values are TBD (require implementation profiling).

### REQ-07: Graceful Error Handling

- If the `projectRoot` path becomes inaccessible (deleted, permissions changed, unmounted volume), the FileTree MUST display an error state rather than crashing.
- **TBD:** Error recovery behavior -- auto-retry, manual retry, root-reset prompt, or a combination. This is a human design decision. (See enrichment C-001.)

### REQ-08: Expand/Collapse State Preservation

The FileTree MUST preserve the user's expand/collapse state across refresh cycles. A refresh (whether periodic or focus-triggered) MUST NOT reset the tree's expand/collapse state.

**ASSUMPTION:** This is a UX best practice not explicitly stated in governance sources, but is referenced in Guidance C4 and Procedure Step 2.3 as expected behavior. Elevating to a requirement ensures verification coverage.

**Source:** Guidance C4; Procedure Step 2.3; enrichment A-003

### REQ-09: K-STATUS-1 Deliverable Status Display (Scope TBD)

TBD -- determine whether the FileTree should display lifecycle status indicators for deliverable folders (as suggested by CONTRACT K-STATUS-1: "FileTree may display status indicators for deliverable folders"). If in scope for DEL-02-01, define the display behavior. If out of scope, explicitly exclude.

**ASSUMPTION:** K-STATUS-1 is listed in the Standards table but no requirement addresses it. This is a human scope decision.

**Source:** CONTRACT K-STATUS-1; Specification Standards table; enrichment D-001

### REQ-10: Electron Security Posture

Filesystem access via the preload bridge MUST respect Electron security best practices:

- `contextIsolation` MUST be enabled.
- `nodeIntegration` MUST NOT be enabled in the renderer process.
- Filesystem APIs MUST be exposed only through a controlled preload script.

**ASSUMPTION:** This is standard Electron security practice. The Datasheet Construction section assumes "standard Electron architecture for filesystem access" but no explicit verification exists for the security posture of the IPC/preload bridge used by FileTree.

**Source:** Electron documentation (**location TBD**); enrichment X-004

---

## Standards

| Standard / Governance | Applicability | Location |
|----------------------|---------------|----------|
| SPEC SS 1 (Execution Root Layout) | FileTree displays this structure | Accessible |
| DIRECTIVE SS 2.1 (Filesystem Is the Database) | Foundational principle for tree display | Accessible |
| CONTRACT K-GHOST-1 (No Ghost Inputs) | Tree shows actual filesystem state, not cached/stale state | Accessible |
| CONTRACT K-STATUS-1 (Lifecycle via _STATUS.md) | FileTree may display status indicators for deliverable folders (scope applicability TBD; see REQ-09) | Accessible |
| SOW-022 (Decomposition SSOW) | Scope definition | Accessible |
| Electron documentation (BrowserWindow focus events, preload bridge, contextIsolation) | Implementation and security reference | **location TBD** |
| Web Visibility API (MDN) | `document.visibilitychange` specification | **location TBD** |

---

## Verification

| ReqID | Verification Approach | Acceptance Criteria |
|-------|----------------------|---------------------|
| REQ-01 | Automated test: mock filesystem changes during polling interval; assert tree updates | Tree reflects new/deleted/renamed items after one polling cycle |
| REQ-01a | Automated test: set projectRoot; assert scan fires immediately without waiting for interval | Initial scan completes before first polling interval elapses |
| REQ-02 | Manual + automated test: simulate `visibilitychange` and focus events; assert refresh fires | Tree refreshes on visibility/focus restore |
| REQ-02a | Automated test: hide window; measure polling behavior; assert policy compliance | Polling pauses/slows/continues per defined policy (TBD) |
| REQ-03 | Integration test: create/delete/rename files externally; trigger refresh; assert tree accuracy | Displayed tree matches filesystem state of projectRoot within one refresh cycle; scope of comparison (hidden files, metadata) TBD per REQ-03 acceptance criterion tightening |
| REQ-03a | Test: create symlink under projectRoot; trigger refresh; assert defined behavior | Symlinks handled per defined policy (TBD) |
| REQ-04 | Unit test: change projectRoot; assert tree re-scans from new root; null root shows empty state | Correct root binding behavior |
| REQ-05 | Code review: no network calls in refresh path | No `fetch`/`XMLHttpRequest`/WebSocket in refresh logic |
| REQ-06 | Performance test: measure UI responsiveness during polling on a representative project directory | No perceptible lag; debounce prevents rapid successive scans |
| REQ-07 | Test: remove/chmod projectRoot during operation; assert error state display | Error state displayed; no crash |
| REQ-08 | Automated test: expand nodes; trigger refresh with filesystem changes; assert expand/collapse state preserved | Expand/collapse state unchanged after refresh |
| REQ-09 | TBD (pending scope decision) | TBD |
| REQ-10 | Code review: verify contextIsolation enabled, nodeIntegration disabled, APIs exposed via controlled preload | Electron security posture confirmed |

---

## Documentation

### Required Artifacts (from Anticipated Artifacts: CODE/TEST/DOC)

| Artifact | Description | Status |
|----------|-------------|--------|
| Source code | FileTree component with refresh logic (`frontend/components/FileTree.tsx` or related) | TBD |
| Test suite | Unit and integration tests for refresh behavior | TBD |
| Documentation | Developer notes on refresh architecture, polling configuration, and event handling | TBD |
