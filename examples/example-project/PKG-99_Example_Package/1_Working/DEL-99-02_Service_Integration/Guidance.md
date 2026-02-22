# Guidance: DEL-99-02 — Service Integration

## Design Rationale

### G1 — Client Architecture

Use a single HTTP client instance with connection pooling rather than per-request client creation. This reduces connection setup overhead and enables connection reuse.

### G2 — Error Classification

Classify errors into transient (retryable) and permanent (non-retryable) categories at the HTTP layer, before business logic processes responses.

### G3 — Schema Validation

Validate responses at the boundary (immediately after HTTP response) rather than deep in business logic. This catches API contract drift early.
