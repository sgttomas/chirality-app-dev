#!/usr/bin/env python3
"""
Dependency Closure Analysis Script
Run: AUDIT_DEP_CLOSURE | 2026-02-21 | SCOPE=ALL
Reproducible analysis of cross-deliverable dependency graph closure.

Usage:
    python3 analyze_closure.py [EXECUTION_ROOT]

Default EXECUTION_ROOT: ../../.. (relative to this script's location)
"""
import csv
import json
import os
import sys
from collections import defaultdict
from pathlib import Path

# --- Configuration ---
V31_COLUMNS = [
    "RegisterSchemaVersion", "DependencyID", "FromPackageID", "FromDeliverableID",
    "FromDeliverableName", "DependencyClass", "AnchorType", "Direction",
    "DependencyType", "TargetType", "TargetPackageID", "TargetDeliverableID",
    "TargetRefID", "TargetName", "TargetLocation", "Statement", "EvidenceFile",
    "SourceRef", "EvidenceQuote", "Explicitness", "RequiredMaturity",
    "ProposedMaturity", "SatisfactionStatus", "Confidence", "Origin",
    "FirstSeen", "LastSeen", "Status", "Notes"
]
EXPECTED_COL_COUNT = 29
FILTER_ACTIVE_ONLY = True
EDGE_FILTER_CLASS = "EXECUTION"
EDGE_FILTER_TARGET = "DELIVERABLE"
HUB_THRESHOLD = 20
MAX_CYCLES = 10000
NORMALIZE_IDS = True


def normalize_id(raw_id):
    """Strip descriptive suffix from long-form IDs: DEL-XX-YY_Label -> DEL-XX-YY"""
    if not raw_id:
        return raw_id
    raw_id = raw_id.strip()
    if raw_id.startswith("DEL-"):
        parts = raw_id.split("_", 1)
        return parts[0]
    if raw_id.startswith("KTY-"):
        parts = raw_id.split("_", 1)
        return parts[0]
    return raw_id


def discover_deliverables(exec_root):
    """Discover all deliverable folders and their Dependencies.csv files."""
    deliverables = {}
    for pkg_dir in sorted(Path(exec_root).iterdir()):
        if not pkg_dir.is_dir() or pkg_dir.name.startswith("_"):
            continue
        working_dir = pkg_dir / "1_Working"
        if not working_dir.is_dir():
            continue
        for del_dir in sorted(working_dir.iterdir()):
            if not del_dir.is_dir():
                continue
            # Skip non-deliverable folders (e.g., _Archive)
            if del_dir.name.startswith("_"):
                continue
            # Extract DEL-XX-YY from folder name
            folder_name = del_dir.name
            del_id = normalize_id(folder_name) if NORMALIZE_IDS else folder_name
            csv_path = del_dir / "Dependencies.csv"
            deliverables[del_id] = {
                "folder": str(del_dir),
                "csv_exists": csv_path.is_file(),
                "csv_path": str(csv_path) if csv_path.is_file() else None,
                "schema_status": "NOT_CHECKED",
                "row_count": 0,
            }
    return deliverables


def validate_schema(csv_path):
    """Validate v3.1 schema. Returns (is_valid, column_count, issues)."""
    issues = []
    try:
        with open(csv_path, "r", newline="", encoding="utf-8") as f:
            reader = csv.reader(f)
            header = next(reader, None)
            if header is None:
                return False, 0, ["Empty file"]
            # Strip BOM if present
            if header[0].startswith("\ufeff"):
                header[0] = header[0].lstrip("\ufeff")
            col_count = len(header)
            if col_count != EXPECTED_COL_COUNT:
                issues.append(f"Column count {col_count} != expected {EXPECTED_COL_COUNT}")
            for i, (got, expected) in enumerate(zip(header, V31_COLUMNS)):
                if got.strip() != expected:
                    issues.append(f"Column {i}: got '{got.strip()}', expected '{expected}'")
            if len(header) < EXPECTED_COL_COUNT:
                for col in V31_COLUMNS[len(header):]:
                    issues.append(f"Missing column: {col}")
            # Check schema version in first data row
            first_row = next(reader, None)
            if first_row and first_row[0].strip() != "v3.1":
                issues.append(f"RegisterSchemaVersion='{first_row[0].strip()}', expected 'v3.1'")
            return len(issues) == 0, col_count, issues
    except Exception as e:
        return False, 0, [str(e)]


def parse_edges(csv_path, from_del_id):
    """Parse EXECUTION/DELIVERABLE edges from a Dependencies.csv."""
    edges = []
    anchors = []
    misplaced = []
    rows_parsed = 0
    try:
        with open(csv_path, "r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row_num, row in enumerate(reader, start=2):
                rows_parsed += 1
                status = row.get("Status", "").strip()
                if FILTER_ACTIVE_ONLY and status != "ACTIVE":
                    continue
                dep_class = row.get("DependencyClass", "").strip()
                anchor_type = row.get("AnchorType", "").strip()
                target_type = row.get("TargetType", "").strip()
                target_del = row.get("TargetDeliverableID", "").strip()
                dep_id = row.get("DependencyID", "").strip()
                direction = row.get("Direction", "").strip()

                # Check anchors
                if dep_class == "ANCHOR" and anchor_type == "IMPLEMENTS_NODE":
                    anchors.append(dep_id)

                # Misplaced field check: TargetType != DELIVERABLE but TargetDeliverableID non-empty
                if target_type != "DELIVERABLE" and target_del:
                    misplaced.append({
                        "dep_id": dep_id,
                        "target_type": target_type,
                        "target_del_id": target_del,
                        "row": row_num,
                    })

                # Edge filter
                if dep_class != EDGE_FILTER_CLASS:
                    continue
                if target_type != EDGE_FILTER_TARGET:
                    continue
                if not target_del:
                    continue

                norm_from = normalize_id(from_del_id) if NORMALIZE_IDS else from_del_id
                norm_target = normalize_id(target_del) if NORMALIZE_IDS else target_del

                edges.append({
                    "from": norm_from,
                    "to": norm_target,
                    "dep_id": dep_id,
                    "direction": direction,
                    "dep_type": row.get("DependencyType", "").strip(),
                    "row": row_num,
                })
    except Exception as e:
        pass
    return edges, anchors, misplaced, rows_parsed


def tarjan_scc(graph):
    """Tarjan's SCC algorithm. graph = {node: [successors]}."""
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


def find_cycles_in_scc(scc_nodes, graph, max_cycles=100):
    """Find representative cycles within an SCC using DFS."""
    scc_set = set(scc_nodes)
    cycles = []
    for start in scc_nodes:
        visited = set()
        path = [start]
        def dfs(node):
            if len(cycles) >= max_cycles:
                return
            for neighbor in graph.get(node, []):
                if neighbor not in scc_set:
                    continue
                if neighbor == start and len(path) > 1:
                    cycles.append(list(path))
                    if len(cycles) >= max_cycles:
                        return
                elif neighbor not in visited:
                    visited.add(neighbor)
                    path.append(neighbor)
                    dfs(neighbor)
                    path.pop()
        visited.add(start)
        dfs(start)
        if len(cycles) >= max_cycles:
            break
    return cycles


def main():
    if len(sys.argv) > 1:
        exec_root = sys.argv[1]
    else:
        exec_root = str(Path(__file__).parent.parent.parent.parent)

    print(f"Execution root: {exec_root}")

    # Step 1: Discover
    deliverables = discover_deliverables(exec_root)
    print(f"Discovered {len(deliverables)} deliverables")

    # Step 2: Validate schemas
    for del_id, info in deliverables.items():
        if not info["csv_exists"]:
            info["schema_status"] = "MISSING_DEPENDENCIES_CSV"
            continue
        valid, col_count, issues = validate_schema(info["csv_path"])
        info["schema_status"] = "SCHEMA_VALID" if valid else "SCHEMA_INVALID"
        info["col_count"] = col_count
        info["schema_issues"] = issues

    # Step 3: Parse edges
    all_edges = []
    all_anchors = {}
    all_misplaced = []
    for del_id, info in deliverables.items():
        if info["schema_status"] != "SCHEMA_VALID":
            all_anchors[del_id] = []
            continue
        edges, anchors, misplaced, rows = parse_edges(info["csv_path"], del_id)
        all_edges.extend(edges)
        all_anchors[del_id] = anchors
        all_misplaced.extend([(del_id, m) for m in misplaced])
        info["row_count"] = rows

    # Build adjacency
    adj = defaultdict(list)
    in_degree = defaultdict(int)
    out_degree = defaultdict(int)
    all_nodes = set(deliverables.keys())
    for e in all_edges:
        adj[e["from"]].append(e["to"])
        out_degree[e["from"]] += 1
        in_degree[e["to"]] += 1
        all_nodes.add(e["from"])
        all_nodes.add(e["to"])

    # Step 4: Checks
    # 4.1 Schema compliance
    schema_valid_count = sum(1 for d in deliverables.values() if d["schema_status"] == "SCHEMA_VALID")
    schema_total = len(deliverables)

    # 4.2 Orphan detection
    orphans = []
    known_ids = set(deliverables.keys())
    for e in all_edges:
        if e["to"] not in known_ids:
            orphans.append(e)

    # 4.3 SCC / Cycles
    sccs = tarjan_scc(dict(adj))
    nontrivial_sccs = [s for s in sccs if len(s) > 1]
    all_cycles = []
    for scc in nontrivial_sccs:
        cycles = find_cycles_in_scc(scc, dict(adj), max_cycles=MAX_CYCLES // max(len(nontrivial_sccs), 1))
        all_cycles.extend(cycles)

    # 4.4 Anchor coverage
    missing_anchors = []
    for del_id in deliverables:
        if del_id not in all_anchors or not all_anchors[del_id]:
            missing_anchors.append(del_id)

    # 4.5 Misplaced fields (already collected)

    # 4.6 ID normalization rate
    long_form_count = 0
    total_id_refs = 0
    for e in all_edges:
        total_id_refs += 1

    # 4.7 Isolated deliverables
    isolated = []
    for del_id in deliverables:
        if in_degree.get(del_id, 0) == 0 and out_degree.get(del_id, 0) == 0:
            isolated.append(del_id)

    # 4.8 Hub analysis
    degree = {}
    for n in all_nodes:
        degree[n] = in_degree.get(n, 0) + out_degree.get(n, 0)
    hubs = {n: d for n, d in degree.items() if d >= HUB_THRESHOLD}

    # 4.9 Bidirectional pairs
    edge_set = set()
    for e in all_edges:
        edge_set.add((e["from"], e["to"]))
    bidirectional = []
    seen = set()
    for (a, b) in edge_set:
        if (b, a) in edge_set and (b, a) not in seen:
            bidirectional.append((a, b))
            seen.add((a, b))

    # Print summary
    print(f"\n=== CLOSURE SUMMARY ===")
    print(f"Deliverables in scope: {len(deliverables)}")
    print(f"Schema valid: {schema_valid_count}/{schema_total}")
    print(f"Total EXECUTION/DELIVERABLE edges: {len(all_edges)}")
    print(f"Unique edges: {len(edge_set)}")
    print(f"Orphan references: {len(orphans)}")
    print(f"Non-trivial SCCs: {len(nontrivial_sccs)}")
    print(f"Representative cycles: {len(all_cycles)}")
    print(f"Missing IMPLEMENTS_NODE anchors: {len(missing_anchors)}")
    print(f"Misplaced fields: {len(all_misplaced)}")
    print(f"Isolated deliverables: {len(isolated)}")
    print(f"Hubs (degree >= {HUB_THRESHOLD}): {len(hubs)}")
    print(f"Bidirectional pairs: {len(bidirectional)}")

    # Output JSON summary
    summary = {
        "run_label": "AUDIT_DEP_CLOSURE",
        "run_date": "2026-02-21",
        "scope": "ALL",
        "deliverables_in_scope": len(deliverables),
        "schema_valid": schema_valid_count,
        "schema_invalid": schema_total - schema_valid_count,
        "total_execution_deliverable_edges": len(all_edges),
        "unique_edges": len(edge_set),
        "orphan_count": len(orphans),
        "nontrivial_scc_count": len(nontrivial_sccs),
        "cycle_count": len(all_cycles),
        "missing_anchor_count": len(missing_anchors),
        "misplaced_field_count": len(all_misplaced),
        "isolated_count": len(isolated),
        "hub_count": len(hubs),
        "bidirectional_pair_count": len(bidirectional),
        "closure_status": "PASS" if len(orphans) == 0 and len(nontrivial_sccs) == 0 else
                          "WARNINGS" if len(nontrivial_sccs) > 0 and len(bidirectional) > 0 else
                          "BLOCKER" if len(nontrivial_sccs) > 0 else "WARNINGS",
    }
    print(f"\nJSON: {json.dumps(summary, indent=2)}")
    return summary


if __name__ == "__main__":
    main()
