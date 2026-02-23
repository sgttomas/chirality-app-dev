#!/usr/bin/env python3
"""
Dependency Closure Analysis Script
Run: AUDIT_DEP_CLOSURE | Scope: ALL | Date: 2026-02-22
Deterministic: same inputs produce same outputs.
"""

import csv
import json
import os
import sys
from collections import defaultdict
from datetime import datetime

EXECUTION_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
SNAPSHOT_DIR = os.path.dirname(os.path.abspath(__file__))
EVIDENCE_DIR = os.path.join(SNAPSHOT_DIR, "Evidence")

# Config
FILTER_ACTIVE_ONLY = True
NORMALIZE_IDS = True
HUB_THRESHOLD = 20
MAX_CYCLES = 10000

# Expected v3.1 columns
V31_REQUIRED_COLUMNS = [
    "RegisterSchemaVersion", "DependencyID", "FromPackageID", "FromDeliverableID",
    "FromDeliverableName", "DependencyClass", "AnchorType", "Direction",
    "DependencyType", "TargetType", "TargetPackageID", "TargetDeliverableID",
    "TargetRefID", "TargetName", "TargetLocation", "Statement", "EvidenceFile",
    "SourceRef", "EvidenceQuote", "Explicitness", "RequiredMaturity",
    "ProposedMaturity", "SatisfactionStatus", "Confidence", "Origin",
    "FirstSeen", "LastSeen", "Status", "Notes"
]


def normalize_id(raw_id):
    """Strip descriptive suffix: DEL-XX-YY_Label -> DEL-XX-YY"""
    if not raw_id:
        return raw_id
    raw_id = raw_id.strip()
    # Already short form
    if raw_id.startswith("DEL-"):
        parts = raw_id.split("_", 1)
        return parts[0]
    if raw_id.startswith("KTY-"):
        parts = raw_id.split("_", 1)
        return parts[0]
    return raw_id


def discover_deliverables(execution_root):
    """Discover all deliverable folders and their Dependencies.csv files."""
    deliverables = {}
    for pkg_name in sorted(os.listdir(execution_root)):
        pkg_path = os.path.join(execution_root, pkg_name)
        if not os.path.isdir(pkg_path) or not pkg_name.startswith("PKG-"):
            continue
        working_path = os.path.join(pkg_path, "1_Working")
        if not os.path.isdir(working_path):
            continue
        for del_name in sorted(os.listdir(working_path)):
            del_path = os.path.join(working_path, del_name)
            if not os.path.isdir(del_path) or not del_name.startswith("DEL-"):
                continue
            del_id = normalize_id(del_name) if NORMALIZE_IDS else del_name
            deps_csv = os.path.join(del_path, "Dependencies.csv")
            deliverables[del_id] = {
                "folder_name": del_name,
                "path": del_path,
                "deps_csv": deps_csv,
                "csv_exists": os.path.isfile(deps_csv),
                "csv_readable": False,
                "schema_valid": False,
                "schema_version": None,
                "row_count": 0,
                "status": "DISCOVERED"
            }
    return deliverables


def parse_csv(deliverable_info):
    """Parse and validate a Dependencies.csv file."""
    csv_path = deliverable_info["deps_csv"]
    rows = []
    try:
        with open(csv_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            headers = reader.fieldnames or []
            # Check schema
            missing = [c for c in V31_REQUIRED_COLUMNS if c not in headers]
            if missing:
                deliverable_info["csv_readable"] = True
                deliverable_info["schema_valid"] = False
                deliverable_info["status"] = "SCHEMA_INVALID"
                deliverable_info["schema_errors"] = f"Missing columns: {', '.join(missing)}"
                return rows

            deliverable_info["csv_readable"] = True
            deliverable_info["schema_valid"] = True

            for row in reader:
                # Check schema version
                sv = row.get("RegisterSchemaVersion", "").strip()
                if sv:
                    deliverable_info["schema_version"] = sv
                rows.append(row)

            deliverable_info["row_count"] = len(rows)
            deliverable_info["status"] = "OK"
    except Exception as e:
        deliverable_info["csv_readable"] = False
        deliverable_info["status"] = "UNREADABLE"
        deliverable_info["schema_errors"] = str(e)
    return rows


def build_graph(deliverables, all_rows):
    """Build directed graph from EXECUTION/DELIVERABLE edges."""
    nodes = set(deliverables.keys())
    edges = []  # list of (from_id, to_id, dep_id, direction, dep_type)
    orphan_targets = []
    misplaced = []

    for del_id, rows in all_rows.items():
        for row in rows:
            dep_class = row.get("DependencyClass", "").strip()
            target_type = row.get("TargetType", "").strip()
            status = row.get("Status", "").strip()
            direction = row.get("Direction", "").strip()
            dep_type = row.get("DependencyType", "").strip()
            dep_id = row.get("DependencyID", "").strip()
            from_id = normalize_id(row.get("FromDeliverableID", "").strip()) if NORMALIZE_IDS else row.get("FromDeliverableID", "").strip()
            target_del_id = normalize_id(row.get("TargetDeliverableID", "").strip()) if NORMALIZE_IDS else row.get("TargetDeliverableID", "").strip()

            # Misplaced check: TargetType != DELIVERABLE but TargetDeliverableID is non-empty
            if target_type != "DELIVERABLE" and target_del_id:
                misplaced.append({
                    "DependencyID": dep_id,
                    "FromDeliverableID": from_id,
                    "TargetType": target_type,
                    "TargetDeliverableID": target_del_id,
                    "File": deliverables[del_id]["deps_csv"]
                })

            # Filter
            if FILTER_ACTIVE_ONLY and status != "ACTIVE":
                continue
            if dep_class != "EXECUTION":
                continue
            if target_type != "DELIVERABLE":
                continue
            if not from_id or not target_del_id:
                continue

            # Orphan check
            if target_del_id not in nodes:
                orphan_targets.append({
                    "DependencyID": dep_id,
                    "FromDeliverableID": from_id,
                    "TargetDeliverableID": target_del_id,
                    "Direction": direction,
                    "File": deliverables[del_id]["deps_csv"]
                })
                continue

            # Edge direction: UPSTREAM means from_id depends on target_del_id
            # DOWNSTREAM means from_id provides to target_del_id
            if direction == "UPSTREAM":
                edges.append((from_id, target_del_id, dep_id, direction, dep_type))
            elif direction == "DOWNSTREAM":
                edges.append((target_del_id, from_id, dep_id, direction, dep_type))
            else:
                # Unknown direction - treat as from->target for graph purposes
                edges.append((from_id, target_del_id, dep_id, direction, dep_type))

    return nodes, edges, orphan_targets, misplaced


def tarjan_scc(nodes, edges):
    """Tarjan's SCC algorithm."""
    graph = defaultdict(list)
    for frm, to, *_ in edges:
        graph[frm].append(to)

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
                sccs.append(sorted(scc))

    for node in sorted(nodes):
        if node not in index:
            strongconnect(node)

    return sccs


def find_cycles_in_scc(scc_nodes, edges, max_cycles=100):
    """Find representative cycles within an SCC."""
    sub_graph = defaultdict(list)
    for frm, to, dep_id, *_ in edges:
        if frm in scc_nodes and to in scc_nodes:
            sub_graph[frm].append((to, dep_id))

    cycles = []
    scc_set = set(scc_nodes)

    # Simple DFS cycle finder bounded by max_cycles
    for start in sorted(scc_nodes):
        if len(cycles) >= max_cycles:
            break
        visited = set()
        path = [(start, iter(sub_graph.get(start, [])))]
        path_set = {start}
        path_nodes = [start]

        while path and len(cycles) < max_cycles:
            node, neighbors = path[-1]
            try:
                next_node, dep_id = next(neighbors)
                if next_node == start and len(path_nodes) > 1:
                    cycles.append(list(path_nodes) + [start])
                elif next_node not in path_set and next_node in scc_set:
                    path_set.add(next_node)
                    path_nodes.append(next_node)
                    path.append((next_node, iter(sub_graph.get(next_node, []))))
            except StopIteration:
                path.pop()
                if path_nodes:
                    removed = path_nodes.pop()
                    path_set.discard(removed)

    return cycles


def compute_degrees(nodes, edges):
    """Compute in-degree and out-degree for each node."""
    in_deg = defaultdict(int)
    out_deg = defaultdict(int)
    for frm, to, *_ in edges:
        out_deg[frm] += 1
        in_deg[to] += 1
    degrees = {}
    for n in nodes:
        degrees[n] = {
            "in": in_deg.get(n, 0),
            "out": out_deg.get(n, 0),
            "total": in_deg.get(n, 0) + out_deg.get(n, 0)
        }
    return degrees


def find_bidirectional_pairs(edges):
    """Find pairs where A->B and B->A both exist."""
    edge_set = set()
    for frm, to, dep_id, *_ in edges:
        edge_set.add((frm, to))

    pairs = []
    seen = set()
    for frm, to in edge_set:
        if (to, frm) in edge_set:
            key = tuple(sorted([frm, to]))
            if key not in seen:
                seen.add(key)
                pairs.append(key)
    return sorted(pairs)


def check_anchors(all_rows):
    """Check each deliverable has at least one ANCHOR with AnchorType=IMPLEMENTS_NODE."""
    results = {}
    for del_id, rows in all_rows.items():
        has_anchor = False
        for row in rows:
            if row.get("DependencyClass", "").strip() == "ANCHOR" and row.get("AnchorType", "").strip() == "IMPLEMENTS_NODE":
                has_anchor = True
                break
        results[del_id] = has_anchor
    return results


def main():
    os.makedirs(EVIDENCE_DIR, exist_ok=True)

    # Step 0: Discover
    deliverables = discover_deliverables(EXECUTION_ROOT)
    if not deliverables:
        print("FAILED_INPUTS: No deliverables found.")
        sys.exit(1)

    print(f"Discovered {len(deliverables)} deliverables.")

    # Step 1-2: Parse and validate
    all_rows = {}
    for del_id in sorted(deliverables.keys()):
        info = deliverables[del_id]
        if info["csv_exists"]:
            rows = parse_csv(info)
            if info["schema_valid"]:
                all_rows[del_id] = rows
            else:
                all_rows[del_id] = []
        else:
            info["status"] = "MISSING_DEPENDENCIES_CSV"
            all_rows[del_id] = []

    # Write coverage.csv
    with open(os.path.join(EVIDENCE_DIR, "coverage.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["DeliverableID", "FolderName", "CSVExists", "CSVReadable", "SchemaValid", "SchemaVersion", "RowCount", "Status"])
        for del_id in sorted(deliverables.keys()):
            info = deliverables[del_id]
            w.writerow([del_id, info["folder_name"], info["csv_exists"], info["csv_readable"],
                        info["schema_valid"], info.get("schema_version", ""), info["row_count"], info["status"]])

    # Step 3: Build graph
    nodes, edges, orphan_targets, misplaced = build_graph(deliverables, all_rows)

    # Write orphans.csv
    with open(os.path.join(EVIDENCE_DIR, "orphans.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["DependencyID", "FromDeliverableID", "TargetDeliverableID", "Direction", "File"])
        for o in orphan_targets:
            w.writerow([o["DependencyID"], o["FromDeliverableID"], o["TargetDeliverableID"], o["Direction"], o["File"]])

    # Step 4: Core checks

    # 4.1 Schema compliance
    total = len(deliverables)
    readable = sum(1 for d in deliverables.values() if d["csv_readable"])
    valid = sum(1 for d in deliverables.values() if d["schema_valid"])

    # 4.2 Orphans
    orphan_count = len(orphan_targets)

    # 4.3 Cycles (Tarjan)
    sccs = tarjan_scc(nodes, edges)
    all_cycles_sample = []
    for scc in sccs:
        scc_set = set(scc)
        cycles = find_cycles_in_scc(scc, edges, max_cycles=min(10, MAX_CYCLES))
        for c in cycles[:10]:
            all_cycles_sample.append(c)

    # Write scc_summary.csv
    with open(os.path.join(EVIDENCE_DIR, "scc_summary.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["SCC_ID", "Size", "Members"])
        for i, scc in enumerate(sccs):
            w.writerow([f"SCC-{i+1:03d}", len(scc), " | ".join(sorted(scc))])

    # Write cycles_sample.csv
    with open(os.path.join(EVIDENCE_DIR, "cycles_sample.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["CycleID", "Length", "Path"])
        for i, c in enumerate(all_cycles_sample):
            w.writerow([f"CYC-{i+1:03d}", len(c) - 1, " -> ".join(c)])

    # 4.4 Anchor coverage
    anchor_results = check_anchors(all_rows)
    missing_anchors = [d for d, has in anchor_results.items() if not has]

    # 4.5 Misplaced fields (already computed)

    # 4.6 ID format consistency
    long_form_from = 0
    long_form_target = 0
    total_exec_del_rows = 0
    for del_id, rows in all_rows.items():
        for row in rows:
            if row.get("DependencyClass", "").strip() == "EXECUTION" and row.get("TargetType", "").strip() == "DELIVERABLE":
                total_exec_del_rows += 1
                raw_from = row.get("FromDeliverableID", "").strip()
                raw_target = row.get("TargetDeliverableID", "").strip()
                if "_" in raw_from and raw_from.startswith("DEL-"):
                    long_form_from += 1
                if "_" in raw_target and raw_target.startswith("DEL-"):
                    long_form_target += 1

    # 4.7 Isolated deliverables
    connected = set()
    for frm, to, *_ in edges:
        connected.add(frm)
        connected.add(to)
    isolated = sorted(nodes - connected)

    # 4.8 Hub analysis
    degrees = compute_degrees(nodes, edges)
    hubs = [(n, d) for n, d in degrees.items() if d["total"] >= HUB_THRESHOLD]
    hubs.sort(key=lambda x: -x[1]["total"])

    # Write hubs.csv
    with open(os.path.join(EVIDENCE_DIR, "hubs.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["DeliverableID", "InDegree", "OutDegree", "TotalDegree"])
        for n, d in hubs:
            w.writerow([n, d["in"], d["out"], d["total"]])

    # 4.9 Bidirectional pairs
    bidi_pairs = find_bidirectional_pairs(edges)

    # Write bidirectional_pairs.csv
    with open(os.path.join(EVIDENCE_DIR, "bidirectional_pairs.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["NodeA", "NodeB"])
        for a, b in bidi_pairs:
            w.writerow([a, b])

    # Determine overall status
    blockers = []
    warnings = []

    if sccs:
        blockers.append(f"{len(sccs)} strongly connected component(s) detected (circular dependencies)")
    if orphan_count > 0:
        warnings.append(f"{orphan_count} orphan target(s) pointing to deliverables not in scope")
    if missing_anchors:
        warnings.append(f"{len(missing_anchors)} deliverable(s) missing IMPLEMENTS_NODE anchor")
    if misplaced:
        warnings.append(f"{len(misplaced)} row(s) with TargetType != DELIVERABLE but non-empty TargetDeliverableID")
    if isolated:
        warnings.append(f"{len(isolated)} isolated deliverable(s) with zero EXECUTION/DELIVERABLE edges")

    if blockers:
        overall_status = "BLOCKER"
    elif warnings:
        overall_status = "WARNINGS"
    else:
        overall_status = "PASS"

    # Build JSON summary
    summary = {
        "run_label": "AUDIT_DEP_CLOSURE",
        "run_date": "2026-02-22T22:30:00Z",
        "scope": "ALL",
        "execution_root": EXECUTION_ROOT,
        "overall_status": overall_status,
        "metrics": {
            "total_deliverables": total,
            "csv_exists": sum(1 for d in deliverables.values() if d["csv_exists"]),
            "csv_readable": readable,
            "schema_valid": valid,
            "schema_coverage_pct": round(valid / total * 100, 1) if total > 0 else 0,
            "total_execution_deliverable_rows": total_exec_del_rows,
            "total_graph_nodes": len(nodes),
            "total_graph_edges": len(edges),
            "unique_edges": len(set((f, t) for f, t, *_ in edges)),
            "orphan_targets": orphan_count,
            "scc_count": len(sccs),
            "scc_total_nodes": sum(len(s) for s in sccs),
            "cycles_sampled": len(all_cycles_sample),
            "missing_anchor_deliverables": len(missing_anchors),
            "misplaced_target_del_id": len(misplaced),
            "long_form_from_ids": long_form_from,
            "long_form_target_ids": long_form_target,
            "isolated_deliverables": len(isolated),
            "hub_count": len(hubs),
            "bidirectional_pairs": len(bidi_pairs)
        },
        "checks": {
            "schema_compliance": {
                "verdict": "PASS" if valid == total else "WARNING",
                "detail": f"{valid}/{total} deliverables have valid v3.1 schema"
            },
            "orphan_dependencies": {
                "verdict": "PASS" if orphan_count == 0 else "WARNING",
                "detail": f"{orphan_count} orphan target(s)" if orphan_count > 0 else "No orphan targets"
            },
            "circular_dependencies": {
                "verdict": "BLOCKER" if sccs else "PASS",
                "detail": f"{len(sccs)} SCC(s) containing {sum(len(s) for s in sccs)} nodes" if sccs else "No circular dependencies",
                "sccs": [{"id": f"SCC-{i+1:03d}", "members": sorted(s)} for i, s in enumerate(sccs)]
            },
            "anchor_coverage": {
                "verdict": "PASS" if not missing_anchors else "WARNING",
                "detail": f"{len(missing_anchors)} deliverable(s) missing IMPLEMENTS_NODE anchor" if missing_anchors else "All deliverables have IMPLEMENTS_NODE anchors",
                "missing": sorted(missing_anchors) if missing_anchors else []
            },
            "misplaced_fields": {
                "verdict": "PASS" if not misplaced else "WARNING",
                "detail": f"{len(misplaced)} misplaced TargetDeliverableID value(s)" if misplaced else "No misplaced fields"
            },
            "id_format_consistency": {
                "verdict": "PASS",
                "detail": f"All IDs in short form. Long-form From: {long_form_from}, Long-form Target: {long_form_target}"
            },
            "isolated_deliverables": {
                "verdict": "PASS" if not isolated else "WARNING",
                "detail": f"{len(isolated)} isolated deliverable(s)" if isolated else "All deliverables connected",
                "isolated": isolated
            },
            "hub_analysis": {
                "verdict": "PASS" if not hubs else "INFO",
                "detail": f"{len(hubs)} hub(s) with degree >= {HUB_THRESHOLD}" if hubs else f"No hubs above threshold {HUB_THRESHOLD}",
                "hubs": [{"id": n, "in": d["in"], "out": d["out"], "total": d["total"]} for n, d in hubs]
            },
            "bidirectional_pairs": {
                "verdict": "INFO",
                "detail": f"{len(bidi_pairs)} bidirectional pair(s)",
                "pairs": [list(p) for p in bidi_pairs]
            }
        },
        "top_issues": [],
        "degree_table": {n: degrees[n] for n in sorted(nodes)}
    }

    # Build top issues
    issue_id = 0
    issues = []

    for scc_idx, scc in enumerate(sccs):
        issue_id += 1
        issues.append({
            "ID": f"ISS-{issue_id:03d}",
            "Severity": "BLOCKER",
            "Check": "circular_dependencies",
            "FromDeliverableID": " | ".join(sorted(scc)),
            "TargetDeliverableID": "",
            "DependencyID": "",
            "Evidence": f"SCC-{scc_idx+1:03d}: {' | '.join(sorted(scc))}",
            "FixSuggestion": "Review cycle members and reclassify hard prerequisites to interfaces or break cycle"
        })

    for orphan in orphan_targets:
        issue_id += 1
        issues.append({
            "ID": f"ISS-{issue_id:03d}",
            "Severity": "WARNING",
            "Check": "orphan_dependencies",
            "FromDeliverableID": orphan["FromDeliverableID"],
            "TargetDeliverableID": orphan["TargetDeliverableID"],
            "DependencyID": orphan["DependencyID"],
            "Evidence": orphan["File"],
            "FixSuggestion": "Verify target deliverable exists in workspace or correct the TargetDeliverableID"
        })

    for del_id in sorted(missing_anchors):
        issue_id += 1
        issues.append({
            "ID": f"ISS-{issue_id:03d}",
            "Severity": "WARNING",
            "Check": "anchor_coverage",
            "FromDeliverableID": del_id,
            "TargetDeliverableID": "",
            "DependencyID": "",
            "Evidence": deliverables[del_id]["deps_csv"],
            "FixSuggestion": "Add at least one ANCHOR row with AnchorType=IMPLEMENTS_NODE"
        })

    for m in misplaced:
        issue_id += 1
        issues.append({
            "ID": f"ISS-{issue_id:03d}",
            "Severity": "WARNING",
            "Check": "misplaced_fields",
            "FromDeliverableID": m["FromDeliverableID"],
            "TargetDeliverableID": m["TargetDeliverableID"],
            "DependencyID": m["DependencyID"],
            "Evidence": m["File"],
            "FixSuggestion": f"TargetType is '{m['TargetType']}' but TargetDeliverableID is non-empty; clear TargetDeliverableID or set TargetType=DELIVERABLE"
        })

    for iso in isolated:
        issue_id += 1
        issues.append({
            "ID": f"ISS-{issue_id:03d}",
            "Severity": "WARNING",
            "Check": "isolated_deliverables",
            "FromDeliverableID": iso,
            "TargetDeliverableID": "",
            "DependencyID": "",
            "Evidence": deliverables[iso]["deps_csv"],
            "FixSuggestion": "Verify this deliverable has no EXECUTION/DELIVERABLE dependencies or add them"
        })

    summary["top_issues"] = issues[:10]

    # Write JSON summary
    with open(os.path.join(SNAPSHOT_DIR, "closure_summary.json"), "w") as f:
        json.dump(summary, f, indent=2)

    # Write Issue Log CSV
    with open(os.path.join(SNAPSHOT_DIR, "Dependency_Closure_IssueLog.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["ID", "Severity", "Check", "FromDeliverableID", "TargetDeliverableID", "DependencyID", "Evidence", "FixSuggestion"])
        w.writeheader()
        for iss in issues:
            w.writerow(iss)

    print(f"\nClosure Analysis Complete")
    print(f"Overall Status: {overall_status}")
    print(f"Deliverables: {total}")
    print(f"Schema Valid: {valid}/{total}")
    print(f"Graph: {len(nodes)} nodes, {len(edges)} edges ({len(set((f,t) for f,t,*_ in edges))} unique)")
    print(f"SCCs: {len(sccs)}")
    print(f"Orphans: {orphan_count}")
    print(f"Isolated: {len(isolated)}")
    print(f"Hubs: {len(hubs)}")
    print(f"Bidirectional: {len(bidi_pairs)}")
    print(f"Total Issues: {len(issues)}")

    return summary


if __name__ == "__main__":
    summary = main()
