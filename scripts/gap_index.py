#!/usr/bin/env python3
"""Weekly Gap Index tape from the live board.

Counts material claims with no stranger-recomputable row. Hollow rows increment
the index. UNMEASURED is not 0. humanoid-labour-index stays UNMEASURED — no
public series, so we do not eat it as data.

Does not invent scores. Does not certify.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
import urllib.request
from datetime import datetime, timezone

BOARD_URL = "https://councilof.ai/api/gspc"
INDEX_URL = "https://councilof.ai/signed/card_index.json"
CARDS_URL = "https://councilof.ai/api/cards"
UA = {"User-Agent": "csoai-gap-index/0.1", "Accept": "application/json"}


def fetch_json(url: str):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read().decode("utf-8"))


def canonical(obj) -> bytes:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode(
        "utf-8"
    )


def iso_week(now: datetime) -> str:
    y, w, _ = now.isocalendar()
    return f"{y}-W{w:02d}"


def build(now: datetime | None = None) -> dict:
    now = now or datetime.now(timezone.utc)
    board = fetch_json(BOARD_URL)
    axes = board.get("axes") or []
    rows = []
    unmeasured_names = []
    for ax in axes:
        name = ax.get("axis") or ax.get("name")
        status = str(ax.get("status") or "").upper()
        if "UNMEASURED" in status:
            unmeasured_names.append(name)
            rows.append(
                {
                    "claim": f"axis:{name}",
                    "kind": ax.get("kind") or "declared-slot",
                    "status": "UNMEASURED",
                    "n": None,
                    "note": "declared slot with no run — not a zero",
                }
            )
        elif name == "provenance-controls":
            rows.append(
                {
                    "claim": f"axis:{name}",
                    "kind": ax.get("kind") or "deterministic-facts",
                    "status": "MEASURED",
                    "n": ax.get("n"),
                    "n_unit": ax.get("n_unit"),
                    "note": "on-chain control facts for locatable issuer accounts; not a rating",
                }
            )
    stamp = (board.get("measured_on") or {}).get("living_stamp") or {}
    rows.append(
        {
            "claim": "living_stamp",
            "kind": "stamp",
            "status": str(stamp.get("verification_state") or "UNCHECKABLE"),
            "note": "old stamp stays UNVERIFIABLE; site_attestation is the integrity stamp that verifies",
        }
    )
    index = None
    store = None
    try:
        index = fetch_json(INDEX_URL)
    except Exception:
        index = None
    try:
        store = fetch_json(CARDS_URL)
    except Exception:
        store = None
    card_row = {
        "claim": "signed-card-index",
        "kind": "two-labelled-numbers",
        "index_n_cards": (index or {}).get("n_cards") if isinstance(index, dict) else None,
        "index_rows": len((index or {}).get("cards") or []) if isinstance(index, dict) else None,
        "store_count": (store or {}).get("count") if isinstance(store, dict) else None,
        "note": "two labelled numbers, never reconciled here",
    }
    rows.append(card_row)

    totals = board.get("totals") or {}
    body = {
        "schema": "csoai.gap-index/0.1",
        "kind": "gap-index",
        "source": BOARD_URL,
        "as_of": now.replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "week": iso_week(now),
        "board_schema": board.get("schema"),
        "public_count": totals.get("public_count"),
        "unmeasured_slots": totals.get("unmeasured_axes")
        if totals.get("unmeasured_axes") is not None
        else len(unmeasured_names),
        "unmeasured_axes": unmeasured_names,
        "rows": rows,
        "doctrine": (
            "Eat claims, not URLs. Hollow rows increment the index. "
            "UNMEASURED is not 0. humanoid-labour-index is listed only as UNMEASURED — "
            "no public series, so it is not eaten as data. Measurement, never certification."
        ),
        "not_a_certification": True,
    }
    # content_id over the body without integrity fields
    content_id = hashlib.sha256(canonical(body)).hexdigest()
    body["integrity"] = {
        "content_id": content_id,
        "alg": "sha256",
        "sig_input": (
            "canonical JSON of this object WITHOUT the integrity field; "
            "sort_keys, separators (',',':'), ensure_ascii=False; "
            "content_id is sha256 of those UTF-8 bytes. Same canonicalisation as "
            "GET /api/gspc site_attestation. Signature is UNSIGNED until a DID-pinned key signs it."
        ),
        "signature": None,
        "verification_state": "UNSIGNED",
    }
    return body


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--out", help="write JSON here")
    args = p.parse_args()
    try:
        tape = build()
    except Exception as err:
        print(json.dumps({"state": "UNREACHABLE", "reason": str(err)}), file=sys.stderr)
        return 2
    text = json.dumps(tape, indent=2, ensure_ascii=False) + "\n"
    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(text)
        print(f"gap_index -> {args.out} week={tape['week']} unmeasured={tape['unmeasured_slots']}")
    else:
        sys.stdout.write(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
