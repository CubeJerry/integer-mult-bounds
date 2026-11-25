# Characteristic-two truncation with a low-rank error

Status: **component proof accepted after independent Route C review and replay**. This supplies a finite-dimensional rank approximation, not an inexpensive correction algorithm or a multiplication overhead theorem. The lead and Route B independently investigated the truncation; Route C independently checked the rank-conjugacy argument. Their complementary contributions are identified below.

Let K be a field of characteristic two and R_m=K[x_1,...,x_m]/(x_1^2,...,x_m^2). It has the 2^m squarefree monomials as a basis. Write e_h for its elementary symmetric element of degree h, with e_0=1 and e_h=0 for h>m. Let M_a denote multiplication by a. The commuting involutions Q_i=M_(1+x_i) satisfy

    F=prod_i(1+x_i)=sum_(h=0)^m e_h.

For 1<=d<=m put P_(d-1)=sum_(h<d)e_h and E_d=F-P_(d-1). If d>m the predictor is exact.

## 1. A direct rank-error bound for every degree

**Theorem C2.1.** For every integer 1<=d<=m,

    rank_K M_(E_d) <= 2 sum_(k<=floor((m-d)/2)) binom(m,k)
                   <= 2^(m+1) exp(-d^2/(2m)).             (C2.1)

More generally the first inequality holds for multiplication by any element with no monomials of degree less than d.

Proof. Let t=floor((m-d)/2). Split the input into degrees at most t and degrees greater than t. The former subspace has dimension A=sum_(k<=t)binom(m,k), so its image has dimension at most A. Every monomial in the image of the latter has degree at least t+d+1. Its dimension is at most B=sum_(k>=t+d+1)binom(m,k)=sum_(k<=m-t-d-1)binom(m,k). The upper index is t when m-d is odd and t-1 when it is even; hence B<=A. Rank is at most A+B<=2A. This argument makes no assumption that the characteristic-two inclusion matrices have full rank.

For X~Bin(m,1/2), E exp(z(X-m/2))=cosh(z/2)^m<=exp(mz^2/8). Markov's inequality with z=-2d/m gives Pr[X<=m/2-d/2]<=exp(-d^2/(2m)). This proves the second bound. QED.

For fixed delta>0, taking d>=sqrt(2m ln(2/delta)) gives error rank at most delta*2^m. It has d=O(sqrt(m)) for constant delta. If that d exceeds m the exact polynomial F is used. This is a rank approximation; it is not pointwise spectral agreement.

This direct two-cut argument was independently supplied by Route B after the lead's finite rank experiments. It is simpler than the special conjugacy proof below when only an upper bound is needed.

## 2. Exact rank identity at binary degrees

**Theorem C2.2.** If d is a power of two and d<=m, then

    rank_K M_(E_d)=rank_K M_(e_d).                         (C2.2)

The elementary product identity is e_a e_b=binom(a+b,a)e_(a+b), by counting disjoint subsets. In characteristic two this coefficient is odd precisely when a and b have disjoint binary digits. This criterion follows by expanding (1+T)^n as the product of (1+T^(2^r)) over the nonzero binary digits of n. Consequently

    P_(d-1)=prod_(2^r<d)(1+e_(2^r)),
    F=prod_(2^r<=m)(1+e_(2^r)).

Every w in R_m with zero constant term has w^2=0. Thus 1+w is a unit, and all the displayed factors are units. For V_d=sum_(q>=1)e_(qd), the binary-digit product identities give E_d=P_(d-1)V_d. These two elements have the same multiplication rank.

Set y_i=x_i prod_(j<i)(1+x_j). The variables y_i square to zero. Recover x_1=y_1 and then x_i=y_i prod_(j<i)(1+x_j) recursively; each prefix product is its own inverse. Substitution x_i -> y_i is therefore an algebra automorphism phi.

For d=1, telescoping gives e_1(y)=F-1=E_1. For d=2a, count the coefficient of a fixed squarefree monomial x_S, |S|=h, in e_d(y). The d selected y indices occur in a pairs. Prefix multiplicities are odd only between the first and second endpoint of a pair. Thus the ordered set S must split into a successive blocks, each with at least two elements; endpoints are the selected indices. There are binom(h-a-1,a-1) such splits when h>=d.

For a a power of two, the binary-digit criterion makes that coefficient odd exactly when a divides h. Hence

    phi(e_d)=sum_(h>=d, a divides h)e_h=(1+e_a)V_d.

The last equality separates the even and odd multiples of a and uses binom(qd+a,a)=1 modulo two. Conjugating M_(e_d) by phi preserves rank; multiplication by the units 1+e_a and P_(d-1) preserves rank as well. This proves C2.2. QED.

As a check, M_(e_d) maps degree k to degree k+d, giving the additional bound sum_k min{binom(m,k),binom(m,k+d)}. The exact characteristic-two graded ranks can be smaller. No full-rank assumption is used in either theorem.

## 3. Meaning for address swaps

On a free orbit of m independent involutions, the group algebra K[(Z/2)^m] is isomorphic to R_m by x_i=Q_i-1. The same rank fraction holds on that orbit. Disjoint physical swaps also have orbits with fixed coordinates. If only a<=m swaps act nontrivially, restriction gives R_a. For a<d the error is zero; otherwise its rank fraction is at most 2 exp(-d^2/(2a)), no larger than the m-based estimate. Direct sums preserve the relative bound. Thus the abstract operator statement applies to arbitrary input data, including equal-field fixed points.

Characteristic two has no separate +1 and -1 eigenspaces. This result cannot be inserted into the original odd-characteristic Hermite spectral repair by relabelling its exceptional rows. Error rank measures address-space dimension here, while the earlier predictor controls exceptional batch rows at each frequency. Those interfaces differ.

## 4. Explicit but potentially expensive correction

The direct proof gives a decomposition, not only an existential factorization. Let pi_lo project onto monomials of degree <=t and pi_hi onto output degrees >=t+d+1. Since E raises degree by at least d,

    M_E = M_E pi_lo + pi_hi M_E (I-pi_lo).

The first term factors through the low-degree subspace; the second through the high-degree output subspace. Together their total intermediate dimension is at most A+B. In the monomial basis these coordinate projections are explicit. This does not make the maps inexpensive in physical address order, nor compute either restricted multiplication cheaply.

A complete continuation must provide full-rate realization of P_(d-1), extraction into these compressed coordinates, an inexpensive recursive correction target, all basis conversions and routing, and a uniform visited-cell bound. The triangular automorphism in C2.2 is an algebraic proof device, not a cheap converter. A rank fraction is not a runtime fraction. The odd-characteristic source root/Hermite and label assumptions are not imported for free.

## 5. Evidence, related work and attribution

The exact checker constructs multiplication matrices in the squarefree monomial basis, performs bitset Gaussian elimination over F_2, checks the triangular substitution and unit identities, and tests degree-cut bounds. Negative controls remove prefix factors and confuse predictor rank with error rank. Scope and results are recorded in `verification.json`. Finite controls supplement the proof; they do not implement a tape algorithm.

Subset-inclusion ranks are established subjects: relevant primary papers include Linial and Rothschild (1981), Wilson (1990), and Frankl (1990). The homogeneous maps here are inclusion matrices. No sharper external rank theorem is used for C2.1, and no priority is claimed for incidence-rank theory. Primary-source read scope is recorded in the programme bibliography.

Developed during S002 for Jerry Chen (@CubeJerry), with substantial AI assistance. The lead derived the exact binary-degree automorphism identity; Route B independently derived the truncation and direct degree-cut bound; Route C checked the automorphism coefficient and tail estimate independently. Efficient physical correction remains open.

## Independent gate

Route C accepted the proof and independently replayed the exact checker; see `../../routes/C/REVIEW-CHAR2-RANK-REPAIR.md`. Its wording correction restricts the square-zero assertion to elements with zero constant term. All uses in the proof already have that property; no algebraic or rank formula changes. Efficient physical correction remains open.
