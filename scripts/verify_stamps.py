#!/usr/bin/env python3
"""Check the two stamps on GET /api/gspc. Three-state. No network-as-proof.

site_attestation  — pin #board-attestation-1, sufficient preimage → VALID/INVALID/UNCHECKABLE
living_stamp      — published UNVERIFIABLE stays UNVERIFIABLE; we do not upgrade it
"""
from __future__ import annotations

import base64
import json
import sys
import urllib.request
from copy import deepcopy

from nacl.exceptions import BadSignatureError
from nacl.signing import VerifyKey

BOARD_URL = "https://councilof.ai/api/gspc"
DID_URLS = (
    "https://csoai.org/.well-known/did.json",
    "https://councilof.ai/.well-known/did.json",
)
UA = {"User-Agent": "csoai-stamp-check/0.1", "Accept": "application/json"}


def fetch_json(url: str) -> dict:
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read().decode("utf-8"))


def canonical(obj) -> bytes:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode(
        "utf-8"
    )


def jwk_x_to_raw(x: str) -> bytes:
    pad = "=" * (-len(x) % 4)
    raw = base64.urlsafe_b64decode(x + pad)
    if len(raw) != 32:
        raise ValueError(f"jwk x decoded to {len(raw)} bytes, want 32")
    return raw


def pin_board_key(did: dict) -> str | None:
    for m in did.get("verificationMethod") or []:
        if str(m.get("id") or "").endswith("#board-attestation-1"):
            x = (m.get("publicKeyJwk") or {}).get("x")
            if x:
                return jwk_x_to_raw(x).hex()
    return None


def verify_site_attestation(board: dict, pinned_hex: str | None) -> dict:
    sa = board.get("site_attestation")
    if not isinstance(sa, dict):
        return {"state": "UNCHECKABLE", "reason": "no site_attestation object"}
    if not pinned_hex:
        return {"state": "UNCHECKABLE", "reason": "could not pin #board-attestation-1 from DID"}
    try:
        pk = bytes.fromhex(pinned_hex)
        sig = bytes.fromhex(sa["sig"])
    except (KeyError, ValueError) as err:
        return {"state": "UNCHECKABLE", "reason": f"malformed sig/key: {err}"}
    x = sa.get("public_key_x") or ""
    try:
        carried = jwk_x_to_raw(x).hex()
    except Exception as err:
        return {"state": "UNCHECKABLE", "reason": f"public_key_x: {err}"}
    if carried != pinned_hex:
        return {
            "state": "INVALID",
            "reason": "site_attestation key is not the DID-pinned #board-attestation-1",
        }
    body = deepcopy(board)
    body.pop("site_attestation", None)
    pre = canonical(body)
    try:
        VerifyKey(pk).verify(pre, sig)
        return {"state": "VALID", "preimage_bytes": len(pre)}
    except BadSignatureError:
        return {"state": "INVALID", "reason": "Ed25519 over canonical(payload minus site_attestation) failed"}


def living_stamp_row(board: dict) -> dict:
    stamp = (board.get("measured_on") or {}).get("living_stamp") or board.get("living_stamp") or {}
    state = str(stamp.get("verification_state") or "UNCHECKABLE").upper()
    if stamp.get("verifiable") is True or state in {"VALID", "VERIFIED", "VERIFIABLE"}:
        # Never upgrade a published UNVERIFIABLE; if the payload lies, still report the field.
        return {
            "state": state,
            "reason": "payload claims verifiable — this script does not re-attest the old stamp",
        }
    return {
        "state": "UNVERIFIABLE" if "UNVERIF" in state or stamp.get("verifiable") is False else state,
        "updated": stamp.get("updated"),
        "reproduction_attempts": stamp.get("reproduction_attempts"),
        "reproduction_verified": stamp.get("reproduction_verified"),
        "note": "old living stamp stays UNVERIFIABLE; next stamp must use docs/PREIMAGE-FIX.md",
    }


def main() -> int:
    try:
        board = fetch_json(BOARD_URL)
    except Exception as err:
        print(json.dumps({"state": "UNREACHABLE", "reason": str(err)}))
        return 2
    pinned = None
    did_err = None
    for url in DID_URLS:
        try:
            pinned = pin_board_key(fetch_json(url))
            if pinned:
                break
        except Exception as err:
            did_err = str(err)
    site = verify_site_attestation(board, pinned)
    living = living_stamp_row(board)
    out = {
        "source": BOARD_URL,
        "schema": board.get("schema"),
        "site_attestation": site,
        "living_stamp": living,
        "did_pin": bool(pinned),
        "did_error": did_err,
        "not_a_certification": True,
    }
    print(json.dumps(out, sort_keys=True))
    if site.get("state") != "VALID":
        return 1
    if living.get("state") not in {"UNVERIFIABLE", "UNCHECKABLE"}:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
