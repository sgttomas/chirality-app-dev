import hashlib
import json
import subprocess
import sys
import tempfile
from pathlib import Path
from unittest import TestCase


SCRIPT_PATH = Path(__file__).resolve().parents[1] / "references_hash_tool.py"


class ReferencesHashToolTest(TestCase):
    def run_script(self, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(SCRIPT_PATH), *args],
            text=True,
            capture_output=True,
            check=False,
        )

    def test_compute_adds_hash_for_out_of_folder_reference(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            repo_root = Path(tmp_dir) / "repo"
            references_dir = repo_root / "execution" / "PKG-08_Test" / "1_Working" / "DEL-08-01_Test"
            docs_dir = repo_root / "docs"
            docs_dir.mkdir(parents=True)
            references_dir.mkdir(parents=True)
            (repo_root / ".git").mkdir()

            source_file = docs_dir / "PLAN.md"
            source_file.write_text("PLAN CONTENT\n", encoding="utf-8")
            (references_dir / "local.txt").write_text("LOCAL\n", encoding="utf-8")

            references_file = references_dir / "_REFERENCES.md"
            references_file.write_text(
                "\n".join(
                    [
                        "# References — DEL-08-01",
                        "",
                        "## Decomposition",
                        "- [Plan](../../../../docs/PLAN.md)",
                        "",
                        "## Local",
                        "- `./local.txt`",
                        "",
                    ]
                ),
                encoding="utf-8",
            )

            completed = self.run_script(
                "compute",
                str(references_dir),
                "--repo-root",
                str(repo_root),
                "--format",
                "json",
            )
            self.assertEqual(completed.returncode, 0, msg=completed.stderr)
            payload = json.loads(completed.stdout)
            self.assertGreaterEqual(payload["summary"]["hashesComputed"], 1)

            expected_hash = hashlib.sha256(source_file.read_bytes()).hexdigest()
            updated_text = references_file.read_text(encoding="utf-8")
            self.assertIn(f"ContentHash: {expected_hash}", updated_text)
            self.assertNotIn("ContentHash: LOCAL", updated_text)

    def test_verify_detects_mismatch_and_records_bypass(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            repo_root = Path(tmp_dir) / "repo"
            references_dir = repo_root / "execution" / "PKG-08_Test" / "1_Working" / "DEL-08-01_Test"
            docs_dir = repo_root / "docs"
            docs_dir.mkdir(parents=True)
            references_dir.mkdir(parents=True)
            (repo_root / ".git").mkdir()

            source_file = docs_dir / "CONTRACT.md"
            source_file.write_text("baseline\n", encoding="utf-8")
            references_file = references_dir / "_REFERENCES.md"
            references_file.write_text(
                "\n".join(
                    [
                        "# References — DEL-08-01",
                        "",
                        "## Applicable References",
                        "- [Contract](../../../../docs/CONTRACT.md)",
                        "",
                    ]
                ),
                encoding="utf-8",
            )

            compute = self.run_script(
                "compute",
                str(references_file),
                "--repo-root",
                str(repo_root),
                "--format",
                "json",
            )
            self.assertEqual(compute.returncode, 0, msg=compute.stderr)

            source_file.write_text("changed\n", encoding="utf-8")

            verify_fail = self.run_script(
                "verify",
                str(references_file),
                "--repo-root",
                str(repo_root),
                "--format",
                "json",
            )
            self.assertEqual(verify_fail.returncode, 1, msg=verify_fail.stderr)
            fail_payload = json.loads(verify_fail.stdout)
            self.assertEqual(fail_payload["summary"]["verificationStatus"], "FAIL")
            self.assertGreaterEqual(fail_payload["summary"]["failedCount"], 1)

            bypass_log = references_dir / "custom_bypass.jsonl"
            verify_bypass = self.run_script(
                "verify",
                str(references_file),
                "--repo-root",
                str(repo_root),
                "--allow-bypass",
                "--actor",
                "test-suite",
                "--reason",
                "intentional update",
                "--bypass-log",
                str(bypass_log),
                "--format",
                "json",
            )
            self.assertEqual(verify_bypass.returncode, 0, msg=verify_bypass.stderr)
            bypass_payload = json.loads(verify_bypass.stdout)
            self.assertEqual(bypass_payload["summary"]["verificationStatus"], "BYPASSED")
            self.assertTrue(bypass_log.exists())

            logged_entry = json.loads(bypass_log.read_text(encoding="utf-8").splitlines()[-1])
            self.assertEqual(logged_entry["actor"], "test-suite")
            self.assertEqual(logged_entry["reason"], "intentional update")
