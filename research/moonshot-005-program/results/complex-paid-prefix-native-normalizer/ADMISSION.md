# Compile a fixed source prefix with an arbitrary restored borrowed bank

**Proved local ordinary primitive compiler and all-width native normalization.**
For a distinguished bit take P=lambda E_uv, Q=P_v, u!=v. Then PQ=P, QP=0
and the exact four-shear identity is

    E01(P) E10(Q) E01(-P) E10(-Q)=diag(I+lambda E_uv,I).

Each coefficient has a two-monomial expansion in I,X,Z,ZX. Restoring its
temporary source after each term gives8 ADD,16 SCALE,12 MONO per elementary
within-bank update. The borrowed bank begins arbitrary and is restored as an
identity block. All scalars and reciprocals used are nonzero Gaussian dyadics.

For the literal source A=C_b R, three such updates and the two ordinary
prefix monomials R,D_b implement p=A tensor I_tail. Specifically,
C_b=U01(-1) U10((1-i)/2) U01(-i) D_b. Both p and p^-1 cost
24 ADD,48 SCALE,38 MONO, with exact uniform primitive-prefix bound3. No Gaussian
call, owner or dirty erasure is introduced. This is an actual implementation
of one nonmonomial prefix, not an assumption that arbitrary prefix matrices
are free. The first-column address rules are fixed before tensor width varies.

Write a=p*b=b*p, b=I_prefix tensor A_tail. The same paid controls normalize
both natives:

    diag(p^-1,I) L(a) diag(I,p^-1)=L(b),
    diag(p^-1,I) U(a) diag(I,p^-1)=U(b).

Each prefix control can borrow the third arbitrary bank and restore it. Three
normalized native calls add144 ADD,288 SCALE,228 MONO, without claiming any
adjacent-control savings. Reattaching actual target prefixes is separately
charged: a tail rank-r head has rank r(V-1), not the required rV.

[Author proof and words](../../sessions/2026-11-17-S020/checkpoint5-evidence/B/distinguished-prefix-native-normalizer/PROOF.md)
and root's [independent sparse exact review](../../sessions/2026-11-17-S020/checkpoint5-evidence/R/prefix-normalizer-review/REVIEW.md)
reconstruct every monomial, primitive prefix and borrowed-bank column, prove
the commutator and tensor identities, reject all48 ADD omissions, and verify
both native types at widths one/two with missing-control negatives. The
all-width proof comes from the fixed-prefix matrix tensored with an identity.

This resolves the local primitive implementation obligation for these prefix
normalizers. The full physical compiler foundation, whole caller precision,
source layout, recursion, target restoration and actual independent endpoints
remain open. Credit @CubeJerry, source/primitive and distinguished-prefix
predecessors, B and root with C arithmetic; OpenAI assistance. No new complete κ. The selected conditional bound remains .00363005817. Both strict suppliers, the outer assembly and all five foundations remain open. The branch is ongoing research and is not PR-ready.
