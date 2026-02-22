#!/usr/bin/env python3
"""
Dependency Closure Analysis Script -- DEL-07-01
Snapshot: CLOSURE_DEL-07-01_2026-02-21
Generated: 2026-02-21

Reproduces the closure analysis performed by AUDIT_DEP_CLOSURE for DEL-07-01.
Run from the repository root with:
    python3 execution/_Reconciliation/DepClosure/CLOSURE_DEL-07-01_2026-02-21/analyze_closure.py

Requires: Python 3.9+ (stdlib only, no external dependencies)
"""

import csv
import json
import os
import re
import sys
from collections import defaultdict
from pathlib import Path

# --- Configuration ---
EXECUTION_ROOT = "execution"
SCOPE = ["DEL-07-01"]
DELIVERABLE_PATH = os.path.join(
    EXECUTION_ROOT,
    "PKG-07_Validation_Example_Assets",
    "1_Working",
    "DEL-07-01_Harness_Validation_Suite",
)
FILTER_ACTIVE_ONLY = True
NORMALIZE_IDS = True
EDGE_FILTER_CLASS = "EXECUTION"
EDGE_FILTER_TARGET_TYPE = "DELIVERABLE"
HUB_THRESHOLD = 20
MAX_CYCLES = 10000

# Known workspace deliverables (32 total)
WORKSPACE_DELIVERABLES = {
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

SHORT_FORM_PATTERN = re.compile(r"^DEL-\d{2}-\d{2}$")


def normalize_id(raw_id: str) -> str:
    """Strip descriptive suffix from long-form IDs (e.g., DEL-07-01_Foo -> DEL-07-01)."""
    if not raw_id:
        return raw_id
    match = re.match(r"^(DEL-\d{2}-\d{2})(?:_.*)?$", raw_id)
    return match.group(1) if match else raw_id


def read_dependencies_csv(path: str) -> tuple:
    """Read and parse Dependencies.csv. Returns (rows, columns, errors)."""
    rows = []
    errors = []
    try:
        with open(path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            columns = reader.fieldnames or []
            for i, row in enumerate(reader, start=2):  # row 1 = header
                rows.append(row)
    except FileNotFoundError:
        errors.append(f"File not found: {path}")
        return [], [], errors
    except Exception as e:
        errors.append(f"Read error: {e}")
        return [], [], errors
    return rows, columns, errors


def validate_schema(columns: list) -> tuple:
    """Validate v3.1 schema columns. Returns (is_valid, missing, extra)."""
    col_set = set(columns)
    required_set = set(REQUIRED_COLUMNS_V31)
    missing = required_set - col_set
    extra = col_set - required_set
    return len(missing) == 0, sorted(missing), sorted(extra)


def tarjan_scc(graph: dict) -> list:
    """Tarjan's SCC algorithm. Returns list of SCCs (each a list of node IDs)."""
    index_counter = [0]
    stack = []
    lowlink = {}
    index = {}
    on_stack = {}
    result = []

    def strongconnect(v):
        index[v] = index_counter[0]
        lowlink[v] = index_counter[0]
        index_counter[0] += 1
        stack.append(v)
        on_stack[v] = True

        for w in graph.get(v, []):
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
            result.append(scc)

    for node in graph:
        if node not in index:
            strongconnect(node)

    return result


def main():
    print("=" * 60)
    print("Dependency Closure Analysis -- DEL-07-01")
    print("=" * 60)

    csv_path = os.path.join(DELIVERABLE_PATH, "Dependencies.csv")
    rows, columns, errors = read_dependencies_csv(csv_path)

    if errors:
        print(f"\nERROR: {errors}")
        sys.exit(1)

    # Check 1: Schema compliance
    schema_valid, missing, extra = validate_schema(columns)
    print(f"\n[Check 1] Schema Compliance: {'PASS' if schema_valid else 'FAIL'}")
    if missing:
        print(f"  Missing columns: {missing}")
    if extra:
        print(f"  Extra columns: {extra}")

    # Filter rows
    active_rows = [r for r in rows if not FILTER_ACTIVE_ONLY or r.get("Status") == "ACTIVE"]
    edge_rows = [
        r for r in active_rows
        if r.get("DependencyClass") == EDGE_FILTER_CLASS
        and r.get("TargetType") == EDGE_FILTER_TARGET_TYPE
    ]
    anchor_rows = [r for r in active_rows if r.get("DependencyClass") == "ANCHOR"]

    print(f"\n  Total rows: {len(rows)}")
    print(f"  Active rows: {len(active_rows)}")
    print(f"  Edge rows (EXECUTION+DELIVERABLE): {len(edge_rows)}")
    print(f"  Anchor rows: {len(anchor_rows)}")

    # Build graph
    graph = defaultdict(list)
    edges = []
    for r in edge_rows:
        from_id = normalize_id(r["FromDeliverableID"]) if NORMALIZE_IDS else r["FromDeliverableID"]
        to_id = normalize_id(r["TargetDeliverableID"]) if NORMALIZE_IDS else r["TargetDeliverableID"]
        if from_id and to_id:
            graph[from_id].append(to_id)
            if to_id not in graph:
                graph[to_id] = []
            edges.append({
                "dependency_id": r["DependencyID"],
                "from": from_id,
                "to": to_id,
                "direction": r.get("Direction", ""),
                "type": r.get("DependencyType", ""),
            })

    # Check 2: Orphan dependencies
    orphans = []
    for e in edges:
        if e["to"] not in WORKSPACE_DELIVERABLES:
            orphans.append(e)
    print(f"\n[Check 2] Orphan Dependencies: {'PASS' if not orphans else 'BLOCKER'}")
    print(f"  Orphans: {len(orphans)}")
    for o in orphans:
        print(f"    {o['dependency_id']}: {o['from']} -> {o['to']}")

    # Check 3: Circular dependencies (Tarjan SCC)
    sccs = tarjan_scc(graph)
    non_trivial = [s for s in sccs if len(s) > 1]
    print(f"\n[Check 3] Circular Dependencies: {'PASS' if not non_trivial else 'BLOCKER'}")
    print(f"  SCCs: {len(sccs)}, Non-trivial: {len(non_trivial)}")
    for s in non_trivial:
        print(f"    Cycle members: {s}")

    # Check 4: Anchor coverage
    implements = [r for r in anchor_rows if r.get("AnchorType") == "IMPLEMENTS_NODE"]
    print(f"\n[Check 4] Anchor Coverage: {'PASS' if implements else 'WARNING'}")
    print(f"  IMPLEMENTS_NODE anchors: {len(implements)}")

    # Check 5: Misplaced fields
    misplaced = []
    for r in active_rows:
        if r.get("TargetType") != "DELIVERABLE" and r.get("TargetDeliverableID", "").strip():
            misplaced.append(r)
    print(f"\n[Check 5] Misplaced Fields: {'PASS' if not misplaced else 'WARNING'}")
    print(f"  Misplaced rows: {len(misplaced)}")

    # Check 6: ID format consistency
    from_ids = [r["FromDeliverableID"] for r in active_rows if r.get("FromDeliverableID")]
    target_ids = [r["TargetDeliverableID"] for r in edge_rows if r.get("TargetDeliverableID")]
    long_from = [i for i in from_ids if not SHORT_FORM_PATTERN.match(i)]
    long_target = [i for i in target_ids if not SHORT_FORM_PATTERN.match(i)]
    print(f"\n[Check 6] ID Format Consistency: {'PASS' if not long_from and not long_target else 'WARNING'}")
    print(f"  Long-form FromIDs: {len(long_from)}, Long-form TargetIDs: {len(long_target)}")

    # Check 7: Isolated deliverables
    in_scope_nodes = set(SCOPE)
    isolated = [n for n in in_scope_nodes if len(graph.get(n, [])) == 0]
    print(f"\n[Check 7] Isolated Deliverables: {'PASS' if not isolated else 'WARNING'}")
    print(f"  Isolated: {len(isolated)}")

    # Check 8: Hub analysis
    degrees = {}
    for node in graph:
        if node in in_scope_nodes:
            out_deg = len(graph[node])
            degrees[node] = {"out": out_deg, "in": 0, "total": out_deg}
    hubs = {k: v for k, v in degrees.items() if v["total"] >= HUB_THRESHOLD}
    print(f"\n[Check 8] Hub Analysis: {'PASS' if not hubs else 'WARNING'}")
    print(f"  Hubs above threshold ({HUB_THRESHOLD}): {len(hubs)}")

    # Check 9: Bidirectional pairs
    edge_set = {(e["from"], e["to"]) for e in edges}
    bidir = [(a, b) for (a, b) in edge_set if (b, a) in edge_set and a < b]
    print(f"\n[Check 9] Bidirectional Pairs: {'PASS' if not bidir else 'INFO'}")
    print(f"  Bidirectional pairs: {len(bidir)}")

    # Overall
    has_blocker = bool(orphans or non_trivial)
    has_warning = bool(misplaced or long_from or long_target or isolated or hubs)
    if has_blocker:
        overall = "BLOCKER"
    elif has_warning:
        overall = "WARNINGS"
    else:
        overall = "PASS"

    print(f"\n{'=' * 60}")
    print(f"OVERALL STATUS: {overall}")
    print(f"{'=' * 60}")

    return 0 if overall == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
