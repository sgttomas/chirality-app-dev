# Working Memory — DEL-06-04

*This file is shared working memory for WORKING_ITEMS and TASK agents operating on this deliverable.*

## Key Decisions

- 2026-02-24: Use a constraints-based publication artifact instead of prescribing one branching model. Output path: `docs/CHANGE_PUBLICATION_GUIDANCE_CONSTRAINTS.md`.
- 2026-02-24: Enforce approval-SHA binding directly in CHANGE instructions by requiring `SHA=<approved_sha>` in approval tokens and re-checking HEAD before execution.
- 2026-02-24: Treat `_Change/` outputs as immutable snapshots with `_LATEST.md` as the only mutable pointer file.

## Open Questions

- Should this deliverable also codify optional branch naming guidance, or leave branch naming fully project-instance configurable?
- Should CHANGE require a staleness triage block on every session, or only when governed inputs changed?

## Notes

- Files updated this pass:
  - `agents/AGENT_CHANGE.md`
  - `docs/CHANGE_PUBLICATION_GUIDANCE_CONSTRAINTS.md`
  - `Datasheet.md` (publication flow + change record format resolved from TBD)
  - `Specification.md` (required artifact path pinned)
  - `Procedure.md` (records path pinned)
  - `_STATUS.md` (this deliverable)
