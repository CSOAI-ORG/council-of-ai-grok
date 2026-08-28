---
name: verify
description: Verify a Council of AI signed measurement card. Three-state verdict only — VALID, INVALID (reason), or UNCHECKABLE. Use for /verify, pasted JSON cards, or councilof.ai card URLs.
when-to-use: verify measurement card, Ed25519, signed receipt, gspc.measurement-card
argument-hint: "<card JSON | URL | path>"
user-invocable: true
metadata:
  author: CSOAI Ltd
  short-description: Three-state card verify
---

# Verify a measurement card

## Rule

A card is `gspc.measurement-card` (or the current published card schema). Verification:

1. Recompute the card id from the canonical body.
2. Check the Ed25519 signature under the **published pinned key** `did:web:csoai.org#card-attestation-1`.
3. A card that is internally consistent but signed with a freshly generated key is **INVALID**, not valid.

## How

Prefer MCP `verify_card` with `{ "card": <object | JSON string | https://councilof.ai/... URL> }`.

Human UI: https://councilof.ai/verify (browser recomputes; nothing needs to be sent to Council).

If the user pastes JSON, do not "summarise the score" before the verdict. Verdict first.

## Output

```
verdict: VALID | INVALID | UNCHECKABLE
reason:  <one line>
id:      <recomputed or stated>
key:     did:web:csoai.org#card-attestation-1
```

Then, only if VALID, quote the measured axes and the empty slots exactly as the card states.

UNCHECKABLE if the payload is truncated, the schema is unknown, or the network origin is not councilof.ai / csoai.org when a URL was given.
