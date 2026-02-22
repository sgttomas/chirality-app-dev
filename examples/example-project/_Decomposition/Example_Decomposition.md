# Example Project — Software Decomposition (Synthetic Fixture)

**Status:** G7-APPROVED (synthetic)
**Date:** 2026-02-22
**Variant:** SOFTWARE_DECOMP

## Structured Outline

### SOW-001 — Widget configuration subsystem
Configure and validate widget parameters for the example application.

### SOW-002 — Service integration layer
Implement service integration with external APIs.

### SOW-003 — Test harness scaffolding
Build automated test harness for regression and conformance testing.

## Decomposition Ledger

| Scope Item | Package | Deliverable | Notes |
|------------|---------|-------------|-------|
| SOW-001 | PKG-99 | DEL-99-01 | Widget Configuration |
| SOW-002 | PKG-99 | DEL-99-02 | Service Integration |
| SOW-003 | PKG-99 | DEL-99-03 | Test Harness |

## Packages

### PKG-99 — Example Package

| Deliverable | Title | Type | Responsibility |
|-------------|-------|------|----------------|
| DEL-99-01 | Widget Configuration | BACKEND_FEATURE_SLICE | Developer |
| DEL-99-02 | Service Integration | BACKEND_FEATURE_SLICE | Developer |
| DEL-99-03 | Test Harness | TEST_SUITE | QA |

## Objectives

| Objective | Description | Supporting Deliverables |
|-----------|-------------|----------------------|
| OBJ-001 | Demonstrate conformant execution root structure | DEL-99-01, DEL-99-02, DEL-99-03 |

## Vocabulary Map

| Term | Canonical | Synonyms |
|------|-----------|----------|
| Widget | Widget | component, control |
| Service | Service | API, endpoint |

## Coverage & Telemetry

- Scope items: 3
- Packages: 1
- Deliverables: 3
- Objectives: 1
- Gaps: 0
