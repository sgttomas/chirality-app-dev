# Dependencies -- DEL-01-01

**Tracking Mode:** FULL_GRAPH
**Status:** ACTIVE
**Register Schema:** v3.1

---

## Declared Upstream Dependencies

- Repository source code (Git repository) -- primary input; available.
- No upstream deliverable dependencies declared in original source documents.
- **[SCA-001]** DEL-01-03 (Frontend Workspace Bootstrap & Packaging Baseline) -- prerequisite; frontend workspace must reach IN_PROGRESS before desktop build can proceed.
- **[SCA-001]** DEL-03-07 (Harness API Baseline in Frontend Runtime) -- prerequisite; harness API routes must reach IN_PROGRESS before build verification can confirm application functions.

## Declared Downstream Dependencies

- **DEL-01-02** (Unsigned DMG Packaging Workflow) -- consumes the `.app` bundle produced by this deliverable.

---

## Extracted Dependency Register

**Total ACTIVE rows:** 11
**Total RETIRED rows:** 0

### ANCHOR rows (4 ACTIVE)

| DependencyID | AnchorType | TargetRefID | TargetName | Confidence |
|---|---|---|---|---|
| DEP-01-01-001 | IMPLEMENTS_NODE | SOW-001 | SOW-001: The Chirality desktop app builds and runs on macOS | HIGH |
| DEP-01-01-002 | TRACES_TO_REQUIREMENT | OBJ-001 | OBJ-001: Working macOS desktop build and install path | HIGH |
| DEP-01-01-003 | TRACES_TO_REQUIREMENT | DEC-PLAT-001 | DEC-PLAT-001: macOS 15+ Apple Silicon only; no signing/notarization | HIGH |
| DEP-01-01-004 | TRACES_TO_REQUIREMENT | DEC-NET-001 | DEC-NET-001: Anthropic-only outbound network | HIGH |

### EXECUTION rows (7 ACTIVE)

| DependencyID | Direction | DependencyType | TargetType | Target | Confidence |
|---|---|---|---|---|---|
| DEP-01-01-005 | DOWNSTREAM | HANDOVER | DELIVERABLE | DEL-01-02: Unsigned DMG Packaging Workflow | HIGH |
| DEP-01-01-006 | DOWNSTREAM | INTERFACE | DELIVERABLE | DEL-03-06: Outbound Network Guardrails + Verification | HIGH |
| DEP-01-01-007 | UPSTREAM | CONSTRAINT | DELIVERABLE | DEL-05-01: Instruction Root Bundling & Runtime Access | HIGH |
| DEP-01-01-008 | UPSTREAM | PREREQUISITE | EXTERNAL | Repository source code (Git repository) | HIGH |
| DEP-01-01-009 | UPSTREAM | CONSTRAINT | DOCUMENT | docs/DIRECTIVE.md | HIGH |
| DEP-01-01-010 | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-01-03: Frontend Workspace Bootstrap & Packaging Baseline | HIGH |
| DEP-01-01-011 | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-03-07: Harness API Baseline in Frontend Runtime | HIGH |

---

## Lifecycle Summary

| Status | Count |
|---|---|
| ACTIVE | 11 |
| RETIRED | 0 |

| SatisfactionStatus | Count |
|---|---|
| TBD | 9 |
| SATISFIED | 2 |

| DependencyClass | ACTIVE | RETIRED |
|---|---|---|
| ANCHOR | 4 | 0 |
| EXECUTION | 7 | 0 |

---

## Run Notes

**Run date:** 2026-02-22
**Mode:** UPDATE
**Strictness:** CONSERVATIVE
**Consumer context:** NONE
**Decomposition path:** `/Users/ryan/ai-env/projects/chirality-app-dev/execution/_Decomposition/ChiralityApp_SoftwareDecomposition_2026-02-21_G7-APPROVED.md`
**Decomposition status:** AVAILABLE (G7-APPROVED + SCA-001 amendment)

### Defaults used

- **SOURCE_DOCS:** AUTO -- scanned deliverable folder; found: Datasheet.md, Specification.md, Guidance.md, Procedure.md, _CONTEXT.md, _REFERENCES.md
- **ANCHOR_DOC:** Datasheet.md (selected as highest-confidence anchor doc per DOC_ROLE_MAP heuristic: contains "datasheet" in filename; confirmed identification fields, scope coverage, and objective mapping)
- **EXECUTION_DOC_ORDER:** Specification.md, Procedure.md, Guidance.md (ordered by workflow clarity for execution signal extraction)
- **_REFERENCES.md:** Read; no deliverable-specific references found beyond decomposition pointer.
- **Decomposition amendment SCA-001:** Read; Scope Amendment A1 section provides explicit execution gating rule for DEL-01-01.

### Assumptions

- OBJ-001 recorded as TRACES_TO_REQUIREMENT (closest anchor type for objective traceability; OBJ-001 is an objective, not a formal requirement).
- DEC-PLAT-001 and DEC-NET-001 recorded as TRACES_TO_REQUIREMENT with TargetType=REQUIREMENT (decision references function as upstream constraints).
- DEL-03-06 interface recorded as DOWNSTREAM because DEL-01-01 build-time findings inform DEL-03-06 runtime scope boundary. The relationship could also be viewed as bidirectional (DEL-03-06 defines the runtime standard DEL-01-01 must set up for); the DOWNSTREAM direction reflects the explicit statement that "this deliverable ensures the build configuration does not introduce unauthorized outbound connections" which DEL-03-06 then enforces at runtime.
- DEL-01-03 and DEL-03-07 prerequisites (DEP-01-01-010, DEP-01-01-011) use `RequiredMaturity=IN_PROGRESS` per the SCA-001 execution gating rule which states deliverables must "reach at least IN_PROGRESS per blocker maturity policy."
- DEL-02-05 and DEL-07-03 are also named in SCA-001 gating rule but are NOT recorded as direct dependencies of DEL-01-01 under CONSERVATIVE strictness: DEL-01-01 does not consume information/artifacts from the workflow shell (DEL-02-05) or validation runbooks (DEL-07-03). The gating rule is a scheduling/coordination constraint, not an information-flow edge, for those two deliverables relative to DEL-01-01. DEL-01-03 and DEL-03-07 are recorded because the desktop build target and functional verification require their artifacts.

### Integration Fan-In Refresh (2026-02-22)

- Re-validated lifecycle truth from upstream `_STATUS.md` files:
  - `DEL-01-03` = `IN_PROGRESS`
  - `DEL-03-07` = `IN_PROGRESS`
- Updated `Dependencies.csv` rows `DEP-01-01-010` and `DEP-01-01-011`:
  - `SatisfactionStatus` set to `SATISFIED` after gate verification.
  - Corrected CSV field alignment so `TargetName`/`Statement`/`EvidenceFile`...`Status`/`Notes` map to the v3.1 schema columns without overflow.
  - Notes normalized to reflect gate-met status while retaining SCA-001 provenance.
- No rows were added or retired in this fan-in refresh.

### Warnings

*(None)*

### Integrity checks

- Parent anchor (IMPLEMENTS_NODE) count: 1 (SOW-001). PASS.
- DependencyID uniqueness: 11 unique IDs, 11 rows. PASS.
- All ACTIVE rows have EvidenceFile and SourceRef. PASS.
- CSV is parseable with required columns present. PASS.
- _DEPENDENCIES.md counts match Dependencies.csv. PASS.
- No obvious duplicate rows. PASS.
- New rows DEP-01-01-010 and DEP-01-01-011 confirmed against decomposition: DEL-01-03 exists in PKG-01, DEL-03-07 exists in PKG-03. PASS.
- SCA-001 gating rows DEP-01-01-010 and DEP-01-01-011 now closure-normalized to SATISFIED after lifecycle verification. PASS.

---

## Run History

| Timestamp | Mode | Strictness | DecompStatus | Warnings | ACTIVE Count |
|---|---|---|---|---|---|
| 2026-02-22 (normalization pass) | UPDATE | CONSERVATIVE | AVAILABLE (G7-APPROVED + SCA-001) | None | 11 |
| 2026-02-22 (fan-in refresh) | UPDATE | CONSERVATIVE | AVAILABLE (G7-APPROVED + SCA-001) | None | 11 |
| 2026-02-22 | UPDATE | CONSERVATIVE | AVAILABLE (G7-APPROVED + SCA-001) | None | 11 |
| 2026-02-21 | UPDATE | CONSERVATIVE | AVAILABLE (G7-APPROVED) | None | 9 |

---

## Downstream Handoff Notes

*(CONSUMER_CONTEXT is NONE; no downstream handoff notes generated.)*
