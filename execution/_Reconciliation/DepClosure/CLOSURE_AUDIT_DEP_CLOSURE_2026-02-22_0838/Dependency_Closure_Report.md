# Dependency Closure Report

**Run:** AUDIT_DEP_CLOSURE | **Date:** 2026-02-22 | **Scope:** ALL (36 deliverables) | **Status:** BLOCKER

---

## 1. Executive Summary

Full-scope dependency closure analysis across all 36 deliverables in 8 packages. The dependency graph contains 36 nodes and 122 unique directed edges (154 total including duplicates from parallel declarations).

**Overall verdict: BLOCKER** -- 3 strongly connected components (circular dependency clusters) detected, involving 28 of 36 deliverables (78%).

Seven of nine checks pass cleanly. The remaining issues are:
- 3 SCCs (circular dependency clusters) -- **BLOCKER**
- 14 bidirectional pairs -- **INFO** (expected in this architecture)

---

## 2. Check Results

### 2.1 Schema Compliance -- PASS

All 36 deliverables have readable Dependencies.csv files with valid v3.1 schema (29 required columns present). Coverage: 100%.

### 2.2 Orphan Dependencies -- PASS

Zero orphan targets. Every TargetDeliverableID in EXECUTION/DELIVERABLE edges points to a deliverable that exists within the execution root. The graph is fully self-contained.

### 2.3 Circular Dependencies -- BLOCKER

3 strongly connected components detected via Tarjan's algorithm:

#### SCC-001 (21 nodes) -- Core Runtime Cluster

| Members |
|---|
| DEL-01-01, DEL-01-02, DEL-01-03, DEL-02-01, DEL-02-02, DEL-02-03, DEL-02-04, DEL-02-05, DEL-03-01, DEL-03-02, DEL-03-03, DEL-03-04, DEL-03-05, DEL-03-06, DEL-03-07, DEL-04-01, DEL-05-01, DEL-05-02, DEL-06-04, DEL-06-05, DEL-07-03 |

**Root cause analysis:** This large SCC is driven by several structural patterns:

1. **Bidirectional build/bundling edges:** DEL-01-01 (build) and DEL-05-01 (instruction root bundling) declare mutual dependencies -- build needs instruction root separation; bundling needs build verification. Similarly DEL-01-02 (DMG packaging) and DEL-05-01 are bidirectional.

2. **Harness runtime mutual dependencies:** DEL-03-01 through DEL-03-07 form a tightly coupled runtime cluster. Session boot (03-01) depends on provider integration (03-05) and API baseline (03-07); turn execution (03-02) depends on session boot and options mapping (03-03); and many of these declare DOWNSTREAM handovers back to each other.

3. **Frontend baseline fan-out:** DEL-01-03 (frontend workspace bootstrap) has 11 inbound edges (most in the graph) and is a hub connecting build, UI, and harness deliverables. Its downstream declarations to DEL-03-07 and DEL-03-07's upstream back to DEL-01-03 create a bidirectional core.

4. **PKG-02 UI deliverables coupling:** DEL-02-01 through DEL-02-05 are mutually wired via layout/shell/navigation interfaces and DOWNSTREAM handovers from DEL-02-05 back up to its siblings.

5. **Governance edges into core:** DEL-06-04 (change management) and DEL-06-05 (governance coherence) depend on DEL-06-01 and declare interfaces into DEL-03-04 (subagent governance) and DEL-03-06 (network guardrails), linking them into the main cluster.

**Representative cycles (shortest):**
- DEL-01-01 -> DEL-05-01 -> DEL-01-01 (length 2)
- DEL-01-01 -> DEL-05-01 -> DEL-01-02 -> DEL-01-01 (length 3)

**Remediation path:** Many of the bidirectional edges represent legitimate information interfaces (verification-time dependencies, not hard start-gates). Reclassifying these from DependencyType=PREREQUISITE to DependencyType=INTERFACE or CONSTRAINT (for the weaker direction) and adjusting the graph to treat INTERFACE edges as non-blocking would significantly reduce SCC membership. Prior HUMAN_RULING_2026-02-22 already reclassified 3 edges in this direction.

#### SCC-002 (5 nodes) -- Lifecycle/Governance Cluster

| Members |
|---|
| DEL-05-03, DEL-05-04, DEL-06-02, DEL-06-03, DEL-08-05 |

**Root cause analysis:**
- DEL-05-03 (lifecycle state) and DEL-05-04 (dependency tracking) are mutually coupled via lifecycle-state/dependency-timing interface.
- DEL-06-02 (local workflow agents) depends on DEL-05-04 for file contract and DEL-06-03 for cross-deliverable boundary, while DEL-06-03 declares a downstream interface back to DEL-06-02.
- DEL-08-05 (lock mechanism) declares downstream ENABLES to DEL-06-02 for agent protocol updates, creating a back-edge.

**Representative cycle:**
- DEL-05-03 -> DEL-06-02 -> DEL-05-04 -> DEL-05-03 (length 3)
- DEL-06-02 -> DEL-06-03 -> DEL-06-02 (length 2)

**Remediation path:** The DEL-06-02/DEL-06-03 bidirectional edge is a natural interface boundary. The DEL-08-05 -> DEL-06-02 ENABLES edge is a future/TBD-scope dependency that could be removed or deferred.

#### SCC-003 (2 nodes) -- Validation Fixtures Cluster

| Members |
|---|
| DEL-07-01, DEL-07-02 |

**Root cause analysis:** DEL-07-02 (example execution roots) declares a DOWNSTREAM HANDOVER to DEL-07-01 (validation suite) because validation scripts consume example roots as test fixtures. DEL-07-02 also declares an UPSTREAM INTERFACE from DEL-07-01 because the example roots' conformance is verified by DEL-07-01's validation scripts. This creates a legitimate bidirectional relationship.

**Representative cycle:**
- DEL-07-01 -> DEL-07-02 -> DEL-07-01 (length 2)

**Remediation path:** Reclassify one direction. DEL-07-02's UPSTREAM INTERFACE from DEL-07-01 (DEP-07-02-009) could be reclassified to DOWNSTREAM or removed, since DEL-07-02 does not truly depend on DEL-07-01 for production -- it is a verification-time relationship.

### 2.4 Anchor Coverage -- PASS

All 36 deliverables have at least one ANCHOR row with AnchorType=IMPLEMENTS_NODE. Full scope-traceability coverage confirmed.

### 2.5 Misplaced Fields -- PASS

Zero rows have TargetType != DELIVERABLE with a non-empty TargetDeliverableID. Schema hygiene is clean.

### 2.6 ID Format Consistency -- PASS

All FromDeliverableID and TargetDeliverableID values are in short form (DEL-XX-YY). Zero long-form IDs detected. NORMALIZE_IDS applied to folder names only during discovery.

### 2.7 Isolated Deliverables -- PASS

Zero isolated deliverables. All 36 nodes participate in at least one EXECUTION/DELIVERABLE edge. The graph is fully connected.

### 2.8 Hub Analysis -- PASS

No nodes exceed the hub threshold of 20. The highest-degree nodes are:

| Deliverable | In-Degree | Out-Degree | Total |
|---|---|---|---|
| DEL-03-01 | 11 | 6 | 17 |
| DEL-03-02 | 9 | 8 | 17 |
| DEL-03-07 | 10 | 7 | 17 |
| DEL-05-04 | 8 | 8 | 16 |
| DEL-07-01 | 1 | 12 | 13 |
| DEL-01-03 | 11 | 1 | 12 |
| DEL-05-01 | 9 | 3 | 12 |

DEL-03-01, DEL-03-02, and DEL-03-07 are the most connected nodes (harness runtime core). DEL-01-03 (frontend workspace bootstrap) has the highest in-degree (11), making it the most depended-upon deliverable in the graph -- consistent with its role as the pre-tier gate workspace foundation.

### 2.9 Bidirectional Pairs -- INFO (14 pairs)

14 pairs of deliverables have edges in both directions (A depends on B, and B depends on A):

| Pair | Nature |
|---|---|
| DEL-01-01 <-> DEL-05-01 | Build baseline / instruction root bundling |
| DEL-01-02 <-> DEL-05-01 | DMG packaging / instruction root bundling |
| DEL-01-03 <-> DEL-03-07 | Frontend workspace / harness API baseline |
| DEL-02-03 <-> DEL-02-04 | Toolkit panel / multipane layout |
| DEL-02-03 <-> DEL-03-03 | Toolkit opts producer / opts fallback consumer |
| DEL-03-01 <-> DEL-03-07 | Session boot / API baseline |
| DEL-03-01 <-> DEL-05-01 | Session boot / instruction root |
| DEL-03-02 <-> DEL-03-03 | Turn execution / opts mapping |
| DEL-03-02 <-> DEL-03-04 | Turn execution / subagent governance |
| DEL-03-02 <-> DEL-03-05 | Turn execution / Anthropic provider |
| DEL-03-02 <-> DEL-03-07 | Turn execution / API baseline |
| DEL-03-02 <-> DEL-04-01 | Turn execution / attachment resolver |
| DEL-06-02 <-> DEL-06-03 | Local workflow agents / cross-deliverable workflows |
| DEL-07-01 <-> DEL-07-02 | Validation suite / example execution roots |

Most of these are legitimate architectural interfaces where two deliverables have complementary producer/consumer roles. They are the primary drivers of the SCCs.

---

## 3. Graph Metrics Summary

| Metric | Value |
|---|---|
| Deliverables (nodes) | 36 |
| Unique directed edges | 122 |
| Total edge declarations | 154 |
| EXECUTION/DELIVERABLE rows parsed | 156 |
| Orphan targets | 0 |
| SCCs | 3 (28 nodes) |
| Cycles sampled | 24 |
| Missing anchors | 0 |
| Misplaced fields | 0 |
| Isolated deliverables | 0 |
| Hubs (degree >= 20) | 0 |
| Bidirectional pairs | 14 |

---

## 4. Package Connectivity

| Package | Deliverables | Internal Edges | External In | External Out |
|---|---|---|---|---|
| PKG-01 | 3 | DEL-01-01<->DEL-01-02, DEL-01-03->DEL-01-01, DEL-01-03->DEL-01-02 | 11 in | 3 out |
| PKG-02 | 5 | DEL-02-05->DEL-02-01/02/03/04, DEL-02-04->DEL-02-01/02/03 | 6 in | 6 out |
| PKG-03 | 7 | Dense internal mesh (03-01 through 03-07) | 8 in | 14 out |
| PKG-04 | 2 | DEL-04-01->DEL-04-02 | 4 in | 4 out |
| PKG-05 | 4 | DEL-05-01<->DEL-05-02/03/04 | 13 in | 5 out |
| PKG-06 | 5 | DEL-06-01<-DEL-06-02/03/04/05 | 4 in | 4 out |
| PKG-07 | 3 | DEL-07-01<->DEL-07-02, DEL-07-03->DEL-07-01 | 8 in | 7 out |
| PKG-08 | 7 | Sequential chain (08-04->08-07, 08-06->08-07) | 5 in | 8 out |

---

## 5. Evidence Files

All evidence files are in the `Evidence/` subdirectory of this snapshot:

| File | Contents |
|---|---|
| `coverage.csv` | Per-deliverable CSV existence, readability, and schema status |
| `orphans.csv` | Orphan target edges (empty -- no orphans) |
| `scc_summary.csv` | SCC membership list |
| `cycles_sample.csv` | Representative cycles within SCCs |
| `hubs.csv` | Hub nodes (empty -- none above threshold) |
| `bidirectional_pairs.csv` | All 14 bidirectional pairs |
