# Sparse disjoint component supports cannot supply a narrow operator escape

**Author source-specific theorem; independent review pending. No new kappa.**

This excludes a broad concrete supplier-code construction class, including
the straightforward pairing of six native halfclass indicators. It allows
arbitrary coefficients over every characteristic-two field and does not
assume a tensor quotient, commuting blocks, or a literal packet history.

## 1. Proposition and exact source premise

Let K be the pinned111-port canonical binary fitting, C=row(K), and
Z_i={j:K_ij=0}. The canonical scalar code has dimension9, every forbidden
restriction has rank8 and kernel span(K_i), and all canonical foreign
degrees are between55 and62. A new exact native certificate proves

    minimum_distance(C restricted to Z_i)>=18          (1)

for every receiver i. The actual111-receiver distance census is
18:7,19:24,20:52,21:16,22:11,23:1. The checker enumerates the entire fixed
binary canonical code, so this is a finite source theorem rather than an
asymptotic extrapolation. The distance lower bound remains true after any
characteristic-two scalar extension: expand a nonzero extended codeword in
a basis of the finite F2-span of its coefficients; any nonzero binary
component has support contained in the extended word's support.

Fix any characteristic-two field k, V>=2, and 0<=q<=V+1. Choose q row-vector
words H_a=(h_{a,0},...,h_{a,V-1}), each with V scalar components in k^111. Assume
the qV component supports S_a,t are pairwise disjoint and each has size at
most8. Empty supports are permitted. Let A be any V-by-V block fitting with
identity diagonal, prescribed zeros on Z_i, and

    row(A) contained in C tensor k^V + span_k(H_1,...,H_q).   (2)

No independence of the H_a or of their canonical quotient classes is
required. The q in this proposition counts algebraic generators, not paid
physical packet identities.

**Theorem.** If V>=3, A retains every canonical foreign block and ell(A)=222.
If V=2, only receivers lying in the union of the component supports can
save a cardinality charge, each saves at most one, and therefore

    222-ell(A) <= |union_(a,t) S_a,t|.                  (3)

In particular, if V=2, q<=3 and every component support has size at most4,
then ell(A)>=198. Such codes cannot meet the retained target ell<=194.

## 2. Sparse residuals force all active generators to be literally local

For a fixed receiver let Q_i=k^{Z_i}/(C restricted to Z_i), and let
rho_a in Q_i^V be the componentwise forbidden residual of H_a. By(1),
rho_a=0 implies every h_a,t is literally zero on Z_i: each restricted
component has weight<=8<18 and belongs to the restricted canonical code.

Moreover no two nonzero rho_a,rho_b are proportional. If rho_a=lambda rho_b
with lambda nonzero, every h_a,t-lambda h_b,t restricted to Z_i belongs to
the restricted code and has support at most16. It must be zero by(1).
Disjointness of S_a,t and S_b,t then makes both restrictions zero separately,
contradicting that the residuals were nonzero. This proof applies to
arbitrary extension-field coefficients, not just binary indicators.

Consider a row i deleting a canonical foreign block. Write its V output
rows in the form canonical rows plus U_i H, with U_i a V-by-q matrix. It
has rank at least V: otherwise some nonzero output vector u has u U_i=0,
so u A_i is canonical. The single forbidden restriction makes it K_i v;
the diagonal gives v=u, and a deleted canonical block then gives u=0.
This is the source's canonical quotient injection argument.

The forbidden conditions put all V independent rows of U_i in the kernel
of the residual map k^q -> Q_i^V. If q<V this is already impossible.
Otherwise its rank is at most q-V<=1. Since the
nonzero residual columns are pairwise nonproportional, at most one can be
nonzero. Every selector row must have coefficient zero on that column.
Consequently every generator used by this deleting receiver is literally
supported on its closed canonical neighborhood. This statement concerns
the actual chosen sparse representatives, with no uncharged change of code.

## 3. The remaining diagonal correction cannot erase a whole block

After discarding the unused nonlocal generator, the canonical portion is
K_i M_i for some V-by-V matrix M_i. At any source coordinate j, disjointness
means at most one scalar component h_a,t(j) is nonzero. Its correction is

    h_a,t(j) u_a e_t^T,

where u_a is column a of U_i. In particular, the own identity block gives
M_i=I if i is outside every component support, and otherwise

    M_i=I-c u_a e_t^T,   c=h_a,t(i) nonzero.            (4)

For V>=3, M_i has rank at least V-1>=2. Every other source correction has
rank at most1, so it cannot cancel M_i on a canonical contact. This
contradicts the assumed deletion and proves the first conclusion.

For V=2, a receiver outside all component supports has M_i=I and likewise
cannot delete a canonical block. At a receiver in S_a,t, a deletion requires
rank M_i=1. Its t diagonal entry must vanish, so c(u_a)_t=1. A correction
at another source uses a single value-coordinate row e_s^T. The row space
of M_i can equal such a coordinate line only when c u_a=e_t; then

    M_i=e_(1-t) e_(1-t)^T.

Thus deletions can occur only in opposite-channel supports S_b,1-t with
b different from a. The paired opposite component of the own generator
has output column proportional to e_t and cannot cancel this matrix.
There are at most q-1<=2 other generators, so at most16 foreign contacts
can be deleted. The foreign support remains at least55-16=39>36. Every
saving is therefore a single unit, and(3) follows by counting eligible
receivers. With six supports of size at most4 their union has at most24
points, proving198.

## 4. Scope and essential hypotheses

The native36 halfclasses form disjoint groups of size at most4. Pairing any
six distinct indicators into three two-component quotient generators is
therefore excluded over every characteristic-two field, not merely by a
finite binary search. Arbitrary linear combinations of those indicators,
overlapping component supports, larger components, and more than V+1
generators are not excluded by this theorem.

The sparse threshold is meaningful. A minimum forbidden codeword of weight18
can be split into two disjoint nine-point words whose nonzero residuals
coincide. Thus increasing8 to9 invalidates the distinct-residual premise.
This is a premise counterexample, not a successful fitting.

Disjointness is also essential: the code generated by e_j tensor k^V has
overlapping one-point scalar components and can replace receiver j by
its point row, deleting every foreign block even when V>=3. Conversely,
the width-two exception is real: at the unique degree55 receiver choose
H_0=(e_i,0), H_1=(0,1_T), where T is any three foreign contacts. A legal
fitting row in their code has foreign support52 and saves one unit. These
are algebraic controls, not physical acquisition or decoder realizations.

The proof does not assert a new general quotient lower bound, supplier,
physical packet count or complete multiplication exponent. It identifies
overlap or stronger scalar mixing as necessary in this concrete sparse
construction family. Prepared for @CubeJerry with OpenAI assistance, with
credit to the native source, canonical rigidity and quotient-injection
predecessors.
