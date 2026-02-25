# Specification: DEL-99-03 — Test Harness

## Requirements

### REQ-01 (MUST)

The test harness MUST run all SPEC Section 12 conformance checks against a target execution root.

### REQ-02 (MUST)

The test harness MUST exit with status code 0 when all checks pass and non-zero when any check fails.

### REQ-03 (MUST)

The test harness MUST report results in machine-readable JSON format.

### REQ-04 (SHOULD)

The test harness SHOULD also produce a human-readable summary on stdout.
