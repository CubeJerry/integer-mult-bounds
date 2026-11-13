# Full minimum-rank block fitting rigidity for the native E8 support

Status: proved from the exact span certificates below; independent proof review pending. The hosted96 and full104 source sets are treated separately. Characteristic zero and every positive field volume. No symmetry, self-adjointness, positive-semidefinite or contact-invertibility hypothesis. No physical construction or new kappa.

Let N be either the96 hosted roots or all104 native first-X roots. Let G be their normalized Gram matrix, B=[5,56,69,100,65,77,96,103], and g_i=G[i,B]^T. Then G_BB=I8, g_i^Tg_i=1 and G_ij=g_i^Tg_j. Suppose K has V-by-V blocks over a characteristic-zero field F, for any V>=1, and satisfies

    K_ii=I_V;   K_ij=0 whenever G_ij=0;   rank_F(K)=8V.

The B identity minor makes8V the minimum possible rank. We prove that there are T_i in GL_V(F) with K_ij=G_ij T_i T_j^(-1). Thus every minimum-rank operator fitting is a block vertex gauge of Gram, including the previously open singular-contact case.

An actual replacement rail Q' must still pass its complete caller inequality <Q'paid-Rold,r^(199/200)><A_m, where A_m=129.9388553172829489...-31.5397783670854135.../(m-1). This classification grants no rank, packet, transport or physical price credit.

## Three exact source facts

Put S_i=g_i g_i^T in the36-dimensional symmetric matrix space Sym8(F).

1. The S_i span all Sym8. An explicit36-by36 integer minor is nonzero after scaling projectors by4.
2. Every native orthogonal8-frame f satisfies sum_(i in f) S_i=I8. Differences of frame incidence vectors have rank |N|-36:60 for hosted96,68 for full104. The respective frame counts are369 and759. Since the full relation space among the projectors has dimension |N|-36, these frame differences generate every projector relation.
3. The symmetric tensors S_i odot S_j for i=j or G_ij=0 span Sym^2(Sym8), dimension666. Each source certificate provides666 actual pairs and a nonzero666-by666 integer minor modulo65537.

A nonzero modular determinant certifies that the corresponding integer determinant is nonzero, hence proves the exact rational rank. All these ranks persist over every characteristic-zero extension field. No unchecked finite-characteristic conclusion is inferred.

Coordinates use E_pp and F_pq=E_pq+E_qp, p<q. Thus w_i=(4g_ip g_iq)_(p<=q) is integral. Tensor coordinates are w_ia*w_ja on a=b and w_ia*w_jb+w_ib*w_ja on a<b. The666-dimensional certificate therefore uses exactly the symmetric bilinear convention in the proof.

## Minimal fitting rank produces idempotents and frame relations

Set C=K[:,B], R=K[B,:]. The identity minor and rank8V give K=CR by the zero Schur complement. With block row C_i and block column R_i, C_i R_i=I_V. Define P_i=R_i C_i in Mat_(8V)(F). Each P_i is an idempotent of rankV. If G_ij=0, then C_i R_j=K_ij=0 and P_i P_j=P_j P_i=0.

For a native orthogonal8-frame f, stack C_i into square C_f and concatenate R_i into square R_f. Since C_f R_f=K_ff=I_(8V), the reverse product is also identity. Hence sum_(i in f) P_i=I_(8V). This argument uses no invertible contact block.

By source facts1-2 every relation among S_i is a linear combination of frame differences, and those differences also vanish on P_i. Thus there is a well-defined F-linear map

    Phi:Sym8(F)->Mat_(8V)(F),   Phi(S_i)=P_i.

Any one frame gives Phi(I8)=I_(8V). For b_p in B, factorization through the identity minor gives C_bp=e_p^T tensor I_V and R_bp=e_p tensor I_V. Therefore Phi(E_pp)=E_pp tensor I_V.

## Tensor spanning forces a Jordan homomorphism

Write X circle Y=(XY+YX)/2. The Jordan defect

    D(X,Y)=Phi(X) circle Phi(Y)-Phi(X circle Y)

is symmetric and bilinear. For i=j it vanishes because both S_i and P_i are idempotent. For native orthogonal i,j it vanishes because both original and image products vanish in both orders. Source fact3 says these test tensors span the whole symmetric-square domain. Therefore D=0 identically: Phi preserves the Jordan product. The image matrices need not commute.

## Matrix units make every B contact invertible

For p!=q put A_pq=Phi(F_pq). The Jordan relations E_rr circle F_pq=0 for r outside{p,q}, and E_pp circle F_pq=F_pq/2, force A_pq to have only its p,q and q,p blocks nonzero. This follows directly from the known standard block projections Phi(E_rr); in particular A_pq has zero diagonal blocks.

Expanding S_i in the matrix-unit basis now gives

    (P_i)_(p,p)=g_ip^2 I_V.

But P_i=R_i C_i, so the left side equals R_pi C_ip. If g_ip!=0, this product is invertible; both square factors are consequently invertible. This removes the hypothesis of the previously proved invertible-contact classification.

A direct completion of the gauge proof is also short. Write the offdiagonal blocks of A_pq as U_pq,U_qp. The identity F_pq^2=E_pp+E_qq gives U_pq U_qp=U_qp U_pq=I_V. For distinct p,q,r, F_pq circle F_qr=F_pr/2 gives U_pq U_qr=U_pr. Setting D_0=I_V and D_p=U_0p yields U_pq=D_p^(-1)D_q. With D=diag(D_p),

    Phi(X)=D^(-1)(X tensor I_V)D,  for every symmetric X.

Thus P_i=D^(-1)(S_i tensor I_V)D. Choose any allowed contact p and set T_i=g_ip^(-1)C_ip D_p^(-1). The p,p and p,q blocks of P_i imply

    C_iq=g_iq T_i D_q,
    R_qi=g_iq D_q^(-1)T_i^(-1).

The formulas include zero contacts. Multiplication gives K_ij=G_ij T_i T_j^(-1), as claimed. Conversely every such block gauge has the fitting zeros, identity diagonal and rank8V.

## Scope and consequence

This proves complete scalar and arbitrary-operator minimum-rank fitting rigidity on each separately certified native support, at every characteristic-zero volume. Whole-source block support, shortened-code dimensions and minimum block distance are invariant under the induced independent GL_V coordinate changes. In particular the proved hosted block-distance42 persists for all minimum-rank hosted fittings.

The gauges are algebraic, with all realization and tariff costs still owed. Higher rank such as9V, a changed earlier source, fragmented or mixed observations, or an interface not represented by this static fitting matrix remains outside scope. BIT characteristic two and other unchecked characteristics remain open. The timed-out Boolean/MILP searches are excluded from the proof and certificates.

Native gzip SHA2562b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883. The deterministic verifier reconstructs roots, source frames, relation and tensor witnesses without producer imports. NumPy is used only for bounded int64 modular arithmetic; every product is at most65536^2, so no overflow occurs. Run without Python -O; use the explicit source-set option for each certificate. All original-endpoint, supplier, compiler, precision, erasure and analytic foundations remain open.

Reproduction of the two separately certified source sets:

    python3 -I -B verify_spans.py --repo REPO --source-set hosted96 --output OUT/96
    python3 -I -B verify_spans.py --repo REPO --source-set full104 --output OUT/104
