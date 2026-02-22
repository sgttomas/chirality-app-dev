#!/usr/bin/env python3
"""
Reproducible dependency closure analysis script for DEL-06-01.

Snapshot: CLOSURE_DEL-06-01_2026-02-21
Run Date: 2026-02-21
Scope:    DEL-06-01

This script reproduces the closure analysis performed by AUDIT_DEP_CLOSURE.
It reads the Dependencies.csv for DEL-06-01, applies the default edge filter,
builds the dependency graph, and runs all 9 core checks.

Usage:
    python3 analyze_closure.py [--execution-root PATH]

Defaults:
    --execution-root: ../../.. (relative to this script's location, resolving to execution/)
"""

import csv
import json
import os
import sys
import argparse
from collections import defaultdict
from pathlib import Path


# --- Configuration ---

SCOPE = ["DEL-06-01"]
DELIVERABLE_PATH = "PKG-06_Agent_Suite_Governance/1_Working/DEL-06-01_Agent_Instruction_Conformance"
EDGE_FILTER_CLASS = "EXECUTION"
EDGE_FILTER_TARGET_TYPE = "DELIVERABLE"
FILTER_ACTIVE_ONLY = True
HUB_THRESHOLD = 20
MAX_CYCLES = 10000

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


def normalize_id(raw_id: str) -> str:
    """Strip descriptive suffix from long-form IDs. DEL-XX-YY_Label -> DEL-XX-YY."""
    if not raw_id:
        return raw_id
    parts = raw_id.split("_", 1)
    prefix = parts[0]
    # Check if prefix matches DEL-XX-YY pattern
    if prefix.startswith("DEL-") and len(prefix.split("-")) == 3:
        return prefix
    return raw_id


def parse_dependencies_csv(filepath: str):
    """Parse a Dependencies.csv file and return (rows, schema_version, schema_valid, error)."""
    rows = []
    schema_version = None
    schema_valid = False
    error = None

    try:
        with open(filepath, "r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            columns = reader.fieldnames or []

            # Check schema
            missing = set(EXPECTED_COLUMNS_V31) - set(columns)
            if missing:
                error = f"Missing columns: {missing}"
                return rows, schema_version, False, error

            schema_valid = True
            for row in reader:
                schema_version = row.get("RegisterSchemaVersion", "UNKNOWN")
                rows.append(row)

    except FileNotFoundError:
        error = f"File not found: {filepath}"
    except Exception as e:
        error = str(e)

    return rows, schema_version, schema_valid, error


def run_checks(rows, schema_valid, schema_version):
    """Run all 9 core checks and return results dict."""
    results = {}

    # --- Check 1: Schema Compliance ---
    results["schema_compliance"] = {
        "verdict": "PASS" if schema_valid else "BLOCKER",
        "schema_version": schema_version,
        "column_count": len(EXPECTED_COLUMNS_V31),
        "row_count": len(rows),
    }

    # --- Filter edges ---
    qualifying_edges = []
    anchor_rows = []
    execution_rows = []

    for row in rows:
        dep_class = row.get("DependencyClass", "")
        target_type = row.get("TargetType", "")
        status = row.get("Status", "")
        anchor_type = row.get("AnchorType", "")

        if dep_class == "ANCHOR":
            anchor_rows.append(row)
        if dep_class == "EXECUTION":
            execution_rows.append(row)

        if FILTER_ACTIVE_ONLY and status != "ACTIVE":
            continue
        if dep_class != EDGE_FILTER_CLASS:
            continue
        if target_type != EDGE_FILTER_TARGET_TYPE:
            continue

        from_id = normalize_id(row.get("FromDeliverableID", ""))
        target_id = normalize_id(row.get("TargetDeliverableID", ""))
        if from_id and target_id:
            qualifying_edges.append((from_id, target_id, row))

    # --- Check 2: Orphan Dependencies ---
    orphans = []
    for from_id, target_id, row in qualifying_edges:
        if target_id not in VALID_DELIVERABLE_IDS:
            orphans.append({
                "from": from_id,
                "target": target_id,
                "dep_id": row.get("DependencyID", ""),
            })

    results["orphan_dependencies"] = {
        "verdict": "BLOCKER" if orphans else "PASS",
        "orphan_count": len(orphans),
        "orphans": orphans,
    }

    # --- Check 3: Circular Dependencies (Tarjan SCC) ---
    graph = defaultdict(list)
    all_nodes = set(SCOPE)
    for from_id, target_id, _ in qualifying_edges:
        graph[from_id].append(target_id)
        all_nodes.add(from_id)
        all_nodes.add(target_id)

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

    for node in all_nodes:
        if node not in index:
            strongconnect(node)

    results["circular_dependencies"] = {
        "verdict": "BLOCKER" if sccs else "PASS",
        "scc_count": len(sccs),
        "sccs": sccs,
    }

    # --- Check 4: Anchor Coverage ---
    implements_node = [r for r in anchor_rows if r.get("AnchorType") == "IMPLEMENTS_NODE"]
    results["anchor_coverage"] = {
        "verdict": "PASS" if implements_node else "WARNING",
        "implements_node_count": len(implements_node),
        "total_anchor_rows": len(anchor_rows),
    }

    # --- Check 5: Misplaced Fields ---
    misplaced = []
    for row in rows:
        target_type = row.get("TargetType", "")
        target_del_id = row.get("TargetDeliverableID", "").strip()
        if target_type != "DELIVERABLE" and target_del_id:
            misplaced.append({
                "dep_id": row.get("DependencyID", ""),
                "target_type": target_type,
                "target_deliverable_id": target_del_id,
            })

    results["misplaced_fields"] = {
        "verdict": "WARNING" if misplaced else "PASS",
        "misplaced_count": len(misplaced),
        "misplaced": misplaced,
    }

    # --- Check 6: ID Format Consistency ---
    long_form_count = 0
    total_ids_checked = 0
    for row in rows:
        for col in ["FromDeliverableID", "TargetDeliverableID"]:
            raw = row.get(col, "").strip()
            if raw:
                total_ids_checked += 1
                if normalize_id(raw) != raw:
                    long_form_count += 1

    results["id_format_consistency"] = {
        "verdict": "PASS",
        "long_form_ids_found": long_form_count,
        "total_ids_checked": total_ids_checked,
    }

    # --- Check 7: Isolated Deliverables ---
    connected_nodes = set()
    for from_id, target_id, _ in qualifying_edges:
        connected_nodes.add(from_id)
        connected_nodes.add(target_id)

    isolated = [n for n in SCOPE if n not in connected_nodes]
    results["isolated_deliverables"] = {
        "verdict": "WARNING" if isolated else "PASS",
        "isolated_count": len(isolated),
        "isolated_ids": isolated,
    }

    # --- Check 8: Hub Analysis ---
    degree = defaultdict(int)
    for from_id, target_id, _ in qualifying_edges:
        degree[from_id] += 1
        degree[target_id] += 1

    hubs = {k: v for k, v in degree.items() if v >= HUB_THRESHOLD}
    results["hub_analysis"] = {
        "verdict": "WARNING" if hubs else "PASS",
        "hub_count": len(hubs),
        "hubs": hubs,
    }

    # --- Check 9: Bidirectional Pairs ---
    edge_set = set()
    for from_id, target_id, _ in qualifying_edges:
        edge_set.add((from_id, target_id))

    bidir = []
    seen = set()
    for a, b in edge_set:
        pair = tuple(sorted([a, b]))
        if (b, a) in edge_set and pair not in seen:
            bidir.append(pair)
            seen.add(pair)

    results["bidirectional_pairs"] = {
        "verdict": "PASS",
        "pair_count": len(bidir),
        "pairs": [list(p) for p in bidir],
    }

    # --- Metrics ---
    metrics = {
        "total_rows": len(rows),
        "anchor_rows": len(anchor_rows),
        "execution_rows": len(execution_rows),
        "qualifying_edges": len(qualifying_edges),
    }

    return results, metrics


def main():
    parser = argparse.ArgumentParser(description="Reproduce DEL-06-01 closure analysis")
    parser.add_argument(
        "--execution-root",
        default=None,
        help="Path to execution/ root (default: auto-detect from script location)",
    )
    args = parser.parse_args()

    if args.execution_root:
        exec_root = Path(args.execution_root)
    else:
        # Auto-detect: this script is at execution/_Reconciliation/DepClosure/CLOSURE_.../
        script_dir = Path(__file__).resolve().parent
        exec_root = script_dir.parent.parent.parent

    csv_path = exec_root / DELIVERABLE_PATH / "Dependencies.csv"
    print(f"Execution root: {exec_root}")
    print(f"Dependencies.csv: {csv_path}")
    print()

    if not csv_path.exists():
        print(f"ERROR: Dependencies.csv not found at {csv_path}")
        sys.exit(1)

    rows, schema_version, schema_valid, error = parse_dependencies_csv(str(csv_path))
    if error:
        print(f"ERROR: {error}")
        sys.exit(1)

    print(f"Schema version: {schema_version}")
    print(f"Schema valid: {schema_valid}")
    print(f"Rows parsed: {len(rows)}")
    print()

    results, metrics = run_checks(rows, schema_valid, schema_version)

    print("=== Core Check Results ===")
    print()
    for check_name, check_result in results.items():
        verdict = check_result.get("verdict", "UNKNOWN")
        print(f"  {check_name}: {verdict}")
    print()
    print(f"Metrics: {json.dumps(metrics, indent=2)}")
    print()

    # Determine overall status
    verdicts = [r["verdict"] for r in results.values()]
    if "BLOCKER" in verdicts:
        overall = "BLOCKER"
    elif "WARNING" in verdicts:
        overall = "WARNINGS"
    else:
        overall = "OK"

    print(f"Overall status: {overall}")

    # Write JSON summary
    output = {
        "snapshot_id": "CLOSURE_DEL-06-01_2026-02-21",
        "run_status": overall,
        "metrics": metrics,
        "check_results": results,
    }
    output_path = Path(__file__).resolve().parent / "closure_summary_reproduced.json"
    with open(output_path, "w") as f:
        json.dump(output, f, indent=2, default=str)
    print(f"Reproduced summary written to: {output_path}")


if __name__ == "__main__":
    main()
