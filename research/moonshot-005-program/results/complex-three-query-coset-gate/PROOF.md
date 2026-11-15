# Coset separation closes the same-side three-query caller

**Author proof for independent review. No new kappa.** One native, two retained roles, and three rank-one one-bank queries cannot produce two independent rank-three endpoints in the fixed faithful Clifford/ordinary model. The argument adds group-coset support to the admitted rank-bimodule framework. Arbitrary invertible ordinary role matrices and ordinary zero divisors are allowed.

## 1. Algebra and proposition

Fix a finite projective Clifford group G, its exact scalar cocycle in an actual tensor-width residue, and a computational-monomial subgroup H. Let A be the twisted complex group algebra and O=C[H] its ordinary subalgebra. Its faithful physical realization has field dimension d. The finite group and exceptional-coordinate count are fixed independently of width. The inherited tensor-independence theorem covers all sufficiently large widths in every actual phase residue.

Let E_r span the projective basis classes of Gaussian rank r and F_s=sum_{r<=s}E_r. Ordinary multiplication preserves E_r. Gaussian products obey both rank triangle inequalities; in particular E_3 a^-1 lies in E_{>=2} for rank-one a. Actual scalar cocycles remain present.

The base is L=[[a,I],[0,a]], with rank(a)=1, and D=diag(a,a). Every exact native orientation, or its inverse as a proof operation, has this form after ordinary role exchange and nonzero scalar normalization. A query is an in-place diag(g,I) or a shear I+e_i c g e_j^T, i!=j, c!=0, with rank(g)=1. Interstage and boundary encodings are arbitrary invertible matrices over O. No mathematical inverse is a free physical primitive.

**Theorem.** A word with L once and three rank-one queries all after L cannot be invertible and pure E_3. By transpose and the admitted mixed-placement theorem, no placement of three rank-one queries gives two independent rank-three Gaussian endpoints.

Any fixed head count is allowed in this algebraic statement. The invoice corollary uses exactly three heads and the common seven-axis body. More natives, extra retained roles, changed body incidences, or width-growing/noncollective ordinary algebras are outside scope.

## 2. Coset support facts

For a,g outside H, gHa is disjoint from both gH and Ha. Equality gh a=gh' would put a in H; equality gh a=h'a would put g in H. Also H is disjoint from Ha^-1H, hence gH is disjoint from gHa^-1H.

These are support statements, not assertions that the ordinary algebra has no zero divisors. Distinct projective classes are independent at faithful width. Nonzero scalar cocycles preserve support. The cosets gH and Ha may intersect; their coefficients may cancel each other. Every element supported on either coset is pure rank one when a,g have rank one.

## 3. The forced intermediate

Suppose M is an invertible pure-E3 endpoint and write W1=Q1 O1 L, W2=Q2 O2 W1, M=Q3 O3 W2. Remove the last query: W2 has no component below two. Forward multiplication gives W2 in F3, with its E3 part confined to Q2's affected row. The other row R is therefore pure E2 and has full physical row rank d.

The E2 part B of W2 has rank exactly d and an ordinary one-role image. The unaffected row of Q3 makes O3 B supported in one row, so rank(B)<=d; R forces equality. Write B=O3^-1 e_i U. Its top block is bU=R with b ordinary, so b is invertible and its inverse ordinary. The lower row of B is consequently C R for ordinary C. Subtracting it makes W2's other row a pure E3 row T.

All E2 contributions in W1 lie in Q1's affected row. Its ordinary multiplier in R must therefore be invertible. Normalize that multiplier to I. Then R and Q1's untouched row S are an ordinary invertible row basis of W1. The second-query stage, followed by the subtraction above, has form

    T=(g lambda-C)R+g mu S             [in-place],
    T=(lambda+g nu-C)R+mu S            [shear],

where lambda,C,nu are ordinary and mu is ordinary invertible. Indeed its ordinary basis matrix has first row (u,0) with u invertible; block triangularity forces mu invertible. Ordinary rescalings of R,S preserve these forms. No other ordinary coefficient is assumed invertible.

## 4. Pure rows after the first query

In both query cases the normalized R has form (q w+h)L, where q is the rank-one first query unit, w=(w1,w2) an ordinary row, and h=(h1,h2) ordinary. Expanding gives

    R=(q w1 a+h1 a, q w1+h1+q w2 a+h2 a).

In the first block, q w1 a has support qHa disjoint from Ha. Purity forces h1=0. In the second block, q w1 and h2 a have supports qH and Ha, both disjoint from qHa. Purity forces

    q w1=-h2 a,        q w2 a in E2.

Thus the entire row equals R=q w D. This exact common-right-factor identity is stronger than its rank projection. It does not identify R with an ordinary independent input: D is nonordinary. The admitted S014 nonordinary-row seed remains consistent with it.

## 5. First query in-place

The first-query rows are q w L and z L, with O=(w;z) ordinary invertible, and S=zL. Write T=A R+B S, where B is g mu or mu as in Section 3. Multiplication on the right by D^-1 O^-1 gives

    R D^-1 O^-1=(q,0),
    S D^-1 O^-1=(0,I)+(0,z1 a^-1)O^-1.

The second block of T D^-1 O^-1 is

    B+B z1 a^-1 (O^-1)22.                           (5.1)

Since T is pure E3, the whole expression has no component below two. If Q2 is in-place, B=g mu is nonzero, invertible and supported in gH, hence pure E1. The second summand is supported in gHa^-1H, disjoint from gH, so it cannot cancel B. If Q2 is a shear, B=mu is nonzero ordinary while the second summand is supported in Ha^-1H, disjoint from H. Again cancellation is impossible. This closes both second-query types without inverting any individual block of O.

## 6. First query a shear

The first-query rows are zL+q wL and wL, with S=wL. Normalize R=(q w+h)L where h=z+v w for ordinary v. Thus (h;w) is invertible ordinary. Section 4 gives h1=0 and q w1=-h2 a. Invertibility of [[0,h2],[w1,w2]] forces h2,w1 invertible; their inverses are ordinary. Rescale R by -h2^-1 and S by w1^-1. With p=w1^-1w2, arbitrary ordinary and possibly singular, the rows become

    R=(a²,a p a),       S=(a,I+p a).                 (6.1)

If a² is not pure E2, purity already fails. Otherwise, write T=A R+B S and Y=T1. Exact noncommutative multiplication gives

    T2=Y a^-1 p a+B,
    T2 a^-1=Y a^-1 p+B a^-1.                        (6.2)

Because Y and T2 are pure E3, both their products by a^-1 have components only of rank at least two. Ordinary multiplication by p preserves this. Hence B a^-1 must also have components only of rank at least two.

If Q2 is a shear, B=mu is invertible ordinary, so B a^-1 is nonzero pure E1: contradiction. If Q2 is in-place, A=g lambda-C and B=g mu. Then

    Y a^-1=g lambda a-Ca+g mu.

The g lambda a term has support gHa, disjoint from both Ha and gH. The remaining two terms are pure E1. Absence of low-rank components forces g mu=Ca. Therefore B a^-1=C is ordinary and also supported in ranks at least two. It must vanish, contradicting invertibility of g mu. All four first/second query combinations are closed.

## 7. Complete fixed-three-head invoice

The admitted mixed-placement theorem reduces the only surviving S014 inventory to the same-side case just excluded. The admitted inventory exhaustion already excludes all other one-native, two-retained-role, three-head, common-seven-body query inventories for every 0<t<1.

For this final case put [r]=r^t and a0=[8]-[7], with 0<a0<1. Its price is P=4+[7]+[8]=4+2[7]+a0. Since independent (3,3) is impossible, endpoint total head rank H<=5. Concavity gives

    T=[7+h1]+[7+h2] <= 2[7]+5a0,
    P-T >=4(1-a0)>0.

Combined with the existing q<=2, q>=4 and larger-query-rank inequalities, EVERY query inventory in this fixed model fails even its optimistic complete movement price, including t=199/200. Ordinary, ownership, precision, compiler and recursive costs can only increase the deficit.

This is a scoped architecture obstruction, not a multiplication lower bound. The exact source, nonordinary seed and phase-faithful algebra remain valid components. All five foundational assumptions remain; no supplier or complete new kappa follows.

## 8. Fixed exceptional factors and limits

The proof also holds with fixed matrix coefficients Mat_D0(C) on each projective bulk group class. Direct support decompositions, ordinary bimodularity and coset disjointness remain. Source a and actual query g must be homogeneous bulk rank-one units with invertible finite-factor coefficients. Arbitrary ordinary role matrices over Mat_D0(C) tensor C[H] are allowed. Invertibility arguments use total physical block dimension.

This includes a fixed finite set of marked tensor columns under the inherited bulk-faithfulness extension. Width-growing exceptional sets, arbitrary per-column ordinary maps, nonhomogeneous sums of distinct nonordinary query units, and larger non-Clifford ordinary models are not included. A proposed escape needs its own source identity and physical invoice.

## 9. Verification and next question

This is a written universal proof within the stated algebra. Exact finite checks supplement the source identities, coset supports and singular-pivot controls; they are not an exhaustive caller search or the universal argument. Independent review is required before admission. DEPENDENCIES.json pins the source, tensor independence, inverse/mixed/placement gates, inventory exhaustion, marked extension and nonordinary seed at eefa411ebab86271d50b56b6953af3a157366bdb; canonical main is separately e54523517d0f03e58352e647c403a5af3e525a57.

**Open next question:** change the two-role single-native interface. Four heads with more queries or a second native on a changed role graph have distinct optimistic budgets, but require actual identities. The obstruction isolates what must change: a pure row from the first query and its untouched ordinary complement cannot supply the second high-rank independent job with one further query. General query lower bounds could avoid a succession of dimension-by-dimension searches.

Credit @CubeJerry, retained native/compiler and tensor-component authors, S013/S014 construction and review work, and S015 Worker B's coset-separation proof with substantial OpenAI assistance. No upstream PR, selected change or foundation discharge is claimed.
