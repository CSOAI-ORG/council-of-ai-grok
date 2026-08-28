# GROK.md — Council of AI × Grok Build

Read this before writing code or answering as an agent on any CSOAI surface.

Companion docs: `AGENTS.md` (monorepo law), `ALIGNMENT.md` (live site / Claude lane), this file (Grok TUI lane).

Last aligned: 2026-08-28.

## Who we are

Council of AI (CSOAI Ltd, UK 16939677) measures AI behaviour on frozen published tests, signs Ed25519 cards, and re-attests when the model or the law moves. **We do not certify. We do not enforce. We do not sell a ranking slot.**

## How Grok should work here

Grok Build is a coding TUI with skills, plugins, hooks, MCP, and ACP. Council sits **under** Grok as an instrument:

- Grok edits code, runs tests, searches the web.
- Council measures claims, verifies cards, seals bytes.

Do not implement a "Grok council persona." Do not special-case Grok on the GSPC board.

## Install (operator)

```bash
curl -fsSL https://x.ai/cli/install.sh | bash
# plugin tree from this pack
grok --plugin-dir /path/to/council-of-ai-grok inspect
```

MCP without the plugin:

```bash
# HTTP (no process)
# POST https://councilof.ai/mcp

# npm GSPC server (board_totals, get_axis, verify_card, list_cards)
npx -y csoai-gspc-mcp

# npm governance server
npx -y csoai-governance-mcp
```

Grok also reads `AGENTS.md` and `CLAUDE.md` without extra config. Keep those honest.

## Live endpoints that count

| URL | What |
|---|---|
| `https://councilof.ai/api/gspc` | Living board (schema declared in payload, 0.5 as of 2026-08-28) |
| `https://councilof.ai/mcp` | Same GSPC tools over streamable HTTP |
| `https://councilof.ai/verify` | Browser verify, no account |
| `https://councilof.ai` | Measurement body |
| `https://csoai.org` | Public site / OS |

## Branch truth

Production is **`master`**. GitHub default may still be **`main`**. Always `git checkout master`. See `docs/DEFAULT-BRANCH.md`.

## Language

Forbidden in user-facing text: certified, accredited, approved, badge, seal of approval, "passed Council", partnered with xAI.

Required when quoting scores: source URL, n, MEASURED vs UNMEASURED, TIE vs SEPARATED.

Internal codenames (SOVOS, sov6, OWEM, SOV-*) stay off public surfaces.
