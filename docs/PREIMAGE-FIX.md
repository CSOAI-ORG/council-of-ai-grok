# Next living-stamp preimage — sufficient rule

The published `measured_on.living_stamp` on GET `/api/gspc` is **UNVERIFIABLE**.
That is a completed finding, not a pending pass. Three faults, already on the
payload: two signatures for one stamp, signer not in `did.json`, axes
re-snapshotted after the signature date. 58,184 reproduction attempts verified 0.

We do not quietly re-label it VALID. The next stamp uses a rule a stranger can
run without guessing.

## Rule (same bytes as the site attestation that DOES verify)

The live `site_attestation` under `did:web:csoai.org#board-attestation-1`
verifies today. Copy that rule for every **new** living stamp:

1. Pin the key from `https://csoai.org/.well-known/did.json` (or
   `https://councilof.ai/.well-known/did.json`) `#board-attestation-1` /
   `#card-attestation-1` as appropriate. A stamp that carries only its own key
   is self-consistent, not authentic.
2. Drop the attestation object itself from the payload (`site_attestation`, or
   the living-stamp `signature` / `signer` / `sig_input` / `verification_state`
   fields — name them in `sig_input`, do not say "signature fields").
3. Canonical JSON: object keys sorted by code point, recursively; no
   whitespace (`separators=(',', ':')`); non-ASCII as literal UTF-8
   (`ensure_ascii=False`). Numbers follow JSON / ECMAScript (integral float
   is `0`, not `0.0` — this is **not** the measurement-card rule).
4. Ed25519 over the **raw UTF-8 bytes**, not a digest, not a hex digest.
5. One signature. One signer. That signer is in the DID document.
6. The axes in the signed bytes **are** the axes that were signed. Re-snapshot
   after sign is forbidden; it is how this stamp became UNVERIFIABLE.

`scripts/verify_stamps.py` checks the live board: site attestation VALID,
living stamp UNVERIFIABLE. Measurement, never certification.

## What this does not do

It does not make the old living stamp valid. It does not fill UNMEASURED
cells. It does not certify a model, an issuer, or a PDF.
