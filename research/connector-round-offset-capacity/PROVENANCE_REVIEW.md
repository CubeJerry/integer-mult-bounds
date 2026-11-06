# Bounded overlap review: deterministic round-offset cancellation

Reviewer: worker B (`recovery_lower`), for @CubeJerry with substantial OpenAI
Codex assistance. Date: 2026-11-06. Canonical source and tree metadata base:
`7c49fe32c55de02c2c873655c804b16e4c3fef0a`.

No matching round-start offset-cancellation construction or proof of capacity
constant one was located in this bounded search. This is not an exhaustive
novelty claim. Partitioning into subset palettes and generic disjoint-union
generation are classical; the specific exact-floor modular-round realization
and its capacity consequence are the contribution under review.

## Substantive predecessor checks

- CrocSwap/integer-mult-bounds#6107 is merged. Its canonical
  `connector-bounded-depth-cap/README.md` leaves the general coefficient in
  `[1/2,1]` open and asks for depth-three blocks on about `2 log_2 c`
  sources. It proves the fixed-depth ceiling that the new construction
  attains to leading order.
- CrocSwap/integer-mult-bounds#6071 is merged. Its canonical
  `connector-gray-growth/README.md` supplies the preceding coefficient
  `1/2`, Gray construction, and `Theta(c log c)` context.
- CrocSwap/integer-mult-bounds#4231 and
  CrocSwap/integer-mult-bounds#4248 are merged. Their canonical interface
  and depth-block READMEs were read: repeated boundaries, ordinary positive
  calls, dirty cancellation, concatenation, and counting are inherited.
- CrocSwap/integer-mult-bounds#6568 is open. Its body gives balanced closed
  walks with an extra `log_2 log_2 c` source term but the same leading
  coefficient `1/2`; no modular round-offset cancellation appears there.
- CrocSwap/integer-mult-bounds#6692 is open. It is a navigation ledger;
  L10 explicitly retains the leading-coefficient question as partial.
- CrocSwap/integer-mult-bounds#4256 is merged. Its full canonical
  `full-coefficient-connector/README.md` was read. It partitions sources
  into blocks and exposes block projections via separately restored torus
  cycles, but treats all `c^n-1` coefficient rows at fixed characteristic,
  allows source multiplicities above `c`, and proves an overhead exponent.
  This is relevant block-palette context, not the binary exact-floor
  capacity result. The partition idea should not be claimed new.
- CrocSwap/integer-mult-bounds#2208 is merged, by `conorholds`, head
  `28480ef4fdb4caeab89765ea56595bf1f6f37688`. Its full PR body was read.
  It supplies earlier block palettes and counting in signed/two-root
  alphabets, not this characteristic-dependent one-root floor theorem.

The canonical `scalable-dirty-connectors/README.md` was also read. It uses
additional dirty roots and paid root transfers in characteristic two; its
frame cancellation differs from the present ordinary boundary read.

## Search coverage

The retained full canonical path metadata was searched for connector,
capacity, round, offset, group, partition, subset-generator, and palette
packages. Relevant READMEs above were read selectively. The approximately
700-open-PR retained snapshot was searched for round-boundary and offset
cancellation, grouped subsets, and leading/capacity constants. The relevant
hit was the still-open L10 question in
CrocSwap/integer-mult-bounds#6692.

Live all-state searches used `repo:CrocSwap/integer-mult-bounds is:pr`,
requested up to 100 results, and returned these counts without pagination
truncation:

| Additional terms | Returned / total |
|---|---:|
| `"round" "connector"` | 58 / 58 |
| `"offset" "connector"` | 3 / 3 |
| `"leading constant"` | 9 / 9 |
| `"partition" "connector"` | 19 / 19 |
| `"grouped" "connector"` | 6 / 6 |
| `"round boundary"` | 46 / 46 |
| `"subset" "capacity"` | 59 / 59 |
| `"constant one"` | 64 / 64 |

Returned titles and matching body passages were screened; technically close
PR bodies were read. GitHub tokenization makes several phrase queries
broad, so these are retrieval counts, not mathematical occurrence counts.
The earlier `depth3-check/OVERLAP.md` gives complementary predecessor
coverage. Its proposed probabilistic theorem was superseded and is not a
published dependency of the deterministic result.

Discussion comments, arbitrary historical diffs, most archive contents,
uncaptured terminology, and unpublished work remain unchecked. No exhaustive
priority or literature novelty certification is claimed.

Generic disjoint-union generators, including partition constructions, have
classical literature, such as Ellis--Sudakov, *Generating all subsets of a
finite set with disjoint unions*, JCTA 118 (2011), 2319--2345,
DOI `10.1016/j.jcta.2011.06.003`, located by the earlier review. This review
did not re-audit that paper; the connector proof is self-contained.
