#!/usr/bin/env python3
"""
Reproducible dependency closure analysis script for DEL-02-01.

Run Label: DEL-02-01
Snapshot: CLOSURE_DEL-02-01_2026-02-21
Date: 2026-02-21

This script reproduces the closure analysis performed by AUDIT_DEP_CLOSURE.
It reads the Dependencies.csv for DEL-02-01, validates schema, builds
the dependency graph, and runs all 9 core checks.

Usage:
    python3 analyze_closure.py [--execution-root PATH]

Default execution root: ../../.. (relative to this script's location,
resolving to the execution/ directory).
"""

import csv
import json
import os
import sys
from collections import defaultdict
from pathlib import Path

# --- Configuration ---

SCOPE = ["DEL-02-01"]
DELIVERABLE_PATH = "PKG-02_Desktop_UI_Workflow/1_Working/DEL-02-01_FileTree_Refresh"
FILTER_ACTIVE_ONLY = True
NORMALIZE_IDS = True
EDGE_FILTER_CLASS = "EXECUTION"
EDGE_FILTER_TARGET_TYPE = "DELIVERABLE"
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
    "DEL-08-01", "DEL-08-02", "DEL-08-03", "DEL-08-04",
    "DEL-08-05", "DEL-08-06", "DEL-08-07",
]

EXPECTED_V31_COLUMNS = [
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
    """Normalize a deliverable ID by stripping descriptive suffixes."""
    if not raw_id or not NORMALIZE_IDS:
        return raw_id
    # Pattern: DEL-XX-YY_SomeDescription -> DEL-XX-YY
    import re
    match = re.match(r"(DEL-\d{2}-\d{2})", raw_id)
    if match:
        return match.group(1)
    return raw_id


def load_csv(filepath: str) -> tuple:
    """Load and parse a Dependencies.csv file. Returns (headers, rows, error)."""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            headers = reader.fieldnames or []
            rows = list(reader)
            return headers, rows, None
    except FileNotFoundError:
        return [], [], "FILE_NOT_FOUND"
    except Exception as e:
        return [], [], f"UNREADABLE: {e}"


def validate_schema(headers: list) -> tuple:
    """Validate v3.1 schema columns. Returns (is_valid, missing_columns)."""
    missing = [c for c in EXPECTED_V31_COLUMNS if c not in headers]
    return len(missing) == 0, missing


def build_edges(rows: list) -> list:
    """Extract graph edges from rows matching the edge filter."""
    edges = []
    for row in rows:
        if FILTER_ACTIVE_ONLY and row.get("Status", "") != "ACTIVE":
            continue
        if row.get("DependencyClass", "") != EDGE_FILTER_CLASS:
            continue
        if row.get("TargetType", "") != EDGE_FILTER_TARGET_TYPE:
            continue
        from_id = normalize_id(row.get("FromDeliverableID", ""))
        to_id = normalize_id(row.get("TargetDeliverableID", ""))
        if from_id and to_id:
            edges.append({
                "dependency_id": row.get("DependencyID", ""),
                "from": from_id,
                "to": to_id,
                "direction": row.get("Direction", ""),
                "dependency_type": row.get("DependencyType", ""),
                "status": row.get("Status", ""),
            })
    return edges


def check_orphans(edges: list) -> list:
    """Check for target IDs not in the valid workspace set."""
    orphans = []
    for e in edges:
        if e["to"] not in VALID_DELIVERABLE_IDS:
            orphans.append(e)
    return orphans


def check_self_loops(edges: list) -> list:
    """Check for self-referential edges."""
    return [e for e in edges if e["from"] == e["to"]]


def check_anchors(rows: list) -> dict:
    """Check anchor coverage."""
    implements_node = []
    other_anchors = []
    for row in rows:
        if row.get("DependencyClass", "") == "ANCHOR":
            if row.get("AnchorType", "") == "IMPLEMENTS_NODE":
                implements_node.append(row.get("DependencyID", ""))
            else:
                other_anchors.append(row.get("DependencyID", ""))
    return {
        "implements_node": implements_node,
        "other_anchors": other_anchors,
        "has_implements_node": len(implements_node) > 0,
    }


def check_misplaced_fields(rows: list) -> list:
    """Check for rows where TargetType != DELIVERABLE but TargetDeliverableID is non-empty."""
    misplaced = []
    for row in rows:
        target_type = row.get("TargetType", "")
        target_del_id = row.get("TargetDeliverableID", "").strip()
        if target_type != "DELIVERABLE" and target_del_id:
            misplaced.append({
                "dependency_id": row.get("DependencyID", ""),
                "target_type": target_type,
                "target_deliverable_id": target_del_id,
            })
    return misplaced


def check_id_format(rows: list) -> dict:
    """Check ID format consistency and normalization rate."""
    import re
    total = 0
    needed_normalization = 0
    for row in rows:
        for field in ["FromDeliverableID", "TargetDeliverableID"]:
            val = row.get(field, "").strip()
            if val:
                total += 1
                if not re.match(r"^DEL-\d{2}-\d{2}$", val):
                    needed_normalization += 1
    return {
        "total_ids_checked": total,
        "needed_normalization": needed_normalization,
        "normalization_rate": needed_normalization / total if total > 0 else 0.0,
    }


def check_hub(edges: list, threshold: int) -> dict:
    """Compute degree and check hub status."""
    in_degree = 0
    out_degree = 0
    for e in edges:
        if e["direction"] == "UPSTREAM":
            in_degree += 1
        elif e["direction"] == "DOWNSTREAM":
            out_degree += 1
    total_degree = in_degree + out_degree
    return {
        "in_degree": in_degree,
        "out_degree": out_degree,
        "total_degree": total_degree,
        "exceeds_threshold": total_degree >= threshold,
    }


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Dependency closure analysis for DEL-02-01")
    parser.add_argument("--execution-root", default=None,
                        help="Path to execution/ directory")
    args = parser.parse_args()

    # Resolve execution root
    if args.execution_root:
        exec_root = Path(args.execution_root)
    else:
        # Default: relative to script location
        exec_root = Path(__file__).parent.parent.parent.parent

    csv_path = exec_root / DELIVERABLE_PATH / "Dependencies.csv"
    print(f"Execution root: {exec_root}")
    print(f"CSV path: {csv_path}")
    print(f"Scope: {SCOPE}")
    print()

    # Step 1: Load CSV
    headers, rows, error = load_csv(str(csv_path))
    if error:
        print(f"FAILED: {error}")
        sys.exit(1)
    print(f"Loaded {len(rows)} rows from Dependencies.csv")

    # Step 2: Validate schema
    schema_valid, missing_cols = validate_schema(headers)
    print(f"Schema valid: {schema_valid}")
    if missing_cols:
        print(f"  Missing columns: {missing_cols}")

    # Step 3: Build edges
    edges = build_edges(rows)
    print(f"EXECUTION+DELIVERABLE edges: {len(edges)}")

    # Step 4: Run checks
    print()
    print("=" * 60)
    print("CORE CHECKS")
    print("=" * 60)

    # Check 1: Schema compliance
    verdict_1 = "PASS" if schema_valid else "BLOCKER"
    print(f"[1] Schema Compliance: {verdict_1}")

    # Check 2: Orphan dependencies
    orphans = check_orphans(edges)
    verdict_2 = "PASS" if len(orphans) == 0 else "WARNING"
    print(f"[2] Orphan Dependencies: {verdict_2} ({len(orphans)} orphans)")

    # Check 3: Circular dependencies
    self_loops = check_self_loops(edges)
    verdict_3 = "PASS" if len(self_loops) == 0 else "WARNING"
    print(f"[3] Circular Dependencies: {verdict_3} ({len(self_loops)} self-loops)")
    print(f"    Note: Full cycle detection requires SCOPE=ALL")

    # Check 4: Anchor coverage
    anchor_info = check_anchors(rows)
    verdict_4 = "PASS" if anchor_info["has_implements_node"] else "WARNING"
    print(f"[4] Anchor Coverage: {verdict_4} "
          f"(IMPLEMENTS_NODE: {len(anchor_info['implements_node'])}, "
          f"other: {len(anchor_info['other_anchors'])})")

    # Check 5: Misplaced fields
    misplaced = check_misplaced_fields(rows)
    verdict_5 = "PASS" if len(misplaced) == 0 else "WARNING"
    print(f"[5] Misplaced Fields: {verdict_5} ({len(misplaced)} issues)")

    # Check 6: ID format consistency
    id_info = check_id_format(rows)
    verdict_6 = "PASS" if id_info["needed_normalization"] == 0 else "WARNING"
    print(f"[6] ID Format Consistency: {verdict_6} "
          f"({id_info['needed_normalization']}/{id_info['total_ids_checked']} needed normalization)")

    # Check 7: Isolated deliverables
    verdict_7 = "PASS" if len(edges) > 0 else "WARNING"
    print(f"[7] Isolated Deliverables: {verdict_7} ({len(edges)} edges)")

    # Check 8: Hub analysis
    hub_info = check_hub(edges, HUB_THRESHOLD)
    verdict_8 = "PASS" if not hub_info["exceeds_threshold"] else "WARNING"
    print(f"[8] Hub Analysis: {verdict_8} "
          f"(degree={hub_info['total_degree']}, threshold={HUB_THRESHOLD})")

    # Check 9: Bidirectional pairs
    # Single register cannot detect bidirectional pairs
    verdict_9 = "PASS"
    print(f"[9] Bidirectional Pairs: {verdict_9} (INFO -- single register)")

    print()
    print("=" * 60)
    verdicts = [verdict_1, verdict_2, verdict_3, verdict_4, verdict_5,
                verdict_6, verdict_7, verdict_8, verdict_9]
    if "BLOCKER" in verdicts:
        overall = "BLOCKER"
    elif "WARNING" in verdicts:
        overall = "WARNINGS"
    else:
        overall = "PASS"
    print(f"OVERALL: {overall}")
    print("=" * 60)


if __name__ == "__main__":
    main()
