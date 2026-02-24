# Harness Validation Suite

This suite validates the harness runtime contract for session lifecycle, turn execution, SSE streaming, options fallback resolution, subagent governance gates, and attachment behavior.

## Scripts

- `npm run harness:validate:section8`
  - Executes `frontend/scripts/validate-harness-section8.mjs`.
  - Emits machine-readable lines:
    - `HARNESS_VALIDATION_SUMMARY_PATH=<path>`
    - `HARNESS_VALIDATION_STATUS=pass|fail`
- `npm run harness:validate:premerge`
  - Executes the section8 validator and enforces required test IDs.
  - Copies the summary to `frontend/artifacts/harness/section8/latest/summary.json`.

## Prerequisites

- Node.js `>=20`
- Frontend dependencies installed in `frontend/`
- Harness API reachable at `HARNESS_BASE_URL` (defaults to `http://127.0.0.1:3000`)
- Valid working root configured via `HARNESS_PROJECT_ROOT` (recommended: `examples/example-project`)

## Local Run

From `frontend/`:

```bash
npm run harness:validate:section8
npm run harness:validate:premerge
```

Optional environment overrides:

```bash
HARNESS_BASE_URL=http://127.0.0.1:3000 \
HARNESS_PROJECT_ROOT=/absolute/path/to/project-root \
npm run harness:validate:premerge
```

## CI Integration

Run in a headless step after the harness API surface is available:

```bash
cd frontend
npm ci
HARNESS_BASE_URL=http://127.0.0.1:3000 \
HARNESS_PROJECT_ROOT=$GITHUB_WORKSPACE/examples/example-project \
npm run harness:validate:premerge
```

Fail the pipeline when command exit code is non-zero.

## Artifacts

- Live run outputs: `${TMPDIR:-/tmp}/chirality-harness-validation/latest/`
- Stable premerge summary: `frontend/artifacts/harness/section8/latest/summary.json`
- Integrity summary (instruction-root): `frontend/artifacts/harness/instruction-root-integrity/latest/summary.json`

## Repeatability Check

Run `npm run harness:validate:premerge` twice against the same harness state and confirm:

- both runs exit `0`
- both summaries report `"status": "pass"`
- required test IDs are unchanged
