# Guidance — DEL-03-07 Harness API Baseline in Frontend Runtime

## Purpose

This deliverable establishes the baseline harness API route surface inside the local `frontend/` workspace. It is the "FE-2" milestone in the phased frontend baseline plan (`docs/PLAN.md` Section 2) -- the second step after the workspace bootstrap (DEL-01-03, FE-1) and a prerequisite for the workflow UI shell (DEL-02-05, FE-3) and validation baseline (DEL-07-03, FE-4).

Without these routes, no harness functionality exists in the local runtime. The existing decomposition (G7-APPROVED) assumed `frontend/` was already available; Scope Amendment A1 (SCA-001) made this explicit by recognizing that the frontend workspace and its API surface must be implemented from this repository state.

This deliverable supports two objectives:

- **OBJ-002** (Harness runtime correctness): The session and turn API routes are the runtime surface through which the harness operates. Route correctness is a prerequisite for all harness behavior.
- **OBJ-008** (Local frontend runtime baseline): The routes must compile, pass contract tests, and be executable entirely from this repository's `frontend/` workspace.

**Source:** Decomposition SCA-001 DEL-03-07 entry; `docs/PLAN.md` Section 2 (FE-2); OBJ-002 acceptance criteria; OBJ-008 acceptance criteria.

---

## Principles

### P1: Routes Are the Contract Surface, Not the Implementation

The route handlers defined here are the HTTP contract surface for the harness runtime. They define what endpoints exist, what they accept, and what they return. The deep implementation logic (SDK integration, event mapping, attachment resolution, option fallback chains) is owned by the respective harness modules (AgentSdkManager, AgentSdkEventMapper, AttachmentResolver, PersonaManager) and covered by sibling deliverables (DEL-03-01 through DEL-03-06, DEL-04-01).

This deliverable ensures the routes exist, compile, delegate to modules, and return correctly typed responses including failure cases. It does not own the module internals.

**Source:** Decomposition package structure (PKG-03 deliverables DEL-03-01 through DEL-03-07 partition responsibility); SOW-045 ("implement baseline harness API routes").

### P2: Typed Failures Are First-Class

The scope statement (SOW-045) explicitly requires "typed failure contracts." This means error handling is not an afterthought -- every route must define its failure modes, error type identifiers, and status codes as part of the baseline contract. Callers (the UI, validation scripts, CI) must be able to programmatically distinguish between different failure types without parsing error message strings.

**Source:** SOW-045; DEL-03-01 Specification REQ-11 (established the error response pattern for session boot).

### P3: Local-Only Execution Is Non-Negotiable

All route code must live in `frontend/` within this repository. There must be no dependency on external clones, remote repositories, or files outside the checked-out workspace. This is enforced by both the local-only source policy (`docs/PLAN.md`) and the SCA-001 execution gating rule.

**Source:** `docs/PLAN.md` local-only source policy; Decomposition SCA-001 execution gating rule.

### P4: Baseline Means Compilable and Testable, Not Feature-Complete

"Baseline" in this context means the route handlers compile under TypeScript, delegate to module interfaces, and pass route-contract tests. Full runtime behavior (live SDK calls, production-grade attachment resolution, complete options mapping) requires the sibling deliverables to be integrated. The baseline routes may use stubs or minimal implementations for module dependencies that are not yet available.

**ASSUMPTION:** The baseline may use module stubs where the full implementation depends on other deliverables (e.g., DEL-03-05 for Anthropic provider integration, DEL-04-01 for attachment resolver). The route contract (types, status codes, response shapes) must be production-grade even if the underlying module is stubbed.

**Source:** SOW-045 acceptance criteria ("route handlers compile and pass baseline route-contract tests"); inference from phased plan sequencing.

---

## Considerations

### C1: Relationship to DEL-03-01 (Working Root Binding & Session Boot)

DEL-03-01 defines the session boot API contract at the requirements level. DEL-03-07 implements those requirements as actual route handlers in `frontend/`. There is intentional overlap in the session boot route specification -- DEL-03-01 is the "what" and DEL-03-07 is the "where" (local `frontend/` implementation).

The route implementations in DEL-03-07 should conform to the contracts defined in DEL-03-01 Specification (REQ-03 through REQ-11). Any conflicts between the two deliverables' specifications should be resolved in favor of DEL-03-01's normative contract, since DEL-03-07 is the implementation vehicle.

**Source:** Decomposition DEL-03-01 and DEL-03-07 entries; DEL-03-01 Specification.md.

### C2: Relationship to DEL-03-02 (Turn Execution API + SSE Streaming)

DEL-03-02 owns the turn execution and SSE streaming behavior in depth. DEL-03-07 implements the route handler that invokes that behavior. The boundary is: DEL-03-07 owns the HTTP endpoint shape, request validation, and response initiation; DEL-03-02 owns the streaming event protocol, SDK message mapping, and turn lifecycle management.

**Source:** Decomposition DEL-03-02 entry (SOW-004, SOW-005, SOW-006).

### C3: Module Stubbing Strategy

For the baseline to compile and pass contract tests without requiring all sibling deliverables to be complete, route handlers should depend on module interfaces (TypeScript interfaces/types) rather than concrete implementations. This enables:

- Compilation with stub implementations during baseline development.
- Progressive replacement of stubs with real implementations as sibling deliverables complete.
- Route-contract tests that validate HTTP-level behavior without requiring live SDK calls.

**ASSUMPTION:** Module interfaces can be defined as part of this deliverable even if the full implementations belong to other deliverables. This is a reasonable boundary because type definitions are contracts, not implementations.

### C4: Validation Script Compatibility

The existing validation scripts (`frontend/scripts/validate-harness-section8.mjs` and `frontend/scripts/validate-harness-premerge.mjs`) exercise the harness API surface. The routes implemented here must be compatible with these scripts' expectations:

- `regression.session_crud`: exercises create, list, get, delete
- `section8.smoke_stream`: exercises turn endpoint and expects ordered SSE events
- `section8.session_persistence_resume`: exercises boot + session persistence
- `section8.interrupt_sigint`: exercises interrupt endpoint

The route paths and response shapes must match what these scripts expect.

**Source:** `docs/harness/harness_manual_validation.md` Section 8 Matrix; `docs/harness/harness_ci_integration.md`.

### C5: Pre-Tier Gate Implications

DEL-03-07 is explicitly listed in the SCA-001 execution gating rule: Tier-2 code-bearing work that depends on frontend paths (including DEL-01-01, DEL-03-01, DEL-05-03, DEL-05-04) remains blocked until DEL-03-07 (among others) reaches at least IN_PROGRESS. This means:

- Delays in DEL-03-07 propagate to block Tier 2 deliverables.
- The baseline should be completed promptly with stubs where necessary, rather than waiting for all sibling deliverables.
- The gate condition is IN_PROGRESS, not ISSUED -- the baseline can unblock Tier 2 work before it is fully polished.

**Source:** Decomposition SCA-001 execution gating rule.

### C6: Next.js App Router Route File Layout

Routes should follow Next.js App Router conventions:

- `frontend/src/app/api/harness/session/create/route.ts`
- `frontend/src/app/api/harness/session/boot/route.ts`
- `frontend/src/app/api/harness/session/list/route.ts`
- `frontend/src/app/api/harness/session/[id]/route.ts` (GET + DELETE)
- `frontend/src/app/api/harness/turn/route.ts`
- `frontend/src/app/api/harness/interrupt/route.ts`

**ASSUMPTION:** The Next.js App Router convention uses file-based routing with `route.ts` handlers. This is the standard pattern for Next.js 13+ API routes. The exact directory structure depends on the frontend workspace configuration established by DEL-01-03.

---

## Trade-offs

### T1: Stub Depth vs. Baseline Fidelity

**Option A (Thin stubs):** Route handlers return hardcoded success/error responses without invoking any module logic. Tests validate HTTP-level contracts only.
- Pro: Fastest path to compilation and baseline tests passing; minimal dependencies.
- Con: Does not exercise any runtime integration; may mask interface mismatches.

**Option B (Module-interface stubs):** Route handlers call module interfaces (SessionManager, AgentSdkManager, etc.) backed by in-memory or filesystem stubs. Tests validate both HTTP contracts and module delegation.
- Pro: Catches interface mismatches early; closer to production behavior.
- Con: Requires defining and implementing stub modules; more upfront work.

**Recommendation (ASSUMPTION):** Option B is preferred because the typed failure contracts require route handlers to handle different error conditions from module operations (e.g., session not found, SDK failure). Thin stubs would not exercise these paths. However, the choice should be confirmed during implementation.

### T2: Error Type Taxonomy -- Enum vs. String Constants

**Option A (String enum):** Error type identifiers are TypeScript string enum values (e.g., `SESSION_NOT_FOUND`, `INVALID_REQUEST`, `SDK_FAILURE`).
- Pro: Type-safe; exhaustive switch checking; IDE completion.
- Con: Enum values are opaque to external callers without documentation.

**Option B (String constants with prefix):** Error types are plain string constants with a namespace prefix (e.g., `harness/session-not-found`).
- Pro: Self-documenting; easy to extend; JSON-friendly.
- Con: No compile-time exhaustiveness checking.

TBD: Human decision required on error type format. Both approaches satisfy the "typed failure contracts" requirement.

---

## Examples

### Example: Session Create Success Response

```json
POST /api/harness/session/create
Content-Type: application/json

{ "projectRoot": "/Users/ryan/ai-env/projects/example-project" }

200 OK
{
  "session": {
    "sessionId": "sess_abc123",
    "projectRoot": "/Users/ryan/ai-env/projects/example-project",
    "createdAt": "2026-02-22T15:00:00Z"
  }
}
```

**ASSUMPTION:** Response shape is inferred from DEL-03-01 Datasheet session record schema and standard API conventions. The exact field names and shapes are TBD pending implementation.

### Example: Typed Failure Response

```json
POST /api/harness/session/boot
Content-Type: application/json

{ "sessionId": "nonexistent-id" }

404 Not Found
{
  "error": {
    "type": "SESSION_NOT_FOUND",
    "message": "Session 'nonexistent-id' does not exist",
    "sessionId": "nonexistent-id"
  }
}
```

**ASSUMPTION:** Error response envelope shape is inferred from the "typed failure contracts" requirement and standard conventions. The exact structure is TBD.

### Example: Turn SSE Stream

```
POST /api/harness/turn
Content-Type: application/json

{ "sessionId": "sess_abc123", "message": "Hello", "opts": {} }

200 OK
Content-Type: text/event-stream

event: session:init
data: {"claudeSessionId":"claude_xyz","model":"claude-sonnet-4-20250514"}

event: chat:delta
data: {"text":"Hello! "}

event: chat:delta
data: {"text":"How can I help?"}

event: chat:complete
data: {"text":"Hello! How can I help?"}

event: session:complete
data: {}

event: process:exit
data: {"exitCode":0}
```

**Source:** `docs/harness/harness_manual_validation.md` Section 8 Matrix (smoke stream ordering); `docs/harness/chirality_harness_graphs_and_sequence.md` sequence diagram.

---

## Conflict Table (for human ruling)

| Conflict ID | Conflict | Source A | Source B | Impacted Sections | Proposed Authority | Human Ruling |
|-------------|---------|----------|----------|-------------------|-------------------|-------------|
| CONFLICT-001 | Session create request body: DEL-03-01 specifies `projectRoot` as the minimum required field, but the Guidance example in DEL-03-01 shows `{ projectRoot, persona, mode }`. It is unclear whether `persona` and `mode` are required at create time or only at boot time for DEL-03-07. | DEL-03-01 Specification REQ-03 | DEL-03-01 Guidance C3 example | Specification REQ-01, Datasheet Session Endpoints | DEL-03-01 Specification REQ-03 (normative) | TBD |
| CONFLICT-002 | Session storage location: DEL-03-01 identifies an unresolved trade-off between storing sessions under the Working Root vs. under an app data directory. DEL-03-07 route handlers need to know where SessionManager reads/writes. | DEL-03-01 Datasheet (session storage location TBD) | DEL-03-01 Guidance T2 | Specification REQ-13 (SessionManager persistence) | Human ruling required (DEL-03-01 CONFLICT-001/002) | TBD |
| CONFLICT-003 | Error type taxonomy format: typed failure contracts require a consistent error type format, but no format is specified in source documents. String enum vs. string constants trade-off is unresolved. | SOW-045 ("typed failure contracts") | No format specification exists | Specification REQ-08, Guidance T2 | Human decision required | TBD |
