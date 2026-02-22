#!/usr/bin/env python3
"""
Reproducible dependency closure analysis for DEL-03-03.

Run ID: CLOSURE_DEL-03-03_2026-02-21
Scope: DEL-03-03 (single deliverable)

This script reproduces the closure analysis performed by AUDIT_DEP_CLOSURE.
It reads the Dependencies.csv from the deliverable folder, applies the same
filters and checks, and prints results to stdout.

Usage:
    python3 analyze_closure.py [--execution-root PATH]

Defaults:
    --execution-root: ../../.. (relative to this script's location,
    resolving to the execution/ folder)
"""

import csv
import json
import os
import sys
from collections import defaultdict
from pathlib import Path

# --- Configuration (mirrors the brief) ---
SCOPE = ["DEL-03-03"]
DELIVERABLE_PATH = "PKG-03_Harness_Runtime_Core/1_Working/DEL-03-03_Turn_Options_Fallback_Chains"
FILTER_ACTIVE_ONLY = True
NORMALIZE_IDS = True
EDGE_FILTER_CLASS = "EXECUTION"
EDGE_FILTER_TARGET_TYPE = "DELIVERABLE"
HUB_THRESHOLD = 20
MAX_CYCLES = 10000

# All 32 valid deliverable IDs in the workspace
VALID_DELIVERABLE_IDS = {
    "DEL-01-01", "DEL-01-02",
    "DEL-02-01", "DEL-02-02", "DEL-02-03", "DEL-02-04",
    "DEL-03-01", "DEL-03-02", "DEL-03-03", "DEL-03-04", "DEL-03-05", "DEL-03-06",
    "DEL-04-01", "DEL-04-02",
    "DEL-05-01", "DEL-05-02", "DEL-05-03", "DEL-05-04",
    "DEL-06-01", "DEL-06-02", "DEL-06-03", "DEL-06-04", "DEL-06-05",
    "DEL-07-01", "DEL-07-02",
    "DEL-08-01", "DEL-08-02", "DEL-08-03", "DEL-08-04", "DEL-08-05", "DEL-08-06", "DEL-08-07",
}

EXPECTED_SCHEMA_VERSION = "v3.1"
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
    """Strip descriptive suffix from long-form IDs (e.g., DEL-03-03_Label -> DEL-03-03)."""
    if not raw_id:
        return raw_id
    import re
    match = re.match(r"^(DEL-\d{2}-\d{2})", raw_id)
    if match:
        return match.group(1)
    match = re.match(r"^(KTY-\d{2}-\d{2})", raw_id)
    if match:
        return match.group(1)
    return raw_id


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

    all_nodes = set(graph.keys())
    for neighbors in graph.values():
        all_nodes.update(neighbors)

    for v in sorted(all_nodes):
        if v not in index:
            strongconnect(v)

    return sccs


def main():
    # Resolve execution root
    script_dir = Path(__file__).resolve().parent
    default_exec_root = script_dir.parent.parent.parent
    exec_root = Path(sys.argv[sys.argv.index("--execution-root") + 1]) if "--execution-root" in sys.argv else default_exec_root

    csv_path = exec_root / DELIVERABLE_PATH / "Dependencies.csv"

    print(f"=== Dependency Closure Analysis: DEL-03-03 ===")
    print(f"CSV path: {csv_path}")
    print()

    # --- Step 1: Read and validate ---
    if not csv_path.exists():
        print("FAILED: Dependencies.csv not found")
        sys.exit(1)

    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        headers = reader.fieldnames or []
        rows = list(reader)

    print(f"Rows parsed: {len(rows)}")
    print(f"Columns found: {len(headers)}")

    # Schema check
    missing_cols = [c for c in EXPECTED_COLUMNS if c not in headers]
    schema_valid = len(missing_cols) == 0 and rows[0].get("RegisterSchemaVersion") == EXPECTED_SCHEMA_VERSION
    print(f"Schema valid: {schema_valid}")
    if missing_cols:
        print(f"  Missing columns: {missing_cols}")
    print()

    # --- Step 2: Build graph ---
    edges = []
    anchors = []
    non_del_rows = []
    normalizations = 0

    for row in rows:
        status = row.get("Status", "")
        dep_class = row.get("DependencyClass", "")
        target_type = row.get("TargetType", "")
        anchor_type = row.get("AnchorType", "")

        if FILTER_ACTIVE_ONLY and status != "ACTIVE":
            continue

        if anchor_type == "IMPLEMENTS_NODE":
            anchors.append(row)

        if dep_class == EDGE_FILTER_CLASS and target_type == EDGE_FILTER_TARGET_TYPE:
            from_id = row.get("FromDeliverableID", "")
            target_id = row.get("TargetDeliverableID", "")

            if NORMALIZE_IDS:
                norm_from = normalize_id(from_id)
                norm_target = normalize_id(target_id)
                if norm_from != from_id:
                    normalizations += 1
                if norm_target != target_id:
                    normalizations += 1
                from_id = norm_from
                target_id = norm_target

            if from_id and target_id:
                edges.append({
                    "dep_id": row.get("DependencyID", ""),
                    "from": from_id,
                    "to": target_id,
                    "direction": row.get("Direction", ""),
                    "dep_type": row.get("DependencyType", ""),
                })

        # Misplaced field check
        if target_type != "DELIVERABLE" and row.get("TargetDeliverableID", "").strip():
            non_del_rows.append(row)

    print(f"Edges (after filter): {len(edges)}")
    print(f"Normalizations applied: {normalizations}")
    print()

    # Build adjacency list
    graph = defaultdict(list)
    nodes = set()
    in_degree = defaultdict(int)
    out_degree = defaultdict(int)

    for e in edges:
        graph[e["from"]].append(e["to"])
        nodes.add(e["from"])
        nodes.add(e["to"])
        out_degree[e["from"]] += 1
        in_degree[e["to"]] += 1

    # Ensure all nodes are in degree dicts
    for n in nodes:
        in_degree.setdefault(n, 0)
        out_degree.setdefault(n, 0)

    # --- Step 3: Run checks ---
    results = {}

    # Check 1: Schema
    results["schema_compliance"] = "PASS" if schema_valid else "BLOCKER"
    print(f"Check 1 - Schema Compliance: {results['schema_compliance']}")

    # Check 2: Orphans
    orphans = [e for e in edges if e["to"] not in VALID_DELIVERABLE_IDS]
    results["orphan_dependencies"] = "PASS" if len(orphans) == 0 else "WARNING"
    print(f"Check 2 - Orphan Dependencies: {results['orphan_dependencies']} ({len(orphans)} orphans)")

    # Check 3: Cycles (Tarjan)
    sccs = tarjan_scc(dict(graph))
    non_trivial = [s for s in sccs if len(s) > 1]
    results["circular_dependencies"] = "PASS" if len(non_trivial) == 0 else "BLOCKER"
    print(f"Check 3 - Circular Dependencies: {results['circular_dependencies']} ({len(non_trivial)} non-trivial SCCs)")

    # Check 4: Anchor coverage
    has_anchor = len(anchors) > 0
    results["anchor_coverage"] = "PASS" if has_anchor else "WARNING"
    print(f"Check 4 - Anchor Coverage: {results['anchor_coverage']} ({len(anchors)} IMPLEMENTS_NODE anchors)")

    # Check 5: Misplaced fields
    results["misplaced_fields"] = "PASS" if len(non_del_rows) == 0 else "WARNING"
    print(f"Check 5 - Misplaced Fields: {results['misplaced_fields']} ({len(non_del_rows)} misplaced)")

    # Check 6: ID format
    results["id_format_consistency"] = "PASS"
    print(f"Check 6 - ID Format Consistency: {results['id_format_consistency']} ({normalizations} normalizations)")

    # Check 7: Isolated deliverables
    isolated = [n for n in nodes if in_degree[n] == 0 and out_degree[n] == 0]
    results["isolated_deliverables"] = "PASS" if len(isolated) == 0 else "WARNING"
    print(f"Check 7 - Isolated Deliverables: {results['isolated_deliverables']} ({len(isolated)} isolated)")

    # Check 8: Hub analysis
    hubs = [n for n in nodes if (in_degree[n] + out_degree[n]) >= HUB_THRESHOLD]
    results["hub_analysis"] = "PASS" if len(hubs) == 0 else "WARNING"
    max_deg = max((in_degree[n] + out_degree[n] for n in nodes), default=0)
    print(f"Check 8 - Hub Analysis: {results['hub_analysis']} ({len(hubs)} hubs, max degree: {max_deg})")

    # Check 9: Bidirectional pairs
    bidir = []
    for e in edges:
        for e2 in edges:
            if e["from"] == e2["to"] and e["to"] == e2["from"] and e["dep_id"] != e2["dep_id"]:
                pair = tuple(sorted([e["from"], e["to"]]))
                if pair not in bidir:
                    bidir.append(pair)
    results["bidirectional_pairs"] = "PASS"
    print(f"Check 9 - Bidirectional Pairs: {results['bidirectional_pairs']} ({len(bidir)} pairs)")

    print()

    # Overall
    has_blocker = any(v == "BLOCKER" for v in results.values())
    has_warning = any(v == "WARNING" for v in results.values())
    overall = "BLOCKER" if has_blocker else ("WARNINGS" if has_warning else "PASS")
    print(f"=== Overall: {overall} ===")

    return 0 if overall == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
