#!/usr/bin/env python3
"""
analyze_closure.py -- Reproducible dependency closure analysis for DEL-06-04

Run Label: DEL-06-04
Date: 2026-02-21
Snapshot: CLOSURE_DEL-06-04_2026-02-21

This script reproduces the closure analysis performed by AUDIT_DEP_CLOSURE.
It reads the Dependencies.csv for DEL-06-04, builds the dependency graph,
and runs all 9 core checks.

Usage:
    python3 analyze_closure.py [--execution-root PATH]

Default execution root: execution/ (relative to repo root)
"""

import csv
import json
import os
import re
import sys
from collections import defaultdict
from pathlib import Path


# --- Configuration ---
DEFAULT_EXECUTION_ROOT = "execution"
DELIVERABLE_ID = "DEL-06-04"
DELIVERABLE_PATH = "PKG-06_Agent_Suite_Governance/1_Working/DEL-06-04_Change_Management_Git_Hygiene"
EDGE_FILTER_CLASS = "EXECUTION"
EDGE_FILTER_TARGET_TYPE = "DELIVERABLE"
FILTER_ACTIVE_ONLY = True
NORMALIZE_IDS = True
HUB_THRESHOLD = 20
MAX_CYCLES = 10000

# All known workspace deliverable IDs (32 total)
WORKSPACE_DELIVERABLES = {
    "DEL-01-01", "DEL-01-02",
    "DEL-02-01", "DEL-02-02", "DEL-02-03", "DEL-02-04",
    "DEL-03-01", "DEL-03-02", "DEL-03-03", "DEL-03-04", "DEL-03-05", "DEL-03-06",
    "DEL-04-01", "DEL-04-02",
    "DEL-05-01", "DEL-05-02", "DEL-05-03", "DEL-05-04",
    "DEL-06-01", "DEL-06-02", "DEL-06-03", "DEL-06-04", "DEL-06-05",
    "DEL-07-01", "DEL-07-02",
    "DEL-08-01", "DEL-08-02", "DEL-08-03", "DEL-08-04", "DEL-08-05", "DEL-08-06", "DEL-08-07",
}

# Expected v3.1 columns
EXPECTED_COLUMNS = [
    "RegisterSchemaVersion", "DependencyID", "FromPackageID", "FromDeliverableID",
    "FromDeliverableName", "DependencyClass", "AnchorType", "Direction",
    "DependencyType", "TargetType", "TargetPackageID", "TargetDeliverableID",
    "TargetRefID", "TargetName", "TargetLocation", "Statement", "EvidenceFile",
    "SourceRef", "EvidenceQuote", "Explicitness", "RequiredMaturity",
    "ProposedMaturity", "SatisfactionStatus", "Confidence", "Origin",
    "FirstSeen", "LastSeen", "Status", "Notes",
]


def normalize_id(raw_id: str) -> str:
    """Normalize a deliverable ID by stripping descriptive suffixes."""
    if not raw_id:
        return raw_id
    match = re.match(r"(DEL-\d+-\d+)", raw_id)
    return match.group(1) if match else raw_id


def tarjan_scc(graph: dict) -> list:
    """Tarjan's algorithm for strongly connected components."""
    index_counter = [0]
    stack = []
    lowlink = {}
    index = {}
    on_stack = {}
    sccs = []

    def strongconnect(v):
        index[v] = index_counter[0]
        lowlink[v] = index_counter[0]
        index_counter[0] += 1
        stack.append(v)
        on_stack[v] = True

        for w in graph.get(v, []):
            if w not in index:
                strongconnect(w)
                lowlink[v] = min(lowlink[v], lowlink[w])
            elif on_stack.get(w, False):
                lowlink[v] = min(lowlink[v], index[w])

        if lowlink[v] == index[v]:
            scc = []
            while True:
                w = stack.pop()
                on_stack[w] = False
                scc.append(w)
                if w == v:
                    break
            sccs.append(scc)

    for v in graph:
        if v not in index:
            strongconnect(v)

    return sccs


def main():
    # Resolve execution root
    exec_root = DEFAULT_EXECUTION_ROOT
    if len(sys.argv) > 2 and sys.argv[1] == "--execution-root":
        exec_root = sys.argv[2]

    csv_path = os.path.join(exec_root, DELIVERABLE_PATH, "Dependencies.csv")
    if not os.path.isfile(csv_path):
        print(f"FAILED_INPUTS: Dependencies.csv not found at {csv_path}")
        sys.exit(1)

    # --- Step 1: Parse CSV ---
    rows = []
    with open(csv_path, "r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        columns = reader.fieldnames or []
        for row in reader:
            rows.append(row)

    print(f"Parsed {len(rows)} rows from {csv_path}")

    # --- Step 2: Schema validation ---
    missing_cols = [c for c in EXPECTED_COLUMNS if c not in columns]
    schema_valid = len(missing_cols) == 0
    print(f"Check 1 - Schema Compliance: {'PASS' if schema_valid else 'FAIL'}")
    if missing_cols:
        print(f"  Missing columns: {missing_cols}")

    # --- Step 3: Build graph ---
    edges = []
    anchor_rows = []
    for row in rows:
        if FILTER_ACTIVE_ONLY and row.get("Status", "") != "ACTIVE":
            continue
        if row.get("DependencyClass", "") == "ANCHOR":
            anchor_rows.append(row)
            continue
        if (row.get("DependencyClass", "") == EDGE_FILTER_CLASS
                and row.get("TargetType", "") == EDGE_FILTER_TARGET_TYPE):
            from_id = normalize_id(row.get("FromDeliverableID", "")) if NORMALIZE_IDS else row.get("FromDeliverableID", "")
            target_id = normalize_id(row.get("TargetDeliverableID", "")) if NORMALIZE_IDS else row.get("TargetDeliverableID", "")
            if from_id and target_id:
                edges.append({
                    "from": from_id,
                    "to": target_id,
                    "dependency_id": row.get("DependencyID", ""),
                    "direction": row.get("Direction", ""),
                    "dependency_type": row.get("DependencyType", ""),
                })

    nodes = set()
    nodes.add(DELIVERABLE_ID)
    for e in edges:
        nodes.add(e["from"])
        nodes.add(e["to"])

    print(f"Graph: {len(nodes)} nodes, {len(edges)} edges")

    # --- Check 2: Orphan dependencies ---
    orphans = [e for e in edges if e["to"] not in WORKSPACE_DELIVERABLES]
    print(f"Check 2 - Orphan Dependencies: {'PASS' if len(orphans) == 0 else 'WARNING'} ({len(orphans)} orphans)")

    # --- Check 3: Circular dependencies (Tarjan SCC) ---
    adj = defaultdict(list)
    for e in edges:
        adj[e["from"]].append(e["to"])
    # Ensure all nodes are in adj
    for n in nodes:
        if n not in adj:
            adj[n] = []

    sccs = tarjan_scc(dict(adj))
    nontrivial = [s for s in sccs if len(s) > 1]
    print(f"Check 3 - Circular Dependencies: {'PASS' if len(nontrivial) == 0 else 'BLOCKER'} ({len(nontrivial)} non-trivial SCCs)")

    # --- Check 4: Anchor coverage ---
    has_implements = any(r.get("AnchorType", "") == "IMPLEMENTS_NODE" for r in anchor_rows)
    print(f"Check 4 - Anchor Coverage: {'PASS' if has_implements else 'WARNING'}")

    # --- Check 5: Misplaced fields ---
    misplaced = []
    for row in rows:
        if (row.get("TargetType", "") != "DELIVERABLE"
                and row.get("TargetDeliverableID", "").strip()):
            misplaced.append(row)
    print(f"Check 5 - Misplaced Fields: {'PASS' if len(misplaced) == 0 else 'WARNING'} ({len(misplaced)} misplaced)")

    # --- Check 6: ID format consistency ---
    id_values = []
    for row in rows:
        for col in ["FromDeliverableID", "TargetDeliverableID"]:
            val = row.get(col, "").strip()
            if val:
                id_values.append(val)
    needs_norm = [v for v in id_values if v != normalize_id(v)]
    print(f"Check 6 - ID Format Consistency: {'PASS' if len(needs_norm) == 0 else 'WARNING'} ({len(needs_norm)}/{len(id_values)} need normalization)")

    # --- Check 7: Isolated deliverables ---
    connected = set()
    for e in edges:
        connected.add(e["from"])
        connected.add(e["to"])
    isolated = [n for n in [DELIVERABLE_ID] if n not in connected]
    print(f"Check 7 - Isolated Deliverables: {'PASS' if len(isolated) == 0 else 'WARNING'} ({len(isolated)} isolated)")

    # --- Check 8: Hub analysis ---
    degree = defaultdict(int)
    for e in edges:
        degree[e["from"]] += 1
        degree[e["to"]] += 1
    hubs = {n: d for n, d in degree.items() if d >= HUB_THRESHOLD}
    print(f"Check 8 - Hub Analysis: {'PASS' if len(hubs) == 0 else 'WARNING'} ({len(hubs)} hubs)")

    # --- Check 9: Bidirectional pairs ---
    edge_set = set()
    for e in edges:
        edge_set.add((e["from"], e["to"]))
    bidir = [(a, b) for (a, b) in edge_set if (b, a) in edge_set and a < b]
    print(f"Check 9 - Bidirectional Pairs: {'PASS' if len(bidir) == 0 else 'INFO'} ({len(bidir)} pairs)")

    # --- Overall ---
    all_pass = (
        schema_valid
        and len(orphans) == 0
        and len(nontrivial) == 0
        and has_implements
        and len(misplaced) == 0
        and len(needs_norm) == 0
        and len(isolated) == 0
        and len(hubs) == 0
    )
    status = "PASS" if all_pass else "WARNINGS"
    print(f"\nOverall Status: {status}")
    return 0 if all_pass else 1


if __name__ == "__main__":
    sys.exit(main())
