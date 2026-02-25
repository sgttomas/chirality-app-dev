# Datasheet -- DEL-02-01 FileTree Refresh & External-Change Detection

---

## Identification

| Field | Value |
|-------|-------|
| **DeliverableID** | DEL-02-01 |
| **Name** | FileTree Refresh & External-Change Detection |
| **PackageID** | PKG-02 |
| **Package** | Desktop UI Workflow |
| **Type** | UX_UI_SLICE |
| **ContextEnvelope** | M |
| **Responsible Party** | TBD |
| **Scope Coverage** | SOW-022 |
| **Objective Association** | OBJ-005 -- confirmed via decomposition (SupportsObjectives column explicitly lists OBJ-005 for DEL-02-01) |
| **Anticipated Artifacts** | CODE / TEST / DOC |

## Issuance Hygiene (2026-02-24)

- Lifecycle state is `ISSUED`.
- REQ-09/REQ-10 interpretation items remain as spec/governance follow-up and are non-blocking for issued status.
- Legacy implementation-phase `TBD` wording is non-blocking unless explicitly reclassified by human ruling.

---

## Attributes

| Attribute | Value | Source |
|-----------|-------|--------|
| **Primary Component** | `frontend/components/FileTree.tsx` | PLAN SS 2 ("Live project-directory refresh in FileTree") |
| **Related Components** | `frontend/components/SystemFileTree.tsx`, `frontend/components/FilePreview.tsx` | UI_POLISH_EXECUTION_PLAN SS F |
| **Runtime Environment** | Electron + Next.js desktop application (macOS 15+, Apple Silicon) | Decomposition DEC-PLAT-001 |
| **Refresh Triggers** | Periodic polling; focus/visibility change events | PLAN SS 2 ("Periodic polling plus focus/visibility refresh") |
| **Refresh Scope** | Project directory (`projectRoot`) selected by operator | PLAN SS 2; DIRECTIVE SS 2.1 |
| **Polling Interval** | TBD (implementation detail; must balance responsiveness vs resource cost; see Guidance C1 for trade-off analysis) | -- |
| **Polling Interval Default** | TBD -- to be determined via implementation profiling against representative Chirality project directories. Cross-reference: Specification REQ-01, Guidance C1, Procedure Step 2.1. | -- |
| **Debounce Strategy** | TBD (implementation detail; see Guidance C3 and B-003 enrichment for considerations on duration and algorithm) | -- |
| **Tree Depth Limit** | TBD (if any limit is imposed on recursion depth for performance; threshold values require implementation profiling) | -- |
| **IPC Channel / Preload API** | TBD -- specific IPC channel name(s) or preload bridge API surface to be determined during implementation discovery (Step 1 audit of existing codebase) | **ASSUMPTION:** standard Electron architecture for filesystem access |
| **Symlink/Alias Handling** | TBD -- policy for symbolic links and macOS aliases during filesystem scan (see Specification REQ-03a) | Decomposition DEC-PLAT-001 (macOS target) |

---

## Conditions

| Condition | Description | Source |
|-----------|-------------|--------|
| **Working Root Binding** | FileTree operates against the currently selected `projectRoot` (Working Root); the tree updates when root changes | DIRECTIVE SS 2.1; PLAN SS 2 |
| **External Change Detection** | Must detect changes made by external processes (editors, agents, CLI) to the filesystem under `projectRoot` | SOW-022 (Decomposition); PLAN SS 2 |
| **Desktop Platform** | macOS 15+ Apple Silicon only | Decomposition DEC-PLAT-001 |
| **No Outbound Network** | FileTree refresh is local filesystem only; no network calls | DIRECTIVE SS 5 ("No external database dependency", "No server requirement"); DEC-NET-001 (Anthropic-only outbound) |
| **Electron Context** | Component runs in Electron renderer process with access to Node.js filesystem APIs via IPC or preload | **ASSUMPTION:** standard Electron architecture for filesystem access |
| **Electron Security Posture** | Filesystem access via preload bridge must respect Electron security best practices (contextIsolation enabled, no nodeIntegration in renderer) | **ASSUMPTION:** standard Electron security model; see Specification Standards and X-004 enrichment |

---

## Construction

| Aspect | Description | Source |
|--------|-------------|--------|
| **Framework** | React component within Next.js + Electron desktop app | PLAN SS 2 |
| **State Management** | TBD (local component state, page-level state, or shared state) | -- |
| **Filesystem Access** | Node.js `fs` APIs accessed via Electron main process IPC (or preload bridge); specific channel/API names TBD pending implementation discovery | **ASSUMPTION:** standard Electron pattern |
| **Visibility API** | Browser `document.visibilitychange` event and/or Electron `BrowserWindow` focus events | **ASSUMPTION:** standard browser/Electron visibility detection |
| **Focus API** | Browser `window.focus` event and/or Electron `BrowserWindow.on('focus')` | **ASSUMPTION:** standard browser/Electron focus detection |
| **Tree Rendering** | Hierarchical folder/file display with expand/collapse | UI_POLISH_EXECUTION_PLAN SS F ("tree readability and row interaction states") |

---

## References

| RefID | Reference | Relevance |
|-------|-----------|-----------|
| REF-01 | PLAN SS 2 | Describes FileTree refresh behavior (polling + focus/visibility) |
| REF-02 | DIRECTIVE SS 2.1, SS 2.6 | Filesystem-as-state principle; instruction/working root separation |
| REF-03 | SPEC SS 1 | Execution root layout that FileTree must display |
| REF-04 | UI_POLISH_EXECUTION_PLAN SS F | FileTree polish requirements and component list |
| REF-05 | Decomposition DEL-02-01 entry | Deliverable definition and scope assignment |
| REF-06 | CONTRACT K-GHOST-1 | No ghost inputs; tree displays actual filesystem state |
| REF-07 | SOW-022 (Decomposition SSOW) | "Provide a live project directory FileTree that refreshes periodically and on focus/visibility changes to detect external filesystem changes" |
| REF-08 | CONTRACT K-STATUS-1 | FileTree may display status indicators for deliverable folders (scope applicability TBD; see Specification REQ-09) |
| REF-09 | Decomposition DEC-PLAT-001 | macOS 15+ Apple Silicon target platform |
