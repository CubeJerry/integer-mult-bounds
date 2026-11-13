# Historical normalization with arbitrary cocharted Y feedback

**Proposed theorem for independent review.** This extends the admitted source-packet scattering interface. It removes purity of the packet/history values and excludes no original Y-to-X or Y-to-packet feedback. It does not build a complete source or admit a supplier. Every geometric route, actual historical coordinate, image constraint and physical cost remains part of the interface.

## 1. Exact model and quantifiers

Fix a field F, a whole-record width V>=1 and the actual111-root BIT chart geometry. All value operations are F-linear; arbitrary noncommuting V-by-V blocks are allowed. There are111 original X records whose physical paths ascend from their own root lines L_j to Hub, and111 original Y records ascending from0 to their distinct final facets F_i. There are q persistent packet lifetimes descending from Hub to0. No packet restarts, extra uncounted descending copies, nonmonotone path or cross-chart value swap is permitted. Track physical carriers through renaming, not only reusable owned labels.

At any chart, arbitrary actual cocharted X/Y/packet operations and their stationary histories are allowed, including Y information fed into X or packets, joint packet mixing, and singular packet-through maps. Every cache is initially zero and receives data only through actual local operations. Optionally, additional zero-born records may ascend from their actual birth charts; count each of their facet arrivals separately. They cannot be initialized with a nonlocal form for free. All original y inputs are independent, start at0, and no fresh nonzero input is introduced later.

The source is a finite chronological linear execution. Every moving record makes one contiguous visit to a given geometric chart because its path is monotone. Identify geometric aliases before forming cells. A packet's first arrival at0, before any ground mixing, is its boundary value Z_p. Its later local reads or legitimate final clearing do not replace Z_p by a different boundary. All q Z_p are actual historical values, possibly mixing x and y.

The endpoint consequence assumes Y_i^final=y_i+x_i for every i. Requiring final X_j=x_j only restricts the source further; it is not needed in the lower-bound proof. For target application, both endpoint families and every other source contract remain required.

## 2. The actual cell and its information coordinates

At every proper nonzero chart C aggregate all its chronological operations into one linear cell. Let U_in include every ascending boundary arrival (both original X and original Y, plus any additional ascending records), and every original input born there. Let P_in and P_out contain the same q_C visiting packet records on their arrival and departure, in a fixed consistent order. Any local history is linear in U_in and P_in. The packet equation is

    P_out = C_C U_in + D_C P_in.

This is an identity in independent formal boundary variables before substituting the actual interleaved arrivals. It is not a claim that those variables are simultaneously physically available. Local zero caches and local births do not introduce independent input variables.

Let nu_C=dim ker(D_C). Choose a complement W_C to ker(D_C), a right inverse on im(D_C), and an arbitrary complement to that image. These give maps R_C, J_C, h_C such that

    R_C D_C = I - J_C h_C,    D_C J_C = 0,
    h_C J_C = I,             h_C R_C = 0.

Here J_C embeds a chosen kernel basis and h_C extracts its coordinates along W_C. The ACTUAL historical kernel coordinate is T_C=h_C P_in. Then

    P_in = R_C(P_out-C_C U_in) + J_C T_C,
    (I-D_C R_C)(P_out-C_C U_in)=0.

The second equation is a retained image-compatibility condition; arbitrary putative G coordinates do not automatically satisfy it. Empty packet cells use the unique zero-dimensional maps. No invertibility assumption on the joint U/packet cell, or on any U block, is needed for this algebraic statement.

Define G to be the actual history vector containing all q first-ground values Z_p and all nonzero T_C at proper nonzero charts. These coordinates are algebraic information coordinates, not free physical reads, clean pure-X data or newly paid packet lifetimes.

## 3. Symbolic y terms are harmless to locality

Write x for all original X inputs and y for all original Y inputs. A normalized history at chart C has the form

    H_C = L_C G + E_C y + B_C x,

where the support of B_C is restricted to original X lines contained in C. Granting all original y symbols as nuisance terms is an algebraic relaxation only. No protocol is allowed to read y_j at a remote chart on this account. These symbols have ZERO x coefficient.

Prove this by induction on the finite visited chart poset from low dimension upward. At0 every history is generated from the actual first-arrival Z_p and the original y inputs, so B_0=0. A record born with zero value at a higher chart contributes no additional independent data.

At a proper C, every ascending arrival from a predecessor C'<C has already been normalized and has local x remainder supported inside C'. Original X inputs born at C have their source lines inside C; original y inputs are born only at0. Each descending packet's outgoing value is its incoming history at its next lower chart D<C, already normalized; if D=0, use its first-ground boundary. Insert these expressions into the actual inverse-cell identity. The T_C term is part of G. Substitution gives the stated normal form for P_in and hence every local history and ascending output. Left multiplication by block matrices changes coefficients but cannot create a new original-X column outside these supports.

Y feedback changes D_C, C_C, the G coordinates and nuisance coefficients E_C. It does not break this induction: original Y records are ascending boundary records and every Y dependence is handled in the same U_in expression. A history mixing x with unknown y is never silently declared pure X.

The rank of the x-coefficient projection G_x satisfies

    rank(G_x) <= qV + sum_C nu_C <= 8qV,

because a descending packet in this rank8 geometry visits at most seven proper nonzero dimensions. The last inequality counts actual physical visits and persists with interleaving, local mixing or reusable owned labels.

## 4. Refined locality at a terminal facet

Let r_i count original X paths visiting F_i, and a_i count separately paid additional ascending-record arrivals there. For each use its immediate proper predecessor chart. Let s_i count packet paths visiting F_i; for each use its first proper successor chart. Let C_i be the last proper chart of original Y_i before F_i.

No other original Y_j visits F_i: its ascending path ends at a distinct facet F_j of the same dimension, so F_i is not contained in F_j. No original X input is born at a facet. The refined cell induction puts the x-local remainder of every history at F_i in the UNION of at most

    1 + r_i + a_i + s_i

proper real subspaces of F_i: C_i and the listed predecessor/successor charts. A stationary record born at F_i is generated from those arrivals and adds none. A paid ascending copy born below F_i is handled by its own predecessor; copying Y information is not free additional access.

Write final Y_i=Lambda_i G+E_i y+B_i x. Taking ONLY the x coefficient in the endpoint identity gives

    e_i = Lambda_i G_x + B_i.

Thus A_i=Lambda_i G_x is a fitting: its own diagonal block is I and its noncontact blocks vanish, because the source line L_i is outside its own facet and every local B_i column comes from a source line inside F_i. On foreign contacts, A_i=-B_i. The y coefficient imposes additional actual-source equations Lambda_i G_y+E_i=e_i, which remain required but are not needed for this necessary fitting condition.

By the independently proved proper-subspace bound36 and two-subspace bound52, put

    ell_i(A)=1[foreign support(A_i)>36]+1[foreign support(A_i)>52].

Then ell_i(A)<=r_i+a_i+s_i. Summing, since each original ascending X and each descending packet visits at most one facet,

    sum_i ell_i(A) <= 111 + q + sum_i a_i.

This is the earlier physical arrival bound, now permitting arbitrary actual original-Y feedback and separately priced generated ascending copies. It still excludes extra descending copies/restarts, nonmonotone paths, nonlocal births and fractional-width carrier accounting.

## 5. Consequences for the retained target

For characteristic-two values the established fitting, rigidity, geometry and code theorems apply to A. In particular a complete source has rank(A)>=9V, so q8 cannot have every proper D_C invertible. This retains actual kernel/image obligations rather than granting an algebraic construction.

In the scalarF2 specified q8 unit invoice at movement test k in[.005,.005006], at most three extra facet arrivals can be paid at any finite fixed even multiplicity. The independently admitted binary-four quotient theorem is a statement about ALL fittings obeying that arrival budget. Its conclusion therefore applies to this Y-feedback model:

    dim_F2((row(A)+C)/C) >= 4.

The original theorem's declared no-Y-feedback scope is not rewritten. This proposition supplies a new normalization bridge into its already proved fitting/arrival inequality. A historical code containing C must consequently have dimension>=13; arbitrary rank(A)>=13 is still NOT asserted. General blocks have minrank9V, not the scalar binary quotient conclusion. Larger fields retain only independently established all-field direction inequalities as applicable.

Neither a favorable fitting nor G's algebraic rank proves physical availability. All222 endpoints, actual initial acquisitions, every image constraint, chronology, restoration, ordinary/owned/precision/compiler charges, both strict suppliers and all five foundations remain. If confirmed, adding cocharted Y feedback alone does not leave the normalized arrival obstruction. A successful source must supply the new actual historical code or legitimately change a stated route/record/price premise. Feedback remains a possible way to realize that noncanonical code; this theorem says it does not exempt the resulting fitting from the arrival conditions.

## Dependencies, checks and credit

Dependencies are the pinned actual BIT native geometry, independently admitted E7 proper/union bounds, source-packet cell normalization, all-V minrank9V, and separately admitted scalar binary-four fitting bound. Exact source/dependency hashes and finite algebraic controls accompany this proof. Controls test singular and nonsingular cells with independent Y nuisance coordinates and reject terminal-only or image-free substitutions; they do not replace the induction proof.

Credit @CubeJerry, retained source/cell/geometry/code authors, root's Y-nuisance extension, independent reviewers as separately recorded, and OpenAI assistance. No complete source or new kappa.
