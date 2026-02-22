#!/usr/bin/env python3
"""
analyze_closure.py -- Reproducible dependency closure analysis for DEL-08-04

Run label: DEL-08-04
Snapshot: CLOSURE_DEL-08-04_2026-02-21
Date: 2026-02-21

This script reproduces the dependency closure analysis performed by
AUDIT_DEP_CLOSURE for the DEL-08-04 deliverable. It reads the
Dependencies.csv from the deliverable folder, applies the same filters
and checks, and prints results to stdout.

Usage:
    python3 analyze_closure.py [--execution-root PATH]

Default execution root: ../../.. (relative to this script's location,
resolving to the execution/ folder).
"""

import csv
import json
import os
import sys
import argparse
from collections import defaultdict
from pathlib import Path


# --- Configuration (matches the run parameters) ---
SCOPE = ["DEL-08-04"]
FILTER_ACTIVE_ONLY = True
NORMALIZE_IDS = True
EDGE_FILTER_DEP_CLASS = "EXECUTION"
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

EXPECTED_COLUMNS_V31 = [
    "RegisterSchemaVersion", "DependencyID", "FromPackageID", "FromDeliverableID",
    "FromDeliverableName", "DependencyClass", "AnchorType", "Direction",
    "DependencyType", "TargetType", "TargetPackageID", "TargetDeliverableID",
    "TargetRefID", "TargetName", "TargetLocation", "Statement", "EvidenceFile",
    "SourceRef", "EvidenceQuote", "Explicitness", "RequiredMaturity",
    "ProposedMaturity", "SatisfactionStatus", "Confidence", "Origin",
    "FirstSeen", "LastSeen", "Status", "Notes",
]

# Deliverable path mapping
DELIVERABLE_PATHS = {
    "DEL-08-04": "PKG-08_Optional_Integrity_Hardening/1_Working/DEL-08-04_Dependency_Graph_Generator",
}


def normalize_id(raw_id: str) -> str:
    """Strip descriptive suffix from a deliverable ID if present."""
    if not raw_id:
        return raw_id
    # Match DEL-XX-YY or DEL-XXX-YY prefix
    parts = raw_id.split("_", 1)
    if parts[0].startswith("DEL-"):
        return parts[0]
    if parts[0].startswith("KTY-"):
        return parts[0]
    return raw_id


def load_dependencies_csv(filepath: str) -> list[dict]:
    """Load and parse a Dependencies.csv file."""
    rows = []
    with open(filepath, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)
    return rows


def validate_schema(rows: list[dict], filepath: str) -> tuple[bool, list[str]]:
    """Check that the CSV has all required v3.1 columns."""
    if not rows:
        return False, ["Empty CSV"]
    actual_cols = list(rows[0].keys())
    missing = [c for c in EXPECTED_COLUMNS_V31 if c not in actual_cols]
    if missing:
        return False, [f"Missing columns: {missing}"]
    # Check schema version
    versions = set(r.get("RegisterSchemaVersion", "") for r in rows)
    if versions != {"v3.1"}:
        return False, [f"Unexpected schema versions: {versions}"]
    return True, []


def build_edges(rows: list[dict]) -> list[dict]:
    """Extract edges matching the edge filter."""
    edges = []
    for row in rows:
        if FILTER_ACTIVE_ONLY and row.get("Status", "").strip() != "ACTIVE":
            continue
        if row.get("DependencyClass", "").strip() != EDGE_FILTER_DEP_CLASS:
            continue
        if row.get("TargetType", "").strip() != EDGE_FILTER_TARGET_TYPE:
            continue

        from_id = row.get("FromDeliverableID", "").strip()
        target_id = row.get("TargetDeliverableID", "").strip()

        if NORMALIZE_IDS:
            from_id = normalize_id(from_id)
            target_id = normalize_id(target_id)

        if not from_id or not target_id:
            continue  # Skip rows with missing IDs

        direction = row.get("Direction", "").strip()
        dep_id = row.get("DependencyID", "").strip()
        dep_type = row.get("DependencyType", "").strip()

        # Determine edge direction
        if direction == "DOWNSTREAM":
            edges.append({
                "dependency_id": dep_id,
                "from": from_id,
                "to": target_id,
                "direction": direction,
                "type": dep_type,
            })
        else:  # UPSTREAM: target provides to from
            edges.append({
                "dependency_id": dep_id,
                "from": target_id,
                "to": from_id,
                "direction": direction,
                "type": dep_type,
            })
    return edges


def check_orphans(edges: list[dict]) -> list[dict]:
    """Find edges where target is not in the valid deliverable set."""
    orphans = []
    for e in edges:
        if e["to"] not in VALID_DELIVERABLE_IDS:
            orphans.append(e)
        if e["from"] not in VALID_DELIVERABLE_IDS:
            orphans.append(e)
    return orphans


def check_cycles_tarjan(edges: list[dict]) -> list[list[str]]:
    """Detect SCCs using Tarjan's algorithm."""
    graph = defaultdict(list)
    nodes = set()
    for e in edges:
        graph[e["from"]].append(e["to"])
        nodes.add(e["from"])
        nodes.add(e["to"])

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
            if len(scc) > 1:
                sccs.append(scc)

    for node in sorted(nodes):
        if node not in index:
            strongconnect(node)

    return sccs


def check_anchors(rows: list[dict]) -> dict:
    """Check for IMPLEMENTS_NODE anchor rows."""
    implements = [r for r in rows
                  if r.get("DependencyClass", "").strip() == "ANCHOR"
                  and r.get("AnchorType", "").strip() == "IMPLEMENTS_NODE"]
    return {
        "has_implements_node": len(implements) > 0,
        "count": len(implements),
        "ids": [r.get("DependencyID", "") for r in implements],
    }


def check_misplaced_fields(rows: list[dict]) -> list[dict]:
    """Find rows where TargetType=DELIVERABLE but TargetDeliverableID is empty,
    or TargetType!=DELIVERABLE but TargetDeliverableID is non-empty."""
    issues = []
    for row in rows:
        target_type = row.get("TargetType", "").strip()
        target_del_id = row.get("TargetDeliverableID", "").strip()
        dep_id = row.get("DependencyID", "").strip()

        if target_type == "DELIVERABLE" and not target_del_id:
            issues.append({
                "dependency_id": dep_id,
                "issue": "TargetType=DELIVERABLE but TargetDeliverableID is empty",
                "target_type": target_type,
            })
        elif target_type != "DELIVERABLE" and target_del_id:
            issues.append({
                "dependency_id": dep_id,
                "issue": "TargetType!=DELIVERABLE but TargetDeliverableID is non-empty",
                "target_type": target_type,
                "target_deliverable_id": target_del_id,
            })
    return issues


def check_id_format(rows: list[dict]) -> dict:
    """Check for long-form IDs."""
    long_form = []
    total = 0
    for row in rows:
        for field in ["FromDeliverableID", "TargetDeliverableID"]:
            val = row.get(field, "").strip()
            if not val:
                continue
            total += 1
            normalized = normalize_id(val)
            if normalized != val:
                long_form.append({
                    "dependency_id": row.get("DependencyID", ""),
                    "field": field,
                    "original": val,
                    "normalized": normalized,
                })
    return {
        "total_id_values": total,
        "long_form_count": len(long_form),
        "long_form_entries": long_form,
    }


def check_hubs(edges: list[dict], threshold: int) -> list[dict]:
    """Find nodes with degree >= threshold."""
    degree = defaultdict(lambda: {"in": 0, "out": 0})
    for e in edges:
        degree[e["from"]]["out"] += 1
        degree[e["to"]]["in"] += 1
    hubs = []
    for node, d in sorted(degree.items()):
        total = d["in"] + d["out"]
        hubs.append({
            "node": node,
            "in_degree": d["in"],
            "out_degree": d["out"],
            "total_degree": total,
            "exceeds_threshold": total >= threshold,
        })
    return hubs


def check_bidirectional(edges: list[dict]) -> list[dict]:
    """Find A->B and B->A pairs."""
    edge_set = set()
    for e in edges:
        edge_set.add((e["from"], e["to"]))
    pairs = []
    seen = set()
    for a, b in edge_set:
        if (b, a) in edge_set and (b, a) not in seen:
            pairs.append({"node_a": a, "node_b": b})
            seen.add((a, b))
    return pairs


def main():
    parser = argparse.ArgumentParser(description="Dependency closure analysis for DEL-08-04")
    parser.add_argument("--execution-root", default=None,
                        help="Path to execution root (default: auto-detect)")
    args = parser.parse_args()

    # Resolve execution root
    if args.execution_root:
        exec_root = Path(args.execution_root)
    else:
        script_dir = Path(__file__).resolve().parent
        # Script is in execution/_Reconciliation/DepClosure/CLOSURE_*/
        exec_root = script_dir.parent.parent.parent

    print(f"Execution root: {exec_root}")
    print(f"Scope: {SCOPE}")
    print()

    # Load Dependencies.csv
    for del_id in SCOPE:
        rel_path = DELIVERABLE_PATHS.get(del_id)
        if not rel_path:
            print(f"ERROR: No path mapping for {del_id}")
            continue

        csv_path = exec_root / rel_path / "Dependencies.csv"
        if not csv_path.exists():
            print(f"MISSING: {csv_path}")
            continue

        print(f"--- {del_id} ---")
        print(f"CSV: {csv_path}")

        rows = load_dependencies_csv(str(csv_path))
        print(f"Rows: {len(rows)}")

        # Check 1: Schema
        valid, errors = validate_schema(rows, str(csv_path))
        print(f"\nCheck 1 - Schema Compliance: {'PASS' if valid else 'FAIL'}")
        if errors:
            for e in errors:
                print(f"  ERROR: {e}")

        # Build edges
        edges = build_edges(rows)
        print(f"\nEdges (after filter): {len(edges)}")
        for e in edges:
            print(f"  {e['from']} -> {e['to']} ({e['dependency_id']}, {e['direction']}, {e['type']})")

        # Check 2: Orphans
        orphans = check_orphans(edges)
        print(f"\nCheck 2 - Orphan Dependencies: {'PASS' if not orphans else 'WARNING'}")
        if orphans:
            for o in orphans:
                print(f"  ORPHAN: {o}")

        # Check 3: Cycles
        sccs = check_cycles_tarjan(edges)
        print(f"\nCheck 3 - Circular Dependencies: {'PASS' if not sccs else 'BLOCKER'}")
        if sccs:
            for scc in sccs:
                print(f"  SCC: {scc}")

        # Check 4: Anchors
        anchor_info = check_anchors(rows)
        print(f"\nCheck 4 - Anchor Coverage: {'PASS' if anchor_info['has_implements_node'] else 'WARNING'}")
        print(f"  IMPLEMENTS_NODE count: {anchor_info['count']}")
        print(f"  IDs: {anchor_info['ids']}")

        # Check 5: Misplaced fields
        misplaced = check_misplaced_fields(rows)
        print(f"\nCheck 5 - Misplaced Fields: {'PASS' if not misplaced else 'WARNING'}")
        if misplaced:
            for m in misplaced:
                print(f"  ISSUE: {m}")

        # Check 6: ID format
        id_info = check_id_format(rows)
        print(f"\nCheck 6 - ID Format Consistency: {'PASS' if id_info['long_form_count'] == 0 else 'WARNING'}")
        print(f"  Total ID values: {id_info['total_id_values']}")
        print(f"  Long-form count: {id_info['long_form_count']}")

        # Check 7: Isolated
        nodes_with_edges = set()
        for e in edges:
            nodes_with_edges.add(e["from"])
            nodes_with_edges.add(e["to"])
        isolated = [d for d in SCOPE if d not in nodes_with_edges]
        print(f"\nCheck 7 - Isolated Deliverables: {'PASS' if not isolated else 'WARNING'}")
        if isolated:
            print(f"  Isolated: {isolated}")

        # Check 8: Hubs
        hub_info = check_hubs(edges, HUB_THRESHOLD)
        has_hubs = any(h["exceeds_threshold"] for h in hub_info)
        print(f"\nCheck 8 - Hub Analysis: {'WARNING' if has_hubs else 'PASS'}")
        for h in hub_info:
            marker = " [HUB]" if h["exceeds_threshold"] else ""
            print(f"  {h['node']}: in={h['in_degree']} out={h['out_degree']} total={h['total_degree']}{marker}")

        # Check 9: Bidirectional
        bidir = check_bidirectional(edges)
        print(f"\nCheck 9 - Bidirectional Pairs: {'INFO' if bidir else 'PASS'}")
        if bidir:
            for b in bidir:
                print(f"  PAIR: {b['node_a']} <-> {b['node_b']}")

    print("\n--- Analysis complete ---")


if __name__ == "__main__":
    main()
