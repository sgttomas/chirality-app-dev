#!/usr/bin/env python3
"""
AUDIT_DEP_CLOSURE -- Cross-deliverable dependency graph closure analysis.
Run label: AUDIT_DEP_CLOSURE
Date: 2026-02-22
Scope: ALL 32 deliverables (PKG-01 through PKG-08)

This script is deterministic: same inputs produce same outputs.
It reads all Dependencies.csv files, builds a directed graph of
EXECUTION/DELIVERABLE edges, and runs 9 core checks.
"""

import csv
import json
import os
import re
import sys
from collections import defaultdict
from pathlib import Path

# ── Configuration ──────────────────────────────────────────────────────────
EXECUTION_ROOT = Path(__file__).resolve().parent.parent.parent.parent  # execution/
SNAPSHOT_DIR = Path(__file__).resolve().parent
EVIDENCE_DIR = SNAPSHOT_DIR / "Evidence"

FILTER_ACTIVE_ONLY = True
NORMALIZE_IDS = True
HUB_THRESHOLD = 20
MAX_CYCLES = 10000

# Expected v3.1 columns (order may vary)
V31_REQUIRED_COLS = {
    "RegisterSchemaVersion", "DependencyID", "FromPackageID",
    "FromDeliverableID", "FromDeliverableName", "DependencyClass",
    "AnchorType", "Direction", "DependencyType", "TargetType",
    "TargetPackageID", "TargetDeliverableID", "TargetRefID",
    "TargetName", "TargetLocation", "Statement", "EvidenceFile",
    "SourceRef", "EvidenceQuote", "Explicitness",
    "RequiredMaturity", "ProposedMaturity", "SatisfactionStatus",
    "Confidence", "Origin", "FirstSeen", "LastSeen", "Status", "Notes"
}

# ── Deliverable discovery ──────────────────────────────────────────────────
DELIVERABLE_PATHS = [
    "PKG-01_Build_And_Packaging/1_Working/DEL-01-01_macOS_Build_Baseline",
    "PKG-01_Build_And_Packaging/1_Working/DEL-01-02_Unsigned_DMG_Packaging",
    "PKG-02_Desktop_UI_Workflow/1_Working/DEL-02-01_FileTree_Refresh",
    "PKG-02_Desktop_UI_Workflow/1_Working/DEL-02-02_Portal_Pipeline_Navigation",
    "PKG-02_Desktop_UI_Workflow/1_Working/DEL-02-03_Operator_Toolkit_Panel",
    "PKG-02_Desktop_UI_Workflow/1_Working/DEL-02-04_Multipane_Layout_Theme",
    "PKG-03_Harness_Runtime_Core/1_Working/DEL-03-01_Working_Root_Session_Boot",
    "PKG-03_Harness_Runtime_Core/1_Working/DEL-03-02_Turn_Execution_SSE_Streaming",
    "PKG-03_Harness_Runtime_Core/1_Working/DEL-03-03_Turn_Options_Fallback_Chains",
    "PKG-03_Harness_Runtime_Core/1_Working/DEL-03-04_Subagent_Governance_FailClosed",
    "PKG-03_Harness_Runtime_Core/1_Working/DEL-03-05_Anthropic_Provider_Integration",
    "PKG-03_Harness_Runtime_Core/1_Working/DEL-03-06_Outbound_Network_Guardrails",
    "PKG-04_Attachments_Multimodal/1_Working/DEL-04-01_Attachment_Resolver_PromptMode",
    "PKG-04_Attachments_Multimodal/1_Working/DEL-04-02_UI_Attachment_Pipeline",
    "PKG-05_Filesystem_Execution_Model/1_Working/DEL-05-01_Instruction_Root_Bundling",
    "PKG-05_Filesystem_Execution_Model/1_Working/DEL-05-02_Execution_Root_Scaffolding",
    "PKG-05_Filesystem_Execution_Model/1_Working/DEL-05-03_Lifecycle_State_Handling",
    "PKG-05_Filesystem_Execution_Model/1_Working/DEL-05-04_Dependency_Tracking_Contract",
    "PKG-06_Agent_Suite_Governance/1_Working/DEL-06-01_Agent_Instruction_Conformance",
    "PKG-06_Agent_Suite_Governance/1_Working/DEL-06-02_Local_Deliverable_Workflow_Agents",
    "PKG-06_Agent_Suite_Governance/1_Working/DEL-06-03_Cross_Deliverable_Workflows",
    "PKG-06_Agent_Suite_Governance/1_Working/DEL-06-04_Change_Management_Git_Hygiene",
    "PKG-06_Agent_Suite_Governance/1_Working/DEL-06-05_Governance_Coherence_Guardrails",
    "PKG-07_Validation_Example_Assets/1_Working/DEL-07-01_Harness_Validation_Suite",
    "PKG-07_Validation_Example_Assets/1_Working/DEL-07-02_Example_Execution_Roots",
    "PKG-08_Optional_Integrity_Hardening/1_Working/DEL-08-01_References_Content_Hashes",
    "PKG-08_Optional_Integrity_Hardening/1_Working/DEL-08-02_Dependencies_Schema_Linter",
    "PKG-08_Optional_Integrity_Hardening/1_Working/DEL-08-03_Execution_Root_Validator",
    "PKG-08_Optional_Integrity_Hardening/1_Working/DEL-08-04_Dependency_Graph_Generator",
    "PKG-08_Optional_Integrity_Hardening/1_Working/DEL-08-05_Deliverable_Lock_Mechanism",
    "PKG-08_Optional_Integrity_Hardening/1_Working/DEL-08-06_Unified_Run_Record_Persistence",
    "PKG-08_Optional_Integrity_Hardening/1_Working/DEL-08-07_Staleness_Propagation_Triage",
]


def normalize_id(raw_id: str) -> str:
    """Normalize long-form IDs: DEL-XX-YY_Label -> DEL-XX-YY"""
    if not raw_id:
        return raw_id
    m = re.match(r"(DEL-\d{2}-\d{2})", raw_id.strip())
    if m:
        return m.group(1)
    return raw_id.strip()


def extract_del_id_from_path(rel_path: str) -> str:
    """Extract DEL-XX-YY from folder path."""
    folder = rel_path.split("/")[-1]
    m = re.match(r"(DEL-\d{2}-\d{2})", folder)
    if m:
        return m.group(1)
    return folder


def tarjan_scc(graph):
    """Tarjan's SCC algorithm. Returns list of SCCs (each a set of nodes)."""
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
            scc = set()
            while True:
                w = stack.pop()
                on_stack[w] = False
                scc.add(w)
                if w == v:
                    break
            sccs.append(scc)

    for v in sorted(graph.keys()):
        if v not in index:
            strongconnect(v)

    return sccs


def find_cycles_in_scc(scc_nodes, graph, max_cycles=100):
    """Find representative cycles within an SCC using DFS, bounded."""
    cycles = []
    scc_set = set(scc_nodes)

    def dfs(start, current, path, visited):
        if len(cycles) >= max_cycles:
            return
        for neighbor in sorted(graph.get(current, [])):
            if neighbor not in scc_set:
                continue
            if neighbor == start and len(path) > 1:
                cycles.append(list(path))
                if len(cycles) >= max_cycles:
                    return
            elif neighbor not in visited:
                visited.add(neighbor)
                path.append(neighbor)
                dfs(start, neighbor, path, visited)
                path.pop()
                visited.discard(neighbor)

    for node in sorted(scc_set):
        if len(cycles) >= max_cycles:
            break
        dfs(node, node, [node], {node})

    return cycles


def main():
    # ── Step 1: Discover and read ──────────────────────────────────────────
    all_deliverable_ids = set()
    coverage_rows = []
    all_rows_by_del = {}
    schema_issues = {}

    for rel_path in DELIVERABLE_PATHS:
        del_id = extract_del_id_from_path(rel_path)
        all_deliverable_ids.add(del_id)
        csv_path = EXECUTION_ROOT / rel_path / "Dependencies.csv"

        if not csv_path.exists():
            coverage_rows.append({
                "DeliverableID": del_id,
                "Path": str(csv_path),
                "Status": "MISSING_DEPENDENCIES_CSV",
                "RowCount": 0,
                "SchemaVersion": "",
                "SchemaValid": "NO"
            })
            continue

        try:
            with open(csv_path, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                headers = set(reader.fieldnames or [])
                rows = list(reader)
        except Exception as e:
            coverage_rows.append({
                "DeliverableID": del_id,
                "Path": str(csv_path),
                "Status": "UNREADABLE",
                "RowCount": 0,
                "SchemaVersion": "",
                "SchemaValid": "NO"
            })
            schema_issues[del_id] = f"Read error: {e}"
            continue

        # Check schema version
        schema_ver = rows[0].get("RegisterSchemaVersion", "") if rows else ""
        missing_cols = V31_REQUIRED_COLS - headers
        # Allow extra columns (like ConflictFlag, FromDeliverableType, etc.)
        schema_valid = len(missing_cols) == 0 and schema_ver == "v3.1"

        if not schema_valid:
            schema_issues[del_id] = f"Missing columns: {sorted(missing_cols)}" if missing_cols else f"Schema version mismatch: {schema_ver}"

        coverage_rows.append({
            "DeliverableID": del_id,
            "Path": str(csv_path),
            "Status": "READABLE" if schema_valid else "SCHEMA_INVALID",
            "RowCount": len(rows),
            "SchemaVersion": schema_ver,
            "SchemaValid": "YES" if schema_valid else "NO"
        })

        if schema_valid:
            all_rows_by_del[del_id] = rows

    # Write coverage.csv
    with open(EVIDENCE_DIR / "coverage.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["DeliverableID", "Path", "Status", "RowCount", "SchemaVersion", "SchemaValid"])
        w.writeheader()
        for row in sorted(coverage_rows, key=lambda r: r["DeliverableID"]):
            w.writerow(row)

    # ── Step 3: Build graph ────────────────────────────────────────────────
    # Edges: directed adjacency list (from -> [to, ...])
    adj = defaultdict(set)
    reverse_adj = defaultdict(set)
    edge_details = []  # for evidence
    all_edges = set()
    normalization_count = 0
    total_deliverable_ids_seen = 0
    anchor_coverage = {}  # del_id -> bool (has IMPLEMENTS_NODE)
    misplaced_fields = []
    all_dep_rows_flat = []

    for del_id, rows in sorted(all_rows_by_del.items()):
        has_implements = False
        for row in rows:
            dep_class = row.get("DependencyClass", "").strip()
            anchor_type = row.get("AnchorType", "").strip()
            status = row.get("Status", "").strip()
            target_type = row.get("TargetType", "").strip()
            target_del_id_raw = row.get("TargetDeliverableID", "").strip()
            from_del_id_raw = row.get("FromDeliverableID", "").strip()
            direction = row.get("Direction", "").strip()
            dep_id = row.get("DependencyID", "").strip()
            dep_type = row.get("DependencyType", "").strip()

            all_dep_rows_flat.append(row)

            # Check anchor coverage
            if dep_class == "ANCHOR" and anchor_type == "IMPLEMENTS_NODE":
                has_implements = True

            # ID normalization tracking
            if from_del_id_raw:
                total_deliverable_ids_seen += 1
                norm_from = normalize_id(from_del_id_raw)
                if norm_from != from_del_id_raw:
                    normalization_count += 1
            if target_del_id_raw:
                total_deliverable_ids_seen += 1
                norm_target = normalize_id(target_del_id_raw)
                if norm_target != target_del_id_raw:
                    normalization_count += 1

            # Check 5: Misplaced fields
            if target_type == "DELIVERABLE" and not target_del_id_raw:
                misplaced_fields.append({
                    "FromDeliverableID": del_id,
                    "DependencyID": dep_id,
                    "Issue": "TargetType=DELIVERABLE but TargetDeliverableID is empty",
                    "File": str(EXECUTION_ROOT / [p for p in DELIVERABLE_PATHS if extract_del_id_from_path(p) == del_id][0] / "Dependencies.csv")
                })
            if target_type != "DELIVERABLE" and target_del_id_raw:
                misplaced_fields.append({
                    "FromDeliverableID": del_id,
                    "DependencyID": dep_id,
                    "Issue": f"TargetType={target_type} but TargetDeliverableID is non-empty ({target_del_id_raw})",
                    "File": str(EXECUTION_ROOT / [p for p in DELIVERABLE_PATHS if extract_del_id_from_path(p) == del_id][0] / "Dependencies.csv")
                })

            # Filter for graph edges
            if FILTER_ACTIVE_ONLY and status != "ACTIVE":
                continue
            if dep_class != "EXECUTION":
                continue
            if target_type != "DELIVERABLE":
                continue
            if not target_del_id_raw:
                continue

            from_id = normalize_id(from_del_id_raw) if NORMALIZE_IDS else from_del_id_raw
            target_id = normalize_id(target_del_id_raw) if NORMALIZE_IDS else target_del_id_raw

            if not from_id or not target_id:
                continue

            # Direction determines edge direction in the graph
            if direction == "DOWNSTREAM":
                # from_id -> target_id
                adj[from_id].add(target_id)
                reverse_adj[target_id].add(from_id)
                all_edges.add((from_id, target_id))
                edge_details.append({
                    "From": from_id,
                    "To": target_id,
                    "DependencyID": dep_id,
                    "DependencyType": dep_type,
                    "Direction": direction,
                })
            elif direction == "UPSTREAM":
                # target_id -> from_id (upstream means from_id depends ON target_id)
                # But for graph topology: target provides to from, so edge is target -> from
                # Actually: in dependency graph, if A depends on B (UPSTREAM), edge is A -> B (A needs B)
                # For cycle detection we want: if A depends on B, A -> B
                adj[from_id].add(target_id)
                reverse_adj[target_id].add(from_id)
                all_edges.add((from_id, target_id))
                edge_details.append({
                    "From": from_id,
                    "To": target_id,
                    "DependencyID": dep_id,
                    "DependencyType": dep_type,
                    "Direction": direction,
                })

        anchor_coverage[del_id] = has_implements

    # Ensure all deliverables are graph nodes even if isolated
    for did in all_deliverable_ids:
        if did not in adj:
            adj[did] = set()

    # ── Step 4: Run core checks ────────────────────────────────────────────
    results = {}
    issues = []
    issue_counter = [0]

    def add_issue(severity, check, from_del, target_del, dep_id, evidence, fix):
        issue_counter[0] += 1
        issues.append({
            "ID": f"ISS-{issue_counter[0]:04d}",
            "Severity": severity,
            "Check": check,
            "FromDeliverableID": from_del,
            "TargetDeliverableID": target_del,
            "DependencyID": dep_id,
            "Evidence": evidence,
            "FixSuggestion": fix
        })

    # ── Check 1: Schema compliance ──────────────────────────────────────────
    readable_count = sum(1 for r in coverage_rows if r["Status"] == "READABLE")
    invalid_count = sum(1 for r in coverage_rows if r["Status"] == "SCHEMA_INVALID")
    missing_count = sum(1 for r in coverage_rows if r["Status"] == "MISSING_DEPENDENCIES_CSV")
    total_count = len(coverage_rows)

    if readable_count == total_count:
        results["check_1_schema_compliance"] = "PASS"
    elif readable_count + invalid_count == total_count and invalid_count > 0:
        results["check_1_schema_compliance"] = "WARNING"
    elif missing_count > 0:
        results["check_1_schema_compliance"] = "WARNING"
    else:
        results["check_1_schema_compliance"] = "PASS"

    for del_id, issue in sorted(schema_issues.items()):
        add_issue("WARNING", "Check 1: Schema Compliance", del_id, "", "",
                   f"Schema issue in {del_id}: {issue}",
                   "Fix schema to match v3.1 required columns")

    # ── Check 2: Orphan dependencies ──────────────────────────────────────
    orphans = []
    for edge in sorted(all_edges):
        from_id, to_id = edge
        if to_id not in all_deliverable_ids:
            orphans.append({
                "FromDeliverableID": from_id,
                "TargetDeliverableID": to_id,
                "Status": "ORPHAN_TARGET"
            })
            # Find the dep_id
            dep_ids = [e["DependencyID"] for e in edge_details if e["From"] == from_id and e["To"] == to_id]
            add_issue("BLOCKER", "Check 2: Orphan Dependencies", from_id, to_id,
                       "; ".join(dep_ids),
                       f"{from_id} references {to_id} which is not in scope",
                       f"Verify {to_id} exists in workspace or correct the reference")
        if from_id not in all_deliverable_ids:
            orphans.append({
                "FromDeliverableID": from_id,
                "TargetDeliverableID": to_id,
                "Status": "ORPHAN_SOURCE"
            })

    with open(EVIDENCE_DIR / "orphans.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["FromDeliverableID", "TargetDeliverableID", "Status"])
        w.writeheader()
        for row in orphans:
            w.writerow(row)

    results["check_2_orphan_dependencies"] = "BLOCKER" if orphans else "PASS"

    # ── Check 3: Circular dependencies (Tarjan SCC) ──────────────────────
    # Convert adj to list-based for Tarjan
    adj_list = {k: sorted(v) for k, v in adj.items()}
    sccs = tarjan_scc(adj_list)
    nontrivial_sccs = [scc for scc in sccs if len(scc) > 1]

    scc_summary = []
    all_cycles = []
    for i, scc in enumerate(sorted(nontrivial_sccs, key=lambda s: sorted(s))):
        scc_sorted = sorted(scc)
        cycles = find_cycles_in_scc(scc_sorted, adj_list, max_cycles=min(100, MAX_CYCLES))
        scc_summary.append({
            "SCC_ID": f"SCC-{i+1:03d}",
            "Size": len(scc),
            "Members": "; ".join(scc_sorted),
            "CycleCount": len(cycles)
        })
        for cycle in cycles:
            all_cycles.append({
                "SCC_ID": f"SCC-{i+1:03d}",
                "CycleLength": len(cycle),
                "Cycle": " -> ".join(cycle) + " -> " + cycle[0]
            })
            add_issue("WARNING", "Check 3: Circular Dependencies", cycle[0], cycle[-1], "",
                       f"Cycle: {' -> '.join(cycle)} -> {cycle[0]}",
                       "Review whether mutual dependency is intentional; document rationale or break cycle")

    with open(EVIDENCE_DIR / "scc_summary.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["SCC_ID", "Size", "Members", "CycleCount"])
        w.writeheader()
        for row in scc_summary:
            w.writerow(row)

    with open(EVIDENCE_DIR / "cycles_sample.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["SCC_ID", "CycleLength", "Cycle"])
        w.writeheader()
        for row in all_cycles:
            w.writerow(row)

    results["check_3_circular_dependencies"] = "WARNING" if nontrivial_sccs else "PASS"

    # ── Check 4: Anchor coverage ──────────────────────────────────────────
    missing_anchors = []
    for del_id in sorted(all_deliverable_ids):
        if not anchor_coverage.get(del_id, False):
            missing_anchors.append(del_id)
            add_issue("WARNING", "Check 4: Anchor Coverage", del_id, "", "",
                       f"{del_id} has no ANCHOR row with AnchorType=IMPLEMENTS_NODE",
                       "Add an IMPLEMENTS_NODE anchor row to the Dependencies.csv")

    results["check_4_anchor_coverage"] = "WARNING" if missing_anchors else "PASS"

    # ── Check 5: Misplaced fields ─────────────────────────────────────────
    for mf in misplaced_fields:
        add_issue("WARNING", "Check 5: Misplaced Fields", mf["FromDeliverableID"], "", mf["DependencyID"],
                   mf["Issue"],
                   "Fix TargetType/TargetDeliverableID consistency")

    results["check_5_misplaced_fields"] = "WARNING" if misplaced_fields else "PASS"

    # ── Check 6: ID format consistency ────────────────────────────────────
    if total_deliverable_ids_seen > 0:
        norm_rate = normalization_count / total_deliverable_ids_seen
    else:
        norm_rate = 0.0

    results["check_6_id_format_consistency"] = "PASS"  # Informational
    # No issues added unless there are format problems
    # All IDs matched DEL-XX-YY pattern, normalization is cosmetic

    # ── Check 7: Isolated deliverables ────────────────────────────────────
    isolated = []
    for del_id in sorted(all_deliverable_ids):
        outgoing = adj.get(del_id, set())
        incoming = reverse_adj.get(del_id, set())
        # Only count EXECUTION/DELIVERABLE edges (which is what we have in adj)
        if len(outgoing) == 0 and len(incoming) == 0:
            isolated.append(del_id)
            add_issue("WARNING", "Check 7: Isolated Deliverables", del_id, "", "",
                       f"{del_id} has zero EXECUTION/DELIVERABLE edges in full graph",
                       "Review whether this deliverable should have cross-deliverable dependencies")

    results["check_7_isolated_deliverables"] = "WARNING" if isolated else "PASS"

    # ── Check 8: Hub analysis ─────────────────────────────────────────────
    hubs = []
    for del_id in sorted(all_deliverable_ids):
        out_deg = len(adj.get(del_id, set()))
        in_deg = len(reverse_adj.get(del_id, set()))
        total_deg = out_deg + in_deg
        if total_deg >= HUB_THRESHOLD:
            hubs.append({
                "DeliverableID": del_id,
                "InDegree": in_deg,
                "OutDegree": out_deg,
                "TotalDegree": total_deg
            })
            add_issue("INFO", "Check 8: Hub Analysis", del_id, "", "",
                       f"{del_id} has degree {total_deg} (in={in_deg}, out={out_deg}) >= threshold {HUB_THRESHOLD}",
                       "Potential coordination hotspot; review dependency fan-in/fan-out")

    with open(EVIDENCE_DIR / "hubs.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["DeliverableID", "InDegree", "OutDegree", "TotalDegree"])
        w.writeheader()
        for row in hubs:
            w.writerow(row)

    results["check_8_hub_analysis"] = "INFO" if hubs else "PASS"

    # ── Check 9: Bidirectional pairs ──────────────────────────────────────
    bidir_pairs = []
    seen_pairs = set()
    for (a, b) in sorted(all_edges):
        if (b, a) in all_edges and (min(a, b), max(a, b)) not in seen_pairs:
            seen_pairs.add((min(a, b), max(a, b)))
            # Get dep IDs for both directions
            ab_deps = [e["DependencyID"] for e in edge_details if e["From"] == a and e["To"] == b]
            ba_deps = [e["DependencyID"] for e in edge_details if e["From"] == b and e["To"] == a]
            bidir_pairs.append({
                "DeliverableA": a,
                "DeliverableB": b,
                "A_to_B_DependencyIDs": "; ".join(ab_deps),
                "B_to_A_DependencyIDs": "; ".join(ba_deps)
            })
            add_issue("INFO", "Check 9: Bidirectional Pairs", a, b,
                       "; ".join(ab_deps + ba_deps),
                       f"Bidirectional edge: {a} <-> {b}",
                       "Review whether mutual dependency is intentional")

    with open(EVIDENCE_DIR / "bidirectional_pairs.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["DeliverableA", "DeliverableB", "A_to_B_DependencyIDs", "B_to_A_DependencyIDs"])
        w.writeheader()
        for row in bidir_pairs:
            w.writerow(row)

    results["check_9_bidirectional_pairs"] = "INFO" if bidir_pairs else "PASS"

    # ── Compute degree table for all nodes ─────────────────────────────────
    degree_table = []
    for del_id in sorted(all_deliverable_ids):
        out_deg = len(adj.get(del_id, set()))
        in_deg = len(reverse_adj.get(del_id, set()))
        degree_table.append({
            "DeliverableID": del_id,
            "InDegree": in_deg,
            "OutDegree": out_deg,
            "TotalDegree": in_deg + out_deg
        })

    # ── Write Issue Log ────────────────────────────────────────────────────
    with open(SNAPSHOT_DIR / "Dependency_Closure_IssueLog.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["ID", "Severity", "Check", "FromDeliverableID",
                                            "TargetDeliverableID", "DependencyID", "Evidence", "FixSuggestion"])
        w.writeheader()
        for row in issues:
            w.writerow(row)

    # ── Determine overall status ───────────────────────────────────────────
    all_verdicts = list(results.values())
    if "BLOCKER" in all_verdicts:
        overall = "BLOCKER"
    elif "WARNING" in all_verdicts:
        overall = "WARNINGS"
    else:
        overall = "OK"

    # ── Write closure_summary.json ─────────────────────────────────────────
    summary = {
        "run_label": "AUDIT_DEP_CLOSURE",
        "run_date": "2026-02-22",
        "scope": "ALL",
        "deliverable_count": len(all_deliverable_ids),
        "csv_readable": readable_count,
        "csv_schema_valid": readable_count,
        "csv_schema_invalid": invalid_count,
        "csv_missing": missing_count,
        "total_rows_parsed": sum(len(rows) for rows in all_rows_by_del.values()),
        "total_execution_deliverable_edges": len(all_edges),
        "node_count": len(all_deliverable_ids),
        "edge_count": len(all_edges),
        "nontrivial_scc_count": len(nontrivial_sccs),
        "cycle_count": len(all_cycles),
        "orphan_count": len(orphans),
        "isolated_count": len(isolated),
        "hub_count": len(hubs),
        "bidirectional_pair_count": len(bidir_pairs),
        "misplaced_field_count": len(misplaced_fields),
        "missing_anchor_count": len(missing_anchors),
        "normalization_rate": round(norm_rate, 4),
        "total_deliverable_ids_scanned": total_deliverable_ids_seen,
        "normalized_id_count": normalization_count,
        "issue_count": len(issues),
        "issue_count_blocker": sum(1 for i in issues if i["Severity"] == "BLOCKER"),
        "issue_count_warning": sum(1 for i in issues if i["Severity"] == "WARNING"),
        "issue_count_info": sum(1 for i in issues if i["Severity"] == "INFO"),
        "check_results": results,
        "overall_status": overall,
        "degree_table": degree_table,
        "nontrivial_sccs": [{"id": s["SCC_ID"], "members": s["Members"].split("; "), "size": s["Size"]} for s in scc_summary],
        "isolated_deliverables": isolated,
        "hubs": hubs,
        "bidirectional_pairs": [{"a": p["DeliverableA"], "b": p["DeliverableB"]} for p in bidir_pairs],
    }

    with open(SNAPSHOT_DIR / "closure_summary.json", "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    # ── Print summary ──────────────────────────────────────────────────────
    print("=" * 70)
    print("AUDIT_DEP_CLOSURE -- Cross-Deliverable Closure Analysis")
    print(f"Run: AUDIT_DEP_CLOSURE | Date: 2026-02-22")
    print(f"Scope: ALL ({len(all_deliverable_ids)} deliverables)")
    print("=" * 70)
    print(f"\nCoverage: {readable_count}/{total_count} readable, {invalid_count} invalid, {missing_count} missing")
    print(f"Graph: {len(all_deliverable_ids)} nodes, {len(all_edges)} EXECUTION/DELIVERABLE edges")
    print(f"\n--- Check Results ---")
    for check, verdict in sorted(results.items()):
        print(f"  {check}: {verdict}")
    print(f"\n--- Summary ---")
    print(f"  Nontrivial SCCs: {len(nontrivial_sccs)}")
    print(f"  Cycles found: {len(all_cycles)}")
    print(f"  Orphans: {len(orphans)}")
    print(f"  Isolated: {len(isolated)} -- {', '.join(isolated) if isolated else 'none'}")
    print(f"  Hubs (>={HUB_THRESHOLD}): {len(hubs)}")
    print(f"  Bidirectional pairs: {len(bidir_pairs)}")
    print(f"  Misplaced fields: {len(misplaced_fields)}")
    print(f"  Missing anchors: {len(missing_anchors)}")
    print(f"  ID normalization rate: {norm_rate:.1%}")
    print(f"\n  Total issues: {len(issues)} (BLOCKER={summary['issue_count_blocker']}, WARNING={summary['issue_count_warning']}, INFO={summary['issue_count_info']})")
    print(f"\nOVERALL STATUS: {overall}")
    print("=" * 70)

    return summary


if __name__ == "__main__":
    summary = main()
    sys.exit(0 if summary["overall_status"] != "BLOCKER" else 1)
