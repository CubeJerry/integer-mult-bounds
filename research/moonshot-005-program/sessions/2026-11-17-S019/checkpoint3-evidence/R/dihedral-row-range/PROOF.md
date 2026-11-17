# A nonregular dihedral row-range obstruction at all sufficiently large even widths

**Proved mathematical range theorem, applied to the retained literal source; independent review pending. No complete supplier or new κ.**

The S019 active-swap gate used a regular D8 character to obtain a row range of dimension 3D/4. Regularity is unnecessary. The exact defect below also excludes the unphased active swap, whose width-one row range has full dimension D. The theorem is restricted to the stated ordinary forward-conjugate and finite-catalogue hypotheses; the spectator swap remains outside them.

## 1. General range theorem

Let H be a complex Hilbert space of dimension d>=2. Let f,t be unitary involutions, and assume z=(ft)^2 satisfies z^2=I and is central in the group they generate. These relations hold whenever (ft)^4=I. Assume t is not scalar. For every positive integer V define collective operators f_V=f^(tensor V), t_V=t^(tensor V), z_V=z^(tensor V), dimension D=d^V, and

    P=(I+f_V)/2, M=I-P, T=(I+t_V)/2,
    Zplus=(I+z_V)/2, Zminus=I-Zplus.

Then the orthogonal range projectors of PT and MT are

    Rplus =P(Zminus+Zplus T),
    Rminus=M(Zminus+Zplus T).                        (1)

Their combined rank is exactly

    rank(Rplus)+rank(Rminus)=D-delta_V,
    delta_V=(d^V+tr(z)^V-tr(t)^V-tr(zt)^V)/4.         (2)

In particular, for every positive even V,

    delta_V >= [d^V-2(d-2)^V]/4.                    (3)

Thus delta_V>0 for all sufficiently large even V. At d=16 the uniform bound is already positive for every even V>=6. No regular representation or zero-trace condition is required.

**Proof.** The relation ft=tfz gives commutation on Zplus and anticommutation on Zminus. On the first sector PT and MT are commuting products of orthogonal projectors. On the second sector PTP=P/2 and MTM=M/2; hence PT maps onto P and MT maps onto M. Exact witnesses for both range inclusions are

    Rplus PT=PT,   PT(2 Zminus P+Zplus)=Rplus,
    Rminus MT=MT,  MT(2 Zminus M+Zplus)=Rminus.

This proves (1). The two projectors have orthogonal ranges, and

    Rplus+Rminus=Zminus+Zplus T=I-Zplus(I-T).

The missing projector Zplus(I-T) has trace (2), since the trace of a tensor power is the corresponding power of the one-column trace.

Every unitary involution is self-adjoint with eigenvalues ±1. Since t is nonscalar, |tr(t)|<=d-2. The involution zt is nonscalar too: if zt=λI, then λ=±1 and t=λz is central, so f and t commute. This forces z=(ft)^2=I, and then t is scalar, a contradiction. Therefore |tr(zt)|<=d-2. For even V the real number tr(z)^V is nonnegative, giving (3). For d=16,V=6, the numerator 16^6-2*14^6=1,718,144 is positive; monotonicity of (14/16)^V establishes all larger even V. This is a dimension theorem for collective powers, not tensor powers of a one-column range projector. ∎

The scalar condition is necessary: t=I or t=-I gives T=I at even widths and delta_V=0. Width-one full range is also compatible with (2) and must not be extrapolated to unbounded widths.

## 2. Source-bound ordinary endpoint exclusion

Use the retained four-bit source a=A^(tensor V), d=16, F=Z_a, and the retained ordinary involution J commuting with F. Let t be a fixed nonscalar root-four monomial involution such that (Ft)^4=I. Suppose the literal conjugates

    A t A^-1,   A J t J A^-1                       (4)

are root-four monomials. The already pinned source also satisfies A F A^-1=Z_d. Let C,Q and all endpoint interfaces be ordinary units in one fixed finite tensor-word catalogue, with their actual inverses included. Consider either first-column orientation

    (C00,C10)=(P T,J M T),  or  (M T,J P T),        (5)

with arbitrary C20 and arbitrary remaining entries of C,Q.

Then the three-native word E=L C U Q L cannot have independent Gaussian (4,2,1) endpoints uniformly at unbounded widths in this interface.

**Proof.** The ordinary block idempotent

    R=diag(a Rplus a^-1, a J Rminus J a^-1, 0)

fixes the source column K=(a C00 a,a C10 a,0)^T for the first orientation. Exchange plus and minus for the second. Its entries are ordinary because (1) is a finite group-algebra expression in F,t, and (4), together with the pinned F conjugate, transports its generators to literal ordinary monomials. It has rank D-delta_V<D for all sufficiently large even widths by (2)-(3).

Only the four-source term -K a [q10 a,q11 a,0] can contain Gaussian class four; all other terms in E have at most three source factors and one-column support at most eight. At sufficiently large faithful widths, ordinary multiplication commutes with exact Gaussian-class extraction in the retained fixed finite catalogue. Therefore R fixes the entire rank-four component E4. Independent endpoints would force rank(E4)=D, preserved by their ordinary invertible encoders and decoders. But rank(E4)<=rank(R)<D, a contradiction. Choose arbitrarily large widths divisible by four if the catalogue's phase convention requires that subsequence. The argument needs no purity or injectivity of K. ∎

This extends the regular-character result without enlarging the allowed ordinary algebra, waiving an inverse, or supplying a free physical projector. Source-dependent or growing catalogues outside the retained separation theorem are not covered.

## 3. Exact unphased active-swap application

Take t=SWAP_ab with no Z_c factor. The literal pair F,t generates eight distinct D8 matrices. In the one-column dimension16 representation, the identity trace is16, tr(t)=tr(zt)=8, and all other nonidentity traces vanish. Both forward conjugates in (4) are literal root-four monomials. Equation (1) gives

    rank(Rplus)=rank(Rminus)=3*16^V/8+8^V/4,
    rank(R)=3*16^V/4+8^V/2.                         (6)

At V=1 the individual ranks are8 and8, and rank(R)=16=D. At V=2 they are112 and112, and rank(R)=224<256. For every V>=2 the defect is

    delta_V=(16^V-2*8^V)/4>0.

Hence both unphased active-swap orientations are excluded by the all-width ordinary row-range gate. The earlier finite negative control deleting Z_c remains exactly correct at width one; it does not establish an all-width escape. No earlier frozen evidence is changed.

The phase-balanced t=SWAP_ab Z_c case has all seven nonidentity traces zero and recovers the earlier 3D/4 formula. The spectator t=SWAP_cd has nonmonomial forward conjugates; its previously verified kernel bridge is not excluded by this theorem.

## 4. Verification and scope

The checker verifies all projector and range identities in the abstract rational group algebra of D8, including noncommuting multiplication. It separately reconstructs the pinned literal four-bit source, both actual active swaps, every exact group trace and both forward conjugates. It checks collective trace/rank formulas and the sharp V=1/V=2 contrast, scalar controls, the spectator conjugacy failure and the uniform positive bound. These finite computations authenticate the source and algebra; (1)-(3) prove the quantified width statement.

Credit @CubeJerry, B's S019 row-range theorem, C's independent D8 review and its unphased width-one control, the retained literal source, and root's nonregular-character extension. Prepared with substantial OpenAI assistance. Both strict suppliers, full recursive accounting and all five foundations remain. **No new κ.**
