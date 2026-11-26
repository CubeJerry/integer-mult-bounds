# Independent acceptance of the telescoping carry supplier

Disposition: **accepted finite formula and absolute polynomial-m grammar
consequence**. A read C's complete `TELESCOPING-PRIME-ARY-CARRY.md` and
independently derived the identity after C communicated the supplier.
This closes the specific PA-formula gate in A's companion note. The
elementary identity is not claimed as a new general fact about addition.

## Formal identity and reduction

For each prefix U_j, rational Vandermonde gives

    sum_(a=1)^(p-1) B_a(U_j) B_(p-a)(Y_j)
      = binom(U_j+Y_j,p)-binom(U_j,p)-binom(Y_j,p).

The sum over j telescopes to `binom(sum Y,p)-sum binom(Y_j,p)`.
Expanding the first term by multivariate Vandermonde leaves exactly the
terms with all component indices less than p; the omitted terms are the
p+1 single-component indices equal to p. Both resulting formulas have
only factorial denominators below p. The equality therefore holds in
the p-integral polynomial ring and reduces to F_p. The argument never
reduces the separate terms binom(U,p), whose denominators contain p.
This is a formal identity, stronger than agreement on digit values.

On p+1 ordinary digits the total is at most p^2-1. Lucas gives the
ordinary carry floor(total/p), an element of {0,...,p-1}. Thus the
incoming carry is correctly allowed to be a whole digit, not only a bit.

## Actual syntax and size

Every freshly copied prefix U_j and shifted affine factor U_j-r has
budget one. A summand has a factors from the first binomial and p-a
from the second, hence actual product length p. Flattening all j,a sums
gives addition budget p throughout the top. The only other additions
are affine, with budget one. No intermediate padded sum is multiplied
past its budget. Substituting digit-i inputs scales these two budgets
to p^i and p^(i+1), so the existing roots-free Frobenius compiler applies.

There are p(p-1) product terms, p factors in each, and at most p variable
occurrences in a copied prefix. Counting binary sums/products and
constant nodes directly gives the stated safe 8p^4 bound. Prefixes need
not be shared. Factorial coefficients and modular inverses below p are
generated in fixed polynomial bit time. This meets the actual formula
and generator requirement rather than only a polynomial circuit bound.

## Uniform p-ary recurrence

At a p-ary tree node, both total input copies and incoming-carry copies
are bounded by a fixed power of p. Unrolling the digit-carry chain gives
`S_(r,k)<=A_p sum_(i<=k) B_p^(k-i) S_(r-1,i)` with A_p,B_p<=p^C
for one absolute effective C. The hockey-stick induction gives

    S_(r,k)<=C0 A_p^r B_p^k binom(r+k,k).

Here r=ceil(log_p m), k<=r, and a fixed offset requires only one extra
level. For 3<=p<=m, the power factors are at most m^(5C), while the
binomial factor is at most 8m^2. Lucas products and the D+1 outer terms
add only absolute polynomial factors in m. The resulting syntax and
its actual generator are therefore m^K with K independent of p.
The p=3 shifted value 3 still has its required high initial digit.

Explicitly, t=ceil(log_p(D+1)) gives p^(t-1)<=D<=m, so every required
digit index k<t satisfies k<=ceil(log_p m). Add a fixed residue offset
as one further p-way node with two nonzero input numbers and p-2 zero
inputs; the same full-digit carry formula and size recurrence apply.
For p=3 the shifted value 3 starts with low digit zero and high digit
one when that high digit is needed. Both are constant-size spectral
indicator formulas, so no p-dependent initial syntax exponent is hidden.

The top length remains L, the least p-power at least D, with L<=pD.
The independent cyclic module can remain exponentially wide; polynomial
log width and a succinct grammar do not make its physical data free.
This result removes the earlier growing-p syntax exponent, while
leaving the factor-p call inflation and all odd-characteristic geometry,
address execution, packing, repair composition and common-space gates.
It supplies no stronger global multiplier theorem by itself.

## Isolated finite evidence

Read the complete checker, copied it and its count-compiler dependency
to `telescoping-carry-review-replay/`, and ran the copy. It compares actual
formal polynomial coefficients with an independent truncated generating
product, rather than treating finite-field value agreement as a proof.
It passed four formal polynomials with 6,469 nonzero coefficients, 223
digit values, 517 actual addition-budget checks and eight negative
controls. The full unfolding sizes were 17,101,639,2169 for p=2,3,5,7.
All root lengths were p and every addition budget was 1 or p.

Checker SHA-256:
`bf0513d59c75929c4ebafd24beca5d28f7f591379c95a4fb853493d467535057`.
The dependency is the already reviewed p-power compiler snapshot
`ff83527440f20499e75553633484edbdd348b201150504bf0f7dd982b78dff97`.
No remaining mathematical correction requested. The finite checks
supplement the unbounded formal, syntax and recurrence proof above.
