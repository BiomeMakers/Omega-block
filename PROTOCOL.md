# Federated evaluation against a baseline you cannot see

A protocol for deciding whether a candidate feature adds anything to a risk model
whose composition is proprietary, without either side disclosing anything.

## The problem

A vendor or an institution has a risk model. Someone proposes a feature that
might improve it. Neither party can run the experiment that settles the question:

- The proposer cannot evaluate against the incumbent baseline, because its
  composition is confidential. Evaluating against a public replica answers a
  different question, and everyone knows it.
- The incumbent cannot evaluate the feature, because its construction is the
  proposer's asset.
- Publishing the comparison is against both parties' interest: if the incumbent
  wins there is nothing to report, and if it loses the report devalues a product.

The result is that this comparison is almost never made. The literature evaluates
against public baselines, and the decisions that matter are taken against private
ones.

## The protocol

Five requirements. The first three make the comparison meaningful, the last two
make it publishable.

**1. The evaluation runs in the incumbent's environment.** The proposer ships a
harness, not a request for data. The harness reads the incumbent's price panel
and rebuilds the whole comparison locally. Nothing is transmitted.

**2. The incumbent's baseline replaces the proposer's.** The harness ships with a
public baseline as a default, which the incumbent substitutes with its own. This
is the point of the exercise and it is the harder test: the candidate must add
over a stronger rival than the one its author could assemble.

**3. The acceptance rule is fixed before the run.** A single pre-registered
criterion, stated in the harness and not chosen afterwards, that resolves to PASS
or FAIL. In the demonstration below: the lower bound of the candidate's paired
confidence interval must exceed the upper bound of a same-width noise placebo.

**4. A placebo floor of the same width.** Columns of noise, as many as the
candidate has, put through the identical pipeline. Without it, a positive number
means nothing: any feature block of sufficient width moves a flexible model.
The placebo is what converts "it went up" into "it went up more than width does".

**5. The output is an aggregates-only receipt.** Means, confidence intervals,
placebo floor, verdict, configuration fingerprint, and a hash. No tickers, no
returns, no baseline composition. The receipt is shareable by construction, so
the incumbent can publish a result without publishing anything about its model.

Two options widen who can participate. In **signal-trial mode** the candidate
ships as a plain table of numbers rather than as code, so no formula enters the
incumbent's environment. And receipts may be listed under a withheld identity,
though a named receipt is worth more to a reader than an anonymous one.

## What the protocol does not solve

**Nobody verifies the run.** The receipt hash certifies that the file has not
been altered after the fact, not that the computation used real data. The
protocol rests on the reputation the submitter puts behind the receipt, which is
why a named receipt from a credible institution is worth many anonymous ones.

**Receipts are not comparable across environments.** A given improvement over a
weak baseline is not the same as the same improvement over a strong one, and each
participant runs its own universe and period. A registry of receipts accumulates
evidence; it does not produce a ranking. Ranking would require a fixed panel and
a fixed calendar, which is a different and weaker exercise, because it no longer
answers the question the incumbent actually has.

**FAILs must be recorded with the same weight as PASSes**, or the registry is
advertising. A protocol whose registry contains only positives has selected them.

## Demonstration

The Omega Block, five correlation-network features for systemic tail-loss
attribution, is the worked example: pre-registered acceptance rule, placebo
floor, receipt, and a public registry that lists PASS and FAIL alike. Harness,
pre-registrations and results at github.com/BiomeMakers/Omega-block; preprint at
SSRN 7363442.

The example is not the point. Any candidate feature for any model whose baseline
is proprietary fits the same five requirements.
