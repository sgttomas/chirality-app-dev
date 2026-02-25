#!/usr/bin/env python3
"""
analyze_closure.py -- Reproducible dependency closure analysis for DEL-07-03

Snapshot: CLOSURE_DEL-07-03_2026-02-22_1430
Generated: 2026-02-22

Usage:
    python3 analyze_closure.py [--execution-root PATH]

Defaults to execution/ relative to the repository root (auto-detected via git).
"""

import csv
import json
import os
import subprocess
import sys
from collections import defaultdict
from pathlib import Path


# --- Configuration ---

SCOPE = ["DEL-07-03"]
FILTER_ACTIVE_ONLY = True
NORMALIZE_IDS = True
EDGE_FILTER_DEP_CLASS = "EXECUTION"
EDGE_FILTER_TARGET_TYPE = "DELIVERABLE"
HUB_THRESHOLD = 20


def find_repo_root():
    """Find the git repository root."""
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            capture_output=True, text=True, check=True
        )
        return Path(result.stdout.strip())
    except (subprocess.CalledProcessError, FileNotFoundError):
        return Path.cwd()


def discover_deliverables(execution_root: Path):
    """Discover all DEL-* folders under execution root."""
    deliverables = {}
    for pkg_dir in sorted(execution_root.iterdir()):
        if not pkg_dir.is_dir() or pkg_dir.name.startswith("_"):
            continue
        working_dir = pkg_dir / "1_Working"
        if not working_dir.is_dir():
            continue
        for del_dir in sorted(working_dir.iterdir()):
            if del_dir.is_dir() and del_dir.name.startswith("DEL-"):
                # Extract short-form ID: DEL-XX-YY
                parts = del_dir.name.split("_", 1)
                del_id = parts[0]
                deliverables[del_id] = del_dir
    return deliverables


def normalize_id(raw_id: str) -> str:
    """Normalize a deliverable ID by stripping descriptive suffix."""
    if not raw_id:
        return raw_id
    # DEL-XX-YY_Label -> DEL-XX-YY
    parts = raw_id.split("_", 1)
    return parts[0]


def parse_dependencies_csv(csv_path: Path):
    """Parse a Dependencies.csv and return rows as dicts."""
    rows = []
    try:
        with open(csv_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                rows.append(row)
    except Exception as e:
        return None, str(e)
    return rows, None


def run_analysis(execution_root: Path):
    """Run full closure analysis."""
    print(f"Execution root: {execution_root}")
    print(f"Scope: {SCOPE}")
    print()

    # Step 0: Discover deliverables
    all_deliverables = discover_deliverables(execution_root)
    print(f"Discovered {len(all_deliverables)} deliverables in workspace")

    # Filter to scope
    scope_deliverables = {
        did: path for did, path in all_deliverables.items()
        if did in SCOPE
    }

    if not scope_deliverables:
        print("ERROR: No deliverables found in scope. Aborting.")
        return {"status": "FAILED_INPUTS"}

    print(f"Deliverables in scope: {list(scope_deliverables.keys())}")
    print()

    # Step 1: Locate and parse Dependencies.csv
    coverage = []
    all_edges = []
    all_anchors = []

    for del_id, del_path in scope_deliverables.items():
        csv_path = del_path / "Dependencies.csv"
        exists = csv_path.exists()
        readable = exists and csv_path.is_file()

        if not readable:
            coverage.append({
                "deliverable_id": del_id,
                "csv_exists": exists,
                "csv_readable": False,
                "schema_valid": False,
                "status": "MISSING_DEPENDENCIES_CSV" if not exists else "UNREADABLE"
            })
            continue

        rows, error = parse_dependencies_csv(csv_path)
        if error:
            coverage.append({
                "deliverable_id": del_id,
                "csv_exists": True,
                "csv_readable": False,
                "schema_valid": False,
                "status": f"PARSE_ERROR: {error}"
            })
            continue

        # Step 2: Validate schema
        schema_valid = True
        if rows:
            schema_version = rows[0].get("RegisterSchemaVersion", "")
            if schema_version != "v3.1":
                schema_valid = False

        coverage.append({
            "deliverable_id": del_id,
            "csv_exists": True,
            "csv_readable": True,
            "schema_valid": schema_valid,
            "total_rows": len(rows),
            "status": "OK" if schema_valid else "SCHEMA_INVALID"
        })

        if not schema_valid:
            continue

        # Step 3: Extract edges and anchors
        for row in rows:
            status = row.get("Status", "").strip()
            if FILTER_ACTIVE_ONLY and status != "ACTIVE":
                continue

            dep_class = row.get("DependencyClass", "").strip()
            target_type = row.get("TargetType", "").strip()
            from_id = row.get("FromDeliverableID", "").strip()
            target_del_id = row.get("TargetDeliverableID", "").strip()

            if NORMALIZE_IDS:
                from_id = normalize_id(from_id)
                target_del_id = normalize_id(target_del_id) if target_del_id else ""

            if dep_class == "ANCHOR":
                all_anchors.append({
                    "dependency_id": row.get("DependencyID", ""),
                    "from_id": from_id,
                    "anchor_type": row.get("AnchorType", ""),
                    "target_type": target_type,
                    "target_name": row.get("TargetName", ""),
                })
                continue

            if (dep_class == EDGE_FILTER_DEP_CLASS and
                    target_type == EDGE_FILTER_TARGET_TYPE and
                    from_id and target_del_id):
                all_edges.append({
                    "dependency_id": row.get("DependencyID", ""),
                    "from_id": from_id,
                    "target_id": target_del_id,
                    "direction": row.get("Direction", ""),
                    "dependency_type": row.get("DependencyType", ""),
                })

    # Step 4: Run checks
    results = {}

    # 4.1 Schema compliance
    valid_count = sum(1 for c in coverage if c.get("schema_valid"))
    results["schema_compliance"] = {
        "status": "PASS" if valid_count == len(scope_deliverables) else "WARNING",
        "valid": valid_count,
        "total": len(scope_deliverables),
    }

    # 4.2 Orphan dependencies
    orphans = []
    for edge in all_edges:
        if edge["target_id"] not in all_deliverables:
            orphans.append(edge)
    results["orphan_dependencies"] = {
        "status": "PASS" if not orphans else "WARNING",
        "orphan_count": len(orphans),
        "orphans": orphans,
    }

    # 4.3 Circular dependencies (self-loops only for single scope)
    self_loops = [e for e in all_edges if e["from_id"] == e["target_id"]]
    results["circular_dependencies"] = {
        "status": "PASS" if not self_loops else "BLOCKER",
        "self_loop_count": len(self_loops),
    }

    # 4.4 Anchor coverage
    implements_node = [a for a in all_anchors if a["anchor_type"] == "IMPLEMENTS_NODE"]
    traces_req = [a for a in all_anchors if a["anchor_type"] == "TRACES_TO_REQUIREMENT"]
    results["anchor_coverage"] = {
        "status": "PASS" if implements_node else "WARNING",
        "implements_node_count": len(implements_node),
        "traces_to_requirement_count": len(traces_req),
    }

    # 4.5 Misplaced fields -- check non-DELIVERABLE rows for TargetDeliverableID
    # (re-parse for this check)
    misplaced = 0
    for del_id, del_path in scope_deliverables.items():
        csv_path = del_path / "Dependencies.csv"
        rows, _ = parse_dependencies_csv(csv_path)
        if rows:
            for row in rows:
                tt = row.get("TargetType", "").strip()
                tdid = row.get("TargetDeliverableID", "").strip()
                if tt != "DELIVERABLE" and tdid:
                    misplaced += 1
    results["misplaced_fields"] = {
        "status": "PASS" if misplaced == 0 else "WARNING",
        "violations": misplaced,
    }

    # 4.6 ID format consistency
    long_form_count = 0
    total_ids = 0
    for edge in all_edges:
        for fld in [edge["from_id"], edge["target_id"]]:
            total_ids += 1
            if "_" in fld:
                long_form_count += 1
    norm_rate = (long_form_count / total_ids * 100) if total_ids else 0
    results["id_format_consistency"] = {
        "status": "PASS",
        "normalization_rate_pct": norm_rate,
    }

    # 4.7 Isolated deliverables
    isolated = []
    for did in scope_deliverables:
        has_edge = any(e["from_id"] == did or e["target_id"] == did for e in all_edges)
        if not has_edge:
            isolated.append(did)
    results["isolated_deliverables"] = {
        "status": "PASS" if not isolated else "WARNING",
        "isolated": isolated,
    }

    # 4.8 Hub analysis
    degree = defaultdict(int)
    for edge in all_edges:
        degree[edge["from_id"]] += 1
        degree[edge["target_id"]] += 1
    hubs = {did: deg for did, deg in degree.items() if deg >= HUB_THRESHOLD}
    results["hub_analysis"] = {
        "status": "PASS" if not hubs else "WARNING",
        "hubs": hubs,
    }

    # 4.9 Bidirectional pairs
    edge_set = set()
    for edge in all_edges:
        edge_set.add((edge["from_id"], edge["target_id"]))
    bidir = []
    for a, b in edge_set:
        if (b, a) in edge_set and a < b:
            bidir.append((a, b))
    results["bidirectional_pairs"] = {
        "status": "PASS",
        "pairs": bidir,
    }

    # Overall status
    statuses = [v["status"] for v in results.values()]
    if "BLOCKER" in statuses:
        overall = "BLOCKER"
    elif "WARNING" in statuses:
        overall = "WARNINGS"
    else:
        overall = "PASS"

    # Print summary
    print("=" * 60)
    print(f"CLOSURE ANALYSIS COMPLETE -- Overall: {overall}")
    print("=" * 60)
    print()
    for check_name, check_result in results.items():
        print(f"  {check_name}: {check_result['status']}")
    print()
    print(f"Edges: {len(all_edges)}")
    print(f"Anchors: {len(all_anchors)}")
    print(f"Orphans: {results['orphan_dependencies']['orphan_count']}")
    print(f"Self-loops: {results['circular_dependencies']['self_loop_count']}")

    return {
        "overall_status": overall,
        "checks": results,
        "edge_count": len(all_edges),
        "anchor_count": len(all_anchors),
    }


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="DEL-07-03 Dependency Closure Analysis")
    parser.add_argument("--execution-root", type=str, default=None,
                        help="Path to execution/ root (default: auto-detect)")
    args = parser.parse_args()

    if args.execution_root:
        exec_root = Path(args.execution_root)
    else:
        repo_root = find_repo_root()
        exec_root = repo_root / "execution"

    if not exec_root.is_dir():
        print(f"ERROR: Execution root not found: {exec_root}")
        sys.exit(1)

    result = run_analysis(exec_root)
    print()
    print(json.dumps(result, indent=2, default=str))
