# Propagation Plan — SCA-003

## Approved Decomposition Propagation

- Apply decomposition Change Log entry for SCA-003.
- Add Scope Amendment A3 section with:
  - `SOW-050` (`IN`)
  - `DEL-02-06` definition
  - OI-001 amendment (`ENV_ONLY -> ENV+UI`)
- Update telemetry counts (`ScopeItemCount`, `DeliverableCount`, active ContextEnvelope mix).
- Update Open Issues OI-001 resolution text and related stable-ID references.

## Filesystem Propagation

- MODIFY `DEL-03-05` `_CONTEXT.md` description to reflect `ENV+UI` contract.
- ADD `DEL-02-06` folder scaffold under:
  - `execution/PKG-02_Desktop_UI_Workflow/1_Working/DEL-02-06_Settings_API_Key_Entry_UI/`
- Create metadata files for DEL-02-06:
  - `_CONTEXT.md`, `_STATUS.md`, `_REFERENCES.md`, `_SEMANTIC.md`, `MEMORY.md`
- Run DEPENDENCIES extraction outputs:
  - create `DEL-02-06/Dependencies.csv` + `_DEPENDENCIES.md`
  - refresh `DEL-03-05/Dependencies.csv` + `_DEPENDENCIES.md`

## Governance Alignment

- Update `docs/SPEC.md` provider policy line for `ENV+UI` contract.
- Update `docs/PLAN.md` policy-ruling section for SCA-003 amendment.

## Downstream Advisory

1. Run `4_DOCUMENTS` for `DEL-02-06` to move lifecycle `OPEN -> INITIALIZED`.
2. Schedule implementation pass for `DEL-02-06` and follow-on DEL-03-05 runtime integration updates.
3. Include DEL-02-06 in next closure audit snapshot and blocker-front scan.
