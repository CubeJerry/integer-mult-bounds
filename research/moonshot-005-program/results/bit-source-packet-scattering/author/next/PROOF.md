# Singular cells: historical-mode normalization and exact constraints

This continues the frozen invertible-through theorem in the parent directory. All cell/path/cache/no-Y-feedback hypotheses there remain. Through blocks may now be singular. Values are V-vectors over a field; noncommuting block coefficients are allowed. Kernels, ranks and complements refer to ordinary finite-dimensional linear maps over that field.

## Exact local parameterization

At a nonzero proper chart C, put m_C=q_C V, D=D_C, and nu_C=dim ker(D). Choose a complement S of ker(D) in its domain and a complement T of image(D) in its codomain. Define R as the inverse of D:S->image(D), extended by zero on T. Let J be a basis injection of ker(D), and h the coordinate projection onto that kernel along S. Then

    R D=I-Jh,   D J=0,   hJ=I,   hR=0,

and DR is the projection onto image(D). For actual cell values let W=P_out-C_C X_in and define the actual historical mode T_C=h P_in. The cell equation gives W=D P_in, so

    P_in=R W+J T_C.

The compatibility equation is retained:

    (I-D R) W=0.

Conversely, if this compatibility equation holds, any Xin,Pout,T_C determine Pin by the displayed formula, and then D Pin=W and h Pin=T_C. Thus this is an exact parameterization of the local linear constraint, not a grant of arbitrary independently realizable observations. The formulas for other outputs/histories are

    X_out=(A_C-B_C R C_C)X_in+B_C R P_out+B_C J T_C,
    H=(E-F R C_C)X_in+F R P_out+F J T_C.

Their ordered products are valid without commuting block maps. Empty packet cells have nu_C=0 and need no mode.

## Ground boundary and all-history theorem

For the sharp count below, define Z0 to be the q packet values at FIRST ARRIVAL at the zero chart, one whole-V value per persistent packet path. These are actual values at possibly different times. All source inputs start at positive-dimensional lines, all X paths ascend, caches start zero, and no Y feeds back. Consequently every X/packet/cache history at zero is a linear function of Z0. No inverse zero-cell through map is required.

If instead one insists on arbitrary later pre-CLEAR terminal payloads, the zero-cell through block may be singular: a cache can retain an old packet and an ADD can cancel that packet before its final clearing. One must then include nu_0 or assume the zero-cell through map invertible. First-arrival Z0 avoids this ambiguity without changing the physical word.

Let G concatenate Z0 and T_C for every visited NONZERO proper chart. These are all actual linear functions of original x; they are not presumed independent. Run the earlier low-to-high chart induction with G as global coordinates. At a chart C, X arrivals from lower charts have normalized remainders inside their predecessor charts; a source born at C is local there; packet departures equal the incoming packet at its next lower chart, already normalized. Add the local T_C term using the exact parameterization above. Every history has form

    H_C=M_C G+N_C x,

with N_C zero outside input lines contained in C. The whole global rank is bounded by

    rank(G)<=qV+sum_C nu_C.

This is an algebraic upper bound on actual historical information; none of its coordinates is physically made available at a new chart.

## Complete-endpoint fitting and finite rank target

Normalize public-Y reads and propagate their global and local parts separately. Public-Y cochart mixing and ascending motion preserve the local remainder property. At each final F_i the remainder B_i has zero own and noncontact columns. Thus complete Y_final=y+x implies an ACTUAL fitting

    A+B=I,    A=Lambda G,
    rank(A)<=rank(G)<=qV+sum_C nu_C.

Every cell image-compatibility equation, the actual Hub acquisition equations, all chronological operation dependencies, and all endpoint restoration equations remain constraints on this factorization. This upper bound does not realize an arbitrary fitting of that rank, and no historical coordinate receives arbitrary price credit. They are earlier subspaces carried by already counted records at actual times, with all movements, lifetimes and erasures still owed.

In ambient dimension eight, each descending packet path visits at most seven distinct nonzero proper charts, one at each dimension1..7. At a cell, nu_C<=q_C V. Summing visits gives

    sum_C nu_C<=V sum_C q_C<=7qV,
    rank(A)<=8qV.

This count does not require unit descents: a jump skips intermediate dimensions. It requires finite monotone paths, no route restarts, and the first-arrival zero boundary just defined. For q=9, rank(A)<=72V. The admitted characteristic-two actual-BIT minrank theorem supplies the necessary lower bound9V. For q=1 and eight completed coordinate-frame targets, seven scalar nullities plus one ground value allow rank eight; the independently proposed root bus is a concrete candidate saturating this information count, pending its separate literal-word review.

## Stronger scalar consequence from refined support

The facet support refinement also persists with singular cells. After all G terms are separated, every history at F_i has local remainder in the union of its r_i X predecessor charts and s_i packet successor charts. The new T_C term contributes to the global part, with zero local remainder. Including Y_i's last proper chart gives the same union of1+r_i+s_i proper subspaces.

For 111 X paths and nine packet paths, an A with canonical foreign support would therefore force r_i+s_i>=2 for all111 roles by the independent E7 52-root theorem, contradicting total visits<=120. Hence the actual normal-form fitting A CANNOT have canonical foreign support, for any choices of generalized inverses and complements.

For SCALAR values over any characteristic-two field, admitted global rank-nine rigidity then gives rank(A)>=10. Its historical global span also has rank>=10. This is a necessary new fitting-space obligation for a completed nine-packet monotone-feedback construction. It does not mean ten packet fields, ten new moves, or ten separately paid returns: nine mutable records can carry more than nine independent historical modes.

For arbitrary V, the exact alternative is: either rank(A)>9V, or A is a minimal-rank fitting in the still-open noncommuting singular-Schur stratum. Scalar operations replicated across V give the scalar lower bound10V, but no general all-V10V theorem follows. A source starting with the canonical nine-dimensional code can still acquire extra historical modes through singular exchanges; its initial code dimension alone does not pin the final normal-form fitting rank.

All claims concern the declared monotone path families with generated caches and no Y feedback/copies. They do not cover extra nonlocal sources, restarted packets, fractional-volume counting, or complete compiler/supplier obligations. No new kappa follows.

An immediate all-V corollary is that ONE persistent descending packet cannot complete all111 Y targets in this interface: its global fitting rank is at most8V, below the admitted9V minimum. This uses no fitting-rigidity stratum. For general q, completion requires qV+sum nu_C>=9V, hence q>=2. This is only a necessary information count. In particular the earlier fresh-nine-field minimum is not a universal nine-persistent-packet requirement after mode exchange; historical modes must be counted. Two through eight mutable packet paths remain open here, with their actual source restoration and price obligations intact.
