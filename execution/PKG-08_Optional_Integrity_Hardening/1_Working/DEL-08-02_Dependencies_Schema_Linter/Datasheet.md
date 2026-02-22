# Datasheet -- DEL-08-02 Dependencies.csv v3.1 Schema Linter

## Identification

| Field | Value |
|-------|-------|
| **DeliverableID** | DEL-08-02 |
| **Name** | Dependencies.csv v3.1 Schema Linter |
| **PackageID** | PKG-08 |
| **Package** | Optional Integrity Hardening |
| **Type** | TEST_SUITE |
| **ContextEnvelope** | S |
| **ResponsibleParty** | TBD -- **NOTE:** No responsible party has been assigned. This weakens prescriptive authority for normative direction of this deliverable. Human assignment required before implementation begins. (Identified via Semantic Lensing A-001) |
| **Scope Coverage** | SOW-033 |
| **Supports Objectives** | OBJ-007 |

## Attributes

| Attribute | Value | Source |
|-----------|-------|--------|
| **Schema Version Targeted** | v3.1 | `docs/SPEC.md` Section 6.1 |
| **Column Count (Core)** | 29 | `docs/SPEC.md` Section 6.2 |
| **Column Count (Extension)** | 2 | `docs/SPEC.md` Section 6.2 |
| **Canonical Enum Families** | 10 (DependencyClass, AnchorType, Direction, DependencyType, TargetType, Explicitness, SatisfactionStatus, Confidence, Origin, Status) | `docs/SPEC.md` Section 6.3 |
| **Implementation Language** | Python -- **ASSUMPTION** (per `docs/PLAN.md` Section 3.2 which states "a Python script") | `docs/PLAN.md` Section 3.2 |
| **Execution Context** | Standalone CLI + CI-level integration | `docs/PLAN.md` Section 3.2; Decomposition DEL-08-02 description |
| **Anticipated Artifacts** | SCRIPT, TEST, DOC | Decomposition DEL-08-02 |
| **Scope Item Status** | TBD (SOW-033 not yet flipped IN) | Decomposition SSOW |

## Conditions

| Condition | Value | Source |
|-----------|-------|--------|
| **SOW-033 Scope Decision** | TBD -- this deliverable is contingent on SOW-033 being flipped to IN | Decomposition SSOW; Open Issue OI-033 |
| **Input File Format** | CSV (comma-separated, UTF-8) | `docs/SPEC.md` Section 6 (implicit; Dependencies.csv) |
| **Target Environments** | Local developer workstation, CI pipeline | `docs/PLAN.md` Section 3.2 |
| **Python Runtime Version** | Python 3.8+ -- **ASSUMPTION** (Guidance C1 identifies 3.8+ as a reasonable floor given ecosystem norms; not specified in governance) | **ASSUMPTION** -- based on Python implementation language; floor per Guidance C1 |
| **No External Network** | Linter must operate offline; no outbound network required | **ASSUMPTION** -- consistent with DIRECTIVE Section 5 structural constraints |
| **No External Dependencies (Core)** | Core validation requires only Python standard library (`csv` module) | **ASSUMPTION** -- per Guidance C1 and P4 (standalone, no runtime dependencies) |

## Construction

| Aspect | Detail |
|--------|--------|
| **Primary Artifact** | Python script (`validate_dependencies.py` or equivalent) |
| **Test Artifacts** | Unit tests for each validation rule; fixture CSV files (valid + invalid variants) |
| **Documentation Artifact** | Usage instructions (CLI invocation, CI integration, exit codes, error output format) |
| **Integration Pattern** | Standalone invocation; no import into other runtime code required -- **ASSUMPTION** |

## References

| Ref | Document | Relevance |
|-----|----------|-----------|
| R1 | `docs/SPEC.md` Section 6 | Authoritative v3.1 schema definition -- column spec, enums, identity rules, provenance requirements, lifecycle tracking, legacy compatibility |
| R2 | `docs/TYPES.md` Section 3 | Dependency vocabulary (classes, anchor types, direction, types, target types, provenance, satisfaction) |
| R3 | `docs/CONTRACT.md` | Invariants K-PROV-1, K-DEP-1, K-DEP-2, K-INVENT-1 governing dependency register integrity |
| R4 | `docs/PLAN.md` Section 3.2 | Future hardening candidate description for this deliverable |
| R5 | Decomposition (`ChiralityApp_SoftwareDecomposition_2026-02-21_G7-APPROVED.md`) | DEL-08-02 entry, SOW-033, OBJ-007, OI-033 |
