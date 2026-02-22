#!/usr/bin/env python3
"""
analyze_closure.py -- Reproducible dependency closure analysis for DEL-03-02

Run: CLOSURE_DEL-03-02_2026-02-21
Scope: DEL-03-02 (single deliverable)
Parameters:
  - FILTER_ACTIVE_ONLY: True
  - NORMALIZE_IDS: True
  - EDGE_FILTER: DependencyClass=EXECUTION, TargetType=DELIVERABLE
  - HUB_THRESHOLD: 20
  - MAX_CYCLES: 10000

Usage:
  python3 analyze_closure.py <path_to_dependencies_csv>

If no argument is provided, defaults to the known relative path.
"""

import csv
import json
import sys
import os
import re
from collections import defaultdict

# --- Configuration ---
FILTER_ACTIVE_ONLY = True
NORMALIZE_IDS = True
EDGE_FILTER_DEP_CLASS = "EXECUTION"
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

# All 32 valid workspace deliverable IDs
VALID_WORKSPACE_IDS = {
    "DEL-01-01", "DEL-01-02",
    "DEL-02-01", "DEL-02-02", "DEL-02-03", "DEL-02-04",
    "DEL-03-01", "DEL-03-02", "DEL-03-03", "DEL-03-04", "DEL-03-05", "DEL-03-06",
    "DEL-04-01", "DEL-04-02",
    "DEL-05-01", "DEL-05-02", "DEL-05-03", "DEL-05-04",
    "DEL-06-01", "DEL-06-02", "DEL-06-03", "DEL-06-04", "DEL-06-05",
    "DEL-07-01", "DEL-07-02",
    "DEL-08-01", "DEL-08-02", "DEL-08-03", "DEL-08-04", "DEL-08-05", "DEL-08-06", "DEL-08-07",
}


def normalize_id(raw_id: str) -> str:
    """Strip descriptive suffix from long-form IDs: DEL-XX-YY_Label -> DEL-XX-YY"""
    if not raw_id:
        return raw_id
    match = re.match(r"^(DEL-\d{2}-\d{2})", raw_id.strip())
    if match:
        return match.group(1)
    return raw_id.strip()


def load_csv(filepath: str) -> list[dict]:
    """Load Dependencies.csv and return list of row dicts."""
    rows = []
    with open(filepath, "r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)
    return rows


def validate_schema(rows: list[dict]) -> dict:
    """Check schema version and required columns."""
    if not rows:
        return {"valid": False, "reason": "Empty CSV", "version": None}
    version = rows[0].get("RegisterSchemaVersion", "").strip()
    columns = list(rows[0].keys())
    missing = [c for c in REQUIRED_COLUMNS_V31 if c not in columns]
    extra = [c for c in columns if c not in REQUIRED_COLUMNS_V31]
    return {
        "valid": len(missing) == 0 and version == "v3.1",
        "version": version,
        "columns_found": len(columns),
        "columns_expected": len(REQUIRED_COLUMNS_V31),
        "missing_columns": missing,
        "extra_columns": extra,
    }


def extract_edges(rows: list[dict]) -> list[dict]:
    """Filter rows to EXECUTION edges targeting DELIVERABLEs."""
    edges = []
    for row in rows:
        if FILTER_ACTIVE_ONLY and row.get("Status", "").strip() != "ACTIVE":
            continue
        if row.get("DependencyClass", "").strip() != EDGE_FILTER_DEP_CLASS:
            continue
        if row.get("TargetType", "").strip() != EDGE_FILTER_TARGET_TYPE:
            continue
        from_id = row.get("FromDeliverableID", "").strip()
        target_id = row.get("TargetDeliverableID", "").strip()
        if NORMALIZE_IDS:
            from_id = normalize_id(from_id)
            target_id = normalize_id(target_id)
        if from_id and target_id:
            edges.append({
                "dependency_id": row.get("DependencyID", "").strip(),
                "from": from_id,
                "to": target_id,
                "direction": row.get("Direction", "").strip(),
                "dependency_type": row.get("DependencyType", "").strip(),
                "confidence": row.get("Confidence", "").strip(),
            })
    return edges


def check_orphans(edges: list[dict]) -> list[dict]:
    """Find edges whose target is not in the valid workspace ID set."""
    orphans = []
    for e in edges:
        if e["to"] not in VALID_WORKSPACE_IDS:
            orphans.append(e)
    return orphans


def check_anchors(rows: list[dict]) -> dict:
    """Check for IMPLEMENTS_NODE anchor presence."""
    anchors = [r for r in rows if r.get("DependencyClass", "").strip() == "ANCHOR"]
    implements = [a for a in anchors if a.get("AnchorType", "").strip() == "IMPLEMENTS_NODE"]
    traces = [a for a in anchors if a.get("AnchorType", "").strip() == "TRACES_TO_REQUIREMENT"]
    return {
        "total_anchors": len(anchors),
        "implements_node_count": len(implements),
        "traces_to_requirement_count": len(traces),
        "implements_node_present": len(implements) > 0,
    }


def check_misplaced_fields(rows: list[dict]) -> list[dict]:
    """Find rows where TargetType != DELIVERABLE but TargetDeliverableID is non-empty."""
    violations = []
    for row in rows:
        target_type = row.get("TargetType", "").strip()
        target_del_id = row.get("TargetDeliverableID", "").strip()
        if target_type != "DELIVERABLE" and target_del_id:
            violations.append({
                "dependency_id": row.get("DependencyID", "").strip(),
                "target_type": target_type,
                "target_deliverable_id": target_del_id,
            })
    return violations


def check_id_format(rows: list[dict]) -> dict:
    """Check how many IDs needed normalization."""
    total_refs = 0
    normalized_count = 0
    for row in rows:
        for col in ["FromDeliverableID", "TargetDeliverableID"]:
            raw = row.get(col, "").strip()
            if raw:
                total_refs += 1
                if normalize_id(raw) != raw:
                    normalized_count += 1
    return {
        "total_references": total_refs,
        "short_form": total_refs - normalized_count,
        "needed_normalization": normalized_count,
        "rate": normalized_count / total_refs if total_refs > 0 else 0.0,
    }


def check_isolated(edges: list[dict], scope_ids: set) -> list[str]:
    """Find scope nodes with zero edges."""
    connected = set()
    for e in edges:
        connected.add(e["from"])
    return [sid for sid in scope_ids if sid not in connected]


def check_hubs(edges: list[dict], threshold: int) -> list[dict]:
    """Find nodes with degree >= threshold."""
    degree = defaultdict(int)
    for e in edges:
        degree[e["from"]] += 1
    return [{"id": nid, "degree": d} for nid, d in degree.items() if d >= threshold]


def main():
    default_path = os.path.join(
        os.path.dirname(__file__), "..", "..", "..",
        "PKG-03_Harness_Runtime_Core", "1_Working",
        "DEL-03-02_Turn_Execution_SSE_Streaming", "Dependencies.csv"
    )
    csv_path = sys.argv[1] if len(sys.argv) > 1 else default_path

    if not os.path.isfile(csv_path):
        print(f"ERROR: File not found: {csv_path}", file=sys.stderr)
        sys.exit(1)

    rows = load_csv(csv_path)
    print(f"Loaded {len(rows)} rows from {csv_path}")

    # Schema validation
    schema = validate_schema(rows)
    print(f"\nSchema: {'VALID' if schema['valid'] else 'INVALID'} "
          f"(version={schema['version']}, cols={schema['columns_found']}/{schema['columns_expected']})")
    if schema["missing_columns"]:
        print(f"  Missing: {schema['missing_columns']}")

    # Edge extraction
    edges = extract_edges(rows)
    print(f"\nEdges extracted: {len(edges)}")

    # Orphan check
    orphans = check_orphans(edges)
    print(f"Orphans: {len(orphans)}")
    for o in orphans:
        print(f"  {o['dependency_id']}: {o['from']} -> {o['to']}")

    # Anchor check
    anchors = check_anchors(rows)
    print(f"\nAnchors: {anchors['total_anchors']} "
          f"(IMPLEMENTS_NODE={anchors['implements_node_count']}, "
          f"TRACES_TO_REQUIREMENT={anchors['traces_to_requirement_count']})")

    # Misplaced fields
    misplaced = check_misplaced_fields(rows)
    print(f"Misplaced fields: {len(misplaced)}")

    # ID format
    id_fmt = check_id_format(rows)
    print(f"ID format: {id_fmt['short_form']}/{id_fmt['total_references']} short-form "
          f"({id_fmt['needed_normalization']} needed normalization)")

    # Isolated
    scope_ids = {"DEL-03-02"}
    isolated = check_isolated(edges, scope_ids)
    print(f"Isolated deliverables: {len(isolated)}")

    # Hubs
    hubs = check_hubs(edges, HUB_THRESHOLD)
    print(f"Hubs (degree >= {HUB_THRESHOLD}): {len(hubs)}")

    # Summary
    overall = "PASS" if (
        schema["valid"]
        and len(orphans) == 0
        and anchors["implements_node_present"]
        and len(misplaced) == 0
        and len(isolated) == 0
    ) else "WARNING"

    print(f"\nOverall: {overall}")

    summary = {
        "overall": overall,
        "schema_valid": schema["valid"],
        "orphans": len(orphans),
        "anchors": anchors,
        "misplaced": len(misplaced),
        "id_format": id_fmt,
        "isolated": len(isolated),
        "hubs": len(hubs),
        "edges": len(edges),
    }
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
