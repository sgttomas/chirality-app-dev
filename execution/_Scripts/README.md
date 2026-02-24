# Execution Scripts

Standalone validation and integrity tooling for the execution workspace.

## `references_hash_tool.py` (DEL-08-01)

Computes and verifies `ContentHash` fields for out-of-folder references in `_REFERENCES.md`.

### Commands

```bash
python3 execution/_Scripts/references_hash_tool.py compute <deliverable_or_references_path>
python3 execution/_Scripts/references_hash_tool.py verify <deliverable_or_references_path>
python3 execution/_Scripts/references_hash_tool.py recompute <deliverable_or_references_path>
```

### Output and Exit Codes

- `compute` / `recompute`
  - `0`: completed (file may or may not have changed)
  - `2`: invalid path or runtime error
- `verify`
  - `0`: verification passed (or bypass recorded with `--allow-bypass`)
  - `1`: verification failed
  - `2`: invalid path, missing bypass metadata, or runtime error

### Bypass Recording

Use only with explicit human approval:

```bash
python3 execution/_Scripts/references_hash_tool.py verify <path> \
  --allow-bypass --actor "<actor>" --reason "<reason>"
```

By default, bypass records append to deliverable-local `HASH_VERIFICATION_BYPASS.jsonl`.

## `validate_dependencies.py` (DEL-08-02)

Lints `Dependencies.csv` files against the v3.1 schema from `docs/SPEC.md` Section 6.

### Commands

```bash
python3 execution/_Scripts/validate_dependencies.py <path/to/Dependencies.csv>
python3 execution/_Scripts/validate_dependencies.py --scan execution/
```

### Output and Exit Codes

- `0`: all files pass (warnings allowed)
- `1`: one or more schema validation failures
- `2`: unreadable/missing inputs or tool failure

### JSON Output

Add `--format json` for machine-readable CI consumption.

## Suggested CI Snippets

```bash
# Workspace-wide dependency schema lint
python3 execution/_Scripts/validate_dependencies.py --scan execution/ --format json

# Pre-run reference integrity check for a target deliverable
python3 execution/_Scripts/references_hash_tool.py verify \
  execution/PKG-08_Optional_Integrity_Hardening/1_Working/DEL-08-01_References_Content_Hashes \
  --format json
```
