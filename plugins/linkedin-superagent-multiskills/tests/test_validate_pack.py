"""Pack-level validation tests.

VINCENZO PICCIUOLO (C) 2026 HRN INNOVATION TECHNOLOGIES LTD
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path

MODULE_PATH = Path(__file__).resolve().parents[1] / "scripts" / "validate_pack.py"
SPEC = importlib.util.spec_from_file_location("validate_pack", MODULE_PATH)
assert SPEC and SPEC.loader
validator = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(validator)


class PackTests(unittest.TestCase):
    def test_pack_validates(self) -> None:
        self.assertEqual(validator.validate(), [])


if __name__ == "__main__":
    unittest.main()
