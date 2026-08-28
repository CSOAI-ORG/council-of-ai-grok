#!/usr/bin/env python3
"""Drive the shipped TUI catalogs, four-tool names, pin text, and board CLI.

Fails if Claude/Cursor marketplace JSON does not parse, if marketplace
name/owner/plugin/source diverge from the published contract, or if
skills/ and commands/ no longer expose council, gspc, verify, sign.
Also fails if marketplace PR text is missing the published pin SHA, if
old SHA/placeholder strings return, if install docs claim the GSPC MCP
is unpublished, or if the shipped board CLI does not print UNREACHABLE
on a failed fetch.

Does not invent scores. Does not fill UNMEASURED.
"""
from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REQUIRED_TOOLS = {"council", "gspc", "verify", "sign"}
PIN_URL = "https://github.com/CSOAI-ORG/council-of-ai-grok.git"
PIN_SHA = "621dd9ccc9b2f71729e58b496c66b87603c9587a"
SHA_RE = re.compile(r'"sha":\s*"([0-9a-f]{40})"')
FORBIDDEN_PIN_FRAGMENTS = ("3a75f16", "REPLACE_WITH_40_CHAR_SHA")
UNPUBLISHED_CLAIM = "not yet published to npm"
INSTALL_DOCS = (
    ROOT / "README.md",
    ROOT / "GROK.md",
    ROOT / "docs" / "MARKETPLACE-PR.md",
    ROOT / "docs" / "ALIGNMENT-GROK-ADDENDUM.md",
)
USER_FACING_GLOBS = (
    "README.md",
    "GROK.md",
    "plugin.json",
    "docs/*.md",
    "skills/*/SKILL.md",
    "commands/*.md",
    "agents/*.md",
    ".claude-plugin/*.json",
    ".cursor-plugin/*.json",
)
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


def published_pin_sha() -> str:
    path = ROOT / "docs" / "MARKETPLACE-PR.md"
    text = path.read_text(encoding="utf-8")
    if PIN_URL not in text:
        raise SystemExit(f"{path}: missing source URL {PIN_URL}")
    for frag in FORBIDDEN_PIN_FRAGMENTS:
        if frag in text:
            raise SystemExit(f"{path}: forbidden pin fragment {frag!r}")
    if PIN_SHA not in text:
        raise SystemExit(f"{path}: missing published pin SHA {PIN_SHA}")
    found = SHA_RE.findall(text)
    if not found:
        raise SystemExit(f"{path}: no 40-char lowercase sha in source.sha")
    sha = found[0]
    if sha != PIN_SHA:
        raise SystemExit(f"{path}: source.sha is {sha}, published pin is {PIN_SHA}")
    return sha


def assert_install_docs() -> None:
    for path in INSTALL_DOCS:
        text = path.read_text(encoding="utf-8")
        if UNPUBLISHED_CLAIM in text:
            raise SystemExit(f"{path}: unpublished-claim {UNPUBLISHED_CLAIM!r}")
        if "not on npm as of" in text:
            raise SystemExit(f"{path}: unpublished-claim 'not on npm as of'")
        if "npx -y csoai-gspc-mcp" not in text:
            raise SystemExit(f"{path}: missing npx -y csoai-gspc-mcp")
        if "https://councilof.ai/mcp" not in text:
            raise SystemExit(f"{path}: missing https://councilof.ai/mcp")
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    if "claude plugin marketplace add CSOAI-ORG/council-of-ai-grok" not in readme:
        raise SystemExit("README.md: missing Claude marketplace add")
    if "grok plugin install CSOAI-ORG/council-of-ai-grok" not in readme:
        raise SystemExit("README.md: missing Grok git install")
    if ".cursor-plugin/marketplace.json" not in readme:
        raise SystemExit("README.md: missing Cursor catalog pointer")


def assert_mcp_json() -> None:
    data = load_json(ROOT / ".mcp.json")
    servers = data.get("mcpServers") or {}
    gspc = servers.get("gspc") or {}
    npm = servers.get("gspc-npm") or {}
    if gspc.get("url") != "https://councilof.ai/mcp":
        raise SystemExit(f".mcp.json gspc.url {gspc.get('url')!r}")
    if npm.get("command") != "npx" or "csoai-gspc-mcp" not in (npm.get("args") or []):
        raise SystemExit(".mcp.json missing gspc-npm npx -y csoai-gspc-mcp")
    gov = servers.get("csoai-governance") or {}
    if "csoai-governance-mcp" not in (gov.get("args") or []):
        raise SystemExit(".mcp.json missing csoai-governance-mcp")


def assert_honesty_language() -> None:
    for glob in USER_FACING_GLOBS:
        for path in sorted(ROOT.glob(glob)):
            text = path.read_text(encoding="utf-8")
            lower = text.lower()
            if re.search(r"\bfaa\b", text, re.I):
                raise SystemExit(f"{path}: FAA language")
            if re.search(r"\bbft\b", text, re.I):
                raise SystemExit(f"{path}: BFT claim")
            if "certified analyst" in lower:
                raise SystemExit(f"{path}: certified analyst")
            if "all 22 measured" in lower:
                raise SystemExit(f"{path}: claims all 22 MEASURED")


def assert_board_cli_unreachable() -> None:
    script = ROOT / "scripts" / "gspc-board.mjs"
    env = os.environ.copy()
    env["GSPC_ORIGIN"] = "http://127.0.0.1:1"
    try:
        proc = subprocess.run(
            ["node", str(script)],
            capture_output=True,
            text=True,
            env=env,
            timeout=15,
            check=False,
        )
    except subprocess.TimeoutExpired as err:
        raise SystemExit(f"board CLI hung on fetch fail: {err}") from err
    out = (proc.stdout or "") + (proc.stderr or "")
    if "UNREACHABLE" not in out:
        raise SystemExit(f"board CLI did not print UNREACHABLE on fetch fail: {out!r}")
    if proc.returncode == 0:
        raise SystemExit("board CLI exited 0 on fetch fail")
    if re.search(r"reserve-attestation\s+MEASURED", out):
        raise SystemExit("board CLI invented a MEASURED reserve-attestation on fetch fail")


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
    pin = published_pin_sha()
    assert_install_docs()
    assert_mcp_json()
    assert_honesty_language()
    assert_board_cli_unreachable()
    print("catalogs_ok claude+cursor name=council-of-ai owner=CSOAI Ltd source=./")
    print("skills", " ".join(sorted(skills)))
    print("commands", " ".join(sorted(commands)))
    print("pin", pin)
    print("mcp npx -y csoai-gspc-mcp")
    return 0


if __name__ == "__main__":
    sys.exit(main())
