#!/usr/bin/env python3
"""Install OYYO LinkedIn skills into any local Agent Skills directory.

VINCENZO PICCIUOLO (C) 2026 HRN INNOVATION TECHNOLOGIES LTD
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path

PLUGIN_ROOT = Path(__file__).resolve().parent.parent
SKILLS_ROOT = PLUGIN_ROOT / "skills"


def install(target: Path, force: bool = False) -> dict[str, list[str]]:
    target = target.expanduser().resolve()
    target.mkdir(parents=True, exist_ok=True)
    installed: list[str] = []
    skipped: list[str] = []
    for source in sorted(path for path in SKILLS_ROOT.iterdir() if path.is_dir()):
        destination = target / source.name
        if destination.exists():
            if not force:
                skipped.append(source.name)
                continue
            shutil.rmtree(destination)
        shutil.copytree(source, destination)
        installed.append(source.name)
    return {"target": [str(target)], "installed": installed, "skipped": skipped}


def main() -> int:
    parser = argparse.ArgumentParser(description="Install OYYO LinkedIn skills locally")
    parser.add_argument("--target", type=Path, required=True, help="destination Agent Skills directory")
    parser.add_argument("--force", action="store_true", help="replace existing skill folders")
    args = parser.parse_args()
    result = install(args.target, force=args.force)
    print(f"Target: {result['target'][0]}")
    print(f"Installed: {len(result['installed'])}")
    print(f"Skipped: {len(result['skipped'])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
