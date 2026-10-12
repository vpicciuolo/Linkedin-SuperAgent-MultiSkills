"""Tests for portable OYYO LinkedIn distributions.

VINCENZO PICCIUOLO (C) 2026 HRN INNOVATION TECHNOLOGIES LTD
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import importlib.util
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

TEST_TEMP_ROOT = Path(__file__).resolve().parent / ".tmp"
TEST_TEMP_ROOT.mkdir(exist_ok=True)


def load_script(name: str):
    path = Path(__file__).resolve().parents[1] / "scripts" / name
    spec = importlib.util.spec_from_file_location(path.stem, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


distribution = load_script("build_distribution.py")
installer = load_script("install_skills.py")


class DistributionTests(unittest.TestCase):
    def test_portable_bundle_contains_every_skill_and_credit(self) -> None:
        bundle = distribution.portable_bundle()
        skills = sorted((distribution.PLUGIN_ROOT / "skills").glob("*/SKILL.md"))
        for skill in skills:
            self.assertIn(f"Skill file: {skill.parent.name}/SKILL.md", bundle)
        self.assertIn("VINCENZO PICCIUOLO (C) 2026 HRN INNOVATION TECHNOLOGIES LTD", bundle)
        self.assertIn("LinkedIn automation warning", bundle)

    def test_zip_has_one_plugin_root_and_manifest(self) -> None:
        with tempfile.TemporaryDirectory(dir=TEST_TEMP_ROOT) as directory:
            result = distribution.build(Path(directory))
            with zipfile.ZipFile(result["plugin_zip"]) as archive:
                names = archive.namelist()
        self.assertIn(
            "linkedin-superagent-multiskills/.codex-plugin/plugin.json",
            names,
        )
        self.assertTrue(all(name.startswith("linkedin-superagent-multiskills/") for name in names))


class InstallerTests(unittest.TestCase):
    def test_installs_and_preserves_existing_skills(self) -> None:
        with tempfile.TemporaryDirectory(dir=TEST_TEMP_ROOT) as directory:
            target = Path(directory) / "skills"
            first = installer.install(target)
            second = installer.install(target)
        self.assertEqual(len(first["installed"]), 24)
        self.assertEqual(len(second["skipped"]), 24)


if __name__ == "__main__":
    unittest.main()
