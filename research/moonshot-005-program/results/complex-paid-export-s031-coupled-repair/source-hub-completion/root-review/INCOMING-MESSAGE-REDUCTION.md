# Incoming-message elimination and rank-one stock repair

**Accepted conditional refinement after [independent review](../review-b-incoming-message-reduction.md).**
Fix the completion theorem's surrounding causal linear circuit, including
the second paid route, and assume rank(C)=909. Vary only chart27's incoming
field ell y and its physical chart3 export multiplier w. The row ell is
supported on chart27's two original inputs. Put z=F inverse w. If N is the
surrounding response with that contribution zero, linearity gives

    M = N + C z ell.

This is not asserted for new feedback or nonlinear surrounding functions.

## The pinned gate is independent of the incoming message

For each of376 pinned outside coordinates, subtracting C z ell R_ya[:,j]
does not change membership of [e_j;0]-M R_ya[:,j] in col(C). Thus condition2
depends only on C,N. No incoming-message or source3 coefficient change can
repair a failed pinned membership with the surrounding circuit fixed.

If all memberships pass, let d_j be the unique baseline preimage and put
d_j/r_j in column i(j) of U_N, with free columns zero. Define

    alpha[i(j)] = ell R_ya[:,j]/r_j; alpha[free]=0.

Then the exact pinned source matrix is U_0(M)=U_N-z alpha.

## Outside-output and stock rank gates

Condition1 requires

    Delta = E_ay-N_a = (C_a z) ell.

Delta must vanish outside chart27's two input columns, have rank at most1,
and have column space in col(C_a). If its rank is1, its row space determines
ell up to nonzero scaling. These are necessary, not sufficient, conditions.

Write C_z,N_z for the stock row blocks; the lowercase column z is the
control vector. Define

    S_N = C_z U_N R_xb + N_z R_yb,
    beta = ell R_yb-alpha R_xb.

Substitution gives S_0(M)=S_N+(C_z z) beta. Every free singleton b column
has zero R_yb and zero pinned R_xb entries, so beta vanishes on all532 free
stock columns. On the370 fixed columns this becomes

    L(M) = L_N+(C_z z) beta_fixed.

It is a rank-at-most-one update. W=C_z ker(C_a) remains unchanged. Therefore
any successful completion necessarily satisfies

    rank(L_N) >= 369,
    dim(span(columns(L_N),W)) >= 901.

One incoming field raises either rank by at most1; the full completion
criterion requires370 and902 respectively. Conditions3 and4 still need
their complete exact checks. Changing surrounding forms changes C,N and
these gates; no endpoint pair is universally excluded here. Numerical
residuals or tolerance ranks do not certify these conditions.

Credit @CubeJerry, the retained rational source, Worker B's completion
theorem and root's refinement. OpenAI assisted. No repaired circuit,
supplier, price improvement or new complete kappa is established.
