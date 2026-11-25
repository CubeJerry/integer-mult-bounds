# Independent review of prime-characteristic count formulas

Route C, S002, 2026-11-25. Read the complete current
`../A/prime-characteristic-count-formulas.md`, PC1--PC10. This review
accepts the finite representation and its p-dependent construction bound.
The backup global comparison is kept separate from the strongest accepted
fixed-F4 theorem.

**Gate: PASS for PC1--PC8.** The original binary-source check-node
paragraph requires p odd; the current note states this explicitly. The
carry and general characteristic-p factorization lemmas themselves also
include p=2. No single dyadic formula uniform across odd primes follows.

## Carry truth table and degree

For digits x,y in {0,...,p-1}, let s=x+y. Vandermonde gives

    G_p(x,y)=binom(s,p) mod p=floor(s/p),
    H_p(x,y)=binom(s,p-1) mod p=1_(s=p-1).

Here 0<=s<=2p-2, so the otherwise possible second boundary s=2p-1
cannot occur. Equivalently

    H_p(x,y)=1-(x+y+1)^(p-1)

in F_p. Thus `G_p+H_p*c` gives the ordinary outgoing carry for both
incoming values c=0 and c=1: an existing carry from s>=p stays one,
and a new carry occurs precisely at s=p-1 when c=1. The result is
always 0 or 1, rather than an arbitrary field residue requiring a further
digit correction. The predecessor c occurs once in the expression.

Every factorial denominator in G_p and H_p has index below p and is a
unit. Assigning digit i degree at most p^i gives degree at most p^(i+1)
for both terms of the next carry, and degree at most p^i for the output
digit. This is a syntactic-degree bound; no quotient simplification or
cancellation is used to establish it.

## Copied size and signed coefficients

An explicit product for B_a(X) copies its input a times. After
substitution of two digit formulas of sizes at most S_i>=1, the stated
`8p^2 S_i` local bounds for G_p and H_p are safe. A carry step therefore
adds at most `16p^2 S_i+2` nodes to the previous carry. The sum digit
adds `2S_i+2` more nodes. Summation in i gives the conservative bound
`32p^2 sum_(i<=k) S_i` in PC4.

Repeated summation on the balanced binary input tree gives exactly the
claimed upper bound

    (32p^2)^r binom(r+k,k), r=ceil(log2 m).

One constant-offset addition uses the same bound with r increased by one.
For h<=D<=m and k below the required base-p residue length, k<=r.
Consequently its logarithmic size is
`O(log(m+2)(1+log p))`, with an absolute implied constant. The polynomial
factors for the Lucas products and the sum over h are absorbed uniformly
for `2<=p<=m`. The exponent dependence on log p is retained.

For negative offsets, `1+T` is a unit in F_p[[T]] and
`(1+T)^(p^t)=1+T^(p^t)`. Its coefficients below p^t therefore depend only
on the exponent modulo p^t even for negative integers. The Lucas product
uses B_(h_i) of each residue digit and has degree at most
`sum h_i p^i=h`. In the actual source constructor the offset is O(m), so
its generation and phase computation are also within the stated budget.

## Full-rate and actual generation scope

For a sum of degree budget d=p^v c, with p not dividing c, the existing
graded tensor construction can use a c-th root. Its mixed Gaussian
coefficients vanish, giving `(X+Y)^c=X^c+Y^c`. The two right-side powers
commute, so characteristic-p Frobenius gives the d-th power identity.
The total-grade blocks still have width d times the product of the two
child widths. Thus the all-rotation invariant and D-stage full-rate
conclusion persist.

For the original binary application p must be odd, both for its initial
indicator denominator two and for the power-of-two check-node inverse
product two. A common conductor coprime to p supplies all required roots
and those check nodes. Its explicit cyclotomic quotient is sufficient;
no field irreducibility search or enumeration of all scalar elements is
needed. Polynomial arithmetic in its coordinate dimension, all shifts,
spectral tables and repair matrices fit

    P_(m,p)<=2^(2^(C log(m+2)(1+log p))).

The numeric rational-address magnitudes `2^(m^c)` fit after increasing the
absolute C. Different primes use different factorial inverses and digit
formulas, so this does not establish the all-odd-characteristic identity
over Z[1/2] requested by the separate dyadic hypothesis.

## Independent exact checks and global status

`verify_prime_count_formula.py` uses the Fermat propagation polynomial,
independently of A's full binomial-sum implementation. It passed all
5,034 digit-pair/carry cases for primes through 31; 2,517 propagation
comparisons; 11,190 balanced-adder assignments including 329 negative
offset counts; 114 explicit copied-size and degree budgets; 1,535,617
signed Lucas identities; 1,530 binary predictor identities with 534
central-window matches; and 30 negative controls. Results are in
`prime-count-formula-verification.json`. The verifier checks the p=2
nonunit-two boundary separately. The mathematical scope restriction is
not inferred from a test.

The substitution p=Theta(J), log m=O(J^3 log J) gives the profile in
PC9 by direct arithmetic. This review does not promote PC10 as a new
global theorem; its complete source/physical composition remains a
separate backup gate and is unnecessary for the stronger already accepted
fixed-F4 envelope. No new strongest rate is claimed from this finite
generalization.
