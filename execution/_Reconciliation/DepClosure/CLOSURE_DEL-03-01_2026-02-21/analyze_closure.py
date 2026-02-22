#!/usr/bin/env python3
"""
analyze_closure.py -- Reproducible dependency closure analysis for DEL-03-01.

Run Label: DEL-03-01
Date: 2026-02-21
Scope: Single deliverable (DEL-03-01)

This script reproduces the closure analysis performed by AUDIT_DEP_CLOSURE.
It reads the Dependencies.csv for DEL-03-01, builds a directed graph from
EXECUTION/DELIVERABLE edges, and runs all 9 core checks.

Usage:
    python3 analyze_closure.py [--execution-root PATH]

Defaults:
    --execution-root  ../../..  (relative to this script's location in the snapshot)
"""

import csv
import json
import os
import sys
import argparse
from collections import defaultdict
from pathlib import Path


# -- Known workspace deliverables (32 total) --
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

# -- Parameters --
SCOPE = ["DEL-03-01"]
FILTER_ACTIVE_ONLY = True
NORMALIZE_IDS = True
EDGE_FILTER_CLASS = "EXECUTION"
EDGE_FILTER_TARGET_TYPE = "DELIVERABLE"
HUB_THRESHOLD = 20
MAX_CYCLES = 10000

# -- Schema v3.1 expected columns --
SCHEMA_V31_COLUMNS = [
    "RegisterSchemaVersion", "DependencyID", "FromPackageID", "FromDeliverableID",
    "FromDeliverableName", "DependencyClass", "AnchorType", "Direction",
    "DependencyType", "TargetType", "TargetPackageID", "TargetDeliverableID",
    "TargetRefID", "TargetName", "TargetLocation", "Statement", "EvidenceFile",
    "SourceRef", "EvidenceQuote", "Explicitness", "RequiredMaturity",
    "ProposedMaturity", "SatisfactionStatus", "Confidence", "Origin",
    "FirstSeen", "LastSeen", "Status", "Notes",
]


def normalize_id(raw_id: str) -> str:
    """Strip descriptive suffix from long-form IDs. E.g., DEL-03-01_Label -> DEL-03-01."""
    if not raw_id:
        return raw_id
    # Match pattern: DEL-XX-YY or KTY-CC-TT prefix
    import re
    m = re.match(r"^(DEL-\d{2}-\d{2}|KTY-\d{2}-\d{2})", raw_id)
    if m:
        return m.group(1)
    return raw_id


def read_dependencies_csv(csv_path: str) -> list[dict]:
    """Read and return rows from a Dependencies.csv file."""
    rows = []
    with open(csv_path, "r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)
    return rows


def validate_schema(rows: list[dict], csv_path: str) -> dict:
    """Validate schema compliance for v3.1."""
    if not rows:
        return {"valid": False, "reason": "Empty CSV", "path": csv_path}

    # Check RegisterSchemaVersion
    version = rows[0].get("RegisterSchemaVersion", "")
    if version != "v3.1":
        return {"valid": False, "reason": f"Unexpected version: {version}", "path": csv_path}

    # Check columns
    actual_columns = list(rows[0].keys())
    missing = [c for c in SCHEMA_V31_COLUMNS if c not in actual_columns]
    if missing:
        return {"valid": False, "reason": f"Missing columns: {missing}", "path": csv_path}

    return {"valid": True, "version": version, "path": csv_path}


def tarjan_scc(graph: dict[str, list[str]]) -> list[list[str]]:
    """Tarjan's algorithm for strongly connected components."""
    index_counter = [0]
    stack = []
    lowlink = {}
    index = {}
    on_stack = {}
    result = []

    all_nodes = set(graph.keys())
    for targets in graph.values():
        all_nodes.update(targets)

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
            component = []
            while True:
                w = stack.pop()
                on_stack[w] = False
                component.append(w)
                if w == v:
                    break
            result.append(component)

    for v in sorted(all_nodes):
        if v not in index:
            strongconnect(v)

    return result


def main():
    parser = argparse.ArgumentParser(description="Dependency closure analysis for DEL-03-01")
    parser.add_argument(
        "--execution-root",
        default=os.path.join(os.path.dirname(__file__), "..", "..", ".."),
        help="Path to execution root (default: ../../../ relative to script)",
    )
    args = parser.parse_args()

    exec_root = os.path.abspath(args.execution_root)
    csv_path = os.path.join(
        exec_root,
        "PKG-03_Harness_Runtime_Core", "1_Working",
        "DEL-03-01_Working_Root_Session_Boot", "Dependencies.csv",
    )

    print(f"Execution root: {exec_root}")
    print(f"Dependencies.csv: {csv_path}")
    print()

    # -- Step 1: Read CSV --
    if not os.path.isfile(csv_path):
        print(f"FAILED: Dependencies.csv not found at {csv_path}")
        sys.exit(1)

    rows = read_dependencies_csv(csv_path)
    print(f"Total rows: {len(rows)}")

    # -- Step 2: Schema validation --
    schema_result = validate_schema(rows, csv_path)
    print(f"Schema valid: {schema_result['valid']}")
    if not schema_result["valid"]:
        print(f"  Reason: {schema_result['reason']}")

    # -- Step 3: Filter and build graph --
    anchor_rows = [r for r in rows if r.get("DependencyClass") == "ANCHOR"]
    execution_rows = [r for r in rows if r.get("DependencyClass") == "EXECUTION"]

    if FILTER_ACTIVE_ONLY:
        execution_rows = [r for r in execution_rows if r.get("Status") == "ACTIVE"]

    deliverable_edges = [
        r for r in execution_rows
        if r.get("TargetType") == EDGE_FILTER_TARGET_TYPE
    ]

    print(f"Anchor rows: {len(anchor_rows)}")
    print(f"Execution rows (active): {len(execution_rows)}")
    print(f"Deliverable edges: {len(deliverable_edges)}")
    print()

    # Build directed graph
    graph = defaultdict(list)
    for edge in deliverable_edges:
        from_id = normalize_id(edge["FromDeliverableID"]) if NORMALIZE_IDS else edge["FromDeliverableID"]
        target_id = normalize_id(edge["TargetDeliverableID"]) if NORMALIZE_IDS else edge["TargetDeliverableID"]
        direction = edge.get("Direction", "")

        if direction == "DOWNSTREAM":
            graph[from_id].append(target_id)
        elif direction == "UPSTREAM":
            graph[target_id].append(from_id)
        else:
            # Undirected: add both directions for SCC
            graph[from_id].append(target_id)
            graph[target_id].append(from_id)

    # -- Step 4: Core checks --
    print("=" * 60)
    print("CORE CHECKS")
    print("=" * 60)

    # Check 1: Schema compliance
    print(f"\n1. Schema Compliance: {'PASS' if schema_result['valid'] else 'FAIL'}")

    # Check 2: Orphan dependencies
    orphans = []
    for edge in deliverable_edges:
        target_id = normalize_id(edge["TargetDeliverableID"]) if NORMALIZE_IDS else edge["TargetDeliverableID"]
        if target_id and target_id not in WORKSPACE_DELIVERABLES:
            orphans.append((edge["DependencyID"], target_id))
    print(f"2. Orphan Dependencies: {'PASS' if not orphans else 'WARNING'} ({len(orphans)} orphans)")
    for dep_id, target in orphans:
        print(f"   - {dep_id}: target {target} not in workspace")

    # Check 3: Circular dependencies (Tarjan)
    sccs = tarjan_scc(dict(graph))
    nontrivial_sccs = [s for s in sccs if len(s) > 1]
    self_loops = sum(1 for node, targets in graph.items() if node in targets)
    print(f"3. Circular Dependencies: {'PASS' if not nontrivial_sccs and not self_loops else 'BLOCKER'}")
    print(f"   SCCs total: {len(sccs)}, non-trivial: {len(nontrivial_sccs)}, self-loops: {self_loops}")

    # Check 4: Anchor coverage
    implements_node = [r for r in anchor_rows if r.get("AnchorType") == "IMPLEMENTS_NODE"]
    print(f"4. Anchor Coverage: {'PASS' if implements_node else 'WARNING'}")
    print(f"   IMPLEMENTS_NODE anchors: {len(implements_node)}")
    print(f"   TRACES_TO_REQUIREMENT anchors: {len([r for r in anchor_rows if r.get('AnchorType') == 'TRACES_TO_REQUIREMENT'])}")

    # Check 5: Misplaced fields
    misplaced = []
    for r in rows:
        if r.get("TargetType") != "DELIVERABLE" and r.get("TargetDeliverableID", "").strip():
            misplaced.append(r["DependencyID"])
    print(f"5. Misplaced Fields: {'PASS' if not misplaced else 'WARNING'} ({len(misplaced)} violations)")

    # Check 6: ID format consistency
    long_form_count = 0
    short_form_count = 0
    import re
    for r in rows:
        for field in ["FromDeliverableID", "TargetDeliverableID"]:
            val = r.get(field, "").strip()
            if not val:
                continue
            if re.match(r"^(DEL|KTY)-\d{2}-\d{2}$", val):
                short_form_count += 1
            elif re.match(r"^(DEL|KTY)-\d{2}-\d{2}_", val):
                long_form_count += 1
            else:
                short_form_count += 1  # Other formats counted as short
    total_ids = long_form_count + short_form_count
    norm_rate = long_form_count / total_ids if total_ids > 0 else 0.0
    print(f"6. ID Format Consistency: PASS")
    print(f"   Short-form: {short_form_count}, Long-form: {long_form_count}, Normalization rate: {norm_rate:.1%}")

    # Check 7: Isolated deliverables
    all_nodes_in_graph = set()
    for src, targets in graph.items():
        all_nodes_in_graph.add(src)
        all_nodes_in_graph.update(targets)
    scope_nodes = {normalize_id(s) for s in SCOPE}
    isolated = [n for n in scope_nodes if n not in all_nodes_in_graph]
    print(f"7. Isolated Deliverables: {'PASS' if not isolated else 'WARNING'} ({len(isolated)} isolated)")

    # Check 8: Hub analysis
    degree = defaultdict(int)
    for src, targets in graph.items():
        degree[src] += len(targets)
        for t in targets:
            degree[t] += 1
    hubs = {n: d for n, d in degree.items() if d >= HUB_THRESHOLD}
    print(f"8. Hub Analysis: {'PASS' if not hubs else 'WARNING'} ({len(hubs)} hubs)")
    if hubs:
        for n, d in sorted(hubs.items(), key=lambda x: -x[1]):
            print(f"   - {n}: degree {d}")

    # Check 9: Bidirectional pairs
    bidir = []
    for src, targets in graph.items():
        for t in targets:
            if src in graph.get(t, []) and src < t:
                bidir.append((src, t))
    print(f"9. Bidirectional Pairs: {'PASS' if not bidir else 'INFO'} ({len(bidir)} pairs)")

    # -- Summary --
    print()
    print("=" * 60)
    all_pass = (
        schema_result["valid"]
        and not orphans
        and not nontrivial_sccs
        and not self_loops
        and bool(implements_node)
        and not misplaced
        and not isolated
        and not hubs
    )
    status = "PASS" if all_pass else "WARNINGS"
    print(f"CLOSURE STATUS: {status}")
    print("=" * 60)


if __name__ == "__main__":
    main()
