# A prime-ary carry formula gives uniform count grammar

Status: **proved finite-grammar improvement; independently checked and
replayed** in `review-telescoping-prime-ary-carry.md`. C supplied the telescoping Vandermonde formula after A posed
the precise syntax gate below. A independently checked its formal
identity, actual factor lengths and fully unfolded size. This
does not improve the admitted multiplier. It follows the accepted
prime-power count compiler and odd-characteristic order-four closure,
whose remaining formula size is `m^{O(1+log p)}`. The proposed change is
a p-ary addition tree, not a different distance constant in the retained
geometry. The formerly open formula gate is solved in section 2.

## 1. The exact many-input carry polynomial

For prime p and 0<=a<p put B_a(X)=binom(X,a) over F_p. Define

    K_p(X_1,...,X_p,C)
      = sum_[0<=a_i<p, sum_(i=1)^(p+1) a_i=p]
          B_(a_1)(X_1)...B_(a_p)(X_p) B_(a_(p+1))(C).
                                                               (PA1)

This is a formal polynomial of total degree at most p. For ordinary
digit values x_1,...,x_p,c in {0,...,p-1}, let S=sum x_j+c. Then
S<=p^2-1. Vandermonde and the vanishing of binom(x,p) for each digit
give

    K_p(x_1,...,x_p,c)=binom(S,p) mod p=floor(S/p).       (PA2)

The last value is an ordinary digit in {0,...,p-1}. Thus the output digit
is sum x_j+c in F_p and the next carry is K_p. The incoming carry need
not be Boolean in a p-way addition.

## 2. The formula gate and its explicit supplier

**PA-formula.** There is one absolute C such that, for every prime p,
PA1 has an explicitly generated arithmetic formula over F_p of size at
most p^C. Give every variable budget one. Every sum gate has an actual
p-power factor-family budget, every product concatenates child lengths,
and the root has length at most p. Constants have the same positive-length
cyclic-family convention as the accepted compiler. Formula generation
and its coefficient computation take p^C bit operations after an absolute
enlargement of C.

The actual length requirement is stronger than formal total degree p.
With maximum length p, a nonconstant sum may be padded only to 1 or p.
Padding an internal degree between 2 and p-1 to p and subsequently
multiplying by another nonconstant expression exceeds the allowed root
length. The supplier must exhibit its syntax, not infer these budgets
from cancellations in an expanded polynomial.

The literal PA1 sum has `binom(2p,p)-(p+1)` terms: weak compositions of p
into p+1 parts, excluding the p+1 forbidden terms with one part p. This
is exponential in p. Truncated polynomial multiplication computes PA1
values or a shared arithmetic circuit in polynomial p work, but unfolding
that circuit into a formula is a separate cost. Evaluation/interpolation
of the full digit generating product may use total syntactic degree
p(p-1), which fails the length-p gate. The following exact formula avoids
both problems.

**Theorem PA-S (C's telescoping supplier).** PA-formula holds. Put
`Y=(X_1,...,X_p,C)`, `U_j=Y_1+...+Y_(j-1)`, and use the previously
verified pair carry polynomial

    G_p(U,V)=sum_(a=1)^(p-1) B_a(U) B_(p-a)(V).

Then the formal identity is

    K_p(Y_1,...,Y_(p+1))
       =sum_(j=2)^(p+1) G_p(U_j,Y_j).                 (PA2a)

**Proof.** Work temporarily over Q. Vandermonde gives

    G_p(U,V)=binom(U+V,p)-binom(U,p)-binom(V,p).

Telescoping over j leaves `binom(sum Y_j,p)-sum_j binom(Y_j,p)`.
The multivariate Vandermonde expansion of this expression is exactly
PA1: the omitted terms are precisely those with one index p. Both PA1
and the right side of PA2a have denominators that are products of
factorials strictly below p. Their coefficients are therefore integral
at p, so the rational polynomial identity reduces legitimately to F_p.
No division by p occurs in the supplied formula.

Expand every occurrence of each prefix U_j freshly. There are at most
p^2 outer (j,a) terms; each has p affine factors, and each factor contains
at most p input variables and a constant. The full formula has O(p^4)
nodes. Modular factorial coefficients and all nodes are generated in a
fixed polynomial number of bit operations in p. No circuit sharing is
used for this size statement.

Each prefix and each shifted prefix U_j-r is affine with budget one.
Each product B_a(U_j)B_(p-a)(Y_j) has actual concatenated length p.
Flatten all (j,a) terms into binary sums of budget p. Thus every sum
budget is 1 or p and the root length is p. After substituting digit-i
inputs of budget p^i, the corresponding budgets become p^i and p^(i+1),
still actual prime powers. This proves PA-formula with one absolute
effective exponent. QED.

## 3. Absolute polynomial grammar

**Theorem PA.** For 3<=p<=m, the order-four count
predictor with degree D<=m has a prime-power-only formula of size m^K
for an absolute K independent of p. Its top length is still the least
p-power L>=D, with L<=pD. This statement concerns syntax and its finite
cyclic factorization, not physical endpoint or repair costs.

Pad m inputs to p^r, where r=ceil(log_p m), and add p children at each
node. Padding adds at most a factor p<=m. Initial ordinary digits,
including the nonzero high digit for shifted value 3 at p=3, have
constant-size affine query descriptions. At digit k substitute budgets
p^k into PA-formula. Its next carry then has budget p^(k+1), and the
low-digit affine sum has budget p^k. Truncating beyond the last needed
digit avoids a superfluous final carry.

Let S_(r,k) bound the full unfolding of an output digit. The number of
copies of an incoming carry is at most p^C, as is the total number of
input-digit copies. For absolute constants, one may take A_p,B_p<=p^C1
so that

    S_(r,k) <= A_p sum_(i=0)^k B_p^(k-i) S_(r-1,i),
    S_(r,k) <= C0 A_p^r B_p^k binom(r+k,k).             (PA3)

The second inequality follows by the same hockey-stick induction as the
binary-tree compiler; B_p^i cancels B_p^(k-i) in the substitution.
The largest required k is at most r, and a fixed offset costs one extra
level. Since p<=m,

    A_p^(r+1) B_p^k <= p^[C1(2log_p m+3)] <= m^(5C1),
    binom(r+k+1,k) <= 2^(r+k+1) <= 8m^2.

Lucas products, the D+1 Newton terms, and their p-power top padding add
only absolute polynomial-m syntax. This proves the stated m^K bound.
The original `m^{O(log p)}` loss came from a polynomial-p local adder
repeated at binary depth; PA-formula permits the matching p-ary depth.

The independent cyclic module may still have width L^(m^K), so its log
width and succinct grade grammar are polynomial m. Its actual complete
payload packing, shared query executor and visited-space coefficient
remain separate obligations. The factor-p inflation in L is not removed.

## 4. Remaining physical steps

PA-S closes the precise formula gate with the required actual lengths.
The accepted roots-free cyclic factorization consequently has a succinct
grammar of absolute polynomial-m size even as p varies in [3,m]. Its
independent row width remains potentially exponential. The top length
still has its factor-p inflation L<=pD. A fully priced odd-characteristic
endpoint compiler, scalar executor, batching, field encoding and common
visited-space bound must be composed before any global rate is claimed.
This backup compiler improvement does not beat the current
fixed-characteristic AQ envelope by itself.

Credits: the elementary Vandermonde/Lucas identity, the accepted S003
p-power compiler, and C's order-four closure. A posed PA-formula and
proved the p-ary recurrence consequence; C supplied the telescoping
formula, then A independently verified its formal reduction, syntax
and recurrence. Prepared for Jerry Chen with substantial ChatGPT
assistance. No priority claim for many-input addition or complete
odd-characteristic machine is asserted.
