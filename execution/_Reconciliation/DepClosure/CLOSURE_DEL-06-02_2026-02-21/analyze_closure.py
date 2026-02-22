#!/usr/bin/env python3
"""
analyze_closure.py -- Reproducible dependency closure analysis for DEL-06-02.

Run Label: DEL-06-02
Run Date: 2026-02-21
Scope: DEL-06-02 (single deliverable)

This script reproduces the analysis performed by the AUDIT_DEP_CLOSURE agent.
It reads the Dependencies.csv for DEL-06-02, builds the dependency graph,
and runs all 9 core checks.

Usage:
    python3 analyze_closure.py [--execution-root PATH]

Defaults:
    --execution-root: execution/
"""

import csv
import json
import os
import sys
from collections import defaultdict
from typing import Dict, List, Set, Tuple, Any

# --- Configuration ---
DEFAULT_EXECUTION_ROOT = "execution/"
DELIVERABLE_ID = "DEL-06-02"
DELIVERABLE_PATH = "PKG-06_Agent_Suite_Governance/1_Working/DEL-06-02_Local_Deliverable_Workflow_Agents"
DEPENDENCIES_FILE = "Dependencies.csv"
FILTER_ACTIVE_ONLY = True
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
    """Normalize a deliverable ID by stripping descriptive suffix."""
    if not raw_id:
        return raw_id
    # Match DEL-XX-YY pattern and strip anything after
    import re
    match = re.match(r"(DEL-\d{2}-\d{2})", raw_id)
    if match:
        return match.group(1)
    return raw_id


def load_dependencies(filepath: str) -> Tuple[List[Dict[str, str]], bool, str]:
    """Load and validate Dependencies.csv. Returns (rows, schema_valid, error_msg)."""
    if not os.path.isfile(filepath):
        return [], False, f"File not found: {filepath}"

    rows = []
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            columns = reader.fieldnames or []

            # Check schema
            missing_cols = [c for c in REQUIRED_COLUMNS_V31 if c not in columns]
            if missing_cols:
                return [], False, f"Missing columns: {missing_cols}"

            for row in reader:
                rows.append(row)
    except Exception as e:
        return [], False, f"Read error: {e}"

    # Check schema version
    for row in rows:
        if row.get("RegisterSchemaVersion") != "v3.1":
            return rows, False, f"Unexpected schema version: {row.get('RegisterSchemaVersion')}"

    return rows, True, ""


def check_schema_compliance(rows: List[Dict], schema_valid: bool) -> Dict[str, Any]:
    """Check 1: Schema compliance."""
    return {
        "verdict": "PASS" if schema_valid else "BLOCKER",
        "detail": "1/1 CSV readable and v3.1 compliant" if schema_valid else "Schema invalid",
    }


def check_orphan_dependencies(edges: List[Dict]) -> Dict[str, Any]:
    """Check 2: Orphan dependencies."""
    orphans = []
    for edge in edges:
        target = normalize_id(edge.get("TargetDeliverableID", ""))
        if target and target not in VALID_DELIVERABLE_IDS:
            orphans.append({
                "DependencyID": edge["DependencyID"],
                "FromDeliverableID": edge["FromDeliverableID"],
                "TargetDeliverableID": target,
            })
    verdict = "PASS" if len(orphans) == 0 else "WARNING"
    return {
        "verdict": verdict,
        "orphan_count": len(orphans),
        "orphans": orphans,
    }


def check_circular_dependencies(edges: List[Dict]) -> Dict[str, Any]:
    """Check 3: Circular dependencies (Tarjan SCC on single-deliverable scope)."""
    # Build adjacency list
    graph: Dict[str, Set[str]] = defaultdict(set)
    nodes: Set[str] = set()
    for edge in edges:
        src = normalize_id(edge.get("FromDeliverableID", ""))
        tgt = normalize_id(edge.get("TargetDeliverableID", ""))
        if src and tgt:
            direction = edge.get("Direction", "UPSTREAM")
            if direction == "UPSTREAM":
                graph[src].add(tgt)
            elif direction == "DOWNSTREAM":
                graph[tgt].add(src)
            nodes.add(src)
            nodes.add(tgt)

    # Tarjan's algorithm
    index_counter = [0]
    stack: List[str] = []
    lowlink: Dict[str, int] = {}
    index: Dict[str, int] = {}
    on_stack: Dict[str, bool] = {}
    sccs: List[List[str]] = []

    def strongconnect(v: str):
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

    for node in nodes:
        if node not in index:
            strongconnect(node)

    nontrivial_sccs = [s for s in sccs if len(s) > 1]
    return {
        "verdict": "PASS" if len(nontrivial_sccs) == 0 else "BLOCKER",
        "scc_count_nontrivial": len(nontrivial_sccs),
        "sccs": nontrivial_sccs,
    }


def check_anchor_coverage(rows: List[Dict]) -> Dict[str, Any]:
    """Check 4: Anchor coverage."""
    implements_node = [r for r in rows if r.get("AnchorType") == "IMPLEMENTS_NODE"]
    traces = [r for r in rows if r.get("AnchorType") == "TRACES_TO_REQUIREMENT"]
    return {
        "verdict": "PASS" if len(implements_node) > 0 else "WARNING",
        "implements_node_count": len(implements_node),
        "traces_to_requirement_count": len(traces),
    }


def check_misplaced_fields(rows: List[Dict]) -> Dict[str, Any]:
    """Check 5: Misplaced fields."""
    misplaced = []
    for row in rows:
        if row.get("TargetType") != "DELIVERABLE" and row.get("TargetDeliverableID", "").strip():
            misplaced.append(row["DependencyID"])
    return {
        "verdict": "PASS" if len(misplaced) == 0 else "WARNING",
        "misplaced_count": len(misplaced),
        "misplaced_ids": misplaced,
    }


def check_id_format(rows: List[Dict]) -> Dict[str, Any]:
    """Check 6: ID format consistency."""
    import re
    long_form = []
    total_ids = 0
    for row in rows:
        for field in ["FromDeliverableID", "TargetDeliverableID"]:
            val = row.get(field, "").strip()
            if val:
                total_ids += 1
                if not re.match(r"^DEL-\d{2}-\d{2}$", val):
                    long_form.append({"DependencyID": row["DependencyID"], "field": field, "value": val})
    rate = len(long_form) / total_ids if total_ids > 0 else 0.0
    return {
        "verdict": "PASS" if len(long_form) == 0 else "WARNING",
        "long_form_count": len(long_form),
        "normalization_rate": rate,
    }


def check_isolated(edges: List[Dict], scope_ids: Set[str]) -> Dict[str, Any]:
    """Check 7: Isolated deliverables."""
    connected = set()
    for edge in edges:
        connected.add(normalize_id(edge.get("FromDeliverableID", "")))
        connected.add(normalize_id(edge.get("TargetDeliverableID", "")))
    isolated = scope_ids - connected
    return {
        "verdict": "PASS" if len(isolated) == 0 else "WARNING",
        "isolated_count": len(isolated),
        "isolated_ids": list(isolated),
    }


def check_hubs(edges: List[Dict]) -> Dict[str, Any]:
    """Check 8: Hub analysis."""
    degree: Dict[str, int] = defaultdict(int)
    for edge in edges:
        src = normalize_id(edge.get("FromDeliverableID", ""))
        tgt = normalize_id(edge.get("TargetDeliverableID", ""))
        if src:
            degree[src] += 1
        if tgt:
            degree[tgt] += 1
    hubs = {k: v for k, v in degree.items() if v >= HUB_THRESHOLD}
    max_deg = max(degree.values()) if degree else 0
    return {
        "verdict": "PASS" if len(hubs) == 0 else "WARNING",
        "max_degree": max_deg,
        "hubs_above_threshold": len(hubs),
    }


def check_bidirectional(edges: List[Dict]) -> Dict[str, Any]:
    """Check 9: Bidirectional pairs."""
    pairs: Set[Tuple[str, str]] = set()
    for edge in edges:
        src = normalize_id(edge.get("FromDeliverableID", ""))
        tgt = normalize_id(edge.get("TargetDeliverableID", ""))
        if src and tgt:
            pairs.add((src, tgt))
    bidirectional = []
    for a, b in pairs:
        if (b, a) in pairs and a < b:
            bidirectional.append((a, b))
    return {
        "verdict": "PASS" if len(bidirectional) == 0 else "INFO",
        "pairs_found": len(bidirectional),
        "pairs": bidirectional,
    }


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Dependency closure analysis for DEL-06-02")
    parser.add_argument("--execution-root", default=DEFAULT_EXECUTION_ROOT)
    args = parser.parse_args()

    csv_path = os.path.join(args.execution_root, DELIVERABLE_PATH, DEPENDENCIES_FILE)
    print(f"[analyze_closure] Loading: {csv_path}")

    rows, schema_valid, error_msg = load_dependencies(csv_path)
    if error_msg:
        print(f"[analyze_closure] Schema issue: {error_msg}")

    print(f"[analyze_closure] Rows loaded: {len(rows)}")

    # Filter edges
    edges = []
    for row in rows:
        if FILTER_ACTIVE_ONLY and row.get("Status") != "ACTIVE":
            continue
        if row.get("DependencyClass") != EDGE_FILTER_CLASS:
            continue
        if row.get("TargetType") != EDGE_FILTER_TARGET_TYPE:
            continue
        edges.append(row)

    print(f"[analyze_closure] EXECUTION/DELIVERABLE edges: {len(edges)}")

    scope_ids = {DELIVERABLE_ID}

    # Run all 9 checks
    results = {
        "1_schema_compliance": check_schema_compliance(rows, schema_valid),
        "2_orphan_dependencies": check_orphan_dependencies(edges),
        "3_circular_dependencies": check_circular_dependencies(edges),
        "4_anchor_coverage": check_anchor_coverage(rows),
        "5_misplaced_fields": check_misplaced_fields(rows),
        "6_id_format_consistency": check_id_format(rows),
        "7_isolated_deliverables": check_isolated(edges, scope_ids),
        "8_hub_analysis": check_hubs(edges),
        "9_bidirectional_pairs": check_bidirectional(edges),
    }

    # Print results
    print("\n=== CLOSURE CHECK RESULTS ===\n")
    overall = "PASS"
    for name, result in results.items():
        verdict = result["verdict"]
        print(f"  {name}: {verdict}")
        if verdict == "BLOCKER":
            overall = "BLOCKER"
        elif verdict == "WARNING" and overall == "PASS":
            overall = "WARNINGS"

    print(f"\n  OVERALL: {overall}\n")

    # Write JSON summary
    summary = {
        "run_label": "DEL-06-02",
        "run_date": "2026-02-21",
        "scope": DELIVERABLE_ID,
        "overall_status": overall,
        "checks": results,
    }
    print(json.dumps(summary, indent=2, default=str))


if __name__ == "__main__":
    main()
