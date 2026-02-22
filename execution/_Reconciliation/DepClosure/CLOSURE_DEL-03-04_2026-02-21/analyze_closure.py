#!/usr/bin/env python3
"""
analyze_closure.py -- Reproducible dependency closure analysis for DEL-03-04

Run Label: DEL-03-04
Snapshot: CLOSURE_DEL-03-04_2026-02-21
Generated: 2026-02-21
Agent: AUDIT_DEP_CLOSURE (Type 2)

Usage:
    python3 analyze_closure.py [--execution-root PATH]

This script reproduces the closure analysis performed by the AUDIT_DEP_CLOSURE
agent. It reads Dependencies.csv from the deliverable folder, applies the same
filters and checks, and prints results to stdout.
"""

import csv
import json
import os
import sys
from collections import defaultdict
from pathlib import Path

# --- Configuration (matches the run brief) ---
RUN_LABEL = "DEL-03-04"
SCOPE = ["DEL-03-04"]
FILTER_ACTIVE_ONLY = True
NORMALIZE_IDS = True
EDGE_FILTER_DEP_CLASS = "EXECUTION"
EDGE_FILTER_TARGET_TYPE = "DELIVERABLE"
HUB_THRESHOLD = 20
MAX_CYCLES = 10000

# All 32 valid workspace deliverable IDs
WORKSPACE_DELIVERABLES = [
    "DEL-01-01", "DEL-01-02",
    "DEL-02-01", "DEL-02-02", "DEL-02-03", "DEL-02-04",
    "DEL-03-01", "DEL-03-02", "DEL-03-03", "DEL-03-04", "DEL-03-05", "DEL-03-06",
    "DEL-04-01", "DEL-04-02",
    "DEL-05-01", "DEL-05-02", "DEL-05-03", "DEL-05-04",
    "DEL-06-01", "DEL-06-02", "DEL-06-03", "DEL-06-04", "DEL-06-05",
    "DEL-07-01", "DEL-07-02",
    "DEL-08-01", "DEL-08-02", "DEL-08-03", "DEL-08-04", "DEL-08-05", "DEL-08-06", "DEL-08-07",
]

# Deliverable path mapping
DELIVERABLE_PATHS = {
    "DEL-03-04": "PKG-03_Harness_Runtime_Core/1_Working/DEL-03-04_Subagent_Governance_FailClosed",
}

# Expected v3.1 columns
EXPECTED_COLUMNS_V31 = [
    "RegisterSchemaVersion", "DependencyID", "FromPackageID", "FromDeliverableID",
    "FromDeliverableName", "DependencyClass", "AnchorType", "Direction",
    "DependencyType", "TargetType", "TargetPackageID", "TargetDeliverableID",
    "TargetRefID", "TargetName", "TargetLocation", "Statement", "EvidenceFile",
    "SourceRef", "EvidenceQuote", "Explicitness", "RequiredMaturity",
    "ProposedMaturity", "SatisfactionStatus", "Confidence", "Origin",
    "FirstSeen", "LastSeen", "Status", "Notes",
]


def normalize_id(raw_id):
    """Strip descriptive suffix from DEL-XX-YY_Description format."""
    if not raw_id:
        return raw_id
    import re
    m = re.match(r"^(DEL-\d{2}-\d{2})", raw_id)
    if m:
        return m.group(1)
    m = re.match(r"^(KTY-\d{2}-\d{2})", raw_id)
    if m:
        return m.group(1)
    return raw_id


def tarjan_scc(graph):
    """Tarjan's strongly connected components algorithm."""
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
        on_stack[v] = True
        stack.append(v)

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

    for v in graph:
        if v not in index:
            strongconnect(v)

    return sccs


def main():
    # Resolve execution root
    exec_root = Path(sys.argv[2]) if len(sys.argv) > 2 and sys.argv[1] == "--execution-root" else Path("execution")
    if not exec_root.is_dir():
        print(f"ERROR: Execution root not found: {exec_root}")
        sys.exit(1)

    results = {
        "run_label": RUN_LABEL,
        "checks": {},
        "edges": [],
        "issues": [],
    }

    # --- Step 1: Locate and read Dependencies.csv ---
    for del_id in SCOPE:
        rel_path = DELIVERABLE_PATHS.get(del_id)
        if not rel_path:
            print(f"WARNING: No path mapping for {del_id}")
            continue

        csv_path = exec_root / rel_path / "Dependencies.csv"
        if not csv_path.is_file():
            print(f"MISSING: {csv_path}")
            continue

        print(f"Reading: {csv_path}")

        with open(csv_path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            headers = reader.fieldnames or []

            # --- Step 2: Schema validation ---
            missing_cols = [c for c in EXPECTED_COLUMNS_V31 if c not in headers]
            if missing_cols:
                print(f"SCHEMA_INVALID: Missing columns: {missing_cols}")
                results["checks"]["schema_compliance"] = {"verdict": "BLOCKER", "missing": missing_cols}
                continue

            results["checks"]["schema_compliance"] = {"verdict": "PASS", "columns": len(headers)}

            rows = list(reader)
            print(f"  Rows: {len(rows)}")

            # --- Step 3: Build edges ---
            edges = []
            anchor_rows = []
            misplaced = []
            ids_checked = []

            for row in rows:
                # Filter active only
                if FILTER_ACTIVE_ONLY and row.get("Status", "").strip() != "ACTIVE":
                    continue

                dep_class = row.get("DependencyClass", "").strip()
                target_type = row.get("TargetType", "").strip()
                from_id = row.get("FromDeliverableID", "").strip()
                target_id = row.get("TargetDeliverableID", "").strip()
                dep_id = row.get("DependencyID", "").strip()

                # Normalize IDs
                if NORMALIZE_IDS:
                    from_id = normalize_id(from_id)
                    target_id = normalize_id(target_id) if target_id else target_id

                # Track IDs for format check
                if from_id:
                    ids_checked.append(from_id)
                if target_id:
                    ids_checked.append(target_id)

                # Check anchors
                if dep_class == "ANCHOR":
                    anchor_rows.append(row)
                    continue

                # Check misplaced fields
                if target_type != "DELIVERABLE" and target_id:
                    misplaced.append({"dep_id": dep_id, "target_type": target_type, "target_del_id": target_id})

                # Edge filter
                if dep_class == EDGE_FILTER_DEP_CLASS and target_type == EDGE_FILTER_TARGET_TYPE:
                    if from_id and target_id:
                        edges.append({
                            "dep_id": dep_id,
                            "from": from_id,
                            "to": target_id,
                            "direction": row.get("Direction", "").strip(),
                            "dep_type": row.get("DependencyType", "").strip(),
                        })

            results["edges"] = edges
            print(f"  Edges (EXECUTION+DELIVERABLE): {len(edges)}")

            # --- Step 4: Core checks ---

            # Check 2: Orphans
            orphans = [e for e in edges if e["to"] not in WORKSPACE_DELIVERABLES]
            results["checks"]["orphan_dependencies"] = {
                "verdict": "BLOCKER" if orphans else "PASS",
                "orphans": [{"dep_id": o["dep_id"], "target": o["to"]} for o in orphans],
            }

            # Check 3: Cycles (Tarjan SCC)
            graph = defaultdict(list)
            for e in edges:
                graph[e["from"]].append(e["to"])
            # Ensure all nodes are in the graph
            for e in edges:
                if e["to"] not in graph:
                    graph[e["to"]] = []

            sccs = tarjan_scc(dict(graph))
            results["checks"]["circular_dependencies"] = {
                "verdict": "BLOCKER" if sccs else "PASS",
                "sccs": sccs[:MAX_CYCLES],
            }

            # Check 4: Anchor coverage
            implements_node = [a for a in anchor_rows if a.get("AnchorType", "").strip() == "IMPLEMENTS_NODE"]
            results["checks"]["anchor_coverage"] = {
                "verdict": "PASS" if implements_node else "WARNING",
                "implements_node_count": len(implements_node),
                "total_anchors": len(anchor_rows),
            }

            # Check 5: Misplaced fields
            results["checks"]["misplaced_fields"] = {
                "verdict": "WARNING" if misplaced else "PASS",
                "violations": misplaced,
            }

            # Check 6: ID format consistency
            import re
            long_form = [i for i in ids_checked if not re.match(r"^(DEL|KTY)-\d{2}-\d{2}$", i)]
            results["checks"]["id_format_consistency"] = {
                "verdict": "PASS",
                "total_ids": len(ids_checked),
                "long_form_ids": long_form,
                "normalization_rate": len(long_form) / max(len(ids_checked), 1),
            }

            # Check 7: Isolated deliverables
            is_isolated = len(edges) == 0
            results["checks"]["isolated_deliverables"] = {
                "verdict": "WARNING" if is_isolated else "PASS",
                "isolated": is_isolated,
                "degree": len(edges),
            }

            # Check 8: Hub analysis
            degree = len(edges)
            is_hub = degree >= HUB_THRESHOLD
            results["checks"]["hub_analysis"] = {
                "verdict": "WARNING" if is_hub else "PASS",
                "degree": degree,
                "threshold": HUB_THRESHOLD,
                "is_hub": is_hub,
            }

            # Check 9: Bidirectional pairs
            edge_set = {(e["from"], e["to"]) for e in edges}
            bidir = [(a, b) for (a, b) in edge_set if (b, a) in edge_set and a < b]
            results["checks"]["bidirectional_pairs"] = {
                "verdict": "PASS",
                "pairs": bidir,
            }

    # --- Output ---
    print("\n=== CLOSURE ANALYSIS RESULTS ===")
    print(f"Run Label: {results['run_label']}")
    print(f"Edges: {len(results['edges'])}")
    print(f"Issues: {len(results['issues'])}")
    print("\nCheck Verdicts:")
    for check, data in results["checks"].items():
        print(f"  {check}: {data['verdict']}")

    overall = "PASS"
    for data in results["checks"].values():
        if data["verdict"] == "BLOCKER":
            overall = "BLOCKER"
            break
        if data["verdict"] == "WARNING" and overall == "PASS":
            overall = "WARNING"

    print(f"\nOverall Verdict: {overall}")
    return 0 if overall == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
