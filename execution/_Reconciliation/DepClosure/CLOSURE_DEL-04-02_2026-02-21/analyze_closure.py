#!/usr/bin/env python3
"""
Reproducible dependency closure analysis for DEL-04-02.

Run Label: DEL-04-02
Snapshot: CLOSURE_DEL-04-02_2026-02-21
Scope: Single deliverable (DEL-04-02)

This script reproduces the closure analysis performed by AUDIT_DEP_CLOSURE.
It reads the Dependencies.csv for DEL-04-02, builds the dependency graph,
and runs all 9 core checks.

Usage:
    python analyze_closure.py [--execution-root PATH]

Defaults:
    --execution-root: execution/  (relative to repo root)
"""

import csv
import json
import os
import re
import sys
from collections import defaultdict
from pathlib import Path

# --- Configuration ---

SCOPE = ["DEL-04-02"]
FILTER_ACTIVE_ONLY = True
NORMALIZE_IDS = True
EDGE_FILTER_DEPENDENCY_CLASS = "EXECUTION"
EDGE_FILTER_TARGET_TYPE = "DELIVERABLE"
HUB_THRESHOLD = 20
MAX_CYCLES = 10000

# All 32 valid deliverable IDs in the workspace
VALID_DELIVERABLE_IDS = [
    "DEL-01-01", "DEL-01-02",
    "DEL-02-01", "DEL-02-02", "DEL-02-03", "DEL-02-04",
    "DEL-03-01", "DEL-03-02", "DEL-03-03", "DEL-03-04", "DEL-03-05", "DEL-03-06",
    "DEL-04-01", "DEL-04-02",
    "DEL-05-01", "DEL-05-02", "DEL-05-03", "DEL-05-04",
    "DEL-06-01", "DEL-06-02", "DEL-06-03", "DEL-06-04", "DEL-06-05",
    "DEL-07-01", "DEL-07-02",
    "DEL-08-01", "DEL-08-02", "DEL-08-03", "DEL-08-04", "DEL-08-05", "DEL-08-06", "DEL-08-07",
]

# Deliverable path mapping (scope deliverables only)
DELIVERABLE_PATHS = {
    "DEL-04-02": "PKG-04_Attachments_Multimodal/1_Working/DEL-04-02_UI_Attachment_Pipeline",
}

# v3.1 required columns
REQUIRED_COLUMNS_V31 = [
    "RegisterSchemaVersion", "DependencyID", "FromPackageID", "FromDeliverableID",
    "FromDeliverableName", "DependencyClass", "AnchorType", "Direction",
    "DependencyType", "TargetType", "TargetPackageID", "TargetDeliverableID",
    "TargetRefID", "TargetName", "TargetLocation", "Statement", "EvidenceFile",
    "SourceRef", "EvidenceQuote", "Explicitness", "RequiredMaturity",
    "ProposedMaturity", "SatisfactionStatus", "Confidence", "Origin",
    "FirstSeen", "LastSeen", "Status", "Notes",
]


def normalize_id(raw_id: str) -> str:
    """Normalize long-form IDs by stripping descriptive suffixes."""
    if not raw_id:
        return raw_id
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

    for v in graph:
        if v not in index:
            strongconnect(v)

    return sccs


def main():
    import argparse
    parser = argparse.ArgumentParser(description="DEL-04-02 Dependency Closure Analysis")
    parser.add_argument("--execution-root", default="execution/",
                        help="Path to execution root (default: execution/)")
    args = parser.parse_args()

    exec_root = Path(args.execution_root)

    print("=" * 70)
    print("DEPENDENCY CLOSURE ANALYSIS -- DEL-04-02")
    print("=" * 70)

    # --- Step 1: Locate and read Dependencies.csv ---
    coverage = {}
    all_rows = []

    for del_id, rel_path in DELIVERABLE_PATHS.items():
        csv_path = exec_root / rel_path / "Dependencies.csv"
        if not csv_path.exists():
            coverage[del_id] = "MISSING_DEPENDENCIES_CSV"
            print(f"  [{del_id}] MISSING: {csv_path}")
            continue

        try:
            with open(csv_path, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                rows = list(reader)
                coverage[del_id] = "READABLE"
                all_rows.extend(rows)
                print(f"  [{del_id}] READABLE: {len(rows)} rows")
        except Exception as e:
            coverage[del_id] = f"UNREADABLE: {e}"
            print(f"  [{del_id}] UNREADABLE: {e}")

    # --- Step 2: Schema validation ---
    schema_valid = {}
    for del_id in DELIVERABLE_PATHS:
        if coverage.get(del_id) != "READABLE":
            schema_valid[del_id] = False
            continue

        del_rows = [r for r in all_rows if r.get("FromDeliverableID", "").startswith(del_id)]
        if not del_rows:
            schema_valid[del_id] = False
            continue

        # Check columns
        actual_cols = list(del_rows[0].keys())
        missing_cols = [c for c in REQUIRED_COLUMNS_V31 if c not in actual_cols]
        if missing_cols:
            print(f"  [{del_id}] SCHEMA_INVALID: missing columns {missing_cols}")
            schema_valid[del_id] = False
        else:
            schema_valid[del_id] = True
            print(f"  [{del_id}] SCHEMA_VALID (v3.1)")

    # --- Step 3: Build graph ---
    nodes = set()
    edges = []

    for row in all_rows:
        from_id = row.get("FromDeliverableID", "").strip()
        target_id = row.get("TargetDeliverableID", "").strip()
        dep_class = row.get("DependencyClass", "").strip()
        target_type = row.get("TargetType", "").strip()
        status = row.get("Status", "").strip()
        dep_id = row.get("DependencyID", "").strip()

        if NORMALIZE_IDS:
            from_id = normalize_id(from_id)
            target_id = normalize_id(target_id)

        # Add source node
        if from_id:
            nodes.add(from_id)

        # Apply filters
        if FILTER_ACTIVE_ONLY and status != "ACTIVE":
            continue
        if dep_class != EDGE_FILTER_DEPENDENCY_CLASS:
            continue
        if target_type != EDGE_FILTER_TARGET_TYPE:
            continue
        if not from_id or not target_id:
            continue

        nodes.add(target_id)
        edges.append({
            "dependency_id": dep_id,
            "from": from_id,
            "to": target_id,
            "direction": row.get("Direction", "").strip(),
            "dependency_type": row.get("DependencyType", "").strip(),
            "confidence": row.get("Confidence", "").strip(),
        })

    print(f"\nGraph: {len(nodes)} nodes, {len(edges)} edges")

    # --- Step 4: Core checks ---
    results = {}

    # Check 1: Schema compliance
    readable_count = sum(1 for v in coverage.values() if v == "READABLE")
    valid_count = sum(1 for v in schema_valid.values() if v)
    results["schema_compliance"] = {
        "verdict": "PASS" if valid_count == len(DELIVERABLE_PATHS) else "WARNING",
        "readable": readable_count,
        "valid": valid_count,
        "total": len(DELIVERABLE_PATHS),
    }
    print(f"\n[Check 1] Schema Compliance: {results['schema_compliance']['verdict']}")

    # Check 2: Orphan dependencies
    orphans = []
    for edge in edges:
        if edge["to"] not in VALID_DELIVERABLE_IDS:
            orphans.append(edge)
    results["orphan_dependencies"] = {
        "verdict": "PASS" if not orphans else "WARNING",
        "count": len(orphans),
    }
    print(f"[Check 2] Orphan Dependencies: {results['orphan_dependencies']['verdict']} ({len(orphans)} orphans)")

    # Check 3: Circular dependencies (Tarjan SCC)
    adj = defaultdict(list)
    all_graph_nodes = set()
    for edge in edges:
        adj[edge["from"]].append(edge["to"])
        all_graph_nodes.add(edge["from"])
        all_graph_nodes.add(edge["to"])

    # Ensure all nodes are in adj
    for n in all_graph_nodes:
        if n not in adj:
            adj[n] = []

    sccs = tarjan_scc(dict(adj))
    nontrivial_sccs = [s for s in sccs if len(s) > 1]
    results["circular_dependencies"] = {
        "verdict": "PASS" if not nontrivial_sccs else "BLOCKER",
        "cycle_count": len(nontrivial_sccs),
        "max_scc_size": max((len(s) for s in sccs), default=0),
    }
    print(f"[Check 3] Circular Dependencies: {results['circular_dependencies']['verdict']} ({len(nontrivial_sccs)} non-trivial SCCs)")

    # Check 4: Anchor coverage
    anchor_rows = [r for r in all_rows
                   if r.get("DependencyClass", "").strip() == "ANCHOR"
                   and r.get("AnchorType", "").strip() == "IMPLEMENTS_NODE"]
    dels_with_anchor = set()
    for r in anchor_rows:
        fid = normalize_id(r.get("FromDeliverableID", "").strip()) if NORMALIZE_IDS else r.get("FromDeliverableID", "").strip()
        dels_with_anchor.add(fid)

    missing_anchor = [d for d in SCOPE if d not in dels_with_anchor]
    results["anchor_coverage"] = {
        "verdict": "PASS" if not missing_anchor else "WARNING",
        "with_anchor": len(dels_with_anchor),
        "missing": missing_anchor,
    }
    print(f"[Check 4] Anchor Coverage: {results['anchor_coverage']['verdict']}")

    # Check 5: Misplaced fields
    misplaced = []
    for row in all_rows:
        target_type = row.get("TargetType", "").strip()
        target_del_id = row.get("TargetDeliverableID", "").strip()
        if target_type != "DELIVERABLE" and target_del_id:
            misplaced.append(row.get("DependencyID", ""))
    results["misplaced_fields"] = {
        "verdict": "PASS" if not misplaced else "WARNING",
        "count": len(misplaced),
    }
    print(f"[Check 5] Misplaced Fields: {results['misplaced_fields']['verdict']} ({len(misplaced)} misplaced)")

    # Check 6: ID format consistency
    all_ids = set()
    for row in all_rows:
        fid = row.get("FromDeliverableID", "").strip()
        tid = row.get("TargetDeliverableID", "").strip()
        if fid:
            all_ids.add(fid)
        if tid:
            all_ids.add(tid)

    normalized_count = 0
    for raw_id in all_ids:
        norm = normalize_id(raw_id)
        if norm != raw_id:
            normalized_count += 1

    results["id_format_consistency"] = {
        "verdict": "PASS" if normalized_count == 0 else "WARNING",
        "total_ids": len(all_ids),
        "normalized": normalized_count,
    }
    print(f"[Check 6] ID Format Consistency: {results['id_format_consistency']['verdict']} ({normalized_count}/{len(all_ids)} needed normalization)")

    # Check 7: Isolated deliverables
    connected = set()
    for edge in edges:
        connected.add(edge["from"])
        connected.add(edge["to"])
    isolated = [d for d in SCOPE if d not in connected]
    results["isolated_deliverables"] = {
        "verdict": "PASS" if not isolated else "WARNING",
        "isolated": isolated,
    }
    print(f"[Check 7] Isolated Deliverables: {results['isolated_deliverables']['verdict']}")

    # Check 8: Hub analysis
    degree = defaultdict(lambda: {"in": 0, "out": 0})
    for edge in edges:
        degree[edge["from"]]["out"] += 1
        degree[edge["to"]]["in"] += 1
    hubs = {n: d["in"] + d["out"] for n, d in degree.items() if d["in"] + d["out"] >= HUB_THRESHOLD}
    results["hub_analysis"] = {
        "verdict": "PASS" if not hubs else "WARNING",
        "hub_count": len(hubs),
        "threshold": HUB_THRESHOLD,
    }
    print(f"[Check 8] Hub Analysis: {results['hub_analysis']['verdict']} ({len(hubs)} hubs, threshold={HUB_THRESHOLD})")

    # Check 9: Bidirectional pairs
    edge_set = set()
    for edge in edges:
        edge_set.add((edge["from"], edge["to"]))
    bidir = [(a, b) for (a, b) in edge_set if (b, a) in edge_set and a < b]
    results["bidirectional_pairs"] = {
        "verdict": "PASS" if not bidir else "INFO",
        "count": len(bidir),
    }
    print(f"[Check 9] Bidirectional Pairs: {results['bidirectional_pairs']['verdict']} ({len(bidir)} pairs)")

    # --- Overall verdict ---
    verdicts = [r["verdict"] for r in results.values()]
    if "BLOCKER" in verdicts:
        overall = "BLOCKER"
    elif "WARNING" in verdicts:
        overall = "WARNINGS"
    else:
        overall = "PASS"

    print(f"\n{'=' * 70}")
    print(f"OVERALL CLOSURE STATUS: {overall}")
    print(f"{'=' * 70}")

    return 0 if overall == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
