# Gap Index tape

Weekly count of **material claims with no stranger-recomputable row**.

- Source: live `GET https://councilof.ai/api/gspc`
- Hollow rows increment the index. UNMEASURED is not 0.
- `humanoid-labour-index` is listed UNMEASURED only. No public series exists, so it is not eaten as data.
- The tape itself is **UNSIGNED** until a DID-pinned key signs it. `content_id` is sha256 of the canonical body (same canonicalisation as `site_attestation`).
- Hugging Face: `csoai/gspc-gap-index`

```bash
python3 scripts/gap_index.py --out gap.json
python3 scripts/verify_stamps.py
```

Measurement, never certification. Procurement pays to narrow a gap, not to buy a medal.
