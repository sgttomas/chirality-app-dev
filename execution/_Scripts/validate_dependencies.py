#!/usr/bin/env python3
"""Standalone Dependencies.csv v3.1 schema linter."""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path

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

EXTENSION_COLUMNS = ["EstimateImpactClass", "ConsumerHint"]

REQUIRED_NON_EMPTY_COLUMNS = {
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
    "Origin",
    "FirstSeen",
    "LastSeen",
    "Status",
}

ENUM_VALUES = {
    "DependencyClass": {"ANCHOR", "EXECUTION"},
    "AnchorType": {"IMPLEMENTS_NODE", "TRACES_TO_REQUIREMENT", "NOT_APPLICABLE"},
    "Direction": {"UPSTREAM", "DOWNSTREAM"},
    "DependencyType": {"PREREQUISITE", "INTERFACE", "HANDOVER", "CONSTRAINT", "ENABLES", "OTHER"},
    "TargetType": {"DELIVERABLE", "PACKAGE", "WBS_NODE", "REQUIREMENT", "DOCUMENT", "EQUIPMENT", "EXTERNAL", "UNKNOWN"},
    "Explicitness": {"EXPLICIT", "IMPLICIT"},
    "SatisfactionStatus": {"TBD", "PENDING", "IN_PROGRESS", "SATISFIED", "WAIVED", "NOT_APPLICABLE"},
    "Confidence": {"HIGH", "MEDIUM", "LOW"},
    "Origin": {"DECLARED", "EXTRACTED"},
    "Status": {"ACTIVE", "RETIRED"},
    "EstimateImpactClass": {"BLOCKING", "ADVISORY", "INFO", "TBD"},
    "ConsumerHint": {"TASK", "TASK_ESTIMATING", "AGGREGATION", "RECONCILIATION", "TBD"},
}

LEGACY_ENUMS = {
    "Direction": {"INBOUND", "OUTBOUND"},
    "DependencyType": {"COORDINATION", "INFORMATION"},
}

PREFERRED_EXECUTION_DEPENDENCY_TYPES = {"PREREQUISITE", "INTERFACE", "HANDOVER", "CONSTRAINT", "ENABLES"}

DEPENDENCY_ID_PATTERN = re.compile(r"^DEP-\d{2,3}-\d{2}-\d{3}$")
DELIVERABLE_ID_PATTERN = re.compile(r"^DEL-\d{2,3}-\d{2}$")
ISO_DATE_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def is_iso_date(value: str) -> bool:
    if not ISO_DATE_PATTERN.match(value):
        return False
    try:
        datetime.strptime(value, "%Y-%m-%d")
    except ValueError:
        return False
    return True


@dataclass
class Issue:
    severity: str
    code: str
    message: str
    row: int | None = None
    column: str | None = None
    value: str | None = None

    def to_dict(self) -> dict:
        payload = {
            "severity": self.severity,
            "code": self.code,
            "message": self.message,
        }
        if self.row is not None:
            payload["row"] = self.row
        if self.column is not None:
            payload["column"] = self.column
        if self.value is not None:
            payload["value"] = self.value
        return payload


@dataclass
class FileValidationResult:
    path: str
    status: str
    rows: int = 0
    errors: list[Issue] = field(default_factory=list)
    warnings: list[Issue] = field(default_factory=list)

    def add_error(
        self,
        code: str,
        message: str,
        row: int | None = None,
        column: str | None = None,
        value: str | None = None,
    ) -> None:
        self.errors.append(
            Issue(
                severity="error",
                code=code,
                message=message,
                row=row,
                column=column,
                value=value,
            )
        )

    def add_warning(
        self,
        code: str,
        message: str,
        row: int | None = None,
        column: str | None = None,
        value: str | None = None,
    ) -> None:
        self.warnings.append(
            Issue(
                severity="warning",
                code=code,
                message=message,
                row=row,
                column=column,
                value=value,
            )
        )

    def as_dict(self) -> dict:
        return {
            "path": self.path,
            "status": self.status,
            "rows": self.rows,
            "errorCount": len(self.errors),
            "warningCount": len(self.warnings),
            "errors": [issue.to_dict() for issue in self.errors],
            "warnings": [issue.to_dict() for issue in self.warnings],
        }


def read_csv_rows(csv_path: Path, result: FileValidationResult) -> tuple[list[str], list[tuple[int, dict[str, str]]]]:
    headers: list[str] = []
    rows: list[tuple[int, dict[str, str]]] = []

    try:
        with csv_path.open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            if not reader.fieldnames:
                result.add_error("MISSING_HEADER", "CSV header row is missing.")
                return [], []

            headers = [header.strip() for header in reader.fieldnames]

            for row_number, row in enumerate(reader, start=2):
                if None in row and row[None]:
                    result.add_error(
                        "MALFORMED_ROW",
                        "Row has more columns than the header.",
                        row=row_number,
                    )
                cleaned: dict[str, str] = {}
                for key, value in row.items():
                    if key is None:
                        continue
                    cleaned[key.strip()] = (value or "").strip()
                rows.append((row_number, cleaned))
    except FileNotFoundError:
        raise
    except PermissionError:
        raise
    except UnicodeDecodeError as exc:
        result.add_error("UNREADABLE_FILE", f"Unable to decode CSV as UTF-8: {exc}")
        return [], []
    except csv.Error as exc:
        result.add_error("MALFORMED_CSV", f"CSV parse error: {exc}")
        return [], []
    except Exception as exc:  # pragma: no cover - defensive fallback
        result.add_error("READ_ERROR", f"Unexpected read error: {exc}")
        return [], []

    return headers, rows


def validate_headers(headers: list[str], result: FileValidationResult) -> None:
    header_set = set(headers)
    missing_core = [column for column in CORE_COLUMNS if column not in header_set]
    if missing_core:
        result.add_error(
            "MISSING_CORE_COLUMNS",
            "Missing required core columns.",
            value=", ".join(missing_core),
        )

    allowed_columns = set(CORE_COLUMNS) | set(EXTENSION_COLUMNS)
    for header in headers:
        if header not in allowed_columns:
            result.add_warning(
                "UNKNOWN_COLUMN",
                "Unknown extension column encountered.",
                column=header,
            )


def check_enum_value(
    row_number: int,
    row: dict[str, str],
    column: str,
    allowed_values: set[str],
    result: FileValidationResult,
) -> str:
    raw_value = row.get(column, "").strip()
    if not raw_value:
        return ""

    normalized = raw_value.upper()
    legacy_values = LEGACY_ENUMS.get(column, set())
    if normalized in legacy_values:
        result.add_warning(
            "LEGACY_ENUM_VALUE",
            f"Legacy enum value used for {column}.",
            row=row_number,
            column=column,
            value=raw_value,
        )
        return normalized

    if normalized not in allowed_values:
        result.add_error(
            "INVALID_ENUM_VALUE",
            f"Invalid enum value for {column}.",
            row=row_number,
            column=column,
            value=raw_value,
        )
        return normalized

    if raw_value != normalized:
        result.add_warning(
            "NON_CANONICAL_CASE",
            f"Non-canonical casing for {column}; expected uppercase.",
            row=row_number,
            column=column,
            value=raw_value,
        )

    return normalized


def validate_rows(
    rows: list[tuple[int, dict[str, str]]],
    result: FileValidationResult,
    execution_dependency_type_severity: str,
) -> None:
    seen_dependency_ids: set[str] = set()
    expected_from_deliverable: str | None = None
    implements_node_active_count = 0

    for row_number, row in rows:
        for column in REQUIRED_NON_EMPTY_COLUMNS:
            if not row.get(column, "").strip():
                result.add_error(
                    "REQUIRED_VALUE_MISSING",
                    "Required field is empty.",
                    row=row_number,
                    column=column,
                )

        schema_version = row.get("RegisterSchemaVersion", "").strip()
        if schema_version and schema_version != "v3.1":
            result.add_error(
                "INVALID_SCHEMA_VERSION",
                "RegisterSchemaVersion must be v3.1.",
                row=row_number,
                column="RegisterSchemaVersion",
                value=schema_version,
            )

        dependency_id = row.get("DependencyID", "").strip()
        if dependency_id:
            if not DEPENDENCY_ID_PATTERN.match(dependency_id):
                result.add_error(
                    "INVALID_DEPENDENCY_ID_FORMAT",
                    "DependencyID must match DEP-{PKG}-{DEL}-{SEQ}.",
                    row=row_number,
                    column="DependencyID",
                    value=dependency_id,
                )
            if dependency_id in seen_dependency_ids:
                result.add_error(
                    "DUPLICATE_DEPENDENCY_ID",
                    "DependencyID must be unique within file.",
                    row=row_number,
                    column="DependencyID",
                    value=dependency_id,
                )
            seen_dependency_ids.add(dependency_id)

        from_deliverable = row.get("FromDeliverableID", "").strip()
        if from_deliverable:
            if not DELIVERABLE_ID_PATTERN.match(from_deliverable):
                result.add_error(
                    "INVALID_FROM_DELIVERABLE_ID",
                    "FromDeliverableID must match DEL-XX-YY.",
                    row=row_number,
                    column="FromDeliverableID",
                    value=from_deliverable,
                )
            if expected_from_deliverable is None:
                expected_from_deliverable = from_deliverable
            elif from_deliverable != expected_from_deliverable:
                result.add_error(
                    "INCONSISTENT_FROM_DELIVERABLE",
                    "FromDeliverableID must be consistent across all rows.",
                    row=row_number,
                    column="FromDeliverableID",
                    value=from_deliverable,
                )

        normalized_enums: dict[str, str] = {}
        for column, allowed_values in ENUM_VALUES.items():
            normalized_enums[column] = check_enum_value(row_number, row, column, allowed_values, result)

        target_type = normalized_enums.get("TargetType", "")
        target_deliverable = row.get("TargetDeliverableID", "").strip()
        if target_type == "DELIVERABLE":
            if not target_deliverable:
                result.add_error(
                    "TARGET_DELIVERABLE_REQUIRED",
                    "TargetDeliverableID is required when TargetType=DELIVERABLE.",
                    row=row_number,
                    column="TargetDeliverableID",
                )
            elif not DELIVERABLE_ID_PATTERN.match(target_deliverable):
                result.add_error(
                    "INVALID_TARGET_DELIVERABLE_ID",
                    "TargetDeliverableID must match DEL-XX-YY.",
                    row=row_number,
                    column="TargetDeliverableID",
                    value=target_deliverable,
                )
        elif target_deliverable:
            result.add_error(
                "TARGET_DELIVERABLE_MUST_BE_EMPTY",
                "TargetDeliverableID must be empty when TargetType is not DELIVERABLE.",
                row=row_number,
                column="TargetDeliverableID",
                value=target_deliverable,
            )

        first_seen = row.get("FirstSeen", "").strip()
        last_seen = row.get("LastSeen", "").strip()
        if first_seen and not is_iso_date(first_seen):
            result.add_error(
                "INVALID_DATE",
                "FirstSeen must be ISO date YYYY-MM-DD.",
                row=row_number,
                column="FirstSeen",
                value=first_seen,
            )
        if last_seen and not is_iso_date(last_seen):
            result.add_error(
                "INVALID_DATE",
                "LastSeen must be ISO date YYYY-MM-DD.",
                row=row_number,
                column="LastSeen",
                value=last_seen,
            )
        if is_iso_date(first_seen) and is_iso_date(last_seen):
            if last_seen < first_seen:
                result.add_error(
                    "INVALID_DATE_ORDER",
                    "LastSeen must be greater than or equal to FirstSeen.",
                    row=row_number,
                    column="LastSeen",
                    value=last_seen,
                )

        dependency_class = normalized_enums.get("DependencyClass", "")
        anchor_type = normalized_enums.get("AnchorType", "")
        dependency_type = normalized_enums.get("DependencyType", "")
        row_status = normalized_enums.get("Status", "")

        if dependency_class == "ANCHOR":
            if anchor_type == "NOT_APPLICABLE":
                result.add_error(
                    "INVALID_ANCHOR_TYPE",
                    "ANCHOR rows must not use AnchorType=NOT_APPLICABLE.",
                    row=row_number,
                    column="AnchorType",
                )
            if dependency_type and dependency_type != "OTHER":
                result.add_error(
                    "INVALID_ANCHOR_DEPENDENCY_TYPE",
                    "ANCHOR rows must set DependencyType=OTHER.",
                    row=row_number,
                    column="DependencyType",
                    value=dependency_type,
                )

            if row_status == "ACTIVE" and anchor_type == "IMPLEMENTS_NODE":
                implements_node_active_count += 1

        if dependency_class == "EXECUTION":
            if anchor_type and anchor_type != "NOT_APPLICABLE":
                result.add_error(
                    "INVALID_EXECUTION_ANCHOR_TYPE",
                    "EXECUTION rows must set AnchorType=NOT_APPLICABLE.",
                    row=row_number,
                    column="AnchorType",
                    value=anchor_type,
                )
            if dependency_type and dependency_type not in PREFERRED_EXECUTION_DEPENDENCY_TYPES:
                message = "EXECUTION row uses non-preferred DependencyType."
                if execution_dependency_type_severity == "error":
                    result.add_error(
                        "NON_PREFERRED_EXECUTION_DEPENDENCY_TYPE",
                        message,
                        row=row_number,
                        column="DependencyType",
                        value=dependency_type,
                    )
                else:
                    result.add_warning(
                        "NON_PREFERRED_EXECUTION_DEPENDENCY_TYPE",
                        message,
                        row=row_number,
                        column="DependencyType",
                        value=dependency_type,
                    )

        if row_status == "ACTIVE":
            evidence_file = row.get("EvidenceFile", "").strip()
            source_ref = row.get("SourceRef", "").strip()
            if not evidence_file:
                result.add_error(
                    "MISSING_ACTIVE_PROVENANCE",
                    "ACTIVE rows require EvidenceFile.",
                    row=row_number,
                    column="EvidenceFile",
                )
            if not source_ref:
                result.add_error(
                    "MISSING_ACTIVE_PROVENANCE",
                    "ACTIVE rows require SourceRef.",
                    row=row_number,
                    column="SourceRef",
                )
            if not row.get("EvidenceQuote", "").strip():
                result.add_warning(
                    "EMPTY_EVIDENCE_QUOTE",
                    "ACTIVE row has empty EvidenceQuote.",
                    row=row_number,
                    column="EvidenceQuote",
                )

    if rows and implements_node_active_count != 1:
        result.add_warning(
            "IMPLEMENTS_NODE_CARDINALITY",
            "File should contain exactly one ACTIVE ANCHOR row with AnchorType=IMPLEMENTS_NODE.",
            value=str(implements_node_active_count),
        )


def validate_file(
    csv_path: Path,
    execution_dependency_type_severity: str,
) -> FileValidationResult:
    result = FileValidationResult(path=str(csv_path.resolve(strict=False)), status="PASS")
    headers, rows = read_csv_rows(csv_path, result)
    result.rows = len(rows)

    if headers:
        validate_headers(headers, result)
    if rows:
        validate_rows(rows, result, execution_dependency_type_severity)

    result.status = "FAIL" if result.errors else "PASS"
    return result


def discover_dependency_files(execution_root: Path) -> list[Path]:
    candidates = execution_root.glob("PKG-*/1_Working/DEL-*/Dependencies.csv")
    return sorted(path.resolve(strict=False) for path in candidates if path.is_file())


def render_text_report(payload: dict) -> None:
    print("Dependencies.csv v3.1 schema linter")
    print(f"Mode: {payload.get('mode')}")
    if payload.get("executionRoot"):
        print(f"Execution root: {payload.get('executionRoot')}")
    print(f"Timestamp: {payload.get('timestamp')}")

    for file_result in payload.get("files", []):
        print(
            f"\nFile: {file_result['path']}\n"
            f"  Status: {file_result['status']}\n"
            f"  Rows: {file_result['rows']}\n"
            f"  Errors: {file_result['errorCount']}\n"
            f"  Warnings: {file_result['warningCount']}"
        )
        for issue in file_result["errors"]:
            location = f"row={issue['row']}" if "row" in issue else "row=n/a"
            column = f", column={issue['column']}" if "column" in issue else ""
            value = f", value={issue['value']}" if "value" in issue else ""
            print(f"    ERROR {issue['code']} ({location}{column}{value}): {issue['message']}")
        for issue in file_result["warnings"]:
            location = f"row={issue['row']}" if "row" in issue else "row=n/a"
            column = f", column={issue['column']}" if "column" in issue else ""
            value = f", value={issue['value']}" if "value" in issue else ""
            print(f"    WARN  {issue['code']} ({location}{column}{value}): {issue['message']}")

    summary = payload.get("summary", {})
    print(
        "\nSummary:"
        f" files={summary.get('filesScanned', 0)}"
        f" pass={summary.get('passFiles', 0)}"
        f" fail={summary.get('failFiles', 0)}"
        f" error={summary.get('errorFiles', 0)}"
        f" totalErrors={summary.get('totalErrors', 0)}"
        f" totalWarnings={summary.get('totalWarnings', 0)}"
    )


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Lint Dependencies.csv files against schema v3.1.")
    parser.add_argument(
        "csv_path",
        nargs="?",
        help="Path to a single Dependencies.csv file.",
    )
    parser.add_argument(
        "--scan",
        help="Scan an execution root for Dependencies.csv files under PKG-*/1_Working/DEL-*/.",
    )
    parser.add_argument(
        "--format",
        choices=("text", "json"),
        default="text",
        help="Output format.",
    )
    parser.add_argument(
        "--execution-dependency-type-severity",
        choices=("warning", "error"),
        default="warning",
        help="Severity for non-preferred EXECUTION DependencyType values.",
    )
    args = parser.parse_args(argv)

    if bool(args.csv_path) == bool(args.scan):
        parser.error("Provide either <csv_path> or --scan <execution_root>, but not both.")

    return args


def main(argv: list[str]) -> int:
    try:
        args = parse_args(argv)
        mode = "scan" if args.scan else "single"
        execution_root: str | None = None
        files_to_check: list[Path] = []
        payload_files: list[dict] = []

        if mode == "single":
            csv_path = Path(args.csv_path).expanduser()
            if not csv_path.exists() or not csv_path.is_file():
                print(f"ERROR: File not found: {csv_path}", file=sys.stderr)
                return 2
            files_to_check = [csv_path.resolve(strict=False)]
        else:
            scan_root = Path(args.scan).expanduser()
            if not scan_root.exists() or not scan_root.is_dir():
                print(f"ERROR: Scan root not found: {scan_root}", file=sys.stderr)
                return 2
            execution_root = str(scan_root.resolve(strict=False))
            files_to_check = discover_dependency_files(scan_root)

        pass_files = 0
        fail_files = 0
        error_files = 0
        total_errors = 0
        total_warnings = 0

        for csv_path in files_to_check:
            try:
                result = validate_file(
                    csv_path=csv_path,
                    execution_dependency_type_severity=args.execution_dependency_type_severity,
                )
            except FileNotFoundError:
                result = FileValidationResult(path=str(csv_path), status="ERROR")
                result.add_error("FILE_NOT_FOUND", "Dependencies.csv file is missing.")
            except PermissionError:
                result = FileValidationResult(path=str(csv_path), status="ERROR")
                result.add_error("FILE_UNREADABLE", "Dependencies.csv is not readable.")
            except Exception as exc:  # pragma: no cover - defensive fallback
                result = FileValidationResult(path=str(csv_path), status="ERROR")
                result.add_error("INTERNAL_ERROR", f"Unexpected linter failure: {exc}")

            if result.status == "PASS":
                pass_files += 1
            elif result.status == "FAIL":
                fail_files += 1
            else:
                error_files += 1

            total_errors += len(result.errors)
            total_warnings += len(result.warnings)
            payload_files.append(result.as_dict())

        payload = {
            "tool": "validate_dependencies",
            "schemaVersion": "v3.1",
            "mode": mode,
            "executionRoot": execution_root,
            "timestamp": utc_now_iso(),
            "files": payload_files,
            "summary": {
                "filesScanned": len(payload_files),
                "passFiles": pass_files,
                "failFiles": fail_files,
                "errorFiles": error_files,
                "totalErrors": total_errors,
                "totalWarnings": total_warnings,
            },
        }

        if args.format == "json":
            print(json.dumps(payload, indent=2, sort_keys=True))
        else:
            render_text_report(payload)

        if error_files > 0:
            return 2
        if fail_files > 0:
            return 1
        return 0
    except SystemExit:
        raise
    except Exception as exc:  # pragma: no cover - defensive fallback
        print(f"ERROR: Unexpected failure: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
