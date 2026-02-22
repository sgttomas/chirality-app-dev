#!/usr/bin/env python3
"""
Dependency Closure Analysis Script
Run: CLOSURE_DEL-01-01_2026-02-21
Scope: DEL-01-01 (single deliverable)

Reproduces the closure analysis performed by AUDIT_DEP_CLOSURE.
Usage: python3 analyze_closure.py [--execution-root PATH]
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
SCOPE = ["DEL-01-01"]
FILTER_ACTIVE_ONLY = True
NORMALIZE_IDS = True
EDGE_FILTER_CLASS = "EXECUTION"
EDGE_FILTER_TARGET_TYPE = "DELIVERABLE"
HUB_THRESHOLD = 20
MAX_CYCLES = 10000

# All valid workspace deliverable IDs (32 total)
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

SHORT_FORM_PATTERN = re.compile(r"^DEL-\d{2}-\d{2}$")


def normalize_id(raw_id: str) -> str:
    """Strip descriptive suffix from long-form IDs. DEL-XX-YY_Label -> DEL-XX-YY."""
    if not raw_id:
        return raw_id
    match = re.match(r"^(DEL-\d{2}-\d{2})", raw_id)
    return match.group(1) if match else raw_id


def find_deliverable_csv(execution_root: str, deliverable_id: str) -> str | None:
    """Find Dependencies.csv for a deliverable by scanning the execution tree."""
    root = Path(execution_root)
    for pkg_dir in sorted(root.iterdir()):
        if not pkg_dir.is_dir() or pkg_dir.name.startswith("_"):
            continue
        working_dir = pkg_dir / "1_Working"
        if not working_dir.exists():
            continue
        for del_dir in sorted(working_dir.iterdir()):
            if del_dir.is_dir() and del_dir.name.startswith(deliverable_id):
                csv_path = del_dir / "Dependencies.csv"
                if csv_path.exists():
                    return str(csv_path)
    return None


def validate_schema(header: list[str], expected_version: str = "v3.1") -> tuple[bool, list[str]]:
    """Check that all required columns are present."""
    missing = [col for col in REQUIRED_COLUMNS_V31 if col not in header]
    return len(missing) == 0, missing


def tarjan_scc(graph: dict[str, set[str]]) -> list[list[str]]:
    """Tarjan's algorithm for strongly connected components."""
    index_counter = [0]
    stack = []
    lowlink = {}
    index = {}
    on_stack = {}
    result = []

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
            result.append(component)

    all_nodes = set(graph.keys())
    for targets in graph.values():
        all_nodes.update(targets)

    for node in sorted(all_nodes):
        if node not in index:
            strongconnect(node)

    return result


def main():
    execution_root = DEFAULT_EXECUTION_ROOT
    if len(sys.argv) > 2 and sys.argv[1] == "--execution-root":
        execution_root = sys.argv[2]

    print(f"Execution root: {execution_root}")
    print(f"Scope: {SCOPE}")
    print()

    # --- Step 1: Locate and read Dependencies.csv ---
    coverage = []
    all_rows = []

    for del_id in SCOPE:
        csv_path = find_deliverable_csv(execution_root, del_id)
        if csv_path is None:
            coverage.append({
                "deliverable_id": del_id,
                "csv_found": False,
                "readable": False,
                "schema_valid": False,
                "status": "MISSING_DEPENDENCIES_CSV",
            })
            print(f"  [{del_id}] MISSING Dependencies.csv")
            continue

        try:
            with open(csv_path, "r", newline="") as f:
                reader = csv.DictReader(f)
                header = reader.fieldnames or []
                schema_valid, missing_cols = validate_schema(header)
                rows = list(reader)
        except Exception as e:
            coverage.append({
                "deliverable_id": del_id,
                "csv_found": True,
                "readable": False,
                "schema_valid": False,
                "status": f"UNREADABLE: {e}",
            })
            print(f"  [{del_id}] UNREADABLE: {e}")
            continue

        status = "OK" if schema_valid else f"SCHEMA_INVALID (missing: {missing_cols})"
        coverage.append({
            "deliverable_id": del_id,
            "csv_found": True,
            "readable": True,
            "schema_valid": schema_valid,
            "row_count": len(rows),
            "status": status,
        })
        print(f"  [{del_id}] {status} -- {len(rows)} rows")

        if schema_valid:
            all_rows.extend(rows)

    print()

    # --- Step 2: Build graph ---
    nodes = set(SCOPE)
    edges = []  # list of (from_id, to_id, dep_id, direction, dep_type)

    for row in all_rows:
        status = row.get("Status", "").strip()
        if FILTER_ACTIVE_ONLY and status != "ACTIVE":
            continue

        dep_class = row.get("DependencyClass", "").strip()
        target_type = row.get("TargetType", "").strip()

        if dep_class != EDGE_FILTER_CLASS or target_type != EDGE_FILTER_TARGET_TYPE:
            continue

        from_id = row.get("FromDeliverableID", "").strip()
        to_id = row.get("TargetDeliverableID", "").strip()

        if NORMALIZE_IDS:
            from_id = normalize_id(from_id)
            to_id = normalize_id(to_id)

        if not from_id or not to_id:
            continue

        dep_id = row.get("DependencyID", "").strip()
        direction = row.get("Direction", "").strip()
        dep_type = row.get("DependencyType", "").strip()

        nodes.add(from_id)
        nodes.add(to_id)
        edges.append((from_id, to_id, dep_id, direction, dep_type))

    print(f"Graph: {len(nodes)} nodes, {len(edges)} edges")
    for e in edges:
        print(f"  {e[0]} -> {e[1]} ({e[2]}, {e[3]}, {e[4]})")
    print()

    # --- Step 3: Run checks ---

    # Check 1: Schema compliance
    valid_count = sum(1 for c in coverage if c.get("schema_valid", False))
    print(f"Check 1 - Schema Compliance: {valid_count}/{len(coverage)} valid")

    # Check 2: Orphan dependencies
    orphans = []
    for from_id, to_id, dep_id, direction, dep_type in edges:
        if to_id not in VALID_DELIVERABLE_IDS:
            orphans.append((dep_id, from_id, to_id))
    print(f"Check 2 - Orphan Dependencies: {len(orphans)} orphans")

    # Check 3: Circular dependencies (Tarjan SCC)
    adj = defaultdict(set)
    for from_id, to_id, dep_id, direction, dep_type in edges:
        adj[from_id].add(to_id)

    sccs = tarjan_scc(dict(adj))
    nontrivial_sccs = [scc for scc in sccs if len(scc) > 1]
    print(f"Check 3 - Circular Dependencies: {len(nontrivial_sccs)} non-trivial SCCs")

    # Check 4: Anchor coverage
    anchors_by_del = defaultdict(list)
    for row in all_rows:
        if row.get("DependencyClass", "").strip() == "ANCHOR":
            del_id = normalize_id(row.get("FromDeliverableID", "").strip()) if NORMALIZE_IDS else row.get("FromDeliverableID", "").strip()
            anchor_type = row.get("AnchorType", "").strip()
            anchors_by_del[del_id].append(anchor_type)

    missing_anchors = []
    for del_id in SCOPE:
        types = anchors_by_del.get(del_id, [])
        if "IMPLEMENTS_NODE" not in types:
            missing_anchors.append(del_id)
    print(f"Check 4 - Anchor Coverage: {len(missing_anchors)} missing IMPLEMENTS_NODE")

    # Check 5: Misplaced fields
    misplaced = []
    for row in all_rows:
        target_type = row.get("TargetType", "").strip()
        target_del_id = row.get("TargetDeliverableID", "").strip()
        if target_type != "DELIVERABLE" and target_del_id:
            misplaced.append(row.get("DependencyID", ""))
    print(f"Check 5 - Misplaced Fields: {len(misplaced)} violations")

    # Check 6: ID format consistency
    all_ids = set()
    for row in all_rows:
        fid = row.get("FromDeliverableID", "").strip()
        tid = row.get("TargetDeliverableID", "").strip()
        if fid:
            all_ids.add(fid)
        if tid:
            all_ids.add(tid)
    long_form = [i for i in all_ids if not SHORT_FORM_PATTERN.match(i)]
    print(f"Check 6 - ID Format: {len(long_form)} long-form IDs out of {len(all_ids)}")

    # Check 7: Isolated deliverables
    connected = set()
    for from_id, to_id, dep_id, direction, dep_type in edges:
        connected.add(from_id)
        connected.add(to_id)
    isolated = [n for n in SCOPE if n not in connected]
    print(f"Check 7 - Isolated Deliverables: {len(isolated)} isolated")

    # Check 8: Hub analysis
    degree = defaultdict(int)
    for from_id, to_id, dep_id, direction, dep_type in edges:
        degree[from_id] += 1
        degree[to_id] += 1
    hubs = [(n, d) for n, d in degree.items() if d >= HUB_THRESHOLD]
    print(f"Check 8 - Hub Analysis: {len(hubs)} hubs (threshold={HUB_THRESHOLD})")

    # Check 9: Bidirectional pairs
    edge_set = set()
    for from_id, to_id, dep_id, direction, dep_type in edges:
        edge_set.add((from_id, to_id))
    bidirectional = [(a, b) for a, b in edge_set if (b, a) in edge_set and a < b]
    print(f"Check 9 - Bidirectional Pairs: {len(bidirectional)} pairs")

    print()
    print("=== Analysis Complete ===")

    # Determine overall status
    has_blockers = len(orphans) > 0 or len(nontrivial_sccs) > 0
    has_warnings = len(missing_anchors) > 0 or len(misplaced) > 0
    if has_blockers:
        status = "BLOCKER"
    elif has_warnings:
        status = "WARNINGS"
    else:
        status = "PASS"
    print(f"Closure Status: {status}")


if __name__ == "__main__":
    main()
