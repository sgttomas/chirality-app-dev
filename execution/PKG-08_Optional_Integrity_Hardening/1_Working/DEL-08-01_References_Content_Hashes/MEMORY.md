# Working Memory — DEL-08-01

*This file is shared working memory for WORKING_ITEMS and TASK agents operating on this deliverable.*

## Key Decisions

- 2026-02-24: Implemented standalone hash tooling as `execution/_Scripts/references_hash_tool.py` with three CLI modes:
  - `compute` (populate/update `ContentHash` fields),
  - `verify` (pre-pipeline integrity check),
  - `recompute` (explicit refresh alias for intentional updates).
- 2026-02-24: Chosen `_REFERENCES.md` inline storage model for hashes (no companion hash file). `ContentHash` values are written as nested bullet fields under out-of-folder references.
- 2026-02-24: Implemented explicit bypass audit trail in deliverable-local `HASH_VERIFICATION_BYPASS.jsonl` with required fields: timestamp, actor, reason, failed references.
- 2026-02-24: Integrated control-plane expectations into agent instructions:
  - `agents/AGENT_PREPARATION.md` now instructs hash computation when script is available.
  - `agents/AGENT_ORCHESTRATOR.md` now defines fail-closed pre-run verification + human-approved bypass flow.
- 2026-02-24: Updated canonical schema notes in `docs/SPEC.md` Section 7 to include optional `ContentHash` field semantics.

## Open Questions

- Should package-reference shorthand paths inside `_REFERENCES.md` (for example `PKG-XX_.../0_References/`) be interpreted relative to execution root by convention, or remain informational-only unless expressed as explicit relative/absolute file paths?

## Notes

- Evidence:
  - `python3 -m unittest discover -s execution/_Scripts/tests -p 'test_*.py'` -> `OK (6 tests)`
  - `python3 execution/_Scripts/references_hash_tool.py compute execution/PKG-08_Optional_Integrity_Hardening/1_Working/DEL-08-01_References_Content_Hashes --format json` -> `fileModified=true`, `hashesComputed=1`
  - `python3 execution/_Scripts/references_hash_tool.py verify execution/PKG-08_Optional_Integrity_Hardening/1_Working/DEL-08-01_References_Content_Hashes --format json` -> `verificationStatus=PASS`
- Deliverable-local `_REFERENCES.md` now includes `ContentHash` for the decomposition document reference.
