#!/usr/bin/env python3
"""
Reproducible dependency closure analysis for DEL-02-05.

Run: CLOSURE_DEL-02-05_2026-02-22_2300
Scope: DEL-02-05 (Frontend Workflow Shell Baseline)

Usage:
    python3 analyze_closure.py --execution-root ../../..

This script reproduces the closure checks performed by AUDIT_DEP_CLOSURE.
It reads Dependencies.csv from the target deliverable and its neighbors,
builds the local dependency graph, and runs all 9 core checks.
"""

import argparse
import csv
import json
import os
import sys
from collections import defaultdict
from pathlib import Path


# --- Configuration ---
SCOPE_DELIVERABLE = "DEL-02-05"
SCOPE_FOLDER = "PKG-02_Desktop_UI_Workflow/1_Working/DEL-02-05_Frontend_Workflow_Shell"
SCHEMA_VERSION = "v3.1"
EXPECTED_COLUMNS = 29
EDGE_FILTER_CLASS = "EXECUTION"
EDGE_FILTER_TARGET_TYPE = "DELIVERABLE"
FILTER_ACTIVE_ONLY = True
HUB_THRESHOLD = 20


def find_deliverable_folders(execution_root: Path) -> dict:
    """Discover all DEL-* folders in the execution root."""
    deliverables = {}
    for pkg_dir in sorted(execution_root.iterdir()):
        if not pkg_dir.is_dir() or pkg_dir.name.startswith("_"):
            continue
        working_dir = pkg_dir / "1_Working"
        if not working_dir.is_dir():
            continue
        for del_dir in sorted(working_dir.iterdir()):
            if del_dir.is_dir() and del_dir.name.startswith("DEL-"):
                # Extract short-form ID: DEL-XX-YY from DEL-XX-YY_Description
                parts = del_dir.name.split("_", 1)
                del_id = parts[0]
                deliverables[del_id] = del_dir
    return deliverables


def parse_dependencies_csv(csv_path: Path) -> list:
    """Parse a Dependencies.csv and return list of row dicts."""
    rows = []
    if not csv_path.exists():
        return rows
    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)
    return rows


def check_schema(rows: list, csv_path: Path) -> dict:
    """Check 1: Schema compliance."""
    result = {"verdict": "PASS", "details": []}
    if not rows:
        result["verdict"] = "WARNING"
        result["details"].append(f"Empty CSV: {csv_path}")
        return result
    # Check column count
    col_count = len(rows[0])
    if col_count != EXPECTED_COLUMNS:
        result["verdict"] = "WARNING"
        result["details"].append(
            f"Column count {col_count} != expected {EXPECTED_COLUMNS}"
        )
    # Check schema version
    for row in rows:
        ver = row.get("RegisterSchemaVersion", "")
        if ver != SCHEMA_VERSION:
            result["verdict"] = "WARNING"
            result["details"].append(
                f"Row {row.get('DependencyID', '?')}: schema {ver} != {SCHEMA_VERSION}"
            )
    return result


def get_execution_deliverable_edges(rows: list) -> list:
    """Filter rows to EXECUTION + DELIVERABLE edges."""
    edges = []
    for row in rows:
        if FILTER_ACTIVE_ONLY and row.get("Status", "") != "ACTIVE":
            continue
        if (
            row.get("DependencyClass", "") == EDGE_FILTER_CLASS
            and row.get("TargetType", "") == EDGE_FILTER_TARGET_TYPE
        ):
            edges.append(row)
    return edges


def check_orphans(edges: list, known_deliverables: set) -> dict:
    """Check 2: Orphan dependencies (targets not in workspace)."""
    result = {"verdict": "PASS", "orphans": []}
    for edge in edges:
        target = edge.get("TargetDeliverableID", "").strip()
        if target and target not in known_deliverables:
            result["orphans"].append(
                {
                    "dep_id": edge.get("DependencyID", ""),
                    "target": target,
                }
            )
    if result["orphans"]:
        result["verdict"] = "WARNING"
    return result


def check_cycles_local(edges: list, subject: str) -> dict:
    """Check 3: Circular dependencies (local star topology only)."""
    result = {"verdict": "PASS", "cycles": []}
    upstream_targets = set()
    downstream_targets = set()
    for edge in edges:
        direction = edge.get("Direction", "").upper()
        target = edge.get("TargetDeliverableID", "").strip()
        if direction == "UPSTREAM":
            upstream_targets.add(target)
        elif direction == "DOWNSTREAM":
            downstream_targets.add(target)
    # A local cycle exists if any target appears in both upstream and downstream
    overlap = upstream_targets & downstream_targets
    if overlap:
        result["verdict"] = "BLOCKER"
        for node in overlap:
            result["cycles"].append(f"{subject} -> {node} -> {subject}")
    return result


def check_anchors(rows: list) -> dict:
    """Check 4: Anchor coverage."""
    result = {"verdict": "PASS", "anchors": []}
    has_implements = False
    for row in rows:
        if row.get("DependencyClass", "") == "ANCHOR":
            result["anchors"].append(row.get("DependencyID", ""))
            if row.get("AnchorType", "") == "IMPLEMENTS_NODE":
                has_implements = True
    if not has_implements:
        result["verdict"] = "WARNING"
        result["details"] = "No IMPLEMENTS_NODE anchor found"
    return result


def check_misplaced_fields(rows: list) -> dict:
    """Check 5: Misplaced fields."""
    result = {"verdict": "PASS", "violations": []}
    for row in rows:
        target_type = row.get("TargetType", "")
        target_del_id = row.get("TargetDeliverableID", "").strip()
        if target_type != "DELIVERABLE" and target_del_id:
            result["violations"].append(
                {
                    "dep_id": row.get("DependencyID", ""),
                    "target_type": target_type,
                    "target_del_id": target_del_id,
                }
            )
    if result["violations"]:
        result["verdict"] = "WARNING"
    return result


def check_id_format(rows: list) -> dict:
    """Check 6: ID format consistency."""
    import re

    result = {"verdict": "PASS", "long_form_ids": []}
    pattern = re.compile(r"^DEL-\d{2}-\d{2}$")
    for row in rows:
        for field in ["FromDeliverableID", "TargetDeliverableID"]:
            val = row.get(field, "").strip()
            if val and not pattern.match(val):
                result["long_form_ids"].append(
                    {"dep_id": row.get("DependencyID", ""), "field": field, "value": val}
                )
    if result["long_form_ids"]:
        result["verdict"] = "WARNING"
    return result


def check_isolated(edges: list, subject: str) -> dict:
    """Check 7: Isolated deliverables."""
    result = {"verdict": "PASS"}
    if not edges:
        result["verdict"] = "WARNING"
        result["details"] = f"{subject} has zero EXECUTION+DELIVERABLE edges"
    return result


def check_hubs(edges: list, subject: str) -> dict:
    """Check 8: Hub analysis."""
    result = {"verdict": "PASS", "degree": len(edges)}
    if len(edges) >= HUB_THRESHOLD:
        result["verdict"] = "WARNING"
        result["details"] = (
            f"{subject} degree {len(edges)} >= threshold {HUB_THRESHOLD}"
        )
    return result


def check_bidirectional(
    edges: list, subject: str, neighbor_edges: dict
) -> dict:
    """Check 9: Bidirectional pairs."""
    result = {
        "verdict": "INFO",
        "consistent": [],
        "contradictory": [],
        "unreciprocated": [],
    }
    for edge in edges:
        target = edge.get("TargetDeliverableID", "").strip()
        dep_id = edge.get("DependencyID", "")
        direction = edge.get("Direction", "").upper()
        if target not in neighbor_edges:
            continue
        # Look for reciprocal edge in neighbor's CSV
        found_reciprocal = False
        for nedge in neighbor_edges[target]:
            ntarget = nedge.get("TargetDeliverableID", "").strip()
            if ntarget == subject:
                found_reciprocal = True
                ndirection = nedge.get("Direction", "").upper()
                # Complementary: UPSTREAM<->DOWNSTREAM
                if (direction == "UPSTREAM" and ndirection == "DOWNSTREAM") or (
                    direction == "DOWNSTREAM" and ndirection == "UPSTREAM"
                ):
                    result["consistent"].append(
                        {
                            "forward": dep_id,
                            "reverse": nedge.get("DependencyID", ""),
                            "target": target,
                        }
                    )
                else:
                    result["contradictory"].append(
                        {
                            "forward": dep_id,
                            "reverse": nedge.get("DependencyID", ""),
                            "target": target,
                        }
                    )
                break
        if not found_reciprocal:
            result["unreciprocated"].append({"dep_id": dep_id, "target": target})
    if result["contradictory"]:
        result["verdict"] = "WARNING"
    return result


def main():
    parser = argparse.ArgumentParser(
        description="Reproduce DEL-02-05 dependency closure analysis"
    )
    parser.add_argument(
        "--execution-root",
        default="../../..",
        help="Path to execution/ root (default: ../../..)",
    )
    args = parser.parse_args()

    execution_root = Path(args.execution_root).resolve()
    print(f"Execution root: {execution_root}")

    # Step 0: Discover deliverables
    deliverables = find_deliverable_folders(execution_root)
    print(f"Discovered {len(deliverables)} deliverable folders")

    if SCOPE_DELIVERABLE not in deliverables:
        print(f"ERROR: {SCOPE_DELIVERABLE} not found in workspace")
        sys.exit(1)

    # Step 1: Locate and parse Dependencies.csv
    csv_path = deliverables[SCOPE_DELIVERABLE] / "Dependencies.csv"
    rows = parse_dependencies_csv(csv_path)
    print(f"Parsed {len(rows)} rows from {csv_path}")

    # Step 2: Schema check
    schema_result = check_schema(rows, csv_path)
    print(f"Check 1 (Schema):     {schema_result['verdict']}")

    # Step 3: Build edges
    edges = get_execution_deliverable_edges(rows)
    print(f"EXECUTION+DELIVERABLE edges: {len(edges)}")

    # Load neighbor edges for bidirectional check
    neighbor_targets = set()
    for edge in edges:
        t = edge.get("TargetDeliverableID", "").strip()
        if t:
            neighbor_targets.add(t)

    neighbor_edges = {}
    for nt in neighbor_targets:
        if nt in deliverables:
            npath = deliverables[nt] / "Dependencies.csv"
            nrows = parse_dependencies_csv(npath)
            neighbor_edges[nt] = get_execution_deliverable_edges(nrows)

    # Step 4: Core checks
    known = set(deliverables.keys())

    orphan_result = check_orphans(edges, known)
    print(f"Check 2 (Orphans):    {orphan_result['verdict']}")

    cycle_result = check_cycles_local(edges, SCOPE_DELIVERABLE)
    print(f"Check 3 (Cycles):     {cycle_result['verdict']}")

    anchor_result = check_anchors(rows)
    print(f"Check 4 (Anchors):    {anchor_result['verdict']}")

    misplaced_result = check_misplaced_fields(rows)
    print(f"Check 5 (Misplaced):  {misplaced_result['verdict']}")

    id_result = check_id_format(rows)
    print(f"Check 6 (ID Format):  {id_result['verdict']}")

    isolated_result = check_isolated(edges, SCOPE_DELIVERABLE)
    print(f"Check 7 (Isolated):   {isolated_result['verdict']}")

    hub_result = check_hubs(edges, SCOPE_DELIVERABLE)
    print(f"Check 8 (Hubs):       {hub_result['verdict']}")

    bidir_result = check_bidirectional(edges, SCOPE_DELIVERABLE, neighbor_edges)
    print(f"Check 9 (Bidir):      {bidir_result['verdict']}")
    print(f"  Consistent pairs:   {len(bidir_result['consistent'])}")
    print(f"  Contradictory:      {len(bidir_result['contradictory'])}")
    print(f"  Unreciprocated:     {len(bidir_result['unreciprocated'])}")

    # Overall verdict
    verdicts = [
        schema_result["verdict"],
        orphan_result["verdict"],
        cycle_result["verdict"],
        anchor_result["verdict"],
        misplaced_result["verdict"],
        id_result["verdict"],
        isolated_result["verdict"],
        hub_result["verdict"],
    ]
    if "BLOCKER" in verdicts:
        overall = "BLOCKER"
    elif "WARNING" in verdicts:
        overall = "WARNINGS"
    else:
        overall = "PASS"

    print(f"\nOverall: {overall}")


if __name__ == "__main__":
    main()
