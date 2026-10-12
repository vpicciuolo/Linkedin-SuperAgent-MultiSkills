#!/usr/bin/env python3
"""Validate the OYYO LinkedIn skill pack without third-party dependencies.

VINCENZO PICCIUOLO (C) 2026 HRN INNOVATION TECHNOLOGIES LTD
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

PLUGIN_ROOT = Path(__file__).resolve().parent.parent
REPO_ROOT = PLUGIN_ROOT.parents[1]
EXPECTED_VERSION = (REPO_ROOT / "VERSION").read_text(encoding="utf-8").strip()
NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def parse_frontmatter(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise ValueError("missing YAML frontmatter")
    try:
        block = text.split("---", 2)[1]
    except IndexError as exc:
        raise ValueError("unterminated YAML frontmatter") from exc
    result: dict[str, str] = {}
    for line in block.splitlines():
        match = re.match(r"^([a-zA-Z_][\w-]*):\s*[\"']?([^\"'].*?)[\"']?\s*$", line)
        if match and not line.startswith("  "):
            result[match.group(1)] = match.group(2).strip().strip('"\'')
    return result


def validate() -> list[str]:
    errors: list[str] = []
    for manifest in (PLUGIN_ROOT / "plugin.json", PLUGIN_ROOT / ".codex-plugin" / "plugin.json", PLUGIN_ROOT / ".claude-plugin" / "plugin.json"):
        try:
            data = json.loads(manifest.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            errors.append(f"{manifest}: invalid JSON: {exc}")
            continue
        if data.get("name") != "linkedin-superagent-multiskills":
            errors.append(f"{manifest}: unexpected plugin name")
        if data.get("version") != EXPECTED_VERSION:
            errors.append(f"{manifest}: version does not match {EXPECTED_VERSION}")

    skills_root = PLUGIN_ROOT / "skills"
    names: set[str] = set()
    skill_files = sorted(skills_root.glob("*/SKILL.md"))
    if len(skill_files) < 20:
        errors.append(f"expected at least 20 skills, found {len(skill_files)}")

    for path in skill_files:
        try:
            metadata = parse_frontmatter(path)
        except ValueError as exc:
            errors.append(f"{path}: {exc}")
            continue
        name = metadata.get("name", "")
        if not NAME_RE.fullmatch(name):
            errors.append(f"{path}: invalid skill name {name!r}")
        if path.parent.name != name:
            errors.append(f"{path}: folder/name mismatch")
        if name in names:
            errors.append(f"{path}: duplicate skill name")
        names.add(name)
        if not metadata.get("description"):
            errors.append(f"{path}: missing description")
        text = path.read_text(encoding="utf-8")
        if "[TODO" in text or "TODO:" in text:
            errors.append(f"{path}: unfinished TODO placeholder")
        if name != "humanizer" and "VINCENZO PICCIUOLO (C) 2026 HRN INNOVATION TECHNOLOGIES LTD" not in text:
            errors.append(f"{path}: missing requested copyright credit")

    for reference in (
        "session-and-safety.md",
        "workspace-state.md",
        "content-system.md",
        "hook-library.md",
        "profile-rubric.md",
        "analytics-schema.md",
    ):
        if not (PLUGIN_ROOT / "references" / reference).is_file():
            errors.append(f"missing reference: {reference}")

    for path in PLUGIN_ROOT.rglob("*"):
        if path.is_symlink():
            errors.append(f"symlink not allowed in distribution: {path}")
    return errors


def main() -> int:
    errors = validate()
    if errors:
        print("PACK VALIDATION FAILED")
        for error in errors:
            print(f"- {error}")
        return 1
    print("PACK VALIDATION PASSED")
    print(f"version={EXPECTED_VERSION} skills={len(list((PLUGIN_ROOT / 'skills').glob('*/SKILL.md')))}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
