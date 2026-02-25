# Execution Path Blocker Analysis

Rule: `EXECUTION + DELIVERABLE + ACTIVE + UPSTREAM + (PREREQUISITE|CONSTRAINT) + non-ASSUMPTION`

## Summary

| View | Nodes | Edges | Nontrivial SCCs | Largest SCC |
|---|---:|---:|---:|---:|
| All subset | 36 | 46 | 0 | 0 |
| Core subset (excluding PKG-08) | 29 | 42 | 0 | 0 |

## Tiered order (all subset)

- Tier 1: DEL-01-02, DEL-01-03, DEL-02-01, DEL-02-02, DEL-02-04, DEL-05-01, DEL-06-01, DEL-06-03, DEL-06-04, DEL-06-05, DEL-07-02, DEL-08-01, DEL-08-03, DEL-08-04, DEL-08-05, DEL-08-06
- Tier 2: DEL-03-07, DEL-06-02, DEL-08-02
- Tier 3: DEL-01-01, DEL-02-05, DEL-03-01, DEL-05-02, DEL-07-03
- Tier 4: DEL-03-03, DEL-05-03, DEL-05-04
- Tier 5: DEL-03-05, DEL-08-07
- Tier 6: DEL-03-06
- Tier 7: DEL-03-02
- Tier 8: DEL-02-03, DEL-03-04, DEL-04-01
- Tier 9: DEL-04-02, DEL-07-01

## Pre-tier frontend gate (SCA-001)

- Required at `IN_PROGRESS`: DEL-01-03, DEL-03-07, DEL-02-05, DEL-07-03
- Met: DEL-01-03, DEL-03-07, DEL-02-05, DEL-07-03
- Pending: none

## Data quality caveats

- None.

## Sequencing policy

- Full dependency graph closure remains audit truth.
- Blocker-subset analysis remains execution sequencing truth.
