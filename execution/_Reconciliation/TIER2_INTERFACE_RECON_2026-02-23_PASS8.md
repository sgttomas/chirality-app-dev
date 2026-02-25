# Tier 2 Interface Reconciliation — 2026-02-23 (Pass 8 Approval-Evidence Alignment)

## Scope

- Reconciliation type: cross-deliverable interface coherence check for lifecycle human-gate approval evidence enforcement
- Tier scope: `DEL-02-05` / `DEL-05-03` / `DEL-05-04`
- Inputs:
  - `frontend/src/lib/lifecycle/transition.ts`
  - `frontend/src/lib/workspace/deliverable-api.ts`
  - `frontend/src/app/pipeline/pipeline-client.tsx`
  - `frontend/src/__tests__/lib/lifecycle-status.test.ts`
  - `frontend/src/__tests__/api/working-root/deliverable-contracts.test.ts`
  - `frontend/src/__tests__/lib/workspace-deliverable-api.test.ts`
  - `execution/_Coordination/_COORDINATION.md`

## Interface Set Reviewed

1. `DEL-05-03 -> DEL-02-05` (lifecycle contract requirements mapped into PIPELINE transition UX)
2. `DEL-05-03 -> DEL-05-04` (lifecycle transition semantics exposed through shared deliverable API helper surface)
3. `DEL-05-04 -> DEL-02-05` (client helper + UI submit constraints for human-gate transitions)

## Findings

| Interface | Expected contract | Observed posture | Result |
|---|---|---|---|
| DEL-05-03 -> DEL-02-05 | Human-gated lifecycle transitions (`CHECKING`, `ISSUED`) must carry approval evidence and fail closed when missing | Backend transition module now rejects missing/malformed `approvalSha` with explicit typed errors; PIPELINE requires `approvalSha` on matching targets | SATISFIED |
| DEL-05-03 -> DEL-05-04 | Transition evidence requirements should be discoverable from shared client helpers to avoid duplicated filtering logic | Shared helper `requiresApprovalShaForTarget` added and consumed by PIPELINE | SATISFIED |
| DEL-05-04 -> DEL-02-05 | UI should prevent unauthorized actor/evidence combinations before route submit | PIPELINE now forces `HUMAN` actor for human-gate targets and blocks submit without `approvalSha` | SATISFIED |

## Contradictions and Actions

- No new cross-deliverable contradictions detected in this pass.
- Carry-forward actions:
  - Maintain helper-level reuse if additional lifecycle transition surfaces are introduced.
  - Keep issuance/checking evidence expectations aligned with deliverable docs and future staleness tooling.

## Reconciliation Disposition

- Tier 2 interface posture for approval-evidence enforcement is coherent across backend contract and PIPELINE consumer layers.
- Regression coverage confirms fail-closed behavior and preserves typed error observability.
