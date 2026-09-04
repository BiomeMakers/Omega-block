# The Omega Block

Correlation-network features that improve systemic tail-loss
attribution beyond downside beta and conditional MES.

Companion repository for the preprint (PDF in `paper/`; SSRN link upon
posting). Five
per-asset features computed from daily prices alone; in pre-registered
paired ablations with a noise-placebo floor, the block adds 1.3 to 3.4
points of out-of-fold R2 to next-year tail-loss attribution over
baselines up to a 31-column replica of a vendor feature set, replicated
on two universes and two nearly disjoint periods, while the placebo
worsens the same model everywhere.

## Run the acceptance test on YOUR data

    python validate_omega_block.py --prices your_prices.csv \
           [--events your_fomc_dates.csv] [--receipt result.json]

`prices.csv`: wide CSV, first column Date, one column per asset. The
harness reruns the full protocol (5 asset folds, paired ablation,
same-width noise placebo, block bootstrap) and prints an explicit
PASS or FAIL. Without an event calendar, only the static features are
tested.

## Signal-trial mode (no formulas needed)

    python validate_omega_block.py --prices your_prices.csv \
           --features omega_features_465.csv

Tests the block as a plain numbers file: nothing but values enters
your environment. `omega_features_465.csv` covers 465 S&P constituents,
2016-2025. Verified blind: +0.036 vs a -0.016 placebo (cert_demo.json).

## Evaluating against a baseline you cannot see

`PROTOCOL.md` states the evaluation method separately from this case: the run
happens in your environment, your baseline replaces ours, the acceptance rule is
fixed before the run, a same-width noise placebo sets the floor, and the receipt
carries only aggregates. It also states what the protocol does not solve.

## Replication registry

See REGISTRY.md. PASS and FAIL results are equally welcome; use
`--receipt` to produce an aggregates-only, shareable JSON (nothing is
ever transmitted automatically).

## Contents

- validate_omega_block.py    acceptance harness (features mode, receipt)
- omega_features_465.csv     signal-trial feature file (SHA-256 committed)
- REGISTRY.md                public replication registry
- paper/                     the preprint PDF
- prereg/                    written pre-registrations, before each run
                             (working documents, in Spanish)
- results/                   result logs for every number in the paper
- figures/                   the paper's figures and their generators

## License and patent notice

Code is released under the MIT License. The quantities Q1-Q5 and their
use as inputs to risk-attribution models are covered by USPTO
provisional applications 64/112,912, 64/121,656 and 64/140,524
(Omega-S family). Research and evaluation use is encouraged; commercial
use in third-party risk products requires a license
(acedo@biomemakers.com).
