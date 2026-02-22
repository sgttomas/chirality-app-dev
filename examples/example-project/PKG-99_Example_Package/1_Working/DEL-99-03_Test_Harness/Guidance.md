# Guidance: DEL-99-03 — Test Harness

## Design Rationale

### G1 — Self-Contained Fixtures

Test fixtures should be self-contained and require no external setup, network access, or database connections. This ensures tests can run in CI environments and offline development setups.

### G2 — Positive and Negative Cases

Include both positive cases (conformant structures that should pass) and negative cases (deliberately non-conformant structures that should be detected and reported).
