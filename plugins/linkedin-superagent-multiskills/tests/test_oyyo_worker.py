"""Tests for the OYYO LinkedIn worker contract.

VINCENZO PICCIUOLO (C) 2026 HRN INNOVATION TECHNOLOGIES LTD
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path

MODULE_PATH = Path(__file__).resolve().parents[1] / "scripts" / "oyyo_worker.py"
TEST_TEMP_ROOT = Path(__file__).resolve().parent / ".tmp"
TEST_TEMP_ROOT.mkdir(exist_ok=True)
SPEC = importlib.util.spec_from_file_location("oyyo_worker", MODULE_PATH)
assert SPEC and SPEC.loader
worker = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = worker
SPEC.loader.exec_module(worker)


class ModeTests(unittest.TestCase):
    def test_default_is_manual_read(self) -> None:
        with tempfile.TemporaryDirectory(dir=TEST_TEMP_ROOT) as directory:
            config = worker.load_config(Path(directory))
        self.assertEqual(config["mode"], "manual")
        self.assertEqual(config["scope"], "read")

    def test_automatic_requires_risk_acknowledgement(self) -> None:
        with tempfile.TemporaryDirectory(dir=TEST_TEMP_ROOT) as directory:
            root = Path(directory)
            with self.assertRaisesRegex(ValueError, "acknowledge-risk"):
                worker.set_mode(root, "automatic", "manage")
            config = worker.set_mode(root, "automatic", "manage", acknowledge_risk=True)
        self.assertTrue(config["automatic"]["risk_acknowledged"])

    def test_api_scopes_are_recorded_without_token_values(self) -> None:
        with tempfile.TemporaryDirectory(dir=TEST_TEMP_ROOT) as directory:
            root = Path(directory)
            config = worker.set_mode(
                root,
                "api",
                "publish",
                api_scopes=["w_member_social", "openid", "w_member_social"],
            )
            report = worker.doctor(root)
        self.assertEqual(config["api"]["granted_scopes"], ["openid", "w_member_social"])
        scope_check = next(item for item in report["checks"] if item["name"] == "api_scope_note")
        self.assertTrue(scope_check["ok"])


class QueueTests(unittest.TestCase):
    def test_write_requires_scope_and_approval(self) -> None:
        with tempfile.TemporaryDirectory(dir=TEST_TEMP_ROOT) as directory:
            root = Path(directory)
            worker.set_mode(root, "manual", "read")
            with self.assertRaisesRegex(ValueError, "scope 'publish'"):
                worker.add_action(root, "publish_post", "Publish launch post")

            worker.set_mode(root, "manual", "publish")
            action = worker.add_action(root, "publish_post", "Publish launch post")
            self.assertEqual(action["status"], "pending_approval")
            with self.assertRaisesRegex(ValueError, "ready or approved"):
                worker.finish_action(root, action["id"], "succeeded")

            approved = worker.approve_action(root, action["id"])
            self.assertEqual(approved["status"], "approved")
            finished = worker.finish_action(root, action["id"], "succeeded", "Published")
            self.assertEqual(finished["status"], "succeeded")
            self.assertTrue(worker.receipts_path(root).is_file())

    def test_read_action_is_ready(self) -> None:
        with tempfile.TemporaryDirectory(dir=TEST_TEMP_ROOT) as directory:
            root = Path(directory)
            worker.set_mode(root, "manual", "read")
            action = worker.add_action(root, "account_audit", "Audit current account")
            self.assertEqual(action["status"], "ready")
            finished = worker.finish_action(root, action["id"], "succeeded")
            self.assertEqual(finished["status"], "succeeded")


if __name__ == "__main__":
    unittest.main()
