# An inverse-native degree-one gate excludes the two-query (3,2) caller

**Proved scoped obstruction, pending independent review. No new kappa.** For two independent retained roles, one exact native half and two rank-one one-bank queries cannot produce independent endpoint Gaussian ranks (3,2), in any placement of the queries. The argument permits arbitrary invertible ordinary role encodings and ordinary zero divisors. It works in every faithful phase sector. It does not establish a lower bound outside the stated finite rank-bimodule interface.

## 1. Algebraic theorem

Let an algebra of physical d-by-d field operators have direct rank components E_r and filtration F_s=sum_{r<=s} E_r. Assume:

1. E_0 is a unital ordinary algebra closed under the inverses used in the caller; every E_r is an E_0 bimodule.
2. Products satisfy F_a F_b subset F_{a+b}.
3. Every coefficient of an invertible two-role base L belongs to F_1.
4. A one-bank query has form I+e_i q e_j^T, with q in F_1 and the query invertible. In-place queries use i=j and q=g-I; distinct-bank shears use i unequal to j and q=cg. The inverses used also have this form with coefficients in F_1.
5. Every interstage and boundary role matrix is invertible over the ordinary algebra.

An independent endpoint of ranks (3,2) means

    M = U diag(G_3,G_2) V,

where U,V are invertible ordinary two-role matrices and G_r is an invertible physical operator in E_r. This explicitly permits full ordinary mixing at both boundaries. In particular

    pi_3(M)=U_3 G_3 V_3,
    pi_2(M)=U_2 G_2 V_2,

where U_j and V_j are the corresponding block column and row. Each of these two rank components has physical rank d, and their input row-spaces are independent because the stacked ordinary rows V_3,V_2 form an invertible matrix.

**Theorem.** Under these hypotheses, no word containing L once and at most two one-bank queries has this endpoint. Queries may both precede L, both follow L, or lie on opposite sides. The statement is algebraic; it does not regard proof projections as free physical operations.

## 2. Split placement: the untouched corner

Absorb the external ordinary matrices into U,V. Write

    M = Q_+ C L D Q_-,

with ordinary invertible C,D. Let i be the affected row of Q_+ and j the source column of Q_-. Expansion shows that every term missing at least one of the two query coefficients belongs to F_2. Hence pi_3(M) is supported only in block (i,j).

Its physical rank is d, so that sole d-by-d block is invertible. From pi_3(M)=U_3 G_3 V_3 it follows that U_3 has only row block i nonzero, and V_3 has only column block j nonzero. Both nonzero blocks are invertible: the image of U_3 is exactly the i-th role and the kernel of V_3 is exactly the other input role.

Let i' and j' be the other row and column. Invertibility of U,V now makes the complementary blocks (U_2)_{i'} and (V_2)_{j'} invertible; this is the elementary block-triangular inverse criterion after permuting the role labels. Therefore

    M_{i'j'}=(U_2)_{i'} G_2 (V_2)_{j'}

is an invertible operator in E_2. But row i' is unaffected by Q_+ and column j' is fixed by Q_-, so

    M_{i'j'}=(C L D)_{i'j'} in F_1.

The direct rank decomposition gives E_2 intersect F_1={0}, a contradiction. No individual ordinary entry was assumed invertible before its invertibility was forced by the independent endpoint.

## 3. Both queries after the base: the shared input row-space

Write

    W=Q_1 D L,             M=Q_2 C W,

after absorbing ordinary boundaries. If k is the first query's affected row, then

    pi_2(W)=e_k R

for a d-by-2d block row R in E_2: D L lies in F_1, so every degree-two term uses Q_1 and lies in its single affected row. W has no component above E_2.

Let i be the second query's affected row and write Q_2=I+e_i q e_j^T. Every degree-three component of M lies in row i. Since pi_3(M) has rank d, the independent endpoint forces U_3 to have only row i nonzero, with that block invertible. The other output row i' of M is consequently the pure rank-two row

    M_{i'}=(U_2)_{i'} G_2 V_2.

It has full row rank d, and the ordinary square factor (U_2)_{i'} is invertible by block triangularity of U. On the other hand, Q_2 leaves row i' unchanged, and its rank-two projection is

    M_{i'}=pi_2((C W)_{i'})=c R,
    c=(e_{i'}^T C e_k) in E_0.

Full row rank of cR forces the square matrix c to be invertible. Its inverse belongs to the ordinary algebra: for any finite-dimensional unital matrix algebra, the inverse of an invertible member lies in that algebra, by its characteristic polynomial. Thus

    R=c^{-1}(U_2)_{i'} G_2 V_2.                 (1)

Now the only degree-three contribution of the second query comes from pi_2(W):

    pi_3(M)=e_i pi_3(q c' R),
    c'=e_j^T C e_k in E_0.

Insert (1) and use ordinary right bimodularity to obtain

    pi_3(M)=e_i Z V_2,
    Z=pi_3(q c' c^{-1}(U_2)_{i'} G_2).

This has input row-space contained in that of V_2. Because pi_3(M) has rank d, its row-space equals the d-dimensional row-space of V_2. But the independent endpoint expression U_3 G_3 V_3 has row-space V_3, which is independent from V_2. This is impossible. The key independent-input condition cannot be replaced by two merely nonzero rank components of the same input job.

## 4. Both queries before the base

Transpose the entire word and use the transposed graded algebra E_r^T. It automatically satisfies the same filtration and bimodule hypotheses; a one-bank query transposes to another one-bank query. The endpoint remains an ordinary encoding of independent ranks (3,2), with the input/output roles exchanged. Section 3 applies. Alternatively the same proof can be written with column spaces and left bimodularity throughout.

## 5. Application to every source orientation

The exact common-head source has the two forms

    N_square = [[A, c A^2], [0,A]],
    N_ordinary = [[A,0],[c I,A]],

where c is a field-level sign and r(A)=1. The latter already has every coefficient in F_1. The former satisfies the exact identity

    N_square^{-1} = [[A^{-1},-c I],[0,A^{-1}]],

whose coefficients are in F_1. No numerical inversion or claimed free inverse source is involved: if a caller identity exists, inverting the whole identity is a valid proof operation. Query inverses remain one-bank rank-one queries, ordinary inverses remain ordinary, and an endpoint Gaussian transform and its inverse have the same Gaussian rank. Role swaps, transpose orientations and A replaced by A^{-1} preserve this argument.

The common seven-axis body factor acts on both retained roles and commutes with the head operations; it can be cancelled from the head identity as an invertible factor. This algebraic cancellation does not remove its paid physical cost. Changed body incidences and head/body mixing remain outside the scope.

For the before-base case in the abstract theorem, one may use the transposed graded algebra E_r^T rather than assume E_r itself transpose-stable. It automatically has the same directness, multiplication and ordinary bimodule properties with reversed products. In the actual Clifford application, transposition also preserves Gaussian rank, so it returns exactly the stated source model.

## 6. Complete two-query invoice consequence

In the F_1-base form, two rank-one queries give no rank component above three. A pair of rank-three independent endpoints is also impossible directly: in split placement pi_3 lies in a single block; with both queries after it lies in the last query's one affected row; with both before the transposed statement confines it to one column. Its physical rank is at most d, whereas two independent rank-three jobs require 2d.

Together with the (3,2) theorem, this leaves total endpoint head rank H at most four. If a rank-three job occurs, its independent partner has rank at most one. Otherwise both ranks are at most two. This statement is a necessary condition for the entire one-native/two-rank-one/two-role family.

Let [r]=r^t for 0<t<1, and let a=[8]-[7], so 0<a<1. Two endpoints with the same fresh seven-axis body satisfy

    T=[7+r_1]+[7+r_2] <= 2[7]+a H <= 2[7]+4a.

The full source-plus-query moment price is

    P=[1]+[7]+[8]+2[1]=3+2[7]+a.

Therefore

    P-T >= 3(1-a) > 0.

Any positive ordinary layout, tape, precision, ownership or recursive expense only worsens this already unfavorable idealized invoice. Thus this entire inventory cannot supply the target saving, including at t=199/200. This is a scoped architectural obstruction, not a global multiplication lower bound.

## 7. Dependencies, controls and next construction

The proof depends on: the exact source gauge and field-level signs in `THREE-HEAD-SOURCE-AND-ONE-QUERY-GATE.md`; tensor separation in each phase sector; the full ordinary Gaussian-rank bimodule decomposition; the rank product inequality; independent retained endpoint jobs; and one-bank query incidence. It does not depend on the 28-odd-form potential or a finite caller search. The square-block inverse and source gauge can be checked at arbitrary finite widths; the component and row-space arguments are the universal proof.

The accompanying diagnostic checks exact source inverses at widths one and two, verifies the corner and single-row coefficient identities in a noncommuting ordinary matrix polynomial model, and includes deliberately invalid independent-input and multi-bank-query controls. Such finite controls do not replace the theorem. Root's projector kernel construction is a separate negative control: ordinary zero-divisor compressions can exist, but they cannot satisfy all independent endpoint requirements above.

The next genuinely open optimistic inventories on three heads are one native with query ranks (2,1), or one native with three rank-one queries, targeting (3,3). Their prices are respectively 2[1]+[2]+[7]+[8] and 4[1]+[7]+[8], against target 2[10]. Both have linear head budget five versus target six. The two-query theorem above assumes both query ranks at most one and does not exclude either inventory. They require an actual all-column caller and full ordinary/compiler admission; favorable arithmetic is not a construction.

Credit @CubeJerry, predecessor source/compiler authors, the programme tensor-component work, S014 Worker B and OpenAI assistance. All five foundational assumptions remain retained. No new complete kappa.

### Same-session supersession, 2026-11-15 S014

The mixed query ranks (2,1) proposal in Section 7 was subsequently closed by `MIXED-QUERY-PURE-ENDPOINT-GATE.md`; its original mention records the order of discovery. The current smallest surviving proposal uses three rank-one queries. `THREE-QUERY-PLACEMENT-GATE.md` further requires all three to lie on one side of the F1 native orientation and specifies the necessary intermediate input representation. No previously stated theorem or proof above is changed by this update.
