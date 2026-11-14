# Independent mathematical review of the scalar Gram family obstruction

**Pass, for the precise source-specific linear continuation theorem. No new kappa.**

Reviewed `relay-sunit-family/PROOF.md` at SHA256
`65f4b9e3feec267a561db4a1fda311de6aa7a32a6c15c8e5bc823731500da791`.
The author checker was not imported or used. This review reconstructed the
76-row Gram matrix from the pinned literal relay source and used an explicit
dyadic block intertwiner to certify its characteristic polynomial. The review
also independently implemented the seventeen S-unit witnesses, their symmetry
orbits, the rational parameter map and the five remaining obstructions.

## Mathematical checks

1. The source matrix has the stated four scalar eigenvalues and two quadratic
   blocks: direct exact multiplication verifies `C P = P B`, while the eight
   nonzero orthogonal columns of P establish invertibility. This independently
   proves the determinant polynomial, rather than reproducing the author's
   nine-point polynomial test.
2. A unit product over `R = Z[1/30]` forces each of its factors to be a unit.
   The identity `u + w = 2v` therefore puts `u/(2v)` and its complement in
   the complete S-unit equation. The parameter formula is correct. The
   exceptional value `x = 4/9` yields an inconsistent equation, not an omitted
   finite lambda.
3. The seventeen triples are primitive, have the required prime support, and
   give seventeen distinct symmetry orbits, containing 99 ordered values.
   This is a finite certificate of witnesses and distinctness; its universal
   completeness comes from the published theorem below.
4. Restricting only lambda's denominator, rather than requiring lambda itself
   to be a unit, is essential and is done correctly. All four linear factors
   are units only for the five listed nonzero parameters. In particular
   `lambda = 7/64` is retained. Each candidate's quadratic factor has a
   numerator prime outside `{2,3,5}`.
5. If the determinant vanishes, the rational kernel prevents exact recovery.
   Otherwise a bad-prime residue kernel does so. Extending the residue field
   to contain a square root of -1 handles `R[i]` without an assumption about
   the splitting of that prime. The identity block on the restored coordinates
   makes the kernel's D component nonzero. Independent initial B fields can
   cancel its B-output component; the other independent public inputs and
   fresh zero helpers cannot remove the obstruction. Tensoring with identity
   covers every whole-field width.
6. `lambda = 0` is correctly excluded. The anisotropic matrix construction
   with determinant `3375/128` is correctly outside the theorem. The theorem
   does not prohibit arbitrary matrix preloads, new division primitives,
   correlated retained state, or an independently proved rounded interface.

## External completeness dependency checked directly

Rafael von Kanel and Benjamin Matschke, *Solving S-unit, Mordell, Thue,
Thue--Mahler and generalized Ramanujan--Nagell equations via Shimura--Taniyama
conjecture*, arXiv:1605.06079v1 (19 May 2016), Theorem A, manuscript page 7:
https://arxiv.org/pdf/1605.06079v1 .

The theorem gives 17 symmetry classes for the first three primes, precisely
`{2,3,5}`. The preceding definition of the classes and their sixfold symmetry
matches this proof. The paper credits this case to de Weger's Theorem 5.4.
The dependence on modularity is an established theorem, not an additional
unproved foundational assumption in this use. The review does not purport to
reprove that classical classification.

## Reproduction and scope

```
python3 -B check.py --repo /path/to/repository \
  --proof /path/to/relay-sunit-family/PROOF.md \
  --output RESULT.json
```

Expected status: `PASS_INDEPENDENT_SCALAR_FAMILY_REVIEW`; seventeen orbits,
99 values, and the five candidates with nonsmooth quadratic factors.

The proof and exact source calculation are accepted within the stated
restricted continuation model. This is an obstruction theorem for one
rescaling family, not an impossibility result for integer multiplication.
It establishes no supplier completion and changes no complete kappa.

Independent review prepared for @CubeJerry with substantial OpenAI assistance.
