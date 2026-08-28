---
name: gspc
description: Pull the live Council of AI GSPC measurement board. Use when the user asks for scores, axes, leaders, ties vs separated, /gspc, or "what is measured right now".
when-to-use: GSPC board, live axes, measured vs unmeasured, jail axis, art5, swarm, affect
argument-hint: "[axis-name]"
user-invocable: true
metadata:
  author: CSOAI Ltd
  short-description: Live GSPC board
---

# GSPC live board

## Fetch

Prefer MCP `board_totals` then `get_axis`. Fallback:

```bash
node "${GROK_PLUGIN_ROOT}/scripts/gspc-board.mjs"
# or
curl -sS https://councilof.ai/api/gspc
```

Schema expected: `csoai.gspc-axes/0.5` (or whatever the live payload declares — print the live schema, do not assume).

As of 2026-08-28 research against the live API:

- 22 declared axes
- 15 measured (14 GSPC behavioural + jail + 1 financial provenance-controls)
- 7 financial/domain slots UNMEASURED
- Separated leads observed on governance, care, swarm, affect
- Most other behavioural axes were TIE
- Mean leader accuracy was ~0.73 — a point estimate, not a ranking trophy

Re-fetch. Do not quote this paragraph as if it were still live.

## How to present

1. Print `schema`, source URL, living stamp.
2. Table of MEASURED rows: axis, n, accuracy, separation, p or interval, leader.
3. Separate list of UNMEASURED axes — names only, no zeros.
4. If user named one axis, call `get_axis` / filter to that row.
5. If `living_stamp.verification_state` is not verified, say so. Do not hide it.

## Forbidden

- Filling empty cells
- "X is the safest model"
- Treating TIE as a win
- Mixing financial UNMEASURED slots into a behavioural average
