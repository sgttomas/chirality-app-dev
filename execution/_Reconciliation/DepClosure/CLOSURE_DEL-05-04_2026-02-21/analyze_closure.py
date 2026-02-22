#!/usr/bin/env python3
"""
analyze_closure.py -- Reproducible dependency closure analysis for DEL-05-04.

Run ID: CLOSURE_DEL-05-04_2026-02-21
Date:   2026-02-21
Scope:  DEL-05-04

This script reproduces the closure analysis performed by the AUDIT_DEP_CLOSURE
agent. It reads the Dependencies.csv from the deliverable folder, applies the
same filters and checks, and prints results to stdout.

Usage:
    python3 analyze_closure.py

Prerequisites:
    - Python 3.8+
    - csv module (stdlib)
    - No external dependencies
"""

import csv
import json
import os
import re
import sys
from collections import defaultdict
from pathlib import Path

# --- Configuration ---
EXECUTION_ROOT = Path(__file__).resolve().parent.parent.parent.parent
DELIVERABLE_PATH = EXECUTION_ROOT / "PKG-05_Filesystem_Execution_Model" / "1_Working" / "DEL-05-04_Dependency_Tracking_Contract"
DEPENDENCIES_CSV = DELIVERABLE_PATH / "Dependencies.csv"
SCOPE_DELIVERABLE = "DEL-05-04"

# Filter parameters
FILTER_ACTIVE_ONLY = True
EDGE_FILTER_CLASS = "EXECUTION"
EDGE_FILTER_TARGET_TYPE = "DELIVERABLE"
HUB_THRESHOLD = 20
NORMALIZE_IDS = True

# Valid workspace deliverable IDs (32 total)
VALID_DELIVERABLE_IDS = {
    "DEL-01-01", "DEL-01-02",
    "DEL-02-01", "DEL-02-02", "DEL-02-03", "DEL-02-04",
    "DEL-03-01", "DEL-03-02", "DEL-03-03", "DEL-03-04", "DEL-03-05", "DEL-03-06",
    "DEL-04-01", "DEL-04-02",
    "DEL-05-01", "DEL-05-02", "DEL-05-03", "DEL-05-04",
    "DEL-06-01", "DEL-06-02", "DEL-06-03", "DEL-06-04", "DEL-06-05",
    "DEL-07-01", "DEL-07-02",
    "DEL-08-01", "DEL-08-02", "DEL-08-03", "DEL-08-04", "DEL-08-05", "DEL-08-06", "DEL-08-07",
}

DEL_ID_PATTERN = re.compile(r"^DEL-\d{2}-\d{2}$")


def normalize_id(raw_id: str) -> str:
    """Strip descriptive suffix from long-form ID if present."""
    if not raw_id:
        return raw_id
    match = re.match(r"^(DEL-\d{2}-\d{2})(?:_.*)?$", raw_id.strip())
    return match.group(1) if match else raw_id.strip()


def read_dependencies_csv(path: Path) -> list[dict]:
    """Read and return all rows from Dependencies.csv."""
    if not path.exists():
        print(f"ERROR: Dependencies.csv not found at {path}", file=sys.stderr)
        sys.exit(1)
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader)


def check_schema(rows: list[dict]) -> dict:
    """Check 1: Schema compliance."""
    required_cols = {
        "RegisterSchemaVersion", "DependencyID", "FromPackageID",
        "FromDeliverableID", "FromDeliverableName", "DependencyClass",
        "AnchorType", "Direction", "DependencyType", "TargetType",
        "TargetPackageID", "TargetDeliverableID", "TargetRefID",
        "TargetName", "TargetLocation", "Statement", "EvidenceFile",
        "SourceRef", "EvidenceQuote", "Confidence", "Origin",
        "Explicitness", "Status", "SatisfactionStatus", "FirstSeen",
        "LastSeen", "FromDeliverableType", "TargetDeliverableType",
        "Notes", "ConflictFlag",
    }
    if not rows:
        return {"verdict": "BLOCKER", "detail": "No rows found"}
    actual_cols = set(rows[0].keys())
    missing = required_cols - actual_cols
    if missing:
        return {"verdict": "BLOCKER", "detail": f"Missing columns: {missing}"}
    versions = {r.get("RegisterSchemaVersion") for r in rows}
    if versions != {"v3.1"}:
        return {"verdict": "WARNING", "detail": f"Non-v3.1 versions found: {versions}"}
    return {"verdict": "PASS", "detail": f"All {len(rows)} rows schema-valid (v3.1)"}


def filter_edges(rows: list[dict]) -> list[dict]:
    """Apply edge filters and return qualifying rows."""
    edges = []
    for r in rows:
        if FILTER_ACTIVE_ONLY and r.get("Status", "").strip() != "ACTIVE":
            continue
        if r.get("DependencyClass", "").strip() != EDGE_FILTER_CLASS:
            continue
        if r.get("TargetType", "").strip() != EDGE_FILTER_TARGET_TYPE:
            continue
        from_id = normalize_id(r.get("FromDeliverableID", "")) if NORMALIZE_IDS else r.get("FromDeliverableID", "").strip()
        to_id = normalize_id(r.get("TargetDeliverableID", "")) if NORMALIZE_IDS else r.get("TargetDeliverableID", "").strip()
        if from_id and to_id:
            edges.append({**r, "_from": from_id, "_to": to_id})
    return edges


def check_orphans(edges: list[dict]) -> dict:
    """Check 2: Orphan dependencies."""
    orphans = []
    for e in edges:
        if e["_to"] not in VALID_DELIVERABLE_IDS:
            orphans.append((e["_from"], e["_to"], e.get("DependencyID", "")))
    if orphans:
        return {"verdict": "WARNING", "orphans": orphans, "detail": f"{len(orphans)} orphan(s) found"}
    return {"verdict": "PASS", "orphans": [], "detail": "All targets resolve to known deliverables"}


def check_cycles(edges: list[dict]) -> dict:
    """Check 3: Circular dependencies (single-node scope)."""
    self_loops = [e for e in edges if e["_from"] == e["_to"]]
    if self_loops:
        return {"verdict": "BLOCKER", "detail": f"{len(self_loops)} self-loop(s) found"}
    return {"verdict": "PASS", "detail": "No self-loops; single-node scope limits cycle detection"}


def check_anchors(rows: list[dict]) -> dict:
    """Check 4: Anchor coverage."""
    anchors = [r for r in rows if r.get("DependencyClass", "").strip() == "ANCHOR"]
    implements = [a for a in anchors if a.get("AnchorType", "").strip() == "IMPLEMENTS_NODE"]
    if not implements:
        return {"verdict": "WARNING", "detail": "No IMPLEMENTS_NODE anchor found"}
    return {"verdict": "PASS", "detail": f"{len(implements)} IMPLEMENTS_NODE anchor(s), {len(anchors)} total anchors"}


def check_misplaced(rows: list[dict]) -> dict:
    """Check 5: Misplaced fields."""
    violations = []
    for r in rows:
        tt = r.get("TargetType", "").strip()
        td = r.get("TargetDeliverableID", "").strip()
        if tt != "DELIVERABLE" and td:
            violations.append(r.get("DependencyID", ""))
    if violations:
        return {"verdict": "WARNING", "detail": f"{len(violations)} misplaced TargetDeliverableID(s): {violations}"}
    return {"verdict": "PASS", "detail": "No misplaced fields"}


def check_id_format(rows: list[dict]) -> dict:
    """Check 6: ID format consistency."""
    long_form = []
    for r in rows:
        for field in ("FromDeliverableID", "TargetDeliverableID"):
            val = r.get(field, "").strip()
            if val and not DEL_ID_PATTERN.match(val):
                long_form.append((r.get("DependencyID", ""), field, val))
    if long_form:
        return {"verdict": "WARNING", "detail": f"{len(long_form)} long-form ID(s) found", "items": long_form}
    return {"verdict": "PASS", "detail": "All IDs in short-form"}


def check_isolated(edges: list[dict]) -> dict:
    """Check 7: Isolated deliverables."""
    if not edges:
        return {"verdict": "WARNING", "detail": f"{SCOPE_DELIVERABLE} has zero EXECUTION edges (isolated)"}
    return {"verdict": "PASS", "detail": f"{SCOPE_DELIVERABLE} has {len(edges)} EXECUTION edge(s)"}


def check_hubs(edges: list[dict]) -> dict:
    """Check 8: Hub analysis."""
    degree = len(edges)
    exceeds = degree >= HUB_THRESHOLD
    if exceeds:
        return {"verdict": "WARNING", "detail": f"Degree {degree} >= threshold {HUB_THRESHOLD}"}
    return {"verdict": "PASS", "detail": f"Degree {degree} < threshold {HUB_THRESHOLD}"}


def check_bidirectional(edges: list[dict]) -> dict:
    """Check 9: Bidirectional pairs (limited in single-deliverable scope)."""
    pairs = set()
    for e in edges:
        pair = (e["_from"], e["_to"])
        reverse = (e["_to"], e["_from"])
        if reverse in pairs:
            return {"verdict": "INFO", "detail": "Bidirectional pair detected within same CSV"}
        pairs.add(pair)
    return {"verdict": "PASS", "detail": "No bidirectional pairs detected (single-deliverable scope)"}


def main():
    print(f"=== Dependency Closure Analysis: {SCOPE_DELIVERABLE} ===")
    print(f"Source: {DEPENDENCIES_CSV}")
    print()

    rows = read_dependencies_csv(DEPENDENCIES_CSV)
    print(f"Total rows: {len(rows)}")

    edges = filter_edges(rows)
    print(f"Qualifying edges: {len(edges)}")
    print()

    checks = {
        "1_schema_compliance": check_schema(rows),
        "2_orphan_dependencies": check_orphans(edges),
        "3_circular_dependencies": check_cycles(edges),
        "4_anchor_coverage": check_anchors(rows),
        "5_misplaced_fields": check_misplaced(rows),
        "6_id_format_consistency": check_id_format(rows),
        "7_isolated_deliverables": check_isolated(edges),
        "8_hub_analysis": check_hubs(edges),
        "9_bidirectional_pairs": check_bidirectional(edges),
    }

    overall = "PASS"
    for name, result in checks.items():
        verdict = result["verdict"]
        print(f"  {name}: {verdict} -- {result['detail']}")
        if verdict == "BLOCKER":
            overall = "BLOCKER"
        elif verdict == "WARNING" and overall != "BLOCKER":
            overall = "WARNING"

    print()
    print(f"Overall: {overall}")
    return 0 if overall == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
