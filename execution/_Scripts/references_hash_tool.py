#!/usr/bin/env python3
"""Compute and verify content hashes for out-of-folder references."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

HASH_PATTERN = re.compile(r"^[a-f0-9]{64}$")
HASH_LINE_PATTERN = re.compile(r"^(\s*)[-*]\s+ContentHash:\s*(.*?)\s*$", re.IGNORECASE)
LINK_PATTERN = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
CODE_PATTERN = re.compile(r"`([^`]+)`")
LOCATION_PATTERN = re.compile(r"[Ll]ocation:\s*([^—]+?)(?:\s+—|$)")
URL_SCHEME_PATTERN = re.compile(r"^[a-zA-Z][a-zA-Z0-9+.-]*:")


@dataclass
class ReferenceEntry:
    index: int
    indent: str
    marker: str
    raw_path: str
    source: str
    hash_line_index: int | None
    hash_line_indent: str | None
    stored_hash: str | None
    resolved_path: Path | None
    resolution: str
    external: bool
    out_of_folder: bool


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def find_repo_root(start: Path) -> Path | None:
    for candidate in [start, *start.parents]:
        if (candidate / ".git").exists():
            return candidate
    return None


def is_path_within(base: Path, candidate: Path) -> bool:
    try:
        candidate.relative_to(base)
        return True
    except ValueError:
        return False


def sanitize_reference_path(raw_path: str) -> str:
    cleaned = raw_path.strip().strip("`").strip()
    if cleaned.endswith((".", ",", ";")):
        cleaned = cleaned[:-1]
    return cleaned


def looks_like_path(token: str) -> bool:
    candidate = token.strip()
    if not candidate:
        return False
    if candidate.startswith(("./", "../", "/", "~")):
        return True
    if "/" in candidate:
        return True
    if candidate.lower().endswith((".md", ".txt", ".csv", ".json", ".yml", ".yaml", ".py", ".ts", ".tsx", ".js", ".mjs")):
        return True
    return False


def extract_reference_path(line: str) -> tuple[str, str] | None:
    stripped = line.lstrip()
    if not re.match(r"^[-*]\s+", stripped):
        return None

    content = re.sub(r"^[-*]\s+", "", stripped, count=1).strip()

    link_match = LINK_PATTERN.search(content)
    if link_match:
        return sanitize_reference_path(link_match.group(1)), "markdown_link"

    code_match = CODE_PATTERN.search(content)
    if code_match:
        candidate = sanitize_reference_path(code_match.group(1))
        if looks_like_path(candidate):
            return candidate, "inline_code"

    location_match = LOCATION_PATTERN.search(content)
    if location_match:
        candidate = sanitize_reference_path(location_match.group(1))
        if looks_like_path(candidate):
            return candidate, "location_field"

    first_token = content.split(" ", 1)[0]
    candidate = sanitize_reference_path(first_token)
    if looks_like_path(candidate):
        return candidate, "plain_token"

    return None


def resolve_reference_path(raw_path: str, references_dir: Path, repo_root: Path | None) -> tuple[Path | None, str, bool]:
    if not raw_path:
        return None, "empty", False

    lowered = raw_path.lower()
    if lowered in {"tbd", "location tbd"}:
        return None, "placeholder", False

    if URL_SCHEME_PATTERN.match(raw_path) and not raw_path.startswith(("./", "../", "/")):
        return None, "external_url", True

    path_without_fragment = raw_path.split("#", 1)[0].split("?", 1)[0]
    candidate = Path(path_without_fragment)

    if candidate.is_absolute():
        return candidate.resolve(strict=False), "absolute", False

    refs_candidate = (references_dir / candidate).resolve(strict=False)
    if refs_candidate.exists():
        return refs_candidate, "relative_to_references", False

    if repo_root is not None:
        repo_candidate = (repo_root / candidate).resolve(strict=False)
        if repo_candidate.exists():
            return repo_candidate, "relative_to_repo_root", False

    return refs_candidate, "unresolved_relative", False


def resolve_references_target(target: Path) -> tuple[Path, Path]:
    if target.is_dir():
        references_file = target / "_REFERENCES.md"
        deliverable_dir = target
    else:
        references_file = target
        deliverable_dir = target.parent

    if references_file.name != "_REFERENCES.md":
        raise ValueError("Target must be a deliverable folder or a _REFERENCES.md file.")

    if not references_file.exists():
        raise FileNotFoundError(f"References file not found: {references_file}")

    if not references_file.is_file():
        raise ValueError(f"References path is not a file: {references_file}")

    if not deliverable_dir.is_dir():
        raise ValueError(f"Deliverable directory not found: {deliverable_dir}")

    return references_file.resolve(strict=False), deliverable_dir.resolve(strict=False)


def parse_references(lines: list[str], references_dir: Path, deliverable_dir: Path, repo_root: Path | None) -> list[ReferenceEntry]:
    entries: list[ReferenceEntry] = []

    for index, line in enumerate(lines):
        extracted = extract_reference_path(line)
        if extracted is None:
            continue

        raw_path, source = extracted
        if not raw_path:
            continue

        indent = line[: len(line) - len(line.lstrip())]
        stripped = line.lstrip()
        marker = stripped[0]
        indent_len = len(indent)

        hash_line_index: int | None = None
        hash_line_indent: str | None = None
        stored_hash: str | None = None

        scan_index = index + 1
        while scan_index < len(lines):
            probe = lines[scan_index]
            probe_stripped = probe.strip()

            if probe_stripped.startswith("## ") or probe_stripped.startswith("# "):
                break

            probe_indent = probe[: len(probe) - len(probe.lstrip())]
            probe_indent_len = len(probe_indent)
            probe_lstripped = probe.lstrip()

            is_probe_bullet = re.match(r"^[-*]\s+", probe_lstripped) is not None
            if is_probe_bullet and probe_indent_len <= indent_len:
                break

            hash_match = HASH_LINE_PATTERN.match(probe)
            if hash_match and probe_indent_len > indent_len:
                hash_line_index = scan_index
                hash_line_indent = hash_match.group(1)
                stored_hash = hash_match.group(2).strip()
                break

            scan_index += 1

        resolved_path, resolution, external = resolve_reference_path(raw_path, references_dir, repo_root)
        out_of_folder = False
        if resolved_path is not None:
            out_of_folder = not is_path_within(deliverable_dir, resolved_path)
        elif raw_path.startswith("../"):
            out_of_folder = True

        entries.append(
            ReferenceEntry(
                index=index,
                indent=indent,
                marker=marker,
                raw_path=raw_path,
                source=source,
                hash_line_index=hash_line_index,
                hash_line_indent=hash_line_indent,
                stored_hash=stored_hash,
                resolved_path=resolved_path,
                resolution=resolution,
                external=external,
                out_of_folder=out_of_folder,
            )
        )

    return entries


def hash_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def compute_hash_value(entry: ReferenceEntry) -> tuple[str | None, str]:
    if entry.external:
        return None, "SKIPPED_EXTERNAL"
    if not entry.out_of_folder:
        return None, "SKIPPED_IN_FOLDER"
    if entry.resolved_path is None:
        return "TBD", "MISSING_FILE"
    if not entry.resolved_path.exists():
        return "TBD", "MISSING_FILE"

    try:
        return hash_file(entry.resolved_path), "HASHED"
    except OSError as exc:
        return f"ERROR: {exc.__class__.__name__}", "READ_ERROR"


def apply_hash_updates(
    original_lines: list[str],
    entries: list[ReferenceEntry],
    computed_values: dict[int, str | None],
) -> tuple[list[str], int]:
    updated = list(original_lines)
    insertions = 0
    updates = 0
    delta = 0

    for entry in sorted(entries, key=lambda item: item.index):
        value = computed_values.get(entry.index)
        if value is None:
            continue

        line_index = entry.index + delta
        new_hash_line = f"{entry.indent}  - ContentHash: {value}"

        if entry.hash_line_index is not None:
            hash_index = entry.hash_line_index + delta
            if updated[hash_index] != new_hash_line:
                updated[hash_index] = new_hash_line
                updates += 1
            continue

        updated.insert(line_index + 1, new_hash_line)
        insertions += 1
        delta += 1

    return updated, insertions + updates


def make_reference_record(
    entry: ReferenceEntry,
    status: str,
    stored_hash: str | None = None,
    computed_hash: str | None = None,
    message: str | None = None,
) -> dict:
    record = {
        "reference": entry.raw_path,
        "source": entry.source,
        "status": status,
        "outOfFolder": entry.out_of_folder,
        "external": entry.external,
        "resolution": entry.resolution,
    }
    if entry.resolved_path is not None:
        record["resolvedPath"] = str(entry.resolved_path)
    if stored_hash is not None:
        record["storedHash"] = stored_hash
    if computed_hash is not None:
        record["computedHash"] = computed_hash
    if message is not None:
        record["message"] = message
    return record


def run_compute(target: Path, repo_root: Path | None, dry_run: bool) -> tuple[int, dict]:
    references_file, deliverable_dir = resolve_references_target(target)
    text = references_file.read_text(encoding="utf-8")
    has_trailing_newline = text.endswith("\n")
    lines = text.splitlines()

    effective_repo_root = repo_root or find_repo_root(references_file.parent)
    entries = parse_references(lines, references_file.parent, deliverable_dir, effective_repo_root)

    computed_values: dict[int, str | None] = {}
    records: list[dict] = []
    hashed_count = 0

    for entry in entries:
        value, status = compute_hash_value(entry)
        computed_values[entry.index] = value
        if status == "HASHED":
            hashed_count += 1
        records.append(
            make_reference_record(
                entry,
                status=status,
                stored_hash=entry.stored_hash,
                computed_hash=value,
            )
        )

    updated_lines, modifications = apply_hash_updates(lines, entries, computed_values)
    wrote_file = False
    if not dry_run and modifications > 0:
        output = "\n".join(updated_lines)
        if has_trailing_newline or output:
            output = f"{output}\n"
        references_file.write_text(output, encoding="utf-8")
        wrote_file = True

    payload = {
        "command": "compute",
        "timestamp": utc_now_iso(),
        "referencesFile": str(references_file),
        "deliverablePath": str(deliverable_dir),
        "repoRoot": str(effective_repo_root) if effective_repo_root else None,
        "dryRun": dry_run,
        "summary": {
            "referencesParsed": len(entries),
            "hashesComputed": hashed_count,
            "fileModified": wrote_file,
            "lineModifications": modifications,
        },
        "results": records,
    }
    return 0, payload


def write_bypass_record(
    deliverable_dir: Path,
    actor: str,
    reason: str,
    failed_references: list[dict],
    bypass_log: Path | None,
) -> Path:
    record_path = bypass_log or (deliverable_dir / "HASH_VERIFICATION_BYPASS.jsonl")
    record_path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "timestamp": utc_now_iso(),
        "actor": actor,
        "reason": reason,
        "failedReferences": failed_references,
    }
    with record_path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(payload, sort_keys=True))
        handle.write("\n")
    return record_path


def run_verify(
    target: Path,
    repo_root: Path | None,
    allow_bypass: bool,
    actor: str | None,
    reason: str | None,
    bypass_log: Path | None,
) -> tuple[int, dict]:
    references_file, deliverable_dir = resolve_references_target(target)
    text = references_file.read_text(encoding="utf-8")
    lines = text.splitlines()

    effective_repo_root = repo_root or find_repo_root(references_file.parent)
    entries = parse_references(lines, references_file.parent, deliverable_dir, effective_repo_root)

    records: list[dict] = []
    failed: list[dict] = []

    for entry in entries:
        if entry.external:
            record = make_reference_record(entry, "SKIPPED_EXTERNAL")
            records.append(record)
            continue
        if not entry.out_of_folder:
            record = make_reference_record(entry, "SKIPPED_IN_FOLDER")
            records.append(record)
            continue

        stored_hash = (entry.stored_hash or "").strip()
        if not stored_hash:
            record = make_reference_record(
                entry,
                "MISSING_STORED_HASH",
                message="Reference is out-of-folder but has no ContentHash field.",
            )
            records.append(record)
            failed.append(record)
            continue

        if stored_hash == "TBD":
            record = make_reference_record(
                entry,
                "UNVERIFIABLE",
                stored_hash=stored_hash,
                message="Stored hash is TBD.",
            )
            records.append(record)
            failed.append(record)
            continue

        if stored_hash.upper().startswith("ERROR:"):
            record = make_reference_record(
                entry,
                "UNVERIFIABLE",
                stored_hash=stored_hash,
                message="Stored hash is an error marker.",
            )
            records.append(record)
            failed.append(record)
            continue

        if not HASH_PATTERN.match(stored_hash):
            record = make_reference_record(
                entry,
                "INVALID_HASH_FORMAT",
                stored_hash=stored_hash,
                message="Stored hash must be lowercase hex with length 64.",
            )
            records.append(record)
            failed.append(record)
            continue

        if entry.resolved_path is None or not entry.resolved_path.exists():
            record = make_reference_record(
                entry,
                "UNVERIFIABLE",
                stored_hash=stored_hash,
                message="Referenced file not found.",
            )
            records.append(record)
            failed.append(record)
            continue

        try:
            current_hash = hash_file(entry.resolved_path)
        except OSError as exc:
            record = make_reference_record(
                entry,
                "UNVERIFIABLE",
                stored_hash=stored_hash,
                message=f"Unable to read file: {exc.__class__.__name__}",
            )
            records.append(record)
            failed.append(record)
            continue

        if current_hash == stored_hash:
            records.append(
                make_reference_record(
                    entry,
                    "PASS",
                    stored_hash=stored_hash,
                    computed_hash=current_hash,
                )
            )
            continue

        mismatch = make_reference_record(
            entry,
            "MISMATCH",
            stored_hash=stored_hash,
            computed_hash=current_hash,
            message="Stored hash does not match current file content.",
        )
        records.append(mismatch)
        failed.append(mismatch)

    bypass_record_path: Path | None = None
    verification_status = "PASS"
    exit_code = 0

    if failed:
        verification_status = "FAIL"
        exit_code = 1
        if allow_bypass:
            if not actor or not actor.strip():
                raise ValueError("Bypass requested but --actor is missing.")
            if not reason or not reason.strip():
                raise ValueError("Bypass requested but --reason is missing.")
            bypass_record_path = write_bypass_record(
                deliverable_dir=deliverable_dir,
                actor=actor.strip(),
                reason=reason.strip(),
                failed_references=failed,
                bypass_log=bypass_log,
            )
            verification_status = "BYPASSED"
            exit_code = 0

    payload = {
        "command": "verify",
        "timestamp": utc_now_iso(),
        "referencesFile": str(references_file),
        "deliverablePath": str(deliverable_dir),
        "repoRoot": str(effective_repo_root) if effective_repo_root else None,
        "summary": {
            "verificationStatus": verification_status,
            "referencesParsed": len(entries),
            "failedCount": len(failed),
            "passCount": sum(1 for record in records if record["status"] == "PASS"),
            "bypassRecorded": bypass_record_path is not None,
            "bypassLogPath": str(bypass_record_path) if bypass_record_path else None,
        },
        "results": records,
    }
    return exit_code, payload


def print_text_report(payload: dict) -> None:
    command = payload.get("command")
    summary = payload.get("summary", {})
    print(f"Command: {command}")
    print(f"References file: {payload.get('referencesFile')}")
    print(f"Deliverable path: {payload.get('deliverablePath')}")
    if command == "compute":
        print(
            "Summary:"
            f" parsed={summary.get('referencesParsed', 0)}"
            f" hashed={summary.get('hashesComputed', 0)}"
            f" modified={summary.get('lineModifications', 0)}"
            f" wrote={summary.get('fileModified', False)}"
        )
    else:
        print(
            "Summary:"
            f" status={summary.get('verificationStatus')}"
            f" pass={summary.get('passCount', 0)}"
            f" fail={summary.get('failedCount', 0)}"
            f" bypass={summary.get('bypassRecorded', False)}"
        )

    for result in payload.get("results", []):
        line = f"- [{result['status']}] {result['reference']}"
        if "message" in result:
            line += f" ({result['message']})"
        print(line)


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Compute and verify ContentHash fields for _REFERENCES.md."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    def add_common_arguments(subparser: argparse.ArgumentParser) -> None:
        subparser.add_argument(
            "target",
            help="Deliverable folder path or _REFERENCES.md path.",
        )
        subparser.add_argument(
            "--repo-root",
            help="Optional repository root for resolving repo-relative reference paths.",
        )
        subparser.add_argument(
            "--format",
            choices=("text", "json"),
            default="text",
            help="Output format.",
        )

    compute_parser = subparsers.add_parser("compute", help="Compute hashes and update _REFERENCES.md.")
    add_common_arguments(compute_parser)
    compute_parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Compute hashes without writing _REFERENCES.md.",
    )

    recompute_parser = subparsers.add_parser("recompute", help="Alias of compute.")
    add_common_arguments(recompute_parser)
    recompute_parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Compute hashes without writing _REFERENCES.md.",
    )

    verify_parser = subparsers.add_parser("verify", help="Verify stored hashes.")
    add_common_arguments(verify_parser)
    verify_parser.add_argument(
        "--allow-bypass",
        action="store_true",
        help="Allow verification bypass (records event and returns success).",
    )
    verify_parser.add_argument("--actor", help="Bypass actor identity.")
    verify_parser.add_argument("--reason", help="Bypass reason.")
    verify_parser.add_argument(
        "--bypass-log",
        help="Optional path for bypass log JSONL file (defaults to deliverable-local log).",
    )

    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    try:
        args = parse_args(argv)
        target = Path(args.target).expanduser()
        repo_root = Path(args.repo_root).expanduser().resolve(strict=False) if args.repo_root else None

        if args.command in {"compute", "recompute"}:
            exit_code, payload = run_compute(target, repo_root, args.dry_run)
        else:
            bypass_log = Path(args.bypass_log).expanduser() if args.bypass_log else None
            exit_code, payload = run_verify(
                target=target,
                repo_root=repo_root,
                allow_bypass=args.allow_bypass,
                actor=args.actor,
                reason=args.reason,
                bypass_log=bypass_log,
            )

        if args.format == "json":
            print(json.dumps(payload, indent=2, sort_keys=True))
        else:
            print_text_report(payload)
        return exit_code
    except FileNotFoundError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    except Exception as exc:  # pragma: no cover - defensive fallback
        print(f"ERROR: Unexpected failure: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
