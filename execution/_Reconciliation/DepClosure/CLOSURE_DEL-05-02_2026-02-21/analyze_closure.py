#!/usr/bin/env python3
"""
analyze_closure.py -- Reproducible dependency closure analysis for DEL-05-02.

Snapshot: CLOSURE_DEL-05-02_2026-02-21
Scope:    DEL-05-02 (single deliverable)
Run Date: 2026-02-21

This script re-derives all findings from the raw Dependencies.csv.
It can be executed standalone to verify the closure report is deterministic.

Usage:
    python3 analyze_closure.py [--csv PATH_TO_DEPENDENCIES_CSV] [--workspace-ids ID1,ID2,...]

Defaults:
    --csv: execution/PKG-05_Filesystem_Execution_Model/1_Working/DEL-05-02_Execution_Root_Scaffolding/Dependencies.csv
    --workspace-ids: All 32 DEL-XX-YY IDs from the workspace
"""

import csv
import json
import re
import sys
from pathlib import Path
from typing import Dict, List, Set, Tuple


# --- Configuration (matches the brief) ---
FILTER_ACTIVE_ONLY = True
NORMALIZE_IDS = True
EDGE_FILTER_DEP_CLASS = "EXECUTION"
EDGE_FILTER_TARGET_TYPE = "DELIVERABLE"
HUB_THRESHOLD = 20

DEFAULT_CSV = "execution/PKG-05_Filesystem_Execution_Model/1_Working/DEL-05-02_Execution_Root_Scaffolding/Dependencies.csv"

WORKSPACE_IDS = {
    "DEL-01-01", "DEL-01-02",
    "DEL-02-01", "DEL-02-02", "DEL-02-03", "DEL-02-04",
    "DEL-03-01", "DEL-03-02", "DEL-03-03", "DEL-03-04", "DEL-03-05", "DEL-03-06",
    "DEL-04-01", "DEL-04-02",
    "DEL-05-01", "DEL-05-02", "DEL-05-03", "DEL-05-04",
    "DEL-06-01", "DEL-06-02", "DEL-06-03", "DEL-06-04", "DEL-06-05",
    "DEL-07-01", "DEL-07-02",
    "DEL-08-01", "DEL-08-02", "DEL-08-03", "DEL-08-04", "DEL-08-05", "DEL-08-06", "DEL-08-07",
}

REQUIRED_COLUMNS_V3_1 = {
    "RegisterSchemaVersion", "DependencyID", "FromPackageID", "FromDeliverableID",
    "FromDeliverableName", "DependencyClass", "AnchorType", "Direction",
    "DependencyType", "TargetType", "TargetPackageID", "TargetDeliverableID",
    "TargetRefID", "TargetName", "TargetLocation", "Statement", "EvidenceFile",
    "SourceRef", "EvidenceQuote", "Explicitness", "RequiredMaturity",
    "ProposedMaturity", "SatisfactionStatus", "Confidence", "Origin",
    "FirstSeen", "LastSeen", "Status", "Notes",
}

ID_PATTERN = re.compile(r"^(DEL-\d{2}-\d{2})")


def normalize_id(raw_id: str) -> str:
    """Strip descriptive suffix from a deliverable ID."""
    if not NORMALIZE_IDS or not raw_id:
        return raw_id
    m = ID_PATTERN.match(raw_id.strip())
    return m.group(1) if m else raw_id.strip()


def load_csv(csv_path: str) -> Tuple[List[str], List[dict]]:
    """Load CSV and return (headers, rows)."""
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        headers = reader.fieldnames or []
        rows = list(reader)
    return headers, rows


def check_schema(headers: List[str]) -> Tuple[str, Set[str], Set[str]]:
    """Check v3.1 schema compliance. Returns (verdict, missing, extra)."""
    header_set = set(headers)
    missing = REQUIRED_COLUMNS_V3_1 - header_set
    extra = header_set - REQUIRED_COLUMNS_V3_1
    verdict = "PASS" if not missing else "BLOCKER"
    return verdict, missing, extra


def build_edges(rows: List[dict]) -> List[dict]:
    """Extract qualifying edges from rows."""
    edges = []
    for row in rows:
        if FILTER_ACTIVE_ONLY and row.get("Status", "").strip() != "ACTIVE":
            continue
        if row.get("DependencyClass", "").strip() != EDGE_FILTER_DEP_CLASS:
            continue
        if row.get("TargetType", "").strip() != EDGE_FILTER_TARGET_TYPE:
            continue
        from_id = normalize_id(row.get("FromDeliverableID", ""))
        target_id = normalize_id(row.get("TargetDeliverableID", ""))
        if from_id and target_id:
            edges.append({
                "from": from_id,
                "to": target_id,
                "direction": row.get("Direction", "").strip(),
                "type": row.get("DependencyType", "").strip(),
                "dep_id": row.get("DependencyID", "").strip(),
            })
    return edges


def check_orphans(edges: List[dict], valid_ids: Set[str]) -> List[dict]:
    """Find edges whose target is not in the valid workspace IDs."""
    orphans = []
    for e in edges:
        if e["to"] not in valid_ids:
            orphans.append(e)
    return orphans


def check_self_loops(edges: List[dict]) -> List[dict]:
    """Find edges where from == to."""
    return [e for e in edges if e["from"] == e["to"]]


def check_anchors(rows: List[dict]) -> Tuple[int, int]:
    """Count anchor rows and IMPLEMENTS_NODE anchors."""
    anchors = [r for r in rows if r.get("DependencyClass", "").strip() == "ANCHOR"]
    impl_nodes = [r for r in anchors if r.get("AnchorType", "").strip() == "IMPLEMENTS_NODE"]
    return len(anchors), len(impl_nodes)


def check_misplaced(rows: List[dict]) -> List[dict]:
    """Find rows where TargetType != DELIVERABLE but TargetDeliverableID is non-empty."""
    misplaced = []
    for row in rows:
        tt = row.get("TargetType", "").strip()
        tdid = row.get("TargetDeliverableID", "").strip()
        if tt != "DELIVERABLE" and tdid:
            misplaced.append(row)
    return misplaced


def check_long_form_ids(rows: List[dict]) -> int:
    """Count rows with long-form IDs (containing suffix after DEL-XX-YY)."""
    count = 0
    for row in rows:
        for field in ("FromDeliverableID", "TargetDeliverableID"):
            raw = row.get(field, "").strip()
            if raw and raw != normalize_id(raw):
                count += 1
    return count


def main():
    import argparse
    parser = argparse.ArgumentParser(description="DEL-05-02 dependency closure analysis")
    parser.add_argument("--csv", default=DEFAULT_CSV, help="Path to Dependencies.csv")
    parser.add_argument("--workspace-ids", default=None, help="Comma-separated valid workspace IDs")
    args = parser.parse_args()

    valid_ids = WORKSPACE_IDS
    if args.workspace_ids:
        valid_ids = set(args.workspace_ids.split(","))

    # Load and validate
    headers, rows = load_csv(args.csv)
    schema_verdict, missing_cols, extra_cols = check_schema(headers)

    # Build edges
    edges = build_edges(rows)

    # Run checks
    orphans = check_orphans(edges, valid_ids)
    self_loops = check_self_loops(edges)
    total_anchors, impl_anchors = check_anchors(rows)
    misplaced = check_misplaced(rows)
    long_form_count = check_long_form_ids(rows)

    # Compute degree for hub analysis
    degree: Dict[str, int] = {}
    for e in edges:
        degree[e["from"]] = degree.get(e["from"], 0) + 1

    hubs = {k: v for k, v in degree.items() if v >= HUB_THRESHOLD}

    # Isolation check
    isolated = [nid for nid in ["DEL-05-02"] if degree.get(nid, 0) == 0]

    # Summary
    results = {
        "schema_compliance": schema_verdict,
        "schema_missing_columns": sorted(missing_cols),
        "total_rows": len(rows),
        "qualifying_edges": len(edges),
        "orphan_count": len(orphans),
        "orphans": orphans,
        "self_loop_count": len(self_loops),
        "anchor_total": total_anchors,
        "implements_node_anchors": impl_anchors,
        "misplaced_field_count": len(misplaced),
        "long_form_id_count": long_form_count,
        "isolated_deliverables": isolated,
        "hub_count": len(hubs),
        "hubs": hubs,
        "del_05_02_degree": degree.get("DEL-05-02", 0),
    }

    # Determine overall status
    blocker = (schema_verdict != "PASS" or len(orphans) > 0 or len(self_loops) > 0)
    warning = (impl_anchors == 0 or len(misplaced) > 0)
    if blocker:
        results["closure_status"] = "BLOCKER"
    elif warning:
        results["closure_status"] = "WARNINGS"
    else:
        results["closure_status"] = "PASS"

    print(json.dumps(results, indent=2))
    return 0 if results["closure_status"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
