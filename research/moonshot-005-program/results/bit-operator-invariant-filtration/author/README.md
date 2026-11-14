# Additive innovation across common invariant operator layers

For a target-compatible native block fitting with a common invariant flag
whose layer dimensions are `v_1,...,v_s`, the proposed theorem gives

    dim((row(A)+C tensor k^V)/(C tensor k^V))
       >= V + sum_a ceil(v_a/17).

The weighted version replaces 17 by `17-min(b,9)`, where `b` counts
double-saving rows. If the coefficient family is simultaneously
triangularizable over any extension field, the quotient must have dimension
at least `2V`. Every commuting family is covered, including nilpotents and
families that do not split over the original field. A noncommuting family
may still preserve a complete flag and therefore remain subject to `2V`.

`PROOF.md` supplies the universal argument. It applies the new proportional
quotient theorem on each invariant layer and proves additivity using a
nonsingular-minor argument for the rectangular upper-triangular matrix
`vertical_stack(A, B tensor I)`. Ordinary rank of `A` alone is not silently
substituted for canonical quotient dimension.

`SCALAR-FITTING.json` freezes an explicit algebraic boundary example with
`ell=193`, rank eleven, and canonical quotient dimension two. It includes
all canonical/fitting rows, patch choices, and a nonsingular eleven-by-eleven
minor. The tensor lift attains the commuting `2V` bound for every width.
Its supported history uses eleven ports (twelve including the retained
pivot), so the point-retained handoff theorem still prevents the corresponding
static point-only realization. No actual decoder is supplied.

The controls include non-diagonalizable commuting matrices, a nonsplit F2
commuting family diagonalized exactly over GF4, noncommuting upper-triangular
coefficients, a two-plus-three invariant flag, and an opposite-nilpotent pair
without a common invariant line even over an algebraic closure. These delimit
the theorem's hypotheses; they do not establish a cheap irreducible source.

```bash
python3 -I -B research/moonshot-005-program/results/bit-operator-invariant-filtration/author/verify.py \
  --native research/paired-query-only-bit/retained/inputs/BIT-NATIVE-WORD.json.gz \
  --density-proof research/moonshot-005-program/results/bit-operator-quotient-density/author/PROOF.md \
  --point-proof research/moonshot-005-program/results/bit-point-retained-handoff-gate/author/PROOF.md \
  --output /tmp/operator-invariant-filtration
```

Expected status: `PASS_OPERATOR_INVARIANT_FILTRATION_CONTROLS`. Normal and
optimized Python runs give identical result and scalar-fitting JSON.
Independent proof review is pending. No new complete kappa, strict supplier,
or foundational discharge is claimed. Credit @CubeJerry, the explicit
predecessor proofs and native contributors; substantial OpenAI assistance.
