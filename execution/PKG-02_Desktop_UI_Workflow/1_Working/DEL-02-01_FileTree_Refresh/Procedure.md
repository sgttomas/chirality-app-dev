# Procedure -- DEL-02-01 FileTree Refresh & External-Change Detection

---

## Purpose

This procedure describes the steps to implement, verify, and document the FileTree refresh and external-change detection behavior for the Chirality desktop application. It covers both producing the deliverable artifacts (CODE/TEST/DOC) and verifying that the implementation satisfies the requirements in `Specification.md`.

---

## Prerequisites

| Prerequisite | Description | Status | Notes |
|-------------|-------------|--------|-------|
| Working development environment | macOS 15+ Apple Silicon with Node.js, Electron, and Next.js toolchain installed and repo building | TBD | |
| `projectRoot` binding | Ability to select a Working Root in the application (DEL-03-01 or existing root selection in `ResizableLayout.tsx`). **ASSUMPTION:** A stub/mock `projectRoot` value (e.g., hardcoded path or environment variable) is sufficient for initial development; full DEL-03-01 UI is not a hard blocker. See Guidance "Prerequisite Sequencing Rationale." | TBD | If re-planning future implementation passes, confirm whether DEL-03-01 must be treated as a hard dependency; the issued baseline accepted stub sufficiency. |
| Access to `frontend/components/FileTree.tsx` | Existing FileTree component source code | TBD | |
| Access to governance documents | PLAN, DIRECTIVE, SPEC, CONTRACT | Available | |
| Decomposition reference | `execution/_Decomposition/ChiralityApp_SoftwareDecomposition_2026-02-21_G7-APPROVED.md` | Available | |

---

## Steps

### Step 1: Audit Existing FileTree Implementation

1.1. Read `frontend/components/FileTree.tsx` and identify current refresh behavior (if any).

1.2. Read `frontend/components/SystemFileTree.tsx` for any shared filesystem scanning logic.

1.3. Document the current state:
- Does polling exist? At what interval?
- Are focus/visibility listeners registered?
- How is the filesystem scanned (IPC to main process, direct `fs` calls, API endpoint)?
- What IPC channel name(s) or preload bridge API(s) are used for filesystem access?
- What tree state is maintained (expand/collapse, selection)?

1.4. Record findings in `MEMORY.md` under "Domain Context."

**Source:** UI_POLISH_EXECUTION_PLAN SS F (component list)

### Step 2: Implement Periodic Polling Refresh

2.1. Add a polling mechanism to the FileTree component:
- Use `setInterval` (or equivalent) to trigger filesystem scan at the configured interval.
- Ensure the interval is defined as a constant or configuration value (not hard-coded inline).
- Ensure the polling timer is cleaned up on component unmount.
- On root set/change, perform an initial scan immediately before starting the polling timer (REQ-01a).

2.2. Implement the filesystem scan:
- Scan the directory tree under `projectRoot` via the existing filesystem access path (Electron IPC or preload bridge).
- Parse results into the component's tree data structure.
- **ASSUMPTION:** The existing scan mechanism can be reused or extended.

2.3. Implement state update:
- Compare new scan results with current tree state.
- Update only changed nodes (or full replace if diff is not feasible in initial implementation).
- Preserve expand/collapse state across refresh cycles (REQ-08).

2.4. Guard against null/empty `projectRoot`:
- Do not start polling when no root is selected.
- Stop polling if root becomes null.

**Satisfies:** REQ-01, REQ-01a, REQ-04, REQ-08

### Step 3: Implement Focus/Visibility Refresh

3.1. Register event listeners for:
- `document.addEventListener('visibilitychange', ...)` -- trigger refresh when `document.visibilityState === 'visible'`.
- `window.addEventListener('focus', ...)` -- trigger refresh on window focus.
- **ASSUMPTION:** Electron-specific `BrowserWindow` focus events may also be useful but are secondary if browser-level events work reliably in Electron's renderer. See Specification REQ-02 rationale for SHOULD vs MUST.

3.2. On each focus/visibility trigger:
- Execute an immediate filesystem scan (same logic as polling tick).
- Reset the polling interval timer to avoid a redundant poll immediately after.

3.3. Implement debounce:
- If multiple focus/visibility events fire within a short window, coalesce into a single scan.
- Use trailing-edge debounce: wait for the debounce window to elapse after the last event, then fire one scan.
- Duration: TBD (e.g., 300-500ms; see Guidance C3 for debounce strategy elaboration). The value used here should be consistent with Specification REQ-06 and Guidance C3.

3.4. Implement hidden-window polling policy (REQ-02a):
- TBD -- pause, slow, or continue polling when window is hidden/minimized.

3.5. Clean up event listeners on component unmount.

**Satisfies:** REQ-02, REQ-02a, REQ-06

### Step 4: Implement Error Handling

4.1. Wrap filesystem scan calls in try/catch (or equivalent error boundary).

4.2. If the scan fails (root inaccessible, permissions denied, path not found):
- Display an inline error state in the FileTree area.
- Do not crash the application.
- **TBD:** Whether to auto-retry, offer manual retry, or prompt for root re-selection (see Specification REQ-07).

4.3. If `projectRoot` is deleted while polling is active:
- Stop polling.
- Display error state.

**Satisfies:** REQ-07

### Step 5: Verify No Network Dependency and Electron Security

5.1. Code review: confirm that the refresh path contains no `fetch`, `XMLHttpRequest`, `WebSocket`, or other network calls.

5.2. Confirm all filesystem access goes through local Node.js APIs (via Electron IPC/preload).

5.3. Verify Electron security posture (REQ-10):
- Confirm `contextIsolation` is enabled.
- Confirm `nodeIntegration` is NOT enabled in the renderer process.
- Confirm filesystem APIs are exposed only through a controlled preload script.

**Satisfies:** REQ-05, REQ-10

### Step 6: Write Tests

6.1. **Mocking/stubbing strategy:** Before writing tests, determine the mocking approach for filesystem operations:
- **Unit tests:** Mock IPC responses to simulate filesystem state without touching the actual filesystem. This isolates renderer-side refresh logic.
- **Integration tests:** Use temporary directory structures (via `fs.mkdtemp` or similar) to verify scan accuracy through the actual IPC path.
- **ASSUMPTION:** The specific approach depends on the IPC architecture discovered in Step 1. Document the chosen strategy in `MEMORY.md`.

**Source:** Enrichment X-002

6.2. **Unit tests** (for refresh logic):
- Test: polling starts when `projectRoot` is set; stops when null.
- Test: refresh fires on `visibilitychange` event simulation.
- Test: refresh fires on `focus` event simulation.
- Test: debounce prevents rapid successive refreshes.
- Test: expand/collapse state preserved across refresh (REQ-08).
- Test: initial scan fires immediately on root set, before first polling interval (REQ-01a).

6.3. **Integration tests** (for external change detection):
- Test: create a file externally; trigger refresh; assert file appears in tree.
- Test: delete a file externally; trigger refresh; assert file disappears from tree.
- Test: rename a file externally; trigger refresh; assert old name gone, new name present.
- Test: create a subdirectory externally; trigger refresh; assert directory appears.

6.4. **Error tests:**
- Test: remove `projectRoot` directory; trigger refresh; assert error state displayed.
- Test: change permissions on `projectRoot`; trigger refresh; assert error state displayed.

6.5. **Performance tests** (if feasible):
- Test: polling on a directory with TBD number of files completes within TBD milliseconds.
- **Note:** Threshold values require implementation profiling against representative Chirality project directories. Define values before writing these tests.

6.6. **Security verification tests** (if feasible):
- Test: confirm that filesystem access occurs only through the preload bridge API, not via direct `require('fs')` in the renderer.

**Satisfies:** Verification matrix in Specification.md

### Step 7: Write Developer Documentation

7.1. Document the refresh architecture:
- Polling mechanism and interval.
- Focus/visibility event handling.
- Filesystem access path (IPC channel names, preload API surface).
- Debounce strategy (algorithm and duration).

7.2. Document configuration points:
- How to change the polling interval.
- Any tree depth or node-count limits.
- Hidden-window polling policy.

7.3. Document error handling behavior and recovery paths.

7.4. Document symlink/alias handling policy (once determined).

**Satisfies:** Anticipated artifact DOC

### Step 8: Cross-Reference Verification

8.1. Verify all requirements in `Specification.md` have been addressed:

| ReqID | Addressed In | Verified By |
|-------|-------------|-------------|
| REQ-01 | Step 2 | Step 6 unit tests |
| REQ-01a | Step 2.1 | Step 6 unit tests |
| REQ-02 | Step 3 | Step 6 unit tests |
| REQ-02a | Step 3.4 | TBD (pending policy decision) |
| REQ-03 | Steps 2-3 | Step 6 integration tests |
| REQ-03a | TBD | TBD (pending policy decision) |
| REQ-04 | Step 2.4 | Step 6 unit tests |
| REQ-05 | Step 5 | Code review |
| REQ-06 | Steps 2-3 (debounce) | Step 6 unit/perf tests |
| REQ-07 | Step 4 | Step 6 error tests |
| REQ-08 | Step 2.3 | Step 6 unit tests |
| REQ-09 | TBD | TBD (pending scope decision) |
| REQ-10 | Step 5.3 | Code review + Step 6 security tests |

8.2. Verify consistency with `Datasheet.md` attributes (component names, technology choices, IPC channel names).

8.3. Verify consistency with `Guidance.md` principles, considerations, and terminology.

---

## Verification

| Check | Method | Pass Criteria | Repeatability |
|-------|--------|---------------|---------------|
| Periodic polling works | Run app; wait for polling interval; observe tree updates after external file creation | Tree shows new file within one polling cycle | Run 3 times with different file types; pass all 3 |
| Initial scan on root set | Set projectRoot; measure time to first tree render | Tree renders before first polling interval elapses | Run 3 times; pass all 3 |
| Focus refresh works | Switch away from app; create file externally; switch back; observe tree | Tree shows new file immediately on return | Run 3 times with 5+ second away periods; pass all 3 |
| Visibility refresh works | Minimize app; create file externally; restore app; observe tree | Tree shows new file on restore | Run 3 times; pass all 3 |
| Expand/collapse preserved | Expand several nodes; trigger refresh after external file creation; observe node states | All previously-expanded nodes remain expanded; new content visible | Run 3 times; pass all 3 |
| No root = no polling | Start app without selecting root; confirm no polling errors in console | No errors; empty state displayed | Run once |
| Root change re-scans | Select root A; observe tree; select root B; observe tree shows B's contents | Correct tree for each root | Run 2 times with different root pairs |
| Error on inaccessible root | Delete projectRoot while app is open; observe error state | Error state displayed; no crash | Run 2 times |
| No network calls | Review code; run with network disabled; confirm refresh works | Refresh operates normally offline | Run once with network disabled |
| Electron security posture | Code review of preload script and main process IPC | contextIsolation enabled; nodeIntegration disabled; APIs via preload only | Code review once |
| Tests pass | Run test suite | All unit/integration/error tests green | Run full suite; all green |

---

## Records

| Record | Description | Location |
|--------|-------------|----------|
| Source code changes | Modified/created files in `frontend/components/` | Git commit(s) |
| Test suite | Test files covering refresh behavior | Git commit(s) alongside source |
| Developer documentation | Architecture and configuration notes | TBD location (likely `frontend/docs/` or inline code comments) |
| Verification results | Test run output; manual verification notes | TBD (MEMORY.md or review record) |
| Status update | `_STATUS.md` updated to reflect completion | `execution/PKG-02_Desktop_UI_Workflow/1_Working/DEL-02-01_FileTree_Refresh/_STATUS.md` |
| IPC/preload audit findings | Discovered IPC channel names and preload API surface | MEMORY.md under "Domain Context" (Step 1.3) |
