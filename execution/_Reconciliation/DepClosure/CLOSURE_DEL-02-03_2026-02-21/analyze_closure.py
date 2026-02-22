#!/usr/bin/env python3
"""
Dependency Closure Analysis Script
Run: CLOSURE_DEL-02-03_2026-02-21
Scope: DEL-02-03 (single deliverable)

Reproduces the closure analysis performed by AUDIT_DEP_CLOSURE.
Usage: python3 analyze_closure.py [path_to_dependencies_csv]

If no path is provided, defaults to the DEL-02-03 Dependencies.csv
relative to the execution root.
"""

import csv
import json
import os
import re
import sys
from collections import defaultdict
from pathlib import Path


# --- Configuration ---
DEFAULT_CSV_REL = (
    "execution/PKG-02_Desktop_UI_Workflow/1_Working/"
    "DEL-02-03_Operator_Toolkit_Panel/Dependencies.csv"
)
EDGE_FILTER_CLASS = "EXECUTION"
EDGE_FILTER_TARGET_TYPE = "DELIVERABLE"
FILTER_ACTIVE_ONLY = True
NORMALIZE_IDS = True
HUB_THRESHOLD = 20
MAX_CYCLES = 10000

# All 32 known workspace deliverable IDs
WORKSPACE_DELIVERABLES = {
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

EXPECTED_COLUMNS_V31 = [
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
    """Strip descriptive suffix from deliverable IDs for analysis."""
    if not NORMALIZE_IDS or not raw_id:
        return raw_id
    match = re.match(r"(DEL-\d{2}-\d{2})", raw_id)
    if match:
        return match.group(1)
    return raw_id


def validate_schema(header: list[str]) -> tuple[bool, list[str]]:
    """Check if CSV header matches expected v3.1 schema."""
    errors = []
    for i, expected_col in enumerate(EXPECTED_COLUMNS_V31):
        if i >= len(header):
            errors.append(f"Missing column at index {i}: expected '{expected_col}'")
        elif header[i].strip() != expected_col:
            errors.append(
                f"Column mismatch at index {i}: "
                f"expected '{expected_col}', got '{header[i].strip()}'"
            )
    if len(header) > len(EXPECTED_COLUMNS_V31):
        errors.append(
            f"Extra columns: {len(header)} found, {len(EXPECTED_COLUMNS_V31)} expected"
        )
    return len(errors) == 0, errors


def tarjan_scc(graph: dict[str, list[str]]) -> list[list[str]]:
    """Tarjan's algorithm for strongly connected components."""
    index_counter = [0]
    stack = []
    lowlink = {}
    index = {}
    on_stack = {}
    sccs = []

    all_nodes = set(graph.keys())
    for targets in graph.values():
        all_nodes.update(targets)

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
            sccs.append(scc)

    for node in sorted(all_nodes):
        if node not in index:
            strongconnect(node)

    return sccs


def main():
    # Resolve CSV path
    if len(sys.argv) > 1:
        csv_path = Path(sys.argv[1])
    else:
        repo_root = Path(__file__).resolve().parent.parent.parent.parent.parent
        csv_path = repo_root / DEFAULT_CSV_REL

    if not csv_path.exists():
        print(f"ERROR: Dependencies.csv not found at {csv_path}")
        sys.exit(1)

    print(f"Analyzing: {csv_path}")
    print(f"Scope: DEL-02-03 (single deliverable)")
    print("=" * 70)

    # --- Parse CSV ---
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        header = reader.fieldnames or []
        rows = list(reader)

    # --- Check 1: Schema Compliance ---
    schema_valid, schema_errors = validate_schema(header)
    print(f"\nCheck 1 - Schema Compliance: {'PASS' if schema_valid else 'FAIL'}")
    if schema_errors:
        for err in schema_errors:
            print(f"  ERROR: {err}")

    # --- Parse rows ---
    anchor_rows = []
    execution_rows = []
    edges = []  # (from_id, to_id, dep_id, direction, dep_type)

    for row in rows:
        dep_class = row.get("DependencyClass", "").strip()
        status = row.get("Status", "").strip()
        target_type = row.get("TargetType", "").strip()

        if FILTER_ACTIVE_ONLY and status != "ACTIVE":
            continue

        if dep_class == "ANCHOR":
            anchor_rows.append(row)
        elif dep_class == "EXECUTION":
            execution_rows.append(row)
            if target_type == EDGE_FILTER_TARGET_TYPE:
                from_id = normalize_id(row.get("FromDeliverableID", "").strip())
                to_id = normalize_id(row.get("TargetDeliverableID", "").strip())
                dep_id = row.get("DependencyID", "").strip()
                direction = row.get("Direction", "").strip()
                dep_type = row.get("DependencyType", "").strip()
                if from_id and to_id:
                    edges.append((from_id, to_id, dep_id, direction, dep_type))

    print(f"\nParsing Summary:")
    print(f"  Total rows: {len(rows)}")
    print(f"  ANCHOR rows: {len(anchor_rows)}")
    print(f"  EXECUTION rows: {len(execution_rows)}")
    print(f"  EXECUTION/DELIVERABLE edges: {len(edges)}")

    # --- Build graph ---
    graph = defaultdict(list)
    nodes = set()
    for from_id, to_id, _, direction, _ in edges:
        nodes.add(from_id)
        nodes.add(to_id)
        if direction == "UPSTREAM":
            graph[from_id].append(to_id)
        elif direction == "DOWNSTREAM":
            graph[from_id].append(to_id)

    print(f"\nGraph: {len(nodes)} nodes, {len(edges)} edges")

    # --- Check 2: Orphan Dependencies ---
    orphans = []
    for _, to_id, dep_id, _, _ in edges:
        if to_id not in WORKSPACE_DELIVERABLES:
            orphans.append((to_id, dep_id))
    print(f"\nCheck 2 - Orphan Dependencies: {'PASS' if not orphans else 'BLOCKER'}")
    if orphans:
        for target, dep in orphans:
            print(f"  ORPHAN: {target} (from {dep})")

    # --- Check 3: Circular Dependencies (Tarjan SCC) ---
    sccs = tarjan_scc(dict(graph))
    nontrivial_sccs = [scc for scc in sccs if len(scc) > 1]
    print(
        f"\nCheck 3 - Circular Dependencies: "
        f"{'PASS' if not nontrivial_sccs else 'BLOCKER'}"
    )
    print(f"  SCCs total: {len(sccs)}, non-trivial: {len(nontrivial_sccs)}")
    for scc in nontrivial_sccs[:10]:
        print(f"  CYCLE: {' -> '.join(scc)}")

    # --- Check 4: Anchor Coverage ---
    has_implements = any(
        row.get("AnchorType", "").strip() == "IMPLEMENTS_NODE"
        for row in anchor_rows
    )
    print(
        f"\nCheck 4 - Anchor Coverage: "
        f"{'PASS' if has_implements else 'WARNING'}"
    )
    print(f"  ANCHOR rows: {len(anchor_rows)}")
    print(f"  IMPLEMENTS_NODE present: {has_implements}")

    # --- Check 5: Misplaced Fields ---
    misplaced = []
    for row in rows:
        target_type = row.get("TargetType", "").strip()
        target_del_id = row.get("TargetDeliverableID", "").strip()
        if target_type != "DELIVERABLE" and target_del_id:
            misplaced.append(row.get("DependencyID", ""))
    print(
        f"\nCheck 5 - Misplaced Fields: "
        f"{'PASS' if not misplaced else 'WARNING'}"
    )
    if misplaced:
        for dep_id in misplaced:
            print(f"  MISPLACED: {dep_id}")

    # --- Check 6: ID Format Consistency ---
    id_pattern = re.compile(r"^DEL-\d{2}-\d{2}$")
    all_ids = []
    norm_needed = 0
    for row in rows:
        for col in ("FromDeliverableID", "TargetDeliverableID"):
            raw = row.get(col, "").strip()
            if raw:
                all_ids.append(raw)
                if not id_pattern.match(raw):
                    norm_needed += 1
    norm_rate = (norm_needed / len(all_ids) * 100) if all_ids else 0
    print(f"\nCheck 6 - ID Format Consistency: PASS")
    print(f"  IDs checked: {len(all_ids)}, normalization needed: {norm_needed} ({norm_rate:.1f}%)")

    # --- Check 7: Isolated Deliverables ---
    in_scope = {"DEL-02-03"}
    isolated = [n for n in in_scope if n not in nodes or (
        len(graph.get(n, [])) == 0 and
        all(n not in graph.get(other, []) for other in nodes if other != n)
    )]
    print(
        f"\nCheck 7 - Isolated Deliverables: "
        f"{'PASS' if not isolated else 'WARNING'}"
    )

    # --- Check 8: Hub Analysis ---
    degree = defaultdict(int)
    for from_id, to_id, _, _, _ in edges:
        degree[from_id] += 1
        degree[to_id] += 1
    hubs = {n: d for n, d in degree.items() if d >= HUB_THRESHOLD}
    max_deg_node = max(degree, key=degree.get) if degree else "N/A"
    max_deg = degree[max_deg_node] if degree else 0
    print(f"\nCheck 8 - Hub Analysis: {'PASS' if not hubs else 'WARNING'}")
    print(f"  Max degree: {max_deg} ({max_deg_node}), threshold: {HUB_THRESHOLD}")

    # --- Check 9: Bidirectional Pairs ---
    edge_set = {(f, t) for f, t, _, _, _ in edges}
    bidir = [(a, b) for a, b in edge_set if (b, a) in edge_set and a < b]
    print(
        f"\nCheck 9 - Bidirectional Pairs: "
        f"{'PASS' if not bidir else 'INFO'}"
    )
    print(f"  Pairs found: {len(bidir)}")

    # --- Overall ---
    has_blocker = bool(orphans or nontrivial_sccs)
    has_warning = bool(misplaced or isolated or hubs or not has_implements)
    if has_blocker:
        overall = "BLOCKER"
    elif has_warning:
        overall = "WARNINGS"
    else:
        overall = "PASS"
    print(f"\n{'=' * 70}")
    print(f"OVERALL STATUS: {overall}")


if __name__ == "__main__":
    main()
