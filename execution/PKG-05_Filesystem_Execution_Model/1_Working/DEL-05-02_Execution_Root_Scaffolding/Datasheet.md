# Datasheet -- DEL-05-02 Execution Root Scaffolding + Layout Conformance

## Identification

| Field | Value |
|-------|-------|
| **Deliverable ID** | DEL-05-02 |
| **Name** | Execution Root Scaffolding + Layout Conformance |
| **Package** | PKG-05 Filesystem Execution Model |
| **Type** | BACKEND_FEATURE_SLICE |
| **Context Envelope** | M |
| **Responsible Party** | TBD -- requires explicit human assignment (`B-001`); non-blocking for current baseline scope. |
| **Scope Items** | SOW-014, SOW-015 |
| **Objectives** | OBJ-004 |
| **Anticipated Artifacts** | CODE / TEST / DOC |
| **Decomposition Ref** | `execution/_Decomposition/ChiralityApp_SoftwareDecomposition_2026-02-21_G7-APPROVED.md` |

## Attributes

| Attribute | Value | Source |
|-----------|-------|--------|
| **Platform** | macOS 15+, Apple Silicon only | Decomposition DEC-PLAT-001 |
| **Runtime** | Electron + Next.js desktop app | Decomposition SOW-001 |
| **State Model** | Filesystem-as-state; no external DB; no server required for project state | DIRECTIVE Section 2.1; SOW-014 |
| **Layout Authority** | `docs/SPEC.md` Section 1 (Execution Root Layout) | SOW-015 |
| **Validation Authority** | `docs/SPEC.md` Section 12 (Folder Structure Validation Checklist) | SPEC Section 12 |
| **ID Formats** | `PKG-XX`, `DEL-XX-YY` per `docs/TYPES.md` Section 2 | TYPES Section 2 |
| **Folder Naming** | `{ID}_{Sanitize(Name)}` per `docs/SPEC.md` Section 10 | SPEC Section 10 |
| **Instruction/Working Root Separation** | Instruction root (app bundle) vs working root (`projectRoot`) | DIRECTIVE Section 2.6; SOW-013 (covered by DEL-05-01) |

## Conditions

| Condition | Constraint | Source |
|-----------|-----------|--------|
| **Execution Root Validity** | At least one `PKG-XX_{Label}/` folder exists; `_Decomposition/` exists with >= 1 decomposition doc; `INIT.md` exists | SPEC Section 12.1 |
| **Package Folder Validity** | Named `{PKG-ID}_{PkgLabel}/`; contains `1_Working/`; validation checklist in SPEC 12.2 uses SHOULD for `0_References/`, `2_Checking/`, `3_Issued/`, while scaffolding creation behavior for DEL-05-02 remains MUST per SPEC 1.1 | SPEC Sections 1.1, 12.2 |
| **Deliverable Folder Validity** | Named `{DEL-ID}_{DelLabel}/`; contains `_STATUS.md`, `_CONTEXT.md`, `_DEPENDENCIES.md`, `_REFERENCES.md` | SPEC Section 12.3 |
| **Tool Root Presence** | `_Aggregation/`, `_Change/`, `_Coordination/`, `_Decomposition/`, `_Estimates/`, `_Reconciliation/`, `_Archive/`, `_Scripts/`, `_Sources/` | SPEC Section 1.2 |
| **Tool Root Sub-structure** | `_Aggregation/_Archive/`, `_Aggregation/_Templates/`, `_Decomposition/_Archive/` are required sub-directories; `_Sources/` has no required sub-structure in current SPEC | SPEC Sections 1, 1.2 |
| **`_Archive/` at Execution Root** | Top-level `_Archive/` exists at execution root as a tool root distinct from `_Archive/` sub-directories within other tool roots -- **[see X-001:]** Verify SPEC Section 1 distinguishes this from sub-directory `_Archive/` instances. | SPEC Section 1 |
| **Snapshot Immutability** | Task agent outputs to tool roots are immutable snapshots; pointer files (`_LATEST.md`) may be overwritten | SPEC Section 11; CONTRACT K-SNAP-1 |
| **No External DB** | No database dependency; filesystem is single source of truth | DIRECTIVE Section 5 (Structural Constraints) |
| **Flat Hierarchy** | Packages contain deliverables; no nesting, no phases | CONTRACT K-HIER-1; TYPES Section 1 |

## Construction

| Element | Description | Source |
|---------|-------------|--------|
| **Scaffolding Logic** | Code that creates the required execution-root directory tree (packages, tool roots, deliverable folders) when a new execution instance is initialized | Implemented at `frontend/src/lib/harness/scaffold.ts` + `POST /api/harness/scaffold` |
| **Package Subfolder Creation** | Creates `0_References/`, `0_References/_Archive/`, `1_Working/`, `1_Working/_Archive/`, `2_Checking/`, `2_Checking/From/`, `2_Checking/To/`, `3_Issued/`, `3_Issued/_Archive/` per package | SPEC Section 1.1 |
| **Tool Root Creation** | Creates all tool root directories listed in SPEC Section 1.2, including required sub-structure (`_Aggregation/_Archive/`, `_Aggregation/_Templates/`, `_Decomposition/_Archive/`) | SPEC Section 1.2 |
| **INIT.md Generation** | Creates `INIT.md` with session initialization parameters at the execution root | SPEC Section 12.1 |
| **Conformance Validator** | Code/tests verify execution-root layout in this deliverable; standalone CLI validator remains optional in DEL-08-03 and non-driving while SOW-034 is `TBD` | Specification REQ-09; `_COORDINATION.md` PKG-08 scope ruling |
| **Label Sanitization** | Implements `Sanitize(name)` per SPEC Section 10.1 for folder naming; steps are applied in declared order (replace, collapse, trim) -- **[see X-002 in Specification REQ-04 for ordering clarification]** | SPEC Section 10 |
| **Error Handling** | Fail-fast with structured diagnostics (`scaffoldStrategy`, `stage`, `targetPath`, partial-create snapshot, rerun guidance); no rollback/delete behavior | `frontend/src/lib/harness/scaffold.ts`; `frontend/src/__tests__/lib/harness-scaffold.test.ts`; `frontend/src/__tests__/api/harness/scaffold-route.test.ts` |
| **Test Suite** | Tests verifying scaffolding correctness and layout conformance, including malformed decomposition input handling | Anticipated artifact: TEST |
| **Documentation** | Developer documentation describing scaffolding behavior and layout contract | Anticipated artifact: DOC |

## References

| Reference | Location | Relevance |
|-----------|----------|-----------|
| SPEC.md | `docs/SPEC.md` | Authoritative layout specification (Sections 1, 10, 11, 12) |
| CONTRACT.md | `docs/CONTRACT.md` | Binding invariants (K-HIER-1, K-SNAP-1, K-WRITE-1) |
| DIRECTIVE.md | `docs/DIRECTIVE.md` | Founding intent and structural constraints |
| TYPES.md | `docs/TYPES.md` | ID formats and folder label rules |
| PLAN.md | `docs/PLAN.md` | Future hardening candidates (Sections 3.3, 3.4) |
| Decomposition | `execution/_Decomposition/ChiralityApp_SoftwareDecomposition_2026-02-21_G7-APPROVED.md` | DEL-05-02 entry and scope ledger |
