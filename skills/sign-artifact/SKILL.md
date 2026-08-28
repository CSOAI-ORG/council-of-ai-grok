---
name: sign
description: Seal a local file or eval receipt with CSOAI Layer-0 Ed25519 via the governance MCP. Use for /sign, "attest this output", "signed receipt". The seal is evidence of bytes at a time, not approval of the system.
when-to-use: sign artifact, seal receipt, Ed25519 attestation, csoai_sign
argument-hint: "<path or text>"
user-invocable: true
metadata:
  author: CSOAI Ltd
  short-description: Seal bytes, do not certify
---

# Sign / seal an artifact

## What this is

`csoai_sign` (MCP `csoai-governance`) binds an Ed25519 signature to the bytes you pass. That is a **receipt**: these bytes, this key, this moment.

It is **not** a certificate that the model, the repo, or the company is safe, legal, or approved.

## Steps

1. Identify the exact file or string. Prefer a file path in the workspace.
2. Call MCP `csoai_sign`. If MCP is missing, tell the user to run `npx -y csoai-governance-mcp` or open https://councilof.ai — do not fake a signature.
3. Return fingerprint, signature, public key.
4. Offer `csoai_verify` on the same payload so the user sees the round-trip.
5. If the artifact is an eval scoreboard, remind them that Council measurement cards are a different object (`gspc.measurement-card`) produced by the measurement body, not by this local seal.

## Forbidden

- Printing a badge, shield, or "certified"
- Signing and then saying the product "passed Council of AI"
- Inventing a signature when the MCP/brain is UNREACHABLE — return the error
