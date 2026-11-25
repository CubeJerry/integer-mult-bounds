# Independent review of the general formula-size transfer

Status: **review passed**, 2026-11-25. Reviewed file:
[`../FORMULA-SIZE-TRANSFER.md`](../FORMULA-SIZE-TRANSFER.md).
This reviews its conditional implications; it does not assert an
unprovided smaller formula family.

The finite contract correctly counts formula duplication and requires
syntactic degree at most the source window degree. Formula generation,
coefficient numerator bits and dyadic denominator exponents are bounded
by fixed polynomials in `m+F_m`; mere arithmetic formula size is not
substituted for these obligations.

For Lemma G1, the cyclic rank satisfies `log K<=F_m log max(2,D_m)`.
The final cyclic assembly and regular representation cost at most a
factor polynomial in `D_m!` and the formula data. Scalar coefficient
bits before descent are polynomial in `m+F_m`, so even a high fixed
polynomial here is absorbed by the displayed exponential budget. The
generator's dense output, all shifts, repair and basis expansions cost
fixed powers of that budget. Refined rational geometry contributes
`2^(m^C)` values and work. Its prime/radix search is therefore of the
same sufficient form.

One wording clarification was requested: constant-only dyadic subtree
evaluation bounds numerator bits using both the leaf numerator bit
lengths and the **values of the denominator exponents**, plus the
addition count. For example `1+2^(-N)` has an `N+1`-bit numerator.
The contract explicitly bounds denominator exponents, so this changes
neither G1 nor any later estimate.

Writing `Q=m^C+f(m)log(m+2)`, the compiler gives logarithms of core
constants and double logarithms of thresholds of order `Q`. Sum-diagonal
enumeration contributes `O((j+Q)^2)`, with `j` absorbed by the source
arity term. Thus the distinct bounds `d_j<=CQ^2` and `b_j<=CQ` in G2
are justified, including the actual generator and common-space wrapper.

For the stated formula envelope, substituting `log m_j=O(Z_j)` gives
`d_j,b_j<=2^(C Z_j^a log^b(Z_j+2))`. The assumptions `a>=1,b>=0`
absorb the independent address term. Since
`Z_j^a log^b(Z_j+2)=O(j^(3a)log^(a+b)(j+3))`, the proposed integer
choice of `j` makes the exponent at most `z/2` eventually. Both
certificate coordinates are then at most `2sqrt(x)`, eligibility
holds, and the remaining `x/(j+2)` gives G5. Integer rounding and the
initial range do not change the asymptotic envelope.

The three table entries `(a,b)=(2,0),(1,1),(1,0)` follow by direct
substitution. The latter two are correctly conditional. The endpoint
qualification concerns these sufficient upper transfers and does not
claim a lower bound for multiplication, arbitrary formula families or
arbitrary matrix roots.

This is written mathematical review with GPT-6 Astra Pro assistance,
not formal verification or external peer review.
