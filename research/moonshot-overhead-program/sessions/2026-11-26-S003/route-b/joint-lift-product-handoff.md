# Final joint-delivery handoff: products with low-rank row mixers

Status: **accepted scoped final-wave lemma after independent C and lead review**. This tests a changed full-rate budget after SL: one m-row independent batch is reused through a product of joint lifted calls, without correlated-copy expansion or a linear pre/post sum. It covers low-rank row reflections used in a natural block-encoding/amplification attempt. It does not cover arbitrary full-rank row mixing or all joint star algorithms.

Use SL's actual star transpositions S_1,...,S_m, m>=2, on complete tuples of m+1 symbols. Assume the pair alphabet has at least m+1 values. Fix any free orbit of tuples with all entries distinct. Its data space has dimension M=(m+1)!, and the coordinate-permutation group acts by its regular representation there. Let

    S_b=sum_j b_j S_j, B=diag(S_1,...,S_m),

with real nonzero coefficients b_j. The desired full-rate map on this orbit is I_m tensor S_b. The joint B is the regular lift from SL; even its controlled rotations will be granted zero cost.

## 1. A fourth-moment rank witness

For any real weights a_j put A=sum_j a_j S_j and Q=sum_j a_j^2. On a regular orbit, the normalized trace of a group permutation is one for the identity and zero otherwise. A length-two star word is the identity only when its two letters agree. A length-four star word is the identity exactly in the patterns i,i,j,j or i,j,j,i, with the all-equal case counted twice. (The shortest noncancellation relation between distinct stars has length six.) Thus

    tr(A^2)=M Q,
    tr(A^4)=M(2Q^2-sum_j a_j^4)<=2M Q^2.              (LP1)

If Q>0, Cauchy--Schwarz on the nonzero eigenvalues gives rank(A)>=M/2. For A-cI, odd traces of A vanish by permutation parity, so

    tr((A-cI)^2)=M(Q+c^2),
    tr((A-cI)^4)<=3M(Q+c^2)^2.                        (LP2)

Consequently rank(A-cI)>=M/3 whenever Q+c^2>0. These claims hold for the actual finite permutation representation, not independent formal oracle variables.

The same moments give a quantitative approximation statement. At least M/12 eigenvalues of A-cI have magnitude at least sqrt((Q+c^2)/2); at least M/8 eigenvalues of A have magnitude at least sqrt(Q/2). Indeed, for a nonnegative random variable Y with mean q and second moment at most Cq^2, Cauchy--Schwarz on {Y>=q/2} gives probability at least 1/(4C). Apply this to squared eigenvalues.

## 2. Product algorithms with low-rank row changes

Fix an integer r>=1. Consider q joint B calls interleaved with scalar-row maps

    O=(A_q tensor I)B(A_(q-1) tensor I)...B(A_0 tensor I),
    A_t=c_t I_m+E_t, rank(E_t)<=r.                     (LP3)

The scalar-row matrices A_t,E_t and scalars c_t are real. They may be singular and the real scalars arbitrary. This is a full m-row product algorithm; it does not invoke SL5's sum-of-compressions assumption. Replacing every A_t by c_t I and telescoping gives

    rank(O-c B^q)<=M sum_t rank(E_t)<=M r(q+1),
    c=product_t c_t.                                  (LP4)

Because B^2=I, the target difference is block diagonal. For even q each block is S_b-cI, of rank at least M/3. For odd q, block j is S_b-cS_j, another nonzero weighted star sum because all other b_i are nonzero, of rank at least M/2. Hence exact equality O=I_m tensor S_b requires

    r(q+1)>=m/3,  q>=m/(3r)-1.                        (LP5)

The divided q bound assumes r>0. If r=0, the undivided inequality rules out exact realization. This remains meaningful when some c_t=0. If r=0, the undivided rank inequality makes exact realization impossible. It does not count row arithmetic as a paid spatial query; it bounds the number of B calls under the explicit per-interval rank-r mixer restriction.

For numerical approximation put b_min=min_j |b_j|>0. Every block has at least M/12 singular values at least

    tau=b_min sqrt((m-1)/2).

If ||O-I_m tensor S_b||_op<tau, LP4 still requires

    r(q+1)>=m/12.                                      (LP6)

To see this, intersect the high-singular-value subspace of the target-minus-baseline with the kernel of O-minus-baseline. If the latter map had smaller rank, a nonzero intersection vector would have error at least tau. Thus small numerical error does not bypass this particular low-rank mixer obstruction.

The same bounds hold for the actual row-dependent diagonal target diag_r(sum_j b_(r,j)S_j), if every real coefficient is nonzero: apply the blockwise argument with b_min=min_(r,j)|b_(r,j)|. For odd q, cancellation changes only one coefficient in each block and leaves m-1 nonzero terms. This extension does not permit arbitrary dense row targets.

## 3. Complete optimistic invoice and portfolio decision

A B call applies the same central/leaf transposition to all m independent row fibres. Its queried volume equals the original batch volume. For fixed r, LP5 or LP6 therefore forces Omega(m) normalized width-f query mass, even when both controlled rotations and every scalar row operation are granted zero cost. The actual T consists of two width-f exchanges in the original separated-half layout. Such a supplier cannot replace SN's m factor by a subpower one. Its regular-split positive majorant is again B(e)>=c m B(f), hence e/poly(log e) on the adaptive logarithmic-width path.

This rejects the low-rank reflection/amplification variant of the joint regular lift. It is distinct from SL's sum-of-compressions restriction, but still not a theorem about arbitrary products: full-rank scalar mixing between joint calls is explicitly outside LP3. Accumulating m rank-one mixers before one call also falls outside a fixed-r per-interval budget and is not excluded by this statement.

**Final protected-route decision.** Stop the tested common-isotropic, separate-query, scalar-compressed lift and fixed-r reflection mechanisms. The concrete open supplier remains a direct weighted-star executor on all independent physical data, with all regrouping charged. A plausible future acceptance test must either price a full-rank mixed product with o(m) joint calls or give a direct orbit transform at subpower-m times J(a), without hiding an address-sort or independent-row loss. No such executor is claimed in this session.

The fourth-moment proof is symbolic. `verify_joint_lift_moments.py` independently enumerates short words in actual star permutations, including weighted and scalar-shift cases, and checks the exact moment inequalities. This is a finite algebraic diagnostic, not a tape runtime lower bound. Prepared for Jerry Chen (@CubeJerry), with substantial OpenAI AI assistance.
