#!/usr/bin/env python3
"""
Dependency Closure Analysis Script -- DEL-07-02
================================================
Reproducible analysis script for CLOSURE_DEL-07-02_2026-02-21.

This script replicates the analysis performed by the AUDIT_DEP_CLOSURE agent
for a single deliverable (DEL-07-02). It reads the Dependencies.csv file,
applies filters, builds the dependency graph, and runs all 9 core checks.

Usage:
    python analyze_closure.py [--execution-root EXECUTION_ROOT]

Default execution root: execution/ (relative to repo root)
"""

import csv
import json
import os
import sys
from collections import defaultdict
from pathlib import Path

# --- Configuration ---

SCOPE_DELIVERABLE = "DEL-07-02"
DELIVERABLE_PATH = "PKG-07_Validation_Example_Assets/1_Working/DEL-07-02_Example_Execution_Roots"
FILTER_ACTIVE_ONLY = True
NORMALIZE_IDS = True
EDGE_FILTER_DEPENDENCY_CLASS = "EXECUTION"
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
    """Normalize a deliverable ID by stripping descriptive suffixes."""
    if not raw_id or not NORMALIZE_IDS:
        return raw_id
    # Strip _Label suffix: DEL-XX-YY_Something -> DEL-XX-YY
    import re
    match = re.match(r"^(DEL-\d{2}-\d{2})", raw_id)
    if match:
        return match.group(1)
    return raw_id


def read_dependencies_csv(filepath: str) -> tuple:
    """Read and parse Dependencies.csv. Returns (rows, columns, errors)."""
    rows = []
    columns = []
    errors = []
    try:
        with open(filepath, "r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            columns = reader.fieldnames or []
            for i, row in enumerate(reader, start=2):  # row 1 is header
                rows.append(row)
    except FileNotFoundError:
        errors.append(f"File not found: {filepath}")
    except Exception as e:
        errors.append(f"Error reading {filepath}: {e}")
    return rows, columns, errors


def check_schema(columns: list) -> dict:
    """Check 1: Schema compliance."""
    missing = [c for c in REQUIRED_COLUMNS_V31 if c not in columns]
    extra = [c for c in columns if c not in REQUIRED_COLUMNS_V31]
    return {
        "verdict": "PASS" if not missing else "BLOCKER",
        "columns_expected": len(REQUIRED_COLUMNS_V31),
        "columns_found": len(columns),
        "missing_columns": missing,
        "extra_columns": extra,
    }


def filter_edges(rows: list) -> list:
    """Filter rows to EXECUTION/DELIVERABLE edges."""
    edges = []
    for row in rows:
        if FILTER_ACTIVE_ONLY and row.get("Status", "").strip() != "ACTIVE":
            continue
        if row.get("DependencyClass", "").strip() != EDGE_FILTER_DEPENDENCY_CLASS:
            continue
        if row.get("TargetType", "").strip() != EDGE_FILTER_TARGET_TYPE:
            continue
        from_id = normalize_id(row.get("FromDeliverableID", "").strip())
        target_id = normalize_id(row.get("TargetDeliverableID", "").strip())
        if from_id and target_id:
            edges.append({
                "dep_id": row.get("DependencyID", "").strip(),
                "from_id": from_id,
                "target_id": target_id,
                "direction": row.get("Direction", "").strip(),
                "dep_type": row.get("DependencyType", "").strip(),
            })
    return edges


def check_orphans(edges: list) -> dict:
    """Check 2: Orphan dependencies."""
    orphans = []
    for e in edges:
        if e["target_id"] not in VALID_DELIVERABLE_IDS:
            orphans.append(e)
    return {
        "verdict": "PASS" if not orphans else "WARNING",
        "orphan_count": len(orphans),
        "orphans": orphans,
    }


def build_directed_graph(edges: list) -> tuple:
    """Build a directed adjacency list from edges using Direction metadata.

    Direction semantics (from the perspective of FromDeliverableID):
    - DOWNSTREAM: FromDeliverableID feeds into TargetDeliverableID
      => directed edge: from_id -> target_id
    - UPSTREAM: FromDeliverableID depends on TargetDeliverableID
      => directed edge: target_id -> from_id (target provides to source)

    For dependency flow analysis, we model "A depends on B" as a directed
    edge A -> B (A needs B). So:
    - UPSTREAM to target: from_id -> target_id (from depends on target)
    - DOWNSTREAM to target: target_id -> from_id (target depends on from)
    """
    graph = defaultdict(set)
    nodes = set()
    directed_edges = []
    for e in edges:
        if e["direction"] == "UPSTREAM":
            # from_id depends on target_id => from_id -> target_id
            graph[e["from_id"]].add(e["target_id"])
            directed_edges.append((e["from_id"], e["target_id"], e))
        elif e["direction"] == "DOWNSTREAM":
            # target_id depends on from_id => target_id -> from_id
            graph[e["target_id"]].add(e["from_id"])
            directed_edges.append((e["target_id"], e["from_id"], e))
        else:
            # Unknown direction: treat as from -> target (conservative)
            graph[e["from_id"]].add(e["target_id"])
            directed_edges.append((e["from_id"], e["target_id"], e))
        nodes.add(e["from_id"])
        nodes.add(e["target_id"])
    return graph, nodes, directed_edges


def check_cycles(edges: list) -> dict:
    """Check 3: Circular dependencies (Tarjan SCC)."""
    graph, nodes, _ = build_directed_graph(edges)

    # Tarjan's algorithm
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

    # Note: The script conservatively reports BLOCKER for any SCC.
    # The AUDIT_DEP_CLOSURE agent may downgrade to WARNING based on
    # contextual analysis (e.g., intentional bidirectional relationships).
    # See Dependency_Closure_Report.md for the authoritative classification.
    return {
        "verdict": "PASS" if not sccs else "BLOCKER",
        "scc_count": len(sccs),
        "sccs": sccs,
    }


def check_anchors(rows: list) -> dict:
    """Check 4: Anchor coverage."""
    anchors = [
        r for r in rows
        if r.get("DependencyClass", "").strip() == "ANCHOR"
        and r.get("AnchorType", "").strip() == "IMPLEMENTS_NODE"
    ]
    return {
        "verdict": "PASS" if anchors else "WARNING",
        "implements_node_count": len(anchors),
    }


def check_misplaced_fields(rows: list) -> dict:
    """Check 5: Misplaced fields."""
    violations = []
    for row in rows:
        target_type = row.get("TargetType", "").strip()
        target_del_id = row.get("TargetDeliverableID", "").strip()
        if target_type != "DELIVERABLE" and target_del_id:
            violations.append({
                "dep_id": row.get("DependencyID", "").strip(),
                "target_type": target_type,
                "target_deliverable_id": target_del_id,
            })
    return {
        "verdict": "PASS" if not violations else "WARNING",
        "violations": violations,
    }


def check_id_format(rows: list) -> dict:
    """Check 6: ID format consistency."""
    import re
    long_form = []
    all_ids = set()
    for row in rows:
        for field in ["FromDeliverableID", "TargetDeliverableID"]:
            raw = row.get(field, "").strip()
            if not raw:
                continue
            all_ids.add(raw)
            if re.match(r"^DEL-\d{2}-\d{2}_.+", raw):
                long_form.append({"field": field, "value": raw, "dep_id": row.get("DependencyID", "")})
    return {
        "verdict": "PASS" if not long_form else "WARNING",
        "long_form_count": len(long_form),
        "long_form_ids": long_form,
        "unique_ids_checked": len(all_ids),
    }


def check_isolated(edges: list) -> dict:
    """Check 7: Isolated deliverables."""
    is_isolated = len(edges) == 0
    return {
        "verdict": "PASS" if not is_isolated else "WARNING",
        "edge_count": len(edges),
        "is_isolated": is_isolated,
    }


def check_hubs(edges: list) -> dict:
    """Check 8: Hub analysis."""
    degree = defaultdict(int)
    for e in edges:
        degree[e["from_id"]] += 1
    hubs = {k: v for k, v in degree.items() if v >= HUB_THRESHOLD}
    return {
        "verdict": "PASS" if not hubs else "WARNING",
        "hub_count": len(hubs),
        "max_degree": max(degree.values()) if degree else 0,
        "hubs": hubs,
    }


def check_bidirectional(edges: list) -> dict:
    """Check 9: Bidirectional pairs.

    Uses directed graph interpretation: if A -> B and B -> A both exist
    in the dependency-flow graph, that is a bidirectional pair.
    """
    _, _, directed_edges = build_directed_graph(edges)
    edge_map = defaultdict(list)
    for src, dst, e in directed_edges:
        edge_map[(src, dst)].append(e)

    bidirectional = []
    seen = set()
    for (a, b), a_edges in edge_map.items():
        if (b, a) in edge_map and (min(a, b), max(a, b)) not in seen:
            seen.add((min(a, b), max(a, b)))
            bidirectional.append({
                "pair": f"{a} <-> {b}",
                "a_to_b": a_edges,
                "b_to_a": edge_map[(b, a)],
            })

    return {
        "verdict": "INFO" if bidirectional else "PASS",
        "pair_count": len(bidirectional),
        "pairs": bidirectional,
    }


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Dependency Closure Analysis for DEL-07-02")
    parser.add_argument("--execution-root", default="execution/", help="Path to execution root")
    args = parser.parse_args()

    exec_root = Path(args.execution_root)
    csv_path = exec_root / DELIVERABLE_PATH / "Dependencies.csv"

    print(f"=== Dependency Closure Analysis: {SCOPE_DELIVERABLE} ===")
    print(f"Input: {csv_path}")
    print()

    # Read CSV
    rows, columns, errors = read_dependencies_csv(str(csv_path))
    if errors:
        print("ERRORS reading CSV:")
        for e in errors:
            print(f"  - {e}")
        sys.exit(1)

    print(f"Rows read: {len(rows)}")
    print(f"Columns: {len(columns)}")
    print()

    # Run checks
    results = {}

    print("--- Check 1: Schema Compliance ---")
    results["schema"] = check_schema(columns)
    print(f"  Verdict: {results['schema']['verdict']}")

    edges = filter_edges(rows)
    print(f"\nFiltered edges (EXECUTION/DELIVERABLE/ACTIVE): {len(edges)}")

    print("\n--- Check 2: Orphan Dependencies ---")
    results["orphans"] = check_orphans(edges)
    print(f"  Verdict: {results['orphans']['verdict']} (orphans: {results['orphans']['orphan_count']})")

    print("\n--- Check 3: Circular Dependencies ---")
    results["cycles"] = check_cycles(edges)
    print(f"  Verdict: {results['cycles']['verdict']} (SCCs: {results['cycles']['scc_count']})")

    print("\n--- Check 4: Anchor Coverage ---")
    results["anchors"] = check_anchors(rows)
    print(f"  Verdict: {results['anchors']['verdict']} (IMPLEMENTS_NODE: {results['anchors']['implements_node_count']})")

    print("\n--- Check 5: Misplaced Fields ---")
    results["misplaced"] = check_misplaced_fields(rows)
    print(f"  Verdict: {results['misplaced']['verdict']} (violations: {len(results['misplaced']['violations'])})")

    print("\n--- Check 6: ID Format Consistency ---")
    results["id_format"] = check_id_format(rows)
    print(f"  Verdict: {results['id_format']['verdict']} (long-form: {results['id_format']['long_form_count']})")

    print("\n--- Check 7: Isolated Deliverables ---")
    results["isolated"] = check_isolated(edges)
    print(f"  Verdict: {results['isolated']['verdict']} (edges: {results['isolated']['edge_count']})")

    print("\n--- Check 8: Hub Analysis ---")
    results["hubs"] = check_hubs(edges)
    print(f"  Verdict: {results['hubs']['verdict']} (max degree: {results['hubs']['max_degree']})")

    print("\n--- Check 9: Bidirectional Pairs ---")
    results["bidirectional"] = check_bidirectional(edges)
    print(f"  Verdict: {results['bidirectional']['verdict']} (pairs: {results['bidirectional']['pair_count']})")

    # Overall
    verdicts = [r["verdict"] for r in results.values()]
    if "BLOCKER" in verdicts:
        overall = "BLOCKER"
    elif "WARNING" in verdicts:
        overall = "WARNING"
    elif "INFO" in verdicts:
        overall = "PASS"
    else:
        overall = "PASS"

    print(f"\n=== Overall Status: {overall} ===")
    print(f"Checks: {len(results)} run, "
          f"{sum(1 for v in verdicts if v == 'PASS')} PASS, "
          f"{sum(1 for v in verdicts if v == 'INFO')} INFO, "
          f"{sum(1 for v in verdicts if v == 'WARNING')} WARNING, "
          f"{sum(1 for v in verdicts if v == 'BLOCKER')} BLOCKER")


if __name__ == "__main__":
    main()
