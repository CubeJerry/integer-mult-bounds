# Joint endpoint rank under actual Y2 input coding

**Proved algebraic identity and exact source corroboration. No new κ.**
This companion reviews the global-code worker's `pivot-piggyback/PROOF.md`
for @CubeJerry, with OpenAI assistance. It emits no new physical word.

## General theorem

Over any field, let the current map on independent b,d be (b+R d,d), with
desired endpoints (b−d,d), and M=I+R. Encode the actual input d as P d.
If a genuinely supplied baseline Kd is subtracted from the b outputs, the
joint endpoint error matrix is

    E(P,K)=[I+R P−K; P−I].

Subtracting R times the second block from the first gives

    rank E(P,K)=rank[M−K;P−I].

For a matrix Q of rank r and kernel-basis matrix Z,

    rank[Q;D]=r+rank(DZ),

because its kernel is exactly {Zz:DZz=0}. Hence

    rank E(P,K)=rank(M−K)+rank((P−I)Z_K).              (1)

No invertibility of P is needed for this identity. A physical proposal with
singular P must separately preserve lost information. The formula holds
for arbitrary block matrices; scalar maps tensored with identity of volume
V have all ranks multiplied by V. Uniform implementation remains separate.

With K=0, initial Y2 coding alone cannot lower joint rank below rank M.
With a supplied baseline, its actual K and cost must be retained. Every
subsequent old read uses P d, not stale d. Omitting original-Y2 restoration
or silently changing K is invalid.

## Exact rank-88 source

The frozen native source has compressed SHA256
`2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883`.
The actual two-frame word has compressed SHA256
`3d7ada763346a5658ef481f84bf895b668005a558e999be431d2257e16fbd101`.
Use its 96 hosted ports only, Gram matrix G=AᵀA/8, and orthogonal frames
B=[5,56,65,69,77,96,100,103], S=[0,7,20,27,36,46,57,111].

In B,U=H\B order, let L=G_UB and C=G_BS. Exact current rows give
M=[[I,C E_Sᵀ],[L,I]], with kernel Z_B=−C, Z_U=LC=G_US and Z_S=I.
Systematic B coding puts G_BH d into raw d_B, so P=[[I,Lᵀ],[0,I]]. Then
(P−I)Z=[LᵀLC;0]. Since the S rows of L form Cᵀ, LᵀL is identity plus a
real positive-semidefinite matrix. It is nonsingular. Thus, without a
delivered baseline,

    rank E(P,0)=96.                                    (2)

The rational rank claim extends to every characteristic-zero field.

## A delivered Gram baseline and every systematic pivot basis

For K=G, the two-frame source has ker(M−G)=span{e_b:b∈B}. In B,S,V order,
V=H\(B∪S), write L0=G_VB. Then

    M−G=[[0,0,−L0ᵀ],[0,0,−CᵀL0ᵀ],[0,−L0 C,I−L0L0ᵀ]].

Its kernel equations imply L0ᵀx_V=0 and x_V=L0 Cx_S. The 80 V roots span
dimension eight; a source basis is recorded in the certificate. Thus
L0ᵀL0 is nonsingular, forcing x_S=x_V=0. B coordinates are free, so
rank(M−G)=88. For the older paired-eight source, M−G is
[[0,−Lᵀ],[0,I−LLᵀ]] in B,U order, and its two equations immediately give
x_U=0. This removes the earlier note's convenient extra root-moment and
I−G invertibility premise.

Choose any eight hosted pivots I whose root columns form a basis, and put
C_I=A_I⁻¹A and P_I=I+E_I(C_I−E_Iᵀ). The systematic pivot map is invertible:
its I-by-I block is identity and every nonpivot coordinate is unchanged.
In (P_I−I)E_B, columns B∩I vanish. The remaining columns are a subset of
the independent columns of A_I⁻¹A_B. Formula (1) therefore proves

    rank E(P_I,G)=96−|B∩I|.                            (3)

I=B preserves joint rank 88 after the baseline is supplied; disjoint pivots
give rank 96. No pivot choice improves the current joint rank in this
interface. Reorienting its kernel or exposing a new useful observation
may still enable later work; the rank identity does not rule that out.

For I=B, 352 off-pivot encoder coefficients, eight copy ADDs and 360 hub
baseline terms give the note's 720 proposed ADDs. The eight facet-to-hub
copies require eight new owned rank-1 calls and actual lifetimes. Those
operations and the original Y2 debts must all remain charged. This package
does not emit or admit that proposed word.

## Verification, provenance and limitations

The accompanying checker extracts the actual R from all 1,880 input
coordinates of the frozen word, checks both kernel interfaces, exhibits
an eight-root basis outside B∪S, and corroborates systematic bases with
all overlaps 0 through 8. The proofs establish the universal statements;
finite tests alone do not. The unchanged-raw/fresh-packet obstruction is
not applied to these changed input rows.

The earlier note's scoped observation claim is also sound: a coordinate
space on at most eight positions intersects the Gram row space trivially,
because every nonzero hosted Gram row has support at least 42 by the
separately reviewed distance theorem. A sole masked companion carrying an
independent nuisance input cannot supply a pure d observation without an
additional observation that cancels that input. These are restrictions
on stated observations, not universal physical impossibility results.

No global cost lower bound follows from endpoint rank alone. Mixed current
rows, actual common history, funded transport, new b-side shears, or a
different output interface can change the hypotheses. All five foundations,
the complete complex/BIT suppliers, precision, erasure and uniform recursive
costs remain. No new complete κ is established.
