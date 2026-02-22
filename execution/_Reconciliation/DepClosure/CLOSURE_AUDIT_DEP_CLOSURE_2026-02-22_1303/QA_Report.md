# QA Report -- AUDIT_DEP_CLOSURE

## Inputs and Coverage

- Execution root: `/Users/ryan/ai-env/projects/chirality-app-dev/execution`
- Scope: `ALL`
- Deliverables discovered: `36`
- Dependencies.csv exists: `36`
- Dependencies.csv readable: `36`
- Schema-valid registers: `36`

## Data Quality Checks

- Orphan targets: `0`
- Misplaced TargetDeliverableID fields: `0`
- Long-form ID normalization hits (from/target): `0` / `0`
- Isolated deliverables: `0`

## Constraints and Limits

- Cycle sampling cap: `MAX_CYCLES=10000` (sample output bounded in `Evidence/cycles_sample.csv`).
- Hub threshold: `20`.

## QA Verdict

- Run status: `BLOCKER`
- No schema/readability failures detected across in-scope deliverables.
