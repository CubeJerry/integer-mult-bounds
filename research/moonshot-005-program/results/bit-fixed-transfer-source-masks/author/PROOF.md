# Exact source-mask completion for a fixed two-wave transfer

## 1. The fixed physical interface

Work over an arbitrary field F. Fix an actual downstream linear word, including its common H/D messages, K/F delivery, pure-phase inverses, owner paths and paid caches. Its source interface at one original donor is:

- b independent original source fields x;
- m designated genuine early source owners carrying Fx, where F is m by b and must have row rank m;
- l designated genuine late visits receiving the added parities Lx, where L is l by b and need not have independent rows.

If m<b, the other genuine early source owners complete F to an invertible b-by-b source map. The stated downstream coefficient on these completion owners must be zero. Otherwise include those owners in F and in the transfer below. Replacing actual unused originals by free zero inputs is not permitted.

For every chosen output bank, stack its actual field coordinates in one space Y=F^n. The fixed downstream word defines matrices C:Y<-F^m and D:Y<-F^l. The proper response of this donor is

    G = C F + D L.                                      (1)

These matrices are obtained from one common word. Separate per-receiver choices of C or D are not allowed. They incorporate the shared K constraints rather than granting a receiver-specific channel. All other donors have their own source matrices and transfer columns; because their original inputs are independent, equation (1) must hold separately for every donor.

The source variables F and L may change native source processing only. Every output coefficient that depends on the chosen source basis must be represented in C or D. Restoring X at Hub does not remove its already captured contribution to Y.

## 2. Exact constructive source criterion

Let B be a prescribed n-by-b proper target for this donor. Write im for column image and rank for matrix rank.

**Theorem 1.** There are F,L satisfying (1) with G=B and rank F=m if and only if

    m <= b,       im[B D] = im[C D].                   (2)

Equivalently, in the quotient Y/im D, the target B and the early transfer C have exactly the same column image. This is an equality of subspaces, not merely equality of their dimensions. No field extension is needed.

**Proof.** Let pi:Y->Y/im D be the quotient. If F has rank m, it is surjective onto F^m. Thus im(pi C F)=im(pi C), which proves necessity.

Conversely put Cbar=pi C, Bbar=pi B, and r=rank Cbar=rank Bbar. Choose r source-coordinate vectors whose Cbar images form a basis of im Cbar. Let J:F^r->F^m be their inclusion. Express Bbar=Cbar J T with T of row rank r. Choose N:F^(m-r)->F^m with image ker Cbar. The square matrix [J N] is invertible.

As m<=b, extend the r independent rows of T by m-r rows M to an independent m-row list. Set

    F = J T + N M.

Then F=[J N][T;M] has rank m and Cbar F=Bbar. Consequently every column of B-CF lies in im D. Solving D L=B-CF column by column gives L. This is a finite Gaussian-elimination construction, not a nonzero-polynomial existence assertion. It also covers m=0, r=0 and l=0. QED.

The m-r rows M are genuine independent source masks. They are functions of the same donor's original b fields. They do not add source dimensions. The construction cannot assign more independent early rows than b. Late rows can repeat or vanish; assigning independent masks to them without need may create unwanted output responses.

When there is no late freedom, the criterion is im B=im C. Thus a collection of individually feasible receiver equations can fail jointly. For example C=I_2 and B=[u;u] has every one-row equation feasible, but its joint target rank is one whereas C has rank two. Two independent early owners cannot realize it in that fixed transfer. Conversely C=[I I] and B=T of row rank r admit the source pair (T+M,M), with 2r independent early rows whenever T and M are independent and b>=2r.

## 3. A prescribed common output lift

The two-sided version is useful when sources share an intended output geometry. Let P:Y->Z be the selected receiver projection, and prescribe a common right inverse R:Z->Y with PR=I. Let each donor have a selected target T_j:F^b->Z. Requiring the entire proper contribution of donor j to equal R T_j is stronger than just P G_j=T_j and controls every actual output coordinate.

For fixed R, Theorem 1 gives the exact donor-by-donor criterion

    m_j<=b,    im[R T_j D_j]=im[C_j D_j].               (3)

The same R and actual C_j,D_j are used for every donor. If every T_j is surjective onto Z, this simplifies to

    im R + im D_j = im C_j + im D_j                    (4)

for every j. Thus the receiver-side lift and the source-side quotient masks can be designed separately and joined by exact subspace equalities. Once (3) holds, the native source maps are constructed by Gaussian elimination and the existing common downstream word already supplies the K/F causal delivery.

This criterion does not construct an arbitrary R or an arbitrary downstream word. The spaces C_j,D_j must come from the actual shared geometry; source and receiver labels alone do not determine them. A complete prescribed B, including a low-return target, can instead be used directly in (2). Then no unprescribed proper response is omitted.

## 4. Exact mask leakage with no compensating late freedom

Fix a full output transfer C_full and selected projection P. Put C_sel=P C_full. Suppose rank F=m and B_sel=C_sel F. Then

    rank((C_full F)|ker B_sel)
       = rank C_full - rank C_sel.                    (5)

Indeed F maps ker(C_sel F) surjectively onto ker C_sel. The left-hand image is therefore C_full(ker C_sel). Its dimension is rank C_full-rank C_sel because ker C_full is contained in ker C_sel.

Consequently independent masks in a full-rank source realization cancel at every actual output exactly when ker C_sel=ker C_full. Cancellation only in selected receiver rows does not imply this. If the kernels differ, the extra source modes in (5) appear elsewhere in the actual output. The statement concerns the source transfer, not the rank of I+B.

Late source freedom is handled by Theorem 1 in the full output space. Projecting away im D for the selected equations alone can hide leakage into unselected outputs. To claim full cancellation or a specific completed map, use the full C,D,B.

A useful special case has l source parities added at one late slice into distinct genuine Y owners, followed only by an invertible pure-Y word. Their full transfer D is injective. Any nonzero mask coefficient matrix V therefore has exactly rank V in the full output, even if selected receiver projections annihilate DV. Pure-Y permutations and shears cannot erase that source information. Further mask-dependent cross additions at other stages can change this conclusion and must be included in the full transfer.

## 5. Minimum full information rank with unrestricted late rows

For one donor, fix full C,D and a selected equation P G=B with rank B=v. Assume the selected version of (2) holds and m<=b. Put

    r0 = rank[C D] - rank D.

Then among all source choices satisfying the selected equation and rank F=m,

    min rank G = max(v,r0).                            (6)

This is a diagnostic for additional source information outside a selected projection. A small rank of G is not the multiplication objective: I+G can have large rank. Nor may (6) be applied to all donors as one freely mixing source; the native source maps are donor-specific.

**Proof.** Set W=im[C D], U={w in W:Pw in im B}. The selected criterion ensures U+im D=W: any w in W has Pw in im B+im(PD), so subtracting a suitable element of im D places it in U. Also P maps U onto im B. Thus on U the two maps to W/im D and im B are surjective, of dimensions r0 and v.

For any two surjective linear maps from a common vector space, a subspace of dimension the larger target dimension surjects onto both. Here is a basis proof valid over every field. Let their kernels be K1,K2 and assume dim K1<=dim K2. Decompose the common space as I direct-sum A direct-sum B0 direct-sum C0, where I=K1 intersect K2, K1=I+A and K2=I+B0. Pair a basis of A with equally many basis elements of B0 and take their sums; include the remaining B0 basis and a C0 basis. The resulting subspace is complementary to K1 and surjects modulo K2. Its dimension is the larger target dimension.

Apply this lemma to obtain S<=U, dim S=max(v,r0), with PS=im B and S+im D=W. Since dim S<=b, there is a surjective G:F^b->S satisfying PG=B: lift a basis of im B and map enough vectors of ker B onto ker(P|S). Then im[G D]=W, and Theorem 1 realizes G by full-rank early rows plus late parities. The reverse inequalities rank G>=v and rank G>=r0 follow respectively from PG=B and im[G D]=W. QED.

## 6. Source compiler and physical costs

These are algebraic choices for a fixed actual word. The retained source compiler still applies and every operation is charged. For F=GF(2^w), let B0=bw and L0=lw. Keep B0 stationary raw source records before changing X, implement the completed invertible source map, use raw snapshots to add the L0 late parities at their genuine visits, and invert the source map at Hub after downstream early inverses. The existing elimination bound gives

    ADD <= 2 B0^2 + B0 L0 + 7 B0,
    INIT = dirty CLEAR = B0, extra native peak = B0.

This is the previously proved source compiler bill, not a new lower price. More economical literal words may cache only needed parities. All downstream costs, closures, births, storage, actual field copies, canonical return and recursive calls remain additional. No new MOVE or free source read is introduced by the criterion itself.

## 7. Native overlapping-tile application and limits

The S027 D12/D99 construction provides a concrete shared H/K setting. The tiles share six original donors and four H planes. For a shared donor, each tile has an invertible four-by-four minor M_12 or M_99 to receiver80's selected early projection. Their combined source transfer is [M_12 M_99]. It has rank four, with four mask directions. Choosing four target rows u and four original mask rows v independent of u gives

    F=[M_12^-1(u+v); M_99^-1 v],

of rank eight. One joint native source basis therefore handles both tiles, including their shared H flags. The eight early packet values are independent at source; their common receiver sum is u.

The actual word uses transformed early X for Y only through its F80 snapshots, accumulated into the four intended F80 rows. Therefore its full early output transfer has the same kernel as the selected transfer. The masks cancel at every actual Y output, not only in a displayed projection. This conclusion requires inspecting the literal capture sites; it does not follow from tile arithmetic alone.

If the late target w is instead distributed as w+v and v through distinct native Y injection owners, selected F1 cancellation does not remove the masks from the complete output. Six independent four-row masks give rank24 of full unwanted mask response because the late injection transfer is injective. The late choice w and zero removes this unnecessary response without requiring a late independence condition. The exact word version and independent intervention checks are recorded separately; this theorem does not promote any unreviewed author word to a supplier.

Even with globally canceled early masks, the unmasked late source values have other actual responses. The small selected projections do not establish the full low-return target. In particular, no inequality here converts a mask response rank, a proper-map rank or a selected-row count into fitting excess h=rank(I+B)-9b. The complete target matrix and actual return need their own check.

The general result is proved by the displayed arguments. Finite exhaustive checks validate the subspace criterion, the source construction, simultaneous-receiver failure controls and the leakage/minimum-rank identities in their stated small domains. No foundational assumption, strict supplier, complete recurrence or new kappa is established.

Credit @CubeJerry, the balanced-source compiler and local transfer authors, and S027 Worker A's actual overlapping-tile construction. Worker B developed the exact causal quotient criterion, source-mask construction, full-output leakage analysis and two-sided lift formulation with substantial OpenAI assistance.
