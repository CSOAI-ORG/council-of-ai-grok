---
name: pack
description: Assemble a Council of AI attested measurement pack via CSOAI 402. Use when the user says /pack, pack assemble, agent invoice, or x402 pack.
when-to-use: pack assemble, CSOAI 402, agent invoice, x402 pack, first-buyer pack
argument-hint: "[scope]"
user-invocable: true
metadata:
  author: CSOAI Ltd
  short-description: Assemble pack (402 invoice)
---

# Pack assemble (CSOAI 402)

Agents pay to assemble the pack; the board stays free.

This is **not** a score, a certificate, or a way to paint the 7 empty cells.

## Call

Hosted mock rail (own Worker, not `/api/gspc`):

`https://csoai-402-pack.nicholastempleman.workers.dev`  
Custom name: `https://pack.councilof.ai` (CF attached; local DNS may lag)

```bash
PACK_URL=https://csoai-402-pack.nicholastempleman.workers.dev \
  python3 /Users/nicholas/clawd/x402-pack-rail/agent_client.py ${GROK_ARG:-first-buyer}
```

Or:

```bash
HOST=https://csoai-402-pack.nicholastempleman.workers.dev
# unpaid → 402
curl -sS -H 'content-type: application/json' -d '{"scope":"first-buyer"}' \
  $HOST/v1/pack/assemble
# mock pay → 200
curl -sS -H 'content-type: application/json' -H 'PAYMENT-SIGNATURE: mock' \
  -d '{"scope":"first-buyer"}' $HOST/v1/pack/assemble
```

Air loopback remains `http://127.0.0.1:8402`.

Live later is owner-gated (`X402_MODE=live` + wallet + facilitator JWT). Do not settle USDC from this TUI.

## How to present

1. If 402: say **invoice for assembly**, scheme `exact`, network Base, `paid_for: assembly`. Do not say “pay to pass.”
2. If 200: print `board.public_count`, list UNMEASURED slots with `n: null`, living stamp state.
3. Quote `verify_url`. The board at `/api/gspc` stays free.

## Forbidden

- Filling empty cells
- Treating the pack as a grade
- Hosting this on `/api/gspc` or `/verify`
- Listing 402 on the homepage as pay-to-pass
