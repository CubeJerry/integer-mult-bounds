# Prime-characteristic count formulas with controlled syntactic degree

Status: **PC1--PC8 accepted by independent Route C review** at
`../C/REVIEW-A-PRIME-COUNT-FORMULA.md`. The backup whole-input prediction
PC10 is not promoted to an independently audited global theorem here.
This is a backup representation for the original odd-characteristic source
and a generalization of the accepted characteristic-two carry mechanism.
It is not needed for the stronger fixed-F4 envelope.

Let p be a prime. All scalar arithmetic below is in F_p. For 0<=a<p,
write B_a(X)=X(X-1)...(X-a+1)/a!, with B_0=1. These are well-defined
polynomials, since a! is a unit modulo p. Define

    G_p(X,Y)=sum_(a=1)^(p-1) B_a(X) B_(p-a)(Y),
    H_p(X,Y)=sum_(a=0)^(p-1) B_a(X) B_(p-1-a)(Y).        (PC1)

Their syntactic degrees are at most p and p-1, respectively. Each has
an explicit formula of O(p^2) nodes and leaf occurrences, with no division
by p. All inverses are known scalar constants of the fixed field.

## 1. A factored base-p carry formula

For ordinary digits x,y in {0,...,p-1}, Vandermonde gives

    G_p(x,y)=binom(x+y,p) modp=floor((x+y)/p),
    H_p(x,y)=binom(x+y,p-1) modp=1_(x+y=p-1).            (PC2)

The binomial equalities follow by collecting coefficients in
(1+T)^x(1+T)^y. Since 0<=x+y<=2p-2, the displayed residues follow from
(1+T)^p=1+T^p. Thus if c is a carry bit in {0,1},

    c_next=G_p(x,y)+H_p(x,y)c,
    z=x+y+c in F_p                                    (PC3)

are exactly the ordinary outgoing carry and the sum digit. The expression
uses its predecessor carry once. For p=2 it becomes xy+(x+y)c.
On these digit inputs the session lead independently noted the simpler
propagation formula H_p(X,Y)=1-(X+Y+1)^{p-1}. It has the same degree
bound and avoids the displayed Vandermonde sum; either explicit formula
suffices for the conservative node count below.

Assign digit i the query-degree budget p^i. If x_i,y_i have degree at
most p^i and c_i at most p^i, then G_p(x_i,y_i) has degree at most
p^{i+1}, and H_p(x_i,y_i)c_i at most
(p-1)p^i+p^i=p^{i+1}. Therefore the output digit at position i has
degree at most p^i, without using cancellations or digit relations.

An explicit product formula for B_a copies its input a times. Counting
all copies in (PC1), binary arithmetic nodes and constants gives, for
input formulas of sizes at most S_i>=1,

    |z_k| <= A_p sum_(i=0)^k S_i,   A_p=32p^2.          (PC4)

For example each of G_p and H_p has fewer than 8p^2 S_i nodes after
substitution. Each carry step contains only one copy of the previous
carry, so summing the local costs proves (PC4).

## 2. Balanced count, fixed offset and Lucas products

Let m input digits have affine indicator representations of their own
base-p digits. For the original binary source these are simply the
Boolean indicator in position zero and zeros in every higher position.
Pad to 2^r inputs, r=ceil(log2 m), and use (PC3) on a balanced tree.
The actual unfolded formula size for count digit k obeys

    S_(0,k)=1,
    S_(r,k)<=A_p sum_(i=0)^k S_(r-1,i),
    S_(r,k)<=A_p^r binom(r+k,k).                        (PC5)

This follows by the same hockey-stick identity as in the binary proof.
Its syntactic degree is at most p^k. Adding a fixed residue -u modulo
p^t requires only one further level of the bound. If D<=m and
t=ceil(log_p(D+1)), then k<t<=r+1. Consequently these digit formulas
have size

    2^{O((log(m+2))(1+log p))}
       =m^{O(1+log p)}                                (PC6)

with absolute implied constants. The formula generator is an explicit
recursive traversal with all copies written, so it has the same type of
time/space bound.

For every integer a, including negative a, the coefficient binom(a,h)
modulo p for h<p^t depends only on a modulo p^t. This follows from
(1+T)^{p^t}=1+T^{p^t} in F_p[[T]], where 1+T is a unit. If a has
residue digits a_i and h has digits h_i, coefficient comparison gives

    binom(a,h) modp = product_i B_(h_i)(a_i).            (PC7)

Substitute the count-offset digit formulas into (PC7). The resulting
formula has syntactic degree at most sum_i h_i p^i=h. The outer truncated
source count predictor, a sum over h<=D with its correct scalar phase,
therefore has degree at most D and size m^{O(1+log p)}, for 2<=p<=m.
The polynomial-size factors from D, t and the binomial formulas fit this
bound. Every coefficient is explicitly computable in F_p.

This is not a polynomial in the ordinary count reduced modulo p. Higher
count digits retain the individual input indicators through the balanced
carry formulas. Thus it is consistent with the count-residue obstruction.
The identity with the original predictor is required only at the allowed
spectral tuples; the factorization below is a formal identity for the
constructed formula on its affine query expressions.

## 3. Full-rate factorization in characteristic p

The cyclic formula lemma extends from characteristic two to p. At a sum
gate of degree budget d, write d=p^v c with p not dividing c. Use a
primitive-c cyclotomic root to obtain
(X+Y)^c=X^c+Y^c with commuting X^c,Y^c. Frobenius then gives

    (X+Y)^d=X^d+Y^d.

The same total-grade restriction has width d*r*s, and the same cyclic
product and constant conventions apply. Thus a degree-D formula of size
S has D affine factors on at most D^S independent rows.

For the original binary source with p odd, choose a common coefficient algebra over
F_p containing roots of every prime-to-p part of the gate lengths and
power-of-two check nodes beyond the pre-descent batch. Its conductor is
coprime to p, and the power-of-two node differences are units because
their explicit product is two. The actual cyclotomic construction, all
binary shifts, all spectral checks and repair tables are bounded by

    P_(m,p) <= 2^{2^{C(log(m+2))(1+log p)}}.             (PC8)

This envelope also absorbs numeric rational-address data of size
2^{m^c}, after an absolute enlargement of C. No irreducible-polynomial
search is needed: the cyclotomic quotient is finite free, and its
coordinate arithmetic and check-node inverses are explicit. Small m can
use the total generic source constructor.

For each fixed p, (PC8) is singly exponential in a fixed polynomial of m.
When p grows with the inverse slack J, the exponent dependence on log p
is retained. No uniform constant independent of p is silently assigned
to the polynomial formula size.

## 4. Backup quantitative consequence and scope

The original odd-prime source label choice p=Theta(J), with
log m=O(J^3 log J), places the logarithmic finite envelope in

    log2 P_(m_j,p_j) <= 2^{O(J^3(log J)^2)}.             (PC9)

Using the separate rational Walsh component and the accepted physical
compiler, the existing common-cap/sparse inversion would then give the
backup displayed envelope

    log2 H(n) = O(s [(log log s)^2/log s]^{1/3}).        (PC10)

Its representation and global composition still require independent
review. It retains the original odd-characteristic label geometry and
binary repair, but is weaker than the new fixed-F4 scale by a factor
(log log s)^{1/3}. It is therefore a robustness alternative, not a new
strongest bound.

The all-odd-characteristic dyadic IP hypothesis remains open. Different p
use different scalar coefficients and digit formulas, and factorials below
p are inverted in F_p. The construction does not provide one identity over
Z[1/2] specializing uniformly to all odd primes.

Credits: elementary base-p addition and Lucas/Vandermonde identities;
the source predictor and label constructions; the cyclic factorization
literature; @CubeJerry; AI-assisted finite-formula derivation.

## 5. Finite exact verification

`verify_prime_carry_formula.py` passed 754 digit/carry cases over
p=2,3,5,7,11,13; 78,390 generalized-binomial cases including negative
arguments; 660 actual copied size/degree recurrences; and 22,800
odd-prime predictor cases. It includes 12 negative controls rejecting
ordinary-count-mod-p aliasing and omission of the propagation term.
The equivalent closed propagation polynomial was also checked. All
arithmetic is exact; the result is `prime-carry-verification.json`.
These tests do not establish a full physical composition or an unbounded
theorem independently of the proof, and no multiplier was executed.
