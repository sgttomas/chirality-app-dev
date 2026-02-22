# Decomposition Coverage Report (Post-SCA-001)

**Run ID:** COV_POST_SCA001_FULL_2026-02-22
**Date:** 2026-02-22
**Decomposition:** ChiralityApp_SoftwareDecomposition_2026-02-21_G7-APPROVED (+ SCA-001)
**Scope:** FULL audit -- all packages, deliverables, scope items, objectives

---

## 1. Forward Coverage (Decomposition -> Execution Tree)

**Check:** Every deliverable declared in the decomposition has a corresponding folder in the execution tree.

### PKG-01 -- Build & Packaging (3 deliverables)

| DeliverableID | Decomp Name | Folder Exists | Folder Path |
|---|---|---|---|
| DEL-01-01 | macOS 15+ Apple Silicon Build Baseline | YES | `PKG-01_Build_And_Packaging/1_Working/DEL-01-01_macOS_Build_Baseline/` |
| DEL-01-02 | Unsigned DMG Packaging Workflow | YES | `PKG-01_Build_And_Packaging/1_Working/DEL-01-02_Unsigned_DMG_Packaging/` |
| DEL-01-03 | Frontend Workspace Bootstrap & Packaging Baseline | YES | `PKG-01_Build_And_Packaging/1_Working/DEL-01-03_Frontend_Workspace_Bootstrap/` |

### PKG-02 -- Desktop UI Workflow (5 deliverables)

| DeliverableID | Decomp Name | Folder Exists | Folder Path |
|---|---|---|---|
| DEL-02-01 | FileTree Refresh & External-Change Detection | YES | `PKG-02_Desktop_UI_Workflow/1_Working/DEL-02-01_FileTree_Refresh/` |
| DEL-02-02 | Portal->Pipeline Navigation & Deliverable Key Semantics | YES | `PKG-02_Desktop_UI_Workflow/1_Working/DEL-02-02_Portal_Pipeline_Navigation/` |
| DEL-02-03 | Operator Toolkit Panel & Local Presets | YES | `PKG-02_Desktop_UI_Workflow/1_Working/DEL-02-03_Operator_Toolkit_Panel/` |
| DEL-02-04 | Multi-pane Layout + Theme Hardening | YES | `PKG-02_Desktop_UI_Workflow/1_Working/DEL-02-04_Multipane_Layout_Theme/` |
| DEL-02-05 | Frontend Workflow Shell Baseline | YES | `PKG-02_Desktop_UI_Workflow/1_Working/DEL-02-05_Frontend_Workflow_Shell/` |

### PKG-03 -- Harness Runtime Core (7 deliverables)

| DeliverableID | Decomp Name | Folder Exists | Folder Path |
|---|---|---|---|
| DEL-03-01 | Working Root Binding & Session Boot | YES | `PKG-03_Harness_Runtime_Core/1_Working/DEL-03-01_Working_Root_Session_Boot/` |
| DEL-03-02 | Turn Execution API + SSE Streaming | YES | `PKG-03_Harness_Runtime_Core/1_Working/DEL-03-02_Turn_Execution_SSE_Streaming/` |
| DEL-03-03 | Turn Options Mapping & Fallback Chains | YES | `PKG-03_Harness_Runtime_Core/1_Working/DEL-03-03_Turn_Options_Fallback_Chains/` |
| DEL-03-04 | Subagent Governance Fail-Closed Enforcement | YES | `PKG-03_Harness_Runtime_Core/1_Working/DEL-03-04_Subagent_Governance_FailClosed/` |
| DEL-03-05 | Anthropic Provider Integration & Key Provisioning Contract | YES | `PKG-03_Harness_Runtime_Core/1_Working/DEL-03-05_Anthropic_Provider_Integration/` |
| DEL-03-06 | Outbound Network Guardrails (Anthropic-only) + Verification | YES | `PKG-03_Harness_Runtime_Core/1_Working/DEL-03-06_Outbound_Network_Guardrails/` |
| DEL-03-07 | Harness API Baseline in Frontend Runtime | YES | `PKG-03_Harness_Runtime_Core/1_Working/DEL-03-07_Harness_API_Baseline/` |

### PKG-04 -- Attachments & Multimodal Turns (2 deliverables)

| DeliverableID | Decomp Name | Folder Exists | Folder Path |
|---|---|---|---|
| DEL-04-01 | Server-side Attachment Resolver + Prompt Mode Selection | YES | `PKG-04_Attachments_Multimodal/1_Working/DEL-04-01_Attachment_Resolver_PromptMode/` |
| DEL-04-02 | UI Attachment Pipeline (Picker, Preview, Rollback, Rehydration) | YES | `PKG-04_Attachments_Multimodal/1_Working/DEL-04-02_UI_Attachment_Pipeline/` |

### PKG-05 -- Filesystem Execution Model (4 deliverables)

| DeliverableID | Decomp Name | Folder Exists | Folder Path |
|---|---|---|---|
| DEL-05-01 | Instruction Root Bundling & Runtime Access | YES | `PKG-05_Filesystem_Execution_Model/1_Working/DEL-05-01_Instruction_Root_Bundling/` |
| DEL-05-02 | Execution Root Scaffolding + Layout Conformance | YES | `PKG-05_Filesystem_Execution_Model/1_Working/DEL-05-02_Execution_Root_Scaffolding/` |
| DEL-05-03 | Lifecycle State Handling (`_STATUS.md` canonical) | YES | `PKG-05_Filesystem_Execution_Model/1_Working/DEL-05-03_Lifecycle_State_Handling/` |
| DEL-05-04 | Dependency Tracking File Contract (v3.1) | YES | `PKG-05_Filesystem_Execution_Model/1_Working/DEL-05-04_Dependency_Tracking_Contract/` |

### PKG-06 -- Agent Suite & Governance (5 deliverables)

| DeliverableID | Decomp Name | Folder Exists | Folder Path |
|---|---|---|---|
| DEL-06-01 | Agent Instruction Suite Structural Conformance | YES | `PKG-06_Agent_Suite_Governance/1_Working/DEL-06-01_Agent_Instruction_Conformance/` |
| DEL-06-02 | Local Deliverable Workflow Agents | YES | `PKG-06_Agent_Suite_Governance/1_Working/DEL-06-02_Local_Deliverable_Workflow_Agents/` |
| DEL-06-03 | Cross-deliverable Workflow Support | YES | `PKG-06_Agent_Suite_Governance/1_Working/DEL-06-03_Cross_Deliverable_Workflows/` |
| DEL-06-04 | Change Management & Git Hygiene Support | YES | `PKG-06_Agent_Suite_Governance/1_Working/DEL-06-04_Change_Management_Git_Hygiene/` |
| DEL-06-05 | Governance Coherence + Guardrails (OUT boundaries) | YES | `PKG-06_Agent_Suite_Governance/1_Working/DEL-06-05_Governance_Coherence_Guardrails/` |

### PKG-07 -- Validation & Example Assets (3 deliverables)

| DeliverableID | Decomp Name | Folder Exists | Folder Path |
|---|---|---|---|
| DEL-07-01 | Harness Validation Suite (local + CI-ready posture) | YES | `PKG-07_Validation_Example_Assets/1_Working/DEL-07-01_Harness_Validation_Suite/` |
| DEL-07-02 | Example Execution Roots + Conformance Fixtures | YES | `PKG-07_Validation_Example_Assets/1_Working/DEL-07-02_Example_Execution_Roots/` |
| DEL-07-03 | Frontend Validation & Runbook Baseline | YES | `PKG-07_Validation_Example_Assets/1_Working/DEL-07-03_Frontend_Validation_Runbook/` |

### PKG-08 -- Optional Integrity Hardening (7 deliverables)

| DeliverableID | Decomp Name | Folder Exists | Folder Path |
|---|---|---|---|
| DEL-08-01 | `_REFERENCES.md` Content Hashes + Verification | YES | `PKG-08_Optional_Integrity_Hardening/1_Working/DEL-08-01_References_Content_Hashes/` |
| DEL-08-02 | Dependencies.csv v3.1 Schema Linter | YES | `PKG-08_Optional_Integrity_Hardening/1_Working/DEL-08-02_Dependencies_Schema_Linter/` |
| DEL-08-03 | Execution Root Folder Structure Validator | YES | `PKG-08_Optional_Integrity_Hardening/1_Working/DEL-08-03_Execution_Root_Validator/` |
| DEL-08-04 | On-demand Dependency Graph Generator | YES | `PKG-08_Optional_Integrity_Hardening/1_Working/DEL-08-04_Dependency_Graph_Generator/` |
| DEL-08-05 | Deliverable-level Lock Mechanism | YES | `PKG-08_Optional_Integrity_Hardening/1_Working/DEL-08-05_Deliverable_Lock_Mechanism/` |
| DEL-08-06 | Unified Pipeline Run Record Persistence | YES | `PKG-08_Optional_Integrity_Hardening/1_Working/DEL-08-06_Unified_Run_Record_Persistence/` |
| DEL-08-07 | Staleness Propagation + Triage Tooling | YES | `PKG-08_Optional_Integrity_Hardening/1_Working/DEL-08-07_Staleness_Propagation_Triage/` |

**FORWARD COVERAGE RESULT: 36/36 deliverables have corresponding execution folders. PASS.**

---

## 2. Reverse Coverage (Execution Tree -> Decomposition)

**Check:** Every deliverable folder in the execution tree has a corresponding entry in the decomposition.

Execution tree deliverable folders found: 36
Decomposition deliverable entries: 36

| Folder ID | In Decomposition |
|---|---|
| DEL-01-01 | YES (PKG-01, line 180) |
| DEL-01-02 | YES (PKG-01, line 181) |
| DEL-01-03 | YES (SCA-001 amendment, line 402) |
| DEL-02-01 | YES (PKG-02, line 187) |
| DEL-02-02 | YES (PKG-02, line 188) |
| DEL-02-03 | YES (PKG-02, line 189) |
| DEL-02-04 | YES (PKG-02, line 190) |
| DEL-02-05 | YES (SCA-001 amendment, line 403) |
| DEL-03-01 | YES (PKG-03, line 196) |
| DEL-03-02 | YES (PKG-03, line 197) |
| DEL-03-03 | YES (PKG-03, line 198) |
| DEL-03-04 | YES (PKG-03, line 199) |
| DEL-03-05 | YES (PKG-03, line 200) |
| DEL-03-06 | YES (PKG-03, line 201) |
| DEL-03-07 | YES (SCA-001 amendment, line 404) |
| DEL-04-01 | YES (PKG-04, line 207) |
| DEL-04-02 | YES (PKG-04, line 208) |
| DEL-05-01 | YES (PKG-05, line 214) |
| DEL-05-02 | YES (PKG-05, line 215) |
| DEL-05-03 | YES (PKG-05, line 216) |
| DEL-05-04 | YES (PKG-05, line 217) |
| DEL-06-01 | YES (PKG-06, line 223) |
| DEL-06-02 | YES (PKG-06, line 224) |
| DEL-06-03 | YES (PKG-06, line 225) |
| DEL-06-04 | YES (PKG-06, line 226) |
| DEL-06-05 | YES (PKG-06, line 227) |
| DEL-07-01 | YES (PKG-07, line 233) |
| DEL-07-02 | YES (PKG-07, line 234) |
| DEL-07-03 | YES (SCA-001 amendment, line 405) |
| DEL-08-01 | YES (PKG-08, line 240) |
| DEL-08-02 | YES (PKG-08, line 241) |
| DEL-08-03 | YES (PKG-08, line 242) |
| DEL-08-04 | YES (PKG-08, line 243) |
| DEL-08-05 | YES (PKG-08, line 244) |
| DEL-08-06 | YES (PKG-08, line 245) |
| DEL-08-07 | YES (PKG-08, line 246) |

**REVERSE COVERAGE RESULT: 36/36 execution folders map to decomposition entries. PASS.**

No orphan folders detected. No phantom deliverables.

---

## 3. Scope Ledger Consistency

**Check:** Every IN-scope item maps to at least one deliverable. Every OUT/TBD item is accounted for.

### IN-scope items (37 total, post-SCA-001)

| ScopeItemID | DeliverableID(s) | Mapped | Notes |
|---|---|---|---|
| SOW-001 | DEL-01-01 | YES | |
| SOW-002 | DEL-01-02 | YES | |
| SOW-003 | DEL-03-01 | YES | |
| SOW-004 | DEL-03-01, DEL-03-02 | YES | |
| SOW-005 | DEL-03-02 | YES | |
| SOW-006 | DEL-03-02, DEL-03-05, DEL-03-06 | YES | |
| SOW-007 | DEL-04-01 | YES | |
| SOW-008 | DEL-04-01 | YES | |
| SOW-009 | DEL-04-01 | YES | |
| SOW-010 | DEL-04-02 | YES | |
| SOW-011 | DEL-03-03 | YES | |
| SOW-012 | DEL-03-04 | YES | |
| SOW-013 | DEL-05-01 | YES | |
| SOW-014 | DEL-05-02 | YES | |
| SOW-015 | DEL-05-02 | YES | |
| SOW-016 | DEL-05-03 | YES | |
| SOW-017 | DEL-06-02 | YES | |
| SOW-018 | DEL-05-04 | YES | |
| SOW-019 | DEL-06-02 | YES | |
| SOW-020 | DEL-06-03 | YES | |
| SOW-021 | DEL-06-04 | YES | |
| SOW-022 | DEL-02-01 | YES | |
| SOW-023 | DEL-02-02 | YES | |
| SOW-024 | DEL-02-02 | YES | |
| SOW-025 | DEL-02-03 | YES | |
| SOW-026 | DEL-02-04 | YES | |
| SOW-027 | DEL-02-04 | YES | |
| SOW-028 | DEL-07-01 | YES | |
| SOW-029 | DEL-07-02 | YES | |
| SOW-030 | DEL-06-05 | YES | |
| SOW-031 | DEL-06-01 | YES | |
| SOW-044 | DEL-01-03 | YES | SCA-001 |
| SOW-045 | DEL-03-07 | YES | SCA-001 |
| SOW-046 | DEL-02-05 | YES | SCA-001 |
| SOW-047 | DEL-01-03 | YES | SCA-001 |
| SOW-048 | DEL-07-03 | YES | SCA-001 |
| SOW-049 | DEL-07-03 | YES | SCA-001 |

### OUT-scope items (5 total)

| ScopeItemID | DeliverableID(s) | Mapped | Notes |
|---|---|---|---|
| SOW-039 | DEL-06-05 | YES | Guardrail deliverable |
| SOW-040 | DEL-06-05 | YES | Guardrail deliverable |
| SOW-041 | DEL-06-05 | YES | Guardrail deliverable |
| SOW-042 | DEL-06-05 | YES | Guardrail deliverable |
| SOW-043 | DEL-06-05 | YES | Guardrail deliverable (Anthropic exception) |

### TBD-scope items (7 total)

| ScopeItemID | DeliverableID(s) | Mapped | Notes |
|---|---|---|---|
| SOW-032 | DEL-08-01 | YES | Optional hardening |
| SOW-033 | DEL-08-02 | YES | Optional hardening |
| SOW-034 | DEL-08-03 | YES | Optional hardening |
| SOW-035 | DEL-08-04 | YES | Optional hardening |
| SOW-036 | DEL-08-05 | YES | Optional hardening |
| SOW-037 | DEL-08-06 | YES | Optional hardening |
| SOW-038 | DEL-08-07 | YES | Optional hardening |

**SCOPE LEDGER RESULT: 49/49 scope items mapped to at least one deliverable. 0 unassigned. PASS.**

---

## 4. Objective Coverage

**Check:** Every objective maps to at least one deliverable.

| ObjectiveID | Name | Deliverables Mapped | Covered |
|---|---|---|---|
| OBJ-001 | Working macOS desktop build and install path | DEL-01-01, DEL-01-02, DEL-01-03, DEL-03-01 | YES |
| OBJ-002 | Harness runtime correctness + Anthropic-only network | DEL-03-01, DEL-03-02, DEL-03-03, DEL-03-04, DEL-03-05, DEL-03-06, DEL-03-07 | YES |
| OBJ-003 | Attachment-enabled turns robust and UX-safe | DEL-04-01, DEL-04-02 | YES |
| OBJ-004 | Filesystem-as-state SPEC-conformant and auditable | DEL-05-01, DEL-05-02, DEL-05-03, DEL-05-04, DEL-06-02, DEL-06-03, DEL-06-04 | YES |
| OBJ-005 | Desktop UI supports intended operator workflow | DEL-02-01, DEL-02-02, DEL-02-03, DEL-02-04, DEL-02-05 | YES |
| OBJ-006 | Validation posture and governance/agent conformance | DEL-03-06, DEL-06-01, DEL-06-02, DEL-06-03, DEL-06-04, DEL-06-05, DEL-07-01, DEL-07-02, DEL-07-03 | YES |
| OBJ-007 | Optional integrity hardening loop (TBD scope) | DEL-08-01 through DEL-08-07 | YES |
| OBJ-008 | Local frontend runtime baseline | DEL-01-03, DEL-02-05, DEL-03-07, DEL-07-03 | YES |

**OBJECTIVE COVERAGE RESULT: 8/8 objectives covered by at least one deliverable. PASS.**

---

## 5. Package Consistency

**Check:** Every package declared in the decomposition has a corresponding folder in the execution tree.

| PackageID | Decomp Name | Folder Exists | Folder Name | Deliverable Count (decomp) | Deliverable Count (folders) | Match |
|---|---|---|---|---|---|---|
| PKG-01 | Build & Packaging | YES | PKG-01_Build_And_Packaging | 3 | 3 | YES |
| PKG-02 | Desktop UI Workflow | YES | PKG-02_Desktop_UI_Workflow | 5 | 5 | YES |
| PKG-03 | Harness Runtime Core | YES | PKG-03_Harness_Runtime_Core | 7 | 7 | YES |
| PKG-04 | Attachments & Multimodal Turns | YES | PKG-04_Attachments_Multimodal | 2 | 2 | YES |
| PKG-05 | Filesystem Execution Model | YES | PKG-05_Filesystem_Execution_Model | 4 | 4 | YES |
| PKG-06 | Agent Suite & Governance | YES | PKG-06_Agent_Suite_Governance | 5 | 5 | YES |
| PKG-07 | Validation & Example Assets | YES | PKG-07_Validation_Example_Assets | 3 | 3 | YES |
| PKG-08 | Optional Integrity Hardening | YES | PKG-08_Optional_Integrity_Hardening | 7 | 7 | YES |

**Per-package deliverable counts:** 3 + 5 + 7 + 2 + 4 + 5 + 3 + 7 = **36**

**PACKAGE CONSISTENCY RESULT: 8/8 packages present. Deliverable counts match in all packages. PASS.**

---

## 6. ID Format Validation

**Check:** All IDs follow the canonical format specified in the decomposition header.

### Format rules (from decomposition header, line 5)
- Package IDs: `PKG-XX` (two-digit zero-padded)
- Deliverable IDs: `DEL-XX-YY` (package prefix + two-digit sequence)
- Scope item IDs: `SOW-NNN` (three-digit zero-padded)
- Objective IDs: `OBJ-NNN` (three-digit zero-padded)

### Package IDs
PKG-01, PKG-02, PKG-03, PKG-04, PKG-05, PKG-06, PKG-07, PKG-08
All match `PKG-XX` format. **PASS.**

### Deliverable IDs
DEL-01-01, DEL-01-02, DEL-01-03,
DEL-02-01, DEL-02-02, DEL-02-03, DEL-02-04, DEL-02-05,
DEL-03-01, DEL-03-02, DEL-03-03, DEL-03-04, DEL-03-05, DEL-03-06, DEL-03-07,
DEL-04-01, DEL-04-02,
DEL-05-01, DEL-05-02, DEL-05-03, DEL-05-04,
DEL-06-01, DEL-06-02, DEL-06-03, DEL-06-04, DEL-06-05,
DEL-07-01, DEL-07-02, DEL-07-03,
DEL-08-01, DEL-08-02, DEL-08-03, DEL-08-04, DEL-08-05, DEL-08-06, DEL-08-07
All match `DEL-XX-YY` format. Sequences are contiguous within each package. **PASS.**

### Scope Item IDs
SOW-001 through SOW-043 (original), SOW-044 through SOW-049 (SCA-001).
All match `SOW-NNN` format. **PASS.**

Note: There is a gap in SOW numbering between SOW-043 and SOW-044 (none missing -- SOW-043 is the last original, SOW-044 is the first amendment item). No gap within any range.

### Objective IDs
OBJ-001 through OBJ-008.
All match `OBJ-NNN` format. Sequence is contiguous. **PASS.**

**ID FORMAT RESULT: All IDs conform to canonical format. PASS.**

---

## 7. Telemetry Consistency

**Check:** Declared counts in the telemetry section match actual counts derived from the document.

### Pre-amendment telemetry (lines 315-333)

| Metric | Declared | Actual (counted from pre-amendment tables) | Match |
|---|---|---|---|
| ScopeItemCount | 43 | 43 (SOW-001..SOW-043) | YES |
| IN | 31 | 31 | YES |
| OUT | 5 | 5 (SOW-039..SOW-043) | YES |
| TBD | 7 | 7 (SOW-032..SOW-038) | YES |
| PackageCount | 8 | 8 | YES |
| DeliverableCount | 32 | 32 | YES |
| ObjectiveCount | 7 | 7 | YES |
| UnassignedScopeItems | 0 | 0 | YES |
| ScopeItemsWithoutDeliverableMapping | 0 | 0 | YES |
| UnmappedObjectives | 0 | 0 | YES |

### Post-amendment telemetry (Telemetry Delta, lines 423-426)

| Metric | Declared Post-A1 | Actual (counted including SCA-001) | Match |
|---|---|---|---|
| ScopeItemCount | 49 | 49 (43 original + 6 new) | YES |
| IN | 37 | 37 (31 original + 6 new) | YES |
| OUT | 5 | 5 (unchanged) | YES |
| TBD | 7 | 7 (unchanged) | YES |
| DeliverableCount | 36 | 36 (32 original + 4 new) | YES |
| ObjectiveCount | 8 | 8 (7 original + 1 new) | YES |

### Context Envelope Counts (declared pre-amendment, lines 326-330)

| Envelope | Declared (pre-amendment) | Actual (pre-amendment deliverables) | Match |
|---|---|---|---|
| S | 5 | 5 (DEL-03-03, DEL-03-04, DEL-06-05, DEL-08-02, DEL-08-03) | YES |
| M | 21 | 21 | YES |
| L | 6 | 6 (DEL-03-06, DEL-05-04, DEL-06-01, DEL-08-05, DEL-08-06, DEL-08-07) | YES |
| XL | 0 | 0 | YES |

Post-amendment context envelope update (SCA-001 adds: 3L + 1M):
- S: 5 (unchanged)
- M: 22 (21 + DEL-07-03)
- L: 9 (6 + DEL-01-03, DEL-02-05, DEL-03-07)
- XL: 0

Note: The pre-amendment telemetry section was not updated in-place to reflect post-SCA-001 totals -- this is by design (the amendment section carries the delta). No issue.

**TELEMETRY RESULT: All declared counts match actual counts. PASS.**

---

## Summary

| Audit Dimension | Result | Issues |
|---|---|---|
| 1. Forward Coverage | PASS | 0 |
| 2. Reverse Coverage | PASS | 0 |
| 3. Scope Ledger Consistency | PASS | 0 |
| 4. Objective Coverage | PASS | 0 |
| 5. Package Consistency | PASS | 0 |
| 6. ID Format Validation | PASS | 0 |
| 7. Telemetry Consistency | PASS | 0 |

**Overall: PASS (7/7 dimensions). 0 issues found.**

The decomposition is fully consistent in its post-SCA-001 state. All 36 deliverables are scaffolded, all 49 scope items are mapped, all 8 objectives are covered, and all telemetry figures are accurate.
