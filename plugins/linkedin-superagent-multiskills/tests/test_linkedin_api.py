"""Tests for the official LinkedIn API adapter payloads.

VINCENZO PICCIUOLO (C) 2026 HRN INNOVATION TECHNOLOGIES LTD
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import importlib.util
import io
import os
import sys
import unittest
from contextlib import redirect_stderr
from pathlib import Path
from unittest.mock import patch

MODULE_PATH = Path(__file__).resolve().parents[1] / "scripts" / "linkedin_api.py"
SPEC = importlib.util.spec_from_file_location("linkedin_api", MODULE_PATH)
assert SPEC and SPEC.loader
linkedin_api = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = linkedin_api
SPEC.loader.exec_module(linkedin_api)


class PayloadTests(unittest.TestCase):
    def test_text_post_payload(self) -> None:
        payload = linkedin_api.build_text_post("urn:li:person:123", "  hello  ")
        self.assertEqual(payload["commentary"], "hello")
        self.assertEqual(payload["author"], "urn:li:person:123")
        self.assertEqual(payload["distribution"]["feedDistribution"], "MAIN_FEED")

    def test_comment_payload(self) -> None:
        payload = linkedin_api.build_comment(
            "urn:li:person:123", "urn:li:activity:456", "Useful point"
        )
        self.assertEqual(payload["message"]["text"], "Useful point")

    def test_social_headers_require_yyyymm(self) -> None:
        with self.assertRaisesRegex(ValueError, "YYYYMM"):
            linkedin_api.social_headers("secret", "2026-10")


class SafetyTests(unittest.TestCase):
    def test_live_write_requires_confirmation_before_environment(self) -> None:
        with patch.dict(os.environ, {}, clear=True), patch.object(
            linkedin_api, "require_confirmation", wraps=linkedin_api.require_confirmation
        ) as confirmation:
            with redirect_stderr(io.StringIO()):
                result = linkedin_api.main(["publish-text", "hello", "--text"])
        self.assertEqual(result, 2)
        confirmation.assert_called_once_with(False)


if __name__ == "__main__":
    unittest.main()
