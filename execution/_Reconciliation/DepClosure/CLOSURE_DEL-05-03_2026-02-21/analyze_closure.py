#!/usr/bin/env python3
"""
Reproducible dependency closure analysis script for DEL-05-03.

Snapshot: CLOSURE_DEL-05-03_2026-02-21
Date: 2026-02-21
Scope: DEL-05-03 (Lifecycle State Handling)

This script reads the Dependencies.csv for DEL-05-03, applies edge filters,
builds the local dependency graph, and runs all 9 core checks.

Usage:
    python3 analyze_closure.py [--execution-root EXECUTION_ROOT]

Defaults:
    --execution-root: execution/ (relative to repo root)
"""

import csv
import json
import os
import re
import sys
from collections import defaultdict
from pathlib import Path


# --- Configuration ---

SCOPE = ["DEL-05-03"]
FILTER_ACTIVE_ONLY = True
NORMALIZE_IDS = True
EDGE_FILTER_DEP_CLASS = "EXECUTION"
EDGE_FILTER_TARGET_TYPE = "DELIVERABLE"
HUB_THRESHOLD = 20
MAX_CYCLES = 10000

# All 32 known deliverable IDs in the workspace
KNOWN_DELIVERABLE_IDS = {
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
    """Normalize long-form IDs by stripping descriptive suffixes."""
    if not raw_id:
        return raw_id
    match = re.match(r"(DEL-\d{2}-\d{2})", raw_id)
    if match:
        return match.group(1)
    match = re.match(r"(KTY-\d{2}-\d{2})", raw_id)
    if match:
        return match.group(1)
    return raw_id


def find_deliverable_path(execution_root: Path, del_id: str) -> Path | None:
    """Find the folder for a deliverable ID by scanning the execution root."""
    for pkg_dir in sorted(execution_root.iterdir()):
        if not pkg_dir.is_dir() or pkg_dir.name.startswith("_"):
            continue
        working_dir = pkg_dir / "1_Working"
        if not working_dir.is_dir():
            continue
        for del_dir in sorted(working_dir.iterdir()):
            if del_dir.is_dir() and del_dir.name.startswith(del_id):
                return del_dir
    return None


def load_dependencies_csv(csv_path: Path) -> tuple[list[dict], list[str]]:
    """Load and return rows from a Dependencies.csv, plus any schema errors."""
    errors = []
    rows = []
    try:
        with open(csv_path, "r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            headers = reader.fieldnames or []
            # Check required columns
            missing = [c for c in REQUIRED_COLUMNS_V31 if c not in headers]
            if missing:
                errors.append(f"Missing columns: {', '.join(missing)}")
                return rows, errors
            for i, row in enumerate(reader, start=2):
                rows.append(row)
    except Exception as e:
        errors.append(f"Read error: {e}")
    return rows, errors


def run_checks(rows: list[dict], csv_path: str) -> dict:
    """Run all 9 core checks and return results."""
    results = {}

    # Separate by class
    anchor_rows = [r for r in rows if r.get("DependencyClass") == "ANCHOR"]
    execution_rows = [r for r in rows if r.get("DependencyClass") == "EXECUTION"]

    # Filter edges
    filtered_edges = []
    for r in execution_rows:
        if FILTER_ACTIVE_ONLY and r.get("Status") != "ACTIVE":
            continue
        if r.get("DependencyClass") != EDGE_FILTER_DEP_CLASS:
            continue
        if r.get("TargetType") != EDGE_FILTER_TARGET_TYPE:
            continue
        from_id = normalize_id(r.get("FromDeliverableID", "")) if NORMALIZE_IDS else r.get("FromDeliverableID", "")
        target_id = normalize_id(r.get("TargetDeliverableID", "")) if NORMALIZE_IDS else r.get("TargetDeliverableID", "")
        if from_id and target_id:
            filtered_edges.append({
                "dependency_id": r.get("DependencyID", ""),
                "from": from_id,
                "to": target_id,
                "direction": r.get("Direction", ""),
                "dependency_type": r.get("DependencyType", ""),
                "confidence": r.get("Confidence", ""),
            })

    # Check 1: Schema compliance
    results["schema_compliance"] = {
        "verdict": "PASS",
        "detail": f"v3.1 valid, {len(rows)} rows, {csv_path}",
    }

    # Check 2: Orphan dependencies
    orphans = []
    for e in filtered_edges:
        if e["to"] not in KNOWN_DELIVERABLE_IDS:
            orphans.append(e)
    results["orphan_dependencies"] = {
        "verdict": "PASS" if not orphans else "WARNING",
        "orphan_count": len(orphans),
        "orphans": orphans,
    }

    # Check 3: Circular dependencies (Tarjan SCC on local graph)
    graph = defaultdict(list)
    nodes = set()
    for e in filtered_edges:
        if e["direction"] == "UPSTREAM":
            graph[e["from"]].append(e["to"])
        elif e["direction"] == "DOWNSTREAM":
            graph[e["from"]].append(e["to"])
        nodes.add(e["from"])
        nodes.add(e["to"])

    # Simple Tarjan for small graphs
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
        "verdict": "PASS" if not sccs else "BLOCKER",
        "scc_count": len(sccs),
        "sccs": sccs,
    }

    # Check 4: Anchor coverage
    implements_nodes = [r for r in anchor_rows if r.get("AnchorType") == "IMPLEMENTS_NODE"]
    results["anchor_coverage"] = {
        "verdict": "PASS" if implements_nodes else "WARNING",
        "implements_node_count": len(implements_nodes),
        "total_anchor_count": len(anchor_rows),
    }

    # Check 5: Misplaced fields
    misplaced = []
    for r in rows:
        if r.get("TargetType") != "DELIVERABLE" and r.get("TargetDeliverableID", "").strip():
            misplaced.append(r.get("DependencyID", ""))
    results["misplaced_fields"] = {
        "verdict": "PASS" if not misplaced else "WARNING",
        "misplaced_count": len(misplaced),
        "misplaced_ids": misplaced,
    }

    # Check 6: ID format consistency
    id_pattern = re.compile(r"^DEL-\d{2}-\d{2}$")
    ids_needing_norm = []
    for r in rows:
        for field in ["FromDeliverableID", "TargetDeliverableID"]:
            val = r.get(field, "").strip()
            if val and not id_pattern.match(val):
                ids_needing_norm.append({"dependency_id": r.get("DependencyID", ""), "field": field, "value": val})
    results["id_format_consistency"] = {
        "verdict": "PASS" if not ids_needing_norm else "WARNING",
        "ids_requiring_normalization": len(ids_needing_norm),
        "details": ids_needing_norm,
    }

    # Check 7: Isolated deliverables
    degree = len(filtered_edges)
    results["isolated_deliverables"] = {
        "verdict": "PASS" if degree > 0 else "WARNING",
        "degree": degree,
    }

    # Check 8: Hub analysis
    results["hub_analysis"] = {
        "verdict": "PASS" if degree < HUB_THRESHOLD else "WARNING",
        "degree": degree,
        "threshold": HUB_THRESHOLD,
    }

    # Check 9: Bidirectional pairs (limited in single-deliverable scope)
    results["bidirectional_pairs"] = {
        "verdict": "PASS",
        "pairs_detected": 0,
        "note": "Single-deliverable scope; reciprocal edges not visible",
    }

    return results


def main():
    # Parse args
    execution_root_str = "execution/"
    for i, arg in enumerate(sys.argv[1:], 1):
        if arg == "--execution-root" and i < len(sys.argv) - 1:
            execution_root_str = sys.argv[i + 1]

    # Resolve paths
    repo_root = Path(__file__).resolve().parent.parent.parent.parent.parent
    execution_root = repo_root / execution_root_str

    if not execution_root.is_dir():
        print(f"ERROR: execution root not found: {execution_root}")
        sys.exit(1)

    # Find DEL-05-03
    del_path = find_deliverable_path(execution_root, "DEL-05-03")
    if not del_path:
        print("ERROR: DEL-05-03 folder not found")
        sys.exit(1)

    csv_path = del_path / "Dependencies.csv"
    if not csv_path.is_file():
        print(f"ERROR: Dependencies.csv not found at {csv_path}")
        sys.exit(1)

    print(f"Loading: {csv_path}")
    rows, errors = load_dependencies_csv(csv_path)
    if errors:
        print(f"Schema errors: {errors}")
        sys.exit(1)

    print(f"Rows parsed: {len(rows)}")
    results = run_checks(rows, str(csv_path))

    # Print results
    print("\n=== Core Check Results ===\n")
    for check_name, result in results.items():
        verdict = result.get("verdict", "UNKNOWN")
        print(f"  {check_name}: {verdict}")

    # Determine overall status
    verdicts = [r["verdict"] for r in results.values()]
    if "BLOCKER" in verdicts:
        overall = "BLOCKER"
    elif "WARNING" in verdicts:
        overall = "WARNINGS"
    else:
        overall = "PASS"

    print(f"\n  Overall: {overall}")

    # Write JSON
    output = {
        "scope": "DEL-05-03",
        "csv_path": str(csv_path),
        "total_rows": len(rows),
        "checks": results,
        "overall": overall,
    }
    print(f"\nJSON output:\n{json.dumps(output, indent=2)}")


if __name__ == "__main__":
    main()
