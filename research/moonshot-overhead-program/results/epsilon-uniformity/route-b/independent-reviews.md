# Independent Route B review of lead-researcher proofs

Reviewer: the separate `/root/route_b` agent. This is genuine cross-agent
review, not human review, Lean verification or a complete source-paper audit.
Review date: 2026-11-26 Melbourne (2026-11-25 UTC).

## Certificate calculus

Reviewed `../CERTIFICATE.md`, SHA-256
`7c40b59f17f9b1b616276e88c1782dfdb7749cce48afc72c843379138f84587b`.

No blocking mathematical error found. Independently checked:

- The fallback-normalized all-length envelope, with common scheduler
  constants, remains valid on taking a nonattained infimum.
- The coverage criterion includes the necessary slack when a prescribed
  infimum is not attained; eventual coverage at some larger fixed level is
  equivalent to eventual boundedness.
- For `b_j=(j+2)^2`, the exact maximizing feasible index gives
  `F(x)=x/floor(sqrt(x))` at every `x>=9`.
- Integer applicability thresholds ensure there are no new feasible
  indices inside consecutive attainable `x_n` intervals. Slopes at most
  `1/3` justify the stated extension with slack.
- Distinct positive enumeration indices tend to infinity even when their
  order is not monotone. The finite-low-level proof correctly concludes
  divergence of the *certificate*, with no actual-runtime inference.
- Under the explicitly additional full sum-diagonal convention, the
  index lower bound is `2+j(j-1)/2`. Its difference from `(j+2)^2/9` has
  positive numerator `7j^2-17j+28`; minimizing `y^2/9+x/y` gives exactly
  the displayed `x^(2/3)` coefficient.
- The integer rate choices meet their threshold conditions with slack.
- The computable delayed-threshold construction terminates under the
  assumed sublinearity of `R`, preserves increasing thresholds and witness
  points, and makes every integer witness attainable by the given `N`.

All conclusions retain their stated analytic/certificate scope.

## Literal p-adic label lift

Reviewed `../PADIC-LIFT-OBSTRUCTION.md`, SHA-256
`aabdffdb45db975747e4f8518ce19765e373eef9707fbf4e3b6eff165e678a12`,
against the source label and Gram definitions in tape `interchange.tex` at
`openai/math@3344da59991ed94f9ba711217b29c1d760badfa6`.

No blocking mathematical error found. Independent proof checks:

1. A monic irreducible lift gives a finite free local extension with
   residue field containing the required root of unity. The one-step
   Newton correction works modulo `p^2`, and `q` being a unit makes the
   character matrix invertible. Factorizations extend to this ring, so
   a lower bound there is a valid lower bound for the original ring.
2. The source's literal label operator is exactly `I+e_p(A_1,...,A_h)`.
   The highest inner character weight has eigenvalue `-binom(2p-1,p)`.
   The count-indicator expansion at weight `p-1` gives
   `1+lambda_(p-1)=q^p (mod p)`, with the sign checked using Wilson's
   identity. The harmonic-pair calculation gives
   `binom(2p-1,p)=1 (mod p^2)`.
3. One distinguished weight-`p-1` factor and the other weight-`h` factors
   produce a valuation-one eigenvalue. The exponent in its multiplicity
   is `p-1+h(h-1)=h^2-p`; the displayed multiplicity is correct.
4. The factor-rank proof genuinely works over the local ring: unit pivot
   elimination reduces `U` to an identity block and a `pC` block. After
   division by `p`, the product's residue rank is at most the factor
   width, whereas the selected diagonal block has full residue rank.
   Reduction modulo `p` alone would not prove this claim.
5. Restricting the rational Gram matrix to one varying inner word and
   changing to sum/difference coordinates gives the stated `J` and
   `J-(2/p)A` blocks. Their ranks prove the reserve lower bound.
6. The Bernoulli estimates, the reserve inequality and `q^h<2m^alpha`
   imply the exact fresh-query-factor bound and its uniform `m^(2/5)`
   weakening. These are restricted invoice/factorization facts.
7. The polynomial degree lemma follows from double roots modulo `p`;
   `(1-X^(p-1))^2` attains it for every odd prime. A scalar polynomial
   modulo `p^s` still cannot distinguish counts separated by `p` after
   final reduction modulo `p`.

### Reproduction actually performed

Ran:

```
python research/moonshot-overhead-program/results/epsilon-uniformity/verify_padic_lift.py
```

Script SHA-256:
`fb1b23c14f863a8ccfebe1067b21abb0e5380b9ed3e655e654a1dfac4d6a6825`.
Python 3.12.14; successful report timestamp
`2026-11-25T14:30:33.212996+00:00`.

The actual successful checks were 88 prime/alphabet cases, 25 reserve
boundary cases, complete binary inner spectra of orders 32, 512 and 8192,
direct order-32 elimination modulo 9 with unit/p/zero pivots `(16,15,1)`,
all 6,561 possible width-one factorizations of the order-two test, and
all 6,561 cubics modulo 9 for the degree test. The script also checks
the non-coprime-alphabet and modulo-`p` negative controls. Its implementation
was read; the direct elimination and transform checks are different
computations from merely substituting the symbolic formulas.

These finite checks do not materialize the enormous outer label matrix,
prove all prime cases by enumeration, verify a full multiplication machine,
or give a global runtime lower bound. The universal statements rest on the
written proofs reviewed above.
