# First-buyer pack — one pager (not a certificate)

Council of AI (CSOAI Ltd, UK 16939677) measures AI behaviour on frozen published tests, signs Ed25519 cards, and re-attests when the model or the law moves. **We do not certify.**

## What you are buying

An **assembled pack**: the live board snapshot, the UNMEASURED slots named, the verify URL, and the assembly invoice. Agents pay for assembly (`CSOAI 402`). The board stays free.

This is **not** a score, a ranking slot, a conformity mark, or a way to paint the seven empty cells.

## Live board (cite `GET https://councilof.ai/api/gspc`)

Quote both numbers, or the smaller:

- 22 axis slots
- 15 MEASURED
- 7 UNMEASURED (empty ≠ 0):  
  `reserve-attestation` · `regulatory-framework` · `distribution-integrity` · `custody-disclosure` · `ai-economy-index` · `human-labour-index` · `humanoid-labour-index`

Verify any card, no account: https://councilof.ai/verify

## How an agent assembles

```
/pack first-buyer
```

Unpaid assemble → HTTP **402** (invoice for assembly, `paid_for: assembly`, USDC `exact` on Base).  
Mock pay → **200** + UNMEASURED `n: null`.

Do not host this on `/api/gspc` or `/verify`. Do not list 402 on the homepage as pay-to-pass.

## MCP (free board)

```
npx -y csoai-gspc-mcp
```

Tools: `board_totals` `get_axis` `verify_card` `list_cards`.

Measurement, never certification.
