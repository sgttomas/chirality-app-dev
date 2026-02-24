import csv
import json
import subprocess
import sys
import tempfile
from pathlib import Path
from unittest import TestCase


SCRIPT_PATH = Path(__file__).resolve().parents[1] / "validate_dependencies.py"

CORE_COLUMNS = [
    "RegisterSchemaVersion",
    "DependencyID",
    "FromPackageID",
    "FromDeliverableID",
    "FromDeliverableName",
    "DependencyClass",
    "AnchorType",
    "Direction",
    "DependencyType",
    "TargetType",
    "TargetPackageID",
    "TargetDeliverableID",
    "TargetRefID",
    "TargetName",
    "TargetLocation",
    "Statement",
    "EvidenceFile",
    "SourceRef",
    "EvidenceQuote",
    "Explicitness",
    "RequiredMaturity",
    "ProposedMaturity",
    "SatisfactionStatus",
    "Confidence",
    "Origin",
    "FirstSeen",
    "LastSeen",
    "Status",
    "Notes",
]


def base_row(**overrides: str) -> dict[str, str]:
    row = {
        "RegisterSchemaVersion": "v3.1",
        "DependencyID": "DEP-01-01-001",
        "FromPackageID": "PKG-01",
        "FromDeliverableID": "DEL-01-01",
        "FromDeliverableName": "Example Deliverable",
        "DependencyClass": "ANCHOR",
        "AnchorType": "IMPLEMENTS_NODE",
        "Direction": "UPSTREAM",
        "DependencyType": "OTHER",
        "TargetType": "WBS_NODE",
        "TargetPackageID": "",
        "TargetDeliverableID": "",
        "TargetRefID": "SOW-001",
        "TargetName": "Scope Item",
        "TargetLocation": "",
        "Statement": "Implements scope item.",
        "EvidenceFile": "Datasheet.md",
        "SourceRef": "Datasheet.md#Scope",
        "EvidenceQuote": "Example quote.",
        "Explicitness": "EXPLICIT",
        "RequiredMaturity": "IN_PROGRESS",
        "ProposedMaturity": "IN_PROGRESS",
        "SatisfactionStatus": "PENDING",
        "Confidence": "HIGH",
        "Origin": "EXTRACTED",
        "FirstSeen": "2026-02-24",
        "LastSeen": "2026-02-24",
        "Status": "ACTIVE",
        "Notes": "",
    }
    row.update(overrides)
    return row


def write_csv(path: Path, headers: list[str], rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=headers)
        writer.writeheader()
        for row in rows:
            writer.writerow({header: row.get(header, "") for header in headers})


class ValidateDependenciesTest(TestCase):
    def run_script(self, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(SCRIPT_PATH), *args],
            text=True,
            capture_output=True,
            check=False,
        )

    def test_valid_file_passes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            csv_path = Path(tmp_dir) / "Dependencies.csv"
            rows = [
                base_row(),
                base_row(
                    DependencyID="DEP-01-01-002",
                    DependencyClass="EXECUTION",
                    AnchorType="NOT_APPLICABLE",
                    DependencyType="PREREQUISITE",
                    TargetType="DELIVERABLE",
                    TargetPackageID="PKG-01",
                    TargetDeliverableID="DEL-01-02",
                    TargetRefID="",
                    TargetName="Upstream Deliverable",
                    Statement="Depends on upstream deliverable.",
                ),
            ]
            write_csv(csv_path, CORE_COLUMNS, rows)

            completed = self.run_script(str(csv_path), "--format", "json")
            self.assertEqual(completed.returncode, 0, msg=completed.stderr)
            payload = json.loads(completed.stdout)
            self.assertEqual(payload["summary"]["failFiles"], 0)
            self.assertEqual(payload["summary"]["errorFiles"], 0)

    def test_missing_core_column_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            csv_path = Path(tmp_dir) / "Dependencies.csv"
            headers = [column for column in CORE_COLUMNS if column != "FromPackageID"]
            write_csv(csv_path, headers, [base_row()])

            completed = self.run_script(str(csv_path), "--format", "json")
            self.assertEqual(completed.returncode, 1, msg=completed.stderr)
            payload = json.loads(completed.stdout)
            self.assertEqual(payload["summary"]["failFiles"], 1)
            error_codes = {issue["code"] for issue in payload["files"][0]["errors"]}
            self.assertIn("MISSING_CORE_COLUMNS", error_codes)

    def test_scan_mode_reports_multiple_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir) / "execution"
            valid_path = root / "PKG-01_Test" / "1_Working" / "DEL-01-01_A" / "Dependencies.csv"
            invalid_path = root / "PKG-01_Test" / "1_Working" / "DEL-01-02_B" / "Dependencies.csv"

            write_csv(valid_path, CORE_COLUMNS, [base_row()])
            write_csv(
                invalid_path,
                CORE_COLUMNS,
                [base_row(RegisterSchemaVersion="v2.0", DependencyID="DEP-01-02-001", FromDeliverableID="DEL-01-02")],
            )

            completed = self.run_script("--scan", str(root), "--format", "json")
            self.assertEqual(completed.returncode, 1, msg=completed.stderr)
            payload = json.loads(completed.stdout)
            self.assertEqual(payload["summary"]["filesScanned"], 2)
            self.assertEqual(payload["summary"]["failFiles"], 1)
            self.assertEqual(payload["summary"]["passFiles"], 1)

    def test_missing_file_returns_exit_code_two(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            missing_path = Path(tmp_dir) / "missing.csv"
            completed = self.run_script(str(missing_path), "--format", "json")
            self.assertEqual(completed.returncode, 2)
