#!/usr/bin/env python3
"""
analyze_closure.py -- Reproducible dependency closure analysis for DEL-03-06

Run Label: DEL-03-06
Date: 2026-02-21
Scope: Single deliverable (DEL-03-06)
Requested By: RECONCILIATION

This script reproduces the dependency closure analysis performed by
AUDIT_DEP_CLOSURE. It reads the Dependencies.csv for DEL-03-06, applies
the same filters and checks, and prints results to stdout.

Usage:
    python3 analyze_closure.py [--execution-root PATH]

Default execution root: execution/ (relative to repo root)
"""

import csv
import json
import os
import sys
import argparse
from collections import defaultdict
from pathlib import Path


# --- Configuration (matches the run parameters) ---

SCOPE = ["DEL-03-06"]
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


def normalize_id(raw_id):
    """Strip descriptive suffix from deliverable IDs if present."""
    if not raw_id:
        return raw_id
    # Match DEL-XX-YY or DEL-XXX-YY prefix
    import re
    m = re.match(r"(DEL-\d{2,3}-\d{2})", raw_id)
    if m:
        return m.group(1)
    # Match KTY-CC-TT prefix (domain, if encountered)
    m = re.match(r"(KTY-\d{2}-\d{2})", raw_id)
    if m:
        return m.group(1)
    return raw_id


def discover_deliverables(execution_root):
    """Discover all DEL-XX-YY folders in the execution root."""
    deliverables = {}
    import re
    for pkg_dir in sorted(Path(execution_root).iterdir()):
        if not pkg_dir.is_dir() or pkg_dir.name.startswith("_"):
            continue
        working_dir = pkg_dir / "1_Working"
        if not working_dir.is_dir():
            continue
        for del_dir in sorted(working_dir.iterdir()):
            if not del_dir.is_dir():
                continue
            m = re.match(r"(DEL-\d{2}-\d{2})", del_dir.name)
            if m:
                del_id = m.group(1)
                deliverables[del_id] = del_dir
    return deliverables


def read_dependencies_csv(csv_path):
    """Read and parse a Dependencies.csv file."""
    rows = []
    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        columns = reader.fieldnames or []
        for row in reader:
            rows.append(row)
    return columns, rows


def validate_schema(columns, expected_version="v3.1"):
    """Check that all required v3.1 columns are present."""
    missing = [c for c in REQUIRED_COLUMNS_V31 if c not in columns]
    return len(missing) == 0, missing


def filter_edges(rows):
    """Apply edge filter to extract graph edges."""
    edges = []
    for row in rows:
        if FILTER_ACTIVE_ONLY and row.get("Status", "") != "ACTIVE":
            continue
        if row.get("DependencyClass", "") != EDGE_FILTER_DEP_CLASS:
            continue
        if row.get("TargetType", "") != EDGE_FILTER_TARGET_TYPE:
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
                "dep_id": row.get("DependencyID", ""),
                "direction": row.get("Direction", ""),
                "dep_type": row.get("DependencyType", ""),
            })
    return edges


def check_orphans(edges, known_deliverables):
    """Check for orphan target references."""
    orphans = []
    for e in edges:
        if e["to"] not in known_deliverables:
            orphans.append(e)
    return orphans


def check_anchor_coverage(rows):
    """Check for at least one IMPLEMENTS_NODE anchor."""
    has_implements = any(
        r.get("DependencyClass") == "ANCHOR"
        and r.get("AnchorType") == "IMPLEMENTS_NODE"
        for r in rows
    )
    return has_implements


def check_misplaced_fields(rows):
    """Check for non-DELIVERABLE rows with populated TargetDeliverableID."""
    violations = []
    for row in rows:
        if (row.get("TargetType", "") != "DELIVERABLE"
                and row.get("TargetDeliverableID", "").strip()):
            violations.append(row)
    return violations


def check_id_format(rows):
    """Check for long-form IDs that needed normalization."""
    import re
    long_form_count = 0
    total_id_fields = 0
    for row in rows:
        for field in ["FromDeliverableID", "TargetDeliverableID"]:
            val = row.get(field, "").strip()
            if not val:
                continue
            total_id_fields += 1
            # Check if it has a suffix beyond DEL-XX-YY
            if re.match(r"DEL-\d{2,3}-\d{2}_.+", val):
                long_form_count += 1
    return long_form_count, total_id_fields


def tarjan_scc(graph):
    """Tarjan's SCC algorithm. graph = {node: [neighbors]}."""
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
            if len(scc) > 1:
                result.append(scc)

    for node in list(graph.keys()):
        if node not in index:
            strongconnect(node)

    return result


def main():
    parser = argparse.ArgumentParser(
        description="Reproducible dependency closure analysis for DEL-03-06"
    )
    parser.add_argument(
        "--execution-root",
        default="execution/",
        help="Path to execution root (default: execution/)",
    )
    args = parser.parse_args()

    execution_root = args.execution_root
    print(f"=== Dependency Closure Analysis: DEL-03-06 ===")
    print(f"Execution root: {execution_root}")
    print()

    # Step 0: Discover deliverables
    all_deliverables = discover_deliverables(execution_root)
    print(f"Workspace deliverables discovered: {len(all_deliverables)}")

    # Step 1: Locate Dependencies.csv for DEL-03-06
    target_del = "DEL-03-06"
    if target_del not in all_deliverables:
        print(f"FAILED: {target_del} not found in workspace")
        sys.exit(1)

    csv_path = all_deliverables[target_del] / "Dependencies.csv"
    if not csv_path.exists():
        print(f"FAILED: Dependencies.csv not found at {csv_path}")
        sys.exit(1)

    print(f"Dependencies.csv: {csv_path}")

    # Step 2: Parse and validate schema
    columns, rows = read_dependencies_csv(csv_path)
    schema_valid, missing_cols = validate_schema(columns)
    print(f"Schema valid: {schema_valid}")
    if not schema_valid:
        print(f"  Missing columns: {missing_cols}")
    print(f"Total rows: {len(rows)}")

    # Step 3: Build edges
    edges = filter_edges(rows)
    print(f"Graph edges (after filter): {len(edges)}")
    for e in edges:
        print(f"  {e['from']} -> {e['to']} [{e['dep_id']}] "
              f"({e['direction']}, {e['dep_type']})")
    print()

    # Step 4: Core checks
    print("--- Core Check Results ---")
    print()

    # Check 1: Schema compliance
    verdict_1 = "PASS" if schema_valid else "BLOCKER"
    print(f"1. Schema compliance: {verdict_1}")

    # Check 2: Orphan dependencies
    orphans = check_orphans(edges, all_deliverables)
    verdict_2 = "PASS" if len(orphans) == 0 else "WARNING"
    print(f"2. Orphan dependencies: {verdict_2} ({len(orphans)} orphans)")
    for o in orphans:
        print(f"   ORPHAN: {o['from']} -> {o['to']} [{o['dep_id']}]")

    # Check 3: Circular dependencies
    adj = defaultdict(list)
    for e in edges:
        adj[e["from"]].append(e["to"])
    # Ensure all targets are in adjacency list as keys
    for e in edges:
        if e["to"] not in adj:
            adj[e["to"]] = []
    sccs = tarjan_scc(dict(adj))
    verdict_3 = "PASS" if len(sccs) == 0 else "BLOCKER"
    print(f"3. Circular dependencies: {verdict_3} ({len(sccs)} non-trivial SCCs)")
    for i, scc in enumerate(sccs):
        print(f"   SCC {i+1}: {scc}")

    # Check 4: Anchor coverage
    has_anchor = check_anchor_coverage(rows)
    verdict_4 = "PASS" if has_anchor else "WARNING"
    print(f"4. Anchor coverage: {verdict_4}")

    # Check 5: Misplaced fields
    misplaced = check_misplaced_fields(rows)
    verdict_5 = "PASS" if len(misplaced) == 0 else "WARNING"
    print(f"5. Misplaced fields: {verdict_5} ({len(misplaced)} violations)")

    # Check 6: ID format consistency
    long_form, total_ids = check_id_format(rows)
    norm_rate = (long_form / total_ids * 100) if total_ids > 0 else 0.0
    verdict_6 = "PASS" if long_form == 0 else "WARNING"
    print(f"6. ID format consistency: {verdict_6} "
          f"({long_form}/{total_ids} long-form, {norm_rate:.1f}% normalization)")

    # Check 7: Isolated deliverables
    degree = len(edges)
    verdict_7 = "PASS" if degree > 0 else "WARNING"
    print(f"7. Isolated deliverables: {verdict_7} (degree={degree})")

    # Check 8: Hub analysis
    verdict_8 = "PASS" if degree < HUB_THRESHOLD else "WARNING"
    print(f"8. Hub analysis: {verdict_8} (degree={degree}, threshold={HUB_THRESHOLD})")

    # Check 9: Bidirectional pairs
    # Single-deliverable scope: cannot confirm, only suspect
    print(f"9. Bidirectional pairs: PASS (INFO) "
          f"(single-deliverable scope, cannot confirm)")
    print()

    # Overall
    all_verdicts = [verdict_1, verdict_2, verdict_3, verdict_4,
                    verdict_5, verdict_6, verdict_7, verdict_8]
    if "BLOCKER" in all_verdicts:
        overall = "BLOCKER"
    elif "WARNING" in all_verdicts:
        overall = "WARNINGS"
    else:
        overall = "PASS"
    print(f"=== Overall Closure Status: {overall} ===")


if __name__ == "__main__":
    main()
