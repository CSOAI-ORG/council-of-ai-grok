# Grok Build marketplace — catalog entry + PR text

Official catalog: https://github.com/xai-org/plugin-marketplace  
Docs: https://docs.x.ai/build/features/skills-plugins-marketplaces  
News: https://x.ai/news/grok-plugin-marketplace

xAI does **not** accept drive-by code in `xai-org/grok-build`. Plugins enter through a catalog PR. Remote plugins must pin a full 40-character commit SHA.

## Before you open the PR

1. Publish this plugin tree on GitHub (recommended: dedicated repo `CSOAI-ORG/council-of-ai-grok`, or `grok-plugin/` on `master` of `councilof-ai`).
2. Pin HEAD:

```bash
git ls-remote https://github.com/CSOAI-ORG/council-of-ai-grok.git HEAD
# or, if vendored in the monorepo, pin that commit and set source.path notes in the PR body
```

3. Confirm `grok inspect` sees skills / MCP after a local `--plugin-dir` load.
4. Confirm `https://councilof.ai/mcp` and `https://councilof.ai/api/gspc` respond.

## Catalog JSON (paste into `.grok-plugin/marketplace.json` `plugins` array)

Replace `REPLACE_WITH_40_CHAR_SHA` after publish.

```json
{
  "name": "council-of-ai",
  "description": "Independent AI-behaviour measurement: live GSPC board, Ed25519 card verify, artifact seals. Measurement, never certification.",
  "category": "monitoring",
  "version": "0.1.0",
  "author": "CSOAI Ltd",
  "homepage": "https://councilof.ai",
  "keywords": [
    "ai-governance",
    "measurement",
    "ed25519",
    "eu-ai-act",
    "gspc",
    "attestation",
    "verify"
  ],
  "domains": [
    "councilof.ai",
    "csoai.org",
    "meok.ai"
  ],
  "tags": ["governance", "security", "evidence"],
  "source": {
    "source": "url",
    "url": "https://github.com/CSOAI-ORG/council-of-ai-grok.git",
    "sha": "REPLACE_WITH_40_CHAR_SHA"
  }
}
```

If the plugin lives only as a subdirectory of `councilof-ai`, say so in the PR and ask catalog maintainers whether they require a repo-root plugin (most installers clone the repo root and expect `plugin.json` / `skills/` at top level). **Prefer a dedicated repo.**

## Local validation (in a checkout of plugin-marketplace)

```bash
python3 scripts/generate-plugin-index.py
python3 scripts/validate-catalog.py
```

## PR title

`Add council-of-ai — independent AI behaviour measurement (third-party)`

## PR body

```markdown
## Summary

Third-party plugin for Council of AI (CSOAI Ltd, UK Companies House 16939677).

Council of AI is an independent measurement body: frozen published tests, Ed25519-signed cards, empty cells published as empty. Verification is free and loginless. This plugin does not certify systems and does not take money from anything on the board.

It adds Grok Build skills `/council`, `/gspc`, `/verify`, `/sign`, a read-only measurement-auditor subagent, non-blocking session hooks, and MCP:

- `https://councilof.ai/mcp` — board_totals, get_axis, verify_card, list_cards
- `npx -y csoai-governance-mcp` — sign / verify / govern / catalog

## Source

Remote, SHA-pinned:

- url: `https://github.com/CSOAI-ORG/council-of-ai-grok.git`
- sha: `<40 char>`

## Honesty / affiliation

Not an xAI partner listing. Not a ranking product. Grok is not given a special board slot by this PR. Measuring a model is permissionless.

## Test plan

- [ ] `python3 scripts/validate-catalog.py` passes
- [ ] `python3 scripts/generate-plugin-index.py --check` passes
- [ ] Local: `grok --plugin-dir /path/to/council-of-ai-grok inspect` lists skills + MCP
- [ ] `/gspc` returns live board with UNMEASURED rows left empty
- [ ] `/verify` on a published card returns VALID; bit-flipped body returns INVALID
```

## After merge

```bash
grok plugin marketplace list
grok plugin install council-of-ai --trust
```

To ship an update, bump the pinned SHA and open a follow-up catalog PR. Do not rely on floating `HEAD`.
