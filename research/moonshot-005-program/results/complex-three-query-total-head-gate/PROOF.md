# Three rank-one queries give total endpoint head rank at most five

**Author proof for independent review. No new kappa.** The coset gate closing the three-head (3,3) inventory extends to a dimension-independent three-query bound. A fourth spectator head does not rescue the proposed (4,2) endpoint. This is a fixed finite-group, two-retained-role theorem; it is not a general multiplication lower bound.

## 1. Statement and dependencies

Use the exact phase-faithful Clifford group algebra, computational-monomial ordinary algebra O, rank spaces E_r and filtration F_s of the companion three-query coset proof. The source or proof-inverse source is L=[[a,I],[0,a]], rank(a)=1. There are exactly three one-bank rank-one queries, of either in-place or additive-shear type, in arbitrary placements. Interstage and boundary matrices are invertible over O. Every source/query/endpoint bulk group and exceptional-factor count is fixed independently of tensor width.

Suppose the endpoint is U diag(G_h,G_k) V, with U,V ordinary invertible and G_h,G_k independent invertible Gaussian jobs of ranks h>=k. Then

    h+k <= 5.                                             (1.1)

The upper product bound gives h<=4. A fourth-rank component is confined to one output row, input column, or corner according to placement; hence two independent rank-four endpoints are impossible. The companion coset theorem excludes (3,3). It remains to exclude (4,2) and (4,3). The next sections do so. The result also excludes their symmetric orientations.

No existing obstruction is reused without its hypotheses: the (3,3) step needs the exact native shape and coset support, while the new (4,2)/(4,3) arguments require the Gaussian endpoint factors and actual homogeneous rank-one query units. Fixed marked factors remain allowed under the companion proof's explicit bulk conditions.

## 2. A maximal-rank endpoint forces an outer in-place query

Suppose the preword W belongs to F_s entrywise and M=Q O W has an independent rank-(s+1) endpoint whose component is confined to Q's affected output row i. Its ordinary output column is e_i u with u invertible ordinary. Isolate that endpoint using the ordinary input column K from the inverse endpoint encoding. Thus M K=e_i u G_(s+1).

If Q is a shear I+e_i g e_j^T with i!=j, its inverse fixes e_i. Therefore O W K=e_i u G_(s+1), a nonzero rank-(s+1) column in F_s: contradiction. The query must be in-place. Transposition gives the analogous statement for an outer query at the input end.

This is a proof operation only. It does not make the inverse query physically free. No rank-projection inequality for arbitrary physical matrix rank is used.

## 3. All three queries after the source

Write W1=Q1 O1 L, W2=Q2 O2 W1, M=Q3 O3 W2. Then W1 is in F2, W2 is in F3, pi2(W1) occupies only Q1's affected row, and pi3(W2) occupies only Q2's affected row k.

Assume endpoint ranks (4,r), r=2 or3. The rank-four component is confined to Q3's affected row i. Section 2 forces Q3 in-place, say diag(g,I) after naming the roles. Let K4 isolate the independent rank-four endpoint and let its ordinary output block be u. Then

    W2 K4=O3^-1 e_i X,       X=g^-1 u G4.

The lower Gaussian rank triangle puts X in ranks at least three. Since W2 belongs to F3 and O3 is ordinary invertible, X is pure E3. It is physically invertible. Consequently

    pi3(W2) K4=O3^-1 e_i X.

The left side is supported only in row k. Invertibility of X forces O3^-1 e_i supported only in row k, with its remaining ordinary square block invertible. Two-role block triangularity therefore forces O3's other row i' to use only row k' of W2, with an invertible ordinary coefficient.

The partner endpoint row is pure E_r, has full physical row rank, and equals that invertible ordinary coefficient times the row k' unaffected by Q2. This unaffected row comes directly from an ordinary combination of W1 and belongs to F2. If r=3 it must vanish, contradiction.

For r=2 it is a full pure E2 row with the partner's ordinary input row V2. Write pi2(W1)=e_l R2. The partner row gives c R2=B G2 V2 for ordinary B,c. Full row rank forces c invertible, and the independently retained endpoint forces B invertible. Thus R2=c^-1 B G2 V2. Every E3 contribution to W2 comes from the second query acting on R2 through ordinary coefficients. Right ordinary bimodularity gives

    pi3(W2)=e_k Z V2.

Every E4 contribution to M then also factors on the right through V2. But the independent rank-four endpoint has ordinary input row V4, independent of V2 because V is invertible. Its rank d component cannot have row space contained in V2. Contradiction.

The case with all three queries before L is the transposed argument. These arguments explicitly obtain the needed physical full rank from the isolated Gaussian endpoint X; they do not assume projection pi3 preserves physical matrix rank.

## 4. Two queries after and one before: the rank-two Schur complement

After ordinary boundaries are absorbed, write

    M=Q3 O3 Q2 O2 L O1 Q1.

All rank-four terms use all three queries and the F1 source, so pi4(M) is supported in the corner (i,j) determined by Q3's affected row and Q1's source column. Its physical rank d forces the high endpoint's ordinary output column and input row to be confined to that corner, with both remaining blocks invertible. The complementary endpoint's blocks on row i' and column j' are then invertible ordinary by block triangularity.

Both outer queries must be in-place by Section 2 and its transpose. Name their units g,k and their positions row0,column0. Removing them leaves

    N=diag(g^-1,I) M diag(k^-1,I)=O3 Q2 O2 L O1.

Therefore N belongs to F2 and pi2(N) has physical rank at most d, since its only degree-two terms come from Q2's one affected row before invertible ordinary multiplication.

If the partner rank is three, the untouched complementary corner is invertible pure E3, contradicting N in F2. It remains to treat partner rank two.

Normalize this complementary corner to a single rank-two Gaussian H by ordinary scaling only row1 and column1. These scalings commute with the respective outer in-place queries and preserve all properties of N. The endpoint has the exact form

    M=[[G+P H Q, P H],
       [H Q,       H]],                                 (4.1)

where P,Q are arbitrary ordinary elements and G is invertible pure E4 (an ordinary left/right encoding of the high Gaussian job). No inverses of P or Q are used.

Set X=N01=g^-1 P H and Y=N10=H Q k^-1. Gaussian lower bounds put these products in ranks at least one; N in F2 excludes ranks above two. Because g and H are individual homogeneous group units, the group-coefficient support of P is partitioned uniquely by the rank of g^-1 p H. There exist ordinary P1,P2 with P=P1+P2 and

    pi1(X)=g^-1 P1 H,       pi2(X)=g^-1 P2 H.

Likewise Q=Q1+Q2 with pi2(Y)=H Q2 k^-1. The partition retains every actual scalar cocycle. This step uses Gaussian endpoint H and homogeneous queries; it would not follow for an arbitrary nonhomogeneous rank-two operator.

Now N11=H is invertible pure E2 and rank(pi2 N)<=d. The physical Schur complement of the rank-two component must vanish:

    pi2(N00)=pi2(X) H^-1 pi2(Y)
             =g^-1 P2 H Q2 k^-1.                       (4.2)

Indeed block elimination makes its rank d plus the rank of that Schur complement. H^-1 is a mathematical proof operation, not an ordinary or free physical primitive.

Let Z=N00-pi2(N00), so Z belongs to F1. Combining (4.1) and (4.2) gives

    G=g Z k-P H Q+P2 H Q2.

The first term lies in F3; the latter two are pure E2 by ordinary bimodularity. Thus G belongs to F3, contradicting its invertible pure-E4 status. This excludes (4,2).

One query after and two before is the transposed proof. The argument includes all middle query types and arbitrary ordinary zero divisors. It does not extrapolate from an unsuccessful finite search.

## 5. Conclusion and full movement implication

At most three rank-one queries give no endpoint rank above four. Cases with total h+k>=6 are precisely (3,3),(4,2),(4,3),(4,4) up to ordering. The companion coset theorem and Sections 2-4 exclude them, proving h+k<=5 for any fixed number of head coordinates.

Consequently adding a fourth or larger spectator head does not rescue a three-rank-one-query, one-native, two-retained-role common-body caller. Retain the source invoice 1+[b]+[b+1], where [r]=r^t. For any positive integer common body b, put a_b=(b+1)^t-b^t with 0<t<1. The complete source-plus-query moment is

    P=4+b^t+(b+1)^t=4+2 b^t+a_b.

Concavity and h+k<=5 give T<=[b+h]+[b+k]<=2b^t+5a_b. Since 0<a_b<1,

    P-T >=4(1-a_b)>0.

Thus every such three-query caller fails even the optimistic movement budget, for every t in (0,1), any fixed head count and any positive common body b. This does not exclude a larger query count or multiple natives. It is stronger than the three-head numerical screen and preserves every body/query expense.

## 6. Verification and open next question

The proof is a universal consequence of the faithful group algebra and physical block rank. Finite checks should separately probe the maximal-rank shear control, source high-component support, the group-coefficient partition, and the Schur-complement argument. They must not be reported as an exhaustive synthesis search. All source dependencies and the exact companion proof are pinned in DEPENDENCIES.json.

The substantive next question is whether the dimension-independent law extends to q rank-one queries as h+k<=q+2, or whether four or more queries can exploit an interface not forced into these pure-row/corner normal forms. The first optimistic pure-four-head inventory has four queries and target (4,4), price5[1]+[b]+[b+1] against2[b+4]; it is not excluded by the present three-query theorem. A changed native/role graph remains a separate constructive direction.

All five foundational assumptions remain. No new supplier, kappa, selected-certificate change, or upstream PR is asserted. Credit @CubeJerry, retained source/rank-component authors, S014 gates, S015 coset construction and independent review, and Worker B's new maximal-rank and Gaussian-Schur argument, with OpenAI assistance.
