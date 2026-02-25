#!/usr/bin/env python3
"""
Reproducible dependency closure analysis for DEL-03-07.

Usage:
    python3 analyze_closure.py [--execution-root EXECUTION_ROOT]

Defaults:
    --execution-root execution/

This script reproduces the AUDIT_DEP_CLOSURE analysis performed on 2026-02-22
for snapshot CLOSURE_DEL-03-07_2026-02-22_0830.

Parameters used:
    SCOPE = DEL-03-07
    FILTER_ACTIVE_ONLY = True
    NORMALIZE_IDS = True
    EDGE_FILTER = DependencyClass=EXECUTION, TargetType=DELIVERABLE
    HUB_THRESHOLD = 20
    MAX_CYCLES = 10000
"""

import csv
import json
import os
import sys
import re
from collections import defaultdict
from pathlib import Path

# --- Configuration ---
SCOPE = ["DEL-03-07"]
FILTER_ACTIVE_ONLY = True
NORMALIZE_IDS = True
EDGE_FILTER_CLASS = "EXECUTION"
EDGE_FILTER_TARGET_TYPE = "DELIVERABLE"
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


def normalize_id(raw_id: str) -> str:
    """Strip descriptive suffix: DEL-XX-YY_Label -> DEL-XX-YY"""
    if not NORMALIZE_IDS:
        return raw_id
    match = re.match(r"(DEL-\d+-\d+)", raw_id)
    return match.group(1) if match else raw_id


def discover_deliverables(execution_root: str) -> dict:
    """Discover all deliverable folders and their Dependencies.csv paths."""
    deliverables = {}
    root = Path(execution_root)
    for pkg_dir in sorted(root.iterdir()):
        if not pkg_dir.is_dir() or pkg_dir.name.startswith("_"):
            continue
        working_dir = pkg_dir / "1_Working"
        if not working_dir.is_dir():
            continue
        for del_dir in sorted(working_dir.iterdir()):
            if not del_dir.is_dir() or not del_dir.name.startswith("DEL-"):
                continue
            del_id = normalize_id(del_dir.name)
            csv_path = del_dir / "Dependencies.csv"
            deliverables[del_id] = {
                "folder": str(del_dir),
                "csv_path": str(csv_path) if csv_path.exists() else None,
                "csv_exists": csv_path.exists(),
            }
    return deliverables


def parse_csv(csv_path: str) -> tuple:
    """Parse Dependencies.csv; return (rows, schema_valid, schema_errors)."""
    rows = []
    schema_errors = []
    with open(csv_path, "r") as f:
        reader = csv.DictReader(f)
        actual_cols = reader.fieldnames or []
        missing = [c for c in REQUIRED_COLUMNS_V31 if c not in actual_cols]
        if missing:
            schema_errors.append(f"Missing columns: {missing}")
        for row in reader:
            rows.append(row)
    return rows, len(schema_errors) == 0, schema_errors


def build_edges(rows: list) -> list:
    """Extract graph edges from parsed rows."""
    edges = []
    for r in rows:
        if FILTER_ACTIVE_ONLY and r.get("Status") != "ACTIVE":
            continue
        if r.get("DependencyClass") != EDGE_FILTER_CLASS:
            continue
        if r.get("TargetType") != EDGE_FILTER_TARGET_TYPE:
            continue
        from_id = normalize_id(r.get("FromDeliverableID", ""))
        target_id = normalize_id(r.get("TargetDeliverableID", ""))
        if from_id and target_id:
            edges.append({
                "dep_id": r["DependencyID"],
                "from": from_id,
                "to": target_id,
                "direction": r.get("Direction", "UNKNOWN"),
                "dep_type": r.get("DependencyType", "UNKNOWN"),
            })
    return edges


def check_orphans(edges: list, workspace_dels: set) -> list:
    """Check for target deliverable IDs not in workspace."""
    orphans = []
    for e in edges:
        if e["to"] not in workspace_dels:
            orphans.append(e)
    return orphans


def check_bidirectional(edges: list) -> list:
    """Find bidirectional pairs (A->B and B->A both present)."""
    directed = defaultdict(list)
    for e in edges:
        if e["direction"] == "UPSTREAM":
            directed[(e["from"], e["to"])].append(e["dep_id"])
        elif e["direction"] == "DOWNSTREAM":
            directed[(e["to"], e["from"])].append(e["dep_id"])

    pairs = []
    seen = set()
    for (s, t), fwd_deps in directed.items():
        if (t, s) in directed and (s, t) not in seen and (t, s) not in seen:
            pairs.append({
                "node_a": s,
                "node_b": t,
                "forward_deps": fwd_deps,
                "reverse_deps": directed[(t, s)],
            })
            seen.add((s, t))
            seen.add((t, s))
    return pairs


def check_misplaced(rows: list) -> list:
    """Rows where TargetType != DELIVERABLE but TargetDeliverableID is set."""
    misplaced = []
    for r in rows:
        if r.get("DependencyClass") != EDGE_FILTER_CLASS:
            continue
        if FILTER_ACTIVE_ONLY and r.get("Status") != "ACTIVE":
            continue
        if r.get("TargetType") != "DELIVERABLE" and r.get("TargetDeliverableID", "").strip():
            misplaced.append(r["DependencyID"])
    return misplaced


def main():
    import argparse

    parser = argparse.ArgumentParser(description="DEL-03-07 closure analysis")
    parser.add_argument(
        "--execution-root",
        default="execution/",
        help="Path to execution root (default: execution/)",
    )
    args = parser.parse_args()

    execution_root = args.execution_root

    # Step 0: Discover workspace
    all_dels = discover_deliverables(execution_root)
    workspace_ids = set(all_dels.keys())
    scope_dels = {k: v for k, v in all_dels.items() if k in SCOPE}

    if not scope_dels:
        print("FAILED_INPUTS: No deliverables found in scope.")
        sys.exit(1)

    print(f"Workspace deliverables: {len(all_dels)}")
    print(f"Scope deliverables: {len(scope_dels)}")
    print()

    # Step 1-2: Parse and validate
    all_rows = []
    for del_id, info in scope_dels.items():
        if not info["csv_exists"]:
            print(f"  {del_id}: MISSING_DEPENDENCIES_CSV")
            continue
        rows, valid, errors = parse_csv(info["csv_path"])
        status = "OK" if valid else f"SCHEMA_INVALID: {errors}"
        print(f"  {del_id}: {len(rows)} rows, schema={status}")
        if valid:
            all_rows.extend(rows)

    print()

    # Step 3: Build edges
    edges = build_edges(all_rows)
    print(f"Graph edges (EXECUTION/DELIVERABLE): {len(edges)}")
    for e in edges:
        print(f"  {e['dep_id']}: {e['from']} --({e['direction']}, {e['dep_type']})--> {e['to']}")
    print()

    # Step 4: Core checks
    # Orphans
    orphans = check_orphans(edges, workspace_ids)
    print(f"Orphan check: {'PASS' if not orphans else 'FAIL'} ({len(orphans)} orphans)")

    # Anchors
    anchors = [r for r in all_rows if r.get("DependencyClass") == "ANCHOR"]
    impl_nodes = [r for r in anchors if r.get("AnchorType") == "IMPLEMENTS_NODE"]
    print(f"Anchor check: {'PASS' if impl_nodes else 'WARNING'} ({len(impl_nodes)} IMPLEMENTS_NODE)")

    # Misplaced
    misplaced = check_misplaced(all_rows)
    print(f"Misplaced check: {'PASS' if not misplaced else 'WARNING'} ({len(misplaced)} misplaced)")

    # Bidirectional
    bidir = check_bidirectional(edges)
    print(f"Bidirectional pairs: {len(bidir)}")
    for p in bidir:
        print(f"  {p['node_a']} <-> {p['node_b']}")

    # Hub
    degree = len(edges)
    is_hub = degree >= HUB_THRESHOLD
    print(f"Hub check: {'HUB' if is_hub else 'PASS'} (degree={degree}, threshold={HUB_THRESHOLD})")

    # Isolated
    is_isolated = degree == 0
    print(f"Isolated check: {'WARNING' if is_isolated else 'PASS'}")

    # Summary
    print()
    status = "PASS"
    if bidir:
        status = "WARNINGS"
    if orphans:
        status = "WARNINGS"
    print(f"Closure status: {status}")

    # Output JSON summary
    summary = {
        "scope": SCOPE,
        "closure_status": status,
        "edges": len(edges),
        "orphans": len(orphans),
        "bidirectional_pairs": len(bidir),
        "degree": degree,
        "is_hub": is_hub,
        "anchors": len(anchors),
        "misplaced": len(misplaced),
    }
    print()
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
