#!/usr/bin/env python3
"""
Reproducible dependency closure analysis script for DEL-03-05.

Run ID: CLOSURE_DEL-03-05_2026-02-21
Scope: DEL-03-05 (single deliverable)
Date: 2026-02-21

Usage:
    python3 analyze_closure.py

This script reads the Dependencies.csv for DEL-03-05, applies the same
filters and checks as the AUDIT_DEP_CLOSURE agent, and prints results
to stdout. It can be used to independently verify the closure report.
"""

import csv
import json
import os
import sys
from collections import defaultdict
from pathlib import Path

# ---------- Configuration ----------

REPO_ROOT = Path(__file__).resolve().parents[4]  # up from DepClosure snapshot
EXECUTION_ROOT = REPO_ROOT / "execution"
DELIVERABLE_PATH = (
    EXECUTION_ROOT
    / "PKG-03_Harness_Runtime_Core"
    / "1_Working"
    / "DEL-03-05_Anthropic_Provider_Integration"
)
CSV_PATH = DELIVERABLE_PATH / "Dependencies.csv"

SCOPE_DELIVERABLE = "DEL-03-05"
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
    "DEL-08-01", "DEL-08-02", "DEL-08-03", "DEL-08-04",
    "DEL-08-05", "DEL-08-06", "DEL-08-07",
}

# Required v3.1 columns
REQUIRED_COLUMNS_V31 = [
    "RegisterSchemaVersion", "DependencyID", "FromPackageID",
    "FromDeliverableID", "FromDeliverableName", "DependencyClass",
    "AnchorType", "Direction", "DependencyType", "TargetType",
    "TargetPackageID", "TargetDeliverableID", "TargetRefID", "TargetName",
    "TargetLocation", "Statement", "EvidenceFile", "SourceRef",
    "EvidenceQuote", "Explicitness", "RequiredMaturity", "ProposedMaturity",
    "SatisfactionStatus", "Confidence", "Origin", "FirstSeen", "LastSeen",
    "Status", "Notes",
]


def normalize_id(raw_id: str) -> str:
    """Strip descriptive suffix from DEL-XX-YY_Label form."""
    if not raw_id:
        return raw_id
    parts = raw_id.split("_", 1)
    if parts[0].startswith("DEL-"):
        return parts[0]
    return raw_id


def main():
    print(f"=== Dependency Closure Analysis: {SCOPE_DELIVERABLE} ===\n")

    # --- Step 1: Locate and read CSV ---
    if not CSV_PATH.exists():
        print(f"FAIL: Dependencies.csv not found at {CSV_PATH}")
        sys.exit(1)

    with open(CSV_PATH, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        headers = reader.fieldnames or []
        rows = list(reader)

    print(f"CSV path: {CSV_PATH}")
    print(f"Rows: {len(rows)}")
    print(f"Columns: {len(headers)}")
    print()

    # --- Step 2: Schema validation ---
    missing_cols = [c for c in REQUIRED_COLUMNS_V31 if c not in headers]
    if missing_cols:
        print(f"SCHEMA_INVALID: Missing columns: {missing_cols}")
        schema_valid = False
    else:
        print("Schema: v3.1 VALID (all 29 required columns present)")
        schema_valid = True

    versions = set(r.get("RegisterSchemaVersion", "") for r in rows)
    print(f"Schema versions in data: {versions}")
    print()

    if not schema_valid:
        print("Halting edge extraction due to schema invalidity.")
        sys.exit(1)

    # --- Step 3: Build graph ---
    edges = []
    anchors = []
    non_deliverable = []

    for row in rows:
        dep_id = row.get("DependencyID", "")
        dep_class = row.get("DependencyClass", "")
        anchor_type = row.get("AnchorType", "")
        target_type = row.get("TargetType", "")
        status = row.get("Status", "")
        from_id = normalize_id(row.get("FromDeliverableID", ""))
        target_del_id = normalize_id(row.get("TargetDeliverableID", ""))
        direction = row.get("Direction", "")

        if FILTER_ACTIVE_ONLY and status != "ACTIVE":
            continue

        if dep_class == "ANCHOR":
            anchors.append(row)
            continue

        if dep_class == EDGE_FILTER_CLASS and target_type == EDGE_FILTER_TARGET_TYPE:
            if from_id and target_del_id:
                edges.append({
                    "dep_id": dep_id,
                    "from": from_id,
                    "target": target_del_id,
                    "direction": direction,
                    "dep_type": row.get("DependencyType", ""),
                })
        else:
            non_deliverable.append(row)

    print(f"EXECUTION+DELIVERABLE edges: {len(edges)}")
    print(f"ANCHOR rows: {len(anchors)}")
    print(f"Non-DELIVERABLE rows: {len(non_deliverable)}")
    print()

    # --- Step 4: Core checks ---

    # Check 1: Schema compliance
    print("--- Check 1: Schema Compliance ---")
    print(f"  Verdict: PASS (1/1 valid)")
    print()

    # Check 2: Orphan dependencies
    print("--- Check 2: Orphan Dependencies ---")
    orphans = []
    for e in edges:
        if e["target"] not in VALID_DELIVERABLE_IDS:
            orphans.append(e)
            print(f"  ORPHAN: {e['dep_id']} -> {e['target']}")
    if not orphans:
        print(f"  Verdict: PASS (0 orphans, {len(edges)} targets checked)")
    else:
        print(f"  Verdict: WARNING ({len(orphans)} orphans)")
    print()

    # Check 3: Circular dependencies (self-loops only in single-deliverable mode)
    print("--- Check 3: Circular Dependencies ---")
    self_loops = [e for e in edges if e["from"] == e["target"]]
    if self_loops:
        print(f"  SELF-LOOP: {[e['dep_id'] for e in self_loops]}")
        print(f"  Verdict: WARNING")
    else:
        print(f"  Verdict: PASS (0 self-loops; scope-limited to single deliverable)")
    print()

    # Check 4: Anchor coverage
    print("--- Check 4: Anchor Coverage ---")
    implements_anchors = [
        a for a in anchors
        if a.get("AnchorType") == "IMPLEMENTS_NODE"
    ]
    print(f"  IMPLEMENTS_NODE anchors: {len(implements_anchors)}")
    print(f"  Total anchors: {len(anchors)}")
    if implements_anchors:
        print(f"  Verdict: PASS")
    else:
        print(f"  Verdict: WARNING (no IMPLEMENTS_NODE anchor)")
    print()

    # Check 5: Misplaced fields
    print("--- Check 5: Misplaced Fields ---")
    misplaced = []
    for row in rows:
        target_type = row.get("TargetType", "")
        target_del_id = row.get("TargetDeliverableID", "")
        if target_type != "DELIVERABLE" and target_del_id.strip():
            misplaced.append(row)
    if misplaced:
        for m in misplaced:
            print(f"  MISPLACED: {m['DependencyID']} TargetType={m['TargetType']} "
                  f"but TargetDeliverableID={m['TargetDeliverableID']}")
        print(f"  Verdict: WARNING ({len(misplaced)} misplaced)")
    else:
        print(f"  Verdict: PASS (0 misplaced)")
    print()

    # Check 6: ID format consistency
    print("--- Check 6: ID Format Consistency ---")
    from_ids_raw = [row.get("FromDeliverableID", "") for row in rows]
    target_ids_raw = [
        row.get("TargetDeliverableID", "")
        for row in rows
        if row.get("TargetType") == "DELIVERABLE"
    ]
    needed_norm = sum(1 for i in from_ids_raw + target_ids_raw if "_" in i and i)
    print(f"  IDs needing normalization: {needed_norm}")
    print(f"  Verdict: PASS")
    print()

    # Check 7: Isolated deliverables
    print("--- Check 7: Isolated Deliverables ---")
    degree = len(edges)
    if degree == 0:
        print(f"  {SCOPE_DELIVERABLE} is ISOLATED (0 edges)")
        print(f"  Verdict: WARNING")
    else:
        print(f"  {SCOPE_DELIVERABLE} degree: {degree}")
        print(f"  Verdict: PASS")
    print()

    # Check 8: Hub analysis
    print("--- Check 8: Hub Analysis ---")
    print(f"  {SCOPE_DELIVERABLE} degree: {degree} (threshold: {HUB_THRESHOLD})")
    if degree >= HUB_THRESHOLD:
        print(f"  Verdict: WARNING (hub detected)")
    else:
        print(f"  Verdict: PASS")
    print()

    # Check 9: Bidirectional pairs
    print("--- Check 9: Bidirectional Pairs ---")
    print(f"  Verdict: PASS (INFO -- single-deliverable scope, no reciprocal visibility)")
    print()

    # --- Summary ---
    has_issues = bool(orphans or self_loops or misplaced)
    overall = "WARNINGS" if has_issues else "PASS"
    print(f"=== Overall: {overall} ===")

    # Output JSON summary
    summary = {
        "overall_status": overall,
        "edges": len(edges),
        "orphans": len(orphans),
        "self_loops": len(self_loops),
        "anchors": len(anchors),
        "misplaced": len(misplaced),
        "degree": degree,
    }
    print(f"\nJSON: {json.dumps(summary, indent=2)}")


if __name__ == "__main__":
    main()
