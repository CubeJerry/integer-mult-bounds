# Frozen-prefix causal arrival floor

**Scoped proof with exact source certificate. No new kappa.**

With literal prescribed main-prefix rows AND literal main MOVE payloads, the
selected source requires **984 new cochart information arrivals** even granting
unlimited stationary memory, free scalar work, free main routes and arbitrary
unit-priced row teleportation. If source-helper MOVEs also always carry one fixed
common code, at least **937 added arrivals** remain after crediting all 47 original
owned routes with arbitrary useful difference data. The unchanged H4 profile
allows at most 98 added positive-rank moves. With literal main MOVE payloads,
at least **839 helper arrivals** must instead carry useful difference data after
both favorable grants. Repurposed main MOVE payloads are an additional explicit
escape and must be added to the generalized innovation tally.

Read [PROOF.md](PROOF.md) for every model restriction, the exact excess-rank proof,
and next construction question. Mere equality at source-event boundaries does
not establish literal main MOVE payloads. The result does not exclude changed
main-state histories or variable helper/main transport codes.

## Reproduction

From the repository root:

```sh
python3 -B research/moonshot-005-program/results/causal-arrival-floor/verify.py
python3 -O -B research/moonshot-005-program/results/causal-arrival-floor/verify.py
python3 -B research/moonshot-005-program/results/causal-arrival-floor/verify.py --records
```

Outside the repository, pass `--source /absolute/path/to/final.json.gz`.
Expected status: `PASS_FROZEN_PREFIX_CAUSAL_ARRIVAL_FLOOR`, 984 arrivals, 7,988
source demands, 1,610 free main innovations, 522 affected charts. `--records`
prints all 984 zero-based event records and by-chart counts, matching
[CERTIFICATE.json](CERTIFICATE.json). Both normal and optimized receipts match.
The verifier authenticates the compressed source before exact Fraction replay.
Equal-span charts 1091/1092 are merged freely; the count stays 984.

The strongest positive control grants every original auxiliary shadow MOVE
for free; the deficit then becomes zero. Other controls cover source corruption,
exact rational dependence and independence, chart-local information, fractional
linear combinations, COPY-zero, nonzero coefficients and cochart operation guards.
A separate reviewer reconstructs the count using fraction-free integer/max-pivot
elimination and reviews the potential proof; see `review/`.

## Evidence and limits

`PROOF.md` states the theorem; `verify.py` reconstructs its finite source count;
`CERTIFICATE.json` retains the full arrival list; `RESULT.json` and
`RESULT-OPTIMIZED.json` are concise receipts; `SOURCES.json` pins dependencies.
No native word, compiler admission, physical tariff, supplier or complete bound
is supplied. All five foundational assumptions remain. This result guides the
ongoing changed-main or adaptive-payload construction; it is not a universal
shared-core barrier.

Prepared for @CubeJerry with substantial OpenAI assistance. Credit the selected
#7000 native authors and the S001 coded-lift/capacity programme. Apache-2.0.
