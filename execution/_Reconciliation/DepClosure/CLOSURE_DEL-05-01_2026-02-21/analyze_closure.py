#!/usr/bin/env python3
"""
analyze_closure.py -- Reproducible dependency closure analysis for DEL-05-01
Run Label: DEL-05-01
Snapshot: CLOSURE_DEL-05-01_2026-02-21
Date: 2026-02-21

This script reproduces the analysis performed by AUDIT_DEP_CLOSURE.
It reads the Dependencies.csv for DEL-05-01 and runs all 9 core checks.

Usage:
    python3 analyze_closure.py [--execution-root PATH]

Default execution root: execution/ (relative to repo root)
"""

import csv
import json
import os
import sys
from collections import defaultdict
from pathlib import Path


# --- Configuration ---

DEFAULTS = {
    "run_label": "DEL-05-01",
    "scope": ["DEL-05-01"],
    "filter_active_only": True,
    "normalize_ids": True,
    "edge_filter_dependency_class": "EXECUTION",
    "edge_filter_target_type": "DELIVERABLE",
    "hub_threshold": 20,
    "max_cycles": 10000,
}

VALID_WORKSPACE_DELIVERABLES = [
    "DEL-01-01", "DEL-01-02",
    "DEL-02-01", "DEL-02-02", "DEL-02-03", "DEL-02-04",
    "DEL-03-01", "DEL-03-02", "DEL-03-03", "DEL-03-04", "DEL-03-05", "DEL-03-06",
    "DEL-04-01", "DEL-04-02",
    "DEL-05-01", "DEL-05-02", "DEL-05-03", "DEL-05-04",
    "DEL-06-01", "DEL-06-02", "DEL-06-03", "DEL-06-04", "DEL-06-05",
    "DEL-07-01", "DEL-07-02",
    "DEL-08-01", "DEL-08-02", "DEL-08-03", "DEL-08-04", "DEL-08-05", "DEL-08-06", "DEL-08-07",
]

V31_REQUIRED_COLUMNS = [
    "RegisterSchemaVersion", "DependencyID", "FromPackageID", "FromDeliverableID",
    "FromDeliverableName", "DependencyClass", "AnchorType", "Direction",
    "DependencyType", "TargetType", "TargetPackageID", "TargetDeliverableID",
    "TargetRefID", "TargetName", "TargetLocation", "Statement", "EvidenceFile",
    "SourceRef", "EvidenceQuote", "Explicitness", "RequiredMaturity",
    "ProposedMaturity", "SatisfactionStatus", "Confidence", "Origin",
    "FirstSeen", "LastSeen", "Status", "Notes",
]

DELIVERABLE_PATH = "PKG-05_Filesystem_Execution_Model/1_Working/DEL-05-01_Instruction_Root_Bundling"


def normalize_id(raw_id: str) -> str:
    """Strip descriptive suffix from DEL-XX-YY_Label format."""
    if not raw_id:
        return raw_id
    import re
    match = re.match(r"(DEL-\d{2}-\d{2})", raw_id)
    if match:
        return match.group(1)
    return raw_id


def load_csv(filepath: str) -> list[dict]:
    """Load a CSV file and return list of row dicts."""
    rows = []
    with open(filepath, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)
    return rows


def check_schema(rows: list[dict], filepath: str) -> dict:
    """Check 1: Schema compliance."""
    if not rows:
        return {"verdict": "WARNING", "detail": "No rows in CSV"}
    header = list(rows[0].keys())
    missing = [c for c in V31_REQUIRED_COLUMNS if c not in header]
    extra = [c for c in header if c not in V31_REQUIRED_COLUMNS]
    schema_version = rows[0].get("RegisterSchemaVersion", "UNKNOWN")
    if missing:
        return {
            "verdict": "BLOCKER",
            "schema_version": schema_version,
            "missing_columns": missing,
            "extra_columns": extra,
        }
    return {
        "verdict": "PASS",
        "schema_version": schema_version,
        "missing_columns": [],
        "extra_columns": extra,
        "coverage_pct": 100.0,
    }


def get_qualifying_edges(rows: list[dict]) -> list[dict]:
    """Filter rows to qualifying EXECUTION/DELIVERABLE edges."""
    edges = []
    for row in rows:
        if DEFAULTS["filter_active_only"] and row.get("Status") != "ACTIVE":
            continue
        if row.get("DependencyClass") != DEFAULTS["edge_filter_dependency_class"]:
            continue
        if row.get("TargetType") != DEFAULTS["edge_filter_target_type"]:
            continue
        from_id = normalize_id(row.get("FromDeliverableID", "")) if DEFAULTS["normalize_ids"] else row.get("FromDeliverableID", "")
        target_id = normalize_id(row.get("TargetDeliverableID", "")) if DEFAULTS["normalize_ids"] else row.get("TargetDeliverableID", "")
        if from_id and target_id:
            edges.append({
                "dependency_id": row.get("DependencyID"),
                "from_id": from_id,
                "target_id": target_id,
                "direction": row.get("Direction"),
                "dependency_type": row.get("DependencyType"),
            })
    return edges


def check_orphans(edges: list[dict]) -> dict:
    """Check 2: Orphan dependencies."""
    orphans = []
    for edge in edges:
        if edge["target_id"] not in VALID_WORKSPACE_DELIVERABLES:
            orphans.append(edge)
    return {
        "verdict": "BLOCKER" if orphans else "PASS",
        "orphan_count": len(orphans),
        "orphans": orphans,
    }


def check_cycles(edges: list[dict]) -> dict:
    """Check 3: Circular dependencies (Tarjan SCC on directed graph)."""
    # Build adjacency list
    adj = defaultdict(list)
    nodes = set()
    for edge in edges:
        direction = edge["direction"]
        if direction == "UPSTREAM":
            adj[edge["from_id"]].append(edge["target_id"])
        elif direction == "DOWNSTREAM":
            adj[edge["from_id"]].append(edge["target_id"])
        nodes.add(edge["from_id"])
        nodes.add(edge["target_id"])

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

        for w in adj.get(v, []):
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

    for node in sorted(nodes):
        if node not in index:
            strongconnect(node)

    nontrivial = [scc for scc in sccs if len(scc) > 1]
    return {
        "verdict": "BLOCKER" if nontrivial else "PASS",
        "scc_count_nontrivial": len(nontrivial),
        "nontrivial_sccs": nontrivial,
        "total_sccs": len(sccs),
    }


def check_anchors(rows: list[dict]) -> dict:
    """Check 4: Anchor coverage."""
    implements_node = [r for r in rows if r.get("AnchorType") == "IMPLEMENTS_NODE"]
    traces = [r for r in rows if r.get("AnchorType") == "TRACES_TO_REQUIREMENT"]
    return {
        "verdict": "PASS" if implements_node else "WARNING",
        "implements_node_present": bool(implements_node),
        "implements_node_ids": [r.get("DependencyID") for r in implements_node],
        "traces_to_requirement_ids": [r.get("DependencyID") for r in traces],
    }


def check_misplaced_fields(rows: list[dict]) -> dict:
    """Check 5: Misplaced fields."""
    violations = []
    for row in rows:
        if row.get("TargetType") != "DELIVERABLE" and row.get("TargetDeliverableID", "").strip():
            violations.append({
                "dependency_id": row.get("DependencyID"),
                "target_type": row.get("TargetType"),
                "target_deliverable_id": row.get("TargetDeliverableID"),
            })
    return {
        "verdict": "WARNING" if violations else "PASS",
        "violation_count": len(violations),
        "violations": violations,
    }


def check_id_format(rows: list[dict]) -> dict:
    """Check 6: ID format consistency."""
    import re
    short_form = re.compile(r"^DEL-\d{2}-\d{2}$")
    ids_checked = set()
    long_form = []

    for row in rows:
        for field in ["FromDeliverableID", "TargetDeliverableID"]:
            val = row.get(field, "").strip()
            if val and val not in ids_checked:
                ids_checked.add(val)
                if not short_form.match(val):
                    long_form.append(val)

    total = len(ids_checked)
    normalization_rate = (len(long_form) / total * 100) if total > 0 else 0.0
    return {
        "verdict": "PASS" if not long_form else "WARNING",
        "total_ids_checked": total,
        "long_form_ids": long_form,
        "normalization_rate_pct": normalization_rate,
    }


def check_isolated(edges: list[dict], scope_ids: list[str]) -> dict:
    """Check 7: Isolated deliverables."""
    connected = set()
    for edge in edges:
        connected.add(edge["from_id"])
    isolated = [sid for sid in scope_ids if sid not in connected]
    return {
        "verdict": "WARNING" if isolated else "PASS",
        "isolated_count": len(isolated),
        "isolated_ids": isolated,
        "total_execution_edges": len(edges),
    }


def check_hubs(edges: list[dict]) -> dict:
    """Check 8: Hub analysis."""
    degree = defaultdict(int)
    for edge in edges:
        degree[edge["from_id"]] += 1
    hubs = {k: v for k, v in degree.items() if v >= DEFAULTS["hub_threshold"]}
    max_node = max(degree, key=degree.get) if degree else None
    max_deg = degree[max_node] if max_node else 0
    return {
        "verdict": "WARNING" if hubs else "PASS",
        "hubs_detected": len(hubs),
        "hub_threshold": DEFAULTS["hub_threshold"],
        "max_degree": max_deg,
        "max_degree_node": max_node,
    }


def check_bidirectional(edges: list[dict]) -> dict:
    """Check 9: Bidirectional pairs."""
    pairs = defaultdict(list)
    for edge in edges:
        key = tuple(sorted([edge["from_id"], edge["target_id"]]))
        pairs[key].append(edge)

    bidirectional = {}
    for key, edge_list in pairs.items():
        directions = set()
        for e in edge_list:
            directions.add(e["direction"])
        if "UPSTREAM" in directions and "DOWNSTREAM" in directions:
            bidirectional[key] = edge_list

    return {
        "verdict": "INFO" if bidirectional else "PASS",
        "pair_count": len(bidirectional),
        "pairs": {
            f"{k[0]}<->{k[1]}": [e["dependency_id"] for e in v]
            for k, v in bidirectional.items()
        },
    }


def main():
    # Resolve execution root
    exec_root = "execution/"
    if len(sys.argv) > 2 and sys.argv[1] == "--execution-root":
        exec_root = sys.argv[2]

    csv_path = os.path.join(exec_root, DELIVERABLE_PATH, "Dependencies.csv")
    if not os.path.isfile(csv_path):
        print(f"ERROR: Dependencies.csv not found at {csv_path}")
        sys.exit(1)

    print(f"Loading: {csv_path}")
    rows = load_csv(csv_path)
    print(f"Rows loaded: {len(rows)}")

    # Run checks
    results = {}

    print("\n--- Check 1: Schema Compliance ---")
    results["schema_compliance"] = check_schema(rows, csv_path)
    print(json.dumps(results["schema_compliance"], indent=2))

    edges = get_qualifying_edges(rows)
    print(f"\nQualifying edges: {len(edges)}")

    print("\n--- Check 2: Orphan Dependencies ---")
    results["orphan_dependencies"] = check_orphans(edges)
    print(json.dumps(results["orphan_dependencies"], indent=2))

    print("\n--- Check 3: Circular Dependencies ---")
    results["circular_dependencies"] = check_cycles(edges)
    print(json.dumps(results["circular_dependencies"], indent=2))

    print("\n--- Check 4: Anchor Coverage ---")
    results["anchor_coverage"] = check_anchors(rows)
    print(json.dumps(results["anchor_coverage"], indent=2))

    print("\n--- Check 5: Misplaced Fields ---")
    results["misplaced_fields"] = check_misplaced_fields(rows)
    print(json.dumps(results["misplaced_fields"], indent=2))

    print("\n--- Check 6: ID Format Consistency ---")
    results["id_format_consistency"] = check_id_format(rows)
    print(json.dumps(results["id_format_consistency"], indent=2))

    print("\n--- Check 7: Isolated Deliverables ---")
    results["isolated_deliverables"] = check_isolated(edges, DEFAULTS["scope"])
    print(json.dumps(results["isolated_deliverables"], indent=2))

    print("\n--- Check 8: Hub Analysis ---")
    results["hub_analysis"] = check_hubs(edges)
    print(json.dumps(results["hub_analysis"], indent=2))

    print("\n--- Check 9: Bidirectional Pairs ---")
    results["bidirectional_pairs"] = check_bidirectional(edges)
    print(json.dumps(results["bidirectional_pairs"], indent=2))

    # Summary
    verdicts = [r["verdict"] for r in results.values()]
    if "BLOCKER" in verdicts:
        overall = "BLOCKER"
    elif "WARNING" in verdicts:
        overall = "WARNINGS"
    else:
        overall = "PASS"

    print(f"\n=== OVERALL CLOSURE STATUS: {overall} ===")
    return 0 if overall == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
