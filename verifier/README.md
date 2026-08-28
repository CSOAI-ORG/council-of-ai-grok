# Verify primitive

One file. No account. Offline after you hold the bytes.

```bash
# CLI (Node 19+)
node verifier/gspc-verify.mjs --json path/to/card.json

# GitHub Action (CI is an agent host)
# uses: CSOAI-ORG/council-of-ai-grok/.github/actions/verify-card@<sha>
# with:
#   card: https://councilof.ai/signed/cards/<id>.json
```

Three states: **VALID / INVALID / UNCHECKABLE**. A bank job that cannot fetch the DID pin must fail UNCHECKABLE, not pass.

Human UI: https://councilof.ai/verify  
Rule: https://councilof.ai/signed/HOW-TO-VERIFY.md

This is measurement, not certification. An INVALID card is a failed integrity check, not a grade.
