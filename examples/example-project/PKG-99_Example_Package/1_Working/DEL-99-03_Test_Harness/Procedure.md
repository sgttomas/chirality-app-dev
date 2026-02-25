# Procedure: DEL-99-03 — Test Harness

## Execution Steps

1. **Define test inventory** — list all SPEC Section 12 checks to implement.
2. **Create positive fixtures** — example execution roots that pass all checks.
3. **Create negative fixtures** — deliberately non-conformant structures for each check.
4. **Implement test runner** — script that walks fixtures and runs checks.
5. **Implement JSON reporter** — machine-readable output format.
6. **Validate fixtures** — run test harness against its own fixtures; verify expected results.
