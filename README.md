# Council of AI — Grok Build plugin

**Measurement, never certification.**

This directory is a [Grok Build](https://x.ai/cli) plugin: skills, slash commands, a read-only auditor subagent, hooks, and MCP wiring for [Council of AI](https://councilof.ai).

Council of AI (CSOAI Ltd, UK Companies House 16939677) runs AI systems against frozen published tests, signs the result (Ed25519), and publishes the empty cells next to the filled ones. Anyone can re-check. No account. No fee to verify.

This plugin does **not** wrap Grok, rank Grok specially, or claim an xAI partnership. It puts the same instrument under the Grok TUI that already sits under Claude Code and Cursor.

## Install (today, before marketplace listing)

```bash
# 1. Install Grok Build
curl -fsSL https://x.ai/cli/install.sh | bash
grok --version

# 2. Drop this folder where Grok looks
mkdir -p ~/.grok/plugins
cp -R council-of-ai-grok ~/.grok/plugins/council-of-ai

# or, in a project
mkdir -p .grok/plugins
cp -R council-of-ai-grok .grok/plugins/council-of-ai

# 3. Confirm discovery
grok inspect
```

Inside the TUI:

```
/plugins
/council
/gspc
/verify
/sign
```

When listed on the official catalog:

```bash
grok plugin install council-of-ai --trust
```

See `docs/MARKETPLACE-PR.md` for the catalog entry and PR text.

## What loads

| Path | Role |
|---|---|
| `plugin.json` | Manifest |
| `skills/council/SKILL.md` | Doctrine + router (`/council`) |
| `skills/gspc/SKILL.md` | Live board (`/gspc`) |
| `skills/verify-card/SKILL.md` | Three-state verify (`/verify`) |
| `skills/sign-artifact/SKILL.md` | Layer-0 seal (`/sign`) |
| `commands/*.md` | Slash command shims |
| `agents/measurement-auditor.md` | Read-only subagent |
| `.mcp.json` | `https://councilof.ai/mcp` + `npx -y csoai-governance-mcp` |
| `hooks/hooks.json` | Session start / stop hints (non-blocking) |
| `scripts/gspc-board.mjs` | Honest CLI summary of `GET /api/gspc` |

## MCP fallbacks

- **GSPC tools over HTTP:** `POST https://councilof.ai/mcp` (`board_totals`, `get_axis`, `verify_card`, `list_cards`)
- **Governance MCP on npm:** `npx -y csoai-governance-mcp` (`csoai_sign`, `csoai_verify`, `csoai_govern`, `csoai_catalog`)
- **GSPC stdio server (not on npm as of 2026-08-27):** `node mcp/gspc-server/index.mjs` in `CSOAI-ORG/councilof-ai`

## Honesty

- Empty cells stay empty.
- Ties are not wins.
- Fetch failure is `UNREACHABLE`, never a remembered score.
- Verify is `VALID` / `INVALID` / `UNCHECKABLE`.
- A local seal is a receipt of bytes, not an approval of a product.

## Live check

```bash
node scripts/gspc-board.mjs
curl -sS https://councilof.ai/api/gspc | head
```

MIT © CSOAI Ltd · https://councilof.ai
