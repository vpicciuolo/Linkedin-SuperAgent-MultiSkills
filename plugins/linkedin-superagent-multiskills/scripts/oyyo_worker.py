#!/usr/bin/env python3
"""Local mode, queue, approval, and receipt manager for OYYO LinkedIn.

VINCENZO PICCIUOLO (C) 2026 HRN INNOVATION TECHNOLOGIES LTD
SPDX-License-Identifier: MIT

This utility stores no credentials and performs no network or browser actions.
The selected AI workspace supplies the manual, browser, or API adapter.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

VERSION = "2.2.0"
COPYRIGHT = "VINCENZO PICCIUOLO (C) 2026 HRN INNOVATION TECHNOLOGIES LTD"
PROJECT_URL = "https://github.com/vpicciuolo/Linkedin-SuperAgent-MultiSkills"
SUPPORT_URL = "https://hrn.ae/githubsupport"
PLUGIN_ROOT = Path(__file__).resolve().parent.parent
TEMPLATE_CONFIG = PLUGIN_ROOT / "templates" / "automation.json"
MODES = ("manual", "automatic", "api")
SCOPES = ("read", "publish", "manage")
READ_ACTIONS = {
    "inspect_profile",
    "inspect_posts",
    "inspect_notifications",
    "inspect_comments",
    "inspect_analytics",
    "account_audit",
}
ACTION_TYPES = tuple(
    sorted(
        READ_ACTIONS
        | {
            "publish_post",
            "schedule_post",
            "edit_post",
            "delete_post",
            "comment",
            "reply",
            "react",
            "send_message",
            "connect",
            "edit_profile",
            "edit_company_page",
            "delete_content",
            "custom",
        }
    )
)
WARNING = (
    "LinkedIn states that it does not permit third-party software or browser "
    "extensions that scrape, modify, or automate activity on its website. "
    "Automated profile management and other browser-based activity may violate "
    "LinkedIn's User Agreement and can lead to account restrictions. Automatic "
    "mode is optional and is used at your own risk."
)


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def workspace_path(value: Path | None = None) -> Path:
    if value is not None:
        return value.expanduser().resolve()
    configured = os.environ.get("OYYO_LINKEDIN_HOME")
    if configured:
        return Path(configured).expanduser().resolve()
    return (Path.cwd() / ".oyyo-linkedin").resolve()


def config_path(root: Path) -> Path:
    return root / "automation.json"


def queue_path(root: Path) -> Path:
    return root / "action-queue.json"


def receipts_path(root: Path) -> Path:
    return root / "action-receipts.jsonl"


def read_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    for attempt in range(3):
        try:
            temporary.replace(path)
            return
        except PermissionError:
            if attempt == 2:
                raise
            time.sleep(0.05)


def default_config() -> dict[str, Any]:
    return json.loads(TEMPLATE_CONFIG.read_text(encoding="utf-8"))


def load_config(root: Path) -> dict[str, Any]:
    config = read_json(config_path(root), default_config())
    if config.get("mode") not in MODES:
        raise ValueError(f"invalid mode in {config_path(root)}")
    if config.get("scope") not in SCOPES:
        raise ValueError(f"invalid scope in {config_path(root)}")
    return config


def set_mode(
    root: Path,
    mode: str,
    scope: str,
    account_label: str = "",
    acknowledge_risk: bool = False,
    api_scopes: list[str] | None = None,
) -> dict[str, Any]:
    if mode == "automatic" and not acknowledge_risk:
        raise ValueError("automatic mode requires --acknowledge-risk after the warning is accepted")
    config = load_config(root)
    config["mode"] = mode
    config["scope"] = scope
    if account_label:
        config["account_label"] = account_label
    config.setdefault("automatic", {})["risk_acknowledged"] = bool(
        acknowledge_risk if mode == "automatic" else config.get("automatic", {}).get("risk_acknowledged", False)
    )
    if mode == "api" and api_scopes is not None:
        config.setdefault("api", {})["granted_scopes"] = sorted(set(api_scopes))
    config["updated_at"] = utc_now()
    write_json(config_path(root), config)
    return config


def required_scope(action_type: str) -> str:
    if action_type in READ_ACTIONS:
        return "read"
    if action_type in {
        "publish_post",
        "schedule_post",
        "edit_post",
        "comment",
        "reply",
        "react",
    }:
        return "publish"
    return "manage"


def scope_allows(configured: str, required: str) -> bool:
    order = {"read": 0, "publish": 1, "manage": 2}
    return order[configured] >= order[required]


def load_queue(root: Path) -> list[dict[str, Any]]:
    queue = read_json(queue_path(root), [])
    if not isinstance(queue, list):
        raise ValueError(f"queue must be a JSON list: {queue_path(root)}")
    return queue


def save_queue(root: Path, queue: list[dict[str, Any]]) -> None:
    write_json(queue_path(root), queue)


def add_action(
    root: Path,
    action_type: str,
    summary: str,
    target: str = "",
    payload_file: str = "",
) -> dict[str, Any]:
    config = load_config(root)
    needed = required_scope(action_type)
    if not scope_allows(config["scope"], needed):
        raise ValueError(
            f"{action_type} needs scope {needed!r}; configured scope is {config['scope']!r}"
        )
    if payload_file and not Path(payload_file).expanduser().exists():
        raise ValueError(f"payload file does not exist: {payload_file}")
    read_only = action_type in READ_ACTIONS
    action = {
        "id": uuid.uuid4().hex[:12],
        "created_at": utc_now(),
        "updated_at": utc_now(),
        "mode": config["mode"],
        "scope": config["scope"],
        "account_label": config.get("account_label", ""),
        "type": action_type,
        "target": target,
        "summary": summary,
        "payload_file": payload_file,
        "required_scope": needed,
        "status": "ready" if read_only else "pending_approval",
        "approval": None,
    }
    queue = load_queue(root)
    queue.append(action)
    save_queue(root, queue)
    return action


def find_action(queue: list[dict[str, Any]], action_id: str) -> dict[str, Any]:
    for action in queue:
        if action.get("id") == action_id:
            return action
    raise ValueError(f"unknown action id: {action_id}")


def approve_action(root: Path, action_id: str, approved_by: str = "user") -> dict[str, Any]:
    queue = load_queue(root)
    action = find_action(queue, action_id)
    if action["status"] != "pending_approval":
        raise ValueError(f"action {action_id} is {action['status']}, not pending_approval")
    action["status"] = "approved"
    action["updated_at"] = utc_now()
    action["approval"] = {"approved_at": utc_now(), "approved_by": approved_by}
    save_queue(root, queue)
    return action


def cancel_action(root: Path, action_id: str, message: str = "") -> dict[str, Any]:
    queue = load_queue(root)
    action = find_action(queue, action_id)
    if action["status"] in {"succeeded", "failed", "cancelled"}:
        raise ValueError(f"action {action_id} is already final: {action['status']}")
    action["status"] = "cancelled"
    action["updated_at"] = utc_now()
    action["result_message"] = message
    save_queue(root, queue)
    append_receipt(root, action)
    return action


def finish_action(root: Path, action_id: str, result: str, message: str = "") -> dict[str, Any]:
    queue = load_queue(root)
    action = find_action(queue, action_id)
    allowed_start = {"ready", "approved"}
    if action["status"] not in allowed_start:
        raise ValueError(
            f"action {action_id} must be ready or approved before finishing; current status is {action['status']}"
        )
    action["status"] = result
    action["updated_at"] = utc_now()
    action["result_message"] = message
    save_queue(root, queue)
    append_receipt(root, action)
    return action


def append_receipt(root: Path, action: dict[str, Any]) -> None:
    receipt = {
        key: action.get(key)
        for key in (
            "id",
            "updated_at",
            "mode",
            "account_label",
            "type",
            "target",
            "summary",
            "status",
            "approval",
            "result_message",
        )
    }
    path = receipts_path(root)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(receipt, ensure_ascii=False) + "\n")


def doctor(root: Path) -> dict[str, Any]:
    config = load_config(root)
    mode = config["mode"]
    checks: list[dict[str, Any]] = [
        {"name": "workspace", "ok": root.exists(), "detail": str(root)},
        {"name": "mode", "ok": True, "detail": mode},
        {"name": "scope", "ok": True, "detail": config["scope"]},
    ]
    if mode == "manual":
        checks.append({"name": "adapter", "ok": True, "detail": "copy/paste and guided UI"})
    elif mode == "automatic":
        acknowledged = bool(config.get("automatic", {}).get("risk_acknowledged"))
        checks.extend(
            (
                {"name": "risk_acknowledged", "ok": acknowledged, "detail": WARNING},
                {
                    "name": "browser_adapter",
                    "ok": None,
                    "detail": "host-provided; verify browser/computer-use capability in the active workspace",
                },
                {
                    "name": "credentials",
                    "ok": True,
                    "detail": "user signs in directly; credentials are never stored by OYYO",
                },
            )
        )
    else:
        api = config.get("api", {})
        token_name = api.get("token_environment_variable", "LINKEDIN_ACCESS_TOKEN")
        actor_name = api.get("actor_urn_environment_variable", "LINKEDIN_ACTOR_URN")
        version_name = api.get("version_environment_variable", "LINKEDIN_VERSION")
        checks.extend(
            (
                {"name": token_name, "ok": bool(os.environ.get(token_name)), "detail": "set" if os.environ.get(token_name) else "missing"},
                {"name": actor_name, "ok": bool(os.environ.get(actor_name)), "detail": "set" if os.environ.get(actor_name) else "missing"},
                {"name": version_name, "ok": bool(os.environ.get(version_name)), "detail": "set" if os.environ.get(version_name) else "missing"},
                {
                    "name": "api_scope_note",
                    "ok": bool(api.get("granted_scopes")),
                    "detail": (
                        ", ".join(api.get("granted_scopes", []))
                        if api.get("granted_scopes")
                        else "no granted scopes recorded; actual actions depend on approved products and scopes"
                    ),
                },
            )
        )
    return {"version": VERSION, "config": config, "checks": checks}


def print_result(value: Any, as_json: bool) -> None:
    if as_json:
        print(json.dumps(value, indent=2, ensure_ascii=False))
        return
    if isinstance(value, list):
        if not value:
            print("No actions.")
            return
        for action in value:
            print(f"{action['id']}  {action['status']:<18} {action['type']:<22} {action['summary']}")
        return
    print(json.dumps(value, indent=2, ensure_ascii=False))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="OYYO LinkedIn worker mode and action queue")
    parser.add_argument("--version", action="version", version=VERSION)
    parser.add_argument("--workspace", type=Path, help="override .oyyo-linkedin workspace")
    parser.add_argument("--json", action="store_true", help="return structured JSON")
    sub = parser.add_subparsers(dest="command", required=True)

    mode = sub.add_parser("mode", help="show or set the operating mode")
    mode_sub = mode.add_subparsers(dest="mode_command", required=True)
    mode_sub.add_parser("show")
    mode_set = mode_sub.add_parser("set")
    mode_set.add_argument("mode", choices=MODES)
    mode_set.add_argument("--scope", choices=SCOPES, default="read")
    mode_set.add_argument("--account-label", default="")
    mode_set.add_argument("--acknowledge-risk", action="store_true")
    mode_set.add_argument(
        "--api-scope",
        action="append",
        default=None,
        help="record a granted OAuth scope; repeat for multiple scopes",
    )

    sub.add_parser("doctor", help="check the configured mode without exposing secrets")

    action = sub.add_parser("action", help="manage the local action queue")
    action_sub = action.add_subparsers(dest="action_command", required=True)
    add = action_sub.add_parser("add")
    add.add_argument("type", choices=ACTION_TYPES)
    add.add_argument("summary")
    add.add_argument("--target", default="")
    add.add_argument("--payload-file", default="")
    listing = action_sub.add_parser("list")
    listing.add_argument("--status")
    approve = action_sub.add_parser("approve")
    approve.add_argument("action_id")
    approve.add_argument("--approved-by", default="user")
    finish = action_sub.add_parser("finish")
    finish.add_argument("action_id")
    finish.add_argument("result", choices=("succeeded", "failed"))
    finish.add_argument("--message", default="")
    cancel = action_sub.add_parser("cancel")
    cancel.add_argument("action_id")
    cancel.add_argument("--message", default="")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    root = workspace_path(args.workspace)
    try:
        if args.command == "mode":
            if args.mode_command == "show":
                result = load_config(root)
            else:
                result = set_mode(
                    root,
                    args.mode,
                    args.scope,
                    account_label=args.account_label,
                    acknowledge_risk=args.acknowledge_risk,
                    api_scopes=args.api_scope,
                )
                if args.mode == "automatic" and not args.json:
                    print(f"WARNING: {WARNING}\n")
        elif args.command == "doctor":
            result = doctor(root)
        elif args.action_command == "add":
            result = add_action(root, args.type, args.summary, args.target, args.payload_file)
        elif args.action_command == "list":
            result = load_queue(root)
            if args.status:
                result = [item for item in result if item.get("status") == args.status]
        elif args.action_command == "approve":
            result = approve_action(root, args.action_id, args.approved_by)
        elif args.action_command == "finish":
            result = finish_action(root, args.action_id, args.result, args.message)
        elif args.action_command == "cancel":
            result = cancel_action(root, args.action_id, args.message)
        else:
            return 2
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    print_result(result, args.json)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
