#!/usr/bin/env python3
"""
analyze_closure.py -- Reproducible dependency closure analysis for DEL-01-02.

Run label: DEL-01-02
Date: 2026-02-21
Agent: AUDIT_DEP_CLOSURE (Type 2)
Requested by: RECONCILIATION

This script reproduces the closure analysis performed by AUDIT_DEP_CLOSURE.
It reads the Dependencies.csv from DEL-01-02, applies the same filters and
checks, and prints a summary to stdout.

Usage:
    python3 analyze_closure.py [--execution-root PATH]

Default --execution-root: execution/  (relative to repo root)
"""

import csv
import json
import os
import re
import sys
from collections import defaultdict
from pathlib import Path

# --- Configuration (matches the brief) ---
SCOPE = ["DEL-01-02"]
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

# Map deliverable IDs to their folder paths (relative to execution root)
DELIVERABLE_PATHS = {
    "DEL-01-02": "PKG-01_Build_And_Packaging/1_Working/DEL-01-02_Unsigned_DMG_Packaging",
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
    """Strip descriptive suffix from deliverable IDs. DEL-01-02_FooBar -> DEL-01-02."""
    if not raw_id:
        return raw_id
    match = re.match(r"^(DEL-\d{2}-\d{2})", raw_id.strip())
    if match:
        return match.group(1)
    match = re.match(r"^(KTY-\d{2}-\d{2})", raw_id.strip())
    if match:
        return match.group(1)
    return raw_id.strip()


def load_dependencies_csv(filepath: str):
    """Load and parse a Dependencies.csv file. Returns (rows, schema_valid, schema_version, error)."""
    if not os.path.isfile(filepath):
        return [], False, None, "FILE_NOT_FOUND"
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            columns = reader.fieldnames or []
            rows = list(reader)
    except Exception as e:
        return [], False, None, f"READ_ERROR: {e}"

    # Check schema version
    schema_version = rows[0].get("RegisterSchemaVersion", "UNKNOWN") if rows else "UNKNOWN"

    # Validate required columns
    missing = [c for c in REQUIRED_COLUMNS_V31 if c not in columns]
    if missing:
        return rows, False, schema_version, f"MISSING_COLUMNS: {missing}"

    return rows, True, schema_version, None


def build_graph(rows):
    """Build adjacency list from filtered rows. Returns (edges, anchor_rows, misplaced_rows, all_rows_by_id)."""
    edges = []
    anchor_rows = []
    misplaced_rows = []

    for row in rows:
        dep_id = row.get("DependencyID", "")
        dep_class = row.get("DependencyClass", "")
        target_type = row.get("TargetType", "")
        status = row.get("Status", "")
        anchor_type = row.get("AnchorType", "")
        from_id = normalize_id(row.get("FromDeliverableID", "")) if NORMALIZE_IDS else row.get("FromDeliverableID", "")
        target_del_id = normalize_id(row.get("TargetDeliverableID", "")) if NORMALIZE_IDS else row.get("TargetDeliverableID", "")

        # Filter by status
        if FILTER_ACTIVE_ONLY and status != "ACTIVE":
            continue

        # Collect anchors
        if dep_class == "ANCHOR":
            anchor_rows.append(row)
            continue

        # Check misplaced fields
        if target_type != "DELIVERABLE" and target_del_id:
            misplaced_rows.append(row)

        # Filter edges
        if dep_class == EDGE_FILTER_CLASS and target_type == EDGE_FILTER_TARGET_TYPE:
            if from_id and target_del_id:
                edges.append({
                    "from": from_id,
                    "to": target_del_id,
                    "dependency_id": dep_id,
                    "direction": row.get("Direction", ""),
                    "dependency_type": row.get("DependencyType", ""),
                })

    return edges, anchor_rows, misplaced_rows


def tarjan_scc(nodes, edges):
    """Tarjan's SCC algorithm. Returns list of SCCs (each a set of node IDs)."""
    graph = defaultdict(list)
    for e in edges:
        graph[e["from"]].append(e["to"])

    index_counter = [0]
    stack = []
    on_stack = set()
    index = {}
    lowlink = {}
    sccs = []

    def strongconnect(v):
        index[v] = index_counter[0]
        lowlink[v] = index_counter[0]
        index_counter[0] += 1
        stack.append(v)
        on_stack.add(v)

        for w in graph.get(v, []):
            if w not in index:
                strongconnect(w)
                lowlink[v] = min(lowlink[v], lowlink[w])
            elif w in on_stack:
                lowlink[v] = min(lowlink[v], index[w])

        if lowlink[v] == index[v]:
            scc = set()
            while True:
                w = stack.pop()
                on_stack.discard(w)
                scc.add(w)
                if w == v:
                    break
            sccs.append(scc)

    for node in nodes:
        if node not in index:
            strongconnect(node)

    return sccs


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Dependency closure analysis for DEL-01-02")
    parser.add_argument("--execution-root", default="execution/", help="Path to execution root")
    args = parser.parse_args()

    exec_root = args.execution_root
    results = {"checks": {}, "issues": []}

    # --- Step 1: Load Dependencies.csv ---
    del_path = os.path.join(exec_root, DELIVERABLE_PATHS["DEL-01-02"], "Dependencies.csv")
    rows, schema_valid, schema_version, error = load_dependencies_csv(del_path)

    print(f"=== Dependency Closure Analysis: DEL-01-02 ===")
    print(f"File: {del_path}")
    print(f"Schema version: {schema_version}")
    print(f"Schema valid: {schema_valid}")
    print(f"Rows loaded: {len(rows)}")
    if error:
        print(f"Schema error: {error}")
    print()

    # Check 1: Schema compliance
    results["checks"]["schema_compliance"] = "PASS" if schema_valid else "BLOCKER"
    print(f"Check 1 - Schema Compliance: {results['checks']['schema_compliance']}")

    if not schema_valid:
        print("FATAL: Schema invalid. Cannot proceed with graph analysis.")
        sys.exit(1)

    # --- Step 3: Build graph ---
    edges, anchor_rows, misplaced_rows = build_graph(rows)
    nodes = set(SCOPE)
    for e in edges:
        nodes.add(e["to"])

    print(f"\nGraph: {len(nodes)} nodes, {len(edges)} edges")
    for e in edges:
        print(f"  {e['from']} -> {e['to']} ({e['dependency_id']}, {e['direction']}, {e['dependency_type']})")
    print()

    # Check 2: Orphan dependencies
    orphans = [e for e in edges if e["to"] not in VALID_DELIVERABLE_IDS]
    results["checks"]["orphan_dependencies"] = "BLOCKER" if orphans else "PASS"
    print(f"Check 2 - Orphan Dependencies: {results['checks']['orphan_dependencies']}")
    for o in orphans:
        print(f"  ORPHAN: {o['to']} referenced by {o['dependency_id']}")
    print()

    # Check 3: Circular dependencies
    sccs = tarjan_scc(nodes, edges)
    nontrivial = [s for s in sccs if len(s) > 1]
    results["checks"]["circular_dependencies"] = "BLOCKER" if nontrivial else "PASS"
    print(f"Check 3 - Circular Dependencies: {results['checks']['circular_dependencies']}")
    print(f"  SCCs: {len(sccs)} total, {len(nontrivial)} non-trivial")
    for s in nontrivial:
        print(f"  CYCLE: {sorted(s)}")
    print()

    # Check 4: Anchor coverage
    implements_node = [r for r in anchor_rows if r.get("AnchorType") == "IMPLEMENTS_NODE"]
    has_anchor = len(implements_node) > 0
    results["checks"]["anchor_coverage"] = "PASS" if has_anchor else "WARNING"
    print(f"Check 4 - Anchor Coverage: {results['checks']['anchor_coverage']}")
    print(f"  IMPLEMENTS_NODE anchors: {len(implements_node)}")
    print()

    # Check 5: Misplaced fields
    results["checks"]["misplaced_fields"] = "WARNING" if misplaced_rows else "PASS"
    print(f"Check 5 - Misplaced Fields: {results['checks']['misplaced_fields']}")
    for m in misplaced_rows:
        print(f"  MISPLACED: {m.get('DependencyID')} has TargetType={m.get('TargetType')} but TargetDeliverableID={m.get('TargetDeliverableID')}")
    print()

    # Check 6: ID format consistency
    ids_checked = 0
    ids_normalized = 0
    for row in rows:
        for col in ["FromDeliverableID", "TargetDeliverableID"]:
            raw = row.get(col, "").strip()
            if raw:
                ids_checked += 1
                norm = normalize_id(raw)
                if norm != raw:
                    ids_normalized += 1
    norm_rate = (ids_normalized / ids_checked * 100) if ids_checked > 0 else 0
    results["checks"]["id_format_consistency"] = "PASS"
    print(f"Check 6 - ID Format Consistency: PASS")
    print(f"  IDs checked: {ids_checked}, normalized: {ids_normalized} ({norm_rate:.1f}%)")
    print()

    # Check 7: Isolated deliverables
    degree = defaultdict(int)
    for e in edges:
        degree[e["from"]] += 1
        degree[e["to"]] += 1
    isolated = [n for n in SCOPE if degree.get(n, 0) == 0]
    results["checks"]["isolated_deliverables"] = "WARNING" if isolated else "PASS"
    print(f"Check 7 - Isolated Deliverables: {results['checks']['isolated_deliverables']}")
    for i in isolated:
        print(f"  ISOLATED: {i}")
    print()

    # Check 8: Hub analysis
    hubs = [n for n in nodes if degree.get(n, 0) >= HUB_THRESHOLD]
    results["checks"]["hub_analysis"] = "WARNING" if hubs else "PASS"
    print(f"Check 8 - Hub Analysis: {results['checks']['hub_analysis']}")
    max_deg = max(degree.values()) if degree else 0
    print(f"  Max degree: {max_deg}, Hubs (>={HUB_THRESHOLD}): {len(hubs)}")
    print()

    # Check 9: Bidirectional pairs
    edge_set = {(e["from"], e["to"]) for e in edges}
    bidir = [(a, b) for (a, b) in edge_set if (b, a) in edge_set and a < b]
    results["checks"]["bidirectional_pairs"] = "PASS"
    print(f"Check 9 - Bidirectional Pairs: PASS")
    print(f"  Pairs found: {len(bidir)}")
    print()

    # --- Overall ---
    verdicts = list(results["checks"].values())
    if "BLOCKER" in verdicts:
        overall = "BLOCKER"
    elif "WARNING" in verdicts:
        overall = "WARNINGS"
    else:
        overall = "PASS"
    print(f"=== Overall: {overall} ===")


if __name__ == "__main__":
    main()
