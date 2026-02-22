#!/usr/bin/env python3
"""
Reproducible dependency closure analysis script for DEL-06-03.

Snapshot: CLOSURE_DEL-06-03_2026-02-21
Scope:    DEL-06-03 (single deliverable)
Filters:  DependencyClass=EXECUTION, TargetType=DELIVERABLE, Status=ACTIVE

Usage:
    python analyze_closure.py --execution-root ../../..

This script reads the Dependencies.csv for DEL-06-03 and all workspace
Dependencies.csv files, applies the edge filter, builds a directed graph,
and runs all 9 core checks.
"""

import csv
import json
import os
import sys
from collections import defaultdict
from pathlib import Path


# --- Configuration ---
SCOPE_DELIVERABLE = "DEL-06-03"
SCOPE_CSV_RELPATH = (
    "PKG-06_Agent_Suite_Governance/1_Working/"
    "DEL-06-03_Cross_Deliverable_Workflows/Dependencies.csv"
)
EDGE_FILTER_CLASS = "EXECUTION"
EDGE_FILTER_TARGET_TYPE = "DELIVERABLE"
FILTER_ACTIVE_ONLY = True
HUB_THRESHOLD = 20
MAX_CYCLES = 10000

REQUIRED_COLUMNS_V31 = [
    "RegisterSchemaVersion", "DependencyID", "FromPackageID",
    "FromDeliverableID", "FromDeliverableName", "DependencyClass",
    "AnchorType", "Direction", "DependencyType", "TargetType",
    "TargetPackageID", "TargetDeliverableID", "TargetRefID",
    "TargetName", "TargetLocation", "Statement", "EvidenceFile",
    "SourceRef", "EvidenceQuote", "Explicitness", "RequiredMaturity",
    "ProposedMaturity", "SatisfactionStatus", "Confidence", "Origin",
    "FirstSeen", "LastSeen", "Status", "Notes",
]

# All 32 valid deliverable IDs in the workspace
VALID_DELIVERABLE_IDS = {
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


def normalize_id(raw_id: str) -> str:
    """Strip descriptive suffix from DEL-XX-YY_Label format."""
    if not raw_id:
        return raw_id
    parts = raw_id.split("_", 1)
    prefix = parts[0]
    if prefix.startswith("DEL-") and len(prefix.split("-")) == 3:
        return prefix
    return raw_id


def read_csv(filepath: str) -> list[dict]:
    """Read a CSV file and return list of row dicts."""
    rows = []
    with open(filepath, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)
    return rows


def validate_schema(rows: list[dict], filepath: str) -> tuple[bool, list[str]]:
    """Validate v3.1 schema columns are present."""
    if not rows:
        return False, ["Empty CSV"]
    actual_cols = set(rows[0].keys())
    missing = [c for c in REQUIRED_COLUMNS_V31 if c not in actual_cols]
    if missing:
        return False, [f"Missing columns: {missing}"]
    return True, []


def filter_edges(rows: list[dict]) -> list[dict]:
    """Apply edge filter: EXECUTION + DELIVERABLE + ACTIVE."""
    result = []
    for row in rows:
        dep_class = row.get("DependencyClass", "").strip()
        target_type = row.get("TargetType", "").strip()
        status = row.get("Status", "").strip()
        if dep_class != EDGE_FILTER_CLASS:
            continue
        if target_type != EDGE_FILTER_TARGET_TYPE:
            continue
        if FILTER_ACTIVE_ONLY and status != "ACTIVE":
            continue
        from_id = normalize_id(row.get("FromDeliverableID", "").strip())
        target_id = normalize_id(row.get("TargetDeliverableID", "").strip())
        if from_id and target_id:
            result.append({
                "dependency_id": row.get("DependencyID", ""),
                "from": from_id,
                "to": target_id,
                "direction": row.get("Direction", ""),
                "dependency_type": row.get("DependencyType", ""),
            })
    return result


def find_sccs(graph: dict[str, set[str]]) -> list[list[str]]:
    """Tarjan's SCC algorithm."""
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

        for w in graph.get(v, set()):
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

    for node in list(graph.keys()):
        if node not in index:
            strongconnect(node)

    return sccs


def main():
    import argparse
    parser = argparse.ArgumentParser(
        description="Dependency closure analysis for DEL-06-03"
    )
    parser.add_argument(
        "--execution-root",
        default="../../..",
        help="Path to execution/ root (default: ../../..)",
    )
    args = parser.parse_args()
    exec_root = Path(args.execution_root).resolve()

    # --- Step 1: Locate and read primary CSV ---
    primary_csv = exec_root / SCOPE_CSV_RELPATH
    if not primary_csv.exists():
        print(f"FAILED: Dependencies.csv not found at {primary_csv}")
        sys.exit(1)

    rows = read_csv(str(primary_csv))
    print(f"Read {len(rows)} rows from {primary_csv}")

    # --- Step 2: Schema validation ---
    valid, errors = validate_schema(rows, str(primary_csv))
    print(f"Schema valid: {valid}")
    if errors:
        for e in errors:
            print(f"  Schema error: {e}")

    # --- Step 3: Filter edges ---
    edges = filter_edges(rows)
    print(f"EXECUTION/DELIVERABLE edges from DEL-06-03: {len(edges)}")
    for e in edges:
        print(f"  {e['from']} -> {e['to']} ({e['dependency_id']}, "
              f"{e['direction']}, {e['dependency_type']})")

    # --- Step 4: Scan workspace for incoming edges ---
    incoming = []
    for csv_path in exec_root.rglob("Dependencies.csv"):
        if "DEL-06-03" in str(csv_path):
            continue  # skip self
        try:
            other_rows = read_csv(str(csv_path))
            for edge in filter_edges(other_rows):
                if normalize_id(edge["to"]) == SCOPE_DELIVERABLE:
                    incoming.append({**edge, "source_file": str(csv_path)})
        except Exception:
            pass

    print(f"Incoming EXECUTION/DELIVERABLE edges to DEL-06-03: {len(incoming)}")
    for e in incoming:
        print(f"  {e['from']} -> {e['to']} ({e['dependency_id']})")

    # --- Step 5: Build graph and detect SCCs ---
    graph = defaultdict(set)
    for e in edges:
        graph[e["from"]].add(e["to"])
    for e in incoming:
        graph[e["from"]].add(e["to"])
    # Ensure all nodes are in graph
    for e in edges:
        if e["to"] not in graph:
            graph[e["to"]] = set()
    for e in incoming:
        if e["from"] not in graph:
            graph[e["from"]] = set()

    sccs = find_sccs(graph)
    print(f"SCCs (size > 1): {len(sccs)}")
    for scc in sccs:
        print(f"  SCC: {scc}")

    # --- Step 6: Orphan check ---
    orphans = []
    for e in edges:
        if normalize_id(e["to"]) not in VALID_DELIVERABLE_IDS:
            orphans.append(e)
    print(f"Orphan dependencies: {len(orphans)}")

    # --- Step 7: Anchor check ---
    anchors = [r for r in rows if r.get("DependencyClass") == "ANCHOR"]
    implements = [
        r for r in anchors if r.get("AnchorType") == "IMPLEMENTS_NODE"
    ]
    print(f"Anchors: {len(anchors)}, IMPLEMENTS_NODE: {len(implements)}")

    # --- Step 8: Misplaced fields ---
    misplaced = [
        r for r in rows
        if r.get("TargetType", "").strip() != "DELIVERABLE"
        and r.get("TargetDeliverableID", "").strip() != ""
    ]
    print(f"Misplaced fields: {len(misplaced)}")

    # --- Step 9: ID format ---
    long_form = []
    for r in rows:
        for field in ["FromDeliverableID", "TargetDeliverableID"]:
            raw = r.get(field, "").strip()
            if raw and normalize_id(raw) != raw:
                long_form.append((r.get("DependencyID"), field, raw))
    print(f"Long-form IDs: {len(long_form)}")

    # --- Step 10: Bidirectional pairs ---
    all_edges_set = set()
    for e in edges:
        all_edges_set.add((e["from"], e["to"]))
    for e in incoming:
        all_edges_set.add((e["from"], e["to"]))
    bidirectional = []
    seen = set()
    for a, b in all_edges_set:
        pair = tuple(sorted([a, b]))
        if (b, a) in all_edges_set and pair not in seen:
            bidirectional.append((a, b))
            seen.add(pair)
    print(f"Bidirectional pairs: {len(bidirectional)}")
    for a, b in bidirectional:
        print(f"  {a} <-> {b}")

    # --- Summary ---
    degree = len(edges) + len(incoming)
    print(f"\nDEL-06-03 degree: {degree} (hub threshold: {HUB_THRESHOLD})")
    print(f"Hub: {'YES' if degree >= HUB_THRESHOLD else 'NO'}")
    print(f"Isolated: {'YES' if degree == 0 else 'NO'}")

    status = "PASS"
    if sccs or orphans:
        status = "WARNINGS"
    print(f"\nOverall status: {status}")


if __name__ == "__main__":
    main()
