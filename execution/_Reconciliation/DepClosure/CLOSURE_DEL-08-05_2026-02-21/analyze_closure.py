#!/usr/bin/env python3
"""
Reproducible dependency closure analysis script for DEL-08-05.

This script reproduces the analysis performed by AUDIT_DEP_CLOSURE
for the CLOSURE_DEL-08-05_2026-02-21 snapshot.

Usage:
    python3 analyze_closure.py [--execution-root EXECUTION_ROOT]

Defaults:
    --execution-root: execution/
"""

import csv
import json
import os
import sys
import argparse
from collections import defaultdict
from pathlib import Path

# --- Configuration ---
SCOPE = ["DEL-08-05"]
DELIVERABLE_PATH = "execution/PKG-08_Optional_Integrity_Hardening/1_Working/DEL-08-05_Deliverable_Lock_Mechanism/"
FILTER_ACTIVE_ONLY = True
NORMALIZE_IDS = True
EDGE_FILTER_CLASS = "EXECUTION"
EDGE_FILTER_TARGET_TYPE = "DELIVERABLE"
HUB_THRESHOLD = 20
MAX_CYCLES = 10000

# All 32 known deliverable IDs in the workspace
VALID_DELIVERABLE_IDS = {
    "DEL-01-01", "DEL-01-02",
    "DEL-02-01", "DEL-02-02", "DEL-02-03", "DEL-02-04",
    "DEL-03-01", "DEL-03-02", "DEL-03-03", "DEL-03-04", "DEL-03-05", "DEL-03-06",
    "DEL-04-01", "DEL-04-02",
    "DEL-05-01", "DEL-05-02", "DEL-05-03", "DEL-05-04",
    "DEL-06-01", "DEL-06-02", "DEL-06-03", "DEL-06-04", "DEL-06-05",
    "DEL-07-01", "DEL-07-02",
    "DEL-08-01", "DEL-08-02", "DEL-08-03", "DEL-08-04", "DEL-08-05",
    "DEL-08-06", "DEL-08-07",
}

EXPECTED_COLUMNS_V31 = [
    "RegisterSchemaVersion", "DependencyID", "FromPackageID",
    "FromDeliverableID", "FromDeliverableName", "DependencyClass",
    "AnchorType", "Direction", "DependencyType", "TargetType",
    "TargetPackageID", "TargetDeliverableID", "TargetRefID", "TargetName",
    "TargetLocation", "Statement", "EvidenceFile", "SourceRef",
    "EvidenceQuote", "Explicitness", "RequiredMaturity", "ProposedMaturity",
    "SatisfactionStatus", "Confidence", "Origin", "FirstSeen", "LastSeen",
    "Status", "Notes",
]


def normalize_id(raw_id: str) -> str:
    """Strip descriptive suffix from deliverable ID if present."""
    if not raw_id:
        return raw_id
    import re
    match = re.match(r"^(DEL-\d{2}-\d{2})", raw_id)
    if match:
        return match.group(1)
    return raw_id


def parse_dependencies_csv(filepath: str):
    """Parse a Dependencies.csv file and return rows + schema validity."""
    rows = []
    schema_valid = False
    schema_version = None

    if not os.path.isfile(filepath):
        return None, False, None

    with open(filepath, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        columns = reader.fieldnames or []

        # Check schema
        if columns:
            schema_version = None
            missing = set(EXPECTED_COLUMNS_V31) - set(columns)
            if not missing:
                schema_valid = True
                schema_version = "v3.1"

        for row in reader:
            if schema_version is None and "RegisterSchemaVersion" in row:
                schema_version = row["RegisterSchemaVersion"]
            rows.append(row)

    return rows, schema_valid, schema_version


def run_checks(rows, schema_valid, schema_version):
    """Run all 9 core checks and return results."""
    results = {}

    # Check 1: Schema Compliance
    results["schema_compliance"] = {
        "verdict": "PASS" if schema_valid else "BLOCKER",
        "schema_version": schema_version,
        "valid": schema_valid,
    }

    # Filter edges for graph
    edges = []
    anchor_rows = []
    for row in rows:
        dep_class = row.get("DependencyClass", "")
        target_type = row.get("TargetType", "")
        status = row.get("Status", "")
        dep_id = row.get("DependencyID", "")

        if dep_class == "ANCHOR":
            anchor_rows.append(row)

        if FILTER_ACTIVE_ONLY and status != "ACTIVE":
            continue

        if dep_class == EDGE_FILTER_CLASS and target_type == EDGE_FILTER_TARGET_TYPE:
            from_id = row.get("FromDeliverableID", "")
            target_id = row.get("TargetDeliverableID", "")
            if NORMALIZE_IDS:
                from_id = normalize_id(from_id)
                target_id = normalize_id(target_id)
            if from_id and target_id:
                edges.append({
                    "dependency_id": dep_id,
                    "from": from_id,
                    "to": target_id,
                    "direction": row.get("Direction", ""),
                    "dependency_type": row.get("DependencyType", ""),
                })

    # Check 2: Orphan Dependencies
    orphans = []
    for edge in edges:
        if edge["to"] not in VALID_DELIVERABLE_IDS:
            orphans.append(edge)
    results["orphan_dependencies"] = {
        "verdict": "BLOCKER" if orphans else "PASS",
        "orphan_count": len(orphans),
        "orphans": orphans,
    }

    # Check 3: Circular Dependencies (Tarjan SCC on single node)
    # With a single source node, no non-trivial SCCs possible
    nodes = set()
    for edge in edges:
        nodes.add(edge["from"])
        nodes.add(edge["to"])

    graph = defaultdict(list)
    for edge in edges:
        graph[edge["from"]].append(edge["to"])

    # Tarjan's SCC
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

    for node in nodes:
        if node not in index:
            strongconnect(node)

    results["circular_dependencies"] = {
        "verdict": "BLOCKER" if sccs else "PASS",
        "scc_count": len(sccs),
        "sccs": sccs,
    }

    # Check 4: Anchor Coverage
    has_implements_node = any(
        r.get("AnchorType") == "IMPLEMENTS_NODE" for r in anchor_rows
    )
    results["anchor_coverage"] = {
        "verdict": "PASS" if has_implements_node else "WARNING",
        "implements_node_count": sum(
            1 for r in anchor_rows if r.get("AnchorType") == "IMPLEMENTS_NODE"
        ),
        "total_anchors": len(anchor_rows),
    }

    # Check 5: Misplaced Fields
    misplaced = []
    for row in rows:
        target_type = row.get("TargetType", "")
        target_del_id = row.get("TargetDeliverableID", "")
        if target_type != "DELIVERABLE" and target_del_id.strip():
            misplaced.append(row.get("DependencyID", ""))
    results["misplaced_fields"] = {
        "verdict": "WARNING" if misplaced else "PASS",
        "misplaced_count": len(misplaced),
        "misplaced_ids": misplaced,
    }

    # Check 6: ID Format Consistency
    import re
    long_form_ids = []
    for row in rows:
        for field in ["FromDeliverableID", "TargetDeliverableID"]:
            val = row.get(field, "").strip()
            if val and re.match(r"^DEL-\d{2}-\d{2}_.+", val):
                long_form_ids.append({"dependency_id": row.get("DependencyID"), "field": field, "value": val})
    results["id_format_consistency"] = {
        "verdict": "PASS",
        "long_form_count": len(long_form_ids),
        "long_form_ids": long_form_ids,
    }

    # Check 7: Isolated Deliverables
    scope_nodes = set(SCOPE)
    isolated = []
    for node in scope_nodes:
        edge_count = sum(1 for e in edges if e["from"] == node or e["to"] == node)
        if edge_count == 0:
            isolated.append(node)
    results["isolated_deliverables"] = {
        "verdict": "WARNING" if isolated else "PASS",
        "isolated_count": len(isolated),
        "isolated": isolated,
    }

    # Check 8: Hub Analysis
    degree = defaultdict(int)
    for edge in edges:
        degree[edge["from"]] += 1
        degree[edge["to"]] += 1
    hubs = [
        {"node": n, "degree": d}
        for n, d in degree.items()
        if d >= HUB_THRESHOLD
    ]
    results["hub_analysis"] = {
        "verdict": "WARNING" if hubs else "PASS",
        "hub_count": len(hubs),
        "hubs": hubs,
        "max_degree": max(degree.values()) if degree else 0,
    }

    # Check 9: Bidirectional Pairs
    edge_set = set()
    for edge in edges:
        edge_set.add((edge["from"], edge["to"]))
    bidirectional = []
    seen = set()
    for a, b in edge_set:
        if (b, a) in edge_set and (b, a) not in seen:
            bidirectional.append((a, b))
            seen.add((a, b))
    results["bidirectional_pairs"] = {
        "verdict": "PASS",
        "pair_count": len(bidirectional),
        "pairs": bidirectional,
    }

    return results, edges


def main():
    parser = argparse.ArgumentParser(description="Dependency closure analysis for DEL-08-05")
    parser.add_argument("--execution-root", default="execution/", help="Path to execution root")
    args = parser.parse_args()

    csv_path = os.path.join(args.execution_root,
        "PKG-08_Optional_Integrity_Hardening/1_Working/DEL-08-05_Deliverable_Lock_Mechanism/Dependencies.csv")

    print(f"Analyzing: {csv_path}")
    rows, schema_valid, schema_version = parse_dependencies_csv(csv_path)

    if rows is None:
        print(f"ERROR: Dependencies.csv not found at {csv_path}")
        sys.exit(1)

    print(f"  Schema: {schema_version} (valid={schema_valid})")
    print(f"  Rows: {len(rows)}")

    results, edges = run_checks(rows, schema_valid, schema_version)

    print(f"\n--- Results ---")
    overall = "PASS"
    for check_name, check_result in results.items():
        verdict = check_result["verdict"]
        print(f"  {check_name}: {verdict}")
        if verdict == "BLOCKER":
            overall = "BLOCKER"
        elif verdict == "WARNING" and overall != "BLOCKER":
            overall = "WARNING"

    print(f"\nOverall: {overall}")
    print(f"Graph edges: {len(edges)}")

    # Output JSON summary
    summary = {
        "run_label": "DEL-08-05",
        "overall_verdict": overall,
        "checks": results,
        "edge_count": len(edges),
    }
    print(f"\nJSON Summary:\n{json.dumps(summary, indent=2, default=str)}")


if __name__ == "__main__":
    main()
