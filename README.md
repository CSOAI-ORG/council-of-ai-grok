# Council of AI — Grok Build plugin

**Measurement, never certification.**

This directory is a [Grok Build](https://x.ai/cli) plugin: skills, slash commands, a read-only auditor subagent, hooks, and MCP wiring for [Council of AI](https://councilof.ai).

Council of AI (CSOAI Ltd, UK Companies House 16939677) runs AI systems against frozen published tests, signs the result (Ed25519), and publishes the empty cells next to the filled ones. Anyone can re-check. No account. No fee to verify.

This plugin does **not** wrap Grok, rank Grok specially, or claim an xAI partnership. It puts the same instrument under the Grok TUI that already sits under Claude Code and Cursor.

## Install (same four tools on every TUI)

```
/council  /gspc  /verify  /sign
```

**Grok Build** — GitHub pin works today. The xAI official-catalog short name waits on [plugin-marketplace#398](https://github.com/xai-org/plugin-marketplace/pull/398).

```bash
grok plugin install CSOAI-ORG/council-of-ai-grok --trust
# or a local checkout
grok plugin install "$HOME/.grok/plugins/council-of-ai" --trust
```

**Claude Code** — catalog is `.claude-plugin/marketplace.json` on this repo:

```bash
claude plugin marketplace add CSOAI-ORG/council-of-ai-grok
claude plugin install council-of-ai@council-of-ai
```

If Claude cached an empty clone:

```bash
claude plugin marketplace add "$HOME/.grok/plugins/council-of-ai"
```

**Cursor** — catalog is `.cursor-plugin/marketplace.json` (source `./`, owner CSOAI Ltd). Add marketplace `CSOAI-ORG/council-of-ai-grok` in Cursor Settings → Plugins, or from a checkout:

```bash
# Cursor reads the repo-root .cursor-plugin/ marketplace; do not copy the four tools
```

**Codex** — skip until `which codex` finds a binary.

**GitHub Action** (verify in CI — a bank’s pipeline is an agent host):

```yaml
- uses: CSOAI-ORG/council-of-ai-grok/.github/actions/verify-card@<40-char-sha>
  with:
    card: https://councilof.ai/signed/cards/<id>.json
```

Pin a full SHA, never `main`. Three states: VALID / INVALID / UNCHECKABLE.

Offline CLI: `node verifier/gspc-verify.mjs --json card.json`  
Human UI: https://councilof.ai/verify

See `docs/MARKETPLACE-PR.md` for the xAI catalog JSON.
`docs/PREIMAGE-FIX.md` is the next living-stamp rule. `docs/GAP-INDEX.md` is the weekly hollow-row tape ([`csoai/gspc-gap-index`](https://huggingface.co/datasets/csoai/gspc-gap-index)).

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
| `.mcp.json` | `https://councilof.ai/mcp` + `npx -y csoai-gspc-mcp` + `npx -y csoai-governance-mcp` |
| `hooks/hooks.json` | Session start / stop hints (non-blocking) |
| `scripts/gspc-board.mjs` | Honest CLI summary of `GET /api/gspc` |

## MCP fallbacks

- **GSPC tools over HTTP:** `POST https://councilof.ai/mcp` (`board_totals`, `get_axis`, `verify_card`, `list_cards`)
- **GSPC stdio (npm):** `npx -y csoai-gspc-mcp` (same four tools)
- **Governance MCP on npm:** `npx -y csoai-governance-mcp` (`csoai_sign`, `csoai_verify`, `csoai_govern`, `csoai_catalog`)

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
