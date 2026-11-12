# Exact raw-return dimension for retained chronological swap records

**A proved linear-information interface, with conditional local reconstruction. No source swap family, transport saving, supplier or new kappa is established.**

This theorem distinguishes the actual displaced values retained by swaps from independently supplied common records. In particular, the auxiliary common values Nu below are hidden: they are never granted to the decoder.

## 1. Exact chronological interface

Let F be any field. Let u in F^n be arbitrary common inputs and q in F^k be arbitrary independent installed signals, independent of u. Every admitted positive complete-field volume V is handled by tensoring the scalar maps below with I_V.

There are k chronological swaps. Immediately before swap i its distinct signal carrier still holds its original q_i. Its actual common helper value is

    h_i = H_i u + sum_(j<i) L_ij delta_j,

where H_i is the baseline common row and L_ij is the exact effect of earlier changes on this helper version. The swap makes the helper equal q_i and leaves its displaced value h_i in the signal carrier. Therefore

    delta_i = q_i-h_i,
    T delta = q-Hu,             T=I_k+L,              (1)

with L strictly lower triangular. In particular T is invertible over every field. The retained signal carriers hold the vector

    R = (h_1,...,h_k)^T = q-delta = Hu+L delta.        (2)

Each R_i must remain at this version until decoding; an erased temporary or a carrier later modified by another receiver operation is not that record.

The available common output data at the decoding location are

    Y = Wu+Z delta,                                  (3)

where W has independent rows. All entries of Y and R are actually available together at the declared decoding cut. This is an access premise, not a route construction. Other common endpoints and source guards must be checked separately.

Choose an auxiliary row matrix N such that [W;N] has independent rows and

    H = Lambda W + Gamma N.                          (4)

Such a choice exists by extending row(W) to include row(H). Nu is not supplied. It represents independent common uncertainty in the displaced values that the decoder cannot read through W. Additional independent auxiliary rows with zero contribution are harmless.

The decoder is additionally supplied real raw returns Aq, where A has r rows. Each row is a physically available combination of the original installed signals, not of a mutated carrier version. The required outputs are Wu and all k original signals q_i. Any other raw inputs or outputs remain caller obligations.

## 2. Observable difference combinations

Define

    B = Lambda Z-L.

Let K have rows forming a basis of the full left nullspace of Gamma, and put

    C = KB.                                         (5)

Substituting Wu=Y-Z delta into (2) gives

    R = Lambda Y-B delta+Gamma Nu.

Thus the actually observed Y,R determine

    C delta = K(Lambda Y-R).                         (6)

The hidden Nu cancels because KGamma=0. The actual raw returns also determine

    A delta = Aq-AR.                                (7)

No inversion of B, Gamma or an assumed terminal self-response is used.

## 3. Necessary and sufficient criterion

**Theorem.** Under the stated interface, Wu and all q_i can be recovered universally from (Y,R,Aq) if and only if

    rank([C;A])=k.                                  (8)

When (8) holds, a linear decoder exists. When it fails, even an arbitrary nonlinear decoder of these fixed linear observations is impossible.

For sufficiency, use a left inverse of [C;A] on the known values (6)-(7) to recover delta. Then

    Wu=Y-Z delta,        q=R+delta.                  (9)

For necessity, choose a nonzero t in ker C intersect ker A. Because K spans the full left annihilator of Gamma, KBt=0 implies Bt belongs to im Gamma. Choose eta satisfying

    Gamma eta=B t.                                  (10)

Independence of [W;N] makes its map onto its row-coordinate space surjective. Hence choose a common displacement v with

    Wv=-Zt,        Nv=eta,

and choose the installed-signal displacement dq=t. Equations (4) and (10) give

    dq-Hv = t+Lambda Zt-Gamma eta
           = t+Lambda Zt-(Lambda Z-L)t
           = (I_k+L)t = Tt.

By (1), the induced difference displacement is exactly t. Equations (2)-(3) then give dR=dq-t=0 and dY=Wv+Zt=0, while A dq=At=0. Every observation is unchanged, but the required raw vector changes by the nonzero t. This is an explicit indistinguishability pair. The positive sign in (10) is essential.

## 4. Sharp number of raw returns

Write c=rank(C). Each additional scalar linear return contributes at most one row of rank, so (8) requires at least k-c independent returns. Conversely, the standard coordinate rows span F^k. Select coordinate rows one at a time that increase the span of row(C), until it is all of F^k. Exactly k-c selected rows suffice. Taking these rows as A returns actual coordinates q_i and attains the lower bound. Therefore

    minimum scalar raw-return dimension = k-rank(C). (11)

Arbitrary linear mixtures of the q_i cannot reduce this dimension below what selected coordinate returns attain. They can nevertheless have different production, location, storage and transport costs. Equation (11) optimizes information dimension only; it does not minimize any of those costs.

For V scalar coordinates per complete field, the interface is tensored with I_V. Even if extra returns are allowed arbitrary linear mixing between field coordinates, the observation criterion is

    rank([C tensor I_V; A_V])=kV.

Thus at least (k-c)V independent scalar return coordinates are required, and k-c complete coordinate-field returns attain this dimension. A declared source model may admit fewer linear maps than this generous algebraic model; the upper bound still requires an admitted implementation. This conclusion does not assert a compression theorem for unrestricted nonlinear encoders of infinite sets.

## 5. Intrinsic form and the hidden common uncertainty

Because K has kernel im(Gamma), applying K identifies the quotient by im(Gamma). Consequently

    rank(KB)=rank([Gamma B])-rank(Gamma),              (12)

where [Gamma B] denotes horizontal concatenation. One way to see (12) is to map the column space im(Gamma)+im(B) through K. Its kernel is im(Gamma), and its image is im(KB). Rank-nullity gives the identity.

Equations (11)-(12) yield

    minimum returns = rank(Gamma)+k-rank([Gamma B])
                    >= rank(Gamma)
                     = rank([W;H])-rank(W).          (13)

The last equality follows because [W;N] has independent rows: quotienting row(H) by row(W) is exactly the row map represented by Gamma. Thus each independent component of the displaced common payloads outside row(W) creates unavoidable raw-return dimension in this interface. Further rank deficiency of [Gamma B] can require additional returns. The two terms in (13) are algebraic dimensions, not a statement that two separately priced physical costs add.

In particular, zero extra returns are possible if and only if every row of H belongs to row(W) and Lambda Z-L is invertible. This follows from (13) and, when Gamma=0, from row(K)=F^k and rank(C)=rank(B).

The criterion is independent of the chosen hidden complement N. Indeed, define intrinsically

    E = { a in F^(1 x k) : aH belongs to row(W) }.

The independence assumption implies E is the left nullspace of Gamma. Because W has independent rows, each a in E has a unique coefficient row ell(a) satisfying aH=ell(a)W. The observable difference row associated with a is

    ell(a)Z-aL.                                     (14)

The span of all rows (14) is exactly row(C). Neither E nor (14) refers to N. This also makes clear why Nu is not an extra observation: only combinations whose hidden common part cancels contribute.

## 6. Why the independence premise cannot be omitted

Suppose one were to use a dependent auxiliary matrix without adding its relations. Take k=n=1, W=N=[1], H=[1], Lambda=0, Gamma=[1], L=0 and Z=[1]. The actual equations are

    delta=q-u,       Y=u+delta=q,       R=u.

The supplied Y,R already reveal both required outputs. But the unqualified formula would give a zero-dimensional left nullspace of Gamma, C empty, and incorrectly demand one extra return. Here Nu is already the common target Wu, so it is not independent hidden uncertainty. Choosing the permitted representation H=W, with no N rows, gives C=[1] and correctly gives zero returns.

The theorem therefore uses an independent row complement. A dependent-row W lies outside the unchanged statement. A reformulation can choose an independent row basis for its common target, but must also retain the extra observed combinations of Y: these can contain pulse-only information. Dropping those observations can invalidate a claimed necessity bound for the original larger interface.

## 7. Conditional physical lowering

The theorem supplies a decoder once the stated records are physically available. Here is one conservative local implementation; it does not price acquisition or transport.

Assume Y and R are in distinct writable carriers at a common decoding chart, all real returns Aq are readable there at their promised versions, and the model admits the required scalar coefficients. Choose matrices J_C,J_A with

    J_C C+J_A A=I_k.

Equations (6)-(7) give

    delta=E_Y Y+E_R R+E_A(Aq),
    E_Y=J_C K Lambda,
    E_R=-(J_C K+J_A A),
    E_A=J_A.                                        (15)

Initialize k owned zero fields and form all k components of (15) before mutating any Y or R carrier. Direct scalar multiply-adds use at most

    nnz(E_Y)+nnz(E_R)+nnz(E_A)

ADD operations, where one permitted nonzero scalar multiply-add is counted as one ADD. Restore Y to Wu using at most nnz(Z) further ADDs, then restore every retained signal carrier with R_i += delta_i, using k further ADDs. The owned delta fields can now be cleared. This gives k INIT/CLEAR lifetimes and a finite exact local word, conditional on coefficient admission and field co-location. It is not a minimum temporary-storage theorem. A concrete source can reuse a returned cache as a difference field and use fewer lifetimes.

At an individual co-located swap, the reversible scalar word

    H += Q
    Q -= H
    H += Q
    Q *= -1

maps (H,Q)=(h,q) to (q,h), over any field. It uses three ADDs and one SCALE and introduces no MOVE at that chart. The chronology must still make Q the original q_i at that point and preserve its retained post-swap value until decoding. A coordinate return q_i can be copied from the helper while it truly holds q_i, or obtained by another admitted route; the existence of that copy, its lifetime and its paid or funded transport are additional source obligations.

All movement and storage of the retained R records, raw returns and delta work fields must be included in a source invoice. Equation (11) neither declares such movement free nor equates one independent return with one rank-one MOVE. Different chart intersections or path choices can give different costs for the same return dimension.

## 8. Basic cases and relation to other restoration interfaces

For one swap with L=0 and a displaced payload entirely in row(W), Gamma is empty and the criterion becomes C=Lambda Z. A nonzero scalar Lambda Z permits recovery without a new raw return; a zero value requires one. If that single displaced payload has a nonzero component outside row(W), Gamma has rank one and the criterion requires one raw return regardless of Z.

For several swaps, chronology enters with the minus sign in B=Lambda Z-L. A test that uses Lambda Z+L can falsely classify a family as requiring no returns. Likewise, treating the retained vector R as the supplied independent common vector Nu changes the information interface and can invalidate necessity. The two models must be kept separate:

- Independent common records Nu, when actually supplied, remove the corresponding common uncertainty directly.
- Retained swap records R=Hu+L delta contain both common uncertainty and earlier swap differences. Their useful difference information is exactly the row space in (14).

This theorem requires all original installed signals q as outputs. If only selected combinations Dq are required, the difference coordinates invisible in (6)-(7) need not all be recovered; equation (11) is then not generally the sharp count. If the installed helpers carry nonidentity combinations Qq, the retained record equation is likewise different and must be re-derived. The general retained-difference theorem covers another such interface, but it cannot be substituted for the present mixed-record equations without checking what is physically retained.

## 9. Proof status, controls and remaining source obligations

The argument in Sections 1-6 is over an arbitrary field, including finite characteristic. A rational or integer source word still has its own scalar-service, precision and admissibility requirements. The conservative local word in Section 7 is conditional on those requirements.

The independently authored checker in review/check_mixed_swap.py constructs observation and target matrices directly in the original independent variables (u,q). Its report review/RATIONAL-RESULT.json records 48 exact rational instances, every coordinate-return subset in those instances, additional arbitrary return matrices and 129 explicit indistinguishable input pairs. Directed cases reject the wrong sign of L, the wrong sign in (10), and omission of the row-independence premise. These are controls of the algebraic proposition, not a source certificate. The proof above, rather than finite testing, establishes the claim for every field and dimension.

A source application must authenticate its actual swap cuts, H, L, Z and W, all record versions and their locations, the remaining common endpoints, source COPY or CLEAR guards, required raw caller map, entry and exit recouplings, all owned lifetimes, coefficient services and complete costs. It must also prove that newly introduced receiver operations leave the retained R versions used here intact, or replace the interface by the actual changed records. None of those obligations follows just from rank([C;A])=k.

The mixed-record proposition was supplied by the root research worker and was independently algebraically reviewed and formalized by the review worker, with substantial OpenAI assistance. Its lineage includes the programme's difference-carrier, joint-restoration and retained-difference-record results. The root worker separately reviewed the complete formal argument and supplied exhaustive finite-field observation checks; see review/ROOT-REVIEW.md.
