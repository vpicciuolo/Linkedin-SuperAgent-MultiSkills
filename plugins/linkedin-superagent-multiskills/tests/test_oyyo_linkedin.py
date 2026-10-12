"""Tests for local OYYO LinkedIn utilities.

VINCENZO PICCIUOLO (C) 2026 HRN INNOVATION TECHNOLOGIES LTD
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import csv
import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path

MODULE_PATH = Path(__file__).resolve().parents[1] / "scripts" / "oyyo_linkedin.py"
TEST_TEMP_ROOT = Path(__file__).resolve().parent / ".tmp"
TEST_TEMP_ROOT.mkdir(exist_ok=True)
SPEC = importlib.util.spec_from_file_location("oyyo_linkedin", MODULE_PATH)
assert SPEC and SPEC.loader
oyyo = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = oyyo
SPEC.loader.exec_module(oyyo)


class CreditTests(unittest.TestCase):
    def test_credit_contains_required_identity_and_links(self) -> None:
        banner = oyyo.credit_banner()
        self.assertIn("VINCENZO PICCIUOLO (C) 2026 HRN INNOVATION TECHNOLOGIES LTD", banner)
        self.assertIn("https://github.com/vpicciuolo/", banner)
        self.assertIn("https://hrn.ae/githubsupport", banner)


class WorkspaceTests(unittest.TestCase):
    def test_init_creates_and_then_preserves_files(self) -> None:
        with tempfile.TemporaryDirectory(dir=TEST_TEMP_ROOT) as directory:
            target = Path(directory) / ".oyyo-linkedin"
            first = oyyo.initialize_workspace(target)
            self.assertEqual(len(first["created"]), len(oyyo.TEMPLATE_FILES))
            profile = target / "profile.md"
            profile.write_text("user content", encoding="utf-8")
            second = oyyo.initialize_workspace(target)
            self.assertEqual(profile.read_text(encoding="utf-8"), "user content")
            self.assertIn(str(profile), second["skipped"])


class LintTests(unittest.TestCase):
    def test_placeholder_blocks_publish(self) -> None:
        report = oyyo.lint_text("We saved {{NEEDS INPUT: hours}} last week.")
        self.assertEqual(report["status"], "BLOCKED")

    def test_clean_copy_is_ready(self) -> None:
        report = oyyo.lint_text("We reduced review time from 4 hours to 45 minutes. Here is the checklist we used.")
        self.assertEqual(report["status"], "READY")

    def test_invisible_character_requires_review(self) -> None:
        report = oyyo.lint_text("A zero-width\u200bspace is here.")
        self.assertEqual(report["status"], "REVIEW")


class AnalyticsTests(unittest.TestCase):
    def write_csv(self, directory: str) -> Path:
        path = Path(directory) / "analytics.csv"
        with path.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(
                handle,
                fieldnames=["Post title", "Views", "Likes", "Comments", "Shares", "Format", "Pillar"],
            )
            writer.writeheader()
            writer.writerow({"Post title": "A", "Views": "1,000", "Likes": "40", "Comments": "10", "Shares": "5", "Format": "Text", "Pillar": "Proof"})
            writer.writerow({"Post title": "B", "Views": "500", "Likes": "10", "Comments": "20", "Shares": "0", "Format": "Text", "Pillar": "Opinion"})
            writer.writerow({"Post title": "C", "Views": "", "Likes": "1", "Comments": "1", "Shares": "0", "Format": "Video", "Pillar": "Proof"})
        return path

    def test_aliases_rates_and_missing_rows(self) -> None:
        with tempfile.TemporaryDirectory(dir=TEST_TEMP_ROOT) as directory:
            report = oyyo.analyze_csv(self.write_csv(directory))
        self.assertEqual(report["summary"]["rows"], 3)
        self.assertEqual(report["summary"]["valid_impression_rows"], 2)
        self.assertEqual(report["summary"]["excluded_rows"], [3])
        self.assertEqual(report["rankings"]["engagement_rate"][0]["title"], "B")

    def test_missing_impressions_header_is_an_error(self) -> None:
        with tempfile.TemporaryDirectory(dir=TEST_TEMP_ROOT) as directory:
            path = Path(directory) / "bad.csv"
            path.write_text("title,likes\nA,2\n", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "impressions"):
                oyyo.analyze_csv(path)


if __name__ == "__main__":
    unittest.main()
