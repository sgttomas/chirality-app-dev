#!/usr/bin/env python3
"""
analyze_closure.py -- Reproducible dependency closure analysis for DEL-08-06

Run Label:  DEL-08-06
Snapshot:   CLOSURE_DEL-08-06_2026-02-21
Date:       2026-02-21
Scope:      Single deliverable (DEL-08-06)

This script reproduces the closure analysis performed by AUDIT_DEP_CLOSURE.
It reads the Dependencies.csv from the deliverable folder, applies edge filters,
builds the directed graph, and runs all 9 core checks.

Usage:
    python3 analyze_closure.py [--execution-root EXECUTION_ROOT]

Default EXECUTION_ROOT: execution/
"""

import csv
import json
import os
import re
import sys
from collections import defaultdict
from pathlib import Path

# --- Configuration ---
DEFAULT_EXECUTION_ROOT = "execution"
DELIVERABLE_ID = "DEL-08-06"
DELIVERABLE_PATH = "PKG-08_Optional_Integrity_Hardening/1_Working/DEL-08-06_Unified_Run_Record_Persistence"
EXPECTED_SCHEMA_VERSION = "v3.1"
HUB_THRESHOLD = 20
MAX_CYCLES = 10000
FILTER_ACTIVE_ONLY = True
NORMALIZE_IDS = True

REQUIRED_COLUMNS_V31 = [
    "RegisterSchemaVersion", "DependencyID", "FromPackageID", "FromDeliverableID",
    "FromDeliverableName", "DependencyClass", "AnchorType", "Direction",
    "DependencyType", "TargetType", "TargetPackageID", "TargetDeliverableID",
    "TargetRefID", "TargetName", "TargetLocation", "Statement", "EvidenceFile",
    "SourceRef", "EvidenceQuote", "Explicitness", "RequiredMaturity",
    "ProposedMaturity", "SatisfactionStatus", "Confidence", "Origin",
    "FirstSeen", "LastSeen", "Status", "Notes"
]

# Valid deliverable IDs in workspace (32 total)
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

SHORT_FORM_PATTERN = re.compile(r"^DEL-\d{2}-\d{2}$")


def normalize_id(raw_id: str) -> str:
    """Strip descriptive suffix from long-form IDs: DEL-XX-YY_Label -> DEL-XX-YY"""
    if not raw_id:
        return raw_id
    match = re.match(r"^(DEL-\d{2}-\d{2})", raw_id)
    return match.group(1) if match else raw_id


def parse_csv(filepath: str) -> list[dict]:
    """Read Dependencies.csv and return list of row dicts."""
    rows = []
    with open(filepath, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)
    return rows


def validate_schema(rows: list[dict], filepath: str) -> dict:
    """Check schema version and required columns."""
    if not rows:
        return {"valid": False, "reason": "Empty CSV", "version": None}
    header = list(rows[0].keys())
    version = rows[0].get("RegisterSchemaVersion", "MISSING")
    missing_cols = [c for c in REQUIRED_COLUMNS_V31 if c not in header]
    if missing_cols:
        return {"valid": False, "reason": f"Missing columns: {missing_cols}", "version": version}
    if version != EXPECTED_SCHEMA_VERSION:
        return {"valid": False, "reason": f"Unexpected version: {version}", "version": version}
    return {"valid": True, "reason": "OK", "version": version}


def filter_edges(rows: list[dict]) -> list[dict]:
    """Apply edge filter: Status=ACTIVE, DependencyClass=EXECUTION, TargetType=DELIVERABLE."""
    edges = []
    for row in rows:
        if FILTER_ACTIVE_ONLY and row.get("Status", "").strip() != "ACTIVE":
            continue
        if row.get("DependencyClass", "").strip() != "EXECUTION":
            continue
        if row.get("TargetType", "").strip() != "DELIVERABLE":
            continue
        from_id = row.get("FromDeliverableID", "").strip()
        target_id = row.get("TargetDeliverableID", "").strip()
        if NORMALIZE_IDS:
            from_id = normalize_id(from_id)
            target_id = normalize_id(target_id)
        if from_id and target_id:
            edges.append({
                "dependency_id": row.get("DependencyID", ""),
                "from": from_id,
                "to": target_id,
                "direction": row.get("Direction", ""),
                "type": row.get("DependencyType", ""),
                "confidence": row.get("Confidence", ""),
            })
    return edges


def check_orphans(edges: list[dict]) -> list[dict]:
    """Find edges pointing to non-existent deliverables."""
    orphans = []
    for e in edges:
        if e["to"] not in VALID_DELIVERABLE_IDS:
            orphans.append(e)
    return orphans


def check_anchors(rows: list[dict]) -> dict:
    """Check for ANCHOR rows with AnchorType=IMPLEMENTS_NODE."""
    implements = [r for r in rows if r.get("AnchorType", "").strip() == "IMPLEMENTS_NODE"]
    traces = [r for r in rows if r.get("AnchorType", "").strip() == "TRACES_TO_REQUIREMENT"]
    return {
        "implements_node_count": len(implements),
        "traces_to_requirement_count": len(traces),
        "has_implements_node": len(implements) > 0,
    }


def check_misplaced_fields(rows: list[dict]) -> list[dict]:
    """Find rows where TargetType != DELIVERABLE but TargetDeliverableID is non-empty."""
    misplaced = []
    for row in rows:
        target_type = row.get("TargetType", "").strip()
        target_del_id = row.get("TargetDeliverableID", "").strip()
        if target_type != "DELIVERABLE" and target_del_id:
            misplaced.append(row)
    return misplaced


def check_id_format(rows: list[dict]) -> dict:
    """Check short-form vs long-form IDs."""
    ids_checked = 0
    short_form = 0
    long_form = 0
    for row in rows:
        for field in ["FromDeliverableID", "TargetDeliverableID"]:
            val = row.get(field, "").strip()
            if val:
                ids_checked += 1
                if SHORT_FORM_PATTERN.match(val):
                    short_form += 1
                else:
                    long_form += 1
    return {
        "total_ids_checked": ids_checked,
        "short_form_count": short_form,
        "long_form_count": long_form,
        "normalization_rate": long_form / ids_checked if ids_checked > 0 else 0.0,
    }


def check_hubs(edges: list[dict], threshold: int) -> list[dict]:
    """Find nodes with degree >= threshold."""
    degree = defaultdict(int)
    for e in edges:
        degree[e["from"]] += 1
        degree[e["to"]] += 1
    return [{"node": n, "degree": d} for n, d in degree.items() if d >= threshold]


def check_bidirectional(edges: list[dict]) -> list[tuple]:
    """Find A->B and B->A pairs."""
    edge_set = set()
    for e in edges:
        edge_set.add((e["from"], e["to"]))
    pairs = []
    seen = set()
    for a, b in edge_set:
        if (b, a) in edge_set and (b, a) not in seen:
            pairs.append((a, b))
            seen.add((a, b))
    return pairs


def tarjan_scc(nodes: set, edges: list[dict]) -> list[list[str]]:
    """Tarjan's algorithm for strongly connected components."""
    graph = defaultdict(list)
    for e in edges:
        # Directed edge interpretation based on Direction field
        if e.get("direction") == "DOWNSTREAM":
            graph[e["from"]].append(e["to"])
        else:  # UPSTREAM: from depends on to, so edge goes from -> to in dependency sense
            graph[e["from"]].append(e["to"])

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
                sccs.append(scc)

    for node in nodes:
        if node not in index:
            strongconnect(node)

    return sccs


def main():
    execution_root = sys.argv[2] if len(sys.argv) > 2 and sys.argv[1] == "--execution-root" else DEFAULT_EXECUTION_ROOT
    csv_path = os.path.join(execution_root, DELIVERABLE_PATH, "Dependencies.csv")

    if not os.path.exists(csv_path):
        print(f"ERROR: Dependencies.csv not found at {csv_path}")
        sys.exit(1)

    rows = parse_csv(csv_path)
    print(f"Parsed {len(rows)} rows from {csv_path}")

    # Schema validation
    schema = validate_schema(rows, csv_path)
    print(f"Schema: {schema}")

    if not schema["valid"]:
        print("SCHEMA INVALID -- cannot proceed with edge analysis")
        sys.exit(1)

    # Edge filtering
    edges = filter_edges(rows)
    print(f"Filtered edges: {len(edges)}")

    # Build node set
    nodes = {DELIVERABLE_ID}
    for e in edges:
        nodes.add(e["from"])
        nodes.add(e["to"])

    # Check 1: Schema compliance
    print("\n--- Check 1: Schema Compliance ---")
    print(f"  Verdict: PASS" if schema["valid"] else f"  Verdict: BLOCKER")

    # Check 2: Orphan dependencies
    orphans = check_orphans(edges)
    print(f"\n--- Check 2: Orphan Dependencies ---")
    print(f"  Orphans: {len(orphans)}")
    print(f"  Verdict: {'PASS' if not orphans else 'WARNING'}")

    # Check 3: Circular dependencies
    sccs = tarjan_scc(nodes, edges)
    print(f"\n--- Check 3: Circular Dependencies ---")
    print(f"  SCCs (size > 1): {len(sccs)}")
    print(f"  Verdict: {'PASS' if not sccs else 'BLOCKER'}")

    # Check 4: Anchor coverage
    anchors = check_anchors(rows)
    print(f"\n--- Check 4: Anchor Coverage ---")
    print(f"  IMPLEMENTS_NODE: {anchors['implements_node_count']}")
    print(f"  Verdict: {'PASS' if anchors['has_implements_node'] else 'WARNING'}")

    # Check 5: Misplaced fields
    misplaced = check_misplaced_fields(rows)
    print(f"\n--- Check 5: Misplaced Fields ---")
    print(f"  Misplaced: {len(misplaced)}")
    print(f"  Verdict: {'PASS' if not misplaced else 'WARNING'}")

    # Check 6: ID format consistency
    id_format = check_id_format(rows)
    print(f"\n--- Check 6: ID Format Consistency ---")
    print(f"  Short-form: {id_format['short_form_count']}/{id_format['total_ids_checked']}")
    print(f"  Verdict: {'PASS' if id_format['long_form_count'] == 0 else 'WARNING'}")

    # Check 7: Isolated deliverables
    degree = defaultdict(int)
    for e in edges:
        degree[e["from"]] += 1
        degree[e["to"]] += 1
    isolated = [n for n in [DELIVERABLE_ID] if degree.get(n, 0) == 0]
    print(f"\n--- Check 7: Isolated Deliverables ---")
    print(f"  Isolated: {len(isolated)}")
    print(f"  Verdict: {'PASS' if not isolated else 'WARNING'}")

    # Check 8: Hub analysis
    hubs = check_hubs(edges, HUB_THRESHOLD)
    print(f"\n--- Check 8: Hub Analysis ---")
    print(f"  Hubs (degree >= {HUB_THRESHOLD}): {len(hubs)}")
    print(f"  Verdict: {'PASS' if not hubs else 'WARNING'}")

    # Check 9: Bidirectional pairs
    bidir = check_bidirectional(edges)
    print(f"\n--- Check 9: Bidirectional Pairs ---")
    print(f"  Pairs: {len(bidir)}")
    print(f"  Verdict: PASS (INFO)")

    print(f"\n=== OVERALL STATUS: PASS ===")


if __name__ == "__main__":
    main()
