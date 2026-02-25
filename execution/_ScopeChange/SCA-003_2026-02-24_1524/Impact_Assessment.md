# Impact Assessment — SCA-003

## Summary

SCA-003 introduces one new UI scope item and one new UI deliverable, and amends the runtime key-provisioning policy contract from env-only to dual-source precedence (`ENV+UI`). The change is additive with one contract amendment and no ID reuse.

## Impact Table

| Action | Directly affected files | Downstream impact | Risk |
|---|---|---|---|
| Add `SOW-050` | Decomposition amendment sections + telemetry | Adds explicit UI key-entry scope in PKG-02 | Low |
| Add `DEL-02-06` | Decomposition amendment sections + new deliverable folder metadata | New UI implementation unit enters lifecycle at `OPEN` | Low |
| Modify `DEL-03-05` contract (`ENV_ONLY -> ENV+UI`) | Decomposition OI-001 wording, DEL-03-05 `_CONTEXT.md`, DEL-03-05 dependency artifacts | Runtime provider contract must accept UI-provided key precedence with env fallback | Medium |
| Modify OI-001 resolution wording | Decomposition open-issues + change-log/amendment sections; policy references | Requires policy wording alignment in governance docs (`docs/SPEC.md`, `docs/PLAN.md`) | Medium |

## Dependency / Estimate / Schedule Impact

- Dependency orphan risk: LOW (`0`) — no removals; one new deliverable interface edge added (`DEL-02-06 -> DEL-03-05`).
- Estimate/schedule staleness risk: LOW-MEDIUM — deliverable set increases by one; future estimate/schedule snapshots should include DEL-02-06.
- Execution sequencing impact: LOW — new dependency is interface-only (non-blocker subset under current coordination policy).

## Recommended Downstream Reruns

1. PREPARATION (executed in this cycle) for `DEL-02-06` scaffold.
2. DEPENDENCIES extraction on `DEL-02-06` (new register) and re-extraction on `DEL-03-05` (contract amendment).
3. Optional: next closure audit cycle to include new deliverable in full-graph health checks.
