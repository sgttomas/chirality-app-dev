#!/usr/bin/env python3
"""
analyze_closure.py -- Reproducible dependency closure analysis for DEL-02-04.

Run Label: DEL-02-04
Snapshot:  CLOSURE_DEL-02-04_2026-02-21
Date:      2026-02-21

This script reproduces the analysis performed by AUDIT_DEP_CLOSURE.
It reads the Dependencies.csv for DEL-02-04, builds the directed graph,
and runs all 9 core checks.

Usage:
    python3 analyze_closure.py [--execution-root PATH]

If --execution-root is not provided, defaults to the 'execution/' directory
relative to the repository root (auto-detected via git).
"""

import csv
import json
import os
import sys
import argparse
from collections import defaultdict
from pathlib import Path


# ---------------------------------------------------------------------------
# Configuration (mirrors the brief)
# ---------------------------------------------------------------------------

SCOPE_DELIVERABLE = "DEL-02-04"
SCOPE_CSV_RELPATH = (
    "PKG-02_Desktop_UI_Workflow/1_Working/"
    "DEL-02-04_Multipane_Layout_Theme/Dependencies.csv"
)

FILTER_ACTIVE_ONLY = True
EDGE_FILTER_CLASS = "EXECUTION"
EDGE_FILTER_TARGET_TYPE = "DELIVERABLE"
HUB_THRESHOLD = 20
MAX_CYCLES = 10000
NORMALIZE_IDS = True

# All 32 known workspace deliverable IDs
WORKSPACE_DELIVERABLES = {
    "DEL-01-01", "DEL-01-02",
    "DEL-02-01", "DEL-02-02", "DEL-02-03", "DEL-02-04",
    "DEL-03-01", "DEL-03-02", "DEL-03-03", "DEL-03-04",
    "DEL-03-05", "DEL-03-06",
    "DEL-04-01", "DEL-04-02",
    "DEL-05-01", "DEL-05-02", "DEL-05-03", "DEL-05-04",
    "DEL-06-01", "DEL-06-02", "DEL-06-03", "DEL-06-04", "DEL-06-05",
    "DEL-07-01", "DEL-07-02",
    "DEL-08-01", "DEL-08-02", "DEL-08-03", "DEL-08-04",
    "DEL-08-05", "DEL-08-06", "DEL-08-07",
}

EXPECTED_COLUMNS_V31 = [
    "RegisterSchemaVersion", "DependencyID", "FromPackageID",
    "FromDeliverableID", "FromDeliverableName", "DependencyClass",
    "AnchorType", "Direction", "DependencyType", "TargetType",
    "TargetPackageID", "TargetDeliverableID", "TargetRefID",
    "TargetName", "TargetLocation", "Statement", "EvidenceFile",
    "SourceRef", "EvidenceQuote", "Explicitness", "RequiredMaturity",
    "ProposedMaturity", "SatisfactionStatus", "Confidence", "Origin",
    "FirstSeen", "LastSeen", "Status", "Notes",
]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def normalize_id(raw_id: str) -> str:
    """Strip descriptive suffix from DEL-XX-YY_Label -> DEL-XX-YY."""
    if not raw_id:
        return raw_id
    parts = raw_id.split("_", 1)
    prefix = parts[0]
    # Only normalize if prefix matches DEL-XX-YY or KTY-CC-TT pattern
    if prefix.startswith("DEL-") or prefix.startswith("KTY-"):
        return prefix
    return raw_id


def tarjan_scc(graph: dict) -> list:
    """Tarjan's SCC algorithm. Returns list of SCCs (each a set of nodes)."""
    index_counter = [0]
    stack = []
    on_stack = set()
    index = {}
    lowlink = {}
    result = []

    def strongconnect(node):
        index[node] = index_counter[0]
        lowlink[node] = index_counter[0]
        index_counter[0] += 1
        stack.append(node)
        on_stack.add(node)

        for neighbor in graph.get(node, []):
            if neighbor not in index:
                strongconnect(neighbor)
                lowlink[node] = min(lowlink[node], lowlink[neighbor])
            elif neighbor in on_stack:
                lowlink[node] = min(lowlink[node], index[neighbor])

        if lowlink[node] == index[node]:
            scc = set()
            while True:
                w = stack.pop()
                on_stack.discard(w)
                scc.add(w)
                if w == node:
                    break
            result.append(scc)

    all_nodes = set(graph.keys())
    for neighbors in graph.values():
        all_nodes.update(neighbors)

    for node in sorted(all_nodes):
        if node not in index:
            strongconnect(node)

    return result


# ---------------------------------------------------------------------------
# Main analysis
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Closure analysis for DEL-02-04")
    parser.add_argument(
        "--execution-root",
        default=None,
        help="Path to the execution/ directory",
    )
    args = parser.parse_args()

    # Resolve execution root
    if args.execution_root:
        exec_root = Path(args.execution_root)
    else:
        # Auto-detect from git root
        repo_root = Path(__file__).resolve().parent
        while repo_root != repo_root.parent:
            if (repo_root / ".git").exists():
                break
            repo_root = repo_root.parent
        exec_root = repo_root / "execution"

    csv_path = exec_root / SCOPE_CSV_RELPATH
    if not csv_path.exists():
        print(f"ERROR: Dependencies.csv not found at {csv_path}", file=sys.stderr)
        sys.exit(1)

    # --- Step 1: Parse CSV ---
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        headers = reader.fieldnames or []
        rows = list(reader)

    print(f"Parsed {len(rows)} rows from {csv_path}")
    print(f"Headers: {headers}")

    # --- Step 2: Schema validation ---
    missing_cols = set(EXPECTED_COLUMNS_V31) - set(headers)
    extra_cols = set(headers) - set(EXPECTED_COLUMNS_V31)
    schema_valid = len(missing_cols) == 0
    print(f"\nCheck 1 - Schema compliance: {'PASS' if schema_valid else 'FAIL'}")
    if missing_cols:
        print(f"  Missing columns: {missing_cols}")
    if extra_cols:
        print(f"  Extra columns: {extra_cols}")

    # --- Step 3: Build graph ---
    graph = defaultdict(list)  # adjacency list
    edge_rows = []
    anchor_rows = []
    all_rows = []

    for row in rows:
        status = row.get("Status", "").strip()
        if FILTER_ACTIVE_ONLY and status != "ACTIVE":
            continue
        all_rows.append(row)

        dep_class = row.get("DependencyClass", "").strip()
        target_type = row.get("TargetType", "").strip()

        if dep_class == "ANCHOR":
            anchor_rows.append(row)

        from_id = row.get("FromDeliverableID", "").strip()
        target_del_id = row.get("TargetDeliverableID", "").strip()

        if NORMALIZE_IDS:
            from_id = normalize_id(from_id)
            target_del_id = normalize_id(target_del_id)

        if (
            dep_class == EDGE_FILTER_CLASS
            and target_type == EDGE_FILTER_TARGET_TYPE
            and from_id
            and target_del_id
        ):
            graph[from_id].append(target_del_id)
            edge_rows.append(row)

    print(f"\nGraph: {len(set(graph.keys()) | {n for ns in graph.values() for n in ns})} nodes, {sum(len(v) for v in graph.values())} edges")

    # --- Check 2: Orphan dependencies ---
    orphans = []
    for row in edge_rows:
        target = normalize_id(row.get("TargetDeliverableID", "").strip()) if NORMALIZE_IDS else row.get("TargetDeliverableID", "").strip()
        if target and target not in WORKSPACE_DELIVERABLES:
            orphans.append((row.get("DependencyID", ""), target))

    print(f"\nCheck 2 - Orphan dependencies: {'PASS' if not orphans else 'WARNING'}")
    if orphans:
        for dep_id, target in orphans:
            print(f"  {dep_id} -> {target} (NOT FOUND)")

    # --- Check 3: Circular dependencies (Tarjan) ---
    sccs = tarjan_scc(dict(graph))
    non_trivial = [scc for scc in sccs if len(scc) > 1]
    print(f"\nCheck 3 - Circular dependencies: {'PASS' if not non_trivial else 'BLOCKER'}")
    print(f"  SCCs: {len(sccs)} total, {len(non_trivial)} non-trivial")
    for scc in non_trivial:
        print(f"  Cycle: {sorted(scc)}")

    # --- Check 4: Anchor coverage ---
    has_implements = any(
        r.get("AnchorType", "").strip() == "IMPLEMENTS_NODE" for r in anchor_rows
    )
    print(f"\nCheck 4 - Anchor coverage: {'PASS' if has_implements else 'WARNING'}")
    print(f"  ANCHOR rows: {len(anchor_rows)}, IMPLEMENTS_NODE present: {has_implements}")

    # --- Check 5: Misplaced fields ---
    misplaced = []
    for row in all_rows:
        target_type = row.get("TargetType", "").strip()
        target_del_id = row.get("TargetDeliverableID", "").strip()
        if target_type != "DELIVERABLE" and target_del_id:
            misplaced.append((row.get("DependencyID", ""), target_type, target_del_id))

    print(f"\nCheck 5 - Misplaced fields: {'PASS' if not misplaced else 'WARNING'}")
    if misplaced:
        for dep_id, tt, td in misplaced:
            print(f"  {dep_id}: TargetType={tt} but TargetDeliverableID={td}")

    # --- Check 6: ID format consistency ---
    ids_checked = set()
    ids_normalized = set()
    for row in all_rows:
        for field in ["FromDeliverableID", "TargetDeliverableID"]:
            raw = row.get(field, "").strip()
            if raw:
                ids_checked.add(raw)
                if normalize_id(raw) != raw:
                    ids_normalized.add(raw)

    norm_rate = (len(ids_normalized) / len(ids_checked) * 100) if ids_checked else 0.0
    print(f"\nCheck 6 - ID format consistency: PASS")
    print(f"  IDs checked: {len(ids_checked)}, needing normalization: {len(ids_normalized)} ({norm_rate:.1f}%)")

    # --- Check 7: Isolated deliverables ---
    all_nodes = set(graph.keys())
    for ns in graph.values():
        all_nodes.update(ns)
    in_degree = defaultdict(int)
    out_degree = defaultdict(int)
    for src, targets in graph.items():
        out_degree[src] += len(targets)
        for t in targets:
            in_degree[t] += 1

    # Only check the in-scope deliverable
    scope_degree = out_degree.get(SCOPE_DELIVERABLE, 0) + in_degree.get(SCOPE_DELIVERABLE, 0)
    isolated = scope_degree == 0
    print(f"\nCheck 7 - Isolated deliverables: {'WARNING' if isolated else 'PASS'}")
    print(f"  {SCOPE_DELIVERABLE} degree: {scope_degree}")

    # --- Check 8: Hub analysis ---
    max_deg = 0
    for node in all_nodes:
        deg = out_degree.get(node, 0) + in_degree.get(node, 0)
        max_deg = max(max_deg, deg)
    hubs = [n for n in all_nodes if (out_degree.get(n, 0) + in_degree.get(n, 0)) >= HUB_THRESHOLD]
    print(f"\nCheck 8 - Hub analysis: {'WARNING' if hubs else 'PASS'}")
    print(f"  Max degree: {max_deg}, threshold: {HUB_THRESHOLD}, hubs: {len(hubs)}")

    # --- Check 9: Bidirectional pairs ---
    bidir = []
    edge_set = set()
    for src, targets in graph.items():
        for t in targets:
            edge_set.add((src, t))
    for a, b in edge_set:
        if (b, a) in edge_set and a < b:
            bidir.append((a, b))

    print(f"\nCheck 9 - Bidirectional pairs: {'INFO' if bidir else 'PASS'}")
    if bidir:
        for a, b in bidir:
            print(f"  {a} <-> {b}")

    # --- Summary ---
    all_pass = (
        schema_valid
        and not orphans
        and not non_trivial
        and has_implements
        and not misplaced
        and not isolated
        and not hubs
    )
    print(f"\n{'='*60}")
    print(f"Overall closure status: {'PASS' if all_pass else 'ISSUES FOUND'}")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
