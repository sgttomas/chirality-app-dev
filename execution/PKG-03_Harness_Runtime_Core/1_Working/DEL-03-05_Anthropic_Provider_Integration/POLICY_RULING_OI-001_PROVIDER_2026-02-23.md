# Policy Ruling Record — DEL-03-05 (2026-02-23)

## Scope

- Deliverable: `DEL-03-05` — Anthropic Provider Integration & Key Provisioning Contract
- Ruling date: 2026-02-23
- Ruling actor: Human
- Session intent: documentation and scope closure only (implementation deferred)

## Rulings Applied

1. `OI-001` resolution: `ENV_ONLY`
- Key provisioning baseline is environment-variable only for current scope.
- Required key source: `ANTHROPIC_API_KEY`.
- Compatibility alias may be supported during migration (`CHIRALITY_ANTHROPIC_API_KEY`) but does not replace the primary contract.
- No keychain, `safeStorage`, or app-settings persistence is in current DEL-03-05 scope unless explicitly re-ruled.

2. Provider implementation ruling: `ADOPT_SDK_NOW`
- DEL-03-05 acceptance path is the official Anthropic SDK integration (`@anthropic-ai/sdk`).
- Direct HTTP provider paths are allowed only as non-authoritative interim experiments and are not sufficient for DEL-03-05 completion.

3. Execution mode for this cycle
- Documentation/scope preparation only.
- No additional implementation is authorized in this ruling pass.

## Required Follow-Through (Subsequent Sessions)

1. Implement SDK-backed provider runtime path for DEL-03-05.
2. Pin SDK version in `frontend/package.json` and document update lifecycle.
3. Align test coverage to SDK path and env-only key contract.
4. Re-run DEL-03-05 dependency + reconciliation fan-in and update checking-readiness evidence.

## References

- `execution/_Coordination/NEXT_INSTANCE_STATE.md`
- `execution/PKG-03_Harness_Runtime_Core/1_Working/DEL-03-05_Anthropic_Provider_Integration/Specification.md`
- `execution/PKG-03_Harness_Runtime_Core/1_Working/DEL-03-05_Anthropic_Provider_Integration/Procedure.md`
