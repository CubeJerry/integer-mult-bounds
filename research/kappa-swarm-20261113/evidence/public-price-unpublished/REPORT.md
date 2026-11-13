# Public helper-relation cache screen

## Scope and result

This is a source-bound, exact-rational screen of the retained #7481 native
word and its 17-call signed caller. It asks whether one helper-only scalar
relation can make a public MOVE target recoverable from strictly earlier
same-span native observations, while the native observation history stays
fixed. It does not change MOVE endpoints or histories, import cross-chart
observations, or claim that a relation can be physically prepared.

The exhaustive first pass covers all 6,279 MOVE events. It separates 468
helper-only targets. Of the remaining 5,811 nonzero-main targets, 1,080 lie in
the prior main-projection history (14 owned and 1,066 public); 4,731 miss it
(33 owned and 4,698 public). Public main-history hits by paid target rank are:

| Target rank | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Public main-history hits | 611 | 128 | 177 | 27 | 111 | 4 | 6 | 2 | 0 |
| Public main-history misses | 3,029 | 706 | 603 | 175 | 175 | 10 | 0 | 0 | 0 |

Every one of the 1,066 public main-history hits is also a strict full-history
miss. A paired main-projection/full-row replay computes the prior helper
kernel `K=P∩H` and, for each target `c`, its helper residual `g=c-p∈H`, where
`p∈P` matches the main projection of `c`. The full-history miss condition is
exactly `g∉K`. In that case the new one-cache relation space is
`K+span(g)`, so its support is the union of the support of `K` and `g`. The
least helper target rank in that union is the minimum one-row debit. If the
cheapest coordinate occurs only in `K`, add a `K` row containing it to `g`,
choosing a nonzero coefficient that avoids cancellation; the sum remains
outside `K`.

The exhaustive optimistic one-relation price classes at \(\kappa=0.0038\)
are 376 positive, 437 exactly zero, and 253 negative. Every zero profile has
equal target and minimum-debit ranks. Since all ranks are positive, for every
\(0\le\kappa<1\) the profile's sign is exactly the sign of the rank
difference; at \(\kappa=1\) all these profiles are zero. The best
gross saving is event 40710: a rank-8 public MOVE (owner 885, frame 3 to 189)
with the helper-only relation

\[
  -h_{1459}-h_{705}+h_{885}.
\]

Its minimum helper target debit has rank 1. The exact certified interval for
\(f(8)-f(1)\) is

\[
  [6.937034079270974725608699,
   6.937034079270974725608700].
\]

For comparison, the exact 17-call invoice has signed moment
\([-59.241933884374900242189582,
-59.241933884374900242139925]\); a single per-call improvement must exceed
\([3.48481964025734707306705,
3.48481964025734707306998]\). Thus the one-relation **rank-price allowance**
for this event exceeds that threshold before any implementation costs.

## Cross-checks

The first screen and the paired all-target replay are separate exact
reconstructions. A further direct source replay independently checked all 16
rank-stratified full-L space samples: the target row and destination history, main-history
hit, full-history miss, `L_E` dimension, minimum debit rank, exact history
identity, and rank-price class all agree with the all-1,066 paired screen.
The exact candidate identity for event 40710 is

\[
  c = (-h_{1459}-h_{705}+h_{885}) + P_0 + P_2,
\]

where `P_0` and `P_2` are the independently replayed prior destination-history
basis rows. The direct checker confirms the relation is outside the prior
helper history and is helper-only. The all-16 check includes a real
equal-rank cancellation control: `f(5)-f(5)=0` exactly, and rejects the
mutant that collapses the profile to a single negative coefficient.

The 4,698 public main-history misses are excluded from this mechanism: a
helper-only relation cannot supply their missing main projection under the
fixed-history model. The 468 helper-only targets are tallied separately.
Equal-span aliases are pooled in the normalized-history screen, deliberately
granting the cache more prior information; this is not evidence that two
physical charts have identical operator semantics.

## Physical limitation

This result does not establish an achievable public cache. The retained
grammar provides no free public INIT/CLEAR or zero-retag opcode, so replacing
a public MOVE with a zeroed destination/cache needs a separately justified
operation and full ordinary-operation, phase, precision, storage, and lifetime
costs. A separate source-specific prefix check also finds that event 40710's
gross rank-price surplus for this one credit does not survive the
unchanged-history preparation gate: `h885` is only available at the empty frame 3 before the event,
while `h1459`'s first later touch occurs after event 40710. Preparing the
destination relation from that source requires rank-8 movement (or changing
the fixed earlier history), which consumes the gross advantage. This is an
optimistic algebraic candidate only, not a physical win, source admission,
or `kappa` claim. This one-credit check does not bound other transfers that
the same helper promise might enable; their individual savings cannot be
summed without a separate shared-promise debit and whole-source bill.

A future positive case needs a source-legal way to prepare the helper
relation before the target without changing any earlier native observation,
and a fully priced public zero/reframe/cache operation. The current screen
does not find such a mechanism.

## Reproduction

Run from the workspace root:

```sh
python3 -I -B worker-c/public-helper-cache/scan.py --screen-only
python3 -I -B worker-c/public-helper-cache/paired_prices.py
python3 -I -B worker-c/public-helper-cache/profile_sign_check.py
python3 -I -B worker-c/public-helper-cache/verify_witness.py
python3 -I -B worker-c/public-helper-cache/crosscheck_samples.py
```

`RESULT.json` contains the first-pass screen and 16 detailed examples;
`ALL-ONE-RELATION-PRICES.json` contains all 1,066 public candidate prices;
`WITNESS-VALIDATION.json` and `SAMPLE-CROSSCHECK.json` are deterministic
validation receipts. `PROFILE-SIGN-VALIDATION.json` confirms all 437 zero
profiles are equal-rank cancellations. The saved source pins are in
`SOURCES.json`.
