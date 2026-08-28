# ALIGNMENT.md addendum — Grok lane (2026-08-28)

Paste this as a new section in `ALIGNMENT.md` on `master` (do not rewrite the Claude / Vite history).

---

## 10. Grok Build TUI (added 2026-08-28)

Council of AI is the **governance floor under Grok Build**, same as under Claude Science / Claude Code.

Plugin pack: `grok-plugin/` in this repo *or* dedicated `CSOAI-ORG/council-of-ai-grok` (preferred for marketplace SHA pins).

Doctrine file for Grok sessions: `GROK.md`.

### Install one-liners

```bash
# TUI plugin (local)
grok --plugin-dir /path/to/council-of-ai-grok inspect

# MCP HTTP
# POST https://councilof.ai/mcp

# MCP npm
npx -y csoai-governance-mcp

# After official catalog merge
grok plugin install council-of-ai --trust
```

### What Grok must not do

- Call `/chat` on the Sovereign brain without the same honesty rules as `askSovereign` (no companion bleed, no fake seals).
- Treat a Layer-0 seal as EU AI Act conformity.
- Check out `main` and deploy it.

### Marketplace

Catalog PR text lives in `docs/MARKETPLACE-PR.md`. Remote source must pin a 40-character SHA. xAI code-owners review required.

---
