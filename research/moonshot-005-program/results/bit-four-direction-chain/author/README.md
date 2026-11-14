# Four-direction chain: exact fitting, binary obstruction, and real geometry

This package proves a scoped all-field chain obstruction and constructs an
exact native algebraic fitting beyond the scalar-envelope-three boundary.
It does not construct a physical source or improve the complete exponent.

- A three-dimensional chain quotient with four scalar envelope directions
  contains no nonzero pure tensor, even after extending the field.
- The displayed native binary fitting has quotient3, scalar envelope4 and
  cardinality charge216. Its fixed permitted binary code has optimum216.
- Any chain whose saving rows use at most three exceptional conic kernels
  has charge at least197. In particular, every binary chain is excluded
  from the target194 class. A larger-field target needs at least four types.
- The displayed fitting has linear/quadratic rank proxy219 and exact capped
  proper-subspace covering proxy220. A rank-six unique vanishing quadratic
  prevents one receiver's support from being covered by two proper charts.

The native source is byte-pinned in every source-dependent script. The
universal arguments are in PROOF.md; the exact finite controls supplement
them and do not replace them. SOURCES.json identifies inherited premises.

## Reproduction

Run the following with Python3.11 or later, replacing PACKAGE by the location
of this package and NATIVE by the pinned BIT-NATIVE-WORD.json.gz file:

```sh
python PACKAGE/author/check.py --native NATIVE --output /tmp/chain-native.json
python PACKAGE/author/capacity.py --output /tmp/chain-capacity.json
python PACKAGE/author/geometry.py --native NATIVE --output /tmp/chain-geometry.json
```

Expected summaries are PASS_NATIVE_FOUR_DIRECTION_CHAIN with216/3/4 and378
row-pair cases; PASS_CHAIN_CAPACITY_CONTROLS with3780 full-rank F4 selectors,
36 identity-admitting binary selectors and coverage census21/15; and
PASS_EXACT_CHAIN_GEOMETRY with216/219/220. Repeat using `python -O`; the JSON
receipts must be identical. No third-party package is required.

## Remaining obligation

Construct a larger-field chain with at least four exceptional receiver
kernels and sufficiently small exact real support incidence, or change the
quotient geometry. Geometric feasibility, a legal physical history and
complete target-supplier accounting remain separate obligations. No new
kappa. Prepared for @CubeJerry with OpenAI assistance and predecessor credit
as stated in PROOF.md.
