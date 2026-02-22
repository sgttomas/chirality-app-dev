# Context: DEL-03-07

**Name:** Harness API Baseline in Frontend Runtime
**Package:** PKG-03 Harness Runtime Core
**Type:** BACKEND_FEATURE_SLICE
**Context Envelope:** L

## Scope Coverage
- SOW-045: Implement baseline harness API routes in `frontend/` for session create/boot/list/get/delete and turn execution with typed failure contracts.

## Objectives
- OBJ-002: Harness runtime correctness
- OBJ-008: Local frontend runtime baseline exists and is executable from this repository only

## Description
Implement baseline `/api/harness/session/*` and `/api/harness/turn` route surfaces with typed failure contracts. Route handlers compile and pass baseline route-contract tests. All API routes are implemented in the local `frontend/` workspace.

## Anticipated Artifacts
- CODE, TEST

## Decomposition Reference
- **Decomposition:** `execution/_Decomposition/ChiralityApp_SoftwareDecomposition_2026-02-21_G7-APPROVED.md`
- **Deliverable ID:** DEL-03-07
- **Amendment:** Scope Amendment A1 (SCA-001, 2026-02-22)
