#!/usr/bin/env python3
"""
Reproducible dependency closure analysis script for DEL-08-03.

Run label: DEL-08-03
Snapshot: CLOSURE_DEL-08-03_2026-02-21
Date: 2026-02-21

This script reproduces the analysis performed by the AUDIT_DEP_CLOSURE agent.
It reads the Dependencies.csv for DEL-08-03, applies the same filters, builds
the graph, and runs all 9 core checks.

Usage:
    python3 analyze_closure.py [--execution-root PATH]

Default execution root: ../../.. (relative to this script's location,
resolving to the execution/ folder).
"""

import csv
import json
import os
import re
import sys
from collections import defaultdict
from pathlib import Path

# --- Configuration (matches the brief) ---
SCOPE = ["DEL-08-03"]
FILTER_ACTIVE_ONLY = True
NORMALIZE_IDS = True
EDGE_FILTER_DEPENDENCY_CLASS = "EXECUTION"
EDGE_FILTER_TARGET_TYPE = "DELIVERABLE"
HUB_THRESHOLD = 20
MAX_CYCLES = 10000

# All 32 valid workspace deliverable IDs
VALID_DELIVERABLE_IDS = [
    "DEL-01-01", "DEL-01-02",
    "DEL-02-01", "DEL-02-02", "DEL-02-03", "DEL-02-04",
    "DEL-03-01", "DEL-03-02", "DEL-03-03", "DEL-03-04", "DEL-03-05", "DEL-03-06",
    "DEL-04-01", "DEL-04-02",
    "DEL-05-01", "DEL-05-02", "DEL-05-03", "DEL-05-04",
    "DEL-06-01", "DEL-06-02", "DEL-06-03", "DEL-06-04", "DEL-06-05",
    "DEL-07-01", "DEL-07-02",
    "DEL-08-01", "DEL-08-02", "DEL-08-03", "DEL-08-04", "DEL-08-05", "DEL-08-06", "DEL-08-07",
]


def normalize_id(raw_id: str) -> str:
    """Normalize a deliverable ID by stripping descriptive suffixes."""
    if not raw_id:
        return raw_id
    match = re.match(r"(DEL-\d{2}-\d{2})", raw_id)
    if match:
        return match.group(1)
    return raw_id


def find_dependencies_csv(execution_root: Path, deliverable_id: str) -> Path | None:
    """Locate Dependencies.csv for a deliverable by scanning the execution root."""
    for pkg_dir in sorted(execution_root.iterdir()):
        if not pkg_dir.is_dir() or pkg_dir.name.startswith("_"):
            continue
        working_dir = pkg_dir / "1_Working"
        if not working_dir.is_dir():
            continue
        for del_dir in sorted(working_dir.iterdir()):
            if del_dir.is_dir() and del_dir.name.startswith(deliverable_id):
                csv_path = del_dir / "Dependencies.csv"
                if csv_path.is_file():
                    return csv_path
    return None


def parse_csv(csv_path: Path) -> list[dict]:
    """Parse a Dependencies.csv and return rows as dicts."""
    rows = []
    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)
    return rows


def validate_schema(rows: list[dict], csv_path: Path) -> tuple[bool, str]:
    """Validate that the CSV has all v3.1 required columns."""
    expected_columns = [
        "RegisterSchemaVersion", "DependencyID", "FromPackageID",
        "FromDeliverableID", "FromDeliverableName", "DependencyClass",
        "AnchorType", "Direction", "DependencyType", "TargetType",
        "TargetPackageID", "TargetDeliverableID", "TargetRefID",
        "TargetName", "TargetLocation", "Statement", "EvidenceFile",
        "SourceRef", "EvidenceQuote", "Explicitness", "RequiredMaturity",
        "ProposedMaturity", "SatisfactionStatus", "Confidence", "Origin",
        "FirstSeen", "LastSeen", "Status", "Notes",
    ]
    if not rows:
        return False, "No rows found"
    actual_columns = list(rows[0].keys())
    missing = set(expected_columns) - set(actual_columns)
    if missing:
        return False, f"Missing columns: {sorted(missing)}"
    for row in rows:
        if row.get("RegisterSchemaVersion") != "v3.1":
            return False, f"Row {row.get('DependencyID')} has version {row.get('RegisterSchemaVersion')}"
    return True, "v3.1 valid"


def build_edges(rows: list[dict]) -> list[dict]:
    """Extract graph edges from rows applying the edge filter."""
    edges = []
    for row in rows:
        if FILTER_ACTIVE_ONLY and row.get("Status") != "ACTIVE":
            continue
        if row.get("DependencyClass") != EDGE_FILTER_DEPENDENCY_CLASS:
            continue
        if row.get("TargetType") != EDGE_FILTER_TARGET_TYPE:
            continue
        from_id = row.get("FromDeliverableID", "")
        target_id = row.get("TargetDeliverableID", "")
        if NORMALIZE_IDS:
            from_id = normalize_id(from_id)
            target_id = normalize_id(target_id)
        if from_id and target_id:
            edges.append({
                "from": from_id,
                "to": target_id,
                "dependency_id": row.get("DependencyID", ""),
                "type": row.get("DependencyType", ""),
                "direction": row.get("Direction", ""),
            })
    return edges


def tarjan_scc(nodes: set, edges: list[dict]) -> list[list[str]]:
    """Tarjan's algorithm for strongly connected components."""
    graph = defaultdict(list)
    for e in edges:
        graph[e["from"]].append(e["to"])

    index_counter = [0]
    stack = []
    on_stack = set()
    index = {}
    lowlink = {}
    sccs = []

    def strongconnect(v):
        index[v] = index_counter[0]
        lowlink[v] = index_counter[0]
        index_counter[0] += 1
        stack.append(v)
        on_stack.add(v)

        for w in graph.get(v, []):
            if w not in index:
                strongconnect(w)
                lowlink[v] = min(lowlink[v], lowlink[w])
            elif w in on_stack:
                lowlink[v] = min(lowlink[v], index[w])

        if lowlink[v] == index[v]:
            scc = []
            while True:
                w = stack.pop()
                on_stack.discard(w)
                scc.append(w)
                if w == v:
                    break
            sccs.append(scc)

    for node in sorted(nodes):
        if node not in index:
            strongconnect(node)

    return sccs


def check_orphans(edges: list[dict], valid_ids: list[str]) -> list[dict]:
    """Check for target IDs not in the valid workspace set."""
    valid_set = set(valid_ids)
    orphans = []
    for e in edges:
        if e["to"] not in valid_set:
            orphans.append(e)
    return orphans


def check_anchors(rows: list[dict]) -> bool:
    """Check if at least one ANCHOR/IMPLEMENTS_NODE row exists."""
    for row in rows:
        if (row.get("DependencyClass") == "ANCHOR"
                and row.get("AnchorType") == "IMPLEMENTS_NODE"):
            return True
    return False


def check_misplaced_fields(rows: list[dict]) -> list[dict]:
    """Find rows where TargetType != DELIVERABLE but TargetDeliverableID is non-empty."""
    issues = []
    for row in rows:
        if (row.get("TargetType") != "DELIVERABLE"
                and row.get("TargetDeliverableID", "").strip()):
            issues.append(row)
    return issues


def check_id_format(rows: list[dict]) -> dict:
    """Check ID format consistency and normalization rate."""
    total = 0
    normalized = 0
    for row in rows:
        for field in ["FromDeliverableID", "TargetDeliverableID"]:
            raw = row.get(field, "").strip()
            if raw:
                total += 1
                norm = normalize_id(raw)
                if norm != raw:
                    normalized += 1
    rate = (normalized / total * 100) if total > 0 else 0
    return {"total_ids": total, "normalized_count": normalized, "rate_pct": rate}


def main():
    # Resolve execution root
    script_dir = Path(__file__).resolve().parent
    default_root = script_dir.parent.parent.parent
    execution_root = Path(sys.argv[1]) if len(sys.argv) > 1 else default_root

    if not execution_root.is_dir():
        print(f"ERROR: Execution root not found: {execution_root}", file=sys.stderr)
        sys.exit(1)

    print(f"Execution root: {execution_root}")
    print(f"Scope: {SCOPE}")
    print()

    # Step 1: Locate Dependencies.csv
    for del_id in SCOPE:
        csv_path = find_dependencies_csv(execution_root, del_id)
        if csv_path is None:
            print(f"  {del_id}: MISSING_DEPENDENCIES_CSV")
            continue
        print(f"  {del_id}: Found at {csv_path}")

        # Step 2: Parse and validate schema
        rows = parse_csv(csv_path)
        valid, msg = validate_schema(rows, csv_path)
        print(f"  Schema: {'VALID' if valid else 'INVALID'} -- {msg}")
        if not valid:
            continue

        # Step 3: Build graph
        edges = build_edges(rows)
        nodes = set()
        for e in edges:
            nodes.add(e["from"])
            nodes.add(e["to"])
        nodes.add(del_id)  # ensure scope deliverable is always a node
        print(f"  Graph: {len(nodes)} nodes, {len(edges)} edges")
        for e in edges:
            print(f"    {e['from']} -> {e['to']} ({e['dependency_id']}, {e['type']})")

        # Step 4: Core checks
        print()
        print("--- Core Checks ---")

        # Check 1: Schema compliance
        print(f"  1. Schema compliance: PASS ({msg})")

        # Check 2: Orphan dependencies
        orphans = check_orphans(edges, VALID_DELIVERABLE_IDS)
        verdict = "PASS" if len(orphans) == 0 else "BLOCKER"
        print(f"  2. Orphan dependencies: {verdict} ({len(orphans)} orphans)")

        # Check 3: Circular dependencies
        sccs = tarjan_scc(nodes, edges)
        nontrivial = [s for s in sccs if len(s) > 1]
        verdict = "PASS" if len(nontrivial) == 0 else "BLOCKER"
        print(f"  3. Circular dependencies: {verdict} ({len(nontrivial)} non-trivial SCCs)")

        # Check 4: Anchor coverage
        has_anchor = check_anchors(rows)
        verdict = "PASS" if has_anchor else "WARNING"
        print(f"  4. Anchor coverage: {verdict}")

        # Check 5: Misplaced fields
        misplaced = check_misplaced_fields(rows)
        verdict = "PASS" if len(misplaced) == 0 else "WARNING"
        print(f"  5. Misplaced fields: {verdict} ({len(misplaced)} issues)")

        # Check 6: ID format consistency
        id_stats = check_id_format(rows)
        verdict = "PASS"
        print(f"  6. ID format consistency: {verdict} (normalization rate: {id_stats['rate_pct']:.1f}%)")

        # Check 7: Isolated deliverables
        out_degree = sum(1 for e in edges if e["from"] == del_id)
        isolated = out_degree == 0
        verdict = "PASS" if not isolated else "WARNING"
        print(f"  7. Isolated deliverables: {verdict} (out-degree={out_degree})")

        # Check 8: Hub analysis
        degree = defaultdict(int)
        for e in edges:
            degree[e["from"]] += 1
            degree[e["to"]] += 1
        max_deg = max(degree.values()) if degree else 0
        hubs = {n: d for n, d in degree.items() if d >= HUB_THRESHOLD}
        verdict = "PASS" if len(hubs) == 0 else "WARNING"
        print(f"  8. Hub analysis: {verdict} (max degree={max_deg}, threshold={HUB_THRESHOLD})")

        # Check 9: Bidirectional pairs
        edge_set = {(e["from"], e["to"]) for e in edges}
        bidir = [(a, b) for (a, b) in edge_set if (b, a) in edge_set and a < b]
        verdict = "PASS" if len(bidir) == 0 else "INFO"
        print(f"  9. Bidirectional pairs: {verdict} ({len(bidir)} pairs)")

        print()
        print("--- Overall: PASS ---" if all([
            len(orphans) == 0,
            len(nontrivial) == 0,
            has_anchor,
            len(misplaced) == 0,
            not isolated,
            len(hubs) == 0,
        ]) else "--- Overall: ISSUES FOUND ---")


if __name__ == "__main__":
    main()
