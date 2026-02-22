#!/usr/bin/env python3
"""
Reproducible dependency closure analysis script.
Run: CLOSURE_DEL-02-02_2026-02-21
Scope: DEL-02-02
Date: 2026-02-21

This script reproduces the analysis performed by the AUDIT_DEP_CLOSURE agent.
It reads the Dependencies.csv for DEL-02-02, builds the graph, runs all 9 core
checks, and prints results to stdout.

Usage:
    python3 analyze_closure.py [--execution-root PATH]

Default execution root: ../../.. (relative to this script's location, i.e.,
execution/ from the snapshot folder).
"""

import csv
import json
import os
import re
import sys
from collections import defaultdict
from pathlib import Path

# --- Configuration ---
SCOPE_DELIVERABLE = "DEL-02-02"
DELIVERABLE_PATH = "PKG-02_Desktop_UI_Workflow/1_Working/DEL-02-02_Portal_Pipeline_Navigation"
FILTER_ACTIVE_ONLY = True
NORMALIZE_IDS = True
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
    "DEL-08-01", "DEL-08-02", "DEL-08-03", "DEL-08-04", "DEL-08-05", "DEL-08-06", "DEL-08-07",
}

REQUIRED_COLUMNS_V31 = [
    "RegisterSchemaVersion", "DependencyID", "FromPackageID", "FromDeliverableID",
    "FromDeliverableName", "DependencyClass", "AnchorType", "Direction",
    "DependencyType", "TargetType", "TargetPackageID", "TargetDeliverableID",
    "TargetRefID", "TargetName", "TargetLocation", "Statement", "EvidenceFile",
    "SourceRef", "EvidenceQuote", "Explicitness", "RequiredMaturity",
    "ProposedMaturity", "SatisfactionStatus", "Confidence", "Origin",
    "FirstSeen", "LastSeen", "Status", "Notes",
]

ID_PATTERN = re.compile(r"^(DEL-\d{2}-\d{2})(?:_.+)?$")


def normalize_id(raw_id: str) -> str:
    """Strip descriptive suffix from DEL-XX-YY_Label format."""
    if not raw_id:
        return raw_id
    m = ID_PATTERN.match(raw_id.strip())
    return m.group(1) if m else raw_id.strip()


def parse_csv(filepath: str) -> list[dict]:
    """Read Dependencies.csv and return list of row dicts."""
    with open(filepath, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader)


def check_schema(rows: list[dict], filepath: str) -> dict:
    """Check 1: Schema compliance."""
    if not rows:
        return {"verdict": "WARNING", "detail": "Empty CSV"}
    header = list(rows[0].keys())
    missing = [c for c in REQUIRED_COLUMNS_V31 if c not in header]
    extra = [c for c in header if c not in REQUIRED_COLUMNS_V31]
    version = rows[0].get("RegisterSchemaVersion", "UNKNOWN")
    valid = len(missing) == 0 and version == "v3.1"
    return {
        "verdict": "PASS" if valid else "WARNING",
        "version": version,
        "missing_columns": missing,
        "extra_columns": extra,
        "column_count": len(header),
    }


def build_graph(rows: list[dict]) -> tuple[set, list]:
    """Build directed graph from filtered rows. Returns (nodes, edges)."""
    nodes = {SCOPE_DELIVERABLE}
    edges = []
    for row in rows:
        if FILTER_ACTIVE_ONLY and row.get("Status", "").strip() != "ACTIVE":
            continue
        if row.get("DependencyClass", "").strip() != EDGE_FILTER_CLASS:
            continue
        if row.get("TargetType", "").strip() != EDGE_FILTER_TARGET_TYPE:
            continue
        from_id = normalize_id(row.get("FromDeliverableID", "")) if NORMALIZE_IDS else row.get("FromDeliverableID", "").strip()
        to_id = normalize_id(row.get("TargetDeliverableID", "")) if NORMALIZE_IDS else row.get("TargetDeliverableID", "").strip()
        if from_id and to_id:
            nodes.add(from_id)
            nodes.add(to_id)
            edges.append({
                "from": from_id,
                "to": to_id,
                "dependency_id": row.get("DependencyID", "").strip(),
                "direction": row.get("Direction", "").strip(),
                "type": row.get("DependencyType", "").strip(),
            })
    return nodes, edges


def tarjan_scc(nodes: set, edges: list) -> list[list]:
    """Tarjan's SCC algorithm. Returns list of SCCs."""
    adj = defaultdict(list)
    for e in edges:
        adj[e["from"]].append(e["to"])

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

        for w in adj.get(v, []):
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
            sccs.append(scc)

    for node in sorted(nodes):
        if node not in index:
            strongconnect(node)

    return sccs


def check_orphans(edges: list) -> list:
    """Check 2: Orphan dependencies."""
    orphans = []
    for e in edges:
        if e["to"] not in VALID_DELIVERABLE_IDS:
            orphans.append(e)
    return orphans


def check_anchors(rows: list) -> dict:
    """Check 4: Anchor coverage."""
    implements_node = 0
    traces_to_req = 0
    for row in rows:
        if row.get("DependencyClass", "").strip() == "ANCHOR":
            anchor_type = row.get("AnchorType", "").strip()
            if anchor_type == "IMPLEMENTS_NODE":
                implements_node += 1
            elif anchor_type == "TRACES_TO_REQUIREMENT":
                traces_to_req += 1
    return {
        "verdict": "PASS" if implements_node >= 1 else "WARNING",
        "implements_node": implements_node,
        "traces_to_requirement": traces_to_req,
    }


def check_misplaced(rows: list) -> list:
    """Check 5: Misplaced fields."""
    misplaced = []
    for row in rows:
        target_type = row.get("TargetType", "").strip()
        target_del_id = row.get("TargetDeliverableID", "").strip()
        if target_type != "DELIVERABLE" and target_del_id:
            misplaced.append({
                "dependency_id": row.get("DependencyID", "").strip(),
                "target_type": target_type,
                "target_deliverable_id": target_del_id,
            })
    return misplaced


def check_id_format(rows: list) -> dict:
    """Check 6: ID format consistency."""
    long_form = 0
    short_form = 0
    for row in rows:
        for field in ["FromDeliverableID", "TargetDeliverableID"]:
            raw = row.get(field, "").strip()
            if not raw:
                continue
            m = ID_PATTERN.match(raw)
            if m and m.group(0) != raw:
                long_form += 1
            else:
                short_form += 1
    total = long_form + short_form
    return {
        "verdict": "PASS",
        "long_form": long_form,
        "short_form": short_form,
        "normalization_rate_pct": (long_form / total * 100) if total > 0 else 0.0,
    }


def main():
    # Resolve execution root
    script_dir = Path(__file__).resolve().parent
    default_root = script_dir.parent.parent.parent  # up from snapshot -> DepClosure -> _Reconciliation -> execution
    exec_root = Path(sys.argv[2]) if len(sys.argv) > 2 and sys.argv[1] == "--execution-root" else default_root

    csv_path = exec_root / DELIVERABLE_PATH / "Dependencies.csv"
    if not csv_path.exists():
        print(f"ERROR: Dependencies.csv not found at {csv_path}")
        sys.exit(1)

    print(f"=== Dependency Closure Analysis: {SCOPE_DELIVERABLE} ===")
    print(f"CSV: {csv_path}")
    print()

    rows = parse_csv(str(csv_path))
    print(f"Total rows: {len(rows)}")

    # Check 1: Schema
    schema = check_schema(rows, str(csv_path))
    print(f"\n[Check 1] Schema Compliance: {schema['verdict']}")
    print(f"  Version: {schema['version']}, Columns: {schema['column_count']}")
    if schema["missing_columns"]:
        print(f"  Missing: {schema['missing_columns']}")

    # Build graph
    nodes, edges = build_graph(rows)
    print(f"\nGraph: {len(nodes)} nodes, {len(edges)} edges")
    for e in edges:
        print(f"  {e['from']} -> {e['to']} ({e['dependency_id']}, {e['type']})")

    # Check 2: Orphans
    orphans = check_orphans(edges)
    print(f"\n[Check 2] Orphan Dependencies: {'PASS' if not orphans else 'WARNING'}")
    if orphans:
        for o in orphans:
            print(f"  ORPHAN: {o['from']} -> {o['to']} ({o['dependency_id']})")

    # Check 3: Cycles (Tarjan SCC)
    sccs = tarjan_scc(nodes, edges)
    non_trivial = [s for s in sccs if len(s) > 1]
    print(f"\n[Check 3] Circular Dependencies: {'PASS' if not non_trivial else 'BLOCKER'}")
    print(f"  SCCs: {len(sccs)} total, {len(non_trivial)} non-trivial")
    for scc in non_trivial:
        print(f"  CYCLE: {' -> '.join(scc)}")

    # Check 4: Anchors
    anchors = check_anchors(rows)
    print(f"\n[Check 4] Anchor Coverage: {anchors['verdict']}")
    print(f"  IMPLEMENTS_NODE: {anchors['implements_node']}, TRACES_TO_REQUIREMENT: {anchors['traces_to_requirement']}")

    # Check 5: Misplaced
    misplaced = check_misplaced(rows)
    print(f"\n[Check 5] Misplaced Fields: {'PASS' if not misplaced else 'WARNING'}")
    if misplaced:
        for m in misplaced:
            print(f"  {m['dependency_id']}: TargetType={m['target_type']}, TargetDeliverableID={m['target_deliverable_id']}")

    # Check 6: ID format
    id_fmt = check_id_format(rows)
    print(f"\n[Check 6] ID Format Consistency: {id_fmt['verdict']}")
    print(f"  Short-form: {id_fmt['short_form']}, Long-form: {id_fmt['long_form']}, Normalization rate: {id_fmt['normalization_rate_pct']:.1f}%")

    # Check 7: Isolated
    degree = defaultdict(int)
    for e in edges:
        degree[e["from"]] += 1
        degree[e["to"]] += 1
    isolated = [n for n in [SCOPE_DELIVERABLE] if degree[n] == 0]
    print(f"\n[Check 7] Isolated Deliverables: {'PASS' if not isolated else 'WARNING'}")
    print(f"  {SCOPE_DELIVERABLE} degree: {degree.get(SCOPE_DELIVERABLE, 0)}")

    # Check 8: Hubs
    hubs = [(n, degree[n]) for n in nodes if degree[n] >= HUB_THRESHOLD]
    print(f"\n[Check 8] Hub Analysis: {'PASS' if not hubs else 'WARNING'}")
    print(f"  Max degree: {max(degree.values()) if degree else 0}, Threshold: {HUB_THRESHOLD}")

    # Check 9: Bidirectional
    edge_set = {(e["from"], e["to"]) for e in edges}
    bidir = [(a, b) for (a, b) in edge_set if (b, a) in edge_set and a < b]
    print(f"\n[Check 9] Bidirectional Pairs: {'PASS' if not bidir else 'INFO'}")
    if bidir:
        for a, b in bidir:
            print(f"  {a} <-> {b}")

    # Summary
    all_pass = (
        schema["verdict"] == "PASS"
        and not orphans
        and not non_trivial
        and anchors["verdict"] == "PASS"
        and not misplaced
        and id_fmt["verdict"] == "PASS"
        and not isolated
        and not hubs
    )
    print(f"\n{'=' * 50}")
    print(f"OVERALL: {'PASS' if all_pass else 'ISSUES FOUND'}")


if __name__ == "__main__":
    main()
