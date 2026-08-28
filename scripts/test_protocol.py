#!/usr/bin/env python3
"""Drive the protocol surfaces: stamps, gap tape, bundled verifier.

Does not fill UNMEASURED. Does not invent a humanoid series.
"""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
UA = {"User-Agent": "csoai-protocol-test/0.1", "Accept": "application/json"}


def run(args, **kw):
    return subprocess.run(args, capture_output=True, text=True, timeout=90, **kw)


def test_stamps() -> None:
    proc = run([sys.executable, str(ROOT / "scripts" / "verify_stamps.py")])
    if proc.returncode != 0:
        raise SystemExit(f"verify_stamps failed rc={proc.returncode} {proc.stdout}{proc.stderr}")
    out = json.loads(proc.stdout)
    if out.get("site_attestation", {}).get("state") != "VALID":
        raise SystemExit(f"site_attestation not VALID: {out.get('site_attestation')}")
    living = out.get("living_stamp", {}).get("state")
    if living != "UNVERIFIABLE":
        raise SystemExit(f"living_stamp should stay UNVERIFIABLE, got {living}")


def test_gap_index() -> None:
    with tempfile.NamedTemporaryFile("w+", suffix=".json", delete=False) as f:
        path = f.name
    proc = run([sys.executable, str(ROOT / "scripts" / "gap_index.py"), "--out", path])
    if proc.returncode != 0:
        raise SystemExit(f"gap_index failed {proc.stderr}")
    tape = json.loads(Path(path).read_text(encoding="utf-8"))
    names = tape.get("unmeasured_axes") or []
    if "humanoid-labour-index" not in names:
        raise SystemExit("humanoid-labour-index missing from UNMEASURED list — do not eat it as data")
    if tape.get("unmeasured_slots") != len(names):
        raise SystemExit("unmeasured_slots does not match names")
    for row in tape.get("rows") or []:
        if row.get("status") == "UNMEASURED" and row.get("n") not in (None,):
            raise SystemExit(f"UNMEASURED row carries n={row.get('n')} — that is a zero in disguise")
        if row.get("status") == "UNMEASURED" and row.get("accuracy") is not None:
            raise SystemExit("UNMEASURED row carries accuracy")
    if tape.get("integrity", {}).get("verification_state") != "UNSIGNED":
        raise SystemExit("gap tape must stay UNSIGNED until a DID-pinned key signs it")
    Path(path).unlink(missing_ok=True)


def test_verifier_bundle() -> None:
    verify = ROOT / "verifier" / "gspc-verify.mjs"
    if not verify.is_file():
        raise SystemExit("missing verifier/gspc-verify.mjs")
    req = urllib.request.Request(
        "https://councilof.ai/signed/card_index.json", headers=UA
    )
    index = json.loads(urllib.request.urlopen(req, timeout=60).read().decode())
    cards = index.get("cards") or []
    url = None
    for row in cards:
        u = row.get("card_url") or row.get("card")
        if not isinstance(u, str):
            continue
        if u.startswith("https://"):
            url = u
            break
        if u.startswith("/"):
            url = "https://councilof.ai" + u
            break
        if len(u) == 64:
            url = f"https://councilof.ai/signed/cards/{u}.json"
            break
    if not url:
        raise SystemExit("card_index has no usable card locator")
    with tempfile.NamedTemporaryFile("wb", suffix=".json", delete=False) as f:
        f.write(urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60).read())
        path = f.name
    proc = run(["node", str(verify), "--json", path])
    if proc.returncode != 0:
        raise SystemExit(
            f"gspc-verify rc={proc.returncode} stdout={proc.stdout[:500]} stderr={proc.stderr[:500]}"
        )


def test_action_present() -> None:
    yml = ROOT / ".github" / "actions" / "verify-card" / "action.yml"
    text = yml.read_text(encoding="utf-8")
    if "gspc-verify.mjs" not in text:
        raise SystemExit("action.yml does not invoke bundled verifier")
    if "UNCHECKABLE" not in text:
        raise SystemExit("action.yml missing UNCHECKABLE")


def main() -> int:
    test_stamps()
    print("stamps_ok site_attestation=VALID living_stamp=UNVERIFIABLE")
    test_gap_index()
    print("gap_index_ok hollow_rows_have_no_n")
    test_verifier_bundle()
    print("verifier_ok published_card=VALID")
    test_action_present()
    print("action_ok")
    return 0


if __name__ == "__main__":
    sys.exit(main())
