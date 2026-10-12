#!/usr/bin/env python3
"""Local utilities for OYYO LinkedIn SuperAgent MultiSkills.

VINCENZO PICCIUOLO (C) 2026 HRN INNOVATION TECHNOLOGIES LTD
SPDX-License-Identifier: MIT

No network calls, telemetry, account access, or third-party dependencies.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import re
import shutil
import statistics
import sys
import unicodedata
from collections import defaultdict
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Iterable

VERSION = "2.0.0"
COPYRIGHT = "VINCENZO PICCIUOLO (C) 2026 HRN INNOVATION TECHNOLOGIES LTD"
PROJECT_URL = "https://github.com/vpicciuolo/Linkedin-SuperAgent-MultiSkills"
SUPPORT_URL = "https://hrn.ae/githubsupport"
PLUGIN_ROOT = Path(__file__).resolve().parent.parent
TEMPLATES = PLUGIN_ROOT / "templates"

TEMPLATE_FILES = (
    "profile.md",
    "voice.md",
    "story-bank.md",
    "strategy.md",
    "calendar.md",
    "content-log.csv",
    "evidence-ledger.csv",
)


def credit_banner() -> str:
    return "\n".join(
        (
            f"OYYO ONE AI | LinkedIn SuperAgent MultiSkills {VERSION}",
            f"Created by {COPYRIGHT}",
            "https://github.com/vpicciuolo/ | https://hrn.ae | https://oyyo.one",
            "Free and open source under MIT.",
            f"Star: {PROJECT_URL}",
            f"Support: {SUPPORT_URL}",
        )
    )


def initialize_workspace(target: Path, force: bool = False) -> dict[str, list[str]]:
    target = target.expanduser().resolve()
    target.mkdir(parents=True, exist_ok=True)
    created: list[str] = []
    skipped: list[str] = []
    for name in TEMPLATE_FILES:
        source = TEMPLATES / name
        destination = target / name
        if destination.exists() and not force:
            skipped.append(str(destination))
            continue
        shutil.copy2(source, destination)
        created.append(str(destination))
    return {"created": created, "skipped": skipped}


def text_stats(text: str) -> dict[str, int]:
    clean = text.rstrip("\r\n")
    return {
        "characters": len(clean),
        "words": len(re.findall(r"\b[^\W_]+(?:['’][^\W_]+)?\b", clean, re.UNICODE)),
        "lines": 0 if not clean else clean.count("\n") + 1,
        "paragraphs": len([p for p in re.split(r"\n\s*\n", clean) if p.strip()]),
        "utf8_bytes": len(clean.encode("utf-8")),
    }


@dataclass(frozen=True)
class Finding:
    severity: str
    code: str
    message: str
    count: int = 1


AI_TELL_PATTERNS: tuple[tuple[str, str, re.Pattern[str]], ...] = (
    (
        "staged-contrast",
        "A not-X-but-Y contrast may add drama without adding information.",
        re.compile(r"\b(?:not just|not only|not merely)\b.{0,90}\bbut\b", re.I | re.S),
    ),
    (
        "dramatic-closer",
        "A stock dramatic closer is present.",
        re.compile(r"(?im)^\s*(?:let that sink in|read that again|that is the real win)\.?\s*$"),
    ),
    (
        "generic-opener",
        "A staged or generic opener is present.",
        re.compile(r"(?i)\b(?:let's dive in|here's what you need to know|in today's fast-paced world)\b"),
    ),
    (
        "engagement-bait",
        "A generic engagement prompt is present.",
        re.compile(r"(?im)^\s*(?:thoughts|agree|who else)\??\s*$"),
    ),
    (
        "generic-praise",
        "Generic praise may read as an automated comment.",
        re.compile(r"(?i)\b(?:great post|love this|so true|this resonates)\b"),
    ),
)


def lint_text(text: str, max_chars: int = 3000) -> dict[str, Any]:
    stats = text_stats(text)
    findings: list[Finding] = []

    placeholders = re.findall(r"\{\{\s*[^{}]+\s*\}\}", text)
    if placeholders:
        findings.append(
            Finding(
                "error",
                "unresolved-placeholder",
                "Resolve every {{...}} placeholder before publishing.",
                len(placeholders),
            )
        )

    invisible = [c for c in text if unicodedata.category(c) == "Cf"]
    if invisible:
        findings.append(
            Finding(
                "warning",
                "invisible-format-character",
                "Invisible Unicode format characters are present; review and remove them.",
                len(invisible),
            )
        )

    if stats["characters"] > max_chars:
        findings.append(
            Finding(
                "error",
                "configured-character-limit",
                f"Text exceeds the configured {max_chars}-character limit by "
                f"{stats['characters'] - max_chars} characters.",
            )
        )

    hashtags = re.findall(r"(?<!\w)#[\w-]+", text, re.UNICODE)
    if len(hashtags) > 5:
        findings.append(
            Finding(
                "warning",
                "hashtag-wall",
                "More than five hashtags may distract from the message.",
                len(hashtags),
            )
        )

    urls = re.findall(r"https?://[^\s)\]]+", text)
    if len(urls) > 1:
        findings.append(
            Finding(
                "info",
                "multiple-links",
                "Multiple links are present; confirm that each one serves the stated goal.",
                len(urls),
            )
        )

    em_dashes = text.count("—")
    if em_dashes >= 2:
        findings.append(
            Finding(
                "warning",
                "dash-density",
                "Several em dashes may create a repetitive AI-like rhythm.",
                em_dashes,
            )
        )

    for code, message, pattern in AI_TELL_PATTERNS:
        count = len(pattern.findall(text))
        if count:
            findings.append(Finding("warning", code, message, count))

    errors = sum(f.severity == "error" for f in findings)
    warnings = sum(f.severity == "warning" for f in findings)
    status = "BLOCKED" if errors else ("REVIEW" if warnings else "READY")
    return {
        "status": status,
        "stats": stats,
        "findings": [asdict(f) for f in findings],
        "configured_max_characters": max_chars,
        "note": "This is an editorial lint, not an AI-authorship detector.",
    }


ALIASES: dict[str, tuple[str, ...]] = {
    "title": ("title", "post", "post title", "hook", "content"),
    "date": ("published_at", "published at", "date", "created at", "created_at"),
    "format": ("format", "post format", "content type", "type"),
    "pillar": ("pillar", "content pillar", "theme", "topic"),
    "goal": ("goal", "objective"),
    "impressions": ("impressions", "views", "post impressions"),
    "reactions": ("reactions", "likes"),
    "comments": ("comments",),
    "reposts": ("reposts", "shares"),
    "saves": ("saves", "bookmarks"),
    "sends": ("sends", "shares in messages"),
    "profile_views": ("profile_views", "profile views"),
    "follows": ("follows", "new followers", "followers gained"),
    "leads": ("leads", "qualified leads"),
    "followers": ("followers", "follower count"),
}

NUMERIC_FIELDS = {
    "impressions",
    "reactions",
    "comments",
    "reposts",
    "saves",
    "sends",
    "profile_views",
    "follows",
    "leads",
    "followers",
}


def normalize_header(value: str) -> str:
    return re.sub(r"\s+", " ", value.strip().lower().replace("-", " ").replace("_", " "))


def build_header_map(fieldnames: Iterable[str]) -> dict[str, str]:
    normalized = {normalize_header(name): name for name in fieldnames if name is not None}
    result: dict[str, str] = {}
    for canonical, aliases in ALIASES.items():
        for alias in aliases:
            match = normalized.get(normalize_header(alias))
            if match is not None:
                result[canonical] = match
                break
    return result


def parse_number(value: Any) -> float | None:
    if value is None:
        return None
    raw = str(value).strip()
    if not raw or raw.lower() in {"n/a", "na", "null", "none", "-"}:
        return None
    negative = raw.startswith("(") and raw.endswith(")")
    cleaned = re.sub(r"[^0-9.+-]", "", raw)
    if cleaned in {"", ".", "+", "-"}:
        return None
    try:
        number = float(cleaned)
    except ValueError:
        return None
    return -number if negative else number


def safe_rate(numerator: float | None, denominator: float | None) -> float | None:
    if numerator is None or denominator is None or denominator <= 0:
        return None
    return numerator / denominator


def median(values: Iterable[float | None]) -> float | None:
    present = [value for value in values if value is not None and math.isfinite(value)]
    return statistics.median(present) if present else None


def analyze_csv(path: Path, follower_override: float | None = None) -> dict[str, Any]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        if not reader.fieldnames:
            raise ValueError("CSV has no header row")
        header_map = build_header_map(reader.fieldnames)
        if "impressions" not in header_map:
            raise ValueError("CSV needs an impressions or views column")
        raw_rows = list(reader)

    rows: list[dict[str, Any]] = []
    for index, raw in enumerate(raw_rows, start=1):
        row: dict[str, Any] = {"row": index}
        for canonical, source in header_map.items():
            value = raw.get(source)
            row[canonical] = parse_number(value) if canonical in NUMERIC_FIELDS else (value or "").strip()

        engagement_components = [row.get("reactions"), row.get("comments"), row.get("reposts")]
        known_engagement = [value for value in engagement_components if value is not None]
        engagement = sum(known_engagement) if known_engagement else None
        impressions = row.get("impressions")
        followers = follower_override if follower_override is not None else row.get("followers")

        row["engagements"] = engagement
        row["engagement_rate"] = safe_rate(engagement, impressions)
        row["conversation_rate"] = safe_rate(row.get("comments"), impressions)
        row["amplification_rate"] = safe_rate(row.get("reposts"), impressions)
        row["save_rate"] = safe_rate(row.get("saves"), impressions)
        row["reach_multiple"] = safe_rate(impressions, followers)
        row["follow_conversion"] = safe_rate(row.get("follows"), row.get("profile_views"))
        row["lead_rate"] = safe_rate(row.get("leads"), impressions)
        rows.append(row)

    valid = [row for row in rows if row.get("impressions") is not None and row["impressions"] > 0]
    excluded = [row["row"] for row in rows if row not in valid]

    rate_fields = (
        "engagement_rate",
        "conversation_rate",
        "amplification_rate",
        "save_rate",
        "reach_multiple",
        "follow_conversion",
        "lead_rate",
    )
    summary: dict[str, Any] = {
        "rows": len(rows),
        "valid_impression_rows": len(valid),
        "excluded_rows": excluded,
        "recognized_columns": sorted(header_map),
        "median_impressions": median(row.get("impressions") for row in valid),
    }
    for field in rate_fields:
        summary[f"median_{field}"] = median(row.get(field) for row in valid)

    rankings: dict[str, list[dict[str, Any]]] = {}
    for field in rate_fields:
        ranked = sorted(
            (row for row in valid if row.get(field) is not None),
            key=lambda item: item[field],
            reverse=True,
        )
        rankings[field] = [
            {
                "row": row["row"],
                "title": row.get("title") or f"Row {row['row']}",
                "value": row[field],
                "impressions": row.get("impressions"),
            }
            for row in ranked[:5]
        ]

    groups: dict[str, dict[str, dict[str, Any]]] = {}
    for dimension in ("format", "pillar", "goal"):
        if dimension not in header_map:
            continue
        buckets: dict[str, list[dict[str, Any]]] = defaultdict(list)
        for row in valid:
            label = str(row.get(dimension) or "(blank)").strip()
            buckets[label].append(row)
        groups[dimension] = {
            label: {
                "n": len(items),
                "median_impressions": median(item.get("impressions") for item in items),
                "median_engagement_rate": median(item.get("engagement_rate") for item in items),
                "median_conversation_rate": median(item.get("conversation_rate") for item in items),
            }
            for label, items in sorted(buckets.items())
        }

    return {"summary": summary, "rankings": rankings, "groups": groups, "rows": rows}


def format_rate(value: float | None) -> str:
    return "n/a" if value is None else f"{value * 100:.2f}%"


def render_analytics(report: dict[str, Any]) -> str:
    summary = report["summary"]
    lines = [
        "LINKEDIN CONTENT ANALYSIS",
        f"Rows: {summary['rows']} · usable impressions: {summary['valid_impression_rows']}",
        f"Median impressions: {summary['median_impressions'] if summary['median_impressions'] is not None else 'n/a'}",
        f"Median engagement rate: {format_rate(summary['median_engagement_rate'])}",
        f"Median conversation rate: {format_rate(summary['median_conversation_rate'])}",
    ]
    if summary["excluded_rows"]:
        lines.append("Excluded rows with missing/zero impressions: " + ", ".join(map(str, summary["excluded_rows"])))

    ranking = report["rankings"].get("engagement_rate", [])
    if ranking:
        lines.extend(("", "TOP BY ENGAGEMENT RATE"))
        for item in ranking:
            lines.append(
                f"{item['row']:>3}  {format_rate(item['value']):>8}  "
                f"{item['impressions']:>10g} impressions  {item['title'][:70]}"
            )

    for dimension, groups in report["groups"].items():
        lines.extend(("", f"BY {dimension.upper()}"))
        for label, values in groups.items():
            caveat = " (small sample)" if values["n"] < 3 else ""
            lines.append(
                f"{label}: n={values['n']}, median engagement "
                f"{format_rate(values['median_engagement_rate'])}{caveat}"
            )

    lines.extend(("", "Treat patterns as hypotheses; observational results do not prove causation."))
    return "\n".join(lines)


def read_text_argument(value: str, literal: bool) -> str:
    if literal:
        return value
    if value == "-":
        return sys.stdin.read()
    return Path(value).read_text(encoding="utf-8")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Local tools for OYYO LinkedIn SuperAgent MultiSkills")
    parser.add_argument("--version", action="version", version=VERSION)
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("welcome", help="show project credits and support links")

    init_parser = sub.add_parser("init", help="initialize local workspace state")
    init_parser.add_argument("--target", type=Path, default=Path.cwd() / ".oyyo-linkedin")
    init_parser.add_argument("--force", action="store_true")
    init_parser.add_argument("--json", action="store_true")

    count_parser = sub.add_parser("count", help="count text characters, words, and paragraphs")
    count_parser.add_argument("input", help="file path, - for stdin, or literal text with --text")
    count_parser.add_argument("--text", action="store_true", help="treat input as literal text")
    count_parser.add_argument("--json", action="store_true")

    lint_parser = sub.add_parser("lint", help="run a deterministic pre-publish editorial check")
    lint_parser.add_argument("input", help="file path, - for stdin, or literal text with --text")
    lint_parser.add_argument("--text", action="store_true", help="treat input as literal text")
    lint_parser.add_argument("--max-chars", type=int, default=3000)
    lint_parser.add_argument("--json", action="store_true")
    lint_parser.add_argument("--strict", action="store_true", help="return non-zero for warnings")

    analytics_parser = sub.add_parser("analytics", help="analyze a LinkedIn content CSV export")
    analytics_parser.add_argument("csv_file", type=Path)
    analytics_parser.add_argument("--followers", type=float)
    analytics_parser.add_argument("--json", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    if args.command == "welcome":
        print(credit_banner())
        return 0

    if args.command == "init":
        result = initialize_workspace(args.target, force=args.force)
        if args.json:
            print(json.dumps(result, indent=2))
        else:
            print(credit_banner())
            print(f"\nWorkspace: {args.target.expanduser().resolve()}")
            print(f"Created: {len(result['created'])} | Skipped: {len(result['skipped'])}")
        return 0

    if args.command == "count":
        result = text_stats(read_text_argument(args.input, args.text))
        print(json.dumps(result, indent=2) if args.json else " | ".join(f"{k}: {v}" for k, v in result.items()))
        return 0

    if args.command == "lint":
        result = lint_text(read_text_argument(args.input, args.text), max_chars=args.max_chars)
        if args.json:
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            print(f"{result['status']} | {result['stats']['characters']} characters")
            for finding in result["findings"]:
                print(f"[{finding['severity'].upper()}] {finding['code']}: {finding['message']} ({finding['count']}x)")
            print(result["note"])
        if result["status"] == "BLOCKED" or (args.strict and result["status"] == "REVIEW"):
            return 1
        return 0

    if args.command == "analytics":
        try:
            result = analyze_csv(args.csv_file, follower_override=args.followers)
        except (OSError, ValueError, csv.Error) as exc:
            print(f"error: {exc}", file=sys.stderr)
            return 2
        print(json.dumps(result, indent=2, ensure_ascii=False) if args.json else render_analytics(result))
        return 0

    return 2


if __name__ == "__main__":
    raise SystemExit(main())
