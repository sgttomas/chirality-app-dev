# Working Memory — DEL-08-02

*This file is shared working memory for WORKING_ITEMS and TASK agents operating on this deliverable.*

## Key Decisions

- 2026-02-24: Implemented standalone linter as `execution/_Scripts/validate_dependencies.py` (Python, no external deps) with:
  - single-file mode (`validate_dependencies.py <Dependencies.csv>`),
  - batch scan mode (`validate_dependencies.py --scan execution/`),
  - text/json output, and deterministic exit codes (`0` pass, `1` validation failures, `2` tooling/input failures).
- 2026-02-24: Added linter coverage tests under `execution/_Scripts/tests/test_validate_dependencies.py` for valid, invalid, scan-mode, and missing-file behaviors.
- 2026-02-24: Kept non-preferred EXECUTION `DependencyType` handling configurable (`--execution-dependency-type-severity warning|error`) to preserve current compatibility while enabling strict policy when desired.
- 2026-02-24: Added script usage documentation and CI command examples in `execution/_Scripts/README.md`.

## Open Questions

- Four current deliverables use non-canonical `DependencyID` patterns (for example `DEP-0205-001`, `DEP-0604-A001`). Decide whether to:
  - normalize those registers to canonical `DEP-XX-YY-NNN`, or
  - formally codify an expanded legacy-compatible ID format in `docs/SPEC.md`.

## Notes

- Evidence:
  - `python3 -m unittest discover -s execution/_Scripts/tests -p 'test_*.py'` -> `OK (6 tests)`
  - `python3 execution/_Scripts/validate_dependencies.py execution/PKG-08_Optional_Integrity_Hardening/1_Working/DEL-08-02_Dependencies_Schema_Linter/Dependencies.csv --format json` -> PASS (`failFiles=0`, `errorFiles=0`)
  - `python3 execution/_Scripts/validate_dependencies.py --scan execution --format json` -> expected validation output with `filesScanned=36`, `passFiles=32`, `failFiles=4`, `errorFiles=0`, `totalErrors=43`
- Current fail set from workspace-wide scan:
  - `DEL-02-04_Multipane_Layout_Theme`
  - `DEL-02-05_Frontend_Workflow_Shell`
  - `DEL-03-06_Outbound_Network_Guardrails`
  - `DEL-06-04_Change_Management_Git_Hygiene`
