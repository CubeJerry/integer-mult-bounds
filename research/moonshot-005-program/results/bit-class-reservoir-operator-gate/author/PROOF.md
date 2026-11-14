# Exact whole-block savings in the native class-code reservoir

**Author source-specific theorem; independent review pending. No new kappa.**

This concerns arbitrary operator-valued subspaces of the canonical
extension by the native fifteen-class indicator code. It does not require
the historical space to contain the whole class code. Its conclusion is an
exact algebraic support optimum, not a physical packet lower bound.

## 1. Spaces and exact native facts

Let K be the pinned111-port binary canonical fitting, C=row(K), and k any
characteristic-two field. Let u_c indicate the fifteen actual orthogonal
classes, whose sizes in the authenticated order are

    8,7,7,8,7,8,8,8,7,8,8,5,8,8,6.

Put U=span(u_c) and D=(C+U)/C. The source has dimensions

    dim C=9, dim U=15, dim(C+U)=19, dim D=10.

Every h_c=u_c+C is nonzero and the fifteen quotient lines are distinct.
For receiver i let c(i) be its class and Z_i={j:K_ij=0}. The decisive
additional exact native fact is

    ker[(C+U) -> k^{Z_i}]=span(K_i,u_c(i)).                (1)

Indeed every forbidden restriction has rank17, while the two displayed
independent words vanish there. These111 binary rank certificates prove(1)
over every characteristic-two extension. Thus every receiver has exactly
one locally available quotient direction despite the ten-dimensional
global reservoir. The checker reconstructs all facts from rational roots.

Fix V>=1 and an arbitrary E<=D tensor k^V. A permitted block fitting A has
identity diagonal, zero blocks on Z_i, and row space in the preimage of E
inside(C+U) tensor k^V. Write L_c=span(h_c) tensor k^V and d=dim E. Neither
E nor the coefficient operators are required to be tensor, commuting,
invertible, or simultaneously triangularizable.

## 2. Every saving uses one complete class line

Apply(1) entrywise. For arbitrary V-by-V matrices M_i,N_i,

    A_ij=K_ij M_i+(u_c(i))_j N_i,    M_i+N_i=I.

Every foreign own-class block is I. Every canonical contact outside that
class has block M_i. Therefore the foreign whole-block support is exactly

    |c(i)|-1 if M_i=0;       deg_K(i) if M_i!=0.          (2)

The native degrees range from55 to62 and the class sizes are at most8.
Consequently the arrival proxy

    ell_i=1[foreign support>36]+1[foreign support>52]

is zero in the first case and two in the second. A nonzero singular M_i
still leaves every whole outside-class block present.

The quotient-row image is v -> h_c(i) tensor(v N_i). If M_i=0, then N_i=I,
so the entire L_c(i) lies in E. Conversely L_c<=E permits u_c tensor I at
every receiver in that class. Hence the exact theorem is

    min_A sum_i ell_i(A)=222-2 sum_{c:L_c<=E}|c|.          (3)

Attain it by choosing class-indicator tensor rows precisely for those
classes whose whole line is in E and canonical rows elsewhere. Independent
choice of rows is legitimate in a fixed permitted linear space. It is not
a claim of simultaneous physical availability.

If d<2V, at most one of the distinct full class lines lies in E. Thus

    d<2V implies ell>=206,                               (4)

sharp for an eight-port class at d=V. If no full class line lies in E,
ell=222. This excludes the target ell<=194 throughout the sub-double-width
class reservoir, including entangled E with large scalar envelopes.

## 3. Exact rank-budget optimum

For a class subset S define r(S)=dim span{h_c:c in S}, and
M_r=max_{S:r(S)<=r} sum_{c in S}|c|. Exact enumeration of all32768 subsets
gives the following source certificate; binary subset ranks persist over
every characteristic-two extension.

| Scalar rank cap r | M_r | Least ell with dim E<=rV |
|---:|---:|---:|
|0|0|222|
|1|8|206|
|2|16|190|
|3|24|174|
|4|32|158|
|5|40|142|
|6|54|114|
|7|63|96|
|8|71|80|
|9|85|52|
|10|111|0|

For arbitrary d use r=min(10,floor(d/V)). If S is the set of full class
lines in E, their sum has dimension r(S)V<=d. This proves the lower bound
using(3). Conversely tensor the scalar span of a maximizing S. Any further
class line in that span is already included in a maximizing subset, since
all class weights are positive. This attains the table's bound.

Two full eight-port classes already attain ell190 at canonical quotient2V.
This is a strict-boundary control, not a source: their eight-root sums span
the Hub, and acquisition, retention, decoding and restoration need a legal
word. The two-class support also remains subject to the point-retained
handoff obstruction if used under that theorem's hypotheses.

## 4. Verification, predecessor scope and limitations

The checker authenticates native bytes, rebuilds the partition and codes,
checks all111 rank17 restrictions and all32768 subset ranks, and records
maximizing class subsets. Tensor witnesses at widths1,2,3,5 check actual
support and canonical quotient. At width2 it exhausts all16 possible
coefficient matrices in each receiver row for an entangled line-free space
and for one complete class line plus a partial second line. Nonzero
singular operators, the exact2V boundary, and a false one-line16-receiver
capacity are meaningful controls. Finite source ranks plus the argument
above give the all-field/all-width theorem; a matrix search alone does not.

The predecessor q>=12 gate for arbitrary one-row class extensions required
a physical history containing U tensor k^V. These E need not contain U;
they are extensions of canonical C. Neither theorem substitutes for the
other. Neither supplies a supplier, chart chronology, public/owned cost,
precision/erasure service, or foundational assumption. No new kappa.

Prepared for @CubeJerry with OpenAI assistance. Credit the native code,
fifteen-class target and independent review, prior class-history gates,
and the companion operator quotient/scalarization results.
