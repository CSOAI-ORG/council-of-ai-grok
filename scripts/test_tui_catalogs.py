#!/usr/bin/env python3
"""Drive the shipped TUI catalogs and four-tool names from disk.

Fails if Claude/Cursor marketplace JSON does not parse, if marketplace
name/owner/plugin/source diverge from the published contract, or if
skills/ and commands/ no longer expose council, gspc, verify, sign.
Does not invent scores. Does not fill UNMEASURED.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REQUIRED_TOOLS = {"council", "gspc", "verify", "sign"}
FRONT = re.compile(r"^---\s*\n(.*?)\n---", re.S)
NAME = re.compile(r"^name:\s*(.+)$", re.M)


def load_json(path: Path) -> dict:
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def frontmatter_name(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    m = FRONT.search(text)
    if not m:
        raise SystemExit(f"{path}: missing YAML frontmatter")
    n = NAME.search(m.group(1))
    if not n:
        raise SystemExit(f"{path}: missing frontmatter name")
    return n.group(1).strip()


def assert_marketplace(path: Path) -> dict:
    data = load_json(path)
    if data.get("name") != "council-of-ai":
        raise SystemExit(f"{path}: marketplace name {data.get('name')!r}")
    owner = data.get("owner") or {}
    if owner.get("name") != "CSOAI Ltd":
        raise SystemExit(f"{path}: owner.name {owner.get('name')!r}")
    plugins = data.get("plugins")
    if not isinstance(plugins, list) or not plugins:
        raise SystemExit(f"{path}: plugins must be a non-empty array")
    hit = next((p for p in plugins if p.get("name") == "council-of-ai"), None)
    if hit is None:
        raise SystemExit(f"{path}: no plugin named council-of-ai")
    src = hit.get("source")
    if src not in ("./", ".", ""):
        raise SystemExit(f"{path}: source {src!r} is not repo root")
    blob = json.dumps(data)
    if "certif" in blob.lower() and "never certification" not in blob.lower():
        raise SystemExit(f"{path}: certification language without the never-clause")
    return data


def collect_names(glob: str) -> set[str]:
    names = set()
    for path in sorted(ROOT.glob(glob)):
        names.add(frontmatter_name(path))
    return names


def main() -> int:
    claude = ROOT / ".claude-plugin" / "marketplace.json"
    cursor = ROOT / ".cursor-plugin" / "marketplace.json"
    assert_marketplace(claude)
    assert_marketplace(cursor)
    load_json(ROOT / ".claude-plugin" / "plugin.json")
    load_json(ROOT / ".cursor-plugin" / "plugin.json")
    skills = collect_names("skills/*/SKILL.md")
    commands = collect_names("commands/*.md")
    missing_s = REQUIRED_TOOLS - skills
    missing_c = REQUIRED_TOOLS - commands
    if missing_s or missing_c:
        raise SystemExit(
            f"four tools missing: skills={sorted(missing_s)} commands={sorted(missing_c)}"
        )
    print("catalogs_ok claude+cursor name=council-of-ai owner=CSOAI Ltd source=./")
    print("skills", " ".join(sorted(skills)))
    print("commands", " ".join(sorted(commands)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
