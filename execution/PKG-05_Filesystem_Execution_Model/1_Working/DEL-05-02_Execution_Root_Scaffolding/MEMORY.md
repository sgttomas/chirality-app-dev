# Working Memory — DEL-05-02

*This file is shared working memory for WORKING_ITEMS and TASK agents operating on this deliverable.*

## Key Decisions & Human Rulings

- Implementation lives in this repo `/Users/ryan/ai-env/projects/chirality-app-dev/` — this deliverable specifies and tracks; code changes apply there.

## Domain Context

### Local Repository Audit (2026-02-22)

**Current state: 0% implemented.** No execution root scaffolding code exists anywhere in the this repo. The only directory creation is:
- `.chirality/sessions/` created by `session-manager.ts` on session save
- `.chirality/prompts/` created by `persona-manager.ts` for system prompt files
- `.chirality/` log directory created by `logger.ts`

None of these create PKG-/DEL- folder trees, tool roots, or parse decomposition documents.

**Related assets:**
- `init/INIT.md` — template markdown file bundled via `extraResources`, contains placeholder fields. This is content, not code.
- `projectRoot` concept exists in the UI as a user-selected working directory.

### Implementation approach (from Procedure.md):

1. **Integration point**: Could be an API endpoint (e.g., `POST /api/harness/scaffold`), a utility module, or a standalone script. The API endpoint approach is most consistent with the existing Next.js harness architecture (session creation, turn handling, etc. all use API routes).

2. **Core modules needed:**
   - `Sanitize(name)` — per SPEC Section 10.1 (3-step: replace illegal chars, collapse whitespace, trim)
   - Decomposition parser — read decomposition markdown, extract PKG/DEL IDs and names
   - Folder creator — idempotent directory tree creation
   - `INIT.md` writer — from template
   - `_COORDINATION.md` writer — from template
   - Layout conformance checker — per SPEC Section 12

3. **Key design decisions (TBD):**
   - Where does the scaffolding module live? (`lib/harness/scaffold.ts` is the natural home)
   - API endpoint or utility-only? (API endpoint preferred for UI integration)
   - How is the decomposition document parsed? (markdown parsing: extract tables + headings)

### Files in this repo to modify/create:

| File | Action | Purpose |
|------|--------|---------|
| `frontend/lib/harness/scaffold.ts` | CREATE | Core scaffolding module |
| `frontend/lib/harness/sanitize.ts` | CREATE | `Sanitize(name)` per SPEC 10.1 |
| `frontend/app/api/harness/scaffold/route.ts` | CREATE | API endpoint (optional) |
| `frontend/lib/harness/__tests__/scaffold.test.ts` | CREATE | Conformance tests |
| `frontend/lib/harness/__tests__/sanitize.test.ts` | CREATE | Sanitize edge cases |

## Open Items

- **TBD**: Integration point decision (API endpoint vs utility module vs standalone script).
- **TBD-A-001**: `INIT.md` content schema (minimum: date, decomposition reference, project name).
- **TBD-F-002**: `_Sources/` sub-structure.
- **CON-04**: Package optional subfolders SHOULD vs MUST (SPEC Section 1.1 is authoritative — treat as MUST until ruled otherwise).
- **CON-05**: Idempotency SHOULD vs MUST.
- **TBD**: Error handling strategy (atomic rollback, best-effort with report, or fail-fast).

## Proposal History

*No proposals applied yet. Gap analysis complete.*

## Interface & Dependency Notes

- DEL-05-01 (Instruction Root Bundling) is independent — no blocker dependency.
- Scaffolded output must be consumable by PREPARATION agent (which populates metadata files).
- Layout conformance checks (this deliverable's REQ-09) are distinct from DEL-08-03's standalone CLI validator.
- Example execution root created for DEL-07-02 can serve as a reference implementation / test fixture.
