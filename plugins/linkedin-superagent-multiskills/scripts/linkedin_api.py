#!/usr/bin/env python3
"""Small official LinkedIn API adapter for approved OYYO worker actions.

VINCENZO PICCIUOLO (C) 2026 HRN INNOVATION TECHNOLOGIES LTD
SPDX-License-Identifier: MIT

Credentials are read from environment variables and are never printed.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import Request, urlopen

VERSION = "2.2.0"
API_ROOT = "https://api.linkedin.com"
TOKEN_ENV = "LINKEDIN_ACCESS_TOKEN"
ACTOR_ENV = "LINKEDIN_ACTOR_URN"
VERSION_ENV = "LINKEDIN_VERSION"


class LinkedInAPIError(RuntimeError):
    """A sanitized LinkedIn API failure."""


def require_environment(name: str) -> str:
    value = os.environ.get(name, "").strip()
    if not value:
        raise ValueError(f"missing required environment variable: {name}")
    return value


def social_headers(token: str, api_version: str) -> dict[str, str]:
    if not api_version.isdigit() or len(api_version) != 6:
        raise ValueError(f"{VERSION_ENV} must use YYYYMM format")
    return {
        "Authorization": f"Bearer {token}",
        "LinkedIn-Version": api_version,
        "X-Restli-Protocol-Version": "2.0.0",
        "Content-Type": "application/json",
    }


def api_request(
    method: str,
    path: str,
    token: str,
    api_version: str | None = None,
    payload: dict[str, Any] | None = None,
) -> dict[str, Any]:
    headers = {"Authorization": f"Bearer {token}", "Accept": "application/json"}
    if api_version is not None:
        headers.update(social_headers(token, api_version))
    body = None if payload is None else json.dumps(payload).encode("utf-8")
    request = Request(f"{API_ROOT}{path}", data=body, headers=headers, method=method)
    try:
        with urlopen(request, timeout=30) as response:
            raw = response.read().decode("utf-8")
            result: dict[str, Any] = {
                "status": response.status,
                "request_id": response.headers.get("x-li-uuid", ""),
                "resource_id": response.headers.get("x-restli-id", ""),
            }
            if raw:
                parsed = json.loads(raw)
                result["body"] = parsed
            return result
    except HTTPError as exc:
        raw = exc.read().decode("utf-8", errors="replace")
        try:
            detail: Any = json.loads(raw) if raw else {}
        except json.JSONDecodeError:
            detail = raw[:500]
        raise LinkedInAPIError(f"LinkedIn API returned HTTP {exc.code}: {detail}") from exc
    except URLError as exc:
        raise LinkedInAPIError(f"LinkedIn API connection failed: {exc.reason}") from exc


def build_text_post(actor: str, text: str, visibility: str = "PUBLIC") -> dict[str, Any]:
    if not actor.startswith(("urn:li:person:", "urn:li:organization:")):
        raise ValueError("actor must be a LinkedIn person or organization URN")
    clean = text.strip()
    if not clean:
        raise ValueError("post text is empty")
    return {
        "author": actor,
        "commentary": clean,
        "visibility": visibility,
        "distribution": {
            "feedDistribution": "MAIN_FEED",
            "targetEntities": [],
            "thirdPartyDistributionChannels": [],
        },
        "lifecycleState": "PUBLISHED",
        "isReshareDisabledByAuthor": False,
    }


def build_comment(actor: str, object_urn: str, text: str) -> dict[str, Any]:
    clean = text.strip()
    if not clean:
        raise ValueError("comment text is empty")
    return {"actor": actor, "object": object_urn, "message": {"text": clean}}


def build_like(actor: str, object_urn: str) -> dict[str, str]:
    return {"actor": actor, "object": object_urn}


def read_text(value: str, literal: bool) -> str:
    return value if literal else Path(value).read_text(encoding="utf-8")


def require_confirmation(confirmed: bool) -> None:
    if not confirmed:
        raise ValueError("live write blocked; inspect the target and add --confirm after user approval")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Official LinkedIn API adapter for OYYO")
    parser.add_argument("--version", action="version", version=VERSION)
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("whoami", help="read the authenticated OIDC userinfo response")

    publish = sub.add_parser("publish-text", help="publish an approved text post")
    publish.add_argument("input", help="UTF-8 file path, or literal text with --text")
    publish.add_argument("--text", action="store_true")
    publish.add_argument("--visibility", choices=("PUBLIC", "CONNECTIONS"), default="PUBLIC")
    publish.add_argument("--confirm", action="store_true")

    comment = sub.add_parser("comment", help="add an approved comment to a post")
    comment.add_argument("object_urn")
    comment.add_argument("input", help="UTF-8 file path, or literal text with --text")
    comment.add_argument("--text", action="store_true")
    comment.add_argument("--confirm", action="store_true")

    like = sub.add_parser("like", help="add an approved like to a post or comment")
    like.add_argument("object_urn")
    like.add_argument("--confirm", action="store_true")

    delete = sub.add_parser("delete-post", help="delete an approved owned post")
    delete.add_argument("post_urn")
    delete.add_argument("--confirm", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        if args.command == "whoami":
            token = require_environment(TOKEN_ENV)
            result = api_request("GET", "/v2/userinfo", token)
        else:
            require_confirmation(args.confirm)
            token = require_environment(TOKEN_ENV)
            actor = require_environment(ACTOR_ENV)
            api_version = require_environment(VERSION_ENV)
            if args.command == "publish-text":
                payload = build_text_post(actor, read_text(args.input, args.text), args.visibility)
                result = api_request("POST", "/rest/posts", token, api_version, payload)
            elif args.command == "comment":
                payload = build_comment(actor, args.object_urn, read_text(args.input, args.text))
                target = quote(args.object_urn, safe="")
                result = api_request(
                    "POST", f"/rest/socialActions/{target}/comments", token, api_version, payload
                )
            elif args.command == "like":
                payload = build_like(actor, args.object_urn)
                target = quote(args.object_urn, safe="")
                result = api_request(
                    "POST", f"/rest/socialActions/{target}/likes", token, api_version, payload
                )
            elif args.command == "delete-post":
                target = quote(args.post_urn, safe="")
                result = api_request("DELETE", f"/rest/posts/{target}", token, api_version)
            else:
                return 2
    except (OSError, ValueError, json.JSONDecodeError, LinkedInAPIError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
