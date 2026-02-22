#!/usr/bin/env python3
"""
Dependency Closure Analysis Script
Run ID: CLOSURE_DEL-06-05_2026-02-21
Scope: DEL-06-05

Reproduces the closure analysis performed by AUDIT_DEP_CLOSURE.
Usage: python3 analyze_closure.py [--execution-root PATH]

Default execution root: execution/
"""

import csv
import json
import os
import sys
from collections import defaultdict
from pathlib import Path

# --- Configuration ---
RUN_LABEL = "DEL-06-05"
SCOPE = ["DEL-06-05"]
FILTER_ACTIVE_ONLY = True
NORMALIZE_IDS = True
EDGE_FILTER_DEPENDENCY_CLASS = "EXECUTION"
EDGE_FILTER_TARGET_TYPE = "DELIVERABLE"
HUB_THRESHOLD = 20
MAX_CYCLES = 10000

# All 32 known deliverable IDs in the workspace
KNOWN_DELIVERABLE_IDS = [
    "DEL-01-01", "DEL-01-02",
    "DEL-02-01", "DEL-02-02", "DEL-02-03", "DEL-02-04",
    "DEL-03-01", "DEL-03-02", "DEL-03-03", "DEL-03-04", "DEL-03-05", "DEL-03-06",
    "DEL-04-01", "DEL-04-02",
    "DEL-05-01", "DEL-05-02", "DEL-05-03", "DEL-05-04",
    "DEL-06-01", "DEL-06-02", "DEL-06-03", "DEL-06-04", "DEL-06-05",
    "DEL-07-01", "DEL-07-02",
    "DEL-08-01", "DEL-08-02", "DEL-08-03", "DEL-08-04", "DEL-08-05", "DEL-08-06", "DEL-08-07",
]

# Deliverable paths (scope)
DELIVERABLE_PATHS = {
    "DEL-06-05": "PKG-06_Agent_Suite_Governance/1_Working/DEL-06-05_Governance_Coherence_Guardrails",
}


def normalize_id(raw_id: str) -> str:
    """Strip descriptive suffix from deliverable ID if NORMALIZE_IDS is True."""
    if not NORMALIZE_IDS or not raw_id:
        return raw_id
    # Match DEL-XX-YY or KTY-CC-TT prefix patterns
    import re
    match = re.match(r"^(DEL-\d{2}-\d{2}|KTY-\d{2}-\d{2})", raw_id)
    if match:
        return match.group(1)
    return raw_id


def parse_dependencies_csv(filepath: str) -> list[dict]:
    """Parse a Dependencies.csv file and return list of row dicts."""
    rows = []
    with open(filepath, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)
    return rows


def validate_schema(rows: list[dict], filepath: str) -> dict:
    """Validate schema version and required columns."""
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
        return {"valid": False, "error": "Empty CSV", "filepath": filepath}

    actual_columns = list(rows[0].keys())
    missing = [c for c in expected_columns if c not in actual_columns]
    schema_version = rows[0].get("RegisterSchemaVersion", "UNKNOWN")

    return {
        "valid": len(missing) == 0,
        "schema_version": schema_version,
        "expected_columns": len(expected_columns),
        "actual_columns": len(actual_columns),
        "missing_columns": missing,
        "filepath": filepath,
    }


def build_graph(rows: list[dict]) -> tuple[set, list[dict]]:
    """Build node set and edge list from qualifying rows."""
    nodes = set()
    edges = []

    for row in rows:
        from_id = normalize_id(row.get("FromDeliverableID", ""))
        if from_id:
            nodes.add(from_id)

        # Apply filters
        if FILTER_ACTIVE_ONLY and row.get("Status", "") != "ACTIVE":
            continue
        if row.get("DependencyClass", "") != EDGE_FILTER_DEPENDENCY_CLASS:
            continue
        if row.get("TargetType", "") != EDGE_FILTER_TARGET_TYPE:
            continue

        target_id = normalize_id(row.get("TargetDeliverableID", ""))
        if not from_id or not target_id:
            continue

        nodes.add(target_id)
        edges.append({
            "from": from_id,
            "to": target_id,
            "dependency_id": row.get("DependencyID", ""),
            "direction": row.get("Direction", ""),
            "dependency_type": row.get("DependencyType", ""),
        })

    return nodes, edges


def tarjan_scc(nodes: set, edges: list[dict]) -> list[list[str]]:
    """Find strongly connected components using Tarjan's algorithm."""
    graph = defaultdict(list)
    for edge in edges:
        graph[edge["from"]].append(edge["to"])

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
            sccs.append(scc)

    for node in sorted(nodes):
        if node not in index:
            strongconnect(node)

    return sccs


def check_orphans(edges: list[dict]) -> list[dict]:
    """Check for target deliverable IDs not in the known workspace."""
    orphans = []
    for edge in edges:
        if edge["to"] not in KNOWN_DELIVERABLE_IDS:
            orphans.append(edge)
    return orphans


def check_anchors(rows: list[dict]) -> dict:
    """Check anchor coverage per deliverable."""
    anchors = defaultdict(list)
    for row in rows:
        if row.get("DependencyClass") == "ANCHOR":
            from_id = normalize_id(row.get("FromDeliverableID", ""))
            anchor_type = row.get("AnchorType", "")
            anchors[from_id].append(anchor_type)

    results = {}
    for del_id in SCOPE:
        types = anchors.get(del_id, [])
        has_implements = "IMPLEMENTS_NODE" in types
        results[del_id] = {
            "total_anchors": len(types),
            "has_implements_node": has_implements,
            "anchor_types": types,
        }
    return results


def check_misplaced_fields(rows: list[dict]) -> list[dict]:
    """Check rows where TargetType != DELIVERABLE but TargetDeliverableID is non-empty."""
    violations = []
    for row in rows:
        target_type = row.get("TargetType", "")
        target_del_id = row.get("TargetDeliverableID", "").strip()
        if target_type != "DELIVERABLE" and target_del_id:
            violations.append(row)
    return violations


def check_id_format(rows: list[dict]) -> dict:
    """Check ID format consistency."""
    import re
    from_ids = set()
    target_ids = set()
    long_form = []

    for row in rows:
        fid = row.get("FromDeliverableID", "").strip()
        tid = row.get("TargetDeliverableID", "").strip()
        if fid:
            from_ids.add(fid)
            if not re.match(r"^DEL-\d{2}-\d{2}$", fid):
                long_form.append(("FromDeliverableID", fid, row.get("DependencyID", "")))
        if tid:
            target_ids.add(tid)
            if not re.match(r"^DEL-\d{2}-\d{2}$", tid):
                long_form.append(("TargetDeliverableID", tid, row.get("DependencyID", "")))

    return {
        "unique_from_ids": len(from_ids),
        "unique_target_ids": len(target_ids),
        "long_form_count": len(long_form),
        "long_form_details": long_form,
    }


def check_bidirectional(edges: list[dict]) -> list[tuple]:
    """Check for bidirectional pairs (A->B and B->A)."""
    edge_set = set()
    for edge in edges:
        edge_set.add((edge["from"], edge["to"]))

    pairs = []
    seen = set()
    for a, b in edge_set:
        if (b, a) in edge_set and (b, a) not in seen:
            pairs.append((a, b))
            seen.add((a, b))
    return pairs


def main():
    execution_root = sys.argv[2] if len(sys.argv) > 2 and sys.argv[1] == "--execution-root" else "execution"
    execution_root = Path(execution_root)

    print(f"=== Dependency Closure Analysis: {RUN_LABEL} ===")
    print(f"Execution root: {execution_root}")
    print(f"Scope: {SCOPE}")
    print()

    # Step 1: Locate and parse
    all_rows = []
    for del_id, rel_path in DELIVERABLE_PATHS.items():
        csv_path = execution_root / rel_path / "Dependencies.csv"
        if not csv_path.exists():
            print(f"  MISSING: {csv_path}")
            continue
        rows = parse_dependencies_csv(str(csv_path))
        print(f"  Parsed {csv_path}: {len(rows)} rows")

        # Step 2: Validate schema
        schema_result = validate_schema(rows, str(csv_path))
        print(f"  Schema valid: {schema_result['valid']} (v{schema_result['schema_version']})")
        if not schema_result["valid"]:
            print(f"  Missing columns: {schema_result['missing_columns']}")
            continue
        all_rows.extend(rows)

    if not all_rows:
        print("ERROR: No valid rows found. Exiting.")
        sys.exit(1)

    # Step 3: Build graph
    nodes, edges = build_graph(all_rows)
    print(f"\nGraph: {len(nodes)} nodes, {len(edges)} edges")
    for e in edges:
        print(f"  {e['from']} --> {e['to']} ({e['dependency_id']})")

    # Step 4: Core checks
    print("\n--- Core Checks ---")

    # Check 1: Schema compliance
    print("\n1. Schema Compliance: PASS")

    # Check 2: Orphan dependencies
    orphans = check_orphans(edges)
    verdict = "PASS" if not orphans else "WARNING"
    print(f"2. Orphan Dependencies: {verdict} ({len(orphans)} orphans)")

    # Check 3: Circular dependencies
    sccs = tarjan_scc(nodes, edges)
    nontrivial = [s for s in sccs if len(s) > 1]
    verdict = "PASS" if not nontrivial else "BLOCKER"
    print(f"3. Circular Dependencies: {verdict} ({len(nontrivial)} non-trivial SCCs)")

    # Check 4: Anchor coverage
    anchor_results = check_anchors(all_rows)
    all_have_implements = all(v["has_implements_node"] for v in anchor_results.values())
    verdict = "PASS" if all_have_implements else "WARNING"
    print(f"4. Anchor Coverage: {verdict}")

    # Check 5: Misplaced fields
    misplaced = check_misplaced_fields(all_rows)
    verdict = "PASS" if not misplaced else "WARNING"
    print(f"5. Misplaced Fields: {verdict} ({len(misplaced)} violations)")

    # Check 6: ID format consistency
    id_result = check_id_format(all_rows)
    verdict = "PASS" if id_result["long_form_count"] == 0 else "WARNING"
    print(f"6. ID Format Consistency: {verdict} ({id_result['long_form_count']} long-form IDs)")

    # Check 7: Isolated deliverables
    connected = set()
    for e in edges:
        connected.add(e["from"])
        connected.add(e["to"])
    isolated = [d for d in SCOPE if d not in connected]
    verdict = "PASS" if not isolated else "WARNING"
    print(f"7. Isolated Deliverables: {verdict} ({len(isolated)} isolated)")

    # Check 8: Hub analysis
    degree = defaultdict(int)
    for e in edges:
        degree[e["from"]] += 1
        degree[e["to"]] += 1
    hubs = {k: v for k, v in degree.items() if v >= HUB_THRESHOLD}
    verdict = "PASS" if not hubs else "WARNING"
    print(f"8. Hub Analysis: {verdict} ({len(hubs)} hubs)")

    # Check 9: Bidirectional pairs
    bidir = check_bidirectional(edges)
    verdict = "PASS" if not bidir else "INFO"
    print(f"9. Bidirectional Pairs: {verdict} ({len(bidir)} pairs)")

    print("\n=== Analysis Complete ===")


if __name__ == "__main__":
    main()
