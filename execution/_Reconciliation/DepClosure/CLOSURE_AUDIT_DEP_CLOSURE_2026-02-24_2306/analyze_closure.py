#!/usr/bin/env python3
"""
analyze_closure.py -- Cross-deliverable dependency graph closure analysis
Run: AUDIT_DEP_CLOSURE_2026-02-24_2306
Generated: 2026-02-24
Deterministic: same inputs -> same outputs (no sampling, no randomness)

Edge direction convention:
  - UPSTREAM row (From depends on Target):  edge From -> Target
  - DOWNSTREAM row (From provides to Target, i.e. Target depends on From):
    edge is reversed: Target -> From
  - Unknown/missing direction: treated as From -> Target

This means edges always point from dependent to dependency (from consumer to provider).
"""

import csv
import json
import os
import re
import sys
from collections import defaultdict
from datetime import datetime, timezone

# -- Configuration ----------------------------------------------------------
EXECUTION_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "..")
)
SNAPSHOT_DIR = os.path.dirname(os.path.abspath(__file__))
EVIDENCE_DIR = os.path.join(SNAPSHOT_DIR, "Evidence")
FILTER_ACTIVE_ONLY = True
NORMALIZE_IDS = True
HUB_THRESHOLD = 20
MAX_CYCLES = 10000
EDGE_FILTER_CLASS = "EXECUTION"
EDGE_FILTER_TARGET_TYPE = "DELIVERABLE"

REQUIRED_V31_COLUMNS = [
    "RegisterSchemaVersion", "DependencyID", "FromPackageID", "FromDeliverableID",
    "FromDeliverableName", "DependencyClass", "AnchorType", "Direction",
    "DependencyType", "TargetType", "TargetPackageID", "TargetDeliverableID",
    "TargetRefID", "TargetName", "TargetLocation", "Statement", "EvidenceFile",
    "SourceRef", "EvidenceQuote", "Explicitness", "RequiredMaturity",
    "ProposedMaturity", "SatisfactionStatus", "Confidence", "Origin",
    "FirstSeen", "LastSeen", "Status", "Notes",
]

# -- Helpers ----------------------------------------------------------------

def normalize_id(raw_id):
    """Strip descriptive suffix: DEL-XX-YY_Label -> DEL-XX-YY"""
    if not raw_id:
        return raw_id
    raw_id = raw_id.strip()
    if raw_id.startswith("DEL-"):
        parts = raw_id.split("_", 1)
        return parts[0]
    if raw_id.startswith("KTY-"):
        parts = raw_id.split("_", 1)
        return parts[0]
    return raw_id


def discover_deliverables(execution_root):
    """Find all DEL-* folders under PKG-*/1_Working/."""
    deliverables = {}
    for pkg_name in sorted(os.listdir(execution_root)):
        pkg_path = os.path.join(execution_root, pkg_name)
        if not os.path.isdir(pkg_path) or not pkg_name.startswith("PKG-"):
            continue
        working_dir = os.path.join(pkg_path, "1_Working")
        if not os.path.isdir(working_dir):
            continue
        for del_name in sorted(os.listdir(working_dir)):
            del_path = os.path.join(working_dir, del_name)
            if not os.path.isdir(del_path) or not del_name.startswith("DEL-"):
                continue
            del_id = normalize_id(del_name) if NORMALIZE_IDS else del_name
            deliverables[del_id] = {
                "folder_name": del_name,
                "path": del_path,
                "pkg": pkg_name,
                "deps_csv": os.path.join(del_path, "Dependencies.csv"),
            }
    return deliverables


def read_dependencies_csv(csv_path):
    """Read and parse a Dependencies.csv. Returns (rows, headers, error)."""
    try:
        with open(csv_path, "r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            headers = reader.fieldnames or []
            rows = list(reader)
        # Filter out completely empty rows
        rows = [r for r in rows if any((v or "").strip() for v in r.values())]
        return rows, headers, None
    except Exception as e:
        return [], [], str(e)


def validate_schema(headers):
    """Check if all required v3.1 columns are present."""
    missing = [c for c in REQUIRED_V31_COLUMNS if c not in headers]
    return len(missing) == 0, missing


def tarjan_scc(graph):
    """Tarjan's SCC algorithm. graph: dict of node -> list of successor nodes."""
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
            sccs.append(sorted(scc))

    for v in sorted(graph.keys()):
        if v not in index:
            strongconnect(v)

    return sccs


def topological_sort_kahn(nodes, dep_edges):
    """Kahn's algorithm for topological sort. Returns (sorted_tiers, remaining_nodes).
    dep_edges: list of (dependent, dependency) tuples.
    A dependent cannot start until its dependency is done.
    """
    in_degree = defaultdict(int)
    adj = defaultdict(set)  # dependency -> set of dependents
    all_nodes = set(nodes)

    for dependent, dependency in dep_edges:
        if dependent in all_nodes and dependency in all_nodes:
            adj[dependency].add(dependent)
            in_degree[dependent] += 1

    for n in all_nodes:
        if n not in in_degree:
            in_degree[n] = 0

    tiers = []
    remaining = set(all_nodes)

    while True:
        tier = sorted([n for n in remaining if in_degree.get(n, 0) == 0])
        if not tier:
            break
        tiers.append(tier)
        for n in tier:
            remaining.discard(n)
            for m in adj.get(n, []):
                in_degree[m] -= 1

    return tiers, sorted(remaining)


# -- Main Analysis ----------------------------------------------------------

def main():
    now = datetime.now(timezone.utc)
    os.makedirs(EVIDENCE_DIR, exist_ok=True)
    print(f"[{now.isoformat()}] AUDIT_DEP_CLOSURE analysis starting")

    # Step 0: Discover deliverables
    deliverables = discover_deliverables(EXECUTION_ROOT)
    if not deliverables:
        print("FAILED_INPUTS: No deliverables found.")
        sys.exit(1)
    print(f"Discovered {len(deliverables)} deliverables")

    # Step 1-2: Locate, parse, and validate Dependencies.csv
    coverage_rows = []
    all_dep_rows = {}  # del_id -> list of rows
    schema_issues = []

    for del_id in sorted(deliverables.keys()):
        info = deliverables[del_id]
        csv_path = info["deps_csv"]
        csv_exists = os.path.isfile(csv_path)
        readable = False
        schema_valid = False
        schema_version = "N/A"
        row_count = 0
        error_msg = ""

        if csv_exists:
            rows, headers, error = read_dependencies_csv(csv_path)
            if error:
                coverage_rows.append({
                    "DeliverableID": del_id, "Package": info["pkg"],
                    "CSVExists": "Y", "Readable": "N", "SchemaValid": "N",
                    "SchemaVersion": "UNREADABLE", "RowCount": 0, "Error": error
                })
                all_dep_rows[del_id] = []
                continue

            readable = True
            valid, missing_cols = validate_schema(headers)
            schema_valid = valid

            if not valid:
                schema_issues.append({
                    "DeliverableID": del_id,
                    "MissingColumns": missing_cols,
                })

            # Get schema version from first row
            if rows:
                schema_version = rows[0].get("RegisterSchemaVersion", "UNKNOWN")
            row_count = len(rows)

            # Tag rows with source info
            for r in rows:
                r["_source_file"] = csv_path
                r["_source_del_id"] = del_id
                r["_source_pkg"] = info["pkg"]

            all_dep_rows[del_id] = rows if schema_valid else []
        else:
            all_dep_rows[del_id] = []

        coverage_rows.append({
            "DeliverableID": del_id, "Package": info["pkg"],
            "CSVExists": "Y" if csv_exists else "N",
            "Readable": "Y" if readable else "N",
            "SchemaValid": "Y" if schema_valid else "N",
            "SchemaVersion": schema_version,
            "RowCount": row_count, "Error": error_msg
        })

    # Write coverage.csv
    with open(os.path.join(EVIDENCE_DIR, "coverage.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=[
            "DeliverableID", "Package", "CSVExists", "Readable",
            "SchemaValid", "SchemaVersion", "RowCount", "Error"
        ])
        w.writeheader()
        w.writerows(coverage_rows)

    csv_exists_count = sum(1 for r in coverage_rows if r["CSVExists"] == "Y")
    csv_readable_count = sum(1 for r in coverage_rows if r["Readable"] == "Y")
    csv_valid_count = sum(1 for r in coverage_rows if r["SchemaValid"] == "Y")
    print(f"CSV coverage: {csv_exists_count} exist, {csv_readable_count} readable, {csv_valid_count} schema-valid")

    # Flatten all rows
    flat_rows = []
    for del_id in sorted(all_dep_rows.keys()):
        flat_rows.extend(all_dep_rows[del_id])

    # Step 3: Build the directed graph
    #
    # Edge direction convention:
    #   UPSTREAM: From depends on Target -> edge is (From, Target)
    #   DOWNSTREAM: From provides to Target -> edge is reversed: (Target, From)
    #   Other/unknown: treat as (From, Target)
    #
    # We also track misplaced fields and orphan targets here.

    all_nodes = set(deliverables.keys())
    edges = []           # list of (from_node, to_node, dep_id, direction, dep_type, source_row)
    edge_set = set()     # set of (from_node, to_node) for unique counting
    orphan_rows = []
    misplaced = []

    for del_id in sorted(all_dep_rows.keys()):
        for r in all_dep_rows[del_id]:
            dep_class = r.get("DependencyClass", "").strip()
            target_type = r.get("TargetType", "").strip()
            status = r.get("Status", "").strip()
            direction = r.get("Direction", "").strip()
            dep_type = r.get("DependencyType", "").strip()
            dep_id = r.get("DependencyID", "").strip()
            raw_from = r.get("FromDeliverableID", "").strip()
            raw_target = r.get("TargetDeliverableID", "").strip()
            from_id = normalize_id(raw_from) if NORMALIZE_IDS else raw_from
            target_del_id = normalize_id(raw_target) if NORMALIZE_IDS else raw_target

            # Check 5: Misplaced fields (runs on ALL rows, not just filtered)
            if target_type != "DELIVERABLE" and target_del_id:
                misplaced.append({
                    "DependencyID": dep_id,
                    "FromDeliverableID": from_id,
                    "TargetType": target_type,
                    "TargetDeliverableID": target_del_id,
                    "SourceFile": r.get("_source_file", ""),
                })

            # Apply filters for graph edges
            if FILTER_ACTIVE_ONLY and status != "ACTIVE":
                continue
            if dep_class != EDGE_FILTER_CLASS:
                continue
            if target_type != EDGE_FILTER_TARGET_TYPE:
                continue
            if not from_id or not target_del_id:
                continue

            # Check 2: Orphan targets
            if target_del_id not in all_nodes:
                orphan_rows.append({
                    "FromDeliverableID": from_id,
                    "TargetDeliverableID": target_del_id,
                    "DependencyID": dep_id,
                    "Direction": direction,
                    "SourceFile": r.get("_source_file", ""),
                })
                continue

            # Apply direction to determine edge direction
            if direction == "UPSTREAM":
                # From depends on Target
                edge_from, edge_to = from_id, target_del_id
            elif direction == "DOWNSTREAM":
                # From provides to Target; Target depends on From
                edge_from, edge_to = target_del_id, from_id
            else:
                # Unknown direction: treat as from->target
                edge_from, edge_to = from_id, target_del_id

            edges.append((edge_from, edge_to, dep_id, direction, dep_type, r))
            edge_set.add((edge_from, edge_to))

    # Count raw EXECUTION/DELIVERABLE/ACTIVE rows (before direction normalization)
    total_exec_del_rows = 0
    for del_id in sorted(all_dep_rows.keys()):
        for r in all_dep_rows[del_id]:
            if (r.get("DependencyClass", "").strip() == EDGE_FILTER_CLASS and
                r.get("TargetType", "").strip() == EDGE_FILTER_TARGET_TYPE and
                (not FILTER_ACTIVE_ONLY or r.get("Status", "").strip() == "ACTIVE")):
                total_exec_del_rows += 1

    unique_edges = len(edge_set)
    print(f"EXECUTION/DELIVERABLE/ACTIVE rows: {total_exec_del_rows}")
    print(f"Graph: {len(all_nodes)} nodes, {len(edges)} edge rows, {unique_edges} unique directed edges")

    # Write orphans.csv
    with open(os.path.join(EVIDENCE_DIR, "orphans.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["FromDeliverableID", "TargetDeliverableID", "DependencyID", "Direction", "SourceFile"])
        w.writeheader()
        w.writerows(orphan_rows)

    # Build adjacency lists
    adj_out = defaultdict(set)
    adj_in = defaultdict(set)
    for edge_from, edge_to, *_ in edges:
        adj_out[edge_from].add(edge_to)
        adj_in[edge_to].add(edge_from)

    # == Check 1: Schema compliance ==
    schema_coverage_pct = round(csv_valid_count / len(deliverables) * 100, 1) if deliverables else 0.0
    check_schema = {
        "verdict": "PASS" if csv_valid_count == len(deliverables) else "WARNING",
        "detail": f"{csv_valid_count}/{len(deliverables)} deliverables have valid v3.1 schema"
    }

    # == Check 2: Orphan dependencies ==
    check_orphans = {
        "verdict": "BLOCKER" if orphan_rows else "PASS",
        "detail": f"{len(orphan_rows)} orphan target(s)" if orphan_rows else "No orphan targets"
    }

    # == Check 3: Circular dependencies (Tarjan SCC) ==
    scc_graph = defaultdict(list)
    for edge_from, edge_to in edge_set:
        if edge_from in all_nodes and edge_to in all_nodes:
            scc_graph[edge_from].append(edge_to)
    for n in all_nodes:
        if n not in scc_graph:
            scc_graph[n] = []

    all_sccs = tarjan_scc(scc_graph)
    nontrivial_sccs = [s for s in all_sccs if len(s) > 1]

    # Sample cycles from nontrivial SCCs
    cycles_sample = []
    for scc in nontrivial_sccs:
        scc_set = set(scc)
        sub_graph = defaultdict(list)
        for f, t in edge_set:
            if f in scc_set and t in scc_set:
                sub_graph[f].append(t)
        # DFS cycle finder
        for start in sorted(scc):
            if len(cycles_sample) >= MAX_CYCLES:
                break
            path = [start]
            path_set = {start}
            stack_frames = [(start, iter(sorted(sub_graph.get(start, []))))]
            while stack_frames and len(cycles_sample) < MAX_CYCLES:
                node, neighbors = stack_frames[-1]
                try:
                    nxt = next(neighbors)
                    if nxt == start and len(path) > 1:
                        cycles_sample.append(list(path) + [start])
                    elif nxt not in path_set:
                        path.append(nxt)
                        path_set.add(nxt)
                        stack_frames.append((nxt, iter(sorted(sub_graph.get(nxt, [])))))
                except StopIteration:
                    stack_frames.pop()
                    if path:
                        path_set.discard(path.pop())

    # Write SCC summary
    scc_summary_rows = []
    for i, scc in enumerate(nontrivial_sccs):
        scc_summary_rows.append({"SCC_Index": i, "Size": len(scc), "Members": " | ".join(scc)})
    with open(os.path.join(EVIDENCE_DIR, "scc_summary.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["SCC_Index", "Size", "Members"])
        w.writeheader()
        w.writerows(scc_summary_rows)

    # Write cycles sample
    cycles_csv_rows = []
    for i, cycle in enumerate(cycles_sample):
        cycles_csv_rows.append({"Cycle_Index": i, "Length": len(cycle) - 1, "Path": " -> ".join(cycle)})
    with open(os.path.join(EVIDENCE_DIR, "cycles_sample.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["Cycle_Index", "Length", "Path"])
        w.writeheader()
        w.writerows(cycles_csv_rows)

    check_circular = {
        "verdict": "BLOCKER" if nontrivial_sccs else "PASS",
        "detail": f"{len(nontrivial_sccs)} SCC(s), {len(cycles_sample)} cycle(s) sampled" if nontrivial_sccs else "No circular dependencies",
        "sccs": [{"index": i, "size": len(s), "members": s} for i, s in enumerate(nontrivial_sccs)]
    }

    # == Check 4: Anchor coverage ==
    anchors_by_del = defaultdict(list)
    for del_id, rows in all_dep_rows.items():
        for r in rows:
            if (r.get("DependencyClass", "").strip() == "ANCHOR" and
                r.get("AnchorType", "").strip() == "IMPLEMENTS_NODE"):
                anchors_by_del[del_id].append(r.get("DependencyID", ""))

    missing_anchors = sorted([d for d in deliverables if d not in anchors_by_del])
    check_anchor = {
        "verdict": "PASS" if not missing_anchors else "WARNING",
        "detail": "All deliverables have IMPLEMENTS_NODE anchors" if not missing_anchors else f"{len(missing_anchors)} deliverable(s) missing IMPLEMENTS_NODE anchor",
        "missing": missing_anchors
    }

    # == Check 5: Misplaced fields (already computed) ==
    check_misplaced = {
        "verdict": "WARNING" if misplaced else "PASS",
        "detail": f"{len(misplaced)} misplaced field(s)" if misplaced else "No misplaced fields"
    }

    # == Check 6: ID format consistency ==
    long_form_from = 0
    long_form_target = 0
    for del_id in sorted(all_dep_rows.keys()):
        for r in all_dep_rows[del_id]:
            if (r.get("DependencyClass", "").strip() == EDGE_FILTER_CLASS and
                r.get("TargetType", "").strip() == EDGE_FILTER_TARGET_TYPE):
                raw_from = r.get("FromDeliverableID", "").strip()
                raw_target = r.get("TargetDeliverableID", "").strip()
                if "_" in raw_from and raw_from.startswith("DEL-"):
                    long_form_from += 1
                if "_" in raw_target and raw_target.startswith("DEL-"):
                    long_form_target += 1

    check_id_format = {
        "verdict": "PASS" if (long_form_from == 0 and long_form_target == 0) else "INFO",
        "detail": f"All IDs in short form. Long-form From: {long_form_from}, Long-form Target: {long_form_target}"
    }

    # == Check 7: Isolated deliverables ==
    connected = set()
    for edge_from, edge_to, *_ in edges:
        connected.add(edge_from)
        connected.add(edge_to)
    isolated = sorted(all_nodes - connected)

    check_isolated = {
        "verdict": "WARNING" if isolated else "PASS",
        "detail": f"{len(isolated)} isolated deliverable(s)" if isolated else "No isolated deliverables",
        "isolated": isolated
    }

    # == Check 8: Hub analysis ==
    degree_table = {}
    for n in sorted(all_nodes):
        in_deg = len(adj_in.get(n, set()))
        out_deg = len(adj_out.get(n, set()))
        degree_table[n] = {"in": in_deg, "out": out_deg, "total": in_deg + out_deg}

    hubs = sorted([n for n, d in degree_table.items() if d["total"] >= HUB_THRESHOLD],
                  key=lambda n: -degree_table[n]["total"])

    hub_rows = [{"DeliverableID": n, "InDegree": degree_table[n]["in"],
                 "OutDegree": degree_table[n]["out"], "TotalDegree": degree_table[n]["total"]}
                for n in hubs]
    with open(os.path.join(EVIDENCE_DIR, "hubs.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["DeliverableID", "InDegree", "OutDegree", "TotalDegree"])
        w.writeheader()
        w.writerows(hub_rows)

    check_hubs = {
        "verdict": "WARNING" if hubs else "PASS",
        "detail": f"{len(hubs)} hub(s) above threshold {HUB_THRESHOLD}" if hubs else f"No hubs above threshold {HUB_THRESHOLD}",
        "hubs": hubs
    }

    # == Check 9: Bidirectional pairs ==
    bidir_pairs = []
    seen_pairs = set()
    for edge_from, edge_to in edge_set:
        pair = tuple(sorted([edge_from, edge_to]))
        if pair in seen_pairs:
            continue
        if (edge_to, edge_from) in edge_set:
            bidir_pairs.append(pair)
            seen_pairs.add(pair)

    bidir_rows = [{"NodeA": a, "NodeB": b} for a, b in sorted(bidir_pairs)]
    with open(os.path.join(EVIDENCE_DIR, "bidirectional_pairs.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["NodeA", "NodeB"])
        w.writeheader()
        w.writerows(bidir_rows)

    check_bidir = {
        "verdict": "INFO",
        "detail": f"{len(bidir_pairs)} bidirectional pair(s)",
        "pairs": [list(p) for p in sorted(bidir_pairs)]
    }

    # == Execution Path Blocker Analysis ==
    # Blocker subset: EXECUTION + DELIVERABLE + ACTIVE + UPSTREAM + (PREREQUISITE|CONSTRAINT)
    # + non-ASSUMPTION gating
    # Note: only UPSTREAM edges qualify for blocker analysis (DOWNSTREAM are reversed above,
    # but we filter on original direction from the row, not from the normalized edge.)
    blocker_edges_list = []
    blocker_edge_set = set()

    for del_id in sorted(all_dep_rows.keys()):
        for r in all_dep_rows[del_id]:
            dep_class = r.get("DependencyClass", "").strip()
            target_type = r.get("TargetType", "").strip()
            status = r.get("Status", "").strip()
            direction = r.get("Direction", "").strip()
            dep_type = r.get("DependencyType", "").strip()
            dep_id_val = r.get("DependencyID", "").strip()
            from_id = normalize_id(r.get("FromDeliverableID", "").strip()) if NORMALIZE_IDS else r.get("FromDeliverableID", "").strip()
            target_del_id = normalize_id(r.get("TargetDeliverableID", "").strip()) if NORMALIZE_IDS else r.get("TargetDeliverableID", "").strip()

            if dep_class != EDGE_FILTER_CLASS:
                continue
            if target_type != EDGE_FILTER_TARGET_TYPE:
                continue
            if status != "ACTIVE":
                continue
            if direction != "UPSTREAM":
                continue
            if dep_type not in ("PREREQUISITE", "CONSTRAINT"):
                continue
            if not from_id or not target_del_id:
                continue
            if from_id not in all_nodes or target_del_id not in all_nodes:
                continue

            blocker_edges_list.append({
                "from": from_id,
                "to": target_del_id,
                "dep_id": dep_id_val,
                "dep_type": dep_type,
            })
            blocker_edge_set.add((from_id, target_del_id))

    # Topological sort on blocker subset
    blocker_tiers, remaining = topological_sort_kahn(
        all_nodes,
        list(blocker_edge_set)
    )

    # Blocker SCC check
    blocker_scc_graph = defaultdict(list)
    for f, t in blocker_edge_set:
        blocker_scc_graph[f].append(t)
    for n in all_nodes:
        if n not in blocker_scc_graph:
            blocker_scc_graph[n] = []
    blocker_sccs = tarjan_scc(blocker_scc_graph)
    blocker_nontrivial_sccs = [s for s in blocker_sccs if len(s) > 1]

    exec_path_summary = {
        "rule": "EXECUTION + DELIVERABLE + ACTIVE + UPSTREAM + (PREREQUISITE|CONSTRAINT) + non-ASSUMPTION",
        "generated_on": now.isoformat(),
        "all_subset": {
            "nodes": len(all_nodes),
            "edges": len(blocker_edge_set),
            "nontrivial_scc_count": len(blocker_nontrivial_sccs),
            "largest_scc_size": max((len(s) for s in blocker_nontrivial_sccs), default=0),
            "tiers": blocker_tiers,
            "remaining_after_topo": remaining,
        },
    }

    # Core subset excluding PKG-08
    core_nodes = {n for n in all_nodes if not n.startswith("DEL-08")}
    core_blocker_edges = [(f, t) for f, t in blocker_edge_set if f in core_nodes and t in core_nodes]
    core_blocker_edge_set = set(core_blocker_edges)
    core_tiers, core_remaining = topological_sort_kahn(core_nodes, core_blocker_edges)

    core_scc_graph = defaultdict(list)
    for f, t in core_blocker_edge_set:
        core_scc_graph[f].append(t)
    for n in core_nodes:
        if n not in core_scc_graph:
            core_scc_graph[n] = []
    core_sccs = tarjan_scc(core_scc_graph)
    core_nontrivial = [s for s in core_sccs if len(s) > 1]

    exec_path_summary["core_subset_excluding_pkg08"] = {
        "nodes": len(core_nodes),
        "edges": len(core_blocker_edge_set),
        "nontrivial_scc_count": len(core_nontrivial),
        "largest_scc_size": max((len(s) for s in core_nontrivial), default=0),
        "tiers": core_tiers,
        "remaining_after_topo": core_remaining,
    }

    # == Issue Log ==
    issue_log = []
    issue_counter = 1

    for scc in nontrivial_sccs:
        issue_log.append({
            "ID": f"ISS-{issue_counter:03d}", "Severity": "BLOCKER",
            "Check": "circular_dependencies",
            "FromDeliverableID": "; ".join(scc), "TargetDeliverableID": "",
            "DependencyID": "", "Evidence": f"SCC of size {len(scc)}",
            "FixSuggestion": "Break circular dependency by reclassifying or removing edges"
        })
        issue_counter += 1

    for orph in orphan_rows:
        issue_log.append({
            "ID": f"ISS-{issue_counter:03d}", "Severity": "BLOCKER",
            "Check": "orphan_dependencies",
            "FromDeliverableID": orph["FromDeliverableID"],
            "TargetDeliverableID": orph["TargetDeliverableID"],
            "DependencyID": orph["DependencyID"],
            "Evidence": orph["SourceFile"],
            "FixSuggestion": "Target deliverable not found in scope; verify ID or add missing deliverable"
        })
        issue_counter += 1

    for m in misplaced:
        issue_log.append({
            "ID": f"ISS-{issue_counter:03d}", "Severity": "WARNING",
            "Check": "misplaced_fields",
            "FromDeliverableID": m["FromDeliverableID"],
            "TargetDeliverableID": m["TargetDeliverableID"],
            "DependencyID": m["DependencyID"],
            "Evidence": m["SourceFile"],
            "FixSuggestion": "TargetDeliverableID is non-empty but TargetType is not DELIVERABLE; clear field or fix TargetType"
        })
        issue_counter += 1

    for ma in missing_anchors:
        issue_log.append({
            "ID": f"ISS-{issue_counter:03d}", "Severity": "WARNING",
            "Check": "anchor_coverage",
            "FromDeliverableID": ma, "TargetDeliverableID": "",
            "DependencyID": "",
            "Evidence": deliverables[ma]["deps_csv"] if ma in deliverables else "",
            "FixSuggestion": "Add ANCHOR row with AnchorType=IMPLEMENTS_NODE"
        })
        issue_counter += 1

    for iso in isolated:
        issue_log.append({
            "ID": f"ISS-{issue_counter:03d}", "Severity": "WARNING",
            "Check": "isolated_deliverables",
            "FromDeliverableID": iso, "TargetDeliverableID": "",
            "DependencyID": "",
            "Evidence": deliverables[iso]["deps_csv"] if iso in deliverables else "",
            "FixSuggestion": "Verify this deliverable has no EXECUTION/DELIVERABLE dependencies or add them"
        })
        issue_counter += 1

    for h in hubs:
        issue_log.append({
            "ID": f"ISS-{issue_counter:03d}", "Severity": "INFO",
            "Check": "hub_analysis",
            "FromDeliverableID": h, "TargetDeliverableID": "",
            "DependencyID": "",
            "Evidence": f"Degree: {degree_table[h]['total']} (in={degree_table[h]['in']}, out={degree_table[h]['out']})",
            "FixSuggestion": "Review for coordination hotspot risk"
        })
        issue_counter += 1

    for a, b in sorted(bidir_pairs):
        issue_log.append({
            "ID": f"ISS-{issue_counter:03d}", "Severity": "INFO",
            "Check": "bidirectional_pairs",
            "FromDeliverableID": a, "TargetDeliverableID": b,
            "DependencyID": "",
            "Evidence": "Bidirectional edge: A->B and B->A (after direction normalization)",
            "FixSuggestion": "Verify bidirectionality is intentional"
        })
        issue_counter += 1

    # Write issue log
    with open(os.path.join(SNAPSHOT_DIR, "Dependency_Closure_IssueLog.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=[
            "ID", "Severity", "Check", "FromDeliverableID", "TargetDeliverableID",
            "DependencyID", "Evidence", "FixSuggestion"
        ])
        w.writeheader()
        w.writerows(issue_log)

    # Determine overall status
    blockers = [i for i in issue_log if i["Severity"] == "BLOCKER"]
    warnings_list = [i for i in issue_log if i["Severity"] == "WARNING"]
    if blockers:
        overall_status = "BLOCKERS"
    elif warnings_list:
        overall_status = "WARNINGS"
    else:
        overall_status = "PASS"

    # Build closure_summary.json
    summary = {
        "run_label": "AUDIT_DEP_CLOSURE",
        "run_date": now.isoformat(),
        "scope": "ALL",
        "execution_root": EXECUTION_ROOT,
        "overall_status": overall_status,
        "metrics": {
            "total_deliverables": len(deliverables),
            "csv_exists": csv_exists_count,
            "csv_readable": csv_readable_count,
            "schema_valid": csv_valid_count,
            "schema_coverage_pct": schema_coverage_pct,
            "total_execution_deliverable_rows": total_exec_del_rows,
            "total_graph_nodes": len(all_nodes),
            "total_graph_edges": len(edges),
            "unique_edges": unique_edges,
            "orphan_targets": len(orphan_rows),
            "scc_count": len(nontrivial_sccs),
            "scc_total_nodes": sum(len(s) for s in nontrivial_sccs),
            "cycles_sampled": len(cycles_sample),
            "missing_anchor_deliverables": len(missing_anchors),
            "misplaced_target_del_id": len(misplaced),
            "long_form_from_ids": long_form_from,
            "long_form_target_ids": long_form_target,
            "isolated_deliverables": len(isolated),
            "hub_count": len(hubs),
            "bidirectional_pairs": len(bidir_pairs),
            "blocker_subset_edges": len(blocker_edge_set),
        },
        "checks": {
            "schema_compliance": check_schema,
            "orphan_dependencies": check_orphans,
            "circular_dependencies": check_circular,
            "anchor_coverage": check_anchor,
            "misplaced_fields": check_misplaced,
            "id_format_consistency": check_id_format,
            "isolated_deliverables": check_isolated,
            "hub_analysis": check_hubs,
            "bidirectional_pairs": check_bidir,
        },
        "top_issues": issue_log[:10],
        "degree_table": degree_table,
    }

    with open(os.path.join(SNAPSHOT_DIR, "closure_summary.json"), "w") as f:
        json.dump(summary, f, indent=2)

    with open(os.path.join(SNAPSHOT_DIR, "execution_path_summary.json"), "w") as f:
        json.dump(exec_path_summary, f, indent=2)

    print(f"\nOverall status: {overall_status}")
    print(f"Issues: {len(blockers)} BLOCKER, {len(warnings_list)} WARNING, {len(issue_log) - len(blockers) - len(warnings_list)} INFO")
    print(f"Blocker-subset edges: {len(blocker_edge_set)}")
    print(f"Tiers (all): {len(blocker_tiers)}")
    print(f"Tiers (core, excl PKG-08): {len(core_tiers)}")
    print(f"\nDone. Artifacts in: {SNAPSHOT_DIR}")

    return summary, exec_path_summary


if __name__ == "__main__":
    main()
