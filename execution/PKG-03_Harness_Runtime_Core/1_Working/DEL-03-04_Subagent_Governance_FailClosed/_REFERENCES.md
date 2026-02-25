# References — DEL-03-04

## Decomposition

- [Decomposition Document](../../../_Decomposition/ChiralityApp_SoftwareDecomposition_2026-02-21_G7-APPROVED.md)

## Package References

*See `PKG-03_Harness_Runtime_Core/0_References/` for package-level reference materials.*

## Deliverable-Specific References

- `docs/SPEC.md` Section 9.7 — runtime metadata contract and fail-closed delegation rule.
- `docs/SPEC.md` Section 9.8 — governance metadata visibility and runtime-authoritative enforcement boundary.
- `frontend/src/lib/harness/subagent-governance.ts` — DEL-03-04 governance gate implementation.
- `frontend/src/lib/harness/agent-instruction.ts` — shared instruction parsing and AGENT_TYPE / AGENT_CLASS extraction support for registry validation.
- `frontend/src/app/api/harness/turn/route.ts` — turn-path integration of governance evaluation.
- `frontend/src/__tests__/lib/harness-subagent-governance.test.ts` — unit-level gate and registry validation coverage.
- `frontend/src/__tests__/api/harness/routes.test.ts` — integration coverage for fail-closed continuation, no-UI-bypass posture, and delegated-subagent propagation.
- `execution/_Coordination/TIER8_CONTROL_LOOP_2026-02-24_PASS1.md` — pass-level control-loop evidence.
- `execution/_Reconciliation/TIER8_INTERFACE_RECON_2026-02-24_PASS1.md` — pass-level interface reconciliation evidence.
