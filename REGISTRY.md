# Omega Block: public replication registry

Every run of `validate_omega_block.py` can produce a result certificate
(`--receipt result.json`, with an optional `--label`): a machine-readable summary of the ablation
(dR2 with CI, placebo floor, pass/fail, configuration fingerprint,
SHA-256 of the receipt). The receipt contains ONLY aggregates: no tickers, no returns, no baseline composition. NOTHING is transmitted automatically, ever.

If you are willing to have your run listed here, send the JSON (and any
context you wish) by opening an issue in this repository or by email.
PASS and FAIL results are equally welcome: passes replicate the claim,
fails map its boundary, and both are credited.

| date | submitter | universe (n, period) | baseline | dR2 Omega (CI95) | placebo | verdict |
|------|-----------|----------------------|----------|------------------|---------|---------|
| 2026-08 | authors | 465 US large caps, 2016-2025 | maximal public + size/liquidity (26) | +0.013 (+0.008, +0.018) | -0.012 | PASS |
| 2026-08 | authors | 459 US large caps, 2012-2017 | maximal public + size/liquidity (26) | +0.013 (+0.006, +0.021) | -0.005 | PASS |

Submissions under NDA (paid evaluations) are recorded in a private
registry and listed here only with written consent of the submitter.
