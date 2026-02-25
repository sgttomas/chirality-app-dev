#!/usr/bin/env python3
"""
Reproducible dependency closure analysis for DEL-01-03.

Snapshot: CLOSURE_DEL-01-03_2026-02-22_0800
Scope: DEL-01-03 (Frontend Workspace Bootstrap & Packaging Baseline)
Source: execution/PKG-01_Build_And_Packaging/1_Working/DEL-01-03_Frontend_Workspace_Bootstrap/Dependencies.csv

Usage:
    python3 analyze_closure.py [--execution-root EXECUTION_ROOT]

Defaults to execution/ relative to the repository root (auto-detected via git).
"""

import csv
import json
import os
import subprocess
import sys
from collections import defaultdict
from pathlib import Path


# --- Configuration ---

SCOPE = ["DEL-01-03"]
FILTER_ACTIVE_ONLY = True
NORMALIZE_IDS = True
EDGE_FILTER_CLASS = "EXECUTION"
EDGE_FILTER_TARGET_TYPE = "DELIVERABLE"
HUB_THRESHOLD = 20
MAX_CYCLES = 10000

REQUIRED_COLUMNS_V31 = [
    "RegisterSchemaVersion", "DependencyID", "FromPackageID",
    "FromDeliverableID", "FromDeliverableName", "DependencyClass",
    "AnchorType", "Direction", "DependencyType", "TargetType",
    "TargetPackageID", "TargetDeliverableID", "TargetRefID",
    "TargetName", "TargetLocation", "Statement", "EvidenceFile",
    "SourceRef", "EvidenceQuote", "Explicitness", "RequiredMaturity",
    "ProposedMaturity", "SatisfactionStatus", "Confidence", "Origin",
    "FirstSeen", "LastSeen", "Status", "Notes",
]


def find_repo_root():
    """Find git repository root."""
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            capture_output=True, text=True, check=True,
        )
        return Path(result.stdout.strip())
    except (subprocess.CalledProcessError, FileNotFoundError):
        return Path.cwd()


def normalize_id(raw_id: str) -> str:
    """Strip descriptive suffix from DEL-XX-YY_Label -> DEL-XX-YY."""
    if not raw_id:
        return raw_id
    parts = raw_id.split("_", 1)
    return parts[0]


def discover_deliverables(execution_root: Path) -> set:
    """Discover all deliverable IDs from folder names."""
    deliverables = set()
    for pkg_dir in sorted(execution_root.glob("PKG-*/1_Working/DEL-*")):
        if pkg_dir.is_dir():
            raw_name = pkg_dir.name
            del_id = normalize_id(raw_name) if NORMALIZE_IDS else raw_name
            deliverables.add(del_id)
    return deliverables


def locate_dependencies_csv(execution_root: Path, del_id: str) -> Path | None:
    """Find Dependencies.csv for a deliverable ID."""
    for pkg_dir in execution_root.glob("PKG-*/1_Working"):
        for del_dir in pkg_dir.glob("DEL-*"):
            folder_id = normalize_id(del_dir.name)
            if folder_id == del_id:
                csv_path = del_dir / "Dependencies.csv"
                if csv_path.is_file():
                    return csv_path
    return None


def validate_schema(headers: list[str]) -> tuple[bool, list[str]]:
    """Check v3.1 required columns are present."""
    missing = [c for c in REQUIRED_COLUMNS_V31 if c not in headers]
    return (len(missing) == 0, missing)


def parse_csv(csv_path: Path) -> list[dict]:
    """Parse Dependencies.csv and return list of row dicts."""
    rows = []
    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)
    return rows


def is_graph_edge(row: dict) -> bool:
    """Check if a row qualifies as a graph edge per EDGE_FILTER."""
    if FILTER_ACTIVE_ONLY and row.get("Status", "") != "ACTIVE":
        return False
    if row.get("DependencyClass", "") != EDGE_FILTER_CLASS:
        return False
    if row.get("TargetType", "") != EDGE_FILTER_TARGET_TYPE:
        return False
    from_id = row.get("FromDeliverableID", "").strip()
    target_id = row.get("TargetDeliverableID", "").strip()
    if not from_id or not target_id:
        return False
    return True


def build_directed_edge(row: dict) -> tuple[str, str]:
    """
    Build a directed edge (source, target) based on Direction.
    DOWNSTREAM from DEL-01-03 means DEL-01-03 -> target (target depends on source).
    UPSTREAM to DEL-01-03 means target -> DEL-01-03 (source depends on target).
    """
    from_id = normalize_id(row["FromDeliverableID"].strip())
    target_id = normalize_id(row["TargetDeliverableID"].strip())
    direction = row.get("Direction", "").strip()

    if direction == "DOWNSTREAM":
        # from_id provides to target_id; edge: from_id -> target_id
        return (from_id, target_id)
    elif direction == "UPSTREAM":
        # from_id depends on target_id; edge: target_id -> from_id
        return (target_id, from_id)
    else:
        # Unknown direction; treat as from -> target
        return (from_id, target_id)


def tarjan_scc(graph: dict[str, set[str]]) -> list[list[str]]:
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

        for w in graph.get(v, set()):
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
            result.append(sorted(component))

    for node in sorted(all_nodes):
        if node not in index:
            strongconnect(node)

    return result


def main():
    import argparse
    parser = argparse.ArgumentParser(description="DEL-01-03 closure analysis")
    parser.add_argument("--execution-root", default=None, help="Path to execution/")
    args = parser.parse_args()

    repo_root = find_repo_root()
    if args.execution_root:
        execution_root = Path(args.execution_root)
    else:
        execution_root = repo_root / "execution"

    if not execution_root.is_dir():
        print(f"ERROR: execution root not found: {execution_root}", file=sys.stderr)
        sys.exit(1)

    # Step 0: Discover workspace deliverables
    workspace_deliverables = discover_deliverables(execution_root)
    print(f"Workspace deliverables: {len(workspace_deliverables)}")

    # Step 1: Locate Dependencies.csv for scope
    coverage = {}
    all_rows = {}
    for del_id in SCOPE:
        csv_path = locate_dependencies_csv(execution_root, del_id)
        if csv_path is None:
            coverage[del_id] = "MISSING_DEPENDENCIES_CSV"
            print(f"  {del_id}: MISSING_DEPENDENCIES_CSV")
            continue

        rows = parse_csv(csv_path)
        if not rows:
            coverage[del_id] = "EMPTY"
            print(f"  {del_id}: EMPTY")
            continue

        # Step 2: Validate schema
        headers = list(rows[0].keys())
        valid, missing_cols = validate_schema(headers)
        if not valid:
            coverage[del_id] = f"SCHEMA_INVALID (missing: {missing_cols})"
            print(f"  {del_id}: SCHEMA_INVALID (missing: {missing_cols})")
            continue

        coverage[del_id] = "OK"
        all_rows[del_id] = rows
        print(f"  {del_id}: OK ({len(rows)} rows)")

    # Step 3: Build graph
    graph = defaultdict(set)  # adjacency list
    edge_details = []  # for reporting

    for del_id, rows in all_rows.items():
        for row in rows:
            if is_graph_edge(row):
                src, tgt = build_directed_edge(row)
                graph[src].add(tgt)
                edge_details.append({
                    "dependency_id": row.get("DependencyID", ""),
                    "from": src,
                    "to": tgt,
                    "direction": row.get("Direction", ""),
                    "type": row.get("DependencyType", ""),
                })

    print(f"\nGraph edges: {len(edge_details)}")
    for e in edge_details:
        print(f"  {e['from']} -> {e['to']} ({e['dependency_id']}, {e['direction']}/{e['type']})")

    # Step 4: Core checks

    # Check 2: Orphans
    orphans = []
    for e in edge_details:
        for node in [e["from"], e["to"]]:
            if node not in workspace_deliverables:
                orphans.append({"node": node, "edge": e["dependency_id"]})
    print(f"\nOrphans: {len(orphans)}")

    # Check 3: SCC / Cycles
    sccs = tarjan_scc(dict(graph))
    non_trivial = [scc for scc in sccs if len(scc) > 1]
    print(f"Non-trivial SCCs: {len(non_trivial)}")
    for scc in non_trivial:
        print(f"  SCC: {scc}")

    # Check 4: Anchor coverage
    for del_id, rows in all_rows.items():
        anchors = [r for r in rows if r.get("DependencyClass") == "ANCHOR"]
        implements = [r for r in anchors if r.get("AnchorType") == "IMPLEMENTS_NODE"]
        print(f"\nAnchor coverage for {del_id}: {len(anchors)} anchors, "
              f"{len(implements)} IMPLEMENTS_NODE")

    # Check 7: Isolated deliverables
    connected_nodes = set()
    for e in edge_details:
        connected_nodes.add(e["from"])
        connected_nodes.add(e["to"])
    for del_id in SCOPE:
        if del_id not in connected_nodes:
            print(f"\nISOLATED: {del_id}")
        else:
            print(f"\n{del_id}: connected (degree {sum(1 for e in edge_details if e['from'] == del_id or e['to'] == del_id)})")

    # Check 8: Hub analysis
    degree_count = defaultdict(int)
    for e in edge_details:
        degree_count[e["from"]] += 1
        degree_count[e["to"]] += 1
    hubs = {n: d for n, d in degree_count.items() if d >= HUB_THRESHOLD}
    print(f"\nHubs (threshold={HUB_THRESHOLD}): {len(hubs)}")

    # Check 9: Bidirectional pairs
    edge_set = set()
    for e in edge_details:
        edge_set.add((e["from"], e["to"]))
    bidir = []
    seen = set()
    for (a, b) in edge_set:
        if (b, a) in edge_set and (b, a) not in seen:
            bidir.append((a, b))
            seen.add((a, b))
    print(f"Bidirectional pairs: {len(bidir)}")
    for a, b in bidir:
        print(f"  {a} <-> {b}")

    # Summary
    status = "PASS"
    if non_trivial or orphans:
        status = "WARNING"

    print(f"\n=== OVERALL STATUS: {status} ===")

    # Write JSON summary
    summary = {
        "scope": SCOPE,
        "overall_status": status,
        "workspace_deliverables": len(workspace_deliverables),
        "graph_edges": len(edge_details),
        "orphans": len(orphans),
        "non_trivial_sccs": len(non_trivial),
        "bidirectional_pairs": len(bidir),
        "hubs": len(hubs),
    }
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
