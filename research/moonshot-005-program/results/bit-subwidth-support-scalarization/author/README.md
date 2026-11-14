# Support scalarization for extensions smaller than one whole width

For any field, any scalar code `B`, and any identity-diagonal block fitting
`A` of width `V`, if

    dim((row(A)+B tensor k^V)/(B tensor k^V)) < V,

then there is a scalar fitting in `B` with each row support contained in
the corresponding whole-block support of `A`. The proof chooses a nonzero
kernel vector separately at each receiver and a functional normalizing its
own coefficient. It allows noncommuting and singular matrices.

For the native canonical code, this gives a new necessary condition:
if the canonical quotient has dimension below `2V` and the complete target
requires `ell<=194`, that quotient cannot contain ANY full scalar-line
tensor `span(h+C) tensor k^V`. Otherwise scalarization relative to
`B=C+span(h)` contradicts the universal scalar205 support bound.

The strict boundaries are real. A two-port repetition-code example fails
scalarization at extra dimension exactly `V`; the native two-patch fitting
has `d=2V`, contains scalar lines and attains `ell=192`. Neither control
is a physical supplier. A three-dimensional graph subspace without a full
scalar line illustrates the remaining algebraic search class.

```bash
python3 -I -B research/moonshot-005-program/results/bit-subwidth-support-scalarization/author/check.py \
  --native research/paired-query-only-bit/retained/inputs/BIT-NATIVE-WORD.json.gz \
  --programme research/moonshot-005-program \
  --output /tmp/subwidth-support-scalarization
```

Expected status: `PASS_SUBWIDTH_SUPPORT_SCALARIZATION_CONTROLS`. Normal and
optimized Python runs give identical JSON. The universal proof is in
`PROOF.md`; finite controls are explicitly F2 examples and do not replace
the all-field argument. Independent review is pending. No new kappa,
strict supplier, foundational discharge, or physical packet-count claim.

Credit @CubeJerry and the named native, scalar, quotient and all-route
predecessors; substantial OpenAI assistance. Apache-2.0.
