# Independent U≤2 movement and descending-cache-chain review

## Directed movement bound

For each of the nine packet paths from Hub (dimension 8) to zero, let `u_p`
be its total upward MOVE rank and `d_p` its downward MOVE rank. Endpoint
telescoping gives `d_p - u_p = 8`, so that path's total MOVE rank is
`8 + 2u_p`. Summing gives total packet MOVE rank at least `72 + 2U`, where
`U = sum_p u_p`.

For every integer MOVE rank `q` from 1 through 8,

`q^(199/200) / q = q^(-1/200) >= 8^(-1/200)`.

Thus the movement moment is at least `(72 + 2U) 8^(-1/200)`. The retained
fixed clean-X/minimum-Y caller leaves less than `5.707155578155487` limiting
moment after the nine direct rank-eight returns. At `U=3`, the extra movement
alone is at least `6·8^(-1/200) > 5.937939938491241`, exceeding that room by
more than `0.2307843603357546`. Therefore every completion in this retained
caller must have integer `U≤2`. The directed 192-bit calculation is in the
JSON receipt.

I also independently recomputed the broader optimistic budgets at the same
exponent:

| Interface and extra movement | First excluded value | Directed deficit above limiting Q ceiling |
|---|---:|---:|
| Fixed clean X, minimum Y, nine packets | `U=3` | `>0.2307843603357546` |
| Arbitrary monotone X/Y routes, nine packets | `U=6` | `>0.3338731499299618` |
| All original records may reverse | `R=7` | `>1.2860363097869528` |

Here `R` is total X/Y downward MOVE rank plus packet upward MOVE rank. Endpoint
variation gives total MOVE rank at least `1626 + 2R`. These are optimistic
necessary movement limits, not constructions. The extra `102` rank-one
arrival arithmetic has deficit `>90.45799327294747`, conditional on the
separate arrival-count premise.

## Exact clean-source reconstruction

I replayed the X/X ADD/SWAP and X MOVE subword directly from the pinned native
word. The replay recreates all 1,027 source histories byte-for-byte against
the pinned screen, restores the 111 X input rows and their endpoint charts,
and charges 628 X ADD/SWAP events with MOVE profile `{1:289, 2:244}`. Every
history row's original-port support was checked to lie in its recorded real
chart.

For a chart of dimension `d`, define its source support as the union of the
original input ports appearing in all observed X-history rows at that chart.
The dynamic program computes the largest port union along one strictly
nested chain of history charts. It intentionally permits combining all rows
at a visited chart, so the result is an optimistic support cap, not a
realizable single packet row or a costed cache schedule.

| Start dimension | Largest whole descending-chain port union | Largest union strictly below the start chart |
|---:|---:|---:|
| 1 | 1 | 0 |
| 2 | 2 | 1 |
| 4 | 11 | 2 |
| 6 | 18 | 11 |
| 7 | 19 | 18 |
| 8 (Hub) | 111 | 19 |

The same caps are computed over every possible native upper frame, including
frames without source histories. The Hub's 111-port union is available only
when reads at the upper Hub chart itself are allowed; a single nested chain
strictly below Hub reaches at most 19 original ports.

## Turn intervals and target-first cap

I enumerated every rank-one and rank-two upward chart edge in the native frame
set. The upper endpoint need not itself have a history row. For each edge
`A→B`, the interval computation asks for source-history charts on a single
nested descending chain from `B` to `A`; each such cache chart must contain
`A`. It reports the support union with an upper-endpoint read and the stricter
union below that endpoint. The maximum number of final facets containing `A`
is shown separately.

| Up rank | Lower dim | Upper dim | Edges | Max final facets containing lower chart | Full interval chain union | Strictly below upper |
|---:|---:|---:|---:|---:|---:|---:|
| 1 | 0 | 1 | 111 | 111 | 1 | 0 |
| 1 | 1 | 2 | 306 | 62 | 2 | 1 |
| 1 | 6 | 7 | 360 | 2 | 15 | 12 |
| 1 | 7 | 8 | 120 | 1 | 111 | 13 |
| 2 | 0 | 2 | 153 | 111 | 2 | 1 |
| 2 | 2 | 4 | 459 | 30 | 10 | 2 |
| 2 | 4 | 6 | 540 | 12 | 16 | 9 |
| 2 | 6 | 8 | 180 | 2 | 111 | 15 |

For each target facet `F_i`, I allowed either one rank-two turn or two
rank-one turns, with each lower endpoint contained in `F_i`. If upper-endpoint
cache reads are excluded, the largest union of original ports on those
interval chains is at most 15 for every one of the 111 targets. The per-target
certificate includes the exact chart-chain witnesses.

## Scope limit

This is a cache-support statement about the exact clean X-only source. It does
not exclude nonlocal information added at an upper endpoint. For example, a
rank-one turn from a target facet to Hub may read Hub histories whose union
contains all 111 input ports; that is a single packet field carrying one
linear value, and it is deliberately not treated as 111 independent rows.
The `≤15` target-first cap concerns only the source-cache rows on the
strictly-lower interval chains. It is not a completion impossibility result.

The exact source and movement receipts are
[`U2-DESCENT-CAPS.json`](U2-DESCENT-CAPS.json) and
[`REVERSAL-BUDGET-REVIEW.json`](REVERSAL-BUDGET-REVIEW.json). Their source
scripts are [`check_u2_descent_caps.py`](check_u2_descent_caps.py) and
[`review_reversal_budgets.py`](review_reversal_budgets.py); the inputs and
outputs are pinned by [`MANIFEST.json`](MANIFEST.json).
