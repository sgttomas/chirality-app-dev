# Decision Log: Decomposition Coverage Audit (Post-SCA-001)

**Run ID:** COV_POST_SCA001_FULL_2026-02-22
**Date:** 2026-02-22

---

## Decisions Made During Audit

| # | Decision | Rationale |
|---|---|---|
| 1 | Treat the pre-amendment telemetry section (lines 315-333) as the baseline and the Telemetry Delta (lines 423-426) as the authoritative post-amendment counts, rather than requiring the pre-amendment section to be updated in-place. | The decomposition uses an append-only amendment model (SCA-001 section). Requiring in-place updates to the base telemetry would violate the stable-document principle. The delta section is sufficient for machine-readability. |
| 2 | Count context envelope totals post-amendment as S:5 M:22 L:9 XL:0, even though the base telemetry section only declares pre-amendment counts (S:5 M:21 L:6 XL:0). | SCA-001 adds 3L (DEL-01-03, DEL-02-05, DEL-03-07) and 1M (DEL-07-03). These are stated in the amendment table (line 400-405). The delta is consistent. |
| 3 | Accept that OUT-scope items (SOW-039..043) map to DEL-06-05 as a "guardrail deliverable" rather than requiring no mapping at all. | The decomposition explicitly assigns OUT items to a governance/guardrail deliverable. This is a design choice documented in the scope ledger and is structurally consistent. |
| 4 | Do not flag the gap between SOW-043 and SOW-044 as an ID format issue. | The gap is the boundary between the original SSOW and the SCA-001 amendment. ID sequences are contiguous within each range. The decomposition does not require globally contiguous SOW numbering. |

## Escalations

None. No issues requiring human decision were discovered.
