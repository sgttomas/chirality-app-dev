# Guidance — DEL-03-01 Working Root Binding & Session Boot

## Purpose

This deliverable establishes the foundational contract through which the Chirality desktop application connects a user's chosen filesystem directory to the harness runtime. Without a reliable working root binding and session boot mechanism, no downstream agent execution can occur. Session boot is the "ignition sequence" that transitions the app from an idle state into a configured, agent-ready session.

This deliverable supports two objectives:

- **OBJ-001** (Working macOS desktop build): The user must be able to select a working directory and begin using the harness -- session boot is the critical path for this.
- **OBJ-002** (Harness runtime correctness): Sessions must boot correctly with proper option parsing and initialization before turns can execute.

**Source:** Decomposition DEL-03-01 entry; OBJ-001 acceptance criteria; OBJ-002 acceptance criteria.

---

## Principles

### P1: Filesystem Is the Session Store

Sessions are filesystem artifacts, consistent with the project's core architectural constraint that "the filesystem is the database" (DIRECTIVE Section 2.1). Session records live on disk, are human-readable, and do not require an external database. This means:

- Session persistence uses file I/O, not a database connection.
- Session state survives application restarts without migration or recovery procedures.
- Session records are implicitly auditable via git (if the storage location is within a tracked directory) or via filesystem tools.

**Source:** DIRECTIVE Section 2.1, Section 5.

### P2: Working Root Is Not Instruction Root

The system maintains a strict separation between what agents know (Instruction Root -- shipped in the app bundle) and where they work (Working Root -- user-selected directory). Session boot must resolve both:

- Instruction Root provides persona definitions, framework docs, and agent instructions.
- Working Root provides the execution context where agents create and modify deliverable state.

This separation ensures that updating the app (Instruction Root) does not alter user project state, and that user project state does not contaminate agent instructions.

**Source:** DIRECTIVE Section 2.6; SOW-013.

### P3: Boot Is Idempotent Configuration, Not Mutation

Session boot should configure the session for execution without modifying the Working Root's content. The boot sequence reads from the Working Root (to establish context) and reads from the Instruction Root (to load persona/prompts), but the only writes should be to session state storage.

**[A-001]** This principle is currently labeled as an ASSUMPTION inferred from the architecture's separation of concerns. If boot idempotency is a binding design constraint, it should be promoted to a normative requirement in Specification.md (e.g., a new REQ or addition to REQ-05). If the bootstrap turn may legitimately write to the Working Root during boot, this principle needs revision. **Human ruling required** -- see Conflict Table entry CONFLICT-004.

**ASSUMPTION:** Inferred from the separation of concerns in the architecture. If the bootstrap turn writes to the Working Root during boot, this principle needs revision.

### P4: Options Follow Explicit Fallback Chains

Runtime options (`opts`) use documented fallback chains rather than silent defaults. This makes the system predictable: an operator can trace exactly which value was used and where it came from. The chain is always:

1. Explicit per-turn/per-boot `opts` value (highest priority).
2. Persona-level frontmatter value.
3. Global or runtime default (lowest priority).

**Source:** SPEC Section 9.8.

---

## Considerations

### C1: Session Identity and Claude Session ID

The harness maintains two identity layers:

- **Harness session ID** (`sessionId`): created by `POST /api/harness/session/create`, used for all harness-level operations.
- **Claude session ID** (`claudeSessionId`): assigned by the Anthropic Agent SDK during the first successful `query()` call, persisted by the harness for session resumption.

The boot sequence bridges these two identities: it takes a harness `sessionId`, executes a bootstrap turn that produces a `claudeSessionId`, and persists both together.

**Source:** harness sequence diagram; `section8.session_persistence_resume` validation check.

### C2: Boot Fingerprinting

The boot sequence computes a `bootFingerprint` via `PersonaManager.getBootFingerprint(persona, mode)`. This fingerprint likely captures the effective configuration at boot time (persona identity, operating mode, and possibly prompt version).

**[B-002]** The following aspects of boot fingerprinting are undocumented and require clarification:

- **Input composition:** What specific inputs feed `getBootFingerprint(persona, mode)`? Does "persona" include the full persona markdown content, a content hash, or just the persona identifier? Does "mode" refer to the operating mode string (e.g., `plan`, `execute`)?
- **Hash construction:** What hashing algorithm is used? Is the fingerprint a deterministic content hash, a UUID, or a composite key?
- **Change detection semantics:** Is the fingerprint used to detect when a re-boot is needed (e.g., persona content changed since last boot)? If so, what action is taken when the fingerprint differs from the stored value?
- **Downstream consumers:** Which components (if any) read the boot fingerprint after it is stored, and for what purpose?

These questions are TBD pending implementation review. Source path: `PersonaManager` module in harness architecture.

**ASSUMPTION:** The boot fingerprint is used for change detection -- if the persona or mode changes, the harness can detect that a re-boot may be needed. Exact fingerprint composition is TBD pending implementation review.

### C3: Error Handling at Boot

The boot sequence involves multiple potentially-failing steps (session resume, persona lookup, SDK query). The error handling strategy should consider:

- **Session not found:** Return `404` with `SESSION_NOT_FOUND`.
- **Persona not found:** Return `404` with `PERSONA_NOT_FOUND`.
- **SDK failure:** Return `500` with `SDK_FAILURE` and diagnostic details when available.
- **Working Root inaccessible:** Return `404` with `WORKING_ROOT_INACCESSIBLE` before attempting SDK call.

These scenarios are captured normatively in Specification REQ-11 and are regression-checked by `frontend/src/__tests__/api/harness/routes.test.ts` and `frontend/scripts/validate-harness-section8.mjs` (`section8.boot_error_taxonomy`).

### C4: Relationship to DEL-03-02 (Turn Execution)

Session boot is a prerequisite for turn execution. DEL-03-02 depends on a successfully booted session to execute turns. The interface contract between boot and turn is:

- Boot produces a session record with `claudeSessionId`, `bootFingerprint`, and `bootedAt`.
- Turn execution resumes the session and uses the persisted `claudeSessionId` for SDK continuity.

**Source:** harness sequence diagram (boot at lines 94-99, turn at lines 101+).

### C5: Relationship to DEL-03-03 (Options Mapping)

DEL-03-03 covers the full opts mapping and fallback chain specification. This deliverable (DEL-03-01) covers the boot-time subset: ensuring that `opts` passed to boot are correctly resolved through fallback chains. The full runtime mapping during turn execution is DEL-03-03's responsibility.

**Source:** Decomposition; SOW-011 (assigned to DEL-03-03).

### C6: Concurrent Session Behavior -- **[F-003]**

The Specification defines CRUD operations for sessions (REQ-08), and multiple sessions can coexist (a user could create several sessions for different projects). However, neither the Specification nor the current Guidance addresses:

- **Concurrent boot requests:** Can multiple sessions be booted simultaneously? If two boot requests arrive for different sessions, are they processed in parallel or serialized?
- **Same-session re-boot:** What happens if a boot request arrives for a session that is already booted or currently booting? Is the boot idempotent (returns existing boot state), does it re-execute the boot sequence, or does it reject with an error?
- **Resource contention:** If concurrent boots both call the Anthropic Agent SDK, are there resource limits (API rate limits, local mutex constraints) that affect behavior?

TBD: Human decision required to determine whether concurrent session behavior is in-scope for this deliverable or explicitly excluded. If in-scope, add requirements to Specification. If out-of-scope, document the exclusion.

**Source:** _SEMANTIC_LENSING.md item F-003; Specification REQ-08 (CRUD implies multiple sessions exist).

---

## Trade-offs

### T1: Eager Boot vs Lazy Boot

| Approach | Pros | Cons |
|----------|------|------|
| Eager boot (boot on session create) | Simpler UX flow; one step to usable session | Slower session creation; wasted SDK call if session is never used |
| Lazy boot (separate boot step after create) | Lighter session creation; boot only when needed | Two-step UX flow; must handle unbooted session state |

The current architecture uses **lazy boot** (separate `create` and `boot` endpoints), labeled as "optional prewarm boot path" in the sequence diagram. This is appropriate for a desktop app where session creation may precede actual use.

**Source:** harness sequence diagram annotation "Optional prewarm boot path."

### T2: Session Storage Location

| Option | Pros | Cons |
|--------|------|------|
| Under Working Root (e.g., `.chirality/sessions/`) | Sessions travel with the project; git-trackable | Pollutes user's project directory; may conflict with user content |
| Under app data directory | Clean separation from project content | Sessions do not travel with the project; no git auditability |

**ASSUMPTION:** The current implementation stores sessions under an app-managed path (`.chirality/sessions`), not directly in the Working Root. This needs confirmation from implementation. The architecture diagram shows filesystem storage at `.chirality/sessions` without specifying the parent path.

**[E-002, E-003]** This trade-off is currently unresolved and creates a cross-document inconsistency. See Conflict Table entries CONFLICT-001 and CONFLICT-002.

---

## Examples

### Example: Minimal Session Boot Flow

```
1. User selects projectRoot via UI file picker
2. UI calls POST /api/harness/session/create { projectRoot, persona, mode }
3. Server creates session record, returns { sessionId }
4. UI calls POST /api/harness/session/boot { sessionId }
5. Server resumes session, computes boot fingerprint, executes bootstrap turn
6. Server persists claudeSessionId + bootFingerprint + bootedAt
7. Server returns 200 { session, boot }
8. Session is now ready for turn execution (DEL-03-02)
```

**[C-002]** Note: Step 2 shows `{ projectRoot, persona, mode }` as the create payload, but Specification REQ-03 only requires the session record to include `projectRoot`. The `persona` and `mode` parameters at create-time are not normatively specified. See Conflict Table CONFLICT-003.

**Source:** Derived from harness sequence diagram.

### Example: Boot with Options Override

```
POST /api/harness/session/boot
{
  "sessionId": "sess_abc123",
  "opts": {
    "model": "claude-sonnet-4-20250514",
    "maxTurns": 5
  }
}

Response 200:
{
  "session": { "id": "sess_abc123", "projectRoot": "/path/to/project", ... },
  "boot": { "claudeSessionId": "csess_xyz", "bootFingerprint": "fp_...", "bootedAt": "..." }
}
```

**ASSUMPTION:** Exact request/response shapes are illustrative and require confirmation from implementation.

---

## Conflict Table (for human ruling)

| Conflict ID | Conflict | Source A | Source B | Impacted Sections | Proposed Authority (PROPOSAL) | Human Ruling |
|-------------|----------|----------|----------|-------------------|-------------------------------|--------------|
| CONFLICT-001 | Session storage canonical base path is undefined: Datasheet assumed `.chirality/sessions/` under app state path; Specification REQ-07 says only "local filesystem"; Guidance T2 presents both "Under Working Root" and "Under app data directory" as open options. | Datasheet.md: Working Root Binding > Session storage location | Guidance.md: T2: Session Storage Location; Specification.md: REQ-07 | Datasheet (Session storage location), Specification (REQ-07), Guidance (T2), Procedure (filesystem paths) | Human decision (depends on T2 resolution) | TBD |
| CONFLICT-002 | Terminology for session storage path varies across documents: "`.chirality/sessions/` under the app's state path" (Datasheet), "local filesystem" (Specification), "Under Working Root" vs "Under app data directory" (Guidance). Need single canonical term and location. | Datasheet.md: Session storage location | Specification.md: REQ-07; Guidance.md: T2 | All four documents (terminology normalization) | Human decision -- adopt one canonical path after T2 resolution | TBD |
| CONFLICT-003 | Session create payload parameters: Guidance example shows `POST /api/harness/session/create { projectRoot, persona, mode }` but Specification REQ-03 only requires the session record to include `projectRoot`. The `persona` and `mode` parameters at create-time are not normatively specified. | Specification.md: REQ-03 | Guidance.md: Example: Minimal Session Boot Flow | Specification (REQ-03), Guidance (Example), Datasheet (Session Record Schema) | Specification.md -- either add `persona` and `mode` as required create parameters or clarify that they are provided at boot time only | TBD |
| CONFLICT-004 | Boot idempotency: Guidance P3 states boot should be idempotent configuration (no Working Root mutation), but this is flagged as ASSUMPTION. If the bootstrap turn writes to the Working Root, P3 must be revised. If idempotency is a binding constraint, it should be a Specification requirement. | Guidance.md: P3: Boot Is Idempotent Configuration, Not Mutation | Specification.md: REQ-05 (bootstrap turn behavior unspecified re: writes) | Specification (potential new REQ or REQ-05 update), Guidance (P3), Procedure (boot verification) | Specification.md -- promote to requirement or revise P3 | TBD |
