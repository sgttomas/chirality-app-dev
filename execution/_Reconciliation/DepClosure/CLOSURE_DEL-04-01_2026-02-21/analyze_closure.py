#!/usr/bin/env python3
"""
Reproducible dependency closure analysis script for DEL-04-01.

Run: CLOSURE_DEL-04-01_2026-02-21
Scope: DEL-04-01
Date: 2026-02-21

This script reproduces the analysis performed by the AUDIT_DEP_CLOSURE agent.
It reads the Dependencies.csv from the deliverable folder, applies the same
filters and checks, and prints results to stdout.

Usage:
    python3 analyze_closure.py [--execution-root PATH]

Default execution root: ../../.. (relative to this script's location,
resolving to the execution/ directory).
"""

import csv
import json
import os
import sys
import argparse
from collections import defaultdict

# -- Configuration (matches the run parameters) --
SCOPE = ["DEL-04-01"]
FILTER_ACTIVE_ONLY = True
NORMALIZE_IDS = True
EDGE_FILTER_DEPENDENCY_CLASS = "EXECUTION"
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

DELIVERABLE_CSV_PATHS = {
    "DEL-04-01": "PKG-04_Attachments_Multimodal/1_Working/DEL-04-01_Attachment_Resolver_PromptMode/Dependencies.csv",
}

V31_REQUIRED_COLUMNS = [
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
    """Strip descriptive suffix from long-form IDs: DEL-XX-YY_Label -> DEL-XX-YY."""
    if not raw_id:
        return raw_id
    parts = raw_id.split("_", 1)
    prefix = parts[0]
    if prefix.startswith("DEL-") and len(prefix.split("-")) == 3:
        return prefix
    return raw_id


def load_csv(filepath: str) -> tuple:
    """Load a Dependencies.csv and return (rows, schema_valid, error_msg)."""
    if not os.path.isfile(filepath):
        return [], False, f"File not found: {filepath}"
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            if reader.fieldnames is None:
                return [], False, "Empty CSV or no header row"
            missing = set(V31_REQUIRED_COLUMNS) - set(reader.fieldnames)
            if missing:
                return [], False, f"Missing columns: {sorted(missing)}"
            rows = list(reader)
            return rows, True, None
    except Exception as e:
        return [], False, str(e)


def run_checks(rows: list, deliverable_id: str) -> dict:
    """Run all 9 core checks and return results dict."""
    results = {}

    # Filter rows
    active_rows = [r for r in rows if not FILTER_ACTIVE_ONLY or r.get("Status") == "ACTIVE"]

    # Edge filter: EXECUTION + DELIVERABLE
    edges = [
        r for r in active_rows
        if r.get("DependencyClass") == EDGE_FILTER_DEPENDENCY_CLASS
        and r.get("TargetType") == EDGE_FILTER_TARGET_TYPE
    ]

    # Normalize IDs on edges
    for e in edges:
        if NORMALIZE_IDS:
            e["_from_normalized"] = normalize_id(e.get("FromDeliverableID", ""))
            e["_target_normalized"] = normalize_id(e.get("TargetDeliverableID", ""))
        else:
            e["_from_normalized"] = e.get("FromDeliverableID", "")
            e["_target_normalized"] = e.get("TargetDeliverableID", "")

    # Check 1: Schema compliance (already validated during load)
    results["schema_compliance"] = {"verdict": "PASS", "issues": 0}

    # Check 2: Orphan dependencies
    orphans = [
        e for e in edges
        if e["_target_normalized"] and e["_target_normalized"] not in VALID_DELIVERABLE_IDS
    ]
    results["orphan_dependencies"] = {
        "verdict": "PASS" if not orphans else "WARNING",
        "issues": len(orphans),
        "orphans": [
            {"dep_id": o.get("DependencyID"), "target": o["_target_normalized"]}
            for o in orphans
        ],
    }

    # Check 3: Circular dependencies (limited in single-deliverable scope)
    self_loops = [e for e in edges if e["_from_normalized"] == e["_target_normalized"]]
    results["circular_dependencies"] = {
        "verdict": "PASS",
        "completeness": "INCOMPLETE",
        "self_loops": len(self_loops),
        "detail": "Single-deliverable scope; full Tarjan SCC requires SCOPE=ALL",
    }

    # Check 4: Anchor coverage
    anchors = [r for r in active_rows if r.get("DependencyClass") == "ANCHOR"]
    implements_node = [r for r in anchors if r.get("AnchorType") == "IMPLEMENTS_NODE"]
    results["anchor_coverage"] = {
        "verdict": "PASS" if implements_node else "WARNING",
        "implements_node_present": bool(implements_node),
        "anchor_count": len(anchors),
    }

    # Check 5: Misplaced fields
    misplaced = [
        r for r in active_rows
        if r.get("TargetType") != "DELIVERABLE"
        and r.get("TargetDeliverableID", "").strip() != ""
    ]
    results["misplaced_fields"] = {
        "verdict": "PASS" if not misplaced else "WARNING",
        "issues": len(misplaced),
    }

    # Check 6: ID format consistency
    all_from_ids = [r.get("FromDeliverableID", "") for r in active_rows if r.get("FromDeliverableID")]
    all_target_ids = [e.get("TargetDeliverableID", "") for e in edges if e.get("TargetDeliverableID")]
    long_form = [i for i in all_from_ids + all_target_ids if "_" in i and i.split("_", 1)[0].startswith("DEL-")]
    total_ids = len(all_from_ids) + len(all_target_ids)
    results["id_format_consistency"] = {
        "verdict": "PASS" if not long_form else "WARNING",
        "long_form_count": len(long_form),
        "total_ids": total_ids,
        "normalization_rate_pct": (len(long_form) / total_ids * 100) if total_ids > 0 else 0,
    }

    # Check 7: Isolated deliverables
    degree = len(edges)
    results["isolated_deliverables"] = {
        "verdict": "PASS" if degree > 0 else "WARNING",
        "degree": degree,
    }

    # Check 8: Hub analysis
    results["hub_analysis"] = {
        "verdict": "PASS" if degree < HUB_THRESHOLD else "WARNING",
        "degree": degree,
        "threshold": HUB_THRESHOLD,
        "is_hub": degree >= HUB_THRESHOLD,
    }

    # Check 9: Bidirectional pairs (INCOMPLETE in single-deliverable scope)
    results["bidirectional_pairs"] = {
        "verdict": "PASS",
        "completeness": "INCOMPLETE",
        "detail": "Requires reciprocal CSVs for detection",
    }

    return results


def main():
    parser = argparse.ArgumentParser(description="DEL-04-01 dependency closure analysis")
    parser.add_argument(
        "--execution-root",
        default=os.path.join(os.path.dirname(__file__), "..", "..", ".."),
        help="Path to execution/ root directory",
    )
    args = parser.parse_args()
    exec_root = os.path.abspath(args.execution_root)

    print(f"Execution root: {exec_root}")
    print(f"Scope: {SCOPE}")
    print(f"Filters: ACTIVE_ONLY={FILTER_ACTIVE_ONLY}, "
          f"DependencyClass={EDGE_FILTER_DEPENDENCY_CLASS}, "
          f"TargetType={EDGE_FILTER_TARGET_TYPE}")
    print("=" * 70)

    for del_id in SCOPE:
        rel_path = DELIVERABLE_CSV_PATHS.get(del_id)
        if not rel_path:
            print(f"[ERROR] No CSV path configured for {del_id}")
            continue

        filepath = os.path.join(exec_root, rel_path)
        print(f"\nLoading: {filepath}")

        rows, schema_valid, error = load_csv(filepath)
        if not schema_valid:
            print(f"[SCHEMA_INVALID] {del_id}: {error}")
            continue

        print(f"  Rows: {len(rows)}, Schema: v3.1 VALID")

        results = run_checks(rows, del_id)

        print(f"\n--- Check Results for {del_id} ---")
        for check_name, result in results.items():
            verdict = result.get("verdict", "UNKNOWN")
            completeness = result.get("completeness", "")
            suffix = f" ({completeness})" if completeness else ""
            print(f"  {check_name}: {verdict}{suffix}")
            for k, v in result.items():
                if k not in ("verdict", "completeness"):
                    print(f"    {k}: {v}")

    print("\n" + "=" * 70)
    print("Analysis complete.")


if __name__ == "__main__":
    main()
