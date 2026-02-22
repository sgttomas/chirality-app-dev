# Working Memory — DEL-07-02

*This file is shared working memory for WORKING_ITEMS and TASK agents operating on this deliverable.*

## Key Decisions & Human Rulings

- Example inventory: 1 primary execution root (`examples/example-project/`) with 1 package (PKG-99) and 3 deliverables at 3 lifecycle states (OPEN, INITIALIZED, SEMANTIC_READY). ASSUMPTION: assumed from Procedure Phase 1 default; needs human confirmation.
- Synthetic IDs: PKG-99, DEL-99-01/02/03 chosen to avoid collision with real project IDs (PKG-01..08).
- Dependencies.csv inclusion: deferred (Procedure Phase 6 conditional; needs human ruling).

## Domain Context

### Fixture Structure (created 2026-02-22)

```
examples/example-project/
  INIT.md
  _Coordination/_COORDINATION.md
  _Decomposition/Example_Decomposition.md
  _Aggregation/, _Change/, _Estimates/, _Reconciliation/, _Archive/, _Scripts/, _Sources/ (tool roots)
  PKG-99_Example_Package/
    0_References/_Archive/
    1_Working/_Archive/
    1_Working/DEL-99-01_Widget_Configuration/  (OPEN — min viable fileset)
    1_Working/DEL-99-02_Service_Integration/   (INITIALIZED — fileset + document kit)
    1_Working/DEL-99-03_Test_Harness/          (SEMANTIC_READY — fileset + kit + _SEMANTIC.md)
    2_Checking/From/, 2_Checking/To/
    3_Issued/_Archive/
```

### SPEC conformance checklist

- [x] REQ-01: Execution root conforms to SPEC Section 1 (PKG, _Decomposition, INIT.md)
- [x] REQ-02: Package folder conforms to SPEC Section 1.1 (all required subfolders)
- [x] REQ-03: Deliverable folders conform to SPEC Section 2 (naming, minimum viable fileset)
- [x] REQ-04: At least one deliverable at INITIALIZED+ with full document kit (DEL-99-02, DEL-99-03)
- [x] REQ-05: Folder names follow SPEC Section 10 sanitization
- [x] REQ-06: Every _STATUS.md has valid state, Last Updated, History
- [x] REQ-07: At least one _SEMANTIC.md with Matrix A and B tables (DEL-99-03)
- [x] REQ-08: Stable IDs consistent across folder names, _CONTEXT.md, _STATUS.md, decomposition
- [x] REQ-09: All content is synthetic (no real project data, credentials, proprietary content)
- [ ] REQ-10: Examples usable by DEL-07-01 validation scripts without external setup — not yet verified (DEL-07-01 validation scripts needed)

## Open Items

- **TBD: Number of example roots** — currently 1; Procedure suggests confirming with human. ASSUMPTION: 1 is sufficient for initial conformance testing.
- **TBD: Dependencies.csv samples** — deferred to Phase 6; needs human ruling on inclusion.
- **REQ-10 verification** — cannot verify until DEL-07-01 validation scripts exist. Cross-deliverable dependency.

## Proposal History

- Initial fixture created this session (1 root, 1 package, 3 deliverables, 3 lifecycle states).

## Interface & Dependency Notes

- DEL-07-01 (Harness Validation Scripts) must be able to exercise these fixtures. Scripts don't exist yet.
- DEL-08-03 (standalone CI validator) is out of scope but may also consume these fixtures.
