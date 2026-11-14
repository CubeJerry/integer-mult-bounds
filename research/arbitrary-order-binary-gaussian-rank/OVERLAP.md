# Bounded overlap and discovery provenance

Canonical base: `e54523517d0f03e58352e647c403a5af3e525a57`.
The lead retained the global allocation/claim manifest; this scope was assigned
as wave 9, structural decoder/adversarial audit, after the source-gauge package
was frozen. No other worker was assigned the same proof. The third worker's
matching/coefficient check was explicitly independent verification.

The exact live PR heads and search counts are in [OVERLAP.json](OVERLAP.json).
The checks below were read on 2026-11-14; they are bounded coverage, not a
proof of novelty or a complete archival survey.

- [#1754](https://github.com/CrocSwap/integer-mult-bounds/pull/1754), head
  `d8046736d984645a6f79159b2a7454d1919d24b3`, proposes structured boundary
  solves for Toeplitz/gauged phase-cell blocks. Its component and precision
  assumptions differ from this all-order generic binary rank theorem.
- [#4198](https://github.com/CrocSwap/integer-mult-bounds/pull/4198), head
  `e457d5e912a27307d725827aeca7198169320b84`, constructs bounded rational
  generators for a supplied displacement matrix. Its generator count is
  that matrix's rank; it does not supply this rank lower bound.
- [#6228](https://github.com/CrocSwap/integer-mult-bounds/pull/6228), head
  `d85df7f7524e41799a6db2d6c082f6cadbd5cc84`, refines generator normalization;
  [#6239](https://github.com/CrocSwap/integer-mult-bounds/pull/6239), head
  `80c537689f297b19dcd435d71623d2c743856650`, binds a normalized rank-one
  row to a rounded child. Neither removes the arbitrary-order rank question.
- [#7263](https://github.com/CrocSwap/integer-mult-bounds/pull/7263), head
  `d9219ca07e69ca08c6cc7ec9dc805955fe87d857`, gives exact factor-one norm
  bounds with at most twice the rank-many generator terms. This proof
  concerns the necessary rank before such normalization.

Live title searches returned three displacement-title records and four
Stein-title records. A broad arbitrary-order query returned the first thirty
of sixty-nine records; broad body searches were noisy and incomplete.
Unpublished work, arbitrary historical diffs and the full Discussion corpus
are outside this bounded check. The prior in-session published lexicographic,
orbit and symmetry results are pinned and distinguished in README/PROOF.

Primary literature search found Olshevsky, Oseledets and Tyrtyshnikov's
[2006 tensor/displacement paper](https://doi.org/10.1016/j.laa.2005.03.040).
Its distinction between tensor structure and displacement structure is
credited background. Searches for Boolean-cube/displacement and
Gaussian/Stein/ordering terms did not identify the exact present theorem;
this is not a worldwide priority claim.

## Discovery ledger and stopping boundary

The initial conjecture was full generic rank N for every order. An exact
rational counterexample only refuted a pointwise strengthening: q=(1/2,1/3,1/5)
can have rank 6 at N=8 despite distinct entries. The determinant polynomial
at that order is nonzero, so this is not a generic counterexample.

A coordinate-specialization certificate covered 4,368 of 5,040 normalized
N=8 orders. Allowing every nonzero translation mask covered all 5,040.
A deterministic exploration with seed 20261114 and a cap of 10,000 orders
per dimension found all-mask connected-criterion failures at sample 296
for d=4 and sample 162 for d=5. At d=6, 10,000 samples completed without
such a failure. Those observations are discovery evidence only; the final
replay retains the exact d4/d5 witnesses and does not rerun the random search.
All larger dimensions and unvisited orders remain unsearched.

The approved pivot was the universal weaker rank bound derived from the
same exact matching coefficients. The stated theorem was proved and checked;
search stopped without extending finite coverage into the unresolved full
rank conjecture. No actual source parameter genericity or rounded tolerance
was attempted. Root and the separate review worker independently checked the
critical proof; those reviews are distinct from rerunning the author code.
