# QA Report

## Coverage

- Deliverables discovered: 36
- CSV exists: 36
- CSV readable: 36
- Schema valid: 36
- Schema coverage: 100.0%

## Data quality caveats

- `DEL-01-01`: Status/Notes field shift observed (DEP-01-01-010, DEP-01-01-011)

## Limits

- Analysis is read-only and does not rewrite malformed dependency rows.
- Blocker-subset advisory depends on declared dependency metadata quality.
